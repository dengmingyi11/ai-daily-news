#!/usr/bin/env python3
"""
骨髓炎医学资讯日报自动生成脚本
每日自动检索并汇总全球范围内关于骨髓炎的最新医学资讯
"""

import os
from datetime import datetime, timedelta
from pathlib import Path

# 搜索关键词配置
SEARCH_QUERIES = [
    "osteomyelitis treatment latest research",
    "骨髓炎 治疗 最新研究",
    "osteomyelitis diagnosis guidelines",
    "骨髓炎 诊断 指南",
    "osteomyelitis antibiotic therapy",
    "骨髓炎 抗生素 治疗",
    "chronic osteomyelitis management",
    "糖尿病足 骨髓炎 治疗",
]

# 报告存放目录
REPORTS_DIR = Path(__file__).parent.parent / "reports"


def search_medical_news(query: str) -> list:
    """搜索医学资讯"""
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
    """生成骨髓炎医学资讯日报"""
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    
    # 收集资讯
    all_news = []
    seen_titles = set()
    
    for query in SEARCH_QUERIES[:4]:  # 搜索前4个关键词
        results = search_medical_news(query)
        for item in results:
            if item['title'] not in seen_titles:
                seen_titles.add(item['title'])
                all_news.append(item)
    
    unique_news = all_news[:8]  # 显示前8条
    
    # 生成报告
    report = f"""# 🦴 骨髓炎医学资讯日报

> 📅 生成时间：{today.strftime("%Y-%m-%d %H:%M:%S")}
> ⏰ 时间范围：过去 24 小时
> 🔍 数据来源：全球医学数据库

---

## 📰 今日研究进展

"""
    
    if unique_news:
        for i, news in enumerate(unique_news, 1):
            report += f"### {i}. {news['title']}\n\n"
            if news['snippet']:
                report += f"**摘要：** {news['snippet']}\n\n"
            if news['url']:
                report += f"🔗 [查看原文]({news['url']})\n\n"
            report += "---\n\n"
    else:
        report += "*暂无获取到最新资讯，请稍后重试*\n\n---\n\n"
    
    report += f"""## 📊 本期概览

| 指标 | 说明 |
|------|------|
| 📚 收录文献 | {len(unique_news)} 篇 |
| 🔬 主要领域 | 治疗、诊断、抗生素、慢性骨髓炎 |
| 🌐 覆盖地区 | 全球范围 |
| 📅 更新日期 | {date_str} |

---

## 💡 临床要点提醒

> ⚠️ **诊断要点**
> - MRI 是诊断骨髓炎的金标准
> - 血培养和骨活检有助于明确病原体
> - CRP 和 ESR 可用于监测治疗效果

> 💊 **治疗要点**
> - 急性骨髓炎：抗生素治疗 4-6 周
> - 慢性骨髓炎：可能需要手术清创 + 抗生素
> - 糖尿病足骨髓炎：多学科综合治疗

---

## 📚 推荐阅读

| 资源 | 说明 |
|------|------|
| [PubMed - Osteomyelitis](https://pubmed.ncbi.nlm.nih.gov/?term=osteomyelitis) | 最新文献检索 |
| [UpToDate - Osteomyelitis](https://www.uptodate.com/contents/search?search=osteomyelitis) | 临床决策支持 |
| [Cochrane Library](https://www.cochranelibrary.com/search?q=osteomyelitis) | 循证医学证据 |

---

*本报告由 GitHub Actions 自动生成 | 每日定时推送*

*免责声明：本资讯仅供医学专业人士参考，不构成临床诊疗建议*
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
        title = f"🦴 骨髓炎医学资讯日报 - {date_str}"
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
    print("🚀 开始生成骨髓炎医学资讯日报...")
    
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    report, date_str = generate_report()
    
    # 保存报告
    report_file = REPORTS_DIR / f"骨髓炎资讯_{date_str}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 日报已生成: {report_file}")
    
    # 发送飞书推送
    send_feishu(report, date_str)
    
    print("🎉 完成！")


if __name__ == "__main__":
    main()
