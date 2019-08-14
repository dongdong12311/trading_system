# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 13:48:20 2019

@author: Administrator
"""

from dataset.converter import StockBarConverter 
from dataset.day_bar_store import DayBarStore
from dataset.base_data_source import BaseDataSource
import datetime
#a = DayBarStore("F:\\bcolz_data\\daily_data",StockBarConverter)
#s = a.get_bars("000001.SZ",['high'])
#temp = a.get_date_range("000001.SZ")

a = BaseDataSource("F:\\data\\bcolz_data")
s = a.history_bars("000001.SZ",10,'1d','close',datetime.datetime(2019,5,30))
s = a.get_trading_calendar(20190102,20191211)
s = a.get_bar("000001.SZ",datetime.datetime(2019,5,30),"1d")

plot_result(res['sys_analyser'])