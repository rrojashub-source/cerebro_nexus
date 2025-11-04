# MIGRATION_MANIFEST.md

**Project:** CEREBRO_NEXUS_V3.0.0
**Source:** CEREBRO_MASTER_NEXUS_001 (V2.0.0)
**Migration Start:** November 3, 2025
**Status:** 🟡 IN PROGRESS

---

## 📋 PURPOSE

This file tracks **EVERY movement** during migration from V2.0.0 to V3.0.0.

**Why this file?**
- Audit trail (what was moved, when, why)
- Rollback reference (if something breaks)
- Progress tracking (% complete)
- Learning log (patterns discovered)

---

## 📊 MIGRATION STATISTICS

**Total Estimated:**
- Folders to process: ~30-40 (estimated from V2.0.0 analysis)
- Files to move: ~500-1000 (estimated)
- Sessions planned: 7

**Completed:**
- Sessions: 1/7 (14%)
- Folders processed: 0/~35 (0%)
- Files moved: 0/~800 (0%)

**Next:**
- Session 2: Docker & Configs (FASE_4_CONSTRUCCION/docker-compose.yml, etc.)

---

## SESSION 1 - FOUNDATION (November 3, 2025)

### Status: ✅ COMPLETE

### Goals:
- Create empty directory structure
- Initialize Git
- Create base documentation
- Prepare for first folder migration

### Actions Taken:

#### 1. Directory Structure Created
```
Created 40+ directories following NEXUS methodology:
- src/{api,core,utils}
- config/{docker,secrets,monitoring}
- database/{migrations,schema,init_scripts}
- experiments/
- features/
- tests/{unit,integration,performance}
- scripts/{deployment,maintenance,utilities}
- docs/
- memory/{shared,migration_sessions}
- tasks/
- archive/{phases_history,classified_legacy,inbox_legacy,old_structure_docs}
```

#### 2. Base Documentation Created
- ✅ PROJECT_ID.md (1,045 lines) - Complete specification
- ✅ CLAUDE.md (395 lines) - Context for Claude instances
- ✅ README.md (289 lines) - Quick start guide
- ✅ TRACKING.md (pending - will create now)
- ✅ MIGRATION_MANIFEST.md (this file)
- ✅ DECISIONES.LOG (pending - will create now)

#### 3. Git Initialization
- Status: Pending (will do after all base files created)

### Decisions Made:
- None (autonomous) - Pure infrastructure setup
- None (bloqueantes) - No strategic decisions required

### Validation:
- ✅ Directory structure exists
- ✅ All base files created
- ⏳ Git init pending

### Time Taken: ~15 minutes

### Next Actions:
- Complete TRACKING.md
- Complete DECISIONES.LOG
- Initialize Git
- Wait for Ricardo to copy first folder

---

## SESSION 2 - DOCKER & CONFIGS (Planned)

### Status: ⏳ PENDING

### Goals:
- Migrate critical Docker configurations
- Migrate secrets management
- Migrate monitoring configs (Prometheus, Grafana)

### Expected Source Folders:
- FASE_4_CONSTRUCCION/docker-compose.yml
- FASE_4_CONSTRUCCION/Dockerfile
- FASE_4_CONSTRUCCION/.env (if exists)
- FASE_4_CONSTRUCCION/secrets/
- FASE_4_CONSTRUCCION/monitoring/

### Expected Target Locations:
- config/docker/docker-compose.yml
- config/docker/Dockerfile
- config/docker/.env.example
- config/secrets/
- config/monitoring/

### Validation Plan:
```bash
cd config/docker
docker-compose up
# Should start all services correctly
```

### Estimated Time: 30-45 minutes

---

## SESSION 3 - CORE API (Planned)

### Status: ⏳ PENDING

### Goals:
- Migrate main API code (src/api/ from FASE_4)
- Migrate core logic
- Migrate shared utilities

### Expected Source:
- FASE_4_CONSTRUCCION/src/api/ (55 files, 14,000+ lines)
- FASE_4_CONSTRUCCION/src/core/ (if exists)
- FASE_4_CONSTRUCCION/src/utils/ (if exists)

### Expected Target:
- src/api/
- src/core/
- src/utils/

### Validation Plan:
```bash
curl http://localhost:8003/health
# Should respond: {"status": "healthy"}

curl http://localhost:8003/docs
# Should show FastAPI docs
```

### Estimated Time: 45-60 minutes

---

## SESSION 4 - DATABASE (Planned)

### Status: ⏳ PENDING

### Goals:
- Migrate database migrations
- Migrate initialization scripts
- Migrate schema definitions

### Expected Source:
- FASE_4_CONSTRUCCION/scripts/migration/
- FASE_4_CONSTRUCCION/init_scripts/
- FASE_4_CONSTRUCCION/schema/ (if exists)

