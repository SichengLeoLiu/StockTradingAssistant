# AI 股票智能分析助手

+ [English README](README.md)

 本项目是一个基于大语言模型和多维度数据分析的 A 股智能分析工具，集成了技术面、基本面以及舆情分析，并自动生成专业的投资建议，适合量化投资、个人投资者以及金融研究人员使用。

## 主要功能

- **股票数据获取**：自动拉取 A 股历史行情、财务、成长、行业等数据。
- **技术指标分析**：支持 MA、MACD、RSI、布林带、KDJ、CCI、DMI、OBV、VR、威廉指标等主流技术指标的批量计算与信号判别。
- **基本面分析**：自动提取并分析净资产收益率、利润率、主营收入、成长性等核心财务指标，结合行业属性生成摘要。
- **舆情分析**：爬取主流财经社区（如东方财富股吧）相关股票新闻，基于情感词典和规则进行情感打分，辅助判断市场情绪。
- **大模型智能问答**：集成智谱 AI（GLM-4）模型，支持自然语言提问，自动调用多种分析工具，生成结构化分析报告和投资建议。
- **一键分析**：只需输入股票代码和分析需求，即可获得详细的多维度分析结果。

## 安装方法

1. **克隆项目**
   ```bash
   git clone <你的仓库地址>
   cd Stock
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```
   > 注意：需提前安装好 [TA-Lib](https://ta-lib.org/) 库，Windows 用户建议参考 [TA-Lib 安装教程](https://blog.csdn.net/weixin_44791964/article/details/131701857)。

3. **环境变量配置**
   - 复制 `.env.example` 为 `.env`，并填写你的 `ZHIPUAI_API_KEY`（智谱 AI）等相关密钥。

## 快速上手

### 命令行一键分析

运行以下命令：
```bash
python main.py
```
程序会提示你输入股票代码（例如"sh.600000"），然后进行后续分析。

### 代码调用示例

你也可以在代码中导入 StockAnalysisAgent，并如下调用（注意在交互模式下，股票代码通过输入提示）：
```python
from main import StockAnalysisAgent

agent = StockAnalysisAgent(start_date="2024-05-01", end_date="2024-06-01")
# 在交互模式下，股票代码通过输入提示。
# 例如，运行 main.py 时，会提示你输入股票代码（例如"sh.600000"）。
query = "请分析该股票的投资价值，并给出具体的投资建议"
result = agent.analyze_stock(code, query)
print(result)
```

## 目录结构

```
.
├── main.py                   # 主程序：集成多维度分析与大模型问答
├── requirements.txt          # 依赖包列表
├── .env.example              # 环境变量模板
├── stock_tools/              # 各类分析工具模块
│   ├── data_fetcher.py           # 股票数据获取
│   ├── technical_analyzer.py     # 技术指标分析
│   ├── fundamental_analyzer.py   # 基本面分析
│   └── sentiment_analyzer.py     # 舆情分析（实现中）
└── README.md                 # 项目说明文档
```

## 注意事项

- 需注册智谱 AI 账号并获取 API Token。
- 股票代码格式：`sh.600519`（上海）或 `sz.000063`（深圳）。
- 本项目仅供学术和技术交流，投资有风险，决策需谨慎。

## 许可证

MIT 