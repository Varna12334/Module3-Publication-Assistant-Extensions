import unittest
from src.utils.helpers import clean_manuscript_text, chunk_text

class TestModule3Utilities(unittest.TestCase):

    def test_clean_manuscript_text(self):
        sample_input = "  This is an   academic   paper draft\nwith messy line breaks.   "
        expected_output = "This is an academic paper draft with messy line breaks."
        self.assertEqual(clean_manuscript_text(sample_input), expected_output)

    def test_chunk_text(self):
        sample_input = "word " * 1500
        chunks = chunk_text(sample_input, chunk_size=500)
        # Should cleanly divide 1500 words into roughly 3 distinct blocks
        self.assertTrue(len(chunks) >= 3)

if __name__ == '__main__':
    unittest.TestCase()
