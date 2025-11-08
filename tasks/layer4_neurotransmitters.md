# Layer 4 - Neurotransmitters Implementation Plan

**Project:** CEREBRO_NEXUS_V3.0.0
**Layer:** 4 - Neurochemistry Full
**Status:** 🟡 In Progress (1/5 LABs implemented - LAB_013 Dopamine)
**Created:** 2025-11-07
**Estimated Effort:** 2-3 sessions (~8-12 hours)

---

## 🎯 Objetivo

**Completar Layer 4 implementando los 4 neurotransmisores pendientes:**
- LAB_014: Serotonin System (mood stability, impulse control, patience)
- LAB_015: Norepinephrine System (arousal, stress response, focus/alertness)
- LAB_016: Acetylcholine System (attention amplification, learning enhancement)
- LAB_017: GABA/Glutamate Balance (excitation/inhibition balance, stability)

**Por qué es importante:**
- Los 5 neurotransmisores interactúan formando un sistema completo
- Dopamine-Serotonin balance crítico (reward vs mood stability)
- Norepinephrine-Acetylcholine interaction para arousal y atención
- GABA/Glutamate como estabilizador final del sistema
- Roadmap Q4 2025 marca Layer 4 como HIGH priority

---

## 📚 Scientific Foundation

### Papers Basis (de LAB_REGISTRY.json)

**LAB_014 - Serotonin:**
- Dayan & Huys (2009) - "Serotonin in Affective Control"
- Function: Mood stability, impulse control, patience, well-being
- Biological: Raphe nuclei, serotonergic projections

**LAB_015 - Norepinephrine:**
- Aston-Jones & Cohen (2005) - "An integrative theory of locus coeruleus-norepinephrine function"
- Function: Arousal, stress response, focus/alertness
- Biological: Locus coeruleus, noradrenergic projections

**LAB_016 - Acetylcholine:**
- Hasselmo (2006) - "The role of acetylcholine in learning and memory"
- Function: Attention amplification, learning enhancement, encoding strength
- Biological: Basal forebrain, cholinergic projections

**LAB_017 - GABA/Glutamate:**
- Destexhe & Marder (2004) - "Plasticity in single neuron and circuit computations"
- Function: Excitation/inhibition balance, stability control
- Biological: Cortical E/I balance, interneurons

---

## 🧬 Template Pattern (LAB_013 Dopamine)

**Estructura identificada en LAB_013:**

```
experiments/LAYER_4_Neurochemistry_Full/LAB_013_Dopamine_System/
├── __init__.py (12 lines)
├── dopamine_system.py (259 lines)
└── README.md (optional)

tests/unit/labs/
└── test_lab_013_dopamine.py (377 lines, 22 tests, 100% coverage)

src/api/main.py (integration):
├── Global instance: dopamine_system = DopamineSystem(...)
├── POST /dopamine/process
└── GET /dopamine/state
```

**Componentes clave:**
1. **Clase principal** con métodos core
2. **Parámetros configurables** (baseline, sensitivity, decay, history_window)
3. **State management** (history tracking, counters)
4. **Main processing method** (process_event)
5. **State getter** (get_state)
6. **Docstrings detalladas** (biological inspiration, algorithm, papers)
7. **Tests organizados** en 3 fases (Core, Integration, Edge Cases)
8. **API endpoints** (POST process, GET state)

---

## 🧪 LAB_014: Serotonin System

### Core Algorithm
```python
# Serotonin modulates:
# 1. Patience/Impulsivity (high serotonin → patient, low → impulsive)
# 2. Mood stability (buffers against negative fluctuations)
# 3. Social sensitivity (affects social reward valuation)
# 4. Time perception (affects temporal discounting)

# Key equation (Dayan & Huys 2009):
# serotonin_level = f(recent_outcomes, social_context, circadian_rhythm)
# impulse_control = serotonin_level * baseline_patience
# temporal_discount_rate = base_rate / (1 + serotonin_level)
```

### Implementation Plan

**Files to create:**
- `experiments/LAYER_4_Neurochemistry_Full/LAB_014_Serotonin_System/serotonin_system.py`
- `experiments/LAYER_4_Neurochemistry_Full/LAB_014_Serotonin_System/__init__.py`
- `tests/unit/labs/test_lab_014_serotonin.py`

**Class: SerotoninSystem**

