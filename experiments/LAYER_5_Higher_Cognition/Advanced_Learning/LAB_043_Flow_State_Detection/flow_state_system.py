"""
LAB_043: Flow State Detection System

Homeostasis: "Optimal experience & performance"

Key Mechanisms:
- Challenge-skill balance: C ≈ S (optimal when matched)
- Attention absorption: Deep focus without distraction
- Time distortion: Subjective time ≠ objective time
- Clear goals + immediate feedback
- Intrinsic motivation (autotelic experience)

Mathematical Model:
- Balance: B = 1 - |challenge - skill|
- Absorption: A = focus_duration / (1 + distractions)
- Time distortion: D = actual_time / perceived_time
- Flow strength: F = (B + A + G + F_fb) / 4

Key Papers:
- Csikszentmihalyi (1990): Flow: The Psychology of Optimal Experience
- Nakamura & Csikszentmihalyi (2002): The concept of flow
- Ullén et al. (2010): Proneness for psychological flow in everyday life
"""

import math
from typing import Dict, Optional


class FlowStateSystem:
    """
    Flow State Detection: Optimal experience & performance

    Core principle: Flow occurs when challenge matches skill

    Implements:
    - Challenge-skill balance assessment
    - Attention absorption measurement
    - Time distortion detection
    - Flow state detection and maintenance
    """

    def __init__(
        self,
        flow_threshold: float = 0.7,
        initial_skill: float = 0.5
    ):
        """
        Initialize Flow State System

        Args:
            flow_threshold: Threshold for flow detection [0-1]
            initial_skill: Initial skill level [0-1]
        """
        self.flow_threshold = flow_threshold
        self.skill_level = initial_skill

        # Flow state
        self.in_flow = False
        self.flow_duration_minutes = 0.0

        # Flow history
        self.flow_episodes: list = []

    def assess_challenge_skill_balance(
        self,
        challenge: float,
        skill: float
    ) -> Dict:
        """
        Assess challenge-skill balance

        Args:
            challenge: Challenge level [0-1]
            skill: Skill level [0-1]

        Returns:
            Balance assessment
        """
        # Balance: 1 - |challenge - skill|
        difference = abs(challenge - skill)
        balance = 1.0 - difference

        # Flow possible if balance > 0.8 (within ±0.2)
        flow_possible = balance > 0.8

        # Determine state
        if flow_possible:
            state = "flow_zone"
        elif challenge > skill + 0.2:
            state = "anxiety"
        elif skill > challenge + 0.2:
            state = "boredom"
        else:
            state = "neutral"

        return {
            "challenge": float(challenge),
            "skill": float(skill),
            "balance": float(balance),
            "flow_possible": flow_possible,
            "state": state
        }

    def measure_attention_absorption(
        self,
        focus_duration_minutes: float,
        distraction_count: int
    ) -> Dict:
        """
        Measure attention absorption (focus depth)

        Args:
            focus_duration_minutes: Duration of focused work
            distraction_count: Number of distractions

        Returns:
            Absorption measurement
        """
        # Absorption: focus / (1 + distractions)
        # Normalize by duration (assume 60min baseline)
        normalized_duration = min(1.0, focus_duration_minutes / 60.0)

        absorption_level = normalized_duration / (1.0 + distraction_count * 0.1)

        absorption_level = min(1.0, absorption_level)

        return {
            "focus_duration_minutes": float(focus_duration_minutes),
            "distraction_count": distraction_count,
            "absorption_level": float(absorption_level)
        }

    def measure_time_distortion(
        self,
        actual_minutes: float,
        perceived_minutes: float
    ) -> Dict:
        """
        Measure time distortion

        Args:
            actual_minutes: Actual elapsed time
            perceived_minutes: Subjectively perceived time

        Returns:
            Time distortion measurement
        """
        if perceived_minutes == 0:
            perceived_minutes = 1  # Avoid division by zero

        # Distortion ratio: actual / perceived
        # > 1 = Time passed faster (flow)
        # < 1 = Time passed slower (no flow)
        distortion_ratio = actual_minutes / perceived_minutes

        # Flow indicator: distortion > 1.5
        flow_indicator = distortion_ratio > 1.5

        return {
            "actual_minutes": float(actual_minutes),
            "perceived_minutes": float(perceived_minutes),
            "distortion_ratio": float(distortion_ratio),
            "flow_indicator": flow_indicator
        }

    def detect_flow(
        self,
        challenge: float,
        skill: float,
        attention_absorption: float,
        clear_goals: bool,
        immediate_feedback: bool
    ) -> Dict:
        """
        Detect flow state

        Args:
            challenge: Challenge level [0-1]
            skill: Skill level [0-1]
            attention_absorption: Absorption level [0-1]
            clear_goals: Whether goals are clear
            immediate_feedback: Whether feedback is immediate

        Returns:
            Flow detection result
        """
        # Assess challenge-skill balance
        balance_result = self.assess_challenge_skill_balance(
            challenge=challenge,
            skill=skill
        )

        balance_score = balance_result["balance"]

        # Goals clarity score
        goals_score = 1.0 if clear_goals else 0.0

        # Feedback immediacy score
        feedback_score = 1.0 if immediate_feedback else 0.0

        # Flow strength: average of all components
        flow_strength = (balance_score + attention_absorption + goals_score + feedback_score) / 4.0

        # Flow detected if:
        # 1. Overall strength > threshold
        # 2. Critical components: balance > 0.8 (strict) AND absorption > 0.7
        critical_components_met = (balance_score > 0.8 and attention_absorption > 0.7)
        in_flow = (flow_strength > self.flow_threshold) and critical_components_met

        # Update state
        previous_flow = self.in_flow
        self.in_flow = in_flow

        # Determine exit reason if flow breaks
        exit_reason = None
        if previous_flow and not in_flow:
            if attention_absorption < 0.5:
                exit_reason = "low_absorption"
            elif balance_score < 0.8:
                exit_reason = "challenge_skill_mismatch"
            else:
                exit_reason = "conditions_not_met"

        return {
            "in_flow": in_flow,
            "flow_strength": float(flow_strength),
            "balance_score": float(balance_score),
            "attention_absorption": float(attention_absorption),
            "clear_goals": clear_goals,
            "immediate_feedback": immediate_feedback,
            "exit_reason": exit_reason,
            "hyperfocus_active": attention_absorption > 0.9  # LAB_045 integration
        }

    def enter_flow(self) -> Dict:
        """
        Enter flow state (explicit)

        Returns:
            Flow entry result
        """
        self.in_flow = True
        self.flow_duration_minutes = 0.0

        return {
            "flow_entered": True
        }

    def update_flow_duration(
        self,
        duration_minutes: float
    ) -> Dict:
        """
        Update flow duration

        Args:
            duration_minutes: Duration to add (minutes)

        Returns:
            Duration update result
        """
        if self.in_flow:
            self.flow_duration_minutes += duration_minutes

        return {
            "flow_duration": float(self.flow_duration_minutes)
        }

    def get_flow_duration(self) -> float:
        """
        Get current flow duration

        Returns:
            Flow duration (minutes)
        """
        return self.flow_duration_minutes

    def apply_to_skill_learning(
        self,
        practice_duration: float
    ) -> Dict:
        """
        Apply flow boost to skill learning (LAB_040 integration)

        Args:
            practice_duration: Practice duration (minutes)

        Returns:
            Learning boost result
        """
        if self.in_flow:
            # Flow state → 1.5x learning boost
            learning_boost = 1.5
        else:
            learning_boost = 1.0

        effective_practice = practice_duration * learning_boost

        return {
            "practice_duration": float(practice_duration),
            "learning_boost": float(learning_boost),
            "effective_practice": float(effective_practice)
        }

    def get_motivation_level(self) -> Dict:
        """
        Get motivation level

        Returns:
            Motivation level
        """
        if self.in_flow:
            motivation_type = "intrinsic"
            motivation_level = 0.9
        else:
            motivation_type = "extrinsic"
            motivation_level = 0.5

        return {
            "motivation_type": motivation_type,
            "motivation_level": float(motivation_level)
        }

    def process_event(
        self,
        event_type: str,
        **kwargs
    ) -> Dict:
        """
        Process flow event

        Args:
            event_type: Type of event ("flow_check", "skill_update", etc.)
            **kwargs: Event-specific parameters

        Returns:
            Processing result
        """
        if event_type == "flow_check":
            # Use current skill if not provided
            skill = kwargs.get("skill", self.skill_level)

            return self.detect_flow(
                challenge=kwargs["challenge"],
                skill=skill,
                attention_absorption=kwargs["attention_absorption"],
                clear_goals=kwargs["clear_goals"],
                immediate_feedback=kwargs.get("immediate_feedback", True)
            )

        elif event_type == "skill_update":
            self.skill_level = kwargs["new_skill_level"]
            return {
                "skill_updated": True,
                "new_skill_level": float(self.skill_level)
            }

        else:
            return {"error": f"Unknown event type: {event_type}"}

    def get_state(self) -> Dict:
        """
        Get current state of flow system

        Returns:
            System state with flow metrics
        """
        return {
            "in_flow": self.in_flow,
            "flow_duration": float(self.flow_duration_minutes),
            "skill_level": float(self.skill_level),
            "flow_threshold": self.flow_threshold,
            "flow_episodes_count": len(self.flow_episodes)
        }
