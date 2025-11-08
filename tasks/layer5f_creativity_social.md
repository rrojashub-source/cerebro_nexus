# LAYER_5F: Creativity & Social Cognition - Implementation Plan

**Date:** November 7, 2025
**Session:** 19 (continuation of Session 18)
**Methodology:** NEXUS TDD (RED → GREEN → REFACTOR)
**Goal:** Implement 6 LABs (4 Creativity + 2 Social Cognition) with full test coverage

---

## Overview

**LABs to implement:**
- **Creativity (4 LABs):** LAB_023-026
- **Social Cognition (2 LABs):** LAB_027-028

**Total scope:** 6 LABs, ~120-150 tests, 12 API endpoints

---

## Implementation Order (Dependency-Based)

```
Creativity Track:
LAB_023 (Divergent Thinking) → Foundation
  ↓
LAB_024 (Conceptual Blending) → Builds on 023
  ↓
LAB_025 (Insight) → Uses 024 for restructuring
  ↓
LAB_026 (Dream Logic) → Independent (uses LAB_001, LAB_003)

Social Track:
LAB_027 (Theory of Mind) → Foundation social cognition
  ↓
LAB_028 (Empathy) → Builds on 027 (cognitive → affective empathy)
```

**Rationale:**
1. **LAB_023 first** - Foundational for creativity, no dependencies
2. **LAB_024 second** - Uses LAB_023 outputs as inputs
3. **LAB_025 third** - Uses LAB_024 blending for problem restructuring
4. **LAB_026 fourth** - Independent (can be done anytime)
5. **LAB_027 fifth** - Foundational for social, no dependencies
6. **LAB_028 sixth** - Uses LAB_027 ToM for empathy

---

## LAB_023: Divergent Thinking Engine

### Specification

**Function:** Generate multiple creative solutions through remote associations

**Class:** `DivergentThinkingSystem`

**Parameters:**
```python
def __init__(
    self,
    semantic_distance_threshold: float = 0.6,  # Min distance for "creative"
    inhibition_strength: float = 0.7,          # Suppress conventional
    generation_time: float = 60.0,             # Seconds for idea generation
    fluency_weight: float = 0.3,               # Weight for number of ideas
    flexibility_weight: float = 0.4,           # Weight for category diversity
    originality_weight: float = 0.3            # Weight for novelty
)
```

**Core Methods:**

1. **`generate_ideas(prompt: str, n_ideas: int = 10) -> List[str]`**
   - Generate multiple ideas for prompt
   - Use semantic distance to filter conventional
   - Return diverse set

2. **`compute_semantic_distance(idea: str, context: str) -> float`**
   - Measure conceptual distance
   - Simulated: Hash-based distance (production: embedding similarity)
   - Range: 0.0 (identical) to 1.0 (completely unrelated)

3. **`inhibit_conventional(ideas: List[str], threshold: float) -> List[str]`**
   - Integration with LAB_019 (Inhibitory Control)
   - Filter out obvious/first associations
   - Keep only remote associations

4. **`score_fluency(ideas: List[str]) -> float`**
   - Count total valid ideas
   - Guilford metric

5. **`score_flexibility(ideas: List[str]) -> float`**
   - Count distinct conceptual categories
   - Simulated: word clustering

6. **`score_originality(ideas: List[str]) -> float`**
   - Statistical rarity metric
   - Simulated: inverse frequency

7. **`process_event(prompt: str) -> Dict`**
   - Main interface: generate + score
   - Return comprehensive creativity metrics

**State:**
```python
self.total_prompts_processed: int
self.total_ideas_generated: int
self.avg_fluency: float
self.avg_flexibility: float
self.avg_originality: float
```

### Test Plan (25 tests)

**Initialization (3 tests):**
- test_default_initialization
- test_custom_parameters
- test_state_initialization

