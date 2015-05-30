import codecs
f = codecs.open('polietilen_037_ZBS.txt', encoding='utf-8')
data = [line.strip() for line in f.readlines()]
f2 = codecs.open('polietilen_037_ZBS_3.txt', 'w', encoding='utf-8')
print (data)
for i in range (0,((len(data)//10)+1)):
	print(data[i*10], file=f2)
f.close()
f2.close()
input()
