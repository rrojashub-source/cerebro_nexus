# LAYER_5A Executive Functions - Implementation Plan

**Created:** November 7, 2025 (Session 18)
**Status:** Planning complete, ready for implementation
**Goal:** Implement 5 Executive Function LABs with TDD methodology

---

## 📋 EXECUTIVE SUMMARY

**Scope:** 5 LABs (LAB_018-022) - Executive Functions (prefrontal cortex)

**Implementation Order:**
1. LAB_019: Inhibitory Control (Core EF - simplest)
2. LAB_020: Cognitive Flexibility (Core EF - builds on 019)
3. LAB_021: Error Detection & Correction (Monitoring - uses dopamine)
4. LAB_018: Planning & Sequencing (Higher-order - needs working memory)
5. LAB_022: Goal-Directed Behavior (Integrative - uses ALL)

**Estimated Effort:**
- Total code: ~1,800-2,300 lines main
- Total tests: ~3,000-3,500 lines tests
- Total time: ~5-6 hours (autonomous execution)

---

## 🧠 LAB_019: INHIBITORY CONTROL

### Overview

**Type:** Core Executive Function (Miyake 2000)
**Neural Substrate:** Right inferior frontal gyrus (rIFG), pre-SMA, OFC
**Function:** Suppression of prepotent (automatic) responses

### Biological Foundation

**Papers:**
- Aron et al. (2014) - "Frontosubthalamic circuits for stopping and suppression"
- Bari & Robbins (2013) - "Inhibition and impulsivity: Behavioral and neural basis"

**Neurochemistry:**
- Serotonin (LAB_014): High 5-HT = strong inhibition, low impulsivity
- Norepinephrine (LAB_015): Optimal arousal enhances control
- GABA (LAB_017): Inhibitory neurotransmission supports response suppression

### Core Concepts

**Stop-Signal Paradigm:**
- Go signal: Execute response
- Stop signal: Inhibit response
- Stop-signal reaction time (SSRT): Measure of inhibitory control

**Response Conflict:**
- Competing response tendencies
- Need to inhibit prepotent (dominant) response
- Select alternative (non-dominant) response

### Implementation Design

**Class:** `InhibitoryControlSystem`

**Parameters:**
```python
baseline_control: float = 0.5          # Baseline inhibition strength
control_gain: float = 2.0              # Control amplification
conflict_sensitivity: float = 0.8     # Sensitivity to response conflict
adaptation_rate: float = 0.1          # Learning rate
history_window: int = 15              # History buffer size
```

**State:**
```python
self.current_control_strength: float  # Current inhibition strength (0-1)
self.control_history: List[float]     # Recent control levels
self.total_inhibitions: int           # Count of inhibition attempts
self.successful_inhibitions: int      # Count of successful stops
```

**Methods:**

1. `update_control_strength(response_conflict, prepotency) -> float`
   - Inputs: conflict level (0-1), prepotency strength (0-1)
   - Updates control strength based on conflict
   - Returns: New control strength

2. `attempt_inhibition(prepotency, control_available) -> bool`
   - Inputs: prepotency (automatic response strength), available control
   - Simulates stop-signal paradigm
   - Returns: True if inhibition successful, False if failed

3. `compute_ssrt() -> float`
   - Computes stop-signal reaction time
   - Lower SSRT = faster/better inhibition
   - Formula: SSRT = base_rt * (1.0 - control_strength)

4. `integrate_serotonin(serotonin_level) -> float`
   - Modulates control strength by serotonin
   - High serotonin → stronger control
   - Returns: Modulated control strength

5. `compute_impulsivity() -> float`
   - Inverse of control strength
   - High control = low impulsivity
   - Returns: Impulsivity index (0-1)

6. `process_event(response_conflict, prepotency) -> Dict`
   - Main interface
   - Returns: {control_strength, ssrt, impulsivity, success_rate}

### Test Plan (28 tests)

**Test Suite:** `test_lab_019_inhibitory_control.py`

**Test Classes:**

1. **TestInitialization** (3 tests)
   - Default parameters correct
   - State initialized properly
   - History buffers empty

2. **TestControlStrengthUpdate** (5 tests)
   - High conflict increases control
   - Low conflict maintains baseline
   - Control strength bounded [0, 1]
   - Adaptation over time
   - History tracking correct

3. **TestInhibitionAttempt** (6 tests)
   - High control successfully inhibits strong prepotency
   - Low control fails to inhibit strong prepotency
   - Success rate tracking
   - Failed inhibition doesn't crash
   - Boundary cases (prepotency=0, prepotency=1)

4. **TestSSRTComputation** (4 tests)
   - High control → low SSRT (fast stopping)
   - Low control → high SSRT (slow stopping)
   - SSRT formula correct
   - SSRT updates with control changes

5. **TestSerotoninIntegration** (4 tests)
   - High serotonin amplifies control
   - Low serotonin weakens control
   - Integration formula realistic
   - Modulation bounded

