from typing import List


def calculate_gap_analysis(assessment_results):
    gaps = []
    for skill_name, data in assessment_results.items():
        final_score = data.get("final_score", 0)
        required_level = data.get("required_level", 3)
        weight = data.get("weight", 2)
        category = data.get("category", "must-have")
        gap = required_level - final_score
        if gap <= 0:
            gap = 0
        category_multiplier = 1.5 if category == "must-have" else 1.0
        priority_score = gap * weight * category_multiplier
        gaps.append({
            "skill": skill_name,
            "current_level": final_score,
            "required_level": required_level,
            "gap": round(gap, 1),
            "weight": weight,
            "category": category,
            "priority_score": round(priority_score, 1),
            "strengths": _collect_field(data, "strengths"),
            "weaknesses": _collect_field(data, "weaknesses"),
        })
    gaps.sort(key=lambda x: x["priority_score"], reverse=True)
    return gaps


def _collect_field(data, field):
    items = []
    for r in data.get("responses", []):
        items.extend(r.get(field, []))
    return list(set(items))


def assign_priority_label(priority_score):
    if priority_score >= 6:
        return "critical"
    elif priority_score >= 3:
        return "high"
    elif priority_score >= 1:
        return "medium"
    else:
        return "low"


def generate_summary_stats(gaps):
    if not gaps:
        return {}
    scores = [g["current_level"] for g in gaps]
    gap_values = [g["gap"] for g in gaps]
    return {
        "average_proficiency": round(sum(scores) / len(scores), 1),
        "skills_at_level": len([g for g in gaps if g["gap"] <= 0]),
        "skills_below_level": len([g for g in gaps if g["gap"] > 0]),
        "critical_gaps": len([g for g in gaps if g["priority_score"] >= 6]),
        "largest_gap_skill": max(gaps, key=lambda x: x["gap"])["skill"] if gaps else None,
        "strongest_skill": max(gaps, key=lambda x: x["current_level"])["skill"] if gaps else None,
        "total_gap_points": round(sum(gap_values), 1),
    }
