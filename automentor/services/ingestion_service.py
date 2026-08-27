"""
Ingestion Service: Parses lecture slides, syllabi, and PDFs to extract structured knowledge graph nodes.
"""

import io
import re
from typing import List, Dict, Any, Optional
from automentor.config import GEMINI_API_KEY
from automentor.tools import update_knowledge_node

class IngestionService:
    def __init__(self):
        self.api_key = GEMINI_API_KEY

    def extract_text_from_pdf(self, file_bytes: bytes) -> str:
        """Extracts text content from uploaded PDF bytes."""
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            if text.strip():
                return text.strip()
            return file_bytes.decode("utf-8", errors="ignore")
        except Exception as e:
            print(f"[IngestionService] PDF parsing notice: {e}. Falling back to raw text decode.")
            return file_bytes.decode("utf-8", errors="ignore")

    def parse_syllabus(self, raw_text: str, source_title: str = "Material de Aula") -> List[Dict[str, Any]]:
        """
        Extracts key topics and learning objectives from text using Gemini 3.5 Flash or deterministic parsing.
        Populates the Knowledge Graph with the discovered concepts.
        """
        extracted_topics = []

        if self.api_key:
            try:
                from google import genai
                client = genai.Client(api_key=self.api_key)
                prompt = (
                    f"Analise o seguinte material de aula/ementa de faculdade ('{source_title}') e extraia "
                    f"os 3 a 7 principais conceitos técnicos que o aluno precisa dominar.\n\n"
                    f"Material:\n{raw_text[:4000]}\n\n"
                    f"Retorne apenas uma lista no formato:\n"
                    f"- Nome do Conceito: Breve descrição da habilidade prática"
                )
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=prompt
                )
                if response.text:
                    for line in response.text.splitlines():
                        if ":" in line:
                            parts = line.split(":", 1)
                            name = parts[0].strip("- *#123456789. ")
                            desc = parts[1].strip()
                            if len(name) > 2:
                                tid = name.lower().replace(" ", "_")[:30]
                                update_knowledge_node(tid, name, "in_progress", 0.2, desc)
                                extracted_topics.append({"topic_id": tid, "topic_name": name, "notes": desc})
                    if extracted_topics:
                        return extracted_topics
            except Exception as e:
                print(f"[IngestionService] Notice: {e}. Using deterministic extraction.")

        # Fallback Deterministic Extraction
        lines = [l.strip() for l in raw_text.splitlines() if len(l.strip()) > 5]
        for line in lines[:5]:
            clean_name = re.sub(r'^[•\-\*\d\.\#\s]+', '', line)[:40].strip()
            if len(clean_name) > 3:
                tid = clean_name.lower().replace(" ", "_")
                update_knowledge_node(tid, clean_name, "in_progress", 0.2, f"Extraído de: {source_title}")
                extracted_topics.append({"topic_id": tid, "topic_name": clean_name, "notes": f"Fonte: {source_title}"})

        return extracted_topics

ingestion_service = IngestionService()
