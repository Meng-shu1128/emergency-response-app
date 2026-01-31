# Streamlit Cloud 部署指南

## 1. requirements.txt 完整内容

```txt
streamlit==1.23.1
python-dotenv==0.21.0
pandas==1.3.5
folium==0.12.1
streamlit-folium==0.12.0
pyttsx3==2.90
plotly==5.11.0
```

### 依赖说明

| 包名 | 版本 | 用途 |
|------|------|------|
| streamlit | 1.23.1 | Web应用框架 |
| python-dotenv | 0.21.0 | 环境变量管理 |
| pandas | 1.3.5 | 数据处理 |
| folium | 0.12.1 | 地图可视化 |
| streamlit-folium | 0.12.0 | Streamlit与Folium集成 |
| pyttsx3 | 2.90 | 文本转语音 |
| plotly | 5.11.0 | 交互式图表 |

### 安装依赖

```bash
pip install -r requirements.txt
```

## 2. .streamlit/config.toml 配置

```toml
[server]
port = 8501
headless = true
runOnSave = true
fileWatcherType = "poll"
maxUploadSize = 200

[browser]
gatherUsageStats = false
serverAddress = "localhost"
showErrorDetails = true

[client]
showErrorDetails = true
toolbarMode = "minimal"
maxCachedMessageAge = 0

[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[logger]
level = "info"

[client.ui]
mode = "wide"

[runner]
fastReruns = false
```

### 配置说明

#### [server] 服务器配置
- `port`: 应用运行端口（本地开发用，Cloud部署时忽略）
- `headless`: 无头模式运行（Cloud部署必须为true）
- `runOnSave`: 保存时自动重新运行
- `fileWatcherType`: 文件监视类型（"poll"更稳定）
- `maxUploadSize`: 最大上传大小（MB）

#### [browser] 浏览器配置
- `gatherUsageStats`: 是否收集使用统计（false保护隐私）
- `serverAddress`: 服务器地址
- `showErrorDetails`: 显示错误详情

#### [client] 客户端配置
- `showErrorDetails`: 显示错误详情
- `toolbarMode`: 工具栏模式（"minimal"更简洁）
- `maxCachedMessageAge`: 最大缓存消息年龄（0禁用）

#### [theme] 主题配置
- `primaryColor`: 主色调（#FF4B4B 红色）
- `backgroundColor`: 背景色（#FFFFFF 白色）
- `secondaryBackgroundColor`: 次要背景色（#F0F2F6 浅蓝）
- `textColor`: 文字颜色（#262730 深灰）
- `font`: 字体（"sans serif" 无衬线字体）

#### [logger] 日志配置
- `level`: 日志级别（"info"）

#### [client.ui] UI配置
- `mode`: UI模式（"wide"宽屏模式）

#### [runner] 运行器配置
- `fastReruns`: 快速重新运行（false避免频繁重载）

## 3. 设置环境变量的方法

### 方法1：使用 .env 文件（推荐）

创建 `.env` 文件：

```env
# Streamlit配置
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=true

# 应用配置
APP_TITLE=老人紧急求助系统
APP_VERSION=1.0.0

# 数据库配置
DB_PATH=./data/emergency_response.db

# 地图配置
MAP_CENTER_LAT=39.9042
MAP_CENTER_LNG=116.4074
MAP_DEFAULT_ZOOM=10

# 语音配置
VOICE_RATE=200
VOICE_VOLUME=1.0

# 通知配置
NOTIFICATION_RETRY_INTERVAL=300
NOTIFICATION_MAX_RETRIES=3

# 缓存配置
CACHE_TTL_SHORT=30
CACHE_TTL_MEDIUM=120
CACHE_TTL_LONG=300
```

### 方法2：在 Streamlit Cloud 中设置

