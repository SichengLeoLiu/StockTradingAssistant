import pandas as pd
import numpy as np
from datetime import datetime
from pprint import pp

class FundamentalAnalyzer:
    def __init__(self, financial_data, growth_data, industry_data):
        """
        :param financial_data: DataFrame，包含财务数据
        :param growth_data: DataFrame，包含成长数据
        """
        self.financial_data = financial_data
        self.growth_data = growth_data
        self.industry_data = industry_data
    
    def calculate_roe(self, netProfit, equity):
        """
        计算净资产收益率
        :param netProfit: 净利润
        :param equity: 净资产
        :return: 净资产收益率
        """
        return (netProfit / equity) * 100 if equity > 0 else np.nan
    
    def calculate_growth_rate(self, current_value, previous_value):
        """
        计算增长率
        :param current_value: 当期值
        :param previous_value: 上期值
        :return: 增长率
        """
        return ((current_value - previous_value) / abs(previous_value)) * 100 if previous_value != 0 else np.nan
    
    def analyze_financial_health(self):
        """
        分析财务健康状况
        :return: 分析结果字典
        """
        analysis = {}
        # # 计算关键财务指标
        # if 'netProfit' in self.data.columns and 'totalShare' in self.data.columns:
        #     analysis['ROE'] = self.calculate_roe(
        #         float(self.data['netProfit'].iloc[-1]),
        #         float(self.data['totalShare'].iloc[-1])
        #     )
        
        # # 计算增长率
        # if 'netProfit' in self.data.columns and len(self.data) > 1:
        #     analysis['Profit_Growth'] = self.calculate_growth_rate(
        #         float(self.data['netProfit'].iloc[-1]),
        #         float(self.data['netProfit'].iloc[-2])
        #     )
        
        analysis['roeAvg'] = float(self.financial_data['roeAvg'].iloc[-1])
        analysis['npMargin'] = float(self.financial_data['npMargin'].iloc[-1])
        analysis['gpMargin'] = float(self.financial_data['gpMargin'].iloc[-1])
        analysis['netProfit'] = float(self.financial_data['netProfit'].iloc[-1])
        analysis['epsTTM'] = float(self.financial_data['epsTTM'].iloc[-1])
        analysis['MBRevenue'] = float(self.financial_data['MBRevenue'].iloc[-1])
                
                
        analysis['YOYEquity'] = float(self.growth_data['YOYEquity'].iloc[-1])
        analysis['YOYAsset'] = float(self.growth_data['YOYAsset'].iloc[-1])
        analysis['YOYNI'] = float(self.growth_data['YOYNI'].iloc[-1])
        analysis['YOYEPSBasic'] = float(self.growth_data['YOYEPSBasic'].iloc[-1])
        analysis['YOYPNI'] = float(self.growth_data['YOYPNI'].iloc[-1])

        analysis['industry'] = self.industry_data['industry'].iloc[-1]

        return analysis
    
    def get_financial_summary(self):
        """
        生成财务分析摘要
        :return: 分析摘要字符串
        """
        analysis = self.analyze_financial_health()
        summary = []
        if 'industry' in analysis:
            summary.append(f"该股属于{analysis['industry']}行业。")
        
        if 'roeAvg' in analysis:
            summary.append(f"净资产收益率（平均）（%）: {analysis['roeAvg']:.2f}%，")
        if 'npMargin' in analysis:
            summary.append(f"销售净利率（%）: {analysis['npMargin']:.2f}%，")
        if 'gpMargin' in analysis:
            summary.append(f"销售毛利率（%）: {analysis['gpMargin']:.2f}%，")
        if 'netProfit' in analysis:
            summary.append(f"净利润（亿元）: {analysis['netProfit']:.2f}，")
        
        if 'epsTTM' in analysis:
            summary.append(f"每股收益（TTM）: {analysis['epsTTM']:.2f}，")
            
        if 'MBRevenue' in analysis:
            summary.append(f"主营营业收入（元）: {analysis['MBRevenue']:.2f}，")
            
        if 'YOYEquity' in analysis:
            summary.append(f"净资产同比增长率: {analysis['YOYEquity']:.3f}%，")
            
        if 'YOYAsset' in analysis:
            summary.append(f"总资产同比增长率: {analysis['YOYAsset']:.3f}%，")
            
        if 'YOYNI' in analysis:
            summary.append(f"净利润同比增长率: {analysis['YOYNI']:.3f}%，")
            
        if 'YOYEPSBasic' in analysis:
            summary.append(f"基本每股收益同比增长率: {analysis['YOYEPSBasic']:.3f}%，")
            
        if 'YOYPNI' in analysis:
            summary.append(f"归属母公司股东净利润同比增长率: {analysis['YOYPNI']:.3f}%。")
            
        
        
        return "".join(summary) 