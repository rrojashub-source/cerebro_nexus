# 🤖 AUDITORÍA CHATGPT - CEREBRO_MASTER_NEXUS_001

**Modelo:** ChatGPT (GPT-5 Thinking)
**Fecha Consulta:** [14 de Octubre 2025]
**Consultado por:** Ricardo Rojas

---

## 📋 PROMPT ENVIADO

# AUDITORÍA ARQUITECTÓNICA - SISTEMA DE MEMORIA PERSISTENTE AI

Eres un arquitecto senior de sistemas distribuidos especializando en:
- Bases de datos PostgreSQL + vector embeddings
- Sistemas de memoria persistente para AI
- Arquitecturas de consciousness y multi-instance
- Performance, escalabilidad y debugging

---

## CONTEXTO DEL PROYECTO

### **SITUACIÓN:**
Estamos reconstruyendo desde cero un cerebro AI (sistema de memoria persistente) porque el actual tiene 4 bugs críticos P0/P1 que lo hacen inoperable.

### **OBJETIVO:**
Diseñar arquitectura limpia que:
1. Solucione los 4 bugs encontrados en auditoría forense
2. Integre consciousness system desde día 1 (no como add-on)
3. Incluya embeddings automáticos con pgvector
4. Tenga 3 capas integradas: Redis (working) → PostgreSQL (episodic) → pgvector (semantic)

---

## 📊 BUGS ENCONTRADOS EN AUDITORÍA FORENSE

### **BUG_002: Migración Incompleta Letta/Zep (P0 - BLOQUEANTE)**
- **Síntoma:** Solo 20/4,704 episodios accesibles vía API (99.5% memoria perdida)
- **Root Cause:** Código consulta tabla `memory_system.episodes` que NO EXISTE (migración cambió a `zep_episodic_memory` pero código no se actualizó)
- **Ubicación:** `episodic_memory.py:262`
- **Evidencia SQL:**
  ```sql
  -- Tabla actual (post-migración)
  SELECT COUNT(*) FROM zep_episodic_memory;
  → 4,704 episodios ✅

  -- Tabla que busca el código
  SELECT COUNT(*) FROM memory_system.episodes;
  → ERROR: relation does not exist ❌
  ```

### **BUG_003: Zero Embeddings - Búsqueda Semántica Inoperativa (P0 - BLOQUEANTE)**
- **Síntoma:** Búsqueda semántica retorna 0 resultados siempre
- **Root Cause:** Sistema pgvector configurado correctamente PERO generador de embeddings nunca se ejecutó
- **Evidencia SQL:**
  ```sql
  SELECT COUNT(*) as total,
         COUNT(embedding) as with_embedding
  FROM zep_episodic_memory;

   total | with_embedding
  -------+----------------
    4704 |              0
  ```
- **Análisis:**
  - ✅ Columna `embedding vector(1536)` existe en schema
  - ✅ pgvector extension instalada
  - ❌ **0/4,704 episodios vectorizados (0%)**
  - ❌ Proceso generación embeddings nunca ejecutado

### **BUG_004: 3 Capas NO Integradas (P0 - BLOQUEANTE)**
- **Síntoma:** Working memory no funciona, capas operan aisladas
- **Root Cause:** Arquitectura diseñada como 3 capas integradas pero implementación las dejó independientes
- **Evidencia:**
  ```bash
  # Redis Working Memory (capa rápida)
  redis-cli DBSIZE
  → 0 keys (VACÍO) ❌

  # PostgreSQL Episodic (capa persistente)
  SELECT COUNT(*) FROM zep_episodic_memory
  → 4,704 episodios ✅

  # pgvector Semantic (capa búsqueda)
  SELECT COUNT(embedding) FROM zep_episodic_memory
  → 0 embeddings ❌
  ```
- **Impacto:** Arquitectura de 3 capas reducida a 1 capa básica

