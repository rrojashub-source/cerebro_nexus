# LAB_029-033: Social Cognition Advanced + Homeostasis - IMPLEMENTATION PLAN

**Date:** November 8, 2025 (Session 20)
**Target:** 5 LABs (2 social cognition + 3 homeostasis)
**Estimated:** 150-180 tests, ~3,500 lines

---

## 🎯 IMPLEMENTATION ORDER

1. **LAB_030: Perspective Taking** (Medium) - Foundation for LAB_029
2. **LAB_029: Social Norms & Ethics** (High) - Builds on LAB_030
3. **LAB_031: Circadian Rhythm** (Medium) - Foundation for LAB_032
4. **LAB_032: Energy Management** (Medium) - Uses LAB_031
5. **LAB_033: Allostatic Load** (High) - Wide integration

**Rationale:** Bottom-up dependencies, social first then homeostasis

---

## 📋 LAB_030: PERSPECTIVE TAKING

### Specification

**Function:** Transform viewpoints (egocentric ↔ allocentric)

**Core Methods:**
```python
class PerspectiveTakingSystem:
    def shift_perspective(self, current_viewpoint, target_viewpoint, context):
        """Transform representation from one perspective to another"""

    def compute_rotation_cost(self, angle_difference):
        """Mental rotation cost (Shepard & Metzler 1971)"""

    def spatial_perspective(self, ego_position, allo_position, landmark):
        """Egocentric → Allocentric spatial transformation"""

    def conceptual_perspective(self, my_belief, their_belief, context):
        """My view → Their view (LAB_027 integration)"""

    def update_belief_from_perspective(self, belief, new_perspective):
        """Update what I believe based on new viewpoint"""
```

**Integration Points:**
- LAB_027 (ToM): "What can they see/know from there?"
- LAB_028 (Empathy): Embodied perspective → emotional resonance
- Working Memory: Hold multiple perspectives simultaneously

**Test Plan (25-30 tests):**
1. Spatial rotation (0°, 90°, 180°)
2. Rotation cost increases linearly with angle
3. Egocentric → Allocentric transformation
4. Conceptual perspective shift (beliefs)
5. Integration with ToM (what they can see)
6. 1st person vs 3rd person imagery

---

## 📋 LAB_029: SOCIAL NORMS & ETHICS

### Specification

**Function:** Moral reasoning, norm detection, fairness computation

**Core Methods:**
```python
class SocialNormsEthicsSystem:
    def detect_norm_violation(self, action, context, observed_reactions):
        """Learn norms from approval/disapproval patterns"""

    def moral_judgment(self, scenario, dilemma_type="trolley"):
        """Dual-process: vmPFC (emotion) vs dlPFC (utility)"""

    def compute_fairness(self, distribution, principle="equality"):
        """Fairness: equal, merit-based, need-based"""

    def action_vs_outcome_judgment(self, action, outcome, intentions):
        """Action-based vs outcome-based morality (Cushman 2013)"""

    def care_ethics_weight(self, empathy_level, relationship):
        """Empathy → deontological bias (LAB_028 integration)"""
```

**Dual-Process Theory:**
```python
# System 1 (vmPFC): Fast, emotional, deontological
emotional_judgment = empathy_level * 0.7 + norm_strength * 0.3

# System 2 (dlPFC): Slow, rational, utilitarian
utilitarian_judgment = (lives_saved / lives_lost) * rational_weight

# Final judgment = weighted combination
final = emotional_judgment * (1 - rational_engagement) + utilitarian_judgment * rational_engagement
```

**Integration Points:**
- LAB_027 (ToM): Intentions matter for moral judgment
- LAB_028 (Empathy): Care ethics (deontological bias)
- LAB_001 (Emotional salience): Moral intuitions
- LAB_030 (Perspective): Fairness from multiple viewpoints

**Test Plan (30-35 tests):**
1. Norm learning from repeated interactions
2. Norm violation detection
3. Trolley problem (utilitarian vs deontological)
4. Personal vs impersonal dilemmas (vmPFC engagement)
5. Action-based vs outcome-based judgments
6. Intention-sensitive morality (LAB_027 integration)
7. Empathy → care ethics (LAB_028 integration)
8. Fairness computation (equality, merit, need)

---

## 📋 LAB_031: CIRCADIAN RHYTHM

### Specification

**Function:** Time-of-day effects, alertness cycles, sleep pressure

