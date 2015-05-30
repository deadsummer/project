#! /usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import codecs
import text_analysis as txtan

from bs4 import BeautifulSoup
import re
f = codecs.open('wiki.txt','w', encoding='utf-8')
def GetURL(url):
    s = 'error'
    try:
        f = urllib.request.urlopen(url)
        s = f.read()
    except urllib.error.HTTPError:
        s = 'connect error'
    except urllib.error.URLError:
        s = 'url error'
    return s
 

soup = BeautifulSoup(GetURL('https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%BA%D0%BE%D0%BD_%D0%91%D0%B8%D0%BE_%E2%80%94_%D0%A1%D0%B0%D0%B2%D0%B0%D1%80%D0%B0_%E2%80%94_%D0%9B%D0%B0%D0%BF%D0%BB%D0%B0%D1%81%D0%B0'))

for x in soup.find_all(class_="reference"):
	x.extract()
for x in soup.find_all(class_="mw-editsection"):
	x.extract()
for x in soup.find_all(style="display:none"):
	x.extract()
for x in soup.find_all(id="toc"):
	x.extract()
for x in soup.find_all(class_="infobox vcard"):
	x.extract()
content=soup.find(id="mw-content-text")

text=content.get_text()
sent=txtan.split_text(text)

words=[]
for x in sent:
	words.append(x.split())


for i in range(len(words)):
	for j in range(len(words[i])):
		l=0
		while l<len(words[i][j]):
			if words[i][j][l].isalnum()==False:
				words[i][j]=words[i][j][:l]+words[i][j][l+1:]
			else:
				l=l+1
for i in range(len(words)):
	j=0
	while j < len(words[i]):
		if len(words[i][j])<1 or words[i][j]=="в":
			del words[i][j]
		else:
			j=j+1
		
for x in words:
	for k in x:
		f.write(k)
		f.write("\n")
	f.write("\n\n")
#s_w=[]
#for x in words:
#	s_w.append(txtan.split_sent(x))
#for x in sent:
#	a=txtan.split_sent(x)
#	f.write(str(a))
#	f.write("\n")
#	
#for x in s_w:
#	for k in x:
#		f.write(k)
#		f.write("\n")
#	f.write("\n\n")
 

