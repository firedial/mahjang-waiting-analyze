import result.waitingAfterPattern
import result.waitingBeforePattern
import result.waitingPattern


# after = result.waitingAfterPattern.getWaitingPatterns()
after = result.waitingPattern.getWaitingPatterns()
before = result.waitingBeforePattern.getWaitingPatterns()

afterPatterns = set(map(lambda x: x['suit'], after))
beforePatterns = set(map(lambda x: x['suit'], before))

count = 0
for pattern in beforePatterns:
    if pattern not in afterPatterns:
        count += 1
        print(pattern)

print(count)

count = 0
for pattern in afterPatterns:
    if pattern not in beforePatterns:
        count += 1
        print(pattern)

print(count)
