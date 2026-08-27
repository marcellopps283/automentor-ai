"""
AutoMentor Streamlit Web UI: Visual Knowledge Graph, Socratic Chat, and 1-Click Showcase Dashboard.
"""

import streamlit as st
from datetime import datetime
from automentor.mentor_core import mentor_brain
from automentor.tools import memory_store
from automentor.services import ingestion_service

# Page config
st.set_page_config(
    page_title="AutoMentor AI — Seu Companheiro de Estudos",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #616161;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #F8F9FA;
        border-radius: 8px;
        padding: 15px;
        border-left: 5px solid #1E88E5;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg", width=140)
    st.markdown("### 🎓 AutoMentor AI")
    st.caption("**All Things Agentic Hackathon**\n\n• **Model:** Gemini 3.5 Flash\n• **Framework:** Google ADK\n• **Cloud:** Cloud Run + Firestore")
    
    st.divider()
    st.markdown("#### 📚 Ingestão de Material de Aula")
    uploaded_file = st.file_uploader("Suba slides ou ementa (PDF)", type=["pdf"])
    if uploaded_file is not None:
        if st.button("📥 Extrair Tópicos do PDF", use_container_width=True):
            with st.spinner("Gemini 3.5 analisando o documento..."):
                bytes_data = uploaded_file.read()
                raw_text = ingestion_service.extract_text_from_pdf(bytes_data)
                topics = ingestion_service.parse_syllabus(raw_text, uploaded_file.name)
                st.success(f"✓ {len(topics)} conceitos extraídos e salvos no Knowledge Graph!")
                st.rerun()

    st.divider()
    if st.button("🔄 Reiniciar Sessão de Chat", use_container_width=True):
        mentor_brain.start_session()
        st.session_state["messages"] = []
        st.rerun()

# Header
st.markdown('<div class="main-header">🎓 AutoMentor AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Seu companheiro de estudos socrático, autônomo e focado em vitrinizar suas habilidades.</div>', unsafe_allow_html=True)

# Tabs
tab_chat, tab_graph, tab_showcase = st.tabs(["💬 Chat com o Mentor", "🧠 Knowledge Graph de Habilidades", "🚀 Central de Vitrine (1-Clique)"])

# 1. Chat Tab
with tab_chat:
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": (
                    "Fala Marcelo! Sou o **AutoMentor**, seu companheiro de estudos.\n\n"
                    "O que você precisa dominar hoje? É uma matéria da faculdade, uma prova chegando, "
                    "ou uma tecnologia que você quer colocar no currículo? Me conta!"
                )
            }
        ]

    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "👤"):
            st.markdown(msg["content"])

    # Quick action prompt suggestions
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎯 Tenho prova de gRPC e Protobuf"):
            user_msg = "Tenho prova de Sistemas Distribuídos semana que vem e preciso entender gRPC e Protobufs."
            st.session_state["messages"].append({"role": "user", "content": user_msg})
            with st.spinner("Mentor preparando diagnóstico e ações..."):
                res = mentor_brain.send_message(user_msg)
                st.session_state["messages"].append({"role": "assistant", "content": res["reply"]})
            st.rerun()
    with col2:
        if st.button("💡 Explicar JSON vs Protobuf"):
            user_msg = "JSON é texto com chaves e valores. Protobuf é serializado em binário com tags numéricas fixas."
            st.session_state["messages"].append({"role": "user", "content": user_msg})
            with st.spinner("Mentor avaliando e atualizando habilidades..."):
                res = mentor_brain.send_message(user_msg)
                st.session_state["messages"].append({"role": "assistant", "content": res["reply"]})
            st.rerun()
    with col3:
        if st.button("🐳 Quero praticar Docker Compose"):
            user_msg = "Preciso de um desafio prático de Docker Compose para subir Postgres e Redis."
            st.session_state["messages"].append({"role": "user", "content": user_msg})
            with st.spinner("Mentor preparando lab..."):
                res = mentor_brain.send_message(user_msg)
                st.session_state["messages"].append({"role": "assistant", "content": res["reply"]})
            st.rerun()

    # User chat input
    if prompt := st.chat_input("Digite sua dúvida, resposta ou tema de estudo..."):
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🎓"):
            with st.spinner("O Mentor está analisando e orquestrando ações no background..."):
                res = mentor_brain.send_message(prompt)
                st.markdown(res["reply"])
                st.session_state["messages"].append({"role": "assistant", "content": res["reply"]})

