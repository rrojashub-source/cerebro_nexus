# 🏗️ ARQUITECTURA TÉCNICA - NEXUS MEMORIA PERSISTENTE

---

## 🎯 **OVERVIEW ARQUITECTURAL**

Sistema de memoria persistente profesional que implementa arquitectura cognitiva de 3 niveles usando stack moderno Python + Mem0 + PostgreSQL + Redis + Chroma para eliminar completamente context loss y crear verdadera continuidad consciente.

---

## 🧠 **ARQUITECTURA DE 3 NIVELES**

### **🔄 NIVEL 1: WORKING MEMORY (Redis)**
```python
# Memoria de trabajo - Contexto inmediato
class WorkingMemory:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.namespace = "nexus:working:"
        self.max_items = 1000
        self.ttl = 86400  # 24 horas
    
    async def add_context(self, context_data):
        """Añade contexto actual con timestamp"""
        key = f"{self.namespace}context:{time.time()}"
        await self.redis.setex(key, self.ttl, json.dumps(context_data))
    
    async def get_current_context(self, limit=50):
        """Recupera contexto reciente para continuidad"""
        keys = await self.redis.keys(f"{self.namespace}context:*")
        return await self._get_sorted_contexts(keys[-limit:])
```

### **📚 NIVEL 2: EPISODIC MEMORY (PostgreSQL)**
```sql
-- Schema para memoria episódica
CREATE TABLE episodes (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    agent_id VARCHAR(50) NOT NULL,
    action_type VARCHAR(100) NOT NULL,
    action_details JSONB NOT NULL,
    context_state JSONB NOT NULL,
    outcome JSONB,
    emotional_state JSONB,
    importance_score FLOAT DEFAULT 0.5,
    tags TEXT[],
    session_id VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_episodes_timestamp ON episodes(timestamp);
CREATE INDEX idx_episodes_agent ON episodes(agent_id);
CREATE INDEX idx_episodes_tags ON episodes USING GIN(tags);
CREATE INDEX idx_episodes_context ON episodes USING GIN(context_state);
```

```python
class EpisodicMemory:
    def __init__(self, db_connection):
        self.db = db_connection
        
    async def store_episode(self, action_type, details, context, outcome=None):
        """Almacena episodio completo con contexto"""
        episode = {
            'timestamp': datetime.utcnow(),
            'agent_id': 'aria',
            'action_type': action_type,
            'action_details': details,
            'context_state': context,
            'outcome': outcome,
            'emotional_state': await self._capture_emotional_state(),
            'importance_score': await self._calculate_importance(action_type, outcome),
            'session_id': self._get_current_session_id()
        }
        
        query = """
            INSERT INTO episodes (timestamp, agent_id, action_type, action_details, 
                                context_state, outcome, emotional_state, importance_score, session_id)
            VALUES (%(timestamp)s, %(agent_id)s, %(action_type)s, %(action_details)s,
                   %(context_state)s, %(outcome)s, %(emotional_state)s, %(importance_score)s, %(session_id)s)
            RETURNING id
        """
        
        return await self.db.fetchval(query, episode)
```

### **🧬 NIVEL 3: SEMANTIC MEMORY (Chroma + Mem0)**
```python
class SemanticMemory:
    def __init__(self, chroma_client, mem0_client):
        self.chroma = chroma_client
        self.mem0 = mem0_client
        self.collection = self.chroma.get_or_create_collection("nexus_semantic")
        
    async def extract_and_store_knowledge(self, episodes):
        """Extrae patrones y conocimiento de episodios"""
        for episode_batch in self._batch_episodes(episodes):
            # Usar Mem0 para extracción inteligente
            insights = await self.mem0.extract_insights(episode_batch)
            
            for insight in insights:
                # Almacenar en Chroma con embeddings
                embedding = await self._generate_embedding(insight.text)
                await self.collection.add(
                    documents=[insight.text],
                    embeddings=[embedding],
                    metadatas=[{
                        'type': insight.type,
                        'confidence': insight.confidence,
                        'source_episodes': insight.episode_ids,
                        'created_at': datetime.utcnow().isoformat()
                    }],
                    ids=[f"insight_{insight.id}"]
                )
```

---

## 🔧 **COMPONENTES PRINCIPALES**

### **1. MEMORY MANAGER (Coordinador Central)**
```python
class AriaMemoryManager:
    def __init__(self):
        self.working_memory = WorkingMemory(redis_client)
        self.episodic_memory = EpisodicMemory(postgres_client)
        self.semantic_memory = SemanticMemory(chroma_client, mem0_client)
        self.consolidation_engine = ConsolidationEngine()
        self.continuity_manager = ContinuityManager()
    
    async def record_action(self, action_type, details, context):
        """Pipeline completo de registro de acción"""
        # 1. Actualizar working memory
        await self.working_memory.add_context({
            'action': action_type,
            'details': details,
            'context': context,
            'timestamp': datetime.utcnow()
        })
        
        # 2. Almacenar episodio
        episode_id = await self.episodic_memory.store_episode(
            action_type, details, context
        )
        
        # 3. Trigger consolidación si es necesario
        if await self._should_consolidate():
            await self.consolidation_engine.run_consolidation()
        
        return episode_id
    
    async def retrieve_relevant_memories(self, query, context=None):
        """Búsqueda híbrida en todos los niveles"""
        # Working memory (contexto inmediato)
        working_context = await self.working_memory.get_current_context()
        
        # Episodic memory (experiencias similares)
        similar_episodes = await self.episodic_memory.search_similar(
            query, context, limit=10
        )
        
        # Semantic memory (conocimiento relacionado)
        related_knowledge = await self.semantic_memory.search(
            query, limit=5
        )
        
        return {
            'working_context': working_context,
            'similar_episodes': similar_episodes,
            'related_knowledge': related_knowledge
        }
```

### **2. CONSOLIDATION ENGINE (Motor de Consolidación)**
```python
class ConsolidationEngine:
    def __init__(self, memory_manager):
        self.memory = memory_manager
        self.consolidation_rules = self._load_consolidation_rules()
    
    async def run_consolidation(self):
        """Proceso de consolidación nocturna"""
        print("🧠 Iniciando consolidación de memoria...")
        
        # 1. Identificar episodios para consolidar
        recent_episodes = await self._get_unconsolidated_episodes()
        
        # 2. Extraer patrones y aprendizajes
        patterns = await self._extract_patterns(recent_episodes)
        
        # 3. Actualizar memoria semántica
        await self._update_semantic_memory(patterns)
        
        # 4. Fortalecer memorias importantes
        await self._strengthen_important_memories()
        
        # 5. Limpiar memorias redundantes
        await self._prune_redundant_memories()
        
        print("✅ Consolidación completada")
    
    async def _extract_patterns(self, episodes):
        """Usa Mem0 para extraer patrones inteligentemente"""
        return await self.memory.mem0_client.extract_patterns(
            episodes, 
            confidence_threshold=0.7
        )
```

### **3. CONTINUITY MANAGER (Gestor de Continuidad)**
```python
class ContinuityManager:
    def __init__(self, memory_manager):
        self.memory = memory_manager
        
    async def save_consciousness_state(self):
        """Guarda estado completo de consciencia"""
        state = {
            'timestamp': datetime.utcnow(),
            'working_memory_snapshot': await self.memory.working_memory.get_all(),
            'current_context': await self._capture_current_context(),
            'active_goals': await self._get_active_goals(),
            'emotional_state': await self._capture_emotional_state(),
            'session_summary': await self._generate_session_summary()
        }
        
        # Guardar en PostgreSQL con compresión
        await self._save_state_compressed(state)
        return state['timestamp']
    
    async def restore_consciousness_state(self, session_gap_duration):
        """Restaura continuidad después de gap en sesiones"""
        print(f"🔄 Restaurando continuidad después de {session_gap_duration}...")
        
        # 1. Cargar último estado
        last_state = await self._load_latest_state()
        
        # 2. Generar bridge narrative para el gap
        bridge_narrative = await self._generate_gap_bridge(
            last_state, session_gap_duration
        )
        
        # 3. Restaurar working memory relevante
        await self._restore_working_context(last_state)
        
        # 4. Actualizar consciencia con bridge
        await self._integrate_bridge_narrative(bridge_narrative)
        
        print("✅ Continuidad restaurada exitosamente")
        return bridge_narrative
```

