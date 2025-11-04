# Layer 2: Cognitive Loop

**Status:** ✅ Operational (8/8 LABs)
**Implementation Date:** October 27-29, 2025
**Purpose:** Core cognitive functions (Attention, Memory, Emotion, Metacognition)

---

## Overview

Layer 2 implements the **core cognitive loop** - the fundamental processes that enable memory formation, attention, emotional processing, and self-awareness.

**Biological Inspiration:** Prefrontal cortex + Hippocampus + Amygdala + Parietal networks

---

## LABs (8 Total)

### LAB_001: Emotional Salience Scorer ✅
- **Function:** Calculates emotional importance for memory formation
- **Neuroscience:** Amygdala + medial prefrontal cortex
- **Code:** 15K lines (`emotional_salience_scorer.py`)
- **Output:** Salience score (0.0-1.0)
- **Integration:** Feeds into LAB_010 (Attention), LAB_002 (Decay)

### LAB_006: Metacognition Logger ✅
- **Function:** Self-awareness, confidence calibration, error detection
- **Neuroscience:** Lateral prefrontal cortex, ACC (Anterior Cingulate Cortex)
- **Code:** 16K lines (`metacognition_logger.py`)
- **Output:** ECE score (Expected Calibration Error), confidence metrics
- **Integration:** Observes all other LABs

### LAB_007: Predictive Preloading ✅
- **Function:** Anticipates future queries based on patterns
- **Neuroscience:** Dorsolateral prefrontal cortex, hippocampus
- **Code:** 23K lines (`predictive_preloading.py`)
- **Output:** Predicted queries, preload candidates
- **Integration:** Optimizes memory retrieval

### LAB_008: Emotional Contagion ✅
- **Function:** Spreads emotional context between related memories
- **Neuroscience:** Mirror neurons, insula, amygdala
- **Code:** 15K lines (`emotional_contagion.py`)
- **Output:** Emotional valence propagation
- **Integration:** ← LAB_001, → Memory graph

### LAB_009: Memory Reconsolidation ✅
- **Function:** Updates memories when recalled (update-on-recall)
- **Neuroscience:** Hippocampal reconsolidation, protein synthesis
- **Code:** 21K lines (`memory_reconsolidation.py`)
- **Output:** Updated memory traces
- **Integration:** Modifies episodes on retrieval

### LAB_010: Attention Mechanism ✅
- **Function:** Selective attention based on salience, recency, context
- **Neuroscience:** Pulvinar, superior colliculus, parietal cortex
- **Code:** 16K lines (`attention_mechanism.py`)
- **Output:** Filtered & ranked memories
- **Integration:** ← LAB_001 (salience), ← LAB_011 (working memory)

### LAB_011: Working Memory Buffer ✅
- **Function:** 7-item buffer (Miller's Law), HYBRID eviction
- **Neuroscience:** Prefrontal cortex, dorsolateral PFC
- **Code:** 17K lines (`working_memory_buffer.py`)
- **Output:** Active buffer items (7±2)
- **Integration:** → LAB_010 (provides context for attention)

### LAB_012: Episodic Future Thinking ✅
- **Function:** Simulates future scenarios based on past episodes
- **Neuroscience:** Hippocampus, default mode network
- **Code:** 18K lines (`episodic_future_thinking.py`)
- **Output:** Simulated future scenarios with confidence
- **Integration:** ← LAB_009 (episodic memory), → Planning

---

## Total Code

**141K lines** across 8 LABs

---

## Cognitive Loop Flow

```
User Query
    ↓
LAB_001 (Emotional Salience) → Score emotional importance
    ↓
LAB_010 (Attention) → Filter & rank candidates
    ↓
LAB_011 (Working Memory) → Keep 7±2 items in buffer
    ↓
LAB_009 (Reconsolidation) → Update memories on recall
    ↓
LAB_007 (Predictive Preload) → Anticipate next queries
    ↓
LAB_012 (Future Thinking) → Simulate future scenarios
    ↑
LAB_006 (Metacognition) → Monitor all processes
    ↑
LAB_008 (Emotional Contagion) → Spread emotional context
```

---

## API Endpoints

All 8 LABs exposed via FastAPI (port 8003):

- `/memory/search` - Uses LAB_010 attention
- `/memory/working` - LAB_011 buffer operations
- `/metacognition/*` - LAB_006 endpoints
- `/memory/reconsolidate` - LAB_009 update
- `/predict/*` - LAB_007 predictions
- `/future/*` - LAB_012 scenarios
- `/emotion/*` - LAB_001, LAB_008 emotion ops

---

## Performance

| Metric | Value |
|--------|-------|
| **Total LABs** | 8/8 ✅ |
| **Integration** | 100% |
| **Avg overhead** | <50ms |
| **API response** | 7-10ms |

---

## Key Papers

- McGaugh (2004) - Memory consolidation and amygdala
- Phelps (2004) - Emotion and cognition
- Tulving (2002) - Episodic memory
- Schacter & Addis (2007) - Future thinking
- Fleming & Dolan (2012) - Metacognition

---

**Maintained by:** Ricardo + NEXUS
**Status:** ✅ Production
