"""
Inspector IA - Pattern Orchestrator
====================================

Orquestador de inyección de patrones de fraude sintético.

Author: Inspector IA Core Team
Version: 2.0
Date: December 2024
"""

from typing import Dict, Any, List
from src.synthetic.injectors.crypto_hiding_injector import CryptoHidingInjector # Asumimos que existe
from src.synthetic.injectors.ring_transaction_injector import RingTransactionInjector
from src.synthetic.injectors.travel_coincidence_injector import TravelCoincidenceInjector
from src.synthetic.injectors.offshore_laundering_injector import OffshoreLaunderingInjector
from src.synthetic.injectors.ghost_company_injector import GhostCompanyInjector
from src.synthetic.injectors.insider_trading_injector import InsiderTradingInjector

class PatternOrchestrator:
    """
    Coordina la inyección de múltiples patrones de fraude en los datos base.
    """
    
    def __init__(self):
        """Inicializa el orquestador con los inyectores disponibles."""
        self.injectors = {
            "CRYPTO_HIDING": CryptoHidingInjector(),
            "RING_TRANSACTIONS": RingTransactionInjector(),
            "TRAVEL_COINCIDENCE": TravelCoincidenceInjector(),
            "OFFSHORE_LAUNDERING": OffshoreLaunderingInjector(),
            "GHOST_COMPANY": GhostCompanyInjector(),
            "INSIDER_TRADING": InsiderTradingInjector(),
            # Aquí se agregarían los demás inyectores
            # ...
        }
        self.available_patterns = list(self.injectors.keys())

    def inject_pattern(self, case: Dict[str, Any], pattern: str) -> Dict[str, Any]:
        """
        Inyecta un patrón específico en un caso sintético.
        
        Args:
            case: El caso base (político, entidad)
            pattern: El patrón a inyectar (e.g., "CRYPTO_HIDING")
            
        Returns:
            El caso modificado con el patrón inyectado.
        """
        if pattern not in self.injectors:
            print(f"⚠️ Advertencia: Inyector para el patrón {pattern} no encontrado.")
            return case
        
        injector = self.injectors[pattern]
        
        # Lógica de inyección
        modified_case = injector.inject(case)
        
        # Actualizar Ground Truth
        if pattern not in modified_case["ground_truth"]["patterns"]:
            modified_case["ground_truth"]["patterns"].append(pattern)
        
        modified_case["ground_truth"]["is_fraud"] = True
        
        return modified_case

    def inject_multiple_patterns(self, case: Dict[str, Any], patterns: List[str]) -> Dict[str, Any]:
        """
        Inyecta múltiples patrones en un solo caso.
        """
        for pattern in patterns:
            case = self.inject_pattern(case, pattern)
        return case

# Ejemplo de uso (simulado)
if __name__ == '__main__':
    orchestrator = PatternOrchestrator()
    
    base_case = {
        "id": "POL-001",
        "type": "politician",
        "name": "Juan Pérez",
        "financial_data": {"crypto_wallets": 0},
        "ground_truth": {"is_fraud": False, "patterns": []}
    }
    
    # Inyección de patrón CRYPTO_HIDING (ejemplo anterior)
    crypto_case = orchestrator.inject_pattern(base_case.copy(), "CRYPTO_HIDING")
    
    # Inyección del nuevo patrón RING_TRANSACTIONS
    ring_case = orchestrator.inject_pattern(base_case.copy(), "RING_TRANSACTIONS")
    
    print("\n--- Caso Base ---")
    print(base_case)
    
    print("\n--- Caso con CRYPTO_HIDING Inyectado ---")
    print(f"Patrones GT: {crypto_case['ground_truth']['patterns']}")
    
    print("\n--- Caso con RING_TRANSACTIONS Inyectado ---")
    print(f"Patrones GT: {ring_case['ground_truth']['patterns']}")
    print(f"Redes Inyectadas: {len(ring_case['complex_networks'])}")
    
    # Mostrar la primera transacción del anillo
    if ring_case['complex_networks']:
        first_transaction = ring_case['complex_networks'][0]['relationships'][0]
        print(f"Primera Transacción: {first_transaction['source_id']} -> {first_transaction['target_id']} ({first_transaction['amount']})")
