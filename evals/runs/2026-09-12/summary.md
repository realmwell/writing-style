# Eval run 2026-09-12

Skill version 2.0.0. Each output was generated with the skill loaded, linted with `scripts/lint.py --register <register>`, then checked against every expectation in `evals/evals.json` by reading. Outputs are in this folder, one file per eval. All inputs were invented; nothing here comes from the private corpus.

| Eval | Register | Words | Lint | Expectations | Notes |
|---|---|---|---|---|---|
| 1 | personal | 58 | 0 errors, 0 warnings | 8 of 8 | Lowercase opening kept; one 6-word sentence and one 25-word sentence; no sign-off |
| 2 | professional | 75 | 0 errors, 0 warnings | 8 of 8 | "Hi Name," thanks, three plain reasons, one "Could you" ask, "Thanks, Max" |
| 3 | professional | 63 | 0 errors, 0 warnings | 7 of 7 | Double opt-in handoff, one exclamation, no bullets |
| 4 | sales | 125 body | 0 errors, 0 warnings | 8 of 8 | First draft was 130 words; trimmed twice to reach the 125 default. Paragraph two passes the test: the recipient could reply that the harder part is the regional source systems |
| 5 | marketing | 78 | 0 errors, 0 warnings | 7 of 7 | First draft claimed the tool shows permit costs, which the prompt never stated. Removed as a fabrication. That also removed a three-item list |
| 6 | professional | 65 | 0 errors, 0 warnings | 7 of 7 | Every vague claim in the source was dropped rather than replaced with an invented number |

Two findings worth keeping:

The sales register runs long on the first pass. The five-paragraph shape wants 130 to 140 words; hitting 125 took two trims. The reference file's default is right for the data, but the skill should expect to cut.

Fabrication risk shows up in marketing copy, where the urge to add a concrete benefit produced one the brief did not support. Rule 2 (facts) caught it on the self-check, not on the draft. That is the order the workflow is built for, and it held.
