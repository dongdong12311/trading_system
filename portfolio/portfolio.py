#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:46:45 2019

@author: dongdong
"""
from abc import ABCMeta, abstractmethod, abstractproperty
class Portfolio(metaclass=ABCMeta):
    def __init__(self):
        pass
'''    
    @abstractmethod
    def GetDebt(self):
        pass

    @abstractmethod
    def GetAvailableMoney(self):
        pass
    
    @abstractmethod
    def GetTotalMoney(self):
        pass
    
    @abstractmethod
    def GetPositions(self):
        pass
    
    @abstractmethod
    def GetPosition(self,code):
        pass
'''    
class SimulatedPortfolio(Portfolio):
    def __init__(self,initial_capital = 1000.0):
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
    def GetPosition(self,code):
        if code not in self.__positions.keys():
            return None
        return self.__positions[code]
    def AvailableMoney(self):
        return self.__basic['available']
    
    def UpdatePositions(self,dataptr):
        for code in self.__positions.keys():
            
            self.__positions[code][4] += 1
            
            price = dataptr.GetLatestPrice(code)
            if price > 0:       
                size = self.__positions[code][2]
                buyprice = self.__positions[code][1]
                
                self.__positions[code][7] = price * size                  
                
                if self.__positions[code][3]=='B':
                    self.__positions[code][5] = (price - buyprice)/buyprice*100
                elif  self.__positions[code][3]=='RS':
                    self.__positions[code][5] = ( buyprice - price )/buyprice*100
                
                self.__positions[code][6] = price
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
        self.__MinuesStock(symbol,quantity)
        self.__AddMoney(quantity * price)    
        
    def __BuyStock(self,symbol,quantity,price,ordertime):
        self.__GetStock(symbol,quantity,price,'B',ordertime)
        self.__MinuesMoney(price * quantity)
        
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
        pass
def CreateSimulatePortfolio():
    return SimulatedPortfolio()