6. **TestImpulsivityComputation** (3 tests)
   - Impulsivity inverse of control
   - High control = low impulsivity
   - Impulsivity range correct

7. **TestProcessEvent** (3 tests)
   - Complete processing cycle
   - All outputs computed
   - State updated correctly

### API Integration

**Endpoints:**

```python
# Process inhibition event
POST /inhibitory_control/process
{
  "response_conflict": 0.7,    # Conflict level (0-1)
  "prepotency": 0.8            # Automatic response strength (0-1)
}

Response:
{
  "control_strength": 0.65,
  "ssrt": 250,                 # milliseconds
  "impulsivity": 0.35,
  "inhibition_success_rate": 0.72,
  "serotonin_modulation": 0.82
}

# Get system state
GET /inhibitory_control/state

Response:
{
  "control_strength": 0.65,
  "control_history": [0.60, 0.63, 0.65],
  "total_inhibitions": 142,
  "successful_inhibitions": 102,
  "success_rate": 0.718,
  "average_ssrt": 265
}
```

### Success Criteria

- ✅ 28/28 tests passing (100%)
- ✅ High serotonin improves inhibition (validated)
- ✅ High conflict increases control (validated)
- ✅ SSRT inversely related to control (validated)
- ✅ API endpoints functional
- ✅ Integrated with LAB_014 (serotonin)

---

## 🔄 LAB_020: COGNITIVE FLEXIBILITY

### Overview

**Type:** Core Executive Function - "Shifting" (Miyake 2000)
**Neural Substrate:** Dorsolateral PFC (dlPFC), ACC, posterior parietal
**Function:** Task switching, rule updating, adaptive behavior

### Biological Foundation

**Papers:**
- Monsell (2003) - "Task switching" (Trends in Cognitive Sciences)
- Kehagia et al. (2010) - "Neuropsychopharmacology of cognitive flexibility"

**Neurochemistry:**
- Dopamine (LAB_013): Facilitates set switching (D2 receptors)
- Norepinephrine (LAB_015): Arousal for attention shift
- Acetylcholine (LAB_016): Encoding new rules

### Core Concepts

**Task Switch Cost:**
- Switch trial: Change from Task A to Task B
- Repeat trial: Continue with same task
- Switch cost: RT_switch - RT_repeat (typically 50-200ms)

**Mental Set:**
- Configuration of cognitive processes for specific task
- Task rules, stimulus-response mappings
- Switching requires: inhibit old set + activate new set

**Reconfiguration:**
- Time needed to adjust mental set
- Affected by: preparation time, task difficulty, age

### Implementation Design

**Class:** `CognitiveFlexibilitySystem`

**Parameters:**
```python
baseline_flexibility: float = 0.5     # Baseline switch capability
switch_cost_base: float = 150.0       # Base switch cost (ms)
reconfiguration_speed: float = 0.8   # Speed of set reconfiguration
rule_encoding_strength: float = 0.7  # Strength of rule learning
adaptation_rate: float = 0.15        # Learning rate
history_window: int = 20             # History buffer size
```

**State:**
```python
self.current_flexibility: float      # Current flexibility level (0-1)
self.current_task_set: str           # Currently active task ("A", "B", etc.)
self.task_set_history: List[str]     # Recent task history
self.switch_count: int               # Total switches attempted
self.successful_switches: int        # Successful switches
self.total_switch_cost: float        # Accumulated switch cost (ms)
```

**Methods:**

1. `switch_task_set(new_task, preparation_time) -> Tuple[bool, float]`
   - Inputs: new task ID, preparation time (ms)
   - Simulates task switch with reconfiguration
   - Returns: (success, switch_cost_ms)

2. `compute_switch_cost(preparedness) -> float`
   - Inputs: How prepared for switch (0-1)
   - Computes switch cost in milliseconds
   - Formula: base_cost * (1.0 - preparedness * flexibility)

3. `update_flexibility(switch_frequency, success_rate) -> float`
   - Inputs: Recent switch frequency, success rate
   - Updates flexibility with practice effects
   - Returns: New flexibility level

4. `integrate_dopamine(dopamine_level) -> float`
   - Modulates flexibility by dopamine
   - Optimal dopamine = optimal flexibility (inverted-U)
   - Returns: Modulated flexibility

5. `integrate_acetylcholine(ach_level) -> float`
   - Modulates rule encoding
   - High ACh = faster rule learning
   - Returns: Encoding boost

6. `detect_perseveration() -> bool`
   - Detects stuck in old task set (perseveration)
   - Indicates poor flexibility
   - Returns: True if perseverating

7. `process_event(new_task, preparation_time) -> Dict`
   - Main interface
   - Returns: {flexibility, switch_cost, success, perseveration}

### Test Plan (30 tests)

**Test Suite:** `test_lab_020_cognitive_flexibility.py`

**Test Classes:**

