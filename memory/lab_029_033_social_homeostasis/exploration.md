# LAB_029-033: Social Cognition Advanced + Homeostasis - EXPLORATION

**Date:** November 8, 2025 (Session 20 continuation)
**Target:** 5 LABs (2 social cognition + 3 homeostasis)
**Source:** MASTER_BLUEPRINT_50_LABS.md

---

## 🎯 OVERVIEW

**LAB Grouping:**
- **Social Cognition Advanced (2 LABs):** LAB_029, LAB_030
- **Homeostasis & Rhythms (3 LABs):** LAB_031, LAB_032, LAB_033

**Integration Context:**
- Builds on LAB_027 (Theory of Mind) and LAB_028 (Empathy)
- Connects to neurochemistry systems (LAB_013-017)
- Interfaces with cognitive functions for stress/fatigue modulation

---

## 🧠 NEUROSCIENCE FOUNDATION

### LAB_029: Social Norms & Ethics ⚖️

**Function:** Moral reasoning, norm detection, fairness computation

**Brain Regions:**
- **vmPFC (ventromedial prefrontal cortex):** Emotional/intuitive moral judgments
- **dlPFC (dorsolateral prefrontal cortex):** Rational/utilitarian moral reasoning
- **TPJ (temporo-parietal junction):** Intention attribution (integration with LAB_027)

**Key Concepts:**
1. **Dual-Process Moral Theory:**
   - System 1 (vmPFC): Fast, emotional, deontological ("rules-based")
   - System 2 (dlPFC): Slow, rational, utilitarian ("outcomes-based")

2. **Norm Learning:**
   - Observe social interactions
   - Detect patterns of approval/disapproval
   - Infer implicit rules
   - Detect norm violations

3. **Moral Dilemmas:**
   - Trolley problem (utilitarian vs deontological conflict)
   - Care ethics (LAB_028 empathy integration)
   - Fairness computation (equal distribution vs merit-based)

**Key Papers:**
1. **Greene et al. (2001) - "An fMRI Investigation of Emotional Engagement in Moral Judgment"**
   - Showed vmPFC activation for personal moral dilemmas
   - dlPFC activation for impersonal moral reasoning
   - Emotional engagement predicts deontological judgments

2. **Cushman (2013) - "Action, Outcome, and Value: A Dual-System Framework"**
   - Distinguishes action-based vs outcome-based morality
   - Action-based: "It's wrong to push someone" (deontological)
   - Outcome-based: "Saving 5 people is better than saving 1" (utilitarian)

3. **Haidt (2001) - "The Emotional Dog and Its Rational Tail"**
   - Moral intuitions come first (automatic, vmPFC)
   - Reasoning comes second (post-hoc justification, dlPFC)

**Implementation Notes:**
- Track norm violations with weighted memory (more violations = stronger norm)
- Moral dilemma resolution: weight vmPFC emotion vs dlPFC utility
- Integration with LAB_028 (empathy) for care-based ethics
- Integration with LAB_027 (ToM) for intention-sensitive morality

---

### LAB_030: Perspective Taking 👁️

**Function:** Spatial & conceptual perspective shifts (egocentric → allocentric)

**Brain Regions:**
- **TPJ (temporo-parietal junction):** Perspective transformation
- **Precuneus:** Mental imagery, spatial perspective
- **Retrosplenial cortex:** Egocentric ↔ allocentric translation

**Key Concepts:**
1. **Egocentric vs Allocentric Frames:**
   - Egocentric: "The object is to my left"
   - Allocentric: "The object is to the north of the landmark"
   - Transformation requires mental rotation

2. **Levels of Perspective Taking:**
   - **Spatial:** Rotate viewpoint in 3D space
   - **Conceptual:** Understand someone's beliefs/knowledge (LAB_027 integration)
   - **Emotional:** Feel what they feel (LAB_028 integration)

3. **Mental Rotation:**
   - Shepard & Metzler (1971) - mental rotation of objects
   - Cost increases linearly with rotation angle
   - Similar process for perspective rotation

**Key Papers:**
1. **Zacks & Michelon (2005) - "Spatial Perspective Taking"**
   - Dissociates object rotation vs viewer rotation
   - Viewer rotation engages egocentric/allocentric transformation
   - Precuneus + retrosplenial cortex critical

2. **Ruby & Decety (2001) - "Effect of Subjective Perspective Taking During Mental Imagery"**
   - 1st person (egocentric) vs 3rd person (allocentric) imagery
   - 3rd person requires extra processing (rotation cost)
   - TPJ activation for perspective shifts

