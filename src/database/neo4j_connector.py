"""
Inspector IA - Neo4j Graph Database Connector
==============================================

Conector para base de datos de grafos Neo4j.
Maneja conexiones, consultas Cypher, y operaciones CRUD.

Author: Inspector IA Core Team
Version: 2.0
Date: December 2024
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import logging
import os

try:
    from neo4j import GraphDatabase, Driver, Session
    from neo4j.exceptions import ServiceUnavailable, AuthError
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False
    logging.warning("neo4j driver not installed. Graph functionality will be limited.")


logger = logging.getLogger(__name__)


class Neo4jConnector:
    """
    Conector para base de datos Neo4j.
    
    Proporciona métodos para:
    - Gestión de conexiones
    - Ejecución de consultas Cypher
    - Operaciones CRUD en nodos y relaciones
    - Análisis de grafos
    """
    
    def __init__(
        self,
        uri: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        database: str = "neo4j"
    ):
        """
        Inicializa el conector Neo4j.
        
        Args:
            uri: URI de conexión (ej: bolt://localhost:7687)
            user: Usuario de Neo4j
            password: Contraseña
            database: Nombre de la base de datos
        """
        if not NEO4J_AVAILABLE:
            logger.warning("Neo4j driver not available. Using mock mode.")
            self.driver = None
            self.mock_mode = True
            return
        
        # Obtener credenciales de variables de entorno si no se proporcionan
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = user or os.getenv("NEO4J_USER", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "password")
        self.database = database
        
        self.driver: Optional[Driver] = None
        self.mock_mode = False
        
        # Intentar conectar
        self._connect()
    
    def _connect(self):
        """Establece conexión con Neo4j."""
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            # Verificar conexión
            self.driver.verify_connectivity()
            logger.info(f"✅ Conectado a Neo4j en {self.uri}")
        except (ServiceUnavailable, AuthError) as e:
            logger.error(f"❌ Error conectando a Neo4j: {e}")
            logger.warning("Operando en modo mock sin base de datos")
            self.mock_mode = True
            self.driver = None
    
    def close(self):
        """Cierra la conexión con Neo4j."""
        if self.driver:
            self.driver.close()
            logger.info("Conexión Neo4j cerrada")
    
    def execute_query(
        self,
        query: str,
        parameters: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Ejecuta una consulta Cypher.
        
        Args:
            query: Consulta Cypher
            parameters: Parámetros de la consulta
        
        Returns:
            Lista de resultados como diccionarios
        """
        if self.mock_mode:
            logger.warning("Mock mode: query not executed")
            return []
        
        parameters = parameters or {}
        
        try:
            with self.driver.session(database=self.database) as session:
                result = session.run(query, parameters)
                return [dict(record) for record in result]
        except Exception as e:
            logger.error(f"Error ejecutando query: {e}")
            raise
    
    def execute_write(
        self,
        query: str,
        parameters: Optional[Dict] = None
    ) -> Dict:
        """
        Ejecuta una consulta de escritura.
        
        Args:
            query: Consulta Cypher de escritura
            parameters: Parámetros de la consulta
        
        Returns:
            Resumen de la operación
        """
        if self.mock_mode:
            logger.warning("Mock mode: write not executed")
            return {"nodes_created": 0, "relationships_created": 0}
        
        parameters = parameters or {}
        
        try:
            with self.driver.session(database=self.database) as session:
                result = session.run(query, parameters)
                summary = result.consume()
                return {
                    "nodes_created": summary.counters.nodes_created,
                    "nodes_deleted": summary.counters.nodes_deleted,
                    "relationships_created": summary.counters.relationships_created,
                    "relationships_deleted": summary.counters.relationships_deleted,
                    "properties_set": summary.counters.properties_set
                }
        except Exception as e:
            logger.error(f"Error ejecutando write: {e}")
            raise
    
    # ==================== OPERACIONES CRUD ====================
    
    def create_politician_node(self, politician_data: Dict) -> str:
        """
        Crea un nodo de político en el grafo.
        
        Args:
            politician_data: Datos del político
        
        Returns:
            ID del nodo creado
        """
        query = """
        CREATE (p:Politico {
            id: $id,
            nombre: $nombre,
            cargo_actual: $cargo,
            partido: $partido,
            nivel_gobierno: $nivel,
            fecha_inicio_mandato: date($fecha_inicio),
            ingreso_anual: $ingreso,
            patrimonio_total: $patrimonio,
            created_at: datetime()
        })
        RETURN p.id as id
        """
        
        parameters = {
            "id": politician_data.get("id"),
            "nombre": politician_data.get("name"),
            "cargo": politician_data.get("position"),
            "partido": politician_data.get("party", ""),
            "nivel": politician_data.get("government_level", "nacional"),
            "fecha_inicio": politician_data.get("start_date", "2020-01-01"),
            "ingreso": politician_data.get("annual_income", 0),
            "patrimonio": politician_data.get("total_assets", 0)
        }
        
        result = self.execute_query(query, parameters)
        return result[0]["id"] if result else politician_data.get("id")
    
    def create_company_node(self, company_data: Dict) -> str:
        """
        Crea un nodo de empresa en el grafo.
        
        Args:
            company_data: Datos de la empresa
        
        Returns:
            ID del nodo creado
        """
        query = """
        CREATE (e:Empresa {
            id: $id,
            nombre: $nombre,
            rfc_cif: $rfc,
            fecha_constitucion: date($fecha),
            sector: $sector,
            es_offshore: $offshore,
            riesgo_fantasma: $riesgo,
            created_at: datetime()
        })
        RETURN e.id as id
        """
        
        parameters = {
            "id": company_data.get("id"),
            "nombre": company_data.get("name"),
            "rfc": company_data.get("tax_id", ""),
            "fecha": company_data.get("incorporation_date", "2000-01-01"),
            "sector": company_data.get("sector", ""),
            "offshore": company_data.get("is_offshore", False),
            "riesgo": company_data.get("ghost_risk_score", 0.0)
        }
        
        result = self.execute_query(query, parameters)
        return result[0]["id"] if result else company_data.get("id")
    
    def create_relationship(
        self,
        from_id: str,
        to_id: str,
        rel_type: str,
        properties: Optional[Dict] = None
    ) -> bool:
        """
        Crea una relación entre dos nodos.
        
        Args:
            from_id: ID del nodo origen
            to_id: ID del nodo destino
            rel_type: Tipo de relación
            properties: Propiedades de la relación
        
        Returns:
            True si se creó exitosamente
        """
        properties = properties or {}
        
        # Construir string de propiedades
        props_str = ", ".join([f"{k}: ${k}" for k in properties.keys()])
        if props_str:
            props_str = f"{{{props_str}, created_at: datetime()}}"
        else:
            props_str = "{created_at: datetime()}"
        
        query = f"""
        MATCH (a {{id: $from_id}})
        MATCH (b {{id: $to_id}})
        CREATE (a)-[r:{rel_type} {props_str}]->(b)
        RETURN r
        """
        
        parameters = {
            "from_id": from_id,
            "to_id": to_id,
            **properties
        }
        
        try:
            result = self.execute_query(query, parameters)
            return len(result) > 0
        except Exception as e:
            logger.error(f"Error creando relación: {e}")
            return False
    
    # ==================== CONSULTAS DE ANÁLISIS ====================
    
    def find_paths_to_contracts(
        self,
        politician_id: str,
        max_degrees: int = 3
    ) -> List[Dict]:
        """
        Encuentra caminos desde un político a contratos públicos.
        
        Args:
            politician_id: ID del político
            max_degrees: Máximo grados de separación
        
        Returns:
            Lista de caminos encontrados
        """
        query = f"""
        MATCH path = (p:Politico {{id: $politico_id}})-[*1..{max_degrees}]-(c:ContratoPublico)
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
            [n IN nodos | n.nombre] as node_names,
            [r IN relaciones | type(r)] as relationship_types,
            [r IN relaciones | properties(r)] as relationship_props,
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
        """
        
        try:
            results = self.execute_query(query, {"politico_id": politician_id})
            return results
        except Exception as e:
            logger.error(f"Error buscando caminos: {e}")
            return []
    
    def detect_ghost_companies(self) -> List[Dict]:
        """
        Detecta empresas fantasma en el grafo.
        
        Returns:
            Lista de empresas con características de fantasma
        """
        query = """
        MATCH (e:Empresa)
        OPTIONAL MATCH (e)-[:TIENE_CUENTA_BANCARIA]->(c)
        OPTIONAL MATCH (e)-[:ES_PROPIETARIO]->(a:Activo)
        OPTIONAL MATCH (e)-[:ADJUDICO]->(cont:ContratoPublico)
        WITH e, 
             count(c) as cuentas,
             count(a) as activos,
             count(cont) as contratos,
             collect(cont.monto_adjudicado) as montos_contratos
        WHERE cuentas = 0 
           OR activos = 0
           OR (contratos > 0 AND size(montos_contratos) > 0)
        WITH e, cuentas, activos, contratos,
            CASE 
                WHEN cuentas = 0 AND activos = 0 THEN 0.9
                WHEN cuentas = 0 OR activos = 0 THEN 0.6
                WHEN contratos > 0 THEN 0.4
                ELSE 0.1
            END as riesgo_calculado
        SET e.riesgo_fantasma = riesgo_calculado
        RETURN e.id as id, e.nombre as nombre, e.riesgo_fantasma as riesgo
        ORDER BY riesgo DESC
        """
        
        try:
            results = self.execute_query(query)
            return results
        except Exception as e:
            logger.error(f"Error detectando empresas fantasma: {e}")
            return []
    
    def find_temporal_coincidences(
        self,
        politician_id: str,
        days_window: int = 90
    ) -> List[Dict]:
        """
        Encuentra coincidencias temporales entre eventos.
        
        Args:
            politician_id: ID del político
            days_window: Ventana de días para considerar coincidencia
        
        Returns:
            Lista de coincidencias encontradas
        """
        query = f"""
        MATCH (p:Politico {{id: $politico_id}})-[:ASISTIO_A]->(r:ReunionOficial)
        MATCH (e:Empresa)-[:ADJUDICO]->(c:ContratoPublico)
        MATCH path = shortestPath((p)-[*1..3]-(e))
        WHERE date(r.fecha) >= date(c.fecha_adjudicacion) - duration('P{days_window}D')
          AND date(r.fecha) <= date(c.fecha_adjudicacion) + duration('P30D')
        WITH p, e, c, r, path,
             duration.between(date(r.fecha), date(c.fecha_adjudicacion)).days as dias_diferencia
        RETURN 
            p.nombre as politico,
            e.nombre as empresa,
            c.numero_expediente as contrato,
            c.monto_adjudicado as monto,
            r.fecha as fecha_reunion,
            c.fecha_adjudicacion as fecha_adjudicacion,
            abs(dias_diferencia) as dias_entre_eventos,
            [n IN nodes(path) | n.nombre] as camino,
            [rel IN relationships(path) | type(rel)] as relaciones
        ORDER BY abs(dias_diferencia) ASC
        LIMIT 20
        """
        
        try:
            results = self.execute_query(query, {"politico_id": politician_id})
            return results
        except Exception as e:
            logger.error(f"Error buscando coincidencias temporales: {e}")
            return []
    
    def get_network_statistics(self, politician_id: str) -> Dict:
        """
        Obtiene estadísticas de la red de un político.
        
        Args:
            politician_id: ID del político
        
        Returns:
            Diccionario con estadísticas
        """
        query = """
        MATCH (p:Politico {id: $politico_id})
        OPTIONAL MATCH (p)-[r1]-(:PersonaNatural)
        OPTIONAL MATCH (p)-[r2]-(:Empresa)
        OPTIONAL MATCH (p)-[r3]-(:ContratoPublico)
        OPTIONAL MATCH (p)-[*1..2]-(offshore:Empresa {es_offshore: true})
        RETURN 
            count(DISTINCT r1) as relaciones_personales,
            count(DISTINCT r2) as relaciones_empresariales,
            count(DISTINCT r3) as contratos_directos,
            count(DISTINCT offshore) as conexiones_offshore
        """
        
        try:
            results = self.execute_query(query, {"politico_id": politician_id})
            if results:
                return results[0]
            return {
                "relaciones_personales": 0,
                "relaciones_empresariales": 0,
                "contratos_directos": 0,
                "conexiones_offshore": 0
            }
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {}
    
    # ==================== UTILIDADES ====================
    
    def clear_database(self):
        """
        PELIGRO: Elimina todos los nodos y relaciones.
        Solo para desarrollo/testing.
        """
        if self.mock_mode:
            logger.warning("Mock mode: database not cleared")
            return
        
        query = "MATCH (n) DETACH DELETE n"
        logger.warning("⚠️  Eliminando toda la base de datos...")
        self.execute_write(query)
        logger.info("✅ Base de datos limpiada")
    
    def create_indexes(self):
        """Crea índices para mejorar el rendimiento."""
        indexes = [
            "CREATE INDEX politician_id IF NOT EXISTS FOR (p:Politico) ON (p.id)",
            "CREATE INDEX empresa_id IF NOT EXISTS FOR (e:Empresa) ON (e.id)",
            "CREATE INDEX contrato_id IF NOT EXISTS FOR (c:ContratoPublico) ON (c.id)",
            "CREATE INDEX persona_id IF NOT EXISTS FOR (p:PersonaNatural) ON (p.id)"
        ]
        
        for index_query in indexes:
            try:
                self.execute_write(index_query)
                logger.info(f"✅ Índice creado")
            except Exception as e:
                logger.warning(f"Índice ya existe o error: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# ==================== FUNCIONES DE UTILIDAD ====================

def get_neo4j_connector() -> Neo4jConnector:
    """
    Factory function para obtener un conector Neo4j.
    
    Returns:
        Instancia de Neo4jConnector
    """
    return Neo4jConnector()