**Idea Generation (6 tests):**
- test_generates_ideas
- test_generates_requested_number
- test_ideas_are_diverse
- test_no_duplicate_ideas
- test_empty_prompt_returns_empty
- test_semantic_distance_filtering

**Scoring (9 tests):**
- test_fluency_score_increases_with_ideas
- test_flexibility_score_with_diverse_categories
- test_originality_score_higher_for_novel
- test_combined_creativity_score
- test_zero_ideas_zero_scores
- test_single_idea_minimal_flexibility
- test_all_same_category_low_flexibility
- test_very_novel_idea_high_originality
- test_conventional_ideas_low_originality

**Integration (4 tests):**
- test_inhibition_filters_conventional
- test_gaba_modulation_reduces_inhibition (LAB_017)
- test_inhibitory_control_integration (LAB_019)
- test_low_inhibition_more_ideas

**Process Event (3 tests):**
- test_process_event_complete
- test_process_event_updates_stats
- test_process_event_returns_best_ideas

### API Integration

**Endpoints:**
```python
POST /divergent_thinking/generate
Request: {
  "prompt": "Alternative uses for a brick",
  "n_ideas": 10
}
Response: {
  "ideas": ["paperweight", "doorstop", "hammer", ...],
  "fluency_score": 10.0,
  "flexibility_score": 7.0,
  "originality_score": 0.68,
  "creativity_score": 0.71,
  "most_novel_idea": "use as a thermal mass for greenhouse"
}

GET /divergent_thinking/state
Response: {
  "total_prompts": 15,
  "total_ideas": 127,
  "avg_fluency": 8.5,
  "avg_flexibility": 6.2,
  "avg_originality": 0.64
}
```

---

## LAB_024: Conceptual Blending

### Specification

**Function:** Create novel concepts through metaphor, analogy, blending

**Class:** `ConceptualBlendingSystem`

**Parameters:**
```python
def __init__(
    self,
    structural_similarity_threshold: float = 0.5,  # Min similarity for mapping
    blend_novelty_weight: float = 0.6,             # Favor surprising blends
    coherence_weight: float = 0.4,                 # Favor coherent blends
    max_blend_complexity: int = 2                  # Max input spaces
)
```

**Core Methods:**

1. **`map_conceptual_spaces(concept_a: Dict, concept_b: Dict) -> Dict`**
   - Find structural correspondences (Structure Mapping Theory)
   - Align relations (not just features)
   - Return mapping dict

2. **`compute_structural_similarity(concept_a: Dict, concept_b: Dict) -> float`**
   - Measure relational alignment
   - Simulated: overlap of "structure" keys

3. **`blend_concepts(concept_a: Dict, concept_b: Dict) -> Dict`**
   - Fauconnier & Turner blending
   - Generic space + emergent structure
   - Return blended concept

4. **`generate_metaphor(source: str, target: str, relation: str) -> str`**
   - "X is like Y because Z"
   - Template-based metaphor generation

5. **`generate_analogies(concept: Dict, n: int = 3) -> List[str]`**
   - Find analogous concepts
   - Based on structural similarity

6. **`score_coherence(blend: Dict) -> float`**
   - Internal consistency check
   - Simulated: no contradictions

7. **`score_novelty(blend: Dict) -> float`**
   - Emergent properties not in inputs
   - Surprise factor

**State:**
```python
self.total_blends_created: int
self.successful_blends: int
self.avg_coherence: float
self.avg_novelty: float
```

### Test Plan (28 tests)

**Initialization (3 tests):**
- test_default_initialization
- test_custom_parameters
- test_state_initialization

**Conceptual Mapping (6 tests):**
- test_maps_structural_similarities
- test_finds_relational_correspondences
- test_no_mapping_for_dissimilar
- test_partial_mapping_for_partial_similarity
- test_alignment_quality_metric
- test_one_to_many_mapping_forbidden

