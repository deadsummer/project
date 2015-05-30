#! /usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import codecs
import text_analysis as txtan
import numpy as np

from sklearn.decomposition import TruncatedSVD
from sklearn.random_projection import sparse_random_matrix

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

s_w=[]
for x in sent:
	s_w.append(txtan.split_sent_simple(x))
	
s_w_roots=list(map(lambda x: list(map(txtan.stem,x)), s_w))

roots1=[]
for x in s_w_roots:
	for k in x:
		roots1.append(k)
print("ready///")		
roots=[]
while len(roots1)>0:
	roots.append(roots1[0])
	k=1
	while k<len(roots1):
		if roots1[k]==roots1[0]:
			del roots1[k]
		else:
			k=k+1
	del roots1[0]
	
n_roots=len(roots)
print("ready///")

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

print("ready///")
for i in range(n_roots):
	for j in range(n_roots):
		if prop_r_r[i][j]>0.01:
			f.write(roots[i])
			f.write("\t")
			f.write(roots[j])
			f.write("\n")
f.write("\n---------\n")
def low_rank_approx(SVD=None, A=None, r=1):
    """
    Computes an r-rank approximation of a matrix
    given the component u, s, and v of it's SVD

    Requires: numpy
    """
    if not SVD:
        SVD = np.linalg.svd(A, full_matrices=False)
    u, s, v = SVD
    Ar = np.zeros((len(u), len(v)))
    for i in range(r):
        Ar += s[i] * np.outer(u.T[i], v[i])
    return Ar

M=prop_r_r-low_rank_approx(A=prop_r_r,r=20)
			
for i,j in zip(*np.where(M>=(0.002))):
	f.write(roots[i]+"  "+roots[j]+"\n")
	
	#bitch!
