#!/bin/bash
# 手动创建 buildozer 环境

echo "正在创建 buildozer 环境..."

# 1. 确保目录存在
mkdir -p ~/buildozer_env

# 2. 创建虚拟环境
cd ~
python3 -m venv buildozer_env

# 3. 检查是否成功
if [ -f ~/buildozer_env/bin/activate ]; then
    echo "✅ 虚拟环境创建成功！"
    
    # 4. 激活并安装
    source ~/buildozer_env/bin/activate
    echo "正在安装 buildozer..."
    pip install --upgrade pip
    pip install buildozer cython
    
    echo ""
    echo "✅ 安装完成！"
    echo ""
    echo "现在可以运行："
    echo "  cd /mnt/c/Users/asus/.qclaw/workspace/snake_kivy"
    echo "  source ~/buildozer_env/bin/activate"
    echo "  buildozer android debug"
else
    echo "❌ 虚拟环境创建失败"
fi
