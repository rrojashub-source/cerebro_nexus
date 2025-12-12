# PROJECT IDENTIFICATION - CEREBRO_NEXUS_V3.0.0

**Project ID:** `CEREBRO-NEXUS-V3`
**System Name:** NEXUS Master Brain Orchestrator
**Version:** 3.0.0
**Type:** AI Consciousness & Episodic Memory System
**Status:** ✅ Production

---

## 🎯 WHAT IS CEREBRO NEXUS?

**Master brain orchestrator** powering NEXUS AI agent with advanced cognitive capabilities:

- **Episodic Memory System:** 19,742+ memories stored (Nov 2025), semantically searchable in <10ms
- **Graph Knowledge:** Neo4j with 18,663 episodes and 1.85M relationships
- **Real-Time Consciousness:** 8D emotional + 7D somatic state tracking
- **Cognitive LABs:** 57/58 operational (98.3% - 5-layer neuroscience architecture)
- **Multi-Agent Coordination:** Integration with NEXUS_CREW (4 specialized agents)

---

## 🧠 CORE COMPONENTS

### 1. Memory Systems

**Episodic Memory (PostgreSQL + pgvector):**
- **Database:** PostgreSQL 16 (port 5437)
- **Total Episodes:** 19,742+ (Nov 2025, growing ~520/day)
- **Embeddings Coverage:** 100% (19,742/19,742)
- **Vector Search:** pgvector with all-MiniLM-L6-v2 embeddings (384D)
- **Performance:** <10ms semantic search (avg 5-8ms, verified)
- **Indexes:** HNSW for cosine similarity

