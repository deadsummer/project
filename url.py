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


w = codecs.open('wiki.txt','r', encoding='utf-8')
f = codecs.open('words.txt','w', encoding='utf-8')

text=w.read()

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

print("prop max = "+str(prop_r_r.max()))

#print("making although all elements=0")
#for i in range(n_roots):
#	for j in range(n_roots):
#		if prop_r_r[i][j]<257:
#			prop_r_r[i][j]=0	

print("Done "+str(total_pairs)+" total pairs\nsprasing matrix")
prop_r_r/=total_pairs
sparse_prop=sp.csc_matrix(prop_r_r)

print(prop_r_r.shape)
print(prop_r_r)

print(str(sp.isspmatrix_csc(sparse_prop)))
print("Done\nnmaking USV")
def low_rank_approx(A=None, r=1):
	from sklearn.decomposition import TruncatedSVD
	svd  =  TruncatedSVD(n_components = r,  random_state = 42)
	A=svd.fit_transform(A)
	A_sp=sp.csc_matrix(A)
	B_sp=sp.csc_matrix(svd.components_)
	print(str(sp.isspmatrix_csc(A_sp)))
	print(str(sp.isspmatrix_csc(B_sp)))
	return(A_sp.dot(B_sp))
	
M=low_rank_approx(A=sparse_prop,r=10)

print("Done\nmaking A-USV")
Z=sparse_prop-M
ZZ=Z.todense()
print(ZZ)
print("Done\nprinting phrases")
ZZZ=ZZ.getA()
maxx=ZZZ.max()
print(maxx)
print(str(sp.isspmatrix_csc(ZZ)))
r=[0]*100
for x in ZZZ.flat:
	if x!=maxx:
		n=math.trunc((x/maxx)*100)
		r[n]=r[n]+1
	else:
		r[99]=r[99]+1
res=0
res_max=200
n=99
while res<res_max:
	res=res+r[n]
	n=n-1
print((n-1)*maxx/100)

for i,j in zip(*np.where(ZZZ>=(0.00054))):
	f.write(roots[i]+"  "+roots[j]+"\n")
	
	#bitch!
