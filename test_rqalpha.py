# run_func_demo
from rqalpha.api import *
from rqalpha import run_func


def init(context):
    logger.info("init")
    context.s1 = "000001.XSHE"
    context.s2 = "600232.XSHG"
    update_universe(context.s1)
    update_universe(context.s2)
    context.fired = False


def before_trading(context):
    pass


def handle_bar(context, bar_dict):
    if not context.fired:
        # order_percent并且传入1代表买入该股票并且使其占有投资组合的100%
        order_percent(context.s1, 0.1)
        order_percent(context.s2, 0.1)
        context.fired = True


config = {
  "base": {
    "start_date": "2016-06-01",
    "end_date": "2016-12-01",
    "benchmark": "000300.XSHG",
    "accounts": {
        "stock": 100000
    }
  },
  "extra": {
    "log_level": "verbose",
  },
  "mod": {
    "sys_analyser": {
      "enabled": True,
      "plot": True
    }
  }
}

# 您可以指定您要传递的参数
a = run_func(init=init, before_trading=before_trading, handle_bar=handle_bar, config=config)