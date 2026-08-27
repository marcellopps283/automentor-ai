# 🎓 AutoMentor AI

> **Autonomous AI Study Companion & Portfolio Builder**  
> Built for the **All Things Agentic Hackathon** using **Gemini 3.5 Flash / Pro**, **Google Agent Development Kit (ADK)**, and **Google Cloud**.

---

## 📌 Overview

**AutoMentor** is a truly autonomous AI study companion designed to remove friction from technical education. It doesn't just answer questions—it actively guides the student through:

1. **📚 Socratic Discovery & Ingestion:** Ingests college slides, PDFs, and syllabus topics to extract a structured knowledge graph.
2. **🎯 Gap Detection:** Calibrates current understanding through Socratic questioning to isolate specific knowledge gaps.
3. **📅 Autonomous Scheduling:** Finds free slots on **Google Calendar** and books focused micro-study sessions.
4. **🧪 Hands-on Lab Generation:** Generates real **GitHub repositories** with scaffolding, buggy code, and unit tests for the student to solve.
5. **🤖 Automated Code Review:** Evaluates Pull Requests with Socratic technical feedback.
6. **🚀 1-Click Showcase:** Drafts technical **LinkedIn articles** and updates the GitHub profile README with verified skill badges upon mastery.

---

## 🏗️ Architecture

- **AI Brain:** Gemini 3.5 Flash / Pro & Gemini Live API
- **Orchestration:** Google Agent Development Kit (ADK) / Google GenAI SDK
- **Persistence & Knowledge Graph:** Google Cloud Firestore & Cloud Storage
- **Compute:** Google Cloud Run (Serverless)
- **Background Autonomy:** Cloud Scheduler & Cloud Tasks
- **Integrations (Actuators):** Google Calendar API, GitHub REST API, LinkedIn API
