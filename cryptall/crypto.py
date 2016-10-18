# -*- coding: utf-8 -*-

from typing import Iterable, TypeVar, Optional
import re


class Space(object):
    def ord(self, c):
        raise Exception('')

    def chr(self, i):
        raise Exception('')

    def len(self):
        raise Exception('')

    def split_words(self, text: str) -> [str]:
        res = []
        buf = ''

        for idx in range(0, len(text)):
            if self.ord(text[idx]) is None:
                if buf:
                    res.append(buf)
                    buf = ''
            else:
                buf += text[idx]

        if buf:
            res.append(buf)

        return res

    def range(self) -> Iterable[str]:
        for idx in range(0, self.len()):
            yield self.chr(idx)


class StrSpace(Space):
    def __init__(self, alphabet):
        self.alphabet = alphabet

    def len(self):
        return len(self.alphabet)

    def ord(self, c):
        if c not in self.alphabet:
            return None
        return self.alphabet.index(c)

    def chr(self, i):
        return self.alphabet[i % len(self.alphabet)]

    def range(self) -> Iterable[str]:
        return list(self.alphabet)


class UnicodeSpace(Space):
    def len(self):
        return 0xFF

    def ord(self, c):
        return ord(c)

    def chr(self, i):
        return chr(i)


ALPHABET_SPACE = StrSpace('abcdefghijklmnopqrstuvwxyz')
UNICODE_SPACE = UnicodeSpace()


class BruteforceContext(object):
    def __init__(self):
        self.dictionaries = {}

    def load(self, lang, filename, encoding='utf-8'):
        with open(filename, 'r', encoding=encoding) as f:
            self.dictionaries[lang] = set(map(lambda x: x.strip().lower(), f.readlines()))

    def find_word(self, word: str) -> Optional[str]:
        for k in self.dictionaries.keys():
            if word in self.dictionaries[k]:
                return k
        return None


KE = TypeVar('KE')
KD = TypeVar('KD')


class Crypto(object):
    def crypt(self, text: str, ke: KE) -> str:
        raise Exception('abstract method')

    def decrypt(self, text: str, kd: KD) -> str:
        raise Exception('abstract method')

    def gen_kd(self) -> Iterable[KD]:
        return []

    def bruteforce(self, text: str, ctx: BruteforceContext, min_score=0.8) -> [(str, KD, float)]:
        res = []
        gen = self.gen_kd()
        for kd in gen:
            clear = self.decrypt(text, kd)

            words = self.space.split_words(clear)

            detected_words = []
            for word in words:
                detected_lang = ctx.find_word(word)
                if detected_lang is not None:
                    detected_words.append((word, detected_lang))

            score = sum(float(len(word)) for word, lang in detected_words) / sum(float(len(word)) for word in words)
            if score < min_score:
                continue

            res.append((clear, kd, score))

            if type(gen).__name__ == 'generator':
                break

        return sorted(res, key=lambda x: x[2], reverse=True)
