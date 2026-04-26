import json
from utils.llm_client import create_completion
from utils.config import MAX_QUESTIONS_PER_SKILL
from agent.prompts import ASSESSMENT_QUESTION_PROMPT, RESPONSE_EVALUATION_PROMPT


class AdaptiveAssessor:
    def __init__(self, skills_data):
        self.skills_data = skills_data
        self.required_skills = skills_data.get("required_skills", [])
        self.candidate_skills = skills_data.get("candidate_claimed_skills", [])
        self.current_skill_index = 0
        self.current_difficulty = 2
        self.questions_asked_for_current = 0
        self.assessment_results = {}
        self.current_question_data = None

    @property
    def current_skill(self):
        if self.current_skill_index < len(self.required_skills):
            return self.required_skills[self.current_skill_index]
        return None

    @property
    def is_complete(self):
        return self.current_skill_index >= len(self.required_skills)

    def get_candidate_context(self, skill_name):
        for cs in self.candidate_skills:
            if skill_name.lower() in cs["skill"].lower() or cs["skill"].lower() in skill_name.lower():
                ctx = cs.get("context", "No context")
                yrs = cs.get("years_experience", "?")
                return f"{cs['skill']}: {ctx} ({yrs} years)"
        return "No prior experience claimed."

    def generate_question(self):
        skill = self.current_skill
        if not skill:
            return {"done": True}

        skill_name = skill["skill"]
        prev_questions = []
        if skill_name in self.assessment_results:
            prev_questions = [
                r["question"] for r in self.assessment_results[skill_name].get("responses", [])
            ]

        prompt = ASSESSMENT_QUESTION_PROMPT.format(
            skill=skill_name,
            skill_description=skill.get("description", ""),
            candidate_context=self.get_candidate_context(skill_name),
            difficulty=self.current_difficulty,
            previous_questions=json.dumps(prev_questions) if prev_questions else "None"
        )

        try:
            response_text = create_completion(
                messages=[
                    {"role": "system", "content": "You are an expert interviewer. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                json_mode=True
            )
            question_data = json.loads(response_text)
            self.current_question_data = question_data
            return {
                "skill": skill_name,
                "skill_index": self.current_skill_index + 1,
                "total_skills": len(self.required_skills),
                "question": question_data["question"],
                "difficulty": self.current_difficulty,
                "question_number": self.questions_asked_for_current + 1,
                "done": False,
            }
        except (json.JSONDecodeError, KeyError) as e:
            return {"error": f"Failed to generate question: {str(e)}"}

    def evaluate_response(self, user_response):
        skill = self.current_skill
        skill_name = skill["skill"]

        prompt = RESPONSE_EVALUATION_PROMPT.format(
            skill=skill_name,
            question=self.current_question_data["question"],
            criteria=self.current_question_data.get("evaluation_criteria", ""),
            response=user_response,
        )

        try:
            response_text = create_completion(
                messages=[
                    {"role": "system", "content": "You are an expert evaluator. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                json_mode=True
            )
            evaluation = json.loads(response_text)
        except Exception:
            evaluation = {
                "score": 2, "justification": "Could not parse",
                "strengths": [], "weaknesses": [], "follow_up_needed": False,
            }

        if skill_name not in self.assessment_results:
            self.assessment_results[skill_name] = {
                "responses": [],
                "required_level": skill.get("required_level", 3),
                "weight": skill.get("weight", 2),
                "category": skill.get("category", "must-have"),
            }

        self.assessment_results[skill_name]["responses"].append({
            "question": self.current_question_data["question"],
            "answer": user_response,
            "score": evaluation.get("score", 2),
            "difficulty": self.current_difficulty,
            "justification": evaluation.get("justification", ""),
            "strengths": evaluation.get("strengths", []),
            "weaknesses": evaluation.get("weaknesses", []),
        })

        self.questions_asked_for_current += 1
        score = evaluation.get("score", 2)

        should_continue = self.questions_asked_for_current < MAX_QUESTIONS_PER_SKILL
        if should_continue and evaluation.get("follow_up_needed", False):
            if score >= 3:
                self.current_difficulty = min(3, self.current_difficulty + 1)
            elif score <= 2:
                self.current_difficulty = max(1, self.current_difficulty - 1)
        else:
            should_continue = False

        if not should_continue:
            responses = self.assessment_results[skill_name]["responses"]
            total_weight = 0
            weighted_sum = 0
            for r in responses:
                w = r["difficulty"]
                weighted_sum += r["score"] * w
                total_weight += w
            final_score = round(weighted_sum / total_weight, 1) if total_weight > 0 else 0
            self.assessment_results[skill_name]["final_score"] = final_score

            self.current_skill_index += 1
            self.current_difficulty = 2
            self.questions_asked_for_current = 0

        evaluation["moving_to_next"] = not should_continue
        evaluation["skill_assessed"] = skill_name
        if not should_continue and skill_name in self.assessment_results:
            evaluation["final_skill_score"] = self.assessment_results[skill_name].get("final_score", score)

        return evaluation
