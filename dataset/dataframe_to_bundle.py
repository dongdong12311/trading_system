#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 21:50:49 2019

@author: dongdong
"""

'create bundle once the bundle is created the meta can not be changed'

import bcolz
from const import bcolz_data_path,metas,base_data_path
from data_transform import change
import os
import numpy as np
from localfile_to_dataframe import LocalFileToDataFrame

base_data = []
for i in range(len(metas)):
    base_data.append(np.array((),dtype = np.uint32))

"create a table "
data = bcolz.ctable(base_data, rootdir=bcolz_data_path, 
                 mode='w',names = metas)



from localfile_to_dataframe import LocalFileToDataFrame



def add(data,meta,array,code):
    begine_line = len(data[meta])
    last_line = begine_line + array.size - 1
    data.attrs['line_map'].update({code:[begine_line,last_line]})
    

#data = bcolz.open(rootdir=bcolz_data_path)
#data.attrs = {'line_map':{}}
import os
files = os.listdir(base_data_path)
line_map  = {}
begin_line = 0
for file in files:
    print("load" + file)
    a =  LocalFileToDataFrame(os.path.join(base_data_path,file),file)
    code = file
    if a is not None:
        for meta in metas:
            a[meta] = change(a,meta)
            
        for index in a.index:
            data.append(list(a.loc[index]))
        end_line = begin_line + a.index.size - 1
        line_map.update({file:[begin_line,end_line]})
        begin_line = end_line + 1

data.attrs['line_map'] = line_map



