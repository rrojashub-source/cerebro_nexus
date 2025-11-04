#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔗 INTEGRATED GRAPH MEMORY - FASE 3 ARIA CEREBRO ELITE
Integración completa GraphRAG + Semantic Cache + Episodic Memory

Implementa:
- Auto-extraction de entidades de nuevos episodios
- Graph-enhanced memory retrieval
- Semantic caching de graph queries
- Enhanced context reasoning
- Performance optimization automático

Fecha: 11 Agosto 2025
Autorizado por: Ricardo (Episode 478+)
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta

from .graph_rag_system import GraphRAGSystem, GraphEntity, GraphRelationship, create_graph_rag_system
from .semantic_cache_system import SemanticCacheSystem, CacheLevel, create_semantic_cache_system

logger = logging.getLogger(__name__)

class IntegratedGraphMemory:
    """
    Sistema integrado que combina:
    - Memoria episódica tradicional
    - Graph RAG para reasoning contextual
    - Semantic caching para performance
    - Auto-extraction pipeline
    """
    
    def __init__(self, episodic_memory, semantic_memory,
                 neo4j_config: Optional[Dict[str, str]] = None,
                 cache_config: Optional[Dict[str, Any]] = None):
        
        self.episodic_memory = episodic_memory
        self.semantic_memory = semantic_memory
        
        # Configuración Neo4j
        self.neo4j_config = neo4j_config or {
            "uri": "bolt://aria_neo4j_knowledge_graph:7687",
            "user": "neo4j", 
            "password": "password"
        }
        
        # Configuración cache - FASE 4 Optimizada
        self.cache_config = cache_config or {
            "max_entries": 5000,
            "ttl_hours": 48,  # Más tiempo para graph results
            "similarity_thresholds": {
                "high": 0.85,    # FASE 4: Reducido para más cache hits
                "medium": 0.75,  # Más permisivo para semantic matching
                "low": 0.60,     # Rango amplio para capturar similitudes
                "context": 0.70  # Context-aware optimizado
            }
        }
        
        # Sistemas componentes
        self.graph_rag: Optional[GraphRAGSystem] = None
        self.semantic_cache: Optional[SemanticCacheSystem] = None
        
        # Configuración
        self.auto_extract_enabled = True
        self.cache_graph_queries = True
        self.enhance_retrieval = True
        
        # Statistics
        self.stats = {
            "episodes_processed": 0,
            "entities_extracted": 0, 
            "relationships_created": 0,
            "graph_enhanced_queries": 0,
            "cache_enhanced_queries": 0,
            "total_performance_improvement_ms": 0.0
        }
        
        logger.info("🔗 Integrated Graph Memory initialized")
    
    async def initialize(self) -> bool:
        """Inicializar todos los componentes"""
        
        try:
            # Inicializar GraphRAG
            self.graph_rag = await create_graph_rag_system(
                neo4j_uri=self.neo4j_config["uri"],
                neo4j_user=self.neo4j_config["user"], 
                neo4j_password=self.neo4j_config["password"]
            )
            
            # Configurar modelo de embeddings (compartido)
            if hasattr(self.semantic_memory, '_embedding_model'):
                self.graph_rag.embedding_model = self.semantic_memory._embedding_model
            
            # Inicializar Semantic Cache con embedding model forzado
            embedding_model = None
            if hasattr(self.semantic_memory, '_embedding_model'):
                embedding_model = self.semantic_memory._embedding_model
                logger.info(f"✅ Using embedding model from semantic memory: {type(embedding_model)}")
            else:
                logger.warning("⚠️ No embedding model found in semantic memory")
            
            self.semantic_cache = create_semantic_cache_system(
                max_entries=self.cache_config["max_entries"],
                ttl_hours=self.cache_config["ttl_hours"],
                embedding_model=embedding_model
            )
            
            # Configurar embedding model explícitamente si está disponible
            if embedding_model:
                self.semantic_cache.set_embedding_model(embedding_model)
                logger.info(f"✅ Embedding model configured in semantic cache: {type(embedding_model)}")
            else:
                logger.warning("⚠️ No embedding model to configure in semantic cache")
            
            # Configurar thresholds del cache
            if "similarity_thresholds" in self.cache_config:
                thresholds = self.cache_config["similarity_thresholds"]
                self.semantic_cache.similarity_thresholds = {
                    CacheLevel.HIGH_SIMILARITY.value: thresholds.get("high", 0.92),
                    CacheLevel.MEDIUM_SIMILARITY.value: thresholds.get("medium", 0.85),
                    CacheLevel.LOW_SIMILARITY.value: thresholds.get("low", 0.7),
                    CacheLevel.CONTEXT_AWARE.value: thresholds.get("context", 0.88)
                }
            
            logger.info("✅ Integrated Graph Memory initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error initializing Integrated Graph Memory: {e}")
            return False
    
    async def process_new_episode(self, episode: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesar nuevo episodio con extracción automática de entidades
        
        Args:
            episode: Episodio a procesar
            
        Returns:
            Resultado del procesamiento con stats
        """
        if not self.auto_extract_enabled or not self.graph_rag:
            return {"entities": 0, "relationships": 0, "graph_updated": False}
        
        start_time = datetime.utcnow()
        
        try:
            # 1. Extraer entidades y relaciones del episodio
            entities, relationships = await self.graph_rag.extract_entities_and_relationships(episode)
            
            # 2. Almacenar en el grafo
            if entities or relationships:
                await self.graph_rag.store_in_graph(entities, relationships)
            
            # 3. Invalidar cache relacionado si cambió el grafo
            if entities:
                await self._invalidate_related_cache(entities)
            
            # 4. Actualizar estadísticas
            self.stats["episodes_processed"] += 1
            self.stats["entities_extracted"] += len(entities)
            self.stats["relationships_created"] += len(relationships)
            
            processing_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            logger.debug(f"🔄 Processed episode {episode.get('episode_id', 'unknown')}: "
                        f"{len(entities)} entities, {len(relationships)} relationships in {processing_time:.1f}ms")
            
            return {
                "entities_extracted": len(entities),
                "relationships_created": len(relationships),
                "processing_time_ms": processing_time,
                "graph_updated": True,
                "entity_details": [{"name": e.name, "type": e.type.value, "confidence": e.confidence} for e in entities]
            }
            
        except Exception as e:
            logger.error(f"❌ Error processing episode for graph extraction: {e}")
            return {"entities": 0, "relationships": 0, "graph_updated": False, "error": str(e)}
    
    async def enhanced_memory_search(self, query: str, 
                                   context: Optional[Dict[str, Any]] = None,
                                   limit: int = 10,
                                   include_graph_reasoning: bool = True) -> Dict[str, Any]:
        """
        Búsqueda enhanced combinando memoria tradicional + graph + cache
        
        Args:
            query: Query de búsqueda
            context: Contexto adicional
            limit: Límite de resultados
            include_graph_reasoning: Incluir reasoning del grafo
            
        Returns:
            Resultados enhanced con múltiples fuentes
        """
        start_time = datetime.utcnow()
        
        # Función de compute que combina todas las fuentes
        async def compute_enhanced_search():
            results = {
                "query": query,
                "timestamp": start_time.isoformat(),
                "sources": {},
                "combined_results": [],
                "reasoning_paths": [],
                "performance_stats": {}
            }
            
            # 1. Búsqueda en memoria episódica tradicional
            episodic_start = datetime.utcnow()
            episodic_results = await self.episodic_memory.search_similar_episodes(
                query_text=query,
                context=context,
                limit=limit
            )
            episodic_time = (datetime.utcnow() - episodic_start).total_seconds() * 1000
            
            results["sources"]["episodic"] = {
                "results": episodic_results,
                "count": len(episodic_results),
                "search_time_ms": episodic_time
            }
            
            # 2. Búsqueda en memoria semántica
            semantic_start = datetime.utcnow()
            semantic_results = await self.semantic_memory.search_semantic(
                query=query,
                limit=limit
            )
            semantic_time = (datetime.utcnow() - semantic_start).total_seconds() * 1000
            
            results["sources"]["semantic"] = {
                "results": semantic_results,
                "count": len(semantic_results),
                "search_time_ms": semantic_time
            }
            
            # 3. Graph-enhanced search si está disponible
            if self.graph_rag and include_graph_reasoning:
                graph_start = datetime.utcnow()
                graph_results = await self.graph_rag.graph_enhanced_search(query, limit)
                graph_time = (datetime.utcnow() - graph_start).total_seconds() * 1000
                
                results["sources"]["graph"] = {
                    "results": graph_results,
                    "count": len(graph_results),
                    "search_time_ms": graph_time
                }
                
                # 4. Buscar reasoning paths si hay entidades relevantes
                if graph_results:
                    reasoning_paths = await self._find_reasoning_connections(query, graph_results)
                    results["reasoning_paths"] = reasoning_paths
            
            # 5. Combinar y rankear resultados
            combined_results = await self._combine_and_rank_results(
                episodic_results, semantic_results, 
                graph_results if include_graph_reasoning and self.graph_rag else [],
                query
            )
            
            results["combined_results"] = combined_results[:limit]
            
            # 6. Calcular estadísticas de performance
            total_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            results["performance_stats"] = {
                "total_search_time_ms": total_time,
                "episodic_time_ms": episodic_time,
                "semantic_time_ms": semantic_time,
                "graph_time_ms": graph_time if include_graph_reasoning else 0,
                "sources_combined": len(results["sources"]),
                "total_raw_results": sum(source["count"] for source in results["sources"].values())
            }
            
            return results
        
        # Usar cache semántico si está habilitado
        if self.cache_graph_queries and self.semantic_cache:
            self.stats["cache_enhanced_queries"] += 1
            
            cached_result, was_hit, cache_meta = await self.semantic_cache.get_or_compute(
                query=f"enhanced_search:{query}",
                compute_function=compute_enhanced_search,
                context=context,
                similarity_level=CacheLevel.HIGH_SIMILARITY
            )
            
            # Añadir metadata de cache
            if isinstance(cached_result, dict):
                cached_result["cache_metadata"] = {
                    "cache_hit": was_hit,
                    "cache_source": cache_meta.get("source"),
                    "similarity": cache_meta.get("similarity"),
                    "cache_age_hours": cache_meta.get("cache_age_hours")
                }
            
            if was_hit:
                self.stats["total_performance_improvement_ms"] += cache_meta.get("saved_time_ms", 0)
                
            return cached_result
        else:
            # Sin cache - compute directo
            return await compute_enhanced_search()
    
    async def _combine_and_rank_results(self, episodic_results: List[Dict], 
                                      semantic_results: List[Dict],
                                      graph_results: List[Dict], 
                                      original_query: str) -> List[Dict[str, Any]]:
        """Combinar y rankear resultados de múltiples fuentes"""
        
        combined = []
        
        # Procesar resultados episódicos
        for result in episodic_results:
            combined.append({
                **result,
                "source_type": "episodic",
                "relevance_score": result.get("similarity", 0.5),
                "boost_factor": 1.0  # Base score
            })
        
        # Procesar resultados semánticos
        for result in semantic_results:
            combined.append({
                **result,
                "source_type": "semantic", 
                "relevance_score": result.get("similarity", 0.5),
                "boost_factor": 1.1  # Pequeño boost para conocimiento consolidado
            })
        
        # Procesar resultados de graph
        for result in graph_results:
            # Graph results tienen estructura diferente
            relevance = result.get("relevance_score", 0.5)
            connectivity_boost = min(result.get("connectivity_score", 0) / 10.0, 0.3)
            
            combined.append({
                **result,
                "source_type": "graph",
                "relevance_score": relevance,
                "boost_factor": 1.2 + connectivity_boost  # Boost mayor para graph + conectividad
            })
        
        # Calcular score final y ordenar
        for item in combined:
            base_score = item["relevance_score"]
            boost = item["boost_factor"]
            
            # Factor de diversidad (penalizar duplicados del mismo tipo)
            diversity_factor = 1.0  # TODO: Implementar detección de duplicados
            
            final_score = base_score * boost * diversity_factor
            item["final_relevance_score"] = final_score
        
        # Ordenar por score final
        combined.sort(key=lambda x: x["final_relevance_score"], reverse=True)
        
        return combined
    
    async def _find_reasoning_connections(self, query: str, 
                                        graph_results: List[Dict]) -> List[Dict[str, Any]]:
        """Buscar conexiones de reasoning entre entidades del grafo"""
        
        if not self.graph_rag or not graph_results:
            return []
        
        reasoning_paths = []
        
        # Extraer entidades principales de la query y resultados
        query_entities = await self._extract_entities_from_text(query)
        result_entities = []
        
        for result in graph_results:
            if result.get("type") == "graph_entity":
                entity_name = result.get("entity", {}).get("name")
                if entity_name:
                    result_entities.append(entity_name)
        
        # Buscar paths de reasoning entre query entities y result entities
        for query_entity in query_entities[:3]:  # Limitar para performance
            for result_entity in result_entities[:3]:
                if query_entity != result_entity:
                    paths = await self.graph_rag.find_reasoning_paths(
                        source_entity=query_entity,
                        target_entity=result_entity,
                        max_hops=2  # Limitar para performance
                    )
                    
                    if paths:
                        reasoning_paths.extend([{
                            "source_entity": query_entity,
                            "target_entity": result_entity,
                            "path_length": path.path_length,
                            "relevance_score": path.relevance_score,
                            "reasoning": path.reasoning,
                            "entities_in_path": [e.name for e in path.entities]
                        } for path in paths[:2]])  # Max 2 paths por par
        
        # Ordenar por relevancia
        reasoning_paths.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return reasoning_paths[:5]  # Top 5 reasoning paths
    
    async def _extract_entities_from_text(self, text: str) -> List[str]:
        """Extraer entidades de un texto para reasoning"""
        
        if not self.graph_rag:
            return []
        
        # Usar el mismo método que GraphRAG
        return await self.graph_rag._extract_query_entities(text)
    
    async def _invalidate_related_cache(self, entities: List[GraphEntity]):
        """Invalidar cache relacionado cuando se actualiza el grafo"""
        
        if not self.semantic_cache:
            return
        
        # Crear tags para invalidation basados en las entidades
        invalidation_tags = []
        
        for entity in entities:
            # Tags por nombre de entidad
            invalidation_tags.append(entity.name.lower())
            
            # Tags por tipo de entidad
            invalidation_tags.append(f"entity_type_{entity.type.value}")
            
            # Tags semánticas específicas
            if entity.type.value in ["person", "project"]:
                invalidation_tags.append(f"semantic_{entity.type.value}")
        
        # Invalidar entradas relacionadas
        if invalidation_tags:
            invalidated_count = await self.semantic_cache.invalidate_by_tags(
                invalidation_tags, 
                exact_match=False
            )
            
            if invalidated_count > 0:
                logger.debug(f"🗑️ Invalidated {invalidated_count} cache entries due to graph update")
    
    async def get_system_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas completas del sistema integrado"""
        
        stats = {
            "integrated_stats": self.stats.copy(),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Estadísticas de GraphRAG
        if self.graph_rag:
            try:
                graph_stats = await self.graph_rag.get_graph_statistics()
                stats["graph_rag_stats"] = graph_stats
            except Exception as e:
                stats["graph_rag_stats"] = {"error": str(e)}
        
        # Estadísticas de Semantic Cache
        if self.semantic_cache:
            try:
                cache_stats = self.semantic_cache.get_cache_statistics()
                stats["semantic_cache_stats"] = cache_stats
            except Exception as e:
                stats["semantic_cache_stats"] = {"error": str(e)}
        
        # Estadísticas combinadas de performance
        total_queries = self.stats.get("graph_enhanced_queries", 0) + self.stats.get("cache_enhanced_queries", 0)
        
        if total_queries > 0:
            stats["performance_summary"] = {
                "total_enhanced_queries": total_queries,
                "avg_improvement_ms": self.stats["total_performance_improvement_ms"] / total_queries,
                "cache_utilization": self.stats["cache_enhanced_queries"] / total_queries,
                "graph_utilization": self.stats["graph_enhanced_queries"] / total_queries
            }
        
        return stats
    
    async def optimize_system(self):
        """Optimización periódica de todos los componentes"""
        
        logger.info("🔧 Starting integrated system optimization")
        
        # Optimizar cache semántico
        if self.semantic_cache:
            await self.semantic_cache.optimize_cache()
        
        # TODO: Optimizar grafo (limpiar entidades de baja confianza, etc.)
        
        # TODO: Analizar patrones de uso y ajustar configuraciones
        
        logger.info("✅ Integrated system optimization completed")
    
    async def bulk_process_episodes(self, episodes: List[Dict[str, Any]], 
                                  batch_size: int = 50) -> Dict[str, Any]:
        """Procesar múltiples episodios en lotes para extracción de entidades"""
        
        if not self.auto_extract_enabled or not episodes:
            return {"processed": 0, "entities": 0, "relationships": 0}
        
        total_processed = 0
        total_entities = 0
        total_relationships = 0
        errors = []
        
        # Procesar en lotes
        for i in range(0, len(episodes), batch_size):
            batch = episodes[i:i + batch_size]
            
            batch_results = []
            for episode in batch:
                try:
                    result = await self.process_new_episode(episode)
                    batch_results.append(result)
                    
                    if result.get("graph_updated"):
                        total_entities += result.get("entities_extracted", 0)
                        total_relationships += result.get("relationships_created", 0)
                        total_processed += 1
                        
                except Exception as e:
                    errors.append({
                        "episode_id": episode.get("episode_id", "unknown"),
                        "error": str(e)
                    })
            
            # Pequeña pausa entre lotes para no sobrecargar
            if i + batch_size < len(episodes):
                await asyncio.sleep(0.1)
        
        logger.info(f"📦 Bulk processed {total_processed}/{len(episodes)} episodes: "
                   f"{total_entities} entities, {total_relationships} relationships")
        
        return {
            "episodes_processed": total_processed,
            "total_episodes": len(episodes),
            "entities_extracted": total_entities,
            "relationships_created": total_relationships,
            "errors_count": len(errors),
            "errors": errors[:10]  # Solo los primeros 10 errores
        }
    
    async def close(self):
        """Cerrar todos los componentes"""
        
        if self.graph_rag:
            await self.graph_rag.close()
        
        # Semantic cache no necesita close explícito
        
        logger.info("🔒 Integrated Graph Memory system closed")


# Factory function
async def create_integrated_graph_memory(episodic_memory, semantic_memory,
                                       neo4j_config: Optional[Dict[str, str]] = None,
                                       cache_config: Optional[Dict[str, Any]] = None) -> IntegratedGraphMemory:
    """Crear y inicializar sistema integrado"""
    
    system = IntegratedGraphMemory(
        episodic_memory=episodic_memory,
        semantic_memory=semantic_memory,
        neo4j_config=neo4j_config,
        cache_config=cache_config
    )
    
    success = await system.initialize()
    
    if not success:
        logger.warning("⚠️ Integrated Graph Memory initialized with limited functionality")
    
    return system


# Testing
if __name__ == "__main__":
    async def test_integrated_system():
        """Test básico del sistema integrado"""
        print("🧪 Testing Integrated Graph Memory System...")
        
        # Mock memory systems
        class MockEpisodicMemory:
            async def search_similar_episodes(self, query_text, context=None, limit=10):
                return [{"episode_id": "mock_1", "similarity": 0.8, "content": "mock episodic result"}]
        
        class MockSemanticMemory:
            async def search_semantic(self, query, limit=10):
                return [{"knowledge_id": "mock_k1", "similarity": 0.7, "content": "mock semantic result"}]
        
        episodic = MockEpisodicMemory()
        semantic = MockSemanticMemory()
        
        # Crear sistema integrado
        integrated = await create_integrated_graph_memory(episodic, semantic)
        
        # Test episode processing
        test_episode = {
            "episode_id": "test_integrated_001",
            "action_type": "project_development",
            "action_details": {
                "project": "ARIA GraphRAG Integration",
                "developers": ["NEXUS", "Ricardo"],
                "technology": "Neo4j"
            }
        }
        
        processing_result = await integrated.process_new_episode(test_episode)
        print(f"📊 Episode processing: {processing_result}")
        
        # Test enhanced search
        search_result = await integrated.enhanced_memory_search(
            query="ARIA project development",
            include_graph_reasoning=True
        )
        
        print(f"🔍 Enhanced search found {len(search_result.get('combined_results', []))} results")
        print(f"   Sources: {list(search_result.get('sources', {}).keys())}")
        
        # Test statistics
        stats = await integrated.get_system_statistics()
        print(f"📈 System stats: {stats['integrated_stats']}")
        
        await integrated.close()
        print("✅ Integrated system test completed")
    
    # asyncio.run(test_integrated_system())
    print("✅ Integrated Graph Memory module loaded successfully")