import json
from utils.llm_client import create_completion


def extract_skills(job_description, resume):
    from agent.prompts import SKILL_EXTRACTION_PROMPT
    prompt = SKILL_EXTRACTION_PROMPT.format(
        job_description=job_description,
        resume=resume
    )
    try:
        response_text = create_completion(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert HR analyst. Return only valid JSON."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            json_mode=True
        )
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse response: {str(e)}"}
    except Exception as e:
        return {"error": f"Skill extraction failed: {str(e)}"}
