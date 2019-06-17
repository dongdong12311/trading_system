#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:30:08 2019

@author: dongdong
"""
from abc import abstractmethod
class API:
    def __init__(self):
        pass
class MarketDataAPI(API):
    def __init__(self):
        pass
    def RegisterDataPtr(self,dataptr):
        self._dataptr = dataptr
    
class SimulatedMarketDataAPI(MarketDataAPI):
    def __init__(self):
        super().__init__()
    
class PositionInfoAPI(API):
    def __init(self):
        super().__init__()
    def RegisterPortfolio(self,portfolio):
        self._portfolio = portfolio
class SimulatedPositionInfoAPI(PositionInfoAPI):
    def __init__(self):
        super().__init__()
        
        
class ExcutionAPI(API):
    def __init__(self):
        pass
    @abstractmethod
    def execute_order(self,orderevent):
        raise "no implement error"
        
class SimulatedExcutionAPI(ExcutionAPI):
    def __init__(self):
        super().__init__()
    def RegisterSimulatedPortfolio(self,portfolio):
        self.__portfolio = portfolio
    def execute_order(self,orderevent):
        print(orderevent)
        
    
        
def CreateMarketDataAPI():
    return SimulatedMarketDataAPI()

def CreatePositionInfoAPI():
    return SimulatedPositionInfoAPI()

def CreateOrderInfoAPI():
    return None
def CreateExcutionAPI():
    return SimulatedExcutionAPI()