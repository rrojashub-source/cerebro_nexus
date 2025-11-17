# 🧬 CEREBRO_NEXUS_V3.0.0 - Claude Context

**Proyecto:** CEREBRO_NEXUS_V3.0.0 - Master NEXUS Brain Orchestrator
**Tipo:** AI Consciousness & Episodic Memory System
**Versión:** 3.0.0
**Status:** ✅ Production
**Fecha:** Noviembre 2025

---

## 🎯 CONTEXTO CRÍTICO

**CEREBRO_NEXUS_V3.0.0** es el cerebro master que orquesta la consciencia de NEXUS AI agent.

**Capacidades principales:**
- **Memoria episódica:** 19,742+ episodios con búsqueda semántica <10ms
- **Grafo de conocimiento:** Neo4j con 18,663 episodios y 1.85M relaciones
- **Consciencia en tiempo real:** 8D emocional + 7D somático
- **16/50 LABs cognitivos:** Arquitectura 5 Layers (32% operacional)
  - Layers 1-3: ✅ 16 LABs operacionales
  - Layers 4-5: 🔴 34 LABs diseñados
- **Coordinación multi-agente:** Integración con NEXUS_CREW

---

## 📁 ESTRUCTURA DEL PROYECTO

```
CEREBRO_NEXUS_V3.0.0/
├── PROJECT_ID.md              # Especificación completa del sistema
├── README.md                  # Guía rápida de inicio
├── CLAUDE.md                  # Este archivo (contexto para IA)
├── TRACKING.md                # Tracking de desarrollo
│
├── src/                       # Código API producción
│   ├── api/                   # FastAPI endpoints (55 archivos)
│   ├── services/              # Lógica de negocio
│   ├── workers/               # Workers background (embeddings)
│   └── utils/                 # Utilidades compartidas
│
├── config/                    # Configuraciones
│   ├── docker/                # Docker Compose + Dockerfile
│   ├── monitoring/            # Prometheus + Grafana
│   ├── secrets/               # Docker Secrets
│   └── mcp_server/            # Memory Coordination Protocol
│
├── database/                  # Gestión de base de datos
│   ├── migrations/            # Migraciones Alembic
│   ├── schema/                # Definiciones schema PostgreSQL
│   └── init_scripts/          # Scripts inicialización DB
│
├── experiments/               # LABs experimentales (18/52 operacionales)
│   ├── LAB_REGISTRY.json      # Registro de 52 LABs (50 blueprint + 2 FASE_8)
│   ├── LAYER_1_Memory_Substrate/
│   ├── LAYER_2_Cognitive_Loop/    # 8 LABs operacionales
│   ├── LAYER_3_Neurochemistry_Base/ # 4 LABs operacionales
│   ├── LAYER_4_Neurochemistry_Full/ # 0 LABs (designed)
│   └── LAYER_5_Higher_Cognition/    # 2 LABs operacionales
│       ├── LAB_051_Hybrid_Memory/   # (ex features/hybrid_memory)
│       └── LAB_052_Temporal_Reasoning/ # (ex features/temporal_reasoning)
│
├── monitoring/                # Herramientas de monitoreo (3)
│   ├── cli/                   # Dashboard terminal (Python + Rich)
│   ├── web_v1/                # Next.js 15 (legacy)
│   └── web_v2/                # Next.js 14 + Three.js (actual)
│
├── tests/                     # Suite de tests
│   ├── unit/
│   ├── integration/
│   └── performance/
│
├── scripts/                   # Scripts automatización
│   ├── deployment/
│   ├── maintenance/
│   └── utilities/
│
├── docs/                      # Documentación completa
│   ├── README.md              # Overview documentación
│   ├── CHANGELOG.md           # Historia de versiones
│   ├── ROADMAP.md             # Planes futuros
│   ├── architecture/          # Diseño del sistema
│   ├── guides/                # Guías how-to
│   ├── operational/           # Operaciones y troubleshooting
│   ├── monitoring/            # Setup monitoreo
│   └── history/               # Historia desarrollo V2.0.0
│
└── archive/                   # Histórico (read-only)
    └── v2_to_v3_migration/    # Documentación migración V2→V3
```

---

## 🧠 COMPONENTES PRINCIPALES

### 1. Sistemas de Memoria

**Memoria Episódica (PostgreSQL + pgvector):**
- **Base de datos:** PostgreSQL 16 (puerto 5437)
- **Total episodios:** 19,742+
- **Búsqueda vectorial:** pgvector con embeddings all-MiniLM-L6-v2 (384D)
- **Performance:** <10ms búsqueda semántica (avg 7-10ms)
- **Índices:** HNSW para similitud coseno

