"""
CRYPTO_HIDING Pattern Injection Engine v2.0
Soporta tres niveles de dificultad con técnicas de evasión crecientemente sofisticadas
"""

from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
import random
import hashlib
from typing import Dict, List, Optional, Tuple, Any
from .mock_blockchain import MockBlockchain
import numpy as np

# ==================== ENUMS Y ESTRUCTURAS DE DATOS ====================

class CryptoEvasionLevel(Enum):
    """Niveles de sofisticación en técnicas de evasión cripto"""
    BASIC = "basic"           # Transferencias directas P2P
    INTERMEDIATE = "intermediate"  # DEX + Wallets en capas  
    ADVANCED = "advanced"     # Mixers + Privacy coins + Obfuscation compleja

class WalletType(Enum):
    """Tipos de wallets para simulación realista"""
    EXCHANGE_HOT = "exchange_hot"      # Wallet vinculada a exchange con KYC
    COLD_STORAGE = "cold_storage"      # Hardware wallet sin conexión
    MIXER_LINKED = "mixer_linked"      # Wallet que interactúa con mixers
    PRIVACY_COIN = "privacy_coin"      # Wallet para Monero/Zcash
    DEX_ONLY = "dex_only"              # Solo para intercambios descentralizados
    BURNER = "burner"                  # Wallet de un solo uso
    MULTISIG = "multisig"              # Wallet con múltiples firmantes

class TransactionPattern(Enum):
    """Patrones típicos de transacciones sospechosas"""
    PEELING_CHAIN = "peeling_chain"        # Grande → múltiples pequeñas
    STRUCTURED = "structured"              # Montos justo bajo límites de reporte
    MIXER_CASCADE = "mixer_cascade"        # Múltiples pasos por mixers
    CROSS_CHAIN_HOP = "cross_chain_hop"    # Saltos entre blockchains
    PRIVACY_COIN_CONVERSION = "privacy_coin_conversion"  # Conversión a XMR/ZEC

@dataclass
class CryptoWallet:
    """Estructura detallada de wallet cripto"""
    address: str
    type: WalletType
    currency: str  # BTC, ETH, XMR, USDT, etc.
    creation_date: datetime
    last_active: datetime
    estimated_balance_fiat: float
    ml_risk_score: float = 0.0  # Puntuación IA de riesgo (0-1)
    
    # Propiedades de riesgo específicas
    known_mixer_interactions: int = 0
    privacy_coin_holdings: bool = False
    cross_chain_transactions: int = 0
    structured_pattern_detected: bool = False
    
    # Conexiones en el grafo
    owner_person_id: Optional[str] = None
    linked_company_id: Optional[str] = None
    
    def to_graph_node(self) -> Dict:
        """Convierte a formato de nodo Neo4j"""
        return {
            "address": self.address,
            "type": self.type.value,
            "currency": self.currency,
            "creation_date": self.creation_date.isoformat(),
            "last_active": self.last_active.isoformat(),
            "estimated_balance_fiat": self.estimated_balance_fiat,
            "ml_risk_score": self.ml_risk_score,
            "risk_flags": self._generate_risk_flags()
        }
    
    def _generate_risk_flags(self) -> List[str]:
        """Genera banderas de riesgo basadas en propiedades"""
        flags = []
        if self.known_mixer_interactions > 0:
            flags.append(f"MIXER_INTERACTIONS_{self.known_mixer_interactions}")
        if self.privacy_coin_holdings:
            flags.append("PRIVACY_COIN_HOLDINGS")
        if self.cross_chain_transactions > 2:
            flags.append("HIGH_CROSS_CHAIN_ACTIVITY")
        if self.structured_pattern_detected:
            flags.append("STRUCTURED_TRANSACTION_PATTERN")
        if self.ml_risk_score > 0.7:
            flags.append("HIGH_ML_RISK_SCORE")
        return flags

@dataclass
class CryptoTransaction:
    """Transacción cripto detallada con metadatos forenses"""
    tx_hash: str
    timestamp: datetime
    from_address: str
    to_address: str
    amount_fiat: float
    amount_crypto: float
    currency: str
    
    # Propiedades críticas para detección
    mixer_used: bool = False
    mixer_service: Optional[str] = None  # Tornado Cash, Wasabi, etc.
    privacy_coin_involved: bool = False
    cross_chain: bool = False
    cross_chain_bridge: Optional[str] = None
    
    # Metadata de evasión
    structured_amount: bool = False  # Monto justo bajo reporting threshold
    peeling_chain_step: Optional[int] = None  # Paso en cadena de peeling
    
    def to_graph_relationship(self) -> Dict:
        """Convierte a formato de relación Neo4j"""
        return {
            "tx_hash": self.tx_hash,
            "timestamp": self.timestamp.isoformat(),
            "amount_fiat": self.amount_fiat,
            "amount_crypto": self.amount_crypto,
            "currency": self.currency,
            "mixer_used": self.mixer_used,
            "mixer_service": self.mixer_service,
            "privacy_coin_involved": self.privacy_coin_involved,
            "cross_chain": self.cross_chain,
            "cross_chain_bridge": self.cross_chain_bridge,
            "structured_amount": self.structured_amount,
            "peeling_chain_step": self.peeling_chain_step
        }

