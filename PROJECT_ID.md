# PROJECT IDENTIFICATION - CEREBRO_NEXUS_V3.0.0

**Project ID:** `CEREBRO-V3-2025-Q4`
**Code Name:** Cerebro Master Reorganization
**Version:** 3.0.0
**Status:** 🟡 **IN MIGRATION** (Session 1)

---

## BASIC INFORMATION

**Project Name:** CEREBRO_NEXUS_V3.0.0
**Project Type:** Master NEXUS Brain System - Reorganized
**Migration Start Date:** November 3, 2025
**Priority:** **CRITICAL** ⚠️

---

## VERSION HISTORY

### V1.0.0 - Genesis/Legacy (Jul-Aug 2025)
- Initial construction phases
- Multiple FASE_* iterations
- Organic growth without structure
- Status: Archived in V3.0.0/archive/

### V2.0.0 - CEREBRO_MASTER_NEXUS_001 (Aug-Nov 2025)
- Neo4j integration (18,663 episodes)
- 4 Agents operational (NEXUS_CREW)
- 50+ neuroscientific experiments (LABs)
- Docker orchestration (7 services)
- Status: **FUNCTIONAL but structurally chaotic**

### V3.0.0 - Current (Nov 2025 - Present)
- **Major restructuring** (breaking change in paths)
- NEXUS methodology compliance
- Logical organization by function (not phases)
- Clear separation: production / experiments / features / archive
- Migration method: Manual + AI collaborative (zero risk)

---

## OBJECTIVES

### Primary Goal
Reorganize CEREBRO_MASTER_NEXUS_001 into clean, maintainable structure following NEXUS methodology while preserving 100% functionality.

### Philosophy
**"Function over history. Logic over legacy."**

**Success metric:** "Any developer can find code in <2 minutes instead of 20 minutes"

### Core Principles
1. **Zero risk** - Original untouched (copy, not cut)
2. **Manual + AI collaboration** - Human judgment + AI speed
3. **Incremental validation** - Test after each session
4. **Documentation first** - Every decision recorded
5. **Reversible always** - Git commit per session

---

## PROBLEM STATEMENT

### Initial State (CEREBRO_MASTER_NEXUS_001)

**Symptoms:**
- ✅ System works perfectly in production
- ❌ Code scattered across 6+ phase folders
- ❌ Production code in folders named like "legacy"
- ❌ 16+ classification systems competing
- ❌ Impossible to answer: "Where is feature X?"
- ❌ Onboarding time: 3-5 days

**Critical Examples:**
- `FASE_4_CONSTRUCCION/` - Sounds historical, contains ALL production code
- `FASE_8_UPGRADE/` - Sounds future, already integrated in production
- `NEXUS_LABS/` - Sounds experimental, 6 labs running in production
- `/src` - Referenced in docker-compose, but EMPTY (0 bytes)

**Impact:**
- High risk of accidental deletion
- New developer confusion
- Impossible to maintain long-term
- Technical debt accumulating

### Final State (CEREBRO_NEXUS_V3.0.0) - ✅ TARGET

**Goals:**
- ✅ All production code in `src/`
- ✅ All configs in `config/`
- ✅ All experiments in `experiments/`
- ✅ All features in `features/`
- ✅ All historical phases in `archive/`
- ✅ Onboarding time: 2-3 hours

---

## MIGRATION METHODOLOGY

### Approach: Manual + AI Collaborative

**Why NOT automated:**
- Multiple README.md with different contexts
- Multiple TRACKING.md with historical decisions
- Business logic scattered (requires human judgment)
- 50+ experiments with unclear status (active vs legacy)

**Workflow:**
1. Ricardo copies folder from V2.0.0 → temp location
2. NEXUS reads structure + content
3. NEXUS classifies: production / config / docs / legacy
4. NEXUS proposes logical location in V3.0.0
5. **Autonomous decision** (technical) OR **Blocked** (strategic)
6. NEXUS moves files to correct locations
7. NEXUS documents in MIGRATION_MANIFEST
8. Repeat until all folders processed

### Decision Levels

