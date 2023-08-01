import src.WaitingPattern as WaitingPattern

result = WaitingPattern.main()

f = open('result/waitingPattern.py', 'w')
f.write("def getWaitingPatterns():\n    return [\n")
for waiting in result:
    print("        ", file = f, end = "")
    print(waiting, file = f, end = ",\n")
f.write("    ]")
f.close()
