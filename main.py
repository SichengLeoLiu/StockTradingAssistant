from stock_tools.data_fetcher import StockDataFetcher
from stock_tools.technical_analyzer import TechnicalAnalyzer
from stock_tools.fundamental_analyzer import FundamentalAnalyzer
from stock_tools.sentiment_analyzer import SentimentAnalyzer
from langchain.agents import Tool, initialize_agent
# from langchain_community.llms import ZhipuAI
from langchain_community.chat_models import ChatZhipuAI
import os
from dotenv import load_dotenv
from datetime import datetime
import warnings

# 加载环境变量
load_dotenv()
class StockAnalysisAgent:
    def __init__(self, start_date, end_date):
        # 初始化数据获取器
        self.data_fetcher = StockDataFetcher()
        
        # 初始化智谱AI模型
        self.llm = ChatZhipuAI(
            model="glm-4-flash",
            temperature=0.1,
            zhipuai_api_key=os.getenv("ZHIPUAI_API_KEY")
        )
        
        # 定义工具
        self.tools = [
            Tool(
                name="get_stock_data",
                func=self.get_stock_data,
                description="获取股票历史数据，包括开盘价、收盘价、最高价、最低价、成交量等。股票代码格式示例：sh.600000"
            ),
            Tool(
                name="analyze_technical",
                func=self.analyze_technical,
                description="分析股票技术指标，包括移动平均线、MACD、RSI、布林带、KDJ、CCI、DMI、OBV、VR、威廉指标等"
            ),
            Tool(
                name="analyze_fundamental",
                func=self.analyze_fundamental,
                description="分析股票基本面，包括财务指标、估值指标等"
            ),
            # Tool(
            #     name="analyze_sentiment",
            #     func=self.analyze_sentiment,
            #     description="分析股票舆情，包括新闻情感分析、市场情绪等"
            # )
        ]
        
        # 初始化Agent
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent="zero-shot-react-description",
            verbose=True
        )
        
        self.start_date = start_date
        self.end_date = end_date
    
    def get_stock_data(self, code):
        """获取股票数据"""
        return self.data_fetcher.get_stock_data(code, self.start_date, self.end_date)
    
    
    def analyze_technical(self, code):
        """分析技术指标"""
        stock_data = self.data_fetcher.get_stock_data(code, self.start_date, self.end_date)
        analyzer = TechnicalAnalyzer(stock_data)
        return analyzer.calculate_all_indicators()
    
    def analyze_fundamental(self, code):
        """分析基本面"""
        financial_data = self.data_fetcher.get_financial_data(code)
        growth_data = self.data_fetcher.get_growth_data(code)
        industry_data = self.data_fetcher.get_stock_industry_data(code)
        analyzer = FundamentalAnalyzer(financial_data, growth_data, industry_data)
        return analyzer.get_financial_summary()
    
    def analyze_sentiment(self, code):
        """分析舆情"""
        analyzer = SentimentAnalyzer()
        return analyzer.get_sentiment_summary(code)
    
    def analyze_stock(self, code, query):
        """
        分析股票
        :param code: 股票代码
        :param query: 分析需求
        :return: 分析结果
        """
        # 确保股票代码格式正确
        if not code.startswith(('sh.', 'sz.')):
            code = 'sh.' + code
            
        prompt = f"""
        请分析股票代码为{code}的股票。
        用户需求：{query}
        
        请使用以下工具获取和分析数据：
        1. 获取股票历史数据
        2. 分析技术指标
        3. 分析基本面
        
        请给出详细的分析报告，并给出具体的投资建议。
        
        请用专业、客观的语言进行分析，并给出具体的长短线投资建议（做多、做空、持有）。
        """
        
        return self.agent.run(prompt)

def main():
    # 初始化分析Agent
    # 忽略警告信息
    warnings.filterwarnings('ignore')
    start_date = "2024-5-1"

    end_date = datetime.now().strftime("%Y-%m-%d")
    agent = StockAnalysisAgent(start_date, end_date)
    
    code = "sz.000063" 
    query = "请分析该股票的投资价值，并给出具体的投资建议"
    
    # 执行分析
    result = agent.analyze_stock(code, query)
    print("\n分析结果：")
    print(result)

if __name__ == "__main__":
    main() 