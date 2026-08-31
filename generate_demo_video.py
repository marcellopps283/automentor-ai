"""
Programmatic Video Generator for AutoMentor AI Demo
Synthesizes high-resolution 1080p visual scenes, audio narration with Google TTS,
and composes a complete .mp4 video using MoviePy and FFmpeg.
"""

import os
import sys
import tempfile
from pathlib import Path

# Fix Windows console encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
import moviepy as mp

OUTPUT_VIDEO = "automentor_demo_video.mp4"
WIDTH, HEIGHT = 1920, 1080

SCENES = [
    {
        "id": "scene_1_intro",
        "title": "AutoMentor AI",
        "subtitle": "Autonomous Socratic Study Companion & Portfolio Builder",
        "badge": "All Things Agentic Hackathon - Google Cloud & Gemini 3.5 Flash",
        "bullets": [
            "Socratic Guidance: Eliminating passive copying and tutorial hell",
            "Autonomous Interactive Notebook with Live In-Browser Pyodide Execution",
            "Proactive Actuators: Google Calendar, GitHub Labs, PR Reviews & LinkedIn Showcases"
        ],
        "bg_color": (15, 23, 42),
        "accent_color": (59, 130, 246),
        "narration": "Welcome to AutoMentor AI, built for the All Things Agentic Hackathon using Gemini 3.5 Flash, Google Agent Development Kit, and Google Cloud. Computer science students often get trapped in tutorial hell or passive AI copying. AutoMentor solves this by being a truly autonomous, Socratic collaborative partner that guides learning through first principles."
    },
    {
        "id": "scene_2_ingestion",
        "title": "Multimodal Ingestion & Socratic Diagnosis",
        "subtitle": "Transforming College Syllabi & PDFs into an Active Knowledge Graph",
        "badge": "Gemini 3.5 Multimodal - Google Cloud Firestore",
        "bullets": [
            "Instant PDF Extraction: Parses university slides and syllabus topics",
            "Dynamic Knowledge Graph: Maps prerequisites and Bloom taxonomy levels",
            "Socratic Calibration: Diagnoses exact conceptual gaps before generating code"
        ],
        "bg_color": (15, 23, 42),
        "accent_color": (168, 85, 247),
        "narration": "AutoMentor ingests university lecture slides and exam syllabi in PDF format, extracting structured competencies into an active Knowledge Graph. Instead of giving away answers, it asks probing questions to calibrate understanding and pinpoint exact knowledge gaps in real-time."
    },
    {
        "id": "scene_3_actuators",
        "title": "Autonomous Real-World Actuators",
        "subtitle": "Closing the Loop with Google Calendar, GitHub & Spaced Repetition",
        "badge": "Real-World Action Triad - Zero-Friction Execution",
        "bullets": [
            "Google Calendar: Books Ebbinghaus spaced-repetition blocks (D+1, D+3, D+7)",
            "GitHub Lab Scaffolding: Injects Dockerfile, unit tests and CI workflows",
            "Google Cloud Firestore: Stores mastery scores and learning trajectories"
        ],
        "bg_color": (15, 23, 42),
        "accent_color": (34, 197, 94),
        "narration": "When a gap is detected, AutoMentor takes autonomous action in the real world: it books focused spaced-repetition study blocks on Google Calendar, scaffolds practical lab repositories on GitHub with Dockerfiles and unit tests, and persists the learner's state in Google Cloud Firestore."
    },
    {
        "id": "scene_4_notebook",
        "title": "Autonomous Live Notebook & Hint Ladder",
        "subtitle": "In-Browser Wasm Code Execution with Monaco Editor & Adaptive Bugs",
        "badge": "Pyodide Wasm Runner - Monaco Editor - 3-Tier Hint Ladder",
        "bullets": [
            "Client-Side Python/Pytest: Instant, zero-latency execution in the browser",
            "Adaptive Fault Injection: Injects bugs calibrated to student skill level",
            "Progressive 3-Tier Hints: Mental Model -> Pseudocode -> Edge-Case Clues"
        ],
        "bg_color": (15, 23, 42),
        "accent_color": (234, 179, 8),
        "narration": "Inside the Cockpit, students work in an Autonomous Live Notebook. The mentor injects adaptive bugs calibrated to the student's skill level, provides progressive three-tier hints, and validates code instantly using client-side Pyodide WebAssembly."
    },
    {
        "id": "scene_5_showcase",
        "title": "PR Webhooks, 1-Click Showcase & Mock Interview",
        "subtitle": "Turning Mastery into Verified Portfolios & Job-Ready Skills",
        "badge": "GitHub Webhooks - LinkedIn Share API - Mock Tech Interview",
        "bullets": [
            "Automated PR Review: GitHub webhooks evaluate student pull requests",
            "1-Click Showcase: Auto-generates technical LinkedIn articles upon mastery",
            "Mock Tech Interview: Fullscreen oral exam simulation with hiring scorecards"
        ],
        "bg_color": (15, 23, 42),
        "accent_color": (236, 72, 153),
        "narration": "When students open Pull Requests, webhooks trigger automated Socratic code reviews. Upon reaching full mastery, AutoMentor auto-generates technical LinkedIn showcase articles. Students can also launch immersive Mock Tech Interviews for real-time oral exam preparation."
    },
    {
        "id": "scene_6_cloud",
        "title": "Google Cloud Architecture & Hackathon Readiness",
        "subtitle": "Production Serverless Backend on Google Cloud Run",
        "badge": "Google Cloud Run - Google ADK - 38 Automated Tests Passing",
        "bullets": [
            "Cloud Run Backend: Serverless FastAPI container with production Dockerfile",
            "100% Test Coverage: 38 deep automated tests verifying all agentic workflows",
            "Open Source on GitHub: github.com/marcellopps283/automentor-ai"
        ],
        "bg_color": (15, 23, 42),
        "accent_color": (59, 130, 246),
        "narration": "AutoMentor is fully containerized on Google Cloud Run with complete end-to-end reliability and 38 automated test suites. AutoMentor: Empowering the next generation of engineers through autonomous Socratic mentorship."
    }
]

