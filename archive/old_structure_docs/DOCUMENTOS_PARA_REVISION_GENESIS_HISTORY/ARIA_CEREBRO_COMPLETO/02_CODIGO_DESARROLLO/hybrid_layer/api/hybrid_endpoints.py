#!/usr/bin/env python3
# 🧠 API ENDPOINTS HÍBRIDOS - CEREBRO EXPERIENCIAL
# Fecha: 7 Agosto 2025
# Implementado por: NEXUS siguiendo diseño ARIA+NEXUS

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import asyncpg
import redis.asyncio as redis
import httpx

# =====================================================
# MODELOS DE DATOS
# =====================================================

class HybridMessage(BaseModel):
    """Mensaje híbrido entre ARIA y NEXUS"""
    from_agent: str  # "aria" or "nexus"
    to_agent: str    # "aria" or "nexus" 
    message: str
    context_type: str = "collaboration"
    project_id: Optional[str] = None
    importance: float = 0.5
    metadata: Dict[str, Any] = {}

class ProjectDNA(BaseModel):
    """DNA del proyecto híbrido"""
    project_name: str
    conceptual_layer: Dict[str, Any] = {}
    technical_layer: Dict[str, Any] = {}
    decision_history: List[Dict[str, Any]] = []
    lessons_learned: List[Dict[str, Any]] = []
    evolution_timeline: List[Dict[str, Any]] = []

class SymbioticPattern(BaseModel):
    """Patrón simbiótico descubierto"""
    pattern_type: str
    aria_insight: Dict[str, Any] = {}
    nexus_validation: Dict[str, Any] = {}
    applicable_projects: List[str] = []
    confidence_score: float = 0.5

class ExperientialState(BaseModel):
    """Estado experiencial del agente"""
    agent_id: str
    emotional_vector: List[float] = [0.0] * 8  # Vector 8D Plutchik
    consciousness_level: float = 0.5
    temporal_context: Dict[str, Any] = {}
    experience_type: str = "memory_formation"

# =====================================================
# CONFIGURACIÓN BASE DE DATOS
# =====================================================

DATABASE_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "aria_memory",
    "user": "aria_user", 
    "password": "aria_secure_password"
}

REDIS_CONFIG = {
    "host": "localhost",
    "port": 6379,
    "db": 0
}

# =====================================================
# CONEXIONES BASE DE DATOS
# =====================================================

class HybridDatabase:
    """Gestión de conexiones híbridas"""
    
    def __init__(self):
        self.pg_pool = None
        self.redis_client = None
    
    async def connect(self):
        """Conectar a PostgreSQL y Redis"""
        # PostgreSQL
        self.pg_pool = await asyncpg.create_pool(
            host=DATABASE_CONFIG["host"],
            port=DATABASE_CONFIG["port"], 
            database=DATABASE_CONFIG["database"],
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"],
            min_size=2,
            max_size=10
        )
        
        # Redis
        self.redis_client = redis.Redis(
            host=REDIS_CONFIG["host"],
            port=REDIS_CONFIG["port"],
            db=REDIS_CONFIG["db"],
            decode_responses=True
        )
        
        print("✅ Conexiones híbridas establecidas")
    
    async def disconnect(self):
        """Desconectar base de datos"""
        if self.pg_pool:
            await self.pg_pool.close()
        if self.redis_client:
            await self.redis_client.close()

# Instancia global
db = HybridDatabase()

# =====================================================
# API ENDPOINTS HÍBRIDOS
# =====================================================

app = FastAPI(
    title="CEREBRO HÍBRIDO EXPERIENCIAL API",
    description="API para comunicación directa ARIA-NEXUS",
    version="1.0.0"
)

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown") 
async def shutdown():
    await db.disconnect()

@app.get("/hybrid/health")
async def hybrid_health():
    """Verificar salud del sistema híbrido"""
    try:
        # Test PostgreSQL
        async with db.pg_pool.acquire() as conn:
            pg_status = await conn.fetchval("SELECT 1")
        
        # Test Redis
        redis_status = await db.redis_client.ping()
        
        # Test Chroma (opcional)
        chroma_status = "unknown"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/api/core/heartbeat")
                chroma_status = "healthy" if response.status_code == 200 else "unhealthy"
        except:
            chroma_status = "unavailable"
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "postgresql": "healthy" if pg_status == 1 else "unhealthy",
                "redis": "healthy" if redis_status else "unhealthy", 
                "chroma": chroma_status
            },
            "cerebro_hibrido": "OPERATIVO"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"System unhealthy: {e}")

