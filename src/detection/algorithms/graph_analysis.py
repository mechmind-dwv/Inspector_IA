"""
Inspector IA - Graph Analysis and Explainable AI System
========================================================

This module implements the complete graph-based network analysis system
with integrated explainable AI for investigative journalism.

Author: Inspector IA Core Team
Version: 2.0
Date: December 2024
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import hashlib
import json
from collections import defaultdict


# ==================== DATA STRUCTURES ====================

class NodeType(Enum):
    """Types of nodes in the influence graph."""
    POLITICIAN = "Politico"
    NATURAL_PERSON = "PersonaNatural"
    COMPANY = "Empresa"
    PUBLIC_CONTRACT = "ContratoPublico"
    ASSET = "Activo"
    OFFICIAL_MEETING = "ReunionOficial"


class RelationType(Enum):
    """Types of relationships in the influence graph."""
    # Personal relationships
    IS_SPOUSE = "ES_CONYUGE"
    IS_CHILD = "ES_HIJO"
    IS_SIBLING = "ES_HERMANO"
    IS_COUSIN = "ES_PRIMO"
    IS_PERSONAL_ASSOCIATE = "ES_SOCIO_PERSONAL"
    
    # Business relationships
    IS_LEGAL_REPRESENTATIVE = "ES_APODERADO"
    IS_ADMINISTRATOR = "ES_ADMINISTRADOR"
    IS_OWNER = "ES_PROPIETARIO"
    HAS_BANK_ACCOUNT = "TIENE_CUENTA_BANCARIA"
    
    # Contract relationships
    AWARDED_CONTRACT = "ADJUDICO"
    SUBCONTRACTED = "SUBCONTRATO"
    MODIFIED_CONTRACT = "MODIFICO_CONTRATO"
    
    # Temporal relationships
    ATTENDED_MEETING = "ASISTIO_A"
    VOTED_IN_FAVOR = "VOTO_A_FAVOR"


@dataclass
class GraphNode:
    """Represents a node in the influence graph."""
    id: str
    node_type: NodeType
    properties: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_neo4j_dict(self) -> Dict:
        """Convert node to Neo4j format."""
        return {
            "id": self.id,
            "type": self.node_type.value,
            **self.properties,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class GraphRelationship:
    """Represents a relationship in the influence graph."""
    from_node_id: str
    to_node_id: str
    relationship_type: RelationType
    properties: Dict[str, Any] = field(default_factory=dict)
    weight: float = 1.0
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_neo4j_dict(self) -> Dict:
        """Convert relationship to Neo4j format."""
        return {
            "from": self.from_node_id,
            "to": self.to_node_id,
            "type": self.relationship_type.value,
            "weight": self.weight,
            **self.properties,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class PathAnalysis:
    """Results of analyzing a path through the graph."""
    path_nodes: List[GraphNode]
    path_relationships: List[GraphRelationship]
    separation_degrees: int
    total_weight: float
    monetary_amount: float
    ghost_companies: int
    temporal_correlation: Optional[float] = None
    risk_score: float = 0.0


# ==================== XAI EXPLANATION ENGINE ====================

class GraphXAIExplainer:
    """
    Explainable AI engine for graph-based anomaly detection.
    
    Generates human-readable explanations for risk scores based on
    graph analysis, suitable for investigative journalists.
    """
    
    def __init__(self, graph_connection):
        """
        Initialize the XAI explainer.
        
        Args:
            graph_connection: Connection to Neo4j or compatible graph database
        """
        self.graph = graph_connection
        self.relationship_weights = self._initialize_relationship_weights()
    
    def _initialize_relationship_weights(self) -> Dict[RelationType, float]:
        """Define risk weights for different relationship types."""
        return {
            RelationType.IS_OWNER: 2.0,
            RelationType.IS_ADMINISTRATOR: 1.5,
            RelationType.IS_LEGAL_REPRESENTATIVE: 1.2,
            RelationType.AWARDED_CONTRACT: 2.5,
            RelationType.IS_SPOUSE: 1.8,
            RelationType.IS_CHILD: 1.5,
            RelationType.IS_SIBLING: 1.3,
            RelationType.IS_PERSONAL_ASSOCIATE: 1.0,
            RelationType.HAS_BANK_ACCOUNT: 0.8,
            RelationType.ATTENDED_MEETING: 0.6,
            RelationType.MODIFIED_CONTRACT: 2.0
        }
    
    def generate_risk_explanation(
        self,
        politician_id: str,
        ira_score: float
    ) -> Dict[str, Any]:
        """
        Generate comprehensive explanation for politician's risk score.
        
        Args:
            politician_id: Unique identifier for politician
            ira_score: Calculated IRA score (0-100)
            
        Returns:
            Dictionary containing structured explanation with narrative
        """
        # Find suspicious paths to public contracts
        suspicious_paths = self.find_contract_paths(politician_id)
        
        # Analyze each path
        path_analyses = []
        for path in suspicious_paths[:5]:  # Top 5 most suspicious
            analysis = self.analyze_path(path)
            path_analyses.append(analysis)
        
        # Generate natural language narrative
        narrative = self.build_narrative(
            politician_id,
            path_analyses,
            ira_score
        )
        
        # Compile explanation package
        return {
            "politician_id": politician_id,
            "ira_score": ira_score,
            "risk_level": self._classify_risk_level(ira_score),
            "narrative": narrative,
            "path_analyses": [self._serialize_path_analysis(pa) for pa in path_analyses],
            "key_findings": self._extract_key_findings(path_analyses),
            "recommended_actions": self._generate_recommendations(path_analyses, ira_score),
            "data_sources": self._list_data_sources(path_analyses),
            "timestamp": datetime.now().isoformat()
        }
    
    def find_contract_paths(
        self,
        politician_id: str,
        max_degrees: int = 3
    ) -> List[List[str]]:
        """
        Find all paths from politician to public contracts.
        
        Uses Neo4j Cypher query to identify connection paths through
        the influence network.
        
        Args:
            politician_id: Politician's unique identifier
            max_degrees: Maximum degrees of separation to search
            
        Returns:
            List of paths (each path is list of node IDs)
        """
        query = """
        MATCH path = (p:Politico {id: $politico_id})-[*1..{max_degrees}]-(c:ContratoPublico)
        WHERE NONE(
            rel IN relationships(path) 
            WHERE type(rel) = 'ES_CONYUGE' AND rel.estado = 'divorciado'
        )
        WITH path, 
             nodes(path) as nodos,
             relationships(path) as relaciones,
             length(path) as distancia
        WHERE distancia <= {max_degrees}
        RETURN 
            [n IN nodos | n.id] as node_ids,
            [n IN nodos | labels(n)[0]] as node_types,
            [r IN relaciones | type(r)] as relationship_types,
            [r IN relaciones | r] as relationship_props,
            distancia,
            reduce(
                score = 0.0, 
                r IN relaciones | 
                score + CASE type(r)
                    WHEN 'ES_PROPIETARIO' THEN 2.0
                    WHEN 'ES_ADMINISTRADOR' THEN 1.5
                    WHEN 'ES_APODERADO' THEN 1.2
                    WHEN 'ADJUDICO' THEN 2.5
                    ELSE 0.5
                END
            ) as weight_score
        ORDER BY weight_score DESC, distancia ASC
        LIMIT 10
        """.format(max_degrees=max_degrees)
        
        results = self.graph.execute_query(query, {"politico_id": politician_id})
        return self._parse_path_results(results)
    
    def analyze_path(self, path_data: Dict) -> PathAnalysis:
        """
        Analyze a specific path for risk indicators.
        
        Args:
            path_data: Path information from Neo4j query
            
        Returns:
            PathAnalysis object with detailed metrics
        """
        node_ids = path_data["node_ids"]
        rel_types = path_data["relationship_types"]
        rel_props = path_data["relationship_props"]
        
        metrics = {
            "separation_degrees": len(node_ids) - 1,
            "relationship_types": [],
            "monetary_amount": 0.0,
            "timeline": [],
            "ghost_companies": 0,
            "temporal_correlations": []
        }
        
        # Analyze each relationship in path
        for i, rel_type in enumerate(rel_types):
            metrics["relationship_types"].append(rel_type)
            
            # Extract monetary amounts
            if "monto" in rel_props[i]:
                metrics["monetary_amount"] += rel_props[i]["monto"]
            
            # Extract temporal information
            if "fecha" in rel_props[i]:
                metrics["timeline"].append(rel_props[i]["fecha"])
        
        # Check for ghost companies in path
        for node_id in node_ids:
            if self._is_ghost_company(node_id):
                metrics["ghost_companies"] += 1
        
        # Calculate temporal correlation
        if len(metrics["timeline"]) >= 2:
            metrics["temporal_correlation"] = self._calculate_temporal_correlation(
                metrics["timeline"]
            )
        
        # Calculate overall path risk score
        risk_score = self._calculate_path_risk_score(metrics)
        
        # Convert to PathAnalysis object
        return PathAnalysis(
            path_nodes=self._load_nodes(node_ids),
            path_relationships=self._load_relationships(rel_props),
            separation_degrees=metrics["separation_degrees"],
            total_weight=path_data["weight_score"],
            monetary_amount=metrics["monetary_amount"],
            ghost_companies=metrics["ghost_companies"],
            temporal_correlation=metrics.get("temporal_correlation"),
            risk_score=risk_score
        )
    
    def build_narrative(
        self,
        politician_id: str,
        path_analyses: List[PathAnalysis],
        ira_score: float
    ) -> str:
        """
        Build natural language explanation of findings.
        
        Args:
            politician_id: Politician identifier
            path_analyses: List of analyzed paths
            ira_score: Overall IRA score
            
        Returns:
            Markdown-formatted narrative explanation
        """
        politician_name = self._get_politician_name(politician_id)
        risk_level = self._classify_risk_level(ira_score)
        
        narrative = f"# Análisis de Red: {politician_name}\n\n"
        narrative += f"**Índice de Riesgo de Anomalía (IRA):** {ira_score:.1f}/100\n"
        narrative += f"**Nivel de Riesgo:** {risk_level}\n\n"
        
        narrative += "## Resumen Ejecutivo\n\n"
        narrative += self._generate_executive_summary(path_analyses, ira_score)
        narrative += "\n\n"
        
        narrative += "## Hallazgos Principales\n\n"
        
        for idx, analysis in enumerate(path_analyses[:3], 1):
            narrative += f"### Conexión #{idx}: "
            narrative += f"{analysis.separation_degrees} Grados de Separación\n\n"
            
            # Describe the connection path
            narrative += self._describe_path(analysis)
            narrative += "\n"
            
            # Highlight monetary amounts
            if analysis.monetary_amount > 0:
                narrative += f"**Montos Involucrados:** "
                narrative += f"${analysis.monetary_amount:,.2f}\n\n"
            
            # Flag ghost companies
            if analysis.ghost_companies > 0:
                narrative += f"⚠️ **Alerta:** Detectadas {analysis.ghost_companies} "
                narrative += "empresas con indicadores de baja actividad operativa\n\n"
            
            # Temporal correlation
            if analysis.temporal_correlation and analysis.temporal_correlation > 0.7:
                narrative += f"📅 **Correlación Temporal Significativa:** "
                narrative += f"{analysis.temporal_correlation:.0%}\n\n"
        
        # Add methodology note
        narrative += "---\n\n"
        narrative += "## Metodología y Limitaciones\n\n"
        narrative += self._generate_methodology_note()
        
        # Legal disclaimer
        narrative += "\n\n## Aviso Legal\n\n"
        narrative += self._generate_legal_disclaimer()
        
        return narrative
    
    def _describe_path(self, analysis: PathAnalysis) -> str:
        """Generate natural language description of connection path."""
        description = "**Ruta de Conexión:**\n\n"
        
        for i, node in enumerate(analysis.path_nodes):
            # Add node description
            description += f"{i+1}. **{node.properties.get('nombre', 'Unknown')}** "
            description += f"({self._translate_node_type(node.node_type)})"
            
            # Add relationship description if not last node
            if i < len(analysis.path_relationships):
                rel = analysis.path_relationships[i]
                description += f"\n   → *{self._translate_relationship(rel.relationship_type)}*"
                
                # Add relationship details
                if rel.properties.get("porcentaje"):
                    description += f" ({rel.properties['porcentaje']:.1f}%)"
                if rel.properties.get("monto"):
                    description += f" (${rel.properties['monto']:,.0f})"
            
            description += "\n"
        
        return description
    
    def _generate_executive_summary(
        self,
        path_analyses: List[PathAnalysis],
        ira_score: float
    ) -> str:
        """Generate executive summary of findings."""
        total_paths = len(path_analyses)
        avg_separation = sum(p.separation_degrees for p in path_analyses) / max(total_paths, 1)
        total_amount = sum(p.monetary_amount for p in path_analyses)
        total_ghost = sum(p.ghost_companies for p in path_analyses)
        
        summary = f"El análisis de red ha identificado **{total_paths} conexiones** "
        summary += f"entre el político y contratos públicos, con una separación "
        summary += f"promedio de **{avg_separation:.1f} grados**. "
        
        if total_amount > 0:
            summary += f"Los montos totales involucrados ascienden a "
            summary += f"**${total_amount:,.2f}**. "
        
        if total_ghost > 0:
            summary += f"\n\n⚠️ Se han detectado **{total_ghost} empresas** con "
            summary += "características de baja actividad operativa en las rutas analizadas. "
        
        summary += f"\n\nEl puntaje IRA de **{ira_score:.1f}** sugiere un nivel "
        summary += f"**{self._classify_risk_level(ira_score).lower()}** de anomalías "
        summary += "que requiere verificación periodística adicional."
        
        return summary
    
    def _generate_methodology_note(self) -> str:
        """Generate methodology explanation."""
        return (
            "Este análisis utiliza técnicas de teoría de grafos para identificar "
            "conexiones entre figuras públicas y contratos gubernamentales a través "
            "de registros públicos. Los grados de separación miden la distancia en "
            "la red entre el político y el contrato.\n\n"
            "Las métricas de riesgo se calculan considerando:\n"
            "- Proximidad de las conexiones (grados de separación)\n"
            "- Naturaleza de las relaciones (propiedad, administración, representación)\n"
            "- Montos monetarios involucrados\n"
            "- Presencia de entidades con baja actividad operativa\n"
            "- Correlaciones temporales entre eventos"
        )
    
    def _generate_legal_disclaimer(self) -> str:
        """Generate legal disclaimer."""
        return (
            "*Este análisis identifica conexiones documentadas en registros públicos "
            "y no constituye evidencia de actividad ilícita. La presencia de conexiones "
            "no implica conducta fraudulenta. Este reporte está diseñado como herramienta "
            "de investigación periodística y requiere verificación adicional antes de "
            "cualquier publicación. Los periodistas deben ejercer criterio profesional "
            "y contrastar la información con múltiples fuentes.*"
        )
    
    def _classify_risk_level(self, ira_score: float) -> str:
        """Classify IRA score into risk level."""
        if ira_score >= 86:
            return "Black Hole Critical"
        elif ira_score >= 71:
            return "Supernova Alert"
        elif ira_score >= 51:
            return "Stellar Anomaly"
        elif ira_score >= 21:
            return "Nebular Suspicion"
        else:
            return "Cosmic Background"
    
    def _extract_key_findings(self, path_analyses: List[PathAnalysis]) -> List[Dict]:
        """Extract key findings from path analyses."""
        findings = []
        
        # Finding 1: Closest connection
        if path_analyses:
            closest = min(path_analyses, key=lambda p: p.separation_degrees)
            findings.append({
                "type": "closest_connection",
                "description": f"Conexión más cercana con {closest.separation_degrees} grados",
                "severity": "high" if closest.separation_degrees <= 2 else "medium"
            })
        
        # Finding 2: Highest monetary value
        highest_value = max(
            path_analyses,
            key=lambda p: p.monetary_amount,
            default=None
        )
        if highest_value and highest_value.monetary_amount > 100000:
            findings.append({
                "type": "high_value_connection",
                "description": f"Conexión de alto valor: ${highest_value.monetary_amount:,.0f}",
                "severity": "high"
            })
        
        # Finding 3: Ghost companies
        total_ghost = sum(p.ghost_companies for p in path_analyses)
        if total_ghost > 0:
            findings.append({
                "type": "ghost_companies",
                "description": f"{total_ghost} empresas con baja actividad detectadas",
                "severity": "high"
            })
        
        return findings
    
    def _generate_recommendations(
        self,
        path_analyses: List[PathAnalysis],
        ira_score: float
    ) -> List[str]:
        """Generate recommended actions for journalists."""
        recommendations = []
        
        if ira_score >= 71:
            recommendations.append(
                "Priorizar investigación en profundidad con solicitudes de información adicional"
            )
        
        if any(p.ghost_companies > 0 for p in path_analyses):
            recommendations.append(
                "Verificar actividad operativa real de empresas identificadas"
            )
        
        if any(p.separation_degrees <= 2 for p in path_analyses):
            recommendations.append(
                "Solicitar declaraciones al político sobre conexiones de primer/segundo grado"
            )
        
        recommendations.append(
            "Contrastar hallazgos con expertos en contratación pública"
        )
        
        return recommendations
    
    def _list_data_sources(self, path_analyses: List[PathAnalysis]) -> List[Dict]:
        """List data sources used in analysis."""
        sources = [
            {
                "type": "registro_mercantil",
                "description": "Registro Mercantil Central",
                "url": "https://example.com/registro"
            },
            {
                "type": "contratos_publicos",
                "description": "Plataforma de Contratación del Estado",
                "url": "https://example.com/contratos"
            },
            {
                "type": "declaraciones_patrimonio",
                "description": "Portal de Transparencia",
                "url": "https://example.com/transparencia"
            }
        ]
        return sources
    
    # Helper methods (would be implemented with actual graph queries)
    
    def _parse_path_results(self, results: List[Dict]) -> List[Dict]:
        """Parse results from Neo4j query."""
        # Implementation would parse actual Neo4j results
        return results
    
    def _is_ghost_company(self, node_id: str) -> bool:
        """Check if company shows ghost company indicators."""
        # Query graph for ghost company indicators
        query = """
        MATCH (e:Empresa {id: $node_id})
        OPTIONAL MATCH (e)-[:TIENE_CUENTA_BANCARIA]->(c)
        OPTIONAL MATCH (e)-[:ES_PROPIETARIO]->(a:Activo)
        WITH e, count(c) as cuentas, count(a) as activos
        RETURN e.riesgo_fantasma > 0.5 
               OR (cuentas = 0 AND activos = 0) as is_ghost
        """
        result = self.graph.execute_query(query, {"node_id": node_id})
        return result[0]["is_ghost"] if result else False
    
    def _calculate_temporal_correlation(self, timeline: List[datetime]) -> float:
        """Calculate temporal correlation score."""
        if len(timeline) < 2:
            return 0.0
        
        # Calculate time differences
        sorted_times = sorted(timeline)
        differences = [
            (sorted_times[i+1] - sorted_times[i]).days
            for i in range(len(sorted_times) - 1)
        ]
        
        # High correlation if events occur within 90 days
        correlation = sum(1 for d in differences if d <= 90) / len(differences)
        return correlation
    
    def _calculate_path_risk_score(self, metrics: Dict) -> float:
        """Calculate risk score for a path."""
        score = 0.0
        
        # Proximity factor (closer = higher risk)
        proximity_score = max(0, 100 - (metrics["separation_degrees"] * 20))
        score += proximity_score * 0.3
        
        # Monetary amount factor
        if metrics["monetary_amount"] > 1000000:
            score += 30
        elif metrics["monetary_amount"] > 500000:
            score += 20
        elif metrics["monetary_amount"] > 100000:
            score += 10
        
        # Ghost company factor
        score += metrics["ghost_companies"] * 15
        
        # Temporal correlation factor
        if metrics.get("temporal_correlation", 0) > 0.7:
            score += 25
        
        return min(100, score)
    
    def _load_nodes(self, node_ids: List[str]) -> List[GraphNode]:
        """Load node objects from graph."""
        # Would query graph database to load full node objects
        nodes = []
        for node_id in node_ids:
            # Placeholder - would load from actual database
            node = GraphNode(
                id=node_id,
                node_type=NodeType.COMPANY,  # Would determine actual type
                properties={"nombre": f"Entity {node_id}"}
            )
            nodes.append(node)
        return nodes
    
    def _load_relationships(self, rel_props: List[Dict]) -> List[GraphRelationship]:
        """Load relationship objects."""
        relationships = []
        for props in rel_props:
            rel = GraphRelationship(
                from_node_id=props.get("from", ""),
                to_node_id=props.get("to", ""),
                relationship_type=RelationType.IS_OWNER,  # Would determine actual type
                properties=props
            )
            relationships.append(rel)
        return relationships
    
    def _get_politician_name(self, politician_id: str) -> str:
        """Get politician name from graph."""
        query = "MATCH (p:Politico {id: $id}) RETURN p.nombre as nombre"
        result = self.graph.execute_query(query, {"id": politician_id})
        return result[0]["nombre"] if result else "Unknown"
    
    def _translate_node_type(self, node_type: NodeType) -> str:
        """Translate node type to Spanish."""
        translations = {
            NodeType.POLITICIAN: "Político",
            NodeType.NATURAL_PERSON: "Persona Natural",
            NodeType.COMPANY: "Empresa",
            NodeType.PUBLIC_CONTRACT: "Contrato Público",
            NodeType.ASSET: "Activo",
            NodeType.OFFICIAL_MEETING: "Reunión Oficial"
        }
        return translations.get(node_type, str(node_type))
    
    def _translate_relationship(self, rel_type: RelationType) -> str:
        """Translate relationship type to Spanish."""
        translations = {
            RelationType.IS_OWNER: "Es propietario de",
            RelationType.IS_ADMINISTRATOR: "Es administrador de",
            RelationType.IS_LEGAL_REPRESENTATIVE: "Es apoderado de",
            RelationType.AWARDED_CONTRACT: "Adjudicó contrato a",
            RelationType.IS_SPOUSE: "Es cónyuge de",
            RelationType.IS_CHILD: "Es hijo/a de",
            RelationType.IS_SIBLING: "Es hermano/a de"
        }
        return translations.get(rel_type, str(rel_type))
    
    def _serialize_path_analysis(self, analysis: PathAnalysis) -> Dict:
        """Serialize PathAnalysis for JSON export."""
        return {
            "separation_degrees": analysis.separation_degrees,
            "total_weight": analysis.total_weight,
            "monetary_amount": analysis.monetary_amount,
            "ghost_companies": analysis.ghost_companies,
            "temporal_correlation": analysis.temporal_correlation,
            "risk_score": analysis.risk_score,
            "path_length": len(analysis.path_nodes)
        }


# ==================== USAGE EXAMPLE ====================

def demonstrate_xai_system():
    """Demonstrate the Graph XAI system."""
    
    print("=" * 80)
    print("Inspector IA - Graph XAI System Demonstration")
    print("=" * 80)
    print()
    
    # Mock graph connection
    class MockGraphConnection:
        def execute_query(self, query: str, params: Dict) -> List[Dict]:
            # Return mock data
            return [{
                "node_ids": ["POL_001", "FAM_001", "EMP_001", "CON_001"],
                "node_types": ["Politico", "PersonaNatural", "Empresa", "ContratoPublico"],
                "relationship_types": ["ES_CONYUGE", "ES_PROPIETARIO", "ADJUDICO"],
                "relationship_props": [
                    {"desde": "2010-01-01"},
                    {"porcentaje": 60.0},
                    {"monto": 500000, "fecha": "2023-06-15"}
                ],
                "weight_score": 6.3
            }]
    
    # Initialize XAI explainer
    graph_conn = MockGraphConnection()
    explainer = GraphXAIExplainer(graph_conn)
    
    # Generate explanation
    print("Generating risk explanation for politician POL_001...")
    print()
    
    explanation = explainer.generate_risk_explanation(
        politician_id="POL_001",
        ira_score=72.5
    )
    
    print("IRA Score:", explanation["ira_score"])
    print("Risk Level:", explanation["risk_level"])
    print()
    print("Narrative:")
    print("-" * 80)
    print(explanation["narrative"])
    print()
    print("=" * 80)
    print("✅ XAI explanation generated successfully!")
    print("=" * 80)


if __name__ == "__main__":
    demonstrate_xai_system()
