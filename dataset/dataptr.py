#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:41:39 2019

@author: dongdong
"""

from event.event import MarketEvent
class DataPtr:
    def __init__(self,dataset):
        self.__ind = 0
        self.dataset = dataset
    def GetLatestPrice(self,code):
        return self.dataset.GetLatestPrice(code)
    def GetSliceData(self,N = 1):
        return self.dataset.GetSliceData(self.__ind,N)
    
    def Update(self,events):

        if self.dataset.ComeToEnd(self.__ind):
            return False
        self.__ind =  self.dataset.Update(self.__ind)
        
        events.put(MarketEvent())
        return True

    
def CreateDataPtr(dataset):
    return DataPtr(dataset)