1. **TestInitialization** (3 tests)
2. **TestTaskSwitching** (6 tests)
   - Successful switch updates task set
   - Switch cost computed correctly
   - Preparation time reduces cost
   - Repeated switches improve performance
3. **TestSwitchCostComputation** (4 tests)
   - Base cost applies without preparation
   - High preparedness reduces cost
   - High flexibility reduces cost
   - Cost never negative
4. **TestFlexibilityUpdate** (5 tests)
   - Practice improves flexibility
   - Success rate affects learning
   - Flexibility bounded [0, 1]
   - Low success degrades flexibility
5. **TestDopamineIntegration** (4 tests)
   - Optimal dopamine = max flexibility (inverted-U)
   - Too low/high dopamine impairs
   - Integration realistic
6. **TestAcetylcholineIntegration** (3 tests)
   - High ACh speeds rule learning
   - Encoding boost realistic
7. **TestPerseverationDetection** (3 tests)
   - Detects when stuck in old set
   - Threshold configurable
8. **TestProcessEvent** (2 tests)

### API Integration

**Endpoints:**

```python
# Process task switch event
POST /cognitive_flexibility/process
{
  "new_task": "B",             # New task ID
  "preparation_time": 500      # Preparation time (ms)
}

Response:
{
  "flexibility": 0.68,
  "switch_cost_ms": 125,
  "switch_success": true,
  "perseveration_detected": false,
  "dopamine_modulation": 0.75,
  "acetylcholine_boost": 0.82
}

# Get system state
GET /cognitive_flexibility/state

Response:
{
  "flexibility": 0.68,
  "current_task_set": "B",
  "task_history": ["A", "A", "B", "A", "B"],
  "switch_count": 87,
  "successful_switches": 74,
  "success_rate": 0.85,
  "average_switch_cost_ms": 142
}
```

### Success Criteria

- ✅ 30/30 tests passing (100%)
- ✅ Switch cost decreases with preparation
- ✅ Practice improves flexibility
- ✅ Dopamine shows inverted-U curve
- ✅ Perseveration detection works
- ✅ API endpoints functional
- ✅ Integrated with LAB_013 (dopamine), LAB_016 (acetylcholine)

---

## 🚨 LAB_021: ERROR DETECTION & CORRECTION

### Overview

**Type:** Monitoring Component (Diamond 2013)
**Neural Substrate:** Anterior cingulate cortex (ACC), medial PFC
**Function:** Performance monitoring, conflict/error detection, behavioral adjustment

### Biological Foundation

**Papers:**
- Botvinick et al. (2001) - "Conflict monitoring and anterior cingulate cortex: an update"
- Holroyd & Coles (2002) - "The neural basis of human error processing: reinforcement learning, dopamine, and the error-related negativity"

**Neurochemistry:**
- Dopamine (LAB_013): Negative RPE signals errors
- Norepinephrine (LAB_015): Arousal spike on error detection
- ACC integrates: Conflict + Error + Dopamine signal

### Core Concepts

**Error-Related Negativity (ERN):**
- EEG signal ~50-100ms after error
- Generated by ACC
- Amplitude correlated with error awareness

**Conflict Monitoring:**
- Detects competing response tendencies
- High conflict → increase control
- Signals need for behavioral adjustment

**Post-Error Slowing:**
- Slower RT on trial after error
- Adaptive: allows more cautious processing
- Mediated by ACC-dlPFC interaction

### Implementation Design

**Class:** `ErrorDetectionSystem`

**Parameters:**
```python
baseline_sensitivity: float = 0.6     # Baseline error sensitivity
conflict_threshold: float = 0.5      # Conflict detection threshold
error_learning_rate: float = 0.2     # Learning from errors
correction_strength: float = 0.8     # Strength of corrective signal
adaptation_rate: float = 0.15        # Overall adaptation speed
history_window: int = 25             # History buffer size
```

**State:**
```python
self.current_sensitivity: float      # Error detection sensitivity (0-1)
self.conflict_level: float           # Current conflict level (0-1)
self.errors_detected: int            # Total errors detected
self.corrections_applied: int        # Corrections triggered
self.conflict_history: List[float]   # Recent conflict levels
self.error_history: List[bool]       # Recent error occurrences
```

**Methods:**

1. `detect_conflict(response_a_strength, response_b_strength) -> float`
   - Inputs: Competing response strengths
   - Computes conflict level
   - Formula: min(a, b) / (max(a, b) + epsilon)
   - Returns: Conflict level (0-1)

2. `detect_error(actual_outcome, expected_outcome, confidence) -> Tuple[bool, float]`
   - Inputs: Actual vs expected outcome, confidence
   - Determines if error occurred
   - Computes error magnitude
   - Returns: (error_detected, error_magnitude)

3. `compute_ern_amplitude(error_magnitude, sensitivity) -> float`
   - Simulates Error-Related Negativity
   - Higher magnitude & sensitivity → larger ERN
   - Returns: ERN amplitude (arbitrary units)

