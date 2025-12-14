"""
Inspector IA - Synthetic Base Dataset
======================================

Define la estructura base para los datasets sintéticos.

Author: Inspector IA Core Team
Version: 2.0
Date: December 2024
"""

from typing import Dict, List, Any
from dataclasses import dataclass, field

@dataclass
class FinancialData:
    """Datos financieros de un individuo."""
    annual_income: int
    total_assets: int
    offshore_accounts: int = 0
    crypto_wallets: int = 0

@dataclass
class NetworkData:
    """Datos de red y relaciones."""
    companies_owned: int = 0
    relatives_in_politics: int = 0
    complex_network_score: float = 0.0

@dataclass
class GroundTruth:
    """Verdad fundamental para validación."""
    is_fraud: bool
    patterns: List[str] = field(default_factory=list)

@dataclass
class SyntheticCase:
    """Estructura de un caso sintético (político o entidad)."""
    id: str
    type: str
    name: str
    age: int
    party: str
    financial_data: FinancialData
    network_data: NetworkData
    ground_truth: GroundTruth

@dataclass
class SyntheticUniverse:
    """Contenedor para el universo de datos sintéticos."""
    all_cases: List[SyntheticCase]
    clean_cases: List[SyntheticCase]
    fraud_cases: List[SyntheticCase]
    complex_networks: List[Dict[str, Any]]
    ground_truth_map: Dict[str, GroundTruth]
    temporal_events: List[Dict[str, Any]]
