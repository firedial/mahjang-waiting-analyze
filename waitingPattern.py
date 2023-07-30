import src.WaitingPattern as WaitingPattern

result = WaitingPattern.main()
f = open('result/waitingPattern.py', 'w')
f.write("def getWaitingPattern():\n\treturn ")
print(result, file = f)
f.close()
