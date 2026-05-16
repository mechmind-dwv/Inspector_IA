"""
Inspector IA - FastAPI Main Application
========================================

API principal para el sistema Inspector IA.
Proporciona endpoints para análisis de riesgo, consultas de grafos,
y gestión de investigaciones periodísticas.

Author: Inspector IA Core Team
Version: 2.0
Date: December 2024
"""

import logging

# Importar módulos internos
import sys
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

sys.path.append("/home/ubuntu/Inspector_IA")

from src.core.anomaly_index import IRACalculator, RiskLevel
from src.core.risk_calculator import RiskCalculator, export_risk_analysis_json

# Configurar logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ==================== INICIALIZACIÓN DE LA APP ====================

app = FastAPI(
    title="Inspector IA API",
    description="API para análisis forense de inteligencia en investigación periodística",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar calculadores
risk_calculator = RiskCalculator()
ira_calculator = IRACalculator()

# ==================== MODELOS PYDANTIC ====================


class PoliticianData(BaseModel):
    """Modelo de datos de un político."""

    id: str = Field(..., description="ID único del político")
    name: str = Field(..., description="Nombre completo")
    position: str = Field(..., description="Cargo actual")
    party: Optional[str] = Field(None, description="Partido político")
    annual_income: float = Field(..., description="Ingreso anual declarado")
    total_assets: float = Field(..., description="Patrimonio total declarado")
    years_in_office: int = Field(..., description="Años en el cargo")
    asset_changes: Optional[List[Dict]] = Field(
        default_factory=list, description="Cambios patrimoniales"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "POL-001",
                "name": "Juan Pérez García",
                "position": "Senador",
                "party": "Partido Ejemplo",
                "annual_income": 150000.0,
                "total_assets": 2500000.0,
                "years_in_office": 8,
                "asset_changes": [{"year": 2023, "percentage_increase": 45.0}],
            }
        }


class GraphData(BaseModel):
    """Modelo de datos del grafo de conexiones."""

    offshore_entities: Optional[List[Dict]] = Field(default_factory=list)
    ghost_companies: Optional[List[Dict]] = Field(default_factory=list)
    suspicious_individuals: Optional[List[Dict]] = Field(default_factory=list)
    crypto_wallets: Optional[List[Dict]] = Field(default_factory=list)
    intermediary_layers: Optional[int] = Field(0)
    unique_jurisdictions: Optional[List[str]] = Field(default_factory=list)
    advanced_concealment_techniques: Optional[List[str]] = Field(default_factory=list)
    circular_ownership_structures: Optional[List[Dict]] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "offshore_entities": [
                    {
                        "name": "Offshore Corp Ltd",
                        "jurisdiction": "Panama",
                        "is_shell_company": True,
                    }
                ],
                "ghost_companies": [
                    {"name": "Ghost Services SA", "ghost_risk_score": 0.85, "no_employees": True}
                ],
                "intermediary_layers": 3,
                "unique_jurisdictions": ["Panama", "Islas Caimán", "Suiza"],
            }
        }


class TemporalEvent(BaseModel):
    """Modelo de evento temporal."""

    type: str = Field(..., description="Tipo de evento")
    date: str = Field(..., description="Fecha del evento")
    description: Optional[str] = Field(None, description="Descripción")
    details: Optional[Dict] = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "type": "legislative_financial_correlation",
                "date": "2024-01-15",
                "description": "Voto favorable seguido de transacción",
                "details": {"days_difference": 5, "transaction_amount": 500000.0},
            }
        }


class RiskAnalysisRequest(BaseModel):
    """Solicitud de análisis de riesgo completo."""

    politician_data: PoliticianData
    graph_data: GraphData
    temporal_events: List[TemporalEvent] = Field(default_factory=list)


class RiskAnalysisResponse(BaseModel):
    """Respuesta de análisis de riesgo."""

    success: bool
    politician_id: str
    politician_name: str
    ira_score: float
    risk_level: str
    risk_color: str
    confidence_level: float
    patterns_detected: int
    analysis_timestamp: str
    executive_summary: str
    detailed_report_url: Optional[str] = None