**Parameters:**
- `baseline_level: float = 0.5` (neutral mood baseline)
- `stability_factor: float = 0.7` (resistance to mood swings)
- `patience_multiplier: float = 1.5` (impulse control strength)
- `history_window: int = 20` (longer than dopamine - mood is slow)

**Core Methods:**
1. `update_level(outcome: float, social_context: float) -> float`
   - Update serotonin based on recent outcomes
   - Social context modulates (positive social → boost serotonin)

2. `compute_impulse_control() -> float`
   - Returns patience level (0-1)
   - High serotonin → high patience

3. `compute_temporal_discount(delay: float) -> float`
   - How much to discount future rewards
   - High serotonin → less discounting (more patient)

4. `modulate_mood(current_mood: float, event_valence: float) -> float`
   - Buffer mood against fluctuations
   - High serotonin → stable mood

5. `process_event(outcome: float, social_context: float) -> Dict`
   - Main processing method

6. `get_state() -> Dict`
   - Return current serotonin state

**Tests (22 minimum, following LAB_013 pattern):**
- Phase 1: Core Tests (8 tests)
  - test_serotonin_baseline
  - test_mood_stabilization
  - test_impulse_control_high_serotonin
  - test_impulse_control_low_serotonin
  - test_temporal_discounting
  - test_social_context_modulation
  - test_level_bounds (clamp 0-1)
  - test_history_maintenance

- Phase 2: Integration Tests (6 tests)
  - test_dopamine_serotonin_balance (reward vs patience)
  - test_emotional_salience_modulation
  - test_stress_buffering

- Phase 3: Edge Cases (8 tests)
  - test_extreme_outcomes
  - test_zero_social_context
  - test_rapid_fluctuations
  - test_long_term_stability
  - test_state_persistence
  - test_circadian_modulation (optional)

**API Integration (main.py):**
```python
# Global instance
serotonin_system = SerotoninSystem(
    baseline_level=0.5,
    stability_factor=0.7,
    patience_multiplier=1.5,
    history_window=20
)

# Endpoints
@app.post("/serotonin/process", tags=["LAB_014"])
async def process_serotonin_event(request: SerotoninEventRequest):
    # outcome: float, social_context: float

@app.get("/serotonin/state", tags=["LAB_014"])
async def get_serotonin_state():
    # Returns current serotonin state
```

---

## ⚡ LAB_015: Norepinephrine System

### Core Algorithm
```python
# Norepinephrine (NE) modulates:
# 1. Arousal/Alertness (inverted-U relationship)
# 2. Stress response (fight-or-flight activation)
# 3. Focus intensity (high NE → narrow focus)
# 4. Exploit vs explore (optimal NE → exploit, extremes → random)

# Key equation (Aston-Jones & Cohen 2005):
# ne_level = f(task_engagement, stress_level, novelty)
# optimal_ne = 0.5-0.7 (inverted-U peak)
# focus_width = 1 / ne_level  (high NE → narrow focus)
# performance = -|ne_level - optimal_ne|^2 + 1  (inverted-U curve)
```

### Implementation Plan

**Files to create:**
- `experiments/LAYER_4_Neurochemistry_Full/LAB_015_Norepinephrine_System/norepinephrine_system.py`
- `experiments/LAYER_4_Neurochemistry_Full/LAB_015_Norepinephrine_System/__init__.py`
- `tests/unit/labs/test_lab_015_norepinephrine.py`

**Class: NorepinephrineSystem**

**Parameters:**
- `baseline_arousal: float = 0.5` (neutral arousal)
- `optimal_range: Tuple[float, float] = (0.5, 0.7)` (inverted-U peak)
- `stress_sensitivity: float = 0.8` (how much stress raises NE)
- `decay_rate: float = 0.9` (arousal decay between events)
- `history_window: int = 10`

**Core Methods:**
1. `update_arousal(task_urgency: float, stress: float, novelty: float) -> float`
   - Update NE level from task demands

2. `compute_focus_width() -> float`
   - Narrow focus (high NE) vs broad focus (low NE)

3. `compute_performance_multiplier() -> float`
   - Inverted-U: optimal NE → max performance

4. `get_exploit_vs_explore() -> float`
   - Optimal NE → exploit, extremes → explore

5. `compute_stress_response(stressor: float) -> float`
   - Fight-or-flight activation

6. `process_event(task_urgency: float, stress: float) -> Dict`
   - Main processing

