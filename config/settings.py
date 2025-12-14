"""
Inspector IA - Configuration Settings
======================================

Configuración centralizada del sistema.

Author: Inspector IA Core Team
Version: 2.0
Date: December 2024
"""

import os
from typing import Optional
from pathlib import Path
# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings:
    """Configuración principal del sistema."""
    
    # ==================== APPLICATION ====================
    APP_NAME: str = "Inspector_IA"
    APP_VERSION: str = "2.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "change-this-in-production"
    
    # ==================== API ====================
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 4
    API_RELOAD: bool = True
    
    # ==================== NEO4J ====================
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "inspector_ia_2024"
    NEO4J_DATABASE: str = "neo4j"
    NEO4J_MAX_CONNECTION_LIFETIME: int = 3600
    NEO4J_MAX_CONNECTION_POOL_SIZE: int = 50
    
    # ==================== POSTGRESQL ====================
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "inspector_ia"
    POSTGRES_USER: str = "inspector"
    POSTGRES_PASSWORD: str = "inspector_ia_2024"
    POSTGRES_POOL_SIZE: int = 20
    
    # ==================== REDIS ====================
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = "inspector_ia_2024"
    REDIS_DB: int = 0
    REDIS_MAX_CONNECTIONS: int = 50
    
    # ==================== RABBITMQ ====================
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "inspector"
    RABBITMQ_PASS: str = "inspector_ia_2024"
    RABBITMQ_VHOST: str = "/"
    
    # ==================== CELERY ====================
    CELERY_BROKER_URL: str = "amqp://inspector:inspector_ia_2024@localhost:5672//"
    CELERY_RESULT_BACKEND: str = "redis://:inspector_ia_2024@localhost:6379/0"
    
    # ==================== SECURITY ====================
    JWT_SECRET_KEY: str = "change-this-jwt-secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60
    BCRYPT_ROUNDS: int = 12
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    CORS_ALLOW_CREDENTIALS: bool = True
    
    # ==================== IRA CONFIGURATION ====================
    IRA_PATRIMONIAL_WEIGHT: float = 0.30
    IRA_NETWORK_WEIGHT: float = 0.40
    IRA_TEMPORAL_WEIGHT: float = 0.30
    IRA_NETWORK_BONUS_MAX: float = 30.0
    COMPLETENESS_THRESHOLD: float = 0.70
    
    # ==================== PATTERN THRESHOLDS ====================
    CRYPTO_HIDING_THRESHOLD: float = 0.70
    OFFSHORE_LAUNDERING_THRESHOLD: float = 0.75
    TRAVEL_COINCIDENCE_THRESHOLD: float = 0.65
    GHOST_COMPANY_THRESHOLD: float = 0.80
    INSIDER_TRADING_THRESHOLD: float = 0.70
    
    # ==================== DATA PROCESSING ====================
    MAX_GRAPH_DEPTH: int = 5
    MAX_PATH_LENGTH: int = 10
    TEMPORAL_WINDOW_DAYS: int = 90
    BATCH_PROCESSING_SIZE: int = 100
    
    # ==================== MONITORING ====================
    PROMETHEUS_PORT: int = 9090
    GRAFANA_PORT: int = 3001
    ENABLE_METRICS: bool = True
    ENABLE_TRACING: bool = False
    
    # ==================== LOGGING ====================
    LOG_DIR: Path = BASE_DIR / "logs"
    LOG_FILE: str = "inspector_ia.log"
    LOG_MAX_BYTES: int = 10485760  # 10MB
    LOG_BACKUP_COUNT: int = 5
    
    # ==================== FILE STORAGE ====================
    UPLOAD_DIR: Path = BASE_DIR / "data" / "uploads"
    REPORT_DIR: Path = BASE_DIR / "reports"
    TEMP_DIR: Path = BASE_DIR / "data" / "temp"
    MAX_UPLOAD_SIZE: int = 52428800  # 50MB
    
    # ==================== EXTERNAL SERVICES ====================
    ETHERSCAN_API_KEY: Optional[str] = None
    BLOCKCHAIN_INFO_API_KEY: Optional[str] = None
    OPENCORPORATES_API_KEY: Optional[str] = None
    ICIJ_OFFSHORELEAKS_API_KEY: Optional[str] = None
    
    # ==================== DEVELOPMENT ====================
    DEV_MODE: bool = True
    HOT_RELOAD: bool = True
    MOCK_EXTERNAL_APIS: bool = False
    SEED_DATABASE: bool = False
    

# Instancia global de configuración
settings = Settings()


# ==================== FUNCIONES DE UTILIDAD ====================

def get_database_url() -> str:
    """Obtiene la URL de conexión a PostgreSQL."""
    return (
        f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
        f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    )


def get_neo4j_config() -> dict:
    """Obtiene la configuración de Neo4j."""
    return {
        "uri": settings.NEO4J_URI,
        "user": settings.NEO4J_USER,
        "password": settings.NEO4J_PASSWORD,
        "database": settings.NEO4J_DATABASE
    }


def get_redis_url() -> str:
    """Obtiene la URL de conexión a Redis."""
    return f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"


def ensure_directories():
    """Asegura que existan los directorios necesarios."""
    directories = [
        settings.LOG_DIR,
        settings.UPLOAD_DIR,
        settings.REPORT_DIR,
        settings.TEMP_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


# Crear directorios al importar
ensure_directories()
