from baseclass.SDetection import SDetection
from tool import config
from sklearn.metrics import classification_report
from sklearn import preprocessing
import numpy as np
from sklearn import metrics
import scipy
from scipy.sparse import csr_matrix
from itertools import combinations

import sys

class HHTSVM(SDetection):
    def __init__(self, conf, trainingSet=None, testSet=None, labels=None, fold='[1]'):
        super(HHTSVM, self).__init__(conf, trainingSet, testSet, labels, fold)

    def __calculateSimilarity(self):
        x = np.zeros((self.itemNum, self.itemNum))
        
        for i,j in combinations(range(self.itemNum),2):
            x[int(i)][int(j)] = 0

        return x

    def __userItemNovelty(self, user, item):
        # All items rated by this user
        itemk, itemv = self.dao.allUserRated(user)
        user_item_novelty = 0
        for k in itemk:
            if (not self.dao.containsItem(k)):
                continue

            i = int(item) - 1
            j = int(k) - 1

            if i > j:
                i, j = j, i

            user_item_novelty += (1 - self.item_similarity_matrix[i][j])

        user_item_novelty /= len(itemk)

        return user_item_novelty

    def readConfiguration(self):
        super(HHTSVM, self).readConfiguration()
        # K = top-K vals of cov
        #self.k = int(self.config['kVals'])
        self.userNum = len(self.dao.trainingSet_u)
        self.itemNum = len(self.dao.trainingSet_i)

        # n = attack size or the ratio of spammers to normal users
        self.n = float(self.config['attackSize'])


    def buildModel(self):
        # Calculate similarity between all items
        #self.item_similarity_matrix = self.__calculateSimilarity
        self.item_similarity_matrix = self.__calculateSimilarity()
        #print self.item_similarity_matrix.shape

        # Construct item novelty vector
        # For every item in  training set
        self.item_novelty_vector = np.zeros(self.itemNum)
        for item in self.dao.trainingSet_i:
            print item
            item_novelty = 0

            # For each genuine user which rated this item
            genuine_users = 0
            for user in self.dao.trainingSet_u:
                if (self.labels[user] == '0'):
                    genuine_users += 1
                    if (self.dao.contains(user, item)):
                        # Calculate the novelty of this item for this user
                        item_novelty += self.__userItemNovelty(user, item)

            item_novelty /= genuine_users


        sys.exit(0)   
        # Construct NBRSu for each user

        # Construct PBRSu for each user

        # Generate first IMF with EMD

        # Generate amplitued, phase, and velocity with HHT

    def predict(self):
        print 'predict spammer'
        spamList = []
        i = 0
        while i < self.n * len(self.disSort):
            spam = self.disSort[i][0]
            spamList.append(spam)
            self.predLabels[spam] = 1
            i += 1

        # trueLabels
        for user in self.dao.trainingSet_u:
            userInd = self.dao.user[user]
            self.testLabels[userInd] = int(self.labels[user])

        return self.predLabels











