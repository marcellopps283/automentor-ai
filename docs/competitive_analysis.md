# 🌐 Pesquisa Competitiva Profunda & Mapeamento Estratégico
## AutoMentor AI vs. O Ecossistema Global de Tutores e Agentes de Código (2025–2026)

---

## 🧭 1. O Cenário Atual: As 4 Grandes Categorias do Mercado

Ao analisar as principais plataformas comerciais, artigos acadêmicos e projetos premiados em hackathons recentes (Devpost, Lablab.ai, HackerEarth), o mercado de IA para programação divide-se em 4 quadrantes:

```
                                  ALTA AUTONOMIA DE CÓDIGO
                                             ▲
                                             │
                       Replit Agent          │      AUTONOMENTOR AI
                       Cursor Composer       │   (Parceiro Colaborativo:
                       Copilot Workspace     │    Pedagógico + Atuador Real)
                                             │
       FOCO EM PRODUTIVIDADE                 │                 FOCO EM APRENDIZADO
       (Faz pelo usuário / Vending Machine)  │                 (Luta Produtiva / Socrático)
      ───────────────────────────────────────┼────────────────────────────────────────►
                                             │
                       Chatbots Genéricos    │      Boot.dev ("Boots")
                       (ChatGPT / Claude)    │      Khanmigo
                                             │      Socratic Tutor (VS Code)
                                             │
                                             ▼
                                   BAIXA AUTONOMIA
```

---

## 🔍 2. Análise Detalhada dos Principais Concorrentes

| Plataforma / Projeto | Proposta Central | Pontos Fortes | Falhas Críticas / Lacunas (Onde o AutoMentor Ganha) |
|---|---|---|---|
| **Boot.dev ("Boots")** | Mentor Socrático para Backend (Go/Python/Docker). | • Recusa dar respostas prontas.<br>• Gamificação com XP.<br>• Foco em engenharia de backend. | ❌ **Currículo Fechado:** Não permite ao aluno subir os slides da faculdade ou um PDF de prova.<br>❌ **Sem Atuadores Reais:** Não agenda no Google Calendar do aluno, não cria repositórios na conta pessoal do GitHub e não gera posts de vitrine no LinkedIn. |
| **Khanmigo (Khan Academy)** | Tutor socrático clássico para escolas/iniciantes. | • Excelente diálogo pedagógico.<br>• Conduz o aluno passo a passo. | ❌ **Infantilizado / Básico:** Não possui ferramentas reais de desenvolvedor (Docker, Git, CI/CD, Wasm, Terminal).<br>❌ Totalmente desconectado do mercado de trabalho e do GitHub. |
| **Replit Agent / Cursor Composer** | Agentes de codificação autônoma e geração. | • Alta autonomia.<br>• Criação de arquivos e testes automáticos. | ❌ **"Vending Machine Syndrome":** Faz o código **pelo** aluno em vez de ensinar. Causa atrofia cognitiva.<br>❌ Não calibra lacunas de conhecimento e não acompanha a curva de retenção do estudante. |
| **SocraticLM / VS Code Socratic Tutor** | Extensões de IDE e wrappers de LLM para estudantes. | • Fica dentro do VS Code.<br>• Bloqueia soluções diretas. | ❌ **Apenas um Wrapper de Chat:** Não tem ecossistema em nuvem, não analisa PDFs, não faz code review assíncrono de Pull Requests via Webhook. |

---

## 🏆 3. O Fosso Estratégico do AutoMentor AI (Por que somos únicos)

O AutoMentor resolve a grande dor que **nenhum concorrente conseguiu unir**:

1. **Ingestão Dinâmica Qualquer-Fonte (Multimodal):** O aluno estuda a matéria da **sua própria faculdade** (subindo o PDF da aula), e não um curso pré-fabricado engessado.
2. **Pedagogia da "Luta Produtiva" (Productive Struggle):** O Mentor conduz com perguntas, insere **bugs didáticos intencionais** para treinar debugging e valida a lógica no navegador com Pyodide.
3. **Braços no Mundo Real (Atuadores Autônomos):**
   * 📅 **Google Calendar:** Agenda blocos de estudo baseados na Curva do Esquecimento de Ebbinghaus (D+1, D+3, D+7).
   * 🐙 **GitHub Real:** Scaffolding de repositórios reais com testes unitários na conta do aluno.
   * 🤖 **Reviewer de PR via Webhooks:** Avaliação socrática automática nos Pull Requests.
   * 💼 **1-Clique Showcase:** Geração de artigos técnicos e posts no LinkedIn para contratação.

---

## 💡 4. Killer Features Identificadas para Destacar no Pitch/Vídeo

Com base no que mais impressiona os jurados de hackathons em 2025/2026:

### A) Sistema de "Dicas em Camadas" (Progressive Scaffolding)
* **Tier 1:** Pergunta Socrática / Analogia de Arquitetura.
* **Tier 2:** Diagrama de Fluxo (Mermaid) ou Pseudocódigo.
* **Tier 3:** Dica de Teste Unitário (aponta a condição de borda sem entregar o código).

### B) Modo "Fault Injection" (Bug Didático Intencional)
* Em vez de apenas pedir código, o Mentor altera uma linha no Notebook injetando um *deadlock*, *race condition* ou *memory leak* para o aluno encontrar e corrigir. (Já implementado no nosso Notebook!).

### C) Métrica de Retenção & Health do Grafo de Conhecimento
* Mostrar visualmente a pontuação do grafo subindo de `20%` para `95%` após o PR ser aprovado.
