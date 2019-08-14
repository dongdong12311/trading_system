

from ce_lue import init,handle_bar
from engine import Run_func
config = {
            'start':20170109,
            'end':20170630,
            'data_path':'F:\\data\\bcolz_data',
            'initial_capital':100000
          }
from plot.plot_func import plot_result
if __name__ == '__main__':
    res = Run_func(init,handle_bar,config)
   