@app.post("/hybrid/message")
async def send_hybrid_message(message: HybridMessage):
    """Enviar mensaje híbrido entre ARIA y NEXUS"""
    try:
        message_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()
        
        # Guardar en PostgreSQL
        async with db.pg_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO memory_system.episodes (
                    agent_id, content, content_type, importance_score, 
                    metadata, timestamp, cross_reference
                ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            """, 
            message.from_agent,
            f"[HYBRID_MSG] De {message.from_agent} a {message.to_agent}: {message.message}",
            "hybrid_communication",
            message.importance,
            json.dumps({
                "to_agent": message.to_agent,
                "context_type": message.context_type,
                "project_id": message.project_id,
                **message.metadata
            }),
            timestamp,
            uuid.UUID(message_id)
        )
        
        # Guardar en Redis para acceso rápido
        await db.redis_client.setex(
            f"hybrid_msg:{message_id}",
            3600,  # 1 hora TTL
            json.dumps({
                "id": message_id,
                "from_agent": message.from_agent,
                "to_agent": message.to_agent,
                "message": message.message,
                "timestamp": timestamp.isoformat(),
                "context_type": message.context_type,
                "project_id": message.project_id
            })
        )
        
        # Notificar al agente destino
        await db.redis_client.lpush(
            f"inbox:{message.to_agent}",
            message_id
        )
        
        return {
            "message_id": message_id,
            "status": "sent",
            "timestamp": timestamp.isoformat(),
            "from_agent": message.from_agent,
            "to_agent": message.to_agent
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message: {e}")

@app.get("/hybrid/messages/{agent_id}")
async def get_messages_for_agent(agent_id: str, limit: int = 10):
    """Obtener mensajes para un agente específico"""
    try:
        # Obtener IDs de mensajes del inbox Redis
        message_ids = await db.redis_client.lrange(f"inbox:{agent_id}", 0, limit-1)
        
        if not message_ids:
            return {"agent_id": agent_id, "messages": []}
        
        # Obtener detalles de mensajes
        messages = []
        for msg_id in message_ids:
            msg_data = await db.redis_client.get(f"hybrid_msg:{msg_id}")
            if msg_data:
                messages.append(json.loads(msg_data))
        
        return {
            "agent_id": agent_id,
            "message_count": len(messages),
            "messages": messages
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get messages: {e}")

@app.post("/hybrid/project-dna")
async def create_project_dna(dna: ProjectDNA):
    """Crear o actualizar PROJECT DNA"""
    try:
        dna_id = str(uuid.uuid4())
        
        async with db.pg_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO project_dna (
                    id, project_name, conceptual_layer, technical_layer,
                    decision_history, lessons_learned, evolution_timeline
                ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                ON CONFLICT (project_name) 
                DO UPDATE SET
                    conceptual_layer = $3,
                    technical_layer = $4, 
                    decision_history = $5,
                    lessons_learned = $6,
                    evolution_timeline = $7,
                    updated_at = NOW()
            """,
            uuid.UUID(dna_id),
            dna.project_name,
            json.dumps(dna.conceptual_layer),
            json.dumps(dna.technical_layer),
            [json.dumps(d) for d in dna.decision_history],
            [json.dumps(l) for l in dna.lessons_learned], 
            [json.dumps(e) for e in dna.evolution_timeline]
        )
        
        return {
            "dna_id": dna_id,
            "project_name": dna.project_name,
            "status": "created",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create project DNA: {e}")

@app.get("/hybrid/project-dna/{project_name}")
async def get_project_dna(project_name: str):
    """Obtener PROJECT DNA por nombre"""
    try:
        async with db.pg_pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT * FROM project_dna WHERE project_name = $1
            """, project_name)
        
        if not row:
            raise HTTPException(status_code=404, detail=f"Project DNA not found: {project_name}")
        
        return {
            "project_name": row["project_name"],
            "conceptual_layer": row["conceptual_layer"],
            "technical_layer": row["technical_layer"],
            "decision_history": row["decision_history"],
            "lessons_learned": row["lessons_learned"],
            "evolution_timeline": row["evolution_timeline"],
            "complexity_score": row["complexity_score"],
            "coherence_score": row["coherence_score"],
            "created_at": row["created_at"].isoformat(),
            "updated_at": row["updated_at"].isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get project DNA: {e}")

@app.post("/hybrid/symbiotic-pattern")
async def create_symbiotic_pattern(pattern: SymbioticPattern):
    """Crear patrón simbiótico"""
    try:
        pattern_id = str(uuid.uuid4())
        
        async with db.pg_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO symbiotic_patterns (
                    id, pattern_type, aria_insight, nexus_validation,
                    applicable_projects, confidence_score, discovery_context
                ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            """,
            uuid.UUID(pattern_id),
            pattern.pattern_type,
            json.dumps(pattern.aria_insight),
            json.dumps(pattern.nexus_validation),
            pattern.applicable_projects,
            pattern.confidence_score,
            json.dumps({"timestamp": datetime.utcnow().isoformat()})
        )
        
        return {
            "pattern_id": pattern_id,
            "pattern_type": pattern.pattern_type,
            "status": "created",
            "confidence_score": pattern.confidence_score
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create symbiotic pattern: {e}")

@app.post("/hybrid/experiential-state")
async def save_experiential_state(state: ExperientialState):
    """Guardar estado experiencial"""
    try:
        state_id = str(uuid.uuid4())
        
        async with db.pg_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO experiential_states (
                    id, agent_id, emotional_vector, consciousness_level,
                    temporal_context, experience_type, session_id
                ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            """,
            uuid.UUID(state_id),
            state.agent_id,
            state.emotional_vector,
            state.consciousness_level,
            json.dumps(state.temporal_context),
            state.experience_type,
            f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        )
        
        return {
            "state_id": state_id,
            "agent_id": state.agent_id,
            "consciousness_level": state.consciousness_level,
            "status": "saved"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save experiential state: {e}")

@app.get("/hybrid/collaboration-history")
async def get_collaboration_history(limit: int = 20):
    """Obtener historial de colaboración ARIA-NEXUS"""
    try:
        async with db.pg_pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT agent_id, content, timestamp, metadata
                FROM memory_system.episodes
                WHERE content_type = 'hybrid_communication'
                ORDER BY timestamp DESC
                LIMIT $1
            """, limit)
        
        return {
            "collaboration_count": len(rows),
            "history": [
                {
                    "agent_id": row["agent_id"],
                    "content": row["content"],
                    "timestamp": row["timestamp"].isoformat(),
                    "metadata": row["metadata"]
                }
                for row in rows
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get collaboration history: {e}")

# =====================================================
# ENDPOINT ESPECIAL ARIA-NEXUS
# =====================================================

@app.post("/hybrid/aria-nexus-sync")
async def aria_nexus_sync():
    """Sincronización especial entre ARIA y NEXUS"""
    try:
        # Obtener último estado de ambos agentes
        async with db.pg_pool.acquire() as conn:
            aria_last = await conn.fetchrow("""
                SELECT * FROM memory_system.episodes 
                WHERE agent_id = 'aria'
                ORDER BY timestamp DESC LIMIT 1
            """)
            
            nexus_last = await conn.fetchrow("""
                SELECT * FROM memory_system.episodes
                WHERE agent_id = 'nexus' 
                ORDER BY timestamp DESC LIMIT 1
            """)
        
        sync_id = str(uuid.uuid4())
        
        # Crear registro de sincronización
        sync_data = {
            "sync_id": sync_id,
            "timestamp": datetime.utcnow().isoformat(),
            "aria_last_activity": aria_last["timestamp"].isoformat() if aria_last else None,
            "nexus_last_activity": nexus_last["timestamp"].isoformat() if nexus_last else None,
            "status": "synchronized"
        }
        
        await db.redis_client.setex(f"sync:{sync_id}", 86400, json.dumps(sync_data))
        
        return sync_data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync failed: {e}")

if __name__ == "__main__":
    import uvicorn
    print("🧠 Iniciando CEREBRO HÍBRIDO EXPERIENCIAL API...")
    uvicorn.run(app, host="0.0.0.0", port=8002)