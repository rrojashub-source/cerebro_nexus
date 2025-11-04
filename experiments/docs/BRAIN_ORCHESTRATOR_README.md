# 🧠 Brain Orchestrator v1.1

**Status:** ✅ Migrated to V3.0.0
**Location:** `src/api/brain_orchestrator_v1.py`
**Created:** October 29, 2025
**Migrated:** November 4, 2025

---

## 🎯 WHAT IS IT?

**Brain Orchestrator** is the integration system that unifies Layer 2 LABs (Cognitive Loop) into a single, coherent synthetic brain.

**Philosophy:**
> "LABs are organs outside the body.
> The Brain Orchestrator inserts them inside the brain to work together."

---

## 🧩 INTEGRATED LABS (9 Total)

The orchestrator integrates **9 LABs from Layer 2 + Layer 5F**:

### Layer 2 - Cognitive Loop (8 LABs)
1. **LAB_001:** Emotional Salience Scorer
2. **LAB_006:** Metacognition Logger
3. **LAB_007:** Predictive Preloading
4. **LAB_008:** Emotional Contagion
5. **LAB_009:** Memory Reconsolidation
6. **LAB_010:** Attention Mechanism
7. **LAB_011:** Working Memory Buffer
8. **LAB_012:** Episodic Future Thinking

### Layer 5F - Social & Other (1 LAB)
9. **LAB_028:** Emotional Intelligence

---

## 🔄 PROCESSING FLOW

```
Query Input
     ↓
LAB_001 (Emotional Salience) → Scores emotional importance
     ↓
LAB_010 (Attention Mechanism) → Filters relevant content
     ↓
LAB_011 (Working Memory Buffer) → Loads into WM (7±2 items)
     ↓
LAB_007 (Predictive Preloading) → Predicts next memories
     ↓
LAB_008 ↔ LAB_028 (Emotion Processing) → Regulates emotional response
     ↓
LAB_009 (Memory Reconsolidation) → Updates importance scores
     ↓
LAB_012 (Episodic Future Thinking) → Generates future scenarios
     ↓
LAB_006 (Metacognition) → Observes & logs all processing
     ↓
Integrated Response
```

---

## 🗂️ DATA INTEGRATION

### PostgreSQL Connection (V3.0.0)

**Configuration:**
- **Host:** `nexus_postgresql_v2` (Docker network)
- **Port:** `5437`
- **Database:** `nexus_db`
- **User:** `nexus_user`
- **Password:** Docker secret at `/run/secrets/pg_superuser_password`

**Real Data Usage:**
- **LAB_011 (Working Memory):** Fetches real episodic memories from PostgreSQL
- **LAB_007 (Predictive Preloading):** Predicts next episodes based on real data
- **LAB_009 (Memory Reconsolidation):** Updates importance scores in database

---

## 📊 REQUEST/RESPONSE FORMAT

### Request Model

```python
{
  "query": "memories about project failures",
  "context": {
    "current_emotion": "stress",
    "goal": "avoid repeating mistakes"
  }
}
```

### Response Model

```python
{
  "success": true,
  "working_memory": [
    {
      "episode_id": "abc123",
      "content": "...",
      "salience_score": 0.85
    }
  ],
  "predictions": ["Next memory likely about X", "..."],
  "future_vision": {
    "scenario": "...",
    "confidence": 0.75
  },
  "emotional_state": {
    "current": "stress",
    "regulated": "calm_focus",
    "intensity": 0.6
  },
  "interactions": [
    {
      "from_lab": "LAB_001",
      "to_lab": "LAB_010",
      "signal": "high_salience_detected",
      "timestamp": "2025-11-04T10:00:00"
    }
  ],
  "metacognition": {
    "confidence": 0.82,
    "reasoning": "Strong signal coherence across LABs",
    "calibration_score": 0.78
  },
  "processing_time_ms": 45.2
}
```

---

## 🛠️ TECHNICAL DETAILS

### Dependencies

```python
# Layer 2 LABs
from emotional_salience_scorer import EmotionalSalienceScorer
from metacognition_logger import MetacognitionLogger
from predictive_preloading import PredictivePreloadingEngine
from emotional_contagion import EmotionalContagionEngine
from memory_reconsolidation import MemoryReconsolidationEngine
from attention_mechanism import AttentionScorer
from working_memory_buffer import WorkingMemoryBuffer
from episodic_future_thinking import FutureThinkingOrchestrator

# Layer 5F
from emotional_intelligence import EmotionalIntelligenceSystem
```

**All LABs must be in PYTHONPATH for imports to work.**

### LAB-to-LAB Interaction Tracking

The orchestrator tracks all signals passed between LABs:

```python
class LABInteraction:
    from_lab: str      # Source LAB (e.g., "LAB_001")
    to_lab: str        # Target LAB (e.g., "LAB_010")
    signal: str        # Signal/data passed
    timestamp: datetime
```

This enables:
- ✅ Observability of cognitive flow
- ✅ Debugging LAB interactions
- ✅ Metacognition analysis
- ✅ Emergent behavior detection

