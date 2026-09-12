# writing-style v2 Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the v1 writing-style skill with a layered v2 that writes like Max and not like a model, folds in the humanizer, and ships to Claude Code, claude.ai, and the plugin.

**Architecture:** Short always-loaded SKILL.md plus five on-demand reference files, a deterministic lint script, rewritten evals, and a blind voice test. Prose files are written from the spec, the five research notes, and the private corpus profile. Code files are built test-first.

**Tech Stack:** Markdown skill files (Claude Code skill format, YAML frontmatter), Python 3.9+ standard library only (no pip installs), pytest for tests if available (falls back to `python3 -m unittest`).

**Spec:** `docs/superpowers/specs/2026-09-12-writing-style-v2-design.md`

**Division of labor:** Tasks 2 through 7 and 9, 11 are prose and depend on the private corpus profile at `~/writing-style/corpus/`; the main session writes them. Tasks 8 and 10 are code; dispatch a fresh subagent per task. Task 12 verification runs in the main session.

**Privacy rule for every task:** nothing from `~/writing-style/corpus/` or from any Drive document text is copied into a file under the repo. Examples are public-safe: Max's public writing, paraphrase, or invented text matching measured patterns.

**Commits:** Max's CLAUDE.md says commit only when asked. Each task ends with a "stage for commit" step, not a commit. Max triggers the commit and push at the end.

---

## Chunk 1: Repo layout and reference files

### Task 1: Clean the repo and lay out v2 directories

**Files:**
- Delete: `references/api_reference.md`, `scripts/example.py`, `assets/example_asset.txt`, `assets/`
- Create: `.gitignore`, `docs/research/` (five files copied), `dist/.gitkeep`

- [ ] **Step 1: Delete placeholders**

```bash
cd /Users/maxmac/writing-style/writing-style
git rm -q references/api_reference.md scripts/example.py assets/example_asset.txt
rmdir assets 2>/dev/null; ls
```
Expected: `SKILL.md docs evals references scripts` (references and scripts now empty).

- [ ] **Step 2: Add .gitignore**

```
dist/*.zip
__pycache__/
.pytest_cache/
*.pyc
evals/blind_test/private/
```

- [ ] **Step 3: Copy research notes into docs/research and scrub**

```bash
mkdir -p docs/research dist && touch dist/.gitkeep
cp ~/writing-style/research/0[1-5]-*.md docs/research/
grep -n -i "maxwell.greenberg\|@gmail\|@databricks" docs/research/*.md || echo CLEAN
grep -c "—" docs/research/*.md
```
Expected: `CLEAN`. Em dash counts may be nonzero in notes 02 and 05 (inside quoted examples); leave quoted examples, but replace any em dash in the notes' own prose with a comma or " - ".

- [ ] **Step 4: Stage**

```bash
git add -A && git status --short
```

### Task 2: references/anti-ai-patterns.md

**Files:**
- Create: `references/anti-ai-patterns.md`
- Source: `docs/research/02-ai-tells-wikipedia-audit.md` section 4 (master list), `docs/research/03-ai-detection-and-claudish.md` (tells and positive rules), humanizer's "add soul" section paraphrased.

- [ ] **Step 1: Write the file** with these sections, in this order, under 260 lines:
  1. `## How to use this file` (3 lines: load on edit and self-check; structure outranks vocabulary; one hit is not proof, clusters are).
  2. `## Structural patterns` : the 14 structural rules from spec section 9, each as: name in bold at line start is NOT allowed; use a plain sentence per rule, then one before/after pair on the next two lines prefixed `Before:` / `After:`. After examples must sound like a person.
  3. `## Content patterns` : significance inflation, vague attribution, notability namedropping, participial tails, formulaic challenges section, vague connection phrasing.
  4. `## Claude-specific tics` : the list from note 03 (contrastive binary, negation fragment, aphoristic closer, anticipate-and-rebut, stacked hedges, over-validation, forced metaphor, bolded lead-ins, one-line zinger paragraphs, "genuinely/honestly/quietly").
  5. `## Chatbot artifacts` : correspondence framing, sycophancy, generic upbeat closer, knowledge-cutoff hedge (marked legacy), model debris tags to grep.
  6. `## Vocabulary watchlist` : three tiers exactly as spec section 9, each tier one comma-separated line, with a one-line rule on enforcement per register.
  7. `## Positive moves` : the 16 "do this" rules from note 03, one line each, no ratings.
  8. `## Self-check prompts` : the two questions from spec section 7 plus "Read it aloud."