4. `trigger_correction(error_magnitude) -> Dict`
   - Generates corrective signal
   - Increases control, slows processing
   - Returns: {control_boost, post_error_slowing_ms}

5. `integrate_dopamine_rpe(rpe) -> float`
   - Uses LAB_013 dopamine RPE as error signal
   - Negative RPE = error detected
   - Returns: Error magnitude from RPE

6. `integrate_norepinephrine_arousal(baseline_arousal) -> float`
   - Error triggers NE arousal spike
   - Returns: Arousal boost magnitude

7. `update_sensitivity(error_frequency, correction_success_rate) -> float`
   - Adjusts sensitivity based on experience
   - Too many false alarms → reduce sensitivity
   - Missed errors → increase sensitivity
   - Returns: New sensitivity level

8. `compute_post_error_slowing() -> float`
   - Computes RT increase after error
   - Typical: 20-50ms slowing
   - Returns: Slowing magnitude (ms)

9. `process_event(response_strengths, actual_outcome, expected_outcome) -> Dict`
   - Main interface
   - Returns: {conflict, error_detected, ern, correction, arousal_boost}

### Test Plan (33 tests)

**Test Suite:** `test_lab_021_error_detection.py`

**Test Classes:**

1. **TestInitialization** (3 tests)
2. **TestConflictDetection** (5 tests)
   - High conflict when responses balanced
   - Low conflict when one dominates
   - Conflict formula correct
   - Threshold detection works
3. **TestErrorDetection** (6 tests)
   - Detects mismatch between expected & actual
   - Confidence modulates detection
   - Error magnitude computed correctly
   - True positives and true negatives
4. **TestERNComputation** (4 tests)
   - ERN amplitude scales with error magnitude
   - Sensitivity modulates ERN
   - ERN realistic range
5. **TestCorrectionTriggering** (5 tests)
   - Correction increases control
   - Post-error slowing computed
   - Correction strength realistic
6. **TestDopamineRPEIntegration** (4 tests)
   - Negative RPE signals error
   - RPE magnitude → error magnitude
   - Integration with LAB_013
7. **TestNorepinephrineIntegration** (3 tests)
   - Error triggers arousal spike
   - Arousal boost realistic
8. **TestSensitivityUpdate** (3 tests)
   - Adapts based on experience
   - False alarms reduce sensitivity
   - Missed errors increase sensitivity

### API Integration

**Endpoints:**

```python
# Process event with error detection
POST /error_detection/process
{
  "response_strengths": [0.7, 0.3],  # Competing responses
  "actual_outcome": "A",
  "expected_outcome": "B",
  "confidence": 0.8
}

Response:
{
  "conflict_level": 0.42,
  "error_detected": true,
  "error_magnitude": 0.75,
  "ern_amplitude": 12.5,
  "correction": {
    "control_boost": 0.3,
    "post_error_slowing_ms": 35
  },
  "dopamine_rpe": -0.75,
  "norepinephrine_arousal_boost": 0.4
}

# Get system state
GET /error_detection/state

Response:
{
  "sensitivity": 0.68,
  "conflict_level": 0.42,
  "errors_detected": 23,
  "corrections_applied": 23,
  "detection_rate": 0.85,
  "false_alarm_rate": 0.12,
  "average_ern": 10.3
}
```

### Success Criteria

- ✅ 33/33 tests passing (100%)
- ✅ Conflict detection works
- ✅ Error detection accurate
- ✅ Dopamine RPE integrated (LAB_013)
- ✅ Norepinephrine arousal spike (LAB_015)
- ✅ Post-error slowing realistic
- ✅ API endpoints functional

---

## 📅 LAB_018: PLANNING & SEQUENCING

### Overview

**Type:** Higher-Order Executive Function (Diamond 2013)
**Neural Substrate:** Dorsolateral PFC (dlPFC), lateral frontal pole
**Function:** Multi-step planning, temporal sequencing, goal decomposition

### Biological Foundation

**Papers:**
- Koechlin & Hyafil (2007) - "Anterior prefrontal function and the limits of human decision-making"
- Badre & D'Esposito (2009) - "Is the rostro-caudal axis of the frontal lobe hierarchical?"

**Neurochemistry:**
- Dopamine (LAB_013): Motivation for planning, reward prediction
- Acetylcholine (LAB_016): Attention to relevant information
- Working Memory (LAB_011): Maintains plan steps

### Core Concepts

**Hierarchical Planning:**
- High-level goals decompose into sub-goals
- Sub-goals decompose into actions
- Tree structure: Goal → Sub-goals → Actions

**Temporal Sequencing:**
- Actions ordered in time
- Dependencies: Action B requires Action A complete
- Deadlines: Actions must complete by time T

**Plan Execution:**
- Monitor progress
- Detect deviations from plan
- Replan if necessary

### Implementation Design

**Class:** `PlanningSystem`

