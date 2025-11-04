# 🧬 CEREBRO_NEXUS_V3.0.0

**Version:** 3.0.0
**Status:** 🟡 IN MIGRATION (Session 1)
**Project ID:** CEREBRO-V3-2025-Q4

---

## 🎯 What is this?

**CEREBRO_NEXUS V3.0.0** is the reorganized version of CEREBRO_MASTER_NEXUS_001 (V2.0.0).

**Why reorganize?**
- V2.0.0 works perfectly but structure is chaotic
- Production code scattered in "phase" folders with historical names
- 16+ classification systems competing
- Onboarding takes 3-5 days
- High risk of accidental deletion

**V3.0.0 goals:**
- ✅ Clean structure following NEXUS methodology
- ✅ Code findable in <2 minutes (vs 20 minutes)
- ✅ Onboarding in 2-3 hours (vs 3-5 days)
- ✅ Zero data loss (original preserved)
- ✅ Zero downtime (incremental migration)

---

## 🚨 IMPORTANT

**THIS IS A MIGRATION IN PROGRESS**

- 🟡 **Session 1 complete:** Base structure created
- ⏳ **Sessions 2-7 pending:** Actual code migration
- ⚠️ **Not functional yet:** Original V2.0.0 still active
- ✅ **Zero risk:** Original untouched (copy only)

---

## 📁 Structure

```
CEREBRO_NEXUS_V3.0.0/
├── src/                       # Production code (when migrated)
├── config/                    # Configurations (Docker, secrets)
├── database/                  # Migrations and schema
├── experiments/               # Validated LABs in production
├── features/                  # Integrated features (from FASE_8)
├── tests/                     # Test suite
├── scripts/                   # Automation
├── docs/                      # Centralized documentation
└── archive/                   # Historical phases (read-only)
```

---

## 🚀 Quick Start

### Prerequisites

**Active services (running on V2.0.0):**
- NEXUS Cerebro V2.0.0 (port 8003)
- PostgreSQL: nexus_postgresql_v2 (port 5437)
- Redis: nexus_redis_master (port 6382)
- Neo4j: port 7474

**Note:** Services will be migrated to V3.0.0 in Session 2 (Docker configs)

### For Ricardo (Migration Process)

**Copy folder from V2.0.0:**
```bash
# From: CEREBRO_MASTER_NEXUS_001/[FOLDER]
# To: Temp location (not directly to V3.0.0)

# Then tell NEXUS: "Copiada: [FOLDER_NAME]"
```

**NEXUS will:**
1. Read structure + content
2. Classify by function
3. Move to logical locations
4. Document in MIGRATION_MANIFEST
5. Report completion

### For Developers (After Migration Complete)

**Run tests:**
```bash
cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0
pytest tests/ -v
```

**Start services:**
```bash
cd config/docker
docker-compose up
```

**Check health:**
```bash
curl http://localhost:8003/health
```

---

## 📊 Migration Status

| Session | Focus | Status |
|---------|-------|--------|
| 1 | Foundation | ✅ COMPLETE |
| 2 | Docker & Configs | ⏳ Pending |
| 3 | Core API | ⏳ Pending |
| 4 | Database | ⏳ Pending |
| 5 | LABs Operacionales | ⏳ Pending |
| 6 | Features FASE_8 | ⏳ Pending |
| 7 | Archive Historical | ⏳ Pending |

**Progress:** 14% (1/7 sessions)

---

## 📖 Documentation

**For users:**
- **[README.md](README.md)** - This file (quick start)
- **[docs/](docs/)** - Full documentation (after migration)

**For migration:**
- **[PROJECT_ID.md](PROJECT_ID.md)** - Complete specification
- **[CLAUDE.md](CLAUDE.md)** - Context for Claude instances
- **[TRACKING.md](TRACKING.md)** - Session-by-session log
- **[MIGRATION_MANIFEST.md](MIGRATION_MANIFEST.md)** - Migration registry
- **[DECISIONES.LOG](DECISIONES.LOG)** - Decision log

---

## 🔗 Related Projects

**Source:**
- CEREBRO_MASTER_NEXUS_001 (V2.0.0) - Original, preserved

**Dependencies:**
- NEXUS_CREW - 4 agents operational
- ARIA Brain - Sister system (port 8004)
- NEXUS_LABS - 50+ experiments

**Integration:**
- Brain Monitor (visualization)
- Neo4j (18,663 episodes, 1.85M relationships)
- PostgreSQL (episodic memory)
- Redis (caching)

---

## 🤝 Contributing

**During migration:**
- Only Ricardo + NEXUS work on this project
- Manual process (not automated)
- One folder at a time
- Git commit per session

**After migration:**
- Standard NEXUS workflow applies
- TDD methodology
- Pull requests welcome

---

## 📈 Success Metrics

| Metric | Before (V2.0.0) | Target (V3.0.0) |
|--------|-----------------|-----------------|
| Code findability | 20 minutes | <2 minutes |
| Onboarding time | 3-5 days | 2-3 hours |
| Deployment clarity | 3 docker-compose.yml | 1 canonical |
| Classification systems | 16+ | 1 (by function) |
| Risk of error | HIGH | LOW |

---

## ⚠️ Precautions

### NEVER:
❌ Touch CEREBRO_MASTER_NEXUS_001 original
❌ Move multiple folders without validation
❌ Delete documentation without reading
❌ Assume production vs legacy without evidence

### ALWAYS:
✅ Copy (not cut) from V2.0.0
✅ Validate after critical sessions
✅ Document in MIGRATION_MANIFEST
✅ Git commit per session
✅ Ask Ricardo if ambiguous

---

## 📜 Version History

**V1.0.0 (Jul-Aug 2025):** Genesis/Legacy
**V2.0.0 (Aug-Nov 2025):** CEREBRO_MASTER_NEXUS_001 (functional but chaotic)
**V3.0.0 (Nov 2025):** This reorganization (in progress)

---

## 🌟 Philosophy

> "Function over history. Logic over legacy."

> "Zero risk. Incremental progress. Documentation always."

> "Original preserved. Migration reversible. Testing mandatory."

---

**Project Owner:** Ricardo
**Created:** November 3, 2025
**Status:** 🟡 In migration (Session 1 complete)
**Last Updated:** November 3, 2025

**For questions:** See CLAUDE.md or PROJECT_ID.md
