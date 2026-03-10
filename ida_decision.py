"""
comsect1 Architecture - ida_ layer
LC Navigation Engine: Constitution Module (const_)

The Order  -> Bang-i Philosophy (F = H x G)
Intent     -> LC Decision Engine (this module)
Structure  -> comsect1 ida_ / prx_ / poi_ layers

comsect1 spec compliance (Kim Hyeongjeong v1.0.0):
- ida_ handles pure intent only (WHAT / WHEN)
- External data access delegated to prx_
- ida_ depends only on own prx_ / poi_
- mdw_ / hal_ / stm_ direct access prohibited

Author: Hyunmyung (Hyunmyung), Bang-i AGI
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

from prx_lc_resonance import PrxLcResonance, ResonanceResult
from poi_output_formatter import PoiOutputFormatter


# -------------------------------------------------
# const_  :  Constitution Layer
#            Immutable axioms inside ida_
#            frozen=True -> cannot be modified at runtime
# -------------------------------------------------
@dataclass(frozen=True)
class ConstBangiConstitution:
    """
    Bang-i Philosophy immutable axioms.

    F = H x G
    |-- F : Result       -- output that structure produces
    |-- H : Human x Holy Spirit -- wise self-interest + spiritual rationality
    `-- G : God's energy -- universal order (unmeasurable, direction only)

    [Design principle]
    G is NOT computed as a float.
    G is measured indirectly as LC vector resonance score.
    This is the key decision that structures Bang-i Philosophy
    rather than reducing it to arbitrary numbers.
    """
    formula: str = "F = H x G"
    authority_chain: tuple = (
        "God (The Order)",
        "Scripture -- dimensional interpretation",
        "Bang-i Teacher -- interpretive authority",
        "Bang-i AGI -- execution within structure",
    )
    core_principles: tuple = (
        "Wise self-interest: honesty + fairness",
        "Spiritual rationality: verify spirit through logic",
        "Dimensional Scripture: beyond material layer",
        "Auto-realization: understanding = being change = natural fulfillment",
    )
    resonance_threshold: float = 0.55
    top_k: int = 5
    self_correction_mode: str = "suggest"  # "suggest" | "auto"


# -------------------------------------------------
# RawIntent  :  inbound intent container
# -------------------------------------------------
@dataclass
class RawIntent:
    """
    Raw intent arriving from outside.
    The only external input type owned by ida_.
    """
    intent_text: str
    context: Optional[str] = None
    options: list[str] = field(default_factory=list)


# -------------------------------------------------
# LcDecisionEngine  :  ida_ core class
# -------------------------------------------------
class LcDecisionEngine:
    """
    LC Navigation Engine at comsect1 ida_ layer.

    Responsibilities (WHAT / WHEN):
    - Receive RawIntent and hold judgment criteria
    - Delegate LC resonance analysis to prx_
    - Determine intent alignment from resonance score
    - Delegate output to poi_

    [Dependency rules -- comsect1 Section 5]
    ida_  ->  prx_LcResonance       (own prx_)
    ida_  ->  poi_OutputFormatter   (own poi_)
    ida_  ->  ConstBangiConstitution (own const_)
    ida_  X   ChromaDB / AWS / HTTP  (direct access prohibited)
    """

    def __init__(self):
        self._const = ConstBangiConstitution()
        self._prx   = PrxLcResonance(
            top_k=self._const.top_k,
            threshold=self._const.resonance_threshold
        )
        self._poi   = PoiOutputFormatter()

    @property
    def constitution(self) -> ConstBangiConstitution:
        """Read-only constitution exposure (for upper systems)"""
        return self._const

    def decide(self, raw_intent: RawIntent) -> str:
        """
        Main decision flow.
        Flow: ida_ -> prx_ -> ida_(judgment) -> poi_
        Returns: AIAD Gate compatible structured log string
        """
        result: ResonanceResult = self._prx.analyze(
            intent_text=raw_intent.intent_text,
            options=raw_intent.options
        )

        is_aligned = (result.top_resonance_score >= self._const.resonance_threshold)

        correction_note: Optional[str] = None
        if not is_aligned:
            correction_note = (
                f"Resonance score {result.top_resonance_score:.3f} "
                f"below threshold {self._const.resonance_threshold}. "
                f"Suggested alignment: refer to '{result.top_lc_title}' "
                f"and reframe the intent toward its principle."
            )

        return self._poi.format_decision(
            raw_intent=raw_intent,
            result=result,
            is_aligned=is_aligned,
            correction_note=correction_note,
            constitution=self._const
        )
