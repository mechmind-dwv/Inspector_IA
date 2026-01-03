"""
Inspector IA - OFFSHORE_LAUNDERING Pattern Injector
===================================================

Inyector para el patrón de fraude "Lavado de Dinero Offshore".
Este patrón se caracteriza por la creación de estructuras de propiedad complejas 
a través de jurisdicciones de bajo impuesto y alto secreto.

Author: Inspector IA Core Team
Version: 2.0
Date: December 2024
"""

import random
from typing import Dict, Any, List
from faker import Faker

fake = Faker('es_ES')

class OffshoreLaunderingInjector:
    """
    Inyector para el patrón OFFSHORE_LAUNDERING.
    """
    
    def __init__(self):
        self.pattern_name = "OFFSHORE_LAUNDERING"
        self.offshore_jurisdictions = [
            "Islas Vírgenes Británicas", "Panamá", "Seychelles", "Chipre", 
            "Jersey", "Guernsey", "Belice", "Samoa"
        ]
        self.max_layers = 4 # Máximo de capas de propiedad

    def _generate_shell_company(self, jurisdiction: str, owner_id: str) -> Dict[str, Any]:
        """
        Genera una empresa fantasma en una jurisdicción offshore.
        """
        company_id = f"SHELL-{fake.uuid4()[:8]}"
        return {
            "id": company_id,
            "type": "Shell_Company",
            "name": fake.company() + " Corp.",
            "jurisdiction": jurisdiction,
            "registered_agent": fake.name(),
            "owner_id": owner_id,
            "is_offshore": True,
            "activity_level": "Low"
        }

    def _generate_ownership_chain(self, politician_id: str) -> Dict[str, Any]:
        """
        Genera una cadena de propiedad compleja (capas de empresas fantasma).
        """
        num_layers = random.randint(2, self.max_layers)
        nodes = [{"id": politician_id, "type": "Politician", "name": "Beneficiario Final"}]
        relationships = []
        
        current_owner_id = politician_id
        
        # 1. Crear la cadena de propiedad
        for i in range(num_layers):
            jurisdiction = random.choice(self.offshore_jurisdictions)
            shell_company = self._generate_shell_company(jurisdiction, current_owner_id)
            
            nodes.append(shell_company)
            
            # Relación de propiedad: El dueño actual posee la nueva empresa fantasma
            relationships.append({
                "source_id": current_owner_id,
                "target_id": shell_company["id"],
                "type": "OWNS",
                "ownership_percentage": 100.0,
                "layer": i + 1
            })
            
            # El dueño de la siguiente capa es la empresa fantasma actual (propiedad circular)
            current_owner_id = shell_company["id"]
            
        # 2. (Opcional) Crear propiedad circular (la última empresa posee la primera)
        if random.random() > 0.5:
            relationships.append({
                "source_id": current_owner_id,
                "target_id": nodes[1]["id"], # La primera shell company
                "type": "OWNS",
                "ownership_percentage": random.randint(10, 40),
                "layer": num_layers + 1,
                "is_circular": True
            })
        
        return {
            "nodes": nodes,
            "relationships": relationships,
            "num_layers": num_layers
        }

    def inject(self, case: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inyecta el patrón OFFSHORE_LAUNDERING en el caso.
        
        Args:
            case: El caso base (político, entidad).
            
        Returns:
            El caso modificado.
        """
        
        # 1. Verificar que el caso sea un político
        if case.get("type") != "politician":
            return case
        
        politician_id = case["id"]
        
        # 2. Generar la cadena de propiedad offshore
        ownership_chain = self._generate_ownership_chain(politician_id)
        
        # 3. Inyectar en los datos de red
        if "complex_networks" not in case:
            case["complex_networks"] = []
            
        case["complex_networks"].append({
            "pattern_type": self.pattern_name,
            "description": f"Cadena de propiedad offshore de {ownership_chain['num_layers']} capas.",
            "nodes": ownership_chain["nodes"],
            "relationships": ownership_chain["relationships"]
        })
        
        # 4. Aumentar el score de red y marcar ground truth
        case["network_data"]["complex_network_score"] = min(1.0, case["network_data"]["complex_network_score"] + 0.5)
        case["financial_data"]["offshore_accounts"] = case["financial_data"].get("offshore_accounts", 0) + ownership_chain["num_layers"]
        
        case["ground_truth"]["is_fraud"] = True
        if self.pattern_name not in case["ground_truth"]["patterns"]:
            case["ground_truth"]["patterns"].append(self.pattern_name)
            
        return case

# Ejemplo de uso
if __name__ == '__main__':
    injector = OffshoreLaunderingInjector()
    
    base_case = {
        "id": "POL-003",
        "type": "politician",
        "name": "Carlos Ruiz",
        "financial_data": {"total_assets": 1000000, "offshore_accounts": 0},
        "network_data": {"complex_network_score": 0.1},
        "ground_truth": {"is_fraud": False, "patterns": []}
    }
    
    fraud_case = injector.inject(base_case)
    
    print("\n--- Caso con Lavado Offshore Inyectado ---")
    print(f"ID: {fraud_case['id']}")
    print(f"Score de Red: {fraud_case['network_data']['complex_network_score']:.2f}")
    print(f"Cuentas Offshore: {fraud_case['financial_data']['offshore_accounts']}")
    print(f"Patrones GT: {fraud_case['ground_truth']['patterns']}")
    
    # Mostrar la cadena de propiedad
    chain = fraud_case['complex_networks'][0]
    print(f"Descripción: {chain['description']}")
    print(f"Nodos Creados: {len(chain['nodes']) - 1}")
    print(f"Relación Inicial: {chain['relationships'][0]['source_id']} OWNS {chain['relationships'][0]['target_id']}")
    if 'is_circular' in chain['relationships'][-1]:
        print(f"Relación Circular: {chain['relationships'][-1]['source_id']} OWNS {chain['relationships'][-1]['target_id']}")
