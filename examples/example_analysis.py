"""
Inspector IA - Example Analysis Script
=======================================

Script de ejemplo que demuestra cómo usar el sistema Inspector IA
para analizar el riesgo de un político.

Author: Inspector IA Core Team
Version: 2.0
Date: December 2024
"""

import sys
sys.path.append('/home/ubuntu/Inspector_IA')

from src.core.risk_calculator import RiskCalculator
from src.core.anomaly_index import format_ira_report
from datetime import datetime
import json


def create_example_politician():
    """Crea datos de ejemplo de un político."""
    return {
        "id": "POL-EXAMPLE-001",
        "name": "Juan Ejemplo Político",
        "position": "Senador",
        "party": "Partido Ejemplo",
        "government_level": "nacional",
        "start_date": "2018-01-01",
        "annual_income": 180000.0,
        "total_assets": 3500000.0,
        "years_in_office": 6,
        "asset_changes": [
            {
                "year": 2020,
                "percentage_increase": 65.0,
                "explanation": "Herencia declarada"
            },
            {
                "year": 2022,
                "percentage_increase": 35.0,
                "explanation": "Inversiones inmobiliarias"
            }
        ],
        "declared_properties": [
            {
                "type": "inmueble",
                "value": 800000.0,
                "location": "Ciudad Capital"
            },
            {
                "type": "vehiculo",
                "value": 120000.0,
                "location": "Ciudad Capital"
            }
        ],
        "financial_disclosures": [
            {
                "year": 2023,
                "total_assets": 3500000.0,
                "total_liabilities": 200000.0
            }
        ]
    }


def create_example_graph_data():
    """Crea datos de ejemplo del grafo de conexiones."""
    return {
        "offshore_entities": [
            {
                "id": "OFF-001",
                "name": "Panama Holdings Ltd",
                "jurisdiction": "Panama",
                "is_shell_company": True,
                "has_nominee_shareholders": True,
                "incorporation_date": "2019-03-15"
            },
            {
                "id": "OFF-002",
                "name": "Cayman Investment Corp",
                "jurisdiction": "Islas Caimán",
                "is_shell_company": True,
                "has_nominee_shareholders": False,
                "incorporation_date": "2020-07-22"
            }
        ],
        "ghost_companies": [
            {
                "id": "GHOST-001",
                "name": "Servicios Fantasma SA",
                "ghost_risk_score": 0.85,
                "no_employees": True,
                "no_physical_office": True,
                "high_government_contracts": True,
                "total_contracts_value": 2500000.0
            }
        ],
        "suspicious_individuals": [
            {
                "id": "IND-001",
                "name": "Socio Sospechoso",
                "relationship": "socio comercial",
                "risk_factors": ["investigaciones previas", "conexiones offshore"]
            }
        ],
        "crypto_wallets": [
            {
                "address": "0x1234567890abcdef",
                "currency": "ETH",
                "mixer_interactions": 3,
                "privacy_coin_holdings": True,
                "cross_chain_transactions": 5,
                "structured_pattern_detected": True,
                "estimated_balance_fiat": 450000.0
            }
        ],
        "intermediary_layers": 3,
        "unique_jurisdictions": ["Panama", "Islas Caimán", "Suiza", "Luxemburgo"],
        "advanced_concealment_techniques": [
            "Uso de mixers de criptomonedas",
            "Estructuras de propiedad circular",
            "Nominee shareholders múltiples"
        ],
        "circular_ownership_structures": [
            {
                "companies_involved": ["GHOST-001", "OFF-001"],
                "complexity_score": 0.75
            }
        ],
        "direct_connections": 15,
        "company_relationships": 8,
        "family_network": 6,
        "contract_paths": 4
    }


def create_example_temporal_events():
    """Crea eventos temporales de ejemplo."""
    return [
        {
            "type": "legislative_financial_correlation",
            "date": "2023-03-15",
            "description": "Voto favorable a ley de infraestructura seguido de transacción",
            "details": {
                "days_difference": 7,
                "transaction_amount": 500000.0,
                "legislative_action": "Voto favorable Ley 123/2023",
                "financial_action": "Adquisición de acciones en constructora"
            }
        },
        {
            "type": "travel_financial_correlation",
            "date": "2023-06-20",
            "description": "Viaje a Panamá seguido de transferencia bancaria",
            "details": {
                "days_difference": 3,
                "destination": "Panama",
                "is_tax_haven": True,
                "transaction_amount": 250000.0
            }
        },
        {
            "type": "legislative_financial_correlation",
            "date": "2023-09-10",
            "description": "Participación en comité de energía antes de inversión",
            "details": {
                "days_difference": 12,
                "transaction_amount": 300000.0,
                "legislative_action": "Comité de Energía - Proyecto renovables",
                "financial_action": "Inversión en empresa de energía solar"
            }
        },
        {
            "type": "travel_financial_correlation",
            "date": "2023-11-05",
            "description": "Viaje a Islas Caimán con movimiento financiero posterior",
            "details": {
                "days_difference": 5,
                "destination": "Islas Caimán",
                "is_tax_haven": True,
                "transaction_amount": 180000.0
            }
        }
    ]