**Blending (8 tests):**
- test_blends_two_concepts
- test_generic_space_extraction
- test_emergent_structure_creation
- test_blend_preserves_key_relations
- test_blend_novelty_higher_than_inputs
- test_blend_coherence_maintained
- test_failed_blend_for_incompatible
- test_blend_with_divergent_ideas (LAB_023 integration)

**Metaphor Generation (5 tests):**
- test_generates_metaphor
- test_metaphor_format_correct
- test_metaphor_relation_meaningful
- test_metaphor_from_blend
- test_multiple_metaphors_for_blend

**Analogy Generation (3 tests):**
- test_generates_analogies
- test_analogies_structurally_similar
- test_analogy_diversity

**Process Event (3 tests):**
- test_process_event_complete
- test_process_event_updates_stats
- test_process_event_with_low_similarity_fails

### API Integration

**Endpoints:**
```python
POST /conceptual_blending/blend
Request: {
  "concept_a": {"type": "atom", "structure": {"center": "nucleus", "orbiting": "electrons"}},
  "concept_b": {"type": "solar_system", "structure": {"center": "sun", "orbiting": "planets"}}
}
Response: {
  "blend": {"type": "planetary_atom", "structure": {"center": "nucleus", "orbiting": "electrons", "emergent": "quantization"}},
  "metaphor": "An atom is like a solar system because both have orbiting bodies around a center",
  "analogies": ["galaxy structure", "dance around maypole"],
  "coherence_score": 0.82,
  "novelty_score": 0.71
}

GET /conceptual_blending/state
```

---

## LAB_025: Insight & Aha Moments

### Specification

**Function:** Sudden insight through problem restructuring, impasse breaking

**Class:** `InsightSystem`

**Parameters:**
```python
def __init__(
    self,
    impasse_threshold: int = 3,                # Failed attempts to trigger incubation
    incubation_duration: float = 120.0,        # Seconds for unconscious processing
    aha_confidence_threshold: float = 0.8,     # Confidence to signal insight
    restructuring_rate: float = 0.15           # Rate of problem space exploration
)
```

**Core Methods:**

1. **`detect_impasse(failed_attempts: int, progress: float) -> bool`**
   - Recognize stuck state
   - Threshold-based detection

2. **`initiate_incubation(problem: Dict) -> float`**
   - Reduce focused attention
   - Return incubation time needed

3. **`restructure_problem(problem: Dict, approach: str) -> Dict`**
   - Change representation
   - Integration with LAB_024 (Conceptual Blending for reframe)
   - Types: constraint_relaxation, analogy, decomposition

4. **`detect_solution_emergence(restructured: Dict, original: Dict) -> bool`**
   - Check if restructuring revealed solution
   - Confidence spike detection

5. **`generate_aha_signal(confidence: float) -> Dict`**
   - Subjective insight feeling
   - Integration with LAB_013 (Dopamine burst)
   - Intensity proportional to confidence spike

6. **`compute_warmth(progress_history: List[float]) -> float`**
   - Metcalfe & Wiebe warmth ratings
   - Analytic: gradual increase
   - Insight: flat then spike

**State:**
```python
self.total_problems_attempted: int
self.insights_achieved: int
self.avg_solving_time: float
self.insight_success_rate: float
```

### Test Plan (30 tests)

**Initialization (3 tests):**
- test_default_initialization
- test_custom_parameters
- test_state_initialization

**Impasse Detection (5 tests):**
- test_detects_impasse_after_threshold
- test_no_impasse_with_progress
- test_impasse_with_repeated_failures
- test_impasse_requires_both_failures_and_no_progress
- test_impasse_counter_resets_on_progress

**Incubation (4 tests):**
- test_initiates_incubation
- test_incubation_duration_variable
- test_incubation_reduces_focused_attention
- test_incubation_integration_with_dmn (future LAB_046)

**Problem Restructuring (8 tests):**
- test_restructures_problem
- test_constraint_relaxation
- test_analogical_restructuring (LAB_024 integration)
- test_problem_decomposition
- test_restructuring_changes_representation
- test_invalid_restructuring_approach_fails
- test_multiple_restructuring_attempts
- test_restructuring_with_conceptual_blend

