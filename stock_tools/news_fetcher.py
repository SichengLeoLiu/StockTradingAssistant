import requests
import pandas as pd
from datetime import datetime, timedelta
import json

class NewsFetcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def _convert_stock_code(self, code):
        """转换股票代码格式"""
        # 移除前缀
        code = code.replace('sh.', '').replace('sz.', '')
        
        # 根据股票代码判断市场
        if code.startswith('6'):
            return f'sh{code}'
        elif code.startswith(('0', '3')):
            return f'sz{code}'
        else:
            return code
    
    def get_stock_news(self, code, count=20):
        """
        获取股票相关新闻
        :param code: 股票代码（如：600000）
        :param count: 获取新闻数量，默认20条
        :return: DataFrame，包含新闻标题、时间、来源、链接等信息
        """
        try:
            # 转换股票代码格式
            sina_code = self._convert_stock_code(code)
            
            # 构建API URL
            url = f'https://finance.sina.com.cn/roll/index.d.html?pageid=155&lid=1686&num={count}&encode=utf-8&stock={sina_code}'
            
            # 发送请求
            response = requests.get(url, headers=self.headers)
            response.encoding = 'utf-8'
            
            # 解析新闻数据
            news_list = []
            if response.status_code == 200:
                # 使用正则表达式提取新闻数据
                import re
                pattern = r'<div class="list_009">.*?<li><a href="(.*?)" target="_blank">(.*?)</a><span>(.*?)</span></li>'
                matches = re.findall(pattern, response.text, re.DOTALL)
                
                for link, title, date in matches:
                    news_list.append({
                        'title': title.strip(),
                        'date': date.strip(),
                        'url': link,
                        'source': '新浪财经'
                    })
            
            return pd.DataFrame(news_list)
            
        except Exception as e:
            print(f"获取新闻数据失败：{str(e)}")
            return pd.DataFrame()
    
    def get_company_news(self, code, count=20):
        """
        获取公司相关新闻（包括公司公告、研报等）
        :param code: 股票代码
        :param count: 获取新闻数量
        :return: DataFrame
        """
        try:
            # 转换股票代码格式
            sina_code = self._convert_stock_code(code)
            
            # 构建API URL
            url = f'https://vip.stock.finance.sina.com.cn/corp/view/vCB_AllBulletin.php?stockid={sina_code}'
            
            # 发送请求
            response = requests.get(url, headers=self.headers)
            response.encoding = 'gbk'
            
            # 解析公告数据
            news_list = []
            if response.status_code == 200:
                import re
                pattern = r'<td><a href="(.*?)" target="_blank">(.*?)</a></td><td>(.*?)</td>'
                matches = re.findall(pattern, response.text, re.DOTALL)
                
                for link, title, date in matches:
                    news_list.append({
                        'title': title.strip(),
                        'date': date.strip(),
                        'url': f'https://vip.stock.finance.sina.com.cn{link}',
                        'source': '公司公告'
                    })
            
            return pd.DataFrame(news_list)
            
        except Exception as e:
            print(f"获取公司公告失败：{str(e)}")
            return pd.DataFrame()
    
    def get_all_news(self, code, count=20):
        """
        获取所有相关新闻（包括市场新闻和公司公告）
        :param code: 股票代码
        :param count: 获取新闻数量
        :return: DataFrame
        """
        # 获取市场新闻
        market_news = self.get_stock_news(code, count)
        # 获取公司公告
        company_news = self.get_company_news(code, count)
        
        # 合并数据
        all_news = pd.concat([market_news, company_news], ignore_index=True)
        # 按日期排序
        all_news['date'] = pd.to_datetime(all_news['date'])
        all_news = all_news.sort_values('date', ascending=False)
        
        return all_news 