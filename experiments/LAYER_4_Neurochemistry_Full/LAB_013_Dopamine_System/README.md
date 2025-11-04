# LAB_013: Dopamine System 🎯

**Status:** 🟡 In Implementation (Session 7)
**Layer:** LAYER 4 - Neurochemistry Full
**Estimated Code:** 600-800 lines
**Implementation Time:** 2-3 hours (TDD)

---

## 🧠 Neuroscience Basis

**Brain Regions:**
- **VTA (Ventral Tegmental Area)** - Reward processing hub
- **Substantia Nigra** - Dopamine production
- **Striatum** - Learning & motivation integration

**Core Function:** **Reward Prediction Error (RPE)**

```
RPE = Actual_Reward - Expected_Reward

If RPE > 0: Better than expected → Positive surprise → Boost learning
If RPE = 0: As expected → No surprise → Normal learning
If RPE < 0: Worse than expected → Negative surprise → Reduce learning
```

---

## 🎯 Capabilities

### 1. Compute Reward Prediction Error
- **Input:** `expected_reward` (float 0-1), `actual_reward` (float 0-1)
- **Output:** `rpe` (float -1 to +1)
- **Algorithm:** `rpe = actual_reward - expected_reward`

### 2. Modulate Learning Rate Dynamically
- **Input:** `base_learning_rate` (float 0-1), `rpe` (float -1 to +1)
- **Output:** `modulated_learning_rate` (float 0-1)
- **Algorithm:**
  ```python
  modulated_lr = base_learning_rate * (1.0 + rpe * sensitivity)
  modulated_lr = clip(modulated_lr, min=0.01, max=1.0)
  ```

### 3. Track Motivation Level
- **Input:** `rpe_history` (list of recent RPEs)
- **Output:** `motivation_level` (float 0-1)
- **Algorithm:** Moving average of positive RPEs (optimism bias)

### 4. Drive Exploration vs Exploitation
- **Input:** `motivation_level`, `uncertainty`
- **Output:** `exploration_bonus` (float 0-1)
- **Algorithm:** High motivation → more exploration

---

## 🔌 Integration Points

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

## 📐 Architecture

### Class: `DopamineSystem`

```python
class DopamineSystem:
    def __init__(self, baseline_lr=0.1, rpe_sensitivity=0.5,
                 motivation_decay=0.95, history_window=10):
        # Configuration
        self.baseline_lr = baseline_lr
        self.rpe_sensitivity = rpe_sensitivity
        self.motivation_decay = motivation_decay
        self.history_window = history_window

        # State
        self.rpe_history: List[float] = []
        self.motivation_level: float = 0.5
        self.total_rpe_events: int = 0

    def compute_rpe(self, expected: float, actual: float) -> float:
        """Compute reward prediction error"""

    def modulate_learning_rate(self, base_lr: float, rpe: float) -> float:
        """Adjust learning rate based on RPE"""

    def update_motivation(self, rpe: float) -> float:
        """Update motivation level from RPE"""

    def get_exploration_bonus(self, uncertainty: float = 0.5) -> float:
        """Compute exploration bonus"""

    def process_event(self, expected: float, actual: float) -> Dict:
        """Main processing: compute RPE, update state, return modulations"""

    def get_state(self) -> Dict:
        """Get current dopamine system state"""
```

---

## 🧪 Testing Strategy (TDD)

### Phase 1: Core RPE Tests
1. **Basic RPE Computation**
   - Positive surprise (actual > expected)
   - Negative surprise (actual < expected)
   - No surprise (actual == expected)

2. **Learning Rate Modulation**
   - LR boost on positive RPE
   - LR reduction on negative RPE
   - LR clipping (0.01-1.0)

3. **Motivation Tracking**
   - Increases with positive RPE
   - Decreases with negative RPE
   - Decays toward baseline

4. **Exploration Bonus**
   - Increases with motivation
   - Amplified by uncertainty

5. **Full Event Processing**
   - Returns complete state
   - Maintains history window

### Phase 2: Integration Tests
- Integration with LAB_004 (Novelty Detection)
- Integration with LAB_001 (Emotional Salience)
- Integration with LAB_002 (Decay Modulation)

### Phase 3: Edge Cases & Performance
- Extreme RPE values
- Zero learning rate handling
- State persistence

---

## 📊 Expected Behavior

**Scenario: Positive Surprise (RPE > 0)**
```python
# User expects mediocre result (0.4) but gets excellent (0.9)
result = dopamine.process_event(expected=0.4, actual=0.9)
# result["rpe"] = 0.5 (high positive surprise)
# result["modulated_lr"] = 0.125 (boosted from 0.1 baseline)
# result["motivation_level"] increases
# result["exploration_bonus"] increases (optimistic → explore more)
```

**Scenario: Negative Surprise (RPE < 0)**
```python
# User expects good result (0.8) but gets poor (0.3)
result = dopamine.process_event(expected=0.8, actual=0.3)
# result["rpe"] = -0.5 (high negative surprise)
# result["modulated_lr"] = 0.075 (reduced from 0.1 baseline)
# result["motivation_level"] decreases
# result["exploration_bonus"] decreases (pessimistic → exploit more)
```

---

## 📚 Key References

**Papers:**
- Schultz, W., Dayan, P., & Montague, P. R. (1997). A neural substrate of prediction and reward. *Science*, 275(5306), 1593-1599.
- Berridge, K. C., & Robinson, T. E. (2003). Parsing reward. *Trends in neurosciences*, 26(9), 507-513.
- Niv, Y., & Schoenbaum, G. (2008). Dialogues on prediction errors. *Trends in cognitive sciences*, 12(7), 265-272.

**Related LABs:**
- LAB_001: Emotional Salience (emotional scoring)
- LAB_002: Intelligent Decay (decay rate modulation)
- LAB_004: Novelty Detection (novelty → expected reward)

---

## ✅ Success Criteria

**Functional:**
- ✅ All unit tests pass (20+ tests)
- ✅ Integration tests pass
- ✅ API endpoints respond correctly
- ✅ State persistence works

**Behavioral:**
- ✅ Positive RPE increases learning rate
- ✅ Negative RPE decreases learning rate
- ✅ Motivation tracks RPE history
- ✅ Exploration increases with motivation

**Performance:**
- ✅ RPE computation <1ms
- ✅ process_event() <5ms
- ✅ Memory footprint <10MB

---

## 🚀 Usage Example

```python
from LAYER_4_Neurochemistry_Full.LAB_013_Dopamine_System import DopamineSystem

# Initialize system
dopamine = DopamineSystem(
    baseline_lr=0.1,
    rpe_sensitivity=0.5,
    motivation_decay=0.95,
    history_window=10
)

# Process reward event
result = dopamine.process_event(expected=0.5, actual=0.8)

print(f"RPE: {result['rpe']}")  # 0.3 (positive surprise)
print(f"Modulated LR: {result['modulated_lr']}")  # ~0.115 (boosted)
print(f"Motivation: {result['motivation_level']}")  # increased
print(f"Exploration: {result['exploration_bonus']}")  # increased

# Get current state
state = dopamine.get_state()
print(f"Total events: {state['total_events']}")
print(f"RPE history: {state['rpe_history']}")
```

---

**Created:** November 4, 2025 (Session 7)
**Author:** NEXUS@CLI + Ricardo
**Implementation:** TDD (Test-Driven Development)
**Breakthrough Potential:** 🔥🔥🔥 HIGH (Foundation of reward learning)
