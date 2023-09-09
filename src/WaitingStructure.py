from dataclasses import dataclass
from typing import ClassVar
import src.WaitingType as WaitingType

@dataclass(frozen=True)
class WaitingStructure:

    waitingStructures: tuple[WaitingType, ...]

    HAND_LENGTH: ClassVar[int] = 9

    def __init__(self, waitingStructures: tuple[WaitingType, ...]):
        if len(waitingStructures) != self.HAND_LENGTH:
            raise ValueError("Wrong waitings length.")

        object.__setattr__(self, "waitingStructures", waitingStructures)

