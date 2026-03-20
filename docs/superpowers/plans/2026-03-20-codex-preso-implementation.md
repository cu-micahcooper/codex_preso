# Codex Presentation Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single-file Reveal.js presentation in `index.html` that matches the approved Cedarville-branded Codex spec, includes speaker notes, and is backed by repeatable structural tests.

**Architecture:** Keep the implementation deliberately small: one self-contained `index.html` for the full deck, one stdlib Python test module to validate structure/content, and one `.gitignore` to keep local noise out of the repo. The HTML should embed all custom styling, slide markup, notes, and any fixed imagery while loading only Reveal.js and Adobe Typekit from CDNs. Use tests to lock down the title/subtitle, required slide copy, tool-versus-output framing, note presence, and the single-file/no-broken-local-assets constraint before final manual browser verification.

**Tech Stack:** HTML5, Reveal.js 5 via CDN, Adobe Typekit, vanilla CSS, vanilla JavaScript, Python 3 `unittest`

---

## File Structure

### Files To Create

- `.gitignore`
  Responsibility: ignore local macOS artifacts, Python cache directories, and brainstorm scratch files so the repo stays clean during implementation and verification.
- `index.html`
  Responsibility: contain the entire Reveal.js presentation, embedded styles, all 22 slides, all speaker notes, and the Reveal initialization script.
- `tests/test_presentation.py`
  Responsibility: provide repeatable smoke tests for presentation existence, structure, required copy, slide count expectations, speaker notes presence, CDN references, and self-contained asset rules.

### Files To Modify

- `README.md`
  Responsibility: no changes planned. Leave untouched unless implementation discovers a real need for run instructions.
- `docs/superpowers/specs/2026-03-19-codex-preso-design.md`
  Responsibility: reference only. Do not modify during implementation unless the user explicitly changes the design again.

## Task 1: Add Repo Hygiene For Local Artifacts

**Files:**
- Create: `.gitignore`
- Test: `.gitignore`

- [ ] **Step 1: Write the failing ignore verification**

Use these commands before creating `.gitignore`:

```bash
git check-ignore .DS_Store docs/.DS_Store .superpowers/test || true
```

Expected: no ignored-path output because the repo does not yet have ignore rules for these files.

- [ ] **Step 2: Create `.gitignore` with only the local-noise patterns the repo currently needs**

```gitignore
.DS_Store
__pycache__/
.superpowers/
```

- [ ] **Step 3: Run ignore verification again**

Run:

```bash
git check-ignore -v .DS_Store docs/.DS_Store .superpowers/test
```

Expected: each path reports a matching ignore rule from `.gitignore`.

- [ ] **Step 4: Commit**

```bash
git add .gitignore
git commit -m "chore: ignore local presentation artifacts"
```

## Task 2: Create The Test Harness And Minimal Reveal Shell

**Files:**
- Create: `tests/test_presentation.py`
- Create: `index.html`
- Test: `tests/test_presentation.py`

- [ ] **Step 1: Write the first failing tests for file existence, title text, and Reveal bootstrap**

```python
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
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
python3 -m unittest tests/test_presentation.py -v
```

Expected: FAIL because `index.html` does not exist yet.

- [ ] **Step 3: Create the minimal `index.html` shell**

Include:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Codex: When you're done Chatting about your problems</title>
  <link rel="stylesheet" href="https://use.typekit.net/apf8ssc.css" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css" />
</head>
<body>
  <div class="reveal">
    <div class="slides">
      <section>
        <h1>Codex: When you're done Chatting about your problems</h1>
        <p>Have Codex build solutions</p>
      </section>
    </div>
  </div>
  <script type="module">
    import Reveal from 'https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.esm.js';
    Reveal.initialize({ hash: true });
  </script>
