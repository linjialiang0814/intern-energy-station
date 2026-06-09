# LLM 接入配置

当前项目支持火山引擎方舟（Volcengine Ark）的 OpenAI 兼容 Chat Completions 接口，并保留规则模板 fallback。

## 配置方式

### Streamlit Cloud

在 Streamlit Cloud 应用的 `Settings -> Secrets` 中添加：

```toml
ARK_API_KEY = "你的火山方舟 API Key"
ARK_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
ARK_MODEL = "你的模型 endpoint id 或模型名"
LLM_TIMEOUT_SECONDS = "20"
```

### 本地运行

方式一：环境变量。

```powershell
$env:ARK_API_KEY="你的火山方舟 API Key"
$env:ARK_BASE_URL="https://ark.cn-beijing.volces.com/api/v3"
$env:ARK_MODEL="你的模型 endpoint id 或模型名"
python -m streamlit run app.py
```

方式二：本地 secrets。

复制 `.streamlit/secrets.example.toml` 为 `.streamlit/secrets.toml`，然后填入真实 Key。

## Fallback 策略

当以下任一情况发生时，系统会自动回退到规则模板输出：

- 未配置 `ARK_API_KEY`。
- API 请求超时。
- API 返回错误。
- 模型返回空内容。

这样可以保证 Demo 在无 Key、无网络或服务异常时仍可完整演示。

## 已接入模块

- 导师带教助手：LLM 生成补充管理洞察。
- 实习生成长助手：LLM 生成鼓励性成长建议。
- AI 周报生成：LLM 生成 HR 周报正文。

评分、风险等级、风险原因仍由本地规则计算，保证结论稳定、可解释。
