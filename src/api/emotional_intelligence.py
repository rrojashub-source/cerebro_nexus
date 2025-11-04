"""
LAB_028: Emotional Intelligence - Recognition and Regulation

Implements emotional intelligence frameworks:
- Mayer & Salovey (1997): Four-branch model of EI
- Gross (2002): Emotion regulation strategies
- Bar-On (2006): Emotional-social intelligence model
- Goleman (1995): EI framework (self-awareness, regulation, social skills)

Core Functions:
1. Emotion recognition (facial, vocal, contextual)
2. Emotion understanding (causes, consequences)
3. Emotion regulation (reappraisal, suppression, acceptance)
4. Emotional self-awareness
5. Social awareness and empathy
6. Relationship management

Neuroscience Foundation:
- Amygdala: Emotion detection, arousal
- Insula: Interoception, emotional awareness
- vmPFC: Emotion regulation, reappraisal
- dlPFC: Cognitive control of emotion
- ACC: Conflict monitoring, emotion-cognition integration

Integration:
- ← LAB_001 (Emotional Salience) for emotion importance
- ← LAB_008 (Emotional Contagion) for emotion spread
- ← LAB_013 (Dopamine) for positive emotion rewards
- ← LAB_014 (Serotonin) for mood regulation
- ← LAB_024 (Empathy) for emotional resonance
"""

import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import deque
from enum import Enum
import numpy as np


class EmotionType(Enum):
    """Basic emotions (Ekman)"""
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    DISGUST = "disgust"
    SURPRISE = "surprise"
    NEUTRAL = "neutral"


class RegulationStrategy(Enum):
    """Emotion regulation strategies (Gross)"""
    SITUATION_SELECTION = "situation_selection"  # Avoid/approach situations
    SITUATION_MODIFICATION = "situation_modification"  # Change situation
    ATTENTIONAL_DEPLOYMENT = "attentional_deployment"  # Distraction
    COGNITIVE_REAPPRAISAL = "cognitive_reappraisal"  # Reinterpret meaning
    RESPONSE_MODULATION = "response_modulation"  # Suppress expression


class EmotionalCompetency(Enum):
    """Goleman's EI competencies"""
    SELF_AWARENESS = "self_awareness"
    SELF_REGULATION = "self_regulation"
    MOTIVATION = "motivation"
    EMPATHY = "empathy"
    SOCIAL_SKILLS = "social_skills"


@dataclass
class EmotionRecognition:
    """Recognized emotion"""
    timestamp: float
    emotion: EmotionType
    intensity: float  # 0-1
    confidence: float  # 0-1
    source: str  # "facial", "vocal", "contextual", "self"
    person_id: Optional[str]


@dataclass
class RegulationAttempt:
    """Emotion regulation attempt"""
    timestamp: float
    initial_emotion: EmotionType
    initial_intensity: float
    strategy: RegulationStrategy
    effort_level: float  # 0-1
    success_rate: float  # 0-1
    final_intensity: float
    cognitive_cost: float  # 0-1


@dataclass
class EmotionalState:
    """Current emotional state"""
    timestamp: float
    primary_emotion: EmotionType
    intensity: float
    valence: float  # -1 to +1
    arousal: float  # 0-1
    regulation_active: bool
    self_awareness_level: float  # 0-1


