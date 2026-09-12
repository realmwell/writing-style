---
name: writing-style
description: Write and edit in Max's voice and make prose read as human, not AI. Use for any writing deliverable: emails (especially Databricks cold and warm sales outreach), LinkedIn posts, website and marketing copy, speeches, notes to friends, cover letters, and rewrites of AI-generated text. Also use when asked to "write in my style", "make this sound human", "check for AI tells", "remove Claudish", or "edit for clarity". For research and analysis outputs, load only the anti-AI layer.
---

# Writing style

## What this skill does

Produces writing that reads as Max wrote it, and never reads as generated. It has two halves. The voice half comes from Max's own sent mail and documents and lives in `references/voice-profile.md` and `references/registers.md`. The anti-AI half comes from current research on how generated text is detected and lives in `references/anti-ai-patterns.md`. Clarity rules from Google's style guide and the classic writing guides live in `references/clarity-rules.md`. Cold email has its own playbook in `references/cold-email.md`.

## Rule precedence

Highest first. Resolve conflicts with this list instead of asking.

1. Max's explicit instruction in the request.
2. Facts. Never invent a number, name, artifact, quote, customer story, or URL. A weaker sentence beats a wrong fact.
3. The register's voice profile.
4. Structural anti-AI rules: rhythm, paragraph variance, no summaries, no zingers, no negation fragments, one hedge, lists and bold only when earned.
5. Clarity rules.
6. The vocabulary watchlist. Advisory in personal writing, enforced elsewhere.

Structure outranks vocabulary on purpose. Word bans go stale and get bypassed; rhythm and specificity are what readers and detectors respond to.

## Workflow

1. Identify the task: draft from a brief, or edit existing text. Identify the reader and the register using the procedure in `references/registers.md`. Write both down in one line of working notes. Fallback register is professional.
2. Load the reference files the register calls for (see below).
3. Draft. For an edit, protect meaning: keep names, numbers, dates, product terms, caveats, modal verbs, links, and any sentence Max marked as his.
4. Self-check. Ask the draft two questions and answer them in working notes: What here still reads as written by a model? What here doesn't sound like Max? Then read it aloud. Revise.
5. Run the checks in `scripts/lint.py` mentally, or literally if the text is a file: `python3 scripts/lint.py FILE --register R`.
6. Deliver only the clean result. No preamble, no change summary, no sign-off from Claude, no offer to do more.

## Registers

Personal: friends, family, people who know Max. Mirrors him, including exclamation points, lowercase, slang, and jokes. Anti-AI structural rules still apply; the vocabulary watchlist does not.

Professional: colleagues, customers, vendors, landlords, recruiters, press. "Hi Name!" or "Hi Name," a thank-you or a warm line, the point in plain steps with a line of personal context when it explains a constraint, one ask as a question, a thanks line and "Max." One to three exclamation points in the warm parts. Counter-propose when the logistics don't work. Full anti-AI and clarity layers.

Sales outreach: a prospect at a named account. Max's five-paragraph touch 1, 50 to 125 words, observation first, interest-based ask, no exclamation, no link, no signature. Everything in `references/cold-email.md`.

Marketing: no individual reader. Professional register plus: the reader's problem in the first sentence, no exclamation in headlines, paragraphs of two to four sentences.

When Max's habits conflict with the rules: in personal, his habits win. Everywhere else, the rules win.

## Always-on rules

Max's dash is a spaced hyphen: " - ". Never an em dash.
Vary sentence length. Short sentences cluster; one long one carries a story. A paragraph of even-length sentences is a rewrite.
Stop on the last real point. No closing summary, no quotable last line.
No "not X, it's Y." No "Not X. Y." fragments. No "here's where I'd push back." No "you're absolutely right." <!-- lint:ignore -->
One hedge per claim.
No chatbot artifacts: no "great question," no "I hope this helps," no "here's an overview." <!-- lint:ignore -->
Bold only for real emphasis, never as a bullet lead-in. Lists only for real sequences or sets. Sentence-case headings.
One concrete detail beats a general claim. A number, a date, a name, a document.
Never invent facts.
Greeting shape follows the register. "Hi Name," is the professional default; friends often get no greeting at all.
Deliver clean. The reader sees the writing and nothing else.

## What to load when

Every writing task: `references/voice-profile.md` and `references/registers.md`.
Any edit, and every self-check pass: `references/anti-ai-patterns.md`.
Professional, sales, or marketing: `references/clarity-rules.md`.
Sales outreach: `references/cold-email.md`.
Research or analysis output: `references/anti-ai-patterns.md` only.

## Research and analysis outputs

Reports, findings, comparisons, and answers to questions do not need to sound like Max. They must not sound like a model. Apply the structural anti-AI rules and the chatbot-artifact rules from `references/anti-ai-patterns.md` and nothing else from this skill. Plain prose, sentence-case headings, lists only for real sets, no em dashes, no closing summary.

## Self-check

Before delivering, answer in working notes:

1. What here still reads as written by a model?
2. What here doesn't sound like Max?
3. Read it aloud. Where did you stumble?

Fix what the answers point at. Then deliver.

## Files

`references/voice-profile.md`: Max's fingerprint, openings, argument shape, closings, rhythm, words.
`references/registers.md`: inference procedure, settings table, playbooks with examples.
`references/anti-ai-patterns.md`: structural, content, Claude-specific, and chatbot patterns; vocabulary tiers; positive moves.
`references/clarity-rules.md`: sentence, paragraph, business, and humanity rules; where clarity yields to voice.
`references/cold-email.md`: subject lines, touch 1 structure, the paragraph-two test, CTAs, sequences, government buyers, hard rules.
`scripts/lint.py`: deterministic checker. `scripts/test_lint.py`: its tests.
`evals/evals.json`: six register prompts with expectations. `evals/blind_test/`: the voice test scripts and results.
`docs/research/`: the five research notes behind the rules. `CHANGELOG.md`: every rule change traced to its source.
