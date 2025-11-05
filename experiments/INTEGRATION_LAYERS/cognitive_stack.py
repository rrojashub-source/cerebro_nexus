"""
CognitiveStack - Full Cognitive Architecture Integration

Complete integration: Layer 2 (Cognitive) ↔ Layer 3 (Memory) ↔ Layer 4 (Neuro)

Author: NEXUS + Ricardo
Date: November 5, 2025
Session: 8 (continued - Full Stack)
"""

from typing import Dict, Optional
from dataclasses import dataclass
import sys
from pathlib import Path
import numpy as np

# Add experiments to path
experiments_path = Path(__file__).parent.parent
sys.path.insert(0, str(experiments_path))

from INTEGRATION_LAYERS.neuro_emotional_bridge import (
    NeuroEmotionalBridge,
    EmotionalState,
    SomaticMarker
)
from LAYER_2_Cognitive_Loop.LAB_001_Emotional_Salience.implementation.emotional_salience_scorer import (
    EmotionalSalienceScorer
)


# ============================================================================
# LAYER 3 SIMPLIFIED INTERFACES
# ============================================================================

class DecayModulator:
    """
    Simplified interface to Layer 3 decay modulation

    Integrates:
    - Emotional salience (Layer 2)
    - Dopamine protection (Layer 4)
    """

    def __init__(self):
        self.base_decay = 0.85

    def compute_decay_rate(
        self,
        salience_score: float,
        dopamine_level: float
    ) -> float:
        """
        Compute decay rate with protection from salience + dopamine

        Parameters:
        -----------
        salience_score : float (0-1)
            Emotional salience
        dopamine_level : float (0-1)
            Dopamine modulation

        Returns:
        --------
        decay_rate : float (0-1)
            Higher = slower decay (more protected)
        """
        # Base decay
        decay_rate = self.base_decay

        # Salience protection
        salience_protection = salience_score * 0.10

        # Dopamine protection
        dopamine_protection = dopamine_level * 0.05

        # Combined
        decay_rate = decay_rate + salience_protection + dopamine_protection

        # Clamp to [0.5, 0.99]
        return max(0.5, min(0.99, decay_rate))


class NoveltyDetector:
    """
    Simplified interface to Layer 3 novelty detection
    """

    def __init__(self):
        pass

    def score(self, novelty: float) -> float:
        """
        Score novelty (pass-through for now, can be enhanced)

        Parameters:
        -----------
        novelty : float (0-1)
            Novelty input

        Returns:
        --------
        novelty_score : float (0-1)
        """
        return novelty


class ConsolidationEngine:
    """
    Simplified interface to Layer 3 consolidation

    Integrates:
    - GABA gating (Layer 4)
    - Salience priority (Layer 2)
    """

    def __init__(self):
        self.gaba_threshold = 0.6

    def is_ready(self, gaba_level: float) -> bool:
        """
        Check if consolidation is ready (high GABA = rest state)

        Parameters:
        -----------
        gaba_level : float (0-1)
            GABA level

        Returns:
        --------
        ready : bool
        """
        return gaba_level >= self.gaba_threshold

    def compute_priority(self, salience_score: float) -> float:
        """
        Compute consolidation priority from salience

        Parameters:
        -----------
        salience_score : float (0-1)
            Emotional salience

        Returns:
        --------
        priority : float (0-1)
        """
        # High salience = high priority
        return salience_score


