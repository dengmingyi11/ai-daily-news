# 🐛 AI 日报系统 - 故障排查指南

如果你没有收到 AI 日报，请按以下步骤排查：

---

## 1️⃣ 检查 GitHub Actions 运行状态

### 访问运行记录页面：
👉 **https://github.com/dengmingyi11/ai-daily-news/actions/workflows/ai-daily-news.yml**

### 你应该看到：

```
┌─────────────────────────────────────────────────────┐
│ AI Daily News (ai-daily-news.yml)                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│ 📄 .github/workflows/ai-daily-news.yml              │
│                                                     │
│ This workflow has a `workflow_dispatch` event,      │
│ meaning it can be run manually from the Actions tab │
│                                                     │
│           ┌────────────────────────────┐           │
│           │    Run workflow    🟢      │           │
│           └────────────────────────────┘           │
│                                                     │
│ Branch: main ▼                                      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 2️⃣ 查看最近的运行记录

### 访问运行列表：
👉 **https://github.com/dengmingyi11/ai-daily--ns/actions/runs**

### 检查：
- 有没有任何运行记录？
- 运行状态是 `✅` 还是 `❌`？
- 最近的运行时间是什么时候？

---

## 3️⃣ 手动运行一次

### 步骤：
1. 点击上面链接
2. 点击蓝色的 **"AI Daily News"**
3. 点击绿色的 **"Run workflow"**
4. 再次点击 **"Run workflow"**

---

## 4️⃣ 查看运行日志

### 点击任意运行记录，查看详细日志：

**日志中应该能看到：**

```
🚀 开始生成 AI 行业日报...
✅ 日报已生成: /workspace/ai-daily-news/reports/AI日报_2025-04-04.md
✅ 飞书推送成功！
🎉 完成！
```

### 如果看到错误：
- `⚠️ 飞书 Webhook URL 未配置，跳过推送` → Secret 没配置
- `❌ 飞书推送失败: ...` → 查看具体错误信息

---

## 5️⃣ 检查 Secrets 配置

### 确认 Secret 是否正确设置：

**访问：** Settings → Secrets and variables → Actions

**检查：**
| Secret 名称 | 值 |
|-------------|-----|
| `FEISHU_WEBHOOK_URL` | `https://open.feishu.cn/open-apis/bot/v2/hook/e55697f5-509b-49be-95a5-629068792d1d` |

**注意：** Secret 名称是 **`FEISHU_WEBHOOK_URL`**（大写）

---

## 6️⃣ 测试飞书 Webhook

### 在本地终端运行：

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "text",
    "content": {
        "text": "🤖 AI 日报系统测试消息\n\n这是一条测试消息，发送时间：$(date '+%Y-%m-%d %H:%M:%S')\n\n如果收到此消息，说明飞书推送功能正常！"
    }
  }' \
  https://open.feishu.cn/open-apis/bot/v2/hook/e55697f5-509b-49be-95a5-629068792d1d
```

### 如果你收到类似这样的响应：

```json
{"StatusCode":0,"StatusMessage":"success","code":0,"data":{},"msg":"success"}
```

说明 Webhook 配置正确。

---

## 7️⃣ 检查飞书设置

### 在飞书中检查：

1. **机器人是否被禁言？**
   - 打开群聊设置
   - 查看机器人权限

2. **消息是否被折叠？**
   - 检查消息记录
   - 查看是否有消息被系统过滤

3. **重新添加机器人**
   - 如果怀疑机器人有问题，可以：
     1. 删除现有机器人
     2. 重新创建机器人
     3. 复制新的 Webhook URL

---

## 8️⃣ 检查定时任务配置

### 工作流配置（每天 UTC 01:30 = 北京时间 09:30）

```yaml
schedule:
  - cron: '30 1 * * *'  # 每天 UTC 01:30
```

**注意：** 如果你想要其他时间，可以修改：
- `30 1 * * *` = 北京时间 09:30
- `0 0 * * *` = 北京时间 08:00
- `0 4 * * *` = 北京时间 12:00

---

## 🚨 常见问题

### ❌ 问题 1：没有运行记录
**原因：** 工作流可能被禁用或从未运行过

### ❌ 问题 2：运行失败
**检查：**
1. Secrets 是否正确配置？
2. Webhook URL 是否有效？
3. 网络是否正常？

### ❌ 问题 3：运行成功但没收到
**检查：**
1. 飞书机器人是否被禁言？
2. 消息是否被折叠到其他文件夹？
3. 是否在飞书群聊中？

---

## 🔧 如果还是不行

请告诉我：

1. **最近一次运行的状态**（✅ 成功 / ❌ 失败）
2. **运行日志中的具体错误信息**
3. **你尝试了哪些排查步骤**

这样我才能帮你进一步解决问题！