**Parameters:**
```python
baseline_planning_capacity: float = 0.6   # Baseline planning ability
max_plan_depth: int = 5                  # Maximum goal hierarchy depth
max_plan_length: int = 10                # Maximum action sequence length
sequencing_precision: float = 0.8        # Temporal ordering accuracy
replanning_threshold: float = 0.3        # When to trigger replanning
adaptation_rate: float = 0.1            # Learning rate
```

**State:**
```python
self.current_capacity: float             # Current planning capacity (0-1)
self.active_plan: Optional[Plan]         # Currently active plan
self.plan_history: List[Plan]            # Recent plans
self.total_plans_created: int           # Total plans generated
self.successful_plans: int              # Plans completed successfully
self.replanning_count: int              # Times replanning triggered
```

**Data Structures:**

```python
@dataclass
class Action:
    id: str
    description: str
    duration_estimate: float  # seconds
    dependencies: List[str]   # Action IDs that must complete first
    priority: float           # 0-1

@dataclass
class SubGoal:
    id: str
    description: str
    actions: List[Action]
    success_criteria: str

@dataclass
class Plan:
    goal: str
    sub_goals: List[SubGoal]
    total_estimated_time: float
    created_at: float
    status: str  # "active", "completed", "failed", "replanning"
```

**Methods:**

1. `create_plan(goal, constraints) -> Plan`
   - Inputs: High-level goal, constraints (time, resources)
   - Decomposes goal into sub-goals and actions
   - Creates hierarchical plan
   - Returns: Plan object

2. `sequence_actions(actions) -> List[Action]`
   - Inputs: Unordered actions
   - Orders actions respecting dependencies
   - Topological sort
   - Returns: Ordered action list

3. `estimate_duration(plan) -> float`
   - Computes total time for plan
   - Accounts for dependencies (parallel vs sequential)
   - Returns: Estimated duration (seconds)

4. `monitor_execution(plan, progress) -> Dict`
   - Inputs: Plan, current progress (which actions complete)
   - Checks if on track
   - Detects deviations
   - Returns: {on_track, deviation_magnitude, should_replan}

5. `trigger_replanning(original_plan, new_constraints) -> Plan`
   - Creates revised plan
   - Reuses successful sub-goals
   - Adapts to new constraints
   - Returns: Updated plan

6. `integrate_working_memory(plan) -> bool`
   - Checks if plan fits in working memory (LAB_011)
   - Working memory capacity: 7±2 items
   - If plan too complex, chunk into sub-plans
   - Returns: True if fits, False if needs chunking

7. `integrate_dopamine(dopamine_level) -> float`
   - High dopamine = more ambitious plans
   - Low dopamine = conservative plans
   - Returns: Planning capacity modulation

8. `integrate_acetylcholine(ach_level) -> float`
   - High ACh = better attention to plan details
   - Returns: Sequencing precision boost

9. `compute_plan_quality(plan) -> float`
   - Evaluates plan quality
   - Factors: feasibility, efficiency, robustness
   - Returns: Quality score (0-1)

10. `process_event(goal, constraints) -> Dict`
    - Main interface
    - Returns: {plan, quality, estimated_duration, fits_in_wm}

### Test Plan (35 tests)

**Test Suite:** `test_lab_018_planning.py`

**Test Classes:**

1. **TestInitialization** (3 tests)
2. **TestPlanCreation** (6 tests)
   - Simple goal creates basic plan
   - Complex goal creates hierarchical plan
   - Plan respects constraints
   - Max depth enforced
   - Max length enforced
3. **TestActionSequencing** (5 tests)
   - Sequences respect dependencies
   - Topological sort correct
   - Parallel actions identified
   - Circular dependencies detected
4. **TestDurationEstimation** (4 tests)
   - Sequential actions sum durations
   - Parallel actions use max duration
   - Estimation realistic
5. **TestExecutionMonitoring** (5 tests)
   - Detects plan deviations
   - On-track detection correct
   - Threshold triggering works
6. **TestReplanning** (4 tests)
   - Replanning triggered appropriately
   - New plan incorporates completed sub-goals
   - Replanning count tracked
7. **TestWorkingMemoryIntegration** (3 tests)
   - Complex plans exceed WM capacity
   - Chunking suggested when needed
   - Integration with LAB_011
8. **TestDopamineIntegration** (3 tests)
   - High dopamine = ambitious plans
   - Modulation realistic
9. **TestPlanQuality** (2 tests)

### API Integration

**Endpoints:**

