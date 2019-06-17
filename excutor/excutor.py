#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:37:13 2019

@author: dongdong
"""

class Excutor:
    def __init__(self):
        pass
    def RegisterAPI(self,excution_API):
        self._excution_API = excution_API
    def execute_order(self,orderevent):
        self._excution_API.execute_order(orderevent)
def CreateExcutor():
    return Excutor()