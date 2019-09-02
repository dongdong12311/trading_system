.. _intro-examples:

==========================================
策略示例
==========================================



在下面我们列举一些常用的投资组合策略，您可以通过我们的平台运行

.. _intro-examples-buy-and-hold:

第一个策略-买入&持有
------------------------------------------------------

这是一个最简单的策略：在某一段时间每次增加10%的仓位一直到期末

..  code-block:: python3
    :linenos:

    # 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
    stocks = ["000001.SZ", "000002.SZ"]
    
    # 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
    def init(context):
        context.stocks = stocks
    
    def handle_bar(context, api):
        prices = []
        # buy 10% everyday 
        weights = [0.1,0.1]
        for stock in context.stocks:
            prices.append(api.latest_price(stock,"1d"))
        api.order_target_percent(stocks,weights,prices)   




.. _intro-examples-Markowitz均值方差模型  :

Markowitz均值方差模型
------------------------------------------------------

以下是一个我们引入pyfolio编写的Markowitz均值方差模型：

..  code-block:: python3

    import datetime
    from trading_system.api.api import get_calendar
    cal = get_calendar()
    start = 20150101
    end = 20151212
    dates = cal.sessions_in_range(start, end)
    
    balance_dates = []
    for i in range(len(dates)):
        if i%20== 0:
            balance_dates.append(dates[i].date())
            
    STOCKS = ['000001.SZ','000002.SZ','000004.SZ','000005.SZ','000006.SZ','000007.SZ',
              '000008.SZ','000009.SZ','000010.SZ']
    expected_return_days = 100 #利用多久的数据估算
    cov_method = 'sample' #如何估算协方差矩阵
    optimization_criterion = 'max_sharpe' #优化方法
    cleaned_weights = True
    
    balance_dates = balance_dates
    
    target_return = 0.2
    target_risk   = 0.1
    risk_free_rate = 0.02    
    
    from pypfopt.efficient_frontier import EfficientFrontier
    from pypfopt import risk_models
    from pypfopt import expected_returns
    
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
        
    import pandas as pd
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
    

条件在险价值（CVAR）模型
------------------------------------------------------

以下是一个我们引入pyfolio编写的CVAR均值方差模型：

..  code-block:: python3

    from pypfopt import value_at_risk,hierarchical_risk_parity
    from trading_system.dataset.base_data_source import BaseDataSource
    from trading_system.dataset.const  import base_path,bcolz_data_path
    import os
    import pandas as pd
    import datetime
    from trading_system.api.api import get_calendar
    cal = get_calendar()
    start = 20150101
    end = 20151212
    dates = cal.sessions_in_range(start, end)
    
    balance_dates = []
    for i in range(len(dates)):
        if i%20== 0:
            balance_dates.append(dates[i].date())
            
    STOCKS = ['000001.SZ','000002.SZ','000004.SZ','000005.SZ','000006.SZ','000007.SZ',
              '000008.SZ','000009.SZ','000010.SZ']
    
    risk_free_rate = 0.02   
    cleaned_weights = True
    expected_return_days = 100 #利用多久的数据估算
    def initialize(context):
        context.stocks = STOCKS
    
        context.expected_return_days = expected_return_days
    
        context.tick  = 0
        context.balance_dates = balance_dates
        context.cleaned_weights = cleaned_weights
        context.risk_free_rate = risk_free_rate
    
        print('initialized!')
    import pandas as pd
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
            model = value_at_risk.CVAROpt(history_prices.pct_change().dropna())
            weights = model.min_cvar()
            weight = []
            prices = []
            for code in context.stocks:
                weight.append(weights[code])
                prices.append(data.latest_price(code,"1d"))
            data.order_target_percent(context.stocks, weight,prices)    

等级风险平价（HPR）模型
------------------------------------------------------

..  code-block:: python3   
    
    from pypfopt import value_at_risk,hierarchical_risk_parity
    from trading_system.dataset.base_data_source import BaseDataSource
    from trading_system.dataset.const  import base_path,bcolz_data_path
    import os
    import pandas as pd
    import datetime
    from trading_system.api.api import get_calendar
    cal = get_calendar()
    start = 20150101
    end = 20151212
    dates = cal.sessions_in_range(start, end)
    
    balance_dates = []
    for i in range(len(dates)):
        if i%20== 0:
            balance_dates.append(dates[i].date())
            
    STOCKS = ['000001.SZ','000002.SZ','000004.SZ','000005.SZ','000006.SZ','000007.SZ',
              '000008.SZ','000009.SZ','000010.SZ']
    
    risk_free_rate = 0.02   
    cleaned_weights = True
    expected_return_days = 100 #利用多久的数据估算
    def initialize(context):
        context.stocks = STOCKS
    
        context.expected_return_days = expected_return_days
    
        context.tick  = 0
        context.balance_dates = balance_dates
        context.cleaned_weights = cleaned_weights
        context.risk_free_rate = risk_free_rate
    
        print('initialized!')
    import pandas as pd
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
            model = hierarchical_risk_parity.HRPOpt(history_prices.pct_change().dropna())
            weights = model.hrp_portfolio()
            weight = []
            prices = []
            for code in context.stocks:
                weight.append(weights[code])
                prices.append(data.latest_price(code,"1d"))
            data.order_target_percent(context.stocks, weight,prices)    




 