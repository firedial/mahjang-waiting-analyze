import src.WaitingTilePattern as WaitingTilePattern
import csv


result = WaitingTilePattern.main()

csvForm = []
for value in result:
    value['suit'] = ''.join(map(lambda x: str(x), value['suit']))
    value.pop("number")
    csvForm.append(value)

with open('result/waitingTilePattern.csv', 'w') as f:
    writer = csv.DictWriter(f, ['suit', 'left', 'right'])
    writer.writerows(csvForm)