```python
# Create plan for goal
POST /planning/create
{
  "goal": "Complete Layer 5A implementation",
  "constraints": {
    "max_time_hours": 6,
    "max_actions": 20
  }
}

Response:
{
  "plan": {
    "goal": "Complete Layer 5A implementation",
    "sub_goals": [
      {
        "id": "sg1",
        "description": "Implement LAB_019",
        "actions": [
          {"id": "a1", "description": "Write tests", "duration": 1800},
          {"id": "a2", "description": "Implement code", "duration": 3600, "dependencies": ["a1"]}
        ]
      },
      ...
    ],
    "total_estimated_time": 18000
  },
  "quality": 0.82,
  "fits_in_working_memory": false,
  "chunking_recommended": true
}

# Monitor plan execution
POST /planning/monitor
{
  "plan_id": "plan_123",
  "completed_actions": ["a1", "a2", "a3"]
}

Response:
{
  "on_track": true,
  "progress": 0.35,
  "deviation": 0.08,
  "should_replan": false,
  "estimated_remaining_time": 12000
}

# Get system state
GET /planning/state

Response:
{
  "planning_capacity": 0.68,
  "active_plan": {...},
  "total_plans": 47,
  "successful_plans": 39,
  "success_rate": 0.83,
  "replanning_count": 5
}
```

### Success Criteria

- ✅ 35/35 tests passing (100%)
- ✅ Hierarchical plans created correctly
- ✅ Action sequencing respects dependencies
- ✅ Execution monitoring works
- ✅ Replanning triggered appropriately
- ✅ Working memory integration (LAB_011)
- ✅ Dopamine + ACh modulation
- ✅ API endpoints functional

---

## 🎯 LAB_022: GOAL-DIRECTED BEHAVIOR

### Overview

**Type:** Integrative Higher-Order EF (Diamond 2013)
**Neural Substrate:** mPFC, OFC, dlPFC, ventral striatum
**Function:** Goal hierarchy, motivation, persistence, integration of cognition + emotion

### Biological Foundation

**Papers:**
- Balleine & O'Doherty (2010) - "Human and rodent homologies in action control"
- Daw et al. (2005) - "Uncertainty-based competition between prefrontal and dorsolateral striatal systems for behavioral control"

**Neurochemistry:**
- **ALL neurotransmitters integrated:**
  - Dopamine (LAB_013): Motivation, reward expectation
  - Serotonin (LAB_014): Patience for delayed rewards
  - Norepinephrine (LAB_015): Sustained arousal/persistence
  - Acetylcholine (LAB_016): Attention to goal-relevant information
  - GABA/Glutamate (LAB_017): E/I balance for stable pursuit

### Core Concepts

**Goal Hierarchy:**
- High-level goals (abstract)
- Mid-level sub-goals
- Low-level actions
- Example: "Get PhD" → "Pass quals" → "Study chapter 3"

**Model-Based vs Model-Free:**
- Model-based: Plan using world model (flexible, slow)
- Model-free: Cached action values (fast, habitual)
- Balance shifts based on: time pressure, confidence, familiarity

**Persistence:**
- Sustained goal pursuit despite obstacles
- Modulated by: expected value, sunk cost, alternative options

**Goal Shielding:**
- Protect active goal from distractors
- Inhibit competing goals
- Requires inhibitory control (LAB_019)

### Implementation Design

**Class:** `GoalDirectedBehaviorSystem`

**Parameters:**
```python
baseline_motivation: float = 0.6     # Baseline motivation level
goal_capacity: int = 5               # Max concurrent goals
persistence_factor: float = 0.8     # Resistance to giving up
model_based_weight: float = 0.6     # Weight for model-based (vs model-free)
goal_shielding_strength: float = 0.7  # Protection from distractors
adaptation_rate: float = 0.12       # Learning rate
```

**State:**
```python
self.current_motivation: float       # Current motivation level (0-1)
self.active_goals: List[Goal]        # Currently pursued goals
self.goal_hierarchy: Tree[Goal]      # Hierarchical goal structure
self.total_goals_set: int           # Lifetime goals set
self.goals_achieved: int            # Goals successfully completed
self.goals_abandoned: int           # Goals given up on
```

**Data Structures:**

```python
@dataclass
class Goal:
    id: str
    description: str
    level: str  # "high", "mid", "low"
    priority: float  # 0-1
    expected_value: float  # Reward expectation (0-1)
    effort_required: float  # 0-1
    deadline: Optional[float]  # seconds
    parent_goal: Optional[str]  # For hierarchy
    status: str  # "active", "completed", "abandoned", "paused"
    creation_time: float
    progress: float  # 0-1
```

**Methods:**

1. `set_goal(goal, parent_goal_id) -> str`
   - Creates new goal in hierarchy
   - Links to parent if specified
   - Returns: Goal ID

2. `compute_goal_value(goal) -> float`
   - Expected value - effort required
   - Modulated by deadline urgency
   - Temporal discounting applied (LAB_014 serotonin)
   - Returns: Net goal value

3. `select_active_goal(goals) -> Goal`
   - Chooses which goal to pursue now
   - Factors: priority, value, urgency
   - Returns: Selected goal

4. `update_motivation(goal_value, recent_progress) -> float`
   - Motivation increases with: high value, recent progress
   - Motivation decreases with: low value, lack of progress
   - Dopamine modulation applied (LAB_013)
   - Returns: Updated motivation

