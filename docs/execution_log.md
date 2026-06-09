# 实习能量站执行记录

## 阶段 1：初始化与数据准备

### 目标

建立 MVP 的工程骨架与可复现的模拟数据，为后续 HR 看板、个人画像、评分规则和 AI 模块提供稳定输入。

### 技术选择

- 使用 `Streamlit` 作为 Demo 主框架，优先保证可运行、可展示、易部署。
- 使用 `CSV` 作为阶段 1 数据载体，降低数据库复杂度。
- 使用 `Faker` 生成更真实的中文姓名；当本地未安装 Faker 时，脚本会使用内置中文样本池降级生成。
- 使用固定随机种子，保证每次生成的数据结构一致，便于演示和调试。

### 已规划数据表

- `interns.csv`：实习生基础信息。
- `mentors.csv`：导师信息。
- `weekly_tasks.csv`：研发、产品、销售三类岗位的周任务。
- `intern_progress.csv`：实习生任务完成记录。
- `mentor_feedback.csv`：导师自然语言反馈与评分。
- `evaluation_results.csv`：适岗评分、等级、风险标签和 AI 摘要。

### 为什么这么做

先用模拟数据跑通核心业务闭环，可以避免一开始陷入账号、权限、数据库和复杂工作流。阶段 1 的重点是让后续页面和服务层都能围绕同一套数据推进，保证 MVP 快速成型。

### 下一步

1. 运行数据生成脚本，确认 20 名实习生数据完整。
2. 补充评分服务和风险服务。
3. 基于数据表实现 HR Dashboard 的首版页面。

### 阶段 1 验收记录

验收时间：2026-06-08

已完成：

- 已创建项目骨架：`data/`、`scripts/`、`services/`、`prompts/`、`pages/`、`utils/`、`docs/`。
- 已创建模拟数据生成脚本：`scripts/generate_mock_data.py`。
- 已生成 6 张 CSV 数据表。
- 已补充数据字典：`docs/data_dictionary.md`。
- 已补充依赖文件：`requirements.txt`。

数据校验结果：

- 实习生总数：20。
- 岗位分布：研发 8 人、产品 6 人、销售 6 人。
- 导师数量：6。
- 岗位周任务：15 条。
- 实习生任务进度：72 条。
- 导师反馈：20 条。
- 评价结果：20 条。
- 风险分布：低风险 10 人、需关注 5 人、高风险 5 人。
- 适岗等级分布：高潜 5 人、稳定 6 人、需关注 4 人、高风险 5 人。
- 适岗分范围：41.8 - 95.4。
- 缺失值：0。

说明：

当前环境未安装 `Faker`，数据生成脚本已按设计使用内置中文姓名池降级生成。后续如果需要更丰富的姓名、学校、城市等模拟数据，可以安装 `Faker` 后重新运行脚本。

### 阶段 1 收口结论

阶段 1 已完成。当前项目已经具备稳定的数据底座，可以支持后续看板、个人画像、导师反馈分析和周报生成。下一阶段不再继续扩展模拟数据规模，优先把评分与风险判断沉淀为服务层能力。

## 阶段 2：评分与风险规则

### 目标

让系统先具备可解释的“判断能力”，为 HR Dashboard 和实习生个人画像提供统一的适岗分、等级、风险原因和行动建议。

### 已完成

- 新增 `services/scoring_service.py`：适岗度评分、等级划分、规则解释。
- 新增 `services/risk_service.py`：风险等级识别、风险原因、行动建议。
- 新增 `scripts/validate_rules.py`：基于现有 CSV 重新计算并校验评分/风险结果。
- 新增 `docs/rules.md`：记录评分权重、等级划分、风险关键词和行动建议。

### 规则设计

适岗度评分采用 5 个维度：

- 任务完成度：30%。
- 导师评价：25%。
- 学习主动性：20%。
- 沟通协作：15%。
- 岗位技能匹配：10%。

风险识别采用规则评分 + 导师反馈关键词混合判断：

- `fit_score < 60` 或 `task_score < 50`：高风险。
- `fit_score < 70` 或导师反馈命中风险关键词：需关注。
- 其他情况：低风险。

