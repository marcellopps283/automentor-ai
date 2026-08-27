"""
Memory Tool: Manages the student's Knowledge Graph, scores, prerequisites, and Ebbinghaus decay.
Supports Google Cloud Firestore with a local JSON fallback.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from automentor.config import LOCAL_MEMORY_PATH, GOOGLE_CLOUD_PROJECT

class MemoryStore:
    def __init__(self):
        self.use_firestore = bool(GOOGLE_CLOUD_PROJECT)
        self.db = None
        if self.use_firestore:
            try:
                from google.cloud import firestore
                self.db = firestore.Client(project=GOOGLE_CLOUD_PROJECT)
            except Exception as e:
                print(f"[MemoryStore] Could not initialize Firestore: {e}. Falling back to local JSON.")
                self.use_firestore = False

    def _read_local(self) -> Dict[str, Any]:
        if not LOCAL_MEMORY_PATH.exists():
            default_data = {
                "student_id": "student_001",
                "topics": {},
                "action_history": []
            }
            LOCAL_MEMORY_PATH.write_text(json.dumps(default_data, indent=2, ensure_ascii=False), encoding="utf-8")
            return default_data
        try:
            return json.loads(LOCAL_MEMORY_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {"student_id": "student_001", "topics": {}, "action_history": []}

    def _write_local(self, data: Dict[str, Any]):
        LOCAL_MEMORY_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def update_node(
        self,
        topic_id: str,
        topic_name: str,
        status: str,
        score: float,
        notes: Optional[str] = None,
        prerequisites: Optional[List[str]] = None,
        bloom_level: str = "apply"
    ) -> Dict[str, Any]:
        """
        Updates or creates a knowledge node in the student's graph.
        status: 'mastered' | 'in_progress' | 'gap' | 'not_started'
        """
        now = datetime.now()
        # Calculate next review due date based on spaced repetition
        review_days = 1 if score < 0.5 else (3 if score < 0.8 else 7)
        next_review = (now + timedelta(days=review_days)).isoformat()

        node_data = {
            "topic_id": topic_id,
            "topic_name": topic_name,
            "status": status,
            "mastery_score": round(score, 2),
            "last_updated": now.isoformat(),
            "next_review_due": next_review,
            "prerequisites": prerequisites or [],
            "bloom_level": bloom_level,
            "notes": notes or ""
        }

        if self.use_firestore and self.db:
            try:
                self.db.collection("students").document("default_student").collection("knowledge_graph").document(topic_id).set(node_data)
                return node_data
            except Exception as e:
                print(f"[MemoryStore] Firestore write error: {e}")

        # Local JSON fallback
        local_data = self._read_local()
        local_data["topics"][topic_id] = node_data
        local_data["action_history"].append({
            "action": "update_knowledge_node",
            "topic_id": topic_id,
            "timestamp": now.isoformat(),
            "status": status,
            "score": score
        })
        self._write_local(local_data)
        return node_data

    def get_all_topics(self) -> List[Dict[str, Any]]:
        if self.use_firestore and self.db:
            try:
                docs = self.db.collection("students").document("default_student").collection("knowledge_graph").stream()
                return [doc.to_dict() for doc in docs]
            except Exception as e:
                print(f"[MemoryStore] Firestore read error: {e}")

        local_data = self._read_local()
        return list(local_data.get("topics", {}).values())

    def get_decaying_topics(self) -> List[Dict[str, Any]]:
        """Returns topics that have passed their recommended review window."""
        topics = self.get_all_topics()
        now = datetime.now()
        decaying = []
        for t in topics:
            due_str = t.get("next_review_due")
            if due_str:
                try:
                    due_date = datetime.fromisoformat(due_str)
                    if now >= due_date:
                        decaying.append(t)
                except Exception:
                    pass
        return decaying

memory_store = MemoryStore()

def update_knowledge_node(
    topic_id: str,
    topic_name: str,
    status: str,
    score: float,
    notes: str = "",
    prerequisites: Optional[List[str]] = None,
    bloom_level: str = "apply"
) -> str:
    """
    Atualiza o Knowledge Graph do aluno com um conceito, nota de proficiência, pré-requisitos e taxonomia de Bloom.

    Args:
        topic_id: Identificador único em snake_case (ex: 'grpc_contracts', 'jwt_auth', 'raft_consensus').
        topic_name: Nome legível do conceito (ex: 'Contratos e Tipagem com Protobuf').
        status: Estado de domínio ('mastered', 'in_progress', 'gap', 'not_started').
        score: Nota de proficiência de 0.0 (nenhum domínio) a 1.0 (domínio total).
        notes: Observações pedagógicas ou o erro específico do aluno.
        prerequisites: Lista de IDs de conceitos pré-requisitos necessários.
        bloom_level: Nível de cognição ('remember', 'understand', 'apply', 'analyze', 'evaluate', 'create').

    Returns:
        Uma mensagem confirmando o registro no Knowledge Graph com a data da próxima revisão espaçada.
    """
    node = memory_store.update_node(topic_id, topic_name, status, score, notes, prerequisites, bloom_level)
    return f"Knowledge Graph atualizado: '{topic_name}' marcado como [{status.upper()}] com score {score:.2f} (Taxonomia: {bloom_level.upper()})."
