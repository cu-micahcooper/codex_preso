from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def read_html():
    return INDEX.read_text(encoding="utf-8") if INDEX.exists() else ""


class PresentationShellTests(unittest.TestCase):
    def test_index_html_exists(self):
        self.assertTrue(INDEX.exists(), "index.html should exist")

    def test_title_and_subtitle_copy_exist(self):
        html = read_html()
        self.assertIn("Codex: When you're done Chatting about your problems", html)
        self.assertIn("Have Codex build solutions", html)

    def test_reveal_assets_are_loaded(self):
        html = read_html()
        self.assertIn("cdn.jsdelivr.net/npm/reveal.js", html)
        self.assertIn("use.typekit.net/apf8ssc.css", html)
