#!/bin/bash
# 推送脚本 - 多种方式尝试

echo "尝试推送..."

# 切回 HTTPS
git remote set-url origin https://github.com/xiaogui-li/snake-game.git

# 方法1: 直接推送
echo "方法1: 直接推送..."
timeout 60 git push && exit 0

# 方法2: 用 web 方式
echo "方法1失败，尝试方法2..."
git config --global http.postBuffer 524288000
timeout 120 git push && exit 0

echo "推送失败，请检查网络或稍后重试"
