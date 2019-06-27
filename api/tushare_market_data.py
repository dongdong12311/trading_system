#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 11:30:16 2019

@author: dongdong
"""

import tushare as ts
ts.set_token('f867cf1c65e806c64096d26d7f7ea70db0c38bddb027c034f20c64de')
pro = ts.pro_api()
data = pro.query('trade_cal', start_date='20180101', end_date='20181231')
