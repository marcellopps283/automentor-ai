"""
Full Automated Live Application Video Recorder & Audio Composer
1. Launches FastAPI and Next.js production servers
2. Executes full browser interactions with Playwright in 1080p
3. Converts and outputs the final video: automentor_live_demo.mp4
"""

import os
import sys
import time
import glob
import urllib.request
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from playwright.sync_api import sync_playwright

RECORDING_DIR = os.path.abspath("recordings")
os.makedirs(RECORDING_DIR, exist_ok=True)
FINAL_LIVE_MP4 = os.path.abspath("automentor_live_demo.mp4")

def wait_for_service(url, timeout_secs=30):
    print(f"[Pipeline] Waiting for {url} to be online...")
    start_time = time.time()
    while time.time() - start_time < timeout_secs:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=2) as resp:
                if resp.status == 200:
                    print(f"[Pipeline] ✓ {url} is online and ready!")
                    return True
        except Exception:
            time.sleep(1)
    return False

def run():
    print("[Pipeline] 1. Starting Backend & Frontend Servers...")
    backend_proc = subprocess.Popen(
        f'"{sys.executable}" -m uvicorn automentor.api.server:app --host 127.0.0.1 --port 8000',
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    frontend_dir = os.path.abspath("frontend")
    frontend_proc = subprocess.Popen(
        "npm.cmd run dev",
        cwd=frontend_dir,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    wait_for_service("http://127.0.0.1:8000/health", timeout_secs=15)
    wait_for_service("http://127.0.0.1:3000", timeout_secs=30)

    recorded_video_path = None

    try:
        print("[Pipeline] 3. Launching Playwright to record live UI interactions in 1080p...")
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox"]
            )
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                record_video_dir=RECORDING_DIR,
                record_video_size={"width": 1920, "height": 1080}
            )
            page = context.new_page()

            # Navigate to Cockpit
            print("[Pipeline] Navigating to http://127.0.0.1:3000...")
            page.goto("http://127.0.0.1:3000", wait_until="networkidle", timeout=20000)
            page.wait_for_timeout(3000)

            # 1. Retention Widget
            print("[Pipeline] Interacting with Retention & Streak Widget...")
            try:
                page.locator("button:has-text('Retenção')").click(timeout=3000)
                page.wait_for_timeout(2500)
                page.locator("button:has-text('Retenção')").click(timeout=3000)
            except Exception:
                pass
            page.wait_for_timeout(1000)

            # 2. Chat with Socratic Mentor
            print("[Pipeline] Typing in Socratic Chat...")
            try:
                chat_input = page.locator("input[placeholder*='dúvidas']")
                chat_input.fill("Tenho prova de Sistemas Distribuídos e preciso entender gRPC e Protobufs.")
                page.wait_for_timeout(800)
                page.keyboard.press("Enter")
                page.wait_for_timeout(4000)
            except Exception:
                pass

            # 3. Interactive Notebook - Run tests
            print("[Pipeline] Executing tests in Interactive Notebook...")
            try:
                page.locator("button:has-text('Executar Testes')").click(timeout=3000)
                page.wait_for_timeout(3000)
            except Exception:
                pass

            # 4. Adaptive Bug Injection
            print("[Pipeline] Injecting Adaptive Bug...")
            try:
                page.locator("button:has-text('Injetar Bug')").click(timeout=3000)
                page.wait_for_timeout(2000)
                page.locator("button:has-text('Executar Testes')").click(timeout=3000)
                page.wait_for_timeout(3000)
            except Exception:
                pass

            # 5. Progressive Hint Ladder
            print("[Pipeline] Expanding 3-Tier Hint Ladder...")
            try:
                hints = page.locator("button:has-text('Nível')")
                for i in range(min(3, hints.count())):
                    hints.nth(i).click(timeout=2000)
                    page.wait_for_timeout(1200)
            except Exception:
                pass

            # 6. Cheat Sheet Modal
            print("[Pipeline] Opening Cheat Sheet Study Guide...")
            try:
                page.locator("button:has-text('Guia de Bolso')").click(timeout=3000)
                page.wait_for_timeout(3000)
                page.locator(".fixed button").first.click(timeout=3000)
                page.wait_for_timeout(1000)
            except Exception:
                pass

            # 7. 2D Knowledge Graph Modal
            print("[Pipeline] Opening 2D Knowledge Graph...")
            try:
                page.locator("button:has-text('Grafo 2D')").click(timeout=3000)
                page.wait_for_timeout(3500)
                page.locator(".fixed button").first.click(timeout=3000)
                page.wait_for_timeout(1000)
            except Exception:
                pass

            # 8. Mock Tech Interview
            print("[Pipeline] Starting Mock Tech Interview Call...")
            try:
                page.locator("button:has-text('Simular Entrevista')").click(timeout=3000)
                page.wait_for_timeout(3000)
                
                # Advance through interview
                for _ in range(3):
                    next_btn = page.locator(".fixed button.bg-blue-600, .fixed button.bg-green-600").last
                    if next_btn.is_visible():
                        next_btn.click(timeout=2000)
                        page.wait_for_timeout(2000)
                
                page.wait_for_timeout(3000)
                close_call = page.locator("button:has-text('Salvar'), button:has-text('Encerrar')").last
                if close_call.is_visible():
                    close_call.click(timeout=2000)
                page.wait_for_timeout(1500)
            except Exception as e:
                print(f"[Pipeline] Interview step note: {e}")

            # 9. 100% Mastery Trigger & Confetti Showcase
            print("[Pipeline] Triggering 100% Mastery & LinkedIn Showcase...")
            try:
                chat_input = page.locator("input[placeholder*='dúvidas']")
                chat_input.fill("Protobuf usa tags numéricas fixas e serialização binária com varints, evitando o parsing de texto do JSON.")
                page.wait_for_timeout(800)
                page.keyboard.press("Enter")
                page.wait_for_timeout(4000)

                showcase_btn = page.locator("button:has-text('Revisar & Publicar')")
                if showcase_btn.is_visible():
                    showcase_btn.click(timeout=3000)
                    page.wait_for_timeout(4000)
                    publish_btn = page.locator("button:has-text('Publicar no LinkedIn')")
                    if publish_btn.is_visible():
                        publish_btn.click(timeout=3000)
                        page.wait_for_timeout(2500)
            except Exception:
                pass

            page.wait_for_timeout(2000)
            recorded_video_path = page.video.path()
            context.close()
            browser.close()

    finally:
        print("[Pipeline] 4. Terminating server processes...")
        try:
            subprocess.run("taskkill /F /IM node.exe /T", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run("taskkill /F /IM uvicorn.exe /T", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

    if recorded_video_path and os.path.exists(recorded_video_path):
        print(f"[Pipeline] 5. Converting {recorded_video_path} to {FINAL_LIVE_MP4} via FFmpeg...")
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-i", recorded_video_path,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            FINAL_LIVE_MP4
        ]
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"[Pipeline] ✓ SUCCESS: Live Demo Video recorded and rendered at: {FINAL_LIVE_MP4}")
    else:
        print("[Pipeline] Video capture path not found.")

if __name__ == "__main__":
    run()
