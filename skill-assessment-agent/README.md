# 🎯 AI-Powered Skill Assessment & Personalised Learning Plan Agent

> A resume tells you what someone *claims* to know — not how well they actually know it.

This agent takes a **Job Description** and a **Candidate's Resume**, conversationally assesses real proficiency on each required skill through adaptive questioning, identifies gaps, and generates a **personalised learning plan** focused on adjacent skills the candidate can realistically acquire — with curated resources and time estimates.

---

## 📋 Table of Contents

- [Live Demo](#-live-demo)
- [Demo Video](#-demo-video)
- [Features](#-features)
- [Architecture Diagram](#-architecture-diagram)
- [Scoring & Logic](#-scoring--logic-description)
- [Sample Inputs & Outputs](#-sample-inputs--outputs)
- [Local Setup Instructions](#-local-setup-instructions)
- [Deployment](#-deployment)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)

---

## 🌐 Live Demo

🔗 **Deployed URL:** [https://skill-assessment-agent.streamlit.app](https://skill-assessment-agent.streamlit.app)

> *(Replace with your actual deployed URL)*

No installation needed — open the link and start using immediately.

---

## 🎥 Demo Video

📹 **Watch the 4-minute walkthrough:** [YouTube/Loom Link Here]

> *(Replace with your actual video URL)*

### Video Walkthrough Summary

| Timestamp | What's Shown |
|-----------|-------------|
| `0:00 - 0:30` | **Introduction** — Problem statement: resumes ≠ real skill proficiency |
| `0:30 - 1:00` | **Step 1: Input** — Paste sample Job Description and Resume |
| `1:00 - 1:30` | **Step 2: Skill Extraction** — AI extracts required skills, identifies overlaps and gaps |
| `1:30 - 3:00` | **Step 3: Adaptive Assessment** — Live Q&A with difficulty adjustment based on responses |
| `3:00 - 3:30` | **Step 4: Gap Analysis** — Radar chart visualization, priority scoring, detailed breakdown |
| `3:30 - 4:30` | **Step 5: Learning Plan** — Personalised roadmap with resources, timelines, quick wins |
| `4:30 - 5:00` | **Wrap-up** — Download plan, summary of how scoring works |

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 **Smart Skill Extraction** | AI parses JD and resume to extract, categorize, and compare skills |
| 💬 **Conversational Assessment** | Chat-based interview that feels natural, not like a quiz |
| 🔄 **Adaptive Difficulty** | Questions get harder or easier based on your answers (easy → medium → hard) |
| 📊 **Radar Chart Visualization** | Visual comparison of current vs. required skill levels |
| 🎯 **Priority-Weighted Gap Analysis** | Gaps scored by importance: `gap × weight × category_multiplier` |
| 🔗 **Adjacent Skill Detection** | Identifies which existing skills transfer to new ones (transferability score) |
| 📚 **Curated Learning Plan** | Phase-by-phase roadmap with specific courses, books, tutorials, and projects |
| ⏱️ **Time Estimates** | Realistic hour and week estimates based on current level and transferability |
| ⚡ **Quick Wins** | Highlights skills achievable in under 2 weeks |
| 📥 **Downloadable Plan** | Export learning plan as JSON for tracking |
| 📎 **PDF Upload Support** | Upload resume and JD as PDF or paste as text |
| 🆓 **Free LLM Support** | Works with Groq (free), Google Gemini (free), Ollama (local), or OpenAI |

---

## 🏗️ Architecture Diagram
