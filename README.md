# 贪吃蛇 APK 打包指南

## 🚀 推荐方法：GitHub Actions（最简单，无需配置环境）

### 1. 创建 GitHub 仓库
1. 访问 https://github.com/new
2. 创建新仓库（比如叫 `snake-game`）
3. 不要初始化 README

### 2. 上传代码
在项目文件夹打开终端/PowerShell：
```bash
cd C:\Users\asus\.qclaw\workspace\snake_kivy

# 初始化 git
git init
git add .
git commit -m "Initial commit"

# 关联远程仓库（替换为你的用户名）
git remote add origin https://github.com/你的用户名/snake-game.git
git branch -M main
git push -u origin main
```

### 3. 自动构建
- 推送后，GitHub 会自动开始构建
- 进入仓库 → Actions 页面查看进度
- 约 15-30 分钟后，在 Actions 页面下载 APK

### 4. 获取 APK
构建完成后，会自动创建 Release，你可以直接下载 APK 安装包！

---

## 🖥️ 本地构建方法（WSL2）

如果你已经在 WSL 中，运行这个安装脚本：

```bash
# 在 WSL Ubuntu 中
cd /mnt/c/Users/asus/.qclaw/workspace/snake_kivy
bash install_buildozer.sh

# 重新加载配置
source ~/.bashrc

# 开始打包
bash ~/build_apk.sh
```

首次构建会下载约 2GB 的 Android SDK/NDK，耗时 30-60 分钟。

---

## 📱 文件说明

```
snake_kivy/
├── main.py              # 游戏主程序
├── buildozer.spec       # 打包配置
├── requirements.txt     # Python依赖
├── install_buildozer.sh # WSL安装脚本
├── .github/
│   └── workflows/
│       └── build.yml    # GitHub自动构建配置
└── README.md            # 本文件
```

---

## 🎮 游戏特点

- ✅ 触屏滑动控制
- ✅ 支持键盘方向键/WASD
- ✅ 四级难度选择
- ✅ 粒子特效
- ✅ 分数记录

---

## ❓ 常见问题

**Q: 构建失败怎么办？**
A: 在 WSL 中运行 `buildozer android clean` 后重试

**Q: APK 安装失败？**
A: 确保手机允许"安装未知来源应用"

**Q: 游戏闪退？**
A: 检查手机 Android 版本是否 >= 5.0

---

## 🔧 修改配置

编辑 `buildozer.spec` 可自定义：
- 应用名称
- 包名
- 版本号
- 图标
- 权限等