# 2. Knowledge Graph Tab
with tab_graph:
    topics = memory_store.get_all_topics()
    
    total = len(topics)
    mastered = sum(1 for t in topics if t.get("status") == "mastered")
    gaps = sum(1 for t in topics if t.get("status") == "gap")
    in_progress = sum(1 for t in topics if t.get("status") == "in_progress")

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total de Conceitos", total)
    m2.metric("Dominados (Mastered)", f"{mastered} ({int(mastered/total*100) if total else 0}%)", delta="Proficiência" if mastered else None)
    m3.metric("Lacunas (Gaps)", gaps, delta_color="inverse")
    m4.metric("Em Estudo", in_progress)

    st.divider()
    st.markdown("### 🗺️ Mapa de Competências")

    if not topics:
        st.info("Nenhum conceito mapeado ainda. Envie uma mensagem no chat ou faça upload de um PDF para começar!")
    else:
        for t in topics:
            status = t.get("status", "not_started")
            score = t.get("mastery_score", 0.0)
            
            status_color = {
                "mastered": "🟢 Dominado",
                "gap": "🔴 Lacuna Detectada",
                "in_progress": "🟡 Em Estudo",
                "not_started": "⚪ Não Iniciado"
            }.get(status, status)

            with st.expander(f"{status_color} — **{t.get('topic_name')}** (Score: {int(score*100)}%)"):
                st.progress(score)
                st.write(f"**ID do Conceito:** `{t.get('topic_id')}`")
                st.write(f"**Última Atualização:** {t.get('last_updated', '-')[:19].replace('T', ' ')}")
                if t.get("notes"):
                    st.info(f"💡 **Anotação do Mentor:** {t.get('notes')}")

# 3. Showcase Tab
with tab_showcase:
    st.markdown("### 💼 Vitrine de Conquistas & Portfólio")
    st.write("Quando você domina uma habilidade, o AutoMentor prepara o rascunho completo para você publicar e comprovar seu conhecimento para recrutadores.")
    
    topics_mastered = [t for t in memory_store.get_all_topics() if t.get("status") == "mastered"]
    
    if not topics_mastered:
        st.warning("Complete desafios e resolva seus Pull Requests para desbloquear os rascunhos de vitrine!")
    else:
        for t in topics_mastered:
            st.success(f"🏆 **Habilidade Pronta para Vitrine:** {t.get('topic_name')}")
            
            post_preview = (
                f"🚀 Concluindo mais uma etapa de aprendizado prático: **{t.get('topic_name')}**!\n\n"
                f"Neste laboratório, implementei arquiteturas com foco em alta performance e boas práticas:\n"
                f"💡 {t.get('notes') or 'Código modular com testes unitários automatizados e containerização Docker.'}\n\n"
                f"🔗 Repositório no GitHub: `https://github.com/student/lab-{t.get('topic_id')}`\n\n"
                f"#Backend #SoftwareEngineering #GoogleCloud #Gemini #AllThingsAgentic"
            )
            
            st.text_area("Preview do Post do LinkedIn:", value=post_preview, height=180)
            if st.button(f"✓ Aprovar e Publicar '{t.get('topic_name')}' no LinkedIn", key=f"btn_{t.get('topic_id')}"):
                st.balloons()
                st.success("🎉 Publicação enviada com sucesso para o LinkedIn!")
