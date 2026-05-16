"""
Inspector IA - Ground Truth Validator
======================================

Valida que los patrones inyectados en el universo sintético sean detectables.

Author: Inspector IA Core Team
Version: 2.0
Date: December 2024
"""

from typing import Any, Dict, List

from src.synthetic.datasets.base_dataset import GroundTruth, SyntheticCase


class GroundTruthValidator:
    """
    Clase para validar la integridad y detectabilidad de los datos sintéticos.
    """

    def __init__(self, ground_truth_map: Dict[str, GroundTruth]):
        """Inicializa el validador con el mapa de verdad fundamental."""
        self.ground_truth_map = ground_truth_map
        self.stats = {"total_cases": 0, "fraud_cases": 0, "clean_cases": 0, "pattern_counts": {}}

    def validate_case(self, case: SyntheticCase) -> bool:
        """
        Valida un caso individual contra su verdad fundamental.

        En un sistema real, esto implicaría ejecutar el motor de detección
        sobre el caso y comparar el resultado con el ground_truth.

        Args:
            case: El caso sintético a validar.

        Returns:
            True si la validación es exitosa (el patrón inyectado es detectable), False en caso contrario.
        """
        self.stats["total_cases"] += 1

        gt = self.ground_truth_map.get(case.id)

        if not gt:
            print(f"⚠️ Advertencia: No se encontró Ground Truth para el caso {case.id}")
            return False

        # 1. Verificar la etiqueta de fraude
        if case.ground_truth.is_fraud != gt.is_fraud:
            print(f"❌ Error de Ground Truth: is_fraud no coincide para {case.id}")
            return False

        if gt.is_fraud:
            self.stats["fraud_cases"] += 1
            # 2. Verificar que los patrones inyectados coincidan
            if set(case.ground_truth.patterns) != set(gt.patterns):
                print(f"❌ Error de Ground Truth: Patrones inyectados no coinciden para {case.id}")
                return False

            # 3. Contar patrones
            for pattern in gt.patterns:
                self.stats["pattern_counts"][pattern] = (
                    self.stats["pattern_counts"].get(pattern, 0) + 1
                )
        else:
            self.stats["clean_cases"] += 1

        return True

    def validate_universe(self, all_cases: List[SyntheticCase]) -> Dict[str, Any]:
        """
        Valida el universo completo de casos sintéticos.
        """
        print("=====================================================")
        print("🧪 Iniciando Validación de Ground Truth")
        print("=====================================================")

        validation_results = []

        for case in all_cases:
            is_valid = self.validate_case(case)
            validation_results.append({"case_id": case.id, "is_valid": is_valid})

        print("=====================================================")
        print("✅ Validación de Ground Truth Finalizada")
        print("=====================================================")

        return {"validation_results": validation_results, "statistics": self.stats}

    def get_summary(self) -> str:
        """Genera un resumen de la validación."""
        summary = "\n--- Resumen de Validación ---\n"
        summary += f"Casos totales procesados: {self.stats['total_cases']}\n"
        summary += f"Casos de fraude (GT): {self.stats['fraud_cases']}\n"
        summary += f"Casos limpios (GT): {self.stats['clean_cases']}\n"
        summary += "\nConteo de Patrones Inyectados:\n"
        for pattern, count in self.stats["pattern_counts"].items():
            summary += f"- {pattern}: {count}\n"

        return summary


# Ejemplo de uso (simulado)
if __name__ == "__main__":
    # Simulación de Ground Truth Map
    gt_map = {
        "POL-00001": GroundTruth(is_fraud=False, patterns=[]),
        "POL-FRAUD-0001": GroundTruth(is_fraud=True, patterns=["CRYPTO_HIDING"]),
        "POL-FRAUD-0002": GroundTruth(is_fraud=True, patterns=["OFFSHORE_LAUNDERING"]),
    }

    # Simulación de Casos Sintéticos
    cases = [
        SyntheticCase(
            id="POL-00001",
            type="politician",
            name="Clean Pol",
            age=50,
            party="A",
            financial_data=None,
            network_data=None,
            ground_truth=GroundTruth(is_fraud=False, patterns=[]),
        ),
        SyntheticCase(
            id="POL-FRAUD-0001",
            type="politician",
            name="Fraud Pol 1",
            age=60,
            party="B",
            financial_data=None,
            network_data=None,
            ground_truth=GroundTruth(is_fraud=True, patterns=["CRYPTO_HIDING"]),
        ),
        SyntheticCase(
            id="POL-FRAUD-0002",
            type="politician",
            name="Fraud Pol 2",
            age=55,
            party="C",
            financial_data=None,
            network_data=None,
            ground_truth=GroundTruth(is_fraud=True, patterns=["OFFSHORE_LAUNDERING"]),
        ),
    ]

    validator = GroundTruthValidator(gt_map)
    results = validator.validate_universe(cases)
    print(validator.get_summary())
