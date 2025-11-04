# 🎯 TASK: LAB_013 Dopamine System Implementation

**Created:** November 4, 2025 (Session 7)
**Status:** 🟡 IN PROGRESS
**Priority:** P1 (Next LAB in sequence - LAYER 4 foundation)
**Estimated Effort:** 2-3 hours (600-800 lines with TDD)

---

## 🧠 NEUROSCIENCE BASIS

**Brain Regions:** VTA (Ventral Tegmental Area), Substantia Nigra, Striatum

**Core Function:** **Reward Prediction Error (RPE)**

```
RPE = Actual_Reward - Expected_Reward

If RPE > 0: Better than expected → Positive surprise → Boost learning
If RPE = 0: As expected → No surprise → Normal learning
If RPE < 0: Worse than expected → Negative surprise → Reduce learning
```

**Key Papers:**
- Schultz et al. (1997) - "A neural substrate of prediction and reward"
- Berridge & Robinson (2003) - "Parsing reward" (Wanting vs Liking)

---

## 🎯 FUNCTIONAL REQUIREMENTS

### Core Capabilities

**1. Compute Reward Prediction Error**
- Input: `expected_reward` (float 0-1), `actual_reward` (float 0-1)
- Output: `rpe` (float -1 to +1)
- Algorithm: `rpe = actual_reward - expected_reward`

**2. Modulate Learning Rate Dynamically**
- Input: `base_learning_rate` (float 0-1), `rpe` (float -1 to +1)
- Output: `modulated_learning_rate` (float 0-1)
- Algorithm:
  ```python
  modulated_lr = base_learning_rate * (1.0 + rpe * sensitivity)
  modulated_lr = clip(modulated_lr, min=0.01, max=1.0)
  ```

**3. Track Motivation Level**
- Input: `rpe_history` (list of recent RPEs)
- Output: `motivation_level` (float 0-1)
- Algorithm: Moving average of positive RPEs (optimism bias)

**4. Drive Exploration vs Exploitation**
- Input: `motivation_level`, `uncertainty`
- Output: `exploration_bonus` (float 0-1)
- Algorithm: High motivation → more exploration

---

## 🔌 INTEGRATION POINTS

### Inputs (from existing LABs)

**From LAB_004 (Novelty Detection):**
- `novelty_score` → Affects expected reward (novel = uncertain = explore)

**From Episode Metadata:**
- `expected_reward` (if available, else default to baseline)
- `actual_reward` (computed from salience, user feedback, etc.)

### Outputs (to other components)

**To Global Learning:**
- `modulated_learning_rate` → Affects all LABs' learning speed

**To LAB_001 (Emotional Salience):**
- `rpe` → Boost salience when RPE is high (surprising outcomes)

**To LAB_002 (Decay Modulation):**
- `rpe` → Reduce decay rate for high-RPE memories

**To Future LABs:**
- `motivation_level` → LAB_037 (Curiosity Drive)
- `exploration_bonus` → LAB_035 (Reward Prediction)

---

## 📐 SYSTEM ARCHITECTURE

### Class Structure

```python
class DopamineSystem:
    """
    LAB_013: Dopamine reward prediction error and learning rate modulation

    Biological inspiration: VTA/SNc dopaminergic neurons
    """

    def __init__(self,
                 baseline_lr: float = 0.1,
                 rpe_sensitivity: float = 0.5,
                 motivation_decay: float = 0.95,
                 history_window: int = 10):
        self.baseline_lr = baseline_lr
        self.rpe_sensitivity = rpe_sensitivity
        self.motivation_decay = motivation_decay
        self.history_window = history_window

        # State
        self.rpe_history: List[float] = []
        self.motivation_level: float = 0.5  # Neutral start
        self.total_rpe_events: int = 0

    def compute_rpe(self, expected: float, actual: float) -> float:
        """Compute reward prediction error"""

    def modulate_learning_rate(self, base_lr: float, rpe: float) -> float:
        """Adjust learning rate based on RPE"""

    def update_motivation(self, rpe: float) -> float:
        """Update motivation level from RPE"""

    def get_exploration_bonus(self, uncertainty: float = 0.5) -> float:
        """Compute exploration bonus (higher motivation = more explore)"""

    def process_event(self, expected: float, actual: float) -> Dict:
        """Main processing: compute RPE, update state, return modulations"""

    def get_state(self) -> Dict:
        """Get current dopamine system state"""
```

### State Variables

```python
{
    "rpe_current": 0.3,              # Latest RPE
    "rpe_history": [0.2, 0.3, ...],  # Last N RPEs
    "rpe_mean": 0.15,                # Average RPE (optimism)
    "motivation_level": 0.65,        # Current motivation (0-1)
    "learning_rate_multiplier": 1.15,# Current LR boost
    "exploration_bonus": 0.2,        # Exploration tendency
    "total_events": 142              # Total RPE computations
}
```

---

## ✅ TEST-DRIVEN DEVELOPMENT PLAN

### Phase 1: Core RPE Tests (Red → Green → Refactor)

