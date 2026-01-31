# 环境变量配置使用指南

## 概述

本项目使用 `.env` 文件来管理敏感配置信息，如API密钥。这些配置通过 `python-dotenv` 库加载。

## 文件结构

```
app/
├── .env                  # 实际的环境变量文件（不提交到Git）
├── .env.example          # 环境变量模板（提交到Git）
└── .gitignore            # 确保.env不被提交
```

## 配置项说明

| 配置项 | 说明 | 示例值 |
|--------|------|--------|
| `MAP_API_KEY` | 地图服务API密钥 | `your_map_api_key_here` |
| `WEATHER_API_KEY` | 天气服务API密钥 | `your_weather_api_key_here` |
| `SMS_API_KEY` | 短信服务API密钥 | `your_sms_api_key_here` |
| `NOTIFICATION_API_KEY` | 通知服务API密钥 | `your_notification_api_key_here` |

## 使用方法

### 1. 在应用启动时加载

在 `main.py` 中：

```python
from dotenv import load_dotenv
import os

load_dotenv()

map_api_key = os.getenv('MAP_API_KEY')
weather_api_key = os.getenv('WEATHER_API_KEY')
```

### 2. 在任何模块中使用

```python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')
```

### 3. 在Streamlit设置页面中配置

访问 **系统设置** → **API配置** 页面，可以：

- 查看当前配置状态
- 输入新的API密钥
- 保存到 `.env` 文件
- 重启应用使配置生效

## 首次配置

### 方法1：通过Web界面配置

1. 启动应用：`streamlit run main.py`
2. 导航到 **系统设置** → **API配置**
3. 在表单中输入API密钥
4. 点击 **保存配置**
5. 点击 **立即重启应用**

### 方法2：手动编辑.env文件

1. 复制模板文件：
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，填入实际的API密钥：
   ```bash
   MAP_API_KEY=your_actual_map_api_key
   WEATHER_API_KEY=your_actual_weather_api_key
   SMS_API_KEY=your_actual_sms_api_key
   NOTIFICATION_API_KEY=your_actual_notification_api_key
   ```

3. 重启应用

## 动态更新配置

### 使用 dotenv.set_key()

```python
from dotenv import set_key
import os

env_file = os.path.join(os.path.dirname(__file__), '.env')

set_key(env_file, 'MAP_API_KEY', 'new_api_key')
```

### 使用 dotenv.dotenv_values()

```python
from dotenv import dotenv_values

env_file = os.path.join(os.path.dirname(__file__), '.env')
env_values = dotenv_values(env_file)

map_api_key = env_values.get('MAP_API_KEY', 'default_value')
```

## 安全注意事项

1. **永远不要提交 .env 文件到版本控制**
   - `.env` 已添加到 `.gitignore`
   - 只提交 `.env.example` 作为模板

2. **使用强密码作为API密钥**
   - 不要使用默认值
   - 定期更换密钥

3. **在部署时使用环境变量**
   - Streamlit Cloud 支持在 Secrets 中配置
   - 不要在代码中硬编码密钥

## Streamlit Cloud 部署

### 配置 Secrets

1. 访问 Streamlit Cloud 项目设置
2. 进入 **Secrets** 部分
3. 添加以下环境变量：
   ```
   MAP_API_KEY=your_map_api_key
   WEATHER_API_KEY=your_weather_api_key
   SMS_API_KEY=your_sms_api_key
   NOTIFICATION_API_KEY=your_notification_api_key
   ```

### 代码中访问 Secrets

```python
import os

map_api_key = os.getenv('MAP_API_KEY')
```

## 故障排除

### 问题：环境变量未加载

**解决方案**：
1. 确保 `.env` 文件存在
2. 检查文件路径是否正确
3. 确认调用了 `load_dotenv()`

### 问题：配置保存失败

**解决方案**：
1. 检查文件写入权限
2. 确认 `.env` 文件未被锁定
3. 查看终端错误信息

### 问题：配置未生效

**解决方案**：
1. 重启应用
2. 清除浏览器缓存
3. 检查 `.env` 文件内容

## 示例代码

### 完整的配置管理类

```python
import os
from dotenv import load_dotenv, set_key, dotenv

class ConfigManager:
    def __init__(self, env_file='.env'):
        self.env_file = env_file
        load_dotenv(env_file)
    
    def get(self, key, default=None):
        return os.getenv(key, default)
    
    def set(self, key, value):
        set_key(self.env_file, key, value)
        load_dotenv(self.env_file)
    
    def get_all(self):
        return dotenv_values(self.env_file)

config = ConfigManager()

map_api_key = config.get('MAP_API_KEY')
config.set('MAP_API_KEY', 'new_key')
```

## 相关文档

- [python-dotenv 文档](https://github.com/theskumar/python-dotenv)
- [Streamlit Secrets 文档](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-your-app/secrets-management)
