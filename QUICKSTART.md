# 🚀 Inspector IA - Inicio Rápido

## ⚡ Instalación en 5 Minutos

### 1. Clonar el Repositorio

```bash
git clone https://github.com/mechmind-dwv/Inspector_IA.git
cd Inspector_IA
```

### 2. Instalar Dependencias

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar paquetes
pip install -r requirements.txt
```

### 3. Ejecutar Análisis de Ejemplo

```bash
cd examples
python example_analysis.py
```

¡Eso es todo! Verás un análisis completo en tu terminal.

---

## 📊 Resultado del Ejemplo

El script analiza un político ficticio y genera:

```
🎯 ÍNDICE DE RIESGO DE ANOMALÍA (IRA): 66.13/100
📊 Nivel de Riesgo: 🟠 Stellar Anomaly
🎓 Confianza del Análisis: 69.3%
⚠️  Patrones de Fraude Detectados: 3
```

### Archivos Generados

- `example_analysis_YYYYMMDD_HHMMSS.json` - Datos completos en JSON
- `example_report_YYYYMMDD_HHMMSS.md` - Reporte legible en Markdown

---

## 🔧 Uso Programático Básico

```python
from src.core.risk_calculator import RiskCalculator

# 1. Inicializar
calculator = RiskCalculator()

# 2. Preparar datos
politician_data = {
    "id": "POL-001",
    "name": "Juan Pérez",
    "annual_income": 150000,
    "total_assets": 2500000,
    "years_in_office": 8
}

graph_data = {
    "offshore_entities": [],
    "ghost_companies": [],
    "crypto_wallets": []
}

temporal_events = []

# 3. Analizar
result = calculator.calculate_comprehensive_risk(
    politician_id="POL-001",
    politician_data=politician_data,
    graph_data=graph_data,
    temporal_events=temporal_events
)

# 4. Ver resultados
print(f"IRA: {result['ira_result']['final_score']:.2f}")
print(f"Nivel: {result['ira_result']['risk_level']}")
```

---

## 🐳 Con Docker (Infraestructura Completa)

```bash
# 1. Copiar configuración
cp .env.example .env

# 2. Iniciar servicios
docker-compose up -d

# 3. Verificar
docker-compose ps

# 4. Acceder a servicios
# API: http://localhost:8000/api/docs
# Neo4j: http://localhost:7474
# Grafana: http://localhost:3001
```

---

## 📚 Próximos Pasos

1. **Leer la documentación completa**: [README_IMPLEMENTATION.md](README_IMPLEMENTATION.md)
2. **Explorar la API**: http://localhost:8000/api/docs
3. **Ver ejemplos avanzados**: [examples/](examples/)
4. **Configurar Neo4j**: [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)

---

## 🆘 Solución de Problemas

### Error: "Module not found"

```bash
# Asegúrate de estar en el entorno virtual
source venv/bin/activate

# Reinstala dependencias
pip install -r requirements.txt
```

### Error: "Connection refused" (Docker)

```bash
# Verifica que los servicios estén corriendo
docker-compose ps

# Reinicia si es necesario
docker-compose restart
```

### El análisis no funciona

```bash
# Verifica la instalación
python -c "from src.core.risk_calculator import RiskCalculator; print('✅ OK')"
```

---

## 📞 Soporte

- **Email**: ia.mechmind@gmail.com
- **Issues**: https://github.com/mechmind-dwv/Inspector_IA/issues
- **Documentación**: [README_IMPLEMENTATION.md](README_IMPLEMENTATION.md)

---

**🌟 ¡Listo para detectar anomalías!**