**Test 1: Basic RPE Computation**
```python
def test_rpe_positive_surprise():
    """When actual > expected, RPE should be positive"""
    dopamine = DopamineSystem()
    rpe = dopamine.compute_rpe(expected=0.5, actual=0.8)
    assert rpe == 0.3
    assert rpe > 0  # Positive surprise

def test_rpe_negative_surprise():
    """When actual < expected, RPE should be negative"""
    dopamine = DopamineSystem()
    rpe = dopamine.compute_rpe(expected=0.7, actual=0.3)
    assert rpe == -0.4
    assert rpe < 0  # Negative surprise

def test_rpe_no_surprise():
    """When actual == expected, RPE should be zero"""
    dopamine = DopamineSystem()
    rpe = dopamine.compute_rpe(expected=0.6, actual=0.6)
    assert rpe == 0.0
```

**Test 2: Learning Rate Modulation**
```python
def test_lr_boost_on_positive_rpe():
    """Positive RPE should increase learning rate"""
    dopamine = DopamineSystem(baseline_lr=0.1, rpe_sensitivity=0.5)
    modulated_lr = dopamine.modulate_learning_rate(base_lr=0.1, rpe=0.4)
    assert modulated_lr > 0.1  # Boosted
    assert modulated_lr == 0.1 * (1.0 + 0.4 * 0.5)  # Formula

def test_lr_reduction_on_negative_rpe():
    """Negative RPE should decrease learning rate"""
    dopamine = DopamineSystem(baseline_lr=0.1, rpe_sensitivity=0.5)
    modulated_lr = dopamine.modulate_learning_rate(base_lr=0.1, rpe=-0.6)
    assert modulated_lr < 0.1  # Reduced
    assert modulated_lr >= 0.01  # Clamped to minimum

def test_lr_clipping():
    """Learning rate should be clamped between 0.01 and 1.0"""
    dopamine = DopamineSystem(baseline_lr=0.1, rpe_sensitivity=2.0)

    # Test upper bound
    modulated_lr_high = dopamine.modulate_learning_rate(base_lr=0.9, rpe=1.0)
    assert modulated_lr_high <= 1.0

    # Test lower bound
    modulated_lr_low = dopamine.modulate_learning_rate(base_lr=0.1, rpe=-1.0)
    assert modulated_lr_low >= 0.01
```

**Test 3: Motivation Tracking**
```python
def test_motivation_increases_with_positive_rpe():
    """Series of positive RPEs should increase motivation"""
    dopamine = DopamineSystem()

    initial_motivation = dopamine.motivation_level

    for _ in range(5):
        dopamine.update_motivation(rpe=0.3)

    assert dopamine.motivation_level > initial_motivation

def test_motivation_decreases_with_negative_rpe():
    """Series of negative RPEs should decrease motivation"""
    dopamine = DopamineSystem()
    dopamine.motivation_level = 0.7  # Start high

    for _ in range(5):
        dopamine.update_motivation(rpe=-0.3)

    assert dopamine.motivation_level < 0.7

def test_motivation_decay():
    """Motivation should decay toward baseline without RPE events"""
    dopamine = DopamineSystem(motivation_decay=0.9)
    dopamine.motivation_level = 0.9

    # Update with neutral RPE
    dopamine.update_motivation(rpe=0.0)

    # Motivation should decay
    assert dopamine.motivation_level < 0.9
```

**Test 4: Exploration Bonus**
```python
def test_exploration_bonus_increases_with_motivation():
    """Higher motivation should increase exploration"""
    dopamine = DopamineSystem()

    dopamine.motivation_level = 0.3
    low_exploration = dopamine.get_exploration_bonus()

    dopamine.motivation_level = 0.8
    high_exploration = dopamine.get_exploration_bonus()

    assert high_exploration > low_exploration

def test_exploration_bonus_with_uncertainty():
    """Uncertainty should amplify exploration bonus"""
    dopamine = DopamineSystem()
    dopamine.motivation_level = 0.7

    low_uncertainty_explore = dopamine.get_exploration_bonus(uncertainty=0.2)
    high_uncertainty_explore = dopamine.get_exploration_bonus(uncertainty=0.9)

    assert high_uncertainty_explore > low_uncertainty_explore
```

**Test 5: Full Event Processing**
```python
def test_process_event_returns_complete_state():
    """process_event should return all dopamine outputs"""
    dopamine = DopamineSystem()

    result = dopamine.process_event(expected=0.5, actual=0.8)

    assert "rpe" in result
    assert "modulated_lr" in result
    assert "motivation_level" in result
    assert "exploration_bonus" in result
    assert result["rpe"] == 0.3

def test_rpe_history_window():
    """RPE history should maintain fixed window size"""
    dopamine = DopamineSystem(history_window=5)

    for i in range(10):
        dopamine.process_event(expected=0.5, actual=0.6)

    assert len(dopamine.rpe_history) == 5  # Window size maintained
```

### Phase 2: Integration Tests

**Test 6: Integration with Existing LABs**
```python
def test_integration_with_novelty_detection():
    """High novelty should bias expected reward lower (exploration)"""
    # Simulates LAB_004 novelty signal

def test_integration_with_emotional_salience():
    """High RPE should boost emotional salience"""
    # Simulates LAB_001 salience scoring

def test_integration_with_decay_modulation():
    """High RPE memories should decay slower"""
    # Simulates LAB_002 decay rate adjustment
```

