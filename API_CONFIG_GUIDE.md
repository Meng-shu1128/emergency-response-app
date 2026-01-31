# API 配置指南

## 概述

本应急响应系统需要配置以下API密钥才能正常工作：

1. **地图API密钥** (MAP_API_KEY) - 用于地图显示和位置服务
2. **天气API密钥** (WEATHER_API_KEY) - 用于获取天气信息进行风险评估
3. **短信API密钥** (SMS_API_KEY) - 用于发送紧急通知短信
4. **通知API密钥** (NOTIFICATION_API_KEY) - 用于APP推送通知

---

## 1. 地图API密钥 (MAP_API_KEY)

### 用途
- 在地图上显示求助位置
- 显示用户位置标记
- 提供位置相关的可视化功能

### 推荐服务提供商

#### 选项1: 高德地图API (推荐)
- 注册地址: https://lbs.amap.com/
- 免费额度: 每日免费调用次数较多
- 获取步骤:
  1. 访问 https://lbs.amap.com/ 注册账号
  2. 进入控制台 -> 应用管理 -> 我的应用
  3. 点击"创建新应用"
  4. 添加Key，选择"Web端(JS API)"
  5. 复制生成的Key

#### 选项2: 百度地图API
- 注册地址: https://lbsyun.baidu.com/
- 免费额度: 每日免费调用次数较多
- 获取步骤:
  1. 访问 https://lbsyun.baidu.com/ 注册账号
  2. 进入控制台 -> 应用管理 -> 我的应用
  3. 点击"创建应用"
  4. 选择"浏览器端"，填写应用名称
  5. 复制生成的AK (Access Key)

#### 选项3: 腾讯位置服务
- 注册地址: https://lbs.qq.com/
- 免费额度: 每日免费调用次数较多
- 获取步骤:
  1. 访问 https://lbs.qq.com/ 注册账号
  2. 进入控制台 -> 应用管理 -> 我的应用
  3. 点击"创建应用"
  4. 选择"Web端(JS API)"
  5. 复制生成的Key

### 配置方法
在系统设置的"API配置"页面，将获取到的Key填入"地图API密钥"字段并保存。

---

## 2. 天气API密钥 (WEATHER_API_KEY)

### 用途
- 获取实时天气信息
- 根据天气状况进行风险评估
- 在暴雨、大雾等恶劣天气时提高风险等级

### 推荐服务提供商

#### 选项1: 和风天气API (推荐)
- 注册地址: https://dev.qweather.com/
- 免费额度: 每日1000次免费调用
- 获取步骤:
  1. 访问 https://dev.qweather.com/ 注册账号
  2. 进入控制台 -> 项目管理 -> 创建项目
  3. 选择"免费订阅"版本
  4. 复制生成的Key

#### 选项2: 心知天气
- 注册地址: https://www.seniverse.com/
- 免费额度: 每日500次免费调用
- 获取步骤:
  1. 访问 https://www.seniverse.com/ 注册账号
  2. 进入控制台 -> 项目管理 -> 创建项目
  3. 复制生成的私钥

### 配置方法
在系统设置的"API配置"页面，将获取到的Key填入"天气API密钥"字段并保存。

---

## 3. 短信API密钥 (SMS_API_KEY)

### 用途
- 向紧急联系人发送求助短信
- 发送系统通知短信
- 在紧急情况下快速通知相关人员

### 推荐服务提供商

#### 选项1: 阿里云短信服务
- 注册地址: https://www.aliyun.com/product/sms
- 免费额度: 新用户有免费试用额度
- 获取步骤:
  1. 访问 https://www.aliyun.com/ 注册账号
  2. 开通短信服务
  3. 创建AccessKey (AccessKey ID 和 AccessKey Secret)
  4. 配置格式: `AccessKeyID:AccessKeySecret`

#### 选项2: 腾讯云短信服务
- 注册地址: https://cloud.tencent.com/product/sms
- 免费额度: 新用户有免费试用额度
- 获取步骤:
  1. 访问 https://cloud.tencent.com/ 注册账号
  2. 开通短信服务
  3. 获取API密钥 (SecretId 和 SecretKey)
  4. 配置格式: `SecretId:SecretKey`

