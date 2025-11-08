# LAYER_5F: Creativity & Social Cognition - Exploration

**Date:** November 7, 2025
**Session:** 19 (continuation of Session 18)
**Goal:** Research foundation for implementing LAB_023-028 (4 Creativity + 2 Social Cognition LABs)

---

## Overview

LAYER_5F combines two distinct but complementary cognitive domains:
- **Creativity (LAB_023-026):** Generative, divergent thinking, insight, unconstrained association
- **Social Cognition (LAB_027-028):** Theory of Mind, empathy, mental state attribution

Both domains rely on **prefrontal-temporal-parietal networks** and integrate with previously implemented systems (emotional salience, executive functions, neurochemistry).

---

## Part 1: CREATIVITY SYSTEMS (LAB_023-026)

### Neuroscience Foundation

**Core Creativity Network:**
- **Default Mode Network (DMN):** Spontaneous thought, idea generation
  - Medial prefrontal cortex (mPFC)
  - Posterior cingulate cortex (PCC)
  - Angular gyrus, precuneus
- **Executive Control Network:** Idea evaluation, selection
  - Dorsolateral PFC (dlPFC)
  - Anterior cingulate cortex (ACC)
- **Right Hemisphere:** Remote associations, novelty detection
  - Right temporal lobe
  - Right parietal cortex

**Key Finding (Beaty et al. 2016):**
> "Creative cognition involves dynamic interplay between DMN (generation) and executive network (evaluation). High-creative individuals show better coupling between these networks."

---

### LAB_023: Divergent Thinking Engine

**Function:** Generate multiple creative solutions through remote associations

**Neuroscience Basis:**
- DMN activation during idea generation
- Right hemisphere semantic networks (broader activation)
- Reduced left hemisphere interference (less constraint)

**Core Mechanisms:**

1. **Remote Association:**
   - Semantic distance metric (ideas far from obvious)
   - Activation spreading beyond typical conceptual neighborhoods
   - Formula: `novelty = semantic_distance(idea, problem_space)`

2. **Inhibition of Conventional Responses:**
   - Integration with LAB_019 Inhibitory Control
   - Suppress obvious/first associations
   - Allow weaker/unconventional links to emerge

3. **Fluency, Flexibility, Originality Scoring (Guilford 1967):**
   - **Fluency:** Total number of ideas generated
   - **Flexibility:** Number of distinct categories
   - **Originality:** Statistical rarity of responses

**Parameters:**
- `semantic_distance_threshold` (0-1): Minimum distance for "creative" idea
- `inhibition_strength` (0-1): How much to suppress conventional
- `generation_time` (seconds): Duration for idea generation

**Output:**
```python
{
  "ideas": ["idea_1", "idea_2", ...],
  "fluency_score": 15,
  "flexibility_score": 7,
  "originality_score": 0.68,
  "most_novel_idea": "idea_3"
}
```

**Key Paper:** Guilford (1967) - "The Nature of Human Intelligence" (divergent thinking framework)

---

### LAB_024: Conceptual Blending

**Function:** Create novel concepts through metaphor, analogy, blending

**Neuroscience Basis:**
- Posterior parietal cortex (relational integration)
- Temporal cortex (semantic representations)
- Prefrontal cortex (structural mapping)

**Core Mechanisms:**

1. **Conceptual Space Mapping (Fauconnier & Turner 2002):**
   - Input Space 1 + Input Space 2 → Blended Space
   - Generic space (common structure)
   - Emergent structure (new properties not in inputs)

2. **Structure Mapping Theory (Gentner 1983):**
   - Align relational structure (not just surface features)
   - Find structural correspondences
   - Transfer inferences from source to target

3. **Metaphor Generation:**
   - "X is like Y because Z"
   - Conceptual domain mapping
   - Novel insight through transfer

**Example:**
```
Input 1: "Atom" (nucleus, electrons, orbits)
Input 2: "Solar System" (sun, planets, orbits)
Blended: "Planetary model of atom" (emergent: quantization)
```

**Parameters:**
- `structural_similarity_threshold` (0-1): Min similarity for mapping
- `blend_novelty_weight` (0-1): Favor surprising vs. coherent blends
- `max_blend_complexity` (1-5): Max number of input spaces

**Output:**
```python
{
  "blend": "Blended concept description",
  "metaphor": "X is like Y because Z",
  "analogies": ["analogy_1", "analogy_2"],
  "coherence_score": 0.82,
  "novelty_score": 0.71
}
```

