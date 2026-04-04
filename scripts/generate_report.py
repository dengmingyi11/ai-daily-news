#!/usr/bin/env python3
"""
AI 行业日报自动生成脚本
通过搜索引擎获取最新 AI 行业动态并生成日报，推送到邮箱
"""

import os
import smtplib
import ssl
from datetime import datetime
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

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


def send_email(report: str, date_str: str):
    """发送邮件"""
    smtp_server = os.environ.get('EMAIL_SMTP_SERVER', 'smtp.163.com')
    smtp_port = int(os.environ.get('EMAIL_SMTP_PORT', '465'))
    username = os.environ.get('EMAIL_USERNAME')
    password = os.environ.get('EMAIL_PASSWORD')
    to_email = os.environ.get('EMAIL_TO')
    
    if not all([username, password, to_email]):
        print("⚠️ 邮件配置不完整，跳过发送")
        print(f"   EMAIL_USERNAME: {'已配置' if username else '未配置'}")
        print(f"   EMAIL_PASSWORD: {'已配置' if password else '未配置'}")
        print(f"   EMAIL_TO: {'已配置' if to_email else '未配置'}")
        return False
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'🤖 AI 行业日报 - {date_str}'
        msg['From'] = formataddr(('AI日报', username))
        msg['To'] = to_email
        
        # 纯文本版本
        text_content = report.replace('#', '').replace('*', '').replace('>', '')
        msg.attach(MIMEText(text_content, 'plain', 'utf-8'))
        
        # HTML 版本
        html = report.replace('\n', '<br>')
        html = html.replace('# 🤖 AI 行业日报', '<h1>🤖 AI 行业日报</h1>')
        html = html.replace('## ', '<h2>')
        html = html.replace('### ', '<h3>')
        html = html.replace('> ', '<blockquote>')
        html = html.replace('---', '<hr>')
        html = html.replace('🔗 ', '<a href="')
        html = html.replace(') [查看详情]', '">查看详情</a>')
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
                h1 {{ color: #2563eb; border-bottom: 2px solid #2563eb; padding-bottom: 10px; }}
                h2 {{ color: #1f2937; margin-top: 30px; }}
                h3 {{ color: #374151; }}
                blockquote {{ background: #f3f4f6; padding: 15px; border-left: 4px solid #2563eb; margin: 10px 0; }}
                a {{ color: #2563eb; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #e5e7eb; padding: 10px; }}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        # 发送
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(username, password)
            server.send_message(msg)
        
        print(f"✅ 邮件已发送至 {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
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
    
    # 发送邮件
    send_email(report, date_str)
    
    print("🎉 完成！")


if __name__ == "__main__":
    main()
