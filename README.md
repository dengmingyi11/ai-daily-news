# 🦴 骨髓炎医学资讯日报

每天北京时间 9:30 自动推送全球骨髓炎最新医学资讯到飞书。

---

## 📋 系统功能

### 自动检索内容

| 类别 | 关键词 |
|------|--------|
| **治疗研究** | osteomyelitis treatment, 骨髓炎治疗 |
| **诊断指南** | osteomyelitis diagnosis, 骨髓炎诊断 |
| **抗生素治疗** | osteomyelitis antibiotic therapy |
| **慢性骨髓炎** | chronic osteomyelitis management |
| **糖尿病足** | 糖尿病足骨髓炎 |

### 日报内容

- 📰 **今日研究进展** - 最新文献和资讯
- 📊 **本期概览** - 收录统计
- 💡 **临床要点提醒** - 诊断和治疗要点
- 📚 **推荐阅读** - PubMed、UpToDate 等资源

---

## 🚀 部署步骤

### 已完成配置
- ✅ GitHub 仓库已创建
- ✅ 飞书 Webhook 已验证
- ✅ 脚本已更新为骨髓炎资讯

### 待完成步骤

#### 1️⃣ 更新代码到 GitHub

代码已修改，需要推送更新：

```bash
cd /workspace/ai-daily-news
git add .
git commit -m "feat: 切换为骨髓炎医学资讯日报"
git push
```

#### 2️⃣ 配置 Secret

**Settings → Secrets → Actions → New repository secret**

| Name | Value |
|------|-------|
| `FEISHU_WEBHOOK_URL` | `https://open.feishu.cn/open-apis/bot/v2/hook/e55697f5-509b-49be-95a5-629068792d1d` |

#### 3️⃣ 启用 Actions 权限

**Settings → Actions → General**
- 选择 **"Read and write permissions"**
- 点击 **Save**

#### 4️⃣ 测试运行

**Actions → Osteomyelitis Medical News → Run workflow**

---

## ⏰ 自动推送

**每天北京时间 9:30**，系统会自动：
1. 🔍 检索全球骨髓炎最新医学资讯
2. 📝 生成结构化日报
3. 📱 推送到你的飞书群聊
4. 💾 保存日报到 GitHub 仓库

---

## ⚠️ 免责声明

本资讯仅供医学专业人士参考，不构成临床诊疗建议。

---

## 🔧 自定义搜索关键词

编辑 `scripts/generate_osteomyelitis_report.py` 第 10-19 行：

```python
SEARCH_QUERIES = [
    "osteomyelitis treatment latest research",
    "骨髓炎 治疗 最新研究",
    "osteomyelitis diagnosis guidelines",
    "骨髓炎 诊断 指南",
    # 添加更多关键词...
]
```
