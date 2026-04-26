# 🎯 AI-Powered Skill Assessment & Personalised Learning Plan Agent

An intelligent agent that takes a Job Description and a candidate's resume, conversationally assesses real proficiency on each required skill, identifies gaps, and generates a personalised learning plan with curated resources and time estimates.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up your API key (free Groq account)
cp .env.example .env
# Edit .env and add your GROQ_API_KEY from console.groq.com

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

## Supported LLM Providers (all free)

| Provider | Setup |
|----------|-------|
| **Groq** | Get free key at console.groq.com |
| **Google Gemini** | Get free key at aistudio.google.com |
| **Ollama** | Install from ollama.com for local inference |
| **OpenAI** | Get key at platform.openai.com (paid) |
