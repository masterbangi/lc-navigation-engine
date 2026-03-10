"""
comsect1 Architecture - poi_ layer
ChromaDB Gateway

Role (comsect1 Section 4 -- Poiesis):
- Mechanical connection to ChromaDB / lc_list.json
- No domain judgment -- bridging only
- Executes queries requested by prx_ and structures raw results

Author: Hyunmyung (Hyunmyung), Bang-i AGI
"""

from __future__ import annotations
import json
import os
import math


_LC_LIST_PATH = os.path.join(os.path.dirname(__file__), "lc_list.json")


class PoiChromadbGateway:
    """
    Connects to ChromaDB (AWS environment)
    or falls back to lc_list.json (local / test environment).

    Only method exposed to prx_: query_resonance()
    """

    def __init__(self):
        self._lc_data = self._load_lc_data()
        self._chroma_client = self._try_connect_chroma()

    def _try_connect_chroma(self):
        try:
            import chromadb
            from sentence_transformers import SentenceTransformer
            client = chromadb.HttpClient(host="3.39.180.4", port=8000)
            self._encoder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
            self._collection = client.get_collection("bangi_core_multilingual")
            return client
        except Exception:
            self._encoder = None
            self._collection = None
            return None

    def _load_lc_data(self) -> list[dict]:
        if os.path.exists(_LC_LIST_PATH):
            with open(_LC_LIST_PATH, encoding="utf-8") as f:
                return json.load(f).get("lcs", [])
        return []

    def query_resonance(self, query_text: str, n_results: int = 5) -> list[dict]:
        if self._chroma_client and self._collection and self._encoder:
            return self._query_via_chromadb(query_text, n_results)
        return self._query_via_keyword_fallback(query_text, n_results)

    def _query_via_chromadb(self, query_text: str, n_results: int) -> list[dict]:
        vec = self._encoder.encode([query_text]).tolist()
        results = self._collection.query(
            query_embeddings=vec,
            n_results=n_results,
            include=["metadatas", "documents", "distances"]
        )
        out = []
        for i, meta in enumerate(results["metadatas"][0]):
            dist = results["distances"][0][i]
            score = max(0.0, 1.0 - dist / 2.0)
            title = (meta.get("title_en") or meta.get("title_ko") or
                     results["documents"][0][i][:60])
            out.append({
                "title": title,
                "score": round(score, 4),
                "preview": results["documents"][0][i][:120],
                "category": meta.get("category", "LC"),
                "meta_id": meta.get("meta_id", "")
            })
        return out

    def _query_via_keyword_fallback(self, query_text: str, n_results: int) -> list[dict]:
        """Keyword-based fallback (offline). TF similarity against LC documents."""
        query_words = set(query_text.lower().split())
        scored = []
        for lc in self._lc_data:
            doc = lc.get("doc_preview", "").lower()
            title = lc.get("title_en") or lc.get("title_ko") or doc[:60]
            doc_words = set(doc.split())
            if not doc_words:
                continue
            overlap = len(query_words & doc_words)
            score = overlap / (math.sqrt(len(query_words)) * math.sqrt(len(doc_words)) + 1e-9)
            score = min(0.85, score * 8)
            scored.append({
                "title": title,
                "score": round(score, 4),
                "preview": lc.get("doc_preview", "")[:120],
                "category": lc.get("category", "LC"),
                "meta_id": lc.get("meta_id", "")
            })
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:n_results]