**Solution Emergence (5 tests):**
- test_detects_solution_after_restructuring
- test_no_solution_without_restructuring
- test_confidence_spike_indicates_insight
- test_false_positive_low_confidence_rejected
- test_solution_verification

**Aha Signal (5 tests):**
- test_generates_aha_signal
- test_aha_intensity_proportional_to_confidence
- test_dopamine_burst_on_aha (LAB_013)
- test_no_aha_for_gradual_solving
- test_aha_distinct_from_regular_success

**Warmth Ratings (3 tests):**
- test_warmth_gradual_for_analytic
- test_warmth_flat_then_spike_for_insight
- test_warmth_distinguishes_solving_types

### API Integration

**Endpoints:**
```python
POST /insight/solve_problem
Request: {
  "problem": {"description": "...", "constraints": [...], "attempts": 5},
  "allow_incubation": true
}
Response: {
  "insight_occurred": true,
  "solution": "Restructured solution approach",
  "aha_intensity": 0.89,
  "solving_time": 145.2,
  "restructuring_type": "constraint_relaxation",
  "warmth_history": [0.2, 0.2, 0.3, 0.9]
}

GET /insight/state
```

---

## LAB_026: Dream Logic

### Specification

**Function:** Unconstrained association, surreal combinations (REM-like)

**Class:** `DreamLogicSystem`

**Parameters:**
```python
def __init__(
    self,
    logical_constraint_strength: float = 0.1,  # 0 = dream, 1 = awake logic
    emotional_connection_weight: float = 0.8,  # Emotion drives associations
    bizarreness_tolerance: float = 0.9,        # Allow unusual combinations
    consolidation_rate: float = 0.05           # Memory consolidation strength
)
```

**Core Methods:**

1. **`suspend_logical_constraints() -> float`**
   - Reduce consistency checking
   - Return constraint strength (low = dream-like)

2. **`associate_by_emotion(memories: List[Dict]) -> List[Tuple]`**
   - Integration with LAB_001 (Emotional Salience)
   - Connect by emotional similarity (not semantic)
   - Formula: `similarity = emotional_overlap(mem_A, mem_B)`

3. **`generate_bizarre_combination(fragments: List[Dict]) -> Dict`**
   - Mix unrelated elements
   - Allow contradictions
   - Surreal narrative generation

4. **`offline_consolidation(memories: List[Dict]) -> List[Dict]`**
   - Integration with LAB_003 (Sleep Consolidation)
   - Reactivate and recombine
   - Pattern extraction

5. **`score_bizarreness(narrative: Dict) -> float`**
   - Measure surrealism
   - Count contradictions, impossibilities

6. **`extract_novel_connections(narrative: Dict) -> List[Tuple]`**
   - Find new associations created by dream
   - Potential creative insights

**State:**
```python
self.total_dream_sessions: int
self.novel_connections_found: int
self.avg_bizarreness: float
```

### Test Plan (24 tests)

**Initialization (3 tests):**
- test_default_initialization
- test_custom_parameters
- test_state_initialization

**Logical Constraint Suspension (4 tests):**
- test_suspends_logical_constraints
- test_dream_mode_low_constraint
- test_wake_mode_high_constraint
- test_constraint_strength_affects_bizarreness

**Emotional Association (6 tests):**
- test_associates_by_emotion (LAB_001)
- test_emotion_overrides_semantic_distance
- test_similar_emotions_connect_unrelated
- test_emotional_themes_emerge
- test_emotional_connection_weight_modulation
- test_no_association_with_opposite_emotions

**Bizarre Combinations (5 tests):**
- test_generates_bizarre_combinations
- test_allows_contradictions
- test_surreal_narrative_creation
- test_bizarreness_increases_with_tolerance
- test_waking_logic_rejects_bizarreness

