# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 22:23:38 2019

@author: Administrator
"""
import datetime
def summarise(res,config):
    port_series = res['sys_analyser']['portfolio']['static_unit_net_value']
    
    summary = {
               'STOCK':config['initial_capital'],
               'alpha':alpha,
               'annualized_returns':1,
               'benchmark_annualized_returns':1,
               'benchmark_total_returns':1,
               'beta':0.1,
               'cash':1,
               'downside_risk':1.1,
               'end_date':datetime.datetime(2017,1,21),
               'information_ratio':1.1,
               'max_drawdown':0.1,
               'run_type':'1',
               'sharpe':1.2,
               'sortino':1.1,
                'start_date':datetime.datetime(2017,1,1),
                'strategy_file':'name',
                'strategy_name':'name',
                'total_returns':1,
                'total_value':12,
                'tracking_error':'123',
                'unit_net_value':.1,
                'units':1,
                'volatility':0.2
            }
    res['sys_analyser']['summary'] = summary       
    return res