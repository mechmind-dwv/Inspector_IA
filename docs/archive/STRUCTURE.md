# 🌌 Inspector IA - Estructura del Proyecto

## 📁 Estructura de Directorios

```
INSPECTOR_IA/
│
├── 📁 docs/                           # Documentación completa
│   ├── 📄 ARCHITECTURE.md            # Arquitectura del sistema
│   ├── 📄 ETHICAL_FRAMEWORK.md       # Principios éticos
│   ├── 📄 DEPLOYMENT_GUIDE.md        # Guía de despliegue
│   └── 📁 diagrams/                   # Diagramas del sistema
│       └── system_architecture.mmd
│
├── 📁 src/                            # Código fuente principal
│   │
│   ├── 📁 core/                       # Núcleo del sistema ✅
│   │   ├── 📄 __init__.py
│   │   ├── 📄 anomaly_index.py       # ✅ IRA Calculator (800 líneas)
│   │   ├── 📄 risk_calculator.py     # ✅ Risk Calculator (600 líneas)
│   │   └── 📁 xai/                    # Explicabilidad (XAI)
│   │       ├── 📄 __init__.py
│   │       ├── 📄 explanations.py
│   │       ├── 📄 visualizations.py
│   │       └── 📄 narrative_builder.py
│   │
│   ├── 📁 data/                       # Gestión de datos
│   │   ├── 📄 __init__.py
│   │   ├── 📁 ingestion/              # Ingesta de datos
│   │   │   ├── 📄 scrapers.py
│   │   │   ├── 📄 normalizers.py
│   │   │   └── 📄 validators.py
│   │   ├── 📁 storage/                # Almacenamiento
│   │   │   ├── 📄 data_lake.py
│   │   │   ├── 📄 graph_db.py
│   │   │   └── 📄 blockchain.py
│   │   └── 📁 integrity/              # ✅ Integridad de datos
│   │       ├── 📄 merkle_tree.py
│   │       ├── 📄 provenance.py
│   │       └── 📄 verification.py
│   │
│   ├── 📁 detection/                  # Motor de detección
│   │   ├── 📄 __init__.py
│   │   ├── 📁 patterns/              # ✅ Patrones de fraude
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 crypto_hiding.py   # ✅ CRYPTO_HIDING
│   │   │   ├── 📄 offshore_laundering.py
│   │   │   ├── 📄 travel_coincidence.py
│   │   │   ├── 📄 ghost_company.py
│   │   │   └── 📄 insider_trading.py
│   │   ├── 📁 algorithms/            # ✅ Algoritmos
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 graph_analysis.py  # ✅ Análisis de grafos
│   │   │   ├── 📄 temporal_patterns.py
│   │   │   ├── 📄 statistical_anomalies.py
│   │   │   └── 📄 ml_models.py
│   │   └── 📁 heuristics/            # Heurísticas
│   │       ├── 📄 crypto_heuristics.py
│   │       ├── 📄 financial_heuristics.py
│   │       └── 📄 network_heuristics.py
│   │
│   ├── 📁 synthetic/                  # ✅ Ecosistema sintético
│   │   ├── 📄 __init__.py
│   │   ├── 📄 fraud_engine.py        # Motor de fraude sintético
│   │   ├── 📁 generators/
│   │   │   ├── 📄 politician_generator.py
│   │   │   ├── 📄 company_generator.py
│   │   │   ├── 📄 transaction_generator.py
│   │   │   └── 📄 network_generator.py
│   │   ├── 📁 injectors/             # ✅ Inyectores
│   │   │   ├── 📄 crypto_hiding_injector.py  # ✅ (900 líneas)
│   │   │   ├── 📄 offshore_injector.py
│   │   │   └── 📄 pattern_orchestrator.py
│   │   ├── 📁 validators/
│   │   │   ├── 📄 ground_truth_validator.py
│   │   │   ├── 📄 realism_validator.py
│   │   │   └── 📄 statistical_validator.py
│   │   └── 📁 datasets/
│   │       ├── 📄 base_dataset.py
│   │       ├── 📄 training_dataset.py
│   │       └── 📄 validation_dataset.py
│   │
│   ├── 📁 graph/                      # Base de datos de grafos
│   │   ├── 📄 __init__.py
│   │   ├── 📄 schema.py              # Esquema Neo4j
│   │   ├── 📄 queries.py             # Consultas Cypher
│   │   ├── 📁 models/
│   │   │   ├── 📄 nodes.py
│   │   │   ├── 📄 relationships.py
│   │   │   └── 📄 embeddings.py
│   │   └── 📁 analysis/
│   │       ├── 📄 centrality.py
│   │       ├── 📄 community_detection.py
│   │       └── 📄 path_finding.py
│   │
│   ├── 📁 api/                        # ✅ API REST
│   │   ├── 📄 __init__.py
│   │   ├── 📄 app.py                 # ✅ FastAPI App (400 líneas)
│   │   ├── 📄 main.py                # ✅ Alias para compatibilidad
│   │   ├── 📁 routes/
│   │   │   ├── 📄 analysis.py
│   │   │   ├── 📄 data.py
│   │   │   └── 📄 admin.py
│   │   ├── 📁 schemas/
│   │   │   ├── 📄 requests.py
│   │   │   ├── 📄 responses.py
│   │   │   └── 📄 models.py
│   │   └── 📁 middleware/
│   │       ├── 📄 auth.py
│   │       ├── 📄 logging.py
│   │       └── 📄 validation.py
│   │
│   ├── 📁 database/                   # ✅ Conectores de BD
│   │   ├── 📄 __init__.py
│   │   └── 📄 neo4j_connector.py     # ✅ Conector Neo4j (500 líneas)
│   │
│   └── 📁 tests/                      # Suite de pruebas
│       ├── 📄 __init__.py
│       ├── 📁 unit/
│       │   ├── 📄 test_anomaly_index.py
│       │   ├── 📄 test_crypto_hiding.py
│       │   └── 📄 test_graph_analysis.py
│       ├── 📁 integration/
│       │   ├── 📄 test_data_pipeline.py
│       │   ├── 📄 test_detection_engine.py
│       │   └── 📄 test_api_endpoints.py
│       ├── 📁 e2e/
│       │   ├── 📄 test_full_analysis.py
│       │   └── 📄 test_journalist_workflow.py
│       └── 📁 synthetic/
│           ├── 📄 test_pattern_generation.py
│           └── 📄 test_ground_truth.py
│
├── 📁 frontend/                       # Dashboard de periodistas
│   ├── 📄 package.json
│   ├── 📄 next.config.js
│   ├── 📁 src/
│   │   ├── 📁 components/
│   │   ├── 📁 pages/
│   │   └── 📁 services/
│   └── 📁 public/
│
├── 📁 examples/                       # ✅ Ejemplos funcionales
│   └── 📄 example_analysis.py        # ✅ Ejemplo completo
│
├── 📁 config/                         # Configuración
│   ├── 📄 settings.py
│   ├── 📄 development.yml
│   ├── 📄 production.yml
│   └── 📄 testing.yml
│
├── 📁 scripts/                        # Scripts de automatización
│   ├── 📄 setup.py
│   ├── 📄 data_ingestion.py
│   ├── 📄 synthetic_generation.py
│   ├── 📄 model_training.py
│   └── 📄 deployment.py
│
├── 📁 infrastructure/                 # ✅ Infraestructura
│   ├── 📄 docker-compose.yml         # ✅ 9 servicios
│   ├── 📄 Dockerfile
│   ├── 📁 docker/
│   │   └── 📄 Dockerfile.api         # ✅ Dockerfile de API
│   ├── 📁 kubernetes/
│   │   ├── 📄 deployment.yaml
│   │   ├── 📄 service.yaml
│   │   └── 📄 ingress.yaml
│   ├── 📁 terraform/
│   │   ├── 📄 main.tf
│   │   ├── 📄 variables.tf
│   │   └── 📄 outputs.tf
│   └── 📁 monitoring/
│       ├── 📄 prometheus.yml
│       ├── 📁 grafana_dashboards/
│       └── 📄 alerts.yml
│
├── 📁 data/                           # Datos (gitignored)
│   ├── 📁 raw/
│   ├── 📁 processed/
│   ├── 📁 synthetic/
│   └── 📁 models/
│
├── 📁 notebooks/                      # Jupyter notebooks
│   ├── 📄 01_data_exploration.ipynb
│   ├── 📄 02_pattern_analysis.ipynb
│   ├── 📄 03_model_training.ipynb
│   └── 📄 04_results_visualization.ipynb
│
├── 📁 .github/                        # GitHub workflows
│   ├── 📁 workflows/
│   │   ├── 📄 ci.yml
│   │   ├── 📄 cd.yml
│   │   └── 📄 security_scan.yml
│   └── 📄 CODEOWNERS
│
├── 📄 .env.example                   # ✅ Variables de entorno
├── 📄 .gitignore
├── 📄 requirements.txt               # ✅ 60+ dependencias
├── 📄 pyproject.toml
│
├── 📄 README.md                      # Documentación principal
├── 📄 README_IMPLEMENTATION.md       # ✅ Guía de implementación
├── 📄 QUICKSTART.md                  # ✅ Inicio rápido
├── 📄 IMPLEMENTATION_SUMMARY.md      # ✅ Resumen técnico
├── 📄 DELIVERY_SUMMARY.md            # ✅ Resumen de entrega
├── 📄 USEFUL_COMMANDS.md             # ✅ Comandos útiles
├── 📄 STRUCTURE.md                   # ✅ Este archivo
│
├── 📄 LICENSE                        # Licencia MIT
├── 📄 CONTRIBUTING.md
├── 📄 CODE_OF_CONDUCT.md
└── 📄 SECURITY.md
```

