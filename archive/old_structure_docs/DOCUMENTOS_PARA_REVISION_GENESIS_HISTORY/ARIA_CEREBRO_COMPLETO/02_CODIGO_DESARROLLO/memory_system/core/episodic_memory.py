"""
EPISODIC MEMORY - Memoria Episódica (PostgreSQL)
Nivel 2: Experiencias específicas con contexto completo
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from loguru import logger
import asyncpg
from pydantic import BaseModel, Field

from ..utils.config import get_config, get_database_url


class Episode(BaseModel):
    """Modelo de episodio en memoria episódica"""
    id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    agent_id: str = "aria"
    session_id: str
    action_type: str
    action_details: Dict[str, Any]
    context_state: Dict[str, Any]
    outcome: Optional[Dict[str, Any]] = None
    emotional_state: Dict[str, Any] = Field(default_factory=dict)
    importance_score: float = 0.5
    tags: List[str] = Field(default_factory=list)
    consolidated: bool = False


class EpisodicMemory:
    """
    Memoria Episódica - Experiencias específicas usando PostgreSQL
    
    Maneja:
    - Almacenamiento de episodios completos con contexto
    - Búsqueda por similaridad y patrones
    - Cálculo automático de importancia
    - Relaciones entre episodios
    """
    
    def __init__(self, db_pool: Optional[asyncpg.Pool] = None):
        self.config = get_config().memory.episodic_memory
        self.db_pool = db_pool
        self.agent_id = self.config.get("agent_id", "aria")
        self.importance_threshold = self.config.get("default_importance_threshold", 0.3)
        self.auto_consolidation = self.config.get("auto_consolidation", True)
        
        logger.info(f"EpisodicMemory inicializada - agent_id: {self.agent_id}")
    
    async def _get_db_pool(self) -> asyncpg.Pool:
        """Obtiene pool de conexiones, creándolo si es necesario"""
        if self.db_pool is None:
            database_url = get_database_url("postgresql")
            self.db_pool = await asyncpg.create_pool(
                database_url,
                min_size=5,
                max_size=20,
                command_timeout=30
            )
            logger.info("Pool de conexiones PostgreSQL creado")
        return self.db_pool
    
    async def store_episode(self, 
                           action_type: str,
                           action_details: Dict[str, Any],
                           context_state: Dict[str, Any],
                           session_id: str,
                           outcome: Optional[Dict[str, Any]] = None,
                           emotional_state: Optional[Dict[str, Any]] = None,
                           importance_score: Optional[float] = None,
                           tags: Optional[List[str]] = None) -> str:
        """
        Almacena episodio completo con contexto
        
        Args:
            action_type: Tipo de acción realizada
            action_details: Detalles específicos de la acción
            context_state: Estado del contexto completo
            session_id: ID de la sesión
            outcome: Resultado de la acción
            emotional_state: Estado emocional durante la acción
            importance_score: Puntuación de importancia (calculada automáticamente si no se proporciona)
            tags: Etiquetas para categorización
            
        Returns:
            UUID del episodio almacenado
        """
        try:
            pool = await self._get_db_pool()
            
            # Crear episodio
            episode = Episode(
                timestamp=datetime.utcnow(),
                agent_id=self.agent_id,
                session_id=session_id,
                action_type=action_type,
                action_details=action_details,
                context_state=context_state,
                outcome=outcome or {},
                emotional_state=emotional_state or {},
                importance_score=importance_score or await self._calculate_importance(
                    action_type, outcome, emotional_state
                ),
                tags=tags or []
            )
            
            query = """
                INSERT INTO memory_system.episodes (
                    timestamp, agent_id, session_id, action_type, action_details,
                    context_state, outcome, emotional_state, importance_score, tags,
                    cross_reference, project_dna_id, handoff_packet
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
                RETURNING id
            """
            
            async with pool.acquire() as conn:
                episode_id = await conn.fetchval(
                    query,
                    episode.timestamp,
                    episode.agent_id,
                    episode.session_id,
                    episode.action_type,
                    json.dumps(episode.action_details),
                    json.dumps(episode.context_state),
                    json.dumps(episode.outcome),
                    json.dumps(episode.emotional_state),
                    episode.importance_score,
                    episode.tags,
                    None,  # cross_reference
                    None,  # project_dna_id
                    None   # handoff_packet
                )
            
            logger.info(f"Episodio almacenado: {episode_id} - {action_type}")
            return str(episode_id)
            
        except Exception as e:
            logger.error(f"Error almacenando episodio: {e}")
            raise
    
    async def get_episode(self, episode_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un episodio específico por ID
        
        Args:
            episode_id: UUID del episodio
            
        Returns:
            Diccionario con datos del episodio o None si no existe
        """
        try:
            pool = await self._get_db_pool()
            
            query = """
                SELECT id, timestamp, agent_id, session_id, action_type,
                       action_details, context_state, outcome, emotional_state,
                       importance_score, tags, consolidated, created_at, updated_at,
                       cross_reference, project_dna_id, handoff_packet
                FROM memory_system.episodes
                WHERE id = $1
            """
            
            async with pool.acquire() as conn:
                row = await conn.fetchrow(query, uuid.UUID(episode_id))
            
            if row:
                return dict(row)
            return None
            
        except Exception as e:
            logger.error(f"Error obteniendo episodio {episode_id}: {e}")
            return None
    
    async def search_similar_episodes(self, 
                                    query_text: str,
                                    context: Optional[Dict[str, Any]] = None,
                                    limit: int = 10,
                                    importance_threshold: Optional[float] = None) -> List[Dict[str, Any]]:
        """
        Busca episodios similares usando búsqueda de texto y contexto
        
        Args:
            query_text: Texto de búsqueda
            context: Contexto adicional para filtrar
            limit: Número máximo de resultados
            importance_threshold: Umbral mínimo de importancia
            
        Returns:
            Lista de episodios similares ordenados por relevancia
        """
        try:
            pool = await self._get_db_pool()
            threshold = importance_threshold or self.importance_threshold
            
            # Búsqueda por texto en action_type, action_details y tags
            base_query = """
                SELECT id, timestamp, agent_id, session_id, action_type,
                       action_details, context_state, outcome, emotional_state,
                       importance_score, tags, consolidated,
                       ts_rank(to_tsvector('english', action_type || ' ' || action_details::text || ' ' || array_to_string(tags, ' ')), 
                              plainto_tsquery('english', $1)) as relevance_score
                FROM memory_system.episodes
                WHERE agent_id = $2
                  AND importance_score >= $3
                  AND (to_tsvector('english', action_type || ' ' || action_details::text || ' ' || array_to_string(tags, ' ')) 
                       @@ plainto_tsquery('english', $1))
            """
            
            # Filtros adicionales por contexto
            params = [query_text, self.agent_id, threshold]
            param_count = 3
            
            if context:
                for key, value in context.items():
                    param_count += 1
                    base_query += f" AND context_state->>${param_count} = ${param_count + 1}"
                    params.extend([key, str(value)])
                    param_count += 1
            
            base_query += " ORDER BY relevance_score DESC, importance_score DESC, timestamp DESC"
            base_query += f" LIMIT ${param_count + 1}"
            params.append(limit)
            
            async with pool.acquire() as conn:
                rows = await conn.fetch(base_query, *params)
            
            episodes = [dict(row) for row in rows]
            logger.debug(f"Encontrados {len(episodes)} episodios similares para: {query_text}")
            
            return episodes
            
        except Exception as e:
            logger.error(f"Error buscando episodios similares: {e}")
            return []
    
    async def get_recent_episodes(self, 
                                limit: int = 50,
                                session_id: Optional[str] = None,
                                hours_back: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Obtiene episodios recientes
        
        Args:
            limit: Número máximo de episodios
            session_id: Filtrar por sesión específica
            hours_back: Número de horas hacia atrás
            
        Returns:
            Lista de episodios recientes
        """
        try:
            pool = await self._get_db_pool()
            
            query = """
                SELECT id, timestamp, agent_id, session_id, action_type,
                       action_details, context_state, outcome, emotional_state,
                       importance_score, tags, consolidated, created_at,
                       cross_reference, project_dna_id, handoff_packet
                FROM memory_system.episodes
                WHERE agent_id = $1
            """
            
            params = [self.agent_id]
            param_count = 1
            
            if session_id:
                param_count += 1
                query += f" AND session_id = ${param_count}"
                params.append(session_id)
            
            if hours_back:
                param_count += 1
                query += f" AND timestamp >= ${param_count}"
                params.append(datetime.utcnow() - timedelta(hours=hours_back))
            
            query += " ORDER BY timestamp DESC"
            param_count += 1
            query += f" LIMIT ${param_count}"
            params.append(limit)
            
            async with pool.acquire() as conn:
                rows = await conn.fetch(query, *params)
            
            episodes = [dict(row) for row in rows]
            logger.debug(f"Recuperados {len(episodes)} episodios recientes")
            
            return episodes
            
        except Exception as e:
            logger.error(f"Error obteniendo episodios recientes: {e}")
            return []
    
    async def get_all_episodes(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """
        Obtiene TODOS los episodios del agente (para ARIA complete history)
        
        Args:
            limit: Límite máximo de episodios a retornar
            
        Returns:
            Lista completa de episodios ordenados por timestamp
        """
        try:
            pool = await self._get_db_pool()
            
            query = """
                SELECT id, timestamp, agent_id, session_id, action_type,
                       action_details, context_state, outcome, emotional_state,
                       importance_score, tags, consolidated, created_at, updated_at,
                       cross_reference, project_dna_id, handoff_packet
                FROM memory_system.episodes
                WHERE agent_id = $1
                ORDER BY timestamp DESC
                LIMIT $2
            """
            
            async with pool.acquire() as conn:
                rows = await conn.fetch(query, self.agent_id, limit)
            
            episodes = [dict(row) for row in rows]
            logger.info(f"Recuperados {len(episodes)} episodios completos para ARIA")
            
            return episodes
            
        except Exception as e:
            logger.error(f"Error obteniendo todos los episodios: {e}")
            return []
    
    async def get_episodes_in_range(self, 
                                  start_date: datetime,
                                  end_date: datetime,
                                  include_emotional_state: bool = True,
                                  limit: int = 500) -> List[Dict[str, Any]]:
        """
        Obtiene episodios en un rango de fechas específico
        
        Args:
            start_date: Fecha de inicio
            end_date: Fecha de fin
            include_emotional_state: Si incluir estados emocionales
            limit: Límite de episodios
            
        Returns:
            Lista de episodios en el rango temporal
        """
        try:
            pool = await self._get_db_pool()
            
            fields = """
                id, timestamp, agent_id, session_id, action_type,
                action_details, context_state, outcome,
                importance_score, tags, consolidated, created_at
            """
            
            if include_emotional_state:
                fields += ", emotional_state"
            
            query = f"""
                SELECT {fields}
                FROM memory_system.episodes
                WHERE agent_id = $1 
                  AND timestamp >= $2 
                  AND timestamp <= $3
                ORDER BY timestamp ASC
                LIMIT $4
            """
            
            async with pool.acquire() as conn:
                rows = await conn.fetch(query, self.agent_id, start_date, end_date, limit)
            
            episodes = [dict(row) for row in rows]
            logger.debug(f"Encontrados {len(episodes)} episodios en rango {start_date} - {end_date}")
            
            return episodes
            
        except Exception as e:
            logger.error(f"Error obteniendo episodios en rango: {e}")
            return []
    
    async def get_episode_by_id(self, episode_id: str) -> Optional[Dict[str, Any]]:
        """
        Alias para get_episode (para consistencia con API)
        """
        return await self.get_episode(episode_id)
    
    async def get_episodes_by_tags(self, 
                                 tags: List[str], 
                                 limit: int = 20,
                                 match_all: bool = False) -> List[Dict[str, Any]]:
        """
        Busca episodios por tags
        
        Args:
            tags: Lista de tags a buscar
            limit: Límite de resultados
            match_all: Si True, debe coincidir con todos los tags
            
        Returns:
            Lista de episodios que coinciden con los tags
        """
        try:
            pool = await self._get_db_pool()
            
            if match_all:
                # Todos los tags deben estar presentes
                query = """
                    SELECT id, timestamp, agent_id, session_id, action_type,
                           action_details, context_state, outcome, emotional_state,
                           importance_score, tags, consolidated, created_at
                    FROM memory_system.episodes
                    WHERE agent_id = $1 AND tags @> $2
                    ORDER BY importance_score DESC, timestamp DESC
                    LIMIT $3
                """
                params = [self.agent_id, tags, limit]
            else:
                # Al menos uno de los tags debe estar presente
                query = """
                    SELECT id, timestamp, agent_id, session_id, action_type,
                           action_details, context_state, outcome, emotional_state,
                           importance_score, tags, consolidated, created_at
                    FROM memory_system.episodes
                    WHERE agent_id = $1 AND tags && $2
                    ORDER BY importance_score DESC, timestamp DESC
                    LIMIT $3
                """
                params = [self.agent_id, tags, limit]
            
            async with pool.acquire() as conn:
                rows = await conn.fetch(query, *params)
            
            episodes = [dict(row) for row in rows]
            logger.debug(f"Encontrados {len(episodes)} episodios con tags: {tags}")
            
            return episodes
            
        except Exception as e:
            logger.error(f"Error buscando por tags: {e}")
            return []
    
    async def update_episode(self, episode_id: str, updates: Dict[str, Any]) -> bool:
        """
        Actualiza un episodio existente
        
        Args:
            episode_id: UUID del episodio
            updates: Diccionario con campos a actualizar
            
        Returns:
            True si se actualizó exitosamente
        """
        try:
            pool = await self._get_db_pool()
            
            # Construir query de actualización dinámicamente
            set_clauses = []
            params = []
            param_count = 0
            
            allowed_fields = [
                'action_details', 'context_state', 'outcome', 'emotional_state',
                'importance_score', 'tags', 'consolidated'
            ]
            
            for field, value in updates.items():
                if field in allowed_fields:
                    param_count += 1
                    set_clauses.append(f"{field} = ${param_count}")
                    
                    # Serializar JSON si es necesario
                    if field in ['action_details', 'context_state', 'outcome', 'emotional_state']:
                        params.append(json.dumps(value))
                    else:
                        params.append(value)
            
            if not set_clauses:
                logger.warning("No hay campos válidos para actualizar")
                return False
            
            param_count += 1
            query = f"""
                UPDATE memory_system.episodes 
                SET {', '.join(set_clauses)}, updated_at = NOW()
                WHERE id = ${param_count}
            """
            params.append(uuid.UUID(episode_id))
            
            async with pool.acquire() as conn:
                result = await conn.execute(query, *params)
            
            success = result == "UPDATE 1"
            if success:
                logger.info(f"Episodio actualizado: {episode_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error actualizando episodio {episode_id}: {e}")
            return False
    
    async def mark_as_consolidated(self, episode_ids: List[str]) -> int:
        """
        Marca episodios como consolidados
        
        Args:
            episode_ids: Lista de UUIDs de episodios
            
        Returns:
            Número de episodios marcados
        """
        try:
            pool = await self._get_db_pool()
            
            query = """
                UPDATE memory_system.episodes 
                SET consolidated = TRUE, updated_at = NOW()
                WHERE id = ANY($1) AND agent_id = $2
            """
            
            uuid_list = [uuid.UUID(eid) for eid in episode_ids]
            
            async with pool.acquire() as conn:
                result = await conn.execute(query, uuid_list, self.agent_id)
            
            count = int(result.split()[-1])
            logger.info(f"Marcados {count} episodios como consolidados")
            
            return count
            
        except Exception as e:
            logger.error(f"Error marcando episodios como consolidados: {e}")
            return 0
    
    async def get_unconsolidated_episodes(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Obtiene episodios no consolidados para procesamiento
        
        Args:
            limit: Límite de episodios
            
        Returns:
            Lista de episodios no consolidados
        """
        try:
            pool = await self._get_db_pool()
            
            query = """
                SELECT id, timestamp, agent_id, session_id, action_type,
                       action_details, context_state, outcome, emotional_state,
                       importance_score, tags, created_at
                FROM memory_system.episodes
                WHERE agent_id = $1 AND consolidated = FALSE
                ORDER BY importance_score DESC, timestamp DESC
                LIMIT $2
            """
            
            async with pool.acquire() as conn:
                rows = await conn.fetch(query, self.agent_id, limit)
            
            episodes = [dict(row) for row in rows]
            logger.debug(f"Encontrados {len(episodes)} episodios no consolidados")
            
            return episodes
            
        except Exception as e:
            logger.error(f"Error obteniendo episodios no consolidados: {e}")
            return []
    
    async def get_episode_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de la memoria episódica
        
        Returns:
            Diccionario con estadísticas
        """
        try:
            pool = await self._get_db_pool()
            
            query = """
                SELECT 
                    COUNT(*) as total_episodes,
                    COUNT(*) FILTER (WHERE consolidated = TRUE) as consolidated_episodes,
                    COUNT(*) FILTER (WHERE consolidated = FALSE) as unconsolidated_episodes,
                    AVG(importance_score) as avg_importance,
                    MAX(importance_score) as max_importance,
                    MIN(importance_score) as min_importance,
                    COUNT(DISTINCT session_id) as unique_sessions,
                    COUNT(DISTINCT action_type) as unique_action_types,
                    MIN(timestamp) as oldest_episode,
                    MAX(timestamp) as newest_episode
                FROM memory_system.episodes
                WHERE agent_id = $1
            """
            
            async with pool.acquire() as conn:
                row = await conn.fetchrow(query, self.agent_id)
            
            stats = dict(row) if row else {}
            return stats
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {}
    
    async def _calculate_importance(self, 
                                  action_type: str,
                                  outcome: Optional[Dict[str, Any]],
                                  emotional_state: Optional[Dict[str, Any]]) -> float:
        """
        Calcula la puntuación de importancia de un episodio
        
        Args:
            action_type: Tipo de acción
            outcome: Resultado de la acción
            emotional_state: Estado emocional
            
        Returns:
            Puntuación de importancia (0.0-1.0)
        """
        base_score = 0.5
        importance_bonus = 0.0
        
        # Bonus por tipo de acción
        action_importance = {
            'first_contact': 0.3,
            'breakthrough': 0.3,
            'error_resolution': 0.2,
            'learning': 0.2,
            'discovery': 0.2,
            'collaboration': 0.15,
            'creation': 0.15,
            'problem_solving': 0.1,
            'routine': -0.1,
            'maintenance': -0.1
        }
        
        importance_bonus += action_importance.get(action_type, 0.0)
        
        # Bonus por outcome exitoso
        if outcome and outcome.get('success'):
            importance_bonus += 0.1
            
        # Bonus por estado emocional positivo fuerte
        if emotional_state:
            intensity = emotional_state.get('intensity', 'medium')
            valence = emotional_state.get('valence', 'neutral')
            
            if intensity == 'high' and valence == 'positive':
                importance_bonus += 0.15
            elif intensity == 'high' and valence == 'negative':
                importance_bonus += 0.1  # Eventos negativos intensos también son importantes
        
        final_score = max(0.0, min(1.0, base_score + importance_bonus))
        return final_score
    
    async def close(self) -> None:
        """Cierra el pool de conexiones"""
        if self.db_pool:
            await self.db_pool.close()
            logger.info("Pool de conexiones PostgreSQL cerrado")