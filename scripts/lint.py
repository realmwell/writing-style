#!/usr/bin/env python3
"""Deterministic checker for the writing-style skill.

Usage: python3 scripts/lint.py FILE [--register personal|professional|sales|marketing]

Prints one finding per line as LEVEL: message (line N), then a SUMMARY line.
Exit 1 if any ERROR, else 0. Standard library only. Never rewrites anything.
Lines that start with "Before:" are exempt so reference files can show bad examples.
Regions between <!-- lint:off --> and <!-- lint:on --> are skipped, as is any line
containing "lint:ignore". Use these for word lists and teaching examples only.
"""
import argparse
import re
import sys
from statistics import mean, pstdev

REGISTERS = ("personal", "professional", "sales", "marketing")

TIER_A_STEMS = ("emphasiz", "enhanc", "highlight", "showcas")
TIER_B = ("leverage", "leverages", "leveraged", "leveraging", "foster", "fosters", "fostering", "underscore",
          "underscores", "boast", "boasts", "garner", "garners", "bolster", "bolsters", "streamline", "streamlines",
          "streamlined", "navigate", "navigates", "navigating", "elevate", "elevates", "unveil", "unveils", "unlock",
          "unlocks", "harness", "harnesses", "interplay", "pivotal", "crucial", "vital", "robust", "comprehensive",
          "seamless", "seamlessly", "transformative", "groundbreaking", "cutting-edge", "innovative", "holistic",
          "multifaceted", "nuanced", "enduring", "align with", "aligns with", "aligned with", "associated with")
TIER_C = ("delve", "delves", "delving", "tapestry", "testament", "meticulous", "meticulously", "landscape",
          "intricate", "intricacies", "realm", "vibrant")
CLAUDE_WATCH = ("genuinely", "honestly", "quietly", "the real", "chef's kiss", "load-bearing")
HEDGES = ("may", "might", "could", "perhaps", "possibly", "arguably", "somewhat", "largely", "tends to",
          "in some sense", "sort of", "kind of", "generally", "almost", "i think", "it seems")
SUMMARY_PHRASES = ("in summary", "in conclusion", "to sum up", "overall,", "at the end of the day", "the bottom line")
CHATBOT = ("great question", "you're absolutely right", "you are absolutely right", "i hope this helps",
           "let me know if", "here is a", "here's a", "here is an", "here's an", "certainly!", "of course!")
DEBRIS = ("contentReference", "oaicite", "[cite:", "grok_card", "【")
SPAM = ("free", "guarantee", "act now", "risk-free", "no obligation", "buy now", "winner")

CONTRASTIVE = re.compile(r"\b(?:not|isn't|isn't|aren't|wasn't|is not|are not) (?:just|only|merely|simply) [^.!?]{1,60}, (?:it's|it is|but|they're|that's)\b", re.I)
FRAGMENT = re.compile(r"(?:^|[.!?]\s+)Not [^.!?]{1,40}\.\s+[A-Z]")
BOLD_LEAD = re.compile(r"^\s*[-*]\s+\*\*[^*]+\*\*:?")
HEADING = re.compile(r"^#{1,6}\s+(.*)")


def _word_re(term):
    return re.compile(r"(?<![\w-])" + re.escape(term) + r"(?![\w-])", re.I)


def _stem_re(stem):
    return re.compile(r"\b" + re.escape(stem) + r"\w*", re.I)


def _strip(text):
    """Return list of (line_no, line) with frontmatter, code fences, and Before: lines removed."""
    lines = text.split("\n")
    out = []
    in_code = False
    i = 0
    if lines and lines[0].strip() == "---":
        j = 1
        while j < len(lines) and lines[j].strip() != "---":
            j += 1
        i = j + 1
    lint_off = False
    for n in range(i, len(lines)):
        ln = lines[n]
        stripped = ln.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if "<!-- lint:off -->" in stripped:
            lint_off = True
            continue
        if "<!-- lint:on -->" in stripped:
            lint_off = False
            continue
        if in_code or lint_off or "lint:ignore" in ln or ln.lstrip().startswith("Before:"):
            continue
        out.append((n + 1, ln))
    return out


def _sentences(prose):
    parts = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", prose).strip())
    return [p for p in parts if re.search(r"[A-Za-z]", p)]


def _paragraphs(kept):
    paras, cur = [], []
    for _, ln in kept:
        if ln.strip():
            cur.append(ln.strip())
        elif cur:
            paras.append(" ".join(cur))
            cur = []
    if cur:
        paras.append(" ".join(cur))
    return paras


