from unittest import TestCase
from csci_utils.hash_str.hash_str import (
    hash_str,
    get_csci_salt,
    get_csci_pepper,
    get_user_id,
)
import base64


class HashTests(TestCase):
    def test_basic(self):
        self.assertEqual(hash_str("world!", salt="hello, ").hex()[:6], "68e656")

    def test_salt_type(self):
        assert isinstance(get_csci_salt(), bytes)

    def test_pepper_type(self):
        assert isinstance(get_csci_pepper(), bytes)

    def test_salt_nonblank(self):
        self.assertNotEqual(get_csci_salt(), bytes.fromhex(""))

    def test_pepper_nonblank(self):
        self.assertNotEqual(get_csci_pepper(), base64.b64decode(""))

    def test_user_id(self):
        self.assertEqual(get_user_id("gorlins"), "70ded892")
