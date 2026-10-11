import unittest

from contamcheck.detector import build_index, score_item

CORPUS = ["The quick brown fox jumps over the lazy dog near the river bank"]


class ScoreItemTests(unittest.TestCase):
    def setUp(self):
        self.index = build_index(CORPUS, n=4)

    def test_verbatim_copy_is_contaminated(self):
        f = score_item("a", "the quick brown fox jumps over the lazy dog", self.index, n=4)
        self.assertEqual(f.overlap, 1.0)
        self.assertTrue(f.contaminated)

    def test_punctuation_and_case_do_not_hide_a_copy(self):
        f = score_item("a", "THE QUICK, brown fox -- jumps over", self.index, n=4)
        self.assertTrue(f.contaminated)

    def test_unrelated_text_is_clean(self):
        f = score_item("a", "what is the capital of france and its population", self.index, n=4)
        self.assertEqual(f.shared, 0)
        self.assertFalse(f.contaminated)

    def test_partial_overlap_respects_threshold(self):
        text = "the quick brown fox then something else entirely happened"
        loose = score_item("a", text, self.index, n=4, threshold=0.1)
        strict = score_item("a", text, self.index, n=4, threshold=0.9)
        self.assertTrue(loose.contaminated)
        self.assertFalse(strict.contaminated)

    def test_short_item_scores_zero(self):
        f = score_item("a", "too short", self.index, n=4)
        self.assertEqual((f.total, f.overlap, f.contaminated), (0, 0.0, False))


if __name__ == "__main__":
    unittest.main()
