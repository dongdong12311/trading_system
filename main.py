
from dataset.const import base_path,bcolz_data_path
import os
from ce_lue import init,handle_bar
from engine import Run_func
config = {
            'start':20170109,
            'end':20170630,
            'data_path':os.path.join(base_path,bcolz_data_path),
            'initial_capital':100000,
            'benchmark':'000001.SH'
          }
from plot.plot import plot_result
res = Run_func(init,handle_bar,config)
plot_result(res['sys_analyser'])