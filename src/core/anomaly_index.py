"""
Inspector IA - Anomaly Risk Index (IRA) Calculator
===================================================

Implementación completa del Índice de Riesgo de Anomalía (IRA)
con ponderación dinámica basada en completitud de datos.

Author: Inspector IA Core Team
Version: 2.0
Date: December 2024
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum
import numpy as np


class RiskLevel(Enum):
    """Niveles de riesgo según el IRA."""
    COSMIC_BACKGROUND = ("Cosmic Background", 0, 20, "🟢", "Routine Monitoring")
    NEBULAR_SUSPICION = ("Nebular Suspicion", 21, 50, "🟡", "Deep Dive Analysis")
    STELLAR_ANOMALY = ("Stellar Anomaly", 51, 70, "🟠", "Priority Investigation")
    SUPERNOVA_ALERT = ("Supernova Alert", 71, 85, "🔴", "Publication Consideration")
    BLACK_HOLE_CRITICAL = ("Black Hole Critical", 86, 100, "⚫", "Urgent Investigation")
    
    def __init__(self, label, min_score, max_score, color, action):
        self.label = label
        self.min_score = min_score
        self.max_score = max_score
        self.color = color
        self.action = action
    
    @classmethod
    def from_score(cls, score: float) -> 'RiskLevel':
        """Determina el nivel de riesgo basado en el score IRA."""
        for level in cls:
            if level.min_score <= score <= level.max_score:
                return level
        return cls.BLACK_HOLE_CRITICAL  # Por defecto si excede 100


@dataclass
class DimensionScore:
    """Score de una dimensión individual del IRA."""
    dimension_name: str
    raw_score: float  # 0-100
    weight: float  # 0-1
    weighted_score: float  # raw_score * weight
    completeness: float  # 0-1
    indicators: List[Dict]  # Indicadores que contribuyen al score
    explanation: str


@dataclass
class IRAResult:
    """Resultado completo del cálculo de IRA."""
    politician_id: str
    politician_name: str
    
    # Scores por dimensión
    patrimonial_dimension: DimensionScore
    network_dimension: DimensionScore
    temporal_dimension: DimensionScore
    
    # Bonus de red
    network_bonus: float  # 0-30
    network_bonus_explanation: str
    
    # Score final
    final_ira_score: float  # 0-130 (100 base + 30 bonus)
    normalized_ira_score: float  # 0-100 normalizado
    risk_level: RiskLevel
    
    # Metadata
    calculation_timestamp: datetime
    data_completeness_overall: float
    weights_used: Dict[str, float]
    confidence_level: float  # 0-1 basado en completitud
    
    # Explicaciones
    key_risk_factors: List[str]
    recommendations: List[str]


class DynamicWeightCalculator:
    """
    Calculador de pesos dinámicos basado en completitud de datos.
    
    Ajusta los pesos de las dimensiones según la disponibilidad y calidad
    de los datos para cada político específico.
    """
    
    # Pesos base según documentación
    BASE_WEIGHTS = {
        'patrimonial': 0.30,
        'network': 0.40,
        'temporal': 0.30
    }
    
    # Umbral mínimo de completitud para peso completo
    COMPLETENESS_THRESHOLD = 0.7
    
    def __init__(self, completeness_threshold: float = 0.7):
        """
        Inicializa el calculador de pesos dinámicos.
        
        Args:
            completeness_threshold: Umbral de completitud (0-1)
        """
        self.threshold = completeness_threshold
    
    def calculate_dynamic_weights(
        self,
        completeness_scores: Dict[str, float]
    ) -> Dict[str, any]:
        """
        Calcula pesos ajustados basados en completitud de datos.
        
        Args:
            completeness_scores: Dict con completitud por dimensión
                {
                    'patrimonial': 0.85,
                    'network': 0.60,
                    'temporal': 0.75
                }
        
        Returns:
            Dict con pesos ajustados y explicaciones
        """
        adjusted_weights = {}
        adjustments = {}
        
        for dimension, base_weight in self.BASE_WEIGHTS.items():
            completeness = completeness_scores.get(dimension, 0.0)
            
            # Ajustar peso si completitud está bajo el umbral
            if completeness < self.threshold:
                adjustment_factor = completeness / self.threshold
                adjusted_weights[dimension] = base_weight * adjustment_factor
                adjustments[dimension] = f"Reducido {(1-adjustment_factor)*100:.1f}% por datos incompletos"
            else:
                adjusted_weights[dimension] = base_weight
                adjustments[dimension] = "Peso completo (datos suficientes)"
        
        # Normalizar para que sumen 1.0
        total = sum(adjusted_weights.values())
        if total > 0:
            normalized_weights = {k: v/total for k, v in adjusted_weights.items()}
        else:
            # Fallback a pesos base si no hay datos
            normalized_weights = self.BASE_WEIGHTS.copy()
        
        return {
            'weights': normalized_weights,
            'completeness_scores': completeness_scores,
            'adjustments': adjustments,
            'overall_completeness': np.mean(list(completeness_scores.values()))
        }


class PatrimonialDimensionCalculator:
    """Calcula el score de la dimensión patrimonial."""
    
    def calculate(
        self,
        politician_data: Dict,
        completeness: float
    ) -> DimensionScore:
        """
        Calcula score patrimonial basado en:
        - Riqueza inexplicada
        - Discrepancias activo-ingreso
        - Cambios súbitos en patrimonio declarado
        
        Args:
            politician_data: Datos del político
            completeness: Completitud de datos (0-1)
        
        Returns:
            DimensionScore con el cálculo completo
        """
        indicators = []
        total_score = 0.0
        
        # 1. Análisis de riqueza inexplicada
        declared_income = politician_data.get('annual_income', 0)
        declared_assets = politician_data.get('total_assets', 0)
        years_in_office = politician_data.get('years_in_office', 1)
        
        expected_max_assets = declared_income * years_in_office * 1.5  # Factor conservador
        
        if declared_assets > expected_max_assets:
            unexplained_ratio = declared_assets / expected_max_assets
            unexplained_score = min(40, (unexplained_ratio - 1) * 40)
            total_score += unexplained_score
            indicators.append({
                'type': 'unexplained_wealth',
                'score': unexplained_score,
                'description': f"Patrimonio {unexplained_ratio:.1f}x superior al esperado",
                'severity': 'high' if unexplained_score > 25 else 'medium'
            })
        
        # 2. Discrepancias activo-ingreso
        asset_income_ratio = declared_assets / max(declared_income, 1)
        if asset_income_ratio > 10:  # Más de 10 años de ingreso en activos
            discrepancy_score = min(30, (asset_income_ratio - 10) * 3)
            total_score += discrepancy_score
            indicators.append({
                'type': 'asset_income_discrepancy',
                'score': discrepancy_score,
                'description': f"Ratio activos/ingreso: {asset_income_ratio:.1f}x",
                'severity': 'high' if discrepancy_score > 20 else 'medium'
            })
        
        # 3. Cambios súbitos en patrimonio
        asset_changes = politician_data.get('asset_changes', [])
        for change in asset_changes:
            if change.get('percentage_increase', 0) > 50:  # Aumento >50% en un año
                sudden_change_score = min(30, change['percentage_increase'] / 2)
                total_score += sudden_change_score
                indicators.append({
                    'type': 'sudden_asset_increase',
                    'score': sudden_change_score,
                    'description': f"Aumento patrimonial de {change['percentage_increase']:.1f}% en {change['year']}",
                    'severity': 'critical' if sudden_change_score > 20 else 'high'
                })
        
        # Normalizar a 0-100
        raw_score = min(100, total_score)
        
        # Generar explicación
        explanation = self._generate_explanation(indicators, raw_score)
        
        return DimensionScore(
            dimension_name="Patrimonial",
            raw_score=raw_score,
            weight=0.0,  # Se asignará después
            weighted_score=0.0,  # Se calculará después
            completeness=completeness,
            indicators=indicators,
            explanation=explanation
        )
    
    def _generate_explanation(self, indicators: List[Dict], score: float) -> str:
        """Genera explicación en lenguaje natural."""
        if score < 20:
            return "Patrimonio declarado consistente con ingresos conocidos."
        elif score < 50:
            return f"Detectadas {len(indicators)} señales de alerta patrimonial que requieren análisis adicional."
        else:
            return f"Múltiples indicadores críticos de discrepancias patrimoniales ({len(indicators)} señales)."


class NetworkDimensionCalculator:
    """Calcula el score de la dimensión de redes."""
    
    def calculate(
        self,
        politician_id: str,
        graph_data: Dict,
        completeness: float
    ) -> DimensionScore:
        """
        Calcula score de redes basado en:
        - Conexiones a entidades offshore
        - Empresas fantasma en la red
        - Individuos con historial financiero sospechoso
        
        Args:
            politician_id: ID del político
            graph_data: Datos del grafo de conexiones
            completeness: Completitud de datos (0-1)
        
        Returns:
            DimensionScore con el cálculo completo
        """
        indicators = []
        total_score = 0.0
        
        # 1. Conexiones offshore
        offshore_connections = graph_data.get('offshore_entities', [])
        if offshore_connections:
            offshore_score = min(40, len(offshore_connections) * 10)
            total_score += offshore_score
            indicators.append({
                'type': 'offshore_connections',
                'score': offshore_score,
                'description': f"{len(offshore_connections)} conexiones a entidades offshore",
                'severity': 'critical' if len(offshore_connections) > 3 else 'high',
                'entities': [e['name'] for e in offshore_connections[:5]]
            })
        
        # 2. Empresas fantasma
        ghost_companies = graph_data.get('ghost_companies', [])
        if ghost_companies:
            ghost_score = min(35, len(ghost_companies) * 12)
            total_score += ghost_score
            indicators.append({
                'type': 'ghost_companies',
                'score': ghost_score,
                'description': f"{len(ghost_companies)} empresas con indicadores de baja actividad",
                'severity': 'critical' if len(ghost_companies) > 2 else 'high',
                'companies': [c['name'] for c in ghost_companies[:5]]
            })
        
        # 3. Conexiones sospechosas
        suspicious_connections = graph_data.get('suspicious_individuals', [])
        if suspicious_connections:
            suspicious_score = min(25, len(suspicious_connections) * 8)
            total_score += suspicious_score
            indicators.append({
                'type': 'suspicious_connections',
                'score': suspicious_score,
                'description': f"{len(suspicious_connections)} conexiones a individuos con historial sospechoso",
                'severity': 'high' if len(suspicious_connections) > 2 else 'medium'
            })
        
        # Normalizar a 0-100
        raw_score = min(100, total_score)
        
        # Generar explicación
        explanation = self._generate_explanation(indicators, raw_score)
        
        return DimensionScore(
            dimension_name="Network",
            raw_score=raw_score,
            weight=0.0,
            weighted_score=0.0,
            completeness=completeness,
            indicators=indicators,
            explanation=explanation
        )
    
    def _generate_explanation(self, indicators: List[Dict], score: float) -> str:
        """Genera explicación en lenguaje natural."""
        if score < 20:
            return "Red de conexiones sin señales de alerta significativas."
        elif score < 50:
            return f"Red presenta {len(indicators)} patrones que requieren investigación adicional."
        else:
            return f"Red altamente compleja con múltiples señales de riesgo ({len(indicators)} indicadores críticos)."


class TemporalDimensionCalculator:
    """Calcula el score de la dimensión temporal."""
    
    def calculate(
        self,
        politician_data: Dict,
        temporal_events: List[Dict],
        completeness: float
    ) -> DimensionScore:
        """
        Calcula score temporal basado en:
        - Correlaciones entre acciones legislativas y movimientos financieros
        - Coincidencias entre viajes y transacciones
        
        Args:
            politician_data: Datos del político
            temporal_events: Lista de eventos temporales
            completeness: Completitud de datos (0-1)
        
        Returns:
            DimensionScore con el cálculo completo
        """
        indicators = []
        total_score = 0.0
        
        # Convertir lista a dict si es necesario
        if isinstance(temporal_events, list):
            # Agrupar eventos por tipo
            events_by_type = {
                'legislative_financial_correlations': [],
                'travel_transaction_correlations': [],
                'suspicious_timing_patterns': []
            }
            for event in temporal_events:
                event_type = event.get('type', '')
                if 'legislative' in event_type:
                    events_by_type['legislative_financial_correlations'].append(event)
                elif 'travel' in event_type:
                    events_by_type['travel_transaction_correlations'].append(event)
                else:
                    events_by_type['suspicious_timing_patterns'].append(event)
            temporal_events = events_by_type
        
        # 1. Correlaciones legislativas-financieras
        legislative_correlations = temporal_events.get('legislative_financial_correlations', [])
        for corr in legislative_correlations:
            days_diff = abs(corr.get('days_difference', 999))
            if days_diff < 30:  # Dentro de 30 días
                correlation_score = min(35, (30 - days_diff) * 1.5)
                total_score += correlation_score
                indicators.append({
                    'type': 'legislative_financial_correlation',
                    'score': correlation_score,
                    'description': f"Movimiento financiero {days_diff} días después de voto legislativo",
                    'severity': 'critical' if days_diff < 7 else 'high',
                    'details': corr
                })
        
        # 2. Correlaciones viaje-transacción
        travel_correlations = temporal_events.get('travel_transaction_correlations', [])
        for corr in travel_correlations:
            days_diff = abs(corr.get('days_difference', 999))
            if days_diff < 15:  # Dentro de 15 días
                travel_score = min(30, (15 - days_diff) * 2.5)
                total_score += travel_score
                indicators.append({
                    'type': 'travel_transaction_correlation',
                    'score': travel_score,
                    'description': f"Transacción {days_diff} días después de viaje a {corr.get('destination', 'desconocido')}",
                    'severity': 'high' if corr.get('is_tax_haven') else 'medium',
                    'details': corr
                })
        
        # 3. Patrones de timing sospechosos
        timing_patterns = temporal_events.get('suspicious_timing_patterns', [])
        for pattern in timing_patterns:
            pattern_score = pattern.get('risk_score', 0)
            total_score += pattern_score
            indicators.append({
                'type': 'suspicious_timing_pattern',
                'score': pattern_score,
                'description': pattern.get('description', 'Patrón temporal sospechoso'),
                'severity': pattern.get('severity', 'medium'),
                'details': pattern
            })
        
        # Normalizar a 0-100
        raw_score = min(100, total_score)
        
        # Generar explicación
        explanation = self._generate_explanation(indicators, raw_score)
        
        return DimensionScore(
            dimension_name="Temporal",
            raw_score=raw_score,
            weight=0.0,
            weighted_score=0.0,
            completeness=completeness,
            indicators=indicators,
            explanation=explanation
        )
    
    def _generate_explanation(self, indicators: List[Dict], score: float) -> str:
        """Genera explicación en lenguaje natural."""
        if score < 20:
            return "No se detectaron correlaciones temporales significativas."
        elif score < 50:
            return f"Detectadas {len(indicators)} correlaciones temporales que requieren análisis."
        else:
            return f"Múltiples correlaciones temporales críticas ({len(indicators)} patrones sospechosos)."


class NetworkBonusCalculator:
    """Calcula el bonus por complejidad de red (0-30 puntos)."""
    
    def calculate(self, graph_data: Dict) -> Tuple[float, str]:
        """
        Calcula bonus basado en:
        - Número de capas intermediarias
        - Diversidad de jurisdicciones
        - Técnicas avanzadas de ocultamiento
        
        Args:
            graph_data: Datos del grafo de conexiones
        
        Returns:
            Tuple (bonus_score, explanation)
        """
        bonus = 0.0
        factors = []
        
        # 1. Capas intermediarias (0-10 puntos)
        intermediary_layers = graph_data.get('intermediary_layers', 0)
        if intermediary_layers > 0:
            layer_bonus = min(10, intermediary_layers * 3)
            bonus += layer_bonus
            factors.append(f"{intermediary_layers} capas intermediarias (+{layer_bonus:.1f})")
        
        # 2. Diversidad jurisdiccional (0-10 puntos)
        jurisdictions = graph_data.get('unique_jurisdictions', [])
        if len(jurisdictions) > 2:
            jurisdiction_bonus = min(10, (len(jurisdictions) - 2) * 2.5)
            bonus += jurisdiction_bonus
            factors.append(f"{len(jurisdictions)} jurisdicciones diferentes (+{jurisdiction_bonus:.1f})")
        
        # 3. Técnicas avanzadas (0-10 puntos)
        advanced_techniques = graph_data.get('advanced_concealment_techniques', [])
        if advanced_techniques:
            technique_bonus = min(10, len(advanced_techniques) * 3.5)
            bonus += technique_bonus
            factors.append(f"{len(advanced_techniques)} técnicas avanzadas de ocultamiento (+{technique_bonus:.1f})")
        
        # Limitar a máximo 30
        bonus = min(30, bonus)
        
        explanation = "Bonus de complejidad de red: " + ", ".join(factors) if factors else "Sin bonus de complejidad"
        
        return bonus, explanation


class IRACalculator:
    """
    Calculador principal del Índice de Riesgo de Anomalía (IRA).
    
    Implementa la fórmula completa con ponderación dinámica:
    IRA = Σ(W_i × S_i) + B_network
    """
    
    def __init__(self):
        """Inicializa el calculador de IRA."""
        self.weight_calculator = DynamicWeightCalculator()
        self.patrimonial_calc = PatrimonialDimensionCalculator()
        self.network_calc = NetworkDimensionCalculator()
        self.temporal_calc = TemporalDimensionCalculator()
        self.bonus_calc = NetworkBonusCalculator()
    
    def calculate_ira(
        self,
        politician_id: str,
        politician_data: Dict,
        graph_data: Dict,
        temporal_events: List[Dict],
        completeness_scores: Optional[Dict[str, float]] = None
    ) -> IRAResult:
        """
        Calcula el IRA completo para un político.
        
        Args:
            politician_id: ID único del político
            politician_data: Datos patrimoniales y personales
            graph_data: Datos del grafo de conexiones
            temporal_events: Eventos temporales correlacionados
            completeness_scores: Scores de completitud por dimensión (opcional)
        
        Returns:
            IRAResult con el cálculo completo y explicaciones
        """
        # 1. Calcular completitud si no se proporciona
        if completeness_scores is None:
            completeness_scores = self._estimate_completeness(
                politician_data, graph_data, temporal_events
            )
        
        # 2. Calcular pesos dinámicos
        weight_info = self.weight_calculator.calculate_dynamic_weights(completeness_scores)
        weights = weight_info['weights']
        
        # 3. Calcular scores por dimensión
        patrimonial_dim = self.patrimonial_calc.calculate(
            politician_data,
            completeness_scores['patrimonial']
        )
        patrimonial_dim.weight = weights['patrimonial']
        patrimonial_dim.weighted_score = patrimonial_dim.raw_score * patrimonial_dim.weight
        
        network_dim = self.network_calc.calculate(
            politician_id,
            graph_data,
            completeness_scores['network']
        )
        network_dim.weight = weights['network']
        network_dim.weighted_score = network_dim.raw_score * network_dim.weight
        
        temporal_dim = self.temporal_calc.calculate(
            politician_data,
            temporal_events,
            completeness_scores['temporal']
        )
        temporal_dim.weight = weights['temporal']
        temporal_dim.weighted_score = temporal_dim.raw_score * temporal_dim.weight
        
        # 4. Calcular bonus de red
        network_bonus, bonus_explanation = self.bonus_calc.calculate(graph_data)
        
        # 5. Calcular IRA final
        base_ira = (
            patrimonial_dim.weighted_score +
            network_dim.weighted_score +
            temporal_dim.weighted_score
        )
        final_ira = base_ira + network_bonus
        
        # Normalizar a escala 0-100 (el bonus puede llevar hasta 130)
        normalized_ira = min(100, (final_ira / 130) * 100)
        
        # 6. Determinar nivel de riesgo
        risk_level = RiskLevel.from_score(normalized_ira)
        
        # 7. Extraer factores clave de riesgo
        key_factors = self._extract_key_risk_factors(
            patrimonial_dim, network_dim, temporal_dim, network_bonus
        )
        
        # 8. Generar recomendaciones
        recommendations = self._generate_recommendations(risk_level, key_factors)
        
        # 9. Calcular nivel de confianza
        confidence = weight_info['overall_completeness']
        
        return IRAResult(
            politician_id=politician_id,
            politician_name=politician_data.get('name', 'Unknown'),
            patrimonial_dimension=patrimonial_dim,
            network_dimension=network_dim,
            temporal_dimension=temporal_dim,
            network_bonus=network_bonus,
            network_bonus_explanation=bonus_explanation,
            final_ira_score=final_ira,
            normalized_ira_score=normalized_ira,
            risk_level=risk_level,
            calculation_timestamp=datetime.now(),
            data_completeness_overall=confidence,
            weights_used=weights,
            confidence_level=confidence,
            key_risk_factors=key_factors,
            recommendations=recommendations
        )
    
    def _estimate_completeness(
        self,
        politician_data: Dict,
        graph_data: Dict,
        temporal_events: List[Dict]
    ) -> Dict[str, float]:
        """Estima la completitud de datos si no se proporciona."""
        # Heurística simple basada en campos presentes
        patrimonial_fields = ['annual_income', 'total_assets', 'asset_changes']
        patrimonial_completeness = sum(
            1 for f in patrimonial_fields if politician_data.get(f)
        ) / len(patrimonial_fields)
        
        network_fields = ['offshore_entities', 'ghost_companies', 'suspicious_individuals']
        network_completeness = sum(
            1 for f in network_fields if graph_data.get(f)
        ) / len(network_fields)
        
        temporal_completeness = 1.0 if temporal_events else 0.3
        
        return {
            'patrimonial': patrimonial_completeness,
            'network': network_completeness,
            'temporal': temporal_completeness
        }
    
    def _extract_key_risk_factors(
        self,
        patrimonial: DimensionScore,
        network: DimensionScore,
        temporal: DimensionScore,
        bonus: float
    ) -> List[str]:
        """Extrae los factores de riesgo más importantes."""
        factors = []
        
        # Ordenar indicadores por score
        all_indicators = (
            patrimonial.indicators +
            network.indicators +
            temporal.indicators
        )
        all_indicators.sort(key=lambda x: x['score'], reverse=True)
        
        # Tomar top 5
        for indicator in all_indicators[:5]:
            factors.append(indicator['description'])
        
        if bonus > 10:
            factors.append(f"Red de alta complejidad (+{bonus:.1f} puntos de bonus)")
        
        return factors
    
    def _generate_recommendations(
        self,
        risk_level: RiskLevel,
        key_factors: List[str]
    ) -> List[str]:
        """Genera recomendaciones basadas en el nivel de riesgo."""
        recommendations = []
        
        if risk_level == RiskLevel.COSMIC_BACKGROUND:
            recommendations.append("Mantener monitoreo rutinario de declaraciones patrimoniales")
            recommendations.append("Revisar actualizaciones trimestrales")
        
        elif risk_level == RiskLevel.NEBULAR_SUSPICION:
            recommendations.append("Realizar análisis profundo de las conexiones identificadas")
            recommendations.append("Solicitar información adicional sobre transacciones específicas")
            recommendations.append("Verificar fuentes de ingresos declaradas")
        
        elif risk_level == RiskLevel.STELLAR_ANOMALY:
            recommendations.append("Priorizar para investigación periodística detallada")
            recommendations.append("Cruzar información con bases de datos internacionales")
            recommendations.append("Analizar documentos corporativos de entidades conectadas")
            recommendations.append("Considerar solicitudes de información pública adicionales")
        
        elif risk_level == RiskLevel.SUPERNOVA_ALERT:
            recommendations.append("URGENTE: Investigación periodística prioritaria")
            recommendations.append("Coordinar con equipo legal antes de publicación")
            recommendations.append("Verificar todos los hallazgos con fuentes múltiples")
            recommendations.append("Preparar documentación de respaldo exhaustiva")
            recommendations.append("Considerar colaboración con medios internacionales")
        
        elif risk_level == RiskLevel.BLACK_HOLE_CRITICAL:
            recommendations.append("CRÍTICO: Investigación inmediata requerida")
            recommendations.append("Activar protocolo de seguridad para periodistas")
            recommendations.append("Coordinar con expertos legales y forenses")
            recommendations.append("Asegurar todas las evidencias digitales")
            recommendations.append("Considerar notificación a autoridades competentes")
            recommendations.append("Preparar estrategia de publicación coordinada")
        
        return recommendations


# ==================== FUNCIONES DE UTILIDAD ====================

def format_ira_report(result: IRAResult) -> str:
    """
    Formatea el resultado del IRA en un reporte legible.
    
    Args:
        result: Resultado del cálculo de IRA
    
    Returns:
        String con el reporte formateado en Markdown
    """
    report = f"""