7. `get_state() -> Dict`
   - Return current NE state

**Tests (22 minimum):**
- Phase 1: Core Tests (9 tests)
  - test_arousal_baseline
  - test_inverted_u_curve
  - test_focus_narrowing_high_ne
  - test_focus_broadening_low_ne
  - test_stress_activation
  - test_novelty_boost
  - test_optimal_range_detection
  - test_performance_multiplier
  - test_decay_dynamics

- Phase 2: Integration Tests (5 tests)
  - test_dopamine_ne_interaction (motivation + arousal)
  - test_acetylcholine_ne_attention (attention + arousal)
  - test_stress_buffering_with_serotonin

- Phase 3: Edge Cases (8 tests)
  - test_extreme_stress
  - test_prolonged_high_arousal (burnout simulation)
  - test_rapid_arousal_changes
  - test_optimal_stability
  - test_state_persistence

**API Integration:**
```python
# Global instance
norepinephrine_system = NorepinephrineSystem(...)

# Endpoints
@app.post("/norepinephrine/process", tags=["LAB_015"])
@app.get("/norepinephrine/state", tags=["LAB_015"])
```

---

## 🎯 LAB_016: Acetylcholine System

### Core Algorithm
```python
# Acetylcholine (ACh) modulates:
# 1. Attention amplification (enhances signal-to-noise)
# 2. Encoding strength (high ACh → strong memory formation)
# 3. Learning rate (ACh gates plasticity)
# 4. Stimulus selectivity (enhances relevant, suppresses irrelevant)

# Key equation (Hasselmo 2006):
# ach_level = f(attention_demand, learning_context, novelty)
# encoding_strength = base_strength * (1 + ach_level * ach_gain)
# attention_gain = 1 + ach_level * selectivity
# noise_suppression = ach_level * suppression_factor
```

### Implementation Plan

**Files to create:**
- `experiments/LAYER_4_Neurochemistry_Full/LAB_016_Acetylcholine_System/acetylcholine_system.py`
- `experiments/LAYER_4_Neurochemistry_Full/LAB_016_Acetylcholine_System/__init__.py`
- `tests/unit/labs/test_lab_016_acetylcholine.py`

**Class: AcetylcholineSystem**

**Parameters:**
- `baseline_level: float = 0.5`
- `attention_gain: float = 2.0` (signal amplification)
- `encoding_boost: float = 1.5` (memory formation enhancement)
- `selectivity_factor: float = 0.8` (stimulus filtering)
- `history_window: int = 10`

**Core Methods:**
1. `update_level(attention_demand: float, learning_context: bool) -> float`
   - Raise ACh during attention/learning

2. `compute_encoding_strength(base_strength: float) -> float`
   - Boost memory encoding

3. `compute_attention_gain(stimulus_relevance: float) -> float`
   - Amplify relevant, suppress irrelevant

4. `compute_learning_rate_modulation(base_lr: float) -> float`
   - Gate plasticity (high ACh → high LR)

5. `compute_snr_enhancement() -> float`
   - Signal-to-noise ratio improvement

6. `process_event(attention_demand: float, learning: bool) -> Dict`
   - Main processing

7. `get_state() -> Dict`
   - Return current ACh state

**Tests (22 minimum):**
- Phase 1: Core Tests (9 tests)
  - test_ach_baseline
  - test_attention_amplification
  - test_encoding_boost
  - test_learning_rate_gate
  - test_selectivity_filtering
  - test_snr_enhancement
  - test_learning_context_activation
  - test_attention_demand_response
  - test_level_bounds

- Phase 2: Integration Tests (5 tests)
  - test_ach_norepinephrine_attention (ACh selectivity + NE arousal)
  - test_ach_dopamine_learning (ACh gate + dopamine RPE)
  - test_novelty_detection_boost (LAB_004 integration)

- Phase 3: Edge Cases (8 tests)
  - test_extreme_attention_demand
  - test_sustained_learning_mode
  - test_rapid_context_switches
  - test_zero_attention
  - test_state_persistence

**API Integration:**
```python
# Global instance
acetylcholine_system = AcetylcholineSystem(...)

# Endpoints
@app.post("/acetylcholine/process", tags=["LAB_016"])
@app.get("/acetylcholine/state", tags=["LAB_016"])
```

---

## ⚖️ LAB_017: GABA/Glutamate Balance