**Memory Consolidation (3 tests):**
- test_offline_consolidation (LAB_003)
- test_pattern_extraction
- test_consolidation_strengthens_connections

**Novel Connections (3 tests):**
- test_extracts_novel_connections
- test_novel_connections_available_on_wake
- test_creative_insights_from_dream

### API Integration

**Endpoints:**
```python
POST /dream_logic/generate
Request: {
  "memory_fragments": [{"content": "...", "emotion": "fear"}, ...],
  "mode": "dream"  # or "wake"
}
Response: {
  "dream_narrative": "Surreal narrative with bizarre combinations",
  "memory_fragments_used": 7,
  "emotional_themes": ["fear", "joy"],
  "novel_connections": [("concept_A", "concept_B", 0.73)],
  "bizarreness_score": 0.82
}

GET /dream_logic/state
```

---

## LAB_027: Theory of Mind

### Specification

**Function:** Infer mental states of others (beliefs, desires, intentions)

**Class:** `TheoryOfMindSystem`

**Parameters:**
```python
def __init__(
    self,
    belief_confidence_threshold: float = 0.6,  # Min confidence for attribution
    max_recursion_depth: int = 3,              # "I think you think..." depth
    context_weight: float = 0.7,               # Context influence on inference
    false_belief_sensitivity: float = 0.8      # Detect belief ≠ reality
)
```

**Core Methods:**

1. **`represent_belief(agent_id: str, content: str, confidence: float) -> Dict`**
   - Track belief state (may differ from reality)
   - Data structure: {agent_id, belief_content, confidence, is_false_belief}

2. **`attribute_intention(action: str, context: Dict) -> str`**
   - Infer goal from observed action
   - Bayesian inference: P(intention | action, context)

3. **`recursive_belief_modeling(depth: int, agent_chain: List[str]) -> Dict`**
   - "I think you think I think..."
   - Depth 1: I know X
   - Depth 2: I know you know X
   - Depth 3: I know you know I know X

4. **`detect_false_belief(belief: Dict, reality: Dict) -> bool`**
   - Critical for ToM: belief ≠ reality
   - Sally-Anne task implementation

5. **`predict_behavior(mental_state: Dict) -> str`**
   - Given beliefs/desires/intentions → predict action
   - Integration with LAB_007 (Predictive Preloading)

6. **`update_belief_from_observation(agent_id: str, observation: str) -> Dict`**
   - Bayesian belief updating
   - Confidence adjustment

**State:**
```python
self.agents_tracked: Dict[str, Dict]  # belief states per agent
self.total_predictions: int
self.prediction_accuracy: float
self.false_beliefs_detected: int
```

### Test Plan (32 tests)

**Initialization (3 tests):**
- test_default_initialization
- test_custom_parameters
- test_state_initialization

**Belief Representation (7 tests):**
- test_represents_belief
- test_tracks_multiple_agents
- test_belief_confidence_tracking
- test_belief_can_differ_from_reality
- test_belief_update_increases_confidence
- test_contradictory_beliefs_handled
- test_agent_belief_independence

**Intention Attribution (6 tests):**
- test_attributes_intention_from_action
- test_context_influences_attribution
- test_ambiguous_action_low_confidence
- test_clear_action_high_confidence
- test_multiple_possible_intentions
- test_intention_updates_with_new_evidence

**Recursive Belief Modeling (5 tests):**
- test_first_order_belief (I know X)
- test_second_order_belief (I know you know X)
- test_third_order_belief (I know you know I know X)
- test_recursion_depth_limit
- test_recursive_confidence_degradation

**False Belief Detection (6 tests):**
- test_detects_false_belief
- test_sally_anne_task
- test_false_belief_when_belief_ne_reality
- test_no_false_belief_when_aligned
- test_false_belief_sensitivity_threshold
- test_false_belief_affects_prediction