# Reporte de Análisis de Riesgo - {result.politician_name}

**ID:** {result.politician_id}  
**Fecha de Análisis:** {result.calculation_timestamp.strftime('%Y-%m-%d %H:%M:%S')}  
**Nivel de Confianza:** {result.confidence_level*100:.1f}%

---

## 📊 Índice de Riesgo de Anomalía (IRA)

**Score Final:** {result.normalized_ira_score:.2f} / 100  
**Nivel de Riesgo:** {result.risk_level.color} {result.risk_level.label}  
**Acción Recomendada:** {result.risk_level.action}

---

## 🔍 Análisis por Dimensiones

### 1. Dimensión Patrimonial
- **Score:** {result.patrimonial_dimension.raw_score:.2f} / 100
- **Peso:** {result.patrimonial_dimension.weight:.2%}
- **Contribución al IRA:** {result.patrimonial_dimension.weighted_score:.2f}
- **Completitud de Datos:** {result.patrimonial_dimension.completeness:.2%}

{result.patrimonial_dimension.explanation}

**Indicadores Detectados:**
"""
    
    for ind in result.patrimonial_dimension.indicators:
        report += f"- [{ind['severity'].upper()}] {ind['description']} (Score: {ind['score']:.1f})\n"
    
    report += f"""
### 2. Dimensión de Redes
- **Score:** {result.network_dimension.raw_score:.2f} / 100
- **Peso:** {result.network_dimension.weight:.2%}
- **Contribución al IRA:** {result.network_dimension.weighted_score:.2f}
- **Completitud de Datos:** {result.network_dimension.completeness:.2%}

