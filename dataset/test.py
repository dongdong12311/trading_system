# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 13:48:20 2019

@author: Administrator
"""

from converter import StockBarConverter 
from day_bar_store import DayBarStore
from base_data_source import BaseDataSource
import datetime
#a = DayBarStore("F:\\bcolz_data\\daily_data",StockBarConverter)
#s = a.get_bars("000001.SZ",['high'])
#temp = a.get_date_range("000001.SZ")

a = BaseDataSource("F:\\bcolz_data")
s = a.history_bars("000001.SZ",10,'1d','close',datetime.datetime(2019,6,1))