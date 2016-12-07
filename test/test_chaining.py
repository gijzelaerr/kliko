import unittest
import kliko.chaining


class TestChaining(unittest.TestCase):
    def test_hash(self):

        x1 = {'a': 'b', 'b': 'a'}
        x2 = {'b': 'a', 'a': 'b'}

        self.assertEqual(kliko.chaining._dict2sha256(x1), kliko.chaining._dict2sha256(x2))

