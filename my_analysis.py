# Guardar como my_analysis.py
from src.core.risk_calculator import RiskCalculator

calculator = RiskCalculator()

politician_data = {
    "id": "POL-CUSTOM-001",
    "name": "Mi Político",
    "annual_income": 200000,
    "total_assets": 1000000,
    "years_in_office": 4
}

graph_data = {
    "offshore_entities": [],
    "ghost_companies": [],
    "crypto_wallets": []
}

temporal_events = []

result = calculator.calculate_comprehensive_risk(
    politician_id="POL-CUSTOM-001",
    politician_data=politician_data,
    graph_data=graph_data,
    temporal_events=temporal_events
)

print(f"IRA: {result['ira_result']['final_score']:.2f}")
print(f"Nivel: {result['ira_result']['risk_level']}")
