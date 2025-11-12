# Session 22: Core Learning Systems (LAB_036-038)

**Fecha:** 2025-11-11
**Decisión:** Opción D (Score: 0.6942) - Análisis matemático multi-variable
**Objetivo:** Implementar 3 LABs fundamentales de aprendizaje avanzado
**Metodología:** TDD estricto (RED → GREEN → REFACTOR)

---

## 🎯 LABs a Implementar

### LAB_036: Intrinsic Motivation 🌱
**Neuroscience:** Self-Determination Theory (Ryan & Deci 2000)
**Function:** Curiosity, mastery, autonomy drives (non-reward-based)
**Tests:** 30 estimados

**Core Mechanisms:**
1. **Curiosity Drive** (epistemic)
   - Novelty-seeking behavior
   - Information gap detection
   - Exploration bonus

2. **Competence/Mastery**
   - Progress tracking
   - Skill improvement satisfaction
   - Optimal challenge (flow zone)

3. **Autonomy Preference**
   - Self-directed action reward
   - Control vs external constraint
   - Intrinsic vs extrinsic reward separation

**Integration:**
- ← LAB_004 (Novelty Detection) - drives curiosity
- ← LAB_037 (Curiosity Drive) - bidirectional feedback
- ← LAB_013 (Dopamine) - intrinsic reward signal

**Key Papers:**
- Ryan & Deci (2000) - Self-determination theory
- Oudeyer et al. (2007) - Intrinsic motivation in robots
- White (1959) - Competence motivation

**Implementation Plan:**

```python
class IntrinsicMotivationSystem:
    def __init__(self,
                 curiosity_weight=0.4,
                 mastery_weight=0.4,
                 autonomy_weight=0.2):
        # State
        self.current_curiosity = 0.0
        self.current_competence = 0.0
        self.current_autonomy = 0.0
        self.intrinsic_reward_history = []

    def compute_curiosity_drive(self, novelty_level, information_gap):
        """Epistemic curiosity (Berlyne 1960)"""
        # Inverted-U: moderate novelty = peak curiosity
        pass

    def compute_competence_motivation(self, skill_level, challenge_level):
        """Mastery drive (White 1959, flow theory)"""
        # Optimal challenge: skill ≈ challenge
        pass

    def compute_autonomy_preference(self, action_source):
        """Self-directed vs externally controlled"""
        # Higher reward for self-initiated actions
        pass

    def compute_intrinsic_reward(self):
        """Total intrinsic motivation"""
        # Weighted sum of 3 components
        pass
```

**Tests to Write (TDD - RED Phase):**
1. Initialization
   - Default parameters
   - Custom weights

2. Curiosity Drive
   - Inverted-U with novelty (moderate = peak)
   - Information gap increases curiosity
   - Integration with LAB_004

3. Competence/Mastery
   - Skill-challenge matching (flow)
   - Progress satisfaction
   - Suboptimal challenge reduces motivation

4. Autonomy
   - Self-directed > externally controlled
   - Autonomy weight modulation

5. Integration
   - Intrinsic vs extrinsic reward separation
   - Dopamine integration (LAB_013)
   - Curiosity drive feedback (LAB_037)

---

### LAB_037: Curiosity Drive 🔍
**Neuroscience:** Information-seeking, LC-NE, ACC, dopamine
**Function:** Exploration bonus, uncertainty reduction
**Tests:** 26 estimados

**Core Mechanisms:**
1. **Information Gap Detection**
   - Uncertainty quantification
   - Knowledge gap identification
   - Prediction error as curiosity signal

2. **Exploration Bonus**
   - Intrinsic reward for information-seeking
   - Exploration vs exploitation balance
   - Curiosity-driven action selection

3. **Uncertainty Reduction Drive**
   - Active learning
   - Query by uncertainty
   - Information gain maximization

**Integration:**
- ← LAB_004 (Novelty Detection) - novelty = high uncertainty
- ← LAB_013 (Dopamine) - curiosity rewarding (VTA)
- ↔ LAB_036 (Intrinsic Motivation) - bidirectional
- → LAB_015 (Norepinephrine) - arousal modulation

