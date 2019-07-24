#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 13:49:27 2019

@author: dongdong
"""

'update data'
from const import *
import numpy as np
import pandas as pd
from ts_api import pro
def Update(file_paths,code):
    global pro
    data = pd.read_csv(file_paths,dtype = {TRADE_DATE:str})
    if len(data[TRADE_DATE]):    
        date = data[TRADE_DATE][-1:].values[0]
    else:
        date = ''

    try:    
        df = pro.query('daily', ts_code=code, start_date=date, end_date='')
    except Exception as e:
        print(e)
        return 
        
    'drop start date'
    df.insert(0,TRADE_DATE,df['trade_date'])
    df = df.drop(len(df[TRADE_DATE])-1)
    df = df.sort_values(by=TRADE_DATE)
    
    print('update' + code + 'from' + df[TRADE_DATE][0] + 'to'+ df[TRADE_DATE][-1:] )
    'contact two csv file'
    listed_meta = list(metas)
    res = pd.concat([data,df[listed_meta]],axis=0,ignore_index=True)
    res.to_csv(file_paths,index = False,columns = listed_meta)
    
