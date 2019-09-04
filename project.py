#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 16:14:54 2019

@author: dongdong
"""

#输入一段时间资产净值序列  按要求返回 结果



#输入实例  
import pandas as pd
series1 = pd.Series([1,1.01,1.02,1.005,0.99,0.95])

series2 =  pd.Series([1,0.99,1.01,1.035,0.99,0.95])
# 均值
def _mean(series1):
	return series1.mean()

# 方差
def _var(serires2):
	....

# 总收益率
def _total_returns(series1):
	...


# 年化收益率
def _annualized_returns(series1,period = '1d'):
	#period 表示我们序列的周期 默认为每一天
	if period == '1d':
		...

# downside_risk 最大回撤
def _downside_risk(series1):
	...



# beta  
#series1 是投资组合净值  series2 是市场收益净值
def _beta(series1,series2):
	
	


#  alpha


# sharpe 夏普比率 series1 是投资组合净值  series2 是市场收益净值
def _sharpe(series1,series2):
    


