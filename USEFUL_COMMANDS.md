# 🛠️ Inspector IA - Comandos Útiles

## 🚀 Inicio Rápido

### Ejecutar Análisis de Ejemplo
```bash
cd /home/ubuntu/Inspector_IA
python3 examples/example_analysis.py
```

### Ver Reportes Generados
```bash
ls -lh example_*.json example_*.md
cat example_report_*.md | head -100
```

---

## 🐳 Docker Commands

### Iniciar Todos los Servicios
```bash
cd /home/ubuntu/Inspector_IA
docker-compose up -d
```

### Ver Estado de Servicios
```bash
docker-compose ps
```

### Ver Logs
```bash
# Todos los servicios
docker-compose logs -f

# Servicio específico
docker-compose logs -f api
docker-compose logs -f neo4j
```

### Detener Servicios
```bash
docker-compose stop
```

### Reiniciar Servicios
```bash
docker-compose restart
```

### Eliminar Todo (CUIDADO)
```bash
docker-compose down -v
```

---

## 🔍 Verificación del Sistema

### Verificar Importaciones
```bash
python3 -c "
from src.core.anomaly_index import IRACalculator
from src.core.risk_calculator import RiskCalculator
print('✅ Sistema OK')
"
```

### Test Rápido de IRA
```bash
python3 -c "
from src.core.anomaly_index import IRACalculator
calc = IRACalculator()
print('✅ IRACalculator funcional')
"
```

### Verificar API (con Docker)
```bash
curl http://localhost:8000/api/health
```

---

## 📊 Análisis Personalizado

### Crear Análisis Personalizado
```python
# Guardar como my_analysis.py
from src.core.risk_calculator import RiskCalculator

calculator = RiskCalculator()

politician_data = {
    "id": "POL-CUSTOM-001",
    "name": "Mi Político",
    "annual_income": 200000,
    "total_assets": 1000000,
    "years_in_office": 4
}

graph_data = {
    "offshore_entities": [],
    "ghost_companies": [],
    "crypto_wallets": []
}

temporal_events = []

result = calculator.calculate_comprehensive_risk(
    politician_id="POL-CUSTOM-001",
    politician_data=politician_data,
    graph_data=graph_data,
    temporal_events=temporal_events
)

print(f"IRA: {result['ira_result']['final_score']:.2f}")
print(f"Nivel: {result['ira_result']['risk_level']}")
```

### Ejecutar
```bash
python3 my_analysis.py
```

---

## 🗄️ Neo4j

### Acceder a Neo4j Browser
```
URL: http://localhost:7474
Usuario: neo4j
Contraseña: inspector_ia_2024
```

### Consultas Cypher Útiles

#### Ver todos los políticos
```cypher
MATCH (p:Politico) RETURN p LIMIT 10
```

#### Ver todas las empresas
```cypher
MATCH (e:Empresa) RETURN e LIMIT 10
```

#### Encontrar caminos sospechosos
```cypher
MATCH path = (p:Politico)-[*1..3]-(c:ContratoPublico)
RETURN path LIMIT 5
```

---

## 📈 API REST

### Análisis Completo (con curl)
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
      "ghost_companies": []
    },
    "temporal_events": []
  }'
```

### Ver Niveles de Riesgo
```bash
curl http://localhost:8000/api/v1/risk-levels
```

### Ver Patrones de Fraude
```bash
curl http://localhost:8000/api/v1/fraud-patterns
```

### Documentación Interactiva
```
http://localhost:8000/api/docs
```

---

## 🧹 Mantenimiento

### Limpiar Archivos Temporales
```bash
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

### Ver Espacio en Disco (Docker)
```bash
docker system df
```

### Limpiar Docker (CUIDADO)
```bash
docker system prune -a
```

---

## 📝 Logs y Debugging

### Ver Logs de Python
```bash
tail -f logs/inspector_ia.log
```

### Modo Debug en API
```bash
# Editar docker-compose.yml
environment:
  - LOG_LEVEL=DEBUG
```

### Python Debug
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🔧 Configuración

### Editar Variables de Entorno
```bash
cp .env.example .env
nano .env
```

### Cambiar Puerto de API
```bash
# En .env
API_PORT=8080

# En docker-compose.yml
ports:
  - "8080:8000"
```

---

## 📊 Monitoreo

### Prometheus
```
URL: http://localhost:9090
```

### Grafana
```
URL: http://localhost:3001
Usuario: admin
Contraseña: inspector_ia_2024
```

---

## 🆘 Solución de Problemas

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Error: "Connection refused" (Docker)
```bash
docker-compose restart
docker-compose ps
```

### Error: "Port already in use"
```bash
# Cambiar puerto en docker-compose.yml
# O detener el servicio que usa el puerto
sudo lsof -i :8000
```

### Resetear Todo
```bash
docker-compose down -v
docker-compose up -d
```

---

## 📚 Recursos

- **Documentación**: README_IMPLEMENTATION.md
- **Inicio Rápido**: QUICKSTART.md
- **API Docs**: http://localhost:8000/api/docs
- **Ejemplos**: examples/example_analysis.py

---

**🌟 ¡Listo para usar Inspector IA!**
