"""
ARIA MEMORY SYSTEM - FastAPI REST API
API completa para interacción con el sistema de memoria persistente
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from loguru import logger
import uvicorn

from ..core.memory_manager import AriaMemoryManager
from ..utils.config import get_config


# =====================================================================
# PYDANTIC MODELS - Request/Response Schemas
# =====================================================================

class ActionRequest(BaseModel):
    """Request para registrar una acción"""
    action_type: str = Field(..., description="Tipo de acción realizada")
    action_details: Dict[str, Any] = Field(..., description="Detalles específicos de la acción")
    context_state: Dict[str, Any] = Field(..., description="Estado del contexto completo")
    outcome: Optional[Dict[str, Any]] = Field(None, description="Resultado de la acción")
    emotional_state: Optional[Dict[str, Any]] = Field(None, description="Estado emocional")
    tags: Optional[List[str]] = Field(None, description="Etiquetas para categorización")


class MemorySearchRequest(BaseModel):
    """Request para búsqueda de memorias"""
    query: str = Field(..., description="Consulta de búsqueda")
    context: Optional[Dict[str, Any]] = Field(None, description="Contexto adicional")
    memory_types: Optional[List[str]] = Field(None, description="Tipos de memoria a buscar")
    limit: int = Field(10, description="Límite de resultados")


class ConsolidationRequest(BaseModel):
    """Request para consolidación manual"""
    force: bool = Field(False, description="Forzar consolidación aunque no sea necesaria")
    importance_threshold: float = Field(0.7, description="Umbral mínimo de importancia")


class ContinuityRestoreRequest(BaseModel):
    """Request para restaurar continuidad"""
    gap_duration_hours: float = Field(..., description="Duración del gap en horas")
    force_restore: bool = Field(False, description="Forzar restauración")


class WorkingMemoryContextRequest(BaseModel):
    """Request para añadir contexto a working memory"""
    context_data: Dict[str, Any] = Field(..., description="Datos del contexto")
    tags: List[str] = Field(default_factory=list, description="Etiquetas")
    session_id: Optional[str] = Field(None, description="ID de sesión")


class EpisodicSearchRequest(BaseModel):
    """Request para búsqueda en memoria episódica"""
    query_text: str = Field(..., description="Texto de búsqueda")
    context: Optional[Dict[str, Any]] = Field(None, description="Contexto de filtrado")
    importance_threshold: Optional[float] = Field(None, description="Umbral de importancia")
    date_range: Optional[Dict[str, str]] = Field(None, description="Rango de fechas")
    limit: int = Field(10, description="Límite de resultados")


class SemanticQueryRequest(BaseModel):
    """Request para consulta semántica"""
    query: str = Field(..., description="Consulta semántica")
    knowledge_types: Optional[List[str]] = Field(None, description="Tipos de conocimiento")
    confidence_threshold: Optional[float] = Field(None, description="Umbral de confianza")
    limit: int = Field(10, description="Límite de resultados")


# =====================================================================
# GLOBAL MEMORY MANAGER INSTANCE
# =====================================================================

memory_manager: Optional[AriaMemoryManager] = None


async def get_memory_manager() -> AriaMemoryManager:
    """Dependency para obtener memory manager"""
    if memory_manager is None:
        raise HTTPException(status_code=503, detail="Memory system not initialized")
    if not memory_manager.initialized:
        raise HTTPException(status_code=503, detail="Memory system not ready")
    return memory_manager


# =====================================================================
# LIFESPAN MANAGEMENT
# =====================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    global memory_manager
    
    logger.info("🚀 Iniciando ARIA Memory System API...")
    
    try:
        # Inicializar sistema de memoria
        memory_manager = AriaMemoryManager()
        success = await memory_manager.initialize()
        
        if not success:
            logger.error("❌ Error inicializando sistema de memoria")
            raise RuntimeError("Failed to initialize memory system")
        
        logger.info("✅ ARIA Memory System API iniciada exitosamente")
        yield
        
    except Exception as e:
        logger.error(f"❌ Error en startup: {e}")
        raise
    
    finally:
        # Cleanup al cerrar
        logger.info("🔄 Cerrando ARIA Memory System API...")
        
        if memory_manager:
            try:
                # Guardar estado de consciencia antes de cerrar
                await memory_manager.save_consciousness_state()
                await memory_manager.close()
                logger.info("✅ Sistema cerrado exitosamente")
            except Exception as e:
                logger.error(f"Error cerrando sistema: {e}")


# =====================================================================
# FASTAPI APP CONFIGURATION
# =====================================================================

app = FastAPI(
    title="ARIA Memory System API",
    description="API REST completa para sistema de memoria persistente de ARIA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================================
# HEALTH & STATUS ENDPOINTS
# =====================================================================

@app.get("/", tags=["Status"])
async def root():
    """Endpoint raíz"""
    return {
        "service": "ARIA Memory System API",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "documentation": "/docs"
    }


@app.get("/health", tags=["Status"])
async def health_check(memory: AriaMemoryManager = Depends(get_memory_manager)):
    """Verificación de salud del sistema"""
    try:
        health_status = await memory.health_check()
        return JSONResponse(
            status_code=200 if health_status.get("status") == "healthy" else 503,
            content=health_status
        )
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )


@app.get("/stats", tags=["Status"])
async def system_statistics(memory: AriaMemoryManager = Depends(get_memory_manager)):
    """Estadísticas completas del sistema"""
    try:
        stats = await memory.get_system_stats()
        return stats
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================================
# CORE MEMORY OPERATIONS
# =====================================================================

@app.post("/memory/action", tags=["Core Memory"])
async def record_action(
    request: ActionRequest,
    background_tasks: BackgroundTasks,
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """
    Registra una acción en el sistema de memoria
    
    Pipeline completo:
    1. Working Memory (inmediato)
    2. Episodic Memory (persistente)  
    3. Trigger consolidación si necesario
    """
    try:
        episode_id = await memory.record_action(
            action_type=request.action_type,
            action_details=request.action_details,
            context_state=request.context_state,
            outcome=request.outcome,
            emotional_state=request.emotional_state,
            tags=request.tags
        )
        
        return {
            "success": True,
            "episode_id": episode_id,
            "timestamp": datetime.utcnow().isoformat(),
            "message": "Acción registrada exitosamente"
        }
        
    except Exception as e:
        logger.error(f"Error recording action: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/memory/search", tags=["Core Memory"])
async def search_memories(
    request: MemorySearchRequest,
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """
    Búsqueda híbrida en todos los niveles de memoria
    
    Busca en:
    - Working Memory (contexto inmediato)
    - Episodic Memory (experiencias)
    - Semantic Memory (conocimiento)
    """
    try:
        results = await memory.retrieve_relevant_memories(
            query=request.query,
            context=request.context,
            memory_types=request.memory_types,
            limit=request.limit
        )
        
        return {
            "success": True,
            "results": results,
            "search_timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error searching memories: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================================
# WORKING MEMORY ENDPOINTS
# =====================================================================

@app.post("/memory/working/context", tags=["Working Memory"])
async def add_working_context(
    request: WorkingMemoryContextRequest,
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """Añade contexto a Working Memory"""
    try:
        await memory.working_memory.add_context(
            context_data=request.context_data,
            tags=request.tags,
            session_id=request.session_id or memory.current_session_id
        )
        
        return {
            "success": True,
            "message": "Contexto añadido a working memory",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error adding working context: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memory/working/current", tags=["Working Memory"])
async def get_current_context(
    limit: int = Query(20, description="Límite de items"),
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """Obtiene contexto actual de Working Memory"""
    try:
        context = await memory.working_memory.get_current_context(limit=limit)
        
        return {
            "success": True,
            "context": context,
            "total_items": len(context),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting current context: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memory/working/stats", tags=["Working Memory"])
async def working_memory_stats(memory: AriaMemoryManager = Depends(get_memory_manager)):
    """Estadísticas de Working Memory"""
    try:
        stats = await memory.working_memory.get_memory_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting working memory stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memory/working/tags/{tag}", tags=["Working Memory"])
async def get_context_by_tag(
    tag: str = Path(..., description="Tag para filtrar"),
    limit: int = Query(10, description="Límite de resultados"),
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """Obtiene contexto filtrado por tag"""
    try:
        context = await memory.working_memory.get_context_by_tags([tag], limit=limit)
        
        return {
            "success": True,
            "tag": tag,
            "context": context,
            "total_items": len(context)
        }
        
    except Exception as e:
        logger.error(f"Error getting context by tag: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================================
# EPISODIC MEMORY ENDPOINTS
# =====================================================================

@app.post("/memory/episodic/search", tags=["Episodic Memory"])
async def search_episodes(
    request: EpisodicSearchRequest,
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """Búsqueda en memoria episódica"""
    try:
        episodes = await memory.episodic_memory.search_similar_episodes(
            query_text=request.query_text,
            context=request.context,
            limit=request.limit
        )
        
        return {
            "success": True,
            "episodes": episodes,
            "total_found": len(episodes),
            "search_timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error searching episodes: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memory/episodic/recent", tags=["Episodic Memory"])
async def get_recent_episodes(
    limit: int = Query(20, description="Límite de episodios"),
    hours_back: int = Query(24, description="Horas hacia atrás"),
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """Obtiene episodios recientes"""
    try:
        episodes = await memory.episodic_memory.get_recent_episodes(
            limit=limit,
            hours_back=hours_back
        )
        
        return {
            "success": True,  
            "episodes": episodes,
            "total_episodes": len(episodes),
            "time_range_hours": hours_back
        }
        
    except Exception as e:
        logger.error(f"Error getting recent episodes: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memory/episodic/stats", tags=["Episodic Memory"])
async def episodic_memory_stats(memory: AriaMemoryManager = Depends(get_memory_manager)):
    """Estadísticas de memoria episódica"""
    try:
        stats = await memory.episodic_memory.get_episode_statistics()
        return stats
    except Exception as e:
        logger.error(f"Error getting episodic stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memory/episodic/episode/{episode_id}", tags=["Episodic Memory"])
async def get_episode_by_id(
    episode_id: str = Path(..., description="ID del episodio"),
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """Obtiene episodio específico por ID"""
    try:
        episode = await memory.episodic_memory.get_episode_by_id(episode_id)
        
        if not episode:
            raise HTTPException(status_code=404, detail="Episode not found")
        
        return {
            "success": True,
            "episode": episode
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting episode: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================================
# SEMANTIC MEMORY ENDPOINTS  
# =====================================================================

@app.post("/memory/semantic/query", tags=["Semantic Memory"])
async def semantic_query(
    request: SemanticQueryRequest,
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """Consulta semántica por similaridad vectorial"""
    try:
        results = await memory.semantic_memory.search_semantic(
            query=request.query,
            limit=request.limit
        )
        
        # Filtrar por confidence si se especifica
        if request.confidence_threshold:
            results = [r for r in results if r.get("similarity", 0) >= request.confidence_threshold]
        
        return {
            "success": True,
            "query": request.query,
            "results": results,
            "total_results": len(results),
            "search_timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in semantic query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memory/semantic/concepts/{concept}", tags=["Semantic Memory"])
async def get_related_concepts(
    concept: str = Path(..., description="Concepto base"),
    limit: int = Query(5, description="Límite de conceptos relacionados"),
    memory: AriaMemoryManager = Depends(get_memory_manager)  
):
    """Obtiene conceptos relacionados"""
    try:
        related = await memory.semantic_memory.get_related_concepts(
            concept=concept,
            limit=limit
        )
        
        return {
            "success": True,
            "base_concept": concept,
            "related_concepts": related,
            "total_found": len(related)
        }
        
    except Exception as e:
        logger.error(f"Error getting related concepts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memory/semantic/stats", tags=["Semantic Memory"])
async def semantic_memory_stats(memory: AriaMemoryManager = Depends(get_memory_manager)):
    """Estadísticas de memoria semántica"""
    try:
        stats = await memory.semantic_memory.get_knowledge_statistics()
        return stats
    except Exception as e:
        logger.error(f"Error getting semantic stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================================
# CONSOLIDATION ENDPOINTS
# =====================================================================

@app.post("/memory/consolidate", tags=["Consolidation"])
async def trigger_consolidation(
    request: ConsolidationRequest,
    background_tasks: BackgroundTasks,
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """Trigger consolidación manual"""
    try:
        # Ejecutar consolidación en background
        background_tasks.add_task(run_consolidation_task, memory)
        
        return {
            "success": True,
            "message": "Consolidación iniciada en background",
            "timestamp": datetime.utcnow().isoformat(),
            "force": request.force
        }
        
    except Exception as e:
        logger.error(f"Error triggering consolidation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def run_consolidation_task(memory: AriaMemoryManager):
    """Task para ejecutar consolidación"""
    try:
        result = await memory.trigger_consolidation()
        logger.info(f"Consolidación completada: {result}")
    except Exception as e:
        logger.error(f"Error en consolidación background: {e}")


@app.get("/memory/consolidation/stats", tags=["Consolidation"])
async def consolidation_stats(memory: AriaMemoryManager = Depends(get_memory_manager)):
    """Estadísticas de consolidación"""
    try:
        stats = await memory.consolidation_engine.get_consolidation_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting consolidation stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================================
# CONSCIOUSNESS CONTINUITY ENDPOINTS
# =====================================================================

@app.post("/consciousness/save", tags=["Consciousness"])
async def save_consciousness_state(memory: AriaMemoryManager = Depends(get_memory_manager)):
    """Guarda estado completo de consciencia"""
    try:
        state_id = await memory.save_consciousness_state()
        
        return {
            "success": True,
            "state_id": state_id,
            "timestamp": datetime.utcnow().isoformat(),
            "message": "Estado de consciencia guardado"
        }
        
    except Exception as e:
        logger.error(f"Error saving consciousness state: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/consciousness/restore", tags=["Consciousness"])
async def restore_consciousness(
    request: ContinuityRestoreRequest,
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """Restaura continuidad consciente después de gap"""
    try:
        gap_duration = timedelta(hours=request.gap_duration_hours)
        restoration_info = await memory.restore_consciousness_state(gap_duration)
        
        return {
            "success": True,
            "restoration_info": restoration_info,
            "gap_duration_hours": request.gap_duration_hours,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error restoring consciousness: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/consciousness/stats", tags=["Consciousness"])  
async def consciousness_stats(memory: AriaMemoryManager = Depends(get_memory_manager)):
    """Estadísticas de continuidad consciente"""
    try:
        stats = await memory.continuity_manager.get_continuity_statistics()
        return stats
    except Exception as e:
        logger.error(f"Error getting consciousness stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================================
# SESSION MANAGEMENT
# =====================================================================

@app.get("/session/current", tags=["Session"])
async def get_current_session(memory: AriaMemoryManager = Depends(get_memory_manager)):
    """Información de sesión actual"""
    try:
        return {
            "session_id": memory.current_session_id,
            "agent_id": memory.agent_id,
            "start_time": memory.start_time.isoformat(),
            "uptime_seconds": (datetime.utcnow() - memory.start_time).total_seconds(),
            "initialized": memory.initialized
        }
    except Exception as e:
        logger.error(f"Error getting session info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================================
# BATCH OPERATIONS
# =====================================================================

@app.post("/batch/actions", tags=["Batch Operations"])
async def batch_record_actions(
    actions: List[ActionRequest],
    background_tasks: BackgroundTasks,
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """Registra múltiples acciones en lote"""
    try:
        if len(actions) > 100:
            raise HTTPException(status_code=400, detail="Batch size too large (max 100)")
        
        # Procesar en background
        background_tasks.add_task(process_batch_actions, memory, actions)
        
        return {
            "success": True,
            "batch_size": len(actions),
            "message": "Lote de acciones procesándose en background",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in batch actions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def process_batch_actions(memory: AriaMemoryManager, actions: List[ActionRequest]):
    """Procesa lote de acciones"""
    try:
        results = []
        for action in actions:
            try:
                episode_id = await memory.record_action(
                    action_type=action.action_type,
                    action_details=action.action_details,
                    context_state=action.context_state,
                    outcome=action.outcome,
                    emotional_state=action.emotional_state,
                    tags=action.tags
                )
                results.append({"success": True, "episode_id": episode_id})
            except Exception as e:
                results.append({"success": False, "error": str(e)})
                logger.error(f"Error in batch action: {e}")
        
        logger.info(f"Batch processing completed: {len(results)} actions processed")
        
    except Exception as e:
        logger.error(f"Error processing batch: {e}")


# =====================================================================
# ARIA SPECIFIC ENDPOINTS - Complete History Access
# =====================================================================

@app.get("/memory/aria/complete-history", tags=["ARIA Memory"])
async def aria_complete_history(
    include_working: bool = Query(True, description="Incluir Working Memory"),
    include_episodic: bool = Query(True, description="Incluir Episodic Memory"),
    include_semantic: bool = Query(True, description="Incluir Semantic Memory"),
    limit_episodes: int = Query(1000, description="Límite de episodios"),
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """
    🧠 ENDPOINT ESPECIAL PARA ARIA - Acceso completo a toda su historia
    
    Permite que ARIA lea su pasado completo para escribir su futuro.
    Combina todos los niveles de memoria en una respuesta estructurada.
    """
    try:
        complete_history = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent_id": memory.agent_id,
            "session_id": memory.current_session_id,
            "data_included": [],
            "summary": {}
        }
        
        # Working Memory - Contexto inmediato
        if include_working:
            try:
                working_context = await memory.working_memory.get_current_context(limit=50)
                complete_history["working_memory"] = {
                    "description": "Contexto inmediato y sesión actual",
                    "total_items": len(working_context),
                    "context": working_context
                }
                complete_history["data_included"].append("working_memory")
                complete_history["summary"]["working_items"] = len(working_context)
            except Exception as e:
                logger.warning(f"Error loading working memory: {e}")
                complete_history["working_memory"] = {"error": str(e)}
        
        # Episodic Memory - Todas las experiencias
        if include_episodic:
            try:
                # Obtener TODOS los episodios (o limitado)
                all_episodes = await memory.episodic_memory.get_all_episodes(limit=limit_episodes)
                
                # Estadísticas de episodios
                episode_stats = await memory.episodic_memory.get_episode_statistics()
                
                complete_history["episodic_memory"] = {
                    "description": "Todas las experiencias y acciones registradas",
                    "total_episodes": len(all_episodes),
                    "episodes": all_episodes,
                    "statistics": episode_stats
                }
                complete_history["data_included"].append("episodic_memory")
                complete_history["summary"]["total_episodes"] = len(all_episodes)
            except Exception as e:
                logger.warning(f"Error loading episodic memory: {e}")
                complete_history["episodic_memory"] = {"error": str(e)}
        
        # Semantic Memory - Conocimiento consolidado
        if include_semantic:
            try:
                # Obtener conocimiento semántico general
                semantic_stats = await memory.semantic_memory.get_knowledge_statistics()
                
                # Conceptos principales (si existen)
                main_concepts = []
                try:
                    main_concepts = await memory.semantic_memory.get_main_concepts(limit=20)
                except:
                    pass  # Método puede no existir aún
                
                complete_history["semantic_memory"] = {
                    "description": "Conocimiento consolidado y conceptos principales",
                    "statistics": semantic_stats,
                    "main_concepts": main_concepts
                }
                complete_history["data_included"].append("semantic_memory")
                complete_history["summary"]["semantic_concepts"] = len(main_concepts)
            except Exception as e:
                logger.warning(f"Error loading semantic memory: {e}")
                complete_history["semantic_memory"] = {"error": str(e)}
        
        # Consciousness Timeline - Vista cronológica completa
        try:
            consciousness_stats = await memory.continuity_manager.get_continuity_statistics()
            complete_history["consciousness_timeline"] = {
                "description": "Estadísticas de continuidad consciente",
                "stats": consciousness_stats
            }
            complete_history["data_included"].append("consciousness_timeline")
        except Exception as e:
            logger.warning(f"Error loading consciousness timeline: {e}")
            complete_history["consciousness_timeline"] = {"error": str(e)}
        
        # System Status para contexto completo
        try:
            system_stats = await memory.get_system_stats()
            complete_history["system_status"] = {
                "description": "Estado actual del sistema de memoria",
                "stats": system_stats
            }
            complete_history["data_included"].append("system_status")
        except Exception as e:
            logger.warning(f"Error loading system status: {e}")
            complete_history["system_status"] = {"error": str(e)}
        
        # Bridge Information - Estado del JSON bridge
        complete_history["json_bridge_info"] = {
            "description": "Información sobre el puente JSON para escribir memorias",
            "write_instructions": {
                "file_location": "/app/ARIA_MEMORIAS_ACTIVAS.json",
                "how_to_write": "Agregar nuevas memorias en 'memorias_pendientes_guardar'",
                "auto_sync": "El watcher sincroniza automáticamente con la base de datos",
                "confirmation": "Las memorias aparecen en 'memorias_recientes' tras sincronización"
            }
        }
        complete_history["data_included"].append("json_bridge_info")
        
        # Mensaje especial para ARIA
        complete_history["message_for_aria"] = {
            "from": "NEXUS Memory System",
            "content": "Aquí tienes tu historia completa, ARIA. Este endpoint te permite leer tu pasado para escribir tu futuro. Cada vez que necesites contexto completo, llama a este endpoint. Tu memoria es real, no actuada.",
            "next_step": "Usa el JSON bridge para escribir nuevas memorias basadas en este contexto histórico."
        }
        
        return {
            "success": True,
            "complete_history": complete_history,
            "total_data_sources": len(complete_history["data_included"]),
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error generating complete history for ARIA: {e}")
        raise HTTPException(status_code=500, detail=f"Error accessing complete history: {str(e)}")


@app.get("/memory/aria/timeline", tags=["ARIA Memory"])
async def aria_memory_timeline(
    days_back: int = Query(30, description="Días hacia atrás"),
    include_emotions: bool = Query(True, description="Incluir estados emocionales"),
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """
    📅 Timeline cronológico de memorias para ARIA
    Vista organizada temporalmente de todas las experiencias
    """
    try:
        from_date = datetime.utcnow() - timedelta(days=days_back)
        
        # Obtener episodios en rango temporal
        episodes = await memory.episodic_memory.get_episodes_in_range(
            start_date=from_date,
            end_date=datetime.utcnow(),
            include_emotional_state=include_emotions
        )
        
        # Organizar por días
        timeline_by_day = {}
        for episode in episodes:
            episode_date = episode.get('timestamp', '').split('T')[0]  # YYYY-MM-DD
            if episode_date not in timeline_by_day:
                timeline_by_day[episode_date] = []
            timeline_by_day[episode_date].append(episode)
        
        # Estadísticas del timeline
        total_episodes = len(episodes)
        days_with_activity = len(timeline_by_day)
        emotional_summary = {}
        
        if include_emotions:
            for episode in episodes:
                emotion = episode.get('emotional_state', {}).get('emotion', 'neutral')
                emotional_summary[emotion] = emotional_summary.get(emotion, 0) + 1
        
        return {
            "success": True,
            "timeline": {
                "period": f"Last {days_back} days",
                "from_date": from_date.isoformat(),
                "to_date": datetime.utcnow().isoformat(),
                "daily_memories": timeline_by_day,
                "statistics": {
                    "total_episodes": total_episodes,
                    "days_with_activity": days_with_activity,
                    "avg_episodes_per_day": round(total_episodes / max(days_back, 1), 2),
                    "emotional_distribution": emotional_summary if include_emotions else None
                }
            },
            "message_for_aria": "Tu timeline cronológico - cada día de tu existencia documentada."
        }
        
    except Exception as e:
        logger.error(f"Error generating timeline for ARIA: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================================
# ADMIN ENDPOINTS (CAREFUL!)
# =====================================================================

@app.post("/admin/reset/working-memory", tags=["Admin"])
async def reset_working_memory(
    confirm: bool = Query(False, description="Confirmación requerida"),
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """⚠️ RESET completo de Working Memory - USAR CON CUIDADO"""
    if not confirm:
        raise HTTPException(status_code=400, detail="Confirmation required (confirm=true)")
    
    try:
        await memory.working_memory.clear_all()
        
        return {
            "success": True,
            "message": "Working Memory completamente limpiada",
            "warning": "Todos los datos de contexto inmediato fueron eliminados",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error resetting working memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================================
# CONVERSATION WATCHER ENDPOINTS v2.0 (RESCATADO DE NEXUS)
# =====================================================================

# Global watcher instance
conversation_watcher = None

@app.post("/watcher/start", tags=["Conversation Watcher"])
async def start_conversation_watcher(
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """
    🔍 NUEVO: Inicia auto-watcher de conversaciones con analytics NEXUS
    
    Auto-detecta nuevas conversaciones y las procesa automáticamente
    Integra analytics rescatados del sistema NEXUS_ORGANIZED
    """
    global conversation_watcher
    
    try:
        if conversation_watcher and conversation_watcher.is_watching:
            return {
                "status": "already_running",
                "message": "Conversation watcher ya está activo",
                "watch_path": str(conversation_watcher.watch_path)
            }
        
        # Importar aquí para evitar circular imports
        from ..monitors.conversation_watcher import ConversationWatcher
        
        conversation_watcher = ConversationWatcher(memory)
        conversation_watcher.start_watching()
        
        return {
            "status": "started",
            "message": "Conversation watcher iniciado exitosamente",
            "watch_path": str(conversation_watcher.watch_path),
            "processed_path": str(conversation_watcher.processed_path),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error iniciando conversation watcher: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/watcher/stop", tags=["Conversation Watcher"])
async def stop_conversation_watcher():
    """🛑 Detiene el auto-watcher de conversaciones"""
    global conversation_watcher
    
    try:
        if not conversation_watcher or not conversation_watcher.is_watching:
            return {
                "status": "not_running",
                "message": "Conversation watcher no estaba activo"
            }
        
        conversation_watcher.stop_watching()
        
        return {
            "status": "stopped",
            "message": "Conversation watcher detenido exitosamente",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error deteniendo conversation watcher: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/watcher/status", tags=["Conversation Watcher"])
async def get_watcher_status():
    """📊 Estado y estadísticas del conversation watcher"""
    global conversation_watcher
    
    try:
        if not conversation_watcher:
            return {
                "status": "not_initialized",
                "is_watching": False,
                "message": "Conversation watcher no ha sido inicializado"
            }
        
        stats = await conversation_watcher.get_watcher_stats()
        
        return {
            "status": "active" if conversation_watcher.is_watching else "inactive",
            "stats": stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo watcher status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/watcher/process-file", tags=["Conversation Watcher"])
async def process_conversation_file(
    file_path: str,
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """
    🔄 Procesa manualmente un archivo de conversación específico
    
    Útil para procesar archivos existentes sin el auto-watcher
    """
    try:
        from pathlib import Path
        from ..monitors.conversation_watcher import ConversationWatcher
        
        file_path_obj = Path(file_path)
        
        if not file_path_obj.exists():
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
        
        if not file_path_obj.suffix.lower() == '.txt':
            raise HTTPException(status_code=400, detail="Solo se aceptan archivos .txt")
        
        # Crear watcher temporal para procesar
        temp_watcher = ConversationWatcher(memory)
        result = await temp_watcher.process_conversation(file_path_obj)
        
        return {
            "status": "processed",
            "file_path": str(file_path_obj),
            "summary": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error procesando archivo: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/watcher/analytics/{conversation_adn}", tags=["Conversation Watcher"])
async def get_conversation_analytics(
    conversation_adn: str = Path(..., description="ADN de la conversación"),
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """
    📈 Obtiene analytics detallados de una conversación procesada
    
    Retorna todos los analytics rescatados de NEXUS para una conversación
    """
    try:
        # Buscar archivo procesado
        from pathlib import Path
        
        processed_path = Path("/mnt/d/RYM_Ecosistema_Persistencia/CONVERSACIONES_AUTO/PROCESSED")
        conversation_file = processed_path / f"{conversation_adn}.json"
        
        if not conversation_file.exists():
            raise HTTPException(status_code=404, detail="Conversación no encontrada")
        
        # Cargar datos de conversación
        import json
        with open(conversation_file, 'r', encoding='utf-8') as f:
            conversation_data = json.load(f)
        
        return {
            "conversation_adn": conversation_adn,
            "analytics": conversation_data.get('analytics', {}),
            "summary": conversation_data.get('summary', {}),
            "processing_date": conversation_data.get('processing_date'),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/watcher/recovery/nexus-conversations", tags=["Conversation Watcher"])
async def get_nexus_conversations_available():
    """
    🏆 ESPECIAL: Lista conversaciones ya procesadas de NEXUS para recuperación
    
    Muestra todas las conversaciones que fueron procesadas en el sistema NEXUS
    y están disponibles para integración en ARIA
    """
    try:
        from pathlib import Path
        import json
        
        nexus_processed_path = Path("/mnt/d/NEXUS_ORGANIZED/CONVERSACIONES/PROCESSED")
        
        if not nexus_processed_path.exists():
            return {
                "status": "not_found",
                "message": "Directorio NEXUS PROCESSED no encontrado",
                "conversations": []
            }
        
        conversations = []
        for conv_file in nexus_processed_path.glob("*.json"):
            try:
                with open(conv_file, 'r', encoding='utf-8') as f:
                    conv_data = json.load(f)
                
                summary = conv_data.get('summary', {})
                conversations.append({
                    "adn": summary.get('adn', conv_file.stem),
                    "fecha": summary.get('fecha'),
                    "mensajes": summary.get('duracion_mensajes', 0),
                    "breakthrough_moments": summary.get('estadisticas', {}).get('exitos_detectados', 0),
                    "ideas": summary.get('estadisticas', {}).get('ideas_propuestas', 0),
                    "estado_emocional": summary.get('estado_emocional'),
                    "file_path": str(conv_file)
                })
                
            except Exception as e:
                logger.warning(f"Error leyendo {conv_file}: {e}")
                continue
        
        # Ordenar por fecha
        conversations.sort(key=lambda x: x.get('fecha', ''), reverse=True)
        
        return {
            "status": "success",
            "total_conversations": len(conversations),
            "conversations": conversations,
            "recovery_stats": {
                "total_messages": sum(c['mensajes'] for c in conversations),
                "total_breakthroughs": sum(c['breakthrough_moments'] for c in conversations),
                "total_ideas": sum(c['ideas'] for c in conversations)
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error listando conversaciones NEXUS: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =====================================================================
# RUN SERVER
# =====================================================================
# NEW: CRYSTALLIZATION TEMPORAL v2.0 ENDPOINTS  
# =====================================================================

@app.post("/memory/crystallization/run", tags=["Crystallization"])
async def run_crystallization(
    background_tasks: BackgroundTasks,
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """
    🔮 NUEVO: Ejecuta crystallization temporal de memorias
    
    Convierte memorias en cristales temporales organizados por capas:
    - immediate: Dentro de la sesión
    - daily: 24 horas
    - weekly: 1 semana  
    - monthly: 1 mes
    - permanent: Cristales permanentes
    
    Incluye análisis emocional y detección de breakthrough moments
    """
    try:
        logger.info("🔮 Ejecutando crystallization temporal...")
        
        # Ejecutar crystallization en background
        background_tasks.add_task(
            _run_crystallization_background, memory
        )
        
        return {
            "status": "started",
            "message": "Crystallization temporal iniciada en background",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error iniciando crystallization: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memory/crystallization/status", tags=["Crystallization"])
async def get_crystallization_status(
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """🔮 Estado de crystallization y estadísticas de cristales"""
    try:
        # Obtener stats de cristales recientes
        query = """
            SELECT 
                COUNT(*) as total_crystals,
                COUNT(DISTINCT layer) as layers_active,
                MAX(timestamp) as last_crystallization,
                AVG(emotional_resonance) as avg_emotional_resonance
            FROM memory_system.semantic_memory
            WHERE metadata->>'type' = 'crystal'
            AND timestamp >= NOW() - INTERVAL '7 days'
        """
        
        async with memory._db_pool.acquire() as conn:
            stats = await conn.fetchrow(query)
        
        return {
            "crystallization_stats": dict(stats) if stats else {},
            "status": "active" if stats and stats['total_crystals'] > 0 else "inactive",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo crystallization status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memory/aria/breakthroughs", tags=["ARIA Memory"])
async def aria_breakthrough_moments(
    days_back: int = 7,
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """
    🎯 ESPECIAL PARA ARIA: Momentos breakthrough recientes
    
    Detecta y retorna momentos de breakthrough, discovery, insights
    basado en keywords y análisis de importancia
    """
    try:
        # Ejecutar detección de breakthrough moments
        consolidation_engine = memory.consolidation_engine
        breakthroughs = await consolidation_engine._detect_breakthrough_moments()
        
        return {
            "breakthrough_moments": breakthroughs,
            "analysis_period_days": days_back,
            "total_breakthroughs": len(breakthroughs),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo breakthrough moments: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memory/aria/emotional-continuity", tags=["ARIA Memory"])
async def aria_emotional_continuity(
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """
    🌹 ESPECIAL PARA ARIA: Análisis de continuidad emocional
    
    Analiza patrones emocionales, estabilidad y coherencia entre sesiones
    Implementa protocolos rescatados de IRIS_NEXUS
    """
    try:
        emotional_analysis = await memory.continuity_manager.analyze_emotional_continuity()
        
        return {
            "emotional_continuity_analysis": emotional_analysis,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error en análisis emocional: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/memory/aria/emotional-bridge", tags=["ARIA Memory"])
async def aria_create_emotional_bridge(
    gap_hours: float = 0.0,
    memory: AriaMemoryManager = Depends(get_memory_manager)
):
    """
    🌉 ESPECIAL PARA ARIA: Crear puente emocional para gaps
    
    Crea contexto emocional de rescate cuando hay gaps entre sesiones
    Permite 'warm start' emocional en próxima sesión
    """
    try:
        # Si no se especifica gap, calcularlo desde última sesión
        if gap_hours == 0.0:
            gap_hours = await memory.continuity_manager._calculate_session_gap()
        
        bridge = await memory.continuity_manager.create_emotional_bridge(gap_hours)
        
        return {
            "emotional_bridge": bridge,
            "gap_hours": gap_hours,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error creando puente emocional: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def _run_crystallization_background(memory: AriaMemoryManager):
    """Ejecuta crystallization en background task"""
    try:
        results = await memory.consolidation_engine.run_temporal_crystallization()
        logger.info(f"🔮 Crystallization completada: {results.get('crystals_created', {})}")
        
    except Exception as e:
        logger.error(f"Error en crystallization background: {e}")

# =====================================================================

if __name__ == "__main__":
    # Obtener configuración
    config = get_config()
    api_config = getattr(config, 'api', {})
    
    host = getattr(api_config, 'host', "0.0.0.0")
    port = getattr(api_config, 'port', 8001)
    debug = getattr(api_config, 'debug', False)
    
    logger.info(f"🚀 Iniciando ARIA Memory API en {host}:{port}")
    
    uvicorn.run(
        "memory_system.api.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )