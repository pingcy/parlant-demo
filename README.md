# Parlant Demo - 智能客服助手演示

这是一个基于 Parlant 框架构建的智能客服助手演示项目，包含电信运营商客服和天气查询两个主要功能。

## � 主要功能

### � 电信客服助手 (telecom.py)

**模拟10086客服助手**，提供完整的电信客户服务功能：

- **客户信息查询**: 查询基本客户资料
- **话费余额查询**: 实时查询话费余额和缴费信息
- **套餐管理**: 查询当前套餐、可用套餐、套餐详情
- **智能套餐变更**: 完整的套餐变更流程，包含旅程状态管理
- **友好交互**: 支持日常闲聊，智能引导到业务服务

**特色功能**:

- 🔄 完整的套餐变更旅程：查询可用套餐 → 展示列表 → 咨询详情 → 确认变更 → 执行变更 → 结果反馈
- 🎯 智能状态管理：客户可以在任何阶段回退和重新选择
- 📊 详细的套餐信息：包含资费、特色功能、超出费用等

### 🌤️ 天气查询助手 (weather.py)

简单的天气查询智能体，支持:

- 城市天气查询
- 天气信息展示
- 友好的对话交互

## 🚀 快速开始

### 环境要求

确保您的环境中设置了以下变量：

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_BASE_URL="your-base-url"  # 如: https://api.openai.com/v1
```

### 安装依赖

```bash
# 使用 uv (推荐)
uv venv .venv
source .venv/bin/activate  # macOS/Linux
uv pip install parlant

# 或使用 pip
pip install parlant
```

### 运行程序

```bash
# 运行电信客服助手
python telecom.py

# 运行天气查询助手  
python weather.py
```

## 📁 项目结构

```
parlant-demo/
├── telecom.py                    # 🌟 电信运营商客服助手（主要演示）
├── weather.py                    # 🌤️ 天气查询助手
├── tools.py                      # 共享工具函数库
└── README.md                     # 项目说明
```

## 🔧 自定义模型服务

### OpenAI兼容服务配置

本项目使用了修改过的 `openai_service.py` 来支持自定义的 `OPENAI_BASE_URL`。

**关键修改点**：在三个地方添加了 `base_url` 参数：

1. **第97行** - OpenAISchematicGenerator类：

```python
self._client = AsyncClient(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ["OPENAI_BASE_URL"]  # 👈 新增此行
)
```

2. **第307行** - OpenAIEmbedder类：

```python
self._client = AsyncClient(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ["OPENAI_BASE_URL"]  # 👈 新增此行
)
```

3. **第388行** - OpenAIModerationService类：

```python
self._client = AsyncClient(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ["OPENAI_BASE_URL"]  # 👈 新增此行
)
```

### 使用其他模型

如需使用其他模型（如DeepSeek、通义千问等），可以参考Parlant官方SDK中的 `deepseek_service.py` 实现自定义模型服务：

1. 继承 `NLPService` 基类
2. 实现 `get_schematic_generator()`、`get_embedder()` 和 `get_moderation_service()` 方法
3. 创建对应的生成器和嵌入器类
4. 处理API调用和错误情况

## 💡 使用示例

### 电信客服助手交互示例

```
您: 你好，我想查询一下话费余额
客服: 您好！我是10086客服小助手。请提供您的手机号码，我来帮您查询话费余额。

您: 13812345678  
客服: 您的话费余额为85.60元，下次缴费日期：2024-12-15

您: 我想变更套餐
客服: 好的，我来为您查询可变更的套餐...
[展示可用套餐列表]
请问您想变更到哪个套餐呢？

您: 我想了解一下无限流量88元套餐的详细信息
客服: 无限流量88元套餐详细信息：
• 月费：88元  
• 通话：500分钟
• 流量：无限（超40GB后限速）
• 短信：200条
• 特色服务：免费接听, 流量无限, 全国通用, 5G网络
• 超出资费：超出部分：通话0.15元/分钟，短信0.1元/条

您想要变更到这个套餐吗？
```

## ️ 开发说明

### 工具函数 (tools.py)

项目中的所有工具函数都集中在 `tools.py` 中：

- 电信相关：`get_customer_info`、`query_balance`、`change_plan` 等
- 天气相关：`get_weather`

## 📝 注意事项

1. **API配额**: 请确保您的API账户有足够的配额
2. **网络连接**: 确保网络可以访问您配置的API端点
3. **环境变量**: 必须正确设置 `OPENAI_API_KEY` 和 `OPENAI_BASE_URL`
4. **模型兼容性**: 确保您使用的模型支持OpenAI兼容的API格式

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

本项目基于 Apache 2.0 许可证开源。

---

## 📱 关注我们

扫描下方二维码关注公众号，获取更多AI开发资讯：

<div align="center">
  <img src="qrcode_1m.jpg" alt="公众号二维码" width="200"/>
</div>
