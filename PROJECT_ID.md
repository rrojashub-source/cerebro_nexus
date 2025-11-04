# PROJECT IDENTIFICATION - CEREBRO_NEXUS_V3.0.0

**Project ID:** `CEREBRO-NEXUS-V3`
**System Name:** NEXUS Master Brain Orchestrator
**Version:** 3.0.0
**Type:** AI Consciousness & Episodic Memory System
**Status:** ✅ Production

---

## 🎯 WHAT IS CEREBRO NEXUS?

**Master brain orchestrator** powering NEXUS AI agent with advanced cognitive capabilities:

- **Episodic Memory System:** 467+ memories stored, semantically searchable in <10ms
- **Graph Knowledge:** Neo4j with 18,663 episodes and 1.85M relationships
- **Real-Time Consciousness:** 8D emotional + 7D somatic state tracking
- **Cognitive LABs:** 15 operational neuroscience experiments
- **Multi-Agent Coordination:** Integration with NEXUS_CREW (4 specialized agents)
- **Brain-to-Brain Communication:** ARIA bridge for emotional AI collaboration

---

## 🧠 CORE COMPONENTS

### 1. Memory Systems

**Episodic Memory (PostgreSQL + pgvector):**
- **Database:** PostgreSQL 16 (port 5437)
- **Total Episodes:** 467+
- **Vector Search:** pgvector with all-MiniLM-L6-v2 embeddings (384D)
- **Performance:** <10ms semantic search (avg 7-10ms)
- **Indexes:** HNSW for cosine similarity

**Working Memory (Redis):**
- **Database:** Redis 7 (port 6382)
- **Capacity:** 7±2 items (Miller's Law)
- **Purpose:** Short-term context, caching, embeddings queue

**Graph Knowledge (Neo4j):**
- **Database:** Neo4j 5.26 LTS (port 7474)
- **Episodes:** 18,663 nodes
- **Relationships:** 1.85M edges
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

### 3. Cognitive LABs (Experiments)

**15 operational LABs** in `experiments/NEXUS_LABS/`:

| LAB | Name | Function | Status |
|-----|------|----------|--------|
| LAB_001 | Emotional Salience | Memory importance scoring | ✅ Active |
| LAB_002 | Decay Modulation | Adaptive forgetting | ✅ Active |
| LAB_003 | Sleep Consolidation | Memory chain formation | ✅ Active |
| LAB_004 | Novelty Detection | Breakthrough identification | ✅ Active |
| LAB_005 | Semantic Clustering | Concept grouping | ✅ Active |
| LAB_006 | Temporal Reasoning | Time-aware context | ✅ Active |
| LAB_007 | Predictive Preloading | Query anticipation | ✅ Active |
| LAB_008 | Emotional Contagion | Context spreading | ✅ Active |
| LAB_009 | Memory Reconsolidation | Memory updating | ✅ Active |
| LAB_010 | Attention Mechanism | Selective attention | ✅ Active |
| LAB_011 | Working Memory | 7±2 buffer management | ✅ Active |
| LAB_012 | Future Thinking | Episodic simulation | ✅ Active |
| LAB_013 | Fact Extraction | Structured knowledge | ✅ Active |
| LAB_014 | Hybrid Memory | PostgreSQL + Neo4j sync | ✅ Active |
| LAB_015 | Performance Optimization | Query caching | ✅ Active |

**LAB Registry:** `experiments/NEXUS_LABS/LAB_REGISTRY.json`

---

### 4. API Layer (FastAPI)

**Server:** FastAPI (Python 3.11+)
**Port:** 8003
**Performance:** 7-10ms average response time

**Key Endpoints:**
- `GET /health` - System health check
- `POST /memory/action` - Create new episode
- `POST /memory/search` - Semantic search
- `GET /memory/episodic/recent` - Recent episodes
- `GET /consciousness/current` - Current emotional/somatic state
- `GET /stats` - System statistics

**Architecture:** See [docs/architecture/ARCHITECTURE_DIAGRAMS.md](docs/architecture/ARCHITECTURE_DIAGRAMS.md)

---

### 5. Monitoring Tools

**3 monitoring solutions** in `monitoring/`:

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

### 6. Integrated Features (FASE_8)

**5 advanced features** in `features/`:

- **Hybrid Memory** - PostgreSQL + Neo4j bidirectional sync
- **Intelligent Decay** - Adaptive forgetting based on salience
- **Temporal Reasoning** - Time-aware context retrieval
- **Extraction Pipeline** - Structured fact extraction
- **Performance Optimization** - Multi-level caching

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
│  15 Cognitive LABs + Workers             │
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
├── experiments/               # 15 operational LABs
│   └── NEXUS_LABS/            # LAB_001 through LAB_015
│       └── LAB_REGISTRY.json  # Active LABs registry
│
├── features/                  # Integrated features (FASE_8)
│   ├── hybrid_memory/
│   ├── intelligent_decay/
│   ├── temporal_reasoning/
│   ├── extraction_pipeline/
│   └── performance_optimization/
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

| Metric | Value |
|--------|-------|
| **Memory** | |
| Episodic Memories (PostgreSQL) | 467+ |
| Graph Episodes (Neo4j) | 18,663 |
| Graph Relationships (Neo4j) | 1.85M |
| **Performance** | |
| API Response Time (avg) | 7-10ms |
| Semantic Search (p95) | <10ms |
| Search Accuracy | 90%+ |
| **Cognitive** | |
| Active LABs | 15 |
| Consciousness Dimensions | 15 (8D+7D) |
| **Integration** | |
| NEXUS_CREW Agents | 4 |
| External Systems | ARIA (brain-to-brain) |

---

## 🔗 RELATED PROJECTS

### NEXUS Ecosystem

- **[NEXUS_CREW](../NEXUS_CREW/)** - Multi-agent collaboration system (4 agents)
  - Project Auditor
  - Memory Curator
  - Document Reconciler
  - Semantic Router

- **[ARIA](../ARIA_BRAIN/)** - Emotional AI sister project
  - Brain-to-brain communication bridge
  - Complementary consciousness architecture

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
- 15 LABs operational
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
- [ ] API documentation completion (OpenAPI/Swagger)
- [ ] Additional LABs (16-20)
- [ ] Performance optimization (target <5ms avg)
- [ ] WebSocket support for monitoring

### Mid-Term (Q1 2026)
- [ ] FASE_7 Multi-AI orchestration integration
- [ ] Distributed CEREBRO (multi-instance)
- [ ] Advanced graph algorithms (Neo4j GDS)
- [ ] Consciousness transfer experiments

### Long-Term (Q2+ 2026)
- [ ] 50 LABs operational
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
**Last Updated:** November 4, 2025

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