def create_scene_image(scene_data: dict, output_path: str):
    img = Image.new("RGB", (WIDTH, HEIGHT), color=scene_data["bg_color"])
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 64)
        font_sub = ImageFont.truetype("arial.ttf", 34)
        font_badge = ImageFont.truetype("arial.ttf", 26)
        font_bullet = ImageFont.truetype("arial.ttf", 36)
        font_footer = ImageFont.truetype("arial.ttf", 24)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = font_title
        font_badge = font_title
        font_bullet = font_title
        font_footer = font_title

    # Header Accent Line
    draw.rectangle([(0, 0), (WIDTH, 14)], fill=scene_data["accent_color"])

    # Badge Pill
    badge_text = f"  {scene_data['badge']}  "
    draw.rounded_rectangle([(100, 70), (1050, 125)], radius=15, fill=(30, 41, 59), outline=scene_data["accent_color"], width=2)
    draw.text((120, 82), badge_text, fill=(241, 245, 249), font=font_badge)

    # Title & Subtitle
    draw.text((100, 160), scene_data["title"], fill=(255, 255, 255), font=font_title)
    draw.text((100, 250), scene_data["subtitle"], fill=(148, 163, 184), font=font_sub)

    # Card Box for Bullets
    draw.rounded_rectangle([(100, 340), (1820, 920)], radius=24, fill=(24, 33, 47), outline=(51, 65, 85), width=2)

    # Bullet Points
    y_offset = 420
    for bullet in scene_data["bullets"]:
        draw.ellipse([(140, y_offset + 10), (160, y_offset + 30)], fill=scene_data["accent_color"])
        draw.text((190, y_offset), bullet, fill=(241, 245, 249), font=font_bullet)
        y_offset += 150

    # Footer
    draw.text((100, 980), "AutoMentor AI - All Things Agentic Hackathon (Devpost & Google Cloud)", fill=(100, 116, 139), font=font_footer)
    draw.text((1400, 980), "Gemini 3.5 Flash | Google ADK", fill=(100, 116, 139), font=font_footer)

    img.save(output_path)

def build_video():
    print("[VideoEngine] Starting AutoMentor Demo Video Generation...")
    temp_dir = tempfile.mkdtemp()
    clips = []

    for idx, scene in enumerate(SCENES):
        print(f"[VideoEngine] [{idx+1}/{len(SCENES)}] Processing: {scene['title']}...")
        
        # 1. Synthesize Speech with gTTS
        audio_path = os.path.join(temp_dir, f"audio_{scene['id']}.mp3")
        tts = gTTS(text=scene["narration"], lang="en", slow=False)
        tts.save(audio_path)

        # 2. Render 1080p Frame
        img_path = os.path.join(temp_dir, f"frame_{scene['id']}.png")
        create_scene_image(scene, img_path)

        # 3. Create Audio & Video Clip
        audio_clip = mp.AudioFileClip(audio_path)
        duration = audio_clip.duration + 1.0

        image_clip = mp.ImageClip(img_path).with_duration(duration)
        image_clip = image_clip.with_audio(audio_clip)

        clips.append(image_clip)

    print("[VideoEngine] Concatenating video clips with audio tracks...")
    final_video = mp.concatenate_videoclips(clips, method="compose")
    
    print(f"[VideoEngine] Rendering final 1080p MP4 to {OUTPUT_VIDEO}...")
    final_video.write_videofile(
        OUTPUT_VIDEO,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        threads=4
    )

    print(f"[VideoEngine] SUCCESS: Video generated at {OUTPUT_VIDEO} (Duration: {final_video.duration:.1f}s)")

if __name__ == "__main__":
    build_video()
