"""Validate mentor feedback analysis and weekly report generation."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from services.data_service import get_dashboard_summary, get_intern_profile, get_intern_options, parse_intern_id
from services.growth_plan_service import generate_growth_plan
from services.mentor_feedback_service import analyze_mentor_feedback
from services.report_service import generate_report_outline, generate_weekly_report


def main() -> int:
    first_option = get_intern_options()[0]
    profile = get_intern_profile(parse_intern_id(first_option))["profile"]
    feedback_text = "本周完成了接口文档阅读，但代码提交较少，开会表达不够主动。"
    analysis = analyze_mentor_feedback(feedback_text, profile)
    growth_plan = generate_growth_plan(profile, "不知道接下来该重点学什么")

    summary = get_dashboard_summary()
    report = generate_weekly_report(summary)
    outline = generate_report_outline(summary)

    checks = {
        "feedback_has_strengths": len(analysis.strengths) > 0,
        "feedback_has_weaknesses": len(analysis.weaknesses) > 0,
        "feedback_has_actions": len(analysis.mentor_actions) > 0,
        "feedback_has_message": len(analysis.message_to_intern) > 20,
        "feedback_has_ai_insight": len(analysis.ai_insight) > 20,
        "report_mentions_total": str(summary["metrics"]["total_interns"]) in report,
        "report_has_actions": "下周建议动作" in report,
        "outline_has_risk_list": "风险名单" in outline,
        "growth_has_focus": len(growth_plan.learning_focus) > 0,
        "growth_has_tasks": len(growth_plan.recommended_tasks) > 0,
        "growth_has_questions": len(growth_plan.mentor_questions) > 0,
        "growth_has_source": bool(growth_plan.llm_provider),
    }

    for name, passed in checks.items():
        print(f"{name}: {passed}")
    print("risk_level:", analysis.risk_level)
    print("report_chars:", len(report))

    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