# ==================== MOTOR DE INYECCIÓN PRINCIPAL ====================

class CryptoHidingInjector:
    """
    Motor de inyección de patrones CRYPTO_HIDING con tres niveles de dificultad
    """
    
    # Configuración por nivel de dificultad
    LEVEL_CONFIGS = {
        CryptoEvasionLevel.BASIC: {
            "wallet_layers": 1,
            "max_intermediaries": 1,
            "allow_mixers": False,
            "allow_privacy_coins": False,
            "allow_cross_chain": False,
            "transaction_patterns": [TransactionPattern.PEELING_CHAIN],
            "ira_bonus_range": (5, 10)
        },
        CryptoEvasionLevel.INTERMEDIATE: {
            "wallet_layers": 2,
            "max_intermediaries": 2,
            "allow_mixers": True,
            "allow_privacy_coins": False,
            "allow_cross_chain": True,
            "transaction_patterns": [TransactionPattern.PEELING_CHAIN, 
                                   TransactionPattern.STRUCTURED],
            "ira_bonus_range": (10, 20)
        },
        CryptoEvasionLevel.ADVANCED: {
            "wallet_layers": 3,
            "max_intermediaries": 3,
            "allow_mixers": True,
            "allow_privacy_coins": True,
            "allow_cross_chain": True,
            "transaction_patterns": [TransactionPattern.PEELING_CHAIN,
                                   TransactionPattern.STRUCTURED,
                                   TransactionPattern.MIXER_CASCADE,
                                   TransactionPattern.CROSS_CHAIN_HOP,
                                   TransactionPattern.PRIVACY_COIN_CONVERSION],
            "ira_bonus_range": (20, 30)
        }
    }
    
    # Servicios conocidos para simulación realista
    KNOWN_MIXERS = ["Tornado Cash", "Wasabi Wallet", "Samourai Whirlpool", 
                    "CoinJoin", "CashFusion"]
    CROSS_CHAIN_BRIDGES = ["Polygon Bridge", "Arbitrum Bridge", "Optimism Gateway",
                          "Wormhole", "Multichain", "Synapse"]
    PRIVACY_COINS = ["XMR", "ZEC", "DASH", "GRIN", "BEAM"]
    
    def __init__(self, blockchain_simulator=None):
        self.blockchain = blockchain_simulator or MockBlockchain()
        # Asumimos que CryptoWalletGenerator y CryptoTransactionGenerator existen o los creamos
        self.wallet_generator = self._create_wallet_generator()
        self.transaction_generator = self._create_transaction_generator()
        
    def _create_wallet_generator(self):
        # Clase dummy para evitar NameError
        class DummyWalletGenerator:
            def generate_wallet(self, wallet_type, currency, base_balance, layer_type):
                return CryptoWallet(
                    address=f"WALLET-{random.randint(1000, 9999)}",
                    type=wallet_type,
                    currency=currency,
                    creation_date=datetime.now() - timedelta(days=random.randint(100, 1000)),
                    last_active=datetime.now(),
                    estimated_balance_fiat=base_balance
                )
        return DummyWalletGenerator()

    def _create_transaction_generator(self):
        # Clase dummy para evitar NameError
        class DummyTransactionGenerator:
            def generate_transaction(self, source_wallet, target_wallet, amount, **kwargs):
                return CryptoTransaction(
                    tx_hash=hashlib.sha256(str(random.random()).encode()).hexdigest()[:10],
                    timestamp=datetime.now(),
                    from_address=source_wallet.address,
                    to_address=target_wallet.address,
                    amount_fiat=amount,
                    amount_crypto=amount / 30000 if amount else 0, # Simulación de precio
                    currency=source_wallet.currency
                )
        return DummyTransactionGenerator()
        
    def inject(self, case: Dict[str, Any]) -> Dict[str, Any]:
        """
        Método de inyección simple para compatibilidad con PatternOrchestrator.
        Llama a la lógica compleja con valores por defecto.
        """
        politician = case
        level = CryptoEvasionLevel.INTERMEDIATE
        amount_to_hide = None
        severity = 0.5
        
        config = self.LEVEL_CONFIGS[level]
        
        # 1. Calcular monto a ocultar si no se especifica
        if amount_to_hide is None:
            amount_to_hide = self._calculate_hidden_amount(politician, severity)
        
        # 2. Crear estructura de wallets según nivel
        wallet_structure = self._create_wallet_structure(
            config["wallet_layers"],
            amount_to_hide,
            config
        )
        
        # 3. Conectar al político a través de intermediarios
        connection_path = self._connect_to_politician(
            politician,
            wallet_structure,
            config["max_intermediaries"]
        )
        
        # 4. Generar transacciones con patrones específicos
        transaction_history = self._generate_transaction_history(
            wallet_structure,
            config["transaction_patterns"],
            severity
        )
        
        # 5. Calcular métricas de riesgo específicas
        risk_metrics = self._calculate_crypto_risk_metrics(
            wallet_structure,
            transaction_history,
            level
        )
        
        # 6. Calcular bonificación IRA
        ira_bonus = self._calculate_ira_bonus(
            risk_metrics,
            config["ira_bonus_range"]
        )
        
        # 7. Actualizar el caso original con los resultados de la inyección
        
        # Marcar Ground Truth
        politician["ground_truth"]["is_fraud"] = True
        if "CRYPTO_HIDING" not in politician["ground_truth"]["patterns"]:
            politician["ground_truth"]["patterns"].append("CRYPTO_HIDING")
            
        # Añadir datos de red (simplificado)
        if "complex_networks" not in politician:
            politician["complex_networks"] = []
            
        politician["complex_networks"].append({
            "pattern_type": "CRYPTO_HIDING",
            "evasion_level": level.value,
            "hidden_amount_fiat": amount_to_hide,
            "ira_bonus": ira_bonus,
            "risk_metrics": risk_metrics
        })
        
        # Aumentar el score de red (si existe)
        if "network_data" in politician and "complex_network_score" in politician["network_data"]:
            politician["network_data"]["complex_network_score"] = min(1.0, politician["network_data"]["complex_network_score"] + 0.2)
            
        return politician

    def inject_pattern(self, 
                      politician: Dict,
                      level: CryptoEvasionLevel = CryptoEvasionLevel.INTERMEDIATE,
                      amount_to_hide: Optional[float] = None,
                      severity: float = 0.5) -> Dict:
        """
        Inyecta un patrón CRYPTO_HIDING en un político sintético
        
        Args:
            politician: Político base (limpio)
            level: Nivel de sofisticación de evasión
            amount_to_hide: Monto total a ocultar (None = calcular automático)
            severity: 0.1 (leve) a 1.0 (agresivo)
            
        Returns:
            Dict con estructura completa del patrón inyectado
        """
        config = self.LEVEL_CONFIGS[level]
        
        # 1. Calcular monto a ocultar si no se especifica
        if amount_to_hide is None:
            amount_to_hide = self._calculate_hidden_amount(politician, severity)
        
        # 2. Crear estructura de wallets según nivel
        wallet_structure = self._create_wallet_structure(
            config["wallet_layers"],
            amount_to_hide,
            config
        )
        
        # 3. Conectar al político a través de intermediarios
        connection_path = self._connect_to_politician(
            politician,
            wallet_structure,
            config["max_intermediaries"]
        )
        
        # 4. Generar transacciones con patrones específicos
        transaction_history = self._generate_transaction_history(
            wallet_structure,
            config["transaction_patterns"],
            severity
        )
        
        # 5. Calcular métricas de riesgo específicas
        risk_metrics = self._calculate_crypto_risk_metrics(
            wallet_structure,
            transaction_history,
            level
        )
        
        # 6. Calcular bonificación IRA
        ira_bonus = self._calculate_ira_bonus(
            risk_metrics,
            config["ira_bonus_range"]
        )
        
        return {
            "pattern_type": "CRYPTO_HIDING",
            "evasion_level": level.value,
            "severity": severity,
            "hidden_amount_fiat": amount_to_hide,
            "wallet_structure": wallet_structure,
            "connection_path": connection_path,
            "transaction_history": transaction_history,
            "risk_metrics": risk_metrics,
            "ira_bonus": ira_bonus,
            "detection_heuristics": self._generate_detection_heuristics(level),
            "ground_truth_flags": self._get_ground_truth_flags(wallet_structure, 
                                                              transaction_history),
            "injection_timestamp": datetime.now().isoformat()
        }
    
    def _calculate_hidden_amount(self, politician: Dict, severity: float) -> float:
        """
        Calcula monto realista a ocultar basado en patrimonio del político
        Usa distribución log-normal para simular valores realistas
        """
        # Base: ingreso anual del político
        annual_income = politician.get("annual_income", 100000)
        
        # Severidad afecta el porcentaje del ingreso a ocultar
        # severity=0.1 -> ~5% del ingreso, severity=1.0 -> ~50% del ingreso
        percentage_to_hide = 0.05 + (severity * 0.45)
        
        base_amount = annual_income * percentage_to_hide
        
        # Añadir variación log-normal (common in financial distributions)
        mu = np.log(base_amount)
        sigma = severity * 0.5  # Más severidad = más variación
        log_normal_amount = np.random.lognormal(mu, sigma)
        
        # Redondear a valores típicos de transacciones cripto
        typical_values = [10000, 25000, 50000, 100000, 250000, 500000, 1000000]
        closest = min(typical_values, key=lambda x: abs(x - log_normal_amount))
        
        return float(closest)
    
    def _create_wallet_structure(self, 
                                layers: int,
                                total_amount: float,
                                config: Dict) -> Dict:
        """
        Crea estructura jerárquica de wallets según nivel de sofisticación
        """
        structure = {
            "entry_layer": [],
            "obfuscation_layers": [],
            "exit_layer": [],
            "total_wallets": 0,
            "total_layers": layers
        }
        
        current_amount = total_amount
        
        # Capa 1: Wallets de entrada (conexión a fiat)
        entry_wallets = self._generate_wallet_layer(
            layer_type="entry",
            amount=current_amount * 0.7,  # 70% entra por aquí
            wallet_count=random.randint(1, 2),
            allow_mixers=False,
            allow_privacy_coins=False
        )
        structure["entry_layer"] = entry_wallets
        structure["total_wallets"] += len(entry_wallets)
        
        # Capas de ofuscación (si hay más de 1 capa)
        for layer_idx in range(1, layers):
            layer_config = {
                "wallet_count": random.randint(1, 3),
                "allow_mixers": config["allow_mixers"] and layer_idx > 0,
                "allow_privacy_coins": config["allow_privacy_coins"] and layer_idx >= layers-2,
                "allow_cross_chain": config["allow_cross_chain"] and layer_idx == 1
            }
            
            # Reducir monto por capa (comisiones, splitting)
            layer_amount = current_amount * random.uniform(0.8, 0.95)
            
            wallets = self._generate_wallet_layer(
                layer_type="obfuscation",
                amount=layer_amount,
                wallet_count=layer_config["wallet_count"],
                allow_mixers=layer_config["allow_mixers"],
                allow_privacy_coins=layer_config["allow_privacy_coins"],
                allow_cross_chain=layer_config["allow_cross_chain"]
            )
            
            structure["obfuscation_layers"].append({
                "layer": layer_idx,
                "wallets": wallets,
                "config": layer_config
            })
            structure["total_wallets"] += len(wallets)
            
            current_amount = layer_amount
        
        # Capa final: Wallets de salida (almacenamiento)
        exit_wallets = self._generate_wallet_layer(
            layer_type="exit",
            amount=current_amount,
            wallet_count=1,
            allow_mixers=False,
            allow_privacy_coins=config["allow_privacy_coins"],
            is_cold_storage=True
        )
        structure["exit_layer"] = exit_wallets
        structure["total_wallets"] += len(exit_wallets)
        
        return structure
    
    def _generate_wallet_layer(self,
                             layer_type: str,
                             amount: float,
                             wallet_count: int,
                             allow_mixers: bool = False,
                             allow_privacy_coins: bool = False,
                             allow_cross_chain: bool = False,
                             is_cold_storage: bool = False) -> List[CryptoWallet]:
        """
        Genera una capa de wallets con propiedades específicas
        """
        wallets = []
        
        for i in range(wallet_count):
            # Determinar tipo de wallet basado en parámetros
            if is_cold_storage:
                wallet_type = WalletType.COLD_STORAGE
            elif allow_mixers and random.random() > 0.7:
                wallet_type = WalletType.MIXER_LINKED
            elif allow_privacy_coins and random.random() > 0.8:
                wallet_type = WalletType.PRIVACY_COIN
            elif layer_type == "entry":
                wallet_type = WalletType.EXCHANGE_HOT
            else:
                wallet_type = random.choice([WalletType.DEX_ONLY, 
                                           WalletType.BURNER,
                                           WalletType.MULTISIG])
            
            # Determinar moneda
            if wallet_type == WalletType.PRIVACY_COIN:
                currency = random.choice(self.PRIVACY_COINS)
            else:
                currency = random.choice(["BTC", "ETH", "USDT"])
            
            # Generar wallet
            wallet = self.wallet_generator.generate_wallet(
                wallet_type=wallet_type,
                currency=currency,
                base_balance=amount / wallet_count,
                layer_type=layer_type
            )
            
            # Añadir propiedades de riesgo según configuración
            if allow_mixers and random.random() > 0.5:
                wallet.known_mixer_interactions = random.randint(1, 5)
            
            if allow_privacy_coins and currency in self.PRIVACY_COINS:
                wallet.privacy_coin_holdings = True
            
            if allow_cross_chain:
                wallet.cross_chain_transactions = random.randint(1, 3)
            
            wallets.append(wallet)
        
        return wallets
    
    def _connect_to_politician(self,
                              politician: Dict,
                              wallet_structure: Dict,
                              max_intermediaries: int) -> List[Dict]:
        """
        Crea camino de conexión desde el político hasta las wallets
        """
        politician_id = politician.get("id", "unknown")
        politician_name = politician.get("name", "Unknown")
        
        # Número de intermediarios (1 a max_intermediaries)
        num_intermediaries = random.randint(1, max_intermediaries)
        
        connection_path = [
            {
                "node_id": politician_id,
                "node_type": "politician",
                "name": politician_name,
                "connection_type": "origin"
            }
        ]
        
        # Generar intermediarios (familiares, empresas pantalla)
        for i in range(num_intermediaries):
            if i == 0:
                # Primer intermediario: familiar directo
                intermediary = {
                    "node_id": f"FAM_{politician_id}_{i}",
                    "node_type": "family_member",
                    "name": f"Family Member {i+1}",
                    "relationship": random.choice(["spouse", "child", "sibling"]),
                    "connection_type": "direct_family"
                }
            else:
                # Intermediarios posteriores: empresas o amigos
                intermediary = {
                    "node_id": f"INT_{politician_id}_{i}",
                    "node_type": "shell_company" if random.random() > 0.5 else "associate",
                    "name": f"Shell Co {i}" if random.random() > 0.5 else f"Associate {i}",
                    "connection_type": "business" if random.random() > 0.5 else "personal"
                }
            
            connection_path.append(intermediary)
        
        # Conectar al primer wallet de entrada
        if wallet_structure["entry_layer"]:
            first_wallet = wallet_structure["entry_layer"][0]
            connection_path.append({
                "node_id": first_wallet.address,
                "node_type": "crypto_wallet",
                "name": f"{first_wallet.currency} Wallet",
                "connection_type": "crypto_entry_point",
                "wallet_type": first_wallet.type.value
            })
        
        return connection_path
    
    def _generate_transaction_history(self,
                                     wallet_structure: Dict,
                                     patterns: List[TransactionPattern],
                                     severity: float) -> List[CryptoTransaction]:
        """
        Genera historial de transacciones con patrones específicos
        """
        transactions = []
        
        # Para cada capa, generar transacciones entre wallets
        all_wallets = []
        all_wallets.extend(wallet_structure["entry_layer"])
        for layer in wallet_structure["obfuscation_layers"]:
            all_wallets.extend(layer["wallets"])
        all_wallets.extend(wallet_structure["exit_layer"])
        
        if len(all_wallets) < 2:
            return transactions
        
        # Determinar patrones a aplicar
        active_patterns = []
        for pattern in patterns:
            if random.random() < severity:  # Mayor severidad = más patrones
                active_patterns.append(pattern)
        
        # Si no hay patrones activos, usar uno básico
        if not active_patterns:
            active_patterns = [TransactionPattern.PEELING_CHAIN]
        
        # Generar transacciones según patrones
        for pattern in active_patterns:
            pattern_transactions = self._generate_pattern_transactions(
                pattern, all_wallets, severity
            )
            transactions.extend(pattern_transactions)
        
        # Ordenar por timestamp
        transactions.sort(key=lambda x: x.timestamp)
        
        return transactions
    
    def _generate_pattern_transactions(self,
                                      pattern: TransactionPattern,
                                      wallets: List[CryptoWallet],
                                      severity: float) -> List[CryptoTransaction]:
        """
        Genera transacciones específicas para un patrón dado
        """
        transactions = []
        
        if pattern == TransactionPattern.PEELING_CHAIN:
            transactions = self._generate_peeling_chain(wallets, severity)
        elif pattern == TransactionPattern.STRUCTURED:
            transactions = self._generate_structured_transactions(wallets, severity)
        elif pattern == TransactionPattern.MIXER_CASCADE:
            transactions = self._generate_mixer_cascade(wallets, severity)
        elif pattern == TransactionPattern.CROSS_CHAIN_HOP:
            transactions = self._generate_cross_chain_hops(wallets, severity)
        elif pattern == TransactionPattern.PRIVACY_COIN_CONVERSION:
            transactions = self._generate_privacy_coin_conversion(wallets, severity)
        
        return transactions
    
    def _generate_peeling_chain(self, wallets: List[CryptoWallet], 
                               severity: float) -> List[CryptoTransaction]:
        """
        Genera patrón de peeling chain: una transacción grande seguida de muchas pequeñas
        """
        transactions = []
        
        if len(wallets) < 3:
            return transactions
        
        # Seleccionar wallet de origen
        source_wallet = random.choice(wallets[:2])  # De las primeras wallets
        
        # Transacción grande inicial
        large_amount = source_wallet.estimated_balance_fiat * 0.6
        intermediate_wallet = random.choice(wallets[2:4])
        
        large_tx = self.transaction_generator.generate_transaction(
            source_wallet=source_wallet,
            target_wallet=intermediate_wallet,
            amount_fiat=large_amount,
            timestamp_offset=0
        )
        transactions.append(large_tx)
        
        # Múltiples transacciones pequeñas desde la wallet intermedia
        num_small_txs = int(severity * 10) + 3  # 3-13 transacciones pequeñas
        
        for i in range(num_small_txs):
            target_wallet = random.choice(wallets[4:]) if len(wallets) > 4 else intermediate_wallet
            
            small_amount = large_amount * random.uniform(0.01, 0.05)  # 1-5% de la grande
            
            small_tx = self.transaction_generator.generate_transaction(
                source_wallet=intermediate_wallet,
                target_wallet=target_wallet,
                amount_fiat=small_amount,
                timestamp_offset=i * random.randint(1, 6),  # Horas entre transacciones
                peeling_chain_step=i+1
            )
            transactions.append(small_tx)
        
        return transactions
    
    def _generate_mixer_cascade(self, wallets: List[CryptoWallet],
                              severity: float) -> List[CryptoTransaction]:
        """
        Genera cascada de transacciones a través de mixers
        """
        transactions = []
        
        # Identificar wallets que pueden usar mixers
        mixer_wallets = [w for w in wallets if w.type in [WalletType.MIXER_LINKED, 
                                                         WalletType.DEX_ONLY]]
        
        if len(mixer_wallets) < 2:
            return transactions
        
        num_mixer_passes = int(severity * 5) + 1  # 1-6 pasos por mixers
        
        current_wallet = mixer_wallets[0]
        
        for pass_num in range(num_mixer_passes):
            next_wallet = mixer_wallets[(pass_num + 1) % len(mixer_wallets)]
            
            amount = current_wallet.estimated_balance_fiat * random.uniform(0.3, 0.7)
            
            tx = self.transaction_generator.generate_transaction(
                source_wallet=current_wallet,
                target_wallet=next_wallet,
                amount_fiat=amount,
                timestamp_offset=pass_num * random.randint(6, 24),  # 6-24 horas entre pasos
                mixer_used=True,
                mixer_service=random.choice(self.KNOWN_MIXERS)
            )
            transactions.append(tx)
            
            current_wallet = next_wallet
        
        return transactions
    
    def _calculate_crypto_risk_metrics(self,
                                      wallet_structure: Dict,
                                      transactions: List[CryptoTransaction],
                                      level: CryptoEvasionLevel) -> Dict:
        """
        Calcula métricas de riesgo específicas para cripto
        """
        # Contar transacciones con mixers
        mixer_transactions = [t for t in transactions if t.mixer_used]
        
        # Contar transacciones con privacy coins
        privacy_coin_txs = [t for t in transactions if t.privacy_coin_involved]
        
        # Calcular complejidad de la estructura
        complexity_score = (
            len(wallet_structure["obfuscation_layers"]) * 0.3 +
            wallet_structure["total_wallets"] * 0.02 +
            len([w for w in wallet_structure.get("entry_layer", []) 
                 if w.ml_risk_score > 0.5]) * 0.2
        )
        
        return {
            "mixer_transaction_count": len(mixer_transactions),
            "privacy_coin_transaction_count": len(privacy_coin_txs),
            "cross_chain_transaction_count": len([t for t in transactions if t.cross_chain]),
            "structured_transaction_count": len([t for t in transactions if t.structured_amount]),
            "wallet_layers": wallet_structure["total_layers"],
            "total_wallets": wallet_structure["total_wallets"],
            "complexity_score": min(1.0, complexity_score),
            "evasion_level_factor": {
                CryptoEvasionLevel.BASIC: 0.3,
                CryptoEvasionLevel.INTERMEDIATE: 0.6,
                CryptoEvasionLevel.ADVANCED: 1.0
            }[level]
        }
    
    def _calculate_ira_bonus(self,
                            risk_metrics: Dict,
                            bonus_range: Tuple[int, int]) -> int:
        """
        Calcula bonificación IRA basada en métricas de riesgo
        """
        base_bonus = bonus_range[0]
        range_size = bonus_range[1] - bonus_range[0]
        
        # Factores de contribución
        factors = {
            "mixer_usage": min(1.0, risk_metrics["mixer_transaction_count"] / 5) * 0.3,
            "privacy_coins": min(1.0, risk_metrics["privacy_coin_transaction_count"] / 3) * 0.25,
            "cross_chain": min(1.0, risk_metrics["cross_chain_transaction_count"] / 4) * 0.2,
            "complexity": risk_metrics["complexity_score"] * 0.15,
            "evasion_level": risk_metrics["evasion_level_factor"] * 0.1
        }
        
        total_factor = sum(factors.values())
        
        bonus = base_bonus + (range_size * total_factor)
        
        return int(round(bonus))
    
    def _generate_detection_heuristics(self, level: CryptoEvasionLevel) -> List[Dict]:
        """
        Genera heurísticas de detección específicas para el nivel
        """
        base_heuristics = [
            {
                "name": "MIXER_INTERACTION_DETECTION",
                "description": "Wallet interactúa con direcciones conocidas de mixers",
                "weight": 0.25
            },
            {
                "name": "PRIVACY_COIN_CONVERSION",
                "description": "Conversión significativa a monedas de privacidad",
                "weight": 0.20
            }
        ]
        
        if level == CryptoEvasionLevel.INTERMEDIATE:
            base_heuristics.extend([
                {
                    "name": "STRUCTURED_TRANSACTIONS",
                    "description": "Transacciones justo bajo límites de reporte",
                    "weight": 0.15
                },
                {
                    "name": "PEELING_CHAIN_DETECTION",
                    "description": "Patrón de grandes cantidades seguidas de pequeñas",
                    "weight": 0.10
                }
            ])
        
        if level == CryptoEvasionLevel.ADVANCED:
            base_heuristics.extend([
                {
                    "name": "CROSS_CHAIN_HOPPING",
                    "description": "Movimientos rápidos entre múltiples blockchains",
                    "weight": 0.15
                },
                {
                    "name": "COMPLEX_WALLET_STRUCTURE",
                    "description": "Estructura multicapa de wallets con propósitos específicos",
                    "weight": 0.10
                },
                {
                    "name": "TEMPORAL_OBFUSCATION",
                    "description": "Patrones temporales diseñados para evadir detección",
                    "weight": 0.05
                }
            ])
        
        # Normalizar pesos
        total_weight = sum(h["weight"] for h in base_heuristics)
        for h in base_heuristics:
            h["weight"] = h["weight"] / total_weight
        
        return base_heuristics
    
    def _get_ground_truth_flags(self,
                               wallet_structure: Dict,
                               transactions: List[CryptoTransaction]) -> List[str]:
        """
        Genera banderas de ground truth para validación
        """
        flags = ["CRYPTO_HIDING_PATTERN"]
        
        # Verificar uso de mixers
        if any(t.mixer_used for t in transactions):
            flags.append("MIXER_UTILIZATION")
        
        # Verificar privacy coins
        if any(t.privacy_coin_involved for t in transactions):
            flags.append("PRIVACY_COIN_USAGE")
        
        # Verificar estructura multicapa
        if wallet_structure["total_layers"] > 1:
            flags.append(f"MULTI_LAYER_STRUCTURE_{wallet_structure['total_layers']}")
        
        # Verificar transacciones estructuradas
        if any(t.structured_amount for t in transactions):
            flags.append("STRUCTURED_TRANSACTIONS")
        
        return flags

