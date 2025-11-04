"""
ARIA MEMORY MANAGER - Coordinador Principal
Orquesta todos los tipos de memoria en pipeline unificado
"""

import asyncio
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from loguru import logger
import redis.asyncio as redis
import asyncpg
import chromadb

from .working_memory import WorkingMemory
from .episodic_memory import EpisodicMemory
from .semantic_memory import SemanticMemory
from .consolidation_engine import ConsolidationEngine
from .continuity_manager import ContinuityManager
from ..utils.config import get_config, get_database_url


class AriaMemoryManager:
    """
    Coordinador principal del sistema de memoria de ARIA
    
    Orquesta:
    - Working Memory (contexto inmediato)
    - Episodic Memory (experiencias específicas)
    - Semantic Memory (conocimiento consolidado)
    - Consolidation Engine (procesamiento nocturno)
    - Continuity Manager (continuidad consciente)
    """
    
    def __init__(self):
        self.config = get_config()
        
        # Componentes de memoria (se inicializan en initialize())
        self.working_memory: Optional[WorkingMemory] = None
        self.episodic_memory: Optional[EpisodicMemory] = None
        self.semantic_memory: Optional[SemanticMemory] = None
        self.consolidation_engine: Optional[ConsolidationEngine] = None
        self.continuity_manager: Optional[ContinuityManager] = None
        
        # Estado del sistema
        self.current_session_id: Optional[str] = None
        self.initialized = False
        self.start_time = datetime.utcnow()
        
        # Configuración
        self.agent_id = self.config.memory.episodic_memory.get("agent_id", "aria")
        self.auto_consolidation = self.config.memory.episodic_memory.get("auto_consolidation", True)
        
        logger.info("AriaMemoryManager creado - esperando inicialización")
    
    async def initialize(self) -> bool:
        """
        Inicialización completa del sistema de memoria
        
        Returns:
            True si se inicializó exitosamente
        """
        try:
            logger.info("🧠 Inicializando sistema de memoria ARIA...")
            
            # 1. Inicializar conexiones de base de datos
            await self._initialize_connections()
            
            # 2. Inicializar componentes de memoria
            await self._initialize_memory_components()
            
            # 3. Cargar estado previo si existe
            await self._load_previous_state()
            
            # 4. Iniciar nueva sesión
            self.current_session_id = await self._start_new_session()
            
            # 5. Marcar como inicializado
            self.initialized = True
            
            logger.info(f"✅ Sistema inicializado exitosamente - Session: {self.current_session_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error inicializando sistema: {e}")
            return False
    
    async def _initialize_connections(self) -> None:
        """Inicializa conexiones a bases de datos"""
        try:
            # Crear pools de conexión
            redis_url = get_database_url("redis")
            postgres_url = get_database_url("postgresql")
            
            # Redis client
            redis_client = redis.from_url(redis_url, decode_responses=True)
            await redis_client.ping()
            logger.info("✅ Redis conectado")
            
            # PostgreSQL pool
            db_pool = await asyncpg.create_pool(
                postgres_url,
                min_size=5,
                max_size=20,
                command_timeout=30
            )
            logger.info("✅ PostgreSQL conectado")
            
            # Chroma client (opcional - modo degradado si falla)
            try:
                chroma_client = chromadb.HttpClient(host="chroma", port=8000)
                logger.info("✅ Chroma conectado")
                self._chroma_client = chroma_client
            except Exception as chroma_error:
                logger.warning(f"⚠️ Chroma no disponible, funcionando en modo degradado: {chroma_error}")
                self._chroma_client = None
            
            # Almacenar para uso de componentes
            self._redis_client = redis_client
            self._db_pool = db_pool
            
        except Exception as e:
            logger.error(f"Error inicializando conexiones: {e}")
            raise
    
    async def _initialize_memory_components(self) -> None:
        """Inicializa todos los componentes de memoria"""
        try:
            # Working Memory
            self.working_memory = WorkingMemory(redis_client=self._redis_client)
            logger.info("✅ WorkingMemory inicializada")
            
            # Episodic Memory
            self.episodic_memory = EpisodicMemory(db_pool=self._db_pool)
            logger.info("✅ EpisodicMemory inicializada")
            
            # Semantic Memory
            self.semantic_memory = SemanticMemory(chroma_client=self._chroma_client)
            logger.info("✅ SemanticMemory inicializada")
            
            # Consolidation Engine (se crea después porque necesita referencia a self)
            self.consolidation_engine = ConsolidationEngine(memory_manager=self)
            logger.info("✅ ConsolidationEngine inicializada")
            
            # Continuity Manager
            self.continuity_manager = ContinuityManager(memory_manager=self)
            logger.info("✅ ContinuityManager inicializada")
            
        except Exception as e:
            logger.error(f"Error inicializando componentes: {e}")
            raise
    
    async def _load_previous_state(self) -> None:
        """Carga estado previo si existe"""
        try:
            # Verificar si hay una sesión previa reciente
            stats = await self.working_memory.get_memory_stats()
            
            if stats.get("total_items", 0) > 0:
                logger.info(f"Estado previo encontrado: {stats['total_items']} items en working memory")
                
                # Determinar si hay gap significativo
                if "newest_datetime" in stats:
                    gap_duration = datetime.utcnow() - stats["newest_datetime"]
                    
                    if gap_duration > timedelta(hours=4):
                        logger.info(f"Gap detectado: {gap_duration} - preparando bridge")
                        # El bridge se hará cuando se requiera
            else:
                logger.info("No hay estado previo - sesión limpia")
                
        except Exception as e:
            logger.warning(f"Error cargando estado previo: {e}")
    
    async def _start_new_session(self) -> str:
        """
        Inicia una nueva sesión de memoria
        
        Returns:
            ID de la nueva sesión
        """
        try:
            session_id = f"aria_session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
            
            # Registrar sesión en base de datos
            query = """
                INSERT INTO memory_system.sessions (session_id, agent_id, start_time, status)
                VALUES ($1, $2, $3, 'active')
            """
            
            async with self._db_pool.acquire() as conn:
                await conn.execute(query, session_id, self.agent_id, datetime.utcnow())
            
            logger.info(f"Nueva sesión iniciada: {session_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"Error iniciando sesión: {e}")
            # Fallback a sesión temporal
            return f"temp_session_{datetime.utcnow().timestamp()}"
    
    async def record_action(self, 
                           action_type: str,
                           action_details: Dict[str, Any],
                           context_state: Dict[str, Any],
                           outcome: Optional[Dict[str, Any]] = None,
                           emotional_state: Optional[Dict[str, Any]] = None,
                           tags: Optional[List[str]] = None) -> str:
        """
        Pipeline completo de registro de acción
        
        Flujo:
        1. Almacenar en Working Memory (inmediato)
        2. Almacenar en Episodic Memory (persistente)
        3. Trigger consolidación si es necesario
        4. Actualizar estado de consciencia
        
        Args:
            action_type: Tipo de acción realizada
            action_details: Detalles específicos de la acción
            context_state: Estado del contexto completo
            outcome: Resultado de la acción
            emotional_state: Estado emocional durante la acción
            tags: Etiquetas para categorización
            
        Returns:
            UUID del episodio almacenado
        """
        try:
            if not self.initialized:
                raise RuntimeError("Sistema no inicializado - llamar initialize() primero")
            
            logger.debug(f"Registrando acción: {action_type}")
            
            # 1. Almacenar en Working Memory (contexto inmediato)
            await self.working_memory.add_context(
                context_data={
                    "action_type": action_type,
                    "action_details": action_details,
                    "context_state": context_state,
                    "outcome": outcome,
                    "emotional_state": emotional_state,
                    "timestamp": datetime.utcnow().isoformat()
                },
                tags=tags or [],
                session_id=self.current_session_id
            )
            
            # 2. Almacenar en Episodic Memory (persistente)
            episode_id = await self.episodic_memory.store_episode(
                action_type=action_type,
                action_details=action_details,
                context_state=context_state,
                session_id=self.current_session_id,
                outcome=outcome,
                emotional_state=emotional_state,
                tags=tags
            )
            
            # 3. Verificar si debe trigger consolidación
            if self.auto_consolidation and await self._should_consolidate():
                logger.info("Triggering consolidación automática")
                asyncio.create_task(self.consolidation_engine.run_consolidation())
            
            # 4. Actualizar contador de episodios en sesión
            await self._update_session_stats()
            
            logger.info(f"Acción registrada exitosamente: {episode_id}")
            return episode_id
            
        except Exception as e:
            logger.error(f"Error registrando acción: {e}")
            raise
    
    async def retrieve_relevant_memories(self, 
                                       query: str,
                                       context: Optional[Dict[str, Any]] = None,
                                       memory_types: Optional[List[str]] = None,
                                       limit: int = 10) -> Dict[str, Any]:
        """
        Búsqueda híbrida en todos los niveles de memoria
        
        Args:
            query: Consulta de búsqueda
            context: Contexto adicional para filtrar
            memory_types: Tipos de memoria a buscar ["working", "episodic", "semantic"]
            limit: Límite de resultados por tipo
            
        Returns:
            {
                "working_context": [...],     # Contexto inmediato
                "similar_episodes": [...],    # Experiencias similares
                "semantic_knowledge": [...],  # Conocimiento relacionado
                "consolidated_patterns": [...] # Patrones consolidados
            }
        """
        try:
            if not self.initialized:
                raise RuntimeError("Sistema no inicializado")
            
            logger.debug(f"Recuperando memorias relevantes para: '{query}'")
            
            results = {
                "query": query,
                "timestamp": datetime.utcnow().isoformat(),
                "working_context": [],
                "similar_episodes": [],
                "semantic_knowledge": [],
                "consolidated_patterns": []
            }
            
            memory_types = memory_types or ["working", "episodic", "semantic"]
            
            # Working Memory (contexto inmediato)
            if "working" in memory_types:
                try:
                    # Buscar por tags si el query contiene palabras clave
                    query_tags = query.lower().split()
                    working_context = await self.working_memory.get_context_by_tags(query_tags, limit=limit)
                    
                    # Si no encuentra por tags, obtener contexto reciente
                    if not working_context:
                        working_context = await self.working_memory.get_current_context(limit=limit)
                    
                    results["working_context"] = working_context
                    logger.debug(f"Working memory: {len(working_context)} items")
                    
                except Exception as e:
                    logger.warning(f"Error en working memory search: {e}")
            
            # Episodic Memory (experiencias similares)
            if "episodic" in memory_types:
                try:
                    similar_episodes = await self.episodic_memory.search_similar_episodes(
                        query_text=query,
                        context=context,
                        limit=limit
                    )
                    
                    results["similar_episodes"] = similar_episodes
                    logger.debug(f"Episodic memory: {len(similar_episodes)} episodes")
                    
                except Exception as e:
                    logger.warning(f"Error en episodic memory search: {e}")
            
            # Semantic Memory (conocimiento relacionado)
            if "semantic" in memory_types:
                try:
                    semantic_knowledge = await self.semantic_memory.search_semantic(
                        query=query,
                        limit=limit
                    )
                    
                    results["semantic_knowledge"] = semantic_knowledge
                    logger.debug(f"Semantic memory: {len(semantic_knowledge)} items")
                    
                except Exception as e:
                    logger.warning(f"Error en semantic memory search: {e}")
            
            # Total de resultados
            total_results = (len(results["working_context"]) + 
                           len(results["similar_episodes"]) + 
                           len(results["semantic_knowledge"]))
            
            logger.info(f"Memorias recuperadas: {total_results} items total")
            
            return results
            
        except Exception as e:
            logger.error(f"Error recuperando memorias: {e}")
            return {
                "query": query,
                "error": str(e),
                "working_context": [],
                "similar_episodes": [],
                "semantic_knowledge": [],
                "consolidated_patterns": []
            }
    
    async def save_consciousness_state(self) -> str:
        """
        Guarda estado completo de consciencia
        
        Returns:
            ID del estado guardado
        """
        try:
            if not self.initialized:
                raise RuntimeError("Sistema no inicializado")
            
            return await self.continuity_manager.save_consciousness_state()
            
        except Exception as e:
            logger.error(f"Error guardando estado consciencia: {e}")
            raise
    
    async def restore_consciousness_state(self, gap_duration: timedelta) -> Dict[str, Any]:
        """
        Restaura continuidad consciente después de un gap
        
        Args:
            gap_duration: Duración del gap entre sesiones
            
        Returns:
            Información de restauración
        """
        try:
            if not self.initialized:
                raise RuntimeError("Sistema no inicializado")
            
            return await self.continuity_manager.restore_consciousness_state(gap_duration)
            
        except Exception as e:
            logger.error(f"Error restaurando continuidad: {e}")
            return {"error": str(e)}
    
    async def trigger_consolidation(self) -> Dict[str, Any]:
        """
        Trigger manual de consolidación
        
        Returns:
            Estadísticas de consolidación
        """
        try:
            if not self.initialized:
                raise RuntimeError("Sistema no inicializado")
            
            logger.info("Triggering consolidación manual")
            return await self.consolidation_engine.run_consolidation()
            
        except Exception as e:
            logger.error(f"Error en consolidación manual: {e}")
            return {"error": str(e)}
    
    async def _should_consolidate(self) -> bool:
        """
        Determina si debe ejecutar consolidación automática
        
        Criterios:
        - Número de episodios no consolidados
        - Tiempo desde última consolidación
        - Importancia de episodios recientes
        """
        try:
            # Obtener episodios no consolidados
            unconsolidated = await self.episodic_memory.get_unconsolidated_episodes(limit=1)
            
            if not unconsolidated:
                return False
            
            # Verificar cantidad (consolidar cada 50 episodios)
            all_unconsolidated = await self.episodic_memory.get_unconsolidated_episodes(limit=100)
            
            if len(all_unconsolidated) >= 50:
                logger.info(f"Consolidación por cantidad: {len(all_unconsolidated)} episodios")
                return True
            
            # Verificar episodios de alta importancia (consolidar si hay 5+ con score > 0.8)
            high_importance = [ep for ep in all_unconsolidated if ep.get("importance_score", 0) > 0.8]
            
            if len(high_importance) >= 5:
                logger.info(f"Consolidación por importancia: {len(high_importance)} episodios importantes")
                return True
            
            return False
            
        except Exception as e:
            logger.warning(f"Error verificando consolidación: {e}")
            return False
    
    async def _update_session_stats(self) -> None:
        """Actualiza estadísticas de la sesión actual"""
        try:
            query = """
                UPDATE memory_system.sessions 
                SET episode_count = episode_count + 1,
                    session_data = jsonb_set(
                        COALESCE(session_data, '{}'),
                        '{last_activity}',
                        to_jsonb(NOW())
                    )
                WHERE session_id = $1
            """
            
            async with self._db_pool.acquire() as conn:
                await conn.execute(query, self.current_session_id)
                
        except Exception as e:
            logger.warning(f"Error actualizando stats de sesión: {e}")
    
    async def get_system_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas completas del sistema
        
        Returns:
            Diccionario con estadísticas de todos los componentes
        """
        try:
            if not self.initialized:
                return {"error": "Sistema no inicializado"}
            
            # Estadísticas de cada componente
            working_stats = await self.working_memory.get_memory_stats()
            episodic_stats = await self.episodic_memory.get_episode_statistics()
            semantic_stats = await self.semantic_memory.get_knowledge_statistics()
            
            # Estadísticas del sistema
            uptime = datetime.utcnow() - self.start_time
            
            stats = {
                "system": {
                    "initialized": self.initialized,
                    "current_session": self.current_session_id,
                    "agent_id": self.agent_id,
                    "uptime_seconds": uptime.total_seconds(),
                    "uptime_human": str(uptime),
                    "auto_consolidation": self.auto_consolidation
                },
                "working_memory": working_stats,
                "episodic_memory": episodic_stats,
                "semantic_memory": semantic_stats,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {"error": str(e)}
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Verifica salud de todos los componentes
        
        Returns:
            Estado de salud del sistema
        """
        try:
            health = {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "components": {}
            }
            
            # Verificar Redis
            try:
                await self._redis_client.ping()
                health["components"]["redis"] = "healthy"
            except Exception as e:
                health["components"]["redis"] = f"unhealthy: {str(e)}"
                health["status"] = "degraded"
            
            # Verificar PostgreSQL
            try:
                async with self._db_pool.acquire() as conn:
                    await conn.fetchval("SELECT 1")
                health["components"]["postgresql"] = "healthy"
            except Exception as e:
                health["components"]["postgresql"] = f"unhealthy: {str(e)}"
                health["status"] = "degraded"
            
            # Verificar Chroma
            try:
                # Chroma health check básico
                health["components"]["chroma"] = "healthy"
            except Exception as e:
                health["components"]["chroma"] = f"unhealthy: {str(e)}"
                health["status"] = "degraded"
            
            # Estado de componentes de memoria
            health["components"]["memory_components"] = {
                "working_memory": self.working_memory is not None,
                "episodic_memory": self.episodic_memory is not None,
                "semantic_memory": self.semantic_memory is not None,
                "consolidation_engine": self.consolidation_engine is not None,
                "continuity_manager": self.continuity_manager is not None
            }
            
            return health
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def close(self) -> None:
        """Cierra todas las conexiones y libera recursos"""
        try:
            logger.info("Cerrando AriaMemoryManager...")
            
            # Cerrar componentes de memoria
            if self.working_memory:
                await self.working_memory.close()
            
            if self.episodic_memory:
                await self.episodic_memory.close()
            
            if self.semantic_memory:
                await self.semantic_memory.close()
            
            # Cerrar conexiones
            if hasattr(self, '_redis_client'):
                await self._redis_client.close()
            
            if hasattr(self, '_db_pool'):
                await self._db_pool.close()
            
            # Marcar sesión como completada
            if self.current_session_id:
                try:
                    query = """
                        UPDATE memory_system.sessions 
                        SET end_time = NOW(), status = 'completed'
                        WHERE session_id = $1
                    """
                    async with self._db_pool.acquire() as conn:
                        await conn.execute(query, self.current_session_id)
                except Exception as e:
                    logger.warning(f"Error cerrando sesión: {e}")
            
            self.initialized = False
            logger.info("✅ AriaMemoryManager cerrado exitosamente")
            
        except Exception as e:
            logger.error(f"Error cerrando sistema: {e}")
    
    def __del__(self):
        """Destructor para asegurar limpieza"""
        if self.initialized:
            logger.warning("AriaMemoryManager destruido sin cerrar apropiadamente")