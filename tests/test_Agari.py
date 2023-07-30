import unittest
import src.Agari as Agari
from src.Suit import Suit

class TestAgari(unittest.TestCase):
    def test_isAgari(self):
        suit = Suit((0, 3, 0, 0, 2, 0, 1, 1, 1))
        self.assertTrue(Agari.isAgari(suit))

        suit = Suit((3, 1, 1, 1, 2, 1, 1, 1, 3))
        self.assertTrue(Agari.isAgari(suit))

        suit = Suit((2, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertTrue(Agari.isAgari(suit))

        suit = Suit((2, 0, 3, 3, 0, 3, 3, 0, 0))
        self.assertTrue(Agari.isAgari(suit))
