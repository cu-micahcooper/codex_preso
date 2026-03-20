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

    def test_brand_tokens_exist(self):
        html = read_html()
        self.assertIn("--cu-blue: #003963;", html)
        self.assertIn("--cu-gold: #FBB93A;", html)
        self.assertIn("--cu-orange: #F59536;", html)
        self.assertIn("--cu-white: #FFFFFF;", html)
        self.assertIn("--cu-gray: #E7E6E6;", html)
        self.assertIn("font-family: 'myriad-pro', sans-serif;", html)
        self.assertIn("font-family: 'minion-pro', serif;", html)

    def test_notes_plugin_and_speaker_notes_markup_exist(self):
        html = read_html()
        self.assertIn("plugin/notes/notes.esm.js", html)
        self.assertIn("<aside class=\"notes\">", html)
        self.assertIn("plugins: [RevealNotes]", html)
        self.assertIn("hash: true", html)
        self.assertIn("transition: 'fade'", html)
        self.assertIn("transitionSpeed: 'fast'", html)

    def test_layout_utilities_exist(self):
        html = read_html()
        self.assertIn(".dark-slide", html)
        self.assertIn(".two-col", html)
        self.assertIn(".callout-box", html)

    def test_core_hook_and_proof_copy_exist(self):
        html = read_html()
        required = [
            "Stop using AI for what you're already good at.",
            "Use it for what you're not good at.",
            "I don't code. I don't want to code.",
            "What tools could you have if you could describe what you wanted in plain English?",
            "Here is what I told Codex to write.",
            "Here is what it gave me.",
            "an LLM answer is a one-time output",
            "repeatable on the next run",
        ]
        for phrase in required:
            self.assertIn(phrase, html)

    def test_first_half_contains_multiple_notes_blocks(self):
        html = read_html()
        self.assertGreaterEqual(html.count('<aside class="notes">'), 11)

    def test_key_first_half_notes_exist(self):
        html = read_html()
        required_notes = [
            "Pause after this line and let the room react.",
            "Replace this box with the real prompt artifact later.",
            "Stress independence, repeatability, and auditability here.",
        ]
        for phrase in required_notes:
            self.assertIn(phrase, html)
