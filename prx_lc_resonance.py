"""
comsect1 Architecture - prx_ layer
LC Resonance Analyzer

Role (comsect1 Section 4 -- Praxis):
- Only layer coupled to external types (ChromaDB, embedding model)
- ida_ has no knowledge of this layer's internals
- Returns only ResonanceResult type to ida_

Author: Hyunmyung (Hyunmyung), Bang-i AGI
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

from poi_chromadb_gateway import PoiChromadbGateway


@dataclass
class ResonanceResult:
    """
    LC resonance analysis result.
    The only contract type exposed to ida_.
    ChromaDB internal structure is fully abstracted here.
    """
    intent_text: str
    top_resonance_score: float
    top_lc_title: str
    matched_lcs: list[dict] = field(default_factory=list)
    option_scores: list[dict] = field(default_factory=list)
    query_used: str = ""


class PrxLcResonance:
    """
    Measures resonance between the 76 LC vectors in ChromaDB
    and the incoming intent.

    Falls back to local lc_list.json when AWS ChromaDB
    is unavailable (offline / test environment).
    """

    def __init__(self, top_k: int = 5, threshold: float = 0.55):
        self._top_k = top_k
        self._threshold = threshold
        self._gateway = PoiChromadbGateway()

    def analyze(self, intent_text: str, options: list[str] = None) -> ResonanceResult:
        """
        Projects intent text into LC vector space and returns resonance values.
        If options are provided, also compares LC alignment for each option.
        """
        matches = self._gateway.query_resonance(
            query_text=intent_text,
            n_results=self._top_k
        )

        option_scores = []
        if options:
            for opt in options:
                opt_matches = self._gateway.query_resonance(query_text=opt, n_results=3)
                top_score = opt_matches[0]["score"] if opt_matches else 0.0
                top_lc = opt_matches[0]["title"] if opt_matches else "N/A"
                option_scores.append({
                    "option": opt,
                    "resonance": top_score,
                    "aligned_lc": top_lc,
                    "is_aligned": top_score >= self._threshold
                })

        top_score = matches[0]["score"] if matches else 0.0
        top_title = matches[0]["title"] if matches else "No match"

        return ResonanceResult(
            intent_text=intent_text,
            top_resonance_score=top_score,
            top_lc_title=top_title,
            matched_lcs=matches,
            option_scores=option_scores,
            query_used=intent_text
        )
