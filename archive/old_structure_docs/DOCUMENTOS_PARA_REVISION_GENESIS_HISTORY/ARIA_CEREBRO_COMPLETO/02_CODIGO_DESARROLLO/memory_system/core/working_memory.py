"""
WORKING MEMORY - Memoria de Trabajo (Redis)
Nivel 1: Contexto inmediato y tareas activas
"""

import json
import time
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from loguru import logger
import redis.asyncio as redis
from pydantic import BaseModel

from ..utils.config import get_config, get_database_url


class ContextItem(BaseModel):
    """Item de contexto en memoria de trabajo"""
    timestamp: float
    data: Dict[str, Any]
    tags: List[str] = []
    importance: float = 0.5
    session_id: Optional[str] = None


class WorkingMemory:
    """
    Memoria de Trabajo - Contexto inmediato usando Redis
    
    Maneja:
    - Contexto de conversación actual
    - Tareas activas
    - Estado temporal del agente
    - Cache de acceso rápido
    """
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.config = get_config().memory.working_memory
        self.redis = redis_client
        self.namespace = self.config.get("namespace", "aria:working:")
        self.max_items = self.config.get("max_items", 1000)
        self.ttl = self.config.get("ttl_seconds", 86400)  # 24 horas
        self.sliding_window_size = self.config.get("sliding_window_size", 50)
        
        logger.info(f"WorkingMemory inicializada - namespace: {self.namespace}, max_items: {self.max_items}")
    
    async def _get_redis(self) -> redis.Redis:
        """Obtiene cliente Redis, creándolo si es necesario"""
        if self.redis is None:
            redis_url = get_database_url("redis")
            self.redis = redis.from_url(redis_url, decode_responses=True)
            logger.info("Cliente Redis conectado")
        return self.redis
    
    async def add_context(self, context_data: Dict[str, Any], 
                         tags: List[str] = None, 
                         importance: float = 0.5,
                         session_id: Optional[str] = None) -> str:
        """
        Añade contexto actual con timestamp
        
        Args:
            context_data: Datos del contexto
            tags: Etiquetas para categorización
            importance: Nivel de importancia (0.0-1.0)
            session_id: ID de sesión actual
            
        Returns:
            Key del contexto almacenado
        """
        try:
            redis_client = await self._get_redis()
            timestamp = time.time()
            
            context_item = ContextItem(
                timestamp=timestamp,
                data=context_data,
                tags=tags or [],
                importance=importance,
                session_id=session_id
            )
            
            key = f"{self.namespace}context:{timestamp}"
            
            await redis_client.setex(
                key, 
                self.ttl, 
                context_item.json()
            )
            
            # Mantener índice ordenado para sliding window
            await redis_client.zadd(
                f"{self.namespace}index",
                {key: timestamp}
            )
            
            # Limpiar items antiguos si excedemos el límite
            await self._cleanup_old_items()
            
            logger.debug(f"Contexto añadido: {key}")
            return key
            
        except Exception as e:
            logger.error(f"Error añadiendo contexto: {e}")
            raise
    
    async def get_current_context(self, limit: int = None) -> List[Dict[str, Any]]:
        """
        Recupera contexto reciente para continuidad
        
        Args:
            limit: Número máximo de items a retornar
            
        Returns:
            Lista de contextos ordenados por timestamp (más reciente primero)
        """
        try:
            if limit is None:
                limit = self.sliding_window_size
                
            redis_client = await self._get_redis()
            
            # Obtener keys más recientes desde el índice ordenado
            keys = await redis_client.zrevrange(
                f"{self.namespace}index", 
                0, 
                limit - 1
            )
            
            if not keys:
                return []
            
            # Obtener todos los contextos
            contexts = []
            for key in keys:
                context_json = await redis_client.get(key)
                if context_json:
                    context_item = ContextItem.parse_raw(context_json)
                    contexts.append({
                        "key": key,
                        "timestamp": context_item.timestamp,
                        "datetime": datetime.fromtimestamp(context_item.timestamp),
                        "data": context_item.data,
                        "tags": context_item.tags,
                        "importance": context_item.importance,
                        "session_id": context_item.session_id
                    })
            
            logger.debug(f"Recuperados {len(contexts)} contextos")
            return contexts
            
        except Exception as e:
            logger.error(f"Error recuperando contexto: {e}")
            return []
    
    async def get_context_by_tags(self, tags: List[str], limit: int = 20) -> List[Dict[str, Any]]:
        """
        Busca contextos por etiquetas
        
        Args:
            tags: Lista de etiquetas a buscar
            limit: Límite de resultados
            
        Returns:
            Lista de contextos que coinciden con las etiquetas
        """
        try:
            all_contexts = await self.get_current_context(limit=self.max_items)
            
            matching_contexts = []
            for context in all_contexts:
                context_tags = set(context.get("tags", []))
                search_tags = set(tags)
                
                # Si hay intersección entre las etiquetas
                if context_tags.intersection(search_tags):
                    matching_contexts.append(context)
                    
                if len(matching_contexts) >= limit:
                    break
            
            logger.debug(f"Encontrados {len(matching_contexts)} contextos con tags: {tags}")
            return matching_contexts
            
        except Exception as e:
            logger.error(f"Error buscando por tags: {e}")
            return []
    
    async def get_session_context(self, session_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Obtiene contexto específico de una sesión
        
        Args:
            session_id: ID de la sesión
            limit: Límite de resultados
            
        Returns:
            Lista de contextos de la sesión
        """
        try:
            all_contexts = await self.get_current_context(limit=self.max_items)
            
            session_contexts = [
                context for context in all_contexts
                if context.get("session_id") == session_id
            ][:limit]
            
            logger.debug(f"Encontrados {len(session_contexts)} contextos para sesión: {session_id}")
            return session_contexts
            
        except Exception as e:
            logger.error(f"Error obteniendo contexto de sesión: {e}")
            return []
    
    async def update_context(self, key: str, updates: Dict[str, Any]) -> bool:
        """
        Actualiza un contexto existente
        
        Args:
            key: Key del contexto a actualizar
            updates: Diccionario con actualizaciones
            
        Returns:
            True si se actualizó exitosamente
        """
        try:
            redis_client = await self._get_redis()
            
            context_json = await redis_client.get(key)
            if not context_json:
                logger.warning(f"Contexto no encontrado para actualizar: {key}")
                return False
            
            context_item = ContextItem.parse_raw(context_json)
            
            # Aplicar actualizaciones
            if "data" in updates:
                context_item.data.update(updates["data"])
            if "tags" in updates:
                context_item.tags = updates["tags"]
            if "importance" in updates:
                context_item.importance = updates["importance"]
            
            # Guardar contexto actualizado
            await redis_client.setex(
                key,
                self.ttl,
                context_item.json()
            )
            
            logger.debug(f"Contexto actualizado: {key}")
            return True
            
        except Exception as e:
            logger.error(f"Error actualizando contexto: {e}")
            return False
    
    async def remove_context(self, key: str) -> bool:
        """
        Elimina un contexto específico
        
        Args:
            key: Key del contexto a eliminar
            
        Returns:
            True si se eliminó exitosamente
        """
        try:
            redis_client = await self._get_redis()
            
            # Eliminar del storage y del índice
            await redis_client.delete(key)
            await redis_client.zrem(f"{self.namespace}index", key)
            
            logger.debug(f"Contexto eliminado: {key}")
            return True
            
        except Exception as e:
            logger.error(f"Error eliminando contexto: {e}")
            return False
    
    async def clear_session(self, session_id: str) -> int:
        """
        Limpia todos los contextos de una sesión
        
        Args:
            session_id: ID de la sesión a limpiar
            
        Returns:
            Número de contextos eliminados
        """
        try:
            session_contexts = await self.get_session_context(session_id)
            
            removed_count = 0
            for context in session_contexts:
                if await self.remove_context(context["key"]):
                    removed_count += 1
            
            logger.info(f"Limpiados {removed_count} contextos de sesión: {session_id}")
            return removed_count
            
        except Exception as e:
            logger.error(f"Error limpiando sesión: {e}")
            return 0
    
    async def clear_all(self) -> bool:
        """
        Limpia toda la memoria de trabajo (usar con cuidado)
        
        Returns:
            True si se limpió exitosamente
        """
        try:
            redis_client = await self._get_redis()
            
            # Obtener todas las keys del namespace
            keys = await redis_client.keys(f"{self.namespace}*")
            
            if keys:
                await redis_client.delete(*keys)
            
            logger.warning(f"Memoria de trabajo limpiada completamente - {len(keys)} items eliminados")
            return True
            
        except Exception as e:
            logger.error(f"Error limpiando memoria de trabajo: {e}")
            return False
    
    async def get_memory_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de la memoria de trabajo
        
        Returns:
            Diccionario con estadísticas
        """
        try:
            redis_client = await self._get_redis()
            
            # Contar items en el índice
            total_items = await redis_client.zcard(f"{self.namespace}index")
            
            # Obtener rango de timestamps
            oldest = await redis_client.zrange(f"{self.namespace}index", 0, 0, withscores=True)
            newest = await redis_client.zrange(f"{self.namespace}index", -1, -1, withscores=True)
            
            stats = {
                "total_items": total_items,
                "max_items": self.max_items,
                "usage_percentage": (total_items / self.max_items) * 100,
                "ttl_seconds": self.ttl,
                "namespace": self.namespace
            }
            
            if oldest:
                stats["oldest_timestamp"] = oldest[0][1]
                stats["oldest_datetime"] = datetime.fromtimestamp(oldest[0][1])
            
            if newest:
                stats["newest_timestamp"] = newest[0][1]
                stats["newest_datetime"] = datetime.fromtimestamp(newest[0][1])
            
            return stats
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {}
    
    async def _cleanup_old_items(self) -> None:
        """Limpia items antiguos si excedemos el límite"""
        try:
            redis_client = await self._get_redis()
            
            current_count = await redis_client.zcard(f"{self.namespace}index")
            
            if current_count > self.max_items:
                # Eliminar los más antiguos
                excess_count = current_count - self.max_items
                old_keys = await redis_client.zrange(
                    f"{self.namespace}index", 
                    0, 
                    excess_count - 1
                )
                
                if old_keys:
                    # Eliminar del storage
                    await redis_client.delete(*old_keys)
                    # Eliminar del índice
                    await redis_client.zrem(f"{self.namespace}index", *old_keys)
                    
                    logger.debug(f"Limpiados {len(old_keys)} items antiguos")
            
        except Exception as e:
            logger.error(f"Error en cleanup: {e}")
    
    async def close(self) -> None:
        """Cierra conexiones"""
        if self.redis:
            await self.redis.close()
            logger.info("Conexión Redis cerrada")