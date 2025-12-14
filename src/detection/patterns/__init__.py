"""
Inspector IA - Detection Patterns Module
=========================================

Este módulo contiene los 5 patrones de fraude detectables:
- CRYPTO_HIDING
- OFFSHORE_LAUNDERING
- TRAVEL_COINCIDENCE
- GHOST_COMPANY
- INSIDER_TRADING

Author: Inspector IA Core Team
Version: 2.0
Date: December 2024
"""

from .crypto_hiding import CryptoHidingDetector
from .offshore_laundering import OffshoreLaunderingDetector
from .travel_coincidence import TravelCoincidenceDetector
from .ghost_company import GhostCompanyDetector
from .insider_trading import InsiderTradingDetector

__all__ = [
    'CryptoHidingDetector',
    'OffshoreLaunderingDetector',
    'TravelCoincidenceDetector',
    'GhostCompanyDetector',
    'InsiderTradingDetector',
]
