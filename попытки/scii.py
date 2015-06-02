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
print(A[2,:])
print(np.dot(A[2,:],A[:,3]))