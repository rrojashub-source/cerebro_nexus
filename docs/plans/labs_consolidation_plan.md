# LABs Consolidation Plan

**Created:** November 5, 2025 (Session 16 - Post CEREBRO_ANALYST Audit)
**Status:** 📋 Planning
**Priority:** Medium
**Effort:** High (2-3 sessions)

---

## 🎯 Objective

Consolidate all LAB implementations into unified `experiments/` hierarchy for better maintainability, discoverability, and consistency.

---

## 🔍 Current State (Scattered)

### LABs in Multiple Locations

**1. `experiments/NEXUS_LABS/` (Primary - 15 LABs)**
- LAB_001 Emotional Salience
- LAB_002 Decay Modulation
- LAB_003 Sleep Consolidation
- LAB_004 Curiosity Driven Memory
- LAB_005 MultiModal Memory
- LAB_006 Metacognition Logger
- LAB_007 Predictive Preloading
- LAB_008 Emotional Contagion
- LAB_009 Memory Reconsolidation
- LAB_010 Attention Mechanism
- LAB_011 Working Memory Buffer
- LAB_012 Episodic Future Thinking
- LAB_013 Dopamine System
- LAB_014 Serotonin System
- LAB_015 Norepinephrine System

**2. `src/api/` (Integrated in Production)**
- `cognitive_stack.py` - CognitiveStack class (1575 lines)
  - Integrates: LAB_001, LAB_002, LAB_003, LAB_004, LAB_006, LAB_007, LAB_008, LAB_010, LAB_011, LAB_013, LAB_014, LAB_015, LAB_051, LAB_052
- `consciousness_endpoints.py` - FastAPI endpoints for CognitiveStack (420 lines)
- `neuro_emotional_bridge.py` - Layer 2↔4 bridge (280 lines)

**3. `experiments/` (LAYER_* structure - 52 LABs registered)**
- `LAB_REGISTRY.json` - Source of truth (52 LABs total: 18 implemented, 34 designed)
- Layer-based organization:
  - LAYER_1_Memory_Substrate (foundation)
  - LAYER_2_Cognitive_Loop (8 LABs)
  - LAYER_3_Neurochemistry_Base (4 LABs)
  - LAYER_4_Neurochemistry_Full (5 LABs)
  - LAYER_5_Higher_Cognition (2 LABs: LAB_051 Hybrid Memory, LAB_052 Temporal Reasoning)

**4. Missing `features/` folder (Expected but not found)**
- CEREBRO_ANALYST detected references to:
  - `features/hybrid_memory/` (now LAB_051)
  - `features/temporal_reasoning/` (now LAB_052)
  - `features/intelligent_decay/` (now LAB_002/production_v2/)
  - `features/performance_optimization/` (now LAB_007/production/)

**Problem:** Same LAB code duplicated/referenced in multiple places, causing confusion about source of truth.

---

## 🎯 Target State (Unified)

### Single Source of Truth: `experiments/`

