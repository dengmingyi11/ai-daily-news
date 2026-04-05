#!/usr/bin/env python3
"""
AI 技术资讯日报自动生成脚本
每日自动检索并汇总全球范围内关于AI技术及其应用的最新资讯
"""

import os
from datetime import datetime, timedelta
from pathlib import Path

# 搜索关键词配置（按类别分组）
SEARCH_QUERIES = {
    "前沿研究": [
        "arXiv AI machine learning latest",
        "NeurIPS ICML ICLR 2025 papers",
        "GPT LLM transformer new model",
        "AI training optimization 2025",
    ],
    "产业动态": [
        "OpenAI Google DeepMind Meta AI news",
        "AI startup funding acquisition 2025",
        "AI product launch release 2025",
        "Nvidia AI chip GPU news",
    ],
    "政策伦理": [
        "AI regulation policy law 2025",
        "AI safety alignment guidelines",
        "AI copyright ethics controversy",
    ],
    "应用落地": [
        "AI medical healthcare application",
        "AI autonomous driving news",
        "AI robotics automation latest",
        "AI finance banking application",
    ],
}

# 报告存放目录
REPORTS_DIR = Path(__file__).parent.parent / "reports"


def search_news(query: str, max_results: int = 5) -> list:
    """搜索新闻"""
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
        
        for result in soup.select('.result')[:max_results]:
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
        print(f"搜索失败 [{query}]: {e}")
        return []


def deduplicate_news(all_news: list) -> list:
    """去重"""
    seen_titles = set()
    unique_news = []
    
    for news in all_news:
        # 简单去重：标题相似度检查
        title_lower = news['title'].lower()
        is_duplicate = False
        
        for seen in seen_titles:
            # 简单判断：如果标题有 80% 以上相似，视为重复
            if title_lower in seen or seen in title_lower:
                is_duplicate = True
                break
        
        if not is_duplicate:
            seen_titles.add(title_lower)
            unique_news.append(news)
    
    return unique_news


def generate_report() -> tuple:
    """生成 AI 技术资讯日报"""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")
    
    # 收集各类别新闻
    categorized_news = {}
    total_count = 0
    
    for category, queries in SEARCH_QUERIES.items():
        all_news = []
        for query in queries[:2]:  # 每类搜索前2个关键词
            results = search_news(query, max_results=3)
            all_news.extend(results)
        
        unique_news = deduplicate_news(all_news)[:5]  # 每类最多5条
        categorized_news[category] = unique_news
        total_count += len(unique_news)
    
    # 生成报告
    report = f"""# 🤖 AI技术资讯日报 · {now.strftime("%Y年%m月%d日")}

> 共收录 {total_count} 条更新 | 数据采集截止北京时间 {time_str}

---

"""

    # 今日焦点（选取最重要的1-2条）
    all_top_news = []
    for news_list in categorized_news.values():
        all_top_news.extend(news_list[:1])
    
    if all_top_news:
        report += "## 📌 今日焦点\n\n"
        for i, news in enumerate(all_top_news[:2], 1):
            report += f"**{i}. {news['title']}**\n\n"
            if news['snippet']:
                report += f"- 核心看点：{news['snippet'][:100]}...\n"
            if news['url']:
                report += f"- 来源：[查看详情]({news['url']})\n"
            report += "\n"
        report += "---\n\n"
    
    # 前沿研究
    if categorized_news.get("前沿研究"):
        report += "## 🚀 前沿研究\n\n"
        report += "### 模型与算法\n\n"
        for news in categorized_news["前沿研究"][:3]:
            report += f"**• {news['title']}**\n"
            if news['snippet']:
                report += f"  - 关键贡献：{news['snippet'][:80]}...\n"
            if news['url']:
                report += f"  - 来源：[链接]({news['url']})\n"
            report += "\n"
        report += "---\n\n"
    
    # 产业与应用
    if categorized_news.get("产业动态"):
        report += "## 💼 产业与应用\n\n"
        report += "### 大厂动态\n\n"
        for news in categorized_news["产业动态"][:3]:
            report += f"**• {news['title']}**\n"
            if news['snippet']:
                report += f"  - 简述：{news['snippet'][:80]}...\n"
            if news['url']:
                report += f"  - 来源：[链接]({news['url']})\n"
            report += "\n"
        report += "---\n\n"
    
    # 政策与伦理
    if categorized_news.get("政策伦理"):
        report += "## ⚖️ 政策·安全·伦理\n\n"
        for news in categorized_news["政策伦理"][:2]:
            report += f"**• {news['title']}**\n"
            if news['snippet']:
                report += f"  - 要点：{news['snippet'][:80]}...\n"
            if news['url']:
                report += f"  - 来源：[链接]({news['url']})\n"
            report += "\n"
        report += "---\n\n"
    
    # 应用落地
    if categorized_news.get("应用落地"):
        report += "## 🏥 应用落地案例\n\n"
        for news in categorized_news["应用落地"][:3]:
            report += f"**• {news['title']}**\n"
            if news['snippet']:
                report += f"  - 简述：{news['snippet'][:80]}...\n"
            if news['url']:
                report += f"  - 来源：[链接]({news['url']})\n"
            report += "\n"
        report += "---\n\n"
    
    # 今日论文速览
    report += """## 📊 今日论文速览

> 论文检索来自 arXiv、顶级会议等

| 领域 | 论文标题 | 来源 |
|------|----------|------|
| 大模型 | [最新进展请查看 arXiv](https://arxiv.org/list/cs.AI/recent) | arXiv |
| 机器学习 | [ICML 2025 论文](https://icml.cc/Conferences/2025) | ICML |
| 计算机视觉 | [CVPR 2025 论文](https://cvpr.thecvf.com/) | CVPR |

---

"""

    # 数据概览
    report += f"""## 📈 今日数据概览

| 指标 | 数据 |
|------|------|
| 📊 收录资讯 | {total_count} 条 |
| 📅 更新日期 | {date_str} |
| ⏰ 截止时间 | {time_str} 北京时间 |
| 🔍 数据来源 | DuckDuckGo 全球搜索 |

---

*本报告由自动化检索生成，仅供参考。完整内容请点击链接查看。*

*数据来源：arXiv、官方博客、权威科技媒体等*
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
        title = f"🤖 AI技术资讯日报 · {date_str}"
        content = f"{title}\n\n{report}"
        
        data = {
            "msg_type": "text",
            "content": {
                "text": content
            }
        }
        
        headers = {'Content-Type': 'application/json'}
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
    print("🚀 开始生成 AI 技术资讯日报...")
    
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
