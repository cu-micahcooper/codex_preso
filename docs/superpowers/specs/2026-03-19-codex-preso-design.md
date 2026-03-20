# Codex Reveal Presentation Design

Date: 2026-03-19
Project: `codex_preso`
Output target: single-file Reveal.js presentation at `index.html`

## Summary

Create a Cedarville University branded Reveal.js presentation that introduces Codex to faculty and staff in a campus-wide setting where most attendees are familiar with ChatGPT but not Codex. The talk should run about 50 minutes, use a provocative and funny voice, remain accessible to non-programmers, and convert attendees into workshop participants who bring a laptop and a real problem to solve.

The presentation should frame Codex primarily as a way to build practical tools and workflows, not as a coding product for software professionals. The core conceptual distinction is between one-off LLM output and a durable tool that can be created with LLM help, then run independently, repeatably, and auditably after it exists. The deck should start with a sharp thesis, answer the "I do not code" objection quickly, prove the value with a concrete app story and prompt-to-output example, explain the difference between generated output and generated tools, expand into campus-relevant use cases, hand off cleanly to Dr. John Delano for a separate live demo, and close with a practical call to action built around the "sigh list" exercise and workshop attendance.

## Audience And Context

- Audience: Cedarville University faculty and staff
- Room type: campus-wide presentation with mixed interest levels
- Prior familiarity: most attendees likely use ChatGPT already, but few if any use Codex
- Duration: about 50 minutes total, including discussion pacing and the Dr. John Delano segment
- Delivery style: presenter-led talk with speaker notes for transitions, stories, jokes, and pacing

## Primary Goals

1. Reframe Codex from "coding tool" to a practical way to build useful tools in plain English.
2. Make non-programmers feel that Codex is relevant to their actual work.
3. Show at least one credible story where Codex produced a useful tool quickly.
4. Explain the difference between a one-off LLM answer and a repeatable, auditable tool.
5. Surface campus-relevant categories of problems that faculty and staff could solve.
6. Convert attendees into workshop participants.
7. Encourage attendees to begin a "sigh list" before the workshop.

## Call To Action

The closing conversion should be explicit and concrete:

1. Start a sigh list this week by writing down recurring frustrations, friction, and tedious work.
2. Bring a laptop to a Codex workshop.
3. Bring one real problem from that list so the workshop can help attack it immediately.

Workshop attendance and sigh-list creation are equally important outcomes.

## Tone And Voice

The deck should preserve the presenter's voice:

- Provocative
- Funny
- Confident
- Plainspoken
- Non-technical in wording, even when describing technical capability

The tone should not become generic institutional marketing. It should still feel appropriate for a broad campus audience, but the opener should have some edge. Every sharp line should be followed by enough evidence or explanation to earn it.

Terminology should reinforce the real message:

- Prefer `tools`, `workflows`, `systems`, and `software that runs on its own`
- Use `programmer` or `programming` sparingly, mainly in the audience objection and at most one additional rhetorical moment
- Explicitly teach that the goal is not merely "AI made something for me once" but "I now have a tool I can run again, inspect, and trust"

## Branding And Visual Direction

Use the local Cedarville Reveal presentation conventions from `/Users/micahcooper/.agents/skills/reveal-presentation-builder/SKILL.md`.

### Brand Tokens

```css
:root {
  --cu-blue: #003963;
  --cu-gold: #FBB93A;
  --cu-orange: #F59536;
  --cu-white: #FFFFFF;
  --cu-gray: #E7E6E6;
}
```

### Typography

- Headings: `myriad-pro`, sans-serif, weight 600
- Body: `minion-pro`, serif
- Adobe Typekit source: `https://use.typekit.net/apf8ssc.css`

### Visual Approach

- Use dark blue Cedarville section/thesis slides for emphasis.
- Use light, uncluttered content slides for examples and explanation.
- Use a few visually stronger proof slides with large statements, prompt panels, screenshot frames, or two-column comparisons.
- Keep content density low. Most slides should do one job.
- Favor bold statements, pull quotes, and clean layouts over dense bullet lists.

## Presentation Architecture

Recommended narrative frame: "You already use AI. Now build tools with it."

The deck should move through seven stages:

1. Hook
2. Objection and reversal
3. Proof
4. Tool distinction
5. Campus problem space
6. Social proof and handoff
7. Action

This is the governing structure for both slide order and speaker notes.

## Slide Plan

Target roughly 21 slides. Exact count can vary by one or two if pacing improves.

### 1. Title Slide

