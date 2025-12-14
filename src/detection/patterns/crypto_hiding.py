"""
Inspector IA - CRYPTO_HIDING Pattern Detector
==============================================

Detecta el patrón de ocultamiento mediante criptomonedas.

Indicadores:
- Uso de mixers/tumblers
- Privacy coins (Monero, Zcash, DASH)
- Transacciones cross-chain
- Patrones estructurados (smurfing)

Author: Inspector IA Core Team
Version: 2.0
Date: December 2024
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class CryptoHidingResult:
    """Resultado de detección de CRYPTO_HIDING."""
    pattern_detected: bool
    risk_score: float
    confidence: float
    indicators: List[Dict]
    details: Dict


class CryptoHidingDetector:
    """
    Detector del patrón CRYPTO_HIDING.
    
    Analiza el uso de técnicas de ocultamiento con criptomonedas.
    """
    
    def __init__(self):
        """Inicializa el detector."""
        self.pattern_name = "CRYPTO_HIDING"
        self.max_score = 50.0
        
        # Pesos de indicadores
        self.weights = {
            'mixer_usage': 15.0,
            'privacy_coins': 12.0,
            'cross_chain': 10.0,
            'structured_patterns': 13.0
        }
    
    def detect(
        self,
        politician_id: str,
        graph_data: Dict,
        completeness: float = 1.0
    ) -> CryptoHidingResult:
        """
        Detecta el patrón CRYPTO_HIDING.
        
        Args:
            politician_id: ID del político
            graph_data: Datos del grafo
            completeness: Completitud de datos (0-1)
        
        Returns:
            CryptoHidingResult con la detección
        """
        indicators = []
        total_score = 0.0
        
        # 1. Detectar uso de mixers
        crypto_wallets = graph_data.get('crypto_wallets', [])
        mixer_count = sum(
            w.get('mixer_interactions', 0) 
            for w in crypto_wallets
        )
        
        if mixer_count > 0:
            mixer_score = min(self.weights['mixer_usage'], mixer_count * 5)
            total_score += mixer_score
            indicators.append({
                'type': 'mixer_usage',
                'severity': 'high' if mixer_count > 2 else 'medium',
                'description': f'{mixer_count} interacciones con mixers detectadas',
                'score': mixer_score
            })
        
        # 2. Detectar privacy coins
        privacy_coin_holders = [
            w for w in crypto_wallets 
            if w.get('privacy_coin_holdings', False)
        ]
        
        if privacy_coin_holders:
            privacy_score = self.weights['privacy_coins']
            total_score += privacy_score
            indicators.append({
                'type': 'privacy_coins',
                'severity': 'high',
                'description': f'{len(privacy_coin_holders)} wallets con privacy coins',
                'score': privacy_score
            })
        
        # 3. Detectar transacciones cross-chain
        cross_chain_count = sum(
            w.get('cross_chain_transactions', 0) 
            for w in crypto_wallets
        )
        
        if cross_chain_count > 0:
            cross_chain_score = min(
                self.weights['cross_chain'], 
                cross_chain_count * 2
            )
            total_score += cross_chain_score
            indicators.append({
                'type': 'cross_chain',
                'severity': 'medium',
                'description': f'{cross_chain_count} transacciones cross-chain',
                'score': cross_chain_score
            })
        
        # 4. Detectar patrones estructurados
        structured_patterns = [
            w for w in crypto_wallets 
            if w.get('structured_pattern_detected', False)
        ]
        
        if structured_patterns:
            structured_score = self.weights['structured_patterns']
            total_score += structured_score
            indicators.append({
                'type': 'structured_patterns',
                'severity': 'high',
                'description': 'Patrones de smurfing detectados',
                'score': structured_score
            })
        
        # Normalizar score
        normalized_score = min(total_score, self.max_score)
        
        # Calcular confianza basada en completitud
        confidence = 0.8 * completeness
        
        # Determinar si el patrón está presente
        pattern_detected = normalized_score >= 15.0  # Umbral
        
        return CryptoHidingResult(
            pattern_detected=pattern_detected,
            risk_score=normalized_score,
            confidence=confidence,
            indicators=indicators,
            details={
                'mixer_interactions': mixer_count,
                'privacy_coin_wallets': len(privacy_coin_holders),
                'cross_chain_transactions': cross_chain_count,
                'structured_patterns': len(structured_patterns),
                'total_crypto_wallets': len(crypto_wallets)
            }
        )
    
    def get_explanation(self, result: CryptoHidingResult) -> str:
        """
        Genera explicación legible del resultado.
        
        Args:
            result: Resultado de detección
        
        Returns:
            Explicación en texto
        """
        if not result.pattern_detected:
            return "No se detectaron indicadores significativos de CRYPTO_HIDING."
        
        explanation = f"**Patrón CRYPTO_HIDING detectado** (Score: {result.risk_score:.1f}/50)\n\n"
        explanation += "Indicadores encontrados:\n"
        
        for indicator in result.indicators:
            severity_emoji = {
                'high': '🔴',
                'medium': '🟠',
                'low': '🟡'
            }.get(indicator['severity'], '⚪')
            
            explanation += f"- {severity_emoji} {indicator['description']}\n"
        
        return explanation
