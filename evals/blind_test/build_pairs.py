#!/usr/bin/env python3
"""Build the blind-test pairs for the writing-style eval.

Standard library only. Three subcommands:

  select              Pick candidate messages from the sent-mail corpus and
                       write private/prompts.jsonl and private/prompts_only.jsonl.

  shuffle --seed N    Pair each selected prompt's real body with the model's
                       generated body, randomize which side (A/B) holds the
                       real one, and write private/pairs_shuffled_N.jsonl and
                       private/key_N.json.

  score --seed N F    Read a judge's answers from file F and report accuracy
                       against private/key_N.json, plus the collected reasons.

Nothing under evals/blind_test/private/ is ever committed (see .gitignore).
"""
import argparse
import glob
import json
import os
import random
import re
import sys
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CORPUS_DIR = os.path.expanduser("~/writing-style/corpus")
DEFAULT_OUTPUT_DIR = os.path.join(SCRIPT_DIR, "private")

CONSUMER_MAIL_DOMAINS = {
    "gmail.com",
    "yahoo.com",
    "hotmail.com",
    "icloud.com",
    "me.com",
    "outlook.com",
    "aol.com",
}


# ---------------------------------------------------------------------------
# Corpus loading
# ---------------------------------------------------------------------------

def load_corpus_records(corpus_dir):
    """Read every sent_*.jsonl file in corpus_dir and return the records."""
    records = []
    for path in sorted(glob.glob(os.path.join(corpus_dir, "sent_*.jsonl"))):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                records.append(json.loads(line))
    return records


def load_jsonl(path):
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")


# ---------------------------------------------------------------------------
# select
# ---------------------------------------------------------------------------

def word_count(text):
    if not text:
        return 0
    return len(text.split())


def passes_filters(record, word_floor, word_ceiling):
    if not record.get("is_reply"):
        return False
    if record.get("to_self"):
        return False
    context = record.get("context")
    if not context or not str(context).strip():
        return False
    wc = word_count(record.get("body"))
    if wc < word_floor or wc > word_ceiling:
        return False
    return True


def guess_register(record):
    """professional if any recipient's domain isn't a consumer mail domain."""
    recipients = list(record.get("to") or []) + list(record.get("cc") or [])
    for addr in recipients:
        if "@" not in addr:
            continue
        domain = addr.rsplit("@", 1)[-1].strip().lower()
        if domain not in CONSUMER_MAIL_DOMAINS:
            return "professional"
    return "personal"


def select_pairs(records, word_floor=20, word_ceiling=200, target=20, cap=2):
    """Pick up to `target` qualifying records, spread across years and
    capped at `cap` messages per first recipient. Deterministic: no RNG."""
    qualifying = [r for r in records if passes_filters(r, word_floor, word_ceiling)]
    qualifying.sort(key=lambda r: (r.get("date") or "", r.get("id") or ""))

    by_year = defaultdict(list)
    for r in qualifying:
        year = (r.get("date") or "")[:4] or "unknown"
        by_year[year].append(r)

    years = sorted(by_year.keys())
    cursor = {y: 0 for y in years}
    recipient_counts = defaultdict(int)
    selected = []

    progressed = True
    while len(selected) < target and progressed:
        progressed = False
        for y in years:
            if len(selected) >= target:
                break
            lst = by_year[y]
            while cursor[y] < len(lst):
                rec = lst[cursor[y]]
                cursor[y] += 1
                to_list = rec.get("to") or []
                first_recipient = to_list[0] if to_list else None
                if first_recipient and recipient_counts[first_recipient] >= cap:
                    continue
                selected.append(rec)
                if first_recipient:
                    recipient_counts[first_recipient] += 1
                progressed = True
                break
    return selected


def cmd_select(args):
    corpus_dir = os.path.expanduser(args.corpus_dir)
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    records = load_corpus_records(corpus_dir)
    selected = select_pairs(
        records,
        word_floor=args.word_floor,
        word_ceiling=args.word_ceiling,
        target=args.target,
        cap=args.cap,
    )

    prompts = []
    prompts_only = []
    for r in selected:
        full = {
            "id": r["id"],
            "register": guess_register(r),
            "subject": r.get("subject") or "",
            "context": r.get("context") or "",
            "body": r.get("body") or "",
        }
        prompts.append(full)
        prompts_only.append({k: v for k, v in full.items() if k != "body"})

    write_jsonl(os.path.join(output_dir, "prompts.jsonl"), prompts)
    write_jsonl(os.path.join(output_dir, "prompts_only.jsonl"), prompts_only)

    years = sorted({(r.get("date") or "")[:4] for r in selected})
    print("selected %d records" % len(selected))
    print("year spread: %s" % (", ".join(years) if years else "none"))
    return selected


# ---------------------------------------------------------------------------
# shuffle
# ---------------------------------------------------------------------------