- Purpose: establish topic and Cedarville context
- Recommended title: `Codex: When you're done Chatting about your problems`
- Recommended subtitle: `Have Codex build solutions`
- Visual treatment: dark slide with Cedarville branding
- Speaker notes: brief setup, name the room, and set expectation that this is practical rather than theoretical

### 2. Thesis Slide

- Main line: `Stop using AI for what you're already good at.`
- Purpose: open with a provocative framing statement
- Visual treatment: very sparse dark slide
- Speaker notes: land the line, pause, and let the room react before explaining it

### 3. Clarification Slide

- Main line: `Use it for what you're not good at.`
- Include the joke that this probably includes coding because the audience does not work for the presenter
- Purpose: make the thesis funny and concrete
- Visual treatment: large typography, minimal text

### 4. Objection Slide

- Main line: `I don't code. I don't want to code.`
- Purpose: articulate the audience's likely resistance in their own voice
- Speaker notes: acknowledge the objection respectfully and set up the reversal

### 5. Knowledge-Base App Story

- Content: in two days, the presenter built an app that scours the knowledge base, analyzes article quality, proposes improvements, and uploads them
- Purpose: offer a concrete story of practical institutional value
- Layout: one strong statement plus 3-4 concise supporting points
- Speaker notes: emphasize that the value is the solved workflow, not the code itself

### 6. Language-Abstraction Reframe

- Main line: the presenter has programmed in many languages and has no idea what language Codex used because they never looked
- Purpose: break the assumption that using Codex requires code literacy
- Speaker notes: the real change is that implementation details can become secondary to clear intent when the desired outcome is a working tool

### 7. Tool Imagination Slide

- Main line: `What tools could you have if you could describe what you wanted in plain English?`
- Purpose: shift from the presenter's story to the audience's imagination
- Visual treatment: clean, high-contrast, contemplative slide

### 8. Prompt Slide

- Heading: `Here is what I told Codex to write.`
- Purpose: show the input side of the process
- Layout: large screenshot or styled text panel
- Notes: the implementation should reserve a clean screenshot region so the real prompt can be dropped in later without redesigning the slide

### 9. Output Slide

- Heading: `Here is what it gave me.`
- Purpose: show the resulting artifact or interface
- Layout: large screenshot frame or split view
- Notes: use a clear placeholder if the real artifact is not yet present at implementation time, but the layout must be ready for easy replacement

### 10. Tool Versus Output Slide

- Purpose: teach the deck's key conceptual distinction
- Message: an LLM answer is a one-time output, but a generated tool can be run again after it has been created
- Required points:
  - the tool continues to run independently of the chat session once built
  - the behavior is repeatable on the next run
  - the steps and outputs can be inspected and audited
  - the value is not just novelty but dependable reuse
- Layout: side-by-side comparison or strong two-column contrast

### 11. Why This Matters Slide

- Purpose: interpret the proof for the audience
- Message: this is about turning a plain-English description into a working tool fast enough to matter and stable enough to use again
- Layout: one key statement with 2-3 supporting lines

### 12. Transition Slide

- Main line: `So... you're interested, but you're not sure where to begin.`
- Purpose: pivot from proof to adoption

### 13. Sigh List Slide

- Introduce Artie Kuhn at Miami University and the "Sigh List" idea
- Message: write down what in your life or work makes you sigh
- Purpose: give the audience a practical starting method
- Speaker notes: credit the source clearly and keep the explanation simple

### 14. Sigh List Examples Slide

- Purpose: make the exercise concrete for faculty and staff
- Include representative examples of routine frustrations, bottlenecks, repetitive formatting, data wrangling, or content transformation work
- Avoid fake specificity; keep examples plausible and recognizable

### 15. Campus Use Cases Slide

- Include:
  - exam questions uploaded into Canvas
  - chemical diagrams
  - learning objects
  - interlinear Bible
- Purpose: show breadth across academic and administrative work
- Layout: grid or four-card slide

### 16. Pattern Recognition Slide

- Purpose: connect the use cases into one idea
- Message: Codex is useful where work involves boring complexity, tedious transformation, repetitive structure, or tasks that benefit from a repeatable tool rather than another manual pass
 
### 17. Audience Reflection Slide

- Main line: `What in your work makes you sigh?`
- Purpose: brief live reflection moment and setup for the workshop CTA

### 18. Dr. John Delano Handoff Slide

- Purpose: transition clearly to a separate live segment
- Naming requirement: always refer to him as `Dr. John Delano`
- Message: here is someone on campus already doing this work
- Layout: clean handoff slide, not crowded with details
- Speaker notes: short verbal intro, then hand over

