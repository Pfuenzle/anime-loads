import unittest
from jdhelper import *

class TestJDHelper(unittest.TestCase):
    def test_decode_cnl(self):
        result = decode_cnl("", "")
        self.assertEqual(result, "asdf", "Failed to decode CNL")