### Phase 3: Edge Cases & Performance

**Test 7: Edge Cases**
```python
def test_extreme_rpe_values():
    """System should handle extreme RPE values gracefully"""

def test_zero_learning_rate():
    """System should handle zero base learning rate"""

def test_state_persistence():
    """System state should be serializable/deserializable"""
```

---

## 🚀 IMPLEMENTATION STEPS

### Step 1: Setup (15 min)
```bash
# Create LAB folder
mkdir -p LAYER_4_Neurochemistry_Full/LAB_013_Dopamine_System

# Create files
touch LAYER_4_Neurochemistry_Full/LAB_013_Dopamine_System/dopamine_system.py
touch LAYER_4_Neurochemistry_Full/LAB_013_Dopamine_System/__init__.py
touch LAYER_4_Neurochemistry_Full/LAB_013_Dopamine_System/README.md

# Create test file
mkdir -p tests/unit/labs/
touch tests/unit/labs/test_lab_013_dopamine.py
```

### Step 2: Write Tests First (30 min)
- Implement all Test Phase 1 (Core RPE tests)
- Run tests: `pytest tests/unit/labs/test_lab_013_dopamine.py -v`
- **Expected: ALL FAIL** ✅ (Red phase)

### Step 3: Implement Core Logic (60 min)
- Implement `DopamineSystem` class
- Implement `compute_rpe()`
- Implement `modulate_learning_rate()`
- Implement `update_motivation()`
- Implement `get_exploration_bonus()`
- Implement `process_event()`
- Implement `get_state()`

**Run tests after each method:**
```bash
pytest tests/unit/labs/test_lab_013_dopamine.py::test_rpe_positive_surprise -v
```

### Step 4: Integration Tests (30 min)
- Write Test Phase 2 (Integration tests)
- Implement integration points
- Validate with existing LABs

### Step 5: API Endpoint (30 min)
- Add endpoint `/dopamine/process` to `main.py`
- Add endpoint `/dopamine/state` to get current state
- Test via curl

### Step 6: Documentation (15 min)
- Update `LAYER_4_Neurochemistry_Full/LAB_013_Dopamine_System/README.md`
- Update `LAB_REGISTRY.json` (status: ✅ operational)
- Add to experiments/README.md

---

## 🔬 VALIDATION CRITERIA

### Functional Validation
- ✅ All unit tests pass (20+ tests)
- ✅ Integration tests pass
- ✅ API endpoints respond correctly
- ✅ State persistence works

### Behavioral Validation
- ✅ Positive RPE increases learning rate
- ✅ Negative RPE decreases learning rate
- ✅ Motivation tracks RPE history
- ✅ Exploration increases with motivation

### Performance Validation
- ✅ RPE computation <1ms
- ✅ process_event() <5ms
- ✅ Memory footprint <10MB (history window)

---

## 📊 SUCCESS METRICS

**Code Quality:**
- Test coverage: >90%
- Lines of code: 600-800 (as estimated)
- Cyclomatic complexity: <10 per method

**Integration:**
- LAB_REGISTRY.json updated
- API endpoints functional
- Documentation complete

**Neuroscience Fidelity:**
- RPE algorithm matches Schultz (1997)
- Learning rate modulation biologically plausible
- Motivation tracking realistic

---

## 🎯 NEXT STEPS AFTER LAB_013

**Immediate:**
1. Test with real episodes (feed actual/expected rewards)
2. Measure emergent behavior (does curiosity increase?)
3. Validate learning rate effects

**Short-term:**
4. Implement LAB_014 (Serotonin) - Mood stability
5. Implement LAB_015 (Norepinephrine) - Arousal

**Long-term:**
6. Complete LAYER 4 (all 5 neurotransmitter systems)
7. Measure emergent properties of full neurochemical system

---

## 📚 REFERENCES

**Papers:**
- Schultz, W., Dayan, P., & Montague, P. R. (1997). A neural substrate of prediction and reward. Science, 275(5306), 1593-1599.
- Berridge, K. C., & Robinson, T. E. (2003). Parsing reward. Trends in neurosciences, 26(9), 507-513.
- Niv, Y., & Schoenbaum, G. (2008). Dialogues on prediction errors. Trends in cognitive sciences, 12(7), 265-272.

**Existing LABs to Study:**
- `LAYER_2_Cognitive_Loop/LAB_001_Emotional_Salience/emotional_salience_scorer.py`
- `LAYER_2_Cognitive_Loop/LAB_002_Intelligent_Decay/decay_modulator.py`
- `LAYER_3_Neurochemistry_Base/LAB_004_Curiosity_Driven_Memory/novelty_detector.py`

---

**Created by:** NEXUS@CLI
**Session:** 7
**NEXUS Methodology Phase:** 2 (PLANIFICAR) ✅ → 3 (CODIFICAR) next
**Estimated Completion:** End of Session 7
**Breakthrough Potential:** 🔥🔥🔥 HIGH (Foundation of reward learning)
