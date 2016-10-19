# -*- coding: utf-8 -*-
from .crypto import Crypto, Space
from itertools import count, product
from typing import Iterable


def egcd(a: int, b: int) -> int:
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modinv(a: int, m: int) -> int:
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


class Affine(Crypto):
    def __init__(self, space: Space):
        self.space = space

    def gen_kd(self):
        m = self.space.len()

        for a in range(0, m):
            g, x, y = egcd(a, m)
            if g != 1:
                continue
            a1 = x % m
            for b in range(0, m):
                yield (a1, b)

    def crypt(self, text: str, ke: (int, int)) -> str:
        a, b = ke

        result = ''

        for idx in range(0, len(text)):
            c = text[idx]
            i = self.space.ord(c)

            if i is None:
                result += c
            else:
                i2 = a*i+b
                result += self.space.chr(i2)

        return result

    def decrypt(self, text: str, kd: (int, int)) -> str:
        a, b = kd
        a1 = modinv(a, self.space.len())

        result = ''

        for idx in range(0, len(text)):
            c = text[idx]
            i = self.space.ord(c)

            if i is None:
                result += c
            else:
                i2 = a1 * (i - b)
                result += self.space.chr(i2)

        return result
