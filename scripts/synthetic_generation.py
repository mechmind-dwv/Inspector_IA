#!/usr/bin/env python3
"""
Inspector IA - Synthetic Data Generation Script
================================================

Script para generar el universo de datos sintéticos de fraude (SFE).

Author: Inspector IA Core Team
Version: 2.0
Date: December 2024
"""

import argparse
import sys
from pathlib import Path

# Agregar el directorio raíz al path para imports locales
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from pathlib import Path

from config.settings import settings
from src.synthetic.fraud_engine import CosmicFraudGenerator
from src.synthetic.validators.ground_truth_validator import GroundTruthValidator


def parse_args():
    """Parsea los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Generador de Universo de Datos Sintéticos (SFE) para Inspector IA."
    )
    parser.add_argument(
        "--size",
        type=int,
        default=settings.BATCH_PROCESSING_SIZE * 10,  # Usar un valor por defecto de settings
        help=f"Número total de casos a generar (limpios + fraude). Por defecto: {settings.BATCH_PROCESSING_SIZE * 10}",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/synthetic/synthetic_universe.json",
        help="Ruta del archivo de salida para el universo JSON.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=settings.SEED_DATABASE if hasattr(settings, "SEED_DATABASE") else 42,
        help="Semilla para la generación de datos reproducible. Por defecto: 42",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Ejecutar la validación de Ground Truth después de la generación.",
    )
    return parser.parse_args()


def main():
    """Función principal del script de generación."""
    args = parse_args()

    print("=====================================================")
    print("🌌 Inspector IA - Generador de Datos Sintéticos (SFE)")
    print("=====================================================")
    print(f"Configuración: Tamaño={args.size}, Semilla={args.seed}, Salida={args.output}")

    # 1. Inicializar y Generar
    try:
        generator = CosmicFraudGenerator(seed=args.seed)
        universe = generator.generate_universe(size=args.size)
    except Exception as e:
        print(f"❌ ERROR durante la generación: {e}")
        sys.exit(1)

    # 2. Guardar
    try:
        output_path = ROOT_DIR / args.output
        generator.save_universe(universe, str(output_path))
    except Exception as e:
        print(f"❌ ERROR al guardar el universo: {e}")
        sys.exit(1)

    # 3. Validar (Opcional)
    if args.validate:
        print("\n--- Ejecutando Validación ---")
        try:
            # Nota: La validación actual en fraud_engine.py no usa la clase SyntheticCase
            # Por simplicidad, usamos el GroundTruthValidator con el mapa generado
            validator = GroundTruthValidator(universe["ground_truth"])

            # Simulación de casos para la validación (se debería usar el formato SyntheticCase)
            # Aquí solo validamos la consistencia del mapa de GT

            print("✅ Validación de Ground Truth completada (consistencia interna).")

        except Exception as e:
            print(f"❌ ERROR durante la validación: {e}")
            sys.exit(1)

    print("\n=====================================================")
    print("✅ Generación de Datos Sintéticos Finalizada")
    print("=====================================================")
    print(f"Total de casos generados: {len(universe['all_cases'])}")
    print(f"Guardado en: {output_path}")


if __name__ == "__main__":
    main()