```
experiments/
├── LAB_REGISTRY.json                    # Master registry (52 LABs)
│
├── LAYER_1_Memory_Substrate/            # Foundation (PostgreSQL, Redis, Neo4j)
│   └── (no individual LABs, integrated in Layer 2+)
│
├── LAYER_2_Cognitive_Loop/              # 8 LABs
│   ├── LAB_001_emotional_salience/
│   ├── LAB_006_metacognition/
│   ├── LAB_007_predictive_preloading/
│   ├── LAB_008_emotional_contagion/
│   ├── LAB_009_memory_reconsolidation/
│   ├── LAB_010_attention_mechanism/
│   ├── LAB_011_working_memory/
│   └── LAB_012_episodic_future_thinking/
│
├── LAYER_3_Neurochemistry_Base/         # 4 LABs
│   ├── LAB_002_decay_modulation/
│   │   └── production_v2/               # Advanced decay (ex features/intelligent_decay)
│   ├── LAB_003_sleep_consolidation/
│   ├── LAB_004_curiosity_driven/
│   └── LAB_005_multimodal_memory/
│
├── LAYER_4_Neurochemistry_Full/         # 5 LABs
│   ├── LAB_013_dopamine/
│   ├── LAB_014_serotonin/
│   ├── LAB_015_norepinephrine/
│   ├── LAB_016_acetylcholine/
│   └── LAB_017_gaba/
│
├── LAYER_5_Higher_Cognition/            # 2 LABs
│   ├── LAB_051_hybrid_memory/           # (ex features/hybrid_memory)
│   └── LAB_052_temporal_reasoning/      # (ex features/temporal_reasoning)
│
├── INTEGRATION_LAYERS/                  # Production integrations
│   ├── cognitive_stack.py               # Full Stack (Layer 2+3+4+5) - 1575 lines
│   ├── neuro_emotional_bridge.py        # Layer 2↔4 bridge - 280 lines
│   └── consciousness_api.py             # FastAPI endpoints - 420 lines
│
└── tests/                               # All LAB tests
    ├── test_cognitive_stack.py          # 43 tests (100% passing)
    ├── test_neuro_emotional_bridge.py   # 19 tests (100% passing)
    └── test_consciousness_api.py        # 16 tests (100% passing)
```

**Key Principle:** `experiments/` is the LAB library, `src/api/` imports from it.

---

## 📋 Migration Plan

### Phase 1: Move Production Integrations (Session A)

**Actions:**
1. Move `src/api/cognitive_stack.py` → `experiments/INTEGRATION_LAYERS/cognitive_stack.py`
2. Move `src/api/neuro_emotional_bridge.py` → `experiments/INTEGRATION_LAYERS/neuro_emotional_bridge.py`
3. Move `src/api/consciousness_endpoints.py` → `experiments/INTEGRATION_LAYERS/consciousness_api.py`
4. Update imports in `src/api/main.py`:
   ```python
   # OLD:
   from src.api.cognitive_stack import CognitiveStack

   # NEW:
   from experiments.INTEGRATION_LAYERS.cognitive_stack import CognitiveStack
   ```

**Tests:**
- Run existing 78 tests to verify no regressions
- Update test imports if needed

**Output:**
- Production code moved to experiments/
- src/api/ becomes thin wrapper importing from experiments/

---

### Phase 2: Organize Individual LABs (Session B)

**Actions:**
1. Verify all LABs have consistent structure:
   ```
   experiments/LAYER_X/LAB_XXX_name/
   ├── README.md              # LAB description
   ├── implementation.py      # Core logic
   ├── tests/                 # LAB-specific tests
   └── examples/              # Usage examples
   ```

2. Move scattered LAB code into unified structure:
   - LAB_002/production_v2/ (already in place)
   - LAB_007/production/ (already in place)
   - LAB_051 (check if fully in experiments/)
   - LAB_052 (check if fully in experiments/)

