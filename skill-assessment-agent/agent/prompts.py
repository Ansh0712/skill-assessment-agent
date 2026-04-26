SKILL_EXTRACTION_PROMPT = """Analyze the following Job Description and Candidate Resume.

## Job Description:
{job_description}

## Candidate Resume:
{resume}

Extract and return a JSON object with this EXACT structure:
{{
  "required_skills": [
    {{
      "skill": "Skill Name",
      "category": "must-have" or "nice-to-have",
      "weight": 1-3,
      "required_level": 1-5,
      "description": "What this skill entails for this role"
    }}
  ],
  "candidate_claimed_skills": [
    {{
      "skill": "Skill Name",
      "years_experience": null,
      "context": "Where/how they used it"
    }}
  ],
  "skill_overlap": ["skills appearing in both JD and resume"],
  "potential_gaps": ["required skills NOT evident in resume"]
}}

Be thorough. Identify 6-12 required skills. Return ONLY valid JSON."""


ASSESSMENT_QUESTION_PROMPT = """You are an expert technical interviewer assessing proficiency in **{skill}**.

Context about the role: {skill_description}
Candidate background: {candidate_context}
Difficulty level: {difficulty} (1=basic, 2=intermediate, 3=advanced)
Previous questions asked: {previous_questions}

Generate ONE focused assessment question that:
1. Tests practical, applied knowledge
2. Is appropriate for the difficulty level
3. Can be answered in 2-4 sentences
4. Is DIFFERENT from previous questions

Return JSON:
{{
  "question": "Your question here",
  "evaluation_criteria": "What a strong answer includes",
  "difficulty_level": {difficulty}
}}

Return ONLY valid JSON."""


RESPONSE_EVALUATION_PROMPT = """Evaluate the candidate response to a technical question.

Skill: {skill}
Question: {question}
Expected: {criteria}
Response: {response}

Score rubric:
0 = No knowledge
1 = Vague awareness
2 = Basic understanding
3 = Solid intermediate
4 = Advanced understanding
5 = Expert level

Return JSON:
{{
  "score": 0-5,
  "justification": "Brief explanation",
  "strengths": ["demonstrated well"],
  "weaknesses": ["gaps identified"],
  "follow_up_needed": true or false
}}

Return ONLY valid JSON."""


LEARNING_PLAN_PROMPT = """Create a personalised learning plan based on this gap analysis.

## Candidate Profile:
Strong skills: {strong_skills}
Results: {assessment_results}

## Skill Gaps:
{skill_gaps}

## Target Role:
{role_summary}

For each gap, consider:
1. ADJACENT SKILLS that transfer
2. REALISTIC TIMELINES
3. CURATED RESOURCES (free and paid)
4. MILESTONES to measure progress

Return JSON:
{{
  "learning_plan": [
    {{
      "skill": "Name",
      "current_level": 0-5,
      "target_level": 1-5,
      "priority": "critical" or "high" or "medium" or "low",
      "transferable_from": ["existing skills"],
      "transferability_score": 0.0-1.0,
      "estimated_hours": 40,
      "timeline_weeks": 4,
      "learning_path": [
        {{
          "phase": "Phase name",
          "duration": "Week 1-2",
          "objectives": ["objectives"],
          "resources": [
            {{
              "title": "Resource name",
              "type": "course or book or tutorial or project",
              "url": "URL",
              "cost": "free or $XX",
              "estimated_hours": 10
            }}
          ],
          "milestone": "What you can do after"
        }}
      ]
    }}
  ],
  "total_estimated_hours": 120,
  "total_timeline_weeks": 12,
  "quick_wins": ["achievable in under 2 weeks"],
  "study_schedule_suggestion": "weekly commitment"
}}

Return ONLY valid JSON."""
