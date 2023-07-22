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

        object.__setattr__(self, "block", block)