### 19. Re-entry Slide

- Purpose: after the Dr. John Delano segment, re-anchor the room if needed
- Suggested line: `So where do you start?`
- If the live flow does not need a re-entry, this slide may be omitted

### 20. Workshops Slide

- Content: drop-in Codex workshops already exist, there are over a dozen people ready to help, and attendees can bring questions or ideas
- Tone: lightly self-aware, including the line about maybe nobody coming and the team being lonely if that still lands well in notes
- Purpose: reduce activation energy by showing help already exists

### 21. Closing Action Slide

- Main message:
  - bring your laptop
  - bring your sigh list
  - bring one real problem
- Purpose: explicit next step
- Visual treatment: high-contrast slide with minimal text

### 22. Final Slide

- Cedarville branded closing slide
- Presenter line: `Micah Cooper`
- Contact line: `micahcooper@cedarville.edu`
- Include workshop-oriented closing message rather than a generic thank-you if that serves the talk better

## Speaker Notes

Speaker notes are required.

They should carry:

- transitions between sections
- comedic timing and phrasing
- the fuller version of the knowledge-base app story
- how to frame the prompt/output example
- how to explain the difference between generated output and generated tools in plain language
- handoff language to Dr. John Delano
- the workshop invitation and sigh-list explanation

Slides should remain sparse even when notes are detailed.

## Assets And Content Strategy

The implementation should assume three asset categories:

1. Cedarville logo assets matching the local Reveal skill conventions
2. Optional screenshot or text artifacts for the prompt and output slides
3. No complex build assets or media dependencies unless they become necessary later

### Logo Handling

The final deliverable is a single-file presentation. If logos are used, they should be embedded directly in `index.html` rather than referenced as external local files. If a suitable logo asset is not available at implementation time, prefer a logo-free branded layout over shipping broken references.

### Placeholder Strategy

The prompt and output slides must be implementation-ready even if the final screenshots are not yet available. Use clearly marked placeholder regions that can be replaced later without changing slide structure, typography, spacing, or notes.

This is not a request for fake demo content. It is a layout requirement so the deck can be built now and finalized later.

## Technical Requirements

- Output format: single self-contained `index.html`
- Framework: Reveal.js loaded via CDN
- Notes plugin enabled
- Adobe Typekit stylesheet included
- Cedarville colors and type applied consistently
- Any required logos or fixed imagery embedded into the HTML rather than referenced by missing local paths
- No build system required unless implementation discovers a concrete need
- Include at least one slide that clearly distinguishes one-off LLM output from a repeatable tool that runs independently after creation

## Testing And Verification Requirements

Before calling the presentation complete, verify at minimum:

1. `index.html` opens locally without missing assets
2. Reveal navigation works
3. Speaker notes view works
4. Typography and brand colors load correctly
5. Slides remain legible at projector-style widescreen dimensions and standard laptop viewing sizes
6. No broken local asset references remain

If screenshots are absent and placeholders are used, verify that the placeholders are visually intentional rather than obviously unfinished.

## Out Of Scope

- Building the actual knowledge-base app described in the story
- Implementing live demo tooling inside this repo
- Creating a multi-file slide system or build pipeline without a demonstrated need
- Turning the talk into a detailed Codex training workshop deck

## Risks And Mitigations

### Risk: The opening feels glib or too sharp

Mitigation: follow provocative lines immediately with a concrete story and practical examples.

### Risk: Audience assumes Codex is only for programmers

Mitigation: place the objection slide early, use "programmer" language sparingly, and keep returning to tools, workflows, and repeatable outcomes.

### Risk: Audience hears "AI made something once" rather than "I now have a dependable tool"

Mitigation: add an explicit tool-versus-output slide and reinforce independence, repeatability, and auditability in both slides and notes.

### Risk: Prompt/output artifacts are not ready when the deck is built

Mitigation: build those slides around swappable placeholders and strong speaker notes.

### Risk: The Dr. John Delano segment feels disconnected

Mitigation: give it a dedicated handoff slide and optional re-entry slide.

## Implementation Notes For Planning

- Use the Cedarville Reveal builder conventions as the baseline visual system.
- Keep the number of custom slide patterns small and reusable.
- Prefer explicit slide-specific notes over overloading slide text.
- Treat the handoff to Dr. John Delano as part of the narrative, not an interruption.
- Optimize for clarity in a live room, not for reading the HTML source.
