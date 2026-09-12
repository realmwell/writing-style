# Anti-AI patterns

## How to use this file

Load this on every edit and on the self-check pass. Structure outranks vocabulary: a paragraph can contain zero banned words and still read as generated, and a real person can use "robust" in a sentence that is obviously theirs. <!-- lint:ignore --> One hit is not proof. A cluster is: formulaic structure plus low specificity plus even rhythm. Fix clusters by rewriting the paragraph, not by swapping words. Sources: `docs/research/02-ai-tells-wikipedia-audit.md` and `docs/research/03-ai-detection-and-claudish.md`.

## Structural patterns

Even rhythm. Sentences that all run 15 to 22 words. Real writing clusters short sentences and then lets one run long.
Before: The plan has three parts. Each part builds on the last one. Together they form a complete approach to the problem.
After: Three parts. Each builds on the last, and the third one is where the money is, because that's where the reader has to decide.

Uniform paragraphs. Four paragraphs of nearly identical length read as a template. Let one be a line and one be six sentences when the content calls for it.

Closing summary. A last paragraph that restates the piece. Stop on the last real point instead.
Before: In summary, the migration will cut costs, reduce risk, and improve reliability.
After: The migration finishes in March. After that the old cluster gets turned off.

Aphoristic closer. A quotable one-liner as the final sentence, there to sound wise rather than to inform.
Before: In the end, the best tool is the one you actually use.
After: We use the spreadsheet. Nobody has opened the dashboard since June.

Contrastive binary. "It's not X, it's Y." The frame implies the reader was wrong about X.
Before: This isn't a tooling problem, it's a culture problem.
After: The tooling is fine. People don't run it because nobody checks.

Negation fragment. "Not X. Y." as a staccato beat for drama.
Before: Not a bug. A design choice.
After: They built it that way on purpose.

Reflexive "rather than." "Y rather than X" used as a tic to sound considered.
Before: We chose to invest in people rather than tools.
After: We hired two engineers and cancelled the tool subscription.

Rule of three. Triads for the feel of completeness: "faster, cheaper, and more reliable."
Before: The new process is faster, simpler, and more transparent.
After: The new process takes two days instead of nine.

False range. "From X to Y" where X and Y are not on a scale.
Before: Everything from onboarding to offboarding to culture.
After: Onboarding and offboarding. Culture is a separate conversation.

Copula avoidance. "Serves as," "stands as," "boasts," "features" in place of "is" and "has." <!-- lint:ignore -->
Before: The library serves as a hub for the neighborhood.
After: The library is where the neighborhood meets.

Participial tail. A dangling "-ing" clause bolted onto a sentence to add unearned significance.
Before: The bill passed, marking a turning point for the region.
After: The bill passed 62 to 38. It takes effect in January.

Anticipate and rebut. "Here's where I'd push back" and its cousins. The writer stages an argument with an imagined reader.
Before: You might say this is overkill. Here's where I'd push back: the cost of getting it wrong is higher.
After: It looks like overkill. It isn't, because a wrong answer here costs a quarter.

Stacked hedges. Two or more softeners in one claim until nothing is claimed.
Before: This could potentially be somewhat of a concern in some cases.
After: This is a problem when the file is over a gigabyte.

Lists for everything. Bullets where the content is an argument, not a set.

Bold lead-ins. Every bullet opening with a bolded label and a colon. Markdown leaking into prose.
Before: - **Speed:** Pages load faster now.
After: Pages load in under a second now, down from four.

Headings without bodies. A heading whose only content is more headings. Title case in headings.

Everything the same finish. Polished to a uniform sheen. Leave a rough edge where a person would.

## Content patterns

Significance inflation. Puffing up a plain fact with talk of pivotal moments, turning points, and lasting legacies. <!-- lint:ignore -->
Before: The launch marked a pivotal moment in the company's evolution.
After: The launch shipped on March 3. Sales doubled by June.

Vague attribution. "Experts say," "studies show," "industry reports" with no name, date, or link.
Before: Experts agree the bridge is at risk.
After: A 2023 state inspection rated the bridge structurally deficient.

Notability namedropping. Listing outlets or follower counts instead of saying what was said.
Before: She has been featured in the Times, the BBC, and NPR.
After: The Times quoted her 2024 comment that rate cuts came too late.

Vague connection. "Associated with," "in connection with," "linked to" in place of a direct claim. <!-- lint:ignore -->
Before: He was associated with the campaign's field program.
After: He ran the campaign's field program.

