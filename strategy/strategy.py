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
        pass 
class MyStrategy(Strategy):
    def __init__(self):
        pass
    def calculate_signals(self,events):
        events.put(OrderEvent("123",1,1,1,1))
        
def CreateStragety():
    return MyStrategy()