---

## 📊 Estado de Implementación

### ✅ Completado (100%)

| Componente | Archivo | Líneas | Estado |
|------------|---------|--------|--------|
| IRA Calculator | `src/core/anomaly_index.py` | 800 | ✅ |
| Risk Calculator | `src/core/risk_calculator.py` | 600 | ✅ |
| Neo4j Connector | `src/database/neo4j_connector.py` | 500 | ✅ |
| FastAPI App | `src/api/app.py` | 400 | ✅ |
| Crypto Hiding Injector | `src/synthetic/injectors/crypto_hiding_injector.py` | 900 | ✅ |
| Graph Analysis | `src/detection/algorithms/graph_analysis.py` | 700 | ✅ |
| Crypto Hiding Detector | `src/detection/patterns/crypto_hiding.py` | 200 | ✅ |
| Docker Compose | `infrastructure/docker-compose.yml` | - | ✅ |
| Ejemplo Funcional | `examples/example_analysis.py` | 300 | ✅ |

### 🚧 En Progreso

- Frontend React/Next.js
- Tests unitarios completos
- Pipeline CI/CD

### 📅 Planificado

- Modelos ML entrenados
- Integración OSINT APIs
- Dashboard de visualización

---

## 🎯 Convenciones del Proyecto

### Nomenclatura de Archivos
- **snake_case.py** para Python
- **PascalCase.tsx** para React
- **kebab-case.yml** para configuraciones

