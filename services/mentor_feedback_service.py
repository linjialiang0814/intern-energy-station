"""Mentor feedback analysis with deterministic AI-style fallback."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from services.llm_service import call_llm
from services.risk_service import assess_risk, find_risk_keywords


POSITIVE_KEYWORDS = ["完成", "主动", "独立", "按时", "认真", "稳定", "积极", "清晰", "优秀"]
WEAKNESS_HINTS = {
    "沉默": "会议表达不够主动",
    "不主动": "主动沟通不足",
    "不足": "主动沟通或阶段产出不足",
    "偏慢": "任务推进节奏偏慢",
    "迷茫": "对业务方向仍不够清晰",
    "不完整": "反馈记录或成果沉淀不完整",
    "不够稳定": "交付质量稳定性不足",
    "提交较少": "实践产出偏少",
    "代码提交较少": "代码实践产出偏少",
}


@dataclass(frozen=True)
class FeedbackAnalysis:
    strengths: list[str]
    weaknesses: list[str]
    risk_level: str
    mentor_actions: list[str]
    hr_actions: list[str]
    message_to_intern: str
    ai_insight: str
    llm_provider: str
    used_fallback: bool


def extract_strengths(feedback_text: str) -> list[str]:
    """Extract positive points from free-form mentor feedback."""
    strengths = []
    for keyword in POSITIVE_KEYWORDS:
        if keyword in feedback_text:
            if keyword == "完成":
                strengths.append("能够完成阶段任务")
            elif keyword == "主动":
                strengths.append("具备主动对齐目标的意识")
            elif keyword == "独立":
                strengths.append("具备一定独立推进能力")
            elif keyword == "认真":
                strengths.append("学习和文档阅读态度认真")
            elif keyword in {"按时", "稳定"}:
                strengths.append("任务交付节奏较稳定")
            elif keyword == "积极":
                strengths.append("协作态度积极")
            elif keyword == "清晰":
                strengths.append("表达或问题拆解较清晰")
            elif keyword == "优秀":
                strengths.append("整体表现突出")

    if not strengths:
        strengths.append("已形成阶段性反馈，具备继续跟进的基础")
    return list(dict.fromkeys(strengths))[:3]


def extract_weaknesses(feedback_text: str) -> list[str]:
    """Extract development gaps from mentor feedback."""
    weaknesses = [label for keyword, label in WEAKNESS_HINTS.items() if keyword in feedback_text]
    if not weaknesses:
        weaknesses.append("需要继续沉淀可复用的阶段成果")
    return list(dict.fromkeys(weaknesses))[:3]


def build_message_to_intern(strengths: list[str], weaknesses: list[str], role: str) -> str:
    """Generate a warm feedback message for the intern."""
    return (
        f"你本周在“{strengths[0]}”方面有积极表现。"
        f"下一阶段建议重点关注“{weaknesses[0]}”，可以和导师确认一个更具体的{role}岗小任务，"
        "并在推进过程中更及时地同步进展和问题。"
    )


def analyze_mentor_feedback(feedback_text: str, intern_profile: Mapping[str, object]) -> FeedbackAnalysis:
    """Analyze mentor feedback into strengths, gaps, risk and actions."""
    profile = dict(intern_profile)
    role = str(profile.get("role", "业务"))
    strengths = extract_strengths(feedback_text)
    weaknesses = extract_weaknesses(feedback_text)
    risk = assess_risk(profile, feedback_text)

    mentor_actions = risk.actions[:]
    if find_risk_keywords(feedback_text):
        mentor_actions.insert(0, "下次反馈中补充一个可量化的任务目标和验收标准")
    else:
        mentor_actions.insert(0, f"为该实习生增加一个真实{role}场景的小任务")

    hr_actions = []
    if risk.risk_level == "高风险":
        hr_actions.append("建议 HR 本周介入，确认实习生是否存在资源、方向或适配问题")
    elif risk.risk_level == "需关注":
        hr_actions.append("建议 HR 下周复查导师反馈和任务完成情况")
    else:
        hr_actions.append("HR 暂不需要介入，保持常规观察即可")

    fallback_insight = (
        f"系统识别到该反馈的核心关注点是“{weaknesses[0]}”。"
        f"建议导师下周围绕一个可验收任务进行带教，并把反馈从主观描述转成具体行为和交付标准。"
    )
    llm_result = call_llm(
        [
            {
                "role": "system",
                "content": "你是企业 HR 实习生带教分析助手，请输出简洁、可执行、温和的中文建议。",
            },
            {
                "role": "user",
                "content": (
                    f"实习生信息：{profile}\n"
                    f"导师反馈：{feedback_text}\n"
                    f"已识别优点：{strengths}\n"
                    f"已识别问题：{weaknesses}\n"
                    "请补充一段 80 字以内的管理洞察，强调下一步具体动作。"
                ),
            },
        ],
        fallback=fallback_insight,
        max_tokens=200,
    )

    return FeedbackAnalysis(
        strengths=strengths,
        weaknesses=weaknesses,
        risk_level=risk.risk_level,
        mentor_actions=list(dict.fromkeys(mentor_actions))[:4],
        hr_actions=hr_actions,
        message_to_intern=build_message_to_intern(strengths, weaknesses, role),
        ai_insight=llm_result.content,
        llm_provider=llm_result.provider,
        used_fallback=llm_result.used_fallback,
    )