{result.network_dimension.explanation}

**Indicadores Detectados:**
"""
    
    for ind in result.network_dimension.indicators:
        report += f"- [{ind['severity'].upper()}] {ind['description']} (Score: {ind['score']:.1f})\n"
    
    report += f"""
### 3. Dimensión Temporal
- **Score:** {result.temporal_dimension.raw_score:.2f} / 100
- **Peso:** {result.temporal_dimension.weight:.2%}
- **Contribución al IRA:** {result.temporal_dimension.weighted_score:.2f}
- **Completitud de Datos:** {result.temporal_dimension.completeness:.2%}

{result.temporal_dimension.explanation}

**Indicadores Detectados:**
"""
    
    for ind in result.temporal_dimension.indicators:
        report += f"- [{ind['severity'].upper()}] {ind['description']} (Score: {ind['score']:.1f})\n"
    
    report += f"""
### 4. Bonus de Complejidad de Red
- **Bonus:** +{result.network_bonus:.2f} puntos
- {result.network_bonus_explanation}

---

## ⚠️ Factores Clave de Riesgo

"""
    
    for i, factor in enumerate(result.key_risk_factors, 1):
        report += f"{i}. {factor}\n"
    
    report += "\n---\n\n## 📋 Recomendaciones\n\n"
    
    for i, rec in enumerate(result.recommendations, 1):
        report += f"{i}. {rec}\n"
    
    report += """
---

## ⚖️ Disclaimer Legal

Este análisis identifica **anomalías estadísticas** basadas en datos públicos disponibles. 
La presencia de anomalías **NO implica actividad ilícita**. Se requiere investigación 
periodística adicional y verificación por profesionales antes de cualquier publicación.

**Inspector IA es una herramienta de apoyo a la investigación periodística, no un sistema judicial.**
"""
    
    return report