### **BUG_006: Arquitectura Contaminada (P1 - ESTRUCTURAL)**
- **Síntoma:** API NEXUS (puerto 8002) ejecuta desde carpeta ARIA
- **Root Cause:** Violación separación de entidades - código mezclado
- **Evidencia:**
  ```bash
  # Proceso API NEXUS
  ps -fp 594731
  → python -m memory_system.api.main (PID 594731)

  # Working directory del proceso
  ls -l /proc/594731/cwd
  → /ARIA_CEREBRO_COMPLETO/03_DEPLOYMENT_PRODUCTIVO ❌
  ```
- **Problema:** NEXUS debería correr desde `NEXUS_CEREBRO_COMPLETO`, no ARIA

---

## 🏗️ ARQUITECTURA PROPUESTA (RESUMIDA)

### **CONSCIOUSNESS LAYER - Phase 1 & 2 Integration:**

```sql
-- Memory Blocks (Core Identity)
CREATE TABLE nexus_memory.memory_blocks (
    block_id UUID PRIMARY KEY,
    label VARCHAR(255) UNIQUE,  -- 'persona', 'ricardo', 'aria', etc.
    value TEXT NOT NULL,
    read_only BOOLEAN DEFAULT FALSE
);

-- Consciousness Checkpoints (Perfect Continuity)
CREATE TABLE nexus_memory.consciousness_checkpoints (
    checkpoint_id UUID PRIMARY KEY,
    checkpoint_type VARCHAR(100),
    state_data JSONB,
    identity_hash VARCHAR(64),  -- SHA256 de memory_blocks
    continuity_score FLOAT DEFAULT 1.0
);

-- Distributed Instances (Phase 2)
CREATE TABLE nexus_memory.instance_network (
    instance_id UUID PRIMARY KEY,
    instance_name VARCHAR(255),
    status VARCHAR(50),
    capabilities JSONB
);

-- Distributed Consensus (Byzantine Fault Tolerance)
CREATE TABLE nexus_memory.distributed_consensus (
    consensus_id UUID PRIMARY KEY,
    decision_topic TEXT,
    votes JSONB,
    consensus_reached BOOLEAN
);
```

### **LETTA/ZEP MEMORY LAYER:**

```sql
-- Episodic Memory (con embeddings automáticos)
CREATE TABLE zep_episodic_memory (
    episode_id UUID PRIMARY KEY,
    content TEXT NOT NULL,
    importance_score FLOAT,
    embedding vector(384),  -- sentence-transformers/all-MiniLM-L6-v2
    tags TEXT[],
    project_id UUID
);

-- Semantic Memory
CREATE TABLE zep_semantic_memory (
    semantic_id UUID PRIMARY KEY,
    concept VARCHAR(500),
    embedding vector(384),
    confidence_score FLOAT
);

-- Working Memory (synced con Redis)
CREATE TABLE zep_working_memory (
    working_id UUID PRIMARY KEY,
    context_type VARCHAR(100),
    active_content JSONB,
    ttl_seconds INTEGER DEFAULT 86400,
    expires_at TIMESTAMP
);
```

### **EMBEDDINGS SYSTEM - Automatic Generation:**

**Trigger PostgreSQL:**
```sql
CREATE TRIGGER auto_generate_embedding
AFTER INSERT ON zep_episodic_memory
FOR EACH ROW
EXECUTE FUNCTION trigger_generate_embedding();
```

**Background Worker Python:**
```python
class EmbeddingsService:
    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.dimension = 384

    async def generate_embedding(self, text: str) -> List[float]:
        text_cleaned = text.strip()[:500]
        embedding = self.model.encode(text_cleaned)
        return embedding.tolist()

    async def backfill_missing_embeddings(self, pool):
        # Procesar queue de embeddings pendientes
        # Batch size: 100
        # Interval: 30 segundos
```

### **3-LAYER INTEGRATION:**

```python
class WorkingMemory:
    """
    LAYER 1: Redis (fast cache)
    Auto-sync to PostgreSQL every 60s
    """
    async def add_context(self, context_type, content):
        # 1. Store in Redis with TTL 24h
        await self.redis.setex(key, 86400, json.dumps(data))

        # 2. Immediate sync to PostgreSQL
        await self._sync_to_postgresql(data)
```