**Behavior Prediction (5 tests):**
- test_predicts_behavior_from_mental_state
- test_false_belief_leads_to_incorrect_behavior_prediction
- test_true_belief_leads_to_correct_behavior_prediction
- test_prediction_confidence_from_belief_confidence
- test_prediction_integration_with_preloading (LAB_007)

### API Integration

**Endpoints:**
```python
POST /theory_of_mind/infer_mental_state
Request: {
  "agent_id": "agent_1",
  "observed_behavior": "Agent looks in box A",
  "context": {"object_location": "box_B", "agent_saw_move": false}
}
Response: {
  "mental_state": {
    "belief": "Object is in box A",
    "desire": "Find object",
    "intention": "Search box A"
  },
  "confidence": 0.85,
  "false_belief_detected": true,
  "predicted_behavior": "Will search box A (incorrect)",
  "recursion_depth": 2
}

GET /theory_of_mind/state
```

---

## LAB_028: Empathy Simulation

### Specification

**Function:** Affective empathy, emotional resonance, compassion

**Class:** `EmpathySystem`

**Parameters:**
```python
def __init__(
    self,
    mirroring_intensity: float = 0.7,           # How strongly to mirror
    self_other_boundary_strength: float = 0.8,  # Prevent contagion
    compassion_threshold: float = 0.6,          # Threshold for prosocial action
    distress_tolerance: float = 0.7             # Max vicarious suffering
)
```

**Core Methods:**

1. **`mirror_emotion(observed_emotion: Dict) -> Dict`**
   - Simulate other's emotion internally
   - Integration with LAB_008 (Emotional Contagion)
   - Formula: `empathic_emotion = observed * mirroring_intensity`

2. **`maintain_self_other_boundary(emotion: Dict) -> Dict`**
   - Critical: Distinguish "their pain" from "my pain"
   - Add "source" tag to emotion (self vs. other)
   - Prevent overwhelming contagion

3. **`generate_compassionate_response(empathic_emotion: Dict) -> str`**
   - Prosocial motivation
   - Integration with LAB_013 (Dopamine - prosocial reward)
   - Types: offer_help, comfort, advocacy

4. **`regulate_empathic_distress(distress_level: float) -> float`**
   - Prevent burnout
   - Integration with LAB_014 (Serotonin - emotion regulation)
   - If distress > tolerance → reduce mirroring

5. **`distinguish_empathy_types(situation: Dict) -> str`**
   - Cognitive empathy (ToM - understand what they feel)
   - Affective empathy (this LAB - feel what they feel)
   - Compassionate empathy (motivated to help)

6. **`compute_empathic_accuracy(mirrored: Dict, actual: Dict) -> float`**
   - How well mirroring matches actual emotion
   - Accuracy metric

**State:**
```python
self.total_empathic_events: int
self.prosocial_actions_triggered: int
self.avg_empathic_accuracy: float
self.distress_regulation_count: int
```

### Test Plan (30 tests)

**Initialization (3 tests):**
- test_default_initialization
- test_custom_parameters
- test_state_initialization

**Emotional Mirroring (7 tests):**
- test_mirrors_observed_emotion (LAB_008)
- test_mirroring_intensity_modulation
- test_mirrors_multiple_emotions
- test_mirroring_preserves_emotion_type
- test_mirroring_intensity_affects_strength
- test_no_mirroring_with_zero_intensity
- test_partial_mirroring_with_medium_intensity

**Self/Other Distinction (6 tests):**
- test_maintains_self_other_boundary
- test_emotion_tagged_with_source
- test_high_boundary_prevents_contagion
- test_low_boundary_allows_contagion
- test_distinguish_my_pain_from_their_pain
- test_boundary_failure_leads_to_overwhelm

**Compassionate Response (5 tests):**
- test_generates_compassionate_response
- test_prosocial_action_above_threshold
- test_no_action_below_threshold
- test_dopamine_reward_for_prosocial (LAB_013)
- test_response_type_matches_situation

