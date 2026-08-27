# AutoMentor AI

> **Autonomous AI Study Companion, Live Interactive Notebook & Portfolio Builder**  
> Built for the **All Things Agentic Hackathon** using **Gemini 3.5 Flash / Pro**, **Google Agent Development Kit (ADK)**, and **Google Cloud**.

---

## Overview

**AutoMentor** is an autonomous AI study companion designed to remove friction from technical education. It actively guides students through a living workspace:

1. **Socratic Discovery & Multimodal Ingestion:** Ingests college slides, PDFs, and syllabus topics to extract a structured knowledge graph using Gemini 3.5.
2. **Autonomous Interactive Notebook (Live AI Canvas):** A reactive workspace where the Mentor autonomously generates theory cells, injects realistic code challenges, inserts intentional bugs for debugging practice, and executes tests in real-time.
3. **Gap Detection:** Calibrates current understanding through Socratic questioning to isolate specific knowledge gaps.
4. **Autonomous Scheduling:** Finds free slots on **Google Calendar** and books focused micro-study sessions.
5. **Hands-on Lab Generation:** Generates real **GitHub repositories** with scaffolding, Dockerfiles, and unit tests for the student to clone and solve.
6. **Automated PR Review:** Evaluates Pull Requests with Socratic technical feedback directly in GitHub comments.
7. **1-Click Showcase:** Drafts technical **LinkedIn articles** and updates the GitHub profile README with verified skill badges upon mastery.

---

## System Architecture

```
                                  ┌────────────────────────────────────────────────────────┐
                                  │               AUTONOMOR COCKPIT (FRONTEND)             │
                                  │                                                        │
                                  │  ┌──────────────────────┐  ┌────────────────────────┐  │
                                  │  │ Socratic Chat & Voice│  │  Autonomous Live       │  │
                                  │  │ (Gemini Live Audio)  │  │  Interactive Notebook  │  │
                                  │  │ • Inline Action Cards│  │  • Markdown Theory     │  │
                                  │  │ • 1-Click Approvals  │  │  • Monaco Code Cells   │  │
                                  │  │ • PDF Dropzone       │  │  • Pyodide Wasm Runner │  │
                                  │  └──────────┬───────────┘  └───────────┬────────────┘  │
                                  └─────────────┼──────────────────────────┼───────────────┘
                                                │                          │
                                                │ HTTPS / WSS              │ In-browser Wasm
                                                ▼                          ▼
                                  ┌────────────────────────────────────────────────────────┐
                                  │          CLOUD RUN SERVERLESS BACKEND (FASTAPI)        │
                                  │                                                        │
                                  │  ┌──────────────────────────────────────────────────┐  │
                                  │  │ Google ADK Orchestrator & Gemini 3.5 Brain       │  │
                                  │  │ • Socratic Dialog Engine                         │  │
                                  │  │ • Automated PR Code Reviewer                     │  │
                                  │  │ • Multimodal PDF / Syllabus Ingestion            │  │
                                  │  └──────────────────────┬───────────────────────────┘  │
                                  └─────────────────────────┼──────────────────────────────┘
                                                            │
                 ┌──────────────────────────────────────────┼──────────────────────────────────────────┐
                 ▼                                          ▼                                          ▼
   ┌───────────────────────────┐              ┌───────────────────────────┐              ┌───────────────────────────┐
   │  Google Cloud Storage     │              │  Google Cloud Tasks &     │              │  External Actuators       │
   │  & Firestore Memory       │              │  Scheduler Engine         │              │  (Real-World Actions)     │
   │                           │              │                           │              │                           │
   │ • Knowledge Graph Nodes   │              │ • Ebbinghaus Spaced Rep.  │              │ • Google Calendar API     │
   │ • Mastery Scores & Logs   │              │ • Asynchronous PR Queues  │              │ • GitHub REST API (Labs)  │
   │ • Lecture PDFs & Assets   │              │ • Daily Routine Audit     │              │ • LinkedIn Share API      │
   └───────────────────────────┘              └───────────────────────────┘              └───────────────────────────┘
```

---

## The Autonomous Notebook Engine

The **Autonomous Interactive Notebook** is the core collaborative canvas where learning happens:
* **Mentor-Manipulated Cells:** The agent dynamically creates markdown explanations, adds architecture diagrams, and scaffolds code cells with editable syntax.
* **Instant Client-Side Execution (Pyodide Wasm):** Python code and unit tests run instantly in the student's browser without latency or compute costs.
* **Live Bug Injection & Socratic Breakpoints:** The Mentor can purposefully introduce edge-case bugs into the notebook for the student to diagnose and fix.
* **Seamless Git Sync:** The completed notebook solution can be exported with 1-click to a dedicated GitHub repository.

---

## Quick Start (Local Setup)

### 1. Backend & CLI
```bash
# Clone the repository
git clone https://github.com/marcellopps283/automentor-ai.git
cd automentor-ai

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows (.venv/bin/activate on Linux/Mac)

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Run the Socratic CLI
automentor

# Or start the FastAPI Backend Server
python -m automentor.api.server
```

### 2. Frontend (Next.js Dashboard)
```bash
cd frontend
npm install
npm run dev
```
Open **[http://localhost:3000](http://localhost:3000)** to access the full AutoMentor Cockpit.

---

## Testing

Run the automated test suite with pytest:
```bash
pytest
```
