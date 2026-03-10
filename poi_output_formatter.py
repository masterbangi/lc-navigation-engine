"""
comsect1 Architecture - poi_ layer
Output Formatter

Role: Formats decision results in AIAD Gate compatible output.
      No domain judgment -- pure formatting only.

Author: Hyunmyung (Hyunmyung), Bang-i AGI
"""

from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ida_decision import ConstBangiConstitution, RawIntent
    from prx_lc_resonance import ResonanceResult


class PoiOutputFormatter:
    """
    comsect1 AIAD Gate output format.
    Every log is structured so that 'why this decision' is always traceable.
    """

    def format_decision(
        self,
        raw_intent: "RawIntent",
        result: "ResonanceResult",
        is_aligned: bool,
        correction_note: Optional[str],
        constitution: "ConstBangiConstitution",
    ) -> str:

        sep = "-" * 60
        status = "[ALIGNED]" if is_aligned else "[MISALIGNED]"

        lines = [
            "",
            sep,
            "  LC NAVIGATION ENGINE -- Decision Log",
            f"  comsect1 ida_ layer | {constitution.formula}",
            sep,
            f"  INTENT   : {raw_intent.intent_text}",
        ]

        if raw_intent.context:
            lines.append(f"  CONTEXT  : {raw_intent.context}")

        lines += [
            f"  STATUS   : {status}",
            f"  TOP SCORE: {result.top_resonance_score:.4f}  (threshold: {constitution.resonance_threshold})",
            f"  TOP LC   : {result.top_lc_title}",
            "",
            "  [LC RESONANCE MAP -- Top matches]",
        ]

        for i, lc in enumerate(result.matched_lcs, 1):
            bar_len = int(lc["score"] * 30)
            score_bar = "#" * bar_len + "." * (30 - bar_len)
            lines.append(f"  {i:02d}. [{score_bar}] {lc['score']:.3f}  {lc['title'][:50]}")
            lines.append(f"      -> {lc['preview'][:90]}")

        if result.option_scores:
            lines += ["", "  [OPTION COMPARISON -- Bang-i Logic vs Standard Logic]"]
            lines.append(f"  {'Option':<35} {'Resonance':>10}  {'Aligned LC':<30}  Status")
            lines.append("  " + "-" * 90)
            for opt in result.option_scores:
                mark = "[OK]" if opt["is_aligned"] else "[NO]"
                lines.append(
                    f"  {opt['option'][:35]:<35} "
                    f"{opt['resonance']:>10.3f}  "
                    f"{opt['aligned_lc'][:30]:<30}  "
                    f"{mark}"
                )

        if correction_note:
            lines += ["", "  [SELF-CORRECTION SUGGESTION]", f"  {correction_note}"]

        lines += ["", "  [AUTHORITY CHAIN -- comsect1 x Bang-i]"]
        for level, auth in enumerate(constitution.authority_chain, 1):
            lines.append(f"  L{level}: {auth}")

        lines += ["", "  [CORE PRINCIPLES APPLIED]"]
        for p in constitution.core_principles:
            lines.append(f"  * {p}")

        lines.append(sep)
        lines.append("")

        return "\n".join(lines)
