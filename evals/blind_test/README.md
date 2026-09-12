# Blind test

Checks whether a Sonnet judge can tell Max's real sent emails apart from
emails the writing-style skill generated for the same subject and context.
If the judge can't do much better than a coin flip, the skill's voice is
passing.

## Commands, in order

1. `python3 build_pairs.py select`
   Reads the sent-mail corpus, filters to real replies with context and a
   body between 20 and 200 words, caps it at two per recipient, and spreads
   the picks across years. Writes `private/prompts.jsonl` (with the real
   body) and `private/prompts_only.jsonl` (without it, for generation).

2. `python3 build_pairs.py shuffle --seed N`
   Pairs each prompt's real body with the model-generated body in
   `private/generated.jsonl`, randomizes which side is A and which is B,
   and writes `private/pairs_shuffled_N.jsonl` (blind) plus
   `private/key_N.json` (the answer key).

3. `python3 build_pairs.py score --seed N private/judge_N.jsonl`
   Compares the judge's per-pair answers against the key and prints
   accuracy plus the judge's stated reasons.

## Where private files live

Everything the corpus or the judge touches lives under
`evals/blind_test/private/`: `prompts.jsonl`, `prompts_only.jsonl`,
`generated.jsonl`, `pairs_shuffled_*.jsonl`, `key_*.json`,
`judge_*.jsonl`. That directory is gitignored.

Nothing in `private/` is ever committed.

Always pass `--sanitize` to `shuffle`. It replaces addresses, phone numbers, and links with placeholders and strips forwarded and quoted blocks from both the real and the generated body, so the judge is scoring voice and not export artifacts. Round 1 of this test ran without it and the judges leaned on those artifacts.
