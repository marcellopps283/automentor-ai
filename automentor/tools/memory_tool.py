"""
Memory Tool: Manages the student's Knowledge Graph, scores, and gaps.
Supports Google Cloud Firestore with a local JSON fallback.
"""

import json
from datetime import datetime
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

    def update_node(self, topic_id: str, topic_name: str, status: str, score: float, notes: Optional[str] = None) -> Dict[str, Any]:
        """
        Updates or creates a knowledge node in the student's graph.
        status: 'mastered' | 'in_progress' | 'gap' | 'not_started'
        """
        node_data = {
            "topic_id": topic_id,
            "topic_name": topic_name,
            "status": status,
            "mastery_score": round(score, 2),
            "last_updated": datetime.now().isoformat(),
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
            "timestamp": datetime.now().isoformat(),
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

memory_store = MemoryStore()

def update_knowledge_node(topic_id: str, topic_name: str, status: str, score: float, notes: str = "") -> str:
    """
    Atualiza o Knowledge Graph do aluno com um tópico e seu status de proficiência.

    Args:
        topic_id: Identificador único em minúsculas (ex: 'grpc_contracts', 'jwt_auth', 'docker_compose').
        topic_name: Nome legível do conceito (ex: 'Contratos e Tipagem com Protobuf').
        status: Estado de domínio ('mastered', 'in_progress', 'gap', 'not_started').
        score: Nota de proficiência de 0.0 (nenhum domínio) a 1.0 (domínio total).
        notes: Observações pedagógicas ou o erro específico do aluno.

    Returns:
        Uma mensagem confirmando o registro no Knowledge Graph.
    """
    node = memory_store.update_node(topic_id, topic_name, status, score, notes)
    return f"Knowledge Graph atualizado: '{topic_name}' marcado como [{status.upper()}] com score {score:.2f}."
