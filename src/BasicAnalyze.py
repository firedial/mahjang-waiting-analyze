from src.util.Suit import Suit
from src.util.WaitingStructure import WaitingStructure
from src.util.WaitingType import WaitingType

def main(records):
    suits = [{'suit': Suit(record['suit']), 'waitingStructure': WaitingStructure.getWaitingStructureFromString(record['waitingStructure'])} for record in records]
