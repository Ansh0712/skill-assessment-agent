# 🎯 AI-Powered Skill Assessment & Personalised Learning Plan Agent

An intelligent agent that takes a Job Description and a candidate's resume, conversationally assesses real proficiency on each required skill, identifies gaps, and generates a personalised learning plan with curated resources and time estimates.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up API key
cp .env.example .env
# Edit .env and add your GROQ_API_KEY from console.groq.com currently I have added my grok key

# 3. Run
streamlit run app.py
```

## Features

- Extracts and compares skills from JD and resume using AI
- Adaptive difficulty assessment (easy to hard based on responses)
- 0-5 proficiency scoring with detailed justification
- Gap analysis with priority scoring and radar chart visualization
- Personalised learning plan with curated resources and timelines
- Supports multiple free LLM providers (Groq, Google Gemini, Ollama)

