.. _intro-tutorial:

====================
教程：均值方差模型
====================

------------------------------------------------------

CNICPortfolio 抽离了策略框架的所有技术细节，以API的方式提供给策略研发者用于编写策略，从而避免陷入过多的技术细节，而非金融程序建模本身。

------------------------------------------------------
------------------------------------------------------
本教程以均值方差模型为例，介绍如何在我们的平台上运行一个投资组合策略

在进行回测的过程中需要明确以下几个回测要素，下面的参数是必须的：

*   策略文件
*   回测起始时间
*   回测结束时间
*   起始资金
*   Benchmark



策略编写流程


首先构造投资组合的调仓日期，假设每20天调仓一次


.. code-block:: python3


    import datetime
    import pandas as pd
    from pypfopt.efficient_frontier import EfficientFrontier
    from pypfopt import risk_models
    from pypfopt import expected_returns
    from trading_system.api.api import get_calendar
    cal = get_calendar()
    start = 20150101
    end = 20151212
    dates = cal.sessions_in_range(start, end)

    #我们假定 每20天调仓一次
    balance_dates = []
    for i in range(len(dates)):
        if i%20== 0:
            balance_dates.append(dates[i].date())
            
定义我们的股票池

.. code-block:: python3
    
    STOCKS = ['000001.SZ','000002.SZ','000004.SZ','000005.SZ','000006.SZ','000007.SZ',
          '000008.SZ','000009.SZ','000010.SZ']

定义一些必要的参数

.. code-block:: python3
          
    #利用多久的数据估算
    expected_return_days = 100 
    
    #如何估算协方差矩阵
    cov_method = 'sample'  
    
    #优化方法
    optimization_criterion = 'max_sharpe'
    
    cleaned_weights = True
    
    balance_dates = balance_dates
    
    #预期收益率预期风险
    target_return = 0.2

    target_risk   = 0.1
    
    #无风险利率
    risk_free_rate = 0.02   
    
CNICPortfolio 的 API 主要分为三类：约定函数、数据查询和交易接口。

*   约定函数: 作为 API 的入口函数，用户必须实现对应的约定函数才可以正确的使用 CNICPortfolio

    *   :func:`init` : 初始化方法，会在程序启动的时候执行
    *   :func:`handle_bar`: bar数据更新时会自动触发调用

.. code-block:: python3
        
    def initialize(context):
        context.stocks = STOCKS
        context.expected_return_days = expected_return_days
        context.opt_criterion = optimization_criterion
        context.tick  = 0
        context.balance_dates = balance_dates
        context.cleaned_weights = cleaned_weights
        context.cov_method = cov_method
        context.target_return = target_return    
        context.targe_risk = target_risk
        context.risk_free_rate = risk_free_rate
    
        print('initialized!')    
    def handle_data(context, data):
        date = data.today()
        if date in context.balance_dates:
            temp = {}
            for code in context.stocks:
                history_price = data.history_bars(code,
                                                  context.expected_return_days,
                                                  '1d','close')
                if history_price is not None:     
                    temp.update({code:history_price})
            history_prices = pd.DataFrame(temp)
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
            
            weight = []
            prices = []
            for code in context.stocks:
                weight.append(weights[code])
                prices.append(data.latest_price(code,"1d"))
            
            data.order_target_percent(context.stocks, weight,prices)    
    


至此，我们写出了一个均值方差模型