class AttentionMechanism:
    """
    Simplified interface to Layer 2 attention

    Integrates:
    - Novelty detection (Layer 3)
    - Acetylcholine modulation (Layer 4)
    """

    def __init__(self):
        self.baseline_attention = 0.5

    def compute_level(
        self,
        novelty_score: float,
        ach_level: float,
        emotional_anticipation: float
    ) -> Dict:
        """
        Compute attention level

        Parameters:
        -----------
        novelty_score : float (0-1)
            Novelty detection score
        ach_level : float (0-1)
            Acetylcholine level
        emotional_anticipation : float (0-1)
            Anticipation emotion

        Returns:
        --------
        result : Dict
            {
                'level': float (0-1),
                'novelty_boost': float,
                'ach_boost': float
            }
        """
        # Base attention
        attention = self.baseline_attention

        # Novelty boost (novel stimuli grab attention)
        novelty_boost = novelty_score * 0.3
        attention += novelty_boost

        # ACh boost (acetylcholine enhances attention)
        ach_boost = ach_level * 0.2
        attention += ach_boost

        # Emotional anticipation
        anticipation_boost = emotional_anticipation * 0.15
        attention += anticipation_boost

        # Clamp to [0, 1]
        attention = max(0.0, min(1.0, attention))

        return {
            'level': float(attention),
            'novelty_boost': float(novelty_boost),
            'ach_boost': float(ach_boost)
        }


class EncodingEngine:
    """
    Memory encoding with multi-layer modulation

    Integrates:
    - Attention (Layer 2)
    - Acetylcholine (Layer 4)
    - Salience (Layer 2)
    """

    def __init__(self):
        self.base_strength = 1.0

    def compute_strength(
        self,
        attention_level: float,
        ach_level: float,
        salience_score: float
    ) -> float:
        """
        Compute encoding strength

        Parameters:
        -----------
        attention_level : float (0-1)
            Attention level
        ach_level : float (0-1)
            Acetylcholine level
        salience_score : float (0-1)
            Emotional salience

        Returns:
        --------
        strength : float (>=1.0)
            Encoding strength multiplier
        """
        # Base
        strength = self.base_strength

        # Attention enhancement
        attention_boost = attention_level * 0.5

        # ACh enhancement
        ach_boost = ach_level * 0.4

        # Salience enhancement
        salience_boost = salience_score * 0.3

        # Combined
        strength = strength + attention_boost + ach_boost + salience_boost

        # Clamp to [1.0, 2.5]
        return max(1.0, min(2.5, strength))


# ============================================================================
# LAYER 2 ADVANCED COGNITION (LAB_006, LAB_007, LAB_008)
# ============================================================================

class MetacognitionLogger:
    """
    Simplified interface to LAB_006 Metacognition Logger

    Tracks confidence in decisions for self-awareness.
    """

    def __init__(self):
        self.decisions = []  # List of (confidence, actual_outcome)

    def log_decision(
        self,
        content: str,
        confidence: float,
        salience_score: float
    ) -> Dict:
        """
        Log a decision with confidence

        Parameters:
        -----------
        content : str
            Decision content
        confidence : float (0-1)
            Confidence in this decision
        salience_score : float (0-1)
            Emotional salience of event

        Returns:
        --------
        result : Dict
            {
                'confidence': float,
                'decisions_logged': int,
                'calibration_score': float
            }
        """
        # Log decision
        self.decisions.append({
            'content': content,
            'confidence': confidence,
            'salience': salience_score
        })

        # Compute calibration score
        calibration_score = self._compute_calibration()

        return {
            'confidence': float(confidence),
            'decisions_logged': len(self.decisions),
            'calibration_score': float(calibration_score)
        }

    def _compute_calibration(self) -> float:
        """
        Compute confidence calibration score

        Returns:
        --------
        calibration : float (0-1)
            How well calibrated confidence is
        """
        if len(self.decisions) < 2:
            return 0.5  # Neutral baseline

        # Simple calibration: variance in confidence
        # Lower variance when experience grows = better calibration
        confidences = [d['confidence'] for d in self.decisions]
        mean_conf = sum(confidences) / len(confidences)
        variance = sum((c - mean_conf) ** 2 for c in confidences) / len(confidences)

        # Convert variance to calibration score (inverse relationship)
        # Low variance = high calibration
        calibration = 1.0 - min(variance, 1.0)

        return max(0.0, min(1.0, calibration))

    def compute_confidence(
        self,
        salience_score: float,
        attention_level: float,
        encoding_strength: float
    ) -> float:
        """
        Compute confidence based on cognitive state

        Parameters:
        -----------
        salience_score : float (0-1)
            Emotional salience
        attention_level : float (0-1)
            Attention level
        encoding_strength : float (>=1.0)
            Encoding strength multiplier

        Returns:
        --------
        confidence : float (0-1)
            Decision confidence
        """
        # Confidence increases with:
        # - High salience (clear emotional signal)
        # - High attention (focused processing)
        # - Strong encoding (robust memory formation)

        # Base confidence
        confidence = 0.3  # Baseline uncertainty

        # Salience contribution (0.4 weight)
        confidence += salience_score * 0.4

        # Attention contribution (0.2 weight)
        confidence += attention_level * 0.2

        # Encoding contribution (0.1 weight, normalized)
        encoding_normalized = min((encoding_strength - 1.0) / 1.5, 1.0)
        confidence += encoding_normalized * 0.1

        # Clamp to [0, 1]
        return max(0.0, min(1.0, confidence))


