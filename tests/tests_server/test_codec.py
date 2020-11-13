from sys import path
from os import remove
import unittest

path.append("../..")

from codec import *


class TestCodec(unittest.TestCase):

    def setUp(self):
        generate_key()

    def tearDown(self):
        remove('../key')

    def test_codec(self):
        encrypted_hash = codec("123", 1)
        decrypted_hash = codec(encrypted_hash, 0)
        self.assertTrue(check_password("123".encode(), decrypted_hash))


if __name__ == '__main__':
    unittest.main()
