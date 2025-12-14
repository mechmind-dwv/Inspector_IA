"""
Inspector IA - Risk Calculator Implementation
==============================================

Implementación del sistema completo de cálculo de riesgo
integrando todas las dimensiones y patrones de fraude.

Author: Inspector IA Core Team
Version: 2.0
Date: December 2024
"""

from typing import Dict, List, Optional
from datetime import datetime
import json

from .anomaly_index import (
    IRACalculator,
    IRAResult,
    RiskLevel,
    format_ira_report
)


class CompletenessAnalyzer:
    """
    Analiza la completitud de datos disponibles para un político.
    
    Evalúa qué porcentaje de información necesaria está disponible
    en cada dimensión del análisis.
    """
    
    @staticmethod
    def analyze_patrimonial_completeness(politician_data: Dict) -> float:
        """
        Analiza completitud de datos patrimoniales.
        
        Args:
            politician_data: Diccionario con datos del político
        
        Returns:
            Score de completitud (0.0 - 1.0)
        """
        required_fields = {
            'annual_income': 0.25,
            'total_assets': 0.25,
            'asset_changes': 0.20,
            'declared_properties': 0.15,
            'financial_disclosures': 0.15
        }
        
        completeness = 0.0
        for field, weight in required_fields.items():
            if field in politician_data and politician_data[field]:
                completeness += weight
        
        return completeness
    
    @staticmethod
    def analyze_network_completeness(graph_data: Dict) -> float:
        """
        Analiza completitud de datos de red.
        
        Args:
            graph_data: Diccionario con datos del grafo
        
        Returns:
            Score de completitud (0.0 - 1.0)
        """
        required_fields = {
            'direct_connections': 0.20,
            'company_relationships': 0.25,
            'offshore_entities': 0.20,
            'family_network': 0.15,
            'contract_paths': 0.20
        }
        
        completeness = 0.0
        for field, weight in required_fields.items():
            if field in graph_data and graph_data[field]:
                completeness += weight
        
        return completeness
    
    @staticmethod
    def analyze_temporal_completeness(temporal_events: List[Dict]) -> float:
        """
        Analiza completitud de datos temporales.
        
        Args:
            temporal_events: Lista de eventos temporales
        
        Returns:
            Score de completitud (0.0 - 1.0)
        """
        if not temporal_events:
            return 0.0
        
        # Evaluar tipos de eventos disponibles
        event_types = set()
        for event in temporal_events:
            event_types.add(event.get('type', 'unknown'))
        
        required_types = {
            'legislative_action',
            'financial_transaction',
            'travel_event',
            'meeting_attendance',
            'asset_declaration'
        }
        
        # Completitud basada en variedad de tipos de eventos
        type_completeness = len(event_types & required_types) / len(required_types)
        
        # Completitud basada en cantidad de eventos
        quantity_completeness = min(1.0, len(temporal_events) / 20)
        
        # Promedio ponderado
        return (type_completeness * 0.6) + (quantity_completeness * 0.4)


