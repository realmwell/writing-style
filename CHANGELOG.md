# Changelog

## 2.0.0 (2026-09-12)

Full rewrite. The v1 skill was a single rulebook of banned words that never described Max's voice and contradicted his habits. v2 is layered: a short SKILL.md plus five reference files, a linter, and a blind voice test. Sources are the five notes in `docs/research/` (numbered 01 to 05) and a private corpus of Max's sent mail.

### Removed

- The em dash as "the number one AI tell" with a one-per-page cap. Wikipedia's guide now says em dashes are common in human writing (02). Replaced with a voice rule: Max's dash is " - "; never use an em dash.
- The blanket ban on exclamation points. Max uses one in about 4 of 10 emails and 7 of 10 to organizations (corpus). Now banned only in sales outreach and marketing headlines (05, 01).
- The SEO/AEO/GEO section. It carried an unsourced citation-rate statistic and prescribed the templated structures the anti-AI layer removes (02).
- Flat banned-word lists. Word bans go stale and get bypassed by synonyms (03). Replaced with a three-tier watchlist.
- "delve," "tapestry," "testament," "meticulous" as headline tells. First-wave 2023 to mid-2024 per Wikipedia's tiering (02). Demoted to tier C.
- The knowledge-cutoff disclaimer as a live tell. Wikipedia now classes it historical (02). Kept as a legacy grep.
- "Here's what we'll cover" as an approved transition. Contradicted the chatbot-artifact rule (02).
- Placeholder reference, script, and asset files from the original scaffold.
- Em dashes and bold-header bullets inside the skill file itself.

### Added

Voice, from the corpus and Max's documents:

- Greeting shapes by register: "Hi Name," to organizations, "Hey Name," or none to friends, "Howdy" occasionally.
- The first move after the greeting: a thank-you or a warm line, then the point. An apology up front when late.
- Argument shape: observation, plain-step reasoning, one ask as a question.
- Rhythm targets: median sentence about 12 words, standard deviation about 22; one-liners common; two to four short paragraphs in professional mail.
- Sign-offs: none most of the time; "Max," "Thanks, Max," "Cheers, Max."
- Words Max uses and words that are not him.
- Habit-versus-rule resolution: Max's habits win in personal writing; the rules win elsewhere.

Structure (02, 03):

- Vary sentence length on purpose; let short sentences cluster.
- Let paragraph lengths differ; a one-line paragraph is allowed when it earns it.
- No closing summary and no aphoristic last line.
- No "not X, it's Y," no "Not X. Y." fragments, no reflexive "rather than."
- One hedge per claim, with a hedge inventory for the linter.
- No "here's where I'd push back," no "you're absolutely right," no "great question."
- Bold only for real emphasis; lists only for real sets; no heading without body text; sentence-case headings.
- No participial tails, no rule-of-three padding, no false ranges, no copula avoidance.
- Grep for leftover model artifacts.
- One concrete detail per section beats a general claim.

Clarity (01, 04):

- Second person, present tense, active voice, condition before instruction, lead with the point.
- Plain word over fancy word; contractions on; cut "just," "simply," "easily."
- Professional and marketing: replace adjectives with data; no weasel words; sentences under 30 words unless the length carries meaning.
- Write like you talk; read it aloud; one tense and person; have a stake; end on the last real point.
- Eight named places where Google's guide yields to voice, resolved per register.

Cold email (05 and Max's own outreach method):

- Subject lines of one to five words naming an artifact, a number, or a problem.
- The five-paragraph touch 1 with the researched observation first, a hypothesis the recipient can correct, one sourced customer example, and an interest-based ask by default.
- The paragraph-two test.
- Touch 1 at 50 to 125 words by default; up to 200 for Max's full structure.
- No link in touch 1 unless Max asks; the customer source is verified live either way.
- Sequence rules, government and regulated-buyer notes, deliverability words, the 300-character LinkedIn follow-up.
- Hard rules on fabrication carried over from Max's prompt.

Vocabulary watchlist, three tiers (02, 03):

- Tier A, Wikipedia's current era: emphasizing, enhance, highlighting, showcasing. <!-- lint:ignore -->
- Tier B, the merged diagnostic list, not era-tiered.
- Tier C, first-wave words, flagged only in clusters.
- Claude-specific phrases, split into confirmed and on-watch.

Tooling:

- `scripts/lint.py` with 22 tests. Checks em dashes, the three vocabulary tiers, exclamation by register, contrastive binaries and negation fragments, stacked hedges, closing summaries, chatbot artifacts, bold lead-ins, title-case headings, burstiness, uniform paragraphs, model debris, and spam triggers in sales.
- `evals/evals.json` rewritten as six register prompts with yes/no expectations that check for voice markers, not only absent tells.
- `evals/blind_test/` with a pair-building script, tests, and results.

### Changed after round 1 of the blind voice test

Round 1 (two judges, 20 pairs each) scored 75% and 95%. Reading the real replies against the imitations showed four gaps, all fixed in the reference files before round 2:

- Professional emails allow one to three exclamation points, not one. The corpus averages one per message to organizations and the real replies often carry two or three. The linter now warns above three in professional.
- Professional replies usually close with a thanks line ("Thanks again!", "Thanks so much,", "Appreciate you reaching out,") and then "Max." The earlier profile said "usually none," which was an artifact of how sign-offs were extracted.
- Intensifiers ("really appreciate," "totally understand," "incredibly disappointed") are Max's warmth markers in professional and personal mail. They are now cut only in sales and marketing, and only from claims elsewhere.
- Max counter-proposes on logistics and adds one line of personal context that explains the constraint. The imitation agreed too cleanly. Both are now in the profile and the professional playbook.

The test itself also changed: real and generated bodies are sanitized before judging (addresses, phones, links, forwarded and quoted blocks replaced with placeholders), because round-1 judges leaned on export artifacts that have nothing to do with voice.

### Changed

- The separate humanizer skill is folded in. Its 24 patterns were audited against the current Wikipedia page (02); the ones that survive are in `references/anti-ai-patterns.md`.
- The skill description now names Databricks sales outreach as a primary use and routes research outputs to the anti-AI layer only.
- Rule precedence is explicit: Max's instruction, then facts, then voice, then structure, then clarity, then vocabulary.
