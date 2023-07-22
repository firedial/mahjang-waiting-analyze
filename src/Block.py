from dataclasses import dataclass
from typing import ClassVar

@dataclass(frozen=True)
class Block:

    block: list[int]
    MAX_TILE_COUNT: ClassVar[int] = 4
    MAX_BLOCK_LENGTH: ClassVar[int] = 9

    def __init__(self, block: list[int]):
        if len(block) > self.MAX_BLOCK_LENGTH or len(block) < 1:
            raise ValueError("Wrong block length.")

        for tile in block:
            if tile > self.MAX_TILE_COUNT or tile < 0:
                raise ValueError("Wrong tile count.")

        # 両端が0でないことをみる
        if block[0] == 0 or block[-1] == 0:
            raise ValueError("Edge is zero.")

        object.__setattr__(self, "block", block)

