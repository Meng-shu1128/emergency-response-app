# Vercel 部署指南

## 📋 部署前检查清单

✅ **已完成的项目：**
- [x] 创建vercel.json配置文件
- [x] 简化requirements.txt，只保留必需依赖
- [x] 修改main.py，确保可以直接运行
- [x] 确保所有文件路径使用相对路径
- [x] 添加runtime.txt文件（python-3.9）
- [x] 代码已推送到GitHub仓库

## 🚀 部署步骤

### 步骤1：注册Vercel账号

1. 访问 Vercel：https://vercel.com/
2. 点击"Sign up"注册账号
3. 使用GitHub账号登录（推荐）
4. 授权Vercel访问您的GitHub仓库

### 步骤2：创建新项目

1. 登录后，点击"Add New..."按钮
2. 选择"Project"
3. 选择您的GitHub仓库：`Meng-shu1128/emergency-response-app`
4. 点击"Import"导入项目

### 步骤3：配置项目设置

Vercel会自动检测以下配置文件：

**vercel.json**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ],
  "installCommand": "pip install -r requirements.txt",
  "buildCommand": "echo 'Build complete'",
  "outputDirectory": "."
}
```

**runtime.txt**
```
python-3.9
```

**requirements.txt**
```
streamlit==1.23.1
python-dotenv==0.21.0
pandas==1.3.5
folium==0.13.0
streamlit-folium==0.12.0
plotly==5.11.0
```

### 步骤4：部署项目

1. 点击"Deploy"按钮开始部署
2. Vercel会自动：
   - 安装Python 3.9运行时
   - 安装requirements.txt中的依赖
   - 构建项目
   - 部署到全球CDN

3. 部署过程通常需要1-3分钟
4. 可以在Dashboard中查看部署进度

### 步骤5：配置环境变量（可选）

部署成功后，您可以配置API密钥：

1. 在项目页面点击"Settings"标签
2. 找到"Environment Variables"部分
3. 添加以下环境变量：

```
MAP_API_KEY=your_map_api_key_here
WEATHER_API_KEY=your_weather_api_key_here
SMS_API_KEY=your_sms_api_key_here
NOTIFICATION_API_KEY=your_notification_api_key_here
```

4. 点击"Save"保存
5. 重新部署项目使配置生效

## 📊 部署后的应用

部署成功后，您将获得一个公开的应用URL，格式如下：
```
https://your-project-name.vercel.app
```

## ⚙️ 应用配置说明

### vercel.json
Vercel配置文件：
- 版本：2
- 构建源：main.py
- 运行时：@vercel/python
- 路由：所有请求路由到main.py
- 安装命令：pip install -r requirements.txt
- 输出目录：当前目录

### runtime.txt
Python运行时版本：
- Python 3.9

### requirements.txt
应用依赖的Python包：
- streamlit==1.23.1
- python-dotenv==0.21.0
- pandas==1.3.5
- folium==0.13.0
- streamlit-folium==0.12.0
- plotly==5.11.0

**注意：** 已移除pyttsx3（文本转语音库），因为Vercel不支持音频输出

## 🔧 常见问题

### Q1: 部署失败，提示依赖安装错误
**A:** 检查requirements.txt中的包版本是否兼容Python 3.9

### Q2: 应用启动后显示错误
**A:** 查看Vercel的部署日志，检查具体的错误信息

### Q3: 数据库文件无法创建
**A:** Vercel是只读文件系统，数据库需要使用外部服务（如Vercel Postgres）

### Q4: 地图不显示
**A:** 需要配置MAP_API_KEY环境变量

### Q5: 语音功能不可用
**A:** Vercel不支持音频输出，pyttsx3已从requirements.txt中移除

### Q6: 如何更新应用
**A:**
1. 修改本地代码
2. git add .
3. git commit -m "更新说明"
4. git push
5. Vercel会自动检测并重新部署

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
- ✅ 风险评估工具（基础功能）

### 需要API密钥的功能
- ❌ 地图显示（需要MAP_API_KEY）
- ❌ 天气风险评估（需要WEATHER_API_KEY）
- ❌ 短信通知（需要SMS_API_KEY）
- ❌ APP推送（需要NOTIFICATION_API_KEY）

### Vercel限制的功能
- ❌ 语音安抚功能（Vercel不支持音频输出）
- ❌ 数据库持久化（Vercel是只读文件系统）

## 💡 重要提示

### 数据库问题
Vercel的文件系统是只读的，无法持久化SQLite数据库。解决方案：

1. **使用Vercel Postgres**
   - 在Vercel项目中添加Postgres数据库
   - 修改代码使用Postgres而不是SQLite
   - 需要安装psycopg2库

2. **使用外部数据库服务**
   - Supabase（推荐）
   - Neon
   - PlanetScale

3. **使用内存数据库（仅用于演示）**
   - 数据在应用重启后会丢失
   - 适合演示和测试

### 语音功能问题
Vercel不支持音频输出，pyttsx3库已从requirements.txt中移除。如果需要语音功能：

1. **使用Streamlit Cloud部署**（推荐）
   - Streamlit Cloud支持音频输出
   - 可以使用pyttsx3库

2. **使用文本转语音API**
   - 集成第三方TTS服务
   - 如Azure TTS、Google TTS等

## 📱 访问应用

部署成功后，您可以通过以下方式访问：

1. **Vercel Dashboard**
   - 访问：https://vercel.com/dashboard
   - 查看您的项目列表
   - 点击项目名称访问

2. **直接URL**
   - 格式：https://your-project-name.vercel.app
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
   - Vercel会自动检测GitHub仓库的更改
   - 自动重新部署应用
   - 可以在Dashboard中查看部署状态

## 📊 监控应用

在Vercel Dashboard中，您可以：

- 查看应用运行状态
- 查看访问日志
- 查看错误日志
- 监控资源使用情况
- 管理环境变量
- 查看部署历史
- 配置域名和SSL

## 🎉 部署完成

恭喜！您的应急响应系统已成功部署到Vercel！

现在您可以：
- 通过URL访问应用
- 分享给团队成员使用
- 随时更新应用
- 监控应用运行状态

## 🔄 Streamlit Cloud vs Vercel

| 特性 | Streamlit Cloud | Vercel |
|------|---------------|---------|
| 部署难度 | 简单 | 中等 |
| 免费额度 | 慷 | 慷 |
| 音频支持 | ✅ 支持 | ❌ 不支持 |
| 数据库持久化 | ✅ 支持 | ❌ 需要外部数据库 |
| 自定义域名 | ✅ 支持 | ✅ 支持 |
| 全球CDN | ✅ 支持 | ✅ 支持 |
| 推荐度 | ⭐⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

**建议：** 对于Streamlit应用，推荐使用Streamlit Cloud部署。

---

## 📞 需要帮助？

如果遇到部署问题，请：
1. 查看Vercel的部署日志
2. 检查GitHub仓库状态
3. 参考Vercel文档：https://vercel.com/docs
4. 查看故障排查指南

---

**部署日期：** 2026-01-31
**应用名称：** 应急响应系统
**GitHub仓库：** https://github.com/Meng-shu1128/emergency-response-app.git
**推荐部署平台：** Streamlit Cloud
