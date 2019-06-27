

from api.api import CreateExcutionAPI,CreateMarketDataAPI,CreateOrderInfoAPI,CreatePositionInfoAPI
from event.event import CreateEventQueue
from strategy.strategy import CreateStragety
from excutor.excutor import CreateExcutor
from dataset.dataptr import CreateDataPtr
from dataset.dataset import CreateHistoryDataSet
from portfolio.portfolio import CreateSimulatePortfolio




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
    def Run(self,strategy, excutor, dataptr, portfolio = None):  
        events = CreateEventQueue()
        strategy.ConnectToEventQueue(events)
        while 1:
            res =  engine._Update(events,dataptr,portfolio)
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
                    strategy.calculate_signals()
                # 执行订单
                elif event.type =='ORDER':   
                    excutor.execute_order(event)
                else:
                    raise TypeError    
                    
start = '20180101'
end = '20180131'               
print('init data')     
dataset = CreateHistoryDataSet()
dataset.init(start,end)
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


order_info_API = CreateOrderInfoAPI()


excution_API = CreateExcutionAPI()
excution_API.RegisterSimulatedPortfolio(portfolio)

#_____________strategy_______________
strategy = CreateStragety()
strategy.RegisterAPI(market_data_API,position_info_API,order_info_API)


#_____________excutor_______________
excutor = CreateExcutor()
excutor.RegisterAPI(excution_API)



# ____________engine________________
engine = Engine()
engine.Run(strategy,excutor,dataptr,portfolio)