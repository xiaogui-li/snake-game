#!/bin/bash
# APK 打包脚本

# 激活虚拟环境
source ~/buildozer_env/bin/activate

# 进入项目目录
cd /mnt/c/Users/asus/.qclaw/workspace/snake_kivy/snake-game

# 开始构建
echo "开始构建 APK..."
buildozer android debug --verbose

echo "构建完成！"
ls -la bin/*.apk 2>/dev/null || echo "检查上方是否有错误"
