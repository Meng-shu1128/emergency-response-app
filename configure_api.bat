@echo off
chcp 65001 >nul
echo ============================================================
echo         应急响应系统 - API快速配置工具
echo ============================================================
echo.
echo 此脚本将帮助您快速配置API密钥
echo.
echo 请选择配置方式：
echo   1. 使用Python交互式配置工具
echo   2. 直接编辑 .env 文件
echo   3. 查看当前配置
echo   4. 退出
echo.
set /p choice="请输入选项 (1-4): "

if "%choice%"=="1" goto interactive
if "%choice%"=="2" goto edit_file
if "%choice%"=="3" goto show_config
if "%choice%"=="4" goto end
goto invalid

:interactive
echo.
echo 启动Python交互式配置工具...
python quick_setup_api.py
goto end

:edit_file
echo.
echo 正在打开 .env 文件...
notepad .env
echo.
echo 编辑完成后，请重启应用使配置生效
goto end

:show_config
echo.
echo 当前配置：
echo ------------------------------------------------------------
if exist .env (
    findstr /C:"MAP_API_KEY" .env
    findstr /C:"WEATHER_API_KEY" .env
    findstr /C:"SMS_API_KEY" .env
    findstr /C:"NOTIFICATION_API_KEY" .env
) else (
    echo 错误：找不到 .env 文件
)
echo ------------------------------------------------------------
goto end

:invalid
echo.
echo 无效选项，请重新运行脚本
goto end

:end
echo.
echo 感谢使用！
echo.
pause
