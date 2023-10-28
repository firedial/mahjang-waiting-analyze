import src.WaitingStructurePattern as WaitingStructurePattern
import csv


result = WaitingStructurePattern.main()

csvForm = []
for value in result:
    value['suit'] = ''.join(map(lambda x: str(x), value['suit']))
    csvForm.append(value)

with open('result/waitingStructurePattern.csv', 'w') as f:
    writer = csv.DictWriter(f, ['suit'])
    writer.writerows(csvForm)