**Two-Process Model (Borbély 1982):**
```python
class CircadianRhythmSystem:
    def update_circadian_phase(self, time_elapsed, light_exposure):
        """Update internal clock (24-hour cycle)"""

    def compute_process_c(self, phase):
        """Process C: Circadian alertness (sinusoidal)"""
        # Peak at ~10 AM and ~9 PM

    def compute_process_s(self, time_awake):
        """Process S: Sleep pressure (homeostatic)"""
        # Builds during wake (~1% per hour)

    def compute_alertness(self, process_c, process_s):
        """Alertness = C - S"""

    def time_of_day_effects(self, cognitive_task, alertness):
        """Modulate cognitive performance by alertness"""
```

**Mathematical Model:**
```python
# Process C (Circadian)
circadian_amplitude = 0.8
peak_phase = 10  # 10 AM
process_c = circadian_amplitude * cos(2π * (phase - peak_phase) / 24)

# Process S (Homeostatic)
sleep_pressure = min(1.0, time_awake_hours * 0.01)

# Alertness
alertness = process_c - sleep_pressure
```

**Integration Points:**
- LAB_003 (Sleep consolidation): Trigger at high sleep pressure
- LAB_015 (Norepinephrine): Arousal modulated by alertness
- LAB_032 (Energy): Baseline energy set by circadian phase

**Test Plan (28-32 tests):**
1. Circadian phase advances correctly (24-hour cycle)
2. Process C peaks at correct times (10 AM, 9 PM)
3. Process S builds during wake
4. Alertness = C - S formula
5. Sleep resets Process S
6. Light entrainment (phase shift)
7. Time-of-day effects on cognition
8. Integration with sleep consolidation (LAB_003)

---

## 📋 LAB_032: ENERGY MANAGEMENT

### Specification

**Function:** Track mental energy, manage fatigue, recovery

**Core Methods:**
```python
class EnergyManagementSystem:
    def deplete_energy(self, task_difficulty, duration, current_energy):
        """Ego depletion: energy decreases with cognitive load"""

    def compute_fatigue_level(self, energy_level):
        """Fatigue = 1 - energy"""

    def compensatory_effort(self, fatigue, task_importance):
        """Under fatigue: increase effort, narrow focus (Hockey 2013)"""

    def recovery_dynamics(self, rest_duration, recovery_rate):
        """Exponential recovery during rest"""

    def modulate_cognitive_functions(self, energy, system):
        """Energy depletion impairs cognition"""
```

**Depletion Formula:**
```python
# Energy depletion
depletion_rate = task_difficulty * time * (1 - energy_level)**0.5

# Compensatory effort
if energy < 0.5:
    effort_multiplier = 1 + (0.5 - energy) * 2.0  # Up to 2x effort
    focus_narrowing = 0.3 + energy * 0.7  # Narrow focus

# Recovery (exponential)
energy += (1.0 - energy) * recovery_rate * rest_duration
```

**Fatigue Effects:**
- Cognitive control impaired (LAB_019)
- Cognitive flexibility reduced (LAB_020)
- Working memory capacity reduced
- Goal prioritization shifts (urgent > long-term)

**Integration Points:**
- LAB_031 (Circadian): Baseline energy modulated by alertness
- LAB_019 (Cognitive control): Weakened under fatigue
- LAB_020 (Cognitive flexibility): Reduced under fatigue
- LAB_033 (Allostatic load): Interacts with stress

**Test Plan (25-30 tests):**
1. Energy depletes with cognitive load
2. Depletion rate depends on task difficulty
3. Recovery during rest (exponential)
4. Compensatory effort under fatigue
5. Focus narrowing under fatigue
6. Cognitive control impaired (LAB_019 integration)
7. Cognitive flexibility reduced (LAB_020 integration)
8. Circadian modulation of baseline energy (LAB_031)

---

## 📋 LAB_033: ALLOSTATIC LOAD

### Specification

**Function:** Cumulative stress tracking, stress effects on cognition

**Core Methods:**
```python
class AllostaticLoadSystem:
    def accumulate_stress(self, stressor_intensity, current_load):
        """Allostatic load builds with stressors"""

    def decay_stress(self, load, recovery_rate, time):
        """Slow decay (chronic stress recovery)"""

    def compute_stress_effects(self, load):
        """Inverted-U performance curve + chronic impairment"""

    def pfc_impairment(self, load):
        """PFC functions impaired when load > 0.6 (Arnsten 2009)"""

    def amygdala_reactivity(self, load):
        """Emotional reactivity enhanced under stress"""
```