**Key Papers:**
- Kidd & Hayden (2015) - Curiosity psychology
- Gottlieb et al. (2013) - Information-seeking neuroscience
- Schmidhuber (1991) - Curiosity-driven learning

**Implementation Plan:**

```python
class CuriosityDriveSystem:
    def __init__(self,
                 exploration_bonus=0.1,
                 uncertainty_threshold=0.5):
        # State
        self.current_curiosity = 0.0
        self.knowledge_gaps = []
        self.exploration_history = []

    def detect_information_gap(self, query, knowledge_base):
        """Detect what we don't know"""
        # Uncertainty quantification
        pass

    def compute_curiosity_level(self, uncertainty, novelty):
        """Curiosity = f(uncertainty, novelty)"""
        # Inverted-U: moderate uncertainty = peak curiosity
        pass

    def compute_exploration_bonus(self, action_novelty):
        """Intrinsic reward for exploration"""
        # Bonus proportional to information gain
        pass

    def balance_explore_exploit(self, curiosity_level, task_value):
        """Explore vs exploit decision"""
        # High curiosity → explore
        # High task value → exploit
        pass
```

**Tests to Write (TDD - RED Phase):**
1. Information Gap Detection
   - Uncertainty quantification
   - Knowledge gap identification
   - Prediction error as signal

2. Curiosity Computation
   - Inverted-U with uncertainty
   - Novelty amplifies curiosity (LAB_004)
   - Zero uncertainty = low curiosity

3. Exploration Bonus
   - Information gain = intrinsic reward
   - Exploration history tracking

4. Explore-Exploit Balance
   - High curiosity biases exploration
   - Task value modulates balance
   - Integration with LAB_013 (dopamine)

5. Integration
   - Bidirectional with LAB_036
   - Novelty detection (LAB_004)
   - Arousal modulation (LAB_015)

---

### LAB_038: Meta-Learning 🧠📚
**Neuroscience:** Learning-to-learn, PFC, hippocampus
**Function:** Improve learning efficiency through experience
**Tests:** 28 estimados

**Core Mechanisms:**
1. **Learning Set Formation** (Harlow 1949)
   - Generalize learning strategies
   - "Learning-to-learn" improvement
   - Transfer across tasks

2. **Strategy Selection**
   - Identify optimal learning approach
   - Adapt strategy based on task structure
   - Meta-cognitive monitoring

3. **Learning Rate Adaptation**
   - Adjust learning rate based on task type
   - Fast vs slow learning contexts
   - Plasticity modulation

**Integration:**
- → LAB_040 (Skill Acquisition) - apply meta-learning
- → LAB_041 (Transfer Learning) - generalize strategies
- ← LAB_034 (Transfer) - build on transfer
- ← LAB_006 (Metacognition) - monitor learning

**Key Papers:**
- Harlow (1949) - The formation of learning sets
- Schmidhuber (2015) - Meta-learning survey
- Thrun & Pratt (1998) - Learning to learn

**Implementation Plan:**

```python
class MetaLearningSystem:
    def __init__(self,
                 adaptation_rate=0.1):
        # State
        self.learning_sets = {}  # Task type → strategy
        self.learning_history = []
        self.current_strategy = None

    def form_learning_set(self, task_type, outcomes):
        """Extract generalizable learning strategy"""
        # Harlow (1949): improve across similar tasks
        pass

    def select_learning_strategy(self, task_structure):
        """Choose optimal strategy for task"""
        # Match task to learned strategy
        pass

    def adapt_learning_rate(self, task_type, performance):
        """Modulate learning rate meta-parameter"""
        # Fast learning for known task types
        # Slow for novel structures
        pass

    def transfer_strategy(self, source_task, target_task):
        """Apply learned strategy to new task"""
        # Similarity-based transfer
        pass
```

