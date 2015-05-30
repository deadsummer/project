import codecs
f = codecs.open('data.txt', encoding='utf-8')
data = f.readlines()

j=0
s=[]
for i in range (0,len(data)):
	g=data[i].split(".")
	s=s+g
#print(s)
#print(len(s))
for i in range (len(s)):
		while s[i][0:1]==" ":
			s[i]=s[i][1:]
		if len(s[i])==0: 
			del s[i]
word=[]
sent=["0"]*len(s)
for i in range(len(s)):
    sent[i] = s[i].split(" ")
print (sent)

input()