# ==================== GENERADORES AUXILIARES ====================

class CryptoWalletGenerator:
    """Genera wallets cripto realistas con propiedades específicas"""
    
    def generate_wallet(self,
                       wallet_type: WalletType,
                       currency: str,
                       base_balance: float,
                       layer_type: str = "general") -> CryptoWallet:
        
        # Generar address según tipo y moneda
        if currency in ["XMR", "ZEC"]:
            # Addresses de privacy coins
            if currency == "XMR":
                address = f"4{self._generate_hex(31)}"  # Monero-style
            else:
                address = f"z{self._generate_hex(33)}"  # Zcash z-address
        else:
            # Ethereum-style address (0x...)
            address = f"0x{self._generate_hex(20)}"
        
        # Fechas realistas
        creation_date = datetime.now() - timedelta(days=random.randint(30, 365*2))
        last_active = creation_date + timedelta(days=random.randint(0, 60))
        
        # Balance con variación
        balance_variation = random.uniform(0.8, 1.2)
        estimated_balance = base_balance * balance_variation
        
        # Score de riesgo inicial basado en tipo
        base_risk_score = {
            WalletType.EXCHANGE_HOT: 0.2,
            WalletType.COLD_STORAGE: 0.4,
            WalletType.MIXER_LINKED: 0.8,
            WalletType.PRIVACY_COIN: 0.9,
            WalletType.DEX_ONLY: 0.6,
            WalletType.BURNER: 0.7,
            WalletType.MULTISIG: 0.3
        }.get(wallet_type, 0.5)
        
        # Ajustar por capa
        layer_multiplier = {
            "entry": 0.8,
            "obfuscation": 1.2,
            "exit": 1.0
        }.get(layer_type, 1.0)
        
        ml_risk_score = min(1.0, base_risk_score * layer_multiplier * random.uniform(0.9, 1.1))
        
        return CryptoWallet(
            address=address,
            type=wallet_type,
            currency=currency,
            creation_date=creation_date,
            last_active=last_active,
            estimated_balance_fiat=estimated_balance,
            ml_risk_score=ml_risk_score
        )
    
    def _generate_hex(self, length: int) -> str:
        """Genera string hexadecimal aleatorio"""
        return hashlib.sha256(str(random.random()).encode()).hexdigest()[:length]

