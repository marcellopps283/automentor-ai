"""
Master Pitch Video Synthesizer for AutoMentor AI
Combines:
1. High-impact Intro Hook (Problem & Vision)
2. Actual Live Screen Recording of the App with synchronized voiceover narration
3. Google Cloud Architecture & Hackathon Outro
Outputs: automentor_pitch_video.mp4
"""

import os
import sys
import tempfile
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
import moviepy as mp

OUTPUT_PITCH_MP4 = "automentor_pitch_video.mp4"
WIDTH, HEIGHT = 1920, 1080

def create_slide(title, subtitle, badge, bullets, accent_color, output_path):
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 62)
        font_sub = ImageFont.truetype("arial.ttf", 32)
        font_badge = ImageFont.truetype("arial.ttf", 24)
        font_bullet = ImageFont.truetype("arial.ttf", 34)
        font_footer = ImageFont.truetype("arial.ttf", 22)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = font_title
        font_badge = font_title
        font_bullet = font_title
        font_footer = font_title

    # Header Accent
    draw.rectangle([(0, 0), (WIDTH, 14)], fill=accent_color)

    # Badge Pill
    draw.rounded_rectangle([(100, 70), (1050, 120)], radius=15, fill=(30, 41, 59), outline=accent_color, width=2)
    draw.text((120, 82), f"  {badge}  ", fill=(241, 245, 249), font=font_badge)

    # Title & Subtitle
    draw.text((100, 150), title, fill=(255, 255, 255), font=font_title)
    draw.text((100, 240), subtitle, fill=(148, 163, 184), font=font_sub)

    # Card
    draw.rounded_rectangle([(100, 320), (1820, 920)], radius=24, fill=(24, 33, 47), outline=(51, 65, 85), width=2)

    y_offset = 390
    for bullet in bullets:
        draw.ellipse([(140, y_offset + 10), (160, y_offset + 30)], fill=accent_color)
        draw.text((190, y_offset), bullet, fill=(241, 245, 249), font=font_bullet)
        y_offset += 130

    # Footer
    draw.text((100, 980), "AutoMentor AI — All Things Agentic Hackathon Pitch (Devpost & Google Cloud)", fill=(100, 116, 139), font=font_footer)
    draw.text((1450, 980), "Gemini 3.5 Flash • Google ADK", fill=(100, 116, 139), font=font_footer)

    img.save(output_path)

def build_pitch():
    print("[PitchEngine] 1. Preparing temp assets and voiceover narration...")
    temp_dir = tempfile.mkdtemp()

    # --- Intro Scene ---
    intro_img = os.path.join(temp_dir, "intro.png")
    create_slide(
        title="🎓 AutoMentor AI: The Autonomous Socratic Partner",
        subtitle="Moving from Passive Code Generation to True Engineering Mastery",
        badge="All Things Agentic Hackathon • Google Cloud Track",
        bullets=[
            "The Problem: Students suffer from AI vending machine syndrome and tutorial hell.",
            "The Solution: A Socratic AI Companion with an Autonomous Live Notebook.",
            "Real Actuators: Autonomous Google Calendar scheduling & GitHub lab scaffolding.",
            "Zero-Latency WASM Execution: Client-side testing powered by Pyodide."
        ],
        accent_color=(59, 130, 246),
        output_path=intro_img
    )

    intro_narration = (
        "Welcome to AutoMentor AI. Most AI tools act like vending machines, spitting out answers and causing "
        "cognitive atrophy. AutoMentor is a truly autonomous Socratic collaborative partner that guides computer science "
        "students through first principles, active live notebooks, and real-world actuators."
    )
    intro_audio_path = os.path.join(temp_dir, "intro_audio.mp3")
    gTTS(text=intro_narration, lang="en").save(intro_audio_path)
    intro_audio = mp.AudioFileClip(intro_audio_path)
    intro_clip = mp.ImageClip(intro_img).with_duration(intro_audio.duration + 0.5).with_audio(intro_audio)

    # --- Live App Walkthrough Scene ---
    live_video_path = os.path.abspath("automentor_live_demo.mp4")
    if not os.path.exists(live_video_path):
        print("Live video not found!")
        return

    live_clip = mp.VideoFileClip(live_video_path)
    
    live_narration = (
        "Here is AutoMentor running live. In the Cockpit, the student tracks memory decay with Ebbinghaus spaced repetition. "
        "When the student asks for help with distributed systems, the mentor diagnoses the knowledge gap and autonomously books a study session on Google Calendar. "
        "In the live interactive notebook, students run Python tests in WebAssembly. The mentor can inject adaptive bugs calibrated to the student's exact skill level, "
        "and provide progressive three-tier hints. "
        "Students can export cheat sheets, explore the 2D Knowledge Graph, or launch an immersive Mock Tech Interview with Google Meet style scorecards. "
        "Once mastered, confetti celebrates their achievement with a one-click LinkedIn showcase post ready for recruiters."
    )
    live_audio_path = os.path.join(temp_dir, "live_audio.mp3")
    gTTS(text=live_narration, lang="en").save(live_audio_path)
    live_audio = mp.AudioFileClip(live_audio_path)

    # Adjust live video duration to match narration smoothly
    if live_clip.duration < live_audio.duration:
        live_clip = live_clip.with_duration(live_audio.duration + 0.5)
    else:
        # Loop or set duration
        live_clip = live_clip.subclipped(0, min(live_clip.duration, live_audio.duration + 1.0))
    live_clip = live_clip.with_audio(live_audio)

    # --- Outro Scene ---
    outro_img = os.path.join(temp_dir, "outro.png")
    create_slide(
        title="☁️ Architecture & Google Cloud Production Readiness",
        subtitle="Serverless Backend on Cloud Run with Google Agent Development Kit",
        badge="Google Cloud Run • Google ADK • 38 Automated Tests Passing",
        bullets=[
            "Google ADK & Gemini 3.5 Flash: Multi-turn Socratic agent with tool calling.",
            "Google Cloud Run & Firestore: Serverless backend and persistent Knowledge Graph.",
            "Exhaustive Test Suite: 38/38 automated tests passing (100% success rate).",
            "Open Source on GitHub: github.com/marcellopps283/automentor-ai"
        ],
        accent_color=(34, 197, 94),
        output_path=outro_img
    )

    outro_narration = (
        "Under the hood, AutoMentor runs on Google Cloud Run with Firestore memory, Google ADK orchestration, and thirty-eight automated test suites. "
        "AutoMentor AI: Empowering the next generation of engineers through autonomous Socratic mentorship. Thank you!"
    )
    outro_audio_path = os.path.join(temp_dir, "outro_audio.mp3")
    gTTS(text=outro_narration, lang="en").save(outro_audio_path)
    outro_audio = mp.AudioFileClip(outro_audio_path)
    outro_clip = mp.ImageClip(outro_img).with_duration(outro_audio.duration + 1.0).with_audio(outro_audio)

    # Concatenate final pitch video
    print("[PitchEngine] 2. Concatenating all scenes into master pitch video...")
    pitch_video = mp.concatenate_videoclips([intro_clip, live_clip, outro_clip], method="compose")

    print(f"[PitchEngine] 3. Rendering {OUTPUT_PITCH_MP4} at 1080p...")
    pitch_video.write_videofile(
        OUTPUT_PITCH_MP4,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="fast",
        threads=4
    )

    print(f"[PitchEngine] ✓ SUCCESS: Master Pitch Video created at: {OUTPUT_PITCH_MP4} (Duration: {pitch_video.duration:.1f}s)")

if __name__ == "__main__":
    build_pitch()
