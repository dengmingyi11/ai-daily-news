#!/usr/bin/env python3
"""
AI 行业日报自动生成脚本
通过搜索引擎获取最新 AI 行业动态并生成日报，推送到飞书
"""

import os
import json
from datetime import datetime
from pathlib import Path

# 配置
SEARCH_QUERIES = [
    "AI 人工智能 最新动态 2025",
    "大模型 行业新闻",
    "GPT OpenAI 最新消息",
]

# 报告存放目录
REPORTS_DIR = Path(__file__).parent.parent / "reports"


def search_ai_news(query: str) -> list:
    """搜索 AI 新闻"""
    try:
        import requests
        from bs4 import BeautifulSoup
        
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        for result in soup.select('.result')[:5]:
            title_elem = result.select_one('.result__a')
            snippet_elem = result.select_one('.result__snippet')
            
            if title_elem:
                results.append({
                    'title': title_elem.get_text(strip=True),
                    'url': title_elem.get('href', ''),
                    'snippet': snippet_elem.get_text(strip=True) if snippet_elem else ''
                })
        
        return results
        
    except Exception as e:
        print(f"搜索失败: {e}")
        return []


def generate_report() -> tuple:
    """生成日报内容"""
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    
    # 收集新闻
    all_news = []
    seen_titles = set()
    
    for query in SEARCH_QUERIES[:2]:
        results = search_ai_news(query)
        for item in results:
            if item['title'] not in seen_titles:
                seen_titles.add(item['title'])
                all_news.append(item)
    
    unique_news = all_news[:5]
    
    # 生成 Markdown 报告
    report = f"""# 🤖 AI 行业日报

> 生成时间：{today.strftime("%Y-%m-%d %H:%M:%S")}

---

## 📰 今日要闻

"""
    
    if unique_news:
        for i, news in enumerate(unique_news, 1):
            report += f"### {i}. {news['title']}\n\n"
            if news['snippet']:
                report += f"> {news['snippet']}\n\n"
            if news['url']:
                report += f"🔗 [查看详情]({news['url']})\n\n"
            report += "---\n\n"
    else:
        report += "*暂无获取到新闻，请稍后重试*\n\n---\n\n"
    
    report += """## 📊 关键数据

| 指标 | 说明 |
|------|------|
| 📈 行业热度 | AI 持续保持高关注度 |
| 🔥 热门领域 | 大模型、智能体、具身智能 |
| 💰 投资动态 | 科技巨头持续加码 AI 投资 |

---

## 💡 一句话趋势点评

> AI 行业持续高速发展，大模型能力边界不断拓展，智能体和具身智能成为新热点。

---

*本报告由 GitHub Actions 自动生成*
"""
    
    return report, date_str


def send_feishu(report: str, date_str: str):
    """发送飞书推送"""
    import requests
    
    webhook_url = os.environ.get('FEISHU_WEBHOOK_URL')
    
    if not webhook_url:
        print("⚠️ 飞书 Webhook URL 未配置，跳过推送")
        return False
    
    try:
        # 构建飞书消息
        title = f"🤖 AI 行业日报 - {date_str}"
        
        # 飞书消息格式（支持 markdown）
        # 飞书 text 类型支持部分 markdown 语法
        content = f"{title}\n\n{report}"
        
        data = {
            "msg_type": "text",
            "content": {
                "text": content
            }
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.post(webhook_url, json=data, headers=headers, timeout=10)
        result = response.json()
        
        if response.status_code == 200 and result.get('code') == 0:
            print(f"✅ 飞书推送成功！")
            return True
        else:
            print(f"❌ 飞书推送失败: {result.get('msg', '未知错误')}")
            return False
        
    except Exception as e:
        print(f"❌ 飞书推送失败: {e}")
        return False


def main():
    """主函数"""
    print("🚀 开始生成 AI 行业日报...")
    
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    report, date_str = generate_report()
    
    # 保存报告
    report_file = REPORTS_DIR / f"AI日报_{date_str}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 日报已生成: {report_file}")
    
    # 发送飞书推送
    send_feishu(report, date_str)
    
    print("🎉 完成！")


if __name__ == "__main__":
    main()