class PredictivePreloader:
    """
    Simplified interface to LAB_007 Predictive Preloading

    Learns temporal patterns and predicts next events.
    """

    def __init__(self):
        self.patterns = {}  # Dict: content → [next_contents]
        self.previous_content = None

    def learn_pattern(
        self,
        current_content: str,
        previous_content: Optional[str] = None
    ):
        """
        Learn temporal pattern: previous → current

        Parameters:
        -----------
        current_content : str
            Current event content
        previous_content : str (optional)
            Previous event content
        """
        if previous_content is None:
            previous_content = self.previous_content

        if previous_content is not None:
            # Learn pattern: previous → current
            if previous_content not in self.patterns:
                self.patterns[previous_content] = []

            self.patterns[previous_content].append(current_content)

        # Update previous
        self.previous_content = current_content

    def predict_next(
        self,
        current_content: str
    ) -> Optional[str]:
        """
        Predict next event based on learned patterns

        Parameters:
        -----------
        current_content : str
            Current event content

        Returns:
        --------
        prediction : str or None
            Predicted next event (or None if no pattern)
        """
        if current_content in self.patterns:
            # Return most frequent next event
            next_events = self.patterns[current_content]
            if next_events:
                # Most common
                from collections import Counter
                most_common = Counter(next_events).most_common(1)
                return most_common[0][0] if most_common else None

        return None

    def get_prediction_confidence(
        self,
        current_content: str
    ) -> float:
        """
        Compute confidence in prediction

        Parameters:
        -----------
        current_content : str
            Current event content

        Returns:
        --------
        confidence : float (0-1)
            Prediction confidence
        """
        if current_content not in self.patterns:
            return 0.0

        next_events = self.patterns[current_content]
        if not next_events:
            return 0.0

        # Confidence based on pattern frequency
        # More observations = higher confidence
        from collections import Counter
        counts = Counter(next_events)
        most_common_count = counts.most_common(1)[0][1]
        total = len(next_events)

        # Frequency ratio + count bonus
        confidence = (most_common_count / total) * min(total / 10.0, 1.0)

        return max(0.0, min(1.0, confidence))

    def get_state(self) -> Dict:
        """
        Get current predictive state

        Returns:
        --------
        state : Dict
            {
                'patterns_learned': int,
                'prediction_confidence': float
            }
        """
        prediction_confidence = 0.0
        if self.previous_content:
            prediction_confidence = self.get_prediction_confidence(self.previous_content)

        return {
            'patterns_learned': len(self.patterns),
            'prediction_confidence': float(prediction_confidence)
        }


