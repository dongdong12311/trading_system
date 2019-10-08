#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 11:56:45 2019

@author: dongdong
"""
class Arg:
    def __init__(self):
        pass
    

arg = Arg()

arg.stragety = 'sample_markowitz'
arg.start = 20180101
arg.end = 20181230
arg.initial_capital = 1000000
arg.benchmark = '000001.SH'
class Test:
    def __init__(self,config):
        names = self.__dict__
        for key in config.keys():
            names[key] = config[key]
config = {
            'start':arg.start,
            'end':arg.end,
            'initial_capital':arg.initial_capital,
            'benchmark':arg.benchmark
          }
a = Test(config)


