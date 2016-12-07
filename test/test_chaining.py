import unittest
import kliko.chaining


class TestChaining(unittest.TestCase):
    def test_hash(self):

        x1 = {'a': 'b', 'b': 'a'}
        x2 = {'b': 'a', 'a': 'b'}
        xhash = '38dd8d5719784dcd2a7ac82f418b93fc4af827032313dea5e5d0cab742a958fb'

        self.assertEqual(kliko.chaining.dict2sha256(x1), xhash)
        self.assertEqual(kliko.chaining.dict2sha256(x2), xhash)
