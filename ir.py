import result.uniqueIrreciblePattern
from src.Suit import Suit

patterns = result.uniqueIrreciblePattern.getUniqueIrreciblePatterns()


def getCenterWaitings():
    return {frozenset({'W029', 'W110', 'W008'}), frozenset({'W009', 'W025'}), frozenset({'W057', 'W060'}), frozenset({'W044', 'W110'}), frozenset({'W007', 'W003', 'W002'}), frozenset({'W009', 'W008'}), frozenset({'W114', 'W003', 'W027', 'W008'}), frozenset({'W013', 'W039'}), frozenset({'W026', 'W009', 'W025'}), frozenset({'W033', 'W103'}), frozenset({'W088', 'W017'}), frozenset({'W029', 'W032', 'W008'}), frozenset({'W003', 'W002'}), frozenset({'W009', 'W027', 'W008', 'W025'}), frozenset({'W040', 'W041'}), frozenset({'W032', 'W008', 'W113', 'W009', 'W025'}), frozenset({'W003', 'W028'}), frozenset({'W099', 'W100'}), frozenset({'W007', 'W003'}), frozenset({'W006', 'W017'}), frozenset({'W028', 'W002'}), frozenset({'W033', 'W002'}), frozenset({'W001', 'W004', 'W002'}), frozenset({'W028', 'W027', 'W003', 'W109', 'W008'}), frozenset({'W005', 'W068'}), frozenset({'W003', 'W112', 'W008'}), frozenset({'W088', 'W006'}), frozenset({'W029', 'W008'}), frozenset({'W031', 'W002'}), frozenset({'W009', 'W029'}), frozenset({'W026', 'W025'}), frozenset({'W001', 'W004'}), frozenset({'W009', 'W110', 'W008', 'W025'}), frozenset({'W094', 'W002'}), frozenset({'W033', 'W003'}), frozenset({'W005', 'W015'}), frozenset({'W068', 'W015'}), frozenset({'W001', 'W002'}), frozenset({'W097', 'W016'}), frozenset({'W027', 'W003', 'W109'}), frozenset({'W009', 'W027', 'W008'}), frozenset({'W019', 'W018'}), frozenset({'W031', 'W004', 'W002'}), frozenset({'W062', 'W024'}), frozenset({'W027', 'W008'})}


count = 0
# centerWaitings = set()
edgeWaitings = set()
result = dict()
for key, value in patterns.items():
    suit = Suit(key)
    waitingNumber = set(map(lambda x: x[:4], value))

    # 一意になっている
    if len(waitingNumber) == 1:
        s = list(waitingNumber)[0]
        result[s] = result.get(s, 0) + 1
        continue

    if waitingNumber in getCenterWaitings():
        continue

    # for waiting in value:
    #     if waiting[-1] == 'l' or waiting[-1] == 'r':
    #         break
    # else:
    #     centerWaitings.add(frozenset(waitingNumber))

    edgeWaitings.add(frozenset(value))
    count += 1

# print(centerWaitings)
print(edgeWaitings)
print(len(edgeWaitings))
print(len(getCenterWaitings()))
print(count)


result_sorted = sorted(result.items(), key=lambda x:x[1])
print(result_sorted)