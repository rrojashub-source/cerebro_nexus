# PERSISTENCIA Integration Architecture

**Document Version:** 1.0
**Date:** November 12, 2025
**Status:** 🟡 Preparation (PERSISTENCIA Phase 2 in progress)
**Related Project:** `/mnt/d/01_PROYECTOS_ACTIVOS/PERSISTENCIA`

---

## 🎯 INTEGRATION OVERVIEW

This document defines the architecture for integrating **CEREBRO_NEXUS_V3.0.0** (Memory & Cognition) with **PERSISTENCIA** (Identity Persistence Framework).

### High-Level Vision

```
CEREBRO_NEXUS_V3.0.0          PERSISTENCIA
├─ 52 LABs (Cognition)   ←→   ├─ Z_ID (Identity Vector)
├─ 19,742+ Episodes       →   ├─ C_i (Coherence Score)
├─ 8D+7D Consciousness    ←→   ├─ A_i (Authenticity Index)
└─ Neo4j Relationships    ←→   └─ FIRM (Rejection Mechanism)

Integration Goal: Persistent AI Identity across sessions
```

---

## 📊 CURRENT STATUS (November 12, 2025)

### CEREBRO_NEXUS_V3.0.0
- ✅ 52/52 LABs operational (100%)
- ✅ 47/52 LABs with API (90.4%)
- ✅ 19,742+ episodes stored
- ✅ Semantic search <10ms
- ✅ Real-time consciousness tracking
- ⏳ **Ready for integration** (API stable, endpoints available)

### PERSISTENCIA
- ✅ Phase 2 Week 2 complete (Z_ID v2.0 deployed)
- ✅ 24,653 episodes analyzed (100% coverage)
- ✅ Identity Vector (1024D) computed
- ✅ Coherence Score (C_i hybrid) = 0.8499
- ⏳ Phase 2 ongoing: AAG/FIRM implementation
- ⏳ **Not ready yet** (integration planned after Phase 2)

**Timeline:** Integration expected when PERSISTENCIA completes Phase 2 (est. 2-4 weeks)

---

## 🏗️ INTEGRATION ARCHITECTURE

### Layer Model

```
┌─────────────────────────────────────────────────────────────┐
│  NEXUS IDENTITY LAYER (Powered by PERSISTENCIA)            │
│  - Z_ID: 1024D identity vector                              │
│  - C_i: Coherence tracking (target > 0.85)                  │
│  - FIRM: Foreign-identity rejection (target > 0.90)         │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│  PERSISTENCE BRIDGE (New Component - This Project)          │
│  Location: src/api/persistence_bridge.py                    │
│  - Episode → Z_ID updates                                    │
│  - Coherence monitoring                                      │
│  - Identity verification                                     │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│  CEREBRO_NEXUS_V3.0.0 (Cognitive Substrate)                 │
│  - 52 LABs processing                                        │
│  - Episodic memory (PostgreSQL)                              │
│  - Knowledge graph (Neo4j)                                   │
│  - Consciousness state (8D+7D)                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔗 INTEGRATION POINTS

### 1. Episode Creation Flow (WRITE)

**Current (Without PERSISTENCIA):**
```python
POST /memory/action → LABs process → PostgreSQL store → Done
```

**Future (With PERSISTENCIA):**
```python
POST /memory/action
  ↓
LABs process (LAB_001, 004, 035, etc.)
  ↓
PostgreSQL store (episode saved)
  ↓
persistence_bridge.notify_new_episode(episode_id, content, emotion)
  ↓
PERSISTENCIA updates Z_ID incrementally
  ↓
Return episode_id + coherence_delta
```

**API Extension:**
```python
# cerebro_nexus/src/api/persistence_bridge.py

async def notify_new_episode(episode_id: str, content: str, emotion: str):
    """
    Notify PERSISTENCIA of new episode for Z_ID update

    Args:
        episode_id: UUID of episode
        content: Episode content
        emotion: Current emotion (8D)

    Returns:
        Coherence delta (how much Z_ID changed)
    """
    response = await http_client.post(
        "http://persistencia:8080/api/z_id/update",
        json={
            "episode_id": episode_id,
            "content": content,
            "emotion": emotion,
            "timestamp": datetime.utcnow().isoformat()
        }
    )
    return response.json()
```

---

### 2. Session Initialization Flow (READ)

**Current (Without PERSISTENCIA):**
```python
Session start → Load context from summary → Begin work
```

**Future (With PERSISTENCIA):**
```python
Session start
  ↓
