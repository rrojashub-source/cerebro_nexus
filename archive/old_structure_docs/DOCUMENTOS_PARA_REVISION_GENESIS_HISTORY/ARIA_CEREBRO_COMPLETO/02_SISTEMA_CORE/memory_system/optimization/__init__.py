#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 MEMORY SYSTEM OPTIMIZATION - FASE 2 ARIA CEREBRO
Módulo de optimizaciones Elite para máximo performance

Componentes implementados:
- EliteMemoryCache: Sistema cache multi-nivel L1/L2/L3
- HybridLocalSearch: Búsqueda vectorial Qdrant + ChromaDB  

Fecha: 11 Agosto 2025
Autorizado por: Ricardo (Episode 477)
"""

from .elite_memory_cache import EliteMemoryCache, create_elite_cache
from .hybrid_local_search import HybridLocalSearch, create_hybrid_search
from .consolidation_engine import MemzeroInspiredConsolidation, create_consolidation_engine
from .local_knowledge_graph import LocalKnowledgeGraph, create_knowledge_graph
from .elite_circuit_breaker import (
    EliteCircuitBreaker, 
    ComprehensiveHealthChecker, 
    create_circuit_breaker, 
    create_health_checker,
    CircuitBreakerOpenException,
    ServiceHealth
)

# FASE 3: GraphRAG + Semantic Caching
from .graph_rag_system import (
    GraphRAGSystem,
    GraphEntity,
    GraphRelationship, 
    EntityType,
    RelationshipType,
    create_graph_rag_system
)
from .semantic_cache_system import (
    SemanticCacheSystem,
    CacheEntry,
    CacheLevel,
    CacheStrategy,
    create_semantic_cache_system
)
from .integrated_graph_memory import (
    IntegratedGraphMemory,
    create_integrated_graph_memory
)

__all__ = [
    # Fase 1 & 2
    'EliteMemoryCache',
    'create_elite_cache', 
    'HybridLocalSearch',
    'create_hybrid_search',
    'MemzeroInspiredConsolidation',
    'create_consolidation_engine',
    'LocalKnowledgeGraph',
    'create_knowledge_graph',
    'EliteCircuitBreaker',
    'ComprehensiveHealthChecker',
    'create_circuit_breaker',
    'create_health_checker',
    'CircuitBreakerOpenException',
    'ServiceHealth',
    
    # Fase 3 - GraphRAG + Semantic Cache
    'GraphRAGSystem',
    'GraphEntity', 
    'GraphRelationship',
    'EntityType',
    'RelationshipType',
    'create_graph_rag_system',
    'SemanticCacheSystem',
    'CacheEntry',
    'CacheLevel',
    'CacheStrategy', 
    'create_semantic_cache_system',
    'IntegratedGraphMemory',
    'create_integrated_graph_memory'
]

__version__ = "3.0.0-graphrag"
__author__ = "NEXUS + ARIA Collaboration"
__description__ = "Elite optimization system: GraphRAG + Semantic Cache + Enhanced Reasoning"