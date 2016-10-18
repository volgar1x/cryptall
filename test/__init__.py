# coding=utf-8

import unittest

from cryptall.caesar import Caesar
from cryptall.vigenere import Vigenere
from cryptall.crypto import BruteforceContext, StrSpace, ALPHABET_SPACE, UNICODE_SPACE


cryptos = [
    # chiffrement de caesar
    (Caesar(ALPHABET_SPACE), 'first', 'svefg', 13, 13),
    (Caesar(ALPHABET_SPACE), 'hello', 'dahhk', 22, 4),
    (Caesar(StrSpace('abcdefghijklmnopqrstuvwxyzéùç')), 'comment ça va ?', 'htrrjsy ef éf ?', 5, 24),
    (Caesar(ALPHABET_SPACE), 'bonjour le monde', 'pcbxcif zs acbrs', 14, 12),

    # chiffrement de vigenere
    (Vigenere(ALPHABET_SPACE), 'comment ça va ?', 'ezqoprv çc zc ?', 'cle', 'cle'),

    # chiffrement affine
    # …
]


ctx = BruteforceContext()
ctx.load('en', '../en.txt', 'ascii')
ctx.load('fr', '../fr.txt', 'latin1')


class TestCrypto(unittest.TestCase):
    def test_identity(self):
        for crypto, text, crypted, ke, kd in cryptos:
            self.assertEqual(text, crypto.decrypt(crypto.crypt(text, ke), kd))

    def test_crypt(self):
        for crypto, text, crypted, ke, kd in cryptos:
            self.assertEqual(crypted, crypto.crypt(text, ke))

    def test_decrypt(self):
        for crypto, text, crypted, ke, kd in cryptos:
            self.assertEqual(text, crypto.decrypt(crypted, kd))

    def test_bruteforce(self):
        for crypto, text, crypted, ke, kd in cryptos:
            found = crypto.bruteforce(crypted, ctx)

            if not found:
                self.fail('couldnt bruteforce "{0}" for crypto {1}'.format(text, crypto.__class__.__name__))

            for clear, found_kd, proba in found:
                if text == clear:
                    self.assertEqual(kd, found_kd, 'invalid kd for "{0}"'.format(text))
                    self.assertAlmostEqual(1.0, proba, delta=0.01)
                else:
                    print(text, clear, found_kd)
                    self.assertTrue(0.0 <= proba <= 1.0, '0 < {0} < 1'.format(proba))


class TestStrSpace(unittest.TestCase):
    def test_split_words(self):
        self.assertEqual(['hello', 'world'], ALPHABET_SPACE.split_words('hello world'))
        self.assertEqual(['hello', 'world'], ALPHABET_SPACE.split_words('hello, world!'))


if __name__ == '__main__':
    unittest.main()
