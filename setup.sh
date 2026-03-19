#!/bin/bash
# 在 WSL Ubuntu 中运行此脚本安装 buildozer

echo "================================"
echo "正在安装 Buildozer 打包环境..."
echo "================================"

# 1. 安装系统依赖
echo ""
echo "[1/4] 安装系统依赖..."
sudo apt update
sudo apt install -y python3-pip python3-venv python3-full git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev automake

# 2. 创建虚拟环境
echo ""
echo "[2/4] 创建 Python 虚拟环境..."
cd ~
python3 -m venv buildozer_env

# 3. 安装 buildozer
echo ""
echo "[3/4] 安装 buildozer..."
source ~/buildozer_env/bin/activate
pip install --upgrade pip
pip install buildozer cython

# 4. 创建快捷命令
echo ""
echo "[4/4] 创建打包脚本..."

cat > ~/build_apk.sh << 'EOF'
#!/bin/bash
# APK 打包脚本

echo "================================"
echo "开始构建贪吃蛇 APK..."
echo "================================"
echo ""

# 激活虚拟环境
source ~/buildozer_env/bin/activate

# 进入项目目录
cd /mnt/c/Users/asus/.qclaw/workspace/snake_kivy

# 开始构建（首次需要下载依赖，约30-60分钟）
echo "正在构建，请耐心等待..."
buildozer android debug

# 检查结果
if [ -f bin/*.apk ]; then
    echo ""
    echo "================================"
    echo "✅ 构建成功！"
    echo "================================"
    echo "APK 文件:"
    ls -lh bin/*.apk
    echo ""
    echo "复制到桌面..."
    cp bin/*.apk /mnt/c/Users/asus/Desktop/
    echo "完成！请在桌面查看 APK 文件"
else
    echo ""
    echo "================================"
    echo "❌ 构建失败"
    echo "================================"
    echo "请检查错误信息"
fi
EOF

chmod +x ~/build_apk.sh

echo ""
echo "================================"
echo "✅ 安装完成！"
echo "================================"
echo ""
echo "使用方法："
echo "  bash ~/build_apk.sh"
echo ""
echo "注意：首次构建需要下载约 2GB 的 Android SDK，"
echo "      请确保网络稳定，耗时约 30-60 分钟"
echo ""
