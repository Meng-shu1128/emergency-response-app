@echo off
chcp 65001 >nul
echo ============================================
echo Git 仓库初始化脚本
echo ============================================
echo.

echo [1] 查找 Git 可执行文件...
echo.

set GIT_PATH=
if exist "C:\Program Files\Git\cmd\git.exe" (
    set GIT_PATH=C:\Program Files\Git\cmd\git.exe
    echo [OK] 找到 Git: C:\Program Files\Git\cmd\git.exe
) else if exist "C:\Program Files (x86)\Git\cmd\git.exe" (
    set GIT_PATH=C:\Program Files (x86)\Git\cmd\git.exe
    echo [OK] 找到 Git: C:\Program Files (x86)\Git\cmd\git.exe
) else if exist "C:\Program Files\Git\bin\git.exe" (
    set GIT_PATH=C:\Program Files\Git\bin\git.exe
    echo [OK] 找到 Git: C:\Program Files\Git\bin\git.exe
) else if exist "%USERPROFILE%\AppData\Local\Programs\Git\cmd\git.exe" (
    set GIT_PATH=%USERPROFILE%\AppData\Local\Programs\Git\cmd\git.exe
    echo [OK] 找到 Git: %USERPROFILE%\AppData\Local\Programs\Git\cmd\git.exe
) else (
    echo [!] 未找到 Git 可执行文件
    echo.
    echo 请确保 Git 已安装，然后重启此脚本。
    pause
    exit /b 1
)

echo.
echo [2] 验证 Git 版本...
echo.
"%GIT_PATH%" --version
if %errorlevel% neq 0 (
    echo [!] Git 验证失败
    pause
    exit /b 1
)

echo.
echo [3] 配置 Git 用户信息...
echo.

"%GIT_PATH%" config --global user.name "Emergency Response App"
"%GIT_PATH%" config --global user.email "emergency@example.com"

echo [OK] Git 用户信息已配置
echo.

echo [4] 初始化 Git 仓库...
echo.

if exist ".git" (
    echo [!] .git 目录已存在，仓库已初始化
    echo.
    echo 如需重新初始化，请先删除 .git 目录
) else (
    "%GIT_PATH%" init
    echo [OK] Git 仓库已初始化
)

echo.
echo [5] 添加所有文件到 Git...
echo.

"%GIT_PATH%" add .

echo [OK] 文件已添加
echo.

echo [6] 创建初始提交...
echo.

"%GIT_PATH%" commit -m "初始化老人紧急求助响应系统"

if %errorlevel% neq 0 (
    echo [!] 提交失败，可能没有文件可提交
    echo.
    echo 这是正常的，如果您已经提交过
) else (
    echo [OK] 初始提交已创建
)

echo.
echo ============================================
echo Git 仓库初始化完成！
echo ============================================
echo.
echo 下一步：
echo 1. 在 GitHub 创建新仓库
echo 2. 添加远程仓库：
echo    "%GIT_PATH%" remote add origin https://github.com/YOUR_USERNAME/emergency-response-app.git
echo 3. 推送到 GitHub：
echo    "%GIT_PATH%" push -u origin main
echo.
pause