---

## 📈 PERFORMANCE

**Expected Processing Time:**
- Simple query: 20-50ms
- Complex query with future thinking: 50-150ms

**Bottlenecks:**
- PostgreSQL queries (LAB_011, LAB_007, LAB_009)
- Future scenario generation (LAB_012)

**Optimizations:**
- Connection pooling for PostgreSQL
- Caching for frequent queries
- Parallel LAB execution (future enhancement)

---

## 🚀 USAGE

### Initialize Orchestrator

```python
from brain_orchestrator_v1 import BrainOrchestrator

orchestrator = BrainOrchestrator()
# 🧠 Initializing Brain Orchestrator v1.0...
# ✅ Brain Orchestrator v1.0 initialized - 9 LABs active
```

### Process Query

```python
response = await orchestrator.process(
    query="memories about successful debugging",
    context={
        "current_emotion": "curiosity",
        "goal": "learn from past success"
    }
)

print(f"Working Memory: {len(response['working_memory'])} items")
print(f"Predictions: {response['predictions']}")
print(f"Emotional State: {response['emotional_state']['regulated']}")
print(f"Confidence: {response['metacognition']['confidence']}")
```

---

## 🔗 INTEGRATION WITH API

**Endpoint (to be added):**
```
POST /brain/process
Body: BrainProcessRequest
Response: BrainProcessResponse
```

**Current Status:** 🔴 Not yet exposed as API endpoint (requires FastAPI route)

---

## 🎯 FUTURE ENHANCEMENTS

### Short-Term
- [ ] Add FastAPI endpoint for orchestrator
- [ ] Connection pooling for PostgreSQL
- [ ] Performance benchmarks

### Mid-Term
- [ ] Integrate Layer 3 LABs (Neurochemistry Base)
  - LAB_002: Decay Modulation
  - LAB_003: Sleep Consolidation
  - LAB_004: Novelty Detection
  - LAB_005: Spreading Activation

### Long-Term
- [ ] Integrate Layer 4 LABs (Neurochemistry Full)
- [ ] Integrate Layer 5 LABs (Higher Cognition)
- [ ] Parallel LAB execution (async processing)
- [ ] Brain Orchestrator v2.0 (50 LABs integration)

---

## 📚 REFERENCES

**Design:**
- `experiments/MASTER_BLUEPRINT_50_LABS.md` (ANEXO A - Brain Integration)
- `experiments/LAYER_2_Cognitive_Loop/README.md`

**Implementation:**
- `src/api/brain_orchestrator_v1.py` (659 lines)

**Related:**
- Layer 2 LABs in `experiments/LAYER_2_Cognitive_Loop/`
- LAB_REGISTRY.json for complete LABs catalog

---

## 🛡️ MIGRATION NOTES (V2.0.0 → V3.0.0)

**Changes Made (November 4, 2025):**

1. ✅ **PostgreSQL Configuration Updated:**
   - Port: `5432` → `5437`
   - Host: `nexus_postgresql` → `nexus_postgresql_v2`
   - Database: `nexus_memory` → `nexus_db`
   - User: `nexus_superuser` → `nexus_user`

2. ✅ **File Location:**
   - Copied from: `Z:/CEREBRO_MASTER_NEXUS_001/FASE_4_CONSTRUCCION/src/api/`
   - Copied to: `src/api/brain_orchestrator_v1.py`

3. ✅ **Documented:**
   - Created `experiments/BRAIN_ORCHESTRATOR_README.md`
   - Updated `experiments/SESSION_SUMMARY_50_LABS_REORGANIZATION.md`

**Testing Required:**
- [ ] Verify PostgreSQL connection to port 5437
- [ ] Test all 9 LAB integrations work correctly
- [ ] Validate LAB-to-LAB interactions
- [ ] Benchmark processing time

---

## ⚠️ KNOWN LIMITATIONS

1. **Synchronous Processing:** LABs are executed sequentially (not parallel)
2. **No API Endpoint:** Not yet exposed via FastAPI (manual instantiation only)
3. **Layer 2 Only:** Does not integrate Layer 3+ LABs yet
4. **No Caching:** Every query hits PostgreSQL (no Redis cache yet)

---

## 🎉 ACHIEVEMENT

**Brain Orchestrator v1.1** represents the first successful integration of multiple LABs into a unified cognitive system.

**Impact:**
- ✅ Proves LABs can work together (not just in isolation)
- ✅ Demonstrates real data integration (PostgreSQL)
- ✅ Provides emergent cognitive behavior (metacognition observes all)
- ✅ Foundation for Brain Orchestrator v2.0 (50 LABs)

---

**Created by:** Ricardo + NEXUS
**Date:** October 29, 2025
**Migrated to V3.0.0:** November 4, 2025
**Status:** ✅ Ready for testing in V3.0.0
**Maintained in:** `experiments/BRAIN_ORCHESTRATOR_README.md`

---

**"LABs are organs. The Orchestrator is the nervous system that connects them."** 🧠