class EmotionalContagion:
    """
    Simplified interface to LAB_008 Emotional Contagion

    Spreads emotional states between related events.
    """

    def __init__(self):
        self.recent_emotions = []  # List of (salience, time_step)
        self.time_step = 0
        self.decay_rate = 0.7  # Contagion decays by 30% per event

    def spread_emotion(
        self,
        current_salience: float,
        previous_salience: Optional[float] = None
    ) -> Dict:
        """
        Compute emotional contagion effect

        Parameters:
        -----------
        current_salience : float (0-1)
            Current event salience
        previous_salience : float (0-1, optional)
            Previous event salience

        Returns:
        --------
        result : Dict
            {
                'contagion_effect': float,
                'temporal_decay': float
            }
        """
        # Increment time
        self.time_step += 1

        # Store current emotion
        self.recent_emotions.append({
            'salience': current_salience,
            'time_step': self.time_step
        })

        # Compute contagion from recent high-emotion events
        contagion_effect = 0.0

        for prev_emotion in self.recent_emotions[:-1]:  # Exclude current
            time_delta = self.time_step - prev_emotion['time_step']

            # Temporal decay
            temporal_decay = self.decay_rate ** time_delta

            # Contagion strength
            source_strength = prev_emotion['salience']

            # Contagion spreads proportionally to source salience
            contagion = source_strength * temporal_decay

            contagion_effect += contagion

        # Normalize by number of recent events
        if len(self.recent_emotions) > 1:
            contagion_effect /= (len(self.recent_emotions) - 1)

        # Clamp to [0, 1]
        contagion_effect = max(0.0, min(1.0, contagion_effect))

        # Temporal decay for most recent event
        temporal_decay = self.decay_rate if len(self.recent_emotions) > 1 else 1.0

        # Cleanup old emotions (keep last 10)
        if len(self.recent_emotions) > 10:
            self.recent_emotions = self.recent_emotions[-10:]

        return {
            'contagion_effect': float(contagion_effect),
            'temporal_decay': float(temporal_decay)
        }


# ============================================================================
# COGNITIVE STACK ORCHESTRATOR
# ============================================================================

