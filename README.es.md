# 🔍 Inspector IA

> **Asistente forense de IA para periodismo de investigación — detecta anomalías en datos públicos financieros y relacionales de figuras públicas mediante análisis de grafos, ML e IA explicable.**

[![Licencia: MIT](https://img.shields.io/badge/Licencia-MIT-blue.svg)](LICENSE)
[![Ética: Adenda](https://img.shields.io/badge/Ética-Adenda-purple.svg)](ETHICS.md)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green)](#)
[![Estado: Alpha / Diseño](https://img.shields.io/badge/Estado-Alpha%20·%20Dise%C3%B1o-yellow)](docs/STATUS.md)
[![English](https://img.shields.io/badge/lang-English-blue.svg)](README.md)

---

## ⚠️ Honestidad primero

Este proyecto está en **alpha temprano / fase de diseño**. Antes de seguir leyendo:

| Área | Estado real |
|---|---|
| Synthetic Fraud Ecosystem (SFE) — generador CRYPTO_HIDING | ✅ Prototipo funcional |
| Algoritmos de análisis de grafos | 🟡 Parcial (esqueleto + 1 algoritmo) |
| Pipeline de entrenamiento de detección de anomalías | 🟡 Solo esqueleto |
| Motor de explicación XAI | ❌ No implementado |
| Dashboard del periodista (UI web) | ❌ No implementado |
| Demo en vivo | ❌ Sin desplegar |
| Deploy en producción | ❌ No |
| Cumplimiento GDPR / CCPA | 🔄 Planeado (sin auditoría) |

Estado consolidado en [`docs/STATUS.md`](docs/STATUS.md).

---

## 🎯 Misión

Inspector IA ayuda a periodistas de investigación a detectar **patrones sospechosos** (no delitos) en datos públicos — flujos cripto, estructuras offshore, correlaciones viaje/dinero, contratos a empresas fantasma y señales de uso de información privilegiada — y **explica cada alerta** con razonamiento legible (XAI).

> **Es una herramienta periodística, no judicial.** Toda alerta requiere verificación humana.

## ✨ Qué la diferencia

- **Synthetic Fraud Ecosystem (SFE)** — genera patrones de fraude etiquetados para entrenar y validar algoritmos de forma ética, sin tocar datos personales reales hasta que el modelo esté calibrado.
- **IRA (Índice de Riesgo de Anomalía)** — puntaje compuesto único y auditable que combina dimensión patrimonial, de red y temporal.
- **Explicabilidad por defecto** — sin alertas tipo caja negra. Cada score viene con las variables que lo dispararon.
- **Solo datos públicos** — por diseño, sin scraping de cuentas privadas.

---

## 🚀 Inicio rápido

```bash
git clone https://github.com/mechmind-dwv/Inspector_IA.git
cd Inspector_IA
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Genera un dataset sintético con el patrón CRYPTO_HIDING inyectado
python -m synthetic_fraud_ecosystem.generators.crypto_hiding_injector --demo
```

Más detalles en [`QUICKSTART.md`](QUICKSTART.md).

---

## 📊 Fórmula del IRA

```
IRA = W₁·S_patrimonial + W₂·S_red + W₃·S_temporal + B_red

W₁ = 0.30   W₂ = 0.40   W₃ = 0.30   B_red ∈ [0, 30]
```

### Niveles de riesgo

| IRA | Nivel | Nombre interno | Acción periodística |
|---|---|---|---|
| 0 – 20  | **Bajo** | Fondo Cósmico | Monitorización rutinaria |
| 21 – 50 | **Medio** | Sospecha Nebular | Análisis profundo |
| 51 – 70 | **Alto** | Anomalía Estelar | Investigación prioritaria |
| 71 – 85 | **Crítico** | Alerta Supernova | Considerar publicación |
| 86 – 100 | **Extremo** | Agujero Negro | Urgente — múltiples señales |

---

## 🔬 Patrones de Detección

| # | Patrón | Estado |
|---|---|---|
| 1 | `CRYPTO_HIDING` — mixers, monedas privadas, cross-chain | ✅ Generador implementado |
| 2 | `OFFSHORE_LAUNDERING` — cadenas de pantalla, testaferros | 🟡 Especificado |
| 3 | `TRAVEL_COINCIDENCE` — viajes a paraísos ↔ movimientos | 🟡 Especificado |
| 4 | `GHOST_COMPANY` — operación baja + contratos altos | 🟡 Especificado |
| 5 | `INSIDER_TRADING` — movimiento patrimonial pre-ley | 🟡 Especificado |

---

## 🏗️ Arquitectura realista (MVP)

La arquitectura ambiciosa original (Neo4j + Spark + Flink + Kafka + Pinecone + Kubernetes + Blockchain) es la **visión a largo plazo** — ver [`docs/ARCHITECTURE_VISION.md`](docs/ARCHITECTURE_VISION.md). El **MVP actual** es deliberadamente mínimo:

```
Dashboard React/Next.js  ──▶  Gateway FastAPI  ──▶  Workers de detección (Python)
                                     │                       │
                                     ▼                       ▼
                              PostgreSQL                  NetworkX
                              (relacional +              (grafo en proceso,
                              snapshots JSONB)            Neo4j más adelante)
```

---

## 👥 Equipo

**Mantenedor** — [Benjamin Cabeza Durán](mailto:ia.mechmind@gmail.com) — concepto, dirección, ética.

**Herramientas de IA usadas durante el desarrollo** (no son miembros humanos del equipo): DeepSeek, Gemini, Claude. Reconocido de forma transparente en nuestra [Adenda Ética](ETHICS.md).

**Buscamos activamente**: periodistas de investigación, investigadores ML, ingenieros de grafos y asesores legales/éticos. Ver [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## 📈 Roadmap (recalibrado a 2026)

- **2026 T1** — Consolidar SFE: los 5 generadores de patrón completos.
- **2026 T2** — Motor XAI funcional + MVP dashboard (Streamlit primero, Next.js después).
- **2026 T3** — Piloto con 1 medio de investigación sobre datos sintéticos + 1 caso real anonimizado.
- **2026 T4** — Release público `v0.1.0` + threat model + auditoría de divulgación responsable.

Estado vivo: [`docs/STATUS.md`](docs/STATUS.md).

---

## 🔐 Ética y licencia

- **Licencia**: [MIT](LICENSE) estándar — totalmente compatible OSI.
- **Adenda Ética**: [ETHICS.md](ETHICS.md) — un **contrato social no vinculante** que pedimos a usuarios honrar. (Lo mantenemos separado de la LICENSE para que el código siga siendo OSI-compatible.)
- **Líneas rojas** — nos desvincularemos públicamente de cualquier uso para:
  - Vigilancia masiva de ciudadanos privados
  - Discriminación por características protegidas
  - Publicación automatizada sin revisión humana
  - Venta de datos a terceros
  - Targeting político

---

## 🙏 Inspiraciones

ICIJ · OCCRP · The Daphne Project · Stanford SNAP · OpenSanctions · OpenCorporates.

> "Las afirmaciones extraordinarias requieren evidencia extraordinaria." — Carl Sagan

---

## 📬 Contacto

- General: [ia.mechmind@gmail.com](mailto:ia.mechmind@gmail.com)
- Seguridad (PGP próximamente): mismo correo, asunto `[SECURITY]`
- Sitio: <https://mechmind-dwv.github.io/Inspector_IA/>
