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

A=([0,0,3,0],[0,0,0,8],[10,0,0,0],[0,0,6,0])
print(A)
A = np.array(A,dtype=np.float)
print(A)
for i in range(4):
	for j in range(4):
		if A[i][j]<10:
			A[i][j]=88
print(A)
A=scipy.sparse.coo_matrix(A)
print(A)

def low_rank_approx(A=None, r=1):
	from sklearn.decomposition import TruncatedSVD
	svd  =  TruncatedSVD(n_components = r,  random_state = 42)
	A=svd.fit_transform(A)

	return(np.dot(A,svd.components_))
	
M=low_rank_approx(A=A,r=3)	
print("/n-----/n")
print(M)