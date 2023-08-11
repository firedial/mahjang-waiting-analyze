import src.WaitingPattern as WaitingPattern
import csv

result = WaitingPattern.main()

csvForm = []
for value in result:
    value['suit'] = ''.join(map(lambda x: str(x), value['suit']))
    csvForm.append(value)

with open('result/waitingPattern.csv', 'w') as f:
    writer = csv.DictWriter(f, ['number', 'suit', 'left', 'right', 'isAcs'])
    writer.writeheader()
    writer.writerows(csvForm)
