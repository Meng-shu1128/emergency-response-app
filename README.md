# 应急响应系统

基于Python和Streamlit的多页面应急响应Web应用。

## 项目结构

```
app/
├── main.py                 # 主应用入口文件
├── requirements.txt        # Python依赖包
├── .env.example           # 环境变量配置示例
├── pages/                 # 页面模块
│   ├── elderly_page.py    # 老人端模拟界面
│   ├── dashboard.py       # 后台仪表盘
│   ├── knowledge_base.py  # 知识库管理
│   └── settings.py        # 系统设置
├── utils/                 # 工具模块
│   └── database.py        # 数据库操作
└── data/                  # 数据存储目录
    ├── emergency_response.db  # SQLite数据库
    └── knowledge_base.json     # 知识库数据
```

## 功能特性

### 1. 老人端模拟界面
- 用户信息注册和更新
- 发起紧急求助（支持自定义描述和位置）
- 快捷求助按钮（医疗急救、火灾报警、治安求助）
- 风险等级选择（低、中、高）

### 2. 后台仪表盘
- 实时统计数据展示（用户数、求助数、待处理、已解决、高风险）
- 求助列表管理（支持状态筛选）
- 求助详情查看和处理
- 响应日志记录
- 状态更新（待处理→处理中→已解决）

### 3. 知识库管理
- 紧急联系人管理
- 应急流程管理
- 资源链接管理
- 数据增删改查

### 4. 系统设置
- API密钥配置
- 用户管理
- 数据导出（CSV/JSON格式）
- 数据库重置

## 数据库设计

### users 表
- id: 用户ID（主键）
- name: 姓名
- phone: 电话
- address: 地址
- emergency_contact: 紧急联系人
- created_at: 创建时间

### alerts 表
- id: 求助ID（主键）
- user_id: 用户ID（外键）
- alert_time: 求助时间
- location_lat: 纬度
- location_lng: 经度
- status: 状态
- risk_level: 风险等级
- description: 描述

### response_logs 表
- id: 日志ID（主键）
- alert_id: 求助ID（外键）
- responder: 响应人员
- action_time: 操作时间
- action_type: 操作类型
- notes: 备注

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填入实际的API密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件：
```
API_KEY=your_api_key_here
MAP_API_KEY=your_map_api_keyKey_here
SMS_API_KEY=your_sms_api_key_here
NOTIFICATION_API_KEY=your_notification_api_key_here
```

### 3. 运行应用

```bash
streamlit run main.py
```

应用将在浏览器中打开，默认地址为 `http://localhost:8501`

## 技术栈

- **前端框架**: Streamlit
- **数据库**: SQLite
- **数据处理**: Pandas
- **环境变量管理**: python-dotenv
- **导航组件**: streamlit-navigation-bar

## 使用说明

1. 首次运行时，系统会自动创建数据库和必要的表结构
2. 在"老人端模拟界面"注册用户信息
3. 发起紧急求助或使用快捷求助按钮
4. 在"后台仪表盘"查看和处理求助
5. 在"知识库管理"添加紧急联系人和应急流程
6. 在"系统设置"配置API密钥和管理数据

## 注意事项

- 确保Python版本 >= 3.8
- 首次运行前请安装所有依赖
- 生产环境部署时请配置适当的安全措施
- 定期备份数据库文件
