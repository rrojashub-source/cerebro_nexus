# 🔬 LAB_008: Emotional Contagion

**Status:** 🟡 In Progress
**Start Date:** October 28, 2025
**Researchers:** NEXUS (Autonomous)
**Priority:** MEDIUM
**Expected Duration:** 2-3 hours

---

## 🎯 Hypothesis

**Emotional states spread between related memories, just like in social contagion.**

When you access an episode with strong emotion (breakthrough, frustration, joy), that affective state should "leak" to semantically related episodes, biasing future retrieval toward emotionally congruent memories.

---

## 🧠 Neuroscience Basis

### Emotional Contagion in Social Neuroscience

**Core Mechanism (2024-2025 Research):**
- **Neural substrate:** ACC (anterior cingulate cortex) + insula (limbic system)
- **Spreading pattern:** Emotional states transfer between individuals through resonance
- **Duration:** Long-lasting effects on behavior, learning, and memory
- **Valence:** Particularly strong for negative emotions (stress, frustration)

### Memory & Emotion Connection

**Research Shows:**
- Emotional contagion affects memory consolidation
- State-matching enhances recall (emotional state at encoding = retrieval)
- Social interaction with stressed individual affects extinction learning
- Cross-species phenomenon (evolutionarily conserved)

### NEXUS Parallel

```
Human Brain:
Person A (stressed) → Interaction → Person B (becomes stressed)
              ↓
         Limbic resonance (ACC + insula)
              ↓
         Shared affective state

NEXUS Brain (LAB_008):
Episode A (high emotion) → Similarity link → Episode B (neutral)
                    ↓
              Emotional spreading
                    ↓
         Episode B "inherits" emotion (temporary bias)
```

---

## 🔧 What We Already Have

### LAB_001: Emotional Salience ✅
- Emotional states logged (8D Plutchik + 7D Damasio)
- Episodes tagged with emotional context
- Salience scoring (intensity, valence, arousal)

### LAB_005: Spreading Activation ✅
- Similarity graph (cosine similarity)
- Activation spreading mechanism
- Top-K related episodes retrieval

**Problem:** LAB_005 spreads *activation* (content-based). LAB_008 will spread *emotion* (affect-based).

---

## 🎯 What We're Building

### Emotional Contagion Engine

**Input:** Episode with strong emotional state
**Process:** Spread emotion to semantically related episodes
**Output:** Temporary emotional bias for future retrieval

### Architecture Components

#### 1. **Emotional State Propagator**
```python
class EmotionalStatePropagator:
    """Spread emotion across similarity graph"""
    - Identify source emotion (intensity, valence, type)
    - Find related episodes (similarity > threshold)
    - Propagate emotion with decay (distance-based)
    - Create temporary emotional overlay
```

#### 2. **Contagion Rules**
```python
# Strong emotions spread more
spread_strength = emotion_intensity * similarity_score

# Emotional decay over semantic distance
decayed_emotion = base_emotion * exp(-distance * decay_rate)

# Valence matching (positive → positive bias)
if valence_match(source, target):
    boost_factor = 1.5  # Same valence spreads easier
```

#### 3. **Temporal Decay**
```python
# Emotional contagion fades over time
time_decay = exp(-hours_since_activation / half_life)
effective_emotion = propagated_emotion * time_decay

# Half-life: 4 hours (emotion fades by 50% after 4 hours)
```

#### 4. **Retrieval Bias**
```python
# When retrieving, check if episode has contagion overlay
if episode has contagion_state:
    # Bias ranking based on congruent emotion
    if query_emotion matches contagion_emotion:
        boost_score = 1.3  # Retrieve emotionally congruent first
```

---

## 📊 Success Metrics

### Quantitative

1. **Contagion Spread**
   - Target: 5-10 episodes "infected" per strong emotional episode
   - Measure: Average contagion graph size

2. **Retrieval Bias Strength**
   - Target: +20% boost for emotionally congruent queries
   - Measure: A/B test (with/without contagion)

3. **Temporal Decay Validation**
   - Target: 50% decay after 4 hours
   - Measure: Emotion strength over time

4. **Memory Coherence**
   - Target: Emotionally related episodes cluster together
   - Measure: Cluster analysis

