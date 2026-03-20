import html as html_lib
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
MARKDOWN_EXPORT = ROOT / "docs" / "presentation-speaker-notes.md"


def read_html():
    return INDEX.read_text(encoding="utf-8") if INDEX.exists() else ""


def read_display_html():
    return html_lib.unescape(read_html())


def read_markdown_export():
    return MARKDOWN_EXPORT.read_text(encoding="utf-8") if MARKDOWN_EXPORT.exists() else ""


PROMPT_TEXT = "Create a web app that lets me search a database of organic molecules and interact with 3D models of them"


class SlidesParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.in_slides_div = False
        self.top_level_slide_count = 0
        self.slide_titles = []
        self.slide_texts = []
        self.slide_has_notes = []
        self._capture_slide_text = False
        self._current_slide_text = []
        self._current_slide_has_notes = False
        self._capture_title = False
        self._current_title = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "div" and attrs_dict.get("class") == "slides":
            self.in_slides_div = True
        elif self.in_slides_div and tag == "section" and not any(item == "section" for item in self.stack):
            self.top_level_slide_count += 1
            self._current_title = []
            self._current_slide_text = []
            self._current_slide_has_notes = False
            self._capture_slide_text = True
        elif self.in_slides_div and tag in {"h1", "h2"} and any(item == "section" for item in self.stack):
            if self._current_title == []:
                self._capture_title = True
        elif self.in_slides_div and tag == "aside" and attrs_dict.get("class") == "notes" and any(
            item == "section" for item in self.stack
        ):
            self._current_slide_has_notes = True
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if self._capture_title and tag in {"h1", "h2"}:
            title = "".join(self._current_title).strip()
            if title:
                self.slide_titles.append(title)
            self._capture_title = False
        if self._capture_slide_text and tag == "section" and any(item == "section" for item in self.stack):
            text = "".join(self._current_slide_text).strip()
            self.slide_texts.append(text)
            self.slide_has_notes.append(self._current_slide_has_notes)
            self._capture_slide_text = False
        if tag == "div" and self.in_slides_div and self.stack and self.stack[-1] == "div":
            if len(self.stack) >= 1 and "section" not in self.stack:
                self.in_slides_div = False
        if self.stack:
            self.stack.pop()

    def handle_data(self, data):
        if self._capture_title:
            self._current_title.append(data)
        if self._capture_slide_text:
            self._current_slide_text.append(data)


def parse_slides():
    parser = SlidesParser()
    parser.feed(read_html())
    return parser


