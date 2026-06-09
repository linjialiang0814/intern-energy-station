# MVP 最终提交清单

## 交付物

- 在线 Demo：<https://intern-energy-station-linjialiang.streamlit.app/>
- 方案说明：`docs/solution_description.md`
- 演示脚本：`docs/demo_script.md`
- 项目 README：`README.md`
- 执行记录：`docs/execution_log.md`

## Demo 页面检查

- 首页可打开，能看到项目定位和演示路径。
- `HR Dashboard` 可展示整体指标、岗位表现、风险分布、适岗排名和风险行动建议。
- `Intern Profile` 可选择实习生并展示个人画像、任务记录、导师反馈和下一步动作。
- `Mentor Assistant` 可生成导师反馈结构化分析。
- `AI Weekly Report` 可生成 HR 周报正文并下载 Markdown。
- `Intern Growth Assistant` 可生成实习生成长建议。

## 本地验收命令

```bash
python scripts/validate_rules.py
python scripts/validate_dashboard_data.py
python scripts/validate_ai_features.py
```

PowerShell 语法检查：

```powershell
$files = @('app.py') + (Get-ChildItem pages,services,scripts -Filter *.py | ForEach-Object { $_.FullName })
python -m py_compile @files
```

## 作业提交建议

提交时建议包含：

1. Streamlit Cloud 在线 Demo 链接。
2. 1000 字以内方案说明。
3. 如需录屏，可按 `docs/demo_script.md` 录制 3 分钟以内演示视频。
