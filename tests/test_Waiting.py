import unittest
from src.Waiting import Waiting

class TestSuit(unittest.TestCase):
    def test_init(self):
        # 長さ8の手牌
        with self.assertRaises(ValueError):
            Waiting((1, 1, 1, 1, 1, 1, 1, 1), False)

        # 長さ10の手牌
        with self.assertRaises(ValueError):
            Waiting((1, 1, 1, 1, 1, 1, 1, 1, 1, 1), False)

        # マイナスが入っている手牌
        with self.assertRaises(ValueError):
            Waiting((1, 1, 1, 1, 1, 1, 1, 1, -1), False)

        # 4を超えているものが入っている手牌
        with self.assertRaises(ValueError):
            Waiting((1, 1, 1, 1, 1, 1, 1, 1, 5), False)

        # 正常系
        waiting = Waiting((1, 2, 3, 4, 0, 0, 2, 1, 1), False)
        self.assertEqual(waiting.waitingCount, (1, 2, 3, 4, 0, 0, 2, 1, 1))

    def test_isTempai(self):
        waiting = Waiting((1, 2, 3, 4, 0, 0, 2, 1, 1), False)
        self.assertTrue(waiting.isTempai())

        waiting = Waiting((0, 0, 0, 0, 0, 0, 0, 0, 0), True)
        self.assertTrue(waiting.isTempai())

        waiting = Waiting((0, 1, 0, 0, 0, 0, 0, 0, 0), True)
        self.assertTrue(waiting.isTempai())

        waiting = Waiting((0, 0, 0, 0, 0, 0, 0, 0, 0), False)
        self.assertFalse(waiting.isTempai())

    def test_getWaitingTileCount(self):
        waiting = Waiting((1, 2, 3, 4, 0, 0, 2, 1, 1), False)
        self.assertEqual(waiting.getWaitingTileCount(), 7)

        waiting = Waiting((0, 0, 0, 0, 0, 0, 0, 0, 0), True)
        self.assertEqual(waiting.getWaitingTileCount(), 0)

        waiting = Waiting((0, 1, 0, 0, 0, 0, 0, 0, 0), True)
        self.assertEqual(waiting.getWaitingTileCount(), 1)

        waiting = Waiting((0, 0, 0, 0, 0, 0, 0, 0, 0), False)
        self.assertEqual(waiting.getWaitingTileCount(), 0)
