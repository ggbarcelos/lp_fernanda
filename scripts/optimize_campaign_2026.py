"""Optimize 2026 MP4 videos and create lightweight covers without changing originals."""

import hashlib
import json
import subprocess
from pathlib import Path

from optimize_videos import ROOT, optimize

OUTPUT = ROOT / "botox-rosa/assets/optimized/2026"
REPORT = ROOT / "scripts/campaign-2026-media.json"


if __name__ == "__main__":
    results = []
    sources = sorted(file for file in (ROOT / "botox-rosa/assets/2026/videos").glob("*")
                     if file.is_file() and not file.is_symlink() and not file.name.startswith(".")
                     and file.suffix.lower() == ".mp4")
    for source in sources:
        destination = OUTPUT / "videos" / source.name
        result = optimize(source, destination, minimum_quality=93, crfs=(25, 24, 23, 22))
        poster = OUTPUT / "posters" / (source.stem + ".jpg")
        poster.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", "1",
                        "-i", str(destination), "-frames:v", "1", "-vf", "scale=360:-2",
                        "-q:v", "3", str(poster)], check=True, capture_output=True)
        result["poster"] = str(poster.relative_to(ROOT))
        result["source_sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
        results.append(result)
    REPORT.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
    print(f"Updated {len(results)} videos and covers; report: {REPORT.relative_to(ROOT)}")
