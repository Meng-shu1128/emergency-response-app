# Git 快速安装指南

## 问题诊断

您的系统上没有安装 Git，导致无法执行 `git push` 命令。

## 解决方案

### 方案1：手动下载并安装 Git（推荐）

1. **下载 Git**
   - 访问：https://git-scm.com/download/win
   - 点击 "Download for Windows"
   - 选择 64-bit 版本（推荐）
   - 下载文件：`Git-2.52.0-64-bit.exe`

2. **安装 Git**
   - 运行下载的安装程序
   - 选择 "Git from the command line"
   - 选择 "Use Git from the Windows Command Prompt"
   - 点击 "Install"
   - 等待安装完成

3. **重启终端**
   - 关闭当前的 PowerShell 或命令提示符
   - 重新打开新的 PowerShell 或命令提示符

4. **验证安装**
   ```powershell
   git --version
   ```
   
   如果安装成功，会显示：
   ```
   git version 2.52.0.windows.1
   ```

### 方案2：使用 winget 安装（需要网络）

打开 PowerShell（管理员权限），运行：

```powershell
winget install --id Git.Git -e --source winget --accept-source-agreements --accept-package-agreements
```

### 方案3：使用 Chocolatey 安装

如果您已安装 Chocolatey：

```powershell
choco install git
```

## 安装后的配置

### 1. 配置用户信息

```powershell
git config --global user.name "您的用户名"
git config --global user.email "您的邮箱@example.com"
```

### 2. 配置默认分支名

```powershell
git config --global init.defaultBranch main
```

### 3. 初始化项目仓库

```powershell
# 进入项目目录
cd D:\meng\Desktop\app

# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 创建初始提交
git commit -m "初始化项目"
```

### 4. 连接到 GitHub

1. 在 GitHub 创建新仓库：`emergency-response-app`
2. 添加远程仓库：

```powershell
git remote add origin https://github.com/YOUR_USERNAME/emergency-response-app.git
```

### 5. 推送到 GitHub

```powershell
git push -u origin main
```

## 部署到 Streamlit Cloud

1. **确保代码已推送到 GitHub**
   ```powershell
   git add .
   git commit -m "准备部署"
   git push
   ```

2. **在 Streamlit Cloud 部署**
   - 访问：https://share.streamlit.io
   - 点击 "New app"
   - 选择 "From GitHub"
   - 选择您的仓库
   - 点击 "Deploy"

## 常见问题

### Q: winget 安装失败

**A**: 使用方案1手动下载并安装 Git。

### Q: 安装后 git 命令仍无法识别

**A**: 
1. 完全关闭所有终端窗口
2. 重新打开新的 PowerShell 或命令提示符
3. 运行 `git --version` 验证

### Q: 推送时提示认证错误

**A**: 
1. 在 GitHub 设置个人访问令牌（Personal Access Token）
2. 或使用 SSH 密钥连接

## 参考资源

- [Git 官方网站](https://git-scm.com/)
- [GitHub 文档](https://docs.github.com/)
- [GIT_SETUP_GUIDE.md](file:///d:\meng\Desktop\app\GIT_SETUP_GUIDE.md) - 完整 Git 指南
- [DEPLOYMENT_GUIDE.md](file:///d:\meng\Desktop\app\DEPLOYMENT_GUIDE.md) - 部署指南

## 快速检查清单

- [ ] Git 已安装（运行 `git --version` 验证）
- [ ] Git 已配置用户信息
- [ ] 项目已初始化为 Git 仓库
- [ ] 已连接到 GitHub 远程仓库
- [ ] 代码已推送到 GitHub
- [ ] 可以在 Streamlit Cloud 中看到仓库

完成所有步骤后，您就可以成功部署到 Streamlit Cloud 了！
