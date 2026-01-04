"""
Inspector IA - INSIDER_TRADING Pattern Injector
===============================================

Inyector para el patrón de fraude "Uso de Información Privilegiada".
Este patrón se caracteriza por la acumulación o venta de activos financieros 
(acciones, bonos, criptomonedas) justo antes de un evento legislativo o regulatorio 
que afecta significativamente el valor de esos activos.

Author: Inspector IA Core Team
Version: 2.0
Date: December 2024
"""

import random
from typing import Dict, Any, List
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('es_ES')

class InsiderTradingInjector:
    """
    Inyector para el patrón INSIDER_TRADING.
    """
    
    def __init__(self):
        self.pattern_name = "INSIDER_TRADING"
        self.asset_types = ["Acciones", "Bonos", "Criptomonedas", "Bienes Raíces"]
        self.event_types = ["Votación Legislativa", "Anuncio Regulatorio", "Aprobación de Contrato"]

    def _generate_suspicious_trade(self, politician_id: str) -> Dict[str, Any]:
        """
        Genera un evento de trading sospechoso.
        """
        
        # 1. Generar fecha del evento legislativo/regulatorio
        event_date = fake.date_time_between(start_date=datetime(2023, 1, 1), end_date=datetime(2024, 12, 31))
        
        # 2. Generar la transacción sospechosa (ocurre antes del evento)
        # La transacción ocurre entre 1 y 6 semanas antes del evento
        trade_date = event_date - timedelta(weeks=random.randint(1, 6))
        
        asset = random.choice(self.asset_types)
        trade_type = random.choice(["Compra Agresiva", "Venta Masiva"])
        trade_amount = random.randint(200000, 5000000) # Monto muy significativo
        
        # 3. Generar el evento legislativo
        legislative_event = {
            "type": random.choice(self.event_types),
            "timestamp": event_date.isoformat(),
            "details": {
                "asset_affected": asset,
                "impact": "Positivo" if trade_type == "Compra Agresiva" else "Negativo",
                "is_public_knowledge": False, # En el momento del trade
                "politician_involvement": "Votante Clave"
            }
        }
        
        # 4. Generar la transacción
        transaction_event = {
            "type": "FINANCIAL_TRADE",
            "politician_id": politician_id,
            "timestamp": trade_date.isoformat(),
            "details": {
                "asset": asset,
                "trade_type": trade_type,
                "amount": trade_amount,
                "description": f"{trade_type} de {asset} antes de {legislative_event['type']}",
                "is_suspicious_timing": True
            }
        }
        
        return {
            "legislative_event": legislative_event,
            "transaction": transaction_event,
            "time_difference_days": (event_date - trade_date).days
        }

    def inject(self, case: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inyecta el patrón INSIDER_TRADING en el caso.
        
        Args:
            case: El caso base (político, entidad).
            
        Returns:
            El caso modificado.
        """
        
        # 1. Verificar que el caso sea un político
        if case.get("type") != "politician":
            return case
        
        politician_id = case["id"]
        
        # 2. Generar entre 1 y 2 eventos de trading
        num_events = random.randint(1, 2)
        
        if "temporal_events" not in case:
            case["temporal_events"] = []
            
        for _ in range(num_events):
            suspicious_event = self._generate_suspicious_trade(politician_id)
            
            # Añadir los eventos a la línea de tiempo del caso
            case["temporal_events"].append(suspicious_event["legislative_event"])
            case["temporal_events"].append(suspicious_event["transaction"])
            
            # Marcar la coincidencia como un hallazgo de riesgo patrimonial/temporal
            if "complex_networks" not in case:
                case["complex_networks"] = []
                
            case["complex_networks"].append({
                "pattern_type": self.pattern_name,
                "description": f"Trade sospechoso de {suspicious_event['transaction']['details']['asset']} {suspicious_event['time_difference_days']} días antes de {suspicious_event['legislative_event']['type']}.",
                "trade_timestamp": suspicious_event["transaction"]["timestamp"],
                "event_timestamp": suspicious_event["legislative_event"]["timestamp"],
            })
        
        # 3. Aumentar el score de riesgo patrimonial y marcar ground truth
        # Asumimos que el caso tiene un campo para riesgo patrimonial
        if "patrimonial_risk_score" not in case["financial_data"]:
            case["financial_data"]["patrimonial_risk_score"] = 0.0
            
        case["financial_data"]["patrimonial_risk_score"] = min(1.0, case["financial_data"]["patrimonial_risk_score"] + 0.5)
        case["ground_truth"]["is_fraud"] = True
        if self.pattern_name not in case["ground_truth"]["patterns"]:
            case["ground_truth"]["patterns"].append(self.pattern_name)
            
        return case

# Ejemplo de uso
if __name__ == '__main__':
    injector = InsiderTradingInjector()
    
    base_case = {
        "id": "POL-005",
        "type": "politician",
        "name": "Elena Torres",
        "financial_data": {"total_assets": 1500000, "patrimonial_risk_score": 0.1},
        "network_data": {"complex_network_score": 0.1},
        "ground_truth": {"is_fraud": False, "patterns": []}
    }
    
    fraud_case = injector.inject(base_case)
    
    print("\n--- Caso con Insider Trading Inyectado ---")
    print(f"ID: {fraud_case['id']}")
    print(f"Score de Riesgo Patrimonial: {fraud_case['financial_data']['patrimonial_risk_score']:.2f}")
    print(f"Patrones GT: {fraud_case['ground_truth']['patterns']}")
    print(f"Eventos Temporales Inyectados: {len(fraud_case['temporal_events'])}")
    
    # Mostrar la primera coincidencia
    first_coincidence = fraud_case['complex_networks'][0]
    print(f"Primera Coincidencia: {first_coincidence['description']}")
    print(f"Trade: {first_coincidence['trade_timestamp']}")
    print(f"Evento: {first_coincidence['event_timestamp']}")
