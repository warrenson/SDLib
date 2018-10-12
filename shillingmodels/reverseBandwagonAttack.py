#coding:utf-8
#author:Benjamin Warren
#modified from bandwagAttack.py, author:Yu Junliang
# Only real difference is not reversing the sort on the items
# and using the min score as the targetScore in the config (config/reverse_bandwagon_config.conf)

import random

import numpy as np
from attack import Attack


class ReverseBandWagonAttack(Attack):
    def __init__(self,conf):
        super(ReverseBandWagonAttack, self).__init__(conf)
        self.coldItems = sorted(self.itemProfile.iteritems(), key=lambda d: len(d[1]), reverse=False)[
                   :int(self.selectedSize * len(self.itemProfile))]


    def insertSpam(self,startID=0):
        print 'Modeling reverse bandwagon attack...'
        itemList = self.itemProfile.keys()
        if startID == 0:
            self.startUserID = len(self.userProfile)
        else:
            self.startUserID = startID

        for i in range(int(len(self.userProfile)*self.attackSize)):
            #fill 装填项目
            fillerItems = self.getFillerItems()
            for item in fillerItems:
                self.spamProfile[str(self.startUserID)][str(itemList[item])] = random.randint(self.minScore,self.maxScore)
            #selected 选择项目
            selectedItems = self.getSelectedItems()
            for item in selectedItems:
                self.spamProfile[str(self.startUserID)][item] = self.targetScore
            #target 目标项目
            for j in range(self.targetCount):
                target = np.random.randint(len(self.targetItems))
                self.spamProfile[str(self.startUserID)][self.targetItems[target]] = self.targetScore
                self.spamItem[str(self.startUserID)].append(self.targetItems[target])
            self.startUserID += 1

    def getFillerItems(self):
        mu = int(self.fillerSize*len(self.itemProfile))
        sigma = int(0.1*mu)
        markedItemsCount = int(round(random.gauss(mu, sigma)))
        if markedItemsCount < 0:
            markedItemsCount = 0
        markedItems = np.random.randint(len(self.itemProfile), size=markedItemsCount)
        return markedItems

    def getSelectedItems(self):

        mu = int(self.selectedSize * len(self.itemProfile))
        sigma = int(0.1 * mu)
        markedItemsCount = abs(int(round(random.gauss(mu, sigma))))
        markedIndexes =  np.random.randint(len(self.coldItems), size=markedItemsCount)
        markedItems = [self.coldItems[index][0] for index in markedIndexes]
        return markedItems