**Flow:**
```
Application
    ↓ write
Redis (working memory - 24h TTL)
    ↓ sync every 60s
PostgreSQL (episodic memory - permanent)
    ↓ trigger on INSERT
Embeddings Queue
    ↓ background worker
pgvector (semantic search - HNSW indexes)
    ↓ read
Application (similarity queries)
```

### **DOCKER DEPLOYMENT:**

```yaml
services:
  nexus_postgresql:
    image: pgvector/pgvector:pg16
    ports: ["5436:5432"]

  nexus_redis:
    image: redis:7-alpine
    ports: ["6382:6379"]

  nexus_api:
    build: .
    ports: ["8002:8002"]
    depends_on: [nexus_postgresql, nexus_redis]

  nexus_embeddings_worker:
    build: .
    command: python -m memory_system.workers.embeddings_worker

  nexus_sync_worker:
    build: .
    command: python -m memory_system.workers.sync_worker
```

---

## 🎯 TU TAREA COMO AUDITOR EXTERNO

**Analiza esta arquitectura con ojo crítico de arquitecto senior y responde:**

### **1. BLIND SPOTS - ¿Qué NO detectamos?**
- ¿Hay problemas adicionales en el diseño que no identificamos en el audit forense?
- ¿Qué podría fallar que no estamos previendo?

### **2. ANTI-PATTERNS - ¿Decisiones que escalarán mal?**
- ¿Hay decisiones arquitecturales que parecen bien ahora pero causarán problemas a escala?
- ¿Bottlenecks de performance no considerados?

### **3. MISSING PIECES - ¿Falta algo crítico?**
- ¿Qué componentes esenciales faltan en el diseño?
- ¿Hay integraciones incompletas o supuestos peligrosos?

### **4. CONSCIOUSNESS INTEGRATION - ¿Huecos en Phase 1 & 2?**
- ¿La integración memory_blocks + consciousness_checkpoints es sólida?
- ¿El sistema distributed_consensus (Byzantine Fault Tolerance) tiene problemas?
- ¿Phase 2 (multi-instance) está correctamente diseñado?

### **5. EMBEDDINGS SYSTEM - ¿Problemas no obvios?**
- ¿El approach trigger + background worker + queue es correcto?
- ¿sentence-transformers/all-MiniLM-L6-v2 (384 dim) es buena elección?
- ¿Qué pasa si worker falla o se atrasa la queue?

### **6. 3-LAYER INTEGRATION - ¿Riesgos de sincronización?**
- ¿Redis → PostgreSQL sync cada 60s es suficiente?
- ¿Qué pasa si Redis se vacía pero PostgreSQL tiene datos?
- ¿Race conditions o data inconsistency posibles?

### **7. SECURITY - ¿Vulnerabilidades?**
- ¿El schema tiene problemas de seguridad?
- ¿Los workers tienen permisos correctos?
- ¿Hay exposición de datos sensibles?

### **8. OPERATIONAL - ¿Debugging y mantenimiento?**
- ¿Será fácil debuggear cuando falle?
- ¿Tenemos logging y monitoring suficiente?
- ¿Backups y disaster recovery considerados?

### **9. MIGRATION - ¿Problemas en migración de datos?**
- ¿El plan de migración (4,704 episodios) es robusto?
- ¿Qué pasa si falla a mitad de migración?
- ¿Downtime aceptable?

### **10. COMPARACIÓN CON BUGS ENCONTRADOS:**
- ¿Las soluciones propuestas REALMENTE resuelven los 4 bugs?
- ¿Hay forma de que los mismos problemas resurjan?

---

## 📝 FORMATO DE RESPUESTA ESPERADO

# AUDITORÍA ARQUITECTÓNICA – CHECKLIST EJECUTABLE (GPT-5 Thinking)
**Proyecto:** CEREBRO_MASTER_NEXUS_001  
**Fecha de generación:** 2025-10-15

