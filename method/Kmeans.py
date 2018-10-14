from baseclass.SDetection import SDetection
from tool import config
from sklearn.metrics import classification_report
from sklearn import preprocessing
import numpy as np
from sklearn import metrics
import scipy
from scipy.sparse import csr_matrix

import math
from scipy.cluster.vq import vq, kmeans, whiten
from numpy import vstack,array
from numpy.random import rand


class Kmeans(SDetection):
    def __init__(self, conf, trainingSet=None, testSet=None, labels=None, fold='[1]', k=None, n=None ):
        super(Kmeans, self).__init__(conf, trainingSet, testSet, labels, fold)


    def readConfiguration(self):
        super(Kmeans, self).readConfiguration()
        # K = top-K vals of cov
        #self.k = int(self.config['kVals'])
	self.depth = int(self.config['depth'])
	self.p = 10
        self.userNum = len(self.dao.trainingSet_u)
        self.itemNum = len(self.dao.trainingSet_i)
       #if self.k >= min(self.userNum, self.itemNum):
       #    self.k = 3
       #    print '*** k-vals is more than the number of user or item, so it is set to', self.k

        # n = attack size or the ratio of spammers to normal users
        #self.n = float(self.config['attackSize'])


    def buildModel(self):
	## U = nxm user item matrix of float values
	## N = stopping criterion, i.e. depth of bdt

	# Generate matrix U
        Umatrix = np.zeros([self.userNum, self.itemNum], dtype=float)
        self.testLabels = np.zeros(self.userNum)
        self.predLabels = np.zeros(self.userNum)
	
        print 'construct matrix'
        for user in self.dao.trainingSet_u:
            for item in self.dao.trainingSet_u[user].keys():
                value = self.dao.trainingSet_u[user][item]
                a = self.dao.user[user]
                b = self.dao.item[item]
                Umatrix[a][b] = value

	print 'Builing Kmean model'

	self.bdt = self.BKM(Umatrix, self.depth)


    ## bdt = bdt from BKM
    ## returns the elements from bdt that are shilling
    def predict(self):
	print 'predicting spammers'
	bdt = self.bdt
	p = self.p
	
	if bdt.leftICC > bdt.rightICC:
	    minimum = bdt.leftICC - (bdt.rightICC *(p/100))
	    maximum = bdt.leftICC + (bdt.rightICC *(p/100))
	    bdt = bdt.left
	else:
	    minimum = bdt.rightICC - (bdt.rightICC *(p/100))
	    maximum = bdt.rightICC + (bdt.rightICC *(p/100))
	    bdt = bdt.right
	while((bdt.leftICC and bdt.rightICC) not in range(minimum,maximum)):
	    if bdt.leftICC > bdt.rightICC:
		parent = bdt.left
		if len(bdt.left) > 0:
		    bdt = bdt.left
	    else:
		parent = bdt.right
		if len(bdt.right) > 0:
		    bdt = bdt.right
	#print parent.shape
	return parent


    class BDT(object):                      ## just a stupid container
	def __init__(self):
	    self.centers = None
	    self.left = []
	    self.leftICC = None
	    self.right = []
	    self.rightICC = None
	    self.parent = None


    def PCC(self, M_i, C, mu_C, sig_C):
	n = len(M_i)
	mu_X = 0.0
	sig_X = 0.0
	mu_C += 0.0
	sig_C += 0.0
	r = 0.0

	for i in range(0,n):
	    mu_X += M_i[i]
	mu_X = mu_X/n                       ## mean of 'x'

	for i in range(0,n):
	    sig_X += (M_i[i] - mu_X)**2
	sig_X = sig_X/(n-1)
	sig_X = math.sqrt(sig_X)            ## std of 'x'

	for i in range(0,n):
	    val = (M_i[i]*C[i])-(n*mu_X*mu_C)
	    print n
	    print "rshape: ", val.shape
	    r += val
	r = r/((n-1)*sig_C*sig_X)

	return r

    def ICC(self, C,M):
        print C.shape
        print M.shape
	similarities = [0 for x in range(len(M))]
	mu_C = 0.0
	sig_C = 0.0

	for i in range(0,len(C)):
	    mu_C += C[i]
	mu_C = mu_C/len(C)

	for i in range(0,len(C)):
	    sig_C += (C[i] - mu_C)**2
	sig_C = sig_C / (len(C)-1)
	sig_C = np.sqrt(sig_C)

	for i in range(0,len(M)):
	    #similarities[i] = self.PCC(M[i],C,mu_C,sig_C)
	    similarities[i] = scipy.stats.mstats.pearsonr(M[i],C)

	mu_s = 0.0
	for i in range(0,len(M)):
	    mu_s += similarities[i]
	mu_s = mu_s/len(M)

	return mu_s

## U = nxm user item matrix of float values
## N = stopping criterion, i.e. depth of bdt
## returns a bdt

    def BKM(self, U,N):
	bdt = self.BDT()
	bdtleft = self.BDT()
	bdtrght = self.BDT()
	bdtleft.parent = bdt
	bdtrght.parent = bdt
	bdt.centers,_ = kmeans(U,2)
        print bdt.centers.shape

	idx,_ = vq(U,bdt.centers)
	for i in range(0,len(U)):
	    if idx[i] == 0:
		bdt.left.append(U[i])
	    else:
		bdt.right.append(U[i])
	bdt.leftICC = self.ICC(bdt.centers,bdt.left)
	bdt.rightICC = self.ICC(bdt.centers,bdt.right)
	if len(bdt.left) > N:
	    bdtleft = self.BKM(bdt.left,N)
	if len(bdt.right) > N:
	    bdtrght = self.BKM(bdt.right,N)
	return bdt