class CryptoTransactionGenerator:
    """Genera transacciones cripto realistas"""
    
    def generate_transaction(self,
                           source_wallet: CryptoWallet,
                           target_wallet: CryptoWallet,
                           amount_fiat: float,
                           timestamp_offset: int = 0,
                           mixer_used: bool = False,
                           mixer_service: Optional[str] = None,
                           peeling_chain_step: Optional[int] = None) -> CryptoTransaction:
        
        # Timestamp base
        base_time = source_wallet.last_active
        timestamp = base_time + timedelta(hours=timestamp_offset)
        
        # Generar hash de transacción
        tx_hash = f"0x{hashlib.sha256(str(random.random()).encode()).hexdigest()[:64]}"
        
        # Calcular cantidad en cripto
        crypto_price = self._get_crypto_price(source_wallet.currency)
        amount_crypto = amount_fiat / crypto_price
        
        # Determinar si es structured amount (justo bajo límite de reporte)
        structured_amount = False
        if 9000 <= amount_fiat <= 10000:  # Justo bajo límite de $10K
            structured_amount = True
        
        # Determinar si involucra privacy coin
        privacy_coin_involved = (source_wallet.currency in ["XMR", "ZEC", "DASH"] or
                               target_wallet.currency in ["XMR", "ZEC", "DASH"])
        
        # Determinar si es cross-chain
        cross_chain = source_wallet.currency != target_wallet.currency
        
        return CryptoTransaction(
            tx_hash=tx_hash,
            timestamp=timestamp,
            from_address=source_wallet.address,
            to_address=target_wallet.address,
            amount_fiat=amount_fiat,
            amount_crypto=amount_crypto,
            currency=source_wallet.currency,
            mixer_used=mixer_used,
            mixer_service=mixer_service,
            privacy_coin_involved=privacy_coin_involved,
            cross_chain=cross_chain,
            cross_chain_bridge=random.choice(["Polygon Bridge", "Arbitrum Bridge"]) 
                              if cross_chain else None,
            structured_amount=structured_amount,
            peeling_chain_step=peeling_chain_step
        )
    
    def _get_crypto_price(self, currency: str) -> float:
        """Precios simulados de criptomonedas"""
        prices = {
            "BTC": 45000.0,
            "ETH": 2500.0,
            "USDT": 1.0,
            "XMR": 150.0,
            "ZEC": 30.0,
            "DASH": 40.0
        }
        return prices.get(currency, 1000.0)

