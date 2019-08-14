#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:46:45 2019

@author: dongdong
"""
from abc import ABCMeta, abstractmethod, abstractproperty
from .analyser import Analyser,TradeStatic
class Portfolio(metaclass=ABCMeta):
    def __init__(self):
        pass
class SimulatedPortfolio(Portfolio):
    def __init__(self,initial_capital = 1000000.0):
        self._log = []
        self.initial_capital = initial_capital
        self.__money = initial_capital
        self.__basic ={'available':self.__money,'debt':0,'total_money':self.__money}
        self.__positions={}
        self.__position_names={}
        self.__position_names['code']=['购买日期','购买价格',
    		               '购买数量','交易方向','持仓时间（天）',
    		               '盈亏比例','现价','市值']        
        '''
        code       [0]date [1]price [2]amount  [3]tradeside 
        股票代码  购买日期  购买价格  购买数量   交易方向   
        [4]inposition_day     [5]rate      [6]now_price     [7]value                          
        持仓时间（天）         盈亏比例       现价            市值
        '''
        
        "分析器"
        self._analyser = Analyser()
    def GetPosition(self,code):
        if code not in self.__positions.keys():
            return None
        return self.__positions[code]
    def GetPositions(self):
        res = []
        for i in self.__positions.keys():
            res.append({i:self.__positions[i]})
        return res
    def AvailableMoney(self):
        return self.__basic['available']
    
    def UpdatePositions(self,dataptr):
        #self._log.append([self.AvailableMoney(),self.GetPositions()])

        for code in self.__positions.keys():
            
            self.__positions[code][4] += 1
            
            price = dataptr.latest_price(code,"1d")
            if price :       
                size = self.__positions[code][2]
                buyprice = self.__positions[code][1]
                
                self.__positions[code][7] = price * size                  
                
                if self.__positions[code][3]=='B':
                    self.__positions[code][5] = (price - buyprice)/buyprice*100
                elif  self.__positions[code][3]=='RS':
                    self.__positions[code][5] = ( buyprice - price )/buyprice*100
                
                self.__positions[code][6] = price
        _date = dataptr.now()
        _position = self.GetPositions()
        self._analyser.append_position(_date,_position)
        money = self.AvailableMoney()
        market_value = self.MarketValue()
        total_value = market_value + money
        static_unit_net_value = total_value/self.initial_capital
        trade_static = TradeStatic(_date,money,market_value,static_unit_net_value,total_value,static_unit_net_value,static_unit_net_value)
        self._analyser.append_static(trade_static)
    def MarketValue(self):
        res = 0
        for i in self.__positions.keys():
            res += self.__positions[i][7]
        return res
    def __GetStock(self,symbol,quantity,price,direction,ordertime):      
        "得到证券"
        if  symbol not in self.__positions.keys() or self.__positions[symbol][2] == 0:
            self.__positions[symbol]=[ordertime, price,quantity, direction, 0,0.0, price,price * quantity]
            return 
        
        original_price = self.__positions[symbol][1]
        original_size = self.__positions[ symbol][2]
        "价格是加权平均"
        self.__positions[symbol][1] =(original_price*original_size+ price* quantity)/(quantity+original_size) 

        "数量增加"
        self.__positions[symbol][2] +=  quantity 
        "市值"
        self.__positions[symbol][7] = price * self.__positions[symbol][2] 
        
    def __getAmount(self,code):
        "查询股票数量"
        if code not in self.__positions.keys():
            return 0
        return self.__positions[code][2]
        
    def __CheckMoney(self,require):
        return  self.AvailableMoney() >= require
    
    def __CheckStock(self,code,require):
        return  self.__getAmount(code) >= require
    
    def __AddMoney(self,money):
        self.__basic['available'] += money
    def __MinuesMoney(self,money):
        self.__basic['available'] -= money
        
    def __MinuesStock(self,symbol,quantity):
        self.__positions[symbol][2] -= quantity
        self.__positions[symbol][7] 
        if (self.__positions[symbol][2] == 0):
            del self.__positions[symbol]
        else:
          self.__positions[symbol][7]  = self.__positions[symbol][2] *self.__positions[symbol][6]
    def __SellStock(self,symbol,quantity,price,ordertime):
        self._log.append(self.AvailableMoney())
        self.__MinuesStock(symbol,quantity)
        self.__AddMoney(quantity * price)    
        self._log.append("sell" + symbol + " "+ str(quantity) + " " +str(price))
        self._log.append(self.AvailableMoney())
    def __BuyStock(self,symbol,quantity,price,ordertime):
        self._log.append(self.AvailableMoney())
        self.__GetStock(symbol,quantity,price,'B',ordertime)
        self.__MinuesMoney(price * quantity)
        self._log.append("buy" + symbol + " "+ str(quantity) + " " +str(price))
    def UpdatePosition(self,symbol,order_type,quantity,price,direction,ordertime):
        if direction == 'S':
            if self.__CheckStock(symbol,quantity):
                self.__SellStock(symbol,quantity,price,ordertime)
        elif direction == 'B':
            if self.__CheckMoney(quantity * price):
                self.__BuyStock(symbol,quantity,price,ordertime)
        else:
            raise "Unknown order"                
    def ShowPosition(self):
        #self._log.append(self.GetPositions())
        pass
    def _ClearALL(self,ordertime):
        positions = []
        prices= []
        quantitys = []
        codes = []
        for code  in self.__positions.keys():
            codes.append(code)
            position = self.GetPosition(code)
            positions.append(position)
            prices.append(position[6])
            quantitys.append(position[2])
        for i  in range(len(positions)):
            self.__SellStock(codes[i],quantitys[i],prices[i],ordertime)
    
    def UpdatePortfolio(self,stocks,weights,prices,ordertime):
        #self._log.append([self.AvailableMoney(),self.GetPositions()])

        self._ClearALL(ordertime)

        money = self.AvailableMoney()
        size = []
        for  i in range(len(weights)):
            if weights[i]:
                if prices[i]:
                    size = int( money*weights[i]/prices[i] /100)*100
                    self.__BuyStock(stocks[i],size,prices[i],ordertime)
    def get_log(self):
        return self._analyser.get_result()
def CreateSimulatePortfolio(initial_capital):
    return SimulatedPortfolio(initial_capital)
