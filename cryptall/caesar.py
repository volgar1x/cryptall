# coding=utf-8

from .crypto import Crypto, Space

class Caesar(Crypto):
    def __init__(self, space: Space):
        self.space = space

    def crypt(self, text, ke):
        res = ''

        for i in range(0, len(text)):
            c = self.space.ord(text[i])
            if c is None:
                res += text[i]
            else:
                res += self.space.chr(c + ke)

        return res

    def decrypt(self, text, kd):
        return self.crypt(text, kd)

    def gen_kd(self):
        return range(1, self.space.len())
