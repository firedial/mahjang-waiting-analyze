from dataclasses import dataclass
from typing import ClassVar, Self
import src.util.WaitingType as WaitingType

@dataclass(frozen=True)
class WaitingStructure:

    waitingStructures: tuple[WaitingType, ...]

    HAND_LENGTH: ClassVar[int] = 9

    def __init__(self, waitingStructures: tuple[WaitingType, ...]):
        if len(waitingStructures) != self.HAND_LENGTH:
            raise ValueError("Wrong waitings length.")

        object.__setattr__(self, "waitingStructures", waitingStructures)

    def addAtama(self, index: int) -> Self:
        addedShampon = self.waitingStructures[index].addShampon()
        return WaitingStructure(self.waitingStructures[:index] + (addedShampon, ) + self.waitingStructures[index + 1:])

    def addAtamaConnectedShuntsu(self, index: int, pattern: int) -> Self:
        if pattern == 311:
            addedShamponAndRyanmen = self.waitingStructures[index].addShampon().addRyanmenLeft()
            addedRyanmen = self.waitingStructures[index + 2].addRyanmenRight()
            return WaitingStructure(self.waitingStructures[:index] + (addedShamponAndRyanmen, self.waitingStructures[index + 1], addedRyanmen) + self.waitingStructures[index + 3:])
        elif pattern == 113:
            addedShamponAndRyanmen = self.waitingStructures[index].addShampon().addRyanmenRight()
            addedRyanmen = self.waitingStructures[index - 2].addRyanmenLeft()
            return WaitingStructure(self.waitingStructures[:index - 2] + (addedRyanmen, self.waitingStructures[index - 1], addedShamponAndRyanmen) + self.waitingStructures[index + 1:])

        raise ValueError("Unexpected pattern.")

    def __eq__(self, other) -> bool:
        for x, y in zip(self.waitingStructures, other.waitingStructures):
            if x != y:
                return False
        else:
            return True

    def __ne__(self, other) -> bool:
        return not (self == other)
