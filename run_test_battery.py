"""
AutoMentor AI: Comprehensive Test Battery Runner
Executes all 6 test suites and displays a formatted summary report.
"""

import sys
import subprocess

def run_battery():
    print("=" * 70)
    print("  🧪 AutoMentor AI — Executando Bateria Completa de Testes")
    print("  Gemini 3.5 Flash • Google ADK • Socratic Dialog • Tools & Memory")
    print("=" * 70 + "\n")

    cmd = [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"]
    result = subprocess.run(cmd)

    print("\n" + "=" * 70)
    if result.returncode == 0:
        print("  ✓ SUCESSO: Todos os cenários e testes da bateria passaram 100%!")
    else:
        print("  ❌ FALHA: Verifique os logs acima para detalhes dos erros.")
    print("=" * 70)
    sys.exit(result.returncode)

if __name__ == "__main__":
    run_battery()
