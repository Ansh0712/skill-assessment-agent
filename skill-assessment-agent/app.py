import streamlit as st
import plotly.graph_objects as go
import json
import pandas as pd
from agent.orchestrator import AgentOrchestrator
from utils.pdf_parser import extract_text_from_upload

st.set_page_config(
    page_title="AI Skill Assessor",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .metric-card {
        background: #f8f9fa; border-radius: 12px; padding: 20px;
        text-align: center; border: 1px solid #e9ecef; margin-bottom: 10px;
    }
    .phase-card {
        background: #ffffff; border-left: 4px solid #4CAF50;
        padding: 15px; margin: 10px 0; border-radius: 0 8px 8px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .badge-green {
        display: inline-block; padding: 4px 12px; border-radius: 16px;
        margin: 2px; font-size: 0.85em; background: #d4edda; color: #155724;
    }
    .badge-red {
        display: inline-block; padding: 4px 12px; border-radius: 16px;
        margin: 2px; font-size: 0.85em; background: #f8d7da; color: #721c24;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "agent" not in st.session_state:
    st.session_state.agent = AgentOrchestrator()
if "stage" not in st.session_state:
    st.session_state.stage = "input"
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "assessment_feedback" not in st.session_state:
    st.session_state.assessment_feedback = []


def reset_app():
    st.session_state.agent = AgentOrchestrator()
    st.session_state.stage = "input"
    st.session_state.current_question = None
    st.session_state.chat_history = []
    st.session_state.assessment_feedback = []


with st.sidebar:
    st.title("🎯 AI Skill Assessor")
    st.markdown("---")
    stages = ["input", "review", "assess", "results", "plan"]
    stage_labels = ["📝 Input", "🔍 Review", "💬 Assess", "📊 Results", "📚 Plan"]
    current_idx = stages.index(st.session_state.stage)
    for i, (stg, label) in enumerate(zip(stages, stage_labels)):
        if i <= current_idx:
            st.markdown(f"**✅ {label}**")
        elif i == current_idx + 1:
            st.markdown(f"**➡️ {label}**")
        else:
            st.markdown(f"⬜ {label}")
    st.markdown("---")
    if st.button("🔄 Start Over", use_container_width=True):
        reset_app()
        st.rerun()
    st.markdown("---")
    st.markdown("### How it works")
    st.markdown("1. **Input** JD and resume\n2. **Review** extracted skills\n"
                "3. **Answer** adaptive questions\n4. **View** gap analysis\n"
                "5. **Get** personalised learning plan")


# ── STAGE 1: INPUT ──────────────────────────────────
if st.session_state.stage == "input":
    st.header("📝 Step 1: Provide Job Description & Resume")
    st.markdown("Paste or upload the job description and candidate resume to begin.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Job Description")
        jd_method = st.radio("Input method:", ["Paste text", "Upload file"], key="jd_method", horizontal=True)
        if jd_method == "Paste text":
            jd_text = st.text_area("Paste JD here:", height=300, placeholder="Paste the full job description...")
        else:
            jd_file = st.file_uploader("Upload JD", type=["pdf", "txt"], key="jd_file")
            jd_text = extract_text_from_upload(jd_file) if jd_file else ""

    with col2:
        st.subheader("Candidate Resume")
        resume_method = st.radio("Input method:", ["Paste text", "Upload file"], key="resume_method", horizontal=True)
        if resume_method == "Paste text":
            resume_text = st.text_area("Paste resume here:", height=300, placeholder="Paste the full resume...")
        else:
            resume_file = st.file_uploader("Upload resume", type=["pdf", "txt"], key="resume_file")
            resume_text = extract_text_from_upload(resume_file) if resume_file else ""

    st.markdown("---")
    col_sample, col_submit = st.columns([1, 2])
    with col_sample:
        if st.button("📄 Load Sample Data"):
            try:
                with open("sample_data/sample_jd.txt", "r") as f:
                    st.session_state["sample_jd"] = f.read()
                with open("sample_data/sample_resume.txt", "r") as f:
                    st.session_state["sample_resume"] = f.read()
                st.rerun()
            except FileNotFoundError:
                st.warning("Sample files not found.")

    if "sample_jd" in st.session_state and jd_method == "Paste text":
        jd_text = st.session_state.get("sample_jd", jd_text)
    if "sample_resume" in st.session_state and resume_method == "Paste text":
        resume_text = st.session_state.get("sample_resume", resume_text)

    with col_submit:
        if st.button("🔍 Extract & Compare Skills", type="primary",
                     use_container_width=True, disabled=not (jd_text and resume_text)):
            with st.spinner("🔄 Analyzing job description and resume..."):
                result = st.session_state.agent.extract_and_compare(jd_text, resume_text)
                if "error" not in result:
                    st.session_state.skills_data = result
                    st.session_state.stage = "review"
                    st.rerun()
                else:
                    st.error(f"Error: {result['error']}")


# ── STAGE 2: REVIEW SKILLS ─────────────────────────
elif st.session_state.stage == "review":
    st.header("🔍 Step 2: Review Extracted Skills")
    data = st.session_state.skills_data

    st.subheader("📋 Required Skills from JD")
    cols = st.columns(3)
    for i, skill in enumerate(data.get("required_skills", [])):
        with cols[i % 3]:
            weight_emoji = "🔴" if skill["weight"] == 3 else ("🟡" if skill["weight"] == 2 else "🟢")
            desc = skill.get("description", "")
            st.markdown(
                f'<div class="metric-card">'
                f'<h4>{weight_emoji} {skill["skill"]}</h4>'
                f'<p><b>{skill["category"]}</b> · Weight: {skill["weight"]}/3 '
                f'· Required: {skill["required_level"]}/5</p>'
                f'<small>{desc}</small></div>',
                unsafe_allow_html=True,
            )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Skill Overlap")
        for skill in data.get("skill_overlap", []):
            st.markdown(f'<span class="badge-green">{skill}</span>', unsafe_allow_html=True)
    with col2:
        st.subheader("⚠️ Potential Gaps")
        for skill in data.get("potential_gaps", []):
            st.markdown(f'<span class="badge-red">{skill}</span>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("💬 Start Skill Assessment", type="primary", use_container_width=True):
        question = st.session_state.agent.get_next_question()
        st.session_state.current_question = question
        st.session_state.stage = "assess"
        st.rerun()


# ── STAGE 3: ASSESSMENT ────────────────────────────
elif st.session_state.stage == "assess":
    st.header("💬 Step 3: Skill Assessment")
    agent = st.session_state.agent
    question = st.session_state.current_question

    if question and not question.get("done") and not question.get("error"):
        progress = (question["skill_index"] - 1) / question["total_skills"]
        st.progress(progress, text=f"Skill {question['skill_index']}/{question['total_skills']}")

        for entry in st.session_state.chat_history:
            with st.chat_message(entry["role"]):
                st.markdown(entry["content"])

        difficulty_label = {1: "🟢 Basic", 2: "🟡 Intermediate", 3: "🔴 Advanced"}
        with st.chat_message("assistant"):
            st.markdown(
                f"**Assessing: {question['skill']}** "
                f"(Q{question['question_number']} · "
                f"{difficulty_label.get(question['difficulty'], '🟡')})"
            )
            st.markdown(question["question"])

        answer = st.chat_input("Type your answer here...")
        if answer:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"**{question['skill']}** ({difficulty_label.get(question['difficulty'], '')})\n\n{question['question']}"
            })
            st.session_state.chat_history.append({"role": "user", "content": answer})

            with st.spinner("Evaluating your response..."):
                evaluation = agent.submit_answer(answer)

            score = evaluation.get("score", 0)
            score_color = "🟢" if score >= 4 else ("🟡" if score >= 2 else "🔴")
            feedback = f"{score_color} **Score: {score}/5** — {evaluation.get('justification', '')}"
            st.session_state.chat_history.append({"role": "assistant", "content": feedback})
            st.session_state.assessment_feedback.append(evaluation)

            if evaluation.get("moving_to_next") and not agent.assessor.is_complete:
                next_q = agent.get_next_question()
                st.session_state.current_question = next_q
            elif agent.assessor.is_complete:
                st.session_state.current_question = {"done": True}
            st.rerun()

    elif question and question.get("error"):
        st.error(f"Error: {question['error']}")
    else:
        st.success("✅ Assessment complete! All skills have been evaluated.")
        for entry in st.session_state.chat_history:
            with st.chat_message(entry["role"]):
                st.markdown(entry["content"])
        st.markdown("---")
        if st.button("📊 View Gap Analysis & Results", type="primary", use_container_width=True):
            with st.spinner("Analyzing results..."):
                st.session_state.gap_results = agent.run_gap_analysis()
                st.session_state.stage = "results"
                st.rerun()


# ── STAGE 4: RESULTS ───────────────────────────────
elif st.session_state.stage == "results":
    st.header("📊 Step 4: Assessment Results & Gap Analysis")
    gap_data = st.session_state.gap_results
    gaps = gap_data["gaps"]
    summary = gap_data["summary"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Avg Proficiency", f"{summary.get('average_proficiency', 0)}/5")
    with c2:
        st.metric("Skills at Level", summary.get("skills_at_level", 0))
    with c3:
        st.metric("Below Level", summary.get("skills_below_level", 0))
    with c4:
        st.metric("Critical Gaps", summary.get("critical_gaps", 0))

    st.markdown("---")

    if gaps:
        categories = [g["skill"] for g in gaps]
        current_scores = [g["current_level"] for g in gaps]
        required_scores = [g["required_level"] for g in gaps]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=current_scores + [current_scores[0]],
            theta=categories + [categories[0]],
            fill="toself", name="Current Level",
            line_color="#FF6B6B", fillcolor="rgba(255,107,107,0.2)",
        ))
        fig.add_trace(go.Scatterpolar(
            r=required_scores + [required_scores[0]],
            theta=categories + [categories[0]],
            fill="toself", name="Required Level",
            line_color="#4ECDC4", fillcolor="rgba(78,205,196,0.2)",
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            showlegend=True, title="Skills Radar: Current vs Required", height=500,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Detailed Gap Analysis")
    from agent.scorer import assign_priority_label
    for g in gaps:
        priority = assign_priority_label(g["priority_score"])
        emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
        with st.expander(f"{emoji} {g['skill']} — Gap: {g['gap']} | Priority: {priority.upper()}"):
            cc1, cc2, cc3 = st.columns(3)
            with cc1:
                st.metric("Current", f"{g['current_level']}/5")
            with cc2:
                st.metric("Required", f"{g['required_level']}/5")
            with cc3:
                st.metric("Priority Score", g["priority_score"])
            if g["strengths"]:
                st.markdown("**Strengths:** " + ", ".join(g["strengths"]))
            if g["weaknesses"]:
                st.markdown("**Improve:** " + ", ".join(g["weaknesses"]))

    st.markdown("---")
    if st.button("📚 Generate Learning Plan", type="primary", use_container_width=True):
        with st.spinner("Generating your personalised learning plan..."):
            plan = st.session_state.agent.create_learning_plan()
            st.session_state.learning_plan = plan
            st.session_state.stage = "plan"
            st.rerun()


# ── STAGE 5: LEARNING PLAN ─────────────────────────
elif st.session_state.stage == "plan":
    st.header("📚 Step 5: Your Personalised Learning Plan")
    plan = st.session_state.learning_plan

    if "error" in plan:
        st.error(plan["error"])
    elif "message" in plan and not plan.get("learning_plan"):
        st.success(plan["message"])
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total Hours", f"{plan.get('total_estimated_hours', 'N/A')}h")
        with c2:
            st.metric("Timeline", f"{plan.get('total_timeline_weeks', 'N/A')} weeks")
        with c3:
            st.metric("Skills to Learn", len(plan.get("learning_plan", [])))

        quick_wins = plan.get("quick_wins", [])
        if quick_wins:
            st.subheader("⚡ Quick Wins (< 2 weeks)")
            for qw in quick_wins:
                st.markdown(f"- ✅ {qw}")

        schedule = plan.get("study_schedule_suggestion", "")
        if schedule:
            st.info(f"📅 **Recommended Schedule:** {schedule}")

        st.markdown("---")

        for item in plan.get("learning_plan", []):
            p_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(
                item.get("priority", "medium"), "⚪"
            )
            with st.expander(
                f"{p_emoji} {item['skill']} — "
                f"{item.get('current_level', '?')} → {item.get('target_level', '?')} | "
                f"{item.get('estimated_hours', '?')}h / {item.get('timeline_weeks', '?')} weeks",
                expanded=item.get("priority") in ["critical", "high"],
            ):
                transferable = item.get("transferable_from", [])
                if transferable:
                    ts = item.get("transferability_score", 0)
                    st.markdown(f"🔗 **Builds on:** {', '.join(transferable)} (Transferability: {ts:.0%})")

                current = item.get("current_level", 0)
                target = item.get("target_level", 5)
                st.progress(min(current / 5, 1.0), text=f"Current: {current}/5 → Target: {target}/5")

                for phase in item.get("learning_path", []):
                    phase_name = phase.get("phase", "")
                    phase_dur = phase.get("duration", "")
                    phase_mile = phase.get("milestone", "N/A")
                    st.markdown(
                        f'<div class="phase-card">'
                        f'<h4>📖 {phase_name} ({phase_dur})</h4>'
                        f'<p><b>Milestone:</b> {phase_mile}</p></div>',
                        unsafe_allow_html=True,
                    )
                    for obj in phase.get("objectives", []):
                        st.markdown(f"  - 🎯 {obj}")
                    st.markdown("  **Resources:**")
                    for res in phase.get("resources", []):
                        url = res.get("url", "#")
                        cost = res.get("cost", "free")
                        hours = res.get("estimated_hours", "?")
                        rtype = res.get("type", "resource")
                        title = res.get("title", "Resource")
                        st.markdown(f"  - [{title}]({url}) ({rtype} · {cost} · ~{hours}h)")

        st.markdown("---")
        st.subheader("📅 Timeline Overview")
        timeline_data = []
        for item in plan.get("learning_plan", []):
            for phase in item.get("learning_path", []):
                timeline_data.append({
                    "Skill": item["skill"],
                    "Phase": phase.get("phase", ""),
                    "Duration": phase.get("duration", "TBD"),
                    "Milestone": phase.get("milestone", ""),
                })
        if timeline_data:
            st.dataframe(pd.DataFrame(timeline_data), use_container_width=True)

        st.markdown("---")
        st.download_button(
            "⬇️ Download Learning Plan (JSON)",
            data=json.dumps(plan, indent=2),
            file_name="personalised_learning_plan.json",
            mime="application/json",
            use_container_width=True,
        )
