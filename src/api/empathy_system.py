"""
LAB_024: Empathy System - Emotional Resonance & Affective Perspective Taking

Implements empathic processes:
- Decety & Jackson (2004): The functional architecture of human empathy
- Singer & Lamm (2009): The social neuroscience of empathy
- Preston & de Waal (2002): Empathy: Its ultimate and proximate bases
- Batson (2009): These things called empathy

Core Functions:
1. Emotional resonance (feeling what others feel)
2. Affective perspective taking (imagining their feelings)
3. Empathic concern (sympathy, compassion)
4. Personal distress (self-focused aversive response)
5. Empathic accuracy (correctly identifying emotions)
6. Emotion regulation during empathy

Neuroscience Foundation:
- Anterior insula (AI): Emotional resonance
- Anterior cingulate cortex (ACC): Shared pain
- Inferior frontal gyrus (IFG): Mirror neurons
- Temporoparietal junction (TPJ): Perspective taking

Integration:
- ← LAB_023 (Theory of Mind) for cognitive empathy
- ← LAB_001 (Emotional Salience) for emotion detection
- ← LAB_008 (Emotional Contagion) for automatic sharing
- → LAB_028 (Emotional Intelligence) for regulation
"""

import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import numpy as np
from enum import Enum


class EmpathyType(Enum):
    """Types of empathy"""
    COGNITIVE = "cognitive"      # Understanding (cold empathy)
    AFFECTIVE = "affective"      # Feeling (hot empathy)
    COMPASSIONATE = "compassionate"  # Concern + motivation to help


class EmotionType(Enum):
    """Basic emotions"""
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    DISGUST = "disgust"
    SURPRISE = "surprise"


@dataclass
class EmotionalState:
    """Emotional state of agent"""
    agent_id: str
    emotion: EmotionType
    intensity: float  # 0-1
    valence: float  # -1 (negative) to +1 (positive)
    arousal: float  # 0 (calm) to 1 (excited)


@dataclass
class EmpathicResponse:
    """Empathic response to observed emotion"""
    timestamp: float
    target_agent: str
    observed_emotion: EmotionType
    observed_intensity: float
    own_resonance: float  # How much we feel it (0-1)
    empathy_type: EmpathyType
    accuracy: float  # How accurate our inference was
    personal_distress: float  # Self-focused distress (0-1)
    empathic_concern: float  # Other-focused concern (0-1)


@dataclass
class CompassionEvent:
    """Compassionate response leading to action"""
    timestamp: float
    target_agent: str
    perceived_need: str
    compassion_level: float
    helping_motivation: float
    action_taken: Optional[str] = None


class EmotionalResonator:
    """
    Implements emotional resonance (automatic sharing).

    Mirror neuron-like emotional contagion.
    """

    def __init__(self, resonance_baseline: float = 0.6):
        self.resonance_baseline = resonance_baseline
        self.resonance_history: deque = deque(maxlen=500)

    def resonate(
        self,
        observed_emotion: EmotionType,
        observed_intensity: float,
        social_closeness: float = 0.5
    ) -> float:
        """
        Compute emotional resonance.

        Resonance increases with:
        - Intensity of observed emotion
        - Social closeness
        - Baseline resonance capacity

        Returns resonance strength (0-1).
        """
        # Base resonance from observed intensity
        base = observed_intensity * self.resonance_baseline

        # Modulated by social closeness
        # Closer relationships → stronger resonance
        resonance = base * (0.5 + social_closeness * 0.5)

        # Negative emotions resonate more strongly (negativity bias)
        if observed_emotion in [EmotionType.SADNESS, EmotionType.FEAR, EmotionType.ANGER]:
            resonance *= 1.2

        # Bounded 0-1
        resonance = min(1.0, resonance)

        return resonance

    def simulate_embodiment(
        self,
        emotion: EmotionType,
        intensity: float
    ) -> Dict[str, float]:
        """
        Simulate somatic markers of emotion.

        Returns physiological response.
        """
        # Map emotions to bodily responses
        if emotion == EmotionType.FEAR:
            return {
                "heart_rate": intensity * 0.8,
                "muscle_tension": intensity * 0.7,
                "sweating": intensity * 0.6
            }
        elif emotion == EmotionType.SADNESS:
            return {
                "heart_rate": -intensity * 0.3,  # Slowed
                "energy": -intensity * 0.6,       # Depleted
                "tears": intensity * 0.4
            }
        elif emotion == EmotionType.ANGER:
            return {
                "heart_rate": intensity * 0.9,
                "muscle_tension": intensity * 0.9,
                "temperature": intensity * 0.5  # Feeling hot
            }
        else:
            # Default mild response
            return {"heart_rate": intensity * 0.3}


