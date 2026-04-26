import json
from utils.llm_client import create_completion
from agent.prompts import LEARNING_PLAN_PROMPT
from agent.scorer import assign_priority_label


def generate_learning_plan(assessment_results, gaps, skills_data):
    strong_skills = [
        f"{skill} (Level {data.get('final_score', 0)})"
        for skill, data in assessment_results.items()
        if data.get("final_score", 0) >= 3
    ]

    formatted_results = []
    for skill, data in assessment_results.items():
        fs = data.get("final_score", 0)
        rl = data.get("required_level", 3)
        formatted_results.append(f"- {skill}: Score {fs}/5 (Required: {rl})")

    formatted_gaps = []
    for g in gaps:
        if g["gap"] > 0:
            wk = ", ".join(g["weaknesses"][:3]) if g["weaknesses"] else "N/A"
            priority = assign_priority_label(g["priority_score"])
            formatted_gaps.append(
                f"- {g['skill']}: Current {g['current_level']}/5 -> "
                f"Need {g['required_level']}/5 "
                f"(Gap: {g['gap']}, Priority: {priority})\n"
                f"  Weaknesses: {wk}"
            )

    if not formatted_gaps:
        return {
            "learning_plan": [],
            "message": "Congratulations! No significant skill gaps detected.",
        }

    role_skills = [s["skill"] for s in skills_data.get("required_skills", [])]
    role_summary = f"Role requires: {', '.join(role_skills)}"

    prompt = LEARNING_PLAN_PROMPT.format(
        strong_skills=", ".join(strong_skills) if strong_skills else "None identified",
        assessment_results="\n".join(formatted_results),
        skill_gaps="\n".join(formatted_gaps),
        role_summary=role_summary,
    )

    try:
        response_text = create_completion(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert L&D consultant. Return only valid JSON.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
            json_mode=True,
        )
        return json.loads(response_text)
    except json.JSONDecodeError:
        return {"error": "Failed to parse learning plan"}
    except Exception as e:
        return {"error": f"Learning plan failed: {str(e)}"}
