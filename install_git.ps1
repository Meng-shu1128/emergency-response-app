Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Git 自动安装脚本" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$gitPath = Get-Command git -ErrorAction SilentlyContinue

if ($gitPath) {
    Write-Host "[OK] Git 已安装！" -ForegroundColor Green
    & git --version
    Write-Host ""
    Write-Host "您可以直接使用 Git 命令了。" -ForegroundColor Green
    Read-Host "按 Enter 键退出..."
    exit 0
}

Write-Host "[!] Git 未安装，开始安装..." -ForegroundColor Red
Write-Host ""

$wingetAvailable = Get-Command winget -ErrorAction SilentlyContinue

if ($wingetAvailable) {
    Write-Host "[OK] winget 可用，开始安装 Git..." -ForegroundColor Green
    Write-Host ""
    
    try {
        winget install --id Git.Git -e --source winget --accept-source-agreements --accept-package-agreements
        Write-Host ""
        Write-Host "[OK] Git 安装成功！" -ForegroundColor Green
        Write-Host ""
        Write-Host "请关闭此窗口并重新打开新的 PowerShell 来使用 Git。" -ForegroundColor Yellow
        Read-Host "按 Enter 键退出..."
        exit 0
    } catch {
        Write-Host "[!] winget 安装失败，尝试手动下载..." -ForegroundColor Red
        Write-Host ""
    }
}

Write-Host "[3] 下载 Git 安装程序程序..." -ForegroundColor Yellow
Write-Host ""

$gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.52.0.windows.1/Git-2.52.0-64-bit.exe"
$gitInstaller = "Git-2.52.0-64-bit.exe"
$tempPath = $env:TEMP
$downloadPath = Join-Path $tempPath $gitInstaller

Write-Host "正在下载 $gitInstaller..."
Write-Host "下载地址: $gitUrl"
Write-Host ""

try {
    Invoke-WebRequest -Uri $gitUrl -OutFile $downloadPath -UseBasicParsing
    
    if (Test-Path $downloadPath) {
        Write-Host "[OK] 下载完成！" -ForegroundColor Green
        Write-Host ""
        
        Write-Host "[4] 安装 Git..." -ForegroundColor Yellow
        Write-Host "正在运行 Git 安装程序..."
        Write-Host ""
        
        Start-Process -FilePath $downloadPath -ArgumentList "/VERYSILENT /NORESTART /NOREBOOT" -Wait
        
        Write-Host ""
        Write-Host "============================================" -ForegroundColor Cyan
        Write-Host "安装完成！" -ForegroundColor Green
        Write-Host "============================================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "重要提示：" -ForegroundColor Yellow
        Write-Host "1. 请关闭此窗口" -ForegroundColor White
        Write-Host "2. 重新打开新的命令提示符或 PowerShell" -ForegroundColor White
        Write-Host "3. 运行: git --version 验证安装" -ForegroundColor White
        Write-Host ""
        Read-Host "按 Enter 键退出..."
    } else {
        Write-Host "[!] 下载失败！" -ForegroundColor Red
        Write-Host ""
        Write-Host "请手动下载并安装 Git：" -ForegroundColor Yellow
        Write-Host "1. 访问: https://git-scm.com/download/win" -ForegroundColor White
        Write-Host "2. 下载 Git for Windows" -ForegroundColor White
        Write-Host "3. 运行安装程序" -ForegroundColor White
        Write-Host ""
        Read-Host "按 Enter 键退出..."
    }
} catch {
    Write-Host "[!] 下载失败: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "请手动下载并安装 Git：" -ForegroundColor Yellow
    Write-Host "1. 访问: https://git-scm.com/download/win" -ForegroundColor White
    Write-Host "2. 下载 Git for Windows" -ForegroundColor White
    Write-Host "3. 运行安装程序" -ForegroundColor White
    Write-Host ""
    Read-Host "按 Enter 键退出..."
}