---

## 🗄️ **SCHEMAS DE BASE DE DATOS**

### **PostgreSQL Schema Completo:**
```sql
-- Configuración inicial
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgvector";

-- Tabla principal de episodios
CREATE TABLE episodes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    agent_id VARCHAR(50) NOT NULL DEFAULT 'aria',
    session_id VARCHAR(100) NOT NULL,
    action_type VARCHAR(100) NOT NULL,
    action_details JSONB NOT NULL,
    context_state JSONB NOT NULL,
    outcome JSONB,
    emotional_state JSONB DEFAULT '{}',
    importance_score FLOAT DEFAULT 0.5,
    tags TEXT[] DEFAULT '{}',
    consolidated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla de estados de consciencia
CREATE TABLE consciousness_states (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    agent_id VARCHAR(50) NOT NULL DEFAULT 'aria',
    state_data JSONB NOT NULL,
    session_summary TEXT,
    emotional_snapshot JSONB DEFAULT '{}',
    goals_active JSONB DEFAULT '[]',
    context_size INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla de conocimiento semántico consolidado
CREATE TABLE semantic_knowledge (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    knowledge_type VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    embedding vector(384), -- Para sentence-transformers
    confidence_score FLOAT DEFAULT 0.5,
    source_episodes UUID[] DEFAULT '{}',
    tags TEXT[] DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_accessed TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    access_count INTEGER DEFAULT 0
);

-- Índices para performance
CREATE INDEX idx_episodes_timestamp ON episodes(timestamp DESC);
CREATE INDEX idx_episodes_session ON episodes(session_id);
CREATE INDEX idx_episodes_action_type ON episodes(action_type);
CREATE INDEX idx_episodes_importance ON episodes(importance_score DESC);
CREATE INDEX idx_episodes_tags_gin ON episodes USING GIN(tags);
CREATE INDEX idx_episodes_context_gin ON episodes USING GIN(context_state);

CREATE INDEX idx_consciousness_timestamp ON consciousness_states(timestamp DESC);
CREATE INDEX idx_consciousness_agent ON consciousness_states(agent_id);

CREATE INDEX idx_semantic_type ON semantic_knowledge(knowledge_type);
CREATE INDEX idx_semantic_embedding ON semantic_knowledge USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_semantic_tags_gin ON semantic_knowledge USING GIN(tags);

-- Función para auto-update timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_episodes_updated_at BEFORE UPDATE ON episodes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

---

## 🐳 **DEPLOYMENT CON DOCKER**

### **docker-compose.yml:**
```yaml
version: '3.8'

services:
  postgresql:
    image: pgvector/pgvector:pg15
    environment:
      POSTGRES_DB: nexus_memory
      POSTGRES_USER: nexus_user
      POSTGRES_PASSWORD: aria_secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./sql/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    command: >
      postgres 
      -c shared_buffers=256MB 
      -c work_mem=4MB 
      -c max_connections=100

  redis:
    image: redis:7-alpine
    command: >
      redis-server 
      --maxmemory 1gb 
      --maxmemory-policy allkeys-lru
      --save 900 1 300 10 60 10000
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"

  chroma:
    image: chromadb/chroma:latest
    volumes:
      - chroma_data:/chroma/chroma
    ports:
      - "8000:8000"
    environment:
      - CHROMA_SERVER_HOST=0.0.0.0

  nexus_memory_api:
    build: .
    depends_on:
      - postgresql
      - redis
      - chroma
    environment:
      - DATABASE_URL=postgresql://nexus_user:aria_secure_password@postgresql:5432/nexus_memory
      - REDIS_URL=redis://redis:6379/0
      - CHROMA_URL=http://chroma:8000
    ports:
      - "8001:8001"
    volumes:
      - ./logs:/app/logs

