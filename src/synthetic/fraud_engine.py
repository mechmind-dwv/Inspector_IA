"""
Inspector IA - Synthetic Fraud Engine (SFE)
============================================

Implementación de la clase CosmicFraudGenerator para crear universos de datos sintéticos.

Author: Inspector IA Core Team
Version: 2.0
Date: December 2024
"""

import random
from typing import Dict, List, Any
from faker import Faker
from datetime import datetime, timedelta
from pathlib import Path

# Inicializar Faker para datos realistas
fake = Faker('es_ES')


class CosmicFraudGenerator:
    """
    Genera patrones de fraude realistas para entrenamiento y validación
    en un entorno controlado y ético.
    """
    
    def __init__(self, seed: int = 42):
        """Inicializa el generador con una semilla para reproducibilidad."""
        random.seed(seed)
        Faker.seed(seed)
        self.seed = seed
        self.politician_ids = []
        self.company_ids = []
        self.transaction_ids = []
        self.start_date = datetime(2018, 1, 1)
        self.end_date = datetime(2024, 12, 31)

    def _generate_clean_base(self, count: int) -> List[Dict[str, Any]]:
        """Genera una base de datos de políticos y entidades 'limpias'."""
        print(f"Generando {count} casos base limpios...")
        clean_cases = []
        for i in range(count):
            pol_id = f"POL-{i:05d}"
            self.politician_ids.append(pol_id)
            
            case = {
                "id": pol_id,
                "type": "politician",
                "name": fake.name(),
                "age": random.randint(35, 70),
                "party": random.choice(["Partido A", "Partido B", "Partido C"]),
                "financial_data": {
                    "annual_income": random.randint(50000, 150000),
                    "total_assets": random.randint(100000, 1000000),
                    "offshore_accounts": 0,
                    "crypto_wallets": 0,
                },
                "network_data": {
                    "companies_owned": random.randint(0, 2),
                    "relatives_in_politics": random.randint(0, 1),
                    "complex_network_score": 0.0,
                },
                "ground_truth": {"is_fraud": False, "patterns": []}
            }
            clean_cases.append(case)
        return clean_cases

    def _inject_fraud_patterns(self, count: int) -> List[Dict[str, Any]]:
        """Inyecta patrones de fraude en una parte de los casos."""
        print(f"Inyectando {count} patrones de fraude sintético...")
        fraud_cases = []
        patterns = ["CRYPTO_HIDING", "OFFSHORE_LAUNDERING", "GHOST_COMPANY"] # Simplificado
        
        for i in range(count):
            pol_id = f"POL-FRAUD-{i:04d}"
            self.politician_ids.append(pol_id)
            
            pattern = random.choice(patterns)
            
            case = {
                "id": pol_id,
                "type": "politician",
                "name": fake.name(),
                "age": random.randint(40, 75),
                "party": random.choice(["Partido D", "Partido E"]),
                "financial_data": {
                    "annual_income": random.randint(80000, 250000),
                    "total_assets": random.randint(500000, 5000000),
                    "offshore_accounts": 1 if pattern == "OFFSHORE_LAUNDERING" else 0,
                    "crypto_wallets": 1 if pattern == "CRYPTO_HIDING" else 0,
                },
                "network_data": {
                    "companies_owned": random.randint(1, 5),
                    "relatives_in_politics": random.randint(0, 2),
                    "complex_network_score": random.uniform(0.5, 0.9),
                },
                "ground_truth": {"is_fraud": True, "patterns": [pattern]}
            }
            fraud_cases.append(case)
        return fraud_cases

    def _create_complex_networks(self, count: int) -> List[Dict[str, Any]]:
        """Crea redes complejas (nodos y relaciones) para el grafo."""
        print(f"Creando {count} redes complejas...")
        networks = []
        for i in range(count):
            network = {
                "network_id": f"NET-{i:04d}",
                "nodes": [],
                "relationships": []
            }
            
            # Crear nodos (políticos, empresas, personas)
            num_nodes = random.randint(5, 20)
            for j in range(num_nodes):
                node_type = random.choice(["Politician", "Company", "Person"])
                node_id = f"{node_type[:3]}-{fake.uuid4()[:8]}"
                network["nodes"].append({"id": node_id, "type": node_type, "properties": {"name": fake.name() if node_type != "Company" else fake.company()}})
            
            # Crear relaciones
            for _ in range(random.randint(5, 30)):
                source = random.choice(network["nodes"])
                target = random.choice(network["nodes"])
                if source["id"] != target["id"]:
                    rel_type = random.choice(["OWNS", "RELATED_TO", "TRANSACTED_WITH", "WORKS_FOR"])
                    network["relationships"].append({
                        "source": source["id"],
                        "target": target["id"],
                        "type": rel_type,
                        "properties": {"date": fake.date_between(start_date=self.start_date, end_date=self.end_date).isoformat()}
                    })
            networks.append(network)
        return networks

    def _generate_validation_labels(self) -> Dict[str, Any]:
        """Genera etiquetas de verdad fundamental (ground truth) para validación."""
        print("Generando etiquetas de verdad fundamental...")
        ground_truth = {}
        # En un sistema real, esto se generaría a partir de los casos inyectados
        # Aquí, simplemente mapeamos los casos de fraude
        
        # Ejemplo: Mapear los IDs de fraude a sus patrones
        for pol_id in self.politician_ids:
            if "FRAUD" in pol_id:
                ground_truth[pol_id] = {
                    "is_fraud": True,
                    "patterns": ["CRYPTO_HIDING", "OFFSHORE_LAUNDERING"] # Simplificado
                }
            else:
                ground_truth[pol_id] = {"is_fraud": False, "patterns": []}
        
        return ground_truth

    def _create_timeline_sequences(self) -> List[Dict[str, Any]]:
        """Crea secuencias de eventos temporales para análisis."""
        print("Creando secuencias de eventos temporales...")
        timeline_sequences = []
        
        for pol_id in random.sample(self.politician_ids, min(100, len(self.politician_ids))):
            num_events = random.randint(5, 20)
            events = []
            current_date = self.start_date
            
            for _ in range(num_events):
                current_date += timedelta(days=random.randint(10, 100))
                if current_date > self.end_date:
                    break
                
                event_type = random.choice(["Transaction", "Travel", "Company_Registration", "Political_Vote"])
                
                event = {
                    "politician_id": pol_id,
                    "timestamp": current_date.isoformat(),
                    "type": event_type,
                    "details": {
                        "amount": random.randint(1000, 50000) if event_type == "Transaction" else None,
                        "location": fake.city() if event_type == "Travel" else None,
                        "entity": fake.company() if event_type == "Company_Registration" else None
                    }
                }
                events.append(event)
            
            timeline_sequences.append({"politician_id": pol_id, "events": events})
            
        return timeline_sequences

    def generate_universe(self, size: int = 10000) -> Dict[str, Any]:
        """
        Genera el universo de datos sintéticos completo.
        
        Args:
            size: Tamaño total del universo (número de casos base).
        
        Returns:
            Diccionario con los datasets generados.
        """
        
        # Definir proporciones
        clean_count = int(size * 0.7)
        fraud_count = int(size * 0.3)
        network_count = int(size * 0.1) # Redes complejas separadas
        
        print("=====================================================")
        print(f"🌌 Iniciando Generación de Universo Sintético (Tamaño: {size})")
        print("=====================================================")
        
        # 1. Generar casos limpios y fraudulentos
        clean_cases = self._generate_clean_base(clean_count)
        fraud_cases = self._inject_fraud_patterns(fraud_count)
        
        # 2. Combinar casos
        all_cases = clean_cases + fraud_cases
        random.shuffle(all_cases)
        
        # 3. Crear redes complejas
        complex_networks = self._create_complex_networks(network_count)
        
        # 4. Generar etiquetas de verdad fundamental
        ground_truth = self._generate_validation_labels()
        
        # 5. Crear secuencias temporales
        temporal_events = self._create_timeline_sequences()
        
        print("=====================================================")
        print("✅ Generación de Universo Sintético Finalizada")
        print("=====================================================")
        
        return {
            "all_cases": all_cases,
            "clean_cases": clean_cases,
            "fraud_cases": fraud_cases,
            "complex_networks": complex_networks,
            "ground_truth": ground_truth,
            "temporal_events": temporal_events
        }

    def save_universe(self, universe: Dict[str, Any], path: str = "data/synthetic/synthetic_universe.json"):
        """Guarda el universo generado en un archivo JSON."""
        import json
        
        print(f"💾 Guardando universo sintético en {path}...")
        
        # Asegurar que el directorio exista
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(universe, f, ensure_ascii=False, indent=4)
        
        print("✅ Guardado completado.")


if __name__ == '__main__':
    # Ejemplo de uso
    generator = CosmicFraudGenerator(seed=100)
    universe = generator.generate_universe(size=100)
    
    print("\n--- Resumen del Universo ---")
    print(f"Total de casos: {len(universe['all_cases'])}")
    print(f"Casos limpios: {len(universe['clean_cases'])}")
    print(f"Casos de fraude: {len(universe['fraud_cases'])}")
    print(f"Redes complejas: {len(universe['complex_networks'])}")
    print(f"Eventos temporales: {len(universe['temporal_events'])}")
    
    # Guardar el universo
    generator.save_universe(universe)