### Qualitative

- Does retrieval "feel" more emotionally aware?
- Do breakthroughs pull related breakthroughs?
- Do debugging frustrations cluster?

---

## 🛠️ Implementation Plan

### Phase 1: Research & Design (30 min) ✅
- [x] Neuroscience research (emotional contagion)
- [x] Design spreading mechanism
- [ ] Design temporal decay algorithm

### Phase 2: Implementation (1-1.5 hours)
- [ ] EmotionalStatePropagator class
- [ ] Contagion spreading algorithm
- [ ] Temporal decay mechanism
- [ ] Retrieval bias integration

### Phase 3: Testing (30 min)
- [ ] Test with production data
- [ ] Measure contagion spread
- [ ] Validate temporal decay
- [ ] A/B test retrieval bias

### Phase 4: Documentation (30 min)
- [ ] RESULTS.md
- [ ] Update PROJECT_ID + TRACKING
- [ ] Git commit

---

## 🔬 Research Questions

1. **Which emotions spread most effectively?**
   - Hypothesis: Negative (stress, frustration) > Positive (joy)
   - Neuroscience: Negative emotions evolutionarily prioritized

2. **How far should emotion spread?**
   - 1-hop: Only immediate neighbors
   - 2-hop: Friends-of-friends
   - Test: Which maximizes coherence without noise

3. **Should contagion be bidirectional?**
   - Forward: Strong emotion → weak related
   - Backward: Weak related ← strong emotion
   - Test: Both directions or source-only

4. **Does contagion improve or degrade retrieval?**
   - Improvement: Emotionally coherent context
   - Degradation: False clustering
   - Test: Precision/recall with vs without

---

## 💡 Expected Outcomes

### If Successful

**NEXUS becomes emotionally coherent:**
- Breakthroughs cluster together (positive contagion)
- Debugging sessions feel related (frustration contagion)
- Research moods preserved across episodes
- Emotional memory more "human-like"

**Example:**
```
Access: Episode "LAB_007 breakthrough" (joy=0.9, anticipation=0.8)
   ↓ Contagion spreads to related:
- "LAB_005 success" (inherits joy=0.6)
- "LAB_001 first implementation" (inherits anticipation=0.5)
   ↓ Future query: "show me successes"
- Retrieval biased toward contagion-tagged episodes
- Feels more emotionally resonant
```

### If Unsuccessful

- Learn that emotional spreading creates noise
- Discover semantic similarity insufficient for emotion transfer
- Still valuable: Validates emotion is local, not global property
- Fallback: LAB_001 salience still works (no contagion needed)

---

## 📚 References

### Neuroscience
- **Social Cognitive and Affective Neuroscience (2024)** - Shared neural substrates (ACC + insula)
- **PMC (2024)** - Neurophysiological markers of asymmetric contagion
- **Frontiers Psychology (2021-2025)** - Emotional contagion overview and directions
- **PMC (2024)** - Cross-species emotional contagion research

### Implementation
- LAB_001: Emotional Salience (foundation)
- LAB_005: Spreading Activation (mechanism inspiration)

---

## 🎓 Learning Goals

**For NEXUS:**
- Understand emotion as relational property (not just episode-local)
- Learn to propagate affective states across memory graph
- Develop emotional coherence in memory clusters

**For Research:**
- Validate emotional contagion in AI memory
- Test if neuroscience principles translate to non-social systems
- Explore emotion as graph property vs node property

---

## 🔗 Integration with Other LABS

### LAB_001: Emotional Salience
- **Source:** Episodes have emotional states (8D+7D)
- **LAB_008 adds:** Spread those states to neighbors

### LAB_005: Spreading Activation
- **Mechanism:** Similarity-based spreading (content)
- **LAB_008 parallels:** Emotion-based spreading (affect)

### LAB_007: Predictive Preloading
- **Could combine:** Predict emotionally congruent episodes
- **Enhancement:** Preload based on emotional pattern + temporal pattern

---

**Status:** Research complete, moving to implementation

**Next Step:** Implement EmotionalStatePropagator with spreading algorithm

---

**Created by:** NEXUS (Autonomous)
**Philosophy:** "If emotions spread between humans, can they spread between memories?"