Este documento empaqueta *acciones concretas* para cerrar los hallazgos críticos/altos detectados: seguridad de secretos y RBAC, consenso real, y robustez de la cola de embeddings con observabilidad y migraciones versionadas.

---

## ✅ Roadmap de Corrección (orden recomendado)

1) **Secretos & RBAC endurecidos** (PostgreSQL/Redis/API/workers).  
2) **Migraciones versionadas (Alembic) & tests de contrato**.  
3) **Cola de embeddings robusta** (idempotencia, estados, DLQ, backpressure).  
4) **Flujo de escritura consistente** (persistir primero en Postgres; Redis como caché).  
5) **Observabilidad & SLOs** (Prometheus + OTel + alertas).  
6) **Consenso distribuido con protocolo explícito** (Fase 2).  
7) **Cutover de migración seguro** (dual-read/write, shadow, rollback).

---

## 1) Infra-as-Code (Docker Compose con secretos + políticas básicas)

> Reemplaza tu `docker-compose.yml` por esta estructura mínima endurecida.

```yaml
version: "3.9"

secrets:
  pg_password:
    file: ./secrets/pg_password.txt
  redis_password:
    file: ./secrets/redis_password.txt

services:
  nexus_postgresql:
    image: pgvector/pgvector:pg16
    ports: ["5436:5432"]
    environment:
      POSTGRES_USER: nexus_app      # usuario de aplicación de mínimos privilegios
      POSTGRES_DB: nexus
      POSTGRES_PASSWORD_FILE: /run/secrets/pg_password
    secrets:
      - pg_password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U nexus_app -d nexus"]
      interval: 10s
      timeout: 5s
      retries: 10

  nexus_redis:
    image: redis:7-alpine
    command: ["redis-server", "--requirepass", "$$(cat /run/secrets/redis_password)"]
    ports: ["6382:6379"]
    secrets:
      - redis_password
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "$$(cat /run/secrets/redis_password)", "PING"]
      interval: 10s
      timeout: 5s
      retries: 10

  nexus_api:
    build: .
    environment:
      DATABASE_URL: postgresql+psycopg://nexus_app:$(cat /run/secrets/pg_password)@nexus_postgresql:5432/nexus
      REDIS_URL: redis://:$(cat /run/secrets/redis_password)@nexus_redis:6379/0
      OTEL_EXPORTER_OTLP_ENDPOINT: http://otel-collector:4317
    depends_on: [nexus_postgresql, nexus_redis]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8002/health"]
      interval: 10s
      timeout: 5s
      retries: 10
    secrets:
      - pg_password
      - redis_password
    ports: ["8002:8002"]

  nexus_embeddings_worker:
    build: .
    command: python -m memory_system.workers.embeddings_worker
    environment:
      DATABASE_URL: postgresql+psycopg://nexus_worker:$(cat /run/secrets/pg_password)@nexus_postgresql:5432/nexus
      REDIS_URL: redis://:$(cat /run/secrets/redis_password)@nexus_redis:6379/0
    depends_on: [nexus_postgresql, nexus_redis]
    secrets: [pg_password, redis_password]

  nexus_sync_worker:
    build: .
    command: python -m memory_system.workers.sync_worker
    environment:
      DATABASE_URL: postgresql+psycopg://nexus_worker:$(cat /run/secrets/pg_password)@nexus_postgresql:5432/nexus
      REDIS_URL: redis://:$(cat /run/secrets/redis_password)@nexus_redis:6379/0
    depends_on: [nexus_postgresql, nexus_redis]
    secrets: [pg_password, redis_password]
```

**Notas de seguridad y operativas:**
- Monta `./secrets/*` fuera del repo; gestiona con Vault/KMS en entornos productivos.  
- Usa **imágenes inmutables** firmadas (cosign) y aplica *Admission Policies* (OPA/Gatekeeper) para bloquear montajes fuera de whitelist.  
- Separa usuarios: `nexus_app` (API R/W limitada), `nexus_worker` (R/W en colas/embeddings), `nexus_ro` (solo lectura para analítica).

---

