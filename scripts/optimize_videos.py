"""Create fast-start H.264 copies, recompressing only with smaller, high-quality results."""

import json
import shutil
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "botox-rosa/assets/optimized/videos"


def optimize(source):
    destination = DESTINATION / source.name
    with tempfile.TemporaryDirectory() as directory:
        candidate = Path(directory) / "candidate.mp4"
        metrics = Path(directory) / "vmaf.json"
        accepted = False
        score = 100.0
        selected_crf = None
        for crf in (25, 24):
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source), "-map", "0:v:0", "-map", "0:a?", "-c:v", "libx264", "-preset", "veryslow", "-crf", str(crf), "-threads", "4", "-pix_fmt", "yuv420p", "-fps_mode", "passthrough", "-c:a", "copy", "-movflags", "+faststart", str(candidate)], check=True, capture_output=True)
            if candidate.stat().st_size >= source.stat().st_size:
                break
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-threads", "2", "-i", str(candidate), "-threads", "2", "-i", str(source), "-lavfi", f"[0:v]setpts=PTS-STARTPTS[d];[1:v]setpts=PTS-STARTPTS[r];[d][r]libvmaf=log_fmt=json:log_path={metrics}:n_subsample=5:n_threads=2", "-an", "-f", "null", "-"], check=True, capture_output=True)
            score = json.loads(metrics.read_text())["pooled_metrics"]["vmaf"]["mean"]
            if score >= 95:
                accepted = True
                selected_crf = crf
                break
        if accepted:
            shutil.copyfile(candidate, destination)
        else:
            # Preserve original encoded video/audio if recompression would hurt.
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source), "-map", "0:v:0", "-map", "0:a?", "-c", "copy", "-movflags", "+faststart", str(destination)], check=True, capture_output=True)
            score = 100.0
        result = {"source": str(source.relative_to(ROOT)), "path": str(destination.relative_to(ROOT)), "before_bytes": source.stat().st_size, "after_bytes": destination.stat().st_size, "crf": selected_crf, "vmaf_mean": score, "video_audio_streams_preserved": not accepted}
        print(f"{source.name}: {result['before_bytes']/1048576:.2f} → {result['after_bytes']/1048576:.2f} MiB; VMAF {score:.2f}", flush=True)
        return result


if __name__ == "__main__":
    DESTINATION.mkdir(parents=True, exist_ok=True)
    sources = sorted((ROOT / "botox-rosa/assets/material/videos").glob("*.mp4"))
    sources += [ROOT / "botox-rosa/assets/media/hero-mix.mp4", ROOT / "botox-rosa/assets/media/gesto.mp4"]
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(optimize, sources))
    (ROOT / "scripts/video-optimization.json").write_text(json.dumps(results, indent=2) + "\n")
