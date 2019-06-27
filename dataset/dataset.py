#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 10:58:38 2019

@author: dongdong
"""


from .tushare_market_data import LoadTradeCalendar,LoadHistoryData
from abc import ABCMeta, abstractmethod, abstractproperty
class DataSet(metaclass=ABCMeta):
    def __init__(self):
        pass
    @abstractmethod
    def Update(self,ind):
        pass
    
    @abstractmethod
    def GetLatestInd(self,N = 1):
        pass
    
    @abstractmethod
    def ComeToEnd(self,ind):
        pass   
    @abstractmethod
    def GetLatestPrice(self,code):
        pass  
    
class HistToryDataSet(DataSet):
    def __init__(self):
        self.__data = {}
    def init(self,start,end):
        self.__ind_list = LoadTradeCalendar(start,end)
        for date in self.__ind_list:
            data = LoadHistoryData(date)
            if data == None:
                raise "Can not find data"
            self.__data.update({date : data})
        self.__datasize = len(self.__ind_list)
    def GetSliceData(self,end_ind,delta):
        if end_ind < delta-1 :
            return None
        if end_ind >= self.__datasize:
            return None
        res = []
        for ind in range(end_ind - delta + 1 , end_ind + 1):
            res.append(self.__data[self.__ind_list[ind]])
        return res
    def Update(self,ind):
        return ind + 1
    def ComeToEnd(self,ind):
        if ind >= self.__datasize - 1:
            return True
        return False
    def GetLatestInd(self,N = 1):
        return self.ind_list[-1]   
    def GetLatestPrice(self,code):
        return 1.0

    
class RealTimeDataSet(DataSet):
    def __init__(self):
        pass
    def Update(self,ind):
        self.data = self.GetNewData()
        return ind
    def ComeToEnd(self,ind):
        timenow = '15:00'
        if timenow:
            return False
def CreateHistoryDataSet():
    return HistToryDataSet()