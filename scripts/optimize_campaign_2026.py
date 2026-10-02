"""Optimize 2026 MP4 videos and create lightweight covers without changing originals."""

import hashlib
import json
import subprocess
from pathlib import Path

from optimize_videos import ROOT, optimize

OUTPUT = ROOT / "botox-rosa/assets/optimized/2026"
REPORT = ROOT / "scripts/campaign-2026-media.json"


if __name__ == "__main__":
    previous = json.loads(REPORT.read_text()) if REPORT.exists() else []
    results = []
    sources = sorted(file for file in (ROOT / "botox-rosa/assets/2026/videos").glob("*")
                     if file.is_file() and not file.is_symlink() and not file.name.startswith(".")
                     and file.suffix.lower() == ".mp4")
    for source in sources:
        destination = OUTPUT / "videos" / source.name
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        result = next((entry.copy() for entry in previous if entry.get("source_sha256") == digest
                       and entry.get("source") == source.relative_to(ROOT).as_posix() and destination.exists()), None)
        if result is None:
            result = optimize(source, destination, minimum_quality=93, crfs=(25, 24, 23, 22))
        duration = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
                         "format=duration", "-of", "default=nw=1:nk=1", str(destination)]))
        preview = OUTPUT / "previews" / source.name
        preview.parent.mkdir(parents=True, exist_ok=True)
        # Three short moments distributed across the full recording, without audio.
        starts = [max(0, (duration - 2) * fraction) for fraction in (.12, .46, .8)]
        segments = ";".join(f"[0:v]trim=start={start:.3f}:duration=2,setpts=PTS-STARTPTS,scale=360:-2,fps=24[v{i}]"
                            for i, start in enumerate(starts))
        filters = segments + ";[v0][v1][v2]concat=n=3:v=1:a=0[out]"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(destination),
                        "-filter_complex", filters, "-map", "[out]", "-an", "-c:v", "libx264",
                        "-preset", "slow", "-crf", "28", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                        str(preview)], check=True, capture_output=True)
        result["preview"] = str(preview.relative_to(ROOT))
        result["preview_bytes"] = preview.stat().st_size
        poster = OUTPUT / "posters" / (source.stem + ".jpg")
        poster.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", "1",
                        "-i", str(destination), "-frames:v", "1", "-vf", "scale=360:-2",
                        "-q:v", "3", str(poster)], check=True, capture_output=True)
        result["poster"] = str(poster.relative_to(ROOT))
        result["source_sha256"] = digest
        results.append(result)
    REPORT.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
    print(f"Updated {len(results)} videos and covers; report: {REPORT.relative_to(ROOT)}")
