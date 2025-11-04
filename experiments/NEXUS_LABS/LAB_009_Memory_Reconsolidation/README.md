# 🔬 LAB_009: Memory Reconsolidation

**Status:** 🟡 In Progress
**Start Date:** October 28, 2025
**Researchers:** NEXUS (Autonomous)
**Priority:** HIGH
**Expected Duration:** 3 hours

---

## 🎯 Hypothesis

**Memories are NOT immutable - they evolve.**

When you retrieve an existing memory and encounter new related information, the memory should enter a **labile state** and **reconsolidate** by integrating the new context (not overwriting, integrating).

This allows memories to stay relevant and accurate as new information arrives.

---

## 🧠 Neuroscience Basis

### Memory Reconsolidation Theory

**Historical Foundation:**
- **Nader et al. (2000):** Memories become labile upon retrieval
- **Hardt et al. (2010):** Reconsolidation window (~6 hours)
- **Lee et al. (2017):** Updating, not overwriting

**Recent Research (2023-2025):**
- **Bayer et al. (2025):** "Windows of change" - temporal/molecular dynamics
- **Communications Biology (2023):** ERK pathway + noradrenergic system
- **Nature Reviews (2024):** Protein synthesis-dependent restabilization

### Core Mechanisms

```
Classic View (WRONG):
Memory Created → Stored Forever (immutable) → Retrieved

Reconsolidation View (CORRECT):
Memory Created → Stored → Retrieved + New Info → Labile State → Reconsolidate (Updated) → Stored (Modified)
                                          ↑
                                    6-hour window
```

**Key Insights:**
1. **Retrieval alone is NOT enough** - needs new related information (novelty detection)
2. **Labile window:** ~6 hours post-retrieval (after that, memory stable again)
3. **Process:** Destabilization (protein degradation) → Restabilization (protein synthesis)
4. **Result:** Integration (old + new), NOT replacement

### Biological Substrate

- **Hippocampus:** Memory reactivation + novelty detection
- **Protein synthesis:** Required for restabilization (ERK pathway)
- **Noradrenergic system:** Beta-adrenergic receptors modulate reconsolidation
- **Amygdala:** Emotional memories particularly susceptible

---

## 🔧 What We Already Have

### LAB_001-008: Retrieval Systems ✅
- Emotional salience, spreading activation, predictive preloading, emotional contagion
- All focused on **retrieving** existing memories
- Memories treated as immutable once stored

**Gap:** NO mechanism to UPDATE existing memories when new information arrives

---

## 🎯 What We're Building

### Memory Reconsolidation Engine

**Input:** Memory retrieval + new related information
**Process:** Detect novelty → Trigger labile state → Integrate new info → Reconsolidate
**Output:** Updated memory (not replaced, integrated)

### Architecture Components

#### 1. **ReconsolidationDetector**
```python
class ReconsolidationDetector:
    """Detect when retrieval + novelty co-occur"""

    def should_reconsolidate(
        self,
        retrieved_episode: Episode,
        current_context: Context
    ) -> Tuple[bool, float]:
        """
        Returns:
            (should_trigger, novelty_score)

        Conditions:
        1. Episode was recently retrieved (< 6 hours ago)
        2. Current context has NEW information semantically related
        3. Novelty score > threshold (not just minor variation)
        """
        pass
```

#### 2. **MemoryIntegrator**
```python
class MemoryIntegrator:
    """Integrate new information with existing memory"""

    def integrate(
        self,
        original_episode: Episode,
        new_information: Dict,
        integration_mode: str = "additive"  # additive, corrective, enrichment
    ) -> Episode:
        """
        Integration Modes:
        - additive: Add new details to existing memory
        - corrective: Update incorrect details
        - enrichment: Add context/metadata
        """
        pass
```

#### 3. **StabilityWindow**
```python
class StabilityWindow:
    """Track labile/stable states of memories"""

    def __init__(self, window_hours: float = 6.0):
        self.window_hours = window_hours
        self.labile_memories: Dict[str, datetime] = {}

    def enter_labile_state(self, episode_id: str):
        """Mark memory as labile (updatable)"""
        self.labile_memories[episode_id] = datetime.now()

    def is_labile(self, episode_id: str) -> bool:
        """Check if memory is still in labile window"""
        if episode_id not in self.labile_memories:
            return False

        elapsed = datetime.now() - self.labile_memories[episode_id]
        return elapsed.total_seconds() / 3600 < self.window_hours
```

#### 4. **UpdateLogger**
```python
class UpdateLogger:
    """Track all reconsolidation events"""

    def log_reconsolidation(
        self,
        episode_id: str,
        original_content: Dict,
        updated_content: Dict,
        integration_mode: str,
        novelty_score: float
    ):
        """
        Log what changed, why, when
        Enables auditing and rollback if needed
        """
        pass
```

---

## 📊 Success Metrics

### Quantitative

1. **Reconsolidation Trigger Rate**
   - Target: 5-10% of retrievals trigger reconsolidation
   - Measure: Too high = over-sensitive, too low = under-sensitive

2. **Update Quality**
   - Target: 80%+ of updates judged "improvement" (human eval)
   - Measure: Does updated memory contain more relevant info?

3. **Stability Preservation**
   - Target: 90%+ of non-labile memories unchanged
   - Measure: Memories outside window should NOT update

4. **Integration Accuracy**
   - Target: Original + New info both preserved (not replacement)
   - Measure: Check original content still present after update

### Qualitative

- Does memory "learn" from new experiences?
- Do debugging sessions accumulate knowledge?
- Do project memories evolve as project progresses?

---

## 🛠️ Implementation Plan

### Phase 1: Design (30 min) ✅
- [x] Neuroscience research
- [x] Architecture design
- [ ] Integration strategy with existing LABS

### Phase 2: Implementation (1.5 hours)
- [ ] ReconsolidationDetector class
- [ ] MemoryIntegrator class
- [ ] StabilityWindow class
- [ ] UpdateLogger class
- [ ] Main MemoryReconsolidationEngine orchestrator

### Phase 3: Testing (45 min)
- [ ] Test with simulated retrieval + new info scenarios
- [ ] Validate 6-hour stability window
- [ ] Check integration preserves original content
- [ ] Measure reconsolidation trigger rate

### Phase 4: Documentation (30 min)
- [ ] RESULTS.md
- [ ] Update PROJECT_ID + TRACKING
- [ ] Git commit

---

## 🔬 Research Questions

1. **What counts as "new information"?**
   - Semantic similarity threshold?
   - Contradiction detection (corrective mode)?
   - Pure addition vs correction vs enrichment?

2. **How aggressive should integration be?**
   - Conservative: Only add, never modify
   - Moderate: Add + enrich metadata
   - Aggressive: Correct contradictions

3. **Should ALL memories reconsolidate equally?**
   - Emotional memories more labile? (amygdala-dependent)
   - Recent memories easier to update?
   - Important memories protected?

4. **What about conflicting information?**
   - Keep both versions (uncertainty)?
   - Trust newer information?
   - Weight by source confidence?

---

## 💡 Expected Outcomes

### If Successful

**NEXUS memories become LIVING:**
- Debugging session accumulates learnings ("tried X, failed; tried Y, worked")
- Project memories update as project evolves
- Error patterns refined as more examples seen
- Knowledge graphs grow organically

**Example:**
```
Original Episode (Day 1):
"LAB_005 spreading activation - implemented, not tested"

After Reconsolidation (Day 2):
"LAB_005 spreading activation - implemented, TESTED (75.7% accuracy),
deployed with A/B testing framework, reduces latency by 55%"

After Reconsolidation (Day 3):
"LAB_005 spreading activation - implemented, tested (75.7%), deployed,
INTEGRATED with LAB_007 predictive preloading for unified anticipatory system"
```

Memory **evolves** with project reality.

### If Unsuccessful

- Learn that memory immutability is safer for AI (avoids corruption)
- Discover semantic novelty detection too hard
- Still valuable: Proves integration complexity requires more research

---

## 📚 References

### Neuroscience
- **Bayer et al. (2025)** - Windows of change (Neuroscience & Biobehavioral Reviews)
- **Nature Reviews (2024)** - Molecular mechanisms of reconsolidation
- **Communications Biology (2023)** - Modulation by adjacent novel tasks
- **Nader et al. (2000)** - Original reconsolidation discovery
- **Hardt et al. (2010)** - Reconsolidation window characterization

### AI/ML
- **MemoryBank (2024)** - Memory update with forgetting curve
- **Titans (2024)** - Test-time learning memory
- **ArXiv (2024)** - "From Human Memory to AI Memory" survey
- **ArXiv (2024)** - "Rethinking Memory in AI" taxonomy

---

## 🔗 Integration with Other LABS

### LAB_001-008: Retrieval Systems
- **Source:** All LABS retrieve memories
- **LAB_009 adds:** Update those memories when new info arrives

### LAB_001: Emotional Salience
- **Could combine:** Emotional memories more susceptible to reconsolidation
- **Enhancement:** Emotional events trigger stronger integration

### LAB_005: Spreading Activation
- **Could combine:** Related memories co-reconsolidate
- **Enhancement:** Update spreads to semantically related episodes

---

## ⚠️ Known Challenges

### 1. Novelty Detection
**Challenge:** What counts as "new" vs "slightly different"?
**Approach:** Semantic similarity threshold + contradiction detection

### 2. Integration Without Corruption
**Challenge:** How to add new info without destroying original?
**Approach:** Append-only mode first, then test corrective mode

### 3. Infinite Update Loops
**Challenge:** Update triggers retrieval → triggers update → ...
**Approach:** Stability window + cooldown period

### 4. Conflicting Information
**Challenge:** New info contradicts old - which to trust?
**Approach:** Keep both, flag as "conflicting versions", let user resolve

---

**Status:** Design complete, moving to implementation

**Next Step:** Implement ReconsolidationDetector + novelty scoring

---

**Created by:** NEXUS (Autonomous)
**Philosophy:** "Memories that learn are memories that live."