Formulaic challenges section. Problems listed, then "despite these challenges" and a hopeful close.
Before: Despite these challenges, the town continues to thrive.
After: The mill closed in 2019. Two cafes and a bike shop opened in the building.

Generic detail. A claim that could be true of any company, town, or product. Replace with one specific: a number, a date, a name, a described moment.

## Claude-specific tics

<!-- lint:off -->
These are documented across multiple independent sources (GitHub issues, practitioner catalogs, the "Claudish" essays) as of September 2026. Treat the confirmed ones as errors in professional writing.

Confirmed: contrastive binaries ("not X, it's Y"), negation fragments ("Not X. Y."), aphoristic zingers as closers, anticipate-and-rebut framing ("here's where I'd push back"), stacked reflexive hedges ("almost," "tends to," "largely," "in some sense"), over-validation ("you're absolutely right"), forced technical metaphors and noun stacks ("load-bearing," "fleet-storm collapse"), bolded lead-in phrases, a rhetorical question answered in the next line, one-line paragraphs used as drumbeats, numbered lists for everything.

On watch, not yet confirmed by a corpus study: "genuinely," "honestly," "quietly," "the real X is," "chef's kiss," "let me be clear," "the thing is."

The tell underneath all of these: the text reads as a model proving its reasoning to the reader instead of telling the reader something. If a sentence explains why the writer is saying the next sentence, cut it.

## Chatbot artifacts

Correspondence pasted as content: "Here is an overview," "I hope this helps," "Let me know if you'd like me to expand." Open with the first real sentence.
Sycophancy: "Great question," "You're absolutely right," "Excellent point." Skip to the answer.
Generic upbeat closer: "The future looks bright." End on the last concrete fact.
Knowledge-cutoff hedge: "As of my last update." A legacy tell, mostly trained out since late 2024; still cut it.
Preview framing: "Here's what we'll cover." Start with the first point.
Model debris to grep for and delete: `contentReference`, `oaicite`, `[cite:`, `grok_card`, lenticular brackets.

## Vocabulary watchlist

Tier A, current-era tells per Wikipedia (mid-2025 onward): emphasizing, enhance, highlighting, showcasing. Error outside personal writing.

Tier B, the merged diagnostic list, not era-tiered: leverage, foster, underscore, boast, garner, bolster, streamline, navigate, elevate, unveil, unlock, harness, interplay, pivotal, crucial, vital, robust, comprehensive, seamless, transformative, groundbreaking, cutting-edge, innovative, holistic, multifaceted, nuanced, enduring, align with, associated with. Error in sales and marketing, warning in professional, off in personal.

Tier C, first-wave tells from 2023 to mid-2024, weak evidence against current models on their own: delve, tapestry, testament, meticulous, landscape (abstract), intricate, realm, vibrant. Warn only when two or more appear together.

Filler and intensifiers, cut on sight in sales and marketing: absolutely, actually, basically, certainly, clearly, definitely, essentially, extremely, fundamentally, incredibly, obviously, quite, really, significantly, simply, truly, ultimately, undoubtedly, very. In professional and personal writing Max uses "really," "totally," "incredibly," "literally," and "so much" for warmth in greetings, thanks, and apologies. Keep them there. Cut them from claims and from the substance of the ask.

Hedge inventory, one per claim at most: may, might, could, perhaps, possibly, arguably, somewhat, largely, tends to, in some sense, sort of, kind of, generally, almost, I think, it seems.
<!-- lint:on -->

## Positive moves

Vary sentence length on purpose. Let three short sentences sit together, then one long one.
Let paragraphs run different lengths. A one-line paragraph is fine when it earns it.
Put one concrete detail in place of each general claim: a number, a name, a date, a moment.
Take a stance and say it plainly.
Use the plain word: "look at" not "delve into," "use" not "leverage," "is" not "serves as." <!-- lint:ignore -->
Stop when the point is made. No summary, no zinger.
Use short transitions or none: "So," "But," "Also," "Then."
Let parallelism be imperfect when the ideas are not parallel.
Digress when the digression is relevant. Real writing circles back.
Refer to shared context by name, not by scaffold sentence.
One hedge per claim.
Lists only when the content is a sequence or a set of comparable items.
Bold only for real emphasis, and rarely.
Match rhythm and word choice to the writer's own samples, not to a helpful-assistant register.
Read it aloud. Cut any sentence that explains your reasoning instead of telling the reader something.
Leave a rough edge. Not every sentence needs the same polish.

## Self-check prompts

After drafting, answer these in working notes, then revise:

1. What here still reads as written by a model?
2. What here doesn't sound like Max?
3. Read it aloud. Where did you stumble?
