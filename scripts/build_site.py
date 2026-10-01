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
    groups = []
    for folder, extensions, kind in (("fotos", PHOTO_EXTENSIONS, "image"), ("videos", VIDEO_EXTENSIONS, "video")):
        directory = root / "botox-rosa/assets/2026" / folder
        files = sorted((file for file in directory.glob("*")
                        if file.is_file() and not file.is_symlink() and not file.name.startswith(".")
                        and file.suffix.lower() in extensions),
                       key=lambda file: tuple((0, int(part)) if part.isdigit() else (1, part.casefold())
                                              for part in re.split(r'(\d+)', file.name)))
        groups.append([(file, kind) for file in files])
    # Interleave photos and videos while preserving natural filename order.
    media = []
    for index in range(max(map(len, groups), default=0)):
        for group in groups:
            if index < len(group):
                file, kind = group[index]
                media.append({"src": quote(file.relative_to(root / "botox-rosa").as_posix(), safe="/"), "type": kind})
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
        action = "Ampliar foto" if item["type"] == "image" else "Assistir ao vídeo"
        icon = "expand" if item["type"] == "image" else "play"
        if item["type"] == "image":
            visual = f'<img src="{source}" alt="Registro da campanha Botox Rosa 2026 na clínica" loading="lazy" decoding="async">'
        else:
            # Only the selected video fetches metadata, never the entire collection.
            visual = f'<video data-preview-src="{source}" preload="none" muted playsinline aria-hidden="true"></video><span class="diary-video-mark"><svg class="icon" aria-hidden="true"><use href="#icon-play"/></svg><span>UMA HISTÓRIA EM VÍDEO</span></span>'
        cards.append(f'''<button type="button" class="diary-card" data-media="{source}" data-type="{item['type']}" data-title="{title}" data-description="Um encontro de autocuidado na edição de 2026." data-track-video="campanha_2026_{number}" data-track-placement="campanha_2026" aria-label="{action}: {title}"{(' hidden' if index else '')}>
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
