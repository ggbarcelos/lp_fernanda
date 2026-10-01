import importlib.util
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
