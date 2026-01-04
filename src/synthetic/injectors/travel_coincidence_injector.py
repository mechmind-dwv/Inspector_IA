"""
Inspector IA - TRAVEL_COINCIDENCE Pattern Injector
==================================================

Inyector para el patrón de fraude "Coincidencia de Viajes".
Este patrón se caracteriza por la correlación temporal-espacial entre viajes a 
jurisdicciones de alto riesgo (paraísos fiscales) y movimientos financieros 
significativos.

Author: Inspector IA Core Team
Version: 2.0
Date: December 2024
"""

import random
from typing import Dict, Any, List
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('es_ES')

class TravelCoincidenceInjector:
    """
    Inyector para el patrón TRAVEL_COINCIDENCE.
    """
    
    def __init__(self):
        self.pattern_name = "TRAVEL_COINCIDENCE"
        self.tax_havens = [
            "Islas Caimán", "Panamá", "Suiza", "Singapur", "Luxemburgo", 
            "Mónaco", "Bermudas", "Hong Kong", "Dubái"
        ]
        self.start_date = datetime(2020, 1, 1)
        self.end_date = datetime(2024, 12, 31)

    def _generate_suspicious_event(self, politician_id: str) -> Dict[str, Any]:
        """
        Genera un evento sospechoso: un viaje a un paraíso fiscal y una transacción.
        """
        
        # 1. Generar fecha del evento (últimos 4 años)
        event_date = fake.date_time_between(start_date=self.start_date, end_date=self.end_date)
        
        # 2. Generar viaje a paraíso fiscal
        travel_location = random.choice(self.tax_havens)
        travel_event = {
            "type": "TRAVEL",
            "politician_id": politician_id,
            "timestamp": event_date.isoformat(),
            "details": {
                "location": travel_location,
                "purpose": random.choice(["Reunión de negocios", "Conferencia", "Vacaciones de lujo"]),
                "is_high_risk_jurisdiction": True
            }
        }
        
        # 3. Generar transacción financiera significativa (cercana en el tiempo)
        # La transacción ocurre entre 3 días antes y 3 días después del viaje
        transaction_date = event_date + timedelta(days=random.randint(-3, 3))
        transaction_amount = random.randint(100000, 500000) # Monto significativo
        
        transaction_event = {
            "type": "TRANSACTION",
            "politician_id": politician_id,
            "timestamp": transaction_date.isoformat(),
            "details": {
                "amount": transaction_amount,
                "currency": random.choice(["USD", "EUR"]),
                "recipient": fake.company(),
                "description": random.choice(["Consultoría", "Inversión", "Compra de activos"]),
                "is_significant_movement": True
            }
        }
        
        return {
            "travel": travel_event,
            "transaction": transaction_event,
            "coincidence_score": 0.85 # Alto score de coincidencia temporal-espacial
        }

    def inject(self, case: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inyecta el patrón TRAVEL_COINCIDENCE en el caso.
        
        Args:
            case: El caso base (político, entidad).
            
        Returns:
            El caso modificado.
        """
        
        # 1. Verificar que el caso sea un político
        if case.get("type") != "politician":
            return case
        
        politician_id = case["id"]
        
        # 2. Generar entre 1 y 3 eventos de coincidencia
        num_coincidences = random.randint(1, 3)
        
        if "temporal_events" not in case:
            case["temporal_events"] = []
            
        for _ in range(num_coincidences):
            suspicious_event = self._generate_suspicious_event(politician_id)
            
            # Añadir los eventos a la línea de tiempo del caso
            case["temporal_events"].append(suspicious_event["travel"])
            case["temporal_events"].append(suspicious_event["transaction"])
            
            # Marcar la coincidencia como un hallazgo de red/temporal
            if "complex_networks" not in case:
                case["complex_networks"] = []
                
            case["complex_networks"].append({
                "pattern_type": self.pattern_name,
                "description": f"Coincidencia de viaje a {suspicious_event['travel']['details']['location']} y transacción significativa.",
                "timestamp_travel": suspicious_event["travel"]["timestamp"],
                "timestamp_transaction": suspicious_event["transaction"]["timestamp"],
                "coincidence_score": suspicious_event["coincidence_score"]
            })
        
        # 3. Aumentar el score de riesgo temporal y marcar ground truth
        # Asumimos que el caso tiene un campo para riesgo temporal
        if "temporal_risk_score" not in case["network_data"]:
            case["network_data"]["temporal_risk_score"] = 0.0
            
        case["network_data"]["temporal_risk_score"] = min(1.0, case["network_data"]["temporal_risk_score"] + 0.4)
        case["ground_truth"]["is_fraud"] = True
        if self.pattern_name not in case["ground_truth"]["patterns"]:
            case["ground_truth"]["patterns"].append(self.pattern_name)
            
        return case

# Ejemplo de uso
if __name__ == '__main__':
    injector = TravelCoincidenceInjector()
    
    base_case = {
        "id": "POL-002",
        "type": "politician",
        "name": "María López",
        "financial_data": {"total_assets": 500000},
        "network_data": {"complex_network_score": 0.2, "temporal_risk_score": 0.1},
        "ground_truth": {"is_fraud": False, "patterns": []}
    }
    
    fraud_case = injector.inject(base_case)
    
    print("\n--- Caso con Coincidencia de Viajes Inyectada ---")
    print(f"ID: {fraud_case['id']}")
    print(f"Score de Riesgo Temporal: {fraud_case['network_data']['temporal_risk_score']:.2f}")
    print(f"Patrones GT: {fraud_case['ground_truth']['patterns']}")
    print(f"Eventos Temporales Inyectados: {len(fraud_case['temporal_events'])}")
    
    # Mostrar la primera coincidencia
    first_coincidence = fraud_case['complex_networks'][0]
    print(f"Primera Coincidencia: {first_coincidence['description']}")
    print(f"Viaje: {first_coincidence['timestamp_travel']}")
    print(f"Transacción: {first_coincidence['timestamp_transaction']}")
