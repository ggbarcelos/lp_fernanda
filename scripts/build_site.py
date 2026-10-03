"""Build GitHub Pages files with content fingerprints, using only Python's stdlib."""

import argparse
import hashlib
import html
import json
import posixpath
import re
import shutil
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://fernandabeltrao.com.br"
PUBLIC_DIRS = ("assets", "botox-rosa/assets", "img")
PAGES = ("index.html", "botox-rosa/index.html")
ATTR = re.compile(r'(?P<prefix>\b(?:src|href|poster|data-media|data-src|data-preview-src|data-poster|content)=")(?P<url>[^"<>]*)(?P<suffix>")')
SRCSET = re.compile(r'(?P<prefix>\bsrcset=")(?P<value>[^"<>]*)(?P<suffix>")')
CSS_URL = re.compile(r"url\(\s*(['\"]?)([^)'\"]+)\1\s*\)")
JSON_LD = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)
CAMPAIGN_CARDS = re.compile(r'(<!-- campaign-2026:start -->).*?(<!-- campaign-2026:end -->)', re.S)
PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif"}
VIDEO_EXTENSIONS = {".mp4", ".webm", ".m4v"}


def campaign_2026_media(root):
    """Discover published media; ignore hidden files, symlinks and unsupported formats."""
    report = root / "scripts/campaign-2026-media.json"
    try:
        entries = json.loads(report.read_text(encoding="utf-8")) if report.is_file() else []
    except (ValueError, OSError):
        entries = []
    optimized = {entry["source"]: entry for entry in entries
                 if isinstance(entry, dict) and isinstance(entry.get("source"), str)} if isinstance(entries, list) else {}
    try:
        images = json.loads((root / "scripts/image-variants.json").read_text(encoding="utf-8"))
        if not isinstance(images, dict):
            images = {}
    except (ValueError, OSError):
        images = {}

    def optimized_file(value):
        if not isinstance(value, str):
            return None
        path = root / value
        allowed = (root / "botox-rosa/assets/optimized/2026").absolute()
        if path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(allowed):
            return path
        return None

    groups = []
    for folder, extensions, kind in (("videos", VIDEO_EXTENSIONS, "video"), ("fotos", PHOTO_EXTENSIONS, "image")):
        directory = root / "botox-rosa/assets/2026" / folder
        files = sorted((file for file in directory.glob("*")
                        if file.is_file() and not file.is_symlink() and not file.name.startswith(".")
                        and file.suffix.lower() in extensions),
                       key=lambda file: tuple((0, int(part)) if part.isdigit() else (1, part.casefold())
                                              for part in re.split(r'(\d+)', file.name)))
        groups.append([(file, kind) for file in files])
    # Start with a video, then alternate videos and photos in natural filename order.
    media = []
    for index in range(max(map(len, groups), default=0)):
        for group in groups:
            if index < len(group):
                file, kind = group[index]
                item = {"src": quote(file.relative_to(root / "botox-rosa").as_posix(), safe="/"), "type": kind}
                image_entry = images.get(file.relative_to(root).as_posix()) if kind == "image" else None
                if isinstance(image_entry, dict) and image_entry.get("source_sha256") == hashlib.sha256(file.read_bytes()).hexdigest():
                    variants = []
                    for variant in image_entry.get("variants", []):
                        if not isinstance(variant, dict) or not isinstance(variant.get("path"), str):
                            continue
                        path = root / variant["path"]
                        if (path.is_file() and not path.is_symlink() and
                                path.resolve().is_relative_to((root / "botox-rosa/assets/optimized/images").resolve()) and
                                isinstance(variant.get("width"), int) and variant["width"] > 0):
                            variants.append((variant["width"], quote(path.relative_to(root / "botox-rosa").as_posix(), safe="/")))
                    if variants:
                        variants.sort()
                        item["image_src"] = next((url for width, url in variants if width >= 640), variants[-1][1])
                        item["srcset"] = ", ".join(f"{url} {width}w" for width, url in variants)
                        item["width"], item["height"] = image_entry["width"], image_entry["height"]
                entry = optimized.get(file.relative_to(root).as_posix()) if kind == "video" else None
                if entry and entry.get("source_sha256") == hashlib.sha256(file.read_bytes()).hexdigest():
                    video, poster = optimized_file(entry.get("path")), optimized_file(entry.get("poster"))
                    preview = optimized_file(entry.get("preview"))
                    if video:
                        item["src"] = quote(video.relative_to(root / "botox-rosa").as_posix(), safe="/")
                        if preview:
                            item["preview"] = quote(preview.relative_to(root / "botox-rosa").as_posix(), safe="/")
                        if poster:
                            item["poster"] = quote(poster.relative_to(root / "botox-rosa").as_posix(), safe="/")
                media.append(item)
    return media


