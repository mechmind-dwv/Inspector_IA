# 📊 Inspector IA — Consolidated Project Status

> Single source of truth for project state. Replaces and consolidates:
> `IMPLEMENTATION_SUMMARY.md`, `DELIVERY_SUMMARY.md`, `FINAL_SUMMARY.txt`,
> `README_IMPLEMENTATION.md`, `REORGANIZATION_SUMMARY.md`, `STRUCTURE.md`,
> `STRUCTURE.txt`, `PROJECT_STRUCTURE.txt`.
> Those files are preserved in [`docs/archive/`](archive/) for historical reference.

Last updated: **2026-02 — see [git log](../../../commits) for live history.**

---

## 1. Module-by-module status

| Module | Path | Status | Notes |
|---|---|---|---|
| Synthetic Fraud Ecosystem — base | `synthetic_fraud_ecosystem/` | 🟡 Skeleton + 1 generator | CRYPTO_HIDING done, 4 patterns pending |
| `CRYPTO_HIDING` generator | `synthetic_fraud_ecosystem/generators/crypto_hiding_injector.py` | ✅ Working | 3 difficulty levels (basic / intermediate / advanced) |
| `OFFSHORE_LAUNDERING` generator | — | ❌ Not started | Spec only |
| `TRAVEL_COINCIDENCE` generator | — | ❌ Not started | Spec only |
| `GHOST_COMPANY` generator | — | ❌ Not started | Spec only |
| `INSIDER_TRADING` generator | — | ❌ Not started | Spec only |
| Graph algorithms | `graph_algorithms/` *(rename pending)* | 🟡 Partial | `graph_analysis.py` initial draft |
| Anomaly detection — training pipeline | `services/anomaly_detection/training_pipeline.py` | 🟡 Skeleton | No real model yet |
| IRA score calculator | — | ❌ Not implemented | Formula defined in README |
| XAI explanation engine | — | ❌ Not started | SHAP/LIME planned |
| FastAPI gateway | — | ❌ Not started | |
| Journalist dashboard (web UI) | — | ❌ Not started | |
| Live demo deployment | — | ❌ Not deployed | |
| Test suite | `tests/` | ❌ Empty / missing | CONTRIBUTING.md requires tests on PRs |
| CI/CD | `.github/workflows/` | 🟡 Added in this audit | Lint + tests skeleton |
| Pre-commit hooks | `.pre-commit-config.yaml` | ❌ Not configured | |
| Docker compose dev env | `docker-compose.yml` | 🟡 File exists, not verified | |
| Documentation | `docs/`, root `*.md` | 🟡 Excessive, being consolidated | This audit |

---

## 2. Compliance & legal — real status

Earlier docs listed "✅ Full Compliance" for GDPR/CCPA. This was aspirational. **Corrected here:**

| Regulation | Real status | Next step |
|---|---|---|
| GDPR | 🔄 **Not audited** | Need DPIA + lawful basis analysis before any real-data ingestion |
| CCPA | 🔄 **Not audited** | Deletion workflow not implemented |
| FCRA | ⚠️ N/A | Not a consumer-reporting product |
| AML laws | 🔄 N/A for product, internal ops only | |
| Journalistic source protection | 🔄 Planned | No source-handling mechanism implemented yet |

---

## 3. Roadmap delta vs. original README

The original README's "Phase 1 (Current) Q1-Q3 2024" was **24 months out of date** at audit time (Feb 2026). The roadmap has been **rebased to 2026** in `README.md`. Original roadmap preserved in `docs/archive/REORGANIZATION_SUMMARY.md`.

---

## 4. Known issues / debt

1. **`graalgorithms/`** is a typo — should be `graph_algorithms/`. Rename via `git mv`.
2. **`example_analysis_*.json` and `example_report_*.md`** were at repo root — relocated to `examples/legacy/`.
3. **`.cosmicstyleguide.md`** is referenced in CONTRIBUTING.md but never existed — file added in this audit (placeholder + style summary).
4. **Team table** previously listed "DeepSeek AI" and "Gemini Pro" as people. They are AI tools, now correctly attributed in README under *"AI tools used during development"*.
5. **LICENSE** was labelled MIT but contained restrictions, making it non-OSI-MIT. Split: real MIT in `LICENSE`, restrictions moved to non-binding `ETHICS.md`.

---

## 5. How to update this file

Anyone merging a PR that changes module status **must** update the relevant row above in the same PR. The CI checks for a touched `docs/STATUS.md` when files outside `docs/archive/` are modified (see `.github/workflows/ci.yml`).
