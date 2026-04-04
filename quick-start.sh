#!/bin/bash
# ============================================
# AI 日报系统 - 一键部署脚本
# GitHub 用户名: dengmingyi11
# ============================================

echo "🚀 开始部署 AI 日报系统..."
echo ""

# 设置变量
USERNAME="dengmingyi11"
REPO="ai-daily-news"
REPO_URL="https://github.com/${USERNAME}/${REPO}.git"

echo "📝 步骤 1: 初始化 Git 仓库"
cd /workspace/ai-daily-news
git init
git branch -M main

echo ""
echo "📝 步骤 2: 添加所有文件"
git add .
git commit -m "feat: 初始化 AI 日报自动推送系统"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⏸️  请先在 GitHub 创建仓库，然后继续"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "👉 打开这个链接创建仓库："
echo "   https://github.com/new"
echo ""
echo "📋 仓库名称填写: ai-daily-news"
echo "   选择 Public 或 Private"
echo "   不要勾选任何初始化选项"
echo "   点击 Create repository"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "✅ 仓库创建完成后按 Enter 继续..."

echo ""
echo "📝 步骤 3: 推送到 GitHub"
git remote add origin ${REPO_URL}
git push -u origin main

echo ""
echo "✅ 部署完成！"
echo ""
echo "📋 接下来请在 GitHub 网页上操作："
echo ""
echo "1️⃣  配置 Secrets："
echo "    ${REPO_URL}/settings/secrets/actions"
echo ""
echo "    添加以下 6 个 Secret："
echo "    ┌─────────────────────┬──────────────────────────┐"
echo "    │ Name                │ Secret                   │"
echo "    ├─────────────────────┼──────────────────────────┤"
echo "    │ EMAIL_SMTP_SERVER   │ smtp.163.com             │"
echo "    │ EMAIL_SMTP_PORT     │ 465                      │"
echo "    │ EMAIL_USERNAME      │ 18973490188@163.com      │"
echo "    │ EMAIL_PASSWORD      │ ALdXTGM7CcAj78KH         │"
echo "    │ EMAIL_TO            │ 18973490188@163.com      │"
echo "    │ EMAIL_USE_SSL       │ true                     │"
echo "    └─────────────────────┴──────────────────────────┘"
echo ""
echo "2️⃣  启用 Actions 权限："
echo "    ${REPO_URL}/settings/actions"
echo "    选择 'Read and write permissions'"
echo "    点击 Save"
echo ""
echo "3️⃣  测试运行："
echo "    ${REPO_URL}/actions"
echo "    点击 'AI Daily News' → 'Run workflow'"
echo ""
echo "🎉 完成！每天北京时间 9:30 自动推送 AI 日报！"