class PresentationShellTests(unittest.TestCase):
    def test_index_html_exists(self):
        self.assertTrue(INDEX.exists(), "index.html should exist")

    def test_markdown_export_exists(self):
        self.assertTrue(MARKDOWN_EXPORT.exists(), "presentation speaker-notes markdown export should exist")

    def test_markdown_export_contains_titles_and_notes(self):
        md = read_markdown_export()
        required = [
            "# Codex: When you’re done Chatting about your problems",
            "## 1. Codex: When you’re done Chatting about your problems",
            "## 9. Chat vs Codex",
            "## 19. Let’s build something useful",
            "Speaker notes",
            "Some of you are thinking something right now. What are they?",
            "Stress independence, repeatability, and auditability here.",
        ]
        for phrase in required:
            self.assertIn(phrase, md)

    def test_title_and_subtitle_copy_exist(self):
        html = read_display_html()
        self.assertIn("Codex: When you’re done Chatting about your problems", html)
        self.assertIn("Let’s build!", html)

    def test_curly_apostrophes_are_used_in_copy(self):
        html = read_html()
        required_entities = [
            "you&#x2019;re done Chatting",
            "I&#x2019;ve heard",
            "It&#x2019;s not better",
            "you&#x2019;re not good",
            "there&#x2019;s friction",
            "you&#x2019;re interested",
            "Let&#x2019;s build something useful",
        ]
        for phrase in required_entities:
            self.assertIn(phrase, html)

    def test_reveal_assets_are_loaded(self):
        html = read_html()
        self.assertIn("cdn.jsdelivr.net/npm/reveal.js", html)
        self.assertIn("use.typekit.net/apf8ssc.css", html)

    def test_no_local_asset_references_exist(self):
        html = read_html()
        self.assertNotRegex(
            html,
            r"""(?is)(?:src|href|poster|data-src|data-background(?:-image|-video|-iframe)?)\s*=\s*['"](?!https?://|data:|#|//)[^'"]+['"]""",
        )
        self.assertNotRegex(html, r"(?is)url\(\s*['\"]?/(?!/)[^'\"\)]+['\"]?\s*\)")
        self.assertNotIn("src=\"assets/", html)
        self.assertNotIn("src='assets/", html)
        self.assertNotIn("href=\"assets/", html)
        self.assertNotIn("href='assets/", html)
        self.assertNotIn("data-src=\"assets/", html)
        self.assertNotIn("data-src='assets/", html)
        self.assertNotIn("poster=\"assets/", html)
        self.assertNotIn("poster='assets/", html)
        self.assertNotIn("url('assets/", html)
        self.assertNotIn('url("assets/', html)
        self.assertNotIn("url(/", html)

    def test_prompt_and_output_slides_exist(self):
        parser = parse_slides()
        self.assertIn("Here is what I told Codex to write.", parser.slide_titles)
        prompt_slide_index = parser.slide_titles.index("Here is what I told Codex to write.")
        self.assertIn(PROMPT_TEXT, parser.slide_texts[prompt_slide_index])
        self.assertIn("Here is what it gave me.", parser.slide_titles)

    def test_output_slide_text_is_removed(self):
        html = read_display_html()
        self.assertNotIn("Output screenshot placeholder", html)
        self.assertNotIn("A working tool.", html)

    def test_prompt_placeholder_is_removed(self):
        self.assertNotIn("Prompt screenshot placeholder", read_html())

    def test_every_slide_has_speaker_notes(self):
        parser = parse_slides()
        self.assertEqual(parser.top_level_slide_count, len(parser.slide_has_notes))
        self.assertTrue(parser.slide_has_notes)
        self.assertTrue(all(parser.slide_has_notes))

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
        self.assertIn(".content-slide", html)
        self.assertIn(".dark-slide", html)
        self.assertIn(".two-col", html)

    def test_two_column_layout_is_used_broadly(self):
        html = read_html()
        self.assertGreaterEqual(html.count('class="two-col"'), 7)

    def test_visual_boxes_are_removed(self):
        html = read_html()
        removed = [
            ".callout-box",
            ".highlight-box",
            ".comparison-card",
            ".prompt-frame",
            ".example-chip",
            ".signal-grid",
            ".dark-panel",
            'class="callout-box"',
            'class="highlight-box"',
            'class="comparison-card"',
            'class="prompt-frame"',
            'class="example-chip"',
            'class="signal-grid"',
            'class="dark-panel"',
        ]
        for phrase in removed:
            self.assertNotIn(phrase, html)

    def test_depth_effects_are_removed(self):
        html = read_html()
        self.assertNotIn("box-shadow:", html)
        self.assertNotIn("radial-gradient(", html)

    def test_dark_slides_use_solid_blue_background(self):
        html = read_html()
        self.assertIn(".dark-slide {", html)
        self.assertIn("background: var(--cu-blue) !important;", html)
        self.assertNotIn("linear-gradient(135deg, #002745 0%, #003963 55%, #155987 100%)", html)

    def test_eyebrow_headers_are_removed_from_slides(self):
        html = read_html()
        self.assertNotIn('class="eyebrow"', html)
        self.assertNotIn("text-transform: uppercase;", html)

    def test_bullet_lists_use_custom_marker_layout(self):
        html = read_html()
        self.assertIn(".reveal ul {", html)
        self.assertIn("list-style: none;", html)
        self.assertIn(".reveal ul li::before {", html)
        self.assertIn('content: "•";', html)

    def test_core_hook_and_proof_copy_exist(self):
        html = read_display_html()
        required = [
            "Biggest issue I’ve heard with ChatGPT:",
            "It’s not better than I am at xyz",
            "Try using it for what you’re not good at",
            "Yeah, me either",
            "anymore",
            "Artie Kuhn, Emerging Technology in Business + Design Department at Miami University",
            "there’s friction to eliminating it",
            "Real-world issues: Sugru",
            "Knowledge-work issues: Codex",
            "Here is what I told Codex to write.",
            "Here is what it gave me.",
            "Runs once in a chat window.",
            "Useful, but not a system.",
            "Runs independently once it is created.",
            "Repeatable on the next run.",
            "Auditable: inspect the logic, inputs, and results.",
        ]
        for phrase in required:
            self.assertIn(phrase, html)

    def test_tool_vs_output_slide_uses_crisp_comparison_copy(self):
        parser = parse_slides()
        self.assertIn("Chat vs Codex", parser.slide_titles)
        slide_index = parser.slide_titles.index("Chat vs Codex")
        slide_text = parser.slide_texts[slide_index]
        required = [
            "LLM-generated output",
            "Runs once in a chat window.",
            "Quick and easy",
            "Useful, but not a system.",
            "Sometimes hallcinates",
            "LLM-built tool",
            "Has access to local tools and data",
            "iterates through the hacclinations",
            "Runs independently once it is created.",
            "Repeatable on the next run.",
            "Auditable: inspect the logic, inputs, and results.",
        ]
        for phrase in required:
            self.assertIn(phrase, slide_text)
        html = read_display_html()
        self.assertIn('alt="Tool vs. output illustration"', html)

    def test_friction_slide_uses_fragmented_parallel_examples(self):
        parser = parse_slides()
        self.assertIn("Friction is the challenge", parser.slide_titles)
        slide_index = parser.slide_titles.index("Friction is the challenge")
        slide_text = parser.slide_texts[slide_index]
        self.assertIn("Real-world issues: Sugru", slide_text)
        self.assertIn("Knowledge-work issues: Codex", slide_text)
        html = read_display_html()
        self.assertIn("class=\"fragment fade-in\"", html)
        self.assertIn("Real-world issues: Sugru", html)
        self.assertIn("Knowledge-work issues: Codex", html)
        self.assertNotIn('class="split-rule"', html)

    def test_objection_slide_uses_anymore_fragment(self):
        parser = parse_slides()
        self.assertIn("I don’t code. I don’t want to code.", parser.slide_titles)
        slide_index = parser.slide_titles.index("I don’t code. I don’t want to code.")
        slide_text = parser.slide_texts[slide_index]
        self.assertIn("anymore", slide_text)
        self.assertEqual(parser.slide_titles[slide_index + 1], "Dr. John Delano")
        html = read_display_html()
        self.assertIn('<span class="fragment fade-in">anymore</span>', html)
        self.assertIn('alt="#vibecoding"', html)
        self.assertIn("data:image/svg+xml", html)

    def test_prompt_slide_uses_styled_blockquote(self):
        html = read_display_html()
        self.assertIn('<blockquote class="prompt-quote">', html)
        self.assertIn(PROMPT_TEXT, html)

    def test_sigh_list_follow_up_slides_are_tightened(self):
        parser = parse_slides()
        self.assertGreaterEqual(len(parser.slide_titles), 15)
        self.assertEqual(parser.slide_titles[12], "Back to the sigh list")
        self.assertEqual(parser.slide_titles[13], "What belongs on the list?")
        slide_text = parser.slide_texts[13]
        required = [
            "Good candidates are recurring, concrete, and easy to recognize when they come back.",
            "exam questions uploaded into Canvas",
            "chemical diagrams",
            "learning objects",
            "interlinear Bible",
        ]
        for phrase in required:
            self.assertIn(phrase, slide_text)

    def test_first_half_contains_multiple_notes_blocks(self):
        parser = parse_slides()
        self.assertGreaterEqual(len(parser.slide_has_notes), 11)
        self.assertTrue(all(parser.slide_has_notes[:11]))

    def test_language_abstraction_slide_is_removed(self):
        parser = parse_slides()
        self.assertNotIn("Language is the abstraction", parser.slide_titles)
        self.assertNotIn("A real constraint", parser.slide_titles)
        self.assertNotIn(
            "You do not need programmer fluency first if you can specify outcomes, constraints, and revisions in plain English.",
            read_display_html(),
        )
        self.assertNotIn("Not answers. Not drafts. Tools that keep doing useful work after the chat ends.", read_display_html())

    def test_slide_count_is_exactly_nineteen(self):
        parser = parse_slides()
        self.assertEqual(parser.top_level_slide_count, 19)

    def test_raw_section_count_is_in_expected_range(self):
        html = read_html()
        slide_count = html.count("<section")
        self.assertGreaterEqual(slide_count, 19)
        self.assertLessEqual(slide_count, 21)

    def test_opening_sequence_matches_task_four_spec(self):
        parser = parse_slides()
        self.assertGreaterEqual(len(parser.slide_titles), 5)
        self.assertEqual(
            parser.slide_titles[:5],
            [
                "Codex: When you’re done Chatting about your problems",
                "Sigh list",
                "Friction is the challenge",
                "Biggest issue I’ve heard with ChatGPT:",
                "I don’t code. I don’t want to code.",
            ],
        )

    def test_opening_slide_uses_fragments(self):
        html = read_display_html()
        self.assertIn('class="fragment fade-in', html)
        self.assertIn("It’s not better than I am at xyz", html)
        self.assertIn("Try using it for what you’re not good at", html)

    def test_key_first_half_notes_exist(self):
        html = read_display_html()
        required_notes = [
            "Some of you are thinking something right now. What are they?",
            "Pause after this line and let the room react.",
            "what is sugru. story of my light switch student",
            "Use the exact prompt text here to show how concrete the request can be.",
            "Stress independence, repeatability, and auditability here.",
        ]
        for phrase in required_notes:
            self.assertIn(phrase, html)

    def test_adoption_and_closing_copy_exist(self):
        html = read_display_html()
        required = [
            "Back to the sigh list",
            "What in your life or work makes you sigh",
            "Real-world issues: Sugru",
            "Knowledge-work issues: Codex",
            "What belongs on the list?",
            "Good candidates are recurring, concrete, and easy to recognize when they come back.",
            "exam questions uploaded into Canvas",
            "chemical diagrams",
            "learning objects",
            "interlinear Bible",
            "Dr. John Delano",
            "Bring your laptop",
            "Bring your sigh list",
            "Bring one real problem",
            "Micah Cooper",
            "micahcooper@cedarville.edu",
        ]
        for phrase in required:
            self.assertIn(phrase, html)

    def test_removed_sigh_phrase_is_not_present(self):
        self.assertNotIn("If it makes you sigh, write it down before you explain it away.", read_display_html())

    def test_key_closing_notes_exist(self):
        html = read_display_html()
        required_notes = [
            "Credit Artie Kuhn at Miami University here.",
            "Short handoff, then stop talking.",
            "These are examples of tool-worthy problems, not just chat prompts.",
        ]
        for phrase in required_notes:
            self.assertIn(phrase, html)