**Empathic Distress Regulation (5 tests):**
- test_regulates_excessive_distress (LAB_014)
- test_distress_above_tolerance_triggers_regulation
- test_regulation_reduces_mirroring
- test_serotonin_modulation_of_regulation
- test_regulation_prevents_burnout

**Empathy Types (4 tests):**
- test_distinguishes_cognitive_vs_affective
- test_cognitive_empathy_uses_tom (LAB_027)
- test_affective_empathy_uses_mirroring
- test_compassionate_empathy_includes_motivation

### API Integration

**Endpoints:**
```python
POST /empathy/process
Request: {
  "observed_emotion": {"type": "sadness", "intensity": 0.75, "context": "lost_job"},
  "agent_id": "person_1"
}
Response: {
  "empathic_emotion": {
    "type": "sadness",
    "intensity": 0.53,  # mirrored * 0.7
    "source": "other"
  },
  "self_other_distinction": 0.85,
  "prosocial_motivation": 0.68,
  "compassionate_action": "offer_emotional_support",
  "empathic_distress_level": 0.42,
  "regulation_active": false
}

GET /empathy/state
```

---

## Integration Summary

### Neurochemistry Integration

| LAB | Integrates With | Mechanism |
|-----|-----------------|-----------|
| LAB_023 | LAB_017 (GABA/Glu) | Low inhibition → more creative ideas |
| LAB_023 | LAB_019 (Inhibition) | Suppress conventional responses |
| LAB_025 | LAB_013 (Dopamine) | Aha moment → dopamine burst (reward) |
| LAB_026 | LAB_001 (Emotion) | Emotional salience drives dream associations |
| LAB_026 | LAB_003 (Sleep) | Offline consolidation during REM |
| LAB_028 | LAB_013 (Dopamine) | Prosocial action → dopamine reward |
| LAB_028 | LAB_014 (Serotonin) | Empathic distress regulation |

### Executive Function Integration

| LAB | Integrates With | Mechanism |
|-----|-----------------|-----------|
| LAB_024 | LAB_023 (Divergent) | Blend divergent ideas into novel concepts |
| LAB_025 | LAB_024 (Blending) | Use blending for problem restructuring |
| LAB_027 | LAB_007 (Predictive) | Predict behavior from mental states |
| LAB_027 | LAB_020 (Flexibility) | Switch perspectives in ToM |
| LAB_028 | LAB_027 (ToM) | Cognitive empathy (understand) + affective empathy (feel) |

### Cognitive Loop Integration

| LAB | Integrates With | Mechanism |
|-----|-----------------|-----------|
| LAB_026 | LAB_008 (Contagion) | Dream associations like emotional contagion |
| LAB_027 | LAB_012 (Future Think) | Simulate others' future mental states |
| LAB_028 | LAB_008 (Contagion) | Emotional mirroring mechanism |

---

## API Design Pattern

All LABs follow consistent pattern:

**POST endpoint:** `/{lab_name}/process` or `/{lab_name}/{action}`
- Main processing function
- Returns comprehensive result + integrations

**GET endpoint:** `/{lab_name}/state`
- Current system state
- Statistics, metrics

**Total endpoints:** 12 (2 per LAB × 6 LABs)

---

## Testing Strategy

### TDD Methodology (RED → GREEN → REFACTOR)

**For each LAB:**

