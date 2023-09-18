import src.WaitingPattern as WaitingPattern
import csv
from src.Hand import Hand

def isSameWaitingStructure(hand: Hand, removedHand: Hand):
    removedSuit = hand.suit - removedHand.suit

    # 面子だった場合は待ちが変わっていないことだけ見ればいい
    if removedSuit.sum() == 3:
        return hand.waitingStructure == removedHand.waitingStructure and hand.isSendable == removedHand.isSendable

    # 雀頭だった場合
    if removedSuit.sum() == 2:
        index2 = removedSuit.findFirstNumber(2)
        if removedHand.isSendable and hand.waitingStructure.waitingStructures[index2].isShampon:
            # if removedHand.waitingStructure.waitingStructures[index2].isShampon:
            #     print(hand)
            #     # シャンポン除いても同じ数字でシャンポン待ちがある場合は4枚使いパターン
            #     raise RuntimeError("Unexpected error.")

            return removedHand.waitingStructure.addShampon(index2) == hand.waitingStructure
        else:
            return removedHand.waitingStructure == hand.waitingStructure

    return False

    # 雀頭接続順子だった場合
    if removedSuit.sum() == 5:
        index3 = removedSuit.findFirstNumber(3)
        index1 = removedSuit.findFirstNumber(1)

        # 311 パターン
        if index3 < index1:
            if self.isSendable and Agari.isShampon(other.suit, index3) and Agari.isRyanmen(other.suit, index3, True) and Agari.isRyanmen(other.suit, index3 + 3, False):
                if self.waiting.waitings[index1 + 2] and self.waiting.waitings[index3]:
                    return False
                addedWaiting = self.waiting.getWaitingAddTile(index1 + 2).getWaitingAddTile(index3)
                return addedWaiting == other.waiting
            else:
                return self.waiting == other.waiting
        # 113 パターン
        else:
            if self.isSendable and Agari.isShampon(other.suit, index3) and Agari.isRyanmen(other.suit, index3, False) and Agari.isRyanmen(other.suit, index3 - 3, True):
                if self.waiting.waitings[index1 - 1] and self.waiting.waitings[index3]:
                    return False
                addedWaiting = self.waiting.getWaitingAddTile(index1 - 1).getWaitingAddTile(index3)
                return addedWaiting == other.waiting
            else:
                return self.waiting == other.waiting

    raise ValueError("Invalid pattern.")

result = WaitingPattern.main(isSameWaitingStructure)

csvForm = []
for value in result:
    value['suit'] = ''.join(map(lambda x: str(x), value['suit']))
    csvForm.append(value)

with open('result/waitingPattern.csv', 'w') as f:
    writer = csv.DictWriter(f, ['number', 'suit', 'left', 'right', 'isAcs'])
    writer.writeheader()
    writer.writerows(csvForm)
