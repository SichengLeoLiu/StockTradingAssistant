import pandas as pd
import numpy as np
import talib

class TechnicalAnalyzer:
    def __init__(self, data):
        """
        :param data: DataFrame，包含OHLCV数据
        """
        self.data = data
        # 确保列名是小写的
        self.data.columns = self.data.columns.str.lower()
        self.close = self.data['close'].astype(float)
        self.high = self.data['high'].astype(float)
        self.low = self.data['low'].astype(float)
        self.volume = self.data['volume'].astype(float)
    
    def calculate_moving_averages(self):
        """计算移动平均线"""
        self.data['MA5'] = talib.MA(self.close, timeperiod=5)
        self.data['MA10'] = talib.MA(self.close, timeperiod=10)
        self.data['MA20'] = talib.MA(self.close, timeperiod=20)
        self.data['MA60'] = talib.MA(self.close, timeperiod=60)
        return self.data
    
    def calculate_macd(self):
        """计算MACD指标"""
        macd, signal, hist = talib.MACD(self.close)
        self.data['MACD'] = macd
        self.data['MACD_SIGNAL'] = signal
        self.data['MACD_HIST'] = hist
        return self.data
    
    def calculate_rsi(self):
        """计算RSI指标"""
        self.data['RSI6'] = talib.RSI(self.close, timeperiod=6)
        self.data['RSI12'] = talib.RSI(self.close, timeperiod=12)
        self.data['RSI24'] = talib.RSI(self.close, timeperiod=24)
        return self.data
    
    def calculate_bollinger_bands(self):
        """计算布林带"""
        upper, middle, lower = talib.BBANDS(self.close)
        self.data['BB_UPPER'] = upper
        self.data['BB_MIDDLE'] = middle
        self.data['BB_LOWER'] = lower
        return self.data
    
    def calculate_kdj(self):
        """计算KDJ指标"""
        self.data['K'], self.data['D'] = talib.STOCH(self.high, self.low, self.close)
        self.data['J'] = 3 * self.data['K'] - 2 * self.data['D']
        return self.data
    
    def calculate_all_indicators(self):
        """计算所有技术指标"""
        self.calculate_moving_averages()
        self.calculate_macd()
        self.calculate_rsi()
        self.calculate_bollinger_bands()
        self.calculate_kdj()
        self.calculate_cci()
        self.calculate_dmi()
        self.calculate_obv()
        self.calculate_vr()
        self.calculate_williams_r()
        return self.data
    
    def calculate_cci(self):
        """计算顺势指标(CCI)"""
        self.data['CCI'] = talib.CCI(self.high, self.low, self.close, timeperiod=14)
        return self.data
    
    def calculate_dmi(self):
        """计算动向指标(DMI)"""
        self.data['PLUS_DI'] = talib.PLUS_DI(self.high, self.low, self.close, timeperiod=14)
        self.data['MINUS_DI'] = talib.MINUS_DI(self.high, self.low, self.close, timeperiod=14)
        self.data['ADX'] = talib.ADX(self.high, self.low, self.close, timeperiod=14)
        return self.data
    
    def calculate_obv(self):
        """计算能量潮指标(OBV)"""
        self.data['OBV'] = talib.OBV(self.close, self.volume)
        return self.data
    
    def calculate_vr(self):
        """计算成交量比率(VR)"""
        close_diff = self.close.diff()
        up_volume = self.volume.where(close_diff > 0, 0)
        down_volume = self.volume.where(close_diff < 0, 0)
        self.data['VR'] = (up_volume.rolling(26).sum() / down_volume.rolling(26).sum()) * 100
        return self.data
    
    def calculate_williams_r(self):
        """计算威廉指标(%R)"""
        self.data['WILLR'] = talib.WILLR(self.high, self.low, self.close, timeperiod=14)
        return self.data
    
    def get_technical_signals(self):
        """获取技术指标信号"""
        signals = {}
        
        # MACD信号
        if self.data['MACD'].iloc[-1] > self.data['MACD_SIGNAL'].iloc[-1]:
            signals['MACD'] = '买入'
        else:
            signals['MACD'] = '卖出'
            
        # RSI信号
        rsi = self.data['RSI14'].iloc[-1]
        if rsi > 70:
            signals['RSI'] = '超买'
        elif rsi < 30:
            signals['RSI'] = '超卖'
        else:
            signals['RSI'] = '中性'
            
        # 布林带信号
        close = self.data['close'].iloc[-1]
        if close > self.data['BB_UPPER'].iloc[-1]:
            signals['BB'] = '超买'
        elif close < self.data['BB_LOWER'].iloc[-1]:
            signals['BB'] = '超卖'
        else:
            signals['BB'] = '中性'
            
        # KDJ信号
        if (self.data['K'].iloc[-1] > self.data['D'].iloc[-1] and 
            self.data['K'].iloc[-2] <= self.data['D'].iloc[-2]):
            signals['KDJ'] = '金叉'
        elif (self.data['K'].iloc[-1] < self.data['D'].iloc[-1] and 
              self.data['K'].iloc[-2] >= self.data['D'].iloc[-2]):
            signals['KDJ'] = '死叉'
        else:
            signals['KDJ'] = '中性'
            
        # CCI信号
        cci = self.data['CCI'].iloc[-1]
        if cci > 100:
            signals['CCI'] = '超买'
        elif cci < -100:
            signals['CCI'] = '超卖'
        else:
            signals['CCI'] = '中性'
            
        # DMI信号
        if (self.data['PLUS_DI'].iloc[-1] > self.data['MINUS_DI'].iloc[-1] and 
            self.data['ADX'].iloc[-1] > 25):
            signals['DMI'] = '强势上涨'
        elif (self.data['PLUS_DI'].iloc[-1] < self.data['MINUS_DI'].iloc[-1] and 
              self.data['ADX'].iloc[-1] > 25):
            signals['DMI'] = '强势下跌'
        else:
            signals['DMI'] = '盘整'
            
        return signals