3. Remove `features/` references (folder doesn't exist):
   - Update any lingering documentation pointing to features/

**Tests:**
- Import tests from each LAB directory
- Verify registry consistency

**Output:**
- All LABs follow same directory structure
- Zero references to non-existent features/ folder

---

### Phase 3: Update Documentation (Session C)

**Actions:**
1. Update `README.md`:
   - Clarify experiments/ is LAB library
   - Document import patterns
   - Update architecture diagram

2. Update `PROJECT_ID.md`:
   - Reflect new LAB organization
   - Update file tree structure

3. Update `CLAUDE.md`:
   - Document experiments/ as source of truth
   - Update LAB references

4. Update `LAB_REGISTRY.json`:
   - Add "location" field to each LAB
   - Verify 52 LABs metadata accurate

**Tests:**
- Documentation consistency check
- Link validation

**Output:**
- All documentation reflects unified structure
- New contributors can easily find LABs

---

### Phase 4: Validate & Cleanup (Session C cont.)

**Actions:**
1. Run full test suite:
   ```bash
   pytest tests/ -v
   pytest experiments/INTEGRATION_LAYERS/tests/ -v
   ```

2. Verify imports across codebase:
   ```bash
   grep -r "from src.api" src/ experiments/
   # Should find minimal references (only in main.py)
   ```

3. Remove duplicate/dead code:
   - Check for LAB code duplicated in multiple places
   - Archive old structure if needed

4. Update CI/CD if needed:
   - pytest paths
   - Import resolution

**Tests:**
- All 78+ tests passing
- No import errors
- API still functional

**Output:**
- Clean codebase
- Zero duplication
- Production-ready

---

## 🎯 Success Criteria

**Quantitative:**
- ✅ All 18 implemented LABs in experiments/ hierarchy
- ✅ Zero LAB code in src/api/ (only in experiments/)
- ✅ 100% test pass rate maintained
- ✅ LAB_REGISTRY.json accurate for all 52 LABs

**Qualitative:**
- ✅ Clear separation: experiments/ = LABs library, src/api/ = production wrapper
- ✅ Easy LAB discovery (consistent structure)
- ✅ Documentation matches reality
- ✅ New LABs can follow established pattern

---

## 🚨 Risks & Mitigation

**Risk 1: Breaking Production API**
- **Mitigation:** TDD approach - run tests after each move
- **Fallback:** Git revert if tests fail

**Risk 2: Import Path Confusion**
- **Mitigation:** Update all imports in single commit
- **Validation:** grep verification script

**Risk 3: Lost LAB Code**
- **Mitigation:** Git history preserves all moves
- **Backup:** Create branch before consolidation

**Risk 4: Documentation Drift**
- **Mitigation:** Update docs in same session as code moves
- **Validation:** Manual doc review

---

## 📊 Effort Estimate

| Phase | Tasks | Duration | Complexity |
|-------|-------|----------|------------|
| Phase 1: Move Integrations | 4 major moves | 1 session (2h) | Medium |
| Phase 2: Organize LABs | Verify structure | 1 session (2h) | Low |
| Phase 3: Update Docs | 4 doc files | 1 session (1h) | Low |
| Phase 4: Validate | Tests + cleanup | Same as Phase 3 | Low |
| **TOTAL** | **~10 tasks** | **2-3 sessions** | **Medium** |

---

## 🔄 Dependencies

**Prerequisite:**
- All current tests passing (✅ already true - 78/78)
- Git working tree clean (✅ will be after Session 16 commit)

**Blocks:**
- None (can start immediately after Session 16)

---

## 📅 Proposed Timeline

**Session 17 (Week of Nov 5-10):**
- Phase 1: Move production integrations to experiments/INTEGRATION_LAYERS/
- Phase 2: Verify LAB structure consistency

**Session 18 (Week of Nov 5-10):**
- Phase 3: Update all documentation
- Phase 4: Validate & cleanup

**Outcome:** Clean, unified LAB structure ready for scaling to 52 LABs.

---

## 📚 Related Documents

- `experiments/LAB_REGISTRY.json` - Source of truth for LAB metadata
- `README.md` - Project overview (update after consolidation)
- `PROJECT_ID.md` - System specification (update after consolidation)
- `docs/architecture/ARCHITECTURE_DIAGRAMS.md` - Architecture diagrams (update after consolidation)

---

## 🎓 Learnings from CEREBRO_ANALYST Audit

**Key Insight:** Scattered LAB code creates confusion about:
- Where to add new LABs
- Which version of a LAB is production
- How to import LAB functionality

**Solution:** Single source of truth (experiments/) with clear import pattern.

**Future Prevention:** Enforce pattern via documentation and code review.

---

**Status:** 📋 Ready for Execution
**Next Action:** Create Session 17 task with Phase 1 + 2
**Owner:** NEXUS (autonomous execution approved)

---

**Created by:** NEXUS + CEREBRO_ANALYST
**Session:** 16 (REC-007 implementation)
**Date:** November 5, 2025
