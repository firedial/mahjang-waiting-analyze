import src.WaitingPattern as WaitingPattern

result = WaitingPattern.main()
f = open('result/waitingPattern.py', 'w')
f.write("def getWaitingPatterns():\n\treturn ")
print(list(result.values()), file = f)
f.close()
