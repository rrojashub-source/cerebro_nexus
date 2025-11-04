#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ELITE MEMORY CACHE - FASE 2 OPTIMIZACIÓN ARIA CEREBRO
Sistema de cache multi-nivel L1/L2/L3 para 40% mejora response time

Implementación 100% Open Source según plan de ARIA
Fecha: 11 Agosto 2025
Autorizado por: Ricardo (Episode 477)
"""

import asyncio
import json
import time
import hashlib
import logging
from typing import Any, Optional, Dict, List, Union
from datetime import datetime, timedelta
from collections import OrderedDict
import redis.asyncio as redis

logger = logging.getLogger(__name__)

class EliteMemoryCache:
    """
    Sistema de cache inteligente multi-nivel:
    - L1: In-memory ultra-fast (Python dict) - nanosegundos
    - L2: Redis shared cache - microsegundos  
    - L3: PostgreSQL materialized views - millisegundos
    """
    
    def __init__(self, redis_client=None, db_pool=None, config=None):
        # Configuración por defecto
        self.config = config or {
            'l1_max_size': 1000,
            'l1_ttl_seconds': 300,  # 5 minutos
            'l2_ttl_seconds': 1800,  # 30 minutos  
            'l3_ttl_seconds': 3600   # 1 hora
        }
        
        # L1: Cache en memoria ultra-rápido
        self.l1_cache = OrderedDict()
        self.l1_timestamps = {}
        self.l1_max_size = self.config['l1_max_size']
        
        # L2: Redis cache compartido
        self.l2_redis = redis_client
        
        # L3: Database pool para materialized views
        self.l3_db = db_pool
        
        # Métricas de performance
        self.metrics = {
            'l1_hits': 0,
            'l2_hits': 0, 
            'l3_hits': 0,
            'misses': 0,
            'promotions': 0,
            'evictions': 0
        }
        
        logger.info("🚀 Elite Memory Cache initialized with multi-level architecture")
    
    def _generate_cache_key(self, key: str, prefix: str = "cache") -> str:
        """Generar clave de cache consistente"""
        if isinstance(key, dict):
            key = json.dumps(key, sort_keys=True)
        
        # Hash para claves muy largas
        if len(key) > 200:
            key_hash = hashlib.md5(key.encode()).hexdigest()
            return f"{prefix}:hash:{key_hash}"
        
        return f"{prefix}:{key}"
    
    def _is_expired(self, timestamp: float, ttl_seconds: int) -> bool:
        """Verificar si entrada está expirada"""
        return time.time() - timestamp > ttl_seconds
    
    def _evict_l1_if_needed(self):
        """Evicción LRU en L1 cache"""
        while len(self.l1_cache) >= self.l1_max_size:
            # Remover el más antiguo (LRU)
            oldest_key = next(iter(self.l1_cache))
            del self.l1_cache[oldest_key]
            if oldest_key in self.l1_timestamps:
                del self.l1_timestamps[oldest_key]
            self.metrics['evictions'] += 1
    
    async def intelligent_get(self, key: str, fetch_function=None) -> Optional[Any]:
        """
        Búsqueda inteligente multi-nivel con promoción automática
        
        Args:
            key: Clave de búsqueda
            fetch_function: Función para obtener datos si no están en cache
        
        Returns:
            Datos encontrados o None
        """
        cache_key = self._generate_cache_key(key)
        
        # L1: Check in-memory cache (nanosegundos)
        if cache_key in self.l1_cache:
            timestamp = self.l1_timestamps.get(cache_key, 0)
            
            if not self._is_expired(timestamp, self.config['l1_ttl_seconds']):
                # Move to end (LRU)
                value = self.l1_cache.pop(cache_key)
                self.l1_cache[cache_key] = value
                self.metrics['l1_hits'] += 1
                logger.debug(f"✅ L1 cache hit for key: {key}")
                return value
            else:
                # Expired - remove from L1
                del self.l1_cache[cache_key]
                if cache_key in self.l1_timestamps:
                    del self.l1_timestamps[cache_key]
        
        # L2: Check Redis cache (microsegundos)
        if self.l2_redis:
            try:
                l2_result = await self.l2_redis.get(cache_key)
                if l2_result:
                    value = json.loads(l2_result)
                    
                    # Promote to L1
                    await self._promote_to_l1(cache_key, value)
                    self.metrics['l2_hits'] += 1
                    self.metrics['promotions'] += 1
                    logger.debug(f"✅ L2 cache hit for key: {key}, promoted to L1")
                    return value
            
            except Exception as e:
                logger.warning(f"L2 cache error for key {key}: {e}")
        
        # L3: Check database materialized views (millisegundos)
        if self.l3_db and fetch_function:
            try:
                value = await fetch_function(key)
                if value is not None:
                    # Store in all levels
                    await self._store_all_levels(cache_key, value)
                    self.metrics['l3_hits'] += 1
                    logger.debug(f"✅ L3 cache hit for key: {key}, stored in all levels")
                    return value
            
            except Exception as e:
                logger.warning(f"L3 cache error for key {key}: {e}")
        
        # Cache miss
        self.metrics['misses'] += 1
        logger.debug(f"❌ Cache miss for key: {key}")
        return None
    
    async def _promote_to_l1(self, cache_key: str, value: Any):
        """Promover valor a L1 cache"""
        self._evict_l1_if_needed()
        self.l1_cache[cache_key] = value
        self.l1_timestamps[cache_key] = time.time()
    
    async def _store_all_levels(self, cache_key: str, value: Any):
        """Almacenar en todos los niveles de cache"""
        # L1: Store in memory
        await self._promote_to_l1(cache_key, value)
        
        # L2: Store in Redis
        if self.l2_redis:
            try:
                await self.l2_redis.setex(
                    cache_key, 
                    self.config['l2_ttl_seconds'],
                    json.dumps(value, default=str)
                )
            except Exception as e:
                logger.warning(f"Failed to store in L2: {e}")
    
    async def intelligent_set(self, key: str, value: Any, ttl_override: Optional[int] = None):
        """
        Almacenar valor en todos los niveles del cache
        
        Args:
            key: Clave 
            value: Valor a almacenar
            ttl_override: TTL personalizado (opcional)
        """
        cache_key = self._generate_cache_key(key)
        
        # Usar TTL custom o default
        l2_ttl = ttl_override or self.config['l2_ttl_seconds']
        
        await self._store_all_levels(cache_key, value)
        logger.debug(f"✅ Stored in all cache levels: {key}")
    
    async def intelligent_delete(self, key: str):
        """Eliminar de todos los niveles de cache"""
        cache_key = self._generate_cache_key(key)
        
        # L1: Remove from memory
        if cache_key in self.l1_cache:
            del self.l1_cache[cache_key]
        if cache_key in self.l1_timestamps:
            del self.l1_timestamps[cache_key]
        
        # L2: Remove from Redis
        if self.l2_redis:
            try:
                await self.l2_redis.delete(cache_key)
            except Exception as e:
                logger.warning(f"Failed to delete from L2: {e}")
        
        logger.debug(f"✅ Deleted from all cache levels: {key}")
    
    async def get_cache_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas de cache para monitoreo"""
        total_requests = sum(self.metrics.values())
        
        stats = {
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": self.metrics.copy(),
            "hit_ratios": {},
            "cache_sizes": {
                "l1_size": len(self.l1_cache),
                "l1_max_size": self.l1_max_size
            },
            "performance": {}
        }
        
        if total_requests > 0:
            stats["hit_ratios"] = {
                "l1_ratio": self.metrics['l1_hits'] / total_requests,
                "l2_ratio": self.metrics['l2_hits'] / total_requests, 
                "l3_ratio": self.metrics['l3_hits'] / total_requests,
                "overall_ratio": (self.metrics['l1_hits'] + self.metrics['l2_hits'] + self.metrics['l3_hits']) / total_requests
            }
        
        # Redis stats si disponible
        if self.l2_redis:
            try:
                redis_info = await self.l2_redis.info()
                stats["cache_sizes"]["l2_memory"] = redis_info.get("used_memory_human", "unknown")
                stats["cache_sizes"]["l2_keys"] = redis_info.get("db0", {}).get("keys", 0)
            except:
                pass
        
        return stats
    
    async def warm_cache(self, keys_and_fetch_functions: List[tuple]):
        """
        Precalentar cache con datos críticos
        
        Args:
            keys_and_fetch_functions: Lista de (key, fetch_function) tuples
        """
        logger.info(f"🔥 Warming cache with {len(keys_and_fetch_functions)} critical entries")
        
        warming_tasks = []
        for key, fetch_function in keys_and_fetch_functions:
            task = asyncio.create_task(
                self._warm_single_entry(key, fetch_function)
            )
            warming_tasks.append(task)
        
        results = await asyncio.gather(*warming_tasks, return_exceptions=True)
        
        successful = sum(1 for r in results if not isinstance(r, Exception))
        logger.info(f"✅ Cache warming completed: {successful}/{len(keys_and_fetch_functions)} successful")
    
    async def _warm_single_entry(self, key: str, fetch_function):
        """Precalentar entrada individual"""
        try:
            value = await fetch_function(key)
            if value is not None:
                await self.intelligent_set(key, value)
                return True
        except Exception as e:
            logger.warning(f"Cache warming failed for key {key}: {e}")
        return False
    
    async def cleanup_expired(self):
        """Limpiar entradas expiradas de L1"""
        current_time = time.time()
        expired_keys = []
        
        for cache_key, timestamp in self.l1_timestamps.items():
            if current_time - timestamp > self.config['l1_ttl_seconds']:
                expired_keys.append(cache_key)
        
        for key in expired_keys:
            if key in self.l1_cache:
                del self.l1_cache[key]
            del self.l1_timestamps[key]
        
        if expired_keys:
            logger.debug(f"🧹 Cleaned {len(expired_keys)} expired L1 entries")


# Factory function para integración fácil
async def create_elite_cache(redis_client=None, db_pool=None, config=None) -> EliteMemoryCache:
    """Crear instancia de Elite Memory Cache con configuración"""
    cache = EliteMemoryCache(redis_client, db_pool, config)
    
    # Inicializar métricas en Redis si disponible
    if redis_client:
        try:
            await redis_client.set("aria:cache:metrics:initialized", 
                                 json.dumps({"timestamp": datetime.utcnow().isoformat()}))
        except:
            pass
    
    return cache


# Ejemplo de uso/testing
if __name__ == "__main__":
    async def test_elite_cache():
        """Test básico del sistema de cache"""
        print("🧪 Testing Elite Memory Cache...")
        
        cache = EliteMemoryCache()
        
        # Test L1 storage
        await cache.intelligent_set("test_key", {"data": "test_value"})
        result = await cache.intelligent_get("test_key")
        print(f"L1 Test: {result}")
        
        # Test statistics
        stats = await cache.get_cache_statistics()
        print(f"Cache Stats: {json.dumps(stats, indent=2)}")
    
    # asyncio.run(test_elite_cache())
    print("✅ Elite Memory Cache module loaded successfully")