import urllib.request
import codecs
import text_analysis as txtan
import numpy as np
import scipy
import math as math

import numpy as np
import scipy.sparse as sp


class max_n:
	m_array=[]
	m_poses=[]
	def init(self,n):
		self.m_array=[0]*n
		self.m_poses=[0]*n
	def add(self,a,pos):
		for i in range(len(self.m_array)):
			if a>self.m_array[i]:
				self.m_array[i], a = a, self.m_array[i]
				self.m_poses[i], pos = pos, self.m_poses[i]
	def get_i_pos(self,i):
		if i<len(self.m_poses):
			return self.m_poses[i]
	def get_i_value(self,i):
		if i<len(self.m_poses):
			return self.m_array[i]
			
def low_rank_approx(P=None, r=1,n=5):
		A=sp.csc_matrix(P)
		from sklearn.decomposition import TruncatedSVD
		svd  =  TruncatedSVD(n_components = r,  random_state = 42)
		C=svd.fit_transform(A)
		B=svd.components_
		print(C[1,:])
		print(B[1,:])
		
		indexes_max=[]
		for i in range(n):
			a=[[0]*2 for i in range(n)]
			line=max_n()
			line.init(5)
			for j in range(n):
				line.add(P[i][j]-np.dot(C[i,:],B[:,j]),j)
			for k in range(5):
				indexes_max.append([i,line.get_i_pos(k),line.get_i_value(k)])
			print(str(i)+" from "+str(n)+" string made")
		return indexes_max
		
def sort_by(arr, axe):
		i = len(arr)
		while i > 1:
			for j in range(i - 1):
				if arr[j][axe] < arr[j + 1][axe]:
					arr[j], arr[j+1] = arr[j+1], arr[j]
			i -= 1
		return(arr)
			
def analis():
	w1 = codecs.open('wiki1.txt','r', encoding='utf-8')
	w2 = codecs.open('wiki2.txt','r', encoding='utf-8')
	f = codecs.open('words.txt','w', encoding='utf-8')

	text1=w1.read()
	text2=w2.read()
	
	sent1=txtan.split_text(text1)
	sent2=txtan.split_text(text2)
	
	s_w1=[]
	for x in sent1:
		s_w1.append(txtan.split_sent_simple(x))
	s_w2=[]
	for x in sent2:
		s_w2.append(txtan.split_sent_simple(x))

		
	s_w_roots1=list(map(lambda x: list(map(txtan.stem,x)), s_w1))
	s_w_roots2=list(map(lambda x: list(map(txtan.stem,x)), s_w2))
	
	word_root1=[]
	for i in range(len(s_w_roots1)):
		for k in range(len(s_w_roots1[i])):
			word_root1.append([s_w1[i][k],s_w_roots1[i][k]])
	word_root2=[]
	for i in range(len(s_w_roots2)):
		for k in range(len(s_w_roots2[i])):
			word_root2.append([s_w2[i][k],s_w_roots2[i][k]])
			
	roots0=[]
	for x in s_w_roots1:
		for k in x:
			roots0.append(k)
	for x in s_w_roots2:
		for k in x:
			roots0.append(k)
	print("List of roots built\nMaking normal list without repits")		
	roots=[]
	roots=set(roots0)
	roots=list(roots)
	n_roots=len(roots)
	print("Done "+str(n_roots)+" roots\nMaking matrix")

	r2i={}
	for i,x in enumerate(roots):
		r2i[x]=i

	prop_r_r=[[0] * n_roots for i in range(n_roots)]

	total_pairs=0
	for k in s_w_roots1:
		for m in range(len(k)-1):
			prop_r_r[r2i[k[m]]][r2i[k[m+1]]]+=1
			total_pairs+=1
	for k in s_w_roots2:
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
			
		
	indexes_max=low_rank_approx(P=prop_r_r,r=10,n=n_roots)
	indexes_max=sort_by(indexes_max,2)
	best_indexes_max=indexes_max[0:50]
	print(len(indexes_max))
	#
	#print("Done\nmaking A-USV")
	#Z=sparse_prop-M
	#ZZ=Z.todense()
	#print(ZZ)
	#print("Done\nprinting phrases")
	#ZZZ=ZZ.getA()
	#maxx=ZZZ.max()
	#print(maxx)
	#print(str(sp.isspmatrix_csc(ZZ)))
	#r=[0]*100
	#for x in ZZZ.flat:
	#	if x!=maxx:
	#		n=math.trunc((x/maxx)*100)
	#		r[n]=r[n]+1
	#	else:
	#		r[99]=r[99]+1
	#res=0
	#res_max=200
	#n=99
	#while res<res_max:
	#	res=res+r[n]
	#	n=n-1
	#print((n-1)*maxx/100)
	#
	final1=[]
	final2=[]
	ii=0
	for i,j,k in best_indexes_max:
		out=set()
		final1.append([])
		for s in range(len(word_root1)-1):
			if word_root1[s][1]==roots[i] and word_root1[s+1][1]==roots[j] and (word_root1[s][0]+word_root1[s+1][0]) not in out:
				out.add(word_root1[s][0]+word_root1[s+1][0])
				final1[ii].append(word_root1[s][0]+"  "+word_root1[s+1][0])
		ii+=1
	ii=0
	for i,j,k in best_indexes_max:
		out=set()
		final2.append([])
		for s in range(len(word_root2)-1):
			if word_root2[s][1]==roots[i] and word_root2[s+1][1]==roots[j] and (word_root2[s][0]+word_root2[s+1][0]) not in out:
				out.add(word_root2[s][0]+word_root2[s+1][0])
				final2[ii].append(word_root2[s][0]+"  "+word_root2[s+1][0])
		ii+=1
	return ([final1, final2])
