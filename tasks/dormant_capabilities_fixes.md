# 🔧 Dormant Capabilities Fixes - Repair Plan

**Created:** November 4, 2025
**Status:** 🟡 In Progress
**Goal:** Fix bugs in 7 dormant capabilities discovered in Session 2
**Methodology:** NEXUS 4-Phase Workflow (TDD)

---

## 🎯 Overview

**Discovered:** 7 dormant capabilities in autodiscovery audit
**Tested:** November 4, 2025 (Session 2)
**Results:** 4/7 functional, 3/7 need fixes

---

## 🐛 Bugs Detected

### 🔴 CRITICAL (Broken)

#### 1. **Priming System** - Database Schema Bug
**Endpoint:** `POST /memory/prime/{uuid}`
**Error:** `relation "zep_episodic_memory" does not exist`
**Root Cause:** Using incorrect table name (zep_* prefix is old schema)
**Expected Table:** `episodic_memories` (current schema)
**Priority:** HIGH
**Estimated Time:** 30 min

**Fix Steps:**
1. Find priming endpoint code (likely in brain_orchestrator_v1.py or separate file)
2. Update SQL query from `zep_episodic_memory` to `episodic_memories`
3. Verify database credentials (nexus_user vs postgres)
4. Write test to verify priming works
5. Test with recent episode UUID

---

### 🟡 PARTIAL (Partially Broken)

#### 2. **Temporal Reasoning /range** - Null Response Bug
**Endpoint:** `POST /memory/temporal/range`
**Error:** Returns `{success: null, count: null, temporal_span: null}`
**Working:** `/before`, `/after`, `/related` work correctly
**Root Cause:** Likely missing response formatting or query bug
**Priority:** MEDIUM
**Estimated Time:** 20 min

**Fix Steps:**
1. Find temporal/range endpoint implementation
2. Compare with working `/before` and `/after` implementations
3. Fix response construction (ensure success, count, temporal_span populated)
4. Write test with valid time range
5. Verify query returns episodes correctly

---

#### 3. **Hybrid Memory /hybrid** - Null Response Bug
**Endpoint:** `POST /memory/hybrid`
**Error:** Returns `{success: null, episodes_count: 0, facts_count: 0}`
**Root Cause:** Likely not querying both episodic + facts tables correctly
**Priority:** MEDIUM
**Estimated Time:** 30 min

**Fix Steps:**
1. Find hybrid memory endpoint implementation
2. Verify facts table exists and has data
3. Fix query to combine episodic_memories + facts
4. Ensure response includes both episodes and facts arrays
5. Write test verifying hybrid search works

---

#### 4. **Hybrid Memory /facts** - Missing fact_type Parameter
**Endpoint:** `POST /memory/facts`
**Error:** `Field required: fact_type`
**Root Cause:** API expects fact_type but unclear what values are valid
**Priority:** LOW (needs documentation more than fix)
**Estimated Time:** 15 min

**Fix Steps:**
1. Find /facts endpoint implementation
2. Document valid fact_type values (e.g., "action", "state", "relationship")
3. Add example to API docs
4. Optional: Make fact_type optional with default "all"
5. Write test with each valid fact_type

---

### ❓ UNTESTED (Need Testing)

#### 5. **Memory Pruning** - Untested
**Endpoints:** `POST /memory/pruning/preview`, `POST /memory/pruning/execute`
**Status:** Not tested yet
**Priority:** LOW
**Estimated Time:** 20 min (test + potential fixes)