### 验收结果

运行命令：

```bash
python scripts/validate_rules.py
```

结果：

- 评价记录：20 条。
- 适岗分/等级不一致：0。
- 风险等级不一致：0。
- 适岗等级分布：高潜 5 人、稳定 6 人、需关注 4 人、高风险 5 人。
- 风险分布：低风险 10 人、需关注 5 人、高风险 5 人。

### 为什么这么做

在接入大模型之前，先用明确规则完成稳定判断，可以让 Demo 的核心结论可解释、可复现，也能避免 AI 输出波动影响演示。后续 LLM 主要负责把规则结果转化为更自然的解释、反馈话术和周报，而不是替代所有判断逻辑。

### 下一步

1. 实现 `data_service.py`，统一读取并合并 CSV。
2. 基于评分与风险服务实现 HR Dashboard 首版。
3. 在看板中展示核心指标、岗位分布、风险分布、适岗排名和行动建议。

## 阶段 3：HR Dashboard 与个人画像页主干

### 目标

先形成能演示的产品主干，让 Demo 可以完成“整体态势 -> 风险定位 -> 个人画像 -> 行动建议”的闭环。

### 已完成

- 新增 `services/data_service.py`：统一读取并聚合 CSV 数据。
- 新增 `scripts/validate_dashboard_data.py`：校验 Dashboard 和个人画像页所需数据结构。
- 新增 `app.py`：项目首页，说明产品定位和演示路径。
- 新增 `pages/1_HR_Dashboard.py`：HR 总览看板。
- 新增 `pages/2_Intern_Profile.py`：实习生个人画像页。
- 已安装 `requirements.txt` 中的运行依赖，用于本地页面验收。

### 页面能力

HR Dashboard 当前支持：

- 展示总人数、高潜人数、风险预警人数、平均任务分、平均适岗分、导师反馈率。
- 按岗位汇总人数、平均任务分、平均适岗分和风险人数。
- 展示风险等级分布与适岗等级分布。
- 展示 Top 5 高潜实习生与 Bottom 5 需跟进实习生。
- 展示风险实习生的原因和下一步行动建议。
- 展示 20 名实习生明细表。

个人画像页当前支持：

- 通过侧边栏选择实习生。
- 展示基础信息、当前周数、适岗分、适岗等级和风险等级。
- 展示能力评分、规则解释、导师反馈、AI 摘要。
- 展示风险原因、下一步行动建议和任务完成记录。

### 验收结果

运行命令：

```bash
python scripts/validate_dashboard_data.py
python -m py_compile app.py pages/1_HR_Dashboard.py pages/2_Intern_Profile.py services/data_service.py
```

结果：

- Dashboard 聚合数据校验通过。
- 页面文件语法检查通过。
- 本地启动 `Streamlit` 后，首页、HR Dashboard、个人画像页均可访问。
- 浏览器检查确认：首页标题、HR 看板指标、风险行动建议、个人画像、导师反馈、风险原因、下一步行动建议、任务记录均可见。

### 说明

浏览器插件在保存截图到本地文件时遇到权限限制，因此本阶段以 DOM 可见性和本地页面访问作为验收依据。页面主干已经足够支撑下一步演示和后续 AI 功能接入。

### 下一步

1. 增加导师反馈分析页，让导师输入自然语言反馈并生成结构化建议。
2. 增加 AI 周报页，把 Dashboard 的群体数据转化为 HR 周报。
3. 根据演示效果微调页面布局和文案。

## 阶段 4：导师反馈分析与 AI 周报生成

### 目标

在已有看板和个人画像基础上补齐 AI 价值表达，让 Demo 不只是展示数据，而是能把自然语言反馈和群体数据转化为结构化建议、行动项和 HR 周报。

### 已完成

