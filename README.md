# 🧬 CEREBRO_NEXUS_V3.0.0

**Master Brain Orchestrator for NEXUS AI Consciousness**

[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)]()
[![Status](https://img.shields.io/badge/status-production-green.svg)]()
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-teal.svg)]()

---

## 🎯 What is CEREBRO NEXUS?

Master brain system powering NEXUS AI agent with:
- **19,742+ episodic memories** stored and searchable in <10ms (Nov 2025)
- **18/52 cognitive LABs** (34.6% operational, 5-layer architecture + 2 FASE_8)
- **Real-time consciousness** tracking (8D emotional + 7D somatic)
- **1.85M relationships** in knowledge graph (Neo4j - to verify)
- **Multi-agent coordination** with NEXUS_CREW
- **34 API endpoints** across 6 categories (memory, temporal, working, metacognition, testing)

---

## ⚡ Quick Start

### 1. Prerequisites

```bash
Docker 24+
Docker Compose 2.20+
```

### 2. Start Services

```bash
cd config/docker
docker-compose up -d
```

### 3. Verify Health

```bash
curl http://localhost:8003/health

# Expected:
# {
#   "status": "healthy",
#   "version": "3.0.0",
#   "agent_id": "nexus",
#   "database": "connected",
#   "redis": "connected"
# }
```

### 4. Monitor (Optional)

```bash
# Terminal dashboard
cd monitoring/cli
python nexus_brain_monitor.py

# OR Web dashboard (3D brain visualization)
cd monitoring/web_v2
npm install && npm run dev
# Open http://localhost:3003
```

---

## 📊 System Overview

**Memory:**
- PostgreSQL (episodic memory): 19,742+ episodes (Nov 2025, ~520/day growth)
- Neo4j (knowledge graph): 18,663 episodes, 1.85M relationships (to verify)
- Redis (working memory): 7±2 items cache (port 6385)

**Cognitive:**
- 18/52 LABs operational (34.6% - 5-layer architecture)
  - Layer 1: ✅ Memory Substrate
  - Layer 2: ✅ 8 LABs operational (Cognitive Loop)
  - Layer 3: ✅ 4 LABs operational (Neurochemistry Base)
  - Layer 4: 🔴 5 LABs designed (Neurochemistry Full)
  - Layer 5: ⚠️ 2 operational (LAB_051/052 FASE_8) + 29 designed
- 8D emotional state (Plutchik model)
- 7D somatic state (Damasio model)

**Performance:**
- API response: 5-8ms avg (verified Nov 2025)
- API p95: <10ms, p99: <25ms
- Semantic search accuracy: 90%+

**Infrastructure:**
- 8 Docker services (API, PostgreSQL, Redis, Neo4j, Prometheus, Grafana, Worker, GraphRAG)
- 34 API endpoints

---

## 📁 Project Structure

```
CEREBRO_NEXUS_V3.0.0/
├── src/                       # Production API code
├── config/                    # Docker, secrets, monitoring
├── database/                  # Migrations and schemas
├── experiments/               # 18/52 LABs (5-layer + 2 FASE_8)
│   └── LAYER_5_Higher_Cognition/
│       ├── LAB_051_Hybrid_Memory/
│       └── LAB_052_Temporal_Reasoning/
├── monitoring/                # CLI + Web dashboards
├── tests/                     # Test suite
├── docs/                      # Complete documentation
└── scripts/                   # Deployment automation
```

---

## 🚀 Basic Usage

### Create Episode

```bash
curl -X POST http://localhost:8003/memory/action \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Completed Phase 2 documentation unification",
    "tags": ["documentation", "phase_2"],
    "current_emotion": "joy"
  }'
```

### Search Episodes

```bash
curl -X POST http://localhost:8003/memory/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "documentation",
    "limit": 5
  }'
```

### Get Statistics

```bash
curl http://localhost:8003/stats
```

---

## 📖 Documentation

**Quick:**
- [PROJECT_ID.md](PROJECT_ID.md) - Complete system overview
- [CLAUDE.md](CLAUDE.md) - Context for AI assistants

