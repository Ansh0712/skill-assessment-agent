# 🎯 AI Skill Assessment & Learning Plan Agent

An AI agent that goes beyond resume screening — it **conversationally tests real skill proficiency**, 
identifies gaps against a job description, and generates a **personalised learning roadmap** 
with curated resources and time estimates.

---

## 💡 The Problem

Resumes show **claims**, not **proof**. Listing "Kubernetes" doesn't mean production-level expertise.
This agent finds the truth through adaptive questioning and builds a plan to close the gaps.

---

## 🔧 Approach

1. **Extract** — AI parses JD and resume, identifies required skills, overlaps, and gaps
2. **Assess** — Adaptive chat-based Q&A per skill (difficulty adjusts based on answers)
3. **Score** — Each response scored 0-5 with weighted averaging
4. **Analyze** — Gap analysis with priority ranking: `gap × weight × category_multiplier`
5. **Plan** — Personalised learning path leveraging adjacent skill transferability

---

## 🏗️ Architecture
# 🎯 AI Skill Assessment & Learning Plan Agent

An AI agent that goes beyond resume screening — it **conversationally tests real skill proficiency**, 
identifies gaps against a job description, and generates a **personalised learning roadmap** 
with curated resources and time estimates.

---

## 💡 The Problem

Resumes show **claims**, not **proof**. Listing "Kubernetes" doesn't mean production-level expertise.
This agent finds the truth through adaptive questioning and builds a plan to close the gaps.

---

## 🔧 Approach

1. **Extract** — AI parses JD and resume, identifies required skills, overlaps, and gaps
2. **Assess** — Adaptive chat-based Q&A per skill (difficulty adjusts based on answers)
3. **Score** — Each response scored 0-5 with weighted averaging
4. **Analyze** — Gap analysis with priority ranking: `gap × weight × category_multiplier`
5. **Plan** — Personalised learning path leveraging adjacent skill transferability

---

## 🏗️ Architecture
# 🎯 AI Skill Assessment & Learning Plan Agent

An AI agent that goes beyond resume screening — it **conversationally tests real skill proficiency**, 
identifies gaps against a job description, and generates a **personalised learning roadmap** 
with curated resources and time estimates.

---

## 💡 The Problem

Resumes show **claims**, not **proof**. Listing "Kubernetes" doesn't mean production-level expertise.
This agent finds the truth through adaptive questioning and builds a plan to close the gaps.

---

## 🔧 Approach

1. **Extract** — AI parses JD and resume, identifies required skills, overlaps, and gaps
2. **Assess** — Adaptive chat-based Q&A per skill (difficulty adjusts based on answers)
3. **Score** — Each response scored 0-5 with weighted averaging
4. **Analyze** — Gap analysis with priority ranking: `gap × weight × category_multiplier`
5. **Plan** — Personalised learning path leveraging adjacent skill transferability

---

## 🏗️ Architecture
JD + Resume
│
▼
┌──────────────┐ ┌───────────────┐ ┌──────────────┐
│ Skill │────▶│ Adaptive │────▶│ Learning │
│ Extractor │ │ Assessor │ │ Plan Gen │
│ │ │ │ │ │
│ • Parse JD │ │ • Ask Q (L1-3)│ │ • Gap Scores │
│ • Parse CV │ │ • Eval Answer │ │ • Resources │
│ • Compare │ │ • Adapt Level │ │ • Timelines │
└──────────────┘ └───────┬───────┘ └──────────────┘
│
┌────────▼────────┐
│ Scoring Engine │
│ │
│ score = Σ(s×d) │
│ ───── │
│ Σ(d) │
│ │
│ priority = gap │
│ × weight │
│ × category │
└────────┬────────┘
│
┌────────▼────────┐
│ LLM Provider │
│ │
│ Groq (free) ⭐ │
│ Gemini (free) │
│ Ollama (local) │
│ OpenAI (paid) │
└─────────────────┘


**Scoring Rubric:** 0=None → 1=Awareness → 2=Beginner → 3=Intermediate → 4=Advanced → 5=Expert

**Adaptive Logic:** Score ≥ 3 → harder question | Score ≤ 2 → easier question

**Time Estimation:** `hours = base × (1 - transferability) × gap`

---

## 📁 Project Structure

├── app.py # Streamlit UI (5 stages)
├── agent/
│ ├── orchestrator.py # Pipeline controller
│ ├── skill_extractor.py # JD + Resume parsing
│ ├── assessor.py # Adaptive Q&A engine
│ ├── scorer.py # Gap analysis & scoring
│ ├── learning_plan.py # Plan generator
│ └── prompts.py # LLM prompts
├── utils/
│ ├── config.py # Environment config
│ ├── llm_client.py # Multi-provider LLM client
│ └── pdf_parser.py # PDF parsing
├── sample_data/ # Test JD & resume
├── requirements.txt
├── .env.example
└── README.md


## Run Locally
1. Download the skill-assessment-agent from github
2. open command prompt and install requirements.txt (python install -r reqirements.txt)
3. python -m streamlit run app.py
4. it will run locally on a localhost
