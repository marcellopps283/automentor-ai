"""
Playwright Automated Screen Recording for AutoMentor AI Live Demo
Records actual high-fidelity browser interactions on http://localhost:3000.
"""

import time
import os
import glob
import subprocess
from playwright.sync_api import sync_playwright

RECORDING_DIR = "recordings"
os.makedirs(RECORDING_DIR, exist_ok=True)

def record_demo():
    print("[Playwright] Starting live browser session recording on http://localhost:3000...")
    
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

        # 1. Navigate to Cockpit
        print("[Playwright] Navigating to http://localhost:3000...")
        for _ in range(15):
            try:
                page.goto("http://localhost:3000", wait_until="networkidle", timeout=5000)
                break
            except Exception:
                time.sleep(1)

        page.wait_for_timeout(3000)

        # 2. Inspect Ebbinghaus Retention Widget
        print("[Playwright] Interacting with Ebbinghaus Retention Widget...")
        try:
            page.locator("button:has-text('Retenção')").click()
            page.wait_for_timeout(2500)
            # Close popover by clicking outside or on retention button
            page.locator("button:has-text('Retenção')").click()
        except Exception as e:
            print(f"[Playwright] Retention notice: {e}")

        page.wait_for_timeout(1500)

        # 3. Type message in Socratic Chat
        print("[Playwright] Sending message in Socratic Chat...")
        try:
            chat_input = page.locator("input[placeholder*='dúvidas']")
            chat_input.fill("Tenho prova de Sistemas Distribuídos semana que vem e preciso entender gRPC e Protobufs.")
            page.wait_for_timeout(800)
            page.keyboard.press("Enter")
            page.wait_for_timeout(3500)
        except Exception as e:
            print(f"[Playwright] Chat notice: {e}")

        # 4. Interactive Notebook: Run tests
        print("[Playwright] Running tests in Interactive Notebook...")
        try:
            page.locator("button:has-text('Executar Testes')").click()
            page.wait_for_timeout(2500)
        except Exception as e:
            print(f"[Playwright] Run tests notice: {e}")

        # 5. Inject Adaptive Bug
        print("[Playwright] Injecting Adaptive Bug...")
        try:
            page.locator("button:has-text('Injetar Bug')").click()
            page.wait_for_timeout(1500)
            page.locator("button:has-text('Executar Testes')").click()
            page.wait_for_timeout(2500)
        except Exception as e:
            print(f"[Playwright] Bug injection notice: {e}")

        # 6. Unlock Progressive Hint Ladder
        print("[Playwright] Unlocking Hint Ladder tiers...")
        try:
            hints = page.locator("button:has-text('Nível')")
            for i in range(min(3, hints.count())):
                hints.nth(i).click()
                page.wait_for_timeout(1000)
        except Exception as e:
            print(f"[Playwright] Hint ladder notice: {e}")

        page.wait_for_timeout(1500)

        # 7. Open Cheat Sheet Modal
        print("[Playwright] Opening Cheat Sheet Modal...")
        try:
            page.locator("button:has-text('Guia de Bolso')").click()
            page.wait_for_timeout(2500)
            # Click close button on modal
            page.locator(".fixed button").first.click()
            page.wait_for_timeout(1000)
        except Exception as e:
            print(f"[Playwright] Cheat sheet notice: {e}")

        # 8. Open 2D Knowledge Graph Modal
        print("[Playwright] Opening 2D Knowledge Graph...")
        try:
            page.locator("button:has-text('Grafo 2D')").click()
            page.wait_for_timeout(3000)
            page.locator(".fixed button").first.click()
            page.wait_for_timeout(1000)
        except Exception as e:
            print(f"[Playwright] Graph notice: {e}")

        # 9. Open Mock Tech Interview
        print("[Playwright] Launching Mock Tech Interview...")
        try:
            page.locator("button:has-text('Simular Entrevista')").click()
            page.wait_for_timeout(3000)
            page.locator("button:has-text('Próxima Pergunta')").click()
            page.wait_for_timeout(2000)
            page.locator("button:has-text('Finalizar & Gerar Scorecard')").click()
            page.wait_for_timeout(3500)
            page.locator("button:has-text('Salvar no Histórico & Fechar')").click()
            page.wait_for_timeout(1500)
        except Exception as e:
            print(f"[Playwright] Interview notice: {e}")

        # 10. Send mastery explanation to trigger 100% celebration
        print("[Playwright] Triggering 100% Mastery & LinkedIn Showcase...")
        try:
            chat_input = page.locator("input[placeholder*='dúvidas']")
            chat_input.fill("Protobuf usa tags numéricas fixas e serialização binária com varints, evitando o parsing de texto do JSON.")
            page.wait_for_timeout(600)
            page.keyboard.press("Enter")
            page.wait_for_timeout(3500)

            # Click on Showcase button if card appears
            page.locator("button:has-text('Revisar & Publicar')").click()
            page.wait_for_timeout(4000)
            page.locator("button:has-text('Publicar no LinkedIn')").click()
            page.wait_for_timeout(2000)
        except Exception as e:
            print(f"[Playwright] Showcase notice: {e}")

        print("[Playwright] Finalizing video recording...")
        page.wait_for_timeout(2000)

        video_path = page.video.path()
        context.close()
        browser.close()

        print(f"[Playwright] Video recorded successfully at: {video_path}")
        return video_path

if __name__ == "__main__":
    record_demo()