class EmotionRecognizer:
    """Recognizes emotions from multiple cues"""

    def __init__(self):
        # Facial expression patterns (simplified)
        self.facial_patterns = {
            "smile": EmotionType.JOY,
            "frown": EmotionType.SADNESS,
            "scowl": EmotionType.ANGER,
            "wide_eyes": EmotionType.FEAR,
            "wrinkled_nose": EmotionType.DISGUST,
            "raised_eyebrows": EmotionType.SURPRISE,
        }

        # Vocal patterns
        self.vocal_patterns = {
            "high_pitch": EmotionType.FEAR,
            "loud": EmotionType.ANGER,
            "soft": EmotionType.SADNESS,
            "fast": EmotionType.JOY,
        }

    def recognize_from_facial(
        self,
        facial_cues: List[str],
        person_id: str
    ) -> EmotionRecognition:
        """
        Recognize emotion from facial expressions.

        Returns emotion recognition.
        """
        # Simple pattern matching (in real system: CNN)
        detected_emotions = []
        for cue in facial_cues:
            if cue in self.facial_patterns:
                detected_emotions.append(self.facial_patterns[cue])

        if not detected_emotions:
            emotion = EmotionType.NEUTRAL
            confidence = 0.5
        else:
            # Most frequent
            emotion = max(set(detected_emotions), key=detected_emotions.count)
            confidence = detected_emotions.count(emotion) / len(detected_emotions)

        # Intensity from number of cues
        intensity = min(1.0, len(facial_cues) * 0.3)

        return EmotionRecognition(
            timestamp=time.time(),
            emotion=emotion,
            intensity=intensity,
            confidence=confidence,
            source="facial",
            person_id=person_id
        )

    def recognize_from_context(
        self,
        situation: str,
        person_id: Optional[str] = None
    ) -> EmotionRecognition:
        """
        Infer emotion from situational context.

        Returns emotion recognition.
        """
        # Context-based inference
        situation_lower = situation.lower()

        if "success" in situation_lower or "win" in situation_lower:
            emotion = EmotionType.JOY
            intensity = 0.7
        elif "loss" in situation_lower or "failure" in situation_lower:
            emotion = EmotionType.SADNESS
            intensity = 0.6
        elif "threat" in situation_lower or "danger" in situation_lower:
            emotion = EmotionType.FEAR
            intensity = 0.8
        elif "injustice" in situation_lower or "frustration" in situation_lower:
            emotion = EmotionType.ANGER
            intensity = 0.7
        elif "unexpected" in situation_lower:
            emotion = EmotionType.SURPRISE
            intensity = 0.6
        else:
            emotion = EmotionType.NEUTRAL
            intensity = 0.3

        return EmotionRecognition(
            timestamp=time.time(),
            emotion=emotion,
            intensity=intensity,
            confidence=0.6,
            source="contextual",
            person_id=person_id
        )

    def integrate_multimodal(
        self,
        recognitions: List[EmotionRecognition]
    ) -> EmotionRecognition:
        """
        Integrate multiple emotion recognitions.

        Returns integrated emotion.
        """
        if not recognitions:
            return EmotionRecognition(
                timestamp=time.time(),
                emotion=EmotionType.NEUTRAL,
                intensity=0.0,
                confidence=0.0,
                source="integrated",
                person_id=None
            )

        # Weighted by confidence
        emotion_scores = {}
        for recog in recognitions:
            if recog.emotion not in emotion_scores:
                emotion_scores[recog.emotion] = 0.0
            emotion_scores[recog.emotion] += recog.confidence * recog.intensity

        best_emotion = max(emotion_scores, key=emotion_scores.get)
        avg_intensity = np.mean([r.intensity for r in recognitions])
        avg_confidence = np.mean([r.confidence for r in recognitions])

        return EmotionRecognition(
            timestamp=time.time(),
            emotion=best_emotion,
            intensity=avg_intensity,
            confidence=avg_confidence,
            source="integrated",
            person_id=recognitions[0].person_id
        )


class EmotionRegulator:
    """Implements emotion regulation strategies"""

    def __init__(self):
        self.regulation_history: deque = deque(maxlen=100)

        # Strategy effectiveness (learned over time)
        self.strategy_effectiveness = {
            RegulationStrategy.COGNITIVE_REAPPRAISAL: 0.7,
            RegulationStrategy.ATTENTIONAL_DEPLOYMENT: 0.6,
            RegulationStrategy.RESPONSE_MODULATION: 0.4,
            RegulationStrategy.SITUATION_MODIFICATION: 0.8,
            RegulationStrategy.SITUATION_SELECTION: 0.9,
        }

    def regulate_emotion(
        self,
        current_emotion: EmotionType,
        current_intensity: float,
        strategy: RegulationStrategy,
        effort: float = 0.7
    ) -> RegulationAttempt:
        """
        Apply emotion regulation strategy.

        Returns regulation attempt record.
        """
        effectiveness = self.strategy_effectiveness[strategy]

        # Regulation success (depends on effectiveness, effort, and intensity)
        success_rate = effectiveness * effort * (1.0 - current_intensity * 0.3)
        success_rate = np.clip(success_rate, 0.0, 1.0)

        # New intensity after regulation
        intensity_reduction = success_rate * current_intensity * 0.6
        final_intensity = max(0.0, current_intensity - intensity_reduction)

        # Cognitive cost (reappraisal costs more than suppression initially)
        if strategy == RegulationStrategy.COGNITIVE_REAPPRAISAL:
            cognitive_cost = 0.6 * effort
        elif strategy == RegulationStrategy.RESPONSE_MODULATION:
            cognitive_cost = 0.3 * effort  # Low initial cost, but long-term costs
        elif strategy == RegulationStrategy.ATTENTIONAL_DEPLOYMENT:
            cognitive_cost = 0.4 * effort
        else:
            cognitive_cost = 0.5 * effort

        attempt = RegulationAttempt(
            timestamp=time.time(),
            initial_emotion=current_emotion,
            initial_intensity=current_intensity,
            strategy=strategy,
            effort_level=effort,
            success_rate=success_rate,
            final_intensity=final_intensity,
            cognitive_cost=cognitive_cost
        )

        self.regulation_history.append(attempt)

        return attempt

    def select_strategy(
        self,
        emotion: EmotionType,
        intensity: float,
        context: str
    ) -> RegulationStrategy:
        """
        Select appropriate regulation strategy.

        Gross's process model: Earlier strategies more effective.

        Returns recommended strategy.
        """
        # High-intensity emotions: situation selection/modification
        if intensity > 0.7:
            if "avoidable" in context.lower():
                return RegulationStrategy.SITUATION_SELECTION
            else:
                return RegulationStrategy.COGNITIVE_REAPPRAISAL

        # Medium intensity: reappraisal or distraction
        elif intensity > 0.4:
            return RegulationStrategy.COGNITIVE_REAPPRAISAL

        # Low intensity: any strategy
        else:
            return RegulationStrategy.ATTENTIONAL_DEPLOYMENT

    def update_strategy_effectiveness(
        self,
        strategy: RegulationStrategy,
        success: bool
    ):
        """Update learned effectiveness of strategy"""
        learning_rate = 0.1

        if success:
            self.strategy_effectiveness[strategy] = min(
                1.0,
                self.strategy_effectiveness[strategy] + learning_rate
            )
        else:
            self.strategy_effectiveness[strategy] = max(
                0.0,
                self.strategy_effectiveness[strategy] - learning_rate * 0.5
            )


