# coding=utf-8

import unittest

from cryptall.caesar import Caesar
from cryptall.vigenere import Vigenere
from cryptall.crypto import BruteforceContext, StrSpace, ALPHABET_SPACE, UNICODE_SPACE, list_shift_places


FRENCH_TEXT = (
    'C’est comme ça qu’il se voyait à cette époque. Un peu rebelle envers ce monde. L’informatique l’avait aidé à s’enfermer un peu plus dans cet état. Il était devenu doué d’une logique à toute épreuve et d’une intelligence remarquable, mais surtout, il était devenu insociable. Avec l’âge, le besoin de trouver l’âme sœur avait pris le dessus et il avait été un peu obligé de rencontrer des gens, de parler avec eux. Très difficile au début, il avait réussi à vaincre ces préjugés. Il avait accepté la lenteur d’esprit des autres ainsi que leur manque de logique.'
    'C’est une informaticienne chevronnée de 35 ans. Une surdouée qui s’est découvert une passion pour l’informatique à l’âge de treize ans lorsqu’elle a vu une publicité pour cet ordinateur familial dont on ventait les mérites à l’aide d’une petite marionnette virtuelle. Elle voulait un ami, elle a eu une marionnette virtuelle. Depuis, la marionnette a laissé place à des projets plus sérieux, plus lucratifs surtout. Mais Sophie, c’est comme ça qu’elle nommait sa marionnette, est toujours là, dans un petit coin de son ordinateur et c’est à Sophie qu’elle s’adresse quand le moral est au plus bas. Mais aujourd’hui, c’est Sophie qui s’adresse à Florence.'
    '« Prélude m’avait dit qu’il désirait connaître l’amour. Les ordinateurs n’ont pas de sentiments et l’amour n’est que sentiments. Il y a bien l’amour physique, mais sans les sentiments, cela ressemble davantage à un instinct de reproduction qu’à de l’amour. Un ordinateur n’a pas ce besoin de reproduction. Et pourquoi m’avoir choisi ? »'
    'Florence avait fini de préparer le matériel demandé par Prélude. Elle était fin prête. Elle vérifia le bon fonctionnement de la liaison entre son ordinateur portable et Internet. Prélude était bien là. A peine connecté à Internet que la voix de Prélude se fit entendre.'
    'Le seul moyen de le stopper serait d’arrêter tout les ordinateurs, ce qui aurait les mêmes conséquences que de laisser Prélude lancer les bombes. Depuis longtemps, toutes les installations à risque étaient contrôlées par des ordinateurs. Si l’on stoppait les ordinateurs, les centrales nucléaires s’emballeraient, les silos nucléaires cracheraient leur mort sur toute la planète. Bien entendu, l’économie mondiale dirigée par la bourse, s’effondrerait. David ne savait plus quoi faire et, manifestement, tout les militaires présents dans la salle comptaient sur lui pour résoudre cette crise.'
)


cryptos = [
    # chiffrement de caesar
    (Caesar(ALPHABET_SPACE), 'first', 'svefg', 13, 13),
    (Caesar(ALPHABET_SPACE), 'hello', 'dahhk', 22, 4),
    (Caesar(StrSpace('abcdefghijklmnopqrstuvwxyzéùç')), 'comment ça va ?', 'htrrjsy ef éf ?', 5, 24),
    (Caesar(ALPHABET_SPACE), 'bonjour le monde', 'pcbxcif zs acbrs', 14, 12),
    (Caesar(ALPHABET_SPACE), FRENCH_TEXT, Caesar(ALPHABET_SPACE).crypt(FRENCH_TEXT, 14), 14, 12),

    # chiffrement de vigenere
    (Vigenere(ALPHABET_SPACE), 'comment ça va ?', 'ezqoprv çc zc ?', 'cle', 'cle'),

    # chiffrement affine
    # …
]


ctx = BruteforceContext()
ctx.load('en', '../en.txt', 'ascii')
ctx.load('fr', '../fr.txt', 'latin1')

print('loading en freqs')
ctx.load_freqs('en', ALPHABET_SPACE)
print('loading fr freqs')
ctx.load_freqs('fr', ALPHABET_SPACE)


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

    def test_ctx_freqs_should_equal_1(self):
        for lang in ctx.freqs.keys():
            self.assertAlmostEqual(1.0, sum(freq for c, freq in ctx.freqs[lang]), delta=0.001)

    def test_guess_with_charac_freq(self):
        for crypto, text, crypted, ke, kd in cryptos:
            print(crypto.guess_with_charac_freq(crypted, ctx))

    def test_list_places(self):
        self.assertEqual([1, 2, 3], list_shift_places([1, 2, 3], 0))
        self.assertEqual([3, 1, 2], list_shift_places([1, 2, 3], 1))
        self.assertEqual([2, 3, 1], list_shift_places([1, 2, 3], 2))
        self.assertEqual([1, 2, 3], list_shift_places([1, 2, 3], 3))


class TestStrSpace(unittest.TestCase):
    def test_split_words(self):
        self.assertEqual(['hello', 'world'], ALPHABET_SPACE.split_words('hello world'))
        self.assertEqual(['hello', 'world'], ALPHABET_SPACE.split_words('hello, world!'))


if __name__ == '__main__':
    unittest.main()
