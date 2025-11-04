#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 LOCAL KNOWLEDGE GRAPH - FASE 2 OPTIMIZACIÓN ARIA CEREBRO
Sistema de knowledge graph local Neo4j para 15-25% mejora precisión

Implementación 100% Open Source para búsqueda graph-enhanced
Fecha: 11 Agosto 2025
Autorizado por: Ricardo (Episode 477)
"""

import asyncio
import json
import logging
import time
from typing import Any, Dict, List, Optional, Tuple, Union
from datetime import datetime, timedelta
import hashlib

try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False

logger = logging.getLogger(__name__)

class LocalKnowledgeGraph:
    """
    Sistema de Knowledge Graph local usando Neo4j:
    - Creación automática de nodos y relaciones desde episodes
    - Búsqueda graph-enhanced que combina vector + graph traversal
    - Análisis de patrones y descubrimiento de conexiones
    - 100% local sin dependencias externas
    """
    
    def __init__(self, config=None):
        self.config = config or {
            'neo4j_uri': 'bolt://localhost:7687',
            'neo4j_user': 'neo4j',
            'neo4j_password': 'aria_knowledge_2025',
            'max_traversal_depth': 3,
            'min_relationship_strength': 0.3,
            'batch_size': 100
        }
        
        # Cliente Neo4j
        self.driver = None
        self.is_initialized = False
        
        # NetworkX para análisis adicional
        self.nx_graph = None if not NETWORKX_AVAILABLE else nx.MultiDiGraph()
        
        # Métricas
        self.metrics = {
            'nodes_created': 0,
            'relationships_created': 0,
            'graph_queries': 0,
            'traversals_performed': 0,
            'patterns_discovered': 0,
            'query_time_ms': []
        }
        
    async def initialize(self):
        """Inicializar conexión a Neo4j y estructuras"""
        logger.info("🌐 Initializing Local Knowledge Graph System...")
        
        if not NEO4J_AVAILABLE:
            logger.error("❌ Neo4j driver not available")
            return False
        
        try:
            # Conectar a Neo4j
            self.driver = GraphDatabase.driver(
                self.config['neo4j_uri'],
                auth=(self.config['neo4j_user'], self.config['neo4j_password']),
                max_connection_lifetime=3600,
                max_connection_pool_size=10
            )
            
            # Test conexión
            with self.driver.session() as session:
                result = session.run("RETURN 1 as test")
                result.single()
            
            logger.info("✅ Neo4j connection established successfully")
            
            # Crear índices y constraints
            await self._create_schema()
            
            self.is_initialized = True
            logger.info("🎯 Knowledge Graph System initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Knowledge Graph: {e}")
            return False
    
    async def _create_schema(self):
        """Crear esquema básico de nodos y índices"""
        
        schema_commands = [
            # Constraints para nodos únicos
            "CREATE CONSTRAINT IF NOT EXISTS FOR (e:Episode) REQUIRE e.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (a:Agent) REQUIRE a.id IS UNIQUE", 
            "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Project) REQUIRE p.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Concept) REQUIRE c.name IS UNIQUE",
            
            # Índices para performance
            "CREATE INDEX IF NOT EXISTS FOR (e:Episode) ON (e.timestamp)",
            "CREATE INDEX IF NOT EXISTS FOR (e:Episode) ON (e.importance_score)",
            "CREATE INDEX IF NOT EXISTS FOR (e:Episode) ON (e.action_type)",
            "CREATE INDEX IF NOT EXISTS FOR (r:RELATES_TO) ON (r.strength)",
        ]
        
        try:
            with self.driver.session() as session:
                for command in schema_commands:
                    session.run(command)
            
            logger.info("✅ Knowledge Graph schema created successfully")
        except Exception as e:
            logger.warning(f"⚠️ Schema creation warning: {e}")
    
    async def create_memory_graph(self, episodes: List[Dict]) -> Dict[str, Any]:
        """
        Crear knowledge graph desde episodes de memoria
        
        Args:
            episodes: Lista de episodes a procesar
            
        Returns:
            Estadísticas de creación del grafo
        """
        if not self.is_initialized:
            raise RuntimeError("System not initialized. Call initialize() first.")
        
        start_time = time.time()
        logger.info(f"🏗️ Creating memory graph from {len(episodes)} episodes")
        
        stats = {
            'timestamp': datetime.utcnow().isoformat(),
            'episodes_processed': 0,
            'nodes_created': 0,
            'relationships_created': 0,
            'errors': 0
        }
        
        try:
            # Procesar en batches
            for i in range(0, len(episodes), self.config['batch_size']):
                batch = episodes[i:i + self.config['batch_size']]
                batch_stats = await self._process_episode_batch(batch)
                
                stats['episodes_processed'] += batch_stats['episodes_processed']
                stats['nodes_created'] += batch_stats['nodes_created']
                stats['relationships_created'] += batch_stats['relationships_created']
                stats['errors'] += batch_stats['errors']
        
            # Crear relaciones adicionales basadas en patrones
            await self._create_pattern_relationships()
            
            processing_time = (time.time() - start_time) * 1000
            stats['processing_time_ms'] = processing_time
            
            # Actualizar métricas
            self.metrics['nodes_created'] += stats['nodes_created']
            self.metrics['relationships_created'] += stats['relationships_created']
            
            logger.info(f"✅ Memory graph created in {processing_time:.2f}ms")
            logger.info(f"📊 Stats: {stats['nodes_created']} nodes, {stats['relationships_created']} relationships")
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Memory graph creation error: {e}")
            stats['error'] = str(e)
            return stats
    
    async def _process_episode_batch(self, episodes: List[Dict]) -> Dict[str, int]:
        """Procesar batch de episodes"""
        
        batch_stats = {
            'episodes_processed': 0,
            'nodes_created': 0,
            'relationships_created': 0,
            'errors': 0
        }
        
        try:
            with self.driver.session() as session:
                for episode in episodes:
                    try:
                        # Crear nodo Episode
                        episode_result = await self._create_episode_node(session, episode)
                        if episode_result:
                            batch_stats['nodes_created'] += 1
                        
                        # Extraer y crear entidades relacionadas
                        entities = self._extract_entities_from_episode(episode)
                        
                        for entity in entities:
                            # Crear nodo de entidad
                            entity_result = await self._create_entity_node(session, entity)
                            if entity_result:
                                batch_stats['nodes_created'] += 1
                            
                            # Crear relación Episode -> Entity
                            rel_result = await self._create_relationship(
                                session, 
                                episode['id'], 
                                entity['id'],
                                entity.get('relationship_type', 'MENTIONS'),
                                entity.get('strength', 0.5)
                            )
                            if rel_result:
                                batch_stats['relationships_created'] += 1
                        
                        batch_stats['episodes_processed'] += 1
                        
                    except Exception as e:
                        logger.warning(f"Episode processing error {episode.get('id')}: {e}")
                        batch_stats['errors'] += 1
        
        except Exception as e:
            logger.error(f"Batch processing error: {e}")
            batch_stats['errors'] += len(episodes)
        
        return batch_stats
    
    async def _create_episode_node(self, session, episode: Dict) -> bool:
        """Crear nodo Episode en Neo4j"""
        
        try:
            query = """
            MERGE (e:Episode {id: $episode_id})
            SET e.action_type = $action_type,
                e.timestamp = datetime($timestamp),
                e.importance_score = $importance,
                e.agent_id = $agent_id,
                e.tags = $tags,
                e.created_at = datetime(),
                e.action_summary = $action_summary
            RETURN e.id as id
            """
            
            # Preparar datos
            action_details = episode.get('action_details', {})
            action_summary = self._summarize_action_details(action_details)
            
            params = {
                'episode_id': str(episode.get('id')),
                'action_type': episode.get('action_type', 'unknown'),
                'timestamp': episode.get('timestamp', datetime.utcnow().isoformat()),
                'importance': float(episode.get('importance_score', 0.0)),
                'agent_id': episode.get('agent_id', 'unknown'),
                'tags': episode.get('tags', []),
                'action_summary': action_summary
            }
            
            result = session.run(query, params)
            return result.single() is not None
            
        except Exception as e:
            logger.warning(f"Episode node creation error: {e}")
            return False
    
    async def _create_entity_node(self, session, entity: Dict) -> bool:
        """Crear nodo de entidad (Agent, Project, Concept, etc.)"""
        
        try:
            entity_type = entity.get('type', 'Concept')
            
            query = f"""
            MERGE (e:{entity_type} {{id: $entity_id}})
            SET e.name = $name,
                e.entity_type = $entity_type,
                e.confidence = $confidence,
                e.created_at = datetime(),
                e.attributes = $attributes
            RETURN e.id as id
            """
            
            params = {
                'entity_id': entity.get('id'),
                'name': entity.get('name', ''),
                'entity_type': entity_type,
                'confidence': float(entity.get('confidence', 0.5)),
                'attributes': json.dumps(entity.get('attributes', {}))
            }
            
            result = session.run(query, params)
            return result.single() is not None
            
        except Exception as e:
            logger.warning(f"Entity node creation error: {e}")
            return False
    
    async def _create_relationship(self, session, from_id: str, to_id: str, rel_type: str, strength: float) -> bool:
        """Crear relación entre nodos"""
        
        try:
            query = f"""
            MATCH (from {{id: $from_id}})
            MATCH (to {{id: $to_id}})
            MERGE (from)-[r:{rel_type}]->(to)
            SET r.strength = $strength,
                r.created_at = datetime(),
                r.last_updated = datetime()
            RETURN r
            """
            
            params = {
                'from_id': str(from_id),
                'to_id': str(to_id),
                'strength': float(strength)
            }
            
            result = session.run(query, params)
            return result.single() is not None
            
        except Exception as e:
            logger.warning(f"Relationship creation error: {e}")
            return False
    
    def _extract_entities_from_episode(self, episode: Dict) -> List[Dict]:
        """Extraer entidades de un episode para crear nodos"""
        
        entities = []
        
        # Agent como entidad
        if episode.get('agent_id'):
            entities.append({
                'id': f"agent_{episode['agent_id']}",
                'name': episode['agent_id'],
                'type': 'Agent',
                'confidence': 1.0,
                'relationship_type': 'CREATED_BY',
                'strength': 0.9
            })
        
        # Tags como conceptos
        for tag in episode.get('tags', []):
            entities.append({
                'id': f"concept_{tag}",
                'name': tag,
                'type': 'Concept',
                'confidence': 0.8,
                'relationship_type': 'TAGGED_AS',
                'strength': 0.6
            })
        
        # Action type como concepto
        if episode.get('action_type'):
            entities.append({
                'id': f"action_{episode['action_type']}",
                'name': episode['action_type'],
                'type': 'ActionType',
                'confidence': 1.0,
                'relationship_type': 'IS_TYPE',
                'strength': 0.8
            })
        
        # Extraer proyectos de action_details
        action_details = episode.get('action_details', {})
        if isinstance(action_details, dict):
            # Buscar menciones de proyectos
            for key, value in action_details.items():
                if 'project' in key.lower() and isinstance(value, str):
                    entities.append({
                        'id': f"project_{value}",
                        'name': value,
                        'type': 'Project',
                        'confidence': 0.7,
                        'relationship_type': 'RELATES_TO_PROJECT',
                        'strength': 0.7
                    })
        
        return entities
    
    def _summarize_action_details(self, action_details: Any) -> str:
        """Crear resumen de action_details para almacenar en nodo"""
        
        if isinstance(action_details, dict):
            # Extraer campos principales como resumen
            summary_parts = []
            
            for key, value in action_details.items():
                if isinstance(value, str) and len(value) < 100:
                    summary_parts.append(f"{key}: {value}")
                elif key in ['project', 'status', 'type', 'result']:
                    summary_parts.append(f"{key}: {str(value)[:50]}")
            
            return "; ".join(summary_parts[:5])  # Max 5 campos
        
        return str(action_details)[:200]  # Max 200 chars
    
    async def _create_pattern_relationships(self):
        """Crear relaciones adicionales basadas en patrones detectados"""
        
        try:
            with self.driver.session() as session:
                # Co-ocurrencia de tags
                cooccurrence_query = """
                MATCH (e1:Episode)-[:TAGGED_AS]->(c1:Concept)
                MATCH (e2:Episode)-[:TAGGED_AS]->(c2:Concept)
                WHERE e1.timestamp > datetime() - duration('P30D')
                  AND e2.timestamp > datetime() - duration('P30D')
                  AND c1.id < c2.id
                  AND exists{(e1)-[:TAGGED_AS]->(c2)}
                WITH c1, c2, count(*) as cooccurrences
                WHERE cooccurrences > 2
                MERGE (c1)-[r:CO_OCCURS_WITH]-(c2)
                SET r.strength = toFloat(cooccurrences) / 10.0,
                    r.cooccurrences = cooccurrences
                RETURN count(r) as relationships_created
                """
                
                result = session.run(cooccurrence_query)
                cooccurrence_count = result.single()['relationships_created']
                
                # Proyectos relacionados por agente
                project_agent_query = """
                MATCH (a:Agent)<-[:CREATED_BY]-(e:Episode)-[:RELATES_TO_PROJECT]->(p:Project)
                WITH a, p, count(e) as collaborations
                WHERE collaborations > 1
                MERGE (a)-[r:WORKS_ON]->(p)
                SET r.strength = toFloat(collaborations) / 5.0,
                    r.collaborations = collaborations
                RETURN count(r) as relationships_created
                """
                
                result = session.run(project_agent_query)
                project_count = result.single()['relationships_created']
                
                logger.info(f"✅ Pattern relationships: {cooccurrence_count} co-occurrence, {project_count} project-agent")
                
        except Exception as e:
            logger.warning(f"Pattern relationships creation error: {e}")
    
    async def graph_enhanced_search(self, query: str, limit: int = 10, depth: int = 2) -> List[Dict]:
        """
        Búsqueda graph-enhanced que combina vector search + graph traversal
        
        Args:
            query: Texto de búsqueda
            limit: Número máximo de resultados
            depth: Profundidad de traversal en el grafo
            
        Returns:
            Resultados combinados de vector + graph
        """
        if not self.is_initialized:
            raise RuntimeError("System not initialized. Call initialize() first.")
        
        start_time = time.time()
        
        try:
            # FASE 1: Vector search inicial (usar hybrid_local_search si está disponible)
            initial_results = await self._initial_vector_search(query, limit // 2)
            
            # FASE 2: Graph expansion desde resultados iniciales
            expanded_results = []
            
            for result in initial_results:
                neighbors = await self._get_graph_neighbors(result['id'], depth)
                expanded_results.extend(neighbors)
            
            # FASE 3: Combinar y rankear resultados
            combined_results = await self._rank_combined_results(initial_results, expanded_results)
            
            search_time = (time.time() - start_time) * 1000
            self.metrics['query_time_ms'].append(search_time)
            self.metrics['graph_queries'] += 1
            self.metrics['traversals_performed'] += len(initial_results)
            
            logger.debug(f"🎯 Graph-enhanced search completed in {search_time:.2f}ms")
            logger.debug(f"   Initial: {len(initial_results)}, Expanded: {len(expanded_results)}, Final: {len(combined_results)}")
            
            return combined_results[:limit]
            
        except Exception as e:
            logger.error(f"❌ Graph-enhanced search error: {e}")
            return []
    
    async def _initial_vector_search(self, query: str, limit: int) -> List[Dict]:
        """Búsqueda vectorial inicial (placeholder - integrar con hybrid search)"""
        
        # Placeholder - en implementación real integrar con HybridLocalSearch
        # Por ahora, búsqueda simple en Neo4j por texto
        
        try:
            with self.driver.session() as session:
                search_query = """
                MATCH (e:Episode)
                WHERE e.action_type CONTAINS $query 
                   OR e.action_summary CONTAINS $query
                   OR any(tag IN e.tags WHERE tag CONTAINS $query)
                RETURN e.id as id,
                       e.action_type as action_type,
                       e.action_summary as summary,
                       e.importance_score as score,
                       e.timestamp as timestamp,
                       'neo4j_text_search' as search_method
                ORDER BY e.importance_score DESC, e.timestamp DESC
                LIMIT $limit
                """
                
                result = session.run(search_query, {'query': query, 'limit': limit})
                
                results = []
                for record in result:
                    results.append({
                        'id': record['id'],
                        'action_type': record['action_type'],
                        'summary': record['summary'],
                        'score': float(record['score']),
                        'timestamp': str(record['timestamp']),
                        'search_method': record['search_method']
                    })
                
                return results
                
        except Exception as e:
            logger.warning(f"Initial vector search error: {e}")
            return []
    
    async def _get_graph_neighbors(self, node_id: str, depth: int = 2) -> List[Dict]:
        """Obtener vecinos de un nodo mediante graph traversal"""
        
        try:
            with self.driver.session() as session:
                traversal_query = f"""
                MATCH path = (start {{id: $node_id}})-[*1..{depth}]-(neighbor)
                WHERE start <> neighbor
                WITH neighbor, relationships(path) as rels, length(path) as distance
                RETURN DISTINCT neighbor.id as id,
                       labels(neighbor)[0] as node_type,
                       neighbor.name as name,
                       distance,
                       reduce(strength = 1.0, r IN rels | strength * coalesce(r.strength, 0.5)) as path_strength
                ORDER BY path_strength DESC, distance ASC
                LIMIT 20
                """
                
                result = session.run(traversal_query, {'node_id': str(node_id)})
                
                neighbors = []
                for record in result:
                    neighbors.append({
                        'id': record['id'],
                        'node_type': record['node_type'],
                        'name': record['name'],
                        'distance': record['distance'],
                        'path_strength': float(record['path_strength']),
                        'search_method': 'graph_traversal'
                    })
                
                return neighbors
                
        except Exception as e:
            logger.warning(f"Graph neighbors error for {node_id}: {e}")
            return []
    
    async def _rank_combined_results(self, vector_results: List[Dict], graph_results: List[Dict]) -> List[Dict]:
        """Combinar y rankear resultados de vector search + graph traversal"""
        
        combined = {}
        
        # Agregar vector results con peso alto
        for result in vector_results:
            result_id = result['id']
            combined[result_id] = result.copy()
            combined[result_id]['combined_score'] = result.get('score', 0.5) * 0.7  # 70% weight
            combined[result_id]['vector_match'] = True
            combined[result_id]['graph_match'] = False
        
        # Agregar graph results con peso basado en path strength
        for result in graph_results:
            result_id = result['id']
            
            if result_id in combined:
                # Ya existe - boost score
                combined[result_id]['combined_score'] += result.get('path_strength', 0.3) * 0.3  # 30% boost
                combined[result_id]['graph_match'] = True
            else:
                # Nuevo resultado del graph
                combined[result_id] = result.copy()
                combined[result_id]['combined_score'] = result.get('path_strength', 0.3) * 0.5  # 50% weight
                combined[result_id]['vector_match'] = False
                combined[result_id]['graph_match'] = True
        
        # Convertir a lista y ordenar
        final_results = list(combined.values())
        final_results.sort(key=lambda x: x['combined_score'], reverse=True)
        
        return final_results
    
    async def get_graph_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas del knowledge graph"""
        
        stats = {
            'timestamp': datetime.utcnow().isoformat(),
            'system_status': {
                'initialized': self.is_initialized,
                'neo4j_available': NEO4J_AVAILABLE,
                'networkx_available': NETWORKX_AVAILABLE
            },
            'metrics': self.metrics.copy(),
            'graph_stats': {},
            'performance': {}
        }
        
        if self.is_initialized:
            try:
                with self.driver.session() as session:
                    # Contar nodos por tipo
                    node_stats = session.run("""
                    MATCH (n)
                    RETURN labels(n)[0] as node_type, count(n) as count
                    """)
                    
                    node_counts = {}
                    total_nodes = 0
                    for record in node_stats:
                        node_type = record['node_type']
                        count = record['count']
                        node_counts[node_type] = count
                        total_nodes += count
                    
                    # Contar relaciones
                    rel_stats = session.run("MATCH ()-[r]->() RETURN count(r) as total_relationships")
                    total_relationships = rel_stats.single()['total_relationships']
                    
                    stats['graph_stats'] = {
                        'total_nodes': total_nodes,
                        'total_relationships': total_relationships,
                        'node_counts': node_counts,
                        'density': total_relationships / max(total_nodes, 1)
                    }
                    
            except Exception as e:
                stats['graph_stats']['error'] = str(e)
        
        # Performance stats
        if self.metrics['query_time_ms']:
            import numpy as np
            stats['performance'] = {
                'avg_query_ms': np.mean(self.metrics['query_time_ms']),
                'max_query_ms': max(self.metrics['query_time_ms'])
            }
        
        return stats
    
    async def close(self):
        """Cerrar conexiones y limpiar recursos"""
        if self.driver:
            self.driver.close()
        logger.info("🔒 Knowledge Graph connections closed")