# ==================== ENDPOINTS ====================


@app.get("/")
async def root():
    """Endpoint raíz con información de la API."""
    return {
        "name": "Inspector IA API",
        "version": "2.0.0",
        "status": "operational",
        "documentation": "/api/docs",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/health")
async def health_check():
    """Verificación de salud del sistema."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "operational",
            "risk_calculator": "operational",
            "ira_calculator": "operational",
        },
    }


@app.post("/api/v1/analyze/risk", response_model=RiskAnalysisResponse)
async def analyze_risk(request: RiskAnalysisRequest, background_tasks: BackgroundTasks):
    """
    Realiza un análisis completo de riesgo para un político.

    Este endpoint calcula el IRA (Índice de Riesgo de Anomalía),
    detecta patrones de fraude, y genera un reporte completo.

    Args:
        request: Datos del político, grafo y eventos temporales
        background_tasks: Tareas en segundo plano

    Returns:
        RiskAnalysisResponse con el análisis completo
    """
    try:
        logger.info(f"Iniciando análisis de riesgo para {request.politician_data.name}")

        # Convertir modelos Pydantic a dicts
        politician_dict = request.politician_data.model_dump()
        graph_dict = request.graph_data.model_dump()
        temporal_list = [event.model_dump() for event in request.temporal_events]

        # Realizar análisis completo
        analysis_result = risk_calculator.calculate_comprehensive_risk(
            politician_id=request.politician_data.id,
            politician_data=politician_dict,
            graph_data=graph_dict,
            temporal_events=temporal_list,
        )

        # Guardar reporte en segundo plano
        report_filename = f"reports/risk_analysis_{request.politician_data.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        background_tasks.add_task(export_risk_analysis_json, analysis_result, report_filename)

        # Preparar respuesta
        ira_result = analysis_result["ira_result"]

        response = RiskAnalysisResponse(
            success=True,
            politician_id=request.politician_data.id,
            politician_name=request.politician_data.name,
            ira_score=ira_result["final_score"],
            risk_level=ira_result["risk_level"],
            risk_color=ira_result["risk_color"],
            confidence_level=ira_result["confidence_level"],
            patterns_detected=analysis_result["patterns_detected_count"],
            analysis_timestamp=analysis_result["analysis_timestamp"],
            executive_summary=analysis_result["executive_summary"],
            detailed_report_url=f"/api/v1/reports/{request.politician_data.id}",
        )

        logger.info(
            f"Análisis completado: IRA={ira_result['final_score']:.2f}, Nivel={ira_result['risk_level']}"
        )

        return response

    except Exception as e:
        logger.error(f"Error en análisis de riesgo: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error al realizar análisis de riesgo: {str(e)}"
        )


@app.post("/api/v1/calculate/ira")
async def calculate_ira_only(request: RiskAnalysisRequest):
    """
    Calcula únicamente el IRA sin análisis completo.

    Endpoint más ligero para cálculos rápidos del índice de riesgo.
    """
    try:
        politician_dict = request.politician_data.model_dump()
        graph_dict = request.graph_data.model_dump()
        temporal_list = [event.model_dump() for event in request.temporal_events]

        ira_result = ira_calculator.calculate_ira(
            politician_id=request.politician_data.id,
            politician_data=politician_dict,
            graph_data=graph_dict,
            temporal_events=temporal_list,
        )

        return {
            "success": True,
            "politician_id": request.politician_data.id,
            "ira_score": ira_result.normalized_ira_score,
            "risk_level": ira_result.risk_level.label,
            "risk_color": ira_result.risk_level.color,
            "confidence": ira_result.confidence_level,
            "dimensions": {
                "patrimonial": ira_result.patrimonial_dimension.weighted_score,
                "network": ira_result.network_dimension.weighted_score,
                "temporal": ira_result.temporal_dimension.weighted_score,
            },
            "network_bonus": ira_result.network_bonus,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Error en cálculo de IRA: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error al calcular IRA: {str(e)}")


@app.get("/api/v1/risk-levels")
async def get_risk_levels():
    """
    Obtiene la matriz de interpretación de niveles de riesgo.

    Returns:
        Lista de niveles de riesgo con sus rangos y acciones
    """
    levels = []
    for level in RiskLevel:
        levels.append(
            {
                "name": level.label,
                "min_score": level.min_score,
                "max_score": level.max_score,
                "color": level.color,
                "action": level.action,
            }
        )

    return {"success": True, "risk_levels": levels}


@app.get("/api/v1/fraud-patterns")
async def get_fraud_patterns():
    """
    Obtiene información sobre los patrones de fraude detectables.

    Returns:
        Lista de patrones de fraude con sus características
    """
    patterns = [
        {
            "id": "CRYPTO_HIDING",
            "name": "Ocultamiento Cripto",
            "description": "Uso de criptomonedas para ocultar flujos de fondos",
            "detection_techniques": [
                "Análisis de interacción con mixers",
                "Tracking de privacy coins",
                "Monitoreo de puentes cross-chain",
                "Detección de peeling chains",
            ],
            "max_score_contribution": 50,
        },
        {
            "id": "OFFSHORE_LAUNDERING",
            "name": "Lavado Offshore",
            "description": "Uso de jurisdicciones extranjeras y shell companies",
            "detection_techniques": [
                "Análisis de nominee shareholders",
                "Detección de estructuras circulares",
                "Tracking de jurisdiction hopping",
            ],
            "max_score_contribution": 50,
        },
        {
            "id": "TRAVEL_COINCIDENCE",
            "name": "Coincidencias de Viaje",
            "description": "Correlación temporal-espacial entre viajes y movimientos financieros",
            "detection_techniques": [
                "Análisis de correlación temporal",
                "Identificación de tax havens",
                "Tracking de movimientos financieros post-viaje",
            ],
            "max_score_contribution": 50,
        },
        {
            "id": "GHOST_COMPANY",
            "name": "Empresas Fantasma",
            "description": "Entidades con baja actividad pero altos contratos",
            "detection_techniques": [
                "Análisis de actividad operativa",
                "Verificación de empleados y activos",
                "Análisis de contratos gubernamentales",
            ],
            "max_score_contribution": 50,
        },
        {
            "id": "INSIDER_TRADING",
            "name": "Uso de Información Privilegiada",
            "description": "Explotación de información no pública para ganancia financiera",
            "detection_techniques": [
                "Correlación votos-transacciones",
                "Análisis de timing de adquisiciones",
                "Tracking de comités y legislación",
            ],
            "max_score_contribution": 50,
        },
    ]

    return {"success": True, "patterns": patterns, "total_patterns": len(patterns)}


@app.get("/api/v1/statistics")
async def get_system_statistics():
    """
    Obtiene estadísticas del sistema.

    Returns:
        Estadísticas de uso y análisis realizados
    """
    # En producción, estos datos vendrían de la base de datos
    return {
        "success": True,
        "statistics": {
            "total_analyses": 0,
            "high_risk_cases": 0,
            "patterns_detected_total": 0,
            "average_ira_score": 0.0,
            "system_uptime": "operational",
            "last_analysis": None,
        },
        "timestamp": datetime.now().isoformat(),
    }


# ==================== MANEJO DE ERRORES ====================


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Manejo personalizado de excepciones HTTP."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.detail, "timestamp": datetime.now().isoformat()},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Manejo de excepciones generales."""
    logger.error(f"Error no manejado: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Error interno del servidor",
            "timestamp": datetime.now().isoformat(),
        },
    )


# ==================== STARTUP/SHUTDOWN ====================


@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación."""
    logger.info("🚀 Inspector IA API iniciando...")
    logger.info("✅ Calculadores de riesgo inicializados")
    logger.info("✅ API lista para recibir solicitudes")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento de cierre de la aplicación."""
    logger.info("🛑 Inspector IA API cerrando...")
    logger.info("✅ Limpieza completada")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
