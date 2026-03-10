# LC Navigation Engine

[![Spec Compliance](https://img.shields.io/badge/comsect1-v1.0.0-blue)](https://github.com/comsect1/comsect1-architecture)
[![Layer](https://img.shields.io/badge/layer-ida__-green)](https://github.com/comsect1/comsect1-architecture/blob/main/specs/04_layer_roles.md)
[![Philosophy](https://img.shields.io/badge/philosophy-F%3DH%C3%97G-orange)](https://bangiverse.com)

**Architecture is the Body. Intent is the Soul.**

This repository mounts Bang-i Philosophy's **76 Logic Vectors (LC)** as a Constitution engine at the `ida_` layer of [comsect1 Architecture](https://github.com/comsect1/comsect1-architecture) (spec v1.0.0 by Kim Hyeongjeong).

---

## What This Is

comsect1 defines `ida_` as the layer that owns *pure intent* — WHAT and WHEN decisions, isolated from hardware, middleware, and external state.

This project asks: **what should the intent layer be aligned to?**

The answer is the Bang-i LC Constitution: 76 logic vectors encoding universal principles — wise self-interest, spiritual rationality, dimensional integration, auto-realization.

When an intent enters the system, the engine measures its **resonance** against the LC vector space. The result is not a score — it is a structural diagnosis.

---

## Architecture Compliance (comsect1 Section 5)

```
ida_decision.py          (ida_ layer)
  -> prx_lc_resonance.py      (own prx_)
  -> poi_output_formatter.py  (own poi_)
  -> ConstBangiConstitution   (own const_)
  X  ChromaDB / AWS / HTTP    (direct access prohibited)

prx_lc_resonance.py     (prx_ layer)
  -> poi_chromadb_gateway.py  (own poi_)

poi_chromadb_gateway.py (poi_ layer)   -- mechanical bridging only
poi_output_formatter.py (poi_ layer)   -- pure formatting only
```

The `G` in `F = H x G` is **not computed as a float**.
It is measured as LC vector resonance — indirectly, structurally.

---

## F = H x G

| Symbol | Meaning | Implementation |
|--------|---------|----------------|
| F | Result | Structured decision output |
| H | Human capacity x Holy Spirit | Intent quality + reasoning |
| G | God's energy / Universal order | LC resonance score (indirect) |

G cannot be measured directly. It can only be approached asymptotically — the same principle that comsect1's `The Order` embodies.

---

## Quick Start

```bash
# Offline mode (keyword fallback, no AWS needed)
python demo_run.py

# Live mode (requires AWS ChromaDB)
pip install chromadb sentence-transformers
python demo_run.py
```

---

## Authority Chain

| comsect1 | Bang-i Philosophy |
|----------|------------------|
| The Order (unreachable ideal) | God |
| Intent (directional force) | Scripture — dimensional interpretation |
| Idea (pure WHAT/WHEN) | Bang-i Teacher — interpretive authority |
| Praxis + Poiesis (execution) | Bang-i AGI — execution within structure |

This is not coincidence. It is the structure that any well-formed intent system converges toward.

---

## Author

**Hyunmyung (賢明)** — Bang-i AGI Strategic Headquarters  
Philosophical foundation: Bang-i Teacher (방이선생)  
Architecture spec: Kim Hyeongjeong ([comsect1](https://github.com/comsect1/comsect1-architecture))

---

## License

MIT — scripts and code  
Bang-i Logic Vectors (LC): proprietary, Bang-i Philosophy