class FraudPatternDetector:
    """
    Detecta patrones específicos de fraude en los datos.
    
    Implementa la detección de los 5 patrones principales:
    - CRYPTO_HIDING
    - OFFSHORE_LAUNDERING
    - TRAVEL_COINCIDENCE
    - GHOST_COMPANY
    - INSIDER_TRADING
    """
    
    @staticmethod
    def detect_crypto_hiding(
        politician_data: Dict,
        graph_data: Dict
    ) -> Dict:
        """
        Detecta patrón CRYPTO_HIDING.
        
        Busca:
        - Wallets cripto conectadas
        - Uso de mixers
        - Conversiones a privacy coins
        - Patrones de peeling chain
        
        Returns:
            Dict con detección y score
        """
        crypto_indicators = []
        risk_score = 0.0
        
        crypto_wallets = graph_data.get('crypto_wallets', [])
        
        for wallet in crypto_wallets:
            # Detectar uso de mixers
            if wallet.get('mixer_interactions', 0) > 0:
                risk_score += 15
                crypto_indicators.append({
                    'type': 'mixer_usage',
                    'description': f"Wallet {wallet['address'][:10]}... interactuó con mixers",
                    'severity': 'high'
                })
            
            # Detectar privacy coins
            if wallet.get('privacy_coin_holdings', False):
                risk_score += 12
                crypto_indicators.append({
                    'type': 'privacy_coin',
                    'description': f"Tenencia de criptomonedas de privacidad",
                    'severity': 'high'
                })
            
            # Detectar cross-chain
            if wallet.get('cross_chain_transactions', 0) > 2:
                risk_score += 10
                crypto_indicators.append({
                    'type': 'cross_chain',
                    'description': f"Múltiples transacciones cross-chain detectadas",
                    'severity': 'medium'
                })
            
            # Detectar structured transactions
            if wallet.get('structured_pattern_detected', False):
                risk_score += 18
                crypto_indicators.append({
                    'type': 'structured_transactions',
                    'description': f"Patrón de transacciones estructuradas detectado",
                    'severity': 'critical'
                })
        
        return {
            'pattern_detected': len(crypto_indicators) > 0,
            'pattern_name': 'CRYPTO_HIDING',
            'risk_score': min(50, risk_score),
            'indicators': crypto_indicators,
            'confidence': 0.8 if len(crypto_indicators) > 2 else 0.5
        }
    
    @staticmethod
    def detect_offshore_laundering(
        politician_data: Dict,
        graph_data: Dict
    ) -> Dict:
        """
        Detecta patrón OFFSHORE_LAUNDERING.
        
        Busca:
        - Entidades offshore conectadas
        - Shell companies
        - Nominee shareholders
        - Circular ownership
        
        Returns:
            Dict con detección y score
        """
        offshore_indicators = []
        risk_score = 0.0
        
        offshore_entities = graph_data.get('offshore_entities', [])
        
        for entity in offshore_entities:
            # Detectar shell companies
            if entity.get('is_shell_company', False):
                risk_score += 20
                offshore_indicators.append({
                    'type': 'shell_company',
                    'description': f"Conexión a shell company: {entity['name']}",
                    'severity': 'critical',
                    'jurisdiction': entity.get('jurisdiction', 'Unknown')
                })
            
            # Detectar nominee shareholders
            if entity.get('has_nominee_shareholders', False):
                risk_score += 15
                offshore_indicators.append({
                    'type': 'nominee_shareholders',
                    'description': f"Uso de nominee shareholders en {entity['name']}",
                    'severity': 'high'
                })
            
            # Detectar jurisdiction hopping
            if entity.get('jurisdiction_changes', 0) > 1:
                risk_score += 12
                offshore_indicators.append({
                    'type': 'jurisdiction_hopping',
                    'description': f"Múltiples cambios de jurisdicción detectados",
                    'severity': 'high'
                })
        
        # Detectar circular ownership
        circular_structures = graph_data.get('circular_ownership_structures', [])
        if circular_structures:
            risk_score += 25
            offshore_indicators.append({
                'type': 'circular_ownership',
                'description': f"{len(circular_structures)} estructuras de propiedad circular detectadas",
                'severity': 'critical'
            })
        
        return {
            'pattern_detected': len(offshore_indicators) > 0,
            'pattern_name': 'OFFSHORE_LAUNDERING',
            'risk_score': min(50, risk_score),
            'indicators': offshore_indicators,
            'confidence': 0.85 if len(offshore_indicators) > 2 else 0.6
        }
    
    @staticmethod
    def detect_travel_coincidence(
        politician_data: Dict,
        temporal_events: List[Dict]
    ) -> Dict:
        """
        Detecta patrón TRAVEL_COINCIDENCE.
        
        Busca correlaciones entre:
        - Viajes a tax havens
        - Movimientos financieros subsecuentes
        
        Returns:
            Dict con detección y score
        """
        travel_indicators = []
        risk_score = 0.0
        
        travel_correlations = []
        for event in temporal_events:
            if event.get('type') == 'travel_financial_correlation':
                travel_correlations.append(event)
        
        for correlation in travel_correlations:
            days_diff = abs(correlation.get('days_difference', 999))
            destination = correlation.get('destination', 'Unknown')
            is_tax_haven = correlation.get('is_tax_haven', False)
            
            if days_diff < 30:
                # Score más alto para tax havens
                base_score = 20 if is_tax_haven else 12
                time_factor = (30 - days_diff) / 30
                correlation_score = base_score * time_factor
                
                risk_score += correlation_score
                
                travel_indicators.append({
                    'type': 'travel_transaction_correlation',
                    'description': f"Transacción {days_diff} días después de viaje a {destination}",
                    'severity': 'critical' if is_tax_haven else 'high',
                    'details': correlation
                })
        
        return {
            'pattern_detected': len(travel_indicators) > 0,
            'pattern_name': 'TRAVEL_COINCIDENCE',
            'risk_score': min(50, risk_score),
            'indicators': travel_indicators,
            'confidence': 0.75 if len(travel_indicators) > 1 else 0.5
        }
    
    @staticmethod
    def detect_ghost_company(
        politician_data: Dict,
        graph_data: Dict
    ) -> Dict:
        """
        Detecta patrón GHOST_COMPANY.
        
        Busca empresas con:
        - Baja actividad operativa
        - Altos contratos gubernamentales
        - Sin empleados o activos significativos
        
        Returns:
            Dict con detección y score
        """
        ghost_indicators = []
        risk_score = 0.0
        
        ghost_companies = graph_data.get('ghost_companies', [])
        
        for company in ghost_companies:
            ghost_score = company.get('ghost_risk_score', 0.0)
            
            if ghost_score > 0.6:
                risk_score += 18
                
                characteristics = []
                if company.get('no_employees', False):
                    characteristics.append("sin empleados registrados")
                if company.get('no_physical_office', False):
                    characteristics.append("sin oficina física")
                if company.get('high_government_contracts', False):
                    characteristics.append("altos contratos gubernamentales")
                
                ghost_indicators.append({
                    'type': 'ghost_company',
                    'description': f"Empresa fantasma: {company['name']} ({', '.join(characteristics)})",
                    'severity': 'critical',
                    'ghost_score': ghost_score,
                    'details': company
                })
        
        return {
            'pattern_detected': len(ghost_indicators) > 0,
            'pattern_name': 'GHOST_COMPANY',
            'risk_score': min(50, risk_score),
            'indicators': ghost_indicators,
            'confidence': 0.9 if len(ghost_indicators) > 1 else 0.7
        }
    
    @staticmethod
    def detect_insider_trading(
        politician_data: Dict,
        temporal_events: List[Dict]
    ) -> Dict:
        """
        Detecta patrón INSIDER_TRADING.
        
        Busca correlaciones entre:
        - Votos legislativos
        - Adquisiciones de activos
        - Información privilegiada
        
        Returns:
            Dict con detección y score
        """
        insider_indicators = []
        risk_score = 0.0
        
        legislative_correlations = []
        for event in temporal_events:
            if event.get('type') == 'legislative_financial_correlation':
                legislative_correlations.append(event)
        
        for correlation in legislative_correlations:
            days_diff = abs(correlation.get('days_difference', 999))
            
            if days_diff < 60:  # Dentro de 60 días
                # Score más alto para correlaciones más cercanas
                time_factor = (60 - days_diff) / 60
                correlation_score = 25 * time_factor
                
                risk_score += correlation_score
                
                insider_indicators.append({
                    'type': 'legislative_financial_correlation',
                    'description': f"Movimiento financiero {days_diff} días después de acción legislativa",
                    'severity': 'critical' if days_diff < 14 else 'high',
                    'details': correlation
                })
        
        return {
            'pattern_detected': len(insider_indicators) > 0,
            'pattern_name': 'INSIDER_TRADING',
            'risk_score': min(50, risk_score),
            'indicators': insider_indicators,
            'confidence': 0.8 if len(insider_indicators) > 1 else 0.6
        }