class PerspectiveTaker:
    """
    Affective perspective taking (imagine their feelings).

    More controlled than automatic resonance.
    """

    def __init__(self):
        self.perspective_history: deque = deque(maxlen=500)

    def imagine_emotion(
        self,
        target_situation: str,
        target_context: Dict[str, any],
        own_experience: Optional[str] = None
    ) -> Tuple[EmotionType, float]:
        """
        Imagine what emotion target feels in situation.

        Uses simulation (mental imagery).

        Returns:
            - imagined_emotion
            - intensity
        """
        # Simplified emotion inference from situation keywords
        # In full system, would use episodic memory + simulation

        situation_lower = target_situation.lower()

        # Pattern matching (learned associations)
        if "loss" in situation_lower or "death" in situation_lower:
            return EmotionType.SADNESS, 0.8
        elif "threat" in situation_lower or "danger" in situation_lower:
            return EmotionType.FEAR, 0.7
        elif "injustice" in situation_lower or "betrayal" in situation_lower:
            return EmotionType.ANGER, 0.7
        elif "success" in situation_lower or "win" in situation_lower:
            return EmotionType.JOY, 0.8
        else:
            # Uncertain
            return EmotionType.SURPRISE, 0.3


class EmpathicAccuracyEvaluator:
    """
    Evaluates accuracy of empathic inferences.

    Compares inferred emotions with actual emotions (when known).
    """

    def __init__(self):
        self.accuracy_history: deque = deque(maxlen=500)

    def compute_accuracy(
        self,
        inferred_emotion: EmotionType,
        inferred_intensity: float,
        actual_emotion: EmotionType,
        actual_intensity: float
    ) -> float:
        """
        Compute empathic accuracy.

        Returns accuracy score (0-1).
        """
        # Emotion match
        if inferred_emotion == actual_emotion:
            emotion_match = 1.0
        else:
            # Partial credit for similar emotions
            # (simplified - could use emotion space)
            emotion_match = 0.3

        # Intensity accuracy
        intensity_error = abs(inferred_intensity - actual_intensity)
        intensity_accuracy = 1.0 - intensity_error

        # Combined
        accuracy = (emotion_match * 0.7) + (intensity_accuracy * 0.3)

        self.accuracy_history.append({
            "timestamp": time.time(),
            "accuracy": accuracy
        })

        return accuracy

    def get_average_accuracy(self) -> float:
        """Get recent average empathic accuracy"""
        if not self.accuracy_history:
            return 0.5  # Unknown

        recent = list(self.accuracy_history)[-20:]
        return np.mean([entry["accuracy"] for entry in recent])


class CompassionModule:
    """
    Implements compassion (empathic concern + helping motivation).

    Transforms empathy into prosocial action.
    """

    def __init__(self):
        self.compassion_history: deque = deque(maxlen=500)

    def generate_compassion(
        self,
        observed_distress: float,
        perceived_need: str,
        empathic_resonance: float,
        personal_distress: float
    ) -> Tuple[float, float]:
        """
        Generate compassion response.

        High empathic concern + low personal distress → compassion
        High personal distress → self-focused, less helping

        Returns:
            - compassion_level
            - helping_motivation
        """
        # Compassion from resonance, reduced by personal distress
        compassion = empathic_resonance * (1.0 - personal_distress * 0.6)

        # Helping motivation from compassion + severity of need
        need_severity = observed_distress
        helping_motivation = compassion * (0.5 + need_severity * 0.5)

        return compassion, helping_motivation

    def decide_helping_action(
        self,
        helping_motivation: float,
        cost_of_helping: float,
        perceived_efficacy: float
    ) -> Tuple[bool, Optional[str]]:
        """
        Decide whether to help and what action.

        Based on cost-benefit and efficacy.

        Returns:
            - will_help
            - action
        """
        # Help if motivation exceeds cost and efficacy is reasonable
        net_motivation = helping_motivation - cost_of_helping + perceived_efficacy

        will_help = net_motivation > 0.5

        if will_help:
            # Choose action based on need (simplified)
            if helping_motivation > 0.7:
                action = "direct_intervention"
            elif helping_motivation > 0.4:
                action = "offer_support"
            else:
                action = "express_concern"
        else:
            action = None

        return will_help, action


