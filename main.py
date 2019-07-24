

from api.api import CreateExcutionAPI,CreateMarketDataAPI,CreateOrderInfoAPI,CreatePositionInfoAPI,User_API
from event.event import CreateEventQueue
from strategy.strategy import CreateStragety
from excutor.excutor import CreateExcutor
from dataset.dataptr import CreateDataPtr
from dataset.dataset import CreateHistoryDataSet
from portfolio.portfolio import CreateSimulatePortfolio
class Context:
    def __init__(self):
        pass


class Handler():
    def __init__(self,events):
        self.events = events
        
    
class Engine:
    def __init__(self):
        pass
        
        
    def __UpdateSimulatedData(self,events,dataptr,portfolio):
        portfolio.ShowPosition()
        if  dataptr.Update(events):
            portfolio.UpdatePositions(dataptr)
            return True
        return False
        
    def __UpdateRealData(self,events,dataptr):
        return  False
    
    def _Update(self,events,dataptr, portfolio = None):
        
        return self.__UpdateSimulatedData(events,dataptr,portfolio)
        '''
        
        return self.__UpdateRealData(events,dataptr)
        
        '''    
    def Run(self,init,handle_bar,api,excutor,dataptr,portfolio = None):  
        context = Context()
        init(context)
        
        events = CreateEventQueue()
        api.RegisterEvents(events)
        while 1:
            res =  self._Update(events,dataptr,portfolio)
            if not res:
                break
            while 1:
                # 获取待处理的事件，如果队列空就结束循环
                if  events.qsize() == 0:
                    break
                else:
                    event = events.get(False)
                # 计算信号    
                if event.type == 'MARKET':
                    handle_bar(context,api)
                # 执行订单
                elif event.type =='ORDER':   
                    excutor.execute_order(event)
                    
                elif event.type =='CHANGE_WEIGHT':   
                    excutor.change_weight(event)
                else:
                    raise TypeError    


def Run(init,handle_bar,config):                    
    start = config['start']
    end = config['end']            
    print('init data')     
    dataset = CreateHistoryDataSet()
    dataset.init(start,end,config['data_path'])
    print('done')
    # _______________dataset_______________   
    dataptr = CreateDataPtr(dataset)
    # ____________portfolio________________
    portfolio = CreateSimulatePortfolio() 
    #_____________apply api________________
          
    market_data_API = CreateMarketDataAPI()
    market_data_API.RegisterDataPtr(dataptr)
    
    
    position_info_API = CreatePositionInfoAPI()
    position_info_API.RegisterPortfolio(portfolio)
    
    'simulated trading do not need order info api'
    #order_info_API = CreateOrderInfoAPI()
    
    
    excution_API = CreateExcutionAPI()
    excution_API.RegisterSimulatedPortfolio(portfolio)
    
    api  = User_API(market_data_API,position_info_API)
    
    #_____________excutor_______________
    excutor = CreateExcutor()
    excutor.RegisterAPI(excution_API)
            
    # ____________engine________________
    engine = Engine()
    engine.Run(init,handle_bar,api,excutor,dataptr,portfolio)
    
from ce_lue import init,handle_bar

config = {
            'start':20160101,
            'end':20161232,
            'data_path':'/home/dongdong/python_project/tushare_database/bcolz_data/daily_data'
          }
Run(init,handle_bar,config)