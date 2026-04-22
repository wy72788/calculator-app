# Calculator App - 构建说明

这是你的 Kivy 计算器APP项目。

## 快速构建方案（推荐）

### 方案1：Termux 手机运行（最简单）
1. 手机下载 **Termux** APP
2. 运行:
```bash
pkg install python
pip install kivy
cd storage/shared
mkdir calculator
cd calculator
# 把 main.py 复制到这里
python main.py
```

### 方案2：GitHub Actions 自动构建（生成APK）

1. 把 `calculator_app` 文件夹上传到你的 GitHub 仓库
2. 打开 Actions，点击 "Build Calculator APK"
3. 点击 "Run workflow"
4. 等待完成后下载 APK

### 方案3：本地构建（需要 Linux/Mac）

```bash
# 安装 buildozer
pip install buildozer

# 进入目录
cd calculator_app

# 初始化
buildozer init

# 构建
buildozer android debug
```

## 文件说明
- `main.py` - Kivy 计算器源码
- `buildozer.spec` - 构建配置
- `.github/workflows/build.yml` - GitHub Actions 配置