**Key Papers:**
- Fauconnier & Turner (2002) - "The Way We Think: Conceptual Blending"
- Gentner (1983) - "Structure-Mapping: A Theoretical Framework for Analogy"

---

### LAB_025: Insight & Aha Moments

**Function:** Sudden insight through problem restructuring, impasse breaking

**Neuroscience Basis:**
- Right anterior temporal lobe (solution emergence)
- ACC burst activity (aha signal)
- Reduced dlPFC during incubation (defocused attention)

**Core Mechanisms:**

1. **Impasse Detection:**
   - Recognize when current approach isn't working
   - Measure: repeated failed attempts, no progress
   - Threshold: `impasse_threshold = failed_attempts > 3`

2. **Incubation:**
   - Reduce focused attention (DMN takes over)
   - Allow unconscious processing
   - Integration with LAB_046 (Default Mode Network - future LAB)
   - Duration: `incubation_time = 60-300 seconds`

3. **Restructuring:**
   - Sudden reframe of problem space
   - Change constraints or representation
   - "Pop" into awareness with aha signal

4. **Aha Signal (Metcalfe & Wiebe 1987):**
   - Subjective feeling of insight
   - Confidence spike
   - Dopamine burst (LAB_013 integration)

**Phenomenology:**
- Analytic solving: Gradual warmth, steady progress
- Insight solving: Flat → sudden spike ("Aha!")

**Parameters:**
- `impasse_threshold` (int): Failed attempts to trigger incubation
- `incubation_duration` (seconds): Time for unconscious processing
- `aha_confidence_threshold` (0-1): Confidence to signal insight

**Output:**
```python
{
  "insight_occurred": True,
  "solution": "Restructured solution",
  "aha_intensity": 0.89,
  "solving_time": 145.2,
  "restructuring_type": "constraint_relaxation"
}
```

**Key Papers:**
- Kounios & Beeman (2014) - "The Cognitive Neuroscience of Insight"
- Metcalfe & Wiebe (1987) - "Intuition in insight and noninsight problem solving"

---

### LAB_026: Dream Logic

**Function:** Unconstrained association, surreal combinations (REM-like)

**Neuroscience Basis:**
- REM sleep: High DMN activity, low dlPFC (reduced executive control)
- Emotional salience drives connections (not logic)
- Hippocampal replay with bizarre recombinations

**Core Mechanisms:**

1. **Suspend Logical Constraints:**
   - Disable consistency checking
   - Allow contradictions
   - Temporal/spatial rules relaxed

2. **Emotional Salience-Driven Association:**
   - Integration with LAB_001 (Emotional Salience)
   - Connect memories by emotional similarity (not logical)
   - Formula: `connection_strength = emotional_similarity(mem_A, mem_B)`

3. **Bizarre Recombinations:**
   - Mix unrelated memory fragments
   - Surreal narratives
   - Novel insights through unconstrained search

4. **Memory Consolidation During Offline Processing:**
   - Integration with LAB_003 (Sleep Consolidation)
   - Reactivate and recombine memories
   - Pattern extraction through randomness

**Parameters:**
- `logical_constraint_strength` (0-1): 0 = fully unconstrained (dream), 1 = fully logical (wake)
- `emotional_connection_weight` (0-1): How much emotion drives associations
- `bizarreness_tolerance` (0-1): Allow unusual combinations

**Output:**
```python
{
  "dream_narrative": "Surreal narrative/associations",
  "memory_fragments": ["fragment_1", "fragment_2", ...],
  "emotional_themes": ["fear", "joy"],
  "novel_connections": [("concept_A", "concept_B", similarity)],
  "bizarreness_score": 0.76
}
```

**Key Papers:**
- Hobson & Friston (2012) - "Waking and dreaming consciousness: Neurobiological and functional considerations"
- Maquet (2000) - "The role of sleep in learning and memory"

---

## Part 2: SOCIAL COGNITION SYSTEMS (LAB_027-028)

### Neuroscience Foundation

**Core Social Brain Network:**
- **Medial Prefrontal Cortex (mPFC):** Self-referential processing, mentalizing
- **Temporoparietal Junction (TPJ):** Belief attribution, perspective taking
- **Superior Temporal Sulcus (STS):** Biological motion, intention detection
- **Precuneus:** Self/other distinction, theory of mind
- **Anterior Insula:** Empathy, interoception
- **Anterior Cingulate Cortex (ACC):** Empathic distress, conflict