class EmpathySystem:
    """
    Main LAB_024 implementation.

    Integrates:
    - Emotional resonance (automatic)
    - Perspective taking (controlled)
    - Empathic accuracy evaluation
    - Compassion and helping
    """

    def __init__(self, resonance_baseline: float = 0.6):
        # Components
        self.resonator = EmotionalResonator(resonance_baseline)
        self.perspective_taker = PerspectiveTaker()
        self.accuracy_evaluator = EmpathicAccuracyEvaluator()
        self.compassion_module = CompassionModule()

        # History
        self.empathic_responses: deque = deque(maxlen=1000)
        self.compassion_events: deque = deque(maxlen=500)

        # Statistics
        self.total_empathic_responses = 0
        self.total_compassion_events = 0

    def respond_to_emotion(
        self,
        agent_id: str,
        observed_emotion: EmotionType,
        observed_intensity: float,
        social_closeness: float = 0.5,
        empathy_type: EmpathyType = EmpathyType.AFFECTIVE
    ) -> EmpathicResponse:
        """
        Generate empathic response to observed emotion.

        Returns empathic response.
        """
        # Emotional resonance (automatic)
        resonance = self.resonator.resonate(
            observed_emotion,
            observed_intensity,
            social_closeness
        )

        # Personal distress (self-focused aversive response)
        # Higher for intense negative emotions
        if observed_emotion in [EmotionType.SADNESS, EmotionType.FEAR]:
            personal_distress = resonance * 0.6
        else:
            personal_distress = resonance * 0.2

        # Empathic concern (other-focused)
        # Inverse of personal distress
        empathic_concern = resonance * (1.0 - personal_distress * 0.5)

        # Accuracy (will be updated if actual emotion known)
        accuracy = 0.7  # Default estimate

        # Create response
        response = EmpathicResponse(
            timestamp=time.time(),
            target_agent=agent_id,
            observed_emotion=observed_emotion,
            observed_intensity=observed_intensity,
            own_resonance=resonance,
            empathy_type=empathy_type,
            accuracy=accuracy,
            personal_distress=personal_distress,
            empathic_concern=empathic_concern
        )

        self.empathic_responses.append(response)
        self.total_empathic_responses += 1

        return response

    def imagine_others_emotion(
        self,
        agent_id: str,
        situation: str,
        context: Dict[str, any]
    ) -> Tuple[EmotionType, float]:
        """
        Imagine emotion through perspective taking.

        Returns inferred emotion and intensity.
        """
        emotion, intensity = self.perspective_taker.imagine_emotion(
            situation,
            context
        )

        # Generate empathic response based on imagined emotion
        self.respond_to_emotion(
            agent_id,
            emotion,
            intensity,
            empathy_type=EmpathyType.COGNITIVE
        )

        return emotion, intensity

    def evaluate_empathic_accuracy(
        self,
        inferred_emotion: EmotionType,
        inferred_intensity: float,
        actual_emotion: EmotionType,
        actual_intensity: float
    ) -> float:
        """
        Evaluate accuracy of empathic inference.

        Returns accuracy score.
        """
        return self.accuracy_evaluator.compute_accuracy(
            inferred_emotion,
            inferred_intensity,
            actual_emotion,
            actual_intensity
        )

    def generate_compassion(
        self,
        agent_id: str,
        perceived_distress: float,
        perceived_need: str,
        cost_of_helping: float = 0.3,
        perceived_efficacy: float = 0.7
    ) -> Tuple[bool, Optional[str]]:
        """
        Generate compassionate response.

        Returns:
            - will_help
            - helping_action
        """
        # Get recent empathic response for this agent
        recent_responses = [
            r for r in list(self.empathic_responses)[-5:]
            if r.target_agent == agent_id
        ]

        if recent_responses:
            latest = recent_responses[-1]
            resonance = latest.own_resonance
            personal_distress = latest.personal_distress
        else:
            # Default
            resonance = 0.5
            personal_distress = 0.3

        # Generate compassion
        compassion, helping_motivation = self.compassion_module.generate_compassion(
            perceived_distress,
            perceived_need,
            resonance,
            personal_distress
        )

        # Decide action
        will_help, action = self.compassion_module.decide_helping_action(
            helping_motivation,
            cost_of_helping,
            perceived_efficacy
        )

        # Record event
        event = CompassionEvent(
            timestamp=time.time(),
            target_agent=agent_id,
            perceived_need=perceived_need,
            compassion_level=compassion,
            helping_motivation=helping_motivation,
            action_taken=action
        )

        self.compassion_events.append(event)
        self.total_compassion_events += 1

        return will_help, action

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        return {
            "total_empathic_responses": self.total_empathic_responses,
            "total_compassion_events": self.total_compassion_events,
            "average_empathic_accuracy": self.accuracy_evaluator.get_average_accuracy(),
            "average_resonance": (
                np.mean([r.own_resonance for r in list(self.empathic_responses)])
                if self.empathic_responses else 0.0
            ),
            "average_personal_distress": (
                np.mean([r.personal_distress for r in list(self.empathic_responses)])
                if self.empathic_responses else 0.0
            ),
            "average_empathic_concern": (
                np.mean([r.empathic_concern for r in list(self.empathic_responses)])
                if self.empathic_responses else 0.0
            ),
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_024: Empathy System - Test")
    print("=" * 60)

    # Create empathy system
    empathy = EmpathySystem(resonance_baseline=0.6)

    # Scenario 1: Emotional resonance
    print("\n💔 Scenario 1: Observing sadness...")
    response = empathy.respond_to_emotion(
        agent_id="friend",
        observed_emotion=EmotionType.SADNESS,
        observed_intensity=0.8,
        social_closeness=0.9
    )
    print(f"  Observed: SADNESS (0.80 intensity)")
    print(f"  Resonance: {response.own_resonance:.3f}")
    print(f"  Personal Distress: {response.personal_distress:.3f}")
    print(f"  Empathic Concern: {response.empathic_concern:.3f}")

    # Scenario 2: Perspective taking
    print("\n🤔 Scenario 2: Imagining emotion...")
    emotion, intensity = empathy.imagine_others_emotion(
        agent_id="colleague",
        situation="Experienced a major loss",
        context={}
    )
    print(f"  Situation: 'Experienced a major loss'")
    print(f"  Imagined Emotion: {emotion.value}")
    print(f"  Imagined Intensity: {intensity:.3f}")

    # Scenario 3: Empathic accuracy
    print("\n🎯 Scenario 3: Empathic accuracy evaluation...")
    accuracy = empathy.evaluate_empathic_accuracy(
        inferred_emotion=EmotionType.SADNESS,
        inferred_intensity=0.8,
        actual_emotion=EmotionType.SADNESS,
        actual_intensity=0.75
    )
    print(f"  Inferred: SADNESS (0.80)")
    print(f"  Actual: SADNESS (0.75)")
    print(f"  Accuracy: {accuracy:.3f}")

    # Scenario 4: Compassion and helping
    print("\n🤝 Scenario 4: Compassionate response...")
    will_help, action = empathy.generate_compassion(
        agent_id="friend",
        perceived_distress=0.8,
        perceived_need="emotional support",
        cost_of_helping=0.2,
        perceived_efficacy=0.8
    )
    print(f"  Perceived Distress: 0.80")
    print(f"  Will Help: {will_help}")
    print(f"  Action: {action}")

    # Show final statistics
    print("\n📈 Final Statistics:")
    stats = empathy.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

    print("\n✅ LAB_024 Test Complete!")
