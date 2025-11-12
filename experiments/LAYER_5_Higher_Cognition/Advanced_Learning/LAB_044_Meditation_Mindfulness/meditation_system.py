"""
LAB_044: Meditation/Mindfulness System

Homeostasis: "Awareness & emotional regulation"

Key Mechanisms:
- Present-moment awareness (attention to now)
- Non-judgmental observation (acceptance)
- Breath awareness (anchor point)
- Body scan (somatic awareness)
- Emotional regulation via acceptance

Mathematical Model:
- Awareness growth: A(t) = A0 + duration * k * (1 - A0)
- Awareness decay: A(t) = A0 * exp(-λ * days)
- Calmness: C = 1 / (1 + breath_rate / baseline)
- Tension release: T_new = T_old * (1 - duration * k)

Key Papers:
- Kabat-Zinn (2003): Mindfulness-Based Stress Reduction
- Tang et al. (2015): The neuroscience of mindfulness meditation
- Lutz et al. (2008): Attention regulation and monitoring in meditation
"""

import math
from typing import Dict, Optional


class MeditationSystem:
    """
    Meditation/Mindfulness: Awareness & emotional regulation

    Core principle: Present-moment awareness without judgment

    Implements:
    - Present-moment awareness training
    - Non-judgmental observation
    - Breath awareness (anchor)
    - Body scan (somatic awareness)
    - Emotion regulation via acceptance
    """

    def __init__(
        self,
        breath_rate: int = 12,
        body_scan_duration: int = 20
    ):
        """
        Initialize Meditation System

        Args:
            breath_rate: Breaths per minute (default 12)
            body_scan_duration: Default body scan duration (minutes)
        """
        self.breath_rate = breath_rate
        self.body_scan_duration = body_scan_duration

        # Mindfulness level [0-1]
        self.mindfulness_level = 0.0

        # Meditation state
        self.is_meditating = False

        # Total meditation time (minutes)
        self.total_meditation_time = 0.0

    def practice_present_moment_awareness(
        self,
        duration_minutes: float
    ) -> Dict:
        """
        Practice present-moment awareness

        Args:
            duration_minutes: Practice duration (minutes)

        Returns:
            Practice result
        """
        # Awareness growth: A(t) = A0 + duration * k * (1 - A0)
        # Growth rate slower at high awareness levels
        growth_rate = 0.02  # Per minute
        awareness_increase = duration_minutes * growth_rate * (1.0 - self.mindfulness_level)

        self.mindfulness_level = min(1.0, self.mindfulness_level + awareness_increase)

        # Track total meditation time
        self.total_meditation_time += duration_minutes

        # Stress reduction (LAB_033 integration)
        stress_reduction = awareness_increase * 0.5

        return {
            "duration_minutes": float(duration_minutes),
            "mindfulness_level": float(self.mindfulness_level),
            "awareness_increase": float(awareness_increase),
            "stress_reduction": float(stress_reduction)
        }

    def apply_awareness_decay(
        self,
        days: int
    ) -> Dict:
        """
        Apply awareness decay (without practice)

        Args:
            days: Days without practice

        Returns:
            Decay result
        """
        # Awareness decay: A(t) = A0 * exp(-λ * days)
        decay_rate = 0.05  # Per day
        decay_factor = math.exp(-decay_rate * days)

        self.mindfulness_level = self.mindfulness_level * decay_factor

        return {
            "days": days,
            "mindfulness_level": float(self.mindfulness_level),
            "decay_factor": float(decay_factor)
        }

    def practice_nonjudgmental_observation(
        self,
        emotional_intensity: float
    ) -> Dict:
        """
        Practice non-judgmental observation

        Args:
            emotional_intensity: Intensity of emotion [0-1]

        Returns:
            Observation result
        """
        # Acceptance level increases with mindfulness
        base_acceptance = 0.3

        # Practicing non-judgmental observation gives immediate boost
        practice_boost = 0.3

        acceptance_level = base_acceptance + self.mindfulness_level * 0.7 + practice_boost

        # Reactivity reduction: higher acceptance → lower reactivity
        reactivity_reduced = acceptance_level > 0.5

        return {
            "emotional_intensity": float(emotional_intensity),
            "acceptance_level": float(acceptance_level),
            "reactivity_reduced": reactivity_reduced
        }

    def observe_with_judgment(
        self,
        emotional_intensity: float
    ) -> Dict:
        """
        Observe with judgment (control condition)

        Args:
            emotional_intensity: Intensity of emotion [0-1]

        Returns:
            Observation result
        """
        # Judgment reduces acceptance
        acceptance_level = 0.2

        return {
            "emotional_intensity": float(emotional_intensity),
            "acceptance_level": float(acceptance_level),
            "reactivity_reduced": False
        }

    def practice_breath_awareness(
        self,
        duration_minutes: float
    ) -> Dict:
        """
        Practice breath awareness (anchor point)

        Args:
            duration_minutes: Practice duration (minutes)

        Returns:
            Breath awareness result
        """
        # Calmness increases with slower breathing
        baseline_breath_rate = 12  # Normal resting rate
        calmness_factor = baseline_breath_rate / max(1, self.breath_rate)
        calmness_level = min(1.0, calmness_factor * 0.7)

        # Mind wandering decreases with practice
        mind_wandering = max(0.0, 0.5 - duration_minutes * 0.015)

        return {
            "duration_minutes": float(duration_minutes),
            "calmness_level": float(calmness_level),
            "mind_wandering": float(mind_wandering),
            "breath_rate": self.breath_rate
        }

    def perform_body_scan(
        self,
        duration_minutes: float,
        initial_tension: float = 0.5
    ) -> Dict:
        """
        Perform body scan (somatic awareness)

        Args:
            duration_minutes: Scan duration (minutes)
            initial_tension: Initial tension level [0-1]

        Returns:
            Body scan result
        """
        # Somatic awareness increases with duration
        somatic_awareness = min(1.0, duration_minutes / 20.0)  # 20 min = full awareness

        # Tension release: T_new = T_old * (1 - duration * k)
        release_rate = 0.025  # Per minute
        tension_reduction = initial_tension * duration_minutes * release_rate
        tension_after = max(0.0, initial_tension - tension_reduction)

        return {
            "duration_minutes": float(duration_minutes),
            "somatic_awareness": float(somatic_awareness),
            "tension_before": float(initial_tension),
            "tension_after": float(tension_after)
        }

    def regulate_emotion(
        self,
        emotion: str,
        intensity: float
    ) -> Dict:
        """
        Regulate emotion through mindfulness

        Args:
            emotion: Emotion type (e.g., "fear", "anger", "sadness")
            intensity: Emotion intensity [0-1]

        Returns:
            Emotion regulation result
        """
        # Regulation strength depends on mindfulness level
        regulation_strength = self.mindfulness_level

        # Reduce intensity via acceptance (not suppression)
        regulated_intensity = intensity * (1.0 - regulation_strength * 0.5)

        # Regulation type
        if self.mindfulness_level > 0.5:
            regulation_type = "acceptance"
            suppressed = False
        else:
            regulation_type = "minimal"
            suppressed = False

        return {
            "emotion": emotion,
            "initial_intensity": float(intensity),
            "regulated_intensity": float(regulated_intensity),
            "regulation_strength": float(regulation_strength),
            "regulation_type": regulation_type,
            "suppressed": suppressed
        }

    def get_rest_quality_boost(self) -> Dict:
        """
        Get rest quality boost from meditation (LAB_034 integration)

        Returns:
            Rest quality boost
        """
        if self.is_meditating or self.mindfulness_level > 0.5:
            # Meditation enhances rest quality
            rest_quality_multiplier = 1.2
        else:
            rest_quality_multiplier = 1.0

        return {
            "rest_quality_multiplier": float(rest_quality_multiplier)
        }

    def get_dmn_modulation(self) -> Dict:
        """
        Get Default Mode Network modulation (LAB_046 integration)

        Returns:
            DMN modulation result
        """
        if self.is_meditating:
            # Meditation modulates DMN (reduces self-referential processing)
            dmn_modulated = True
            dmn_activity_level = 0.3  # Reduced
        else:
            dmn_modulated = False
            dmn_activity_level = 0.7  # Baseline

        return {
            "dmn_modulated": dmn_modulated,
            "dmn_activity_level": float(dmn_activity_level)
        }

    def process_event(
        self,
        event_type: str,
        **kwargs
    ) -> Dict:
        """
        Process meditation event

        Args:
            event_type: Type of event ("meditate", "body_scan", etc.)
            **kwargs: Event-specific parameters

        Returns:
            Processing result
        """
        if event_type == "meditate":
            self.is_meditating = True
            result = self.practice_present_moment_awareness(
                duration_minutes=kwargs["duration_minutes"]
            )
            self.is_meditating = False
            return result

        elif event_type == "body_scan":
            result = self.perform_body_scan(
                duration_minutes=kwargs["duration_minutes"],
                initial_tension=kwargs.get("initial_tension", 0.5)
            )
            return result

        else:
            return {"error": f"Unknown event type: {event_type}"}

    def get_state(self) -> Dict:
        """
        Get current state of meditation system

        Returns:
            System state with meditation metrics
        """
        return {
            "mindfulness_level": float(self.mindfulness_level),
            "is_meditating": self.is_meditating,
            "total_meditation_time": float(self.total_meditation_time),
            "breath_rate": self.breath_rate,
            "body_scan_duration": self.body_scan_duration
        }
