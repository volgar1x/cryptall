# -*- coding: utf-8 -*-

from typing import Iterable
from itertools import count, product
from time import sleep
from .crypto import Crypto, Space


class Vigenere(Crypto):
    def __init__(self, space: Space):
        self.space = space

    def gen_kd(self) -> Iterable[str]:
        for n in count(1):
            for k in product(self.space.range(), repeat=n):
                k = ''.join(k)
                # print(k)
                # sleep(0.01)
                yield k

    def crypt(self, text: str, ke: str) -> str:
        res = ''

        for idx in range(0, len(text)):
            mi = self.space.ord(text[idx])
            ki = self.space.ord(ke[idx % len(ke)])

            if mi is None:
                res += text[idx]
            else:
                res += self.space.chr(mi + ki)

        return res

    def decrypt(self, text: str, kd: str) -> str:
        res = ''

        for idx in range(0, len(text)):
            mi = self.space.ord(text[idx])
            ki = self.space.ord(kd[idx % len(kd)])

            if mi is None:
                res += text[idx]
            else:
                res += self.space.chr(mi - ki)

        return res