def run(text, register="professional"):
    if register not in REGISTERS:
        raise ValueError(f"unknown register {register}")
    personal = register == "personal"
    kept = _strip(text)
    findings = []

    def add(level, msg, line):
        findings.append((level, msg, line))

    for n, ln in kept:
        low = ln.lower()
        if "—" in ln:
            add("ERROR", "em dash; use ' - ' or a comma", n)
        for tag in DEBRIS:
            if tag in ln:
                add("ERROR", f"model debris '{tag}'", n)
        for stem in TIER_A_STEMS:
            for m in _stem_re(stem).finditer(ln):
                add("INFO" if personal else "ERROR", f"tier A word '{m.group(0)}'", n)
        if not personal:
            for term in TIER_B:
                if _word_re(term).search(ln):
                    add("ERROR" if register in ("sales", "marketing") else "WARN", f"tier B word '{term}'", n)
            for term in CLAUDE_WATCH:
                if _word_re(term).search(ln):
                    add("WARN", f"claude watch word '{term}'", n)
        for phrase in CHATBOT:
            if phrase in low:
                add("WARN", f"chatbot artifact '{phrase}'", n)
        if BOLD_LEAD.match(ln):
            add("WARN", "bold lead-in bullet", n)
        h = HEADING.match(ln)
        if h:
            words = [w for w in re.findall(r"[A-Za-z][A-Za-z'-]*", h.group(1)) if len(w) >= 4]
            if len(words) >= 2 and sum(1 for w in words if w[0].isupper()) > len(words) / 2:
                add("WARN", "title case heading; use sentence case", n)
        if register == "sales":
            for term in SPAM:
                if _word_re(term).search(ln):
                    add("WARN", f"spam trigger word '{term}'", n)

    prose = "\n".join(ln for _, ln in kept)
    if not personal:
        tier_c_hits = {t for t in TIER_C if _word_re(t).search(prose)}
        if len(tier_c_hits) >= 2:
            add("WARN", "tier C cluster: " + ", ".join(sorted(tier_c_hits)), 0)

    excl = prose.count("!")
    if register == "sales" and excl:
        add("ERROR", f"exclamation point in sales ({excl})", 0)
    elif register == "professional" and excl > 3:
        add("WARN", f"more than three exclamation points ({excl})", 0)
    elif register == "marketing" and excl > 1:
        add("WARN", f"more than one exclamation point ({excl})", 0)

    level = "WARN" if personal else "ERROR"
    for m in CONTRASTIVE.finditer(prose):
        add(level, "'not X, it's Y' contrastive binary", 0)
    for m in FRAGMENT.finditer(prose):
        add(level, "'Not X. Y.' negation fragment", 0)

    sents = _sentences(prose)
    if not personal:
        for s in sents:
            hits = [h for h in HEDGES if _word_re(h).search(s)]
            if len(hits) >= 2:
                add("WARN", "stacked hedges: " + ", ".join(hits), 0)

    paras = _paragraphs(kept)
    if paras:
        last = paras[-1].lower()
        for phrase in SUMMARY_PHRASES:
            if phrase in last:
                add("WARN", f"closing summary phrase '{phrase.strip(',')}'", 0)
    plens = [len(p.split()) for p in paras]
    if len(plens) >= 4:
        m = mean(plens)
        if m and all(abs(x - m) <= 0.2 * m for x in plens):
            add("WARN", "uniform paragraph lengths", 0)

    slens = [len(re.findall(r"[A-Za-z'’-]+", s)) for s in sents]
    slens = [x for x in slens if x]
    if len(slens) >= 6 and pstdev(slens) < 6:
        add("WARN", f"low burstiness: sentence length stdev {pstdev(slens):.1f}", 0)
    wc = len(re.findall(r"[A-Za-z'’-]+", prose))
    if slens:
        add("INFO", f"{wc} words, {len(slens)} sentences, mean {mean(slens):.1f}, stdev {pstdev(slens):.1f}", 0)
    else:
        add("INFO", f"{wc} words, 0 sentences", 0)
    return findings


def main(argv=None):
    ap = argparse.ArgumentParser(description="Lint prose against the writing-style rules.")
    ap.add_argument("file")
    ap.add_argument("--register", default="professional", choices=REGISTERS)
    args = ap.parse_args(argv)
    with open(args.file, encoding="utf-8") as f:
        text = f.read()
    findings = run(text, args.register)
    errors = warns = 0
    for level, msg, line in findings:
        loc = f" (line {line})" if line else ""
        print(f"{level}: {msg}{loc}")
        errors += level == "ERROR"
        warns += level == "WARN"
    print(f"SUMMARY: {errors} errors, {warns} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
