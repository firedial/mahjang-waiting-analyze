import unittest
from src.util.Suit import Suit

class TestSuit(unittest.TestCase):
    def test_init(self):
        # 長さ8の手牌
        with self.assertRaises(ValueError):
            Suit((1, 1, 1, 1, 1, 1, 1, 1))

        # 長さ10の手牌
        with self.assertRaises(ValueError):
            Suit((1, 1, 1, 1, 1, 1, 1, 1, 1, 1))

        # マイナスが入っている手牌
        with self.assertRaises(ValueError):
            Suit((1, 1, 1, 1, 1, 1, 1, 1, -1))

        # 4を超えているものが入っている手牌
        with self.assertRaises(ValueError):
            Suit((1, 1, 1, 1, 1, 1, 1, 1, 5))

        # 正常系
        suit = Suit((1, 2, 3, 4, 0, 0, 2, 1, 1))
        self.assertEqual(suit.suit, (1, 2, 3, 4, 0, 0, 2, 1, 1))

    def test_length(self):
        suit = Suit((1, 2, 3, 4, 0, 0, 2, 1, 1))
        self.assertEqual(suit.length(), 9)

    def test_sum(self):
        suit = Suit((1, 2, 3, 4, 0, 0, 2, 1, 1))
        self.assertEqual(suit.sum(), 14)

        suit = Suit((1, 0, 3, 0, 0, 0, 2, 1, 1))
        self.assertEqual(suit.sum(), 8)

    def test_isTempai(self):
        suit = Suit((2, 2, 2, 2, 0, 0, 1, 1, 1))
        self.assertTrue(suit.isTempai())

        suit = Suit((4, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertFalse(suit.isTempai())

    def test_isTempaiWithoutTileCount(self):
        suit = Suit((2, 2, 2, 2, 0, 0, 1, 1, 1))
        self.assertTrue(suit.isTempaiWithoutTileCount())

        suit = Suit((4, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertTrue(suit.isTempaiWithoutTileCount())

    def test_isSendable(self):
        suit = Suit((0, 0, 2, 2, 0, 0, 1, 1, 1))
        self.assertFalse(suit.isSendable())

        suit = Suit((0, 0, 2, 0, 0, 0, 0, 0, 0))
        self.assertTrue(suit.isSendable())

        suit = Suit((0, 0, 3, 1, 1, 0, 0, 0, 0))
        self.assertTrue(suit.isSendable())

        suit = Suit((0, 0, 3, 3, 2, 0, 0, 0, 0))
        self.assertTrue(suit.isSendable())

        suit = Suit((0, 3, 1, 1, 1, 1, 1, 0, 0))
        self.assertTrue(suit.isSendable())

        suit = Suit((0, 2, 2, 2, 2, 0, 0, 0, 0))
        self.assertTrue(suit.isSendable())

        suit = Suit((0, 1, 1, 4, 1, 1, 0, 0, 0))
        self.assertTrue(suit.isSendable())

        suit = Suit((0, 3, 3, 3, 1, 1, 0, 0, 0))
        self.assertTrue(suit.isSendable())

        suit = Suit((0, 2, 3, 3, 1, 1, 1, 0, 0))
        self.assertTrue(suit.isSendable())

        suit = Suit((0, 2, 2, 2, 3, 1, 1, 0, 0))
        self.assertTrue(suit.isSendable())

    def test_isRangeFull(self):
        suit = Suit((0, 2, 2, 2, 3, 1, 1, 0, 0))
        self.assertFalse(suit.isRangeFull())

        suit = Suit((1, 2, 2, 2, 3, 1, 1, 2, 0))
        self.assertFalse(suit.isRangeFull())

        suit = Suit((1, 2, 2, 2, 3, 1, 1, 2, 2))
        self.assertTrue(suit.isRangeFull())

    def test_hasOneRoomRange(self):
        suit = Suit((0, 2, 2, 2, 3, 1, 1, 0, 0))
        self.assertFalse(suit.hasOneRoomRange())

        suit = Suit((1, 2, 2, 2, 3, 1, 1, 2, 0))
        self.assertTrue(suit.hasOneRoomRange())

        suit = Suit((1, 2, 2, 2, 3, 1, 1, 2, 2))
        self.assertFalse(suit.hasOneRoomRange())

    def test_getLeftAttachSuit(self):
        suit = Suit((0, 0, 2, 2, 3, 0, 0, 1, 0))
        self.assertEqual(suit.getLeftAttachSuit(), Suit((2, 2, 3, 0, 0, 1, 0, 0, 0)))

        suit = Suit((0, 2, 2, 2, 3, 0, 0, 0, 0))
        self.assertEqual(suit.getLeftAttachSuit(), Suit((2, 2, 2, 3, 0, 0, 0, 0, 0)))

    def test_getRightAttachSuit(self):
        suit = Suit((0, 0, 2, 2, 3, 0, 0, 1, 0))
        self.assertEqual(suit.getRightAttachSuit(), Suit((0, 0, 0, 2, 2, 3, 0, 0, 1)))

        suit = Suit((0, 2, 2, 2, 3, 0, 0, 0, 0))
        self.assertEqual(suit.getRightAttachSuit(), Suit((0, 0, 0, 0, 0, 2, 2, 2, 3)))

    def test_getSuitNumber(self):
        suit = Suit((0, 0, 2, 0, 0, 0, 0, 0, 0))
        self.assertEqual(suit.getSuitNumber(), 78200000000)

        suit = Suit((0, 2, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(suit.getSuitNumber(), 78200000000)

        suit = Suit((0, 2, 2, 2, 2, 0, 0, 0, 0))
        self.assertEqual(suit.getSuitNumber(), 34222200000)

    def test_isFirstTIleZero(self):
        suit = Suit((1, 2, 3, 4, 0, 0, 2, 0, 0))
        self.assertFalse(suit.isFirstTIleZero())

        suit = Suit((0, 2, 3, 4, 0, 0, 2, 0, 0))
        self.assertTrue(suit.isFirstTIleZero())

    def test_isBasicForm(self):
        suit = Suit((0, 2, 3, 4, 0, 0, 2, 3, 0))
        self.assertFalse(suit.isBasicForm())

        suit = Suit((0, 4, 3, 4, 0, 0, 2, 3, 0))
        self.assertTrue(suit.isBasicForm())

        suit = Suit((0, 0, 4, 3, 4, 0, 0, 2, 3))
        self.assertFalse(suit.isBasicForm())

        suit = Suit((0, 4, 4, 3, 4, 0, 0, 2, 3))
        self.assertTrue(suit.isBasicForm())

        suit = Suit((4, 4, 3, 4, 0, 0, 2, 3, 0))
        self.assertFalse(suit.isBasicForm())

        suit = Suit((4, 4, 3, 4, 0, 0, 2, 3, 1))
        self.assertTrue(suit.isBasicForm())

        suit = Suit((1, 2, 3, 4, 0, 0, 2, 3, 1))
        self.assertFalse(suit.isBasicForm())

    def test_waitingStructure(self):
        # ノーテン形
        suit = Suit((0, 1, 0, 2, 0, 1, 0, 0, 0))
        self.assertEqual(suit.waitingStructure.getWaitingStructureString(), '⠂⠂⠂⠂⠂⠂⠂⠂⠂')

        # 単騎待ち
        suit = Suit((0, 1, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(suit.waitingStructure.getWaitingStructureString(), '⠂⠒⠂⠂⠂⠂⠂⠂⠂')

        # カンチャン待ち
        suit = Suit((0, 1, 0, 1, 0, 0, 0, 0, 0))
        self.assertEqual(suit.waitingStructure.getWaitingStructureString(), '⠂⠂⠢⠂⠂⠂⠂⠂⠂')

        # シャンポン待ち
        suit = Suit((0, 2, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(suit.waitingStructure.getWaitingStructureString(), '⠂⣂⠂⠂⠂⠂⠂⠂⠂')

        # 両面待ち
        suit = Suit((0, 1, 1, 0, 0, 0, 0, 0, 0))
        self.assertEqual(suit.waitingStructure.getWaitingStructureString(), '⠊⠂⠂⠃⠂⠂⠂⠂⠂')

        # 単騎待ち + カンチャン待ち
        suit = Suit((0, 1, 2, 1, 0, 0, 0, 0, 0))
        self.assertEqual(suit.waitingStructure.getWaitingStructureString(), '⠂⠂⠲⠂⠂⠂⠂⠂⠂')

        # 雀頭接続順子
        suit = Suit((0, 3, 1, 1, 0, 0, 0, 0, 0))
        self.assertEqual(suit.waitingStructure.getWaitingStructureString(), '⠂⣊⠂⠂⠃⠂⠂⠂⠂')

        # 九蓮宝燈
        suit = Suit((3, 1, 1, 1, 1, 1, 1, 1, 3))
        self.assertEqual(suit.waitingStructure.getWaitingStructureString(), '⣊⠒⠋⠋⠒⠋⠋⠒⣃')

        # 七連宝燈
        suit = Suit((0, 1, 1, 4, 1, 4, 1, 1, 0))
        self.assertEqual(suit.waitingStructure.getWaitingStructureString(), '⠊⠒⠪⣋⠒⣋⠣⠒⠃')

        # 七連宝燈
        suit = Suit((0, 1, 4, 1, 1, 1, 4, 1, 0))
        self.assertEqual(suit.waitingStructure.getWaitingStructureString(), '⠊⠒⠂⠣⠒⠪⠂⠒⠃')

        # 八連宝燈
        suit = Suit((1, 1, 4, 1, 1, 1, 1, 3, 0))
        self.assertEqual(suit.waitingStructure.getWaitingStructureString(), '⠒⠪⣋⠒⠋⠋⠒⣃⠃')

        # 八連宝燈
        suit = Suit((0, 1, 4, 2, 1, 1, 1, 3, 0))
        self.assertEqual(suit.waitingStructure.getWaitingStructureString(), '⠊⠊⣪⠓⠋⠋⠒⣃⠃')

        # 八連宝燈
        suit = Suit((0, 1, 1, 4, 1, 1, 1, 1, 3))
        self.assertEqual(suit.waitingStructure.getWaitingStructureString(), '⠊⠒⠪⣋⠒⠋⠋⠒⣃')
