"""
LAB_045: Hyperfocus Mechanism System

Homeostasis: "Intense single-task concentration"

Key Mechanisms:
- Intense attention focus (narrowed scope)
- Time blindness (lose track of time)
- Task immersion (high absorption)
- Resistance to interruption
- Dopamine modulation (LAB_035 integration)

Mathematical Model:
- Hyperfocus strength: H = (attention * immersion * motivation) / task_count
- Time distortion: D = actual_time / perceived_time
- Interruption resistance: R = hyperfocus_strength * base_resistance
- Dopamine modulation: H_mod = H * (1 + dopamine * k)

Key Papers:
- Ashinoff & Abu-Akel (2021): Hyperfocus: the forgotten frontier of attention
- Carson (2011): Hyperfocus in creativity and ADHD
- Brown (2005): Attention & hyperfocus in ADHD
"""

import math
from typing import Dict, Optional


class HyperfocusSystem:
    """
    Hyperfocus Mechanism: Intense single-task concentration

    Core principle: Extreme attention narrowing + task immersion

    Implements:
    - Intense attention focus
    - Time blindness detection
    - Task immersion assessment
    - Interruption resistance
    - Dopamine-driven hyperfocus
    """

    def __init__(
        self,
        hyperfocus_threshold: float = 0.85,
        interruption_resistance: float = 0.8
    ):
        """
        Initialize Hyperfocus System

        Args:
            hyperfocus_threshold: Threshold for hyperfocus detection [0-1]
            interruption_resistance: Base resistance to interruptions [0-1]
        """
        self.hyperfocus_threshold = hyperfocus_threshold
        self.interruption_resistance = interruption_resistance

        # Hyperfocus state
        self.in_hyperfocus = False

        # Hyperfocus history
        self.hyperfocus_episodes: list = []

    def assess_attention_scope(
        self,
        task_count: int,
        attention_level: float
    ) -> Dict:
        """
        Assess attention scope (narrow vs broad)

        Args:
            task_count: Number of concurrent tasks
            attention_level: Attention level [0-1]

        Returns:
            Attention scope assessment
        """
        # Narrow scope: single task + high attention
        if task_count == 1 and attention_level > 0.9:
            attention_scope = "narrow"
            hyperfocus_possible = True
        elif task_count <= 2 and attention_level > 0.85:
            attention_scope = "moderate"
            hyperfocus_possible = False
        else:
            attention_scope = "broad"
            hyperfocus_possible = False

        return {
            "task_count": task_count,
            "attention_level": float(attention_level),
            "attention_scope": attention_scope,
            "hyperfocus_possible": hyperfocus_possible
        }

    def measure_focus_intensity(
        self,
        duration_minutes: float
    ) -> Dict:
        """
        Measure focus intensity

        Args:
            duration_minutes: Duration of continuous focus

        Returns:
            Focus intensity measurement
        """
        # Intensity increases with duration (up to saturation)
        # I = 1 - exp(-k * t)
        k = 0.01  # Growth rate
        focus_intensity = 1.0 - math.exp(-k * duration_minutes)

        return {
            "duration_minutes": float(duration_minutes),
            "focus_intensity": float(focus_intensity)
        }

    def assess_time_awareness(
        self,
        actual_minutes: float,
        perceived_minutes: float
    ) -> Dict:
        """
        Assess time awareness (blindness)

        Args:
            actual_minutes: Actual elapsed time
            perceived_minutes: Subjectively perceived time

        Returns:
            Time awareness assessment
        """
        if perceived_minutes == 0:
            perceived_minutes = 1  # Avoid division by zero

        # Distortion ratio: actual / perceived
        distortion_ratio = actual_minutes / perceived_minutes

        # Time blind if distortion > 3.0 (extreme)
        time_blind = distortion_ratio > 3.0

        # Hyperfocus indicator if distortion > 5.0
        hyperfocus_indicator = distortion_ratio > 5.0

        return {
            "actual_minutes": float(actual_minutes),
            "perceived_minutes": float(perceived_minutes),
            "distortion_ratio": float(distortion_ratio),
            "time_blind": time_blind,
            "hyperfocus_indicator": hyperfocus_indicator
        }

    def detect_hyperfocus(
        self,
        attention_level: float,
        task_count: int,
        immersion_level: float,
        intrinsic_motivation: bool
    ) -> Dict:
        """
        Detect hyperfocus state

        Args:
            attention_level: Attention level [0-1]
            task_count: Number of concurrent tasks
            immersion_level: Task immersion level [0-1]
            intrinsic_motivation: Whether motivation is intrinsic

        Returns:
            Hyperfocus detection result
        """
        # Hyperfocus requires single task
        if task_count > 1:
            return {
                "in_hyperfocus": False,
                "reason": "Multiple tasks (hyperfocus requires single task)"
            }

        # Motivation factor
        motivation_factor = 1.0 if intrinsic_motivation else 0.5

        # Hyperfocus strength: (attention * immersion * motivation)
        hyperfocus_strength = attention_level * immersion_level * motivation_factor

        # Hyperfocus detected if strength > threshold
        in_hyperfocus = hyperfocus_strength > self.hyperfocus_threshold

        # Update state
        self.in_hyperfocus = in_hyperfocus

        # Flow overlap (LAB_043 integration)
        # Hyperfocus is more intense than flow (threshold 0.9 vs 0.7)
        flow_active = hyperfocus_strength > 0.7

        return {
            "in_hyperfocus": in_hyperfocus,
            "hyperfocus_strength": float(hyperfocus_strength),
            "attention_level": float(attention_level),
            "immersion_level": float(immersion_level),
            "intrinsic_motivation": intrinsic_motivation,
            "flow_active": flow_active
        }

    def attempt_interruption(
        self,
        interruption_strength: float
    ) -> Dict:
        """
        Attempt to interrupt hyperfocus

        Args:
            interruption_strength: Strength of interruption [0-1]

        Returns:
            Interruption attempt result
        """
        if not self.in_hyperfocus:
            # Not in hyperfocus → easily interrupted
            interrupted = True
        else:
            # In hyperfocus → resistant to interruptions
            # Interrupted if interruption_strength > resistance
            interrupted = interruption_strength > self.interruption_resistance

            if interrupted:
                self.in_hyperfocus = False

        return {
            "interruption_strength": float(interruption_strength),
            "interrupted": interrupted,
            "in_hyperfocus": self.in_hyperfocus
        }

    def trigger_from_dopamine(
        self,
        dopamine_level: float
    ) -> Dict:
        """
        Trigger hyperfocus from dopamine surge (LAB_035 integration)

        Args:
            dopamine_level: Dopamine level [0-1]

        Returns:
            Dopamine trigger result
        """
        # High dopamine → hyperfocus trigger
        if dopamine_level > 0.8:
            hyperfocus_triggered = True
            self.in_hyperfocus = True
        else:
            hyperfocus_triggered = False

        return {
            "dopamine_level": float(dopamine_level),
            "hyperfocus_triggered": hyperfocus_triggered
        }

    def modulate_by_dopamine(
        self,
        base_intensity: float,
        dopamine_level: float
    ) -> Dict:
        """
        Modulate hyperfocus intensity by dopamine (LAB_035 integration)

        Args:
            base_intensity: Base hyperfocus intensity [0-1]
            dopamine_level: Dopamine level [0-1]

        Returns:
            Modulated intensity result
        """
        # Dopamine modulation: H_mod = H * (1 + dopamine * k)
        modulation_factor = 1.0 + dopamine_level * 0.3

        modulated_intensity = min(1.0, base_intensity * modulation_factor)

        return {
            "base_intensity": float(base_intensity),
            "dopamine_level": float(dopamine_level),
            "modulated_intensity": float(modulated_intensity)
        }

    def apply_to_skill_learning(
        self,
        practice_duration: float
    ) -> Dict:
        """
        Apply hyperfocus boost to skill learning (LAB_040 integration)

        Args:
            practice_duration: Practice duration (minutes)

        Returns:
            Learning boost result
        """
        if self.in_hyperfocus:
            # Hyperfocus → 2x learning boost (stronger than flow 1.5x)
            learning_boost = 2.0
        else:
            learning_boost = 1.0

        effective_practice = practice_duration * learning_boost

        return {
            "practice_duration": float(practice_duration),
            "learning_boost": float(learning_boost),
            "effective_practice": float(effective_practice)
        }

    def process_event(
        self,
        event_type: str,
        **kwargs
    ) -> Dict:
        """
        Process hyperfocus event

        Args:
            event_type: Type of event ("hyperfocus_check", "interruption", etc.)
            **kwargs: Event-specific parameters

        Returns:
            Processing result
        """
        if event_type == "hyperfocus_check":
            return self.detect_hyperfocus(
                attention_level=kwargs["attention_level"],
                task_count=kwargs["task_count"],
                immersion_level=kwargs["immersion_level"],
                intrinsic_motivation=kwargs.get("intrinsic_motivation", True)
            )

        elif event_type == "interruption":
            return self.attempt_interruption(
                interruption_strength=kwargs["interruption_strength"]
            )

        else:
            return {"error": f"Unknown event type: {event_type}"}

    def get_state(self) -> Dict:
        """
        Get current state of hyperfocus system

        Returns:
            System state with hyperfocus metrics
        """
        return {
            "in_hyperfocus": self.in_hyperfocus,
            "hyperfocus_threshold": self.hyperfocus_threshold,
            "interruption_resistance": self.interruption_resistance,
            "hyperfocus_episodes_count": len(self.hyperfocus_episodes)
        }