</body>
</html>
```

- [ ] **Step 4: Run the tests to verify they pass**

Run:

```bash
python3 -m unittest tests/test_presentation.py -v
```

Expected: PASS for the three shell tests.

- [ ] **Step 5: Commit**

```bash
git add index.html tests/test_presentation.py
git commit -m "feat: add reveal presentation shell"
```

## Task 3: Add Cedarville Theme Tokens, Layout Utilities, And Notes Support

**Files:**
- Modify: `index.html`
- Modify: `tests/test_presentation.py`
- Test: `tests/test_presentation.py`

- [ ] **Step 1: Extend the tests so theme and notes requirements fail first**

Add tests like:

```python
    def test_brand_tokens_exist(self):
        html = read_html()
        self.assertIn("--cu-blue: #003963;", html)
        self.assertIn("--cu-gold: #FBB93A;", html)
        self.assertIn("font-family: 'myriad-pro', sans-serif;", html)
        self.assertIn("font-family: 'minion-pro', serif;", html)

    def test_notes_plugin_and_speaker_notes_markup_exist(self):
        html = read_html()
        self.assertIn("plugin/notes/notes.esm.js", html)
        self.assertIn("<aside class=\"notes\">", html)

    def test_layout_utilities_exist(self):
        html = read_html()
        self.assertIn(".dark-slide", html)
        self.assertIn(".two-col", html)
        self.assertIn(".callout-box", html)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
