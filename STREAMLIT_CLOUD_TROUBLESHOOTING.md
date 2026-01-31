# Streamlit Cloud 部署问题解决指南

## 当前安装状态

从日志来看，Streamlit Cloud正在安装依赖包：

```
Collecting streamlit==1.23.1
Collecting python-dotenv==0.21.0
Collecting pandas==1.3.5 (4.7 MB)
Installing build dependencies: started
Installing build dependencies: finished with status 'done'
```

这是正常的安装过程，请耐心等待。

## 常见部署问题及解决方案

### 问题1：依赖版本冲突

**错误信息**：
```
ERROR: Cannot install -r requirements.txt because these package versions have conflicting dependencies.
```

**解决方案**：

#### 方案A：调整依赖版本（推荐）

修改 `requirements.txt`，使用更宽松的版本约束：

```txt
# 使用版本范围而不是固定版本
streamlit>=1.20.0,<1.24.0
python-dotenv>=0.20.0,<1.0.0
pandas>=1.3.0,<2.0.0
folium>=0.13.0,<0.15.0
streamlit-folium>=0.12.0,<0.13.0
plotly>=5.0.0,<6.0.0

# pyttsx3 在Cloud中可能无法使用，可以移除或使用替代方案
# pyttsx3>=2.80,<3.0
```

#### 方案B：移除问题依赖

如果 `pyttsx3` 在Cloud中无法安装，可以：

1. **移除pyttsx3依赖**：
   ```txt
   # 注释掉或删除这行
   # pyttsx3==2.90
   ```

2. **修改语音功能代码**：
   在 `utils/voice_player.py` 中添加Cloud兼容检查：

   ```python
   import streamlit as st
   
   try:
       import pyttsx3
       PYTTSX3_AVAILABLE = True
   except ImportError:
       PYTTSX3_AVAILABLE = False
       st.warning("语音功能在Cloud环境中不可用")
   ```

### 问题2：Python版本不兼容

**错误信息**：
```
ERROR: Package 'xxx' requires a different Python version
```

**解决方案**：

Streamlit Cloud支持的Python版本：
- Python 3.8.x
- Python 3.9.x
- Python 3.10.x
- Python 3.11.x

**如果您的项目使用Python 3.7**：

1. 升级依赖版本到支持Python 3.8+
2. 或使用Docker容器部署
3. 或使用其他云平台（如Heroku、Render）

### 问题3：网络超时

**错误信息**：
```
ERROR: ReadTimeoutError
```

**解决方案**：

1. **重试部署**：有时网络问题导致超时
2. **使用国内镜像**：如果在中国，可以配置pip镜像
3. **减少依赖数量**：移除不必要的包

### 问题4：构建失败

**错误信息**：
```
ERROR: Build failed
```

**解决方案**：

1. **查看详细日志**：点击"Logs"查看完整错误信息
2. **检查语法错误**：确保所有Python文件语法正确
3. **检查导入错误**：确保所有导入的包都已安装

### 问题5：运行时错误

**错误信息**：
```
ERROR: Application failed to start
```

**解决方案**：

1. **检查main.py**：确保入口文件正确
2. **检查数据库初始化**：确保数据库路径正确
3. **检查环境变量**：确保所有必需的环境变量已设置

## 部署后检查清单

部署成功后，检查以下功能：

### 基本功能
- [ ] 应用可以正常访问
- [ ] 页面导航正常
- [ ] 没有JavaScript错误

### 核心功能
- [ ] 老人端模拟界面可以访问
- [ ] 后台仪表盘可以访问
- [ ] 数据库可以正常读写

### 地图功能
- [ ] 地图可以正常显示
- [ ] 标记点可以正常显示
- [ ] 地图交互正常

### 其他功能
- [ ] 实时警报模拟可以启动
- [ ] 数据看板可以正常显示
- [ ] 知识库管理可以正常使用

## 环境变量配置

确保在Streamlit Cloud中配置以下环境变量：

### 必需变量
```env
STREAMLIT_SERVER_HEADLESS=true
DB_PATH=./data/emergency_response.db
```

### 可选变量
```env
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
```

## 性能优化建议

### 1. 减少初始加载时间

```python
# 在main.py中添加
import streamlit as st

@st.cache_resource
def load_cached_data():
    # 加载缓存数据
    pass
```

### 2. 优化数据库查询

```python
# 使用分页查询
def get_alerts(page=1, page_size=50):
    offset = (page - 1) * page_size
    # 分页查询逻辑
    pass
```

### 3. 使用异步加载

```python
# 使用st.spinner显示加载状态
with st.spinner("正在加载..."):
    # 加载数据
    pass
```

## 监控和日志

### 启用日志

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # 应用代码
    pass
except Exception as e:
    logger.error(f"Error: {e}")
    st.error(f"发生错误: {e}")
```

### 错误处理

```python
# 在关键函数中添加错误处理
def create_alert(user_id, location_lat, location_lng):
    try:
        # 创建警报逻辑
        pass
    except Exception as e:
        st.error(f"创建警报失败: {e}")
        return None
```

## 备份和恢复

### 数据备份

```python
import shutil
from datetime import datetime

def backup_database():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"database_backup_{timestamp}.db"
    shutil.copy("data/emergency_response.db", backup_path)
    return backup_path
```

### 数据恢复

```python
def restore_database(backup_path):
    shutil.copy(backup_path, "data/emergency_response.db")
```

## 联系支持

如果遇到无法解决的问题：

### 1. Streamlit官方支持
- 文档：https://docs.streamlit.io/
- 社区：https://discuss.streamlit.io/
- GitHub：https://github.com/streamlit/streamlit

### 2. 常见问题搜索
- Stack Overflow：https://stackoverflow.com/questions/tagged/streamlit
- GitHub Issues：https://github.com/streamlit/streamlit/issues

### 3. 获取帮助
- Streamlit Cloud状态页面：https://status.streamlit.io/
- 部署日志：在Streamlit Cloud应用页面查看

## 快速修复命令

### 重新部署

```bash
# 在本地
git add .
git commit -m "修复部署问题"
git push

# Streamlit Cloud会自动检测更新并重新部署
```

### 清除缓存

```bash
# 在Streamlit Cloud中
# 没有直接的清除缓存命令
# 但可以通过修改代码触发重新部署
```

### 回滚到之前的版本

```bash
# 回滚到上一个版本
git reset --hard HEAD~1
git push --force

# 然后在Streamlit Cloud中会自动回滚
```

## 最佳实践

### 1. 版本控制

```bash
# 使用语义化版本
git tag -a v1.0.0 -m "Initial release"
git push --tags
```

### 2. 持续集成

```bash
# 设置GitHub Actions自动部署
# .github/workflows/deploy.yml
name: Deploy to Streamlit Cloud
on:
  push:
    branches: [main]
```

### 3. 监控

```python
# 添加健康检查端点
@st.cache_data(ttl=60)
def health_check():
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }
```

## 总结

1. **等待安装完成**：当前正在安装依赖，请耐心等待
2. **查看错误日志**：如果失败，查看详细错误信息
3. **根据错误修复**：参考上述解决方案
4. **重新部署**：修复后推送到GitHub
5. **验证功能**：部署后测试所有功能

祝部署顺利！🚀
