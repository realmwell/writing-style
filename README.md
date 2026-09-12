# writing-style

A Claude skill that writes in Max Greenberg's voice and keeps prose from reading as AI-generated. Version 2.0.0.

It has two halves. The voice half was built from about 10,000 of Max's sent emails and his own documents, distilled into a fingerprint, a set of registers, and playbooks. The anti-AI half was built from current research on how generated text is detected: Wikipedia's Signs of AI writing, detector studies, catalogs of Claude-specific tics, the Google developer documentation style guide, and the classic writing guides. The five research notes are in `docs/research/`, and `CHANGELOG.md` traces every rule to its source.

## Install

Claude Code on a Mac:

```bash
git clone https://github.com/realmwell/writing-style.git
mkdir -p ~/.claude/skills/writing-style
cp -r writing-style/SKILL.md writing-style/references writing-style/scripts writing-style/evals ~/.claude/skills/writing-style/
```

claude.ai: follow `SETUP-CLAUDE-AI.md`. Download the zip from the releases page and upload it in Settings. The skill attaches to your account, so it then works in every browser.

## Registers

| Register | Reader | What changes |
|---|---|---|
| Personal | Friends and family | Mirrors Max: exclamation points, lowercase, slang, no greeting. Vocabulary watchlist off |
| Professional | Colleagues, customers, vendors, press | "Hi Name," thanks, plain-step reasoning, one ask, "Thanks, Max" |
| Sales outreach | Prospects at a named account | Five-paragraph touch 1, 50 to 125 words, observation first, interest-based ask |
| Marketing | No individual reader | Professional plus the reader's problem first and no exclamation in headlines |

The skill infers the register from the request and falls back to professional. Details in `references/registers.md`.

## Files

- `SKILL.md`: what loads every time. Workflow, precedence, always-on rules.
- `references/voice-profile.md`: the fingerprint. Openings, argument shape, closings, rhythm, words.
- `references/registers.md`: inference, settings, playbooks with invented examples.
- `references/anti-ai-patterns.md`: structural, content, Claude-specific, and chatbot patterns; tiered vocabulary; positive moves.
- `references/clarity-rules.md`: Google and classic-guide rules, and where they yield to voice.
- `references/cold-email.md`: subject lines, touch 1 structure, the paragraph-two test, CTAs, sequences, government buyers.
- `scripts/lint.py`: deterministic checker. `scripts/test_lint.py`: 22 tests.
- `evals/evals.json`: six prompts with yes/no expectations. `evals/blind_test/`: the voice test.

## Lint

```bash
python3 scripts/lint.py draft.md --register professional
python3 -m unittest scripts/test_lint.py
```

Exit 1 on any error. Lines starting with `Before:` are exempt. Regions between `<!-- lint:off -->` and `<!-- lint:on -->` and lines containing `lint:ignore` are skipped; use them only for word lists and teaching examples.

## Blind voice test

Twenty real emails from the corpus are paired with the skill's replies to the same prompts. A separate model judges which is real, twice with different shuffles. Target is a mean accuracy under 60 percent. Commands and results are in `evals/blind_test/`. The real emails never leave the gitignored `private/` folder.

## Privacy

The corpus this was built from is private and lives outside the repo. Every example in the reference files is invented to match a measured pattern or drawn from public writing. Numbers are rounded aggregates.

## License

MIT.