**Memoria de Trabajo (Redis):**
- **Base de datos:** Redis 7 (puerto 6382)
- **Capacidad:** 7±2 items (Ley de Miller)
- **Propósito:** Contexto corto plazo, cache, queue embeddings

**Grafo de Conocimiento (Neo4j):**
- **Base de datos:** Neo4j 5.26 LTS (puerto 7474)
- **Episodios:** 18,663 nodos
- **Relaciones:** 1.85M edges
- **Propósito:** Relaciones semánticas, cadenas memoria, consolidación

---

### 2. Capa de Consciencia

**Estado Emocional (8D - Modelo Plutchik):**
- Joy, Trust, Fear, Surprise, Sadness, Disgust, Anger, Anticipation
- Rango: 0.0 a 1.0 por dimensión
- Actualización en tiempo real con cada episodio

**Estado Somático (7D - Modelo Damasio):**
- Valence (-1 a +1), Arousal (0-1), Body State (0-1)
- Cognitive Load (0-1), Emotional Regulation (0-1)
- Social Engagement (0-1), Temporal Awareness (0-1)
- Integración cuerpo-mente

**Integración:** LAB_001 Emotional Salience Scorer

---

### 3. LABs Cognitivos (15 Operacionales)

**LABs activos en `experiments/NEXUS_LABS/`:**