- 新增 `services/mentor_feedback_service.py`：导师反馈结构化分析服务。
- 新增 `services/report_service.py`：HR 周报生成服务。
- 新增 `pages/3_Mentor_Assistant.py`：导师带教助手页面。
- 新增 `pages/4_AI_Weekly_Report.py`：AI 周报生成页面。
- 新增 `scripts/validate_ai_features.py`：AI 功能验收脚本。
- 新增 `prompts/mentor_feedback_prompt.txt` 和 `prompts/weekly_report_prompt.txt`，为后续接入 LLM 预留提示词模板。

### 功能说明

导师带教助手当前支持：

- 选择实习生并自动带出其当前画像。
- 输入或复用导师自然语言反馈。
- 输出优点、问题/短板、风险等级、导师下周动作、HR 建议和给实习生的反馈话术。

AI 周报生成当前支持：

- 汇总实习生总数、高潜人数、风险人数、平均适岗分和导师反馈覆盖率。
- 生成结构化周报要点：整体结论、风险名单、下周动作。
- 生成可复制/下载的 HR 周报正文。

### 验收结果

运行命令：

```bash
python scripts/validate_ai_features.py
python -m py_compile services/mentor_feedback_service.py services/report_service.py pages/3_Mentor_Assistant.py pages/4_AI_Weekly_Report.py scripts/validate_ai_features.py
```

结果：

- 导师反馈分析：优点、问题、动作建议、反馈话术均可生成。
- 周报生成：可识别总人数、包含下周建议动作、包含风险名单结构。
- 生成周报正文长度：523 字。
- 页面和服务语法检查通过。

### 说明

`streamlit run app.py` 是持续运行的 Web 服务命令，不适合作为普通一次性验收命令直接前台执行。后续本地页面验收应使用后台启动、HTTP 探活和必要的浏览器检查，完成后及时关闭服务。

当前 AI 能力采用“规则 + 模板”的稳定 fallback，暂未依赖外部 LLM API。这样可以保证无网络或无 API Key 时 Demo 仍可完整演示；后续接入 LLM 时，可复用现有 prompt 和结构化数据。

### 下一步

1. 加入统一 `llm_service.py`，支持 API Key 存在时调用真实模型，失败时回退模板。
2. 优化页面视觉和演示动线。
3. 准备部署配置和 1000 字以内方案说明。

## 阶段 5：MVP 反思与实习生成长助手补齐

### 反思结论

对照题目要求和初始计划，前一版 Demo 已覆盖 HR 看板、个人画像、导师反馈分析和 AI 周报，但还缺少一个重要视角：实习生本人如何知道“我接下来该学什么”。这正是题目中的核心痛点之一，因此不应放到增强版，而应纳入 MVP。

### 已补齐

- 新增 `services/growth_plan_service.py`：根据岗位、当前周次、能力短板生成成长建议。
- 新增 `pages/5_Intern_Growth_Assistant.py`：实习生成长助手页面。
- 更新 `app.py`：补充完整 MVP 功能说明。
- 更新 `scripts/validate_ai_features.py`：加入成长助手验收项。

### 当前 MVP 范围

当前 MVP 已包含：

1. HR 总览看板。
2. 实习生个人画像。
3. 适岗度评分。
4. 风险等级识别。
5. 导师反馈结构化分析。
6. 实习生成长助手。
7. AI 周报生成。

这 7 个模块已经覆盖题目中的三类核心问题：

- 导师规范带教：由导师带教助手和风险行动建议支撑。
- 实习生成长迷茫：由实习生成长助手和个人画像支撑。
- 多角色协同效率：由 HR Dashboard、个人画像、周报和统一评分规则支撑。

### 验收结果

运行命令：

```bash
python scripts/validate_ai_features.py
python scripts/validate_dashboard_data.py
python -m py_compile app.py pages/*.py services/*.py scripts/*.py
```

说明：在 PowerShell 中第三条命令实际使用文件枚举方式执行。

结果：

- Dashboard 数据聚合通过。
- 导师反馈分析通过。
- AI 周报生成通过。
- 实习生成长建议通过。
- 所有页面、服务和脚本语法检查通过。

### 下一阶段判断

MVP 功能已经完整。继续堆功能的边际收益开始下降，下一步不建议先做复杂登录、数据库权限、历史趋势等增强功能。更合理的顺序是：

