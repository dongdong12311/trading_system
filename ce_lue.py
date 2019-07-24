#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 21:50:39 2019

@author: dongdong
"""


import datetime

import pandas as pd
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns  
        
        
target_return = 0.15
target_risk   = 0.1
risk_free_rate = 0.02

expected_return_days = 100 #利用多久的数据估算
cov_method = 'sample' #如何估算协方差矩阵
optimization_criterion = 'max_sharpe' #优化方法
cleaned_weights = True
stocks = ["000001.SZ", "000002.SZ","000004.SZ","000005.SZ",
          "000007.SZ","000009.SZ"]

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    context.stocks = stocks
    context.expected_return_days = expected_return_days
    context.opt_criterion = optimization_criterion
    context.tick  = 0
    context.balance_dates = [datetime.datetime(2016, 6, 1, 0, 0),datetime.datetime(2016, 6, 7, 0, 0)]
    context.cleaned_weights = cleaned_weights
    context.cov_method = cov_method
    context.target_return = target_return
    
    context.targe_risk = target_risk
    context.risk_free_rate = risk_free_rate
    #context.s1 = "000001.XSHE"
    # 是否已发送了order
    context.fired = False
    

def handle_bar(context, api):

    date = api.now()
    print(date)
    #if date in context.balance_dates:
    history_prices = {}
    for stock in context.stocks:
        history_price = api.history_bars(stock, context.expected_return_days, '1d','close')
        print(history_price)
        history_prices.update({stock:history_price})
    history_prices = pd.DataFrame(history_prices)
    mu = expected_returns.mean_historical_return(history_prices)
    if context.cov_method == 'sample':
        S = risk_models.sample_cov(history_prices)
    elif context.cov_method == 'semi':
        S = risk_models.semicovariance(history_prices)
    elif context.cov_method == 'exp_cov':
        S = risk_models.exp_cov(history_prices)
        
    ef = EfficientFrontier(mu, S)
    
    if context.opt_criterion == 'max_sharpe':
        weights = ef.max_sharpe()
    elif context.opt_criterion == 'efficient_return':
        weights = ef.efficient_return(context.target_return)
    elif context.opt_criterion == 'efficient_risk':
        weights = ef.efficient_risk(context.targe_risk, context.risk_free_rate)
    elif context.opt_criterion == 'min_volatility':
        weights = ef.min_volatility()
    
    if context.cleaned_weights is True:
        weights = ef.clean_weights()
    
    for stock in context.stocks:
        weight = weights[stock]
        api.order_target_percent(stock, weight)   
    
