import streamlit as st

from services.data_service import get_intern_options, get_intern_profile, parse_intern_id
from services.growth_plan_service import generate_growth_plan


st.set_page_config(page_title="实习生成长助手", layout="wide")

st.title("实习生成长助手")
st.caption("回答实习生最核心的问题：我现在该学什么、做什么、问导师什么。")

options = get_intern_options()
selected = st.sidebar.selectbox("选择实习生", options)
intern_id = parse_intern_id(selected)
profile_data = get_intern_profile(intern_id)
profile = profile_data["profile"]

left, right = st.columns([1, 1])

with left:
    st.subheader(f"{profile['name']}｜{profile['role']}实习生")
    st.markdown(
        f"""
**当前阶段**：第 {int(profile['current_week'])} 周  
**适岗分**：{profile['fit_score']}  
**适岗等级**：{profile['level']}  
**风险等级**：{profile['risk_level']}
"""
    )
    question = st.text_area(
        "我的困惑",
        value=f"我是{profile['role']}岗实习生，现在第 {int(profile['current_week'])} 周，不知道接下来该重点学什么？",
        height=140,
    )
    generate_clicked = st.button("生成本周成长建议", type="primary")

with right:
    st.subheader("当前能力短板参考")
    for key, value in profile_data["ability_scores"].items():
        st.progress(int(value), text=f"{key}：{value:.0f}/100")

st.divider()

if generate_clicked or question:
    plan = generate_growth_plan(profile, question)

    st.subheader(f"当前阶段：{plan.stage}")
    c1, c2 = st.columns(2)

    with c1:
        st.write("本周学习重点：")
        for item in plan.learning_focus:
            st.markdown(f"- {item}")

        st.write("推荐任务：")
        for item in plan.recommended_tasks:
            st.markdown(f"- {item}")

    with c2:
        st.write("建议交付物：")
        for item in plan.deliverables:
            st.markdown(f"- {item}")

        st.write("主动向导师确认的问题：")
        for item in plan.mentor_questions:
            st.markdown(f"- {item}")

    source_text = "规则模板 fallback" if plan.used_fallback else f"LLM：{plan.llm_provider}"
    st.caption(f"生成来源：{source_text}")
    st.success(plan.encouragement)
