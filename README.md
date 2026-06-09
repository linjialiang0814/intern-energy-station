# 实习能量站

AI 驱动的业务部实习生成长导航智能看板。

本项目面向 HR、业务导师、实习生和招聘团队，提供实习生成长看板、个人画像、适岗度评分、风险预警、导师反馈分析、实习生成长助手和 HR 周报生成能力。

## 在线 Demo

公网访问地址：[https://intern-energy-station-linjialiang.streamlit.app/](https://intern-energy-station-linjialiang.streamlit.app/)

## 核心价值

- 帮 HR 快速掌握 20 名实习生的整体进展、风险分布和适岗情况。
- 帮导师把自然语言反馈转成结构化评价、带教动作和反馈话术。
- 帮实习生明确当前阶段该学什么、做什么、问导师什么。
- 帮招聘同学查看适岗分、风险等级和后续培养建议。

## 功能模块

1. `HR Dashboard`：整体指标、岗位分布、风险分布、适岗排名、风险行动建议。
2. `Intern Profile`：实习生基础信息、能力评分、导师反馈、任务记录、风险原因。
3. `Mentor Assistant`：导师反馈结构化分析，输出优点、问题、风险和带教建议。
4. `AI Weekly Report`：自动生成 HR 周报正文和结构化周报要点。
5. `Intern Growth Assistant`：根据岗位、周次和能力短板生成成长计划。

## 技术栈

- 前端与应用框架：Streamlit
- 数据：CSV 模拟数据
- 数据处理：Pandas
- AI 能力：规则 + 模板 fallback，预留 Prompt 模板用于后续接入 LLM API
- LLM 接入：支持火山引擎方舟 OpenAI 兼容接口，未配置时自动 fallback
- 部署建议：Streamlit Cloud 或 Hugging Face Spaces

## 本地运行

```bash
pip install -r requirements.txt
python scripts/generate_mock_data.py
python -m streamlit run app.py
```

访问本地地址：

```text
http://localhost:8501
```

## 验收命令

推荐一键验收：

```bash
python scripts/quality_check.py
```

也可以分模块执行：

```bash
python scripts/validate_rules.py
python scripts/validate_dashboard_data.py
python scripts/validate_ai_features.py
```

在 PowerShell 中执行全量语法检查：

```powershell
$files = @('app.py') + (Get-ChildItem pages,services,scripts -Filter *.py | ForEach-Object { $_.FullName })
python -m py_compile @files
```

## 项目结构

```text
.
├── app.py
├── data/
├── docs/
├── pages/
├── prompts/
├── scripts/
├── services/
└── requirements.txt
```

## 交付材料

- 在线 Demo：[https://intern-energy-station-linjialiang.streamlit.app/](https://intern-energy-station-linjialiang.streamlit.app/)
- 方案说明：[docs/solution_description.md](docs/solution_description.md)
- 最终提交清单：[docs/final_submission_checklist.md](docs/final_submission_checklist.md)
- 演示脚本：[docs/demo_script.md](docs/demo_script.md)
- 部署说明：[docs/deployment.md](docs/deployment.md)
- LLM 配置说明：[docs/llm_config.md](docs/llm_config.md)
- 第二阶段工程化总结：[docs/engineering_review.md](docs/engineering_review.md)
- 执行记录：[docs/execution_log.md](docs/execution_log.md)
- 作业题目备份：[docs/assignment.md](docs/assignment.md)
