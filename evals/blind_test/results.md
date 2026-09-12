# Blind voice test results

Judge model: Claude Sonnet 5, one fresh judge per run, no access to the skill or the corpus. Twenty pairs per run. Each pair holds one real email Max sent and one reply the skill wrote to the same prompt (subject plus the prior message). No email text appears in this file; the pair files and answer keys stay in the gitignored `private/` folder.

## Round 1, 2026-09-12, before sanitizing

| Run | Seed | Judge accuracy |
|---|---|---|
| 1 | 1 | 75% (15 of 20) |
| 2 | 2 | 95% (19 of 20) |
| Mean | | 85% |

Failed the target of under 60%. The judges' stated reasons split into two kinds.

Leakage, not voice: forwarded-message markers, quoted third-party text, image placeholders, real phone numbers and addresses, links, and private facts the generator could not know (a credit score, a friend's birthday). These made the real email identifiable without reading it as prose.

Voice, and useful: the real writer counter-proposes on logistics instead of agreeing; over-explains a personal reason; stacks exclamation points to family; writes terse shorthand notes to himself; and uses slightly clunky, literal phrasing. The imitation was smoother and more compliant.

Changes made in response: the profile and the professional playbook now call for one to three exclamation points, a closing thanks line, intensifiers used for warmth, a line of personal context that explains a constraint, and a counter-proposal when the logistics don't work. The linter's professional exclamation threshold moved from one to three. The generator was given the same facts the real email contained, so the pairs differ in voice and not in knowledge. The pair builder gained a sanitize step that replaces addresses, phones, and links with placeholders and strips forwarded and quoted blocks on both sides.

## Round 2, 2026-09-12, sanitized, revised profile

| Run | Seed | Judge accuracy |
|---|---|---|
| 3 | 3 | 20% (4 of 20) |
| 4 | 4 | 45% (9 of 20) |
| Mean | | 32.5% |

Passes the target. Both judges did worse than a coin flip, which means they could not tell the skill's output from Max's real emails on voice alone, and when they guessed wrong they usually called the skill's version the more human one.

The judges' most common reasons for picking the imitation over the real email: the real email used a formal courtesy word ("additionally," "certainly," "is it possible to," "truly appreciated") that read to them as AI polish, or an elevated idiom ("set the wheels in motion," "kick off festivities"). Their most common reasons for picking the real email correctly: a typo, telegraphic shorthand like a time written without a colon, a verbatim quote of someone else's message, and dropped-subject fragments.

What that says about the skill: after round 1 it matched the warmth, the counter-proposals, and the fragments. It was still a touch plainer and breezier than Max, who is warm and slightly old-fashioned with strangers. The profile now names the dropped-subject fragment and the formal courtesy word as a paired fingerprint, and the professional playbook asks for one of each. Those edits landed after the round-2 replies were generated, so they are untested here.

## Caveats

Twenty pairs per run is a small sample; a single run can swing ten points on two pairs. Two runs per round reduce but do not remove that noise. The judge is a model, not a human who knows Max; a friend of his would likely do better than 32%. The prompts are replies to real threads, which favors short logistics mail; the test says less about long-form writing. The sales register was not tested here because Max's work email is on a separate account. It was checked with the evals in `evals/runs/` and the linter instead.

## Rerun

```bash
python3 evals/blind_test/build_pairs.py select
# generate private/generated.jsonl with the skill, one reply per prompt, using the facts from prompts.jsonl
python3 evals/blind_test/build_pairs.py shuffle --seed 5 --sanitize
# judge private/pairs_shuffled_5.jsonl with a fresh model into private/judge_5.jsonl
python3 evals/blind_test/build_pairs.py score --seed 5 private/judge_5.jsonl
```
