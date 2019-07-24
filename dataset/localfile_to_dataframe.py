#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 22:58:44 2019

@author: dongdong
"""
import pandas as pd
from const import base_data_path
def LocalFileToDataFrame(filepath,code):
    try:
        data = pd.read_csv(filepath)
        return data
    except:
        return None
