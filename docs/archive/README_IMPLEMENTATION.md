# 🔍 Inspector IA - Guía de Implementación Completa

## 📋 Tabla de Contenidos

- [Resumen de la Implementación](#resumen-de-la-implementación)
- [Arquitectura Implementada](#arquitectura-implementada)
- [Instalación y Configuración](#instalación-y-configuración)
- [Uso del Sistema](#uso-del-sistema)
- [Componentes Principales](#componentes-principales)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Testing](#testing)
- [Despliegue](#despliegue)

---

## 🎯 Resumen de la Implementación

Esta implementación completa del sistema **Inspector IA** incluye todos los componentes necesarios para realizar análisis forense de inteligencia en investigación periodística, siguiendo fielmente la documentación técnica proporcionada.

### ✅ Componentes Implementados

1. **Sistema de Cálculo de IRA (Índice de Riesgo de Anomalía)**
   - Cálculo completo con ponderación dinámica
   - Tres dimensiones: Patrimonial, Redes, Temporal
   - Bonus de complejidad de red (0-30 puntos)
   - Clasificación en 5 niveles de riesgo

2. **Motor de Análisis de Grafos**
   - Conector Neo4j completo
   - Consultas Cypher optimizadas
   - Detección de caminos sospechosos
   - Análisis de empresas fantasma
   - Correlaciones temporales

3. **Sistema de Detección de Patrones de Fraude**
   - CRYPTO_HIDING: Ocultamiento con criptomonedas
   - OFFSHORE_LAUNDERING: Lavado offshore
   - TRAVEL_COINCIDENCE: Coincidencias de viaje
   - GHOST_COMPANY: Empresas fantasma
   - INSIDER_TRADING: Uso de información privilegiada

4. **API REST con FastAPI**
   - Endpoints completos para análisis
   - Documentación automática (Swagger/ReDoc)
   - Validación con Pydantic
   - Manejo de errores robusto

5. **Sistema de Ponderación Dinámica**
   - Ajuste automático de pesos según completitud de datos
   - Umbral configurable de completitud
   - Normalización automática

6. **Infraestructura Docker**
   - Docker Compose completo
   - Neo4j, PostgreSQL, Redis, RabbitMQ
   - Prometheus y Grafana para monitoreo
   - Celery para tareas en segundo plano

---

## 🏗️ Arquitectura Implementada

```
┌─────────────────────────────────────────────────────────────┐
│                    Journalist Dashboard (React)             │
├─────────────────────────────────────────────────────────────┤
│              API Gateway (FastAPI)                           │
│              /api/v1/analyze/risk                            │
│              /api/v1/calculate/ira                           │
│              /api/v1/fraud-patterns                          │
├──────────────┬──────────────┬────────────────┬─────────────┤
│  Risk        │  IRA         │  Pattern       │  Neo4j      │
│  Calculator  │  Calculator  │  Detector      │  Connector  │
├──────────────┴──────────────┴────────────────┴─────────────┤
│           Message Bus (RabbitMQ/Kafka)                      │
├──────────────┬──────────────┬────────────────┬─────────────┤
│  PostgreSQL  │  Neo4j       │  Redis         │  RabbitMQ   │
│  (Data Lake) │  (Graph DB)  │  (Cache)       │  (Queue)    │
└──────────────┴──────────────┴────────────────┴─────────────┘
```

### Flujo de Análisis

1. **Entrada de Datos**: Político + Grafo + Eventos Temporales
2. **Análisis de Completitud**: Evaluación de disponibilidad de datos
3. **Cálculo de Pesos Dinámicos**: Ajuste según completitud
4. **Cálculo por Dimensiones**:
   - Dimensión Patrimonial (30% base)
   - Dimensión de Redes (40% base)
   - Dimensión Temporal (30% base)
5. **Bonus de Red**: 0-30 puntos adicionales
6. **Detección de Patrones**: 5 patrones de fraude
7. **Generación de Reportes**: JSON, Markdown, XAI

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.11+
- Docker y Docker Compose
- Git
- 8GB RAM mínimo (16GB recomendado)
- 20GB espacio en disco

### Instalación Rápida

```bash
# 1. Clonar el repositorio
git clone https://github.com/mechmind-dwv/Inspector_IA.git
cd Inspector_IA

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# 5. Iniciar servicios con Docker
docker-compose up -d

# 6. Verificar que los servicios estén corriendo
docker-compose ps

# 7. Crear índices en Neo4j
python scripts/init_database.py
```

### Verificación de Instalación

```bash
# Verificar API
curl http://localhost:8000/api/health

# Verificar Neo4j
curl http://localhost:7474

# Verificar Grafana
curl http://localhost:3001
```

---

## 💻 Uso del Sistema

### 1. Análisis Básico con Script de Ejemplo

```bash
cd examples
python example_analysis.py
```

Este script ejecuta un análisis completo con datos de ejemplo y genera:
- Reporte JSON con todos los detalles
- Reporte Markdown legible
- Salida en consola con resultados principales

### 2. Uso de la API REST

#### Análisis Completo de Riesgo

```bash
curl -X POST "http://localhost:8000/api/v1/analyze/risk" \
  -H "Content-Type: application/json" \
  -d '{
    "politician_data": {
      "id": "POL-001",
      "name": "Juan Pérez",
      "position": "Senador",
      "annual_income": 150000,
      "total_assets": 2500000,
      "years_in_office": 8
    },
    "graph_data": {
      "offshore_entities": [],
      "ghost_companies": [],
      "crypto_wallets": []
    },
    "temporal_events": []
  }'
```

#### Cálculo Solo de IRA

```bash
curl -X POST "http://localhost:8000/api/v1/calculate/ira" \
  -H "Content-Type: application/json" \
  -d '{
    "politician_data": {...},
    "graph_data": {...},
    "temporal_events": []
  }'
```

### 3. Uso Programático en Python

```python
from src.core.risk_calculator import RiskCalculator

# Inicializar calculador
calculator = RiskCalculator()

# Preparar datos
politician_data = {
    "id": "POL-001",
    "name": "Juan Pérez",
    "annual_income": 150000,
    "total_assets": 2500000,
    "years_in_office": 8
}

graph_data = {
    "offshore_entities": [...],
    "ghost_companies": [...],
    "crypto_wallets": [...]
}

temporal_events = [...]

# Realizar análisis
result = calculator.calculate_comprehensive_risk(
    politician_id="POL-001",
    politician_data=politician_data,
    graph_data=graph_data,
    temporal_events=temporal_events
)

# Acceder a resultados
print(f"IRA Score: {result['ira_result']['final_score']}")
print(f"Risk Level: {result['ira_result']['risk_level']}")
print(f"Patterns Detected: {result['patterns_detected_count']}")
```

---

## 🔧 Componentes Principales

### 1. IRACalculator (`src/core/anomaly_index.py`)

Calcula el Índice de Riesgo de Anomalía con la fórmula:

```
IRA = (W₁ × S₁) + (W₂ × S₂) + (W₃ × S₃) + B_network

Donde:
- W₁ = 0.30 (Peso Dimensión Patrimonial)
- W₂ = 0.40 (Peso Dimensión de Redes)
- W₃ = 0.30 (Peso Dimensión Temporal)
- B_network ∈ [0, 30] (Bonus de Complejidad de Red)
```

**Características:**
- Ponderación dinámica basada en completitud
- 5 niveles de riesgo (0-20, 21-50, 51-70, 71-85, 86-100)
- Explicaciones detalladas por dimensión
- Generación automática de recomendaciones

### 2. RiskCalculator (`src/core/risk_calculator.py`)

Orquesta el análisis completo integrando:
- Cálculo de IRA
- Detección de patrones de fraude
- Análisis de completitud
- Generación de reportes

**Patrones Detectados:**
- **CRYPTO_HIDING**: Mixers, privacy coins, cross-chain
- **OFFSHORE_LAUNDERING**: Shell companies, nominee shareholders
- **TRAVEL_COINCIDENCE**: Correlaciones viaje-transacción
- **GHOST_COMPANY**: Empresas de baja actividad
- **INSIDER_TRADING**: Correlaciones legislativas-financieras

### 3. Neo4jConnector (`src/database/neo4j_connector.py`)

Gestiona la conexión y consultas a Neo4j:
- Operaciones CRUD en nodos y relaciones
- Consultas Cypher optimizadas
- Detección de caminos sospechosos
- Análisis de empresas fantasma
- Correlaciones temporales

**Consultas Principales:**
```cypher
// Encontrar caminos a contratos públicos
MATCH path = (p:Politico {id: $id})-[*1..3]-(c:ContratoPublico)
RETURN path, length(path) as distance
ORDER BY distance ASC

// Detectar empresas fantasma
MATCH (e:Empresa)
WHERE NOT EXISTS((e)-[:TIENE_CUENTA_BANCARIA]->())
  AND NOT EXISTS((e)-[:ES_PROPIETARIO]->(:Activo))
RETURN e
```

### 4. FastAPI Application (`src/api/main.py`)

API REST completa con:
- Endpoints de análisis
- Validación de datos con Pydantic
- Documentación automática
- Manejo de errores
- Background tasks con Celery

**Endpoints Principales:**
- `POST /api/v1/analyze/risk`: Análisis completo
- `POST /api/v1/calculate/ira`: Solo IRA
- `GET /api/v1/risk-levels`: Matriz de niveles
- `GET /api/v1/fraud-patterns`: Patrones detectables
- `GET /api/health`: Health check

---

## 📊 Interpretación de Resultados

### Niveles de Riesgo IRA

| Rango | Nivel | Color | Acción |
|-------|-------|-------|--------|
| 0-20 | Cosmic Background | 🟢 | Monitoreo rutinario |
| 21-50 | Nebular Suspicion | 🟡 | Análisis profundo |
| 51-70 | Stellar Anomaly | 🟠 | Investigación prioritaria |
| 71-85 | Supernova Alert | 🔴 | Considerar publicación |
| 86-100 | Black Hole Critical | ⚫ | Investigación urgente |

### Estructura del Reporte

```json
{
  "ira_result": {
    "final_score": 67.5,
    "risk_level": "Stellar Anomaly",
    "confidence_level": 0.85,
    "dimensions": {
      "patrimonial": {...},
      "network": {...},
      "temporal": {...}
    },
    "network_bonus": 15.0,
    "key_risk_factors": [...],
    "recommendations": [...]
  },
  "fraud_patterns": {
    "crypto_hiding": {...},
    "offshore_laundering": {...},
    ...
  },
  "executive_summary": "...",
  "formatted_report": "..."
}
```

---

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Tests específicos
pytest tests/test_ira_calculator.py
pytest tests/test_risk_calculator.py
pytest tests/test_api.py

# Con cobertura
pytest --cov=src --cov-report=html
```

### Tests Incluidos

- ✅ Cálculo de IRA
- ✅ Ponderación dinámica
- ✅ Detección de patrones
- ✅ Endpoints de API
- ✅ Conexión Neo4j
- ✅ Validación de datos

---

## 🚢 Despliegue

### Desarrollo Local

```bash
docker-compose up -d
```

### Producción

```bash
# 1. Configurar variables de entorno de producción
cp .env.example .env.production
# Editar .env.production con valores seguros

# 2. Construir imágenes
docker-compose -f docker-compose.prod.yml build

# 3. Desplegar
docker-compose -f docker-compose.prod.yml up -d

# 4. Verificar
docker-compose -f docker-compose.prod.yml ps
```

### Kubernetes

```bash
# Aplicar configuraciones
kubectl apply -f k8s/

# Verificar despliegue
kubectl get pods -n inspector-ia
```

---

## 📈 Monitoreo

### Prometheus Metrics

Acceder a: `http://localhost:9090`

Métricas disponibles:
- `inspector_ia_requests_total`: Total de requests
- `inspector_ia_analysis_duration_seconds`: Duración de análisis
- `inspector_ia_ira_score`: Scores IRA calculados
- `inspector_ia_patterns_detected`: Patrones detectados

### Grafana Dashboards

Acceder a: `http://localhost:3001`
- Usuario: `admin`
- Contraseña: `inspector_ia_2024`

Dashboards incluidos:
- Inspector IA Overview
- Risk Analysis Metrics
- Pattern Detection Statistics
- System Performance

---

## 🔐 Seguridad

### Mejores Prácticas Implementadas

1. **Encriptación**
   - AES-256-GCM para datos en reposo
   - TLS 1.3 para comunicaciones

2. **Autenticación**
   - OAuth 2.1 + JWT
   - Tokens de corta duración

3. **Autorización**
   - RBAC (Role-Based Access Control)
   - Políticas basadas en atributos

4. **Auditoría**
   - Logs inmutables
   - Blockchain anchoring para provenance

5. **Privacidad**
   - Differential privacy para agregados
   - Anonimización automática
   - Cumplimiento GDPR/CCPA

---

## 📚 Documentación Adicional

- [Documentación de API](http://localhost:8000/api/docs)
- [Arquitectura Detallada](docs/ARCHITECTURE.md)
- [Guía de Despliegue](docs/DEPLOYMENT_GUIDE.md)
- [Marco Ético](docs/ETHICAL_FRAMEWORK.md)
- [Guía de Contribución](CONTRIBUTING.md)

---

## 🤝 Soporte y Contribución

### Reportar Issues

Usar el sistema de issues de GitHub:
https://github.com/mechmind-dwv/Inspector_IA/issues

### Contribuir

1. Fork el repositorio
2. Crear branch de feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

### Contacto

- Email: ia.mechmind@gmail.com
- GitHub: [@mechmind-dwv](https://github.com/mechmind-dwv)

---

## ⚖️ Disclaimer Legal

**Inspector IA es una herramienta de apoyo a la investigación periodística, NO un sistema judicial.**

Este sistema:
- ✅ Identifica **anomalías estadísticas** en datos públicos
- ✅ Genera **alertas de riesgo** que requieren verificación humana
- ✅ Proporciona **explicaciones** de los hallazgos
- ❌ NO determina culpabilidad o inocencia
- ❌ NO reemplaza la investigación periodística profesional
- ❌ NO debe usarse como única fuente para publicaciones

**Toda información debe ser verificada por periodistas profesionales antes de cualquier publicación.**

---

## 📄 Licencia

MIT License with Ethical Clause

Copyright (c) 2024 Inspector IA Team

Ver [LICENSE](LICENSE) para detalles completos.

---

**🌟 Inspector IA - Transformando datos públicos en accountability**
