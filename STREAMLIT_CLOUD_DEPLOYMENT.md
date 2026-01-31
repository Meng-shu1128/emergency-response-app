# Streamlit Cloud 部署指南

## 📋 部署前检查清单

✅ **已完成的项目：**
- [x] 应用代码已开发完成
- [x] 所有bug已修复
- [x] 代码已推送到GitHub仓库
- [x] requirements.txt 已配置
- [x] .streamlit/config.toml 已配置
- [x] .gitignore 已配置（保护敏感信息）
- [x] main.py 已配置

## 🚀 部署步骤

### 步骤1：确认GitHub仓库

您的代码已推送到：
```
https://github.com/Meng-shu1128/emergency-response-app.git
```

### 步骤2：注册Streamlit Cloud账号

1. 访问 Streamlit Cloud：https://share.streamlit.io/
2. 点击"Sign up"注册账号
3. 使用GitHub账号登录（推荐）
4. 授权Streamlit Cloud访问您的GitHub仓库

### 步骤3：创建新应用

1. 登录后，点击"New app"按钮
2. 选择您的GitHub仓库：`Meng-shu1128/emergency-response-app`
3. 选择分支：`main`
4. 主文件路径：`main.py`（默认）
5. 点击"Deploy"开始部署

### 步骤4：配置环境变量（可选）

部署完成后，您可以配置API密钥：

1. 在应用页面点击"Settings"标签
2. 找到"Secrets"部分
3. 添加以下环境变量：

```
MAP_API_KEY=your_map_api_key_here
WEATHER_API_KEY=your_weather_api_key_here
SMS_API_KEY=your_sms_api_key_here
NOTIFICATION_API_KEY=your_notification_api_key_here
```

4. 点击"Save"保存
5. 点击"Rerun"重新启动应用

## 📊 部署后的应用

部署成功后，您将获得一个公开的应用URL，格式如下：
```
https://your-app-name.streamlit.app
```

## ⚙️ 应用配置说明

### requirements.txt
应用依赖的Python包：
- streamlit==1.23.1
- python-dotenv==0.21.0
- pandas==1.3.5
- folium==0.13.0
- streamlit-folium==0.12.0
- pyttsx3==2.90
- plotly==5.11.0

### .streamlit/config.toml
Streamlit配置：
- 端口：8501
- 布局：wide
- 侧边栏：expanded
- 主题：自定义红色主题

### .gitignore
已排除的文件：
- 数据库文件（*.db, *.sqlite）
- 环境变量文件（.env）
- Python缓存（__pycache__）
- 虚拟环境（venv/, env/）

## 🔧 常见问题

### Q1: 部署失败，提示依赖安装错误
**A:** 检查requirements.txt中的包版本是否兼容Python 3.7

### Q2: 应用启动后显示错误
**A:** 查看Streamlit Cloud的日志，检查具体的错误信息

### Q3: 地图不显示
**A:** 需要配置MAP_API_KEY环境变量

### Q4: 天气评估功能不可用
**A:** 需要配置WEATHER_API_KEY环境变量

### Q5: 如何更新应用
**A:** 
1. 修改本地代码
2. git add .
3. git commit -m "更新说明"
4. git push
5. Streamlit Cloud会自动检测并重新部署

## 📝 环境变量配置

### 必需的环境变量（可选）
以下环境变量不是必需的，但配置后可以启用更多功能：

| 变量名 | 用途 | 是否必需 |
|---------|------|---------|
| MAP_API_KEY | 地图显示 | 否 |
| WEATHER_API_KEY | 天气评估 | 否 |
| SMS_API_KEY | 短信通知 | 否 |
| NOTIFICATION_API_KEY | APP推送 | 否 |

### 如何获取API密钥
参考 [API_CONFIG_GUIDE.md](file:///d:\meng\Desktop\app\API_CONFIG_GUIDE.md) 获取详细的API密钥获取指南。

## 🎯 部署后的功能

### 可以正常使用的功能
- ✅ 用户管理
- ✅ 求助记录管理
- ✅ 数据看板
- ✅ 系统设置
- ✅ 老人端模拟界面
- ✅ 语音安抚功能
- ✅ 风险评估工具（基础功能）

### 需要API密钥的功能
- ❌ 地图显示（需要MAP_API_KEY）
- ❌ 天气风险评估（需要WEATHER_API_KEY）
- ❌ 短信通知（需要SMS_API_KEY）
- ❌ APP推送（需要NOTIFICATION_API_KEY）

## 📱 访问应用

部署成功后，您可以通过以下方式访问：

1. **Streamlit Cloud Dashboard**
   - 访问：https://share.streamlit.io/
   - 查看您的应用列表
   - 点击应用名称访问

2. **直接URL**
   - 格式：https://your-app-name.streamlit.app
   - 可以分享给其他人访问

## 🔄 更新应用

当您需要更新应用时：

1. **修改本地代码**
   ```bash
   # 编辑代码文件
   ```

2. **提交更改**
   ```bash
   git add .
   git commit -m "更新说明"
   git push
   ```

3. **自动部署**
   - Streamlit Cloud会自动检测GitHub仓库的更改
   - 自动重新部署应用
   - 可以在Dashboard中查看部署状态

## 📊 监控应用

在Streamlit Cloud Dashboard中，您可以：

- 查看应用运行状态
- 查看访问日志
- 查看错误日志
- 监控资源使用情况
- 管理环境变量
- 删除或重新部署应用

## 🎉 部署完成

恭喜！您的应急响应系统已成功部署到Streamlit Cloud！

现在您可以：
- 通过URL访问应用
- 分享给团队成员使用
- 随时更新应用
- 监控应用运行状态

---

## 📞 需要帮助？

如果遇到部署问题，请：
1. 查看Streamlit Cloud的日志
2. 检查GitHub仓库状态
3. 参考Streamlit Cloud文档：https://docs.streamlit.io/streamlit-cloud/
4. 查看故障排查指南：STREAMLIT_CLOUD_TROUBLESHOOTING.md

---

**部署日期：** 2026-01-31
**应用名称：** 应急响应系统
**GitHub仓库：** https://github.com/Meng-shu1128/emergency-response-app.git
