

from api.api import CreateExcutionAPI,CreateMarketDataAPI,CreateOrderInfoAPI,CreatePositionInfoAPI
from event.event import CreateEventQueue
from strategy.strategy import CreateStragety
from excutor.excutor import CreateExcutor
from dataset.dataptr import CreateDataPtr
from portfolio.portfolio import CreateSimulatePortfolio




class Engine:
    def __init__(self):
        self.__events = CreateEventQueue()
    def init(self,strategy,excutor,dataptr):
        self._RegisterDataPtr(dataptr)
        self._RegisterExcutor(excutor)
        self._RegisterStrategy(strategy)
        
    def _RegisterStrategy(self,strategy):
        self.__strategy = strategy
    def _RegisterExcutor(self,excutor):
        self.__excutor = excutor
    def _RegisterDataPtr(self,dataptr):
        self.__dataptr = dataptr
    def _Update(self,events):
        return self.__dataptr.Update(events)
            
    def Run(self):        
        while 1:
            res =  engine._Update(self.__events)
            if not res:
                break
            while 1:
                # 获取待处理的事件，如果队列空就结束循环
                if  self.__events.qsize() == 0:
                    break
                else:
                    event = self.__events.get(False)
                # 计算信号    
                if event.type == 'MARKET':
                    self.__strategy.calculate_signals(self.__events)
                # 执行订单
                elif event.type =='ORDER':   
                    self.__excutor.execute_order(event)
                else:
                    raise TypeError    
    
# _______________dataset_______________   
dataptr = CreateDataPtr()



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
engine.init(strategy,excutor,dataptr) 
engine.Run()