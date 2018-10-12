#coding:utf-8
#author:Yu Junliang

import random

import numpy as np
from attack import Attack


class SegmentAttack(Attack):
    def __init__(self,conf):
        super(SegmentAttack, self).__init__(conf)
        raise NotImplementedError # not working 

    def insertSpam(self,startID=0):
        print 'Modeling bandwagon attack...'
        itemList = self.itemProfile.keys()
        if startID == 0:
            self.startUserID = len(self.userProfile)
        else:
            self.startUserID = startID

        for i in range(int(len(self.userProfile)*self.attackSize)):
            #fill 装填项目
            fillerItems = self.getFillerItems()
            for item in fillerItems:
                self.spamProfile[str(self.startUserID)][str(itemList[item])] = self.minScore
            #selected 选择项目
            selectedItems = self.getSelectedItems()
            for item in selectedItems:
                self.spamProfile[str(self.startUserID)][item] = self.maxScore
            #target 目标项目
            for j in range(self.targetCount):
                target = np.random.randint(len(self.targetItems))
                self.spamProfile[str(self.startUserID)][self.targetItems[target]] = self.targetScore
                self.spamItem[str(self.startUserID)].append(self.targetItems[target])
            self.startUserID += 1

    #def getFillerItems(self): USING DEFAULT

    def getSelectedItems(self):
        
        # Segment the item set, randomly
        segment_size = int(self.selectedSize * len(self.itemProfile)) 
        markedItemsCount = abs(int(round(segment_size)))
        end = len(self.itemProfile) - markedItemsCount
        start = np.random.randint(0, high=end)
        markedIndexes =  range(start, start + markedItemsCount)
        markedItems = [self.itemProfile.iteritems()[index][0] for index in markedIndexes]
        return markedItems

