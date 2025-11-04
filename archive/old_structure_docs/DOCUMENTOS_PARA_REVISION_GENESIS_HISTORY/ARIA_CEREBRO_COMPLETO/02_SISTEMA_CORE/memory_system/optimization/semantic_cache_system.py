#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 SEMANTIC CACHE SYSTEM - FASE 3 ARIA CEREBRO ELITE
Sistema de caching semántico avanzado para 60% reducción compute en queries similares

Implementa:
- Cache semántico con embeddings similarity
- Invalidation inteligente basada en contexto
- Multi-level semantic matching
- Query result optimization
- Temporal decay para relevancia

Fecha: 11 Agosto 2025
Autorizado por: Ricardo (Episode 478+)
"""

import asyncio
import json
import logging
import hashlib
import time
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import math

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

logger = logging.getLogger(__name__)

class CacheLevel(Enum):
    """Niveles del cache semántico"""
    EXACT = "exact"           # Match exacto (hash-based)
    HIGH_SIMILARITY = "high"   # Similaridad > 0.95
    MEDIUM_SIMILARITY = "medium" # Similaridad > 0.8  
    LOW_SIMILARITY = "low"     # Similaridad > 0.6
    CONTEXT_AWARE = "context"  # Con contexto adicional

class CacheStrategy(Enum):
    """Estrategias de caching"""
    LRU = "lru"               # Least Recently Used
    LFU = "lfu"               # Least Frequently Used  
    TTL = "ttl"               # Time To Live
    SEMANTIC_DECAY = "semantic_decay"  # Decay basado en similaridad semántica
    ADAPTIVE = "adaptive"      # Estrategia adaptativa

@dataclass
class CacheEntry:
    """Entrada del cache semántico"""
    key: str                    # Hash de la query
    original_query: str         # Query original
    query_embedding: List[float] # Embedding de la query
    result: Any                 # Resultado cacheado
    
    # Metadata temporal
    created_at: datetime
    last_accessed: datetime
    access_count: int
    
    # Metadata semántica
    similarity_threshold: float  # Threshold usado para crear esta entrada
    context_hash: str           # Hash del contexto cuando se creó
    semantic_tags: List[str]    # Tags semánticas para invalidation
    
    # Metadata de performance
    original_compute_time_ms: float  # Tiempo original de cómputo
    cache_hit_count: int        # Veces que fue hit
    saved_compute_time_ms: float # Tiempo ahorrado acumulado
    
    # Decay factors
    relevance_score: float      # Score de relevancia actual [0,1]
    temporal_decay: float       # Factor de decay temporal [0,1]

@dataclass  
class CacheStats:
    """Estadísticas del cache semántico"""
    total_entries: int
    total_queries: int
    cache_hits: int
    cache_misses: int
    hit_rate: float
    
    # Estadísticas por nivel
    hits_by_level: Dict[str, int]
    avg_similarity_by_level: Dict[str, float]
    
    # Performance
    total_compute_time_saved_ms: float
    avg_response_time_improvement: float
    
    # Memory usage
    estimated_memory_mb: float
    entries_by_strategy: Dict[str, int]

class SemanticCacheSystem:
    """
    Sistema de cache semántico avanzado:
    - Similarity matching con embeddings
    - Invalidation inteligente 
    - Multi-level caching strategy
    - Adaptive optimization
    - Performance monitoring
    """
    
    def __init__(self, max_entries: int = 10000, 
                 default_ttl_hours: int = 24,
                 similarity_thresholds: Optional[Dict[str, float]] = None,
                 embedding_model=None):
        
        self.max_entries = max_entries
        self.default_ttl_hours = default_ttl_hours
        
        # Thresholds de similaridad por nivel
        self.similarity_thresholds = similarity_thresholds or {
            CacheLevel.HIGH_SIMILARITY.value: 0.95,
            CacheLevel.MEDIUM_SIMILARITY.value: 0.8,
            CacheLevel.LOW_SIMILARITY.value: 0.6,
            CacheLevel.CONTEXT_AWARE.value: 0.85
        }
        
        # Storage
        self.cache_entries: Dict[str, CacheEntry] = {}
        self.embedding_index: List[Tuple[str, np.ndarray]] = []  # (key, embedding) pairs
        
        # Embedding model (puede ser el mismo que semantic memory)
        self.embedding_model = embedding_model
        self._embedding_cache: Dict[str, List[float]] = {}  # Cache de embeddings
        
        # Statistics
        self.stats = CacheStats(
            total_entries=0, total_queries=0, cache_hits=0, cache_misses=0, hit_rate=0.0,
            hits_by_level={}, avg_similarity_by_level={}, 
            total_compute_time_saved_ms=0.0, avg_response_time_improvement=0.0,
            estimated_memory_mb=0.0, entries_by_strategy={}
        )
        
        # Configuration
        self.strategy = CacheStrategy.ADAPTIVE
        self.enable_context_aware = True
        self.enable_temporal_decay = True
        self.decay_rate = 0.1  # 10% decay per day
        
        logger.info("🧠 Semantic Cache System initialized")
    
    def set_embedding_model(self, embedding_model):
        """Configurar modelo de embeddings (compartido con semantic memory)"""
        self.embedding_model = embedding_model
        logger.info("✅ Embedding model configured for semantic cache")
    
    async def get_or_compute(self, query: str, compute_function, 
                           context: Optional[Dict[str, Any]] = None,
                           similarity_level: CacheLevel = CacheLevel.HIGH_SIMILARITY,
                           force_refresh: bool = False) -> Tuple[Any, bool, Dict[str, Any]]:
        """
        Obtener resultado del cache o computar si no existe
        
        Args:
            query: Query de búsqueda
            compute_function: Función async para computar si no está en cache
            context: Contexto adicional para cache context-aware
            similarity_level: Nivel de similaridad requerido
            force_refresh: Forzar recómputo ignorando cache
        
        Returns:
            Tuple de (resultado, fue_cache_hit, metadata)
        """
        start_time = time.time()
        self.stats.total_queries += 1
        
        # Si forzamos refresh, computar directamente
        if force_refresh:
            result = await self._compute_and_cache(query, compute_function, context, start_time)
            return result, False, {"source": "forced_refresh"}
        
        # 1. Buscar match exacto primero
        query_hash = self._generate_query_hash(query, context)
        if query_hash in self.cache_entries:
            entry = self.cache_entries[query_hash]
            
            # Verificar si está expirado
            if not self._is_expired(entry):
                # Cache hit exacto
                self._update_access_stats(entry, start_time)
                self.stats.cache_hits += 1
                
                logger.debug(f"🎯 Exact cache hit for query: {query[:50]}")
                return entry.result, True, {
                    "source": "exact_match",
                    "similarity": 1.0,
                    "cache_age_hours": (datetime.utcnow() - entry.created_at).total_seconds() / 3600
                }
        
        # 2. Buscar match semántico
        if self.embedding_model:
            semantic_match = await self._find_semantic_match(query, context, similarity_level)
            
            if semantic_match:
                entry, similarity = semantic_match
                
                # Verificar que no esté expirado
                if not self._is_expired(entry):
                    self._update_access_stats(entry, start_time)
                    self.stats.cache_hits += 1
                    
                    # Actualizar estadísticas por nivel
                    level_str = self._similarity_to_level(similarity).value
                    self.stats.hits_by_level[level_str] = self.stats.hits_by_level.get(level_str, 0) + 1
                    
                    logger.debug(f"🧠 Semantic cache hit (similarity: {similarity:.3f}) for query: {query[:50]}")
                    return entry.result, True, {
                        "source": "semantic_match",
                        "similarity": similarity,
                        "original_query": entry.original_query,
                        "cache_age_hours": (datetime.utcnow() - entry.created_at).total_seconds() / 3600
                    }
        
        # 3. Cache miss - computar y cachear
        self.stats.cache_misses += 1
        result = await self._compute_and_cache(query, compute_function, context, start_time)
        
        logger.debug(f"❌ Cache miss for query: {query[:50]}")
        return result, False, {"source": "computed"}
    
    async def _compute_and_cache(self, query: str, compute_function, 
                               context: Optional[Dict[str, Any]], start_time: float):
        """Computar resultado y añadir al cache"""
        
        # Computar resultado
        compute_start = time.time()
        result = await compute_function()
        compute_time = (time.time() - compute_start) * 1000  # ms
        
        # Generar embedding para cache semántico  
        query_embedding = await self._get_or_generate_embedding(query)
        
        # Crear entrada de cache
        query_hash = self._generate_query_hash(query, context)
        context_hash = self._generate_context_hash(context) if context else ""
        semantic_tags = self._extract_semantic_tags(query, context)
        
        entry = CacheEntry(
            key=query_hash,
            original_query=query,
            query_embedding=query_embedding,
            result=result,
            created_at=datetime.utcnow(),
            last_accessed=datetime.utcnow(),
            access_count=1,
            similarity_threshold=self.similarity_thresholds[CacheLevel.HIGH_SIMILARITY.value],
            context_hash=context_hash,
            semantic_tags=semantic_tags,
            original_compute_time_ms=compute_time,
            cache_hit_count=0,
            saved_compute_time_ms=0.0,
            relevance_score=1.0,
            temporal_decay=1.0
        )
        
        # Añadir al cache
        await self._add_to_cache(entry)
        
        logger.debug(f"📝 Cached new result (compute: {compute_time:.1f}ms): {query[:50]}")
        
        return result
    
    async def _find_semantic_match(self, query: str, context: Optional[Dict[str, Any]], 
                                 similarity_level: CacheLevel) -> Optional[Tuple[CacheEntry, float]]:
        """Encontrar match semántico en el cache"""
        
        if not self.embedding_model or not self.embedding_index:
            return None
        
        # Generar embedding de la query
        query_embedding = await self._get_or_generate_embedding(query)
        if not query_embedding:
            return None
        
        query_array = np.array(query_embedding).reshape(1, -1)
        
        # Buscar similaridad con todas las entradas
        best_match = None
        best_similarity = 0.0
        threshold = self.similarity_thresholds[similarity_level.value]
        
        for cache_key, cached_embedding in self.embedding_index:
            if cache_key not in self.cache_entries:
                continue
            
            cached_array = cached_embedding.reshape(1, -1)
            
            try:
                if SKLEARN_AVAILABLE:
                    similarity = cosine_similarity(query_array, cached_array)[0][0]
                else:
                    # Fallback: cosine similarity manual
                    similarity = self._manual_cosine_similarity(query_embedding, cached_embedding.tolist())
                
                # Ajustar similaridad por contexto si está habilitado
                if self.enable_context_aware and context:
                    context_bonus = self._calculate_context_bonus(
                        context, self.cache_entries[cache_key].context_hash
                    )
                    similarity += context_bonus
                
                # Aplicar decay temporal
                if self.enable_temporal_decay:
                    entry = self.cache_entries[cache_key] 
                    temporal_factor = self._calculate_temporal_decay(entry)
                    similarity *= temporal_factor
                
                if similarity > threshold and similarity > best_similarity:
                    best_similarity = similarity
                    best_match = self.cache_entries[cache_key]
                    
            except Exception as e:
                logger.warning(f"Error calculating similarity: {e}")
                continue
        
        return (best_match, best_similarity) if best_match else None
    
    async def _get_or_generate_embedding(self, text: str) -> List[float]:
        """Obtener o generar embedding para texto"""
        
        # Cache de embeddings para evitar recálculos
        if text in self._embedding_cache:
            return self._embedding_cache[text]
        
        if not self.embedding_model:
            logger.warning("⚠️ No embedding model available")
            return []
        
        try:
            # Usar el modelo de embeddings (mismo que semantic memory)
            if hasattr(self.embedding_model, 'encode'):
                # Sentence transformers
                embedding = self.embedding_model.encode([text])[0].tolist()
            elif hasattr(self.embedding_model, 'embed_query'):
                # LangChain style
                embedding = await self.embedding_model.embed_query(text)
            else:
                # Fallback
                logger.warning("⚠️ Unknown embedding model interface")
                return []
            
            # Cache embedding
            self._embedding_cache[text] = embedding
            
            # Limpiar cache si es muy grande
            if len(self._embedding_cache) > 1000:
                # Remover 20% más antiguos (simple FIFO)
                keys_to_remove = list(self._embedding_cache.keys())[:200]
                for key in keys_to_remove:
                    del self._embedding_cache[key]
            
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return []
    
    def _manual_cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Cosine similarity manual si sklearn no está disponible"""
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0
        
        # Dot product
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        
        # Magnitudes
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(a * a for a in vec2))
        
        if magnitude1 == 0.0 or magnitude2 == 0.0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def _generate_query_hash(self, query: str, context: Optional[Dict[str, Any]]) -> str:
        """Generar hash único para query + context"""
        
        # Normalizar query
        normalized_query = query.lower().strip()
        
        # Incluir contexto relevante
        context_str = ""
        if context:
            # Solo incluir claves importantes para el hash
            relevant_keys = ['memory_types', 'limit', 'importance_threshold', 'date_range']
            relevant_context = {k: v for k, v in context.items() if k in relevant_keys}
            context_str = json.dumps(relevant_context, sort_keys=True)
        
        combined = f"{normalized_query}|{context_str}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def _generate_context_hash(self, context: Optional[Dict[str, Any]]) -> str:
        """Generar hash solo del contexto"""
        if not context:
            return ""
        return hashlib.md5(json.dumps(context, sort_keys=True).encode()).hexdigest()
    
    def _extract_semantic_tags(self, query: str, context: Optional[Dict[str, Any]]) -> List[str]:
        """Extraer tags semánticas para invalidation inteligente"""
        tags = []
        
        # Tags de la query
        query_words = query.lower().split()
        important_words = [w for w in query_words if len(w) > 3]
        tags.extend(important_words[:5])  # Máximo 5 palabras importantes
        
        # Tags del contexto
        if context:
            if 'memory_types' in context:
                tags.extend([f"memory_type_{mt}" for mt in context['memory_types']])
            
            if 'tags' in context:
                tags.extend([f"context_tag_{tag}" for tag in context['tags']])
        
        # Tags semánticas generales
        if any(word in query.lower() for word in ['proyecto', 'project']):
            tags.append('semantic_project')
        
        if any(word in query.lower() for word in ['error', 'problema', 'issue']):
            tags.append('semantic_problem')
        
        if any(word in query.lower() for word in ['implementar', 'desarrollar', 'crear']):
            tags.append('semantic_development')
        
        return list(set(tags))  # Remover duplicados
    
    async def _add_to_cache(self, entry: CacheEntry):
        """Añadir entrada al cache con gestión de memoria"""
        
        # Verificar límite de entradas
        if len(self.cache_entries) >= self.max_entries:
            await self._evict_entries()
        
        # Añadir entrada
        self.cache_entries[entry.key] = entry
        
        # Añadir al índice de embeddings si tenemos embedding
        if entry.query_embedding and NUMPY_AVAILABLE:
            embedding_array = np.array(entry.query_embedding)
            self.embedding_index.append((entry.key, embedding_array))
        
        # Actualizar estadísticas
        self.stats.total_entries = len(self.cache_entries)
        self._update_memory_stats()
        
        logger.debug(f"📝 Added cache entry: {entry.key}")
    
    async def _evict_entries(self, eviction_percentage: float = 0.2):
        """Evict entradas según estrategia configurada"""
        
        num_to_evict = int(len(self.cache_entries) * eviction_percentage)
        
        if self.strategy == CacheStrategy.LRU:
            # Evict least recently used
            entries_by_access = sorted(
                self.cache_entries.items(), 
                key=lambda x: x[1].last_accessed
            )
        elif self.strategy == CacheStrategy.LFU:
            # Evict least frequently used
            entries_by_access = sorted(
                self.cache_entries.items(),
                key=lambda x: x[1].access_count
            )
        elif self.strategy == CacheStrategy.SEMANTIC_DECAY:
            # Evict by relevance score (includes temporal decay)
            entries_by_relevance = sorted(
                self.cache_entries.items(),
                key=lambda x: self._calculate_entry_relevance(x[1])
            )
            entries_by_access = entries_by_relevance
        else:  # ADAPTIVE
            # Combinación de factores
            entries_by_score = sorted(
                self.cache_entries.items(),
                key=lambda x: self._calculate_adaptive_score(x[1])
            )
            entries_by_access = entries_by_score
        
        # Evict entries
        for i in range(min(num_to_evict, len(entries_by_access))):
            key, entry = entries_by_access[i]
            await self._remove_from_cache(key)
        
        logger.info(f"🗑️ Evicted {num_to_evict} cache entries using {self.strategy.value} strategy")
    
    async def _remove_from_cache(self, key: str):
        """Remover entrada del cache"""
        
        if key in self.cache_entries:
            del self.cache_entries[key]
        
        # Remover del índice de embeddings
        self.embedding_index = [(k, emb) for k, emb in self.embedding_index if k != key]
        
        self.stats.total_entries = len(self.cache_entries)
    
    def _calculate_entry_relevance(self, entry: CacheEntry) -> float:
        """Calcular relevancia actual de una entrada"""
        
        # Factor temporal
        temporal_factor = self._calculate_temporal_decay(entry)
        
        # Factor de uso
        usage_factor = min(entry.access_count / 10.0, 1.0)  # Normalizado
        
        # Factor de ahorro computacional
        compute_factor = min(entry.original_compute_time_ms / 1000.0, 1.0)  # Normalizado
        
        relevance = (temporal_factor * 0.4 + usage_factor * 0.4 + compute_factor * 0.2)
        
        return relevance
    
    def _calculate_adaptive_score(self, entry: CacheEntry) -> float:
        """Score adaptativo combinando múltiples factores"""
        
        relevance = self._calculate_entry_relevance(entry)
        
        # Hit rate factor
        hit_rate = entry.cache_hit_count / max(entry.access_count, 1)
        
        # Recency factor
        hours_since_access = (datetime.utcnow() - entry.last_accessed).total_seconds() / 3600
        recency_factor = math.exp(-hours_since_access / 24.0)  # Decay exponencial
        
        adaptive_score = relevance * 0.5 + hit_rate * 0.3 + recency_factor * 0.2
        
        return adaptive_score
    
    def _calculate_temporal_decay(self, entry: CacheEntry) -> float:
        """Calcular decay temporal para una entrada"""
        
        if not self.enable_temporal_decay:
            return 1.0
        
        age_hours = (datetime.utcnow() - entry.created_at).total_seconds() / 3600
        
        # Decay exponencial
        decay_factor = math.exp(-age_hours * self.decay_rate / 24.0)
        
        return max(decay_factor, 0.1)  # Mínimo 10%
    
    def _calculate_context_bonus(self, current_context: Dict[str, Any], cached_context_hash: str) -> float:
        """Calcular bonus de similaridad por contexto"""
        
        if not current_context or not cached_context_hash:
            return 0.0
        
        current_hash = self._generate_context_hash(current_context)
        
        # Match exacto = bonus máximo
        if current_hash == cached_context_hash:
            return 0.1
        
        # TODO: Implementar similaridad parcial de contexto
        # Por ahora, solo bonus por match exacto
        
        return 0.0
    
    def _is_expired(self, entry: CacheEntry) -> bool:
        """Verificar si una entrada ha expirado"""
        
        age_hours = (datetime.utcnow() - entry.created_at).total_seconds() / 3600
        
        return age_hours > self.default_ttl_hours
    
    def _update_access_stats(self, entry: CacheEntry, request_start_time: float):
        """Actualizar estadísticas de acceso"""
        
        current_time = datetime.utcnow()
        response_time = (time.time() - request_start_time) * 1000  # ms
        
        # Actualizar entrada
        entry.last_accessed = current_time
        entry.access_count += 1
        entry.cache_hit_count += 1
        
        # Tiempo ahorrado estimado
        saved_time = max(entry.original_compute_time_ms - response_time, 0)
        entry.saved_compute_time_ms += saved_time
        
        # Actualizar estadísticas globales
        self.stats.total_compute_time_saved_ms += saved_time
        
        # Recalcular hit rate
        self.stats.hit_rate = self.stats.cache_hits / max(self.stats.total_queries, 1)
    
    def _similarity_to_level(self, similarity: float) -> CacheLevel:
        """Convertir similarity score a CacheLevel"""
        
        if similarity >= self.similarity_thresholds[CacheLevel.HIGH_SIMILARITY.value]:
            return CacheLevel.HIGH_SIMILARITY
        elif similarity >= self.similarity_thresholds[CacheLevel.MEDIUM_SIMILARITY.value]:
            return CacheLevel.MEDIUM_SIMILARITY
        elif similarity >= self.similarity_thresholds[CacheLevel.LOW_SIMILARITY.value]:
            return CacheLevel.LOW_SIMILARITY
        else:
            return CacheLevel.CONTEXT_AWARE  # Fallback
    
    def _update_memory_stats(self):
        """Actualizar estadísticas de memoria"""
        
        # Estimación simple de uso de memoria
        estimated_bytes = 0
        
        for entry in self.cache_entries.values():
            # Estimación conservadora
            estimated_bytes += len(entry.original_query) * 2  # Query string
            estimated_bytes += len(entry.query_embedding) * 8  # Embeddings (float64)
            estimated_bytes += 1000  # Metadata + result (estimación)
        
        self.stats.estimated_memory_mb = estimated_bytes / (1024 * 1024)
    
    async def invalidate_by_tags(self, tags: List[str], exact_match: bool = False):
        """Invalidar entradas por tags semánticas"""
        
        invalidated_count = 0
        keys_to_remove = []
        
        for key, entry in self.cache_entries.items():
            should_invalidate = False
            
            if exact_match:
                # Invalidar si coincide algún tag exacto
                should_invalidate = any(tag in entry.semantic_tags for tag in tags)
            else:
                # Invalidar si coincide parcialmente
                for tag in tags:
                    if any(tag.lower() in entry_tag.lower() for entry_tag in entry.semantic_tags):
                        should_invalidate = True
                        break
            
            if should_invalidate:
                keys_to_remove.append(key)
        
        # Remover entradas
        for key in keys_to_remove:
            await self._remove_from_cache(key)
            invalidated_count += 1
        
        logger.info(f"🗑️ Invalidated {invalidated_count} cache entries by tags: {tags}")
        
        return invalidated_count
    
    async def invalidate_by_age(self, max_age_hours: int = None):
        """Invalidar entradas por edad"""
        
        max_age = max_age_hours or self.default_ttl_hours
        invalidated_count = 0
        keys_to_remove = []
        
        cutoff_time = datetime.utcnow() - timedelta(hours=max_age)
        
        for key, entry in self.cache_entries.items():
            if entry.created_at < cutoff_time:
                keys_to_remove.append(key)
        
        # Remover entradas
        for key in keys_to_remove:
            await self._remove_from_cache(key)
            invalidated_count += 1
        
        logger.info(f"🗑️ Invalidated {invalidated_count} cache entries older than {max_age} hours")
        
        return invalidated_count
    
    async def optimize_cache(self):
        """Optimización periódica del cache"""
        
        # Limpiar entradas expiradas
        await self.invalidate_by_age()
        
        # Recalcular relevance scores
        for entry in self.cache_entries.values():
            entry.relevance_score = self._calculate_entry_relevance(entry)
            entry.temporal_decay = self._calculate_temporal_decay(entry)
        
        # Actualizar estadísticas
        self._update_memory_stats()
        
        # Optimizar embedding index si es muy grande
        if len(self.embedding_index) > self.max_entries * 1.2:
            # Reindexar solo entradas que existen
            valid_embeddings = [(k, emb) for k, emb in self.embedding_index if k in self.cache_entries]
            self.embedding_index = valid_embeddings
        
        logger.info("🔧 Semantic cache optimization completed")
    
    def get_cache_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas detalladas del cache"""
        
        # Actualizar estadísticas dinámicas
        self._update_memory_stats()
        
        # Estadísticas por nivel
        total_hits = sum(self.stats.hits_by_level.values())
        
        # Distribución por TTL
        now = datetime.utcnow()
        age_distribution = {"0-1h": 0, "1-6h": 0, "6-24h": 0, "24h+": 0}
        
        for entry in self.cache_entries.values():
            age_hours = (now - entry.created_at).total_seconds() / 3600
            if age_hours < 1:
                age_distribution["0-1h"] += 1
            elif age_hours < 6:
                age_distribution["1-6h"] += 1
            elif age_hours < 24:
                age_distribution["6-24h"] += 1
            else:
                age_distribution["24h+"] += 1
        
        # Estadísticas de performance
        avg_compute_savings = (
            self.stats.total_compute_time_saved_ms / max(self.stats.cache_hits, 1)
        ) if self.stats.cache_hits > 0 else 0
        
        return {
            **asdict(self.stats),
            "configuration": {
                "max_entries": self.max_entries,
                "strategy": self.strategy.value,
                "similarity_thresholds": self.similarity_thresholds,
                "ttl_hours": self.default_ttl_hours,
                "temporal_decay_enabled": self.enable_temporal_decay,
                "context_aware_enabled": self.enable_context_aware
            },
            "distribution": {
                "age_distribution": age_distribution,
                "avg_compute_savings_ms": avg_compute_savings,
                "embedding_index_size": len(self.embedding_index),
                "embedding_cache_size": len(self._embedding_cache)
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def clear_cache(self):
        """Limpiar completamente el cache"""
        
        self.cache_entries.clear()
        self.embedding_index.clear()
        self._embedding_cache.clear()
        
        # Reset estadísticas
        self.stats = CacheStats(
            total_entries=0, total_queries=0, cache_hits=0, cache_misses=0, hit_rate=0.0,
            hits_by_level={}, avg_similarity_by_level={},
            total_compute_time_saved_ms=0.0, avg_response_time_improvement=0.0,
            estimated_memory_mb=0.0, entries_by_strategy={}
        )
        
        logger.info("🗑️ Semantic cache cleared completely")


# Factory function
def create_semantic_cache_system(max_entries: int = 10000,
                                ttl_hours: int = 24,
                                embedding_model=None) -> SemanticCacheSystem:
    """Crear sistema de cache semántico"""
    
    return SemanticCacheSystem(
        max_entries=max_entries,
        default_ttl_hours=ttl_hours,
        embedding_model=embedding_model
    )


# Testing  
if __name__ == "__main__":
    async def test_semantic_cache():
        """Test básico del sistema de cache semántico"""
        print("🧪 Testing Semantic Cache System...")
        
        cache = create_semantic_cache_system(max_entries=100)
        
        # Test queries similares
        async def mock_compute_function():
            await asyncio.sleep(0.1)  # Simular compute time
            return {"result": "mock_result", "timestamp": datetime.utcnow().isoformat()}
        
        # Query 1
        result1, hit1, meta1 = await cache.get_or_compute(
            "ARIA memoria persistente", 
            mock_compute_function
        )
        print(f"Query 1 - Hit: {hit1}, Source: {meta1.get('source')}")
        
        # Query 2 (similar)
        result2, hit2, meta2 = await cache.get_or_compute(
            "ARIA sistema de memoria", 
            mock_compute_function
        )
        print(f"Query 2 - Hit: {hit2}, Source: {meta2.get('source')}, Similarity: {meta2.get('similarity', 'N/A')}")
        
        # Query 3 (exacta)
        result3, hit3, meta3 = await cache.get_or_compute(
            "ARIA memoria persistente",
            mock_compute_function
        )
        print(f"Query 3 - Hit: {hit3}, Source: {meta3.get('source')}")
        
        # Estadísticas
        stats = cache.get_cache_statistics()
        print(f"📊 Cache stats: {stats['cache_hits']} hits, {stats['cache_misses']} misses, {stats['hit_rate']:.1%} rate")
        
        print("✅ Semantic Cache System test completed")
    
    # asyncio.run(test_semantic_cache())
    print("✅ Semantic Cache System module loaded successfully")