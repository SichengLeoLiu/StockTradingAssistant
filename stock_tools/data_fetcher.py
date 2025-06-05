import baostock as bs
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Callable

class StockDataFetcher:
    def __init__(self):
        self.lg = bs.login()
    
    def __del__(self):
        try:
            bs.logout()
        except Exception:
            pass

    def _format_stock_code(self, code: str) -> str:
        """
        格式化股票代码
        :param code: 原始股票代码
        :return: 格式化后的股票代码
        """
        code = code.strip()[:9]
        if not code.startswith(('sh.', 'sz.')):
            code = 'sh.' + code
        if len(code.split('.')[1]) < 6:
            code = code.split('.')[0] + '.' + code.split('.')[1].zfill(6)
        return code

    def _fetch_data(self, query_func: Callable, error_msg: str, **kwargs) -> pd.DataFrame:
        """
        通用数据获取方法
        :param query_func: 查询函数
        :param error_msg: 错误信息前缀
        :param kwargs: 查询参数
        :return: DataFrame
        """
        rs = query_func(**kwargs)
        if rs.error_code != '0':
            print(f"{error_msg}，错误代码：{rs.error_code}，错误信息：{rs.error_msg}")
            return pd.DataFrame()
            
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
            
        return pd.DataFrame(data_list, columns=rs.fields) if data_list else pd.DataFrame()

    def get_stock_data(self, code: str, start_date: str, end_date: Optional[str] = None) -> pd.DataFrame:
        """
        获取股票日线数据
        :param code: 股票代码，格式如：sh.600000
        :param start_date: 开始日期，格式：YYYY-MM-DD
        :param end_date: 结束日期，格式：YYYY-MM-DD，默认为今天
        :return: DataFrame
        """
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        code = self._format_stock_code(code)
        return self._fetch_data(
            bs.query_history_k_data_plus,
            "获取数据失败",
            code=code,
            fields="date,code,open,high,low,close,volume,amount,adjustflag",
            start_date=start_date,
            end_date=end_date,
            frequency="d",
            adjustflag="3"
        )
    
    def get_stock_basic_info(self, code: str) -> pd.DataFrame:
        """
        获取股票基本信息
        :param code: 股票代码
        :return: DataFrame
        """
        code = self._format_stock_code(code)
        return self._fetch_data(
            bs.query_stock_basic,
            "获取基本信息失败",
            code=code
        )
    
    def get_financial_data(self, code: str, year: int = 2024, quarter: int = 4) -> pd.DataFrame:
        """
        获取财务数据
        :param code: 股票代码
        :param year: 年份
        :param quarter: 季度
        :return: DataFrame
        """
        code = self._format_stock_code(code)
        return self._fetch_data(
            bs.query_profit_data,
            "获取财务数据失败",
            code=code,
            year=year,
            quarter=quarter
        )
    
    def get_growth_data(self, code: str, year: int = 2024, quarter: int = 4) -> pd.DataFrame:
        """
        获取成长数据
        :param code: 股票代码
        :param year: 年份
        :param quarter: 季度
        :return: DataFrame
        """
        code = self._format_stock_code(code)
        return self._fetch_data(
            bs.query_growth_data,
            "获取成长数据失败",
            code=code,
            year=year,
            quarter=quarter
        )
    
    def get_stock_industry_data(self, code: str) -> pd.DataFrame:
        """
        获取股票行业数据
        :param code: 股票代码
        :return: DataFrame
        """     
        code = self._format_stock_code(code)
        return self._fetch_data(
            bs.query_stock_industry,
            "获取行业数据失败",
            code=code
        )

    def get_adjust_factors(self, code: str, year: int = 2024) -> pd.DataFrame:
        """
        获取除权数据
        :param code: 股票代码
        :param year: 年份
        :return: DataFrame
        """
        code = self._format_stock_code(code)
        return self._fetch_data(
            bs.query_dividend_data,
            "获取除权数据失败",
            code=code,
            year=year
        )