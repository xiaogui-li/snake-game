#!/bin/bash
# 一键安装并打包

echo "================================"
echo "贪吃蛇 APK 一键打包"
echo "================================"
echo ""

# 检查虚拟环境是否存在
if [ ! -d ~/buildozer_env ]; then
    echo "[1/2] 首次运行，先安装依赖环境..."
    echo ""
    
    # 安装系统依赖
    echo "  → 安装系统依赖 (需要 sudo 密码)..."
    sudo apt update -qq
    sudo apt install -y -qq python3-pip python3-venv python3-full git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev automake
    
    # 创建虚拟环境
    echo "  → 创建 Python 虚拟环境..."
    python3 -m venv ~/buildozer_env
    
    # 安装 buildozer
    echo "  → 安装 buildozer..."
    source ~/buildozer_env/bin/activate
    pip install -q --upgrade pip
    pip install -q buildozer cython
    
    echo ""
    echo "✅ 环境安装完成！"
    echo ""
else
    echo "[1/2] 环境已存在，跳过安装"
    source ~/buildozer_env/bin/activate
fi

# 进入项目目录
cd /mnt/c/Users/asus/.qclaw/workspace/snake_kivy

# 开始构建
echo "[2/2] 开始构建 APK..."
echo "    (首次构建需下载 Android SDK，约 30-60 分钟)"
echo ""

buildozer android debug

# 检查结果
if ls bin/*.apk 1> /dev/null 2>&1; then
    echo ""
    echo "================================"
    echo "✅ 构建成功！"
    echo "================================"
    echo ""
    ls -lh bin/*.apk
    echo ""
    echo "正在复制到桌面..."
    cp bin/*.apk /mnt/c/Users/asus/Desktop/ 2>/dev/null
    echo "✅ APK 已保存到桌面！"
else
    echo ""
    echo "================================"
    echo "❌ 构建失败，请检查错误信息"
    echo "================================"
fi