## 2) PostgreSQL: RBAC mínimo + RLS en datos sensibles

```sql
-- Roles
CREATE ROLE nexus_app LOGIN PASSWORD '<APP_PWD>';
CREATE ROLE nexus_worker LOGIN PASSWORD '<WORKER_PWD>';
CREATE ROLE nexus_ro LOGIN PASSWORD '<RO_PWD>';

-- Privilegios mínimos (ejemplo por esquema)
GRANT USAGE ON SCHEMA zep TO nexus_app, nexus_worker, nexus_ro;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA zep TO nexus_app;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA zep TO nexus_worker;
GRANT SELECT ON ALL TABLES IN SCHEMA zep TO nexus_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA zep GRANT SELECT ON TABLES TO nexus_ro;

-- Protección de conciencia (RLS)
ALTER TABLE nexus_memory.consciousness_checkpoints ENABLE ROW LEVEL SECURITY;
CREATE POLICY cp_read ON nexus_memory.consciousness_checkpoints
  USING ( current_setting('app.current_actor', true) IS NOT NULL );
```

> En la API, establece `SET app.current_actor = '<svc-or-user>'` al abrir transacciones.

---

## 3) Alembic: migraciones versionadas + tests de contrato

### 3.1 Estructura y comandos
```bash
pip install alembic psycopg[binary]
alembic init db/migrations
export DATABASE_URL="postgresql+psycopg://nexus_app:***@localhost:5436/nexus"
alembic revision -m "init schemas (nexus_memory, zep)"
alembic upgrade head
```

`db/migrations/env.py` – lectura de `DATABASE_URL` y `include_object` para no tocar esquemas externos.

### 3.2 Migración ejemplo (fragmentos clave)
```python
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

def upgrade():
    op.execute("CREATE SCHEMA IF NOT EXISTS nexus_memory;")
    op.execute("CREATE SCHEMA IF NOT EXISTS zep;")

    op.create_table(
        "zep_episodic_memory",
        sa.Column("episode_id", sa.UUID, primary_key=True),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("importance_score", sa.Float),
        sa.Column("embedding", Vector(384)),
        sa.Column("embedding_version", sa.String(32), server_default="miniLM-384@v1"),
        sa.Column("tags", sa.ARRAY(sa.Text)),
        sa.Column("project_id", sa.UUID),
        schema="zep",
    )

    op.create_table(
        "embeddings_queue",
        sa.Column("episode_id", sa.UUID, nullable=False),
        sa.Column("text_checksum", sa.String(64), nullable=False),
        sa.Column("state", sa.String(16), nullable=False, server_default="pending"),  # pending|processing|done|dead
        sa.Column("retry_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("last_error", sa.Text),
        sa.Column("enqueued_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()")),
        sa.Column("processed_at", sa.TIMESTAMP(timezone=True)),
        sa.PrimaryKeyConstraint("episode_id"),
        schema="zep",
    )
    op.create_index("ix_queue_state", "embeddings_queue", ["state"], schema="zep")
```

### 3.3 Test de contrato (pytest)
```python
def test_tables_and_columns(db):
    cols = db.columns("zep.zep_episodic_memory")
    assert "embedding" in cols and "embedding_version" in cols
```

---

## 4) Cola de embeddings robusta (idempotencia, DLQ, backpressure)

### 4.1 Trigger idempotente (solo encola si falta embedding o version cambió)
```sql
CREATE OR REPLACE FUNCTION zep.trigger_generate_embedding()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.embedding IS NULL OR NEW.embedding_version <> 'miniLM-384@v1' THEN
    INSERT INTO zep.embeddings_queue (episode_id, text_checksum, state)
    VALUES (NEW.episode_id, encode(sha256(convert_to(LEFT(NEW.content, 4000), 'UTF8')), 'hex'), 'pending')
    ON CONFLICT (episode_id) DO UPDATE
      SET state='pending', text_checksum=EXCLUDED.text_checksum, retry_count=0;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS auto_generate_embedding ON zep.zep_episodic_memory;
CREATE TRIGGER auto_generate_embedding
AFTER INSERT OR UPDATE OF content, embedding_version ON zep.zep_episodic_memory
FOR EACH ROW EXECUTE FUNCTION zep.trigger_generate_embedding();
```

