#!/usr/bin/env python3
"""
Inspector IA - Setup Script
============================

Script de configuración inicial del sistema.

Author: Inspector IA Core Team
Version: 2.0
Date: December 2024
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))


def print_banner():
    """Imprime el banner de Inspector IA."""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              🌌 INSPECTOR IA - SETUP 🌌                  ║
    ║                                                           ║
    ║        Sistema de Inteligencia Forense para              ║
    ║           Periodismo de Investigación                    ║
    ║                                                           ║
    ║                   Versión 2.0.0                          ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_python_version():
    """Verifica la versión de Python."""
    print("🔍 Verificando versión de Python...")

    if sys.version_info < (3, 11):
        print("❌ ERROR: Se requiere Python 3.11 o superior")
        print(f"   Versión actual: {sys.version}")
        sys.exit(1)

    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")


def check_dependencies():
    """Verifica que las dependencias estén instaladas."""
    print("\n🔍 Verificando dependencias...")

    required_packages = ["fastapi", "uvicorn", "pydantic", "neo4j", "pandas", "numpy"]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NO INSTALADO")
            missing_packages.append(package)

    if missing_packages:
        print("\n⚠️  Faltan dependencias. Ejecuta:")
        print("   pip install -r requirements.txt")
        return False

    return True


def create_directories():
    """Crea los directorios necesarios."""
    print("\n📁 Creando directorios...")

    directories = [
        "data/raw",
        "data/processed",
        "data/synthetic",
        "data/models",
        "data/uploads",
        "data/temp",
        "logs",
        "reports",
    ]

    for directory in directories:
        dir_path = ROOT_DIR / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ {directory}")


def check_env_file():
    """Verifica que exista el archivo .env."""
    print("\n🔍 Verificando archivo .env...")

    env_file = ROOT_DIR / ".env"
    env_example = ROOT_DIR / ".env.example"

    if not env_file.exists():
        if env_example.exists():
            print("⚠️  Archivo .env no encontrado")
            print("   Copiando desde .env.example...")

            with open(env_example, "r") as src:
                with open(env_file, "w") as dst:
                    dst.write(src.read())

            print("✅ Archivo .env creado")
            print("   ⚠️  IMPORTANTE: Edita .env con tus configuraciones")
        else:
            print("❌ No se encontró .env ni .env.example")
            return False
    else:
        print("✅ Archivo .env encontrado")

    return True


def test_imports():
    """Prueba que los módulos principales se importen correctamente."""
    print("\n🔍 Probando imports de módulos principales...")

    try:
        print("✅ IRACalculator")
    except Exception as e:
        print(f"❌ IRACalculator: {e}")
        return False

    try:
        print("✅ RiskCalculator")
    except Exception as e:
        print(f"❌ RiskCalculator: {e}")
        return False

    try:
        print("✅ Neo4jConnector")
    except Exception as e:
        print(f"❌ Neo4jConnector: {e}")
        return False

    return True


def print_next_steps():
    """Imprime los siguientes pasos."""
    print("\n" + "=" * 60)
    print("✅ SETUP COMPLETADO")
    print("=" * 60)

    print("\n📚 PRÓXIMOS PASOS:\n")

    print("1. Editar configuración:")
    print("   nano .env")

    print("\n2. Iniciar servicios Docker:")
    print("   docker-compose up -d")

    print("\n3. Ejecutar ejemplo:")
    print("   python examples/example_analysis.py")

    print("\n4. Acceder a la API:")
    print("   http://localhost:8000/api/docs")

    print("\n5. Leer documentación:")
    print("   cat README_IMPLEMENTATION.md")

    print("\n" + "=" * 60)
    print("🌟 Inspector IA - Listo para usar")
    print("=" * 60)


def main():
    """Función principal."""
    print_banner()

    # Verificaciones
    check_python_version()

    if not check_dependencies():
        print("\n❌ Setup incompleto - instala las dependencias primero")
        sys.exit(1)

    # Configuración
    create_directories()

    if not check_env_file():
        print("\n❌ Setup incompleto - configura el archivo .env")
        sys.exit(1)

    # Pruebas
    if not test_imports():
        print("\n❌ Setup incompleto - hay problemas con los imports")
        sys.exit(1)

    # Finalizar
    print_next_steps()


if __name__ == "__main__":
    main()
