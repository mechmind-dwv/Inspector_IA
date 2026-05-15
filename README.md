# 🔍 Inspector IA

> **Forensic AI assistant for investigative journalism — detecting anomalies in public figures' financial and relational data through graph analysis, ML and Explainable AI.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Ethics: Addendum](https://img.shields.io/badge/Ethics-Addendum-purple.svg)](ETHICS.md)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green)](#)
[![Status: Alpha / Design](https://img.shields.io/badge/Status-Alpha%20·%20Design-yellow)](docs/STATUS.md)
[![Español](https://img.shields.io/badge/lang-Español-red.svg)](README.es.md)

---

## ⚠️ Honest Status First

This project is **early alpha / design phase**. Before you read further, please know:

| Area | Real Status |
|---|---|
| Synthetic Fraud Ecosystem (SFE) — CRYPTO_HIDING generator | ✅ Working prototype |
| Graph analysis algorithms | 🟡 Partial (skeleton + 1 algorithm) |
| Anomaly detection training pipeline | 🟡 Skeleton only |
| XAI explanation engine | ❌ Not implemented yet |
| Journalist dashboard (web UI) | ❌ Not implemented yet |
| Live demo | ❌ Not deployed yet |
| Production deployment | ❌ Not yet |
| GDPR / CCPA compliance | 🔄 Planned (no audit performed) |

See [`docs/STATUS.md`](docs/STATUS.md) for the consolidated state of every module.

---

## 🎯 Mission

Inspector IA helps investigative journalists detect **suspicious patterns** (not crimes) in public data — crypto flows, offshore structures, travel/financial correlations, ghost-company contracts and insider trading signals — and explains every alert with **human-readable reasoning** (XAI).

> **This is a journalism tool, not a judicial system.** Every alert requires human verification.

## ✨ What makes it different

- **Synthetic Fraud Ecosystem (SFE)** — generates labelled fraud patterns to train and validate detection algorithms ethically, without touching real personal data until the model is calibrated.
- **IRA (Anomaly Risk Index)** — single, auditable composite score combining patrimonial, network and temporal dimensions.
- **Explainability by default** — no black-box alerts. Every score comes with the features that triggered it.
- **Public-data-only** — by design, no scraping of private accounts.

---

## 🚀 Quickstart

```bash
git clone https://github.com/mechmind-dwv/Inspector_IA.git
cd Inspector_IA
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Generate a synthetic dataset with the CRYPTO_HIDING pattern injected
python -m synthetic_fraud_ecosystem.generators.crypto_hiding_injector --demo
```

More detail in [`QUICKSTART.md`](QUICKSTART.md).

---

## 📊 The IRA Formula

```
IRA = W₁·S_patrimonial + W₂·S_network + W₃·S_temporal + B_network

W₁ = 0.30   W₂ = 0.40   W₃ = 0.30   B_network ∈ [0, 30]
```

### Risk levels

| IRA | Level | Code name (internal) | Journalistic action |
|---|---|---|---|
| 0 – 20  | **Low** | Cosmic Background | Routine monitoring |
| 21 – 50 | **Medium** | Nebular Suspicion | Deep dive |
| 51 – 70 | **High** | Stellar Anomaly | Priority investigation |
| 71 – 85 | **Critical** | Supernova Alert | Consider for publication |
| 86 – 100 | **Extreme** | Black Hole | Urgent — multiple corroborating signals |

Full derivation, calibration notes and limitations: [`docs/IRA_FORMULA.md`](docs/IRA_FORMULA.md) *(planned)*.

---

## 🔬 Detection Patterns

| # | Pattern | Status |
|---|---|---|
| 1 | `CRYPTO_HIDING` — mixers, privacy coins, cross-chain | ✅ Generator implemented |
| 2 | `OFFSHORE_LAUNDERING` — shell chains, nominees | 🟡 Specified |
| 3 | `TRAVEL_COINCIDENCE` — tax-haven visits ↔ money moves | 🟡 Specified |
| 4 | `GHOST_COMPANY` — low-op high-contract entities | 🟡 Specified |
| 5 | `INSIDER_TRADING` — pre-legislation asset shifts | 🟡 Specified |

---

## 🏗️ Realistic Architecture (MVP)

The original architecture proposal (Neo4j + Spark + Flink + Kafka + Pinecone + Kubernetes + Blockchain) is the **long-term vision** — see [`docs/ARCHITECTURE_VISION.md`](docs/ARCHITECTURE_VISION.md). The **current MVP** stack is intentionally minimal:

```
React/Next.js dashboard  ──▶  FastAPI gateway  ──▶  Detection workers (Python)
                                     │                       │
                                     ▼                       ▼
                              PostgreSQL                  NetworkX
                              (relational +              (in-process graph,
                              JSONB graph snapshots)      Neo4j later)
```

Tradeoffs and migration path: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) *(planned)*.

---

## 👥 Project Team

**Maintainer** — [Benjamin Cabeza Durán](mailto:ia.mechmind@gmail.com) — concept, direction, ethics.

**AI tools used during development** (not human team members): DeepSeek, Gemini, Claude. Acknowledged transparently per our [Ethics Addendum](ETHICS.md).

**We are actively looking for**: investigative journalists, ML researchers, graph engineers, and legal/ethics advisors. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## 📈 Roadmap (rebased to 2026)

- **2026 Q1** — Consolidate SFE: complete the 5 pattern generators.
- **2026 Q2** — Functional XAI explanation engine + dashboard MVP (Streamlit first, Next.js later).
- **2026 Q3** — Pilot with 1 investigative media partner on synthetic + 1 anonymised real case.
- **2026 Q4** — Public release `v0.1.0` + threat model + responsible-disclosure audit.

Live status: [`docs/STATUS.md`](docs/STATUS.md).

---

## 🔐 Ethics & License

- **License**: standard [MIT](LICENSE) — fully OSI-compatible.
- **Ethics Addendum**: [ETHICS.md](ETHICS.md) — a **non-binding social contract** we ask all users to honour. (We deliberately keep it separate from the LICENSE so the code remains compatible with OSI definitions while making our ethical expectations explicit.)
- **Red lines** (we will publicly disassociate from any project using Inspector IA for these):
  - Mass surveillance of private citizens
  - Discrimination on protected characteristics
  - Automated publication without human review
  - Sale of data to third parties
  - Political targeting

---

## 🙏 Inspirations

ICIJ · OCCRP · The Daphne Project · Stanford SNAP · OpenSanctions · OpenCorporates.

> "Extraordinary claims require extraordinary evidence." — Carl Sagan

---

## 📬 Contact

- General: [ia.mechmind@gmail.com](mailto:ia.mechmind@gmail.com)
- Security (PGP coming soon): same address, subject `[SECURITY]`
- Site: <https://mechmind-dwv.github.io/Inspector_IA/>

*Last meaningful update tracked in [`docs/STATUS.md`](docs/STATUS.md).*