**Key Finding (Frith & Frith 2003):**
> "Theory of Mind requires representing others' mental states as separate from our own. TPJ critical for belief attribution, especially when beliefs differ from reality (false belief tasks)."

---

### LAB_027: Theory of Mind

**Function:** Infer mental states of others (beliefs, desires, intentions)

**Neuroscience Basis:**
- mPFC: Mentalizing about self and others
- TPJ: Belief attribution (especially false beliefs)
- STS: Intention detection from actions
- Precuneus: Self/other distinction

**Core Mechanisms:**

1. **Belief Representation (even if false):**
   - Track what others believe (may differ from reality)
   - False belief task: "Sally-Anne" paradigm
   - Formula: `belief_other != belief_self` (critical for ToM)

2. **Intention Attribution:**
   - Infer goals from observed actions
   - Predict behavior based on intentions
   - Formula: `intention = argmax(goal | action, context)`

3. **Recursive Belief Modeling:**
   - "I think you think I think..."
   - Depth: 1st order (I know X), 2nd order (I know you know X), etc.
   - Typical depth: 2-3 levels before cognitive load

4. **Behavior Prediction:**
   - Given mental state → predict action
   - Integration with LAB_007 (Predictive Preloading)
   - Formula: `action_predicted = f(belief, desire, intention)`

**Parameters:**
- `belief_confidence` (0-1): Confidence in inferred belief
- `recursion_depth` (1-5): Depth of "I think you think..."
- `context_weight` (0-1): How much context influences inference

**Output:**
```python
{
  "mental_state": {
    "belief": "They believe X",
    "desire": "They want Y",
    "intention": "They intend to Z"
  },
  "confidence": 0.78,
  "predicted_behavior": "Will do action A",
  "false_belief_detected": True,
  "recursion_depth": 2
}
```

**Key Papers:**
- Frith & Frith (2003) - "Development and neurophysiology of mentalizing"
- Saxe & Kanwisher (2003) - "People thinking about thinking people: TPJ and theory of mind"

---

### LAB_028: Empathy Simulation

**Function:** Affective empathy, emotional resonance, compassion

**Neuroscience Basis:**
- Anterior insula: Feeling others' emotions (affective empathy)
- ACC: Empathic distress, vicarious pain
- Mirror neuron system: Motor resonance
- mPFC: Self/other distinction (avoid emotional contagion)

**Core Mechanisms:**

1. **Emotional Mirroring:**
   - Simulate others' emotional state internally
   - Integration with LAB_008 (Emotional Contagion)
   - Formula: `empathic_emotion = mirror(observed_emotion) * intensity`

2. **Self/Other Distinction:**
   - Critical: Distinguish "their pain" from "my pain"
   - Without distinction → emotional contagion (overwhelm)
   - With distinction → compassionate response
   - Formula: `self_other_boundary = 1 - contagion_risk`

3. **Compassionate Response Generation:**
   - Prosocial motivation to help
   - Integration with LAB_013 (Dopamine - prosocial reward)
   - Care-based ethics (vs. rule-based)

4. **Empathic Distress Regulation:**
   - Prevent burnout from too much vicarious suffering
   - Integration with LAB_014 (Serotonin - emotion regulation)
   - Balance: Feel enough to care, not so much to freeze

**Types of Empathy:**
- **Cognitive Empathy:** Understand what they feel (ToM component)
- **Affective Empathy:** Feel what they feel (this LAB)
- **Compassionate Empathy:** Motivated to help

**Parameters:**
- `mirroring_intensity` (0-1): How strongly to mirror emotion
- `self_other_boundary_strength` (0-1): Prevent emotional contagion
- `compassion_threshold` (0-1): Threshold to trigger prosocial action
- `distress_tolerance` (0-1): How much vicarious suffering before regulation

**Output:**
```python
{
  "empathic_emotion": {
    "type": "sadness",
    "intensity": 0.62,
    "source": "other"
  },
  "self_other_distinction": 0.85,
  "prosocial_motivation": 0.71,
  "compassionate_action": "offer_help",
  "empathic_distress_level": 0.34
}
```

**Key Papers:**
- Decety & Jackson (2004) - "The functional architecture of human empathy"
- Singer & Lamm (2009) - "The social neuroscience of empathy"

---

## Integration with Existing Systems

### Integration Matrix