python3 -m unittest tests/test_presentation.py -v
```

Expected: FAIL on missing brand token, notes plugin, and utility-class assertions.

- [ ] **Step 3: Expand `index.html` with the shared presentation system**

Implement:

```html
<style>
  :root {
    --cu-blue: #003963;
    --cu-gold: #FBB93A;
    --cu-orange: #F59536;
    --cu-white: #FFFFFF;
    --cu-gray: #E7E6E6;
  }
  .reveal { font-family: 'minion-pro', serif; color: #222; }
  .reveal h1, .reveal h2, .reveal h3 {
    font-family: 'myriad-pro', sans-serif;
    font-weight: 600;
  }
  .dark-slide { background: var(--cu-blue) !important; color: white; }
  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
  .callout-box { background: var(--cu-blue); color: white; padding: 0.75rem 1rem; }
</style>
```

And update the Reveal bootstrap:

```html
<script type="module">
  import Reveal from 'https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.esm.js';
  import RevealNotes from 'https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/notes/notes.esm.js';

  Reveal.initialize({
    plugins: [RevealNotes],
    hash: true,
    transition: 'fade',
    transitionSpeed: 'fast'
  });
</script>
```

Also add one temporary `<aside class="notes">...</aside>` block to the title slide so the notes test can pass.

- [ ] **Step 4: Run the tests to verify they pass**

Run:

```bash
python3 -m unittest tests/test_presentation.py -v
```

Expected: PASS for shell and theme tests.

- [ ] **Step 5: Commit**

```bash
git add index.html tests/test_presentation.py
git commit -m "feat: add branded reveal theme and notes support"
```

## Task 4: Implement Slides 1 Through 11 And Lock Them With Tests

**Files:**
- Modify: `index.html`
- Modify: `tests/test_presentation.py`
- Test: `tests/test_presentation.py`

- [ ] **Step 1: Add failing tests for the first half of the narrative**

Add tests that assert these strings exist in `index.html`:

```python
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
```

Also add:

```python
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
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
python3 -m unittest tests/test_presentation.py -v
```

Expected: FAIL because the first-half slides and notes do not yet exist.

- [ ] **Step 3: Implement slides 1 through 11 in `index.html`**

Build slides for:

- title
- thesis
- clarification
- objection
- knowledge-base app story
- language-abstraction reframe
- tool imagination
- prompt placeholder
- output placeholder
- tool-versus-output comparison
- why-this-matters summary

Implementation requirements for this step:

```html
<section class="dark-slide">
  <h2>Stop using AI for what you're already good at.</h2>
  <aside class="notes">Pause after this line and let the room react.</aside>
</section>

<section class="content-slide">
  <h2>Here is what I told Codex to write.</h2>
  <div class="callout-box">Prompt screenshot placeholder</div>
  <aside class="notes">Replace this box with the real prompt artifact later.</aside>
</section>

<section class="content-slide">
  <h2>Tool vs. output</h2>
  <div class="two-col">
    <div>
      <h3>LLM output</h3>
      <p>An answer you got once in chat.</p>
    </div>
    <div>
      <h3>LLM-built tool</h3>
      <p>A tool you can run again, inspect, and trust.</p>
    </div>
  </div>
  <aside class="notes">Stress independence, repeatability, and auditability here.</aside>
</section>
```

- [ ] **Step 4: Run the tests to verify they pass**

Run:

```bash
python3 -m unittest tests/test_presentation.py -v
```

Expected: PASS for all first-half slide assertions.

- [ ] **Step 5: Commit**

```bash
git add index.html tests/test_presentation.py
git commit -m "feat: add codex presentation opening and proof slides"
```

## Task 5: Implement Slides 12 Through 22 And Lock The Closing Arc With Tests

**Files:**
- Modify: `index.html`
- Modify: `tests/test_presentation.py`
- Test: `tests/test_presentation.py`

- [ ] **Step 1: Add failing tests for the second half of the presentation**

Add tests like:

```python
    def test_adoption_and_closing_copy_exist(self):
        html = read_html()
        required = [
            "So... you're interested, but you're not sure where to begin.",
            "Sigh List",
            "What in your life or work makes you sigh",
            "exam questions uploaded into Canvas",
            "chemical diagrams",
            "learning objects",
            "interlinear Bible",
            "Dr. John Delano",
            "bring your laptop",
            "bring your sigh list",
            "micahcooper@cedarville.edu",
        ]
        for phrase in required:
            self.assertIn(phrase, html)
```

And a slide-count smoke test:

```python
    def test_slide_count_is_in_expected_range(self):
        html = read_html()
        slide_count = html.count("<section")
        self.assertGreaterEqual(slide_count, 22)
        self.assertLessEqual(slide_count, 24)

    def test_key_closing_notes_exist(self):
        html = read_html()
        required_notes = [
            "Credit Artie Kuhn at Miami University here.",
            "Short handoff, then stop talking.",
            "These are examples of tool-worthy problems, not just chat prompts.",
        ]
        for phrase in required_notes:
            self.assertIn(phrase, html)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
python3 -m unittest tests/test_presentation.py -v
```

Expected: FAIL because the closing slides and full slide count are not yet present.

- [ ] **Step 3: Implement slides 12 through 22 in `index.html`**

Build slides for:

- transition to adoption
- Sigh List explanation
- Sigh List examples
- campus use cases
- pattern recognition
- audience reflection
- Dr. John Delano handoff
- re-entry
- workshops
- closing action
- final contact slide

Implementation requirements for this step:

```html
<section>
  <h2>Sigh List</h2>
  <p>What in your life or work makes you sigh?</p>
  <aside class="notes">Credit Artie Kuhn at Miami University here.</aside>
</section>

<section>
  <h2>What types of problems?</h2>
  <ul>
    <li>exam questions uploaded into Canvas</li>
    <li>chemical diagrams</li>
    <li>learning objects</li>
    <li>interlinear Bible</li>
  </ul>
  <aside class="notes">These are examples of tool-worthy problems, not just chat prompts.</aside>
</section>

<section class="dark-slide">
  <h2>Dr. John Delano</h2>
  <p>Here is someone on campus already doing this work.</p>
  <aside class="notes">Short handoff, then stop talking.</aside>
</section>
```

- [ ] **Step 4: Run the tests to verify they pass**

Run:

```bash
python3 -m unittest tests/test_presentation.py -v
```

Expected: PASS for all slide-copy and slide-count assertions.

- [ ] **Step 5: Commit**

```bash
git add index.html tests/test_presentation.py
git commit -m "feat: add codex presentation closing slides"
```

## Task 6: Enforce Single-File Delivery, Placeholder Discipline, And Notes Coverage

**Files:**
- Modify: `index.html`
- Modify: `tests/test_presentation.py`
- Test: `tests/test_presentation.py`

- [ ] **Step 1: Add failing tests for self-contained delivery and required placeholders**

Add tests like:

```python
    def test_no_local_asset_references_exist(self):
        html = read_html()
        self.assertNotIn('src="assets/', html)
        self.assertNotIn("url('assets/", html)
        self.assertNotIn('url("assets/', html)
        self.assertNotRegex(html, r'src="(?!https?://|data:|#)[^"]+"')
        self.assertNotRegex(html, r"href=\"(?!https?://|data:|#)[^\"]+\\.(png|jpg|jpeg|svg|gif|webp)\"")

    def test_prompt_and_output_placeholders_exist(self):
        html = read_html()
        self.assertIn("Prompt screenshot placeholder", html)
        self.assertIn("Output screenshot placeholder", html)

    def test_every_slide_has_speaker_notes(self):
        html = read_html()
        sections = html.count("<section")
        notes = html.count('<aside class="notes">')
        self.assertGreaterEqual(notes, sections)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
python3 -m unittest tests/test_presentation.py -v
```

Expected: FAIL if any slide is missing notes or if placeholders/self-contained rules are incomplete.

- [ ] **Step 3: Tighten `index.html` until the tests pass**

Ensure:

- every slide has an `aside.notes`
- prompt and output slides contain clearly labeled placeholders
- no local `assets/` references remain
- any fixed imagery is embedded directly in the HTML, not loaded from disk
- the deck still uses only CDN-hosted Reveal.js and Typekit dependencies

- [ ] **Step 4: Run the tests to verify they pass**

Run:

```bash
python3 -m unittest tests/test_presentation.py -v
```

Expected: PASS for the full automated smoke suite.

- [ ] **Step 5: Commit**

```bash
git add index.html tests/test_presentation.py
git commit -m "test: enforce self-contained presentation requirements"
```

## Task 7: Final Verification And Delivery Readiness

**Files:**
- Modify: `index.html` (only if verification finds issues)
- Modify: `tests/test_presentation.py` (only if verification finds coverage gaps)
- Test: `tests/test_presentation.py`

- [ ] **Step 1: Run the full automated test suite**

Run:

```bash
python3 -m unittest tests/test_presentation.py -v
```

Expected: all tests PASS.

- [ ] **Step 2: Serve the presentation locally for browser verification**

Run:

```bash
python3 -m http.server 4173
```

Expected: terminal reports `Serving HTTP on 0.0.0.0 port 4173`.

- [ ] **Step 3: Verify the deck manually in the browser**

Check:

- slide navigation works
- theme and typography load
- dark slides and light slides both look intentional
- notes view opens and shows speaker notes
- prompt/output placeholders are visually intentional
- the tool-versus-output slide reads clearly at presentation size

- [ ] **Step 4: If manual verification finds issues, fix them and rerun the automated suite**

Run after any fix:

```bash
python3 -m unittest tests/test_presentation.py -v
```

Expected: PASS remains true after the polish edits.

- [ ] **Step 5: Commit the finished deck**

```bash
git add .gitignore index.html tests/test_presentation.py
git commit -m "feat: deliver codex reveal presentation"
```

## Execution Notes

- Use `@superpowers:subagent-driven-development` to execute this plan.
- Follow `@superpowers:test-driven-development` during implementation of each task.
- Before claiming success, run `@superpowers:verification-before-completion`.
- Do not introduce a build system unless implementation hits a concrete blocker that the current three-file structure cannot solve.
- Do not change the approved title, subtitle, or tools-first framing without explicit user approval.
