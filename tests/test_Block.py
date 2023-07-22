import unittest
import src.Block as Block

class TestBlock(unittest.TestCase):
    def test_init(self):
        # 長さが0であるブロック
        with self.assertRaises(ValueError):
            Block.Block([])

        # 長さ10のブロック
        with self.assertRaises(ValueError):
            Block.Block([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

        # マイナスが入っているブロック
        with self.assertRaises(ValueError):
            Block.Block([1, 1, 1, 1, 1, 1, 1, 1, -1])

        # 4を超えているものが入っているブロック
        with self.assertRaises(ValueError):
            Block.Block([1, 1, 1, 1, 1, 1, 1, 1, 5])

        # 正常系
        block = Block.Block([1, 2, 3])
        self.assertEqual(block.block, [1, 2, 3])