1. **RED Phase:**
   - Write all tests FIRST (based on specification)
   - Tests will FAIL (code doesn't exist yet)
   - Verify failures are expected

2. **GREEN Phase:**
   - Implement minimum code to pass tests
   - Run tests frequently
   - Iterate until all tests pass

3. **REFACTOR Phase:**
   - Optimize code (performance, readability)
   - Add error handling
   - Keep tests passing

### Test Coverage Goals

- **Initialization tests:** 3 per LAB (18 total)
- **Core mechanism tests:** 15-20 per LAB (90-120 total)
- **Integration tests:** 5-7 per LAB (30-42 total)
- **Total tests:** ~140-180 tests

### Test Categories

1. **Unit tests:** Individual methods work correctly
2. **Integration tests:** LAB integrates with existing systems
3. **Edge case tests:** Boundary conditions, invalid inputs
4. **Biological realism tests:** Behavior matches neuroscience

---

## Implementation Checklist

### LAB_023 (Divergent Thinking):
- [ ] Create `experiments/LAYER_5_Higher_Cognition/Creativity_Social/LAB_023_Divergent_Thinking/`
- [ ] Implement `divergent_thinking_system.py`
- [ ] Write `tests/unit/labs/test_lab_023_divergent_thinking.py`
- [ ] Run TDD cycle (RED → GREEN → REFACTOR)
- [ ] Integrate API endpoints in `src/api/main.py`
- [ ] Verify integration with LAB_017, LAB_019

### LAB_024 (Conceptual Blending):
- [ ] Create folder structure
- [ ] Implement `conceptual_blending_system.py`
- [ ] Write `test_lab_024_conceptual_blending.py`
- [ ] TDD cycle
- [ ] API integration
- [ ] Verify integration with LAB_023

### LAB_025 (Insight):
- [ ] Create folder structure
- [ ] Implement `insight_system.py`
- [ ] Write `test_lab_025_insight.py`
- [ ] TDD cycle
- [ ] API integration
- [ ] Verify integration with LAB_013, LAB_024

### LAB_026 (Dream Logic):
- [ ] Create folder structure
- [ ] Implement `dream_logic_system.py`
- [ ] Write `test_lab_026_dream_logic.py`
- [ ] TDD cycle
- [ ] API integration
- [ ] Verify integration with LAB_001, LAB_003

### LAB_027 (Theory of Mind):
- [ ] Create folder structure
- [ ] Implement `theory_of_mind_system.py`
- [ ] Write `test_lab_027_theory_of_mind.py`
- [ ] TDD cycle
- [ ] API integration
- [ ] Verify integration with LAB_007, LAB_012, LAB_020

### LAB_028 (Empathy):
- [ ] Create folder structure
- [ ] Implement `empathy_system.py`
- [ ] Write `test_lab_028_empathy.py`
- [ ] TDD cycle
- [ ] API integration
- [ ] Verify integration with LAB_008, LAB_013, LAB_014, LAB_027

---

## Documentation Updates

### After all LABs complete:

1. **LAB_REGISTRY.json:**
   - Update version 1.3 → 1.4
   - Update total_labs_implemented: 28 → 34
   - Update completion_percentage: 53.8% → 65.4%
   - Update layer_5 status
   - Update sublayer_5F status: "🔴 designed" → "✅ operational (6/6 LABs)"
   - Add detailed entries for LAB_023-028

2. **TRACKING.md:**
   - Add Session 19 comprehensive summary
   - Document all 6 LABs with metrics
   - TDD methodology summary
   - Learnings and achievements

3. **Git Commits:**
   - Comprehensive commit message
   - Reference all files created/modified
   - Include test summary

---

## Success Criteria

**Session 19 complete when:**
- ✅ All 6 LABs implemented (LAB_023-028)
- ✅ All tests passing (~140-180 tests)
- ✅ 12 API endpoints operational
- ✅ LAB_REGISTRY.json updated
- ✅ TRACKING.md updated
- ✅ Git commits created
- ✅ Integration verified with existing systems

**Quality metrics:**
- Test coverage: 100% (all tests passing)
- Code quality: Clean, well-commented, TDD-validated
- Integration: All neurochemistry/EF integrations working
- Documentation: Comprehensive and up-to-date

---

## Estimated Effort

**Per LAB:** ~30-45 minutes (based on Session 18 experience)
**Total LABs:** 6
**Total time:** ~3-4.5 hours

**Token budget:** 108K remaining (sufficient for 6 LABs)

---

**Plan Complete - Ready for Implementation Phase**

**Next:** Begin CODIFICAR phase with LAB_023 (Divergent Thinking)
