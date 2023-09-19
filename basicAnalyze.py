import src.BasicAnalyze as BasicAnalyze
import csv

with open('result/allWaitingStructurePattern.csv') as f:
    reader = csv.DictReader(f, fieldnames = ['suit', 'waitingStructure'])
    records = [{'suit': tuple(map(lambda x: int(x), row['suit'])), 'waitingStructure': row['waitingStructure'].replace('|', '')} for row in reader]

BasicAnalyze.main(records)