**Tests to Write (TDD - RED Phase):**
1. Learning Set Formation
   - Multiple trials improve performance
   - Generalization across similar tasks
   - Harlow (1949) learning-to-learn curve

2. Strategy Selection
   - Match task structure to strategy
   - Novel tasks = exploratory strategy
   - Known tasks = efficient strategy

3. Learning Rate Adaptation
   - Modulate based on task familiarity
   - Fast for known, slow for novel
   - Performance feedback integration

4. Transfer
   - Strategy transfer between tasks
   - Similarity-based generalization
   - Integration with LAB_034

5. Meta-Cognition
   - Monitor learning effectiveness
   - Strategy switching on failure
   - Integration with LAB_006

---

## 📊 Success Criteria

### Tests (TDD)
- [ ] LAB_036: 30/30 tests passing (100%)
- [ ] LAB_037: 26/26 tests passing (100%)
- [ ] LAB_038: 28/28 tests passing (100%)
- [ ] **Total: 84/84 tests passing**

### Code Quality
- [ ] Full docstrings (Google style)
- [ ] Type hints (Python 3.11+)
- [ ] Integration points documented
- [ ] Paper references in code comments

### Integration
- [ ] LAB_036 ↔ LAB_037 bidirectional working
- [ ] LAB_004 (novelty) → LAB_037 (curiosity)
- [ ] LAB_013 (dopamine) → intrinsic rewards
- [ ] LAB_006 (metacognition) ← LAB_038

### Documentation
- [ ] Git commit with metrics
- [ ] TRACKING.md updated
- [ ] LAB_REGISTRY.json updated (35 → 38 LABs, 73.1%)

---

## 🔄 Workflow

### Phase 1: EXPLORAR ✅
- [x] Análisis matemático de opciones
- [x] Selección óptima: LAB_036-038
- [x] Plan creado en tasks/

### Phase 2: PLANIFICAR
**LAB_036:**
1. Write 30 tests FIRST (RED)
2. Implement curiosity/mastery/autonomy
3. Validate integration LAB_004, LAB_037

**LAB_037:**
1. Write 26 tests FIRST (RED)
2. Implement information gap detection
3. Validate explore-exploit balance

**LAB_038:**
1. Write 28 tests FIRST (RED)
2. Implement learning sets (Harlow)
3. Validate strategy transfer

### Phase 3: CODIFICAR (TDD)
**For each LAB:**
1. RED: Write failing tests
2. GREEN: Implement minimum code to pass
3. REFACTOR: Clean up, optimize
4. INTEGRATE: Test with existing LABs

### Phase 4: CONFIRMAR
1. Run full test suite (84 tests)
2. Git commit with detailed message
3. Update TRACKING.md (Session 22)
4. Update LAB_REGISTRY.json

---

## 🎯 Estimated Timeline

| Phase | Duration | Output |
|-------|----------|--------|
| EXPLORAR | ✅ Done | Plan created |
| PLANIFICAR | 0.5h | Detailed design |
| CODIFICAR LAB_036 | 1.5h | 30 tests + impl |
| CODIFICAR LAB_037 | 1.3h | 26 tests + impl |
| CODIFICAR LAB_038 | 1.5h | 28 tests + impl |
| CONFIRMAR | 0.3h | Commit + docs |
| **TOTAL** | **~5.1h** | **3 LABs complete** |

---

## 📚 Papers Reference List

1. **Ryan & Deci (2000)** - Self-determination theory
2. **Oudeyer et al. (2007)** - Intrinsic motivation in developmental robotics
3. **White (1959)** - Motivation reconsidered: The concept of competence
4. **Kidd & Hayden (2015)** - The psychology and neuroscience of curiosity
5. **Gottlieb et al. (2013)** - Information-seeking, curiosity, and attention
6. **Schmidhuber (1991)** - A possibility for implementing curiosity and boredom
7. **Harlow (1949)** - The formation of learning sets
8. **Thrun & Pratt (1998)** - Learning to learn

---

**STATUS:** Ready to begin Phase 2 (PLANIFICAR) → Phase 3 (CODIFICAR)