def run_example_analysis():
    """Ejecuta un análisis de ejemplo completo."""
    print("=" * 80)
    print("INSPECTOR IA - ANÁLISIS DE RIESGO DE EJEMPLO")
    print("=" * 80)
    print()
    
    # 1. Crear datos de ejemplo
    print("📊 Preparando datos de ejemplo...")
    politician_data = create_example_politician()
    graph_data = create_example_graph_data()
    temporal_events = create_example_temporal_events()
    
    print(f"✅ Político: {politician_data['name']}")
    print(f"✅ Cargo: {politician_data['position']}")
    print(f"✅ Patrimonio declarado: ${politician_data['total_assets']:,.2f}")
    print(f"✅ Conexiones offshore: {len(graph_data['offshore_entities'])}")
    print(f"✅ Empresas fantasma detectadas: {len(graph_data['ghost_companies'])}")
    print(f"✅ Eventos temporales: {len(temporal_events)}")
    print()
    
    # 2. Inicializar calculador
    print("🔧 Inicializando calculador de riesgo...")
    risk_calculator = RiskCalculator()
    print("✅ Calculador inicializado")
    print()
    
    # 3. Realizar análisis
    print("🔍 Realizando análisis completo de riesgo...")
    print("   (Esto puede tomar unos segundos...)")
    print()
    
    analysis_result = risk_calculator.calculate_comprehensive_risk(
        politician_id=politician_data["id"],
        politician_data=politician_data,
        graph_data=graph_data,
        temporal_events=temporal_events
    )
    
    # 4. Mostrar resultados
    print("=" * 80)
    print("RESULTADOS DEL ANÁLISIS")
    print("=" * 80)
    print()
    
    ira_result = analysis_result['ira_result']
    
    print(f"🎯 ÍNDICE DE RIESGO DE ANOMALÍA (IRA): {ira_result['final_score']:.2f}/100")
    print(f"📊 Nivel de Riesgo: {ira_result['risk_color']} {ira_result['risk_level']}")
    print(f"🎓 Confianza del Análisis: {ira_result['confidence_level']*100:.1f}%")
    print(f"⚠️  Patrones de Fraude Detectados: {analysis_result['patterns_detected_count']}")
    print()
    
    print("-" * 80)
    print("DIMENSIONES DEL IRA")
    print("-" * 80)
    
    for dim_name, dim_data in ira_result['dimensions'].items():
        print(f"\n{dim_name.upper()}:")
        print(f"  Score: {dim_data['score']:.2f}/100")
        print(f"  Peso: {dim_data['weight']:.2%}")
        print(f"  Contribución: {dim_data['weighted_score']:.2f}")
        print(f"  Indicadores: {dim_data['indicators_count']}")
    
    print(f"\nBONUS DE COMPLEJIDAD DE RED: +{ira_result['network_bonus']:.2f}")
    print()
    
    print("-" * 80)
    print("PATRONES DE FRAUDE DETECTADOS")
    print("-" * 80)
    
    for pattern_name, pattern_data in analysis_result['fraud_patterns'].items():
        if pattern_data['pattern_detected']:
            print(f"\n✓ {pattern_data['pattern_name']}")
            print(f"  Score de Riesgo: {pattern_data['risk_score']:.2f}")
            print(f"  Confianza: {pattern_data['confidence']*100:.0f}%")
            print(f"  Indicadores: {len(pattern_data['indicators'])}")
    
    print()
    print("-" * 80)
    print("FACTORES CLAVE DE RIESGO")
    print("-" * 80)
    print()
    
    for i, factor in enumerate(ira_result['key_risk_factors'], 1):
        print(f"{i}. {factor}")
    
    print()
    print("-" * 80)
    print("RECOMENDACIONES")
    print("-" * 80)
    print()
    
    for i, rec in enumerate(ira_result['recommendations'][:5], 1):
        print(f"{i}. {rec}")
    
    print()
    print("=" * 80)
    print("RESUMEN EJECUTIVO")
    print("=" * 80)
    print()
    print(analysis_result['executive_summary'])
    
    # 5. Guardar reportes
    print()
    print("=" * 80)
    print("GUARDANDO REPORTES")
    print("=" * 80)
    print()
    
    # Guardar JSON
    json_filename = f"example_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(analysis_result, f, indent=2, ensure_ascii=False, default=str)
    print(f"✅ Reporte JSON guardado: {json_filename}")
    
    # Guardar Markdown
    md_filename = f"example_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(md_filename, 'w', encoding='utf-8') as f:
        f.write(analysis_result['formatted_report'])
    print(f"✅ Reporte Markdown guardado: {md_filename}")
    
    print()
    print("=" * 80)
    print("ANÁLISIS COMPLETADO")
    print("=" * 80)
    print()
    print("⚖️  DISCLAIMER LEGAL:")
    print("Este análisis identifica anomalías estadísticas basadas en datos públicos.")
    print("La presencia de anomalías NO implica actividad ilícita.")
    print("Se requiere investigación periodística adicional y verificación profesional.")
    print()
    print("Inspector IA es una herramienta de apoyo, no un sistema judicial.")
    print("=" * 80)


if __name__ == "__main__":
    try:
        run_example_analysis()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
