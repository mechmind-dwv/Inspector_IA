"""
Inspector IA - GHOST_COMPANY Pattern Injector
=============================================

Inyector para el patrón de fraude "Empresa Fantasma".
Este patrón se caracteriza por la creación de una entidad con:
1. Mínima o nula actividad operativa real.
2. Máxima obtención de contratos gubernamentales.
3. Vínculo directo o indirecto con el político.

Author: Inspector IA Core Team
Version: 2.0
Date: December 2024
"""

import random
from typing import Dict, Any, List
from faker import Faker

fake = Faker('es_ES')

class GhostCompanyInjector:
    """
    Inyector para el patrón GHOST_COMPANY.
    """
    
    def __init__(self):
        self.pattern_name = "GHOST_COMPANY"
        self.contract_types = [
            "Consultoría Estratégica", "Suministro de Materiales", 
            "Servicios de Mantenimiento", "Desarrollo de Software"
        ]

    def _generate_ghost_company(self, politician_id: str) -> Dict[str, Any]:
        """
        Genera una empresa fantasma con características sospechosas.
        """
        company_id = f"GHOST-{fake.uuid4()[:8]}"
        return {
            "id": company_id,
            "type": "Ghost_Company",
            "name": fake.company() + " S.A.S.",
            "registration_date": fake.date_this_decade().isoformat(),
            "owner_id": politician_id, # Propiedad directa para simplificar
            "employees": random.randint(0, 3), # Baja cantidad de empleados
            "operational_expenses": random.randint(1000, 5000), # Bajos gastos operativos
            "is_ghost": True
        }

    def _generate_government_contracts(self, company_id: str, num_contracts: int) -> List[Dict[str, Any]]:
        """
        Genera múltiples contratos gubernamentales de alto valor.
        """
        contracts = []
        for i in range(num_contracts):
            contract_amount = random.randint(500000, 5000000)
            contracts.append({
                "contract_id": f"GOV-CON-{fake.uuid4()[:8]}",
                "company_id": company_id,
                "type": random.choice(self.contract_types),
                "amount": contract_amount,
                "awarding_entity": fake.company() + " (Gobierno)",
                "date": fake.date_this_year().isoformat(),
                "is_high_value": True,
                "is_suspicious": True
            })
        return contracts

    def inject(self, case: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inyecta el patrón GHOST_COMPANY en el caso.
        
        Args:
            case: El caso base (político, entidad).
            
        Returns:
            El caso modificado.
        """
        
        # 1. Verificar que el caso sea un político
        if case.get("type") != "politician":
            return case
        
        politician_id = case["id"]
        
        # 2. Generar la empresa fantasma
        ghost_company = self._generate_ghost_company(politician_id)
        
        # 3. Generar contratos gubernamentales
        num_contracts = random.randint(3, 7)
        contracts = self._generate_government_contracts(ghost_company["id"], num_contracts)
        
        # 4. Inyectar en los datos de red
        if "complex_networks" not in case:
            case["complex_networks"] = []
            
        # Añadir la empresa fantasma y los contratos a la red
        case["complex_networks"].append({
            "pattern_type": self.pattern_name,
            "description": f"Empresa fantasma '{ghost_company['name']}' con {num_contracts} contratos gubernamentales.",
            "nodes": [ghost_company],
            "relationships": contracts # Los contratos se modelan como relaciones en el grafo
        })
        
        # 5. Aumentar el score de red y marcar ground truth
        case["network_data"]["complex_network_score"] = min(1.0, case["network_data"]["complex_network_score"] + 0.4)
        case["network_data"]["companies_owned"] = case["network_data"].get("companies_owned", 0) + 1
        
        case["ground_truth"]["is_fraud"] = True
        if self.pattern_name not in case["ground_truth"]["patterns"]:
            case["ground_truth"]["patterns"].append(self.pattern_name)
            
        return case

# Ejemplo de uso
if __name__ == '__main__':
    injector = GhostCompanyInjector()
    
    base_case = {
        "id": "POL-004",
        "type": "politician",
        "name": "Roberto Gómez",
        "financial_data": {"total_assets": 800000},
        "network_data": {"complex_network_score": 0.1, "companies_owned": 0},
        "ground_truth": {"is_fraud": False, "patterns": []}
    }
    
    fraud_case = injector.inject(base_case)
    
    print("\n--- Caso con Empresa Fantasma Inyectada ---")
    print(f"ID: {fraud_case['id']}")
    print(f"Score de Red: {fraud_case['network_data']['complex_network_score']:.2f}")
    print(f"Empresas Poseídas: {fraud_case['network_data']['companies_owned']}")
    print(f"Patrones GT: {fraud_case['ground_truth']['patterns']}")
    
    # Mostrar la empresa fantasma y un contrato
    ghost_company = fraud_case['complex_networks'][0]['nodes'][0]
    first_contract = fraud_case['complex_networks'][0]['relationships'][0]
    
    print(f"Empresa Fantasma: {ghost_company['name']} (Empleados: {ghost_company['employees']})")
    print(f"Contrato 1: {first_contract['type']} por {first_contract['amount']} de {first_contract['awarding_entity']}")