_SANITIZE_RULES = [
    (re.compile(r"-{5,}\s*(Forwarded message|Original Message).*", re.S | re.I), ""),
    (re.compile(r"^\s*>.*$", re.M), ""),
    (re.compile(r"\[image:[^\]]*\]", re.I), ""),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "[email]"),
    (re.compile(r"(?<!\d)(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}(?!\d)"), "[phone]"),
    (re.compile(r"<?https?://\S+>?"), "[link]"),
    (re.compile(r"<\[link\]>"), "[link]"),
    (re.compile(r"\*"), ""),
    (re.compile(r"[ \t]+\n"), "\n"),
    (re.compile(r"\n{3,}"), "\n\n"),
]


def sanitize(body):
    """Strip export artifacts and contact details so a judge sees only prose.

    Applied to both the real and the generated body so neither side carries
    a tell that has nothing to do with voice: forwarded blocks, quoted replies,
    image placeholders, addresses, phone numbers, links, and markdown emphasis.
    """
    out = body or ""
    for pattern, repl in _SANITIZE_RULES:
        out = pattern.sub(repl, out)
    return out.strip()


def cmd_shuffle(args):
    output_dir = args.output_dir
    prompts = load_jsonl(os.path.join(output_dir, "prompts.jsonl"))
    generated = load_jsonl(os.path.join(output_dir, "generated.jsonl"))
    generated_by_id = {g["id"]: g["body"] for g in generated}
    if getattr(args, "sanitize", False):
        for p in prompts:
            p["body"] = sanitize(p["body"])
        generated_by_id = {k: sanitize(v) for k, v in generated_by_id.items()}

    missing = [p["id"] for p in prompts if p["id"] not in generated_by_id]
    if missing:
        raise SystemExit(
            "missing generated bodies for ids: %s" % ", ".join(missing)
        )

    rng = random.Random(args.seed)
    pairs = []
    key = {}
    for i, p in enumerate(prompts, start=1):
        real_body = p["body"]
        gen_body = generated_by_id[p["id"]]
        if rng.random() < 0.5:
            a, b, real_side = real_body, gen_body, "A"
        else:
            a, b, real_side = gen_body, real_body, "B"
        pairs.append({"pair_no": i, "A": a, "B": b})
        key[str(i)] = real_side

    pairs_path = os.path.join(output_dir, "pairs_shuffled_%d.jsonl" % args.seed)
    key_path = os.path.join(output_dir, "key_%d.json" % args.seed)
    write_jsonl(pairs_path, pairs)
    with open(key_path, "w", encoding="utf-8") as f:
        json.dump(key, f, indent=2)

    print("wrote %d pairs to %s" % (len(pairs), pairs_path))
    print("wrote key to %s" % key_path)
    return pairs, key


# ---------------------------------------------------------------------------
# score
# ---------------------------------------------------------------------------

def cmd_score(args):
    output_dir = args.output_dir
    key_path = os.path.join(output_dir, "key_%d.json" % args.seed)
    with open(key_path, "r", encoding="utf-8") as f:
        key = json.load(f)

    judge_lines = load_jsonl(args.judge_file)
    reasons = []
    correct = 0
    total = 0
    for line in judge_lines:
        pair_no = line["pair_no"]
        answer = line.get("answer")
        reason = line.get("reason", "")
        expected = key.get(str(pair_no))
        is_correct = answer == expected
        total += 1
        if is_correct:
            correct += 1
        reasons.append({"pair_no": pair_no, "correct": is_correct, "reason": reason})

    accuracy = correct / total if total else 0.0
    print("accuracy: %d/%d = %.1f%%" % (correct, total, accuracy * 100))
    print("reasons:")
    for r in reasons:
        status = "correct" if r["correct"] else "incorrect"
        print("  pair %s (%s): %s" % (r["pair_no"], status, r["reason"]))

    return accuracy, reasons


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_arg_parser():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)

    p_select = sub.add_parser("select", help="Select prompts from the corpus.")
    p_select.add_argument("--corpus-dir", default=DEFAULT_CORPUS_DIR)
    p_select.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    p_select.add_argument("--word-floor", type=int, default=20)
    p_select.add_argument("--word-ceiling", type=int, default=200)
    p_select.add_argument("--target", type=int, default=20)
    p_select.add_argument("--cap", type=int, default=2)
    p_select.set_defaults(func=cmd_select)

    p_shuffle = sub.add_parser("shuffle", help="Shuffle real/generated bodies into A/B pairs.")
    p_shuffle.add_argument("--seed", type=int, required=True)
    p_shuffle.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    p_shuffle.add_argument("--sanitize", action="store_true",
                           help="Strip forwarded blocks, quoted lines, addresses, phones, links from both sides.")
    p_shuffle.set_defaults(func=cmd_shuffle)

    p_score = sub.add_parser("score", help="Score judge answers against the key.")
    p_score.add_argument("--seed", type=int, required=True)
    p_score.add_argument("judge_file")
    p_score.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    p_score.set_defaults(func=cmd_score)

    return parser


def main(argv=None):
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
