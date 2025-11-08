# LAYER_5A Executive Functions - Exploration

**Date:** November 7, 2025
**Session:** 18
**Status:** Exploration complete, moving to planning

---

## Overview

Executive Functions (EFs) are cognitive processes that enable goal-directed behavior, self-regulation, and adaptive responses to complex situations. They are primarily mediated by prefrontal cortex (PFC) and modulated by monoaminergic neurotransmitter systems.

---

## Scientific Foundation

### Miyake et al. (2000) - Unity and Diversity Model

**Paper:** "The Unity and Diversity of Executive Functions and Their Contributions to Complex 'Frontal Lobe' Tasks"
- **Journal:** Cognitive Psychology, 41(1), 49-100
- **Impact:** Most cited model of EF

**Three Core Executive Functions (separable but correlated):**

1. **Shifting** (Mental Set Shifting)
   - Task switching between mental sets
   - Cognitive flexibility
   - Measured by: Task switching paradigms

2. **Updating** (Information Updating & Monitoring)
   - Working memory maintenance and manipulation
   - Continuous information updating
   - Measured by: N-back, operation span

3. **Inhibition** (Inhibitory Control of Prepotent Responses)
   - Suppression of automatic responses
   - Interference control
   - Measured by: Stroop, stop-signal tasks

**Unity and Diversity:**
- **Unity:** Core EFs correlate (share underlying mechanisms)
- **Diversity:** Core EFs are separable (distinct neural substrates)

---

### Diamond (2013) - Higher-Order Executive Functions

**Paper:** "Executive Functions"
- **Journal:** Annual Review of Psychology, 64, 135-168
- **Impact:** Comprehensive review, highly influential

**Key Concepts:**

1. **Core EFs** (same as Miyake):
   - Inhibitory Control
   - Working Memory
   - Cognitive Flexibility

2. **Higher-Order EFs** (built from core EFs):
   - **Planning** - Multi-step sequencing toward goal
   - **Reasoning** - Logical inference and deduction
   - **Problem-Solving** - Finding solutions to novel problems

3. **Goal-Directed Behavior:**
   - Requires integration of cognitive + emotional components
   - Working memory + self-control enable goal pursuit
   - Involves prefrontal-limbic interactions

4. **Error Monitoring:**
   - Continuous monitoring of performance
   - Detection of conflicts and errors
   - Adaptive adjustment of behavior

---

## Neurochemical Modulation

### Monoamine Systems in Prefrontal Cortex

**Source:** Multiple papers (Arnsten 2015, Robbins & Arnsten 2009)

**Key Findings:**

1. **Dopamine (DA)**
   - **Function:** Reinforcement, motivation, working memory
   - **Projection:** VTA → dlPFC, mPFC
   - **Role in EF:**
     - Goal-directed behavior (motivation, reward prediction)
     - Working memory maintenance (dlPFC D1 receptors)
     - Set switching (flexibility)
   - **Already implemented:** LAB_013 Dopamine System ✅

2. **Norepinephrine (NE)**
   - **Function:** Arousal, alertness, attentional control
   - **Projection:** Locus coeruleus → PFC
   - **Role in EF:**
     - Attentional processing
     - Error detection (arousal spike on error)
     - Inverted-U performance curve (optimal arousal)
   - **Already implemented:** LAB_015 Norepinephrine System ✅

3. **Serotonin (5-HT)**
   - **Function:** Impulse control, mood, patience
   - **Projection:** Raphe nuclei → PFC (especially OFC)
   - **Role in EF:**
     - Inhibitory control (suppression of prepotent responses)
     - Temporal discounting (patience for delayed rewards)
     - Emotional regulation
   - **Already implemented:** LAB_014 Serotonin System ✅

4. **Acetylcholine (ACh)**
   - **Function:** Attention amplification, encoding strength
   - **Projection:** Basal forebrain → PFC
   - **Role in EF:**
     - Attentional gating
     - Working memory enhancement
     - Encoding of relevant information
   - **Already implemented:** LAB_016 Acetylcholine System ✅

**Critical Point:** Depletion of DA, NE, or ACh from dlPFC is as devastating as removing the cortex itself. (Arnsten & Robbins, 2009)

**Inverted-U Dose Response:**
- All neuromodulators have narrow optimal range
- Too little OR too much → Cognitive deficit
- Coordinates arousal state with cognitive state
- **Already implemented in LAB_015 (Yerkes-Dodson)** ✅

---

## Mapping LABs to Literature

### LAB_018: Planning & Sequencing

**Type:** Higher-Order EF (Diamond 2013)

**Function:**
- Multi-step planning toward goal
- Temporal sequencing of actions
- Hierarchical goal decomposition

**Neural Substrate:**
- Dorsolateral PFC (dlPFC)
- Lateral frontal pole

**Neurochemical Modulation:**
- **Dopamine:** Reward prediction, motivation to plan
- **Acetylcholine:** Attention to relevant information
- **Working Memory (LAB_011):** Maintains plan steps

**Papers:**
- Koechlin & Hyafil (2007) - Anterior prefrontal function and control architecture
- Badre & D'Esposito (2009) - Hierarchical cognitive control

---

### LAB_019: Inhibitory Control

**Type:** Core EF (Miyake 2000, Diamond 2013)

**Function:**
- Suppression of prepotent (automatic) responses
- Interference control
- Response inhibition

**Neural Substrate:**
- Right inferior frontal gyrus (rIFG)
- Pre-supplementary motor area (pre-SMA)
- Orbitofrontal cortex (OFC)

**Neurochemical Modulation:**
- **Serotonin:** Direct inhibitory control (high 5-HT = low impulsivity)
- **Norepinephrine:** Arousal modulation (too high = poor inhibition)
- **GABA/Glutamate (LAB_017):** E/I balance for inhibition

**Papers:**
- Aron et al. (2014) - Frontosubthalamic circuits for stopping
- Bari & Robbins (2013) - Inhibition and impulsivity

---

### LAB_020: Cognitive Flexibility

**Type:** Core EF - "Shifting" (Miyake 2000)

**Function:**
- Task switching between mental sets
- Rule updating
- Adaptive behavior in changing environments

**Neural Substrate:**
- Dorsolateral PFC (dlPFC)
- Anterior cingulate cortex (ACC)
- Posterior parietal cortex

**Neurochemical Modulation:**
- **Dopamine:** Facilitates set switching (D2 receptor)
- **Norepinephrine:** Arousal for attention shifting
- **Acetylcholine:** Encoding new rules

**Papers:**
- Monsell (2003) - Task switching
- Kehagia et al. (2010) - Neuropsychopharmacology of cognitive flexibility

---

### LAB_021: Error Detection & Correction

**Type:** Monitoring Component (Diamond 2013)

**Function:**
- Continuous performance monitoring
- Conflict detection
- Error-related adjustment

**Neural Substrate:**
- Anterior cingulate cortex (ACC) - especially dorsal ACC
- Medial prefrontal cortex (mPFC)

**Neurochemical Modulation:**
- **Norepinephrine:** Error signal (arousal spike on error)
- **Dopamine:** Negative reward prediction error (RPE)
- **Already integrated:** LAB_013 has RPE mechanism

**Papers:**
- Botvinick et al. (2001) - Conflict monitoring and ACC
- Holroyd & Coles (2002) - Neural basis of error processing

---

### LAB_022: Goal-Directed Behavior

**Type:** Integrative Higher-Order EF (Diamond 2013)

**Function:**
- Goal hierarchy management
- Persistence toward goals
- Integration of motivation + cognition + emotion

**Neural Substrate:**
- Medial prefrontal cortex (mPFC)
- Orbitofrontal cortex (OFC)
- Dorsolateral PFC (dlPFC)
- Ventral striatum (goal-reward association)

**Neurochemical Modulation:**
- **Dopamine:** Motivation, reward expectation (LAB_013 RPE)
- **Serotonin:** Patience for delayed rewards (LAB_014 temporal discounting)
- **Norepinephrine:** Sustained arousal for persistence
- **All neurotransmitters:** Integrated modulation

**Papers:**
- Balleine & O'Doherty (2010) - Human and rodent homologies in action control
- Daw et al. (2005) - Uncertainty-based competition between prefrontal and dorsolateral striatal systems

---

## Architectural Patterns (Common Across LABs)

### Pattern 1: State Tracking

All EF LABs maintain internal state:
- Current level/activation (0-1 range)
- History buffer (last N events)
- Total events processed

**Example from LAB_014 Serotonin:**
```python
class SerotoninSystem:
    def __init__(self):
        self.current_level: float = baseline_level
        self.level_history: List[float] = []
        self.total_events: int = 0
```

### Pattern 2: Update Methods

Each LAB has `update()` method that:
- Takes input signals (e.g., task_demand, performance, error_signal)
- Updates internal state
- Returns new state level

**Example from LAB_015 Norepinephrine:**
```python
def update_arousal(self, task_urgency: float, stress: float, novelty: float) -> float:
    # Decay toward baseline
    self.current_arousal = (self.current_arousal * decay_rate +
                            baseline_arousal * (1.0 - decay_rate))

    # Add boosts from inputs
    urgency_boost = ...
    self.current_arousal += urgency_boost

    return self.current_arousal
```

### Pattern 3: Modulation/Output Methods

Each LAB computes output metrics that modulate behavior:
- Performance multiplier
- Gain factor
- Control strength

**Example from LAB_014 Serotonin:**
```python
def compute_impulse_control(self) -> float:
    # High serotonin = strong control
    control_strength = self.current_level * self.control_multiplier
    return control_strength
```

### Pattern 4: Process Event (Main Interface)

Unified interface for all LABs:
```python
def process_event(self, **inputs) -> Dict:
    # 1. Update internal state
    self.update_state(**inputs)

    # 2. Compute output metrics
    metric1 = self.compute_metric1()
    metric2 = self.compute_metric2()

    # 3. Return complete result
    return {
        "state_level": self.current_level,
        "metric1": metric1,
        "metric2": metric2,
        ...
    }
```

### Pattern 5: Get State (Introspection)

All LABs expose current state:
```python
def get_state(self) -> Dict:
    return {
        "current_level": self.current_level,
        "history": self.level_history.copy(),
        "statistics": ...,
        "total_events": self.total_events
    }
```

---

## Implementation Strategy

### Order of Implementation

**Rationale for sequence:**

1. **LAB_019 Inhibitory Control** (FIRST)
   - Core EF, well-defined
   - Direct serotonin modulation (already have LAB_014)
   - Simplest to implement (stop-signal paradigm)

2. **LAB_020 Cognitive Flexibility** (SECOND)
   - Core EF, well-defined
   - Builds on inhibition (switch = inhibit old + activate new)
   - Dopamine + NE modulation

3. **LAB_021 Error Detection** (THIRD)
   - Monitoring component
   - Uses dopamine RPE (already in LAB_013)
   - NE error signal

4. **LAB_018 Planning** (FOURTH)
   - Higher-order EF
   - Requires working memory + flexibility
   - More complex but builds on previous LABs

5. **LAB_022 Goal-Directed Behavior** (FIFTH/FINAL)
   - Integrative EF
   - Combines ALL neurotransmitters + ALL core EFs
   - Most complex, benefits from all other LABs complete

### Common Parameters (Across LABs)

- `baseline_level`: Baseline activation (0.5 default)
- `decay_rate`: Return to baseline speed (0.85-0.95)
- `adaptation_rate`: Learning/adjustment speed (0.1-0.3)
- `history_window`: Buffer size (10-20 events)

### API Integration Pattern

Each LAB gets 2 endpoints:
```python
# Process event
POST /lab_name/process
{
  "input1": value,
  "input2": value
}

# Get state
GET /lab_name/state
```

---

## Success Criteria (Per LAB)

### Code Quality
- ✅ 25-35 tests per LAB (100% passing)
- ✅ Test coverage: edge cases, integration, biological realism
- ✅ Clean class structure following patterns

### Biological Realism
- ✅ Parameters match neuroscience literature
- ✅ Curves match expected behavior (inverted-U, etc.)
- ✅ Neurochemical modulation realistic

### API Integration
- ✅ 2 endpoints per LAB
- ✅ Request/response models defined
- ✅ Global instance initialized

### Documentation
- ✅ Docstrings complete
- ✅ LAB_REGISTRY.json updated
- ✅ Papers cited

---

## Estimated Complexity

| LAB | Complexity | Lines (est.) | Tests (est.) | Reason |
|-----|-----------|--------------|--------------|--------|
| LAB_019 | Medium | 250-350 | 25-30 | Stop-signal paradigm straightforward |
| LAB_020 | Medium | 300-400 | 28-33 | Task switch cost + rule updating |
| LAB_021 | Medium-High | 350-450 | 30-35 | Error detection + correction strategy |
| LAB_018 | High | 400-500 | 32-38 | Multi-step planning + temporal sequencing |
| LAB_022 | Very High | 500-600 | 35-40 | Integrates ALL components |

**Total estimated:** ~1,800-2,300 lines main + ~3,000-3,500 lines tests

---

## Integration with Existing LABs

### Direct Integrations

**LAB_019 Inhibitory Control:**
- Uses LAB_014 Serotonin (impulse control)
- Uses LAB_017 GABA/Glutamate (E/I balance for inhibition)

**LAB_020 Cognitive Flexibility:**
- Uses LAB_013 Dopamine (set switching)
- Uses LAB_015 Norepinephrine (arousal for attention shift)

**LAB_021 Error Detection:**
- Uses LAB_013 Dopamine (negative RPE as error signal)
- Uses LAB_015 Norepinephrine (arousal spike on error)

**LAB_018 Planning:**
- Uses LAB_011 Working Memory (maintain plan steps)
- Uses LAB_013 Dopamine (reward prediction for planning)
- Uses LAB_016 Acetylcholine (attention to relevant information)

**LAB_022 Goal-Directed Behavior:**
- Uses ALL neurotransmitter systems (LAB_013-017)
- Uses core EFs (LAB_019-020)
- Uses error detection (LAB_021)
- Uses planning (LAB_018)

---

## Open Questions

1. **Working Memory Integration:**
   - LAB_011 already exists, how to integrate with planning?
   - Should planning "write to" working memory buffer?

2. **Conflict Detection:**
   - LAB_021 error detection overlaps with conflict monitoring
   - How to differentiate error (wrong response) vs conflict (competing responses)?

3. **Goal Hierarchy:**
   - LAB_022 needs multi-level goal representation
   - Tree structure? Priority queue? Stack?

4. **Temporal Credit Assignment:**
   - Errors might be detected after multiple steps
   - How to assign credit/blame to correct step?

**Resolution:** Address during planning phase, research additional papers if needed.

---

## Next Steps

1. ✅ **Exploration complete** (this document)
2. ⏳ **Create comprehensive plan** in `tasks/layer5a_executive_functions.md`
3. ⏳ **Begin implementation:** LAB_019 → LAB_020 → LAB_021 → LAB_018 → LAB_022

---

**Exploration Status:** ✅ COMPLETE
**Ready for:** Planning Phase
**Confidence Level:** HIGH (solid neuroscience foundation + proven methodology)