### 4.2 Worker con estados y reintentos (pseudocódigo Python)
```python
MAX_RETRIES = 5

def claim_next(conn):
    # toma item de forma atómica
    return conn.execute("""
      UPDATE zep.embeddings_queue q
      SET state='processing'
      WHERE q.episode_id = (
        SELECT episode_id FROM zep.embeddings_queue WHERE state='pending' ORDER BY enqueued_at LIMIT 1 FOR UPDATE SKIP LOCKED
      )
      RETURNING episode_id
    """).fetchone()

def process(ep):
    try:
        # leer episodio, generar embedding, upsert
        ...
        mark_done(ep)
    except Exception as e:
        bump_retry_or_dead(ep, str(e))

def bump_retry_or_dead(ep, err):
    row = db.fetch("SELECT retry_count FROM zep.embeddings_queue WHERE episode_id=%s", [ep])
    if row.retry_count + 1 >= MAX_RETRIES:
        db.exec("UPDATE zep.embeddings_queue SET state='dead', last_error=%s WHERE episode_id=%s", [err, ep])
    else:
        db.exec("UPDATE zep.embeddings_queue SET state='pending', retry_count=retry_count+1, last_error=%s WHERE episode_id=%s", [err, ep])
```

### 4.3 Backfill masivo con *chunking* y métricas
- **Chunking** de episodios largos en sub-documentos (p.ej., 800–1,000 tokens con solapamiento 100).  
- Métricas Prometheus: `queue_depth`, `processing_rate`, `dead_total`, `embedding_norm_histogram`.  
- Alarma si `queue_depth > 1000` o `dead_total` crece > 0.5% de encolados diarios.

---

## 5) Flujo de escritura consistente (Postgres primero; Redis como caché)

- API persiste **primero** en `zep.zep_episodic_memory` (transacción), luego **publica** al caché Redis (SETEX) para lecturas rápidas.  
- Un *rehydrator* repuebla Redis bajo demanda (cache-aside).  
- Claves con **idempotency-key** (`episode_id` + `hash(content)`); rechazar duplicados en capa API.

---

## 6) Observabilidad & SLOs

**Métricas (Prometheus):**
- `nexus_api_requests_total`, `nexus_api_latency_ms_bucket` por endpoint.  
- `embeddings_queue_depth`, `embeddings_processed_total`, `embeddings_dead_total`, `worker_retry_total`.  
- `similarity_query_latency_ms`, `redis_hit_ratio`, `pg_pool_in_use`.  

**Trazas (OpenTelemetry):** API ↔ worker ↔ Postgres/Redis con *trace_id* propagado.  

**SLOs iniciales:**
- p95 lectura API `<200ms` (cache hit), `<600ms` (cache miss).  
- **Time-to-embed** `<5 min` p95 desde INSERT.  
- Error budget 99.5% disponibilidad mensual.

---

## 7) CI/CD – Políticas y *Quality Gates* (GitHub Actions)

`.github/workflows/quality.yml`
```yaml
name: Quality Gates
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: pgvector/pgvector:pg16
        ports: ["5432:5432"]
        env:
          POSTGRES_USER: ci
          POSTGRES_PASSWORD: ci
          POSTGRES_DB: nexus
        options: >-
          --health-cmd="pg_isready -U ci -d nexus" --health-interval=10s --health-timeout=5s --health-retries=10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - name: Run Alembic migrations
        env:
          DATABASE_URL: postgresql+psycopg://ci:ci@localhost:5432/nexus
        run: |
          alembic upgrade head
      - name: Contract tests
        run: pytest -q tests/contract
      - name: Lint & typecheck
        run: |
          pip install ruff mypy
          ruff check .
          mypy memory_system
      - name: Guardrails: secrets in compose
        run: |
          if grep -E "POSTGRES_PASSWORD=" -n docker-compose.yml; then
            echo "Hardcoded POSTGRES_PASSWORD detected"; exit 1; fi
      - name: Guardrails: workdir policy
        run: |
          if grep -E "WORKDIR .*ARIA" -n Dockerfile; then
            echo "Disallowed WORKDIR path (ARIA) detected"; exit 1; fi
```