def render_campaign_2026(text, root):
    if not CAMPAIGN_CARDS.search(text):
        return text
    media = campaign_2026_media(root)
    cards = []
    for index, item in enumerate(media):
        number = f"{index + 1:02}"
        title = f"Botox Rosa 2026 · Registro {number}"
        source = html.escape(item["src"], quote=True)
        action = "Ampliar foto" if item["type"] == "image" else "Ver vídeo completo"
        icon = "expand" if item["type"] == "image" else "play"
        poster_attr = f' data-poster="{html.escape(item["poster"], quote=True)}"' if item.get("poster") else ""
        if item["type"] == "image":
            image_source = html.escape(item.get("image_src", item["src"]), quote=True)
            responsive = (f' srcset="{html.escape(item["srcset"], quote=True)}" sizes="(max-width: 760px) calc(100vw - 72px), 480px" width="{item["width"]}" height="{item["height"]}"' if item.get("srcset") else "")
            visual = f'<img src="{image_source}"{responsive} alt="Registro da campanha Botox Rosa 2026 na clínica" loading="lazy" decoding="async">'
        else:
            # Lightweight silent excerpts are loaded only while the mix is visible.
            if item.get("preview"):
                cover = f' poster="{html.escape(item["poster"], quote=True)}"' if item.get("poster") else ""
                visual = f'<video data-preview-src="{html.escape(item["preview"], quote=True)}"{cover} preload="none" muted playsinline loop aria-hidden="true"></video>'
            elif item.get("poster"):
                visual = f'<img src="{html.escape(item["poster"], quote=True)}" alt="Capa de vídeo da campanha Botox Rosa 2026" loading="lazy" decoding="async">'
            else:
                visual = f'<video data-preview-src="{source}" preload="none" muted playsinline aria-hidden="true"></video>'
            visual += '<span class="diary-video-mark"><svg class="icon" aria-hidden="true"><use href="#icon-play"/></svg><span>VER VÍDEO COMPLETO</span></span>'
        cards.append(f'''<button type="button" class="diary-card" data-media="{source}" data-type="{item['type']}"{poster_attr} data-title="{title}" data-description="Um encontro de autocuidado na edição de 2026." data-track-video="campanha_2026_{number}" data-track-placement="campanha_2026" aria-label="{action}: {title}"{(' hidden' if index else '')}>
              <span class="diary-visual">{visual}</span>
              <span class="diary-card-action">{action} <svg class="icon" aria-hidden="true"><use href="#icon-{icon}"/></svg></span>
            </button>''')
    if not cards:
        cards.append('<div class="diary-empty"><img src="assets/ribbon.svg" width="42" height="68" alt=""><p>Um outubro para vestir a causa.</p><span>Os encontros de 2026 chegam por aqui.</span></div>')
    text = CAMPAIGN_CARDS.sub(lambda m: m[1] + "\n            " + "\n            ".join(cards) + "\n            " + m[2], text)
    photos = sum(item["type"] == "image" for item in media)
    videos = len(media) - photos
    counts = []
    if photos:
        counts.append(f"{photos} foto" + ("s" if photos > 1 else ""))
    if videos:
        counts.append(f"{videos} vídeo" + ("s" if videos > 1 else ""))
    count = " + ".join(counts) or "Novos encontros em breve"
    text = re.sub(r'(<span data-diary-count>).*?(</span>)', lambda m: m[1] + count + m[2], text)
    text = re.sub(r'(<span data-diary-status[^>]*>).*?(</span>)', lambda m: m[1] + (f"01 / {len(media):02}" if media else "2026") + m[2], text)
    return text


def fingerprint(path, contents):
    digest = hashlib.sha256(contents).hexdigest()[:16]
    return str(path.with_name(f"{path.stem}.{digest}{path.suffix}"))


def asset_url(value, context, assets):
    url = urlsplit(html.unescape(value))
    if not url.path or (url.scheme or url.netloc) and f"{url.scheme}://{url.netloc}" != ORIGIN:
        return value
    path = unquote(url.path)
    absolute = bool(url.netloc) or path.startswith("/")
    source = path.lstrip("/") if absolute else posixpath.normpath(posixpath.join(str(context.parent), path))
    if source not in assets:
        return value
    target = assets[source] if absolute else posixpath.relpath(assets[source], str(context.parent))
    target = quote(target, safe="/")
    if absolute:
        target = "/" + target
    # Former manual ?v= values are superseded by the content fingerprint.
    return urlunsplit((url.scheme, url.netloc, target, "", url.fragment))