1. 先写方案说明和 README，确保交付物可解释。
2. 准备部署配置并部署公网 Demo。
3. 再做轻量工程化优化，例如统一 LLM fallback、页面文案润色、部署说明、演示脚本。

## 阶段 6：说明文件完善

### 目标

补齐课程作业交付所需的说明材料，让项目不仅能运行，也能被清楚理解、演示和部署。

### 已完成

- 改造根目录 `README.md`：从作业题目说明改为项目说明、功能介绍、运行命令和验收命令。
- 新增 `docs/assignment.md`：备份原始作业题目。
- 新增 `docs/solution_description.md`：1000 字以内方案说明。
- 新增 `docs/demo_script.md`：3 分钟演示脚本。
- 新增 `docs/deployment.md`：Streamlit Cloud 和 Hugging Face Spaces 部署说明。

### 文档定位

- `README.md`：给运行者和评审者快速理解项目。
- `solution_description.md`：用于课程作业提交。
- `demo_script.md`：用于录屏或现场演示。
- `deployment.md`：用于部署公网 Demo。
- `execution_log.md`：记录项目推进过程和迭代思路。

### 验收结果

- `docs/solution_description.md` 正文约 863 字，满足 1000 字以内要求。
- `python scripts/validate_ai_features.py` 通过，说明文档调整未影响核心功能。

### 下一步

1. 进行一次本地完整页面走查。
2. 准备部署到 Streamlit Cloud 或 Hugging Face Spaces。
3. 部署完成后将公网链接补充到 README 和最终方案说明中。

## 阶段 7：MVP 最终收口

### 目标

在公网部署完成后，补齐最终提交材料中的 Demo 链接和提交清单，完成 MVP 阶段交付闭环。

### 已完成

- Streamlit Cloud 公网 Demo 已部署：
  <https://intern-energy-station-linjialiang.streamlit.app/>
- 更新 `README.md`：补充在线 Demo 地址和最终提交清单入口。
- 更新 `docs/deployment.md`：补充当前 Streamlit Cloud 部署信息。
- 更新 `docs/solution_description.md`：补充公网 Demo 链接。
- 新增 `docs/final_submission_checklist.md`：整理最终交付物、页面检查项和验收命令。

### 收口判断

MVP 阶段已经完成。当前项目具备：

- 可公网访问的完整 Demo。
- 1000 字以内方案说明。
- 本地验收脚本。
- 演示脚本和部署说明。
- 项目推进记录。

### 后续方向

第二阶段可以围绕工程化增强继续推进，优先级建议为：

1. 接入真实 LLM API，并保留规则 fallback。
2. 优化页面视觉和演示动线。
3. 将 `validate_*.py` 升级为正式测试。
4. 增加导出能力，例如单个实习生画像摘要和周报导出。

## 阶段 8：LLM 接入增强

### 目标

在保留 MVP 稳定性的前提下接入真实大模型能力。优先支持火山引擎方舟 OpenAI 兼容接口，同时保证未配置 API Key、请求失败或模型异常时自动回退到现有规则模板。

### 已完成

- 新增 `services/llm_service.py`：统一 LLM 调用层。
- 支持环境变量和 Streamlit Secrets 配置：
  - `ARK_API_KEY`
  - `ARK_BASE_URL`
  - `ARK_MODEL`
  - `LLM_TIMEOUT_SECONDS`
- 更新 `services/mentor_feedback_service.py`：导师反馈分析增加 LLM 补充洞察。
- 更新 `services/growth_plan_service.py`：实习生成长助手增加 LLM 鼓励性建议。
- 更新 `services/report_service.py`：HR 周报正文支持 LLM 生成，失败时回退模板。
- 更新页面显示生成来源：真实 LLM 或规则模板 fallback。
- 新增 `.streamlit/secrets.example.toml`。
- 新增 `docs/llm_config.md`。
- 新增 `scripts/validate_llm_fallback.py`。

### 验收结果

运行命令：

```bash
python scripts/validate_llm_fallback.py
python scripts/validate_ai_features.py
python scripts/validate_rules.py
python scripts/validate_dashboard_data.py
```