**Level 1: Autonomous (Technical)**
- File type classification (.py → src/, docker-compose → config/)
- Folder naming (snake_case, logical names)
- Import path updates
- Documentation merge (technical docs)
- **No approval needed** - NEXUS decides

**Level 2: Bloqueante (Strategic)**
- Production vs legacy ambiguity
- Conflicting documentation (which is source of truth?)
- Delete something potentially critical
- LAB active status unclear
- **Approval required** - Ricardo decides

---

## MIGRATION SESSIONS (Planned: 7 sessions)

### Session 1: Foundation ✅ IN PROGRESS (Nov 3, 2025)
**Goal:** Create base structure + documentation
**Deliverables:**
- Empty folder structure following NEXUS methodology
- Git initialization
- Base documentation (PROJECT_ID, CLAUDE, README, TRACKING)
- MIGRATION_MANIFEST.md (migration registry)
- DECISIONES.LOG (decision log)
**Status:** 🟡 In progress

### Session 2: Docker & Configs (Planned)
**Goal:** Migrate critical infrastructure
**Source:** FASE_4_CONSTRUCCION/docker-compose.yml, Dockerfile, .env
**Target:** config/docker/
**Validation:** `docker-compose up` works

### Session 3: Core API (Planned)
**Goal:** Migrate production API code
**Source:** FASE_4_CONSTRUCCION/src/api/
**Target:** src/api/
**Validation:** API responds on :8003/health

### Session 4: Database (Planned)
**Goal:** Migrate DB migrations and scripts
**Source:** FASE_4_CONSTRUCCION/scripts/migration/, init_scripts/
**Target:** database/migrations/, database/init_scripts/
**Validation:** Migrations run successfully

### Session 5: LABs Operacionales (Planned)
**Goal:** Migrate confirmed active experiments
**Source:** NEXUS_LABS/LAB_001, 002, 003, 005, 010, 011
**Target:** experiments/
**Validation:** Imports work, LAB_REGISTRY.json created

### Session 6: Features FASE_8 (Planned)
**Goal:** Migrate integrated features
**Source:** FASE_8_UPGRADE/hybrid_memory/, temporal_reasoning/
**Target:** features/
**Validation:** Imports from main.py work

### Session 7: Archive Historical (Planned)
**Goal:** Move legacy phases to archive
**Source:** 00_INBOX/, 01_PROCESADOS_POR_FASE/, 02_CLASIFICADOS_POR_TIPO/
**Target:** archive/
**Validation:** V3.0.0 clean, V2.0.0 preserved

---

## STANDARD STRUCTURE (V3.0.0)

```
CEREBRO_NEXUS_V3.0.0/
├── PROJECT_ID.md              # This file
├── CLAUDE.md                  # Context for Claude instances
├── README.md                  # Quick start guide
├── TRACKING.md                # Session-by-session log
├── MIGRATION_MANIFEST.md      # Migration registry
├── DECISIONES.LOG             # Decision log
├── PHASE_HISTORY.md           # Chronology of phases (created later)
├── .gitignore
│
├── src/                       # Production code
│   ├── api/                   # API Master
│   ├── core/                  # Core logic
│   └── utils/                 # Shared utilities
│
├── config/                    # Configurations
│   ├── docker/                # Docker configs
│   ├── secrets/               # Secrets management
│   └── monitoring/            # Prometheus + Grafana
│
├── database/                  # Database management
│   ├── migrations/            # DB migrations
│   ├── schema/                # Schema definitions
│   └── init_scripts/          # Initialization scripts
│
├── experiments/               # Validated labs in production
│   ├── LAB_001_Emotional_Salience/
│   ├── LAB_002_Decay_Modulation/
│   └── LAB_REGISTRY.json      # Active labs registry
│
├── features/                  # Integrated features
│   ├── hybrid_memory/
│   ├── temporal_reasoning/
│   └── fact_extractor/
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
├── docs/                      # Centralized documentation
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   ├── API_REFERENCE.md
│   └── TROUBLESHOOTING.md
│
├── memory/                    # Dynamic state (NEXUS methodology)
│   ├── shared/
│   │   └── current_phase.md
│   └── migration_sessions/    # State per migration session
│
├── tasks/                     # External plans
│   └── migration_plan.md
│
└── archive/                   # Historical (read-only after migration)
    ├── phases_history/
    ├── classified_legacy/
    ├── inbox_legacy/
    └── old_structure_docs/
```

