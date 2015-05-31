#! /usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import codecs
import text_analysis as txtan
import numpy as np
import scipy
import math as math

import numpy as np
import scipy.sparse as sp


from bs4 import BeautifulSoup
import re
w = codecs.open('wiki.txt','w', encoding='utf-8')
f = codecs.open('words.txt','w', encoding='utf-8')
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
 

def parser1 (link, text):
	s = BeautifulSoup(GetURL(link))
	nodispclass=["gallerytext","magnify","reference","mw-editsection","display:none","infobox vcard"]
	nodispid=["toc","bitch"]
	content=s.find(id="mw-content-text")
	hren=content.findAll(class_=nodispclass)
	for x in hren:
		x.extract()
	text=text+"\n"+content.get_text()
	return text
	
def parser2 (link0,links,n):
	soup = BeautifulSoup(GetURL(link0))
	CatItems=soup.findAll(class_="CategoryTreeItem")
	
	catlinks=[]
	for x in CatItems:
		catlinks.append("http://ru.wikipedia.org"+x.find('a')['href'])
	Items=soup.find(class_="mw-category")
	links_text=[]
	if Items!=None:
		a=Items.findAll('a')
		for x in a:
			n=n+1
			links.append("http://ru.wikipedia.org"+x['href'])
			links_text.append(x.get_text())
			print(n)
	for x in catlinks:
		links=parser2(x,links,n)
	return links
	
start_page='https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D0%BE%D1%8D%D1%82%D0%B5%D1%81%D1%81%D1%8B_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B9%D1%81%D0%BA%D0%BE%D0%B9_%D0%B8%D0%BC%D0%BF%D0%B5%D1%80%D0%B8%D0%B8'
print("Making links")
links=[]
text=""
links=parser2(start_page, links,0)
print("Done "+str(len(links))+" total links\nMaking text")
links=set(links)
print("Done "+str(len(links))+" different links\nMaking text")
f.write("\n----------\n")

n=0
for x in links:
	n=n+1
	text=parser1(x,text)
	print(n)
w.write(text)
print("Done\nStemming the text")
sent=txtan.split_text(text)

s_w=[]
for x in sent:
	s_w.append(txtan.split_sent_simple(x))
	
s_w_roots=list(map(lambda x: list(map(txtan.stem,x)), s_w))

roots1=[]
for x in s_w_roots:
	for k in x:
		roots1.append(k)
print("List of roots built\nMaking normal list without repits")		
roots=[]
roots=set(roots1)
roots=list(roots)
n_roots=len(roots)
print("Done "+str(n_roots)+" roots\nMaking matrix")

r2i={}
for i,x in enumerate(roots):
	r2i[x]=i

prop_r_r=[[0] * n_roots for i in range(n_roots)]

total_pairs=0
for k in s_w_roots:
	for m in range(len(k)-1):
		prop_r_r[r2i[k[m]]][r2i[k[m+1]]]+=1
		total_pairs+=1
prop_r_r = np.array(prop_r_r,dtype=np.float)

print(prop_r_r.shape)
prop_r_r/=total_pairs

print("Done "+str(total_pairs)+" total pairs\nprinting popular words")
#for i in range(n_roots):
#	for j in range(n_roots):
#		if prop_r_r[i][j]>0.001:
#			f.write(roots[i])
#			f.write("\t")
#			f.write(roots[j])
#			f.write("\n")
#f.write("\n---------\n")
print("Done\nApproxinating matrix")
def low_rank_approx(A=None, r=1):
	from sklearn.decomposition import TruncatedSVD
	svd  =  TruncatedSVD(n_components = r,  random_state = 42)
	A=svd.fit_transform(A)

	return(np.dot(A,svd.components_))
	
M=prop_r_r-low_rank_approx(A=prop_r_r,r=math.ceil(total_pairs/10)	)	
print("Done\nprinting phrases")
for i,j in zip(*np.where(M>=((0.93*M.max())))):
	f.write(roots[i]+"  "+roots[j]+"\n")
	
	#bitch!