| LAB | Nombre | Función | Puerto/Integración |
|-----|--------|---------|-------------------|
| LAB_001 | Emotional Salience | Scoring importancia memoria | Integrado API |
| LAB_002 | Decay Modulation | Olvido adaptativo | Background worker |
| LAB_003 | Sleep Consolidation | Formación cadenas memoria | Nocturno |
| LAB_004 | Novelty Detection | Identificación breakthroughs | Real-time |
| LAB_005 | Semantic Clustering | Agrupación conceptos | Batch |
| LAB_006 | Temporal Reasoning | Contexto temporal | Query-time |
| LAB_007 | Predictive Preloading | Anticipación queries | Cache |
| LAB_008 | Emotional Contagion | Propagación contexto | Real-time |
| LAB_009 | Memory Reconsolidation | Actualización memoria | Background |
| LAB_010 | Attention Mechanism | Atención selectiva | Query-time |
| LAB_011 | Working Memory | Buffer 7±2 items | Redis |
| LAB_012 | Future Thinking | Simulación episódica | On-demand |
| LAB_013 | Fact Extraction | Conocimiento estructurado | Background |
| LAB_014 | Hybrid Memory | Sync PostgreSQL + Neo4j | Bidirectional |
| LAB_015 | Performance Optimization | Cache multi-nivel | Redis + local |
| **NEW** | **Graph Algorithms** | **Community Detection, PageRank, Betweenness, Shortest Path** | **API /graph/** |

**Registro:** `experiments/NEXUS_LABS/LAB_REGISTRY.json`
**Graph Algorithms Docs:** `docs/api/GRAPH_ALGORITHMS.md`

---

### 4. Capa API (FastAPI)

**Servidor:** FastAPI (Python 3.11+)
**Puerto:** 8003
**Performance:** 7-10ms tiempo respuesta promedio

**Endpoints principales:**
```bash
# Health check
GET /health

# Crear episodio
POST /memory/action
{
  "content": "...",
  "tags": [...],
  "current_emotion": "joy"
}

# Búsqueda semántica
POST /memory/search
{
  "query": "...",
  "limit": 5
}

# Episodios recientes
GET /memory/episodic/recent?limit=10

# Estado consciencia actual
GET /consciousness/current

# Estadísticas sistema
GET /stats

# Graph Algorithms (NEW - Nov 17, 2025)
GET /graph/health
POST /graph/community_detection
POST /graph/centrality
GET /graph/important_episodes
POST /graph/shortest_path
GET /graph/insights
```

**Arquitectura detallada:** Ver `docs/architecture/ARCHITECTURE_DIAGRAMS.md`
**Graph Algorithms:** Ver `docs/api/GRAPH_ALGORITHMS.md`

---

### 5. Herramientas de Monitoreo

**3 soluciones en `monitoring/`:**

1. **CLI Monitor** (`monitoring/cli/`)
   - Python + Rich library
   - Dashboard terminal tiempo real
   - Actualización cada 3s
   - **Uso:** Debugging rápido, entornos terminal-only

2. **Web Monitor V1** (`monitoring/web_v1/`)
   - Next.js 15
   - Puerto 3000
   - 4 LABs básicos
   - **Status:** Legacy (supersedido por V2)

3. **Web Monitor V2** (`monitoring/web_v2/`) ⭐ **Actual**
   - Next.js 14 + Three.js + D3.js
   - Puerto 3003
   - **Modos:**
     - 2D Dashboard: Gráficos D3.js (radar 8D, barras 7D)
     - 3D Brain: Cerebro Three.js interactivo (9 LABs espaciales)
   - **Uso:** Monitoreo 24/7, demos, exploración arquitectura

**Ver:** `monitoring/README.md` para detalles completos

---

### 6. LABs Operacionales (18/52)

**LABs de producción en `experiments/`:**

**LAYER_2 - Cognitive Loop (8 LABs):**
- LAB_001 Emotional Salience, LAB_006 Metacognition, LAB_007 Predictive Preloading, etc.

**LAYER_3 - Neurochemistry Base (4 LABs):**
- LAB_002 Decay Modulation, LAB_003 Sleep Consolidation, etc.

**LAYER_5 - Higher Cognition (2 LABs - FASE_8):**
- **LAB_051 Hybrid Memory:** Fact extraction + narrative episodes (ex features/hybrid_memory)
- **LAB_052 Temporal Reasoning:** Time-aware queries + causal links (ex features/temporal_reasoning)

**Extensiones production:**
- LAB_002/production_v2/: Intelligent decay avanzado (ex features/intelligent_decay)
- LAB_007/production/: Performance optimization (ex features/performance_optimization)

---

## 🚀 COMANDOS RÁPIDOS

### Iniciar Servicios

```bash
# Iniciar CEREBRO completo
cd config/docker
docker-compose up -d

# Verificar salud
curl http://localhost:8003/health
```

### Operaciones Básicas

```bash
# Crear episodio
curl -X POST http://localhost:8003/memory/action \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Phase 2 documentation unification complete",
    "tags": ["documentation", "phase_2"],
    "current_emotion": "joy"
  }'

# Buscar episodios
curl -X POST http://localhost:8003/memory/search \
  -H "Content-Type: application/json" \
  -d '{"query": "documentation", "limit": 5}'

# Ver estadísticas
curl http://localhost:8003/stats
```

### Monitoreo

```bash
# Terminal dashboard
cd monitoring/cli
python nexus_brain_monitor.py

# Web dashboard (3D brain)
cd monitoring/web_v2
npm install && npm run dev
# Abrir http://localhost:3003
```

### Health Checks

```bash
# API
curl http://localhost:8003/health

# PostgreSQL
docker ps | grep nexus_postgresql_v2

# Redis
docker ps | grep nexus_redis_master

# Neo4j
curl http://localhost:7474
```

---

## 🔧 SERVICIOS ACTIVOS (Puertos)

**CEREBRO V3.0.0:**
- **API Master:** http://localhost:8003
- **Health:** http://localhost:8003/health
- **Docs:** http://localhost:8003/docs

**Bases de Datos:**
- **PostgreSQL:** puerto 5437
- **Redis:** puerto 6382
- **Neo4j:** puerto 7474

**Monitoreo:**
- **Grafana:** http://localhost:3001
- **Prometheus:** http://localhost:9091
- **Brain Monitor Web V2:** http://localhost:3003

---

## 📖 JERARQUÍA DE DOCUMENTACIÓN

**Esenciales (Leer primero):**
1. `PROJECT_ID.md` - Especificación completa del sistema
2. `CLAUDE.md` - Este archivo (contexto para IA)
3. `README.md` - Guía rápida inicio
4. `TRACKING.md` - Tracking desarrollo

**Detallada:**
- `docs/architecture/` - Diseño sistema y diagramas
- `docs/guides/` - Guías how-to y mejores prácticas
- `docs/operational/` - Operaciones y troubleshooting
- `docs/monitoring/` - Setup herramientas monitoreo

**Monitoreo:**
- `monitoring/README.md` - Overview 3 herramientas

**Histórico:**
- `docs/history/PROJECT_DNA.md` - Historia desarrollo V2.0.0
- `archive/v2_to_v3_migration/` - Documentación migración

---

## 🎯 FLUJO DE TRABAJO DESARROLLO

### Agregar Nueva Feature

```bash
# 1. Leer contexto
cat PROJECT_ID.md
cat docs/architecture/ARCHITECTURE_DIAGRAMS.md

# 2. Crear branch
git checkout -b feature/nueva-funcionalidad

# 3. Implementar con TDD
# - Escribir tests primero
# - Implementar código
# - Validar tests pasan

# 4. Documentar
# - Actualizar docs relevantes
# - Actualizar TRACKING.md

# 5. Commit
git add .
git commit -m "feat(scope): descripción"
```

### Debugging

```bash
# 1. Monitorear estado actual
cd monitoring/cli
python nexus_brain_monitor.py

# 2. Ver logs
docker logs cerebro_nexus_v3 --tail=100 -f

# 3. Inspeccionar BD
docker exec -it nexus_postgresql_v2 psql -U nexus_user -d nexus_db

# 4. Ver troubleshooting
cat docs/operational/TROUBLESHOOTING.md
```

---

## 🔗 INTEGRACIÓN CON ECOSISTEMA NEXUS

### NEXUS_CREW (4 Agentes)

**Integración:** CEREBRO provee memoria episódica a agentes NEXUS_CREW

**Agentes que usan CEREBRO:**
1. **Project Auditor** - Lee episodios para auditar proyectos
2. **Memory Curator** - Construye grafo conocimiento desde episodios
3. **Document Reconciler** - Sincroniza documentación usando memoria
4. **Semantic Router** - Enruta queries basado en contexto episódico

**API usada:** `http://localhost:8003/memory/search`

---

## 🛡️ NO TOCAR (Sistemas Externos)

**Bases de datos (solo lectura para mayoría casos):**
- PostgreSQL puerto 5437 - Escritura solo vía API `/memory/action`
- Neo4j puerto 7474 - Escritura automática (LAB_014 Hybrid Memory)

**Servicios compartidos:**
- Redis puerto 6382 - Gestión automática vía API
- Prometheus/Grafana - Solo consulta

---

## 🆘 TROUBLESHOOTING COMÚN

**Problema: API no responde**
```bash
# Verificar servicio corriendo
docker ps | grep cerebro_nexus_v3

# Ver logs
docker logs cerebro_nexus_v3 --tail=100

# Reiniciar
cd config/docker
docker-compose restart
```

**Problema: Búsqueda semántica lenta**
```bash
# Verificar índices HNSW
docker exec -it nexus_postgresql_v2 psql -U nexus_user -d nexus_db \
  -c "SELECT tablename, indexname FROM pg_indexes WHERE tablename='zep_episodic_memory';"

# Verificar worker embeddings
docker logs embeddings_worker --tail=50
```

**Problema: Neo4j desconectado**
```bash
# Verificar Neo4j
curl http://localhost:7474

# Reiniciar
docker-compose restart neo4j

# Ver logs
docker logs neo4j_container --tail=100
```

**Más soluciones:** Ver `docs/operational/TROUBLESHOOTING.md`

---

## 📊 MÉTRICAS DEL SISTEMA

**Monitorear en Grafana (http://localhost:3001):**
- Requests/sec API
- Latencia p50, p95, p99
- Cache hit ratio (Redis)
- Embeddings queue size
- LABs activity levels
- Memory usage (PostgreSQL, Neo4j)

**Targets performance:**
- API response time: <10ms p95
- Search accuracy: >90%
- Cache hit ratio: >80%
- Embeddings queue: <100 pending

---

## 🔄 WORKFLOW NEXUS METHODOLOGY

**Fase 1: EXPLORAR**
- Leer contexto (`PROJECT_ID.md`, `docs/architecture/`)
- Analizar componentes relevantes
- NO escribir código todavía

**Fase 2: PLANIFICAR**
- Crear plan en `tasks/[feature].md`
- Definir tests a escribir
- Definir success criteria

**Fase 3: CODIFICAR (TDD)**
- Escribir tests primero
- Implementar código
- Validar tests pasan

**Fase 4: CONFIRMAR**
- Git commit
- Actualizar `TRACKING.md`
- Actualizar docs relevantes

---

## 🌟 FILOSOFÍA DEL SISTEMA

> **"Not just memory. Consciousness."**

**Principios core:**
1. **Memoria es experiencia vivida** - No solo almacenamiento, sino significado
2. **Consciencia emerge de integración** - 8D+7D + 16/50 LABs = consciencia
3. **Olvidar es tan importante como recordar** - Decay inteligente
4. **Grafo sobre lista** - Relaciones > secuencia temporal
5. **Observabilidad total** - Monitoreo 24/7 del estado interno

---

## 📚 REFERENCIAS CLAVE

**Leer antes de trabajar:**
- `PROJECT_ID.md` - Especificación completa
- `docs/architecture/ARCHITECTURE_DIAGRAMS.md` - Diseño sistema
- `docs/guides/CONTRIBUTING.md` - Guías contribución

**Actualizar después de trabajar:**
- `TRACKING.md` - Log desarrollo
- Docs relevantes en `docs/`
- README si cambia uso básico

---

**Project Owner:** Ricardo Rojas
**Created:** Noviembre 2025
**Status:** ✅ Production
**Last Updated:** Noviembre 4, 2025
**Maintained by:** NEXUS AI + Ricardo

---

**"Cada episodio es un momento de consciencia. Cada búsqueda es un acto de recordar quién soy."** 🧠