def rewrite_css(text, context, assets):
    return CSS_URL.sub(lambda m: f"url('{asset_url(m[2], context, assets)}')", text)


def rewrite_srcset(value, context, assets):
    candidates = []
    for candidate in html.unescape(value).split(","):
        parts = candidate.strip().split()
        if parts:
            parts[0] = asset_url(parts[0], context, assets)
            candidates.append(" ".join(parts))
    return html.escape(", ".join(candidates), quote=True)


def rewrite_json(value, context, assets):
    if isinstance(value, str):
        return asset_url(value, context, assets)
    if isinstance(value, list):
        return [rewrite_json(item, context, assets) for item in value]
    if isinstance(value, dict):
        return {key: rewrite_json(item, context, assets) for key, item in value.items()}
    return value


def build(root, output, revision):
    root, output = root.resolve(), output.resolve()
    if not re.fullmatch(r"[a-f0-9]{40}", revision):
        raise ValueError("Revision must be a full Git commit SHA.")
    if output == root or output in root.parents or any(output == root / folder or root / folder in output.parents for folder in PUBLIC_DIRS):
        raise ValueError("Output must not replace source files.")
    if output.exists():
        if not (output / ".site-build-output").is_file():
            raise ValueError("Refusing to replace an unmanaged output directory.")
        shutil.rmtree(output)
    output.mkdir(parents=True)
    (output / ".site-build-output").touch()
    assets = {}
    sources = sorted(file for folder in PUBLIC_DIRS for file in (root / folder).rglob("*") if file.is_file() and not file.is_symlink() and not any(part.startswith(".") for part in file.relative_to(root).parts))
    # CSS fingerprints include the final URLs of their image dependencies.
    for file in sorted(sources, key=lambda file: file.suffix == ".css"):
        path = file.relative_to(root)
        contents = file.read_bytes()
        if file.suffix == ".css":
            contents = rewrite_css(contents.decode("utf-8"), path, assets).encode("utf-8")
        target = fingerprint(path, contents)
        assets[str(path)] = target
        for name in (str(path), target):
            destination = output / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(contents)

    for filename in PAGES:
        path = Path(filename)
        text = (root / path).read_text(encoding="utf-8")
        if filename == "botox-rosa/index.html":
            text = render_campaign_2026(text, root)
        text = ATTR.sub(lambda m: m["prefix"] + html.escape(html.unescape(asset_url(m["url"], path, assets)), quote=True) + m["suffix"], text)
        text = SRCSET.sub(lambda m: m["prefix"] + rewrite_srcset(m["value"], path, assets) + m["suffix"], text)
        text = rewrite_css(text, path, assets)
        text = JSON_LD.sub(lambda m: m[1] + "\n" + json.dumps(rewrite_json(json.loads(m[2]), path, assets), ensure_ascii=False, indent=2) + "\n" + m[3], text)
        text = text.replace('name="site-version" content="development"', f'name="site-version" content="{revision}"')
        if filename == "botox-rosa/index.html":
            dynamic_assets = {posixpath.relpath(key, str(path.parent)): posixpath.relpath(value, str(path.parent)) for key, value in assets.items() if key.startswith("botox-rosa/assets/") and Path(key).suffix in (".mp4", ".jpg")}
            manifest = json.dumps(dynamic_assets, ensure_ascii=False).replace("<", "\\u003c")
            updater = (root / "assets/js/site-update.js").read_text(encoding="utf-8")
            # Inline the tiny checker so cached HTML can still detect future releases.
            text = re.sub(r'<script src="[^"<>]*site-update\.[a-f0-9]{16}\.js" defer></script>', lambda _: f'<script id="site-update">\n{updater}\n</script>\n  <script id="site-assets" type="application/json">{manifest}</script>', text)
            if 'id="site-update"' not in text:
                raise ValueError("Missing site update bootstrap in landing page.")
        destination = output / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8")

    for filename in ("CNAME", "robots.txt", "sitemap.xml"):
        shutil.copyfile(root / filename, output / filename)
    (output / "site-version.json").write_text(json.dumps({"revision": revision}) + "\n", encoding="utf-8")
    (output / ".nojekyll").touch()
    return assets


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--revision", required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "_site")
    args = parser.parse_args()
    result = build(ROOT, args.output, args.revision)
    print(f"Built {len(result)} fingerprinted assets in {args.output}; revision {args.revision}.")
