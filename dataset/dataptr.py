#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:41:39 2019

@author: dongdong
"""

from event.event import MarketEvent
class DataPtr:
    def __init__(self):
        self.ind = 0
    def Update(self,events):
        self.ind += 1
        if self.ind < 10:
           events.put(MarketEvent())
           return True
        return False
    
def CreateDataPtr():
    return DataPtr()