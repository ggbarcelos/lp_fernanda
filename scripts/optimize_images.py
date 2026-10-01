"""Create responsive WebP copies; keep every supplied photograph unchanged."""

import hashlib
import json
import re
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "botox-rosa/assets/optimized/images"


def generate():
    DESTINATION.mkdir(parents=True, exist_ok=True)
    sources = sorted((ROOT / "botox-rosa/assets/material/fotos").glob("*.jpeg"))
    sources += [ROOT / "botox-rosa/assets/material/fotos/principal.png"]
    sources += sorted((ROOT / "botox-rosa/assets/media").glob("*poster.jpg"))
    sources += [ROOT / "botox-rosa/assets/imama-logo.png"]
    sources += sorted((ROOT / "img").glob("logo*.png"))
    catalog = {}
    for source in sources:
        name = re.sub(r"[^a-z0-9]+", "-", source.stem.lower()).strip("-")
        with Image.open(source) as original:
            image = ImageOps.exif_transpose(original)
            image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
            profile = original.info.get("icc_profile", b"")
            is_logo = "logo" in name
            variants = []
            widths = [image.width] if is_logo else sorted(set([w for w in (360, 640, 960) if w < image.width] + [image.width]))
            for width in widths:
                resized = image.resize((width, round(image.height * width / image.width)), Image.Resampling.LANCZOS)
                path = DESTINATION / f"{name}-{width}.webp"
                resized.save(path, "WEBP", quality=94 if source.name == "principal.png" else 90, lossless=is_logo, method=6, icc_profile=profile)
                if width == image.width and not is_logo and source.suffix in (".jpg", ".jpeg") and path.stat().st_size >= source.stat().st_size:
                    path.unlink()
                    path = source
                variants.append({"path": str(path.relative_to(ROOT)), "width": width, "height": resized.height, "bytes": path.stat().st_size})
            full = variants[-1]["path"] if is_logo else str(source.relative_to(ROOT))
            if source.name == "principal.png":
                path = DESTINATION / "principal-original.webp"
                image.save(path, "WEBP", lossless=True, method=6, icc_profile=profile)
                full = str(path.relative_to(ROOT))
            catalog[str(source.relative_to(ROOT))] = {"source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "source_bytes": source.stat().st_size, "width": image.width, "height": image.height, "variants": variants, "full": full}
            print(f"{source.name}: {source.stat().st_size // 1024} KiB → {variants[0]['bytes'] // 1024} KiB (small), {variants[-1]['bytes'] // 1024} KiB (full display)")
    (ROOT / "scripts/image-variants.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    generate()