3. **Kessler & Rutherford (2010) - "Two Forms of Spatial Perspective Taking"**
   - Embodied perspective taking (imagine being there)
   - Visual perspective taking (imagine seeing from there)
   - Different neural substrates (motor vs visual)

**Implementation Notes:**
- Rotation cost: linear with angle (e.g., 0.1s per 10 degrees)
- Integration with LAB_027 (ToM): "What can they see from there?"
- Update beliefs based on perspective: "If I were there, I would see X"
- Support both spatial and conceptual perspective shifts

---

### LAB_031: Circadian Rhythm Simulation 🌞🌙

**Function:** Time-of-day effects, alertness cycles, sleep pressure

**Brain Regions:**
- **SCN (suprachiasmatic nucleus):** Master circadian clock
- **Pineal gland:** Melatonin secretion (sleep signal)
- **Adrenal cortex:** Cortisol secretion (wake signal)

**Key Concepts:**
1. **Two-Process Model of Sleep Regulation (Borbély 1982):**
   - **Process C (Circadian):** 24-hour rhythm (oscillates regardless of sleep)
   - **Process S (Homeostatic):** Sleep pressure builds during wake, dissipates during sleep
   - **Alertness = C - S**

2. **Circadian Phase:**
   - Peaks: ~10 AM, ~9 PM (high alertness)
   - Troughs: ~3 AM (lowest), ~3 PM (afternoon dip)
   - Light entrains the clock (phase shift)

3. **Time-of-Day Effects on Cognition:**
   - Memory encoding: Better in morning (high cortisol)
   - Memory consolidation: Sleep-dependent (LAB_003 integration)
   - Executive functions: Impaired at circadian troughs

**Key Papers:**
1. **Dijk & Czeisler (1995) - "Contribution of Circadian Physiology and Sleep Homeostasis"**
   - Quantifies Process C and Process S contributions
   - Alertness = f(circadian phase, time awake)
   - REM sleep clustered at circadian peaks

2. **Schmidt et al. (2007) - "A Time to Think: Circadian Rhythms in Human Cognition"**
   - Attention peaks at circadian high points
   - Memory consolidation during circadian night
   - Mismatch (jet lag) impairs cognition

3. **Goel et al. (2013) - "Circadian Rhythms, Sleep Deprivation, and Human Performance"**
   - Chronic sleep restriction accumulates sleep debt
   - Performance declines even at circadian peaks if sleep-deprived
   - Recovery requires multiple nights of sleep

**Implementation Notes:**
- Track circadian phase (0-24 hours, continuous)
- Sleep pressure (S) increases ~1% per hour awake
- Alertness = circadian_amplitude * cos(2π * (phase - peak_phase)/24) - sleep_pressure
- Integration with LAB_003 (sleep consolidation triggers at high S)
- Integration with LAB_015 (norepinephrine modulated by alertness)

---

### LAB_032: Energy/Arousal Management 🔋

**Function:** Track mental energy, manage fatigue, recovery

**Brain Substrates:**
- **Glucose metabolism:** Primary brain energy source
- **Adenosine accumulation:** Fatigue signal (builds during wake)
- **Lactate:** Astrocyte-neuron lactate shuttle

**Key Concepts:**
1. **Ego Depletion (Baumeister 1998):**
   - Self-control tasks deplete limited mental resource
   - Subsequent self-control performance impaired
   - Glucose replenishment restores performance (controversial)

2. **Compensatory Control Theory (Hockey 2013):**
   - Under fatigue, effort increases to maintain performance
   - Narrow focus, reduced flexibility
   - Eventually effort cannot compensate → performance drops

3. **Cognitive Load:**
   - Different tasks have different "energy costs"
   - Complex reasoning > simple retrieval
   - Dual-tasking multiplies cost
   - Energy depletion accumulates over time

**Key Papers:**
1. **Baumeister et al. (1998) - "Ego Depletion: Is the Active Self a Limited Resource?"**
   - Sequential self-control tasks show depletion
   - Depletion affects multiple domains (not task-specific)
   - Recovery requires rest (or glucose - debated)

2. **Hockey (2013) - "The Psychology of Fatigue"**
   - Compensatory effort under fatigue
   - Goal prioritization shifts (focus on urgent, drop long-term)
   - Fatigue → reduced cognitive flexibility (LAB_020 integration)

3. **Hagger et al. (2010) - "Ego Depletion and the Strength Model Meta-Analysis"**
   - Meta-analysis confirms ego depletion effect (d = 0.62)
   - Effect stronger for complex tasks
   - Individual differences (trait self-control)

