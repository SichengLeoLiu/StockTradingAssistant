import baostock as bs
import pandas as pd
from datetime import datetime, timedelta

class StockDataFetcher:
    def __init__(self):
        self.lg = bs.login()
    
    def __del__(self):
        try:
            bs.logout()
        except Exception as e:
            pass
            # print(f"登出失败，错误信息：{e}")
    
    def get_stock_data(self, code, start_date, end_date=None):
        """
        获取股票日线数据
        :param code: 股票代码，格式如：sh.600000
        :param start_date: 开始日期，格式：YYYY-MM-DD
        :param end_date: 结束日期，格式：YYYY-MM-DD，默认为今天
        :return: DataFrame
        """
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        # 确保股票代码格式正确
        code = code.strip()
        if not code.startswith(('sh.', 'sz.')):
            code = 'sh.' + code
        if len(code.split('.')[1]) < 6:
            code = code.split('.')[0] + '.' + code.split('.')[1].zfill(6)
        # 只保留股票代码前9位
        code = code[:9]
        rs = bs.query_history_k_data_plus(
            code,
            "date,code,open,high,low,close,volume,amount,adjustflag",
            start_date=start_date,
            end_date=end_date,
            frequency="d",
            adjustflag="3"  # 复权类型，3：后复权
        )
        
        if rs.error_code != '0':
            print(f"获取数据失败，错误代码：{rs.error_code}，错误信息：{rs.error_msg}")
            return pd.DataFrame()
            
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
            
        if not data_list:
            print("未获取到数据")
            return pd.DataFrame()
            
        return pd.DataFrame(data_list, columns=rs.fields)
    
    def get_stock_basic_info(self, code):
        """
        获取股票基本信息
        :param code: 股票代码
        :return: DataFrame
        """
        # 确保股票代码格式正确
        code = code.strip()
        code = code[:9]
        if not code.startswith(('sh.', 'sz.')):
            code = 'sh.' + code
        if len(code.split('.')[1]) < 6:
            code = code.split('.')[0] + '.' + code.split('.')[1].zfill(6)
            
        rs = bs.query_stock_basic(code=code)
        if rs.error_code != '0':
            print(f"获取基本信息失败，错误代码：{rs.error_code}，错误信息：{rs.error_msg}")
            return pd.DataFrame()
            
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        return pd.DataFrame(data_list, columns=rs.fields)
    
    def get_financial_data(self, code, year=2024, quarter=4):
        """
        获取财务数据
        :param code: 股票代码
        :param year: 年份
        :param quarter: 季度
        :return: DataFrame
        """
        # 确保股票代码格式正确
        code = code.strip()
        code = code[:9]
        if not code.startswith(('sh.', 'sz.')):
            code = 'sh.' + code
        if len(code.split('.')[1]) < 6:
            code = code.split('.')[0] + '.' + code.split('.')[1].zfill(6)
            
        rs = bs.query_profit_data(code=code, year=year, quarter=quarter)
        if rs.error_code != '0':
            print(f"获取财务数据失败，错误代码：{rs.error_code}，错误信息：{rs.error_msg}")
            return pd.DataFrame()
            
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        return pd.DataFrame(data_list, columns=rs.fields) 
    
    def get_growth_data(self, code, year=2024, quarter=4):
        """
        获取成长数据
        :param code: 股票代码
        :param year: 年份
        :param quarter: 季度
        :return: DataFrame
        """
        # 确保股票代码格式正确
        code = code.strip()
        code = code[:9]
        if not code.startswith(('sh.', 'sz.')):
            code = 'sh.' + code
        if len(code.split('.')[1]) < 6:
            code = code.split('.')[0] + '.' + code.split('.')[1].zfill(6)
            
        rs = bs.query_growth_data(code=code, year=year, quarter=quarter)
        if rs.error_code != '0':
            print(f"获取成长数据失败，错误代码：{rs.error_code}，错误信息：{rs.error_msg}")
            return pd.DataFrame()
        
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        return pd.DataFrame(data_list, columns=rs.fields)
    
    def get_stock_industry_data(self, code):
        """
        获取股票行业数据
        :param code: 股票代码
        :param year: 年份
        :param quarter: 季度
        :return: DataFrame
        """     
        code = code.strip()
        code = code[:9]
        if not code.startswith(('sh.', 'sz.')):
            code = 'sh.' + code
        if len(code.split('.')[1]) < 6:
            code = code.split('.')[0] + '.' + code.split('.')[1].zfill(6)
            
        rs = bs.query_stock_industry(code=code)
        if rs.error_code != '0':
            print(f"获取行业数据失败，错误代码：{rs.error_code}，错误信息：{rs.error_msg}")
            return pd.DataFrame()
        
        data_list = []
        while (rs.error_code == '0') & rs.next():   
            data_list.append(rs.get_row_data())
        return pd.DataFrame(data_list, columns=rs.fields)

