# AI Stock Intelligent Analysis Assistant

+ [中文版说明文档](README_zh.md)

 This project is an intelligent A-share stock analysis tool based on large language models and multi-dimensional data analysis. It integrates technical, fundamental, and sentiment analysis, and automatically generates professional investment advice. It is suitable for quantitative investment, individual investors, and financial researchers.

## Key Features

- **Stock Data Fetching**: Automatically retrieves A-share historical market, financial, growth, and industry data.
- **Technical Indicator Analysis**: Supports batch calculation and signal detection for mainstream indicators such as MA, MACD, RSI, Bollinger Bands, KDJ, CCI, DMI, OBV, VR, Williams %R, etc.
- **Fundamental Analysis**: Automatically extracts and analyzes core financial metrics like ROE, profit margin, main business income, and growth, combined with industry attributes to generate summaries.
- **LLM-powered Q&A**: Integrates ZhipuAI (GLM-4) model, supports natural language queries, automatically invokes multiple analysis tools, and generates structured analysis reports and investment advice.
- **One-click Analysis**: Simply input the stock code and analysis requirement to get a detailed multi-dimensional analysis result.

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Stock
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   > Note: You need to install [TA-Lib](https://ta-lib.org/) in advance. For Windows users, refer to [TA-Lib Installation Guide](https://blog.csdn.net/weixin_44791964/article/details/131701857).

3. **Environment Variables**
   - Copy `.env.example` to `.env` and fill in your `ZHIPUAI_API_KEY` (ZhipuAI) and other related keys.

## Quick Start

### One-click analysis via command line

Run the following command:
```bash
python main.py
```
The program will prompt you to input a stock code (for example, "sh.600000") and then proceed with the analysis.

### Example: Use in your own code

You can also import the StockAnalysisAgent in your own code and call it as follows (note that in the interactive mode, the stock code is prompted via input):
```python
from main import StockAnalysisAgent

agent = StockAnalysisAgent(start_date="2024-05-01", end_date="2024-06-01")
# In interactive mode, the stock code is prompted via input.
# For example, if you run main.py, you will be prompted to enter a stock code (e.g., "sh.600000").
query = "请分析该股票的投资价值，并给出具体的投资建议"
result = agent.analyze_stock(code, query)
print(result)
```

## Project Structure

```
.
├── main.py                   # Main program: integrates multi-dimensional analysis and LLM Q&A
├── requirements.txt          # Dependency list
├── .env.example              # Environment variable template
├── stock_tools/              # Analysis tool modules
│   ├── data_fetcher.py           # Stock data fetching
│   ├── technical_analyzer.py     # Technical indicator analysis
│   ├── fundamental_analyzer.py   # Fundamental analysis
│   └── sentiment_analyzer.py     # Sentiment analysis (Implementing)
└── README.md                 # Project documentation
```

## Notes

- You need to register a ZhipuAI account and obtain an API Token.
- Stock code format: `sh.600519` (Shanghai) or `sz.000063` (Shenzhen).

- This project is for academic and technical exchange only. Investment involves risks. Please make decisions cautiously.
