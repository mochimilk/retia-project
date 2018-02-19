import unittest
from stream_test import is_babu

class TestBabuDetection(unittest.TestCase):

    def test_mama_t(self):
        self.assertTrue(is_babu("ママーッ！"))

    def test_mama_f(self):
        self.assertFalse(is_babu("ママー|"))

if __name__ == '__main__':
    unittest.main()