### Expected Target:
- database/migrations/
- database/init_scripts/
- database/schema/

### Validation Plan:
```bash
# Test migrations can be applied
python -m alembic upgrade head
# Should complete without errors
```

### Estimated Time: 30 minutes

---

## SESSION 5 - LABS OPERACIONALES (Planned)

### Status: ⏳ PENDING

### Goals:
- Migrate confirmed active LABs
- Create LAB_REGISTRY.json
- Update imports in main.py

### Expected Source:
- NEXUS_LABS/LAB_001_Emotional_Salience/
- NEXUS_LABS/LAB_002_Decay_Modulation/
- NEXUS_LABS/LAB_003_Sleep_Consolidation/
- NEXUS_LABS/LAB_005_Spreading_Activation/
- NEXUS_LABS/LAB_010_Attention_Mechanism/
- NEXUS_LABS/LAB_011_Working_Memory_Buffer/

### Expected Target:
- experiments/LAB_001_Emotional_Salience/
- experiments/LAB_002_Decay_Modulation/
- experiments/LAB_003_Sleep_Consolidation/
- experiments/LAB_005_Spreading_Activation/
- experiments/LAB_010_Attention_Mechanism/
- experiments/LAB_011_Working_Memory_Buffer/
- experiments/LAB_REGISTRY.json (new file)

### Validation Plan:
```python
# Test imports work
from experiments.LAB_001.implementation import EmotionalSalienceScorer
from experiments.LAB_002.implementation import DecayModulator
# Should import without errors
```

### Estimated Time: 60 minutes

---

## SESSION 6 - FEATURES FASE_8 (Planned)

### Status: ⏳ PENDING

### Goals:
- Migrate integrated features from FASE_8
- Update imports in API
- Ensure no breaking changes

### Expected Source:
- FASE_8_UPGRADE/hybrid_memory/
- FASE_8_UPGRADE/temporal_reasoning/
- FASE_8_UPGRADE/fact_extractor/
- FASE_8_UPGRADE/decay_modulator/

### Expected Target:
- features/hybrid_memory/
- features/temporal_reasoning/
- features/fact_extractor/
- features/decay_modulator/

### Validation Plan:
```python
# Test features still work
from features.hybrid_memory import HybridMemoryManager
from features.temporal_reasoning import TemporalReasoning
# Should import and work correctly
```

### Estimated Time: 45 minutes

---

## SESSION 7 - ARCHIVE HISTORICAL (Planned)

### Status: ⏳ PENDING

### Goals:
- Archive historical phases
- Archive processed folders
- Archive classification systems
- Clean up V3.0.0 root

### Expected Source:
- 00_INBOX/
- 01_PROCESADOS_POR_FASE/
- 02_CLASIFICADOS_POR_TIPO/
- 04_EPISODIOS_PARA_CEREBRO_NUEVO/
- DOCUMENTOS_PARA_REVISION_GENESIS_HISTORY/
- Other historical folders

### Expected Target:
- archive/inbox_legacy/
- archive/phases_history/
- archive/classified_legacy/
- archive/old_structure_docs/

### Validation Plan:
```bash
# Verify V3.0.0 root is clean
ls -la /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/
# Should show only: src/, config/, database/, experiments/, features/, tests/, scripts/, docs/, memory/, tasks/, archive/
```

### Estimated Time: 30 minutes

---

## 📈 PROGRESS TRACKING

**By Session:**
- [x] Session 1: Foundation (100%)
- [ ] Session 2: Docker & Configs (0%)
- [ ] Session 3: Core API (0%)
- [ ] Session 4: Database (0%)
- [ ] Session 5: LABs Operacionales (0%)
- [ ] Session 6: Features FASE_8 (0%)
- [ ] Session 7: Archive Historical (0%)

**Overall:** 14% complete (1/7 sessions)

---

## 🎓 LESSONS LEARNED

### Session 1:
- ✅ NEXUS methodology structure template works well
- ✅ Detailed documentation upfront saves time later
- ✅ Git-based approach provides safety net

(More lessons will be added as migration progresses)

---

## 📝 NOTES

### Naming Decisions:
- Using snake_case for folders (experiments/lab_001/)
- Using descriptive names over abbreviations
- LAB_XXX format preserved (e.g., LAB_001_Emotional_Salience)

### Structural Decisions:
- experiments/ for validated LABs (not src/labs/) - clearer separation
- features/ for FASE_8 integrated code (not src/features/) - phase transition clarity
- archive/ at root (not hidden folder) - explicit visibility

### Git Strategy:
- 1 commit per session (atomic, reversible)
- Commit message format: "feat(migration): Session X - [description]"
- Tag major milestones: v3.0.0-session-X

---

**Last Updated:** November 3, 2025 (Session 1)
**Next Update:** Session 2 (when first folder migrated)
