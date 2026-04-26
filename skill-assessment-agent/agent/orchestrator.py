from agent.skill_extractor import extract_skills
from agent.assessor import AdaptiveAssessor
from agent.scorer import calculate_gap_analysis, generate_summary_stats
from agent.learning_plan import generate_learning_plan


class AgentOrchestrator:
    def __init__(self):
        self.skills_data = None
        self.assessor = None
        self.gaps = None
        self.learning_plan_data = None
        self.summary_stats = None
        self.state = "init"

    def extract_and_compare(self, job_description, resume):
        self.skills_data = extract_skills(job_description, resume)
        if "error" not in self.skills_data:
            self.assessor = AdaptiveAssessor(self.skills_data)
            self.state = "extracted"
        return self.skills_data

    def get_next_question(self):
        if not self.assessor:
            return {"error": "Skills not yet extracted"}
        self.state = "assessing"
        return self.assessor.generate_question()

    def submit_answer(self, answer):
        if not self.assessor:
            return {"error": "No active assessment"}
        return self.assessor.evaluate_response(answer)

    def run_gap_analysis(self):
        if not self.assessor or not self.assessor.assessment_results:
            return {"error": "Assessment not complete"}
        self.gaps = calculate_gap_analysis(self.assessor.assessment_results)
        self.summary_stats = generate_summary_stats(self.gaps)
        self.state = "analyzed"
        return {"gaps": self.gaps, "summary": self.summary_stats}

    def create_learning_plan(self):
        if not self.gaps:
            return {"error": "Gap analysis not complete"}
        self.learning_plan_data = generate_learning_plan(
            self.assessor.assessment_results, self.gaps, self.skills_data
        )
        self.state = "planned"
        return self.learning_plan_data
