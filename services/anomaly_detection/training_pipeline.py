from synthetic_fraud_ecosystem.generators.cosmic_fraud_generator import CosmicFraudGenerator
from synthetic_fraud_ecosystem.generators.crypto_hiding_injector import CryptoEvasionLevel

def generate_training_batch(politician_list: List[Dict]):
    generator = CosmicFraudGenerator()
    
    for politician in politician_list:
        # Inyectar un caso avanzado en el 10% de los políticos
        if random.random() < 0.1:
            injected_pattern = generator.inject_pattern(
                pattern_type="CRYPTO_HIDING",
                politician=politician,
                level=CryptoEvasionLevel.ADVANCED,
                severity=random.uniform(0.7, 1.0)
            )
            # El ground_truth_flags se usa para etiquetar el dataset de entrenamiento.
            politician["is_fraudulent"] = True
            politician["ground_truth"] = injected_pattern["ground_truth_flags"]
        # ... continuar con otros patrones