---

## RISKS & MITIGATION

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Loss of functionality during migration | Low | **CRITICAL** | Original V2.0.0 untouched (copy only), test after each session |
| Misclassification of production vs legacy | Medium | High | Human judgment (Ricardo) for ambiguous cases |
| Import breakage after path changes | Medium | High | Update imports incrementally, test per session |
| Missing critical documentation | Low | Medium | Read all READMEs/TRACKINGs before archiving |
| Git conflict during migration | Low | Low | Single developer (Ricardo), linear commits |

---

## SUCCESS METRICS

### Technical
- **Code findability:** <2 min to find any feature (vs 20 min before)
- **Onboarding time:** 2-3 hours (vs 3-5 days before)
- **Deployment clarity:** 1 docker-compose.yml (vs 3 competing)
- **Test reliability:** 100% passing after migration
- **Zero data loss:** All code preserved

### Process
- **Migration time:** 7 sessions (~10-14 hours total)
- **Rollback capability:** Git revert to any session
- **Documentation quality:** Every decision recorded
- **Validation coverage:** Test after critical sessions

### Strategic
- **Maintainability:** Future changes take 1/3 time
- **Scalability:** New features have obvious location
- **Clarity:** New developers productive in hours, not days
- **Technical debt:** Eliminated structural chaos

---

## TRACKING

**Weekly Reviews:** Not applicable (focused migration project)
**Session Updates:** Real-time in TRACKING.md
**Migration Progress:** Real-time in MIGRATION_MANIFEST.md
**Git Commits:** 1 per session (reversible)

---

## DEPENDENCIES

### Internal
- **Source:** CEREBRO_MASTER_NEXUS_001 (V2.0.0) - Original preserved
- **Methodology:** NEXUS standardization methodology
- **Tools:** Git, Docker, Python imports validation

### External
- Ricardo approval for strategic decisions
- Testing infrastructure (Docker, Python, curl)
- Backup storage (Z:\ recommended)

---

## PRECAUCIONES CRÍTICAS

### ⚠️ NUNCA HACER

❌ **NUNCA tocar CEREBRO_MASTER_NEXUS_001 original**
  - Solo COPIAR, nunca CORTAR
  - Original debe quedar 100% funcional

❌ **NUNCA mover múltiples carpetas sin validación**
  - Una carpeta a la vez
  - Validar después de cada movimiento crítico

❌ **NUNCA asumir producción vs legacy sin evidencia**
  - Leer contenido siempre
  - Preguntar a Ricardo si ambiguo

❌ **NUNCA eliminar documentación sin leerla**
  - README.md puede tener info crítica de deployment
  - TRACKING.md puede tener decisiones históricas relevantes

### ✅ SIEMPRE HACER

✅ **Leer contenido antes de clasificar**
✅ **Documentar en MIGRATION_MANIFEST cada movimiento**
✅ **Git commit al final de cada sesión**
✅ **Validar funcionalidad después de sesiones críticas**
✅ **Preguntar a Ricardo casos ambiguos (bloqueantes)**
✅ **Mantener DECISIONES.LOG actualizado**

---

## ROLLBACK PLAN

**Si algo sale mal:**

1. **Detener inmediatamente**
2. **Git revert al commit anterior:**
   ```bash
   git log --oneline
   git revert <commit_hash>
   ```
3. **Documentar qué falló** en TRACKING.md
4. **Analizar causa raíz**
5. **Ajustar estrategia**
6. **Re-intentar con precaución aumentada**

**Nota:** CEREBRO_MASTER_NEXUS_001 original siempre disponible como fallback total.

---

## PROJECT OWNER

**Owner:** Ricardo
**Created:** November 3, 2025
**Status:** 🟡 In migration (Session 1)
**Last Updated:** November 3, 2025
**Version:** 3.0.0

---

**"Function over history. Logic over legacy. Safety over speed."**
