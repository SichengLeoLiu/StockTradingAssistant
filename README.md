# AI股票分析助手

这是一个基于大语言模型的股票分析助手，可以分析股票的技术面、基本面和舆情，并提供投资建议。

## 功能特点

- 使用baostock获取股票数据
- 计算多种技术指标（MA、MACD、RSI、布林带、KDJ等）
- 分析基本面数据（财务指标、估值指标等）
- 分析舆情数据（新闻情感分析）
- 使用DeepSeek模型进行综合分析
- 提供详细的投资建议

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

1. 复制`.env.example`文件为`.env`
2. 在`.env`文件中填入你的HuggingFace API Token

## 使用方法

1. 运行主程序：
```bash
python main.py
```

2. 在代码中自定义分析：
```python
from main import StockAnalysisAgent

agent = StockAnalysisAgent()
result = agent.analyze_stock("sh.600519", "请分析该股票的投资价值")
print(result)
```

## 项目结构

```
.
├── main.py                 # 主程序
├── requirements.txt        # 依赖包
├── .env                   # 环境变量
└── stock_tools/           # 工具模块
    ├── data_fetcher.py    # 数据获取
    ├── technical_analyzer.py  # 技术分析
    ├── fundamental_analyzer.py  # 基本面分析
    └── sentiment_analyzer.py  # 舆情分析
```

## 注意事项

1. 需要安装TA-Lib库，安装方法请参考[TA-Lib官网](http://ta-lib.org/)
2. 需要注册HuggingFace账号并获取API Token
3. 股票代码格式为：sh.600519（上海）或sz.000001（深圳）

## 许可证

MIT 