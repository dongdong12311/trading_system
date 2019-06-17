#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:31:56 2019

@author: dongdong
"""
from abc import abstractmethod
from event.event import OrderEvent
class Strategy:
    def __init__(self):
        pass
    @abstractmethod
    def calculate_signals(self,events):
        raise "no implement error"
        
        
    def RegisterAPI(self,market_data_API,position_info_API,order_info_API):
        self._market_data_API = market_data_API
        self._position_info_API = position_info_API
        self._order_info_API = order_info_API
class MyStrategy(Strategy):
    def __init__(self):
        self.p = 0.0
    def calculate_signals(self,events):
        code = '123'
        self.p = 1
        events.put(OrderEvent(code,1,100,self.p,'B',2018))
        positions = self._position_info_API.GetPosition(code)
        if positions:
            events.put(OrderEvent(code,1,100,self.p ,'S',2018))
        

def CreateStragety():
    return MyStrategy()