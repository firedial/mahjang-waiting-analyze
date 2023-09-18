import src.AllWaitingStructurePattern as AllWaitingStructurePattern
import csv


result = AllWaitingStructurePattern.main()

csvForm = []
for value in result:
    value['suit'] = ''.join(map(lambda x: str(x), value['suit']))
    value['waitingStructure'] = "|" + value['waitingStructure'][0:3] + "|" + value['waitingStructure'][3:6] + "|" + value['waitingStructure'][6:] + "|"
    csvForm.append(value)

with open('result/allWaitingStructurePattern.csv', 'w') as f:
    writer = csv.DictWriter(f, ['suit', 'waitingStructure'])
    writer.writerows(csvForm)
