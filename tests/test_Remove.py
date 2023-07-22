import unittest
import src.Remove as Remove
import src.Hand as Hand
import src.Block as Block

class TestRemove(unittest.TestCase):
    def test_getRemovedBlockPatterns_1(self):
        hand = Hand.Hand([0, 3, 0, 2, 4, 1, 1, 1, 1])
        block = Block.Block([3, 1])
        removedHands = Remove.getRemovedBlockPatterns(hand, block)

        self.assertEqual(len(removedHands), 1)
        self.assertEqual(removedHands[0].hand, [0, 3, 0, 2, 1, 0, 1, 1, 1])

    def test_getRemovedBlockPatterns_2(self):
        hand = Hand.Hand([0, 3, 0, 2, 4, 1, 1, 1, 1])
        block = Block.Block([2])
        removedHands = Remove.getRemovedBlockPatterns(hand, block)

        self.assertEqual(len(removedHands), 3)
        self.assertEqual(removedHands[0].hand, [0, 1, 0, 2, 4, 1, 1, 1, 1])
        self.assertEqual(removedHands[1].hand, [0, 3, 0, 0, 4, 1, 1, 1, 1])
        self.assertEqual(removedHands[2].hand, [0, 3, 0, 2, 2, 1, 1, 1, 1])

    def test_getRemovedMultiBlockPatterns(self):
        hand = Hand.Hand([0, 3, 0, 2, 4, 1, 1, 1, 1])
        block = Block.Block([2])
        block2 = Block.Block([3])
        removedHands = Remove.getRemovedMultiBlockPatterns(hand, [block, block2])

        self.assertEqual(len(removedHands), 5)
        self.assertEqual(removedHands[0].hand, [0, 1, 0, 2, 4, 1, 1, 1, 1])
        self.assertEqual(removedHands[1].hand, [0, 3, 0, 0, 4, 1, 1, 1, 1])
        self.assertEqual(removedHands[2].hand, [0, 3, 0, 2, 2, 1, 1, 1, 1])
        self.assertEqual(removedHands[3].hand, [0, 0, 0, 2, 4, 1, 1, 1, 1])
        self.assertEqual(removedHands[4].hand, [0, 3, 0, 2, 1, 1, 1, 1, 1])

    def test_getRemovedAtamaPatterns(self):
        hand = Hand.Hand([0, 3, 0, 2, 4, 1, 1, 1, 1])
        removedHands = Remove.getRemovedAtamaPatterns(hand)

        self.assertEqual(len(removedHands), 3)
        self.assertEqual(removedHands[0].hand, [0, 1, 0, 2, 4, 1, 1, 1, 1])
        self.assertEqual(removedHands[1].hand, [0, 3, 0, 0, 4, 1, 1, 1, 1])
        self.assertEqual(removedHands[2].hand, [0, 3, 0, 2, 2, 1, 1, 1, 1])

    def test_getRemovedKotsuPatterns(self):
        hand = Hand.Hand([0, 3, 0, 2, 4, 1, 1, 1, 1])
        removedHands = Remove.getRemovedKotsuPatterns(hand)

        self.assertEqual(len(removedHands), 2)
        self.assertEqual(removedHands[0].hand, [0, 0, 0, 2, 4, 1, 1, 1, 1])
        self.assertEqual(removedHands[1].hand, [0, 3, 0, 2, 1, 1, 1, 1, 1])

    def test_getRemovedShuntsuPatterns(self):
        hand = Hand.Hand([0, 3, 0, 2, 4, 1, 1, 1, 1])
        removedHands = Remove.getRemovedShuntsuPatterns(hand)

        self.assertEqual(len(removedHands), 4)
        self.assertEqual(removedHands[0].hand, [0, 3, 0, 1, 3, 0, 1, 1, 1])
        self.assertEqual(removedHands[1].hand, [0, 3, 0, 2, 3, 0, 0, 1, 1])
        self.assertEqual(removedHands[2].hand, [0, 3, 0, 2, 4, 0, 0, 0, 1])
        self.assertEqual(removedHands[3].hand, [0, 3, 0, 2, 4, 1, 0, 0, 0])

    def test_getRemovedAtamaConnectedShuntsuPatterns(self):
        hand = Hand.Hand([0, 3, 1, 2, 4, 1, 1, 1, 1])
        removedHands = Remove.getRemovedAtamaConnectedShuntsuPatterns(hand)

        self.assertEqual(len(removedHands), 3)
        self.assertEqual(removedHands[0].hand, [0, 0, 0, 1, 4, 1, 1, 1, 1])
        self.assertEqual(removedHands[1].hand, [0, 3, 1, 2, 1, 0, 0, 1, 1])
        self.assertEqual(removedHands[2].hand, [0, 3, 0, 1, 1, 1, 1, 1, 1])

    def test_getRemovedMentsuPatterns(self):
        hand = Hand.Hand([0, 3, 0, 2, 4, 1, 1, 1, 1])
        removedHands = Remove.getRemovedMentsuPatterns(hand)

        self.assertEqual(len(removedHands), 6)
        self.assertEqual(removedHands[0].hand, [0, 0, 0, 2, 4, 1, 1, 1, 1])
        self.assertEqual(removedHands[1].hand, [0, 3, 0, 2, 1, 1, 1, 1, 1])
        self.assertEqual(removedHands[2].hand, [0, 3, 0, 1, 3, 0, 1, 1, 1])
        self.assertEqual(removedHands[3].hand, [0, 3, 0, 2, 3, 0, 0, 1, 1])
        self.assertEqual(removedHands[4].hand, [0, 3, 0, 2, 4, 0, 0, 0, 1])
        self.assertEqual(removedHands[5].hand, [0, 3, 0, 2, 4, 1, 0, 0, 0])

    def test_getRemovedSendableFormPatterns(self):
        hand = Hand.Hand([0, 3, 1, 2, 4, 1, 1, 1, 1])
        removedHands = Remove.getRemovedSendableFormPatterns(hand)

        self.assertEqual(len(removedHands), 6)
        self.assertEqual(removedHands[0].hand, [0, 1, 1, 2, 4, 1, 1, 1, 1])
        self.assertEqual(removedHands[1].hand, [0, 3, 1, 0, 4, 1, 1, 1, 1])
        self.assertEqual(removedHands[2].hand, [0, 3, 1, 2, 2, 1, 1, 1, 1])
        self.assertEqual(removedHands[3].hand, [0, 0, 0, 1, 4, 1, 1, 1, 1])
        self.assertEqual(removedHands[4].hand, [0, 3, 1, 2, 1, 0, 0, 1, 1])
        self.assertEqual(removedHands[5].hand, [0, 3, 0, 1, 1, 1, 1, 1, 1])