1. 登录 [Streamlit Cloud](https://share.streamlit.io)
2. 创建新应用或选择现有应用
3. 进入 "Settings" → "Secrets"
4. 添加环境变量：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `STREAMLIT_SERVER_HEADLESS` | `true` | 无头模式 |
| `DB_PATH` | `./data/emergency_response.db` | 数据库路径 |
| `MAP_CENTER_LAT` | `39.9042` | 地图中心纬度 |
| `MAP_CENTER_LNG` | `116.4074` | 地图中心经度 |
| `MAP_DEFAULT_ZOOM` | `10` | 默认缩放级别 |
| `VOICE_RATE` | `200` | 语音语速 |
| `VOICE_VOLUME` | `1.0` | 语音音量 |
| `NOTIFICATION_RETRY_INTERVAL` | `300` | 通知重试间隔（秒） |
| `NOTIFICATION_MAX_RETRIES` | `3` | 最大重试次数 |

### 方法3：在代码中使用环境变量

```python
import os
from dotenv import load_dotenv

load_dotenv()

MAP_CENTER_LAT = float(os.getenv('MAP_CENTER_LAT', '39.9042'))
MAP_CENTER_LNG = float(os.getenv('MAP_CENTER_LNG', '116.4074'))
MAP_DEFAULT_ZOOM = int(os.getenv('MAP_DEFAULT_ZOOM', '10'))

VOICE_RATE = int(os.getenv('VOICE_RATE', '200'))
VOICE_VOLUME = float(os.getenv('VOICE_VOLUME', '1.0'))
```

### 环境变量优先加载顺序

1. Streamlit Cloud Secrets（最高优先级）
2. .env 文件
3. 系统环境变量
4. 代码中的默认值（最低优先级）

## 4. 处理静态文件的最佳实践

### 4.1 项目结构

```
app/
├── .streamlit/
│   └── config.toml
├── static/
│   ├── images/
│   │   ├── logo.png
│   │   ├── icons/
│   │   │   ├── alert.png
│   │   │   └── user.png
│   │   └── banners/
│   │       └── hero.jpg
│   ├── audio/
│   │   ├── alert_sound.mp3
│   │   ├── notification.wav
│   │   └── emergency.mp3
│   └── css/
│       └── custom.css
├── data/
│   └── emergency_response.db
├── pages/
│   ├── dashboard.py
│   ├── elderly_page.py
│   └── knowledge_base.py
├── utils/
│   ├── database.py
│   ├── map_component.py
│   ├── voice_player.py
│   ├── risk_assessment.py
│   ├── alert_simulator.py
│   ├── dashboard_analytics.py
│   └── notification_system.py
├── main.py
├── requirements.txt
└── .env
```

### 4.2 图片文件处理

#### 图片格式选择

| 格式 | 适用场景 | 优势 | 劣势 |
|------|---------|------|------|
| PNG | 图标、Logo | 无损压缩 | 文件较大 |
| JPEG | 照片、横幅 | 压缩率高 | 有损压缩 |
| WebP | 现代浏览器 | 最优压缩 | 旧浏览器不支持 |
| SVG | 图标、矢量图 | 无限缩放 | 不适合照片 |

#### 图片优化建议

```python
import streamlit as st

# 使用本地图片
st.image("static/images/logo.png", width=200)

# 使用URL图片（CDN加速）
st.image("https://cdn.example.com/images/logo.png", width=200)

# 使用base64编码（小图标）
import base64
with open("static/images/icon.png", "rb") as f:
    encoded = base64.b64encode(f.read()).decode()
st.markdown(f'<img src="data:image/png;base64,{encoded}" width="50">', unsafe_allow_html=True)
```

#### 图片懒加载

```python
import streamlit as st

# 使用expander实现懒加载
with st.expander("查看详细地图", expanded=False):
    st.image("static/images/map_detail.png", use_column_width=True)
```

### 4.3 音频文件处理

#### 音频格式选择

| 格式 | 适用场景 | 优势 | 劣势 |
|------|---------|------|------|
| MP3 | 通用音频 | 兼容性好 | 专利格式 |
| WAV | 无损音频 | 高质量 | 文件大 |
| OGG | 开源音频 | 无专利 | 兼容性一般 |

#### 音频优化建议

```python
import streamlit as st

# 播放本地音频
st.audio("static/audio/alert_sound.mp3")

# 播放URL音频
st.audio("https://cdn.example.com/audio/notification.mp3")

# 使用自定义音频播放器
st.markdown('''
<audio controls>
    <source src="static/audio/emergency.mp3" type="audio/mpeg">
    您的浏览器不支持音频元素。
</audio>
''', unsafe_allow_html=True)
```

#### 音频文件压缩

使用工具压缩音频文件：

```bash
# 使用ffmpeg压缩MP3
ffmpeg -i input.mp3 -b:a 128k output.mp3

# 使用lame压缩MP3
lame --preset standard input.mp3 output.mp3
```

### 4.4 CSS文件处理

#### 自定义CSS

创建 `static/css/custom.css`：

```css
/* 自定义主题 */
:root {
    --primary-color: #FF4B4B;
    --secondary-color: #F0F2F6;
    --text-color: #262730;
}

/* 优化加载动画 */
.stSpinner {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* 优化按钮样式 */
.stButton > kind {
    transition: all 0.3s ease;
}

.stButton > kind:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* 优化表格样式 */
.stDataFrame {
    font-size: 14px;
}

.stDataFrame th {
    background-color: var(--primary-color);
    color: white;
    padding: 12px;
}

/* 优化卡片样式 */
.stMetric {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* 优化地图容器 */
folium {
    border-radius: 8px;
;
}
```

#### 加载自定义CSS

```python
import streamlit as st

# 方法1：使用st.markdown
with open("static/css/custom.css", "r", encoding="utf-8") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# 方法2：使用st.markdown（推荐）
st.markdown("""
<style>
    .stAppViewContainer {
        max-width: 1200px;
    }
</style>
""", unsafe_allow_html=True)
```

### 4.5 静态文件CDN加速

#### 使用CDN的优势

1. **全球加速**：就近访问，降低延迟
2. **缓存优化**：CDN自动缓存静态资源
3. **带宽节省**：减少服务器负载
4. **高可用性**：多节点冗余

#### CDN配置示例

```python
import streamlit as st

# 使用CDN URL
CDN_BASE_URL = "https://cdn.example.com/static"

# 图片
st.image(f"{CDN_BASE_URL}/images/logo.png")

# 音频
st.audio(f"{CDN_BASE_URL}/audio/alert.mp3")

# CSS
st.markdown(f'<link rel="stylesheet" href="{CDN_BASE_URL}/css/custom.css">', 
            unsafe_allow_html=True)
```

### 4.6 静态文件版本控制

#### 文件版本化

```python
import os

def get_static_url(filename):
    """获取带版本号的静态文件URL"""
    file_path = f"static/{filename}"
    
    if os.path.exists(file_path):
        mtime = os.path.getmtime(file_path)
        version = str(int(mtime))
        return f"{filename}?v={version}"
    
    return filename

# 使用
logo_url = get_static_url("images/logo.png")
st.image(logo_url)
```

## 5. Streamlit Cloud 部署步骤

### 5.1 准备部署

1. **确保所有文件已提交到Git**
```bash
git add .
git commit -m "准备部署到Streamlit Cloud"
git push
```

2. **检查项目结构**
```
app/
├── .streamlit/
│   └── config.toml
├── main.py
├── requirements.txt
└── .env
```

3. **验证本地运行**
```bash
streamlit run main.py
```

### 5.2 部署到Streamlit Cloud

#### 方法1：通过GitHub连接（推荐）

1. 登录 [Streamlit Cloud](https://share.streamlit.io)
2. 点击 "New app"
3. 选择 "From GitHub"
4. 授权Streamlit访问你的GitHub仓库
5. 选择仓库和分支
6. 选择 `main.py` 作为主文件
7. 点击 "Deploy"

#### 方法2：通过本地文件上传

1. 登录 [Streamlit Cloud](https://share.streamlit.io)
2. 点击 "New app"
3. 选择 "From local files"
4. 上传项目文件（支持拖拽）
5. 选择 `main.py` 作为主文件
6. 点击 "Deploy"

### 5.3 配置应用

#### 设置应用信息

1. 进入应用设置
2. 设置应用名称和描述
3. 添加应用图标（上传logo）
4. 设置应用URL

#### 配置环境变量

1. 进入 "Settings" → "Secrets"
2. 添加必要的环境变量
3. 保存更改

#### 配置访问权限

1. 进入 "Settings" → "Access control"
2. 选择访问模式：
   - Public（公开）
   - Private（私有）
   - Password protected（密码保护）

### 5.4 监部署状态

部署过程中，Streamlit Cloud会显示：
- **Building**: 构建应用
- **Installing dependencies**: 安装依赖
- **Running**: 运行应用
- **Deployed**: 部署成功

查看日志：
```bash
# 在Streamlit Cloud界面中
# 点击 "Logs" 查看部署日志
```

## 6. 部署后优化

### 6.1 性能监控

使用Streamlit Cloud内置监控：
- 访问统计
- 资源使用
- 错误日志

### 6.2 缓存优化

启用Streamlit Cloud缓存：
```toml
[client]
maxCachedMessageAge = 0  # 禁用消息缓存
```

### 6.3 错误处理

添加全局错误处理：
```python
import streamlit as st
import traceback

try:
    st.title("老人紧急求助系统")
except Exception as e:
    st.error(f"应用错误: {str(e)}")
    st.code(traceback.format_exc())
```

## 7. 常见问题

### Q1: 部署失败，提示依赖安装错误

**A**: 检查 `requirements.txt` 中的版本是否正确，确保所有依赖都存在。

### Q2: 静态文件无法加载

**A**: 确保静态文件在项目根目录或 `static/` 文件夹中，路径正确。

### Q3: 环境变量不生效

**A**: 确保在Streamlit Cloud的 "Secrets" 中正确设置，变量名和值都正确。

### Q4: 应用运行缓慢

**A**: 
1. 检查是否启用了缓存
2. 减少单次加载的数据量
3. 使用CDN加速静态资源

### Q5: 数据库文件丢失

**A**: Streamlit Cloud是临时环境，每次重启会重置。建议：
1. 使用外部数据库服务
2. 或在应用启动时创建数据库

```python
import os

DB_PATH = os.getenv('DB_PATH', './data/emergency_response.db')

# 确保数据库目录存在
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# 初始化数据库
init_database()
```

## 8. 参考资源

- [Streamlit Cloud文档](https://docs.streamlit.io/streamlit-cloud/get-started)
- [Streamlit配置](https://docs.streamlit.io/library/core/configuration.html)
- [Streamlit部署最佳实践](https://docs.streamlit.io/deploy/streamlit-cloud)
