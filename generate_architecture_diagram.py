"""
Architecture Diagram Generator for AutoMentor AI
Produces a crisp, high-resolution 1920x1080 PNG diagram suitable for Devpost submission.
"""

import sys
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

WIDTH, HEIGHT = 1920, 1080
OUTPUT_PNG = "automentor_architecture_diagram.png"

def render_diagram():
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(15, 23, 42)) # Slate 900
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 46)
        font_subtitle = ImageFont.truetype("arial.ttf", 24)
        font_box_title = ImageFont.truetype("arial.ttf", 26)
        font_box_sub = ImageFont.truetype("arial.ttf", 20)
        font_text = ImageFont.truetype("arial.ttf", 18)
        font_badge = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        font_title = ImageFont.load_default()
        font_subtitle = font_title
        font_box_title = font_title
        font_box_sub = font_title
        font_text = font_title
        font_badge = font_title

    # Header
    draw.rectangle([(0, 0), (WIDTH, 12)], fill=(59, 130, 246)) # Blue accent top
    draw.text((80, 50), "AutoMentor AI - End-to-End System Architecture", fill=(255, 255, 255), font=font_title)
    draw.text((80, 110), "All Things Agentic Hackathon  |  Google Cloud, Gemini 3.5 Flash & Google Agent Development Kit (ADK)", fill=(148, 163, 184), font=font_subtitle)

    # 4 Main Columns / Layers

    # 1. FRONTEND COCKPIT (Left)
    x1, y1, w1, h1 = 80, 180, 400, 780
    draw.rounded_rectangle([(x1, y1), (x1 + w1, y1 + h1)], radius=18, fill=(24, 33, 47), outline=(59, 130, 246), width=2)
    draw.rounded_rectangle([(x1 + 20, y1 + 20), (x1 + w1 - 20, y1 + 70)], radius=10, fill=(30, 58, 138))
    draw.text((x1 + 40, y1 + 32), "1. FRONTEND COCKPIT", fill=(255, 255, 255), font=font_box_title)
    draw.text((x1 + 30, y1 + 85), "Next.js 15 (App Router) - React 19", fill=(147, 197, 253), font=font_box_sub)

    components_fe = [
        ("Socratic Chat & Voice", "- Multi-turn Socratic questions\n- Inline Action Cards\n- 1-Click approval buttons"),
        ("Live Interactive Notebook", "- Monaco Code Editor\n- Markdown Theory Cells\n- 3-Tier Hint Ladder"),
        ("Pyodide Wasm Engine", "- Zero-latency Python execution\n- Client-side Pytest runner\n- Adaptive Bug Diagnosis"),
        ("Knowledge Graph Visualizer", "- 2D Node Map (Mastery / Gaps)\n- Ebbinghaus Retention Widget\n- Fullscreen Mock Tech Interview")
    ]
    cy = y1 + 130
    for title, desc in components_fe:
        draw.rounded_rectangle([(x1 + 20, cy), (x1 + w1 - 20, cy + 135)], radius=12, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
        draw.text((x1 + 35, cy + 12), title, fill=(96, 165, 250), font=font_box_sub)
        draw.text((x1 + 35, cy + 42), desc, fill=(203, 213, 225), font=font_text)
        cy += 155

    # 2. SERVERLESS BACKEND (Middle Left)
    x2, y2, w2, h2 = 520, 180, 420, 780
    draw.rounded_rectangle([(x2, y2), (x2 + w2, y2 + h2)], radius=18, fill=(24, 33, 47), outline=(168, 85, 247), width=2)
    draw.rounded_rectangle([(x2 + 20, y2 + 20), (x2 + w2 - 20, y2 + 70)], radius=10, fill=(88, 28, 135))
    draw.text((x2 + 40, y2 + 32), "2. CLOUD RUN BACKEND", fill=(255, 255, 255), font=font_box_title)
    draw.text((x2 + 30, y2 + 85), "FastAPI - Google ADK Orchestrator", fill=(216, 180, 254), font=font_box_sub)

    components_be = [
        ("Gemini 3.5 Flash Brain", "- Google GenAI SDK v2.20\n- Socratic Cognitive Guardrails\n- Tool Calling & Function Dispatch"),
        ("Multimodal Ingestion Service", "- PDF Syllabus parsing (pypdf)\n- Topic & Competency extraction\n- Prerequisite dependency tree"),
        ("Automated PR Reviewer", "- GitHub Webhook receiver\n- Unified git diff evaluation\n- Socratic code review comments"),
        ("REST API & Webhooks", "- OpenAPI endpoints (/api/chat)\n- Serverless auto-scaling\n- Containerized in Docker")
    ]
    cy = y2 + 130
    for title, desc in components_be:
        draw.rounded_rectangle([(x2 + 20, cy), (x2 + w2 - 20, cy + 135)], radius=12, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
        draw.text((x2 + 35, cy + 12), title, fill=(192, 132, 252), font=font_box_sub)
        draw.text((x2 + 35, cy + 42), desc, fill=(203, 213, 225), font=font_text)
        cy += 155

    # 3. GOOGLE CLOUD MEMORY (Middle Right)
    x3, y3, w3, h3 = 980, 180, 420, 780
    draw.rounded_rectangle([(x3, y3), (x3 + w3, y3 + h3)], radius=18, fill=(24, 33, 47), outline=(234, 179, 8), width=2)
    draw.rounded_rectangle([(x3 + 20, y3 + 20), (x3 + w3 - 20, y3 + 70)], radius=10, fill=(113, 63, 18))
    draw.text((x3 + 40, y3 + 32), "3. PERSISTENCE & MEMORY", fill=(255, 255, 255), font=font_box_title)
    draw.text((x3 + 30, y3 + 85), "Google Cloud Firestore & Storage", fill=(253, 224, 71), font=font_box_sub)

    components_mem = [
        ("Google Cloud Firestore", "- Student Knowledge Graph nodes\n- Mastery scores (0.0 to 1.0)\n- Bloom taxonomy classification"),
        ("Ebbinghaus Retention Engine", "- Spaced repetition tracking\n- D+1, D+3, D+7, D+14 schedules\n- Next-review-due calculation"),
        ("Google Cloud Storage (GCS)", "- Uploaded lecture slides & PDFs\n- Generated code assets & cheatsheets\n- Audio & test artifact caching"),
        ("Local Fallback Storage", "- Embedded JSON memory store\n- Zero-downtime offline mode\n- Instant recovery mechanism")
    ]
    cy = y3 + 130
    for title, desc in components_mem:
        draw.rounded_rectangle([(x3 + 20, cy), (x3 + w3 - 20, cy + 135)], radius=12, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
        draw.text((x3 + 35, cy + 12), title, fill=(250, 204, 21), font=font_box_sub)
        draw.text((x3 + 35, cy + 42), desc, fill=(203, 213, 225), font=font_text)
        cy += 155

    # 4. EXTERNAL ACTUATORS (Right)
    x4, y4, w4, h4 = 1440, 180, 400, 780
    draw.rounded_rectangle([(x4, y4), (x4 + w4, y4 + h4)], radius=18, fill=(24, 33, 47), outline=(34, 197, 94), width=2)
    draw.rounded_rectangle([(x4 + 20, y4 + 20), (x4 + w4 - 20, y4 + 70)], radius=10, fill=(20, 83, 45))
    draw.text((x4 + 40, y4 + 32), "4. REAL-WORLD ACTUATORS", fill=(255, 255, 255), font=font_box_title)
    draw.text((x4 + 30, y4 + 85), "Autonomous Ecosystem Integrations", fill=(134, 239, 172), font=font_box_sub)

    components_act = [
        ("Google Calendar API", "- Micro-study session booking\n- Ebbinghaus interval calculation\n- Web reservation links"),
        ("GitHub Lab Scaffolder", "- Repositories creation via API\n- Dockerfile & Pytest templates\n- Multi-language CI Workflows"),
        ("1-Click Showcase Tool", "- Recruiter-ready LinkedIn posts\n- Markdown badges for READMEs\n- Resume bullet point generation"),
        ("Cheat Sheet Generator", "- High-yield exam study guides\n- Markdown, Notion & Obsidian sync\n- Pitfall & mental model summary")
    ]
    cy = y4 + 130
    for title, desc in components_act:
        draw.rounded_rectangle([(x4 + 20, cy), (x4 + w4 - 20, cy + 135)], radius=12, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
        draw.text((x4 + 35, cy + 12), title, fill=(74, 222, 128), font=font_box_sub)
        draw.text((x4 + 35, cy + 42), desc, fill=(203, 213, 225), font=font_text)
        cy += 155

    # Connecting Flow Arrows / Badges at bottom
    draw.rounded_rectangle([(80, 990), (1840, 1040)], radius=12, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    draw.text((120, 1005), "Flow: Multimodal Ingestion -> Socratic Diagnosis -> Live WASM Notebook -> Cloud Memory -> Calendar & GitHub Actuation", fill=(226, 232, 240), font=font_badge)

    img.save(OUTPUT_PNG)
    print(f"[DiagramEngine] SUCCESS: Diagram rendered at: {OUTPUT_PNG}")

if __name__ == "__main__":
    render_diagram()
