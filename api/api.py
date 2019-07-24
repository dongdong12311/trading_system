#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:30:08 2019

@author: dongdong
"""
from abc import abstractmethod
from event.event import ChangeWeightEvent
class API:
    def __init__(self):
        pass
class MarketDataAPI(API):
    def __init__(self):
        pass
    def RegisterDataPtr(self,dataptr):
        self._dataptr = dataptr
    def GetSliceData(self,N):
        return self._dataptr.GetSliceData(N)
    
    def now(self):
        return self._dataptr.now()
    def history_bars(self,stock, expected_return_days, period,field):
        return self._dataptr.history_bars(stock, expected_return_days, period,field)
class SimulatedMarketDataAPI(MarketDataAPI):
    def __init__(self):
        super().__init__()
    
class PositionInfoAPI(API):
    def __init(self):
        super().__init__()
    def RegisterPortfolio(self,portfolio):
        self._portfolio = portfolio
    def GetPosition(self,code):
        return self._portfolio.GetPosition(code)
    def GetAvailableMoney(self):
        return self._portfolio.AvailableMoney()
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
        symbol = orderevent.symbol
        order_type = orderevent.order_type
        quantity = orderevent.quantity
        price = orderevent.price
        direction = orderevent.direction
        ordertime = 2018
        self.__portfolio.UpdatePosition(symbol,order_type,quantity,price,direction,ordertime)
    
    def change_weight(self,event):
        symbol = event.symbol
        weight = event.weight
        self.__portfolio.UpdatePosition(symbol,weight)
    
        
def CreateMarketDataAPI():
    return SimulatedMarketDataAPI()

def CreatePositionInfoAPI():
    return SimulatedPositionInfoAPI()

def CreateOrderInfoAPI():
    return None
def CreateExcutionAPI():
    return SimulatedExcutionAPI()


class User_API:
    def __init__(self,market_data_api,position_info_api):
        self._market_data_api = market_data_api
        self._position_info_api = position_info_api
    def RegisterEvents(self,events):
        self._events = events
    def history_bars(self,stock, expected_return_days, period,field):
        return self._market_data_api.history_bars(stock, expected_return_days, period,field)
    def order_target_percent(self,stock, weight):
        self._events.put()
    def GetPositionWeight(self,code):
        pass
    
    def Buy(self,code,price,size):
        pass
    
    def Sell(self,code,price,size):
        pass
    
    def LatestPrice(self,stock):
        pass
    
    def PositionValue(self):
        pass
    
    def now(self):
        return self._market_data_api.now()