**Stress Accumulation:**
```python
# Acute stressor
load += stressor_intensity * 0.1

# Chronic decay (slow)
load *= 0.98  # per time unit

# Inverted-U performance
if load < 0.3:
    performance = 0.6 + load * 1.0  # Under-aroused
elif load < 0.6:
    performance = 0.9 + (0.6 - load) * 0.3  # Optimal
else:
    performance = 1.0 - (load - 0.6) * 1.5  # Over-aroused
```

**Stress Effects (Load > 0.6):**
- PFC impairment:
  - Cognitive control weakened (LAB_019)
  - Cognitive flexibility reduced (LAB_020)
  - Error monitoring impaired (LAB_021)
  - Planning impaired (LAB_018)
- Amygdala hyperactivity:
  - Emotional salience amplified (LAB_001)
  - Working memory capacity reduced (LAB_011)
- Norepinephrine spike (LAB_015)

**Integration Points:**
- LAB_001 (Emotional salience): Amplified under stress
- LAB_011 (Working memory): Capacity reduced
- LAB_015 (Norepinephrine): Acute stress response
- LAB_018-021 (Executive functions): All impaired
- LAB_032 (Energy): Stress accelerates depletion

**Test Plan (28-32 tests):**
1. Load accumulates with stressors
2. Slow decay (chronic stress)
3. Acute vs chronic stress distinction
4. Inverted-U performance curve
5. PFC impairment at load > 0.6
6. Amygdala reactivity enhancement
7. Working memory capacity reduction (LAB_011)
8. Cognitive control impairment (LAB_019)
9. Emotional salience amplification (LAB_001)
10. Norepinephrine integration (LAB_015)
11. Recovery dynamics (prolonged rest needed)

---

## 🧪 TDD METHODOLOGY

### Red Phase (Write Failing Tests First)
```python
def test_perspective_rotation_cost_linear():
    """Rotation cost increases linearly with angle (Shepard & Metzler)"""
    system = PerspectiveTakingSystem()

    cost_30 = system.compute_rotation_cost(30)
    cost_60 = system.compute_rotation_cost(60)
    cost_90 = system.compute_rotation_cost(90)

    assert cost_60 == pytest.approx(cost_30 * 2, abs=0.05)
    assert cost_90 == pytest.approx(cost_30 * 3, abs=0.05)
```

### Green Phase (Implement to Pass)
```python
def compute_rotation_cost(self, angle_degrees: float) -> float:
    """Mental rotation cost (linear with angle)"""
    base_cost_per_degree = 0.01  # 10ms per degree (literature)
    return abs(angle_degrees) * base_cost_per_degree
```

### Refactor Phase (Optimize, Error Handling)
- Add bounds checking
- Handle edge cases
- Optimize performance
- Add documentation

---

## 📊 ESTIMATED TOTALS

| LAB | Tests | Lines (Main) | Lines (Tests) | Difficulty |
|-----|-------|--------------|---------------|------------|
| LAB_030 | 25-30 | 400-500 | 300-400 | Medium |
| LAB_029 | 30-35 | 600-700 | 400-500 | High |
| LAB_031 | 28-32 | 500-600 | 350-450 | Medium |
| LAB_032 | 25-30 | 400-500 | 300-400 | Medium |
| LAB_033 | 28-32 | 600-700 | 350-450 | High |
| **TOTAL** | **136-159** | **2,500-3,000** | **1,700-2,200** | **High** |

**Integration Complexity:** HIGH (affects 10+ existing LABs)

---

## ✅ SUCCESS CRITERIA

1. **All tests passing** (TDD methodology strict)
2. **Integration points working** (LAB_027, LAB_028, LAB_001, LAB_011, LAB_015, LAB_018-021)
3. **Neuroscience fidelity** (equations match papers)
4. **API endpoints** (2 per LAB = 10 total)
5. **Documentation** (docstrings, comments)
6. **Quality maintained** (no velocity compromises)

---

## 🎯 READY TO IMPLEMENT

**Next:** Start with LAB_030 (Perspective Taking) - Medium difficulty, clear interface

**Estimated Session 20 Total:** 5 LABs, 150-180 tests, ~3,500 lines, 4-5 hours

---

**Plan created:** November 8, 2025 (Session 20)
**NEXUS@CLI**
**Status:** ✅ READY TO CODE