# Factory function
async def create_knowledge_graph(config=None) -> Optional[LocalKnowledgeGraph]:
    """Crear y inicializar sistema de knowledge graph"""
    graph = LocalKnowledgeGraph(config)
    
    success = await graph.initialize()
    if not success:
        logger.error("❌ Failed to initialize Knowledge Graph")
        return None
    
    return graph


# Testing
if __name__ == "__main__":
    async def test_knowledge_graph():
        """Test básico del knowledge graph"""
        print("🧪 Testing Knowledge Graph...")
        
        graph = LocalKnowledgeGraph()
        success = await graph.initialize()
        
        if success:
            # Test con episode de prueba
            test_episodes = [
                {
                    'id': 'test_episode_1',
                    'action_type': 'project_update',
                    'action_details': {'project': 'test_project', 'status': 'completed'},
                    'agent_id': 'nexus',
                    'importance_score': 0.8,
                    'tags': ['testing', 'knowledge_graph'],
                    'timestamp': datetime.utcnow().isoformat()
                }
            ]
            
            creation_stats = await graph.create_memory_graph(test_episodes)
            print(f"Graph creation: {json.dumps(creation_stats, indent=2)}")
            
            search_results = await graph.graph_enhanced_search("test project", limit=5)
            print(f"Search results: {len(search_results)}")
            
            graph_stats = await graph.get_graph_statistics()
            print(f"Graph stats: {json.dumps(graph_stats, indent=2)}")
            
            await graph.close()
        else:
            print("❌ Initialization failed")
    
    # asyncio.run(test_knowledge_graph())
    print("✅ Knowledge Graph module loaded successfully")