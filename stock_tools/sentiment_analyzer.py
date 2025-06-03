import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import jieba
from collections import Counter
import numpy as np
import os
from dotenv import load_dotenv
import time
import random

# 加载环境变量
load_dotenv()

class SentimentAnalyzer:
    def __init__(self):
        # 初始化情感词典
        self.positive_words = set([
            '上涨', '增长', '利好', '突破', '创新高', '强势', '看好', '推荐', '买入',
            '增持', '超预期', '盈利', '收益', '增长', '扩张', '发展', '机会', '潜力',
            '龙头', '领先', '优势', '突破', '创新', '升级', '转型', '成功', '突破'
        ])
        
        self.negative_words = set([
            '下跌', '下跌', '利空', '亏损', '风险', '警告', '减持', '卖出', '不看好',
            '低于预期', '压力', '困难', '挑战', '问题', '危机', '衰退', '萎缩', '下滑',
            '疲软', '弱势', '调整', '震荡', '波动', '风险', '警告', '谨慎', '观望'
        ])
        
        # 情感词权重
        self.word_weights = {
            '上涨': 2.0, '增长': 2.0, '利好': 2.5, '突破': 2.0, '创新高': 2.5,
            '下跌': -2.0, '亏损': -2.5, '利空': -2.5, '风险': -2.0, '警告': -2.5
        }
        
        # 程度副词权重
        self.intensity_words = {
            '非常': 1.5, '极其': 1.5, '特别': 1.3, '十分': 1.3, '很': 1.2,
            '稍微': 0.8, '略微': 0.8, '有点': 0.8, '较为': 0.9, '相对': 0.9
        }
        
        # 否定词
        self.negation_words = set(['不', '没有', '未', '无', '非', '否'])
    
    def get_news_data(self, stock_code):
        """
        获取股票相关评论
        :param stock_code: 股票代码（如：600519）
        :return: DataFrame
        """
        # 移除股票代码前缀（如果有）
        stock_code = stock_code.replace('sh.', '').replace('sz.', '')
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        
        # 东方财富股吧URL
        base_url = f'http://guba.eastmoney.com/list,{stock_code}.html'
        
        url = base_url
        print(url)
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.select('tbody.listbody tr.listitem')

        news_data = []
        for post in posts:
            try:
                date = post.select_one('.update').text
                title = post.select_one('.title a').text
                content = post.select_one('.title a')['href']  # 获取帖子链接
                source = post.select_one('.author a').text
                url = f"http://guba.eastmoney.com{content}"
                
                news_data.append({
                    'date': date,
                    'title': title, 
                    'source': source,
                    'url': url
                })
            except (AttributeError, TypeError) as e:
                continue

        return pd.DataFrame(news_data)
    
    def analyze_sentiment(self, title, content):
        """
        使用基于词典和规则的方法分析文本情感
        :param title: 新闻标题
        :param content: 新闻内容(不使用)
        :return: 情感分析结果字典
        """
        try:
            # 分词
            title_words = list(jieba.cut(title))
            
            # 初始化情感分析结果
            sentiment_score = 0
            key_words = []
            intensity = 1.0
            
            # 分析每个词
            for i, word in enumerate(title_words):
                # 检查程度副词
                if word in self.intensity_words:
                    intensity = self.intensity_words[word]
                    continue
                
                # 检查否定词
                if word in self.negation_words:
                    intensity = -1.0
                    continue
                
                # 检查情感词
                if word in self.positive_words:
                    weight = self.word_weights.get(word, 1.0)
                    sentiment_score += weight * intensity
                    key_words.append(word)
                elif word in self.negative_words:
                    weight = self.word_weights.get(word, 1.0)
                    sentiment_score -= weight * intensity
                    key_words.append(word)
                
                # 重置强度
                intensity = 1.0
            
            # 归一化情感得分到0-10分
            normalized_score = min(max((sentiment_score + 10) / 2, 0), 10)
            
            # 确定情感倾向
            if normalized_score > 6:
                sentiment = "正面"
            elif normalized_score < 4:
                sentiment = "负面"
            else:
                sentiment = "中性"
            
            # 生成影响分析
            impact = self._generate_impact_analysis(sentiment, normalized_score, key_words)
            
            return {
                "sentiment": sentiment,
                "score": normalized_score,
                "key_words": list(set(key_words)),
                "impact": impact
            }
            
        except Exception as e:
            print(f"情感分析出错: {str(e)}")
            return {
                "sentiment": "中性",
                "score": 5,
                "key_words": [],
                "impact": "无法分析"
            }
    
    def _generate_impact_analysis(self, sentiment, score, key_words):
        """生成对股价影响的简要分析"""
        if sentiment == "正面":
            if score > 8:
                return "强烈看涨信号，可能推动股价大幅上涨"
            else:
                return "温和看涨信号，可能对股价有积极影响"
        elif sentiment == "负面":
            if score < 2:
                return "强烈看跌信号，可能导致股价大幅下跌"
            else:
                return "温和看跌信号，可能对股价有消极影响"
        else:
            return "中性信号，对股价影响可能有限"
    
    def get_sentiment_analysis(self, stock_code):
        """
        获取股票舆情分析
        :param stock_code: 股票代码
        :return: 分析结果字典
        """
        news_df = self.get_news_data(stock_code)
        print(news_df)
        
        sentiment_results = []
        for _, row in news_df.iterrows():
            result = self.analyze_sentiment(row['title'], row['content'])
            sentiment_results.append(result)
        
        # 计算总体情感得分
        scores = [r['score'] for r in sentiment_results]
        avg_score = np.mean(scores)
        
        # 统计情感倾向
        sentiments = [r['sentiment'] for r in sentiment_results]
        sentiment_counts = Counter(sentiments)
        
        # 收集所有关键词
        all_keywords = []
        for r in sentiment_results:
            all_keywords.extend(r['key_words'])
        keyword_counts = Counter(all_keywords)
        
        analysis = {
            'average_score': avg_score,
            'sentiment_distribution': dict(sentiment_counts),
            'top_keywords': dict(keyword_counts.most_common(10)),
            'recent_trend': '看涨' if avg_score > 5 else '看跌',
            'detailed_analysis': sentiment_results
        }
        
        return analysis
    
    def get_sentiment_summary(self, stock_code):
        """
        生成舆情分析摘要
        :param stock_code: 股票代码
        :return: 分析摘要字符串
        """
        analysis = self.get_sentiment_analysis(stock_code)
        
        summary = [
            f"舆情分析:",
            f"平均情感得分: {analysis['average_score']:.2f}",
            f"情感分布: {analysis['sentiment_distribution']}",
            f"热门关键词: {analysis['top_keywords']}",
            f"近期趋势: {analysis['recent_trend']}",
            "\n详细分析:"
        ]
        
        # 添加每条新闻的详细分析
        for i, detail in enumerate(analysis['detailed_analysis'], 1):
            summary.append(f"\n新闻 {i}:")
            summary.append(f"情感: {detail['sentiment']}")
            summary.append(f"得分: {detail['score']}")
            summary.append(f"关键词: {', '.join(detail['key_words'])}")
            summary.append(f"影响分析: {detail['impact']}")
        
        return "\n".join(summary) 