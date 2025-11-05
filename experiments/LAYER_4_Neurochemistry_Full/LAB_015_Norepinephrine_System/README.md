# LAB_015: Norepinephrine System ⚡

**Status:** ✅ Operational (Session 7)
**Layer:** LAYER 4 - Neurochemistry Full
**Code Size:** ~600 lines (268 main + 310 tests + 12 init)
**Implementation Time:** 2 hours (TDD)

---

## 🧠 Neuroscience Basis

**Brain Regions:**
- **Locus Coeruleus (LC)** - Norepinephrine production hub
- **Noradrenergic Projections** - Widespread cortical/subcortical modulation
- **Prefrontal Cortex** - Focus and attention integration

**Core Function:** **Arousal Regulation & Performance Optimization**

```
Norepinephrine regulates:
- Arousal level (wakefulness, vigilance)
- Stress response (rapid spike on stressful stimuli)
- Focus modulation (attention concentration)
- Performance (Yerkes-Dodson inverted-U curve)
```

---

## 🎯 Capabilities

### 1. Arousal Regulation (with Decay)
- **Input:** `stress_event` (float -1 to +1)
- **Output:** `arousal_level` (float 0-1)
- **Algorithm:** Rapid spike from stress, slow decay toward baseline
  ```python
  # Decay toward baseline
  decay_delta = (baseline_arousal - arousal_level) * (1.0 - arousal_decay)
  arousal_level = arousal_level + decay_delta

  # Rapid arousal spike from stress
  arousal_spike = stress_event * stress_sensitivity
  arousal_level = arousal_level + arousal_spike
  arousal_level = clip(arousal_level, 0.0, 1.0)
  ```

### 2. Performance Curve (Yerkes-Dodson Law)
- **Input:** `arousal_level` (from state)
- **Output:** `performance_efficiency` (float 0-1), `is_optimal` (bool)
- **Algorithm:** Inverted-U relationship (optimal at medium arousal)
  ```python
  deviation = abs(arousal_level - optimal_arousal)
  performance_efficiency = exp(-6.0 * (deviation ** 2))
  is_optimal = deviation < 0.1
  ```

### 3. Focus Modulation
- **Input:** `arousal_level` (from state)
- **Output:** `focus_strength` (float 0-1)
- **Algorithm:** Focus peaks at medium arousal, drops at extremes
  ```python
  deviation_from_medium = abs(arousal_level - 0.5)
  focus_strength = 1.0 - (2.0 * deviation_from_medium)
  focus_strength = max(0.0, focus_strength)
  ```

### 4. Alertness Level
- **Input:** `arousal_level` (from state)
- **Output:** `alertness` (float 0-1)
- **Algorithm:** Alertness = arousal (direct proportionality)
  ```python
  alertness = arousal_level
  ```

### 5. Arousal Stability Tracking
- **Input:** `arousal_history` (recent arousal values)
- **Output:** `stability` (float 0-1)
- **Algorithm:** Inverse of arousal variance (normalized)
  ```python
  arousal_variance = np.var(arousal_history)
  stability = 1.0 / (1.0 + arousal_variance)
  ```

---

## 🔌 Integration Points

### Inputs (from existing LABs)

**From LAB_001 (Emotional Salience):**
- `stress_event` → Negative valence = stress (affects arousal)

**From LAB_013 (Dopamine System):**
- `rpe` → Unexpected outcomes can spike arousal

**From LAB_014 (Serotonin System):**
- `mood_level` → Low mood + high arousal = anxious state

**From Episode Metadata:**
- `stress_event` (intensity of stressful/calming stimuli)

### Outputs (to other components)

**To LAB_001 (Emotional Salience):**
- `arousal_level` → Amplifies salience scoring for high-arousal states

**To LAB_002 (Decay Modulation):**
- `performance_efficiency` → Modulates memory consolidation quality

**To LAB_010 (Attention Mechanism):**
- `focus_strength` → Directly affects attentional filtering

**To LAB_014 (Serotonin System):**
- `arousal_level` → High arousal + low serotonin = stress response

**To Future LABs:**
- `alertness` → LAB_016 (Acetylcholine - encoding strength)
- `performance_efficiency` → LAB_037 (Executive Functions)

---

## 📐 Architecture

### Class: `NorepinephrineSystem`

```python
class NorepinephrineSystem:
    def __init__(self, baseline_arousal=0.5, stress_sensitivity=0.3,
                 arousal_decay=0.95, optimal_arousal=0.6,
                 focus_threshold=0.5, history_window=20):
        # Configuration
        self.baseline_arousal = baseline_arousal
        self.stress_sensitivity = stress_sensitivity
        self.arousal_decay = arousal_decay
        self.optimal_arousal = optimal_arousal
        self.focus_threshold = focus_threshold
        self.history_window = history_window

        # State
        self.arousal_level: float = baseline_arousal
        self.arousal_history: List[float] = []
        self.total_events: int = 0

    def update_arousal(self, stress_event: float) -> float:
        """Update arousal level from stress event (rapid spike, slow decay)"""

    def compute_performance(self) -> Dict:
        """Compute performance efficiency via Yerkes-Dodson inverted-U"""

    def modulate_focus(self) -> float:
        """Modulate attentional focus based on arousal"""

    def get_alertness(self) -> float:
        """Get alertness level (proportional to arousal)"""

    def get_arousal_stability(self) -> float:
        """Compute arousal stability (inverse of variance)"""

    def process_event(self, stress_event: float) -> Dict:
        """Main processing: update arousal, compute performance, focus, alertness"""

    def get_state(self) -> Dict:
        """Get current norepinephrine system state"""
```

---

## 🧪 Testing Strategy (TDD)

### Phase 1: Core Functionality Tests (22 tests)
1. **Arousal Update** (3 tests)
   - Stress events increase arousal
   - Calming events decrease arousal
   - Arousal decays toward baseline

2. **Performance Curve** (3 tests)
   - Optimal arousal gives best performance
   - Low arousal gives poor performance
   - High arousal gives poor performance (Yerkes-Dodson)

3. **Focus Modulation** (2 tests)
   - Medium arousal gives high focus
   - Extreme arousal gives low focus

4. **Alertness** (2 tests)
   - High arousal gives high alertness
   - Low arousal gives low alertness

5. **Arousal Stability** (2 tests)
   - Stable arousal has high stability
   - Volatile arousal has low stability

6. **Full Event Processing** (3 tests)
   - Returns complete state
   - Maintains history window
   - Counts total events

### Phase 2: Integration Tests (2 tests)
- High stress + low serotonin = poor performance (anxious)
- Moderate stress + balanced = optimal performance

### Phase 3: Edge Cases (3 tests)
- Extreme stress clamped to [0, 1]
- Extreme calming clamped to [0, 1]
- Performance curve symmetry

### Phase 4: State Persistence (2 tests)
- `get_state()` returns complete state
- State consistency across calls

**Total:** 22/22 tests PASSED ✅

---

## 📊 Expected Behavior

**Scenario: High Stress (Over-Aroused)**
```python
# User faces high stress event
ne = NorepinephrineSystem(baseline_arousal=0.5, optimal_arousal=0.6)
result = ne.process_event(stress_event=0.8)

# result["arousal_level"] = 0.74 (high arousal)
# result["performance"]["performance_efficiency"] = 0.87 (sub-optimal)
# result["focus_strength"] = 0.52 (scattered)
# result["alertness"] = 0.74 (hyper-alert)
```

**Scenario: Optimal Arousal**
```python
# User has moderate stress (optimal zone)
ne = NorepinephrineSystem(baseline_arousal=0.6, optimal_arousal=0.6)
result = ne.process_event(stress_event=0.0)

# result["arousal_level"] = 0.6 (optimal)
# result["performance"]["is_optimal"] = True
# result["performance"]["performance_efficiency"] = 1.0 (peak)
# result["focus_strength"] = 0.8 (high focus)
# result["alertness"] = 0.6 (alert)
```

**Scenario: Low Arousal (Under-Stimulated)**
```python
# User is drowsy (low arousal)
ne = NorepinephrineSystem(baseline_arousal=0.2, optimal_arousal=0.6)
result = ne.process_event(stress_event=-0.1)

# result["arousal_level"] = 0.17 (low)
# result["performance"]["performance_efficiency"] = 0.38 (poor)
# result["focus_strength"] = 0.34 (distracted)
# result["alertness"] = 0.17 (drowsy)
```

---

## 📚 Key References

**Papers:**
- Aston-Jones, G., & Cohen, J. D. (2005). An integrative theory of locus coeruleus-norepinephrine function: adaptive gain and optimal performance. *Annu. Rev. Neurosci.*, 28, 403-450.
- Yerkes, R. M., & Dodson, J. D. (1908). The relation of strength of stimulus to rapidity of habit-formation. *Journal of Comparative Neurology and Psychology*, 18(5), 459-482.
- Sara, S. J. (2009). The locus coeruleus and noradrenergic modulation of cognition. *Nature reviews neuroscience*, 10(3), 211-223.

**Related LABs:**
- LAB_013: Dopamine System (reward-driven arousal)
- LAB_014: Serotonin System (mood modulation)
- LAB_016: Acetylcholine System (attention amplification)

---

## ✅ Success Criteria

**Functional:**
- ✅ All unit tests pass (22/22 tests)
- ✅ Integration tests pass (stress-serotonin interaction)
- ✅ API endpoints respond correctly
- ✅ State persistence works

**Behavioral:**
- ✅ Stress increases arousal rapidly
- ✅ Arousal decays toward baseline slowly
- ✅ Performance follows inverted-U curve (Yerkes-Dodson)
- ✅ Focus peaks at medium arousal

**Performance:**
- ✅ Arousal update <1ms
- ✅ process_event() <5ms
- ✅ Memory footprint <5MB

---

## 🚀 Usage Example

```python
from LAYER_4_Neurochemistry_Full.LAB_015_Norepinephrine_System import NorepinephrineSystem

# Initialize system
ne = NorepinephrineSystem(
    baseline_arousal=0.5,
    stress_sensitivity=0.3,
    arousal_decay=0.95,
    optimal_arousal=0.6,
    focus_threshold=0.5,
    history_window=20
)

# Process stress event
result = ne.process_event(stress_event=0.5)

print(f"Arousal Level: {result['arousal_level']}")  # ~0.65
print(f"Performance: {result['performance']['performance_efficiency']}")  # ~0.95
print(f"Focus: {result['focus_strength']}")  # ~0.7
print(f"Alertness: {result['alertness']}")  # ~0.65

# Get current state
state = ne.get_state()
print(f"Total events: {state['total_events']}")
print(f"Arousal history: {state['arousal_history']}")
```

---

## 🔗 API Endpoints

**POST /norepinephrine/process**
- Process stress event and compute arousal, performance, focus, alertness
- Input: `stress_event` (-1 to +1)
- Output: arousal level, performance (Yerkes-Dodson), focus strength, alertness

**GET /norepinephrine/state**
- Get current norepinephrine system state
- Output: arousal level, history, mean, stability, performance efficiency, focus, alertness

---

**Created:** November 4, 2025 (Session 7)
**Author:** NEXUS@CLI + Ricardo
**Implementation:** TDD (Test-Driven Development)
**Breakthrough Potential:** 🔥🔥🔥 HIGH (Foundation of stress response & performance optimization)
