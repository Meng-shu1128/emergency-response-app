@echo off
chcp 65001 >nul
echo ============================================
echo Git 自动安装脚本
echo ============================================
echo.

echo [1] 检查 Git 是否已安装...
where git >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Git 已安装！
    git --version
    echo.
    echo 您可以继续使用 Git 命令了。
    pause
    exit /b 0
)

echo [!] Git 未安装，开始安装...
echo.

echo [2] 检查 winget 是否可用...
winget --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] winget 可用，开始安装 Git...
    winget install --id Git.Git -e --source winget --accept-source-agreements --accept-package-agreements
    if %errorlevel% equ 0 (
        echo [OK] Git 安装成功！
        echo.
        echo 请关闭此窗口并重新打开新的命令提示符或 PowerShell 来使用 Git。
        pause
        exit /b 0
    ) else (
        echo [!] winget 安装失败，尝试手动下载...
    )
)

echo [3] 下载 Git 安装程序...
echo.
set GIT_URL=https://github.com/git-for-windows/git/releases/download/v2.52.0.windows.1/Git-2.52.0-64-bit.exe
set GIT_INSTALLER=Git-2.52.0-64-bit.exe

echo 正在下载 %GIT_INSTALLER%...
echo 下载地址: %GIT_URL%
echo.

powershell -Command "& {Invoke-WebRequest -Uri '%GIT_URL%' -OutFile '%GIT_INSTALLER%'}"

if not exist "%GIT_INSTALLER%" (
    echo [!] 下载失败！
    echo.
    echo 请手动下载并安装 Git：
    echo 1. 访问: https://git-scm.com/download/win
    echo 2. 下载 Git for Windows
    echo 3. 运行安装程序
    echo.
    pause
    exit /b 1
)

echo [OK] 下载完成！
echo.

echo [4] 安装 Git...
echo.
echo 正在运行 Git 安装程序...
echo.
start /wait "" "%GIT_INSTALLER%" /VERYSILENT /NORESTART /NOREBOOT

echo.
echo ============================================
echo 安装完成！
echo ============================================
echo.
echo 重要提示：
echo 1. 请关闭此窗口
echo 2. 重新打开新的命令提示符或 PowerShell
echo 3. 运行: git --version 验证安装
echo.
pause
