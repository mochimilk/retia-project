import unittest
from stream_test import is_babu
from stream_test import is_kiite

class TestBabuDetection(unittest.TestCase):

    def test_mama_t(self):
        self.assertTrue(is_babu("ママーッ！"))

    def test_mama_f(self):
        self.assertFalse(is_babu("ママー|"))

class TestElderSisterDetection(unittest.TestCase):

    def test_sister_t(self):
        self.assertTrue(is_kiite("おねえちゃん"))

if __name__ == '__main__':
    unittest.main()