- [ ] **Step 2: Lint the file by hand**

```bash
grep -c "—" references/anti-ai-patterns.md
grep -n "^\s*[-*] \*\*" references/anti-ai-patterns.md | head
wc -l references/anti-ai-patterns.md
```
Expected: em dash count 0 outside `Before:` lines; no bold-header bullets; under 260 lines.

- [ ] **Step 3: Stage** `git add references/anti-ai-patterns.md`

### Task 3: references/clarity-rules.md

**Files:**
- Create: `references/clarity-rules.md`
- Source: `docs/research/01-google-style-guide.md` transferable rules; `docs/research/04-classic-guides-and-amazon.md` top 25 and "what the guides add".

- [ ] **Step 1: Write the file**, under 120 lines: `## Applies to` (professional, sales, marketing; off in personal), `## Sentence rules` (Google: second person, present tense, active, condition first, lead with the point, short sentences, contractions, plain word, cut just/simply/easily, "lets you" not "allows you to", spell out abbreviations), `## Paragraph and document rules` (topic sentence first, one idea per paragraph, sentence-case headings, lists only for sequences or sets, descriptive link text), `## Business rules` (Amazon: adjectives to data, so-what test, no weasel words, under 30 words, anticipate objections; Bernoff: point in the first sentence), `## Humanity rules` (Zinsser and Graham: write like you talk, read aloud, one consistent tense and person, have a stake, end on the last real point, not a summary), `## Where clarity yields to voice` (the eight conflicts from note 01, each resolved per register).

- [ ] **Step 2: Lint by hand** as in Task 2. Expected: 0 em dashes, under 120 lines.

- [ ] **Step 3: Stage.**

### Task 4: references/cold-email.md

**Files:**
- Create: `references/cold-email.md`
- Source: `docs/research/05-cold-email-craft.md`; Max's outreach method (five-paragraph touch 1, paragraph-two test, artifact subject lines, one verified Databricks customer source, four-touch sequence, hard rules on fabrication). Do not copy Appendix A of Max's prompt (a real customer email).

- [ ] **Step 1: Write the file**, under 200 lines: `## When this loads`, `## Before drafting` (required inputs: recipient, account context, sender line, optional angle and financial hook; refuse to draft without a recipient and account context), `## Subject lines` (rules and 6 examples with placeholder artifacts), `## Touch 1 structure` (Max's five paragraphs, with the interest-based CTA as default and the structured 30/45-minute close as the named alternative), `## The paragraph-two test`, `## Openers` (rules, 4 examples), `## CTAs` (rules, 4 examples), `## Touches 2 to 4`, `## Government and regulated buyers`, `## Hard rules` (no invented facts, the customer source verified live even when not linked, no link in touch 1 unless Max asks, no flattery opener, no "hope this finds you well", no exclamation, no emoji, touch 1 is 50 to 125 words by default and up to 200 for Max's full structure), `## Deliverability words to avoid`, `## LinkedIn follow-up` (300 characters).

- [ ] **Step 2: Lint by hand.** Expected: 0 em dashes; every example subject line under 6 words.

- [ ] **Step 3: Stage.**

### Task 5: references/voice-profile.md

**Files:**
- Create: `references/voice-profile.md`
- Source: `~/writing-style/corpus/analyze.py` output and the opening-line analysis (private); Max's public writing for examples.