# ==================== EJEMPLO DE USO ====================

def demonstrate_crypto_hiding_injection():
    """Demuestra la inyección de patrones en los tres niveles"""
    
    # Político de ejemplo
    example_politician = {
        "id": "POL_001",
        "name": "John Public",
        "annual_income": 200000,
        "declared_assets": 500000,
        "position": "Congress Member"
    }
    
    injector = CryptoHidingInjector()
    
    print("=" * 80)
    print("CRYPTO_HIDING PATTERN INJECTION DEMONSTRATION")
    print("=" * 80)
    
    # Inyectar los tres niveles
    for level in CryptoEvasionLevel:
        print(f"\n🔵 Injecting {level.value.upper()} level pattern...")
        
        pattern = injector.inject_pattern(
            politician=example_politician,
            level=level,
            severity=0.7
        )
        
        # Resumen del patrón inyectado
        print(f"   Hidden Amount: ${pattern['hidden_amount_fiat']:,.2f}")
        print(f"   Wallet Layers: {pattern['wallet_structure']['total_layers']}")
        print(f"   Total Wallets: {pattern['wallet_structure']['total_wallets']}")
        print(f"   Transactions: {len(pattern['transaction_history'])}")
        
        # Métricas de riesgo
        risk = pattern['risk_metrics']
        print(f"   Mixer Transactions: {risk['mixer_transaction_count']}")
        print(f"   Privacy Coin TXs: {risk['privacy_coin_transaction_count']}")
        print(f"   IRA Bonus: +{pattern['ira_bonus']} points")
        
        # Ground truth flags
        print(f"   Ground Truth Flags: {', '.join(pattern['ground_truth_flags'])}")
    
    print("\n" + "=" * 80)
    print("✅ All patterns injected successfully!")
    print("=" * 80)

# Ejecutar demostración
if __name__ == "__main__":
    demonstrate_crypto_hiding_injection()
