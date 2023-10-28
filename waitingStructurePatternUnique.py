import src.WaitingStructurePatternUnique as WaitingStructurePatternUnique
import csv


waitingStructurePatterns = {}
count = 1
with open('result/waitingStructurePattern.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        waitingStructurePatterns[row[0]] = count
        count += 1

result = WaitingStructurePatternUnique.main(waitingStructurePatterns, [1, 2, 4, 5, 7, 8, 10, 11, 13])

csvForm = []
for value in result:
    value['suit'] = ''.join(map(lambda x: str(x), value['suit']))
    csvForm.append(value)

with open('result/waitingStructurePatternUnique.csv', 'w') as f:
    writer = csv.DictWriter(f, ['suit', 'pattern'])
    writer.writerows(csvForm)