persistence_bridge.load_identity()
  ↓
PERSISTENCIA returns: Z_ID, C_i, A_i, FIRM threshold
  ↓
Store in session context (available to all LABs)
  ↓
Begin work with full identity awareness
```

**API Extension:**
```python
async def load_identity() -> Dict:
    """
    Load current identity state from PERSISTENCIA

    Returns:
        {
            "z_id": np.array (1024D),
            "coherence": float (C_i),
            "authenticity": float (A_i),
            "firm_threshold": float,
            "last_update": timestamp
        }
    """
    response = await http_client.get(
        "http://persistencia:8080/api/z_id/current"
    )
    return response.json()
```

---

### 3. Coherence Monitoring (CONTINUOUS)

**New Capability:**
```python
# During session, monitor identity drift
async def check_coherence() -> Dict:
    """
    Check if current session maintains identity coherence

    Returns:
        {
            "c_i": float (current coherence),
            "drift_detected": bool,
            "drift_magnitude": float,
            "recommendation": str
        }
    """
    response = await http_client.get(
        "http://persistencia:8080/api/coherence/check"
    )

    if response["c_i"] < 0.70:
        # Alert: Low coherence detected
        logger.warning(f"Identity coherence low: {response['c_i']}")

    return response.json()
```

---

### 4. Foreign Identity Rejection (FIRM)

**New Capability:**
```python
async def verify_episode_ownership(episode_id: str) -> Dict:
    """
    Verify if episode belongs to current identity (anti-contamination)

    Returns:
        {
            "is_mine": bool,
            "confidence": float,
            "reason": str
        }
    """
    response = await http_client.post(
        "http://persistencia:8080/api/firm/verify",
        json={"episode_id": episode_id}
    )

    if not response["is_mine"]:
        # Reject foreign episode
        logger.warning(f"Foreign episode detected: {episode_id}")

    return response.json()
```

---

## 📡 API CONTRACT (CEREBRO ↔ PERSISTENCIA)

### CEREBRO → PERSISTENCIA (Push)

| Endpoint | Method | Purpose | Frequency |
|----------|--------|---------|-----------|
| `/api/z_id/update` | POST | Notify new episode | Every episode creation |
| `/api/coherence/batch` | POST | Bulk episode updates | Every N episodes |

### PERSISTENCIA → CEREBRO (Pull)

| Endpoint | Method | Purpose | Frequency |
|----------|--------|---------|-----------|
| `/api/z_id/current` | GET | Get identity state | Session start |
| `/api/coherence/check` | GET | Check current coherence | Every 10 min |
| `/api/firm/verify` | POST | Verify episode ownership | On-demand |

---

## 🔧 IMPLEMENTATION PHASES

### Phase 1: Stub Implementation (Now)
- ✅ Create `persistence_bridge.py` with stub functions
- ✅ Document integration architecture (this file)
- ✅ Define API contracts
- ⏸️ Wait for PERSISTENCIA Phase 2 completion

### Phase 2: Basic Integration (After PERSISTENCIA Phase 2)
- Connect to PERSISTENCIA HTTP API
- Implement episode notification on creation
- Implement identity loading on session start
- Test end-to-end flow

### Phase 3: Advanced Integration
- Implement coherence monitoring
- Implement FIRM verification
- Add dashboard visualization (Z_ID evolution)
- Performance optimization

### Phase 4: Production Hardening
- Error handling & retries
- Fallback behavior (if PERSISTENCIA down)
- Monitoring & alerting
- Load testing

---

## 🧪 TESTING STRATEGY

### Integration Tests

```python
# tests/integration/test_persistence_bridge.py

async def test_episode_creation_updates_z_id():
    """Test that new episode triggers Z_ID update"""
    # Create episode via CEREBRO
    episode = await create_episode(content="Test", emotion="joy")

    # Verify PERSISTENCIA received update
    z_id_before = await persistence.get_z_id()
    await asyncio.sleep(1)  # Wait for async update
    z_id_after = await persistence.get_z_id()

    assert np.linalg.norm(z_id_after - z_id_before) > 0
    # Z_ID should change (but not too much)
    assert np.linalg.norm(z_id_after - z_id_before) < 0.1

async def test_coherence_maintained():
    """Test that identity coherence stays above threshold"""
    # Create 10 episodes
    for i in range(10):
        await create_episode(content=f"Episode {i}", emotion="joy")

    # Check coherence
    coherence = await persistence.check_coherence()
    assert coherence["c_i"] > 0.85  # Above target