**Test Steps:**
1. Test `/pruning/preview` with decay threshold
2. Verify it returns list of episodes to prune (without deleting)
3. Test `/pruning/execute` (be careful - deletes data!)
4. Verify it only deletes low-importance old episodes
5. Write tests (mock execution, don't delete real data)

---

#### 6. **A/B Testing Framework** - Untested
**Endpoints:** `POST /ab-test/record`, `GET /ab-test/compare`
**Status:** Not tested yet
**Priority:** LOW
**Estimated Time:** 20 min (test + potential fixes)

**Test Steps:**
1. Test `/ab-test/record` with test_id, variant, outcome
2. Verify it stores A/B test results
3. Test `/ab-test/compare` with two variants
4. Verify it returns statistical comparison
5. Write tests for A/B framework

---

## ✅ Success Criteria

### Per Bug Fix:
- [ ] Bug identified and root cause understood
- [ ] Fix implemented with minimal changes
- [ ] Test written to verify fix works
- [ ] Test passes locally
- [ ] No regressions in existing tests
- [ ] Code reviewed (if complex)

### Overall:
- [ ] 3 critical bugs fixed (Priming, Temporal/range, Hybrid/hybrid)
- [ ] 1 documentation fix (Hybrid/facts)
- [ ] 2 capabilities tested (Pruning, A/B Testing)
- [ ] All tests pass
- [ ] TRACKING.md updated
- [ ] Git commit created

---

## 📊 Estimated Timeline

**Total Time:** ~2.5 hours

| Task | Time | Priority |
|------|------|----------|
| 1. Priming System fix | 30 min | HIGH |
| 2. Temporal /range fix | 20 min | MEDIUM |
| 3. Hybrid /hybrid fix | 30 min | MEDIUM |
| 4. Hybrid /facts docs | 15 min | LOW |
| 5. Pruning testing | 20 min | LOW |
| 6. A/B Testing testing | 20 min | LOW |
| 7. Integration tests | 15 min | - |
| **TOTAL** | **2h 30m** | - |

---

## 🧪 Test Strategy (TDD)

### For Each Fix:

**Red Phase:**
```python
# tests/test_dormant_capabilities.py

def test_priming_system_works():
    # Test priming endpoint with valid UUID
    response = client.post(f"/memory/prime/{valid_uuid}")
    assert response.status_code == 200
    assert response.json()["success"] == True
    # Should fail initially (table name bug)

def test_temporal_range_returns_episodes():
    # Test temporal range with valid time window
    response = client.post("/memory/temporal/range", json={
        "start_time": "2025-11-04T00:00:00Z",
        "end_time": "2025-11-04T23:59:59Z",
        "limit": 5
    })
    assert response.json()["success"] == True
    assert response.json()["count"] is not None
    # Should fail initially (null response bug)
```

**Green Phase:**
```python
# Fix implementation in src/api/
# Re-run tests → All pass ✅
```

**Refactor Phase:**
```python
# Optimize queries if needed
# Add error handling
# Re-run tests → Still pass ✅
```

---

## 📝 Implementation Notes

### Database Schema Reference:
```sql
-- Current schema (V2.0.0):
episodic_memories (uuid, content, created_at, importance_score, embedding)
facts (id, episode_id, fact_type, fact_content, extracted_at)
working_memory (episode_id, added_at, importance)
metacognition_log (action_id, action_type, confidence, timestamp)
```

### NOT using:
```sql
-- Old schema (legacy):
zep_episodic_memory  ❌ Don't use
zep_facts           ❌ Don't use
```

---

## 🔄 Rollback Plan

If fixes break existing functionality:
1. `git revert` the fix commit
2. Document issue in TRACKING.md
3. Mark capability as "needs redesign" in LAB_REGISTRY.json
4. Schedule for next session

---

## 📚 References

- **Autodiscovery Audit:** `docs/history/SESSION_20251104_autodiscovery_audit.md`
- **LAB_REGISTRY.json:** `experiments/LAB_REGISTRY.json`
- **V14.0 Awakening:** `~/.claude/identities/nexus.sh`
- **Database Schema:** `database/schema/episodic_memories.sql`

---

**Created:** November 4, 2025 (Session 2)
**Owner:** NEXUS + Ricardo
**Next:** FASE 3 - CODIFICAR (TDD)

---

**"Every bug fixed is a superpower unlocked."** 🔧🚀