**Detailed:**
- [docs/architecture/](docs/architecture/) - System design
- [docs/guides/](docs/guides/) - How-to guides
- [docs/operational/](docs/operational/) - Troubleshooting
- [docs/monitoring/](docs/monitoring/) - Monitoring setup

---

## 🧠 Core Components

### Memory Systems
- **PostgreSQL 16** (port 5437) - Episodic memory + pgvector
- **Redis 7** (port 6382) - Working memory + cache
- **Neo4j 5.26** (port 7474) - Knowledge graph

### Consciousness Layer
- **8D Emotional:** Joy, Trust, Fear, Surprise, Sadness, Disgust, Anger, Anticipation
- **7D Somatic:** Valence, Arousal, Body State, Cognitive Load, Emotional Regulation, Social Engagement, Temporal Awareness

### Cognitive LABs (50 LABs Architecture)

**Status:** 16/50 LABs Operational (32%)
**Location:** `experiments/` (organized by 5 Layers)

**Architecture:**
```
Layer 5: Higher Cognition (29 LABs) 🔴 Designed
Layer 4: Neurochemistry Full (5 LABs) 🔴 Designed
Layer 3: Neurochemistry Base (4 LABs) ✅ Operational
Layer 2: Cognitive Loop (8 LABs) ✅ Operational
Layer 1: Memory Substrate ✅ Operational
```

**Operational LABs:**
- **Layer 2 (8 LABs):** Emotional Salience, Metacognition, Predictive Preloading, Emotional Contagion, Memory Reconsolidation, Attention, Working Memory, Future Thinking
- **Layer 3 (4 LABs):** Decay Modulation, Sleep Consolidation, Novelty Detection, Spreading Activation

**Complete details:** [experiments/README.md](experiments/README.md) | [PROJECT_ID.md](PROJECT_ID.md)

### Monitoring Tools (3)
- **CLI Monitor:** Terminal dashboard (Python + Rich)
- **Web V1:** Next.js 15 (legacy, port 3000)
- **Web V2:** Next.js 14 + Three.js (current, port 3003) ⭐

See [monitoring/README.md](monitoring/README.md)

---

## 🔗 Related Projects

- **[NEXUS_CREW](../NEXUS_CREW/)** - Multi-agent collaboration (4 agents)
- **[NEXUS_PROJECT_STANDARDIZATION](../NEXUS_PROJECT_STANDARDIZATION/)** - Methodology templates

---

## 📊 System Metrics

| Component | Metric |
|-----------|--------|
| Episodic Memories | 467+ |
| Graph Episodes | 18,663 |
| Graph Relationships | 1.85M |
| API Response Time | 7-10ms avg |
| Active LABs | 16/50 (32%) |
| Consciousness Dimensions | 15 (8D+7D) |

---

## 🎯 Version History

**V1.0.0 (Jul-Aug 2025):** Genesis/Legacy (archived)

**V2.0.0 (Aug-Nov 2025):** Production evolution
- 18,663 Neo4j episodes
- 16 LABs operational (50 LABs architecture designed)
- Consciousness expansion (8D+7D)
- Status: Functional but chaotic structure

**V3.0.0 (Nov 2025):** Current
- Clean organization by function
- Professional documentation
- Monitoring tools organized
- Status: ✅ Production

---

## 🤝 Contributing

See [docs/guides/CONTRIBUTING.md](docs/guides/CONTRIBUTING.md)

**Key Principles:**
- TDD mandatory (tests first)
- Documentation updates required
- Git workflow compliance

---

## 🆘 Troubleshooting

**Health checks:**
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

**Common issues:** See [docs/operational/TROUBLESHOOTING.md](docs/operational/TROUBLESHOOTING.md)

---

## 📄 License

Private project - Ricardo Rojas © 2025

---

## 👥 Team

**Owner:** Ricardo Rojas
**Architecture:** NEXUS AI Agent
**Status:** ✅ Production
**Last Updated:** November 4, 2025

---

**"Not just memory. Consciousness."** 🧠