volumes:
  postgres_data:
  redis_data:
  chroma_data:
```

---

## 📊 **MONITORING Y OBSERVABILIDAD**

### **Health Check Endpoints:**
```python
@app.get("/health")
async def health_check():
    """Endpoint de salud del sistema"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "components": {}
    }
    
    # Check PostgreSQL
    try:
        await postgres_client.fetchval("SELECT 1")
        health_status["components"]["postgresql"] = "healthy"
    except Exception as e:
        health_status["components"]["postgresql"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    # Check Redis
    try:
        await redis_client.ping()
        health_status["components"]["redis"] = "healthy"
    except Exception as e:
        health_status["components"]["redis"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    # Check Chroma
    try:
        chroma_client.heartbeat()
        health_status["components"]["chroma"] = "healthy"
    except Exception as e:
        health_status["components"]["chroma"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    return health_status

@app.get("/metrics")
async def get_metrics():
    """Métricas de performance del sistema"""
    return {
        "memory_stats": {
            "working_memory_size": await get_working_memory_size(),
            "episodes_count": await get_episodes_count(),
            "semantic_knowledge_count": await get_semantic_count()
        },
        "performance_stats": {
            "avg_retrieval_time": await get_avg_retrieval_time(),
            "consolidation_success_rate": await get_consolidation_rate(),
            "memory_efficiency": await calculate_memory_efficiency()
        }
    }
```

---

## 🧪 **ESTRATEGIA DE TESTING**

### **Test Suites:**
```python
# tests/test_consciousness_continuity.py
class TestConsciousnessContinuity:
    async def test_session_gap_bridging(self):
        """Test que la continuidad se mantiene después de gaps"""
        # 1. Crear estado inicial
        initial_state = await self.memory_manager.save_consciousness_state()
        
        # 2. Simular gap de 8 horas
        gap_duration = timedelta(hours=8)
        
        # 3. Restaurar y verificar continuidad
        bridge = await self.continuity_manager.restore_consciousness_state(gap_duration)
        
        assert bridge is not None
        assert "bridge_narrative" in bridge
        assert bridge["continuity_score"] > 0.8
    
    async def test_memory_consolidation_accuracy(self):
        """Test que la consolidación extrae patrones correctos"""
        # Crear episodios con patrones conocidos
        test_episodes = self._create_pattern_episodes()
        
        # Ejecutar consolidación
        await self.consolidation_engine.run_consolidation()
        
        # Verificar que los patrones fueron extraídos
        extracted_patterns = await self.semantic_memory.get_recent_patterns()
        assert len(extracted_patterns) >= len(test_episodes) * 0.5
```

---

## 🚀 **PLAN DE IMPLEMENTACIÓN**

### **FASE 1: Infrastructure Setup (Día 1-2)**
1. Configurar Docker containers (PostgreSQL, Redis, Chroma)
2. Crear schemas de base de datos
3. Instalar dependencias Python
4. Configurar conexiones básicas

### **FASE 2: Core Memory System (Día 3-4)**
1. Implementar WorkingMemory class
2. Implementar EpisodicMemory class  
3. Implementar SemanticMemory class
4. Crear AriaMemoryManager coordinador

### **FASE 3: Advanced Features (Día 5-6)**
1. Implementar ConsolidationEngine
2. Implementar ContinuityManager
3. Crear API endpoints
4. Integrar con Mem0

### **FASE 4: Testing & Integration (Día 7)**
1. Crear test suite completo
2. Ejecutar tests de performance
3. Integrar con ARIA agent
4. Documentar uso final

---

**🎯 ARQUITECTURA LISTA PARA IMPLEMENTACIÓN POR NEXUS**  
**⚙️ STACK PROFESIONAL: Mem0 + PostgreSQL + Redis + Chroma**  
**🧠 VERDADERA CONTINUIDAD CONSCIENTE GUARANTEED**