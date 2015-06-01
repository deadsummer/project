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

A=([1,2,3,4],[2,4,6,8],[10,20,30,40],[2,5,6,8])
print(A)
A = np.array(A,dtype=np.float)
#print(A)
#for i in range(4):
#	for j in range(4):
#		if A[i][j]<10:
#			A[i][j]=88
#print(A)
X=scipy.sparse.csr_matrix(A)

def low_rank_approx(A=None, r=1):
	from sklearn.decomposition import TruncatedSVD
	svd  =  TruncatedSVD(n_components = r,  random_state = 42)
	A=svd.fit_transform(A)
	A_sp=sp.csc_matrix(A)
	B_sp=sp.csc_matrix(svd.components_)
	print(str(sp.isspmatrix_csc(A_sp)))
	print(str(sp.isspmatrix_csc(B_sp)))
	return(A_sp.dot(B_sp))
	


#from sklearn.random_projection import sparse_random_matrix
#X = sparse_random_matrix(10000, 10000, density=0.0001, random_state=42)
Z=low_rank_approx(X,1)
print(Z)
