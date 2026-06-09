# 部署说明

## 当前公网 Demo

已部署到 Streamlit Cloud：

[https://intern-energy-station-linjialiang.streamlit.app/](https://intern-energy-station-linjialiang.streamlit.app/)

## 推荐方案一：Streamlit Cloud

适合课程作业快速部署。

### 前置条件

1. 将项目推送到 GitHub 仓库。
2. 仓库根目录包含：
   - `app.py`
   - `requirements.txt`
   - `data/`
   - `pages/`
   - `services/`

### 部署步骤

1. 登录 Streamlit Cloud。
2. 选择 GitHub 仓库。
3. Main file path 填写：

```text
app.py
```

4. Python 依赖会根据 `requirements.txt` 自动安装。
5. 部署完成后复制公网链接，填入最终作业提交材料。

本项目当前配置：

```text
Main file path: app.py
Demo URL: https://intern-energy-station-linjialiang.streamlit.app/
```

## 推荐方案二：Hugging Face Spaces

适合需要稳定公开链接的 Demo。

### Space 类型

选择 `Streamlit`。

### 必要文件

```text
app.py
requirements.txt
data/
pages/
services/
prompts/
```

### 启动方式

Hugging Face Spaces 会自动识别 `app.py` 并启动 Streamlit 应用。

## 本地部署验证

```bash
pip install -r requirements.txt
python scripts/generate_mock_data.py
python -m streamlit run app.py
```

如果页面可以在 `http://localhost:8501` 打开，则说明部署所需文件基本完整。

## 注意事项

- 当前版本支持火山方舟 LLM 增强，但不强依赖外部 LLM API；未配置 API Key 时会自动回退到规则模板。
- 如需启用真实模型调用，请在 Streamlit Cloud Secrets 中配置 `ARK_API_KEY`、`ARK_BASE_URL` 和 `ARK_MODEL`，详见 `docs/llm_config.md`。
- 数据使用 CSV 模拟，适合 Demo 展示。
- 如果后续接入真实模型，建议通过平台 Secret 管理 API Key，不要写入代码仓库。