class CognitiveStack:
    """
    Full Cognitive Stack Integration

    Orchestrates:
    - Layer 2: Cognitive Loop (emotions, attention, salience)
    - Layer 3: Memory Dynamics (decay, consolidation, novelty)
    - Layer 4: Neurochemistry (dopamine, ACh, GABA, serotonin, NE)

    Complete flow:
    Event → Emotion → Neuro → Attention → Encoding → Memory → Consolidation
    """

    def __init__(self):
        # Layer 2: Cognitive (Basic)
        self.emotional_salience = EmotionalSalienceScorer()
        self.attention = AttentionMechanism()

        # Layer 2: Cognitive (Advanced - LAB_006, LAB_007, LAB_008)
        self.metacognition = MetacognitionLogger()
        self.predictive = PredictivePreloader()
        self.contagion = EmotionalContagion()

        # Layer 3: Memory
        self.decay_modulation = DecayModulator()
        self.novelty_detection = NoveltyDetector()
        self.consolidation = ConsolidationEngine()
        self.encoding = EncodingEngine()

        # Layer 4: Neuro (via existing bridge)
        self.neuro_bridge = NeuroEmotionalBridge()

    def process_event(
        self,
        content: str,
        emotional_state: EmotionalState,
        somatic_marker: Optional[SomaticMarker] = None,
        novelty: float = 0.5
    ) -> Dict:
        """
        Full stack event processing

        Parameters:
        -----------
        content : str
            Event content
        emotional_state : EmotionalState
            Current emotional state (8D)
        somatic_marker : SomaticMarker (optional)
            Somatic marker (7D)
        novelty : float (0-1)
            Novelty score

        Returns:
        --------
        result : Dict
            {
                'emotional_state': dict,
                'neuro_state': dict,
                'attention': dict,
                'memory': dict
            }
        """
        # Default somatic marker if not provided
        if somatic_marker is None:
            somatic_marker = SomaticMarker()

        # ====================================================================
        # PHASE 1: EMOTIONAL PROCESSING (Layer 2)
        # ====================================================================

        # Compute emotional salience
        salience_score = self._compute_salience(emotional_state, somatic_marker)

        # ====================================================================
        # PHASE 2: NEURO MODULATION (Layer 4)
        # ====================================================================

        # Forward pass: Emotions → Neurotransmitters
        neuro_result = self.neuro_bridge.process_event(emotional_state, somatic_marker)
        neuro_state = neuro_result['neuro_state']

        # ====================================================================
        # PHASE 3: ATTENTION GATING (Layer 2 + Layer 3 + Layer 4)
        # ====================================================================

        # Novelty detection
        novelty_score = self.novelty_detection.score(novelty)

        # Attention computation (novelty + ACh + anticipation)
        attention_result = self.attention.compute_level(
            novelty_score=novelty_score,
            ach_level=neuro_state['acetylcholine'],
            emotional_anticipation=emotional_state.anticipation
        )

        # ====================================================================
        # PHASE 4: MEMORY ENCODING (Layer 3)
        # ====================================================================

        # Encoding strength (attention + ACh + salience)
        encoding_strength = self.encoding.compute_strength(
            attention_level=attention_result['level'],
            ach_level=neuro_state['acetylcholine'],
            salience_score=salience_score
        )

        # ====================================================================
        # PHASE 5: DECAY PROTECTION (Layer 3 + Layer 4)
        # ====================================================================

        # Decay rate (salience + dopamine protection)
        decay_rate = self.decay_modulation.compute_decay_rate(
            salience_score=salience_score,
            dopamine_level=neuro_state['dopamine']
        )

        # ====================================================================
        # PHASE 6: CONSOLIDATION (Layer 3 + Layer 4)
        # ====================================================================

        # Consolidation readiness (GABA gating)
        consolidation_ready = self.consolidation.is_ready(neuro_state['gaba'])

        # Consolidation priority (salience)
        consolidation_priority = self.consolidation.compute_priority(salience_score)

        # ====================================================================
        # PHASE 7: METACOGNITION (LAB_006)
        # ====================================================================

        # Compute confidence based on cognitive state
        confidence = self.metacognition.compute_confidence(
            salience_score=salience_score,
            attention_level=attention_result['level'],
            encoding_strength=encoding_strength
        )

        # Log decision
        metacognition_result = self.metacognition.log_decision(
            content=content,
            confidence=confidence,
            salience_score=salience_score
        )

        # ====================================================================
        # PHASE 8: PREDICTIVE PRELOADING (LAB_007)
        # ====================================================================

        # Learn temporal pattern
        self.predictive.learn_pattern(current_content=content)

        # Get predictive state
        predictive_result = self.predictive.get_state()

        # ====================================================================
        # PHASE 9: EMOTIONAL CONTAGION (LAB_008)
        # ====================================================================

        # Compute emotional contagion
        contagion_result = self.contagion.spread_emotion(
            current_salience=salience_score
        )

        # ====================================================================
        # RETURN COMPLETE STATE
        # ====================================================================

        return {
            'emotional_state': {
                'joy': float(emotional_state.joy),
                'anticipation': float(emotional_state.anticipation),
                'surprise': float(emotional_state.surprise),
                'trust': float(emotional_state.trust)
            },
            'neuro_state': neuro_state,
            'attention': attention_result,
            'memory': {
                'content': content,
                'salience_score': float(salience_score),
                'encoding_strength': float(encoding_strength),
                'decay_rate': float(decay_rate),
                'consolidation_ready': bool(consolidation_ready),
                'consolidation_priority': float(consolidation_priority)
            },
            'metacognition': metacognition_result,
            'predictive': predictive_result,
            'contagion': contagion_result
        }

    def _compute_salience(
        self,
        emotional_state: EmotionalState,
        somatic_marker: SomaticMarker
    ) -> float:
        """
        Compute emotional salience score

        Uses LAB_001 algorithm (simplified)

        Parameters:
        -----------
        emotional_state : EmotionalState
            8D emotional state
        somatic_marker : SomaticMarker
            Somatic marker

        Returns:
        --------
        salience : float (0-1)
        """
        # Emotional intensity (L2 norm)
        emotions = [
            emotional_state.joy,
            emotional_state.trust,
            emotional_state.fear,
            emotional_state.surprise,
            emotional_state.sadness,
            emotional_state.disgust,
            emotional_state.anger,
            emotional_state.anticipation
        ]

        l2_norm = np.sqrt(sum(e**2 for e in emotions))
        intensity = l2_norm / np.sqrt(8)

        # Emotional complexity (entropy)
        total = sum(emotions) + 1e-10
        probs = [e / total for e in emotions]
        entropy = -sum(p * np.log2(p) if p > 0 else 0 for p in probs)
        complexity = entropy / 3.0  # Normalize

        # Somatic contribution
        valence_contrib = abs(somatic_marker.valence) * 0.2
        arousal_contrib = somatic_marker.arousal * 0.15

        # Weighted sum
        salience = (
            intensity * 0.40 +
            complexity * 0.25 +
            valence_contrib +
            arousal_contrib
        )

        # Clamp to [0, 1]
        return max(0.0, min(1.0, salience))


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Test full stack
    stack = CognitiveStack()

    # Breakthrough event
    emotional_state = EmotionalState(
        joy=0.95,
        surprise=0.9,
        anticipation=0.85,
        trust=0.8
    )
    somatic_marker = SomaticMarker(
        valence=0.95,
        arousal=0.8,
        situation="breakthrough"
    )

    print("=" * 60)
    print("COGNITIVE STACK - FULL INTEGRATION TEST")
    print("=" * 60)

    print("\n📊 INPUT:")
    print(f"  Content: Major breakthrough discovery")
    print(f"  Emotional State: joy={emotional_state.joy}, surprise={emotional_state.surprise}")
    print(f"  Novelty: 0.95")

    result = stack.process_event(
        content="Major breakthrough discovery",
        emotional_state=emotional_state,
        somatic_marker=somatic_marker,
        novelty=0.95
    )

    print("\n🧠 LAYER 2 (Cognitive):")
    print(f"  Salience: {result['memory']['salience_score']:.3f}")
    print(f"  Attention: {result['attention']['level']:.3f}")

    print("\n🧪 LAYER 4 (Neuro):")
    print(f"  Dopamine: {result['neuro_state']['dopamine']:.3f}")
    print(f"  Acetylcholine: {result['neuro_state']['acetylcholine']:.3f}")
    print(f"  GABA: {result['neuro_state']['gaba']:.3f}")

    print("\n💾 LAYER 3 (Memory):")
    print(f"  Encoding Strength: {result['memory']['encoding_strength']:.3f}")
    print(f"  Decay Rate: {result['memory']['decay_rate']:.3f}")
    print(f"  Consolidation Ready: {result['memory']['consolidation_ready']}")
    print(f"  Consolidation Priority: {result['memory']['consolidation_priority']:.3f}")

    print("\n🤔 LAYER 2 ADVANCED (Metacognition):")
    print(f"  Confidence: {result['metacognition']['confidence']:.3f}")
    print(f"  Decisions Logged: {result['metacognition']['decisions_logged']}")
    print(f"  Calibration Score: {result['metacognition']['calibration_score']:.3f}")

    print("\n🔮 LAYER 2 ADVANCED (Predictive):")
    print(f"  Patterns Learned: {result['predictive']['patterns_learned']}")
    print(f"  Prediction Confidence: {result['predictive']['prediction_confidence']:.3f}")

    print("\n💫 LAYER 2 ADVANCED (Emotional Contagion):")
    print(f"  Contagion Effect: {result['contagion']['contagion_effect']:.3f}")
    print(f"  Temporal Decay: {result['contagion']['temporal_decay']:.3f}")

    print("\n✅ Full stack integration complete (Session 9: +LAB_006, +LAB_007, +LAB_008)")
