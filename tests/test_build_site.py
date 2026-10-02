import importlib.util
import hashlib
import json
import re
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("build_site", Path(__file__).resolve().parents[1] / "scripts/build_site.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class VersionedBuildTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "source"
        self.output = Path(self.temp.name) / "output"
        files = {
            "CNAME": "fernandabeltrao.com.br",
            "robots.txt": "User-agent: *\nAllow: /",
            "sitemap.xml": "<urlset/>",
            "index.html": '<meta name="site-version" content="development"><meta http-equiv="refresh" content="0; url=botox-rosa/"><meta property="og:image" content="https://fernandabeltrao.com.br/botox-rosa/assets/photo image.jpg">',
            "botox-rosa/index.html": '<meta name="site-version" content="development" data-manifest="../site-version.json"><script src="../assets/js/site-update.js" defer></script><link href="assets/style.css?v=old"><img src="assets/photo%20image.jpg"><button data-media="assets/video.mp4"></button><span style="background-image:url(\'assets/photo%20image.jpg\')"></span><a href="https://example.com/?a=1&amp;b=2">Link</a><script type="application/ld+json">{"image":"https://fernandabeltrao.com.br/botox-rosa/assets/photo%20image.jpg"}</script>',
            "assets/js/site-update.js": "window.checkUpdate = true;",
            "botox-rosa/assets/style.css": "body{background:url('photo%20image.jpg')}",
            "botox-rosa/assets/photo image.jpg": "photo one",
            "botox-rosa/assets/video.mp4": "video one",
            "img/logo.png": "logo",
            ".git/private": "secret",
            "unrelated.png": "do not publish",
        }
        for name, text in files.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)

    def test_changed_assets_and_css_dependencies_receive_new_urls(self):
        first = builder.build(self.root, self.output, "a" * 40)
        (self.root / "botox-rosa/assets/photo image.jpg").write_text("photo two")
        second = builder.build(self.root, self.output, "b" * 40)
        self.assertNotEqual(first["botox-rosa/assets/photo image.jpg"], second["botox-rosa/assets/photo image.jpg"])
        self.assertNotEqual(first["botox-rosa/assets/style.css"], second["botox-rosa/assets/style.css"])
        self.assertEqual(first["img/logo.png"], second["img/logo.png"])
        self.assertEqual(first["botox-rosa/assets/video.mp4"], second["botox-rosa/assets/video.mp4"])

    def test_all_media_paths_and_metadata_are_versioned(self):
        assets = builder.build(self.root, self.output, "a" * 40)
        text = (self.output / "botox-rosa/index.html").read_text()
        self.assertNotIn("?v=old", text)
        self.assertIn('content="' + "a" * 40 + '"', text)
        self.assertIn('id="site-update"', text)
        self.assertIn("window.checkUpdate = true;", text)
        self.assertIn("photo%20image.", text)
        self.assertIn("https://example.com/?a=1&amp;b=2", text)
        self.assertNotIn("&amp;amp;", text)
        dynamic = json.loads(re.search(r'<script id="site-assets" type="application/json">(.*?)</script>', text).group(1))
        self.assertEqual(dynamic["assets/video.mp4"], assets["botox-rosa/assets/video.mp4"].removeprefix("botox-rosa/"))
        structured = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', text, re.S).group(1))
        self.assertIn("photo%20image.", structured["image"])
        root_text = (self.output / "index.html").read_text()
        self.assertIn("photo%20image.", root_text)
        self.assertIn('content="0; url=botox-rosa/"', root_text)
        self.assertEqual(json.loads((self.output / "site-version.json").read_text())["revision"], "a" * 40)
        self.assertFalse((self.output / ".git").exists())
        self.assertFalse((self.output / "unrelated.png").exists())

    def test_build_is_reproducible_and_keeps_legacy_urls_working(self):
        first = builder.build(self.root, self.output, "a" * 40)
        html = (self.output / "botox-rosa/index.html").read_bytes()
        second = builder.build(self.root, self.output, "a" * 40)
        self.assertEqual(first, second)
        self.assertEqual(html, (self.output / "botox-rosa/index.html").read_bytes())
        self.assertTrue((self.output / "botox-rosa/assets/photo image.jpg").exists())

    def test_rejects_unsafe_output_and_invalid_revision(self):
        with self.assertRaises(ValueError):
            builder.build(self.root, self.root, "a" * 40)
        with self.assertRaises(ValueError):
            builder.build(self.root, self.output, "invalid")
        self.output.mkdir()
        (self.output / "keep.txt").write_text("keep")
        with self.assertRaises(ValueError):
            builder.build(self.root, self.output, "a" * 40)
        self.assertTrue((self.output / "keep.txt").exists())

    def test_responsive_candidates_are_fingerprinted_with_descriptors(self):
        source = self.root / "botox-rosa/index.html"
        source.write_text(source.read_text() + '<img srcset="assets/photo%20image.jpg 360w, assets/photo%20image.jpg 720w" sizes="50vw">')
        builder.build(self.root, self.output, "a" * 40)
        text = (self.output / "botox-rosa/index.html").read_text()
        self.assertRegex(text, r'srcset="assets/photo%20image\.[a-f0-9]{16}\.jpg 360w, assets/photo%20image\.[a-f0-9]{16}\.jpg 720w"')
        self.assertIn('sizes="50vw"', text)

    def add_campaign_file(self, name, contents="media"):
        path = self.root / "botox-rosa/assets/2026" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents)
        return path

    def add_campaign_section(self):
        source = self.root / "botox-rosa/index.html"
        source.write_text(source.read_text() + '<span data-diary-count>old</span><span data-diary-status aria-live="polite">old</span><!-- campaign-2026:start -->stale<!-- campaign-2026:end -->')

    def test_campaign_discovers_added_and_removed_media_with_versioned_urls(self):
        self.add_campaign_section()
        photo = self.add_campaign_file("fotos/Encontro 01.PNG")
        self.add_campaign_file("fotos/Encontro 10.webp")
        self.add_campaign_file("fotos/Encontro 2.jpg")
        self.add_campaign_file("videos/Depoimento & carinho.mp4")
        self.add_campaign_file("fotos/.DS_Store")
        self.add_campaign_file("fotos/notes.txt")
        self.add_campaign_file("videos/.oculto.mp4")
        self.add_campaign_file("fotos/atalho.jpg").unlink()
        (photo.parent / "atalho.jpg").symlink_to(photo)
        assets = builder.build(self.root, self.output, "a" * 40)
        text = (self.output / "botox-rosa/index.html").read_text()
        self.assertIn("3 fotos + 1 vídeo", text)
        self.assertIn("01 / 04", text)
        self.assertEqual(text.count('class="diary-card"'), 4)
        self.assertIn('data-preview-src="assets/2026/videos/Depoimento%20%26%20carinho.', text)
        self.assertIn(assets["botox-rosa/assets/2026/fotos/Encontro 01.PNG"].removeprefix("botox-rosa/").replace(" ", "%20"), text)
        self.assertLess(text.index("Encontro%202."), text.index("Encontro%2010."))
        self.assertNotIn("atalho", text)
        self.assertFalse((self.output / "botox-rosa/assets/2026/fotos/.DS_Store").exists())
        photo.unlink()
        self.add_campaign_file("videos/mais um.webm")
        builder.build(self.root, self.output, "b" * 40)
        text = (self.output / "botox-rosa/index.html").read_text()
        self.assertIn("2 fotos + 2 vídeos", text)
        self.assertNotIn("Encontro%2001.", text)
        self.assertIn("mais%20um.", text)

    def test_campaign_has_useful_empty_state_and_escapes_filenames(self):
        self.add_campaign_section()
        builder.build(self.root, self.output, "a" * 40)
        text = (self.output / "botox-rosa/index.html").read_text()
        self.assertIn('class="diary-empty"', text)
        self.assertNotIn('class="diary-card"', text)
        self.add_campaign_file('fotos/encontro "><script>.jpg')
        builder.build(self.root, self.output, "b" * 40)
        text = (self.output / "botox-rosa/index.html").read_text()
        self.assertIn('1 foto', text)
        self.assertIn('%22%3E%3Cscript%3E', text)
        self.assertNotIn('encontro "><script>', text)

    def test_campaign_uses_optimized_video_and_cover_only_for_matching_source(self):
        self.add_campaign_section()
        self.add_campaign_file('fotos/photo.jpg')
        source = self.add_campaign_file('videos/video.mp4', 'original video')
        video = self.root / 'botox-rosa/assets/optimized/2026/videos/video.mp4'
        poster = self.root / 'botox-rosa/assets/optimized/2026/posters/video.jpg'
        for path in (video, poster):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('optimized media')
        report = self.root / 'scripts/campaign-2026-media.json'
        report.parent.mkdir(parents=True)
        report.write_text(json.dumps([{
            'source': source.relative_to(self.root).as_posix(),
            'path': video.relative_to(self.root).as_posix(),
            'poster': poster.relative_to(self.root).as_posix(),
            'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        }]))
        self.assertEqual([item['type'] for item in builder.campaign_2026_media(self.root)], ['video', 'image'])
        assets = builder.build(self.root, self.output, 'a' * 40)
        text = (self.output / 'botox-rosa/index.html').read_text()
        self.assertIn('1 foto + 1 vídeo', text)
        self.assertIn('data-media="' + assets[video.relative_to(self.root).as_posix()].removeprefix('botox-rosa/') + '"', text)
        self.assertIn('data-poster="' + assets[poster.relative_to(self.root).as_posix()].removeprefix('botox-rosa/') + '"', text)
        self.assertNotIn('data-preview-src', text)
        source.write_text('replacement video')
        media = builder.campaign_2026_media(self.root)[0]
        self.assertEqual(media['src'], 'assets/2026/videos/video.mp4')
        self.assertNotIn('poster', media)
        report.write_text('invalid JSON')
        self.assertEqual(builder.campaign_2026_media(self.root)[0]['src'], 'assets/2026/videos/video.mp4')