5. `compute_persistence(goal, obstacles_encountered) -> float`
   - Should continue pursuing goal?
   - Factors: sunk cost, expected value, alternatives
   - Serotonin modulation (patience)
   - Returns: Persistence strength (0-1)

6. `apply_goal_shielding(active_goal, distractors) -> List[float]`
   - Inhibits competing goals/distractors
   - Uses inhibitory control (LAB_019)
   - Returns: Distractor suppression strengths

7. `decide_model_based_vs_model_free(familiarity, time_pressure) -> str`
   - Chooses control mode
   - High familiarity + time pressure → model-free
   - Low familiarity + time available → model-based
   - Returns: "model_based" or "model_free"

8. `integrate_all_neurotransmitters() -> Dict`
   - Dopamine: Motivation, reward prediction
   - Serotonin: Patience, temporal discounting
   - Norepinephrine: Sustained arousal
   - Acetylcholine: Attention to goal
   - GABA/Glutamate: Stability
   - Returns: Modulation factors

9. `integrate_executive_functions() -> Dict`
   - Planning (LAB_018): Create action plan
   - Inhibitory Control (LAB_019): Shield from distractors
   - Flexibility (LAB_020): Switch goals if needed
   - Error Detection (LAB_021): Detect goal failures
   - Returns: EF contributions

10. `monitor_progress(goal, actions_completed) -> float`
    - Tracks progress toward goal
    - Updates progress field
    - Returns: Progress ratio (0-1)

11. `decide_abandonment(goal) -> bool`
    - Should abandon goal?
    - Factors: low value, high obstacles, better alternatives
    - Returns: True if should abandon

12. `process_event(goal_updates, context) -> Dict`
    - Main interface
    - Returns: {motivation, active_goal, persistence, progress, modulations}

### Test Plan (38 tests)

**Test Suite:** `test_lab_022_goal_directed_behavior.py`

**Test Classes:**

1. **TestInitialization** (3 tests)
2. **TestGoalSetting** (5 tests)
   - Goal created with correct structure
   - Hierarchy maintained
   - Priority ordering
   - Capacity limits enforced
3. **TestGoalValueComputation** (5 tests)
   - Value = expected_value - effort
   - Deadline urgency increases value
   - Temporal discounting applied (serotonin)
   - Value realistic
4. **TestGoalSelection** (4 tests)
   - Highest value goal selected
   - Priority breaks ties
   - Urgency considered
5. **TestMotivationUpdate** (5 tests)
   - Progress increases motivation
   - High value increases motivation
   - Dopamine modulation (LAB_013)
   - Motivation bounded [0, 1]
6. **TestPersistence** (5 tests)
   - High sunk cost increases persistence
   - Better alternatives decrease persistence
   - Serotonin modulation (patience)
   - Persistence realistic
7. **TestGoalShielding** (4 tests)
   - Active goal suppresses distractors
   - Uses inhibitory control (LAB_019)
   - Shielding strength configurable
8. **TestModelBasedVsModelFree** (3 tests)
   - Familiarity shifts to model-free
   - Time pressure shifts to model-free
   - Decision logic correct
9. **TestNeurotransmitterIntegration** (4 tests)
   - All 5 systems integrated
   - Modulations realistic
   - Integration with LAB_013-017
10. **TestExecutiveFunctionIntegration** (2 tests)
    - All core EFs integrated
    - LAB_018-021 contributions
11. **TestProgressMonitoring** (2 tests)
12. **TestGoalAbandonment** (1 test)

### API Integration

**Endpoints:**

```python
# Set new goal
POST /goal_directed_behavior/set_goal
{
  "description": "Complete LAYER_5A",
  "level": "high",
  "priority": 0.9,
  "expected_value": 0.85,
  "effort_required": 0.7,
  "deadline_hours": 6
}

Response:
{
  "goal_id": "goal_789",
  "goal_value": 0.68,
  "motivation_boost": 0.3,
  "estimated_completion_time": 21600
}

# Process goal pursuit event
POST /goal_directed_behavior/process
{
  "goal_id": "goal_789",
  "progress_update": 0.35,
  "obstacles_encountered": 2,
  "distractors": ["email", "slack"]
}

Response:
{
  "motivation": 0.74,
  "persistence": 0.81,
  "active_goal": "goal_789",
  "progress": 0.35,
  "goal_shielding": {
    "email": 0.85,
    "slack": 0.92
  },
  "control_mode": "model_based",
  "neurotransmitter_modulation": {
    "dopamine": 0.78,
    "serotonin": 0.82,
    "norepinephrine": 0.65,
    "acetylcholine": 0.71,
    "gaba_glutamate_ei_ratio": 0.73
  },
  "executive_functions": {
    "planning": 0.68,
    "inhibition": 0.75,
    "flexibility": 0.62,
    "error_detection": 0.58
  }
}

# Get system state
GET /goal_directed_behavior/state

Response:
{
  "motivation": 0.74,
  "active_goals": [...],
  "goal_hierarchy": {...},
  "total_goals_set": 123,
  "goals_achieved": 98,
  "goals_abandoned": 15,
  "achievement_rate": 0.796
}
```