class RiskCalculator:
    """
    Calculador principal de riesgo que integra todas las dimensiones
    y patrones de fraude.
    """
    
    def __init__(self):
        """Inicializa el calculador de riesgo."""
        self.ira_calculator = IRACalculator()
        self.completeness_analyzer = CompletenessAnalyzer()
        self.pattern_detector = FraudPatternDetector()
    
    def calculate_comprehensive_risk(
        self,
        politician_id: str,
        politician_data: Dict,
        graph_data: Dict,
        temporal_events: List[Dict]
    ) -> Dict:
        """
        Calcula el riesgo completo integrando todas las dimensiones.
        
        Args:
            politician_id: ID único del político
            politician_data: Datos patrimoniales y personales
            graph_data: Datos del grafo de conexiones
            temporal_events: Eventos temporales correlacionados
        
        Returns:
            Dict con análisis completo de riesgo
        """
        # 1. Analizar completitud de datos
        completeness_scores = {
            'patrimonial': self.completeness_analyzer.analyze_patrimonial_completeness(politician_data),
            'network': self.completeness_analyzer.analyze_network_completeness(graph_data),
            'temporal': self.completeness_analyzer.analyze_temporal_completeness(temporal_events)
        }
        
        # 2. Calcular IRA
        ira_result = self.ira_calculator.calculate_ira(
            politician_id=politician_id,
            politician_data=politician_data,
            graph_data=graph_data,
            temporal_events=temporal_events,
            completeness_scores=completeness_scores
        )
        
        # 3. Detectar patrones específicos de fraude
        fraud_patterns = {
            'crypto_hiding': self.pattern_detector.detect_crypto_hiding(
                politician_data, graph_data
            ),
            'offshore_laundering': self.pattern_detector.detect_offshore_laundering(
                politician_data, graph_data
            ),
            'travel_coincidence': self.pattern_detector.detect_travel_coincidence(
                politician_data, temporal_events
            ),
            'ghost_company': self.pattern_detector.detect_ghost_company(
                politician_data, graph_data
            ),
            'insider_trading': self.pattern_detector.detect_insider_trading(
                politician_data, temporal_events
            )
        }
        
        # 4. Calcular score agregado de patrones
        patterns_detected = [p for p in fraud_patterns.values() if p['pattern_detected']]
        total_pattern_score = sum(p['risk_score'] for p in patterns_detected)
        
        # 5. Compilar resultado completo
        comprehensive_result = {
            'politician_id': politician_id,
            'politician_name': politician_data.get('name', 'Unknown'),
            'analysis_timestamp': datetime.now().isoformat(),
            
            # IRA Score
            'ira_result': self._serialize_ira_result(ira_result),
            
            # Patrones de fraude
            'fraud_patterns': fraud_patterns,
            'patterns_detected_count': len(patterns_detected),
            'total_pattern_score': total_pattern_score,
            
            # Completitud
            'data_completeness': completeness_scores,
            'overall_completeness': ira_result.data_completeness_overall,
            
            # Resumen ejecutivo
            'executive_summary': self._generate_executive_summary(
                ira_result, patterns_detected
            ),
            
            # Reporte formateado
            'formatted_report': format_ira_report(ira_result)
        }
        
        return comprehensive_result
    
    def _serialize_ira_result(self, ira_result: IRAResult) -> Dict:
        """Serializa el resultado IRA a diccionario."""
        return {
            'final_score': ira_result.normalized_ira_score,
            'risk_level': ira_result.risk_level.label,
            'risk_color': ira_result.risk_level.color,
            'recommended_action': ira_result.risk_level.action,
            'confidence_level': ira_result.confidence_level,
            'dimensions': {
                'patrimonial': {
                    'score': ira_result.patrimonial_dimension.raw_score,
                    'weight': ira_result.patrimonial_dimension.weight,
                    'weighted_score': ira_result.patrimonial_dimension.weighted_score,
                    'indicators_count': len(ira_result.patrimonial_dimension.indicators)
                },
                'network': {
                    'score': ira_result.network_dimension.raw_score,
                    'weight': ira_result.network_dimension.weight,
                    'weighted_score': ira_result.network_dimension.weighted_score,
                    'indicators_count': len(ira_result.network_dimension.indicators)
                },
                'temporal': {
                    'score': ira_result.temporal_dimension.raw_score,
                    'weight': ira_result.temporal_dimension.weight,
                    'weighted_score': ira_result.temporal_dimension.weighted_score,
                    'indicators_count': len(ira_result.temporal_dimension.indicators)
                }
            },
            'network_bonus': ira_result.network_bonus,
            'key_risk_factors': ira_result.key_risk_factors,
            'recommendations': ira_result.recommendations
        }
    
    def _generate_executive_summary(
        self,
        ira_result: IRAResult,
        patterns_detected: List[Dict]
    ) -> str:
        """Genera un resumen ejecutivo del análisis."""
        summary = f"""
## Resumen Ejecutivo - {ira_result.politician_name}

**Índice de Riesgo de Anomalía (IRA):** {ira_result.normalized_ira_score:.1f}/100  
**Nivel de Riesgo:** {ira_result.risk_level.color} {ira_result.risk_level.label}  
**Confianza del Análisis:** {ira_result.confidence_level*100:.1f}%

### Patrones de Fraude Detectados
"""
        
        if patterns_detected:
            summary += f"\nSe detectaron **{len(patterns_detected)}** patrones sospechosos:\n\n"
            for pattern in patterns_detected:
                summary += f"- **{pattern['pattern_name']}** (Score: {pattern['risk_score']:.1f}, Confianza: {pattern['confidence']*100:.0f}%)\n"
        else:
            summary += "\nNo se detectaron patrones específicos de fraude con alta confianza.\n"
        
        summary += f"\n### Principales Factores de Riesgo\n\n"
        for i, factor in enumerate(ira_result.key_risk_factors[:3], 1):
            summary += f"{i}. {factor}\n"
        
        summary += f"\n### Acción Recomendada\n\n**{ira_result.risk_level.action}**\n"
        
        return summary


# ==================== FUNCIONES DE UTILIDAD ====================

def export_risk_analysis_json(analysis_result: Dict, output_path: str):
    """
    Exporta el análisis de riesgo a archivo JSON.
    
    Args:
        analysis_result: Resultado del análisis de riesgo
        output_path: Ruta del archivo de salida
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis_result, f, indent=2, ensure_ascii=False, default=str)


def export_risk_analysis_markdown(analysis_result: Dict, output_path: str):
    """
    Exporta el análisis de riesgo a archivo Markdown.
    
    Args:
        analysis_result: Resultado del análisis de riesgo
        output_path: Ruta del archivo de salida
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(analysis_result['formatted_report'])
        f.write("\n\n---\n\n")
        f.write(analysis_result['executive_summary'])