| New LAB | Integrates With | Purpose |
|---------|-----------------|---------|
| **LAB_023** | LAB_017 (GABA/Glu) | Reduced inhibition for creativity |
| **LAB_023** | LAB_019 (Inhibition) | Suppress conventional responses |
| **LAB_024** | LAB_023 (Divergent) | Blend divergent ideas |
| **LAB_025** | LAB_013 (Dopamine) | Aha reward burst |
| **LAB_026** | LAB_001 (Emotion) | Emotional salience drives associations |
| **LAB_026** | LAB_003 (Sleep) | Offline processing, consolidation |
| **LAB_027** | LAB_007 (Predictive) | Predict others' behavior |
| **LAB_027** | LAB_012 (Future Think) | Simulate others' future actions |
| **LAB_028** | LAB_008 (Contagion) | Emotional mirroring |
| **LAB_028** | LAB_013 (Dopamine) | Prosocial reward |
| **LAB_028** | LAB_014 (Serotonin) | Empathic distress regulation |

---

## Implementation Considerations

### Creativity LABs (023-026):

1. **Semantic Networks:**
   - Need semantic distance metric
   - Could use embedding similarity (cosine distance)
   - Word2Vec, GloVe, or similar

2. **Randomness vs. Structure:**
   - LAB_023 (Divergent): Structured randomness
   - LAB_026 (Dream Logic): Pure unconstrained
   - Balance exploration vs. coherence

3. **Evaluation Metrics:**
   - Fluency, flexibility, originality (Guilford)
   - Coherence, novelty trade-off
   - Human-like vs. random distinction

### Social Cognition LABs (027-028):

1. **Belief Representation:**
   - Need data structure for "belief states"
   - Track: agent_id, belief_content, confidence, false_belief_flag

2. **Self/Other Boundary:**
   - Critical for empathy (avoid contagion)
   - Represent "source" of emotion (self vs. other)

3. **Recursion Depth:**
   - Theory of Mind recursion can be expensive
   - Limit to 2-3 levels for practical implementation

---

## Testing Strategy

### Creativity Tests:

1. **Divergent Thinking:**
   - Alternative Uses Task (brick, paperclip)
   - Measure fluency, flexibility, originality

2. **Conceptual Blending:**
   - Test known metaphors (time is money)
   - Generate novel analogies

3. **Insight:**
   - Classic insight problems (9-dot, matchstick)
   - Measure aha signal, restructuring detection

4. **Dream Logic:**
   - Generate surreal narratives
   - Validate emotional theme consistency

### Social Cognition Tests:

1. **Theory of Mind:**
   - Sally-Anne false belief task
   - Second-order belief attribution
   - Behavior prediction accuracy

2. **Empathy:**
   - Emotional mirroring accuracy
   - Self/other distinction maintenance
   - Compassionate response generation

---

## Key Design Decisions

1. **Creativity as Stochastic Process:**
   - Use controlled randomness (not purely deterministic)
   - Seed-based for reproducibility in tests

2. **Social Cognition as Inference:**
   - Bayesian belief updating
   - Confidence-weighted predictions

3. **Neurochemistry Integration:**
   - Dopamine: Reward for insight, prosocial behavior
   - Serotonin: Empathic distress regulation
   - GABA: Disinhibition for creativity

4. **Executive Function Integration:**
   - Inhibitory Control: Suppress conventional (LAB_023)
   - Cognitive Flexibility: Switch perspectives (LAB_027)
   - Error Detection: Detect false beliefs (LAB_027)

---

## Summary

**Creativity Systems (LAB_023-026):**
- Divergent Thinking → Conceptual Blending → Insight → Dream Logic
- Progression from structured to unconstrained
- DMN-driven generation, executive evaluation

**Social Cognition Systems (LAB_027-028):**
- Theory of Mind (cognitive empathy) → Empathy Simulation (affective empathy)
- Social brain network (mPFC, TPJ, insula, ACC)
- Self/other distinction critical

**Both domains:**
- Integrate with existing neurochemistry (DA, 5-HT, GABA)
- Integrate with executive functions (inhibition, flexibility, error detection)
- Real-world application: Creative problem-solving + social interaction

---

**Exploration Complete - Ready for Planning Phase**

Total LABs: 6 (4 Creativity + 2 Social)
Estimated complexity: High (semantic networks, belief representation, recursive modeling)
Key challenge: Balance novelty vs. coherence in creativity, self/other distinction in empathy

**Next:** Create comprehensive implementation plan in `tasks/layer5f_creativity_social.md`