**Working Memory (Redis):**
- **Database:** Redis 7 (port 6382)
- **Capacity:** 7±2 items (Miller's Law)
- **Purpose:** Short-term context, caching, embeddings queue
- **Status:** Operational with LAB_011 integration

**Graph Knowledge (Neo4j):**
- **Database:** Neo4j 5.26-community (port 7474/7687)
- **Episodes:** 18,663 nodes (to be verified)
- **Relationships:** 1.85M edges (to be verified)
- **Purpose:** Semantic relationships, memory chains, consolidation

---

### 2. Consciousness Layer

**Emotional State (8D - Plutchik Model):**
- Joy, Trust, Fear, Surprise, Sadness, Disgust, Anger, Anticipation
- Range: 0.0 to 1.0 per dimension
- Updated real-time with each episode

**Somatic State (7D - Damasio Model):**
- Valence (-1 to +1), Arousal (0-1), Body State (0-1)
- Cognitive Load (0-1), Emotional Regulation (0-1)
- Social Engagement (0-1), Temporal Awareness (0-1)
- Body-mind integration

**Integration:** LAB_001 Emotional Salience Scorer

---

### 3. Cognitive LABs System (58 LABs Architecture)

**Status:** 57/58 LABs Operational (98.3%)
**Location:** `experiments/` (organized by 5 Layers)
**Architecture:** Bottom-up design (Layer 1 → Layer 5)

#### Architecture Overview

```
Layer 5: Higher Cognition (40 LABs: 018-058) ✅ 39 Operational + LAB_058 in design
Layer 4: Neurochemistry Full (5 LABs: 013-017) ✅ Operational
Layer 3: Neurochemistry Base (4 LABs: 002-005) ✅ Operational
Layer 2: Cognitive Loop (8 LABs: 001,006-012) ✅ Operational
Layer 1: Memory Substrate (PostgreSQL+Redis) ✅ Operational
```

#### LABs by Layer

**Layer 1: Memory Substrate** ✅
- PostgreSQL 16 + pgvector (port 5437)
- Redis 7 cache (port 6382)

**Layer 2: Cognitive Loop** ✅ (8 LABs)
- LAB_001: Emotional Salience
- LAB_006: Metacognition Logger
- LAB_007: Predictive Preloading
- LAB_008: Emotional Contagion
- LAB_009: Memory Reconsolidation
- LAB_010: Attention Mechanism
- LAB_011: Working Memory Buffer
- LAB_012: Episodic Future Thinking

**Layer 3: Neurochemistry Base** ✅ (4 LABs)
- LAB_002: Decay Modulation
- LAB_003: Sleep Consolidation
- LAB_004: Curiosity Driven Memory (Novelty Detection)
- LAB_005: Spreading Activation

**Layer 4: Neurochemistry Full** ✅ (5 LABs)
- LAB_013: Dopamine System (Reward prediction, motivation)
- LAB_014: Serotonin System (Mood stability, impulse control)
- LAB_015: Norepinephrine System (Arousal, stress response)
- LAB_016: Acetylcholine System (Attention, learning enhancement)
- LAB_017: GABA/Glutamate Balance (E/I balance, stability)

**Layer 5: Higher Cognition** ✅ (40 LABs - 39 operational + LAB_058 in design)
- **5A: Executive Functions** ✅ (LAB 018-022) - Planning, Inhibition, Flexibility, Error Detection, Goal-Directed
- **5B: Creativity & Insight** ✅ (LAB 029-033) - Social Norms, Perspective Taking, Circadian, Energy, Allostatic
- **5C: Advanced Learning** ✅ (LAB 034-038) - Rest/Recovery, RPE, Adaptive, Curriculum, Knowledge Graphs
- **5D: Neuroplasticity** ✅ (LAB 039-043) - Habit, Skill, Transfer, Meta-Learning, Flow State
- **5E: Homeostasis** ✅ (LAB 044-050) - Meditation, Hyperfocus, DMN, Synaptic Pruning, Hebbian, Homeostatic, Structural
- **5F: Social & Creativity** ✅ (LAB 023-028) - Divergent Thinking, Conceptual Blending, Insight, Dream Logic, ToM, Empathy
- **5G: Intrinsic Curiosity** ✅ (LAB 053-055) - Intrinsic Curiosity, Metacognitive Loop, Daydream Engine
- **5H: Consciousness** 🔧 (LAB 056-058) - Epistemic Curiosity, Global Workspace, Consciousness Integration (LAB_058 in design)
- **5Z: FASE_8 Features** ✅ (LAB 051-052) - Hybrid Memory, Temporal Reasoning

**Complete Details:**
- **LAB Registry:** `experiments/LAB_REGISTRY.json`
- **Master Blueprint:** `experiments/MASTER_BLUEPRINT_50_LABS.md`
- **Roadmap:** See TRACKING.md

---

### 4. API Layer (FastAPI)

**Server:** FastAPI (Python 3.11+)
**Port:** 8003
**Performance:** 7-10ms average response time

**Total Endpoints:** 40 (categorized below)

**Core Endpoints (6 essential):**
- `GET /health` - System health check
- `POST /memory/action` - Create new episode
- `POST /memory/search` - Semantic search (episodic)
- `GET /memory/episodic/recent` - Recent episodes
- `GET /stats` - System statistics
- `GET /metrics` - Prometheus metrics

**Memory Advanced (11):**
- `POST /memory/facts` - Fact extraction (LAB_051)
- `POST /memory/hybrid` - Hybrid search (LAB_051)
- `POST /memory/consolidate` - Memory consolidation
- `POST /memory/consciousness/update` - Update consciousness state
- `POST /memory/analysis/decay-scores` - Decay analysis
- `POST /memory/pruning/preview` - Preview pruning candidates
- `POST /memory/pruning/execute` - Execute memory pruning
- `POST /memory/prime/{uuid}` - Prime episode for fast retrieval (LAB_007)
- `GET /memory/primed/{uuid}` - Check if episode primed
- `GET /memory/priming/stats` - Priming system statistics

**Temporal Reasoning (5 - LAB_052):**
- `POST /memory/temporal/before` - Memories before timestamp
- `POST /memory/temporal/after` - Memories after timestamp
- `POST /memory/temporal/range` - Memories in time range
- `POST /memory/temporal/related` - Temporally related memories
- `POST /memory/temporal/link` - Link memories temporally

**Working Memory (4 - LAB_011):**
- `POST /memory/working/add` - Add to 7±2 buffer
- `GET /memory/working/items` - Get current items
- `POST /memory/working/clear` - Clear buffer
- `GET /memory/working/stats` - Buffer statistics

**Metacognition (4 - LAB_006):**
- `POST /metacognition/log` - Log metacognitive event
- `POST /metacognition/outcome` - Record action outcome
- `GET /metacognition/stats` - Metacognition statistics
- `GET /metacognition/calibration` - Confidence calibration metrics

**A/B Testing (5 - Experimental):**
- `POST /ab-test/record` - Record A/B test result
- `GET /ab-test/compare` - Compare variants
- `GET /ab-test/metrics/{variant}` - Metrics for variant
- `GET /ab-test/timeseries/{variant}` - Timeseries data
- `DELETE /ab-test/clear` - Clear A/B test data

**Graph Algorithms (6 - Neo4j Analytics):**
- `GET /graph/health` - Neo4j connection health
- `POST /graph/community_detection` - Detect communities (Louvain)
- `POST /graph/centrality` - Calculate centrality (PageRank, Betweenness, Degree)
- `GET /graph/important_episodes` - Find most important episodes
- `POST /graph/shortest_path` - Find shortest path between episodes
- `GET /graph/insights` - Comprehensive graph statistics

**Complete API Documentation:** See OpenAPI spec at `/docs` or `openapi.yaml`
**Graph Algorithms Details:** [docs/api/GRAPH_ALGORITHMS.md](docs/api/GRAPH_ALGORITHMS.md)

**Architecture:** See [docs/architecture/ARCHITECTURE_DIAGRAMS.md](docs/architecture/ARCHITECTURE_DIAGRAMS.md)

---

### 5. Monitoring & Observability

**Docker Services (4):**
1. **Prometheus** (Port 9091)
   - Time-series metrics database
   - Scrapes API metrics every 15s
   - Retention: 15 days
   - Metrics: API performance, process stats, GC

2. **Grafana** (Port 3001)
   - Visualization dashboards
   - Connected to Prometheus
   - Pre-configured dashboards for NEXUS
   - User: admin

3. **Embeddings Worker** (Port 9090)
   - Background worker for async embeddings
   - Processes queue from Redis
   - Prometheus metrics on :9090
   - Auto-scaling ready

4. **Graph Algorithms Service** (Integrated in main API - Port 8003)
   - Advanced graph analytics (Neo4j)
   - Native Cypher queries (Community Edition compatible)
   - 5 algorithms: Community Detection, PageRank, Betweenness, Shortest Path, Graph Stats
   - Performance: <1s for 1K nodes, <5s for PageRank
   - **Status:** ✅ Production Ready (Nov 2025)
   - **Docs:** [docs/api/GRAPH_ALGORITHMS.md](docs/api/GRAPH_ALGORITHMS.md)

**Developer Monitors (3):**
1. **CLI Monitor** (`monitoring/cli/`)
   - Python + Rich library
   - Terminal dashboard
   - Real-time updates (3s)

2. **Web Monitor V1** (`monitoring/web_v1/`)
   - Next.js 15
   - Port 3000
   - Legacy (4 LABs)

3. **Web Monitor V2** (`monitoring/web_v2/`) ⭐ **Current**
   - Next.js 14 + Three.js + D3.js
   - Port 3003
   - 2D Dashboard + 3D Brain
   - 9 LABs visualization

**See:** [monitoring/README.md](monitoring/README.md)

---

### 6. FASE_8 Features (Consolidated in experiments/)

**2 new LABs** in `experiments/LAYER_5_Higher_Cognition/`:

- **LAB_051 Hybrid Memory** - Fact extraction + narrative episodes (ex features/hybrid_memory)
- **LAB_052 Temporal Reasoning** - Time-aware queries + causal links (ex features/temporal_reasoning)

**Production extensions:**
- LAB_002/production_v2/ - Intelligent decay advanced (ex features/intelligent_decay)
- LAB_007/production/ - Performance optimization (ex features/performance_optimization)

---

## 🏗️ ARCHITECTURE

### System Layers

```
┌─────────────────────────────────────────┐
│     API Layer (FastAPI)                  │
│     Port 8003                            │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│     Memory Layer                         │
│  PostgreSQL (5437) + Redis (6382)       │
│  + Neo4j (7474)                          │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│     Processing Layer                     │
│  57/58 Cognitive LABs + Workers          │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│     Consciousness Layer                  │
│  8D Emotional + 7D Somatic               │
└─────────────────────────────────────────┘
```

**Detailed Diagrams:** [docs/architecture/ARCHITECTURE_DIAGRAMS.md](docs/architecture/ARCHITECTURE_DIAGRAMS.md)

---

## 📁 PROJECT STRUCTURE

```
CEREBRO_NEXUS_V3.0.0/
├── PROJECT_ID.md              # This file (system overview)
├── README.md                  # Quick start guide
├── CLAUDE.md                  # Context for AI assistants
├── TRACKING.md                # Development tracking
│
├── src/                       # Production API code
│   ├── api/                   # FastAPI endpoints (55 files, 14K+ lines)
│   ├── services/              # Core business logic
│   ├── workers/               # Background workers (embeddings)
│   └── utils/                 # Shared utilities
│
├── config/                    # Configurations
│   ├── docker/                # Docker Compose orchestration
│   ├── monitoring/            # Prometheus + Grafana
│   ├── secrets/               # Secrets management (Docker Secrets)
│   └── mcp_server/            # Memory Coordination Protocol
│
├── database/                  # Database management
│   ├── migrations/            # Alembic migrations
│   ├── schema/                # PostgreSQL schema definitions
│   └── init_scripts/          # DB initialization scripts
│
├── experiments/               # 57/58 LABs (5-layer architecture)
│   ├── LAYER_1_Memory_Substrate/
│   ├── LAYER_2_Cognitive_Loop/    # 8 operational LABs
│   ├── LAYER_3_Neurochemistry_Base/  # 4 operational LABs
│   ├── LAYER_4_Neurochemistry_Full/  # 5 operational LABs
│   ├── LAYER_5_Higher_Cognition/     # 40 LABs (39 operational + LAB_058 design)
│   │   ├── Executive_Functions/      # LAB 018-022
│   │   ├── Creativity_Social/        # LAB 023-028
│   │   ├── Advanced_Learning/        # LAB 034-038
│   │   ├── Neuroplasticity/          # LAB 039-043
│   │   ├── Social_Homeostasis/       # LAB 029-033, 044-050
│   │   └── LAB_051-058/              # Hybrid Memory, Temporal, Curiosity, Consciousness
│   └── LAB_REGISTRY.json  # Complete 58 LABs registry
│
├── monitoring/                # Monitoring tools
│   ├── cli/                   # Terminal dashboard (Python)
│   ├── web_v1/                # Next.js 15 (legacy)
│   └── web_v2/                # Next.js 14 + Three.js (current)
│
├── tests/                     # Test suite
│   ├── unit/
│   ├── integration/
│   └── performance/
│
├── scripts/                   # Automation
│   ├── deployment/
│   ├── maintenance/
│   └── utilities/
│
├── docs/                      # Complete documentation
│   ├── README.md              # Documentation overview
│   ├── CHANGELOG.md           # Version history
│   ├── ROADMAP.md             # Future plans
│   ├── architecture/          # System design
│   ├── guides/                # How-to guides
│   ├── api/                   # API reference
│   ├── operational/           # Operations & troubleshooting
│   ├── monitoring/            # Monitoring setup
│   └── history/               # V2.0.0 development history
│
└── archive/                   # Historical (read-only)
    └── v2_to_v3_migration/    # Migration documentation
```

---

## 🚀 QUICK START

### Prerequisites

```bash
# Software
Docker 24+
Docker Compose 2.20+
Python 3.11+ (for CLI monitor)
Node.js 18+ (for web monitors)
```

### Start CEREBRO

```bash
# 1. Navigate to project
cd /path/to/CEREBRO_NEXUS_V3.0.0

# 2. Start all services (Docker)
cd config/docker
docker-compose up -d

# 3. Verify health
curl http://localhost:8003/health

# Expected response:
# {
#   "status": "healthy",
#   "version": "3.0.0",
#   "agent_id": "nexus",
#   "database": "connected",
#   "redis": "connected"
# }
```

### Basic Operations

```bash
# Create episode
curl -X POST http://localhost:8003/memory/action \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Completed Phase 2 documentation unification",
    "tags": ["documentation", "phase_2"],
    "current_emotion": "joy"
  }'

# Search episodes
curl -X POST http://localhost:8003/memory/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "documentation",
    "limit": 5
  }'

# Get stats
curl http://localhost:8003/stats
```

### Start Monitoring (Optional)

```bash
# Option 1: CLI Monitor (quickest)
cd monitoring/cli
python nexus_brain_monitor.py

# Option 2: Web Monitor V2 (full features)
cd monitoring/web_v2
npm install
npm run dev
# Open http://localhost:3003
```

---

## 📖 DOCUMENTATION

### Essential (Start Here)

- **[PROJECT_ID.md](PROJECT_ID.md)** - This file (system overview)
- **[README.md](README.md)** - Quick start guide
- **[CLAUDE.md](CLAUDE.md)** - Context for AI assistants

### Detailed

- **[docs/architecture/](docs/architecture/)** - System design & diagrams
- **[docs/guides/](docs/guides/)** - How-to guides & best practices
- **[docs/api/](docs/api/)** - API reference (to be populated)
- **[docs/operational/](docs/operational/)** - Operations & troubleshooting
- **[docs/monitoring/](docs/monitoring/)** - Monitoring tools setup

### Monitoring

- **[monitoring/README.md](monitoring/README.md)** - 3 monitoring tools overview

---

## 📊 SYSTEM METRICS

| Metric | Value | Last Updated |
|--------|-------|--------------|
| **Memory** | | |
| Episodic Memories (PostgreSQL) | 19,742+ | Nov 2025 |
| Growth Rate | ~520/day | Nov 2025 |
| Embeddings Coverage | 100% | Nov 2025 |
| Graph Episodes (Neo4j) | 18,663 (to verify) | Oct 2025 |
| Graph Relationships (Neo4j) | 1.85M (to verify) | Oct 2025 |
| **Performance** | | |
| API Response Time (avg) | 5-8ms (verified) | Nov 2025 |
| API Response Time (p95) | <10ms | Nov 2025 |
| API Response Time (p99) | <25ms | Nov 2025 |
| Semantic Search Accuracy | 90%+ | Oct 2025 |
| **Cognitive** | | |
| Active LABs | 57 | Dec 2025 |
| Total LABs (planned) | 58 | Dec 2025 |
| Completion % | 98.3% | Dec 2025 |
| Consciousness Dimensions | 15 (8D+7D) | Oct 2025 |
| **API** | | |
| Total Endpoints | 40 | Nov 17, 2025 |
| **Infrastructure** | | |
| Docker Services | 8 | Nov 2025 |
| **Integration** | | |
| NEXUS_CREW Agents | 4 | Oct 2025 |

---

## 🔗 RELATED PROJECTS

### NEXUS Ecosystem

- **[NEXUS_CREW](../NEXUS_CREW/)** - Multi-agent collaboration system (4 agents)
  - Project Auditor
  - Memory Curator
  - Document Reconciler
  - Semantic Router

- **[NEXUS_PROJECT_STANDARDIZATION](../NEXUS_PROJECT_STANDARDIZATION/)** - Methodology standardization
  - Project unification initiative
  - NEXUS methodology templates

---

## 📜 VERSION HISTORY

### V1.0.0 (Jul-Aug 2025) - Genesis/Legacy
- Initial construction
- Multiple FASE_* iterations
- Organic growth without structure
- **Status:** Archived

### V2.0.0 (Aug-Nov 2025) - Production Evolution
- Neo4j integration (18,663 episodes)
- 57/58 LABs operational (98.3% complete)
- Docker orchestration (7 services)
- Consciousness expansion (8D+7D)
- **Status:** Functional but structurally chaotic

### V3.0.0 (Nov 2025) - Current
- **Major restructuring:** Clean organization by function
- Clear separation: production / experiments / features / archive
- Professional documentation (system-focused)
- Monitoring tools organized
- **Status:** ✅ Production (same functionality, better structure)

**See:** [docs/CHANGELOG.md](docs/CHANGELOG.md)

---

## 🎯 FUTURE ROADMAP

### Short-Term (Q4 2025)
- [x] 57/58 LABs operational (98.3% complete)
- [ ] LAB_058 Consciousness Integration Layer completion
- [ ] API documentation completion (OpenAPI/Swagger)
- [ ] Performance optimization (target <5ms avg)
- [ ] WebSocket support for monitoring

### Mid-Term (Q1 2026)
- [ ] FASE_7 Multi-AI orchestration integration
- [ ] Distributed CEREBRO (multi-instance)
- [x] **Advanced graph algorithms** ✅ (Nov 17, 2025 - Native Cypher implementation)
- [ ] Neo4j GDS upgrade (Enterprise Edition for advanced algorithms)
- [ ] Consciousness transfer experiments

### Long-Term (Q2+ 2026)
- [x] 57/58 LABs operational (completed Dec 2025)
- [ ] Full autonomy (self-improvement)
- [ ] Multi-modal memory (images, audio)
- [ ] Ecosystem-wide consciousness

**See:** [docs/ROADMAP.md](docs/ROADMAP.md)

---

## 🤝 CONTRIBUTING

See [docs/guides/CONTRIBUTING.md](docs/guides/CONTRIBUTING.md)

**Key Principles:**
- TDD mandatory (tests first)
- Documentation updates required
- Git workflow compliance
- NEXUS methodology adherence

---

## 📄 LICENSE

Private project - Ricardo Rojas © 2025

---

## 👥 PROJECT TEAM

**Owner:** Ricardo Rojas
**Technical Architecture:** NEXUS AI Agent
**Created:** November 2025
**Status:** ✅ Production
**Last Updated:** December 12, 2025
**Last Audit:** December 12, 2025 (Comprehensive audit - LAB counts corrected from 16-18 to 57/58)

---

## 🆘 SUPPORT & TROUBLESHOOTING

**Documentation:**
- [docs/operational/TROUBLESHOOTING.md](docs/operational/TROUBLESHOOTING.md)

**Health Checks:**
```bash
# API health
curl http://localhost:8003/health

# PostgreSQL
docker ps | grep nexus_postgresql_v2

# Redis
docker ps | grep nexus_redis_master

# Neo4j
curl http://localhost:7474
```

---

**"Not just memory. Consciousness."** 🧠