- [ ] **Step 1: Refresh the numbers**

```bash
cd ~/writing-style/corpus && python3 analyze.py > profile_$(date +%Y%m%d).txt && head -40 profile_*.txt
```

- [ ] **Step 2: Write the file**, under 160 lines: `## Who Max is on the page` (six sentences: warm, direct, specific, opinionated, funny with friends, formal but not stiff with strangers; ex-consultant and AWS, now Databricks AE; urbanist and political reader; likes primary sources), `## Fingerprint` (a table: habit, what Max does, measured rate as a rounded range, e.g., "exclamation point in professional email: roughly 4 in 10 messages"), `## How Max opens` (greeting shapes and the first move after the greeting, with 5 invented example openings per register), `## How Max builds an argument` (observation, plain-step reasoning, one ask; two invented examples), `## How Max closes` (sign-off table), `## Rhythm` (median and burstiness, one-liners, long story sentences), `## Words Max uses and avoids` (uses: "so sorry", "thanks so much", "would love to", "happy to", "hope you're well", "worth", "let's", "hang soon"; avoids: corporate filler, AI-tell vocabulary in email), `## Things that are not Max` (10 lines: no "I hope this finds you well", no "reach out", no em dashes, no triads, no closing summary, no "great question", no bold lead-ins, no "leverage"), `## Public examples` (two short passages from Max's public writing on the DC Permit Navigator site or his LinkedIn, cited).

- [ ] **Step 3: Privacy check**

```bash
cd /Users/maxmac/writing-style/writing-style
grep -n -i -f <(python3 -c "import json,glob;print('\n'.join(sorted({t.split('@')[0] for f in glob.glob('/Users/maxmac/writing-style/corpus/sent_*.jsonl') for l in open(f) for t in json.loads(l).get('to',[]) if '@' in t and 'maxwell' not in t})))") references/voice-profile.md || echo "NO CORRESPONDENT NAMES"
```
Expected: `NO CORRESPONDENT NAMES`.

- [ ] **Step 4: Stage.**

### Task 6: references/registers.md

**Files:**
- Create: `references/registers.md`
- Source: spec section 5 table and habit-vs-rule resolution.

- [ ] **Step 1: Write the file**, under 140 lines: `## Inference procedure` (the five ordered rules from spec section 5; fallback professional; state the guess in working notes only), the settings table from the spec, then a `## Playbook` for personal, professional, and sales outreach with: reader, shape (opening, body, close), what to load, five-line example in that register (invented), and the three most common mistakes. Marketing gets a four-line note (professional plus its three rules), no playbook.

- [ ] **Step 2: Lint by hand. Step 3: Stage.**

### Task 7: SKILL.md

**Files:**
- Modify: `SKILL.md` (full rewrite)

- [ ] **Step 1: Write frontmatter**

```yaml
---
name: writing-style
description: Write and edit in Max's voice and make prose read as human, not AI. Use for any writing deliverable: emails (especially Databricks cold and warm sales outreach), LinkedIn posts, website and marketing copy, speeches, notes to friends, cover letters, and rewrites of AI-generated text. Also use when asked to "write in my style", "make this sound human", "check for AI tells", "remove Claudish", or "edit for clarity". For research and analysis outputs, load only the anti-AI layer.
---
```

- [ ] **Step 2: Write the body**, under 190 lines, sections in order: `## What this skill does` (4 lines), `## Rule precedence` (spec section 6, six lines), `## Workflow` (spec section 7, six steps), `## Registers` (one paragraph each plus the fallback; point to references/registers.md), `## Always-on rules` (12 lines max: the dash rule, no em dash, no closing summary, no negation fragments, burstiness, one hedge, no chatbot artifacts, no bold lead-ins, lists only for sets, sentence-case headings, never invent facts, deliver clean only), `## What to load when` (spec section 4 loading rules), `## Research and analysis outputs` (3 lines), `## Self-check` (the two questions and read-aloud), `## Files` (one line per reference, script, eval).

- [ ] **Step 3: Self-test the skill file with its own rules**

```bash
grep -c "—" SKILL.md; grep -n "^\s*[-*] \*\*" SKILL.md; wc -l SKILL.md
grep -n -i -E "comprehensive|robust|leverage|delve|seamless|ruthless" SKILL.md
```
Expected: `0`, no matches, under 190 lines, no vocabulary hits.

- [ ] **Step 4: Stage.**

## Chunk 2: Lint script, evals, blind test

### Task 8: scripts/lint.py (subagent, test-first)

**Files:**
- Create: `scripts/lint.py`, `scripts/test_lint.py`

Behavior: `python3 scripts/lint.py FILE [--register personal|professional|sales|marketing]` reads a text or markdown file, prints one finding per line as `LEVEL: message (line N)`, prints a summary line, exits 1 if any `ERROR`, else 0. Default register professional.

Checks and levels:
- `ERROR` em dash present (any register).
- Tier A words (emphasizing, enhance, highlighting, showcasing, matched as word stems: emphasiz, enhanc, highlight, showcas): `ERROR` outside personal, `INFO` in personal.
- Tier B words (leverage, foster, underscore, boast, garner, bolster, streamline, navigate, elevate, unveil, unlock, harness, interplay, pivotal, crucial, vital, robust, comprehensive, seamless, transformative, groundbreaking, cutting-edge, innovative, holistic, multifaceted, nuanced, enduring, "align with", "associated with"): `ERROR` in sales and marketing, `WARN` in professional, nothing in personal.
- Tier C words (delve, tapestry, testament, meticulous, landscape, intricate, realm, vibrant): `WARN` when 2 or more distinct ones appear, any register except personal.
- Unconfirmed Claude words (genuinely, honestly, quietly, "the real", "chef's kiss", "load-bearing"): `WARN` outside personal.
- `WARN` two or more hedge words in one sentence (may, might, could, perhaps, possibly, arguably, somewhat, largely, tends to, in some sense, sort of, kind of, generally, almost, I think, it seems), outside personal.
- `ERROR` exclamation point in sales; `WARN` when more than 1 in professional or marketing; never flagged in personal.
- `ERROR` regex `\bnot (just|only|merely) [^.]{1,60}, (it's|it is|but) ` and `(^|\. )Not [^.]{1,40}\. [A-Z]` (negation fragment) outside personal; `WARN` in personal.
- `WARN` closing-summary phrases in the last paragraph: "in summary", "in conclusion", "to sum up", "overall,", "at the end of the day", "the bottom line".
- `WARN` chatbot artifacts anywhere: "great question", "you're absolutely right", "i hope this helps", "let me know if", "here is a", "here's a", "certainly!", "of course!".
- `WARN` bold lead-in bullets: lines matching `^\s*[-*]\s+\*\*[^*]+\*\*:?`.
- `WARN` title-case headings: `^#+ ` lines where more than half of words of 4+ letters are capitalized.
- `WARN` low burstiness: sentence-length standard deviation under 6 when there are 6 or more sentences.
- `WARN` uniform paragraphs: 4 or more paragraphs whose word counts are all within 20% of the mean.
- `ERROR` model debris: `contentReference`, `oaicite`, `[cite:`, `grok_card`, `【`.
- `WARN` spam triggers in sales only: "free", "guarantee", "act now", "risk-free", "no obligation", "buy now", "winner".
- `INFO` word count, sentence count, mean and stdev sentence length.

- [ ] **Step 1: Write failing tests** in `scripts/test_lint.py` using `unittest`. One test per check, using small inline strings written to a temp file, asserting on `lint.run(text, register)` return value (a list of `(level, message, line)` tuples) so tests don't shell out. Include a test that `run()` on a clean professional paragraph returns no ERROR or WARN.

- [ ] **Step 2: Run** `python3 -m unittest scripts/test_lint.py -v`. Expected: ImportError or failures.

- [ ] **Step 3: Implement** `lint.py` with `run(text: str, register: str = "professional") -> list[tuple[str, str, int]]` and a `main()` that parses args, reads the file, prints findings, and sets the exit code. Standard library only.

- [ ] **Step 4: Run tests.** Expected: all pass.

- [ ] **Step 5: Run the linter on every skill file**

```bash
for f in SKILL.md references/*.md; do echo "== $f"; python3 scripts/lint.py "$f" --register professional | tail -3; done
```
Expected: no ERROR lines except inside `Before:` example lines, which the linter must skip (lines starting with `Before:` are exempt; implement and test this).

- [ ] **Step 6: Stage** `git add scripts/lint.py scripts/test_lint.py`

### Task 9: evals/evals.json

**Files:**
- Modify: `evals/evals.json` (full rewrite)

- [ ] **Step 1: Write six evals**, ids 1 to 6, each with `prompt`, `register`, `expected_output` (one line), and `expectations` (5 to 8 checkable strings). Prompts: (1) personal: reply to a friend who sent a link about DC housing policy; (2) vendor: ask a property manager to schedule a repair before winter; (3) professional: introduce two contacts by email for a job referral; (4) sales: touch-1 cold email to a federal deputy CIO given a placeholder OIG finding and an open requisition; (5) marketing: a 90-word "what this is" paragraph for a civic web tool; (6) edit: rewrite a supplied 120-word AI-sounding paragraph (include the paragraph in the prompt). Expectations must include presence checks: greeting shape, one ask, a specific detail, sentence-length variety, register-appropriate exclamation use, and the register-specific sign-off.

- [ ] **Step 2: Validate JSON** `python3 -c "import json;json.load(open('evals/evals.json'))"`.

- [ ] **Step 3: Stage.**

### Task 10: evals/blind_test (subagent for harness; main session runs the judge)

**Files:**
- Create: `evals/blind_test/build_pairs.py`, `evals/blind_test/README.md`, `evals/blind_test/results.md`
- Private, gitignored: `evals/blind_test/private/`

- [ ] **Step 1: Write `build_pairs.py`** (standard library). Subcommands: `select` reads the corpus JSONL files under `~/writing-style/corpus/` (glob `sent_*.jsonl`), picks 20 messages with `is_reply` true, `context` non-empty, body 20 to 200 words, `to_self` false, at most 2 per first recipient, spread across years, and writes `private/prompts.jsonl` (id, register guess from recipient domain, subject, context, real body) and `private/prompts_only.jsonl` (same minus real body). `shuffle --seed N` reads `private/prompts.jsonl` and `private/generated.jsonl` (id, body) and writes `private/pairs_shuffled_N.jsonl` (pair_no, A, B) plus `private/key_N.json` (pair_no to "A" or "B" for the real one). `score --seed N private/judge_N.jsonl` reads judge lines (pair_no, answer, reason) and prints accuracy and the reasons. Add unit tests for the selection filter, the shuffle key, and scoring in `evals/blind_test/test_build_pairs.py`, using synthetic records in a temp directory.

- [ ] **Step 2: Generate replies.** Main session: for each prompt, invoke the v2 skill to write Max's reply from subject and context only. Save to `private/generated.jsonl`.

- [ ] **Step 3: Judge, twice.** `build_pairs.py shuffle --seed N --sanitize` (sanitize strips addresses, phones, links, forwarded and quoted blocks from both sides so the judge sees only prose) writes `private/pairs_shuffled_N.jsonl` (random A/B order, ids hidden, answer key in `private/key_N.json`). Main session dispatches a Sonnet subagent per seed (seeds 1 and 2) that reads the pairs file and outputs, per pair, which one is the real human email and a one-line reason. `build_pairs.py --score private/judge_N.jsonl --seed N` computes accuracy.

- [ ] **Step 4: Record** `results.md`: date, n, judge model, both accuracies and the mean, the judge's most common stated reasons, and what changed in the skill in response. No email text. Target: mean under 60%. If above, revise voice-profile.md and registers.md on the judge's reasons and rerun once.

- [ ] **Step 5: Stage** `git add evals/blind_test/build_pairs.py evals/blind_test/test_build_pairs.py evals/blind_test/README.md evals/blind_test/results.md`

## Chunk 3: Docs, verification, distribution

### Task 11: README.md and CHANGELOG.md

- [ ] **Step 1: README** under 80 lines: what the skill is, install for Claude Code (`cp -r` to `~/.claude/skills/writing-style`), install on claude.ai (upload zip), the registers in one table, how to run the linter, how to run the blind test, privacy note, license line.
- [ ] **Step 2: CHANGELOG** with a `## 2.0.0 (2026-09-12)` section: Removed (spec section 8 table as bullets, each with source), Added (spec section 9, grouped), Changed (humanizer folded in; evals rewritten; placeholders deleted).
- [ ] **Step 3: Lint both. Stage.**

### Task 12: Verification

- [ ] **Step 1:** `python3 -m unittest discover -s scripts -p "test_*.py" -v` and `python3 -m unittest evals/blind_test/test_build_pairs.py -v`. Expected: all pass.
- [ ] **Step 2:** `for f in SKILL.md README.md CHANGELOG.md references/*.md; do python3 scripts/lint.py "$f" || echo "FAIL $f"; done`. Expected: no FAIL.
- [ ] **Step 3: Run the six evals.** For each prompt in `evals/evals.json`, generate output with the v2 skill, save to `evals/runs/2026-09-12/<id>.md` (gitignored if it contains anything sensitive; these are invented so they can be committed), lint each with its register, and check every expectation by hand. Record pass/fail in `evals/runs/2026-09-12/summary.md`.
- [ ] **Step 4: Privacy grep across the repo**

```bash
grep -rn -i "maxwell.greenberg\|@gmail.com\|@yahoo.com" --include="*.md" --include="*.json" --include="*.py" . | grep -v docs/superpowers || echo CLEAN
```
Expected: `CLEAN`.

- [ ] **Step 5: Show Max** the full diff summary, the voice profile, the changelog, and the blind-test results. Wait for "push".

### Task 13: Distribution (only after Max says push)

- [ ] **Step 1: Commit and tag**

```bash
git add -A && git commit -m "feat: writing-style v2, layered voice + anti-AI skill" -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
git tag v2.0.0 && git push origin main --tags
```

- [ ] **Step 2: Claude Code install** `rm -rf ~/.claude/skills/writing-style && mkdir -p ~/.claude/skills/writing-style && cp -r SKILL.md references scripts evals ~/.claude/skills/writing-style/`
- [ ] **Step 3: Zip for claude.ai** `zip -r dist/writing-style-v2.0.0.zip SKILL.md references scripts evals -x "evals/blind_test/private/*" "*/__pycache__/*"` then tell Max the path and that he uploads it in claude.ai skill settings to replace the existing user skill.
- [ ] **Step 4: Plugin sync** `rsync -a --delete --exclude private SKILL.md references scripts evals ~/max-skills/writing-style/skills/writing-style/` and bump `~/max-skills/writing-style/.claude-plugin/plugin.json` version to `2.0.0`.
- [ ] **Step 5: Global CLAUDE.md** edit `/Users/maxmac/.claude/CLAUDE.md`: replace the humanizer instruction block with the writing-style routing rule (all writing deliverables through writing-style; research and analysis outputs run only its anti-AI layer).
- [ ] **Step 6: Archive humanizer** `mkdir -p ~/.claude/skills-archive && mv ~/.claude/skills/humanizer ~/.claude/skills-archive/humanizer`
- [ ] **Step 7: Verify** `ls ~/.claude/skills/writing-style ~/.claude/skills-archive; grep -n writing-style ~/.claude/CLAUDE.md`.