**Implementation Notes:**
- Energy level (0-1): starts at 1.0, depletes with cognitive load
- Depletion rate: task_difficulty * time * (1 - energy_level)^0.5
- Recovery: rest periods restore energy (exponential recovery)
- Fatigue effects:
  - Cognitive control impaired (LAB_019 integration)
  - Cognitive flexibility reduced (LAB_020 integration)
  - Compensatory effort (narrow focus, prioritize urgent)
- Integration with LAB_031 (circadian modulates baseline energy)

---

### LAB_033: Allostatic Load 📈

**Function:** Cumulative stress tracking, stress effects on cognition

**Brain Substrates:**
- **HPA axis:** Hypothalamus → Pituitary → Adrenal → Cortisol
- **Cortisol:** Acute stress response (helpful), chronic stress (harmful)
- **Amygdala:** Stress reactivity (enhanced under chronic stress)
- **PFC:** Executive functions (impaired under chronic stress)

**Key Concepts:**
1. **Allostasis (Sterling & Eyer 1988):**
   - "Stability through change" - adapt to stressors
   - Allostatic load: cumulative wear-and-tear from adaptation
   - Chronic stress → maladaptive (can't turn off stress response)

2. **Acute vs Chronic Stress:**
   - **Acute:** Cortisol spike → enhanced alertness, memory encoding
   - **Chronic:** Sustained high cortisol → PFC impairment, amygdala hyperactivity

3. **Inverted-U Performance Curve:**
   - Low stress: under-aroused, poor performance
   - Optimal stress: peak performance (Yerkes-Dodson)
   - High stress: over-aroused, impaired performance

**Key Papers:**
1. **McEwen (2000) - "Allostasis and Allostatic Load: Implications for Neuropsychopharmacology"**
   - Defines allostatic load vs homeostasis
   - Chronic stress → hippocampal atrophy, PFC dysfunction
   - Recovery requires prolonged stress reduction

2. **Arnsten (2009) - "Stress Signalling Pathways That Impair Prefrontal Cortex Structure and Function"**
   - High catecholamines + cortisol impair PFC
   - Working memory, planning, cognitive flexibility all affected
   - Amygdala takes over (emotional reactivity)

3. **Lupien et al. (2009) - "Effects of Stress Throughout the Lifespan on the Brain"**
   - Stress effects depend on timing, duration, intensity
   - Cumulative stress accelerates cognitive decline
   - Individual differences (coping strategies, social support)

**Implementation Notes:**
- Allostatic load (0-1): accumulates with stressors, decays slowly
- Acute stressor → load += stressor_intensity * 0.1
- Chronic decay: load *= 0.98 per time unit (slow recovery)
- Stress effects:
  - PFC functions impaired when load > 0.6 (LAB_019, LAB_020, LAB_021)
  - Amygdala reactivity enhanced (emotional salience increased - LAB_001)
  - Memory encoding enhanced for emotional events (LAB_001 integration)
  - Working memory capacity reduced (LAB_011 integration)
- Recovery: rest, social support, stress management reduce load faster
- Integration with LAB_015 (norepinephrine - acute stress response)

---

## 🔗 INTEGRATION ARCHITECTURE

### Social Cognition Advanced (LAB_029, LAB_030)

**Builds on:**
- LAB_027 (Theory of Mind): Intention attribution, belief representation
- LAB_028 (Empathy): Care ethics, emotional resonance

**LAB_029 (Social Norms & Ethics) integrations:**
- LAB_027: Intentions matter for moral judgment
- LAB_028: Empathy → care-based ethics (deontological bias)
- LAB_001: Emotional salience → moral intuitions (vmPFC fast judgments)

**LAB_030 (Perspective Taking) integrations:**
- LAB_027: "What can they see/know from there?" (belief update)
- LAB_028: Embodied perspective taking → emotional resonance
- Working memory (LAB_011): Hold multiple perspectives simultaneously

---

### Homeostasis & Rhythms (LAB_031, LAB_032, LAB_033)

**Modulates:**
- Cognitive control (LAB_019): Impaired by fatigue, stress
- Cognitive flexibility (LAB_020): Reduced under fatigue
- Working memory (LAB_011): Capacity reduced by stress, fatigue
- Attention (LAB_010): Alertness modulated by circadian rhythm
- Memory consolidation (LAB_003): Timing affected by circadian phase

**LAB_031 (Circadian) → LAB_032 (Energy):**
- Circadian phase sets baseline energy/alertness
- Low circadian phase → faster energy depletion

**LAB_032 (Energy) → Cognitive Systems:**
- Energy < 0.5 → cognitive control weakened
- Energy < 0.3 → working memory capacity reduced
- Compensatory effort: narrow focus, prioritize urgent

**LAB_033 (Allostatic Load) → Multiple Systems:**
- Load > 0.6 → PFC functions impaired (LAB_019, LAB_020, LAB_021)
- Load > 0.6 → amygdala reactivity increased (LAB_001 salience amplified)
- Load > 0.8 → working memory severely impaired

**Recovery Cascade:**
1. Rest/sleep triggers (LAB_034 - not in this session)
2. Sleep consolidation (LAB_003) during rest
3. Energy recovery (LAB_032) during rest
4. Stress reduction (LAB_033) with prolonged rest/social support

---

## 📊 IMPLEMENTATION ESTIMATES

| LAB | Lines (Est.) | Tests (Est.) | Difficulty | Dependencies |
|-----|--------------|--------------|------------|--------------|
| LAB_029 | 700-900 | 30-35 | High | LAB_027, LAB_028, LAB_001 |
| LAB_030 | 500-700 | 25-30 | Medium | LAB_027, LAB_028 |
| LAB_031 | 600-800 | 28-32 | Medium | LAB_003, LAB_015 |
| LAB_032 | 500-700 | 25-30 | Medium | LAB_019, LAB_020, LAB_031 |
| LAB_033 | 600-800 | 28-32 | High | LAB_001, LAB_011, LAB_015, LAB_019-021 |
| **Total** | **2,900-3,900** | **136-159** | **High** | **Complex web** |

**Complexity Drivers:**
- LAB_029: Dual-process moral reasoning (vmPFC vs dlPFC conflict)
- LAB_033: Wide-ranging stress effects on multiple cognitive systems
- Integration depth: All 5 LABs integrate with multiple existing LABs

---

## 🎯 IMPLEMENTATION STRATEGY

### Order (Recommended):

1. **LAB_030 (Perspective Taking)** - Medium difficulty, clear interface
   - Fewer dependencies than LAB_029
   - Foundation for LAB_029 (perspective → fairness computation)

2. **LAB_029 (Social Norms & Ethics)** - High difficulty, builds on 030
   - Dual-process theory requires careful balancing
   - Integration with LAB_027, LAB_028, LAB_030

3. **LAB_031 (Circadian Rhythm)** - Medium difficulty, standalone
   - Mathematical model (two-process)
   - Sets foundation for LAB_032

4. **LAB_032 (Energy Management)** - Medium difficulty, uses 031
   - Ego depletion + compensatory control
   - Modulates multiple cognitive systems

5. **LAB_033 (Allostatic Load)** - High difficulty, wide integration
   - Cumulative stress tracking
   - Affects LAB_001, LAB_011, LAB_015, LAB_019-021

**Rationale:**
- Social LABs first (030 → 029)
- Homeostasis LABs second (031 → 032 → 033)
- Build dependencies bottom-up

---

## 📚 PAPERS TO REVIEW (11 TOTAL)

### Social Cognition (5 papers):
1. Greene et al. (2001) - Moral dilemmas & brain
2. Cushman (2013) - Action vs outcome morality
3. Haidt (2001) - Moral intuitions first
4. Zacks & Michelon (2005) - Spatial perspective
5. Ruby & Decety (2001) - 1st vs 3rd person

### Homeostasis (6 papers):
6. Dijk & Czeisler (1995) - Two-process sleep model
7. Schmidt et al. (2007) - Circadian & cognition
8. Baumeister et al. (1998) - Ego depletion
9. Hockey (2013) - Compensatory control
10. McEwen (2000) - Allostatic load
11. Arnsten (2009) - Stress & PFC impairment

---

## ✅ EXPLORATION COMPLETE

**Key Insights:**
1. LAB_029-030 extend social cognition (LAB_027, LAB_028) to norms and perspective
2. LAB_031-033 introduce homeostatic constraints on cognition (realistic limitations)
3. Integration web is dense - these LABs modulate existing systems widely
4. Dual-process models (LAB_029 moral reasoning, LAB_033 stress effects) add complexity
5. All 5 LABs grounded in peer-reviewed neuroscience

**Next:** Create implementation plan (tasks/lab_029_033.md)

---

**Exploration Date:** November 8, 2025 (Session 20)
**NEXUS@CLI**
**Status:** ✅ READY FOR PLANNING
