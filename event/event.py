# -*- coding: utf-8 -*-
"""
Created on Mon May 21 14:30:55 2018

@author: Administrator
"""

from queue import PriorityQueue
def  CreateEventQueue():
    return PriorityQueue()

class Event(object):
    "定义事件的优先级 中间"
    def __init__(self,priority):
        self.priority = priority
    def __lt__(self,other): 
        return self.priority < other.priority  


class MarketEvent(Event):
    'update data'
    def __init__(self,priority = 5):   
        super().__init__(priority)
        self.type = 'MARKET'
      
        
class SignalEvent(Event):
    'generate signal '
    def __init__(self, symbol, quantity,price,direction,priority = 4):
        super().__init__(priority)
        self.type = 'SIGNAL'
        self.symbol = symbol    
        self.quantity = quantity
        self.price = price
        self.direction = direction
       
    
      
class OrderEvent(Event):
    'generate order'
    def __init__(self, symbol, order_type, quantity,price, direction,priority = 3):  
        """
        Parameters:
        symbol - The instrument to trade.
        order_type - 'MKT' or 'LMT' for Market or Limit.
        quantity - Non-negative integer for quantity.
        direction - 'B' :证券买入 'S' :证券卖出
                    'RB':（融券买券）买券还券 'RS':融券卖出
        """
        super().__init__(priority)
        self.type = 'ORDER'
        self.symbol = symbol
        self.price = price 
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction

    def __str__(self):
        return  ("Order: Symbol=%s, Type=%s, Quantity=%s, Price=%.2f ,Direction=%s" % \
            (self.symbol, self.order_type, self.quantity, self.price, self.direction))
        
        
class TradeResultEvent(Event):
    "市场返回成交的结果"
    def __init__(self, timeindex, symbol, order_type, quantity,price, direction,errorcode,priority = 1):         
        super().__init__(priority)
        self.type = 'TradeResult'
        self.timeindex = timeindex
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.price = price
        self.direction = direction
        self.errorcode = errorcode
    
        
        
        
