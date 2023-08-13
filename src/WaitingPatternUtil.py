from src.Hand import Hand
from dataclasses import dataclass
import csv


@dataclass(frozen=True)
class WaitingPatternUtil:

    waitingPatterns: dict

    def __init__(self):
        waitingPatterns = []
        with open('result/waitingPattern.csv') as f:
            reader = csv.DictReader(f)
            patterns = [row for row in reader]

            for value in patterns:
                value['suit'] = tuple(int(x) for x in value['suit'])
                value['isAcs'] = value['isAcs'] == 'True'
                value['left'] = value['left'] == 'True'
                value['right'] = value['right'] == 'True'
                waitingPatterns.append(value)


        object.__setattr__(self, "waitingPatterns", waitingPatterns)


    def getWaitingPatternNumber(self, hand: Hand):
        acsFiltered = list(filter(lambda x: x['isAcs'] == hand.isAtamaConnectedShuntsu, self.waitingPatterns))
        suit = hand.suit

        positionNumber = suit.getPosition()
        # 左接地系
        if positionNumber == 0:
            position = "l"
        # 右接地系
        elif positionNumber + suit.getRange() == 9:
            position = "r"
        else:
            # 1 始まりなので 1 足している
            position = str(positionNumber + 1)

        # 前方重心 or 対称形
        if suit.getSuitGravityPosition() >= 0:
            direction = "a"
        # 後方重心
        else:
            direction = "d"

        basicFormSuit = suit.getBasicFormSuit()
        basicFormFiltered = list(filter(lambda x: x['suit'] == basicFormSuit.suit, acsFiltered))

        # なかった場合
        if len(basicFormFiltered) == 0:
            return None

        # 一つあった場合
        if len(basicFormFiltered) == 1:
            if (position == "l" and direction == "a") or (position == "r" and direction == "d"):
                if not basicFormFiltered[0]['left']:
                    return None

            if (position == "l" and direction == "d") or (position == "r" and direction == "a"):
                if not basicFormFiltered[0]['right']:
                    return None

            return basicFormFiltered[0]['number'] + '-' + direction + position

        raise RuntimeError("something wrong")
