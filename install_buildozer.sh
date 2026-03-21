#!/bin/bash
# 安装脚本 - 在 WSL Ubuntu 中运行

# 1. 安装系统依赖
echo "安装系统依赖..."
sudo apt update
sudo apt install -y python3-pip python3-venv python3-full git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev automake

# 2. 创建虚拟环境
echo "创建 Python 虚拟环境..."
cd ~
python3 -m venv buildozer_env
source buildozer_env/bin/activate

# 3. 安装 buildozer 和依赖
echo "安装 buildozer..."
pip install --upgrade pip
pip install buildozer cython kivy

# 4. 设置环境变量
echo 'export PATH="$HOME/buildozer_env/bin:$PATH"' >> ~/.bashrc
echo 'alias buildozer="$HOME/buildozer_env/bin/buildozer"' >> ~/.bashrc

# 5. 创建打包脚本
cat > ~/build_apk.sh << 'EOF'
#!/bin/bash
# APK 打包脚本

# 激活虚拟环境
source ~/buildozer_env/bin/activate

# 进入项目目录（修改为你的实际路径）
cd /mnt/c/Users/asus/.qclaw/workspace/snake_kivy

# 清理旧构建
# buildozer android clean

# 开始构建
echo "开始构建 APK..."
buildozer android debug

echo "构建完成！APK 位置:"
ls -la bin/*.apk 2>/dev/null || echo "构建可能失败，请检查错误信息"
EOF

chmod +x ~/build_apk.sh

echo ""
echo "============================================"
echo "安装完成！"
echo "============================================"
echo ""
echo "使用方法:"
echo "1. 先激活环境: source ~/buildozer_env/bin/activate"
echo "2. 然后打包:   ~/build_apk.sh"
echo ""
echo "或者直接运行:"
echo "  bash ~/build_apk.sh"
echo ""