class EmotionalAwarenessMonitor:
    """Monitors emotional self-awareness"""

    def __init__(self):
        self.awareness_level = 0.5
        self.interoceptive_accuracy = 0.5  # Accuracy of bodily sensation detection

    def assess_awareness(
        self,
        reported_emotion: EmotionType,
        actual_emotion: EmotionType,
        reported_intensity: float,
        actual_intensity: float
    ) -> float:
        """
        Assess emotional self-awareness accuracy.

        Returns awareness score (0-1).
        """
        # Emotion match
        emotion_match = 1.0 if reported_emotion == actual_emotion else 0.0

        # Intensity accuracy
        intensity_error = abs(reported_intensity - actual_intensity)
        intensity_accuracy = 1.0 - intensity_error

        # Combined awareness
        awareness = 0.6 * emotion_match + 0.4 * intensity_accuracy

        # Update running awareness level
        self.awareness_level = 0.9 * self.awareness_level + 0.1 * awareness

        return awareness

    def detect_emotional_state(
        self,
        bodily_signals: Dict[str, float]
    ) -> EmotionalState:
        """
        Detect emotional state from interoceptive signals.

        bodily_signals: {"heart_rate": 0.8, "muscle_tension": 0.6, ...}

        Returns detected emotional state.
        """
        # Arousal from physiological signals
        arousal = np.mean([
            bodily_signals.get("heart_rate", 0.5),
            bodily_signals.get("respiration", 0.5),
            bodily_signals.get("skin_conductance", 0.5),
        ])

        # Valence from signals
        valence = bodily_signals.get("facial_feedback", 0.0)

        # Map arousal/valence to emotion (Russell's circumplex)
        if valence > 0.5 and arousal > 0.5:
            emotion = EmotionType.JOY
            intensity = 0.7
        elif valence < -0.5 and arousal > 0.5:
            emotion = EmotionType.ANGER
            intensity = 0.8
        elif valence < -0.5 and arousal < 0.5:
            emotion = EmotionType.SADNESS
            intensity = 0.6
        elif valence > 0.5 and arousal < 0.5:
            emotion = EmotionType.JOY  # Contentment
            intensity = 0.5
        else:
            emotion = EmotionType.NEUTRAL
            intensity = 0.3

        state = EmotionalState(
            timestamp=time.time(),
            primary_emotion=emotion,
            intensity=intensity,
            valence=valence,
            arousal=arousal,
            regulation_active=False,
            self_awareness_level=self.awareness_level
        )

        return state


