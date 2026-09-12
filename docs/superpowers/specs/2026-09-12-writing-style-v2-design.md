# writing-style v2 design

Date: 2026-09-12
Status: draft for Max's review
Repo: realmwell/writing-style (public)

## 1. Goal

Rewrite the writing-style skill so Claude produces prose that (a) reads as written by a person, not a model, and (b) reads as written by Max specifically. Fold the separate humanizer skill into it. Ground every rule in either Max's own writing corpus or a cited source. Ship it as a Claude Code skill, a claude.ai uploaded skill, and a plugin.

Near-term use: Max writes cold and warm sales emails for Databricks federal, tribal, and regulated-industry accounts every week. The professional register and its sales-outreach sub-case get the most depth.

## 2. What was wrong with v1

- Subtractive only. It banned words and phrases but never described Max's voice.
- Contradicted Max's real habits: banned exclamation points (Max uses one in 40% of emails and 64% of emails to organizations), treated the em dash as the number one AI tell (Max uses " - " and almost never an em dash), banned words Max uses in formal writing.
- Flat blocklists. Research shows word bans go stale (the "delve" curve) and get bypassed by synonyms; rhythm and structure carry the signal.
- Duplicated the humanizer skill with a different list, so the two disagreed (for example on "here's what we'll cover").
- SEO section carried an unsourced statistic and prescribed templated structures that the anti-AI rules remove.
- Weak evals (absence of banned words only). Placeholder reference, script, and asset files.
- The skill file itself broke its own rules (em dashes, "comprehensive", bold-header bullets).

## 3. Sources

Research notes live in `docs/research/` (copied from the private research folder, public-safe):

1. `01-google-style-guide.md`: Google developer documentation style guide plus the nbj-write-clearly and Johansen prior-art skills.
2. `02-ai-tells-wikipedia-audit.md`: current Wikipedia "Signs of AI writing" audited against the humanizer and v1 skills; merged master pattern list.
3. `03-ai-detection-and-claudish.md`: detector mechanics, evidence-rated tells, Claude-specific tics, positive rules, blocklists vs structure.
4. `04-classic-guides-and-amazon.md`: Orwell, Strunk, Zinsser, Amazon writing culture, Economist, Bernoff, Graham.
5. `05-cold-email-craft.md`: subject lines, body copy, CTAs, sequences, government and regulated buyers, deliverability.

Voice evidence (private, never committed): about 10,000 sent-mail opening lines 2011 to 2026, a few hundred full email bodies, and Drive documents in Max's voice (MBA essays, a wedding speech, a LinkedIn summary, the Databricks cold outreach prompt Max wrote). Profile lives at `~/writing-style/corpus/`.

## 4. Architecture

Layered. The always-loaded part stays short; detail loads on demand.

```
writing-style/
  SKILL.md                      # ~180 lines: triggers, workflow, register model, always-on rules
  references/
    voice-profile.md            # Max's fingerprint, per register, with public-safe examples
    registers.md                # settings table + playbook per register incl. sales outreach
    anti-ai-patterns.md         # merged master list, tiered by evidence and era
    clarity-rules.md            # Google + classic-guide rules that transfer to prose
    cold-email.md               # subject, body, CTA, sequence, gov/regulated buyer rules
  scripts/
    lint.py                     # deterministic checker: tells, rhythm, length, punctuation
  evals/
    evals.json                  # rewritten prompts and expectations
    blind_test/                 # harness + results for the voice test
  docs/
    research/*.md               # the five research notes
    superpowers/specs/          # this document
  README.md
  CHANGELOG.md                  # every rule change traced to a source
```

Loading rules, written into SKILL.md:

- Always: SKILL.md.
- Any writing task: `voice-profile.md` and `registers.md`.
- Edit or self-check pass: `anti-ai-patterns.md`.
- Professional or marketing register: `clarity-rules.md`.
- Sales outreach: `cold-email.md`.
- Research or analysis output (not in Max's voice): `anti-ai-patterns.md` only.

## 5. Register model

Three registers plus one sub-case. The skill infers the register from audience cues (named recipient, their relationship to Max, purpose, where the text lands) and states the guess in one line at the top of its working, never in the deliverable. Fallback when unsure: professional.

| Setting | Personal | Professional | Sales outreach (sub-case) | Marketing |
|---|---|---|---|---|
| Who | Friends, family, people who know Max | Colleagues, customers, vendors, landlords, recruiters, press | Cold or warm prospects at an account | Anonymous readers of a site, post, or ad |
| Exclamation points | Free, as Max does | Allowed, one per email max, never in a subject | Never | Never in headlines; rare in body |
| Contractions and slang | Yes, including lowercase, "lol", profanity when it fits | Contractions yes, slang no | Contractions yes, slang no | Contractions yes |
| Dash | " - " spaced hyphen. Never an em dash | Same | Same | Same |
| Greeting | "Hey Name," or "Howdy Name!" or none | "Hi Name," | "Hi Name," | n/a |
| First line after greeting | Warm and specific | "Thanks so much for..." / "Hope you're well" / straight to it | The researched observation. No "hope you're well" | The reader's problem |
| Sign-off | None, or "Max" | "Thanks, Max" / "Cheers, Max" / "Max" | Structured close from the outreach playbook; signature appended by Max | n/a |
| Length (whole message) | Median about 15 words; one-liners common | Median about 30 words; 2 to 4 short paragraphs | Touch 1: 50 to 125 words by default (Lavender and Gong data); up to 200 when Max asks for his full five-paragraph structure | Short paragraphs, 2 to 4 sentences |
| Sentence length | Median about 12 words in all registers, standard deviation about 22 (very bursty) | Same | Same | Same |
| Humor and asides | Yes | Light | No | Light if on-brand |
| Anti-AI layer | Structural rules only; vocabulary watchlist off | Full | Full plus cold-email tells | Full |
| Clarity layer (Google, Amazon) | Off | On | On | On |

Habit-vs-rule resolution, per Max's decision: in personal writing Max's habits win. In professional, sales, and marketing, the anti-AI and clarity rules win where they conflict with a habit.

Inference procedure, in order, first match wins:

1. Max names the register or the reader's relationship. Use it.
2. The reader is a friend, family member, or someone the request describes as knowing Max. Personal.
3. The reader is a prospect or contact at a named account, or the request says outreach, cold, prospect, or sequence. Sales outreach.
4. There is no individual reader (a page, a post, an ad, a product description). Marketing.
5. Anything else, including editing text with no stated audience. Professional.

Marketing is deliberately thin: it is the professional register plus three rules (the reader's problem in the first sentence, no exclamation in headlines, paragraphs of two to four sentences). It gets no separate playbook in v2. The near-term priority is sales outreach.

## 6. Rule precedence

Highest first. Written into SKILL.md so the model can resolve conflicts without asking.

1. Max's explicit instruction in the request.
2. Facts. Never invent a number, name, artifact, quote, customer story, or URL. A weaker sentence beats a wrong fact.
3. The register's voice profile.
4. Structural anti-AI rules (rhythm, paragraph variance, no summaries, no zingers, no negation fragments, hedges, lists, bold).
5. Clarity rules (Google, Amazon, classic guides).
6. Vocabulary watchlist, tiered by era. Advisory in personal; enforced in the other registers.

Structure outranks vocabulary on purpose. Source: research note 03, "Blocklists versus structural rules".

## 7. Workflow

1. Identify the task type: draft from a brief, or edit existing text. Identify the reader and the register. State both in one line (working, not output).
2. Load the reference files the register calls for.
3. Draft. For an edit, apply the protect-meaning list: keep names, numbers, dates, product terms, caveats, modal verbs, links, and any sentence Max marked as his.
4. Self-check pass. Ask two questions of the draft: "What here still reads as written by a model?" and "What here doesn't sound like Max?" Answer in working notes, then revise.
5. Run the mechanical checks from `lint.py` mentally, or literally if the file is on disk.
6. Deliver only the clean result. No change summary, no preamble, no sign-off from Claude.

## 8. What v2 removes from v1, with reason

| Removed | Reason and source |
|---|---|
| Em dash as "#1 AI tell", one-per-page cap | Wikipedia's guide now says em dashes are common in human writing (note 02). Replaced by a voice rule: Max's dash is " - "; never use an em dash. |
| Blanket ban on exclamation points | Max uses them in 40% of emails; 64% to organizations (corpus). Banned only in sales outreach and marketing headlines (note 05, note 01). |
| SEO/AEO/GEO section | Unsourced "15 to 30%" citation-rate claim; prescribes the templated shapes the anti-AI layer removes (note 02, contradiction 4). |
| Flat banned-word lists | Word bans go stale and get bypassed (note 03). Replaced by tiered watchlist. |
| "delve", "tapestry", "testament", "meticulous" as headline tells | First-wave (2023 to mid-2024) per Wikipedia tiering (note 02). Demoted, kept for older-model output. |
| Knowledge-cutoff disclaimer as a live tell | Wikipedia classes it historical (note 02). |
| "Here's what we'll cover" as an approved transition | Contradicts the chatbot-artifact rule (note 02, contradiction 1). |
| Placeholder reference, script, and asset files | Scaffold leftovers. |
| Bold-header bullet lists and em dashes inside the skill file | The skill must pass its own rules. |

## 9. What v2 adds, with source

Voice (from the corpus and Drive documents):

All voice bullets below are aggregate findings from the corpus, stated as patterns. Short phrases in quotes are common-English formulas that recur across hundreds of messages, not quotations of any one email.

- Greeting shapes: "Hi Name," dominant to organizations and work; "Hey Name," to friends; "Howdy" occasional since 2020; exclamation after the name about a quarter of the time in professional mail.
- First move after the greeting: a thank-you or a warm line, then straight to the point. An apology when late.
- Reasoning in plain steps before the ask, then one clear ask, often phrased as a question.
- Specific numbers, dates, and primary sources. Dislikes secondhand summaries.
- Sentence rhythm: median 12 words, very bursty (standard deviation about 22). One-liners common. Long sentences appear, usually to carry a story or a list of specifics.
- Sign-offs: none most of the time; "Max", "Thanks, Max", "Cheers, Max".
- Vocabulary: near zero AI-tell words in email (under 1 per 1,000). In essays, uses "vibrant", "enhance", "fortify" freely, which is why the watchlist is off in personal register.
- Stance: has opinions, says them, hedges with structure ("from the outside it reads as...") not with adverb stacks.

Structure (note 03, note 02):

- Vary sentence length on purpose; let short sentences cluster.
- Let paragraph lengths differ; a one-line paragraph is allowed when it earns it.
- No section-ending summary; no aphoristic closing line; stop on the last real point.
- No "not X, it's Y"; no "Not X. Y." fragments; no "Y rather than X" as a reflex.
- One hedge per sentence that makes a claim, never stacked. Hedge inventory for the linter: may, might, could, perhaps, possibly, arguably, somewhat, largely, tends to, in some sense, sort of, kind of, generally, almost, I think, it seems.
- No "here's where I'd push back", no "you're absolutely right", no "great question".
- Bold only for real emphasis; never as a lead-in to every bullet.
- Lists only for real sequences or sets; prose otherwise.
- No heading without body text; sentence-case headings.
- No participial tails ("..., marking a shift").
- No rule-of-three padding; no false ranges ("from X to Y").
- No copula avoidance ("serves as", "stands as", "boasts").
- Grep for leftover model artifacts (cite tags, contentReference).
- One concrete detail per section beats a general claim.

Clarity (note 01, note 04):

- Second person, present tense, active voice, condition before instruction, lead with the point.
- Plain word over fancy word; contractions on; cut "just", "simply", "easily".
- Professional and marketing: replace adjectives with data; no weasel words; sentences under 30 words unless the length carries meaning. The "so what" test (every sentence must matter to the reader) is a heuristic, not a rule: note 04 treats it as Amazon house practice, note 05 rates it weak evidence.
- Write like you talk; read it aloud; have a stake in the subject; end deliberately.

Cold email (note 05, plus Max's own outreach prompt):

- Subject names an artifact, a number, or a problem. No "quick question", no "following up", no exclamation, no emoji.
- Open with the researched observation. Never "hope this finds you well", never "I wanted to reach out", never restate the recipient's job.
- The paragraph-two test: the recipient must be able to reply "actually the harder part is X."
- One ask. Default is an interest question ("Worth a look?"), which Gong's 304,000-email study found beat meeting-time asks about 2 to 1 on first touch. Max's structured 30 or 45 minute close is the named alternative when he asks for it.
- One customer example, sourced from a Databricks-published page, verified live. Default is to name the customer in text and offer the link on reply, because note 05 rates "no links in the first touch" as moderate evidence. Include the hyperlink only when Max asks or when using his full five-paragraph structure. This is a deliberate deviation from note 05, made because Max's method requires the source to exist and be verified even when it isn't linked.
- 50 to 125 words for touch 1 by default; up to 200 for Max's full structure. Plain text.
- Hard rules on fabrication carried over from Max's prompt.

Vocabulary watchlist, three tiers. Sources stated per tier.

- Tier A, Wikipedia's current era (mid-2025 onward) per note 02: emphasizing, enhance, highlighting, showcasing. Enforced (linter ERROR) in non-personal registers.
- Tier B, the merged top-40 diagnostic list from note 02 section 4, not era-tiered by Wikipedia: leverage, foster, underscore, boast, garner, bolster, streamline, navigate, elevate, unveil, unlock, harness, interplay, pivotal, crucial, vital, robust, comprehensive, seamless, transformative, groundbreaking, cutting-edge, innovative, holistic, multifaceted, nuanced, enduring, align with, associated with. Enforced (ERROR) in sales and marketing; WARN in professional; off in personal.
- Tier C, first-wave 2023 to mid-2024 per note 02: delve, tapestry, testament, meticulous, landscape (abstract), intricate, realm, vibrant. WARN only when two or more appear.
- Claude-specific words and phrases. Confirmed by note 03 with multiple sources: "load-bearing", "It's not X, it's Y", "Not X. Y.", "here's where I'd push back", "you're absolutely right", stacked hedges, aphoristic closers. Unconfirmed, on watch from practitioner chatter and not yet on Wikipedia's page (note 02 checked): genuinely, honestly, quietly, "the real X is", "chef's kiss". The unconfirmed set is WARN only.

## 10. Lint script

`scripts/lint.py <file> [--register R]` prints findings, no rewrites. Default register professional. Levels:

- ERROR (exit 1): any em dash; Tier A word outside personal; Tier B word in sales or marketing; exclamation point in sales; negation fragment or "not X, it's Y" outside personal; model debris tags.
- WARN (exit 0): Tier B in professional; two or more Tier C words; unconfirmed Claude words; more than one exclamation in professional or marketing; closing-summary phrase in the last paragraph; chatbot artifacts; bold lead-in bullets; title-case headings; sentence-length standard deviation under 6 with six or more sentences; four or more paragraphs within 20% of the mean length; spam-trigger words in sales (the list from note 05: free, guarantee, act now, risk-free, no obligation, buy now, winner); two or more hedge-inventory words in one sentence.
- INFO: word count, sentence count, sentence-length mean and standard deviation.

The burstiness floor of 6 comes from the corpus: Max's short vendor emails, his least varied register, measure a standard deviation of about 7. Lines beginning with `Before:` are exempt so the reference files can show bad examples. Full check list with regexes lives in the implementation plan, Task 8.

## 11. Evals

- `evals.json`: six prompts across registers (personal reply, vendor email, professional intro, cold touch 1, marketing paragraph, edit of an AI-written paragraph). Schema per eval: `id`, `prompt`, `register`, `expected_output` (one line), `expectations` (5 to 8 strings, each a yes/no question a reviewer answers by reading the output, such as "Opens with Hi or Hey plus a name"). Expectations check presence of voice markers, not only absence of tells.
- Blind voice test: for 20 corpus emails, reconstruct the prompt from the subject and the `context` field (the first 300 characters of the prior message from the other party, already stored in the corpus), generate a reply with the skill, and hand pairs (real, generated) to a Sonnet judge in random order asking which is Max. Run the judge twice with different shuffles and report both accuracies, since a single 20-pair run is noisy. Target: mean under 60%. Results and harness committed under `evals/blind_test/`; real emails, generated replies, and pair files stay in a gitignored `private/` folder.
- Corpus stats comparison (optional, not a v2 deliverable): run `analyze.py` on generated outputs and compare against the register baseline.

## 12. Distribution and prod

Exact commands for every step are in the implementation plan, Task 13.

1. Repo: commit v2, tag `v2.0.0`, push to `realmwell/writing-style` main.
2. Claude Code on this Mac: copy `SKILL.md`, `references/`, `scripts/`, `evals/` to `~/.claude/skills/writing-style/` (currently absent there).
3. claude.ai: `zip -r dist/writing-style-v2.0.0.zip SKILL.md references scripts evals` excluding `evals/blind_test/private`; Max uploads it in claude.ai skill settings to replace the existing user skill (skill id ending in c72mMC).
4. Plugin: `rsync -a --delete` the same four paths into `~/max-skills/writing-style/skills/writing-style/` and set `plugin.json` version to 2.0.0.
5. Global `~/.claude/CLAUDE.md`: replace the humanizer instruction with: run writing-style on every writing deliverable; run only its anti-AI layer on research and analysis outputs.
6. Humanizer: move `~/.claude/skills/humanizer/` to `~/.claude/skills-archive/humanizer/`. Not deleted.
7. Memory: already recorded (corpus privacy, all-writing rule).

Commits and pushes happen only when Max says so, per his CLAUDE.md.

## 13. Privacy

The repo is public. No email text, correspondent names, or Drive document text goes into any committed file, including this spec, the plan, and the research notes under `docs/`. Voice examples in `voice-profile.md` are either from Max's public writing, paraphrased, or invented to match the measured pattern. Corpus-derived numbers are stated as rounded aggregates. The corpus, the analysis output, the spec review notes, and the blind-test real emails stay outside the repo in `~/writing-style/`. Task 12 of the plan runs a grep for addresses and correspondent names across the repo before anything is committed.

## 14. Open items

- Full-body corpus: waiting on a Google Takeout export (Sent label). Until then the profile rests on ~10,000 opening lines, ~200 full bodies, and the Drive documents. The profile will be refreshed and the blind test rerun when the export arrives.
- Databricks work email is on a separate account and cannot be exported. The sales register leans on Max's own outreach prompt, the cold-email research, and his emails to organizations.
