# 🎓 AutoMentor AI

> **Autonomous AI Study Companion, Live Interactive Notebook & Portfolio Builder**  
> Built for the **All Things Agentic Hackathon** using **Gemini 3.5 Flash / Pro**, **Google Agent Development Kit (ADK)**, and **Google Cloud**.

---

## 📌 Overview

**AutoMentor** is a truly autonomous AI study companion designed to remove friction from technical education. It doesn't just answer questions—it actively guides the student through a living workspace:

1. **📚 Socratic Discovery & Multimodal Ingestion:** Ingests college slides, PDFs, and syllabus topics to extract a structured knowledge graph using Gemini 3.5.
2. **📓 Autonomous Interactive Notebook (Live AI Canvas):** A reactive workspace where the Mentor autonomously generates theory cells, injects realistic code challenges, inserts intentional bugs for debugging practice, and executes tests in real-time.
3. **🎯 Gap Detection:** Calibrates current understanding through Socratic questioning to isolate specific knowledge gaps.
4. **📅 Autonomous Scheduling:** Finds free slots on **Google Calendar** and books focused micro-study sessions.
5. **🧪 Hands-on Lab Generation:** Generates real **GitHub repositories** with scaffolding, Dockerfiles, and unit tests for the student to clone and solve.
6. **🤖 Automated PR Review:** Evaluates Pull Requests with Socratic technical feedback directly in GitHub comments.
7. **🚀 1-Click Showcase:** Drafts technical **LinkedIn articles** and updates the GitHub profile README with verified skill badges upon mastery.

---

## 🏗️ System Architecture

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

## 📓 The Autonomous Notebook Engine

The **Autonomous Interactive Notebook** is the core collaborative canvas where learning happens:
* **Mentor-Manipulated Cells:** The agent dynamically creates markdown explanations, adds architecture diagrams, and scaffolds code cells with editable syntax.
* **Instant Client-Side Execution (Pyodide Wasm):** Python code and unit tests run instantly in the student's browser without latency or compute costs.
* **Adaptive Bug Injection & Socratic Breakpoints:** The Mentor introduces calibrated bugs according to the student's mastery score (< 0.4: validation errors, 0.4-0.7: schema mismatch, > 0.7: concurrency deadlocks).
* **Progressive 3-Tier Hint Ladder:** 1) Mental Model analogy, 2) Pseudocode logic, 3) Edge-case condition.

---

## 🚀 Quick Start (Local Setup)

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

### 2. Frontend (Next.js Cockpit)
```bash
cd frontend
npm install
npm run dev
```
Open **[http://localhost:3000](http://localhost:3000)** to access the full AutoMentor Cockpit.

---

## 🧪 Reproducible Testing Instructions

For judges and evaluators to verify the autonomous agent, tool executions, and full-stack behavior in a clean environment:

### 1. Automated Test Battery (38 Test Scenarios — 100% Pass Rate)

Ensure your Python virtual environment is activated, then run the comprehensive test suite:

```bash
# Option A: Standard Pytest execution with verbose output
pytest tests/ -v

# Option B: Run the formatted test battery runner
python run_test_battery.py
```

#### 📊 Test Suites Coverage Breakdown:

| Test File | Focus Area | Scenarios Covered |
| :--- | :--- | :--- |
| `tests/test_student_scenarios.py` | Student Cognitive Flows | Exam panic, conceptual misconceptions, cheat attempts, short inputs, mastery celebrations. |
| `tests/test_tool_execution.py` | Actuator Executions | Google Calendar Ebbinghaus intervals (D+1 to D+14), GitHub multi-stack scaffolding (Python, Go, TS), LinkedIn Showcases, Cheat Sheets. |
| `tests/test_pr_evaluator_deep.py` | Automated PR Reviewer | Perfect submissions, buggy diffs, empty pull requests, markdown GitHub comment generation. |
| `tests/test_knowledge_graph_memory.py` | Firestore / Memory Graph | Node lifecycle progression, filtering, Bloom taxonomy, Ebbinghaus decay tracking. |
| `tests/test_ingestion_edge_cases.py` | Multimodal Ingestion | Corrupted PDF fallbacks, structured syllabus concept extraction, accents/multilingual preservation. |
| `tests/test_end_to_end_scenarios.py` | Full Golden Path & Cloud Run | End-to-end autonomous student journey from panic prompt to LinkedIn showcase; OpenAPI spec compliance. |
| `tests/test_api.py` | FastAPI Server Endpoints | `/health`, `/api/chat`, `/api/graph`, `/api/ingest/pdf`, `/api/webhooks/github`. |

---

### 2. End-to-End Full-Stack Verification (Cockpit UI)

1. Start both servers:
   ```bash
   # Terminal 1: Backend API (Port 8000)
   python -m uvicorn automentor.api.server:app --port 8000

   # Terminal 2: Next.js Frontend (Port 3000)
   cd frontend && npm run dev
   ```
2. Open `http://localhost:3000` in your browser.
3. **Verify Socratic Flow:** Send `"Tenho prova de gRPC"` in the chat — observe the Socratic question and the Google Calendar booking card.
4. **Verify WASM Test Runner:** Click `[ ▶ Executar Testes (Wasm) ]` in the notebook to watch Pyodide execute Python tests client-side.
5. **Verify Fault Injection:** Click `[ 🐛 Injetar Bug Calibrado ]` to observe adaptive bug injection and test failure diagnosis.
6. **Verify Hint Ladder:** Click on the `[ Dicas em 3 Camadas ]` accordion to unlock Tier 1, Tier 2, and Tier 3 hints.
7. **Verify 100% Mastery:** Send `"Protobuf usa tags numéricas fixas e serialização binária com varints"` to trigger the confetti celebration and LinkedIn showcase modal.

---

## ☁️ Google Cloud Deployment (Cloud Run)

To deploy the serverless backend to Google Cloud Run:

```bash
# Ensure gcloud CLI is authenticated
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Deploy using the automated script
./deploy_cloudrun.sh        # Linux / MacOS
./deploy_cloudrun.ps1       # Windows PowerShell
```

---

## 📜 License

MIT License — Built with ❤️ for the Google **All Things Agentic Hackathon**.
