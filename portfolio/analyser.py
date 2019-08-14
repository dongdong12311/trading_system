# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 16:39:16 2019

@author: Administrator
"""
import datetime
import pandas as pd

    
class TradeStatic:
    def __init__(self,trade_date,cash,market_value,static_unit_net_value,
                 total_value,unit_net_value,units):
        self.trade_date = trade_date
        self.cash = cash
        self.market_value = market_value
        self.static_unit_net_value = static_unit_net_value
        self.total_value = total_value
        self.units = units
        self.unit_net_value = unit_net_value
class Analyser:
    def __init__(self):
        self.res = {'sys_analyser':
            {
                 'portfolio':{},
                'positions':{},
                'summary':{}
            }
            }
        self._trade_statics = []
        self._positions = {}

    def _transform(self):
        self.res['sys_analyser']['positions'] = self._positions
        temp =  pd.DataFrame(self._trade_statics,columns =
                         ['trade_date','cash', 'market_value', 'static_unit_net_value', 'total_value',
       'unit_net_value', 'units'])
        temp.index = temp['trade_date']
        self.res['sys_analyser']['portfolio'] = temp
    def append_position(self,trade_date,position):
        self._positions.update({ trade_date : position })
    def append_static(self,trade_static):
        self._trade_statics.append([trade_static.trade_date,trade_static.cash,
                                    trade_static.market_value,
                                    trade_static.static_unit_net_value,
                                    trade_static.total_value,
                                    trade_static.unit_net_value,
                                    trade_static.units
                                    ])
    
    
    def get_result(self):
        self._transform()
        return self.res