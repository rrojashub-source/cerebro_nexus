#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 HYBRID LOCAL SEARCH - FASE 2 OPTIMIZACIÓN ARIA CEREBRO
Sistema de búsqueda vectorial híbrido Qdrant + ChromaDB para 4x mejora RPS

Implementación 100% Open Source según investigación de ARIA
Fecha: 11 Agosto 2025
Autorizado por: Ricardo (Episode 477)
"""

import asyncio
import json
import logging
import time
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
import numpy as np

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

logger = logging.getLogger(__name__)

class HybridLocalSearch:
    """
    Sistema de búsqueda híbrido local:
    - Primary: Qdrant (4x más rápido según benchmarks)
    - Fallback: ChromaDB (sistema actual)
    - Encoding: SentenceTransformers local (all-MiniLM-L6-v2, 22MB)
    """
    
    def __init__(self, config=None):
        self.config = config or {
            'qdrant_host': 'localhost',
            'qdrant_port': 6333,
            'collection_name': 'aria_memories_v2',
            'model_name': 'all-MiniLM-L6-v2',
            'vector_size': 384,
            'fallback_enabled': True
        }
        
        # Estado de inicialización
        self.qdrant_client = None
        self.encoder = None
        self.chroma_client = None  # Se pasará desde el sistema existente
        self.is_initialized = False
        
        # Métricas de performance
        self.metrics = {
            'qdrant_queries': 0,
            'chroma_fallbacks': 0,
            'encoding_time_ms': [],
            'search_time_ms': [],
            'total_errors': 0
        }
        
    async def initialize(self, chroma_client=None):
        """Inicializar componentes del sistema híbrido"""
        logger.info("🚀 Initializing Hybrid Local Search System...")
        
        # 1. Inicializar encoder local
        if TRANSFORMERS_AVAILABLE:
            try:
                logger.info(f"📥 Loading local model: {self.config['model_name']}")
                self.encoder = SentenceTransformer(self.config['model_name'])
                logger.info("✅ Local encoder initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to load local encoder: {e}")
                return False
        else:
            logger.error("❌ sentence-transformers not available")
            return False
        
        # 2. Inicializar Qdrant client
        if QDRANT_AVAILABLE:
            try:
                self.qdrant_client = QdrantClient(
                    host=self.config['qdrant_host'],
                    port=self.config['qdrant_port'],
                    timeout=30
                )
                
                # Test conexión
                collections = await asyncio.to_thread(self.qdrant_client.get_collections)
                logger.info(f"✅ Qdrant connected. Collections: {len(collections.collections)}")
                
                # Crear colección si no existe
                await self._ensure_collection_exists()
                
            except Exception as e:
                logger.warning(f"⚠️ Qdrant initialization failed: {e}")
                if not self.config['fallback_enabled']:
                    return False
        else:
            logger.warning("⚠️ Qdrant client not available, fallback mode only")
            if not self.config['fallback_enabled']:
                return False
        
        # 3. Configurar ChromaDB fallback
        self.chroma_client = chroma_client
        
        self.is_initialized = True
        logger.info("🎯 Hybrid Local Search System initialized successfully")
        return True
    
    async def _ensure_collection_exists(self):
        """Crear colección Qdrant si no existe"""
        try:
            collection_name = self.config['collection_name']
            
            # Verificar si existe
            collections_response = await asyncio.to_thread(
                self.qdrant_client.get_collections
            )
            
            existing_names = [c.name for c in collections_response.collections]
            
            if collection_name not in existing_names:
                logger.info(f"🏗️ Creating Qdrant collection: {collection_name}")
                
                await asyncio.to_thread(
                    self.qdrant_client.create_collection,
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=self.config['vector_size'], 
                        distance=Distance.COSINE
                    )
                )
                logger.info("✅ Collection created successfully")
            else:
                logger.info(f"✅ Collection {collection_name} already exists")
                
        except Exception as e:
            logger.error(f"❌ Failed to ensure collection exists: {e}")
            raise
    
    async def encode_query_local(self, query: str) -> np.ndarray:
        """Encode query usando modelo local"""
        if not self.encoder:
            raise RuntimeError("Encoder not initialized")
        
        start_time = time.time()
        
        try:
            # Encoding usando SentenceTransformers
            vector = await asyncio.to_thread(
                self.encoder.encode, 
                [query]
            )
            
            encoding_time = (time.time() - start_time) * 1000
            self.metrics['encoding_time_ms'].append(encoding_time)
            
            logger.debug(f"⚡ Query encoded in {encoding_time:.2f}ms")
            return vector[0]
            
        except Exception as e:
            logger.error(f"❌ Encoding error: {e}")
            raise
    
    async def advanced_search(self, query: str, limit: int = 10, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Búsqueda avanzada híbrida con Qdrant primary + ChromaDB fallback
        
        Args:
            query: Texto de búsqueda
            limit: Número máximo de resultados
            filters: Filtros adicionales (action_type, timestamp, etc.)
            
        Returns:
            Lista de resultados ordenados por relevancia
        """
        if not self.is_initialized:
            raise RuntimeError("System not initialized. Call initialize() first.")
        
        search_start = time.time()
        
        try:
            # 1. Encoding local del query
            query_vector = await self.encode_query_local(query)
            
            # 2. Búsqueda en Qdrant (primary)
            if self.qdrant_client:
                try:
                    results = await self._search_qdrant(query_vector, query, limit, filters)
                    
                    search_time = (time.time() - search_start) * 1000
                    self.metrics['search_time_ms'].append(search_time)
                    self.metrics['qdrant_queries'] += 1
                    
                    logger.debug(f"🎯 Qdrant search completed in {search_time:.2f}ms, {len(results)} results")
                    return results
                    
                except Exception as e:
                    logger.warning(f"⚠️ Qdrant search failed: {e}")
                    if not self.config['fallback_enabled']:
                        raise
            
            # 3. Fallback a ChromaDB
            if self.chroma_client and self.config['fallback_enabled']:
                logger.info("🔄 Falling back to ChromaDB search")
                results = await self._search_chroma_fallback(query_vector, query, limit, filters)
                
                search_time = (time.time() - search_start) * 1000
                self.metrics['search_time_ms'].append(search_time)
                self.metrics['chroma_fallbacks'] += 1
                
                logger.debug(f"🎯 ChromaDB fallback completed in {search_time:.2f}ms")
                return results
            
            # 4. No hay opciones disponibles
            logger.error("❌ No search backends available")
            return []
            
        except Exception as e:
            self.metrics['total_errors'] += 1
            logger.error(f"❌ Search error: {e}")
            raise
    
    async def _search_qdrant(self, query_vector: np.ndarray, query_text: str, limit: int, filters: Optional[Dict]) -> List[Dict]:
        """Realizar búsqueda en Qdrant"""
        
        # Construir filtros Qdrant si se proporcionan
        qdrant_filter = None
        if filters:
            conditions = []
            
            # Filter por action_type
            if 'action_type' in filters:
                conditions.append(
                    FieldCondition(
                        key="action_type",
                        match=MatchValue(value=filters['action_type'])
                    )
                )
            
            # Filter por agent_id
            if 'agent_id' in filters:
                conditions.append(
                    FieldCondition(
                        key="agent_id", 
                        match=MatchValue(value=filters['agent_id'])
                    )
                )
            
            if conditions:
                qdrant_filter = Filter(must=conditions)
        
        # Realizar búsqueda
        search_response = await asyncio.to_thread(
            self.qdrant_client.search,
            collection_name=self.config['collection_name'],
            query_vector=query_vector.tolist(),
            query_filter=qdrant_filter,
            limit=limit,
            with_payload=True,
            with_vectors=False
        )
        
        # Formatear resultados
        results = []
        for point in search_response:
            result = {
                'id': point.payload.get('episode_id', point.id),
                'score': point.score,
                'action_type': point.payload.get('action_type', 'unknown'),
                'action_details': point.payload.get('action_details', {}),
                'timestamp': point.payload.get('timestamp', ''),
                'agent_id': point.payload.get('agent_id', 'unknown'),
                'tags': point.payload.get('tags', []),
                'search_method': 'qdrant_primary'
            }
            results.append(result)
        
        return results
    
    async def _search_chroma_fallback(self, query_vector: np.ndarray, query_text: str, limit: int, filters: Optional[Dict]) -> List[Dict]:
        """Fallback a ChromaDB (implementación placeholder)"""
        
        # Esta implementación depende de la integración con el sistema existente de ChromaDB
        # Por ahora devuelve una estructura compatible
        
        logger.info("🔄 ChromaDB fallback search (placeholder implementation)")
        
        # Simular búsqueda en ChromaDB
        results = [{
            'id': 'fallback_result',
            'score': 0.5,
            'action_type': 'fallback_search',
            'action_details': {'note': 'ChromaDB fallback - integration pending'},
            'timestamp': datetime.utcnow().isoformat(),
            'agent_id': 'fallback',
            'tags': ['fallback'],
            'search_method': 'chroma_fallback'
        }]
        
        return results
    
    async def index_episode(self, episode: Dict) -> bool:
        """
        Indexar episode en Qdrant para búsquedas futuras
        
        Args:
            episode: Diccionario con datos del episode
            
        Returns:
            True si indexación exitosa
        """
        if not self.is_initialized or not self.qdrant_client:
            logger.warning("⚠️ Qdrant not available for indexing")
            return False
        
        try:
            # Crear texto para encoding
            text_content = f"{episode.get('action_type', '')} {json.dumps(episode.get('action_details', {}))}"
            
            # Encode contenido
            vector = await self.encode_query_local(text_content)
            
            # Crear point para Qdrant
            point = PointStruct(
                id=episode.get('id', f"ep_{int(time.time())}"),
                vector=vector.tolist(),
                payload={
                    'episode_id': episode.get('id'),
                    'action_type': episode.get('action_type', ''),
                    'action_details': episode.get('action_details', {}),
                    'timestamp': episode.get('timestamp', ''),
                    'agent_id': episode.get('agent_id', 'unknown'),
                    'tags': episode.get('tags', []),
                    'importance_score': episode.get('importance_score', 0.0),
                    'indexed_at': datetime.utcnow().isoformat()
                }
            )
            
            # Insertar en Qdrant
            await asyncio.to_thread(
                self.qdrant_client.upsert,
                collection_name=self.config['collection_name'],
                points=[point]
            )
            
            logger.debug(f"✅ Episode {episode.get('id')} indexed successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Indexing error for episode {episode.get('id')}: {e}")
            return False
    
    async def bulk_index_episodes(self, episodes: List[Dict]) -> Dict[str, int]:
        """
        Indexación masiva de episodes
        
        Args:
            episodes: Lista de episodes a indexar
            
        Returns:
            Estadísticas de indexación
        """
        logger.info(f"📥 Starting bulk indexing of {len(episodes)} episodes")
        
        results = {'success': 0, 'errors': 0}
        
        # Procesar en batches para mejor performance
        batch_size = 50
        for i in range(0, len(episodes), batch_size):
            batch = episodes[i:i + batch_size]
            
            tasks = [self.index_episode(episode) for episode in batch]
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in batch_results:
                if isinstance(result, Exception):
                    results['errors'] += 1
                    logger.warning(f"Batch indexing error: {result}")
                elif result:
                    results['success'] += 1
                else:
                    results['errors'] += 1
        
        logger.info(f"✅ Bulk indexing completed: {results['success']} success, {results['errors']} errors")
        return results
    
    async def get_search_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas del sistema de búsqueda"""
        stats = {
            'timestamp': datetime.utcnow().isoformat(),
            'system_status': {
                'qdrant_available': self.qdrant_client is not None,
                'encoder_loaded': self.encoder is not None,
                'fallback_enabled': self.config['fallback_enabled']
            },
            'metrics': self.metrics.copy(),
            'performance': {}
        }
        
        # Calcular métricas de performance
        if self.metrics['encoding_time_ms']:
            stats['performance']['avg_encoding_ms'] = np.mean(self.metrics['encoding_time_ms'])
            stats['performance']['max_encoding_ms'] = max(self.metrics['encoding_time_ms'])
        
        if self.metrics['search_time_ms']:
            stats['performance']['avg_search_ms'] = np.mean(self.metrics['search_time_ms'])
            stats['performance']['max_search_ms'] = max(self.metrics['search_time_ms'])
        
        # Stats de Qdrant si disponible
        if self.qdrant_client:
            try:
                collection_info = await asyncio.to_thread(
                    self.qdrant_client.get_collection,
                    collection_name=self.config['collection_name']
                )
                stats['qdrant'] = {
                    'vectors_count': collection_info.vectors_count,
                    'points_count': collection_info.points_count,
                    'status': collection_info.status
                }
            except Exception as e:
                stats['qdrant'] = {'error': str(e)}
        
        return stats


# Factory function para integración fácil
async def create_hybrid_search(config=None, chroma_client=None) -> HybridLocalSearch:
    """Crear instancia de Hybrid Local Search con configuración"""
    search_system = HybridLocalSearch(config)
    
    success = await search_system.initialize(chroma_client)
    if not success:
        logger.error("❌ Failed to initialize Hybrid Local Search")
        return None
    
    return search_system


# Testing/ejemplo de uso
if __name__ == "__main__":
    async def test_hybrid_search():
        """Test básico del sistema híbrido"""
        print("🧪 Testing Hybrid Local Search...")
        
        search = HybridLocalSearch()
        success = await search.initialize()
        
        if success:
            results = await search.advanced_search("test query", limit=5)
            print(f"Search results: {len(results)}")
            
            stats = await search.get_search_statistics()
            print(f"Search stats: {json.dumps(stats, indent=2)}")
        else:
            print("❌ Initialization failed")
    
    # asyncio.run(test_hybrid_search())
    print("✅ Hybrid Local Search module loaded successfully")