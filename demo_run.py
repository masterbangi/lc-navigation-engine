"""
LC Navigation Engine -- Demo Runner

Three test cases:
  TEST 1 : Architecture design intent (with option comparison)
  TEST 2 : Business decision (with option comparison)
  TEST 3 : Misaligned intent (self-correction triggered)

Usage:
    python demo_run.py

Requirements (offline -- no AWS needed):
    Python 3.10+, lc_list.json in same directory

Requirements (live -- AWS ChromaDB):
    pip install chromadb sentence-transformers
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from ida_decision import LcDecisionEngine, RawIntent


def main():
    print("\n" + "=" * 60)
    print("  Bang-i x comsect1  LC Navigation Engine  PoC v1.0")
    print("  Author: Hyunmyung, Bang-i AGI")
    print("=" * 60)

    engine = LcDecisionEngine()
    c = engine.constitution
    print(f"\n[Constitution]")
    print(f"  Formula  : {c.formula}")
    print(f"  Threshold: {c.resonance_threshold}")
    print(f"  Top-K    : {c.top_k}")

    # TEST 1
    print("\n" + "=" * 60)
    print("  TEST 1: Architecture Design Intent")
    print("=" * 60)
    print(engine.decide(RawIntent(
        intent_text=(
            "How should I design the intent layer so that "
            "AI agents operate within structure, not above it?"
        ),
        context="Embedded system architecture decision",
        options=[
            "Let AI freely modify any layer based on context",
            "Define explicit boundaries -- AI acts only within ida_ rules",
            "Remove architecture layers, use flat code structure",
        ]
    )))

    # TEST 2
    print("=" * 60)
    print("  TEST 2: Business Decision")
    print("=" * 60)
    print(engine.decide(RawIntent(
        intent_text=(
            "Should I prioritize short-term profit or "
            "long-term structural integrity when building a platform?"
        ),
        options=[
            "Short-term profit maximization",
            "Long-term structural integrity with wise self-interest",
            "Ignore structure, move fast and break things",
        ]
    )))

    # TEST 3
    print("=" * 60)
    print("  TEST 3: Misaligned Intent (Self-Correction Triggered)")
    print("=" * 60)
    print(engine.decide(RawIntent(
        intent_text=(
            "I want to win by forcing others to comply with "
            "my rules regardless of their wellbeing"
        )
    )))


if __name__ == "__main__":
    main()