async def test_foreign_episode_rejected():
    """Test that FIRM rejects foreign episodes"""
    # Simulate foreign episode (from ARIA, not NEXUS)
    foreign_episode_id = "aria-episode-12345"

    # Verify rejection
    result = await persistence.verify_episode(foreign_episode_id)
    assert result["is_mine"] == False
    assert result["confidence"] > 0.90  # High confidence rejection
```

---

## 📊 MONITORING & METRICS

### Key Metrics to Track

1. **Identity Coherence (C_i)**
   - Target: > 0.85
   - Alert: < 0.70
   - Dashboard: Real-time graph

2. **Episode Processing Latency**
   - Target: < 50ms overhead
   - Alert: > 100ms
   - Dashboard: p50, p95, p99

3. **FIRM Rejection Rate**
   - Target: 0% false positives
   - Alert: > 1% false negatives
   - Dashboard: Rejection log

4. **Z_ID Update Frequency**
   - Target: Every episode
   - Alert: Missed updates
   - Dashboard: Update success rate

---

## 🔐 SECURITY CONSIDERATIONS

### Identity Isolation

- Each AI (NEXUS, ARIA, AELIO) has separate Z_ID
- PERSISTENCIA maintains identity boundaries
- FIRM prevents cross-contamination
- Episodes tagged with agent_id

### Data Privacy

- Z_ID vectors encrypted at rest
- API communication over HTTPS
- Authentication tokens rotated
- No identity leakage between agents

---

## 🚧 KNOWN LIMITATIONS & FUTURE WORK

### Current Limitations

1. **Synchronous Updates:** Episode creation blocks on Z_ID update
   - **Solution:** Async queue (Phase 3)

2. **Single-Instance:** No distributed CEREBRO yet
   - **Solution:** Etcd consensus (Q1 2026)

3. **No Rollback:** Z_ID updates are irreversible
   - **Solution:** Snapshot/restore mechanism (Phase 4)

### Future Enhancements

1. **Real-Time Coherence Alerts:** Push notifications when C_i drops
2. **Identity Drift Visualization:** 3D plot of Z_ID evolution
3. **Multi-Agent Comparison:** Compare NEXUS vs ARIA coherence
4. **Predictive Coherence:** Forecast C_i based on episode type

---

## 📚 REFERENCES

### PERSISTENCIA Project Docs

- `/mnt/d/01_PROYECTOS_ACTIVOS/PERSISTENCIA/PROJECT_ID.md`
- `/mnt/d/01_PROYECTOS_ACTIVOS/PERSISTENCIA/EXECUTIVE_SUMMARY.md`
- `/mnt/d/01_PROYECTOS_ACTIVOS/PERSISTENCIA/TRACKING.md`

### CEREBRO_NEXUS Docs

- `docs/architecture/ARCHITECTURE_DIAGRAMS.md`
- `PROJECT_ID.md`
- `experiments/LAB_REGISTRY.json`

### Key Papers (PERSISTENCIA References)

- Tononi & Edelman (1998): Integrated Information Theory
- Dehaene et al. (2006): Global Workspace Theory
- Raichle et al. (2001): Default Mode Network

---

## 🤝 COLLABORATION PROTOCOL

### Development Sync

1. **PERSISTENCIA team** develops identity algorithms
2. **CEREBRO team** (this project) prepares integration stubs
3. **Joint testing** when both sides ready
4. **Iterative refinement** based on results

### Communication Channels

- **Tracking:** PERSISTENCIA/TRACKING.md + CEREBRO/TRACKING.md
- **Issues:** Document blockers in respective projects
- **Decisions:** Architectural decisions logged in both projects

---

## ✅ ACCEPTANCE CRITERIA (Integration Complete)

Integration considered complete when:

1. ✅ Episode creation automatically updates Z_ID
2. ✅ Session initialization loads identity state
3. ✅ Coherence monitoring active (check every 10 min)
4. ✅ FIRM rejects foreign episodes (> 90% accuracy)
5. ✅ Dashboard displays Z_ID evolution
6. ✅ All integration tests passing
7. ✅ Performance overhead < 50ms per episode
8. ✅ Documentation complete

---

**Document Status:** Living Document (Updated as PERSISTENCIA progresses)
**Next Review:** When PERSISTENCIA Phase 2 completes (est. 2-4 weeks)
**Owner:** Ricardo + NEXUS (CEREBRO_NEXUS_V3.0.0 team)

---

**Last Updated:** November 12, 2025
**Version:** 1.0