#### 选项3: 容联云通讯
- 注册地址: https://www.yuntongxun.com/
- 免费额度: 新用户有免费试用额度
- 获取步骤:
  1. 访问 https://www.yuntongxun.com/ 注册账号
  2. 开通短信服务
  3. 获取AccountSid和AuthToken
  4. 配置格式: `AccountSid:AuthToken`

### 配置方法
在系统设置的"API配置"页面，将获取到的密钥按指定格式填入"短信API密钥"字段并保存。

---

## 4. 通知API密钥 (NOTIFICATION_API_KEY)

### 用途
- 向移动端APP推送紧急通知
- 实时提醒相关人员
- 支持批量推送和优先级控制

### 推荐服务提供商

#### 选项1: 极光推送 (推荐)
- 注册地址: https://www.jiguang.cn/
- 免费额度: 免费版功能已足够
- 获取步骤:
  1. 访问 https://www.jiguang.cn/ 注册账号
  2. 创建应用
  3. 获取AppKey和MasterSecret
  4. 配置格式: `AppKey:MasterSecret`

#### 选项2: 个推
- 注册地址: https://www.getui.com/
- 免费额度: 免费版功能已足够
- 获取步骤:
  1. 访问 https://www.getui.com/ 注册账号
  2. 创建应用
  3. 获取AppID、AppKey和MasterSecret
  4. 配置格式: `AppID:AppKey:MasterSecret`

#### 选项3: 友盟推送
- 注册地址: https://www.umeng.com/
- 免费额度: 免费版功能已足够
- 获取步骤:
  1. 访问 https://www.umeng.com/ 注册账号
  2. 创建应用
  3. 获取AppKey和AppMasterSecret
  4. 配置格式: `AppKey:AppMasterSecret`

### 配置方法
在系统设置的"API配置"页面，将获取到的密钥按指定格式填入"通知API密钥"字段并保存。

---

## 快速配置步骤

1. **启动应用**
   ```bash
   streamlit run main.py
   ```

2. **访问系统设置页面**
   - 在浏览器中打开 http://localhost:8501
   - 点击侧边栏的"⚙️ 系统设置"

3. **配置API密钥**
   - 在"🔑 API配置"标签页中
   - 填入您获取到的API密钥
   - 点击"保存并重新加载"按钮
   - 点击"🔄 立即重启应用"使配置生效

4. **验证配置**
   - 重启后，在"当前配置"部分查看配置状态
   - 绿色✅表示配置成功且有效
   - 黄色⚠️表示配置无效或未配置

---

## 测试配置

配置完成后，您可以：

1. **测试地图功能**
   - 访问"📊 后台仪表盘"
   - 查看求助地图是否正常显示

2. **测试天气功能**
   - 访问"👴 老人端模拟界面"
   - 在"🎯 风险评估"标签页测试风险评估功能

3. **测试通知功能**
   - 访问"👴 老人端模拟界面"
   - 在"📢 通知系统"标签页测试通知发送

---

## 注意事项

1. **安全性**
   - 不要将API密钥提交到公开的代码仓库
   - 定期更换API密钥
   - 监控API调用次数，避免超出免费额度

2. **免费额度**
   - 大多数API服务都有免费额度
   - 注意监控调用次数，避免产生费用
   - 可以在API服务商的控制台查看调用统计

3. **配置文件**
   - API密钥保存在 `.env` 文件中
   - 该文件不会被提交到Git（已在.gitignore中）
   - 可以手动编辑 `.env` 文件直接修改配置

4. **故障排查**
   - 如果API调用失败，检查密钥是否正确
   - 查看终端输出的错误日志
   - 确认API服务是否正常工作

---

## 联系支持

如果遇到配置问题，请：
1. 查看API服务商的官方文档
2. 检查终端的错误日志
3. 确认网络连接正常
4. 验证API密钥格式是否正确

---

## 更新日志

- 2026-01-31: 创建API配置指南