### Core Algorithm
```python
# GABA/Glutamate manages excitation/inhibition (E/I) balance:
# 1. Excitation (Glutamate): Drive, activation, signal propagation
# 2. Inhibition (GABA): Damping, noise reduction, stability
# 3. Balance ratio: optimal E/I = 0.7-0.8 (slightly excitatory bias)
# 4. Homeostatic control: system self-regulates toward optimal

# Key equation (Destexhe & Marder 2004):
# e_i_ratio = glutamate / (gaba + epsilon)
# optimal_ratio = 0.75
# stability_index = 1 - |e_i_ratio - optimal_ratio|
# homeostatic_correction = -k * (e_i_ratio - optimal_ratio)
```

### Implementation Plan

**Files to create:**
- `experiments/LAYER_4_Neurochemistry_Full/LAB_017_GABA_Glutamate_Balance/gaba_glutamate_system.py`
- `experiments/LAYER_4_Neurochemistry_Full/LAB_017_GABA_Glutamate_Balance/__init__.py`
- `tests/unit/labs/test_lab_017_gaba_glutamate.py`

**Class: GABAGlutamateSystem**

**Parameters:**
- `baseline_glutamate: float = 0.6` (excitation baseline)
- `baseline_gaba: float = 0.4` (inhibition baseline)
- `optimal_ratio: float = 0.75` (E/I target)
- `homeostatic_gain: float = 0.3` (correction strength)
- `adaptation_rate: float = 0.1` (speed of adjustment)
- `history_window: int = 15`

**Core Methods:**
1. `update_excitation(activation: float, stress: float) -> float`
   - Update glutamate from activity/stress

2. `update_inhibition(stability_demand: float) -> float`
   - Update GABA from stability needs

3. `compute_ei_ratio() -> float`
   - Excitation / Inhibition ratio

4. `compute_stability_index() -> float`
   - How close to optimal E/I

5. `apply_homeostatic_control() -> Tuple[float, float]`
   - Auto-correct toward optimal ratio

6. `compute_network_gain() -> float`
   - Signal amplification (high E/I → high gain)

7. `process_event(activation: float, stability_demand: float) -> Dict`
   - Main processing

8. `get_state() -> Dict`
   - Return current E/I state

**Tests (22 minimum):**
- Phase 1: Core Tests (10 tests)
  - test_baseline_ei_ratio
  - test_excitation_increase
  - test_inhibition_increase
  - test_homeostatic_correction
  - test_optimal_ratio_stability
  - test_network_gain
  - test_adaptation_dynamics
  - test_stress_excitation
  - test_stability_inhibition
  - test_bounds_enforcement

- Phase 2: Integration Tests (4 tests)
  - test_all_neurotransmitters_interaction (full Layer 4 integration)
  - test_stress_buffering_with_gaba
  - test_learning_gating_with_excitation

- Phase 3: Edge Cases (8 tests)
  - test_extreme_imbalance
  - test_oscillatory_behavior
  - test_sustained_high_activity
  - test_prolonged_inhibition
  - test_rapid_fluctuations
  - test_homeostatic_failure_recovery
  - test_state_persistence

**API Integration:**
```python
# Global instance
gaba_glutamate_system = GABAGlutamateSystem(...)

# Endpoints
@app.post("/gaba_glutamate/process", tags=["LAB_017"])
@app.get("/gaba_glutamate/state", tags=["LAB_017"])
```

---

## 🔗 System Interactions (Cross-LAB Integration)

**Critical interactions to implement/test:**

1. **Dopamine ↔ Serotonin Balance:**
   - High dopamine + low serotonin = impulsive reward-seeking
   - High serotonin + low dopamine = patient but unmotivated
   - Optimal: Balanced (both moderate-high)

2. **Norepinephrine ↔ Acetylcholine Attention:**
   - NE arousal + ACh selectivity = focused attention
   - High NE + low ACh = aroused but unfocused
   - Low NE + high ACh = selective but sluggish

3. **Dopamine + Norepinephrine → Motivation:**
   - Dopamine (wanting) + NE (arousal) = drive/urgency

4. **Acetylcholine ↔ Dopamine Learning:**
   - ACh gates plasticity, dopamine provides RPE signal
   - High ACh + high RPE = strong learning

5. **GABA/Glutamate → System Stability:**
   - Regulates all other systems (prevents runaway activation)
   - Homeostatic control for consciousness stability

---