结果：

- 未配置 API Key 时，LLM 调用正确回退到 fallback。
- 导师反馈分析、成长助手、周报生成均可正常输出。
- 评分规则和 Dashboard 数据聚合未受影响。
- 全量 Python 语法检查通过。

### 配置说明

详见 `docs/llm_config.md`。公网部署建议通过 Streamlit Cloud Secrets 配置真实 API Key，不要写入代码仓库。

## 阶段 9：适岗评分解释增强

### 目标

提升评分可信度，让 HR 和导师不仅看到“适岗分”，还能理解分数来源、权重贡献、等级含义和下一步动作依据。

### 已完成

- 更新 `services/scoring_service.py`：
  - 增加评分维度中文名。
  - 增加等级解释。
  - 增加每个维度的权重、原始分、贡献分、状态和解释。
- 更新 `pages/2_Intern_Profile.py`：
  - 展示等级含义。
  - 增加“适岗分贡献拆解”表格。
- 更新 `pages/1_HR_Dashboard.py`：
  - 明细表补充导师分、主动性、沟通分和技能匹配分。
- 新增 `scripts/validate_score_explanations.py`。
- 更新 `docs/rules.md`。

### 验收标准

- 每个实习生都有 5 个评分维度。
- 每个维度都有权重、贡献分和解释。
- 贡献分加总与适岗分一致。
- 原有评分、风险、Dashboard 和 AI 功能不受影响。

## 阶段 10：页面体验优化与内容导出

### 目标

提升演示顺滑度和内容可复用性，让 HR 看板、个人画像和周报不仅能看，还能下载、复盘和提交。

### 已完成

- 新增 `services/export_service.py`：
  - Dashboard Markdown 摘要导出。
  - 实习生个人画像 Markdown 导出。
  - DataFrame CSV 导出，使用 UTF-8 BOM 兼容 Excel 中文显示。
- 更新 `app.py`：
  - 增加推荐演示路径。
  - 增加 LLM fallback 说明。
- 更新 `pages/1_HR_Dashboard.py`：
  - 增加实习生明细 CSV 下载。
  - 增加 HR 看板摘要 Markdown 下载。
- 更新 `pages/2_Intern_Profile.py`：
  - 增加个人画像 Markdown 下载。
  - 增加任务记录 CSV 下载。
- 更新 `pages/4_AI_Weekly_Report.py`：
  - 保留周报 Markdown 下载。
  - 增加风险名单 CSV 下载。
- 新增 `scripts/validate_exports.py`。

### 验收标准

- Dashboard Markdown 包含标题、核心指标、岗位表现和风险对象。
- 个人画像 Markdown 包含基础信息、评分解释、风险原因和任务记录。
- CSV 导出带 UTF-8 BOM，便于 Excel 打开中文。
- 原有规则、Dashboard、AI 和 LLM fallback 验收不受影响。

## 阶段 11：测试与工程化收口

### 目标

为第二阶段建立统一质量检查入口，并完成工程化总结与后续规划。

### 已完成

- 新增 `scripts/quality_check.py`：
  - 执行规则校验。
  - 执行 Dashboard 数据校验。
  - 执行 AI 功能校验。
  - 执行 LLM fallback 校验。
  - 执行评分解释校验。
  - 执行导出功能校验。
  - 执行 Python 语法检查。
- 新增 `docs/engineering_review.md`：
  - 总结第二阶段完成项。
  - 梳理当前限制、缺点与风险。
  - 规划后续值得提升的功能。
- 更新 `README.md` 和 `docs/final_submission_checklist.md`：增加一键验收命令。

### 反思结论

当前项目的核心 Demo、LLM 增强、导出能力和质量检查已经闭环。仍存在数据未持久化、无登录权限、评分模型未用真实数据校准等限制，但这些属于后续产品化阶段，不应继续阻塞当前作业交付。

### 第二阶段收口判断

第二阶段完成，可以进入最终演示、提交和轻量维护。后续如继续推进，应优先做数据持久化、角色权限、历史趋势和 GitHub Actions 测试。
