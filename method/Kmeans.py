from baseclass.SDetection import SDetection
from tool import config
from sklearn.metrics import classification_report
from sklearn import preprocessing
import numpy as np
from sklearn import metrics
import scipy

import math
from scipy.cluster.vq import vq, kmeans, whiten
from numpy import vstack,array
from numpy.random import rand


class Kmeans(SDetection):
    def __init__(self, conf, trainingSet=None, testSet=None, labels=None, fold='[1]', k=None, n=None ):
        super(Kmeans, self).__init__(conf, trainingSet, testSet, labels, fold)


    def readConfiguration(self):
        super(Kmeans, self).readConfiguration()
	self.depth = int(self.config['depth'])
	self.p = int(self.config['precision'])
        self.userNum = len(self.dao.trainingSet_u)
        self.itemNum = len(self.dao.trainingSet_i)

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

	self.bdt = self.BKM(Umatrix, self.depth, range(len(Umatrix)) )


    ## bdt = bdt from BKM
    ## returns the elements from bdt that are shilling
    def predict(self):
	print 'predicting spammers'
	bdt = self.bdt
	p = self.p
	parent = bdt
        # Left or right?
	if bdt.leftICC > bdt.rightICC:
            # Going left
            #parent = bdt.left
            parentICC = bdt.leftICC
	    bdt = bdt.left
	else:
            # Going right
            #parent = bdt.right
            parentICC = bdt.rightICC
	    bdt = bdt.right

        minimum = parentICC - (parentICC *(p/100))
        maximum = parentICC + (parentICC *(p/100))
	while(
            (bdt.leftICC   < minimum or bdt.leftICC  > maximum) and
            (bdt.rightICC  < minimum or bdt.rightICC > maximum)
            ):
            if bdt.leftICC > bdt.rightICC:
                parent = bdt
                parentICC = bdt.leftICC
                if bdt.left: # if left subtree exists, go
                    bdt = bdt.left
                else:
                    break
            else:
                parent = bdt
                parentICC = bdt.rightICC
                if bdt.right: # right subtree exists, go
                    bdt = bdt.right
                else:
                    break
            minimum = parentICC - (parentICC *(p/100))
            maximum = parentICC + (parentICC *(p/100))

        for s in parent.sidx:
            self.predLabels[s] = 1 # mark shillers

        # trueLabels
        for user in self.dao.trainingSet_u:
            userInd = self.dao.user[user]
            self.testLabels[userInd] = int(self.labels[user])

	return self.predLabels


    class BDT:                      ## Tree node
	def __init__(self, parent, sidx):
	    self.centers = None # This node's data's centres, 2 x M matrix
	    self.left = None # left subtree (BDT)
	    self.leftICC = None # ICC of left subtree (float)
	    self.right = None # right subtree (BDT)
	    self.rightICC = None # ICC of right subtree (float)
	    self.parent = parent # parent node (BDT)
            self.data = [] # this node's data, M x k
            self.sidx = sidx


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
	    r += (M_i[i]*C[i])-(n*mu_X*mu_C)
	r = r/((n-1)*sig_C*sig_X)

	return r

    def ICC(self, C,M):
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
	    similarities[i] = self.PCC(M[i],C,mu_C,sig_C)
	    #similarities[i] = scipy.stats.mstats.pearsonr(M[i],C)

	mu_s = 0.0
	for i in range(0,len(M)):
	    mu_s += similarities[i]
	mu_s = mu_s/len(M)

	return mu_s

## U = nxm user item matrix of float values
## N = stopping criterion, i.e. depth of bdt
## returns a bdt

    def BKM(self, U, N, sidx):
	bdt = self.BDT(None, sidx)
        bdt.data.append(U)
	bdt.centers,_ = kmeans(U,2)
        bdt.left = self.BDT(bdt, [])
        bdt.right = self.BDT(bdt, [])

       #import sys
       #print "---"
       #for sh in sidx:
       #    sys.stdout.write(str(sh))
       #    sys.stdout.write(',')
       #print "---"

	idx,_ = vq(U,bdt.centers)
	for i in range(0,len(U)):
	    if idx[i] == 0:
		bdt.left.data.append(U[i])
		bdt.left.sidx.append(sidx[i])
	    else:
		bdt.right.data.append(U[i])
		bdt.right.sidx.append(sidx[i])
	bdt.leftICC = self.ICC(bdt.centers[0],bdt.left.data)
	bdt.rightICC = self.ICC(bdt.centers[1],bdt.right.data)
	if len(bdt.left.data) > N:
	    bdt.left = self.BKM(bdt.left.data,N, bdt.left.sidx)
	if len(bdt.right.data) > N:
	    bdt.right = self.BKM(bdt.right.data,N, bdt.right.sidx)
	return bdt