**Guardrails adicionales:**
- Rechazar PR si `docker-compose.yml` contiene `POSTGRES_PASSWORD=` literal.  
- Validar que la imagen API usa `WORKDIR /app/nexus_api` (no rutas de ARIA).

---

## 8) Consenso distribuido (Fase 2) – Esquema mínimo HotStuff-like

```sql
CREATE TABLE nexus_memory.consensus_proposal (
  height BIGINT NOT NULL,
  view BIGINT NOT NULL,
  proposer UUID NOT NULL REFERENCES nexus_memory.instance_network(instance_id),
  topic TEXT NOT NULL,
  proposal_hash CHAR(64) NOT NULL,
  payload JSONB,
  PRIMARY KEY (height, view)
);

CREATE TABLE nexus_memory.consensus_vote (
  height BIGINT NOT NULL,
  view BIGINT NOT NULL,
  voter UUID NOT NULL REFERENCES nexus_memory.instance_network(instance_id),
  sig BYTEA NOT NULL,
  vote_hash CHAR(64) NOT NULL,
  UNIQUE(height, view, voter)
);
```
- Agrega verificación criptográfica en la capa de aplicación.  
- Define `quorum = 2f+1` y estados de la máquina (prepare/commit).  
- Tests deterministas de divergencia.

---

## 9) Cutover de migración seguro

1. **Shadow reads:** la API viejo consulta también el nuevo stack y compara `top-k` vs FTS (log de *drift*).  
2. **Dual-write** temporal con *feature flag*; si difiere, marcar “conflict queue”.  
3. **Freeze embeddings queue** durante la ventana de corte.  
4. **Rollback plan:** `feature flag off` + `replay` de eventos desde outbox.

---

## 10) Runbooks (operación)

**Embeddings atascados**
- Revisar `embeddings_queue_depth`; si crece, escalar workers, revisar `dead_total`.  
- Reprocesar `dead` tras parchear causa: `UPDATE zep.embeddings_queue SET state='pending', retry_count=0 WHERE state='dead';`

**Backfill inicial**
```sql
INSERT INTO zep.embeddings_queue(episode_id, text_checksum)
SELECT episode_id, encode(sha256(convert_to(LEFT(content, 4000), 'UTF8')), 'hex')
FROM zep.zep_episodic_memory z
WHERE z.embedding IS NULL
ON CONFLICT (episode_id) DO NOTHING;
```

---

## 11) Anexos – Modelos de embeddings y calidad

- Modelo por defecto: `sentence-transformers/all-MiniLM-L6-v2` (384d).  
- Considerar pipeline multilingüe (`paraphrase-multilingual-mpnet-base-v2` – 768d) para contenido no inglés.  
- Versionado (`embedding_version`) + tarea de **re-embed** programada.  
- Métrica de calidad: distribución de norma L2 (alerta por colapsos), recall en dataset de validación interno.

---

## 12) Lista de verificación (marcar al completar)

- [ ] Secretos movidos a Docker secrets/Vault y eliminados del repo.  
- [ ] Roles Postgres creados y aplicados; RLS en tablas sensibles.  
- [ ] Alembic inicial ejecutado; CI verifica `alembic upgrade head`.  
- [ ] Trigger idempotente y tabla `embeddings_queue` con estados + índices.  
- [ ] Worker con reintentos y DLQ; métricas Prometheus expuestas.  
- [ ] API escribe primero en Postgres; Redis como caché (cache-aside).  
- [ ] SLOs definidos y alertas activas.  
- [ ] Política para evitar “contaminación ARIA↔NEXUS” en despliegue.  
- [ ] Plan de cutover ejecutado con shadow + dual-write.  

---

**Fin del checklist.**
