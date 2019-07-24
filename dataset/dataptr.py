#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:41:39 2019

@author: dongdong
"""
import numpy as np
from event.event import MarketEvent
class DataPtr:
    def __init__(self,dataset,stock_list,start):
        self.__ind = 0
        self._dataset = dataset
        self._stock_list = stock_list
        self._init(start)
    def _init(self,start):
        self._line_map = {}
        for code in self._stock_list:
            
            self._line_map.update({code : line})
            
    def GetLatestPrice(self,code):
        return self._dataset.GetLatestPrice(code)
    def history_bars(self,stock, expected_return_days, period,field):
        line_map = self._GetLine_map(stock)
        if line_map is not None:
            data =  self._dataset.data[line_map-expected_return_days+1:line_map+1][field]
            data.astype(np.float16)
            data = data/10000
        
    def _GetLine_map(self,stock):
        return self._line_map[stock]
        
        
    def Update(self,events):

        if self._dataset.ComeToEnd(self.__ind):
            return False
        self.__ind =  self._dataset.Update(self.__ind)
        
        events.put(MarketEvent())
        return True

    def now(self):
        return self._dataset.now(self.__ind)
def CreateDataPtr(dataset):
    return DataPtr(dataset)