# 腾讯云函数部署指南

## 📋 部署前准备

✅ **已完成的项目：**
- [x] 应用代码已开发完成
- [x] 所有bug已修复
- [x] 代码已推送到GitHub仓库
- [x] requirements.txt 已配置
- [x] .streamlit/config.toml 已配置
- [x] .gitignore 已配置（保护敏感信息）
- [x] main.py 已配置
- [x] index.py 已创建（腾讯云函数入口）

## 🚀 腾讯云函数部署步骤

### 步骤1：注册腾讯云账号

1. 访问腾讯云控制台：https://console.cloud.tencent.com/
2. 注册/登录账号
3. 进入"云函数"服务

### 步骤2：创建云函数

1. 点击"新建"按钮
2. 选择"从头新建"
3. 填写函数信息：
   - **函数名称**：emergency-response-app
   - **运行环境**：Python 3.7
   - **函数代码**：选择"在线编辑"或"上传ZIP包"
   - **执行方法**：index.main

### 步骤3：配置函数代码

#### 方式1：在线编辑（适合快速测试）

1. 在"函数代码"标签页
2. 创建以下文件结构：

```
emergency-response-app/
├── index.py          # 入口文件
├── main.py           # 主应用文件
├── requirements.txt   # 依赖包
├── .streamlit/
│   └── config.toml  # Streamlit配置
├── pages/            # 页面模块
│   ├── dashboard.py
│   ├── elderly_page.py
│   ├── knowledge_base.py
│   └── settings.py
└── utils/             # 工具模块
    ├── alert_simulator.py
    ├── config_manager.py
    ├── dashboard_analytics.py
    ├── database.py
    ├── map_component.py
    ├── notification_system.py
    ├── risk_assessment.py
    └── voice_player.py
```

3. 将所有文件内容复制到在线编辑器中

#### 方式2：上传ZIP包（推荐）

1. 在本地打包项目：
   ```bash
   # 排除不必要的文件
   cd d:\meng\Desktop\app
   zip -r emergency-response-app.zip . -x "*.git*" -x "*.db" -x "*.log" -x ".env"
   ```

2. 在云函数控制台选择"上传ZIP包"
3. 上传 `emergency-response-app.zip`

### 步骤4：配置函数触发器

1. 在"触发管理"标签页
2. 点击"创建触发器"
3. 选择"API网关触发器"
4. 配置触发器：
   - **触发器名称**：streamlit-api
   - **鉴权方式**：免鉴权（测试用）或API密钥鉴权（生产用）
   - **请求方法**：ANY
   - **路径**：/

### 步骤5：配置环境变量（可选）

1. 在"函数配置"标签页
2. 找到"环境变量"部分
3. 添加以下环境变量：

```
STREAMLIT_SERVER_PORT=9000
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

4. 如果有API密钥，也可以添加：

```
MAP_API_KEY=your_map_api_key_here
WEATHER_API_KEY=your_weather_api_key_here
SMS_API_KEY=your_sms_api_key_here
NOTIFICATION_API_KEY=your_notification_api_key_here
```

### 步骤6：配置内存和超时

1. 在"函数配置"标签页
2. 设置运行配置：
   - **内存**：512MB 或 1024MB
   - **超时时间**：60秒 或更长（根据需要）

## 📊 部署后的访问

部署成功后，您将获得一个API网关URL，格式如下：

```
https://service-xxx.gz.apigw.tencentcloudapi.com/release/
```

## ⚙️ index.py 说明

`index.py` 是腾讯云函数的入口文件，主要功能：

1. **设置环境变量**
   - STREAMLIT_SERVER_PORT=9000
   - STREAMLIT_SERVER_ADDRESS=0.0.0.0

2. **设置Python路径**
   - 将当前目录添加到sys.path
   - 确保可以导入main.py

3. **启动Streamlit应用**
   - 导入main.py中的main函数
   - 调用main函数启动应用

## 🔧 常见问题

### Q1: 部署后无法访问
**A:** 
- 检查API网关触发器是否配置正确
- 确认函数状态为"运行中"
- 查看函数日志检查错误

### Q2: 导入模块错误
**A:**
- 确认所有依赖都在requirements.txt中
- 检查文件结构是否正确
- 查看函数日志中的具体错误信息

### Q3: 数据库文件无法创建
**A:**
- 腾讯云函数的文件系统是只读的
- 需要使用腾讯云数据库（如TDSQL）或对象存储
- 修改database.py以使用云数据库

### Q4: 静态文件无法加载
**A:**
- 将静态文件（图片、音频）上传到腾讯云COS
- 修改代码中的文件路径为COS URL

### Q5: 内存不足错误
**A:**
- 在函数配置中增加内存分配
- 优化代码减少内存使用
- 考虑使用异步处理

## 📝 数据库迁移（重要）

由于腾讯云函数的文件系统是只读的，需要将SQLite数据库迁移到云数据库：

### 方案1：使用腾讯云TDSQL（推荐）

1. 创建TDSQL MySQL实例
2. 修改 `utils/database.py` 使用MySQL连接
3. 更新requirements.txt添加pymysql依赖

### 方案2：使用腾讯云COS + 本地缓存

1. 将数据库文件上传到COS
2. 下载到临时目录使用
3. 定期将更改上传回COS

### 方案3：使用腾讯云API网关 + 云数据库

1. 使用云数据库存储数据
2. 通过API网关访问数据
3. 实现完整的无服务器架构

## 🔄 更新应用

当您需要更新应用时：

1. **修改本地代码**
   ```bash
   # 编辑代码文件
   ```

2. **提交到Git**
   ```bash
   git add .
   git commit -m "更新说明"
   git push
   ```

3. **更新云函数**
   - 方式1：在在线编辑器中更新文件
   - 方式2：重新打包并上传ZIP包

## 📊 监控和日志

在腾讯云函数控制台中，您可以：

- 查看函数运行状态
- 查看实时日志
- 查看监控指标（调用次数、错误率等）
- 设置告警规则
- 查看API网关访问日志

## 💡 最佳实践

1. **使用版本控制**
   - 为每个部署创建新版本
   - 支持快速回滚

2. **配置环境变量**
   - 使用不同的环境变量区分开发/生产环境
   - 不要在代码中硬编码敏感信息

3. **监控和告警**
   - 设置函数错误告警
   - 监控API网关访问量
   - 定期查看日志

4. **性能优化**
   - 使用适当的内存配置
   - 优化数据库查询
   - 使用缓存减少计算

## 🎯 部署完成

恭喜！您的应急响应系统已成功部署到腾讯云函数！

现在您可以：
- 通过API网关URL访问应用
- 分享给团队成员使用
- 随时更新应用
- 监控应用运行状态

---

## 📞 需要帮助？

如果遇到部署问题，请：
1. 查看腾讯云函数日志
2. 检查函数配置
3. 参考腾讯云文档：https://cloud.tencent.com/document/product/583
4. 查看Streamlit文档：https://docs.streamlit.io/

---

**部署日期：** 2026-01-31
**应用名称：** 应急响应系统
**云函数名称：** emergency-response-app
**运行环境：** Python 3.7