### Success Criteria

- ✅ 38/38 tests passing (100%)
- ✅ Goal hierarchy managed correctly
- ✅ Motivation updates realistically
- ✅ Persistence modulation works
- ✅ Goal shielding effective
- ✅ All 5 neurotransmitter systems integrated (LAB_013-017)
- ✅ All 4 core EFs integrated (LAB_018-021)
- ✅ Model-based vs model-free decision works
- ✅ API endpoints functional
- ✅ **MOST COMPLEX LAB - INTEGRATES EVERYTHING**

---

## 📊 SUMMARY TABLE

| LAB | Name | Type | Tests | Lines (est.) | Complexity | Dependencies |
|-----|------|------|-------|--------------|------------|--------------|
| LAB_019 | Inhibitory Control | Core EF | 28 | 250-350 | Medium | LAB_014, LAB_017 |
| LAB_020 | Cognitive Flexibility | Core EF | 30 | 300-400 | Medium | LAB_013, LAB_015, LAB_016 |
| LAB_021 | Error Detection | Monitoring | 33 | 350-450 | Medium-High | LAB_013, LAB_015 |
| LAB_018 | Planning | Higher-Order | 35 | 400-500 | High | LAB_011, LAB_013, LAB_016 |
| LAB_022 | Goal-Directed | Integrative | 38 | 500-600 | Very High | ALL (LAB_013-021) |
| **TOTAL** | **5 LABs** | **Mixed** | **164** | **1,800-2,300** | **High** | **Complete integration** |

---

## 🔄 IMPLEMENTATION SEQUENCE

### Phase 1: Core EFs (LAB_019, LAB_020)

**Rationale:**
- Core EFs are well-defined
- Simpler than higher-order EFs
- Build confidence with TDD methodology in Layer 5

**Estimated time:** 2-2.5 hours

---

### Phase 2: Monitoring (LAB_021)

**Rationale:**
- Uses dopamine RPE (already implemented)
- Bridges core EFs and higher-order EFs
- Needed for LAB_022

**Estimated time:** 1.5-2 hours

---

### Phase 3: Higher-Order (LAB_018)

**Rationale:**
- Requires working memory integration (LAB_011)
- More complex than core EFs
- Needed for LAB_022

**Estimated time:** 1.5-2 hours

---

### Phase 4: Integrative (LAB_022)

**Rationale:**
- Integrates ALL previous LABs
- Most complex
- Grand finale

**Estimated time:** 2-2.5 hours

---

## ✅ GLOBAL SUCCESS CRITERIA

**Code:**
- ✅ All 164 tests passing (100% coverage)
- ✅ ~1,800-2,300 lines main code
- ✅ ~3,000-3,500 lines test code
- ✅ Clean architecture following patterns

**Integration:**
- ✅ All 5 neurotransmitter systems used (LAB_013-017)
- ✅ Working memory integrated (LAB_011)
- ✅ 10 new API endpoints (2 per LAB)
- ✅ Global instances initialized in main.py

**Documentation:**
- ✅ LAB_REGISTRY.json updated (v1.2 → v1.3)
  - total_labs_implemented: 23 → 28
  - completion_percentage: 44.2% → 53.8%
  - LAYER_5A status: "✅ operational (5/5 LABs - 100%)"
- ✅ TRACKING.md Session 18 added
- ✅ Git commit comprehensive

**Scientific Validity:**
- ✅ All LABs cite peer-reviewed papers
- ✅ Neurochemistry modulation realistic
- ✅ Behavioral patterns match literature
- ✅ Parameters within biological ranges

---

## 🎯 FINAL DELIVERABLE

**After completing all 5 LABs:**

```
LAYER_5A Executive Functions: ✅ OPERATIONAL (5/5 LABs - 100%)

├── LAB_018: Planning & Sequencing ✅
├── LAB_019: Inhibitory Control ✅
├── LAB_020: Cognitive Flexibility ✅
├── LAB_021: Error Detection & Correction ✅
└── LAB_022: Goal-Directed Behavior ✅

Total Tests: 164/164 passing (100%)
Total Code: ~5,000 lines (main + tests)
API Endpoints: 10 new endpoints
Integration: Complete (all neurotransmitters + core EFs)

CEREBRO_NEXUS_V3.0.0 Progress: 28/52 LABs (53.8%)
```

---

**Plan Status:** ✅ COMPLETE
**Ready for:** Implementation (LAB_019 first)
**Confidence:** HIGH (proven TDD methodology + solid neuroscience foundation)
**Estimated Total Time:** 5-6 hours autonomous execution

---

**Created by:** NEXUS AI (Session 18)
**Date:** November 7, 2025
**Next Action:** Begin LAB_019 Inhibitory Control implementation (TDD RED phase)