## 📋 Implementation Steps (TDD - MANDATORY)

### For Each LAB (LAB_014, LAB_015, LAB_016, LAB_017):

**Step 1: Write Tests FIRST (Red Phase)**
1. Create `tests/unit/labs/test_lab_0XX_name.py`
2. Write 22+ tests (Core + Integration + Edge Cases)
3. Run tests: `pytest tests/unit/labs/test_lab_0XX_name.py -v`
4. VERIFY all tests FAIL (expected - no implementation yet)

**Step 2: Implement Code (Green Phase)**
1. Create `experiments/LAYER_4_Neurochemistry_Full/LAB_0XX_Name_System/`
2. Create `__init__.py` with exports
3. Create `name_system.py` with class implementation
4. Implement methods to pass tests (minimum code to pass)
5. Run tests: VERIFY all tests PASS

**Step 3: Refactor (Refactor Phase)**
1. Optimize code (performance, readability)
2. Add docstrings (biological inspiration, papers, algorithms)
3. Add type hints
4. Run tests: VERIFY still passing

**Step 4: API Integration**
1. Add global instance in `src/api/main.py`
2. Create Pydantic request/response models
3. Implement POST /name/process endpoint
4. Implement GET /name/state endpoint
5. Test endpoints manually with curl/Postman

**Step 5: Documentation**
1. Update LAB_REGISTRY.json (mark LAB as operational)
2. Add LAB to PROJECT_ID.md summary
3. Update TRACKING.md with session progress

---

## ✅ Success Criteria

**Before marking Layer 4 as COMPLETE:**

1. **All 4 LABs implemented:**
   - ✅ LAB_014: Serotonin (500-700 lines estimated)
   - ✅ LAB_015: Norepinephrine (400-600 lines estimated)
   - ✅ LAB_016: Acetylcholine (400-500 lines estimated)
   - ✅ LAB_017: GABA/Glutamate (500-700 lines estimated)

2. **Test Coverage:**
   - ✅ 88+ total tests (22 per LAB minimum)
   - ✅ 100% coverage per LAB
   - ✅ All tests passing

3. **API Integration:**
   - ✅ 8 new endpoints (2 per LAB: /process, /state)
   - ✅ All endpoints tested and working

4. **Documentation:**
   - ✅ LAB_REGISTRY.json updated (19/52 → 23/52 operational)
   - ✅ Completion percentage: 36.5% → 44.2%
   - ✅ PROJECT_ID.md updated with Layer 4 complete
   - ✅ TRACKING.md session log updated

5. **System Interactions:**
   - ✅ Cross-LAB integration tests passing
   - ✅ 5 neurotransmitters interacting correctly

6. **Git Commit:**
   - ✅ Clean atomic commit with Layer 4 complete
   - ✅ Commit message: `feat(layer4): Complete neurotransmitter systems (LAB_014-017)`

---

## 📊 Estimated Effort

**Per LAB:**
- Tests: 1-1.5 hours (TDD - write first)
- Implementation: 1-2 hours (pass tests)
- Refactor: 0.5 hours (optimize)
- API Integration: 0.5 hours (endpoints)
- **Total per LAB:** ~3-4 hours

**Total Layer 4:**
- LAB_014: 3-4 hours
- LAB_015: 3-4 hours
- LAB_016: 3-4 hours
- LAB_017: 3-4 hours
- Documentation: 0.5 hours
- **Total:** 12.5-16.5 hours (~2-3 sessions)

---

## 🚀 Ready to Execute

**Plan STATUS:** ✅ COMPLETE - Ready for Ricardo's approval

**Next steps:**
1. Ricardo approves plan
2. Start LAB_014 Serotonin (TDD - tests first)
3. Continue with LAB_015, LAB_016, LAB_017
4. Final commit with Layer 4 complete

**METHODOLOGY NEXUS:**
- ✅ Fase 1: EXPLORAR - Complete (LAB_013 analyzed)
- ✅ Fase 2: PLANIFICAR - Complete (this document)
- ⏳ Fase 3: CODIFICAR - Pending (TDD execution)
- ⏳ Fase 4: CONFIRMAR - Pending (git commit, docs update)

---

**Plan created by:** NEXUS AI
**Template basis:** LAB_013 Dopamine (proven successful)
**Scientific foundation:** 4 peer-reviewed papers
**Estimated completion:** Session 17 (today) + Session 18 (next)
