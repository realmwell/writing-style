# Google developer documentation style guide: research notes

Sources accessed 2026-09-12.

## Rules that transfer to general prose

### Voice and person
- Address the reader as "you," not "we." Direct address reads clearer in any writing, not just docs. https://developers.google.com/style/person
- Prefer active voice so the reader always knows who is doing what. https://developers.google.com/style/voice
- Write conversational and approachable, like a knowledgeable friend, not a lecture or a press release. https://developers.google.com/style/tone

### Verbs and tense
- Default to present tense. Save "will" for things that genuinely happen later. https://developers.google.com/style/tense
- Use standard contractions (don't, isn't, there's). They read more natural, and a negative contraction is harder to misread at a glance than "not." https://developers.google.com/style/contractions

### Sentence and paragraph shape
- Put the condition before the instruction: "If X, do Y," not "Do Y if X." https://developers.google.com/style/sentence-structure
- Keep sentences short. Length is one of the biggest levers on comprehension. https://developers.google.com/style/translation
- Lead each paragraph with the important information so a skimmer gets the point first. https://developers.google.com/style/translation

### Word choice
- Cut filler qualifiers like "just," "simply," "easily." They add little and can read as condescending. https://developers.google.com/style/word-list
- Use the plain word over the fancy one: "use" not "utilize," "start" not "commence." https://developers.google.com/style/word-list
- Drop "please" from routine instructions. Save it for actual requests or apologies. https://developers.google.com/style/tone
- Say "click," not "click on." Say "lets you," not "allows you to." https://developers.google.com/style/word-list
- Avoid ableist and militaristic metaphors and outdated pairs like "master/slave" or "blacklist/whitelist." https://developers.google.com/style/inclusive-documentation
- Spell out abbreviations on first use. Write "that is" and "for example" instead of "i.e." and "e.g." https://developers.google.com/style/abbreviations

### Formatting
- Use sentence case for headings, not title case. https://developers.google.com/style/capitalization
- Match list type to content: numbered for sequences, bulleted for options. Keep list items grammatically parallel. https://developers.google.com/style/lists
- Write descriptive link text. Never "click here." https://developers.google.com/style/accessibility

### Audience
- Skip idioms, humor, and culture-specific references. "Ballpark figure" doesn't travel. https://developers.google.com/style/translation
- Use diverse example names and unambiguous date formats. https://developers.google.com/style/translation
- Don't make images carry information that text should carry. Pictures don't translate. https://developers.google.com/style/translation
- Avoid directional language like "the button on the right." Name the element instead. https://developers.google.com/style/accessibility

## Rules that do not transfer

These are artifacts of maintaining structured reference material rendered as fixed components on a docs site, and they have no analog in an email, a blog post, or a personal essay:

- Command-line syntax notation for optional and required flags (brackets, pipes). Only meaningful in a CLI reference. https://developers.google.com/style/code-syntax
- Code font for commands and file names, bold for UI labels. A markup convention tied to a rendering system, not a prose rule. https://developers.google.com/style
- Table header-row and cell-formatting rules. General prose rarely uses tables at all. https://developers.google.com/style/tables
- Description-list punctuation for run-in headings (period vs. colon, case after each). A docs layout tool, not a sentence-level rule.
- Product-name and trademark capitalization. A legal and branding requirement, not a style choice.
- The alt-text and semantic-HTML machinery for accessibility. The underlying instinct (describe images in words) transfers, but the HTML implementation does not.

We skip these because a general-purpose writing skill has no fixed component types to format. It only has sentences and paragraphs.

## Where Google's guide conflicts with "sound like a human"

- Exclamation points. Google says avoid them almost entirely. A human voice reaches for one when something is genuinely exciting or urgent. https://developers.google.com/style/tone
- Idioms and cultural references. Google forbids them for translatability. A personal or brand voice often uses them on purpose, because a shared reference is what makes writing sound like it came from a specific person. https://developers.google.com/style/translation
- Humor. Google warns against jokes and "wackiness." For a lot of writing, humor is the main thing making it enjoyable to read. https://developers.google.com/style/tone
- "Please." Google limits it to formal requests and apologies. Ordinary polite speech uses "please" freely, and cutting it everywhere can read as curt. https://developers.google.com/style/tone
- One universal register. Google flattens tone toward a single approachable-but-neutral voice so it scales across a huge, unknown, global readership. Writing to a known reader can be warmer, sharper, or funnier, because the audience isn't anonymous. https://developers.google.com/style/tone
- No hypotheticals. Google discourages "would" and future-tense speculation in favor of flat present tense. Persuasive and conversational writing often needs the hedge or the hypothetical to carry nuance ("that would help," "you might notice"). https://developers.google.com/style/tense
- No figurative language. Google cuts metaphor for translatability and clarity. General prose often needs a metaphor to make an abstract idea land emotionally, which a literal restatement can't do. https://developers.google.com/style/translation
- Sentence-case headings everywhere. A brand or personal voice may deliberately choose a distinct heading style for visual identity, especially in marketing copy. https://developers.google.com/style/capitalization

## How the two prior-art skills are structured

### nbj-write-clearly (daniel-p-green fork)
Repo: https://github.com/daniel-p-green/nbj-write-clearly

Layout: a compact `SKILL.md` plus a `references/` folder holding a conditional technical guide and an `official-index.md` that routes specialized questions to Google's live pages instead of duplicating them. Also present: `scripts/`, `README.md`, `AGENTS.md`, `EVALUATION.md`, MIT license.

SKILL.md sections, in order: Outcome, Apply the right authority, Write or revise, Protect meaning and voice, Validate.

The authority section sets a five-tier precedence: the user's explicit request first, then source facts, then project style, then Google's guidance, then other references last.

The "write or revise" section opens by telling the model to identify the reader and their goal, then put the result or purpose first, the core "lead with the reader's answer" trick. It follows with steps like naming the actor, putting conditions before actions, using familiar precise words defined on first use, and cutting throat-clearing.

The "protect meaning and voice" section lists what must survive a rewrite untouched: technical tokens, API names, file names, product identifiers, modal verbs, and caveats.

Validation is an eight-point checklist covering opening clarity, actor identification, condition placement, pronoun reference, consistency, factual accuracy, global readability, and voice preservation.

Modes: draft, revise, or audit. Audit reports findings without changing the text.

On demand vs. always: the ten-step process and the preservation rules load every time the skill runs. The technical reference and the official index load only when the content needs procedure, code, command, UI, table, or accessibility guidance.

### Bjorn Johansen's fork
Source: https://bjornjohansen.com/write-clearly-skill/

Three layers instead of one skill file. A roughly 15-line global baseline lives in `CLAUDE.md` and applies to every session automatically. The full skill loads on demand for actual documentation work. A preloaded copy is baked into the frontmatter of specific subagents that always produce docs, so those agents never need to load it separately.

The notable trick here is vendoring: instead of fetching the 70 Google style-guide pages live each time (which forces a lossy summary), the fork stores them as local Markdown files, so the model gets an exact, offline read of the rule text.

Scope is broadened past documentation to commit messages, code review comments, docstrings, merge-request descriptions, and changelog entries.

## What Nate B. Jones actually claimed

Jones posted on X (https://x.com/natebjones/status/2089457435459404093) that if you're tired of generic AI writing, sometimes called "Claude-lish" or "Chat-lish," you should tell your AI to read the Google Developer Docs Style Guide and build a skill around it, calling the result "like magic." He said he'd also tried the ASD-STE100 Simplified Technical English standard (a controlled-vocabulary rulebook built for aviation maintenance manuals) and found the Google guide worked better. It works, plausibly, because Google's guide turns "sound natural" into checkable rules instead of a vague adjective: active voice, present tense, short sentences, plain words, a reader-first sentence order. That gives a model something to enforce rather than a vibe to imitate. It's also free, public, and almost certainly present in the model's training data, so pointing at it costs nothing to set up. Choosing it over ASD-STE100 suggests Jones wanted a guide rigorous enough to cut jargon and bloat, but not so restrictive on vocabulary that it kills normal readability.
