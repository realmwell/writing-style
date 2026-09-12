"""Unit tests for build_pairs.py.

These tests use synthetic records written to a temp directory. They never
read the real corpus under ~/writing-style/corpus/.
"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import build_pairs  # noqa: E402


def make_record(
    id_,
    date="2020-05-01T00:00:00Z",
    to=None,
    cc=None,
    subject="Re: hi",
    body_words=30,
    context="some context here",
    is_reply=True,
    to_self=False,
):
    body = " ".join(["word"] * body_words) if body_words is not None else ""
    return {
        "id": id_,
        "threadId": "t-" + id_,
        "date": date,
        "to": to if to is not None else ["friend@gmail.com"],
        "cc": cc if cc is not None else [],
        "subject": subject,
        "body": body,
        "raw_len": len(body),
        "signoff": None,
        "context": context,
        "is_reply": is_reply,
        "to_self": to_self,
    }


def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")


class SelectionFilterTests(unittest.TestCase):
    def test_word_count_bounds(self):
        too_short = make_record("a", body_words=5)
        too_long = make_record("b", body_words=250)
        just_right = make_record("c", body_words=50)
        floor_edge = make_record("d", body_words=20)
        ceiling_edge = make_record("e", body_words=200)

        self.assertFalse(build_pairs.passes_filters(too_short, 20, 200))
        self.assertFalse(build_pairs.passes_filters(too_long, 20, 200))
        self.assertTrue(build_pairs.passes_filters(just_right, 20, 200))
        self.assertTrue(build_pairs.passes_filters(floor_edge, 20, 200))
        self.assertTrue(build_pairs.passes_filters(ceiling_edge, 20, 200))

    def test_is_reply_required(self):
        not_reply = make_record("a", is_reply=False)
        is_reply = make_record("b", is_reply=True)
        self.assertFalse(build_pairs.passes_filters(not_reply, 20, 200))
        self.assertTrue(build_pairs.passes_filters(is_reply, 20, 200))

    def test_context_required(self):
        no_context = make_record("a", context=None)
        empty_context = make_record("b", context="")
        blank_context = make_record("c", context="   ")
        has_context = make_record("d", context="a real snippet of context")
        self.assertFalse(build_pairs.passes_filters(no_context, 20, 200))
        self.assertFalse(build_pairs.passes_filters(empty_context, 20, 200))
        self.assertFalse(build_pairs.passes_filters(blank_context, 20, 200))
        self.assertTrue(build_pairs.passes_filters(has_context, 20, 200))

    def test_to_self_excluded(self):
        self_msg = make_record("a", to_self=True)
        other_msg = make_record("b", to_self=False)
        self.assertFalse(build_pairs.passes_filters(self_msg, 20, 200))
        self.assertTrue(build_pairs.passes_filters(other_msg, 20, 200))

    def test_per_recipient_cap(self):
        # Three qualifying messages to the same first recipient; cap is 2.
        records = [
            make_record("a", date="2019-01-01T00:00:00Z", to=["x@work.com"]),
            make_record("b", date="2019-02-01T00:00:00Z", to=["x@work.com"]),
            make_record("c", date="2019-03-01T00:00:00Z", to=["x@work.com"]),
        ]
        selected = build_pairs.select_pairs(records, word_floor=20, word_ceiling=200, target=20, cap=2)
        self.assertEqual(len(selected), 2)
        ids = {r["id"] for r in selected}
        self.assertEqual(ids, {"a", "b"})

    def test_selection_end_to_end_with_temp_corpus(self):
        with tempfile.TemporaryDirectory() as corpus_dir, tempfile.TemporaryDirectory() as out_dir:
            records = []
            years = ["2017", "2018", "2019", "2020", "2021"]
            for i in range(30):
                year = years[i % len(years)]
                records.append(
                    make_record(
                        "id%02d" % i,
                        date="%s-01-01T00:00:00Z" % year,
                        to=["recipient%d@gmail.com" % i],
                    )
                )
            # A batch that should all be filtered out.
            records.append(make_record("bad-reply", is_reply=False))
            records.append(make_record("bad-self", to_self=True))
            records.append(make_record("bad-short", body_words=3))
            records.append(make_record("bad-context", context=None))

            write_jsonl(os.path.join(corpus_dir, "sent_2017-2021.jsonl"), records)

            args = build_pairs.build_arg_parser().parse_args(
                [
                    "select",
                    "--corpus-dir",
                    corpus_dir,
                    "--output-dir",
                    out_dir,
                    "--target",
                    "20",
                ]
            )
            args.func(args)

            prompts_path = os.path.join(out_dir, "prompts.jsonl")
            prompts_only_path = os.path.join(out_dir, "prompts_only.jsonl")
            self.assertTrue(os.path.exists(prompts_path))
            self.assertTrue(os.path.exists(prompts_only_path))

            with open(prompts_path) as f:
                prompts = [json.loads(line) for line in f]
            with open(prompts_only_path) as f:
                prompts_only = [json.loads(line) for line in f]

            self.assertEqual(len(prompts), 20)
            self.assertEqual(len(prompts_only), 20)
            for p in prompts:
                self.assertIn("body", p)
                self.assertIn("register", p)
            for p in prompts_only:
                self.assertNotIn("body", p)


class RegisterGuessTests(unittest.TestCase):
    def test_all_consumer_domains_is_personal(self):
        rec = make_record("a", to=["friend@gmail.com", "other@yahoo.com"])
        self.assertEqual(build_pairs.guess_register(rec), "personal")

    def test_any_non_consumer_domain_is_professional(self):
        rec = make_record("a", to=["friend@gmail.com", "boss@company.com"])
        self.assertEqual(build_pairs.guess_register(rec), "professional")


class ShuffleTests(unittest.TestCase):
    def setUp(self):
        self.out_dir = tempfile.mkdtemp()
        self.prompts = [
            {"id": "p%d" % i, "register": "personal", "subject": "s", "context": "c", "body": "REAL-%d" % i}
            for i in range(10)
        ]
        write_jsonl(os.path.join(self.out_dir, "prompts.jsonl"), self.prompts)
        generated = [{"id": p["id"], "body": "GEN-%s" % p["id"]} for p in self.prompts]
        write_jsonl(os.path.join(self.out_dir, "generated.jsonl"), generated)

    def _run_shuffle(self, seed):
        args = build_pairs.build_arg_parser().parse_args(
            ["shuffle", "--seed", str(seed), "--output-dir", self.out_dir]
        )
        args.func(args)

    def test_key_maps_each_pair_to_side_with_real_body(self):
        self._run_shuffle(1)
        pairs_path = os.path.join(self.out_dir, "pairs_shuffled_1.jsonl")
        key_path = os.path.join(self.out_dir, "key_1.json")
        with open(pairs_path) as f:
            pairs = [json.loads(line) for line in f]
        with open(key_path) as f:
            key = json.load(f)

        self.assertEqual(len(pairs), 10)
        for pair in pairs:
            pair_no = pair["pair_no"]
            real_side = key[str(pair_no)]
            self.assertIn(real_side, ("A", "B"))
            real_text = pair[real_side]
            other_side = "B" if real_side == "A" else "A"
            other_text = pair[other_side]
            self.assertTrue(real_text.startswith("REAL-"))
            self.assertTrue(other_text.startswith("GEN-"))

    def test_ab_order_varies_across_pairs_for_fixed_seed(self):
        self._run_shuffle(2)
        pairs_path = os.path.join(self.out_dir, "pairs_shuffled_2.jsonl")
        key_path = os.path.join(self.out_dir, "key_2.json")
        with open(key_path) as f:
            key = json.load(f)
        sides = [key[str(i)] for i in range(1, 11)]
        # With 10 pairs and a real coin flip per pair, both sides must appear.
        self.assertIn("A", sides)
        self.assertIn("B", sides)

    def test_shuffle_is_deterministic_for_same_seed(self):
        self._run_shuffle(3)
        key_path = os.path.join(self.out_dir, "key_3.json")
        with open(key_path) as f:
            key_first = json.load(f)
        self._run_shuffle(3)
        with open(key_path) as f:
            key_second = json.load(f)
        self.assertEqual(key_first, key_second)


class ScoreTests(unittest.TestCase):
    def setUp(self):
        self.out_dir = tempfile.mkdtemp()
        self.seed = 7
        key = {"1": "A", "2": "B", "3": "A", "4": "B"}
        with open(os.path.join(self.out_dir, "key_%d.json" % self.seed), "w") as f:
            json.dump(key, f)

    def _judge_file(self, lines):
        path = os.path.join(self.out_dir, "judge.jsonl")
        write_jsonl(path, lines)
        return path

    def test_accuracy_computed_correctly(self):
        judge_lines = [
            {"pair_no": 1, "answer": "A", "reason": "formal tone"},
            {"pair_no": 2, "answer": "A", "reason": "too polished"},  # wrong
            {"pair_no": 3, "answer": "A", "reason": "typo present"},
            {"pair_no": 4, "answer": "B", "reason": "short and blunt"},
        ]
        judge_path = self._judge_file(judge_lines)
        args = build_pairs.build_arg_parser().parse_args(
            ["score", "--seed", str(self.seed), "--output-dir", self.out_dir, judge_path]
        )
        accuracy, reasons = args.func(args)
        self.assertAlmostEqual(accuracy, 0.75)
        self.assertEqual(len(reasons), 4)

    def test_reasons_are_collected(self):
        judge_lines = [
            {"pair_no": 1, "answer": "A", "reason": "formal tone"},
            {"pair_no": 2, "answer": "A", "reason": "too polished"},
        ]
        judge_path = self._judge_file(judge_lines)
        args = build_pairs.build_arg_parser().parse_args(
            ["score", "--seed", str(self.seed), "--output-dir", self.out_dir, judge_path]
        )
        _, reasons = args.func(args)
        collected = [r["reason"] for r in reasons]
        self.assertEqual(collected, ["formal tone", "too polished"])
        self.assertTrue(reasons[0]["correct"])
        self.assertFalse(reasons[1]["correct"])


class SanitizeTests(unittest.TestCase):
    def test_strips_artifacts_and_contact_details(self):
        raw = (
            "Hi there,\n\nCall me at 215-555-0100 or mail max@example.com. See <https://x.y/z>.\n\n"
            "Thanks so much,\n\nMax\n\n---------- Forwarded message ----------\nFrom: someone\nquoted stuff\n"
        )
        out = build_pairs.sanitize(raw)
        self.assertNotIn("215-555-0100", out)
        self.assertNotIn("max@example.com", out)
        self.assertNotIn("https://", out)
        self.assertNotIn("Forwarded message", out)
        self.assertNotIn("quoted stuff", out)
        self.assertIn("[phone]", out)
        self.assertIn("[email]", out)
        self.assertIn("[link]", out)
        self.assertTrue(out.endswith("Max"))

    def test_strips_quoted_lines_and_emphasis(self):
        raw = "Yes and they said:\n> earlier text here\nI would *love* to.\n\n\n\nMax"
        out = build_pairs.sanitize(raw)
        self.assertNotIn("earlier text", out)
        self.assertIn("I would love to.", out)
        self.assertNotIn("\n\n\n", out)


if __name__ == "__main__":
    unittest.main()
