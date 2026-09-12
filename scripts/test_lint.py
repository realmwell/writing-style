"""Tests for scripts/lint.py. Run: python3 -m unittest scripts/test_lint.py -v"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import lint  # noqa: E402

CLEAN = (
    "Hi Dana,\n\nThanks for the quick turnaround on the estimate. Two things.\n\n"
    "The scope lists the roof work but not the crane, and the vendor told me on the phone that the "
    "crane is the part that drives the timeline they keep calling a while. Can you confirm it's in? "
    "They also offered window units tomorrow as a stopgap. We'd take that.\n\n"
    "Could you help us get it scheduled?\n\nThanks,\n\nMax\n"
)


def levels(findings, level):
    return [f for f in findings if f[0] == level]


def has(findings, level, needle):
    return any(f[0] == level and needle.lower() in f[1].lower() for f in findings)


class CleanText(unittest.TestCase):
    def test_clean_professional_has_no_errors_or_warnings(self):
        f = lint.run(CLEAN, "professional")
        self.assertEqual(levels(f, "ERROR"), [])
        self.assertEqual(levels(f, "WARN"), [])
        self.assertTrue(has(f, "INFO", "words"))


class EmDash(unittest.TestCase):
    def test_em_dash_is_error_in_every_register(self):
        for reg in ("personal", "professional", "sales", "marketing"):
            self.assertTrue(has(lint.run("The plan — such as it was — failed.", reg), "ERROR", "em dash"))

    def test_before_lines_are_exempt(self):
        self.assertFalse(has(lint.run("Before: The plan — ambitious — failed.", "professional"), "ERROR", "em dash"))


class Vocabulary(unittest.TestCase):
    def test_tier_a_error_outside_personal_info_inside(self):
        text = "This will enhance the process and we are showcasing results."
        self.assertTrue(has(lint.run(text, "professional"), "ERROR", "tier a"))
        self.assertTrue(has(lint.run(text, "sales"), "ERROR", "tier a"))
        f = lint.run(text, "personal")
        self.assertFalse(has(f, "ERROR", "tier a"))
        self.assertTrue(has(f, "INFO", "tier a"))

    def test_tier_b_error_in_sales_warn_in_professional_silent_in_personal(self):
        text = "We leverage a robust platform that will align with your goals."
        self.assertTrue(has(lint.run(text, "sales"), "ERROR", "tier b"))
        self.assertTrue(has(lint.run(text, "marketing"), "ERROR", "tier b"))
        self.assertTrue(has(lint.run(text, "professional"), "WARN", "tier b"))
        self.assertFalse(any("tier b" in f[1].lower() for f in lint.run(text, "personal")))

    def test_tier_c_warns_only_when_two_or_more(self):
        one = "Let me delve into this."
        two = "Let me delve into this rich tapestry."
        self.assertFalse(has(lint.run(one, "professional"), "WARN", "tier c"))
        self.assertTrue(has(lint.run(two, "professional"), "WARN", "tier c"))
        self.assertFalse(has(lint.run(two, "personal"), "WARN", "tier c"))

    def test_unconfirmed_claude_words_warn_outside_personal(self):
        text = "This is genuinely the load-bearing part."
        self.assertTrue(has(lint.run(text, "professional"), "WARN", "claude"))
        self.assertFalse(has(lint.run(text, "personal"), "WARN", "claude"))

    def test_hedge_stack_warns(self):
        text = "This could perhaps be somewhat of a concern."
        self.assertTrue(has(lint.run(text, "professional"), "WARN", "hedge"))
        self.assertFalse(has(lint.run("This could be a concern.", "professional"), "WARN", "hedge"))
        self.assertFalse(has(lint.run(text, "personal"), "WARN", "hedge"))


class Exclamation(unittest.TestCase):
    def test_sales_error_professional_warn_over_three_personal_silent(self):
        text = "Thanks! Great to meet you! See you Tuesday!"
        four = text + " Can't wait!"
        self.assertTrue(has(lint.run(text, "sales"), "ERROR", "exclamation"))
        self.assertFalse(has(lint.run(text, "professional"), "WARN", "exclamation"))
        self.assertTrue(has(lint.run(four, "professional"), "WARN", "exclamation"))
        self.assertTrue(has(lint.run(text, "marketing"), "WARN", "exclamation"))
        self.assertFalse(any("exclamation" in f[1].lower() for f in lint.run(four, "personal")))


class Negation(unittest.TestCase):
    def test_contrastive_binary(self):
        text = "This isn't just a tooling problem, it's a culture problem."
        self.assertTrue(has(lint.run(text, "professional"), "ERROR", "not x"))
        self.assertTrue(has(lint.run(text, "personal"), "WARN", "not x"))

    def test_negation_fragment(self):
        text = "We looked at it. Not a bug. A design choice."
        self.assertTrue(has(lint.run(text, "professional"), "ERROR", "fragment"))
        self.assertTrue(has(lint.run(text, "personal"), "WARN", "fragment"))


class Closers(unittest.TestCase):
    def test_closing_summary_in_last_paragraph(self):
        text = "First point here.\n\nSecond point here.\n\nIn summary, both points matter."
        self.assertTrue(has(lint.run(text, "professional"), "WARN", "summary"))

    def test_summary_phrase_not_in_last_paragraph_is_fine(self):
        text = "In summary is a phrase I dislike.\n\nHere is the actual point."
        self.assertFalse(has(lint.run(text, "professional"), "WARN", "summary"))


class Artifacts(unittest.TestCase):
    def test_chatbot_artifacts_warn(self):
        for phrase in ("Great question.", "You're absolutely right.", "I hope this helps.", "Here is an overview."):
            self.assertTrue(has(lint.run(phrase, "professional"), "WARN", "chatbot"), phrase)

    def test_model_debris_is_error(self):
        for tag in ("contentReference", "oaicite", "[cite:", "grok_card", "【"):
            self.assertTrue(has(lint.run(f"Text {tag} text", "personal"), "ERROR", "debris"), tag)


class Formatting(unittest.TestCase):
    def test_bold_lead_in_bullets(self):
        text = "- **Speed:** pages load faster.\n- **Cost:** it is cheaper."
        self.assertTrue(has(lint.run(text, "professional"), "WARN", "bold"))

    def test_title_case_heading(self):
        self.assertTrue(has(lint.run("## Strategic Negotiations And Global Partnerships", "professional"), "WARN", "title case"))
        self.assertFalse(has(lint.run("## Strategic negotiations and global partnerships", "professional"), "WARN", "title case"))

    def test_low_burstiness(self):
        text = " ".join(["This sentence has exactly seven words in it."] * 6)
        self.assertTrue(has(lint.run(text, "professional"), "WARN", "burst"))

    def test_uniform_paragraphs(self):
        para = "One two three four five six seven eight nine ten."
        text = "\n\n".join([para] * 4)
        self.assertTrue(has(lint.run(text, "professional"), "WARN", "uniform"))

    def test_spam_words_sales_only(self):
        text = "This is free and we guarantee it."
        self.assertTrue(has(lint.run(text, "sales"), "WARN", "spam"))
        self.assertFalse(has(lint.run(text, "professional"), "WARN", "spam"))


class Skipping(unittest.TestCase):
    def test_lint_off_region_and_inline_ignore(self):
        text = "Plain.\n<!-- lint:off -->\nWe leverage — things.\n<!-- lint:on -->\nStill plain.\nGreat question. <!-- lint:ignore -->\n"
        f = lint.run(text, "sales")
        self.assertFalse(has(f, "ERROR", "em dash"))
        self.assertFalse(has(f, "ERROR", "tier b"))
        self.assertFalse(has(f, "WARN", "chatbot"))

    def test_frontmatter_and_code_blocks_skipped(self):
        text = "---\nname: x\ndescription: we leverage — things\n---\n\n```\nleverage — code\n```\n\nPlain text."
        f = lint.run(text, "sales")
        self.assertFalse(has(f, "ERROR", "em dash"))
        self.assertFalse(has(f, "ERROR", "tier b"))


if __name__ == "__main__":
    unittest.main()
