[app]
# 应用标题
title = 贪吃蛇

# 包名
package.name = snakegame

# 包域名
package.domain = org.example

# 源码目录
source.dir = .

# 主程序文件
source.include_exts = py,png,jpg,kv,atlas

# 版本号
version = 1.0.0

# 应用要求
requirements = python3,kivy

# 应用图标（可选）
# icon.filename = %(source.dir)s/icon.png

# 应用启动画面（可选）
# presplash.filename = %(source.dir)s/presplash.png

# 应用方向
orientation = portrait

# 全屏模式
fullscreen = 0

# Android 特定配置
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33

# 权限
android.permissions = INTERNET

# 架构
android.archs = arm64-v8a, armeabi-v7a

# 日志级别
android.logcat_filters = *:S python:D

# 应用主题
android.apptheme = "@android:style/Theme.NoTitleBar"

[buildozer]
# 日志级别
log_level = 2

# 警告模式
warn_on_root = 1
