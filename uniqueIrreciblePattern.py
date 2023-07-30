import src.UniqueIrreciblePattern as UniqueIrreciblePattern

result = UniqueIrreciblePattern.main()
f = open('result/uniqueIrreciblePattern.py', 'w')
f.write("def getUniqueIrreciblePatterns():\n\treturn ")
print(result, file = f)
f.close()
