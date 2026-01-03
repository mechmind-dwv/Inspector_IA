"""
Inspector IA - RING_TRANSACTIONS Pattern Injector
==================================================

Inyector para el patrón de fraude "Transacciones en Anillo".
Este patrón se caracteriza por una serie de transacciones que regresan al punto de origen
o a una entidad muy cercana, a menudo a través de múltiples intermediarios.

Author: Inspector IA Core Team
Version: 2.0
Date: December 2024
"""

import random
from typing import Dict, Any, List
from faker import Faker

fake = Faker('es_ES')

class RingTransactionInjector:
    """
    Inyector para el patrón RING_TRANSACTIONS.
    """
    
    def __init__(self):
        self.pattern_name = "RING_TRANSACTIONS"
        self.max_ring_size = 5 # Máximo de intermediarios en el anillo

    def _generate_ring_network(self, politician_id: str, num_intermediaries: int) -> List[Dict[str, Any]]:
        """
        Genera una red de transacciones en anillo.
        
        Args:
            politician_id: ID del político que inicia el anillo.
            num_intermediaries: Número de entidades intermediarias.
            
        Returns:
            Lista de transacciones que forman el anillo.
        """
        
        # 1. Crear las entidades intermediarias
        intermediaries = []
        for i in range(num_intermediaries):
            intermediaries.append({
                "id": f"ENT-{fake.uuid4()[:8]}",
                "type": random.choice(["Company", "Shell_Company", "Person"]),
                "name": fake.company() if i % 2 == 0 else fake.name(),
                "is_ring_entity": True
            })
        
        # 2. Definir el orden del anillo
        ring_order = [politician_id] + [e["id"] for e in intermediaries] + [politician_id]
        
        # 3. Generar las transacciones
        transactions = []
        for i in range(len(ring_order) - 1):
            source_id = ring_order[i]
            target_id = ring_order[i+1]
            
            # La cantidad se mantiene constante o disminuye ligeramente
            amount = random.randint(50000, 200000)
            
            transactions.append({
                "source_id": source_id,
                "target_id": target_id,
                "type": "TRANSFER",
                "amount": amount,
                "date": fake.date_this_year().isoformat(),
                "description": f"Pago por servicios {fake.word()}",
                "is_ring_transaction": True
            })
            
        return transactions, intermediaries

    def inject(self, case: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inyecta el patrón RING_TRANSACTIONS en el caso.
        
        Args:
            case: El caso base (político, entidad).
            
        Returns:
            El caso modificado.
        """
        
        # 1. Verificar que el caso sea un político
        if case.get("type") != "politician":
            return case
        
        politician_id = case["id"]
        
        # 2. Generar la red de anillo
        num_intermediaries = random.randint(2, self.max_ring_size)
        transactions, intermediaries = self._generate_ring_network(politician_id, num_intermediaries)
        
        # 3. Inyectar en los datos de red
        if "complex_networks" not in case:
            case["complex_networks"] = []
        
        ring_network = {
            "network_id": f"RING-{fake.uuid4()[:8]}",
            "description": f"Patrón de Transacciones en Anillo de {num_intermediaries} intermediarios",
            "nodes": [{"id": politician_id, "type": "Politician"}] + intermediaries,
            "relationships": transactions
        }
        
        case["complex_networks"].append(ring_network)
        
        # 4. Aumentar el score de red y marcar ground truth
        case["network_data"]["complex_network_score"] = min(1.0, case["network_data"]["complex_network_score"] + 0.3)
        case["ground_truth"]["is_fraud"] = True
        if self.pattern_name not in case["ground_truth"]["patterns"]:
            case["ground_truth"]["patterns"].append(self.pattern_name)
            
        return case

# Ejemplo de uso
if __name__ == '__main__':
    injector = RingTransactionInjector()
    
    base_case = {
        "id": "POL-001",
        "type": "politician",
        "name": "Juan Pérez",
        "financial_data": {"crypto_wallets": 0},
        "network_data": {"complex_network_score": 0.1},
        "ground_truth": {"is_fraud": False, "patterns": []}
    }
    
    fraud_case = injector.inject(base_case)
    
    print("\n--- Caso con Anillo Inyectado ---")
    print(f"ID: {fraud_case['id']}")
    print(f"Score de Red: {fraud_case['network_data']['complex_network_score']:.2f}")
    print(f"Patrones GT: {fraud_case['ground_truth']['patterns']}")
    print(f"Redes Inyectadas: {len(fraud_case['complex_networks'])}")
    
    # Mostrar la primera transacción del anillo
    first_transaction = fraud_case['complex_networks'][0]['relationships'][0]
    print(f"Primera Transacción: {first_transaction['source_id']} -> {first_transaction['target_id']} ({first_transaction['amount']})")