### Estructura de Imports
```python
# Standard library
import os
from typing import Dict, List

# Third party
import pandas as pd
from fastapi import FastAPI

# Local
from src.core.anomaly_index import IRACalculator
from src.database.neo4j_connector import Neo4jConnector
```

### Docstrings
```python
def calculate_risk(politician_id: str) -> float:
    """
    Calcula el riesgo de un político.
    
    Args:
        politician_id: ID del político
    
    Returns:
        Score de riesgo (0-100)
    
    Raises:
        ValueError: Si el ID es inválido
    """
    pass
```

---

## 🚀 Flujo de Desarrollo

### 1. Configurar Entorno
```bash
git clone https://github.com/mechmind-dwv/Inspector_IA.git
cd Inspector_IA
pip install -r requirements.txt
cp .env.example .env
```

### 2. Ejecutar Análisis
```bash
python examples/example_analysis.py
```

### 3. Iniciar API
```bash
docker-compose up -d
# API: http://localhost:8000/api/docs
```

### 4. Ejecutar Tests
```bash
pytest src/tests/
```

---

## 📚 Documentación Adicional

- **README_IMPLEMENTATION.md** - Guía completa de implementación
- **QUICKSTART.md** - Inicio rápido en 5 minutos
- **USEFUL_COMMANDS.md** - Comandos útiles
- **docs/ARCHITECTURE.md** - Arquitectura detallada
- **docs/ETHICAL_FRAMEWORK.md** - Marco ético

---

## 🤝 Contribución

Para contribuir:

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/amazing-feature`)
3. Commit cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

---

## 📞 Soporte

- **Email**: ia.mechmind@gmail.com
- **GitHub**: [@mechmind-dwv](https://github.com/mechmind-dwv)
- **Issues**: https://github.com/mechmind-dwv/Inspector_IA/issues

---

**🌟 Inspector IA - Transformando datos públicos en accountability**

*Versión: 2.0.0 | Fecha: Diciembre 2024*
