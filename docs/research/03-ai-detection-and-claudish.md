# AI Detection and Claudish

## How detectors work

Most detectors combine a few signals. Perplexity measures how predictable a text is to a reference language model; low perplexity (the model isn't surprised by the next word) reads as AI-like. Burstiness measures variation in sentence length, usually as the standard deviation of words per sentence; human text clusters short and long sentences unevenly, AI text tends toward a narrower band. Older tools layered on vocabulary richness (type-token ratio), function-word ratios, and punctuation counts.

Binoculars (Hans et al., 2024) is the cleanest zero-shot method: it compares perplexity computed by an "observer" model against cross-perplexity from a "performer" model, and the ratio holds up even against models it never trained on. The paper reports over 90% detection at a 0.01% false-positive rate, but that number comes from curated benchmark data, not messy real-world text.

Commercial tools have moved past pure statistics into trained classifiers. Pangram's technical report claims 99% accuracy with a false-positive rate roughly three times better than GPTZero's. GPTZero's own benchmarking claims similar accuracy and leads on recall in head-to-head tests it ran itself. Turnitin claims about 98% accuracy and under 1% false positives, but only under its own test conditions and only when more than 20% of a document is flagged as AI-written.

Independent evaluation tells a rougher story. The RAID benchmark (6M+ generations, 11 generators, 8 domains, 11 adversarial attacks) found that all 12 detectors it tested, open and closed source, lose substantial accuracy against unseen models, unseen domains, and simple adversarial edits like paraphrasing or a repetition penalty. The most cited false-positive result is Liang et al. (Stanford, 2023, published in *Patterns*): seven commercial detectors run against 91 TOEFL essays by non-native English speakers produced an average 61.3% false-positive rate, with 19.8% of essays flagged as AI by every single detector. Non-native and formal writers use simpler sentence structures and more common vocabulary, which happens to overlap with what detectors treat as an AI signature. Vanderbilt, Yale, Johns Hopkins, and other universities have since turned Turnitin's AI detector off for this reason.

## AI tells, evidence-rated

**Lexical inflation (delve, underscore, intricate, meticulous, boundaries, tapestry, testament).** Example: "The study delves into the intricate tapestry of..." Rating: Strong. Kobak et al. (Stanford, analyzing 15M+ PubMed abstracts, 2010-2024) and Juzek & Ward (COLING 2025) both find these words spiked sharply after ChatGPT's release, with "delves" showing roughly a 28-fold increase in some corpora.

**Promotional and grandiose language ("stands as a testament to," "plays a vital role," "rich cultural heritage").** Rating: Strong. Named independently by Wikipedia's Signs of AI Writing guide and by the same PubMed vocabulary studies.

**Section-ending summaries ("In summary," "Overall,").** Rating: Strong. Consistent across Wikipedia's guide and practitioner editing sources; Wikipedia articles don't normally summarize a section that's three paragraphs long, so the habit stands out.

**Overused conjunctive transitions (moreover, furthermore, additionally).** Rating: Strong. Same sources as above, plus general practitioner consensus on rewriting AI drafts.

**Em dash overuse.** Example: a sentence that pauses twice with dashes instead of commas or a full stop. Rating: Strong. A population-level study of medRxiv preprints found a measurable rise in em-dash frequency coinciding with LLM adoption; a separate analysis found GPT-4.1 uses em dashes at roughly 3.3 times the human baseline rate in matched essays. Human usage varies enormously by writer (from under 1 to over 17 per thousand words), which is why em-dash count alone is a weak signal on its own but a strong one in aggregate studies.

**Uniform paragraph and sentence length (low burstiness).** Rating: Strong. Documented in the detector literature above and treated as the more durable of the two classic statistical signals, since a model's default sampling doesn't naturally produce the clustering that human writers fall into.

**Contrastive binary framing ("It's not a style but an attractor," "not decoration but error-prevention").** Rating: Moderate, Claude-specific. Named independently by a catalog of Claude phrasing patterns (Velitchkov, "22 Claude Clichés") and by a separate essay on "Claudish" writing that lists "It's not X, it's Y" as a level-one formulaic tic.

**Staccato fragment for emphasis ("Not X. Y.").** Rating: Moderate, Claude-specific. Reported in the same two sources and echoed in a GitHub bug report on Claude Code (issue 77136) describing "leading sentences with negation."

**Aphoristic zinger endings ("evidence of training, not of virtue").** Rating: Moderate, Claude-specific. One dedicated catalog source, but consistent with broader complaints about Claude closing on a quotable line rather than stopping.

**Anticipate-and-rebut framing ("here's where I'd push back," "here's where I'd hold the line").** Rating: Moderate, Claude-specific. Named in the Claude Code GitHub issue and matched by the clichés catalog's "Anticipate-and-Rebut Reversal" entry.

**Stacked reflexive hedges (almost, tends to, largely, in some sense).** Rating: Moderate, Claude-specific. Same catalog source; also a longstanding general complaint about AI hedging, but the stacking pattern specifically is reported by fewer, more specialized sources.

**Over-validation ("You're absolutely right").** Rating: Strong for Claude specifically. Widely reported, including a GitHub issue (anthropics/claude-code #3382) documenting the phrase used 12 times in one conversation, and trade press coverage of the same complaint.

**Forced technical metaphor and noun-stacking jargon ("load-bearing," "fleet-storm collapse," "study-lifecycle handlers").** Rating: Moderate, Claude-specific. Reported in the Claude Code GitHub issue and in independent commentary on "Opus 5 Claudisms."

**Rule-of-three lists and triads.** Rating: Weak to Moderate. Widely named in practitioner "de-AI" guides but rarely backed by a frequency study; treat as a real pattern worth watching, not a proven statistical marker.

**Bolded lead-in phrases before list items.** Rating: Weak to Moderate. Consistent in practitioner guides and matches the "markdown leaking into prose" hypothesis from a 2026 analysis of how markdown-heavy training data shapes LLM output, but not independently quantified the way em dashes have been.

**Title case in headings instead of sentence case.** Rating: Weak. Named specifically by Wikipedia's guide; not corroborated elsewhere as a strong signal on its own.

## Positive rules for human-sounding prose

**Vary sentence length on purpose, and let short ones cluster.** Rating: Strong. This is the direct positive form of the burstiness signal: three short sentences in a row, then one longer subordinate one, is a documented human pattern that a model's default output doesn't reproduce without explicit instruction.

**Let paragraphs run different lengths, including a one-line paragraph when it earns its place.** Rating: Moderate. Named across multiple practitioner sources as a fix for the "uniform block" feel of AI drafts.

**Put in one concrete, specific detail instead of a generic claim.** Example: a number, a name, or a described moment instead of "plays a vital role." Rating: Moderate. Practitioner and detector-adjacent sources converge on specificity as a positive signal, though it isn't measured with the same rigor as perplexity.

**Take a real stance and state it plainly.** Rating: Moderate. Multiple practitioner sources tie first-person opinion and committed claims to human-sounding writing, in contrast to the qualifier-heavy default.

**Use plain, common words over inflated near-synonyms.** Example: "look at" instead of "delve into." Rating: Strong. Direct inverse of the lexical-inflation studies above.

**Cut the closing summary; stop when the point is made.** Rating: Strong. Direct inverse of the section-ending-summary tell, and specifically named in Wikipedia's editorial guide as a fix.

**Use short transitions or none, instead of moreover/furthermore/additionally.** Rating: Strong. Same evidentiary basis as the transition-word tell.

**Allow imperfect, incomplete parallelism between clauses.** Rating: Weak. Argued in practitioner posts as a marker of unedited human drafting, but not independently studied.

**Write a genuine digression when one is relevant, rather than holding a rigid outline.** Rating: Moderate. Practitioner sources describe human writing as "messy, ranting, circling back" in contrast to AI's uniform blocks.

**Reference shared context specifically** (a name, a prior detail, an exact figure) rather than a generic scaffold sentence. Rating: Weak. Argued rather than measured, but consistent with the specificity findings above.

**Keep hedges to one per claim, not stacked.** Rating: Moderate, direct inverse of the Claude-specific stacked-hedging tell.

**Skip the aphoristic closer.** Rating: Moderate, direct inverse of the Claude-specific zinger tell; end on the actual last point instead of a quotable line.

**Use lists only when the content is actually a sequence or a set of comparable items**, not as a default structure. Rating: Moderate. Consistent practitioner advice, paired with the numbered-lists-for-everything tell.

**Bold sparingly, and only for genuine emphasis, not as a lead-in tic for every list item.** Rating: Moderate.

**Match rhythm and word choice to a sample of your own prior writing** rather than a generic helpful-assistant register. Rating: Moderate. Practitioner workflow ("paste 1-2 paragraphs of your own writing" before drafting) reported across multiple 2026 editing guides.

**Read a passage aloud and cut any sentence that explains your own reasoning rather than telling the reader something.** Rating: Weak. A single but specific practitioner heuristic, matched to the "Claudish" complaint that these patterns read as "an AI proving its reasoning rather than informing a reader."

**Leave a typo or an unresolved rough edge occasionally rather than polishing everything to the same finish.** Rating: Weak. Argued in practitioner sources on human-like typing behavior; not something to engineer deliberately, but worth not over-correcting away in a light edit pass.

## Blocklists versus structural rules

The evidence points away from word-banning as a durable fix. "Delve" itself is the case study: it spiked after ChatGPT's release, got noticed, got banned in a hundred style guides, and faded through 2025 as models and prompts shifted, which means any fixed list goes stale on its own timeline, not the writer's. Word-level bans are also trivially defeated by synonym substitution, and the substitutes (elevate, underscore, robust) are themselves ordinary English words that plenty of human writers use honestly. Banning "delve" doesn't touch the sentence built the same way with a different verb in that slot.

The more durable finding, from the detector literature and from editors who work with AI drafts daily, is that structure carries the signal that vocabulary can't fake as easily. RAID's benchmark shows detectors lose most of their edge against structural adversarial changes (paraphrasing, altered sampling, a repetition penalty) faster than against straight vocabulary swaps, which implies the reverse is also true: changing rhythm and structure moves the needle more than changing word choice. Editors converge on the same conclusion from the other direction: the recommended workflow across 2026 practitioner guides is "human strategy, AI draft, human edit," where the edit pass targets sentence-length variation, paragraph rhythm, cut transitions, and one concrete detail per section, not a find-and-replace against a banned-word list. A single overused word is weak evidence on its own; a cluster of formulaic structure plus low specificity plus uniform rhythm is what both detectors and human readers actually respond to.

## Sources

- [Spotting LLMs With Binoculars: Zero-Shot Detection of Machine-Generated Text](https://arxiv.org/abs/2401.12070), accessed 2026-09-12
- [RAID: A Shared Benchmark for Robust Evaluation of Machine-Generated Text Detectors](https://arxiv.org/pdf/2405.07940), accessed 2026-09-12
- [Technical Report on the Pangram AI-Generated Text Classifier](https://arxiv.org/pdf/2402.14873), accessed 2026-09-12
- [How does Pangram compare against GPTZero?](https://www.pangram.com/blog/how-does-pangram-compare-against-gptzero), accessed 2026-09-12
- [How AI Detection Benchmarking Works at GPTZero (2025)](https://gptzero.me/news/ai-accuracy-benchmarking/), accessed 2026-09-12
- [Contra generative AI detection in higher education assessments](https://arxiv.org/pdf/2312.05241), accessed 2026-09-12 (references Liang et al., Stanford, *Patterns*, 2023, TOEFL false-positive study)
- [Delving into ChatGPT usage in academic writing through excess vocabulary](https://arxiv.org/html/2406.07016v1) (Kobak et al., Stanford), accessed 2026-09-12
- [Why Does ChatGPT "Delve" So Much? Exploring the Sources of Lexical Overrepresentation](https://aclanthology.org/2025.coling-main.426.pdf) (Juzek & Ward, COLING 2025), accessed 2026-09-12
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), accessed 2026-09-12
- [22 Claude Clichés - Catalog](https://www.linkandth.ink/p/catalog-of-claude-cliches) (Velitchkov), accessed 2026-09-12
- [The One Thing I Hate About Claude ("Claudish")](https://slhck.info/software/2026/06/22/claudish.html), accessed 2026-09-12
- [Claude Opus 5 Claudisms: Why It Says "Load-Bearing"](https://explainx.ai/blog/claude-opus-5-load-bearing-claudisms-writing-tells-2026), accessed 2026-09-12
- [GitHub: Claude increasingly defaults to repetitive rhetorical tics, issue #77136](https://github.com/anthropics/claude-code/issues/77136), accessed 2026-09-12
- [GitHub: Claude says "You're absolutely right!" about everything, issue #3382](https://github.com/anthropics/claude-code/issues/3382), accessed 2026-09-12
- [Claude Code's endless sycophancy annoys customers](https://www.theregister.com/software/2025/08/13/claude-codes-endless-sycophancy-annoys-customers/328260), accessed 2026-09-12
- [Em-ergence of the em-dash: a population-level rise in em-dash frequency in medRxiv preprints](https://arxiv.org/pdf/2606.29540), accessed 2026-09-12
- [Why Large Language Models Seem to Overuse Em-Dashes](https://www.gunvir.ca/papers/why-llms-seem-to-overuse-em-dashes.html), accessed 2026-09-12
- [The Last Fingerprint: How Markdown Training Shapes LLM Prose](https://arxiv.org/html/2603.27006v1), accessed 2026-09-12
- [Why do AI models use so many em-dashes?](https://www.seangoedecke.com/em-dashes/), accessed 2026-09-12