class EmotionalIntelligenceSystem:
    """
    Main LAB_028 implementation.

    Manages:
    - Emotion recognition (self and others)
    - Emotion regulation
    - Emotional self-awareness
    - Social awareness
    """

    def __init__(self):
        # Components
        self.emotion_recognizer = EmotionRecognizer()
        self.emotion_regulator = EmotionRegulator()
        self.awareness_monitor = EmotionalAwarenessMonitor()

        # State
        self.current_state: Optional[EmotionalState] = None
        self.recognized_emotions: deque = deque(maxlen=100)

        # Competencies (0-1 scores)
        self.competencies = {
            EmotionalCompetency.SELF_AWARENESS: 0.5,
            EmotionalCompetency.SELF_REGULATION: 0.5,
            EmotionalCompetency.MOTIVATION: 0.5,
            EmotionalCompetency.EMPATHY: 0.5,
            EmotionalCompetency.SOCIAL_SKILLS: 0.5,
        }

    def recognize_emotion(
        self,
        source: str,
        cues: List[str],
        person_id: Optional[str] = None,
        context: Optional[str] = None
    ) -> EmotionRecognition:
        """
        Recognize emotion from cues.

        Returns emotion recognition.
        """
        if source == "facial":
            recognition = self.emotion_recognizer.recognize_from_facial(cues, person_id or "unknown")
        elif source == "contextual":
            recognition = self.emotion_recognizer.recognize_from_context(
                context or " ".join(cues),
                person_id
            )
        else:
            # Default: contextual
            recognition = self.emotion_recognizer.recognize_from_context(
                " ".join(cues),
                person_id
            )

        self.recognized_emotions.append(recognition)

        # Update empathy competency (recognizing others' emotions)
        if person_id and person_id != "self":
            self.competencies[EmotionalCompetency.EMPATHY] = min(
                1.0,
                self.competencies[EmotionalCompetency.EMPATHY] + 0.01
            )

        return recognition

    def assess_self_emotion(
        self,
        bodily_signals: Dict[str, float]
    ) -> EmotionalState:
        """
        Assess own emotional state.

        Returns emotional state.
        """
        state = self.awareness_monitor.detect_emotional_state(bodily_signals)
        self.current_state = state

        # Update self-awareness competency
        self.competencies[EmotionalCompetency.SELF_AWARENESS] = state.self_awareness_level

        return state

    def regulate_emotion(
        self,
        strategy: Optional[RegulationStrategy] = None,
        effort: float = 0.7
    ) -> RegulationAttempt:
        """
        Regulate current emotion.

        Returns regulation attempt.
        """
        if not self.current_state:
            # No current state
            return None

        # Select strategy if not provided
        if strategy is None:
            strategy = self.emotion_regulator.select_strategy(
                self.current_state.primary_emotion,
                self.current_state.intensity,
                context="general"
            )

        # Apply regulation
        attempt = self.emotion_regulator.regulate_emotion(
            self.current_state.primary_emotion,
            self.current_state.intensity,
            strategy,
            effort
        )

        # Update state
        self.current_state.intensity = attempt.final_intensity
        self.current_state.regulation_active = True

        # Update self-regulation competency
        self.competencies[EmotionalCompetency.SELF_REGULATION] = min(
            1.0,
            self.competencies[EmotionalCompetency.SELF_REGULATION] + 0.02 * attempt.success_rate
        )

        # Update strategy effectiveness
        success = attempt.success_rate > 0.5
        self.emotion_regulator.update_strategy_effectiveness(strategy, success)

        return attempt

    def respond_to_emotion(
        self,
        recognized_emotion: EmotionRecognition,
        person_id: str
    ) -> str:
        """
        Generate appropriate emotional response.

        Returns response action.
        """
        emotion = recognized_emotion.emotion
        intensity = recognized_emotion.intensity

        # Empathic responses
        if emotion == EmotionType.SADNESS and intensity > 0.5:
            response = "Offer comfort and support"
        elif emotion == EmotionType.ANGER and intensity > 0.5:
            response = "Acknowledge frustration, give space"
        elif emotion == EmotionType.FEAR:
            response = "Provide reassurance"
        elif emotion == EmotionType.JOY:
            response = "Share in positive emotion"
        else:
            response = "Maintain neutral supportive presence"

        # Update social skills competency
        self.competencies[EmotionalCompetency.SOCIAL_SKILLS] = min(
            1.0,
            self.competencies[EmotionalCompetency.SOCIAL_SKILLS] + 0.01
        )

        return response

    def get_ei_profile(self) -> Dict:
        """Get emotional intelligence profile"""
        return {
            "competencies": {c.value: score for c, score in self.competencies.items()},
            "overall_ei": np.mean(list(self.competencies.values())),
            "self_awareness_level": self.awareness_monitor.awareness_level,
            "regulation_history_length": len(self.emotion_regulator.regulation_history),
            "recognition_history_length": len(self.recognized_emotions),
        }

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        return {
            "current_emotion": self.current_state.primary_emotion.value if self.current_state else "none",
            "current_intensity": self.current_state.intensity if self.current_state else 0.0,
            "overall_ei": np.mean(list(self.competencies.values())),
            "total_recognitions": len(self.recognized_emotions),
            "total_regulations": len(self.emotion_regulator.regulation_history),
            "avg_regulation_success": (
                np.mean([r.success_rate for r in self.emotion_regulator.regulation_history])
                if self.emotion_regulator.regulation_history else 0.0
            ),
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_028: Emotional Intelligence - Test")
    print("=" * 60)

    system = EmotionalIntelligenceSystem()

    # Scenario 1: Emotion recognition from facial cues
    print("\n😊 Scenario 1: Recognizing emotion from facial expressions...")
    recognition = system.recognize_emotion(
        source="facial",
        cues=["smile", "raised_eyebrows"],
        person_id="alice"
    )
    print(f"  Recognized emotion: {recognition.emotion.value}")
    print(f"  Intensity: {recognition.intensity:.3f}")
    print(f"  Confidence: {recognition.confidence:.3f}")
    print(f"  Source: {recognition.source}")

    # Scenario 2: Self-awareness (interoception)
    print("\n🧘 Scenario 2: Assessing own emotional state...")
    bodily_signals = {
        "heart_rate": 0.8,
        "respiration": 0.7,
        "skin_conductance": 0.6,
        "facial_feedback": 0.3,
        "muscle_tension": 0.5,
    }
    state = system.assess_self_emotion(bodily_signals)
    print(f"  Detected emotion: {state.primary_emotion.value}")
    print(f"  Intensity: {state.intensity:.3f}")
    print(f"  Valence: {state.valence:.3f}")
    print(f"  Arousal: {state.arousal:.3f}")
    print(f"  Self-awareness level: {state.self_awareness_level:.3f}")

    # Scenario 3: Emotion regulation
    print("\n🎭 Scenario 3: Regulating negative emotion...")
    # Simulate high-intensity fear
    system.current_state = EmotionalState(
        timestamp=time.time(),
        primary_emotion=EmotionType.FEAR,
        intensity=0.8,
        valence=-0.6,
        arousal=0.9,
        regulation_active=False,
        self_awareness_level=0.6
    )

    print(f"  Initial: {system.current_state.primary_emotion.value}, intensity={system.current_state.intensity:.3f}")

    # Apply cognitive reappraisal
    attempt = system.regulate_emotion(strategy=RegulationStrategy.COGNITIVE_REAPPRAISAL, effort=0.8)
    print(f"  Strategy: {attempt.strategy.value}")
    print(f"  Success rate: {attempt.success_rate:.3f}")
    print(f"  Final intensity: {attempt.final_intensity:.3f} (reduced by {attempt.initial_intensity - attempt.final_intensity:.3f})")
    print(f"  Cognitive cost: {attempt.cognitive_cost:.3f}")

    # Scenario 4: Multiple regulation attempts
    print("\n🔄 Scenario 4: Learning regulation effectiveness...")
    for i in range(5):
        # Simulate emotion
        system.current_state = EmotionalState(
            timestamp=time.time(),
            primary_emotion=EmotionType.ANGER,
            intensity=0.7,
            valence=-0.5,
            arousal=0.8,
            regulation_active=False,
            self_awareness_level=0.6
        )

        attempt = system.regulate_emotion(strategy=RegulationStrategy.COGNITIVE_REAPPRAISAL)

    print(f"  After 5 attempts:")
    print(f"  Strategy effectiveness: {system.emotion_regulator.strategy_effectiveness[RegulationStrategy.COGNITIVE_REAPPRAISAL]:.3f}")
    print(f"  Self-regulation competency: {system.competencies[EmotionalCompetency.SELF_REGULATION]:.3f}")

    # Scenario 5: Social awareness and response
    print("\n🤝 Scenario 5: Recognizing and responding to others' emotions...")
    # Recognize sadness in another person
    recognition = system.recognize_emotion(
        source="contextual",
        cues=["loss", "grief"],
        person_id="bob",
        context="Bob experienced a loss"
    )
    print(f"  Recognized {recognition.person_id}'s emotion: {recognition.emotion.value}")
    print(f"  Intensity: {recognition.intensity:.3f}")

    # Generate empathic response
    response = system.respond_to_emotion(recognition, "bob")
    print(f"  Appropriate response: '{response}'")

    # EI Profile
    print("\n📊 Emotional Intelligence Profile:")
    profile = system.get_ei_profile()
    print(f"  Overall EI: {profile['overall_ei']:.3f}")
    print(f"  Competencies:")
    for comp, score in profile['competencies'].items():
        print(f"    {comp}: {score:.3f}")

    # Final statistics
    print("\n📈 Final Statistics:")
    stats = system.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

    print("\n✅ LAB_028 Test Complete!")
