# Git 安装和配置指南

## 1. 安装 Git

### 方法1：使用 Git for Windows 安装程序（推荐）

1. 访问 [Git 官方网站](https://git-scm.com/download/win)
2. 下载最新版本的 Git for Windows
3. 运行安装程序
4. 安装选项：
   - 选择 "Git from the command line and also from 3rd-party software"
   - 选择 "Use Git from the Windows Command Prompt"
   - 选择 "Checkout Windows-style, commit Unix-style line endings"
   - 选择 "Use MinTTY (the default terminal of MSYS2 Git)"
   - 选择 "Enable file system caching"
   - 选择 "Enable Git Credential Manager"
5. 完成安装后，**重启命令提示符或PowerShell**

### 方法2：使用 Chocolatey 安装

如果您已安装 Chocolatey：

```powershell
choco install git
```

### 方法3：使用 winget 安装（Windows 10/11）

```powershell
winget install --id Git.Git -e --source winget
```

### 方法4：使用 Scoop 安装

```powershell
scoop install git
```

## 2. 验证 Git 安装

打开新的 PowerShell 或命令提示符，运行：

```powershell
git --version
```

如果安装成功，会显示类似：
```
git version 2.43.0.windows.1
```

## 3. 配置 Git

### 3.1 设置用户信息

```powershell
git config --global user.name "您的用户名"
git config --global user.email "您的邮箱@example.com"
```

### 3.2 配置默认分支名（Git 2.28+）

```powershell
git config --global init.defaultBranch main
```

### 3.3 配置换行符（Windows推荐）

```powershell
git config --global core.autocrlf true
```

### 3.4 配置凭证助手

```powershell
git config --global credential.helper manager
```

## 4. 初始化 Git 仓库

### 4.1 如果项目还没有 Git 仓库

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

### 4.2 如果已有 Git 仓库

```powershell
# 进入项目目录
cd D:\meng\Desktop\app

# 查看状态
git status
```

## 5. 连接到 GitHub

### 5.1 创建 GitHub 仓库

1. 登录 [GitHub](https://github.com)
2. 点击右上角的 "+" 号
3. 选择 "New repository"
4. 填写仓库信息：
   - Repository name: `emergency-response-app`
   - Description: `老人紧急求助响应系统`
   - Public/Private: 根据需要选择
5. 点击 "Create repository"

### 5.2 连接本地仓库到 GitHub

```powershell
# 进入项目目录
cd D:\meng\Desktop\app

# 添加远程仓库（替换 YOUR_USERNAME 为您的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/emergency-response-app.git

# 查看远程仓库
git remote -v
```

## 6. 推送代码到 GitHub

### 6.1 首次推送

```powershell
# 推送到 GitHub
git push -u origin main
```

### 6.2 后续推送

```powershell
# 添加修改的文件
git add .

# 提交修改
git commit -m "描述您的修改"

# 推送到 GitHub
git push
```

## 7. 常用 Git 命令

### 查看状态

```powershell
git status
```

### 查看修改内容

```powershell
git diff
```

### 查看提交历史

```powershell
git log --oneline
```

### 创建新分支

```powershell
git checkout -b feature-branch-name
```

### 切换分支

```powershell
git checkout main
```

### 合并分支

```powershell
git checkout main
git merge feature-branch-name
```

### 拉取远程更新

```powershell
git pull origin main
```

### 查看远程仓库

```powershell
git remote -v
```

## 8. .gitignore 配置

创建 `.gitignore` 文件，忽略不需要版本控制的文件：

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# 虚拟环境
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Streamlit
.streamlit/secrets.toml

# 数据库
*.db
*.sqlite
*.sqlite3

# 环境变量
.env
.env.local

# 日志
*.log

# 临时文件
*.tmp
*.temp
.DS_Store
Thumbs.db

# 静态文件（如果使用CDN）
# static/
```

## 9. 推送到 Streamlit Cloud

### 9.1 确保 GitHub 仓库是最新的

```powershell
cd D:\meng\Desktop\app
git add .
git commit -m "准备部署到Streamlit Cloud"
git push
```

### 9.2 在 Streamlit Cloud 中部署

1. 登录 [Streamlit Cloud](https://share.streamlit.io)
2. 点击 "New app" 或选择现有应用
3. 选择 "From GitHub"
4. 授权 GitHub 访问权限
5. 选择您的仓库：`emergency-response-app`
6. 选择分支：`main`
7. 选择主文件：`main.py`
8. 点击 "Deploy"

## 10. 常见问题

### Q1: git 命令无法识别

**A**: 
1. 确保已安装 Git
2. 重启 PowerShell 或命令提示符
3. 检查 Git 是否在 PATH 中：
   ```powershell
   where git
   ```

### Q2: 推送时提示认证错误

**A**: 
1. 配置 GitHub 凭证助手
2. 使用个人访问令牌（Personal Access Token）
3. 或使用 SSH 密钥

### Q3: .gitignore 不生效

**A**: 
1. 确保文件已提交到仓库
2. 如果文件已提交，先从缓存中移除：
   ```powershell
   git rm --cached filename
   git commit -m "从版本控制中移除文件"
   ```

### Q4: 合并冲突

**A**: 
1. 手动解决冲突
2. 标记为已解决：
   ```powershell
   git add .
   git commit -m "解决合并冲突"
   ```

## 11. Git 工作流最佳实践

### 提交频率
- 频繁提交，每次完成一个小功能
- 提交信息清晰，使用中文或英文
- 提交信息格式：`类型: 简短描述`

### 分支策略
- `main` - 生产环境，稳定代码
- `develop` - 开发环境
- `feature/*` - 新功能开发
- `bugfix/*` - 错误修复

### 代码审查
- 使用 Pull Request 合并代码
- 代码审查后再合并到主分支

## 12. 快速参考

### Git 官方文档
- [Git 官方网站](https://git-scm.com/)
- [Git 参考手册](https://git-scm.com/docs)
- [Pro Git 书籍](https://git-scm.com/book/en/v2)

### GitHub 文档
- [GitHub 指南](https://docs.github.com/)
- [GitHub 工作流](https://docs.github.com/en/get-started/quickstart)

### Streamlit Cloud 文档
- [Streamlit Cloud 部署](https://docs.streamlit.io/deploy/streamlit-cloud)
