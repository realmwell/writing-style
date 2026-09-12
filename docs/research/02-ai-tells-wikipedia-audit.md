# AI-tells audit: humanizer skill vs. current Wikipedia "Signs of AI writing"

Access date: 2026-09-12. Primary source: [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), plus its [edit history](https://en.wikipedia.org/w/index.php?title=Wikipedia:Signs_of_AI_writing&action=history) and [WikiProject AI Cleanup/Guide](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup/Guide). The page was edit-protected on 2026-09-12 after heavy disruptive editing; it has been revised 30+ times since August 23, 2026, mostly example cleanup and wording tweaks, not new patterns.

## 1. Patterns on the current page the humanizer skill misses

- **Vague connection phrasing**: "in connection with," "associated with," "particularly associated with" used instead of a direct claim. Example: "identified as being associated with leadership" instead of "was CEO."
- **List/broad titles treated as proper nouns**: A lead defines a non-proper-noun title as if it were a formal entity. Example: "Catchment area (health) refers to the geographic area..."
- **"X and Y" section headers as a tic**: "Awards and Recognition," "Challenges and Legacy" used reflexively, not because content demands two axes.
- **Structural markup tells**: headings that contain only subheadings with no body text, skipped heading levels, overuse of level-1 headings, decorative horizontal-rule breaks between sections, and unusual/unnecessary tables.
- **Negative-parallelism subtype "Y rather than X"**: humanizer only covers "not just X, it's Y" and "not X, but Y." The page separately tracks "rather than" framing.
- **Leftover model artifacts**: literal copy-paste debris like ChatGPT's `contentReference`/`oaicite`, Gemini's `[cite: 1]`, Grok's `grok_card`, DeepSeek's lenticular brackets. Not style, but a hard tell worth a mechanical grep.
- **"Signs of human writing" (positive checks)**: ability to explain a specific editorial choice, distinctive personal syntax, text predating November 2022. The page treats these as counter-evidence, not just AI-ism removal.
- **Explicit "ineffective indicators" and meta-caveat**: the page warns these are "signs of a problem, not the problem itself" and that treating the signs themselves as the target "could just make detection harder." Humanizer has no equivalent caution against over-indexing on the checklist.
- **Detection-accuracy caveat**: cites a 2025 study that humans overall detect AI text "no better than random chance," while heavy LLM users hit roughly 90%. Useful context the skill doesn't carry.
- **Model-specific vocabulary**: Grok overuses "causal, empirical, correlate" and keeps overusing "underscore" past when other models dropped it. Humanizer treats "AI vocabulary" as one undifferentiated list.

## 2. Patterns softened, reworded, or no longer emphasized

- **Em dashes**: the companion Guide page now explicitly hedges: "emdashes often appear in human-written content as well" (WP:AIDASH). The page still lists em-dash overuse, but no longer treats it as a standalone tell: it wants it paired with other signals. Humanizer's section 13 and writing-style's "CRITICAL... #1 AI tell... maximum one per page" both present it as near-decisive, which the source page no longer supports.
- **AI vocabulary is now tiered by era, not one flat list**: the page splits words into 2023–mid-2024 ("delve," "tapestry," "testament," "meticulous," "landscape"), mid-2024–mid-2025 ("align with," "fostering," "showcasing"), and mid-2025-onward (just "emphasizing," "enhance," "highlighting," "showcasing"). Several of humanizer's headline words ("delve," "tapestry," "testament," "intricate") have dropped out of the current tier: they're first-wave tells, still worth flagging in older-model output but weaker evidence against current models.
- **Knowledge-cutoff disclaimers**: the page now buckets "I'm an AI, my training data..." language under **historical/outdated** signs, phased out by late 2024 as products hardened their system prompts. Humanizer's section 20 presents this as a live, current pattern without noting it's now rare outside jailbroken or older-model output.
- **Markdown-as-tell weakened**: the Guide page notes markdown formatting used to be a signal but has become less reliable as more contexts legitimately expect markdown. Neither skill mentions markdown at all, so this is moot for them, but worth knowing if the pattern list is ever extended.

## 3. Patterns that look outdated (or newly emerging) for 2026 models - flagged as judgment/speculation

- **"delve" specifically**: strong signal for 2023 GPT-3.5/4 output; the current page no longer lists it in its mid-2025+ tier. Likely still a tell for older or smaller models, weak evidence against frontier 2026 models. Judgment call, not sourced as "gone."
- **Em dash overuse**: search evidence shows GPT-4o used roughly 10x more em dashes than GPT-3.5, and GPT-4.1 more still ([Sean Goedecke, "Why do AI models use so many em-dashes?"](https://www.seangoedecke.com/em-dashes/)). No public data confirms whether September 2026 flagship models (GPT-6 Astra, Claude Fable 5.1) kept that rate. Treat "still elevated" as speculation; treat "no longer decisive alone" as sourced (see above).
- **Staccato fragments and deliberate cadence breaks**: multiple 2026 writing-tool comparisons describe Claude's prose as using "short staccato fragments for dramatic effect" and "deliberate fragments" to vary rhythm ([Fable, "Claude vs ChatGPT for Creative Writing 2026"](https://www.fable.la/blog/claude-vs-chatgpt-creative-writing); [arslandg.substack.com](https://arslandg.substack.com/p/claude-vs-chatgpt-in-2026-the-honest)). This is speculation, not a Wikipedia-sourced tell, but it lines up with "Not X. Y." fragment patterns and one-line paragraphs the task asked about: the current Wikipedia page has not caught these yet (checked directly: no section addresses "genuinely," "quietly," staccato fragments, or "Not X. Y." patterns).
- **"You're absolutely right!" reflex**: still called out in 2026 commentary as ChatGPT's most-upvoted user complaint, so sycophantic-tone tells (already in humanizer #21) remain current, not outdated.
- **New colon-preamble pattern (speculative, per search, not independently verified on-page)**: "Major/comprehensive [X]:" openers reported as a 2025-onward tell. Neither skill covers it. Flag as worth testing against real 2026 output before adopting.
- **Elegant variation / synonym cycling**: the page marks this as declining ("less frequent now") in its historical-indicators section, while humanizer still presents it (#11) as a live, common pattern. Likely still real but weaker than the page implies it once was.

## 4. Merged, deduplicated master list

**(1) Content-level**
- *Significance inflation*: puffing up an arbitrary fact's importance. "The vote marked a pivotal moment for the region." → "The vote passed 62 to 38."
- *Notability namedropping*: listing outlets/followers instead of quoting content. "Featured in the Times, BBC, and NPR." → "The Times quoted her 2024 comment on rate cuts."
- *Superficial -ing tack-ons*: fake depth glued onto a plain sentence. "The mural uses red, reflecting the town's history." → "The mural is red because the co-op couldn't afford more paint."
- *Vague attribution*: opinions pinned on nobody in particular. "Experts say the bridge is at risk." → "A 2023 state inspection rated the bridge structurally deficient."
- *Formulaic challenges section*: negative-then-hopeful template close. "Despite challenges, the town continues to thrive." → "The mill closed in 2019; two cafes opened in its place."
- *Vague connection phrasing*: dodging a direct claim. "He was associated with the campaign." → "He ran the campaign's field operations."
- *Awards-and-recognition reflex heading*: a two-noun header used out of habit, not need. "## Awards and Recognition" (empty of real content) → cut the header; state the one award in a sentence.

**(2) Sentence-level**
- *Negative parallelism*: "not just X, it's Y" in any of its three forms. "It's not just a song, it's a statement." → "The chorus is the whole point of the song."
- *Rule of three*: forcing items into triads for false comprehensiveness. "Innovation, inspiration, and insight." → "Two workshops and a Q&A."
- *Copula avoidance*: swapping "is" for "serves as/boasts/features." "The gallery serves as LAAA's exhibition space." → "The gallery is LAAA's exhibition space."
- *Elegant variation*: cycling synonyms to dodge repeating a noun. "The protagonist... the main character... the hero..." → "She... she... she..."
- *False range*: "from X to Y" where X and Y aren't a real scale. "From the Big Bang to the birth of stars." → "The book covers the Big Bang and star formation."
- *Participial tail*: a dangling "-ing" clause bolted onto the end. "The bill passed, marking a shift in policy." → "The bill passed. It's the first change to the law since 2011."
- *Preview/wrap chatbot framing*: "here's what we'll cover" or "to sum up" used as connective tissue. "Here's what we'll cover in this guide." → just start with the first point.

**(3) Word-level: top 40 diagnostic words**
delve, leverage, foster, underscore, showcase, highlight (verb), emphasize, enhance, boast, garner, bolster, streamline, navigate, elevate, unveil, unlock, harness, tapestry, landscape (abstract), interplay, intricate/intricacies, meticulous, pivotal, crucial, vital, robust, comprehensive, seamless, transformative, groundbreaking, cutting-edge, innovative, holistic, multifaceted, nuanced, testament, enduring, vibrant, align with, associated with.

Note: per the page's own tiering, "delve," "tapestry," "testament," "meticulous," and "landscape" are first-wave (2023–mid-2024) tells, weaker evidence against 2026 output on their own. "Emphasizing," "enhance," "highlighting," "showcasing" are the current (mid-2025+) tier and the most diagnostic right now.

**(4) Punctuation and formatting**
- *Em dash overuse* — real, but no longer decisive alone; pair with other tells. "The plan—ambitious as it was—failed." → "The plan was ambitious. It failed."
- *Mechanical boldface*: bolding terms with no emphasis logic. "It blends **OKRs** and **KPIs**." → "It blends OKRs and KPIs."
- *Inline-header bullet lists*: "**Term:** definition" repeated down a list. "**Speed:** Faster load times." → "Pages load faster now."
- *Title case headings*: every word capitalized out of habit. "## Strategic Negotiations And Global Partnerships" → "## Strategic negotiations and global partnerships"
- *Emoji as structure*: emoji standing in for actual organization. "🚀 **Launch:** Q3" → "The launch is set for Q3."
- *Curly quotes in plain text*: "smart" quote marks where straight ones are the convention. "He said "it's on track."" → "He said "it's on track.""
- *Headings with no body*: a parent heading holding only subheadings, nothing else.

**(5) Chatbot artifacts**
- *Correspondence pasted as content*: "Here is an overview..." or "I hope this helps!" left in the output. "Here is an overview of the topic. I hope this helps!" → open with the first real sentence, cut the framing entirely.
- *Sycophantic tone*: "Great question! You're absolutely right." → skip straight to the answer.
- *Knowledge-cutoff hedge*: now mostly a legacy tell, largely trained out since late 2024. "As of my last update..." → state what you know, cite the source and date.
- *Excessive hedging*: stacking qualifiers until the claim disappears. "It could potentially possibly be argued that..." → "This may affect outcomes."
- *Generic upbeat closer*: a vague, energetic sign-off with no content. "The future looks bright. Exciting times ahead." → end on the last concrete fact instead.

## 5. Contradictions between the two skills

- **"Here is a..." vs. "Here's what we'll cover..."**: humanizer (section 19, line 317) flags "here is a..." as a chatbot artifact to delete, with "Here is an overview of the French Revolution" as the bad example. writing-style's "Approved Transitions" (line 99) explicitly recommends "Here's what we'll cover..." and "This guide walks you through..." as natural previewing language. Same construction, opposite verdict.
- **Confident-and-unqualified vs. acknowledge-complexity**: writing-style's core principle 4 says "Confident over qualified: Remove 'almost,' 'very,' 'really'" and its filler list bans "basically" and "definitely" outright. humanizer's own featured "humanized" rewrite uses both: "Definitely not architecture" and "you're basically guessing" (its own worked example, lines 456–462). One skill's model answer violates the other skill's explicit ban.
- **Em dash tolerance**: humanizer treats em dashes as one pattern among many to trim case-by-case. writing-style hard-caps it at "Maximum one per page" and calls it "the #1 AI tell." Given the source page's own hedge that em dashes are common in human writing too, writing-style's absolute cap is stricter than the evidence supports, and stricter than humanizer's own stance.
- **Templated structure vs. anti-formula**: humanizer explicitly kills formulaic three-part templates and outline-like sections (rule of three, "Challenges and Future Prospects"). writing-style's SEO/AEO section prescribes its own three/four-part templates ("evidence sandwich: claim → evidence bullets → concluding insight," definition blocks, step-by-step blocks, comparison tables) for every SEO piece. Followed literally, writing-style's SEO rules reproduce the same formulaic shape humanizer is built to strip out.
