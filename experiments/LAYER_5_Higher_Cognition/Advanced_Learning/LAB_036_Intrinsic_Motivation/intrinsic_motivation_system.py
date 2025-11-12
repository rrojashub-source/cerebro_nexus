"""
LAB_036: Intrinsic Motivation System

Function: Curiosity, mastery, autonomy drives (non-reward-based)
Neuroscience Basis: Self-Determination Theory, epistemic curiosity, competence

Key Papers:
- Ryan & Deci (2000) - Self-determination theory
- Oudeyer et al. (2007) - Intrinsic motivation in robots
- White (1959) - Motivation reconsidered: The concept of competence
- Berlyne (1960) - Curiosity and exploration

Intrinsic Motivation Model:
- Curiosity drive: Inverted-U with novelty (moderate = peak)
- Competence/Mastery: Flow theory (skill ≈ challenge)
- Autonomy: Self-directed > externally controlled
- Total reward: Weighted sum of 3 components
- Undermining effect: External rewards reduce intrinsic motivation
"""

from typing import Dict, Optional
import math


class IntrinsicMotivationSystem:
    """
    LAB_036: Intrinsic Motivation System

    Models non-reward-based motivation through:
    - Epistemic curiosity (Berlyne 1960): Information-seeking
    - Competence motivation (White 1959): Mastery drive
    - Autonomy preference (Deci & Ryan): Self-directed action
    - Intrinsic vs extrinsic separation (undermining effect)

    Integration:
    - LAB_004 (Novelty Detection) → drives curiosity
    - LAB_037 (Curiosity Drive) ↔ bidirectional feedback
    - LAB_013 (Dopamine) → intrinsic reward signal

    Parameters:
    -----------
    curiosity_weight : float
        Weight for curiosity component (default: 0.4)
    mastery_weight : float
        Weight for competence/mastery component (default: 0.4)
    autonomy_weight : float
        Weight for autonomy component (default: 0.2)
    """

    def __init__(
        self,
        curiosity_weight: float = 0.4,
        mastery_weight: float = 0.4,
        autonomy_weight: float = 0.2
    ):
        # Weights
        self.curiosity_weight = curiosity_weight
        self.mastery_weight = mastery_weight
        self.autonomy_weight = autonomy_weight

        # State
        self.current_curiosity: float = 0.0
        self.current_competence: float = 0.0
        self.current_autonomy: float = 0.0

        # History
        self.intrinsic_reward_history = []

    def compute_curiosity_drive(
        self,
        novelty_level: float,
        information_gap: float
    ) -> float:
        """
        Compute epistemic curiosity drive

        Based on Berlyne (1960): Curiosity follows inverted-U curve
        with novelty. Moderate novelty = peak curiosity.

        Integration with LAB_004 (Novelty Detection): novelty_level
        comes from novelty detection system.

        Parameters:
        -----------
        novelty_level : float
            Novelty of stimulus (0-1, from LAB_004)
        information_gap : float
            Uncertainty/information gap (0-1)

        Returns:
        --------
        curiosity : float
            Curiosity drive level (0-1)
        """
        # Inverted-U curve with novelty
        # Peak at novelty = 0.5 (moderate)
        optimal_novelty = 0.5
        novelty_distance = abs(novelty_level - optimal_novelty)

        # Gaussian-like curve (inverted-U)
        # Using negative quadratic for inverted-U shape
        novelty_factor = 1.0 - (novelty_distance / 0.5) ** 2

        # Information gap amplifies curiosity
        gap_factor = 0.5 + (information_gap * 0.5)  # 0.5 to 1.0

        # Combined curiosity
        curiosity = novelty_factor * gap_factor

        # Clamp to 0-1
        curiosity = max(0.0, min(1.0, curiosity))

        # Update state
        self.current_curiosity = curiosity

        return float(curiosity)

    def compute_competence_motivation(
        self,
        skill_level: float,
        challenge_level: float
    ) -> float:
        """
        Compute competence/mastery motivation

        Based on White (1959) competence motivation + flow theory
        (Csikszentmihalyi): Optimal when skill ≈ challenge.

        Motivation follows inverted-U:
        - Challenge << skill → boredom (low motivation)
        - Challenge ≈ skill → flow (peak motivation)
        - Challenge >> skill → anxiety (low motivation)

        Parameters:
        -----------
        skill_level : float
            Current skill level (0-1)
        challenge_level : float
            Task challenge level (0-1)

        Returns:
        --------
        competence : float
            Competence motivation level (0-1)
        """
        # Distance from optimal (skill = challenge)
        mismatch = abs(skill_level - challenge_level)

        # Inverted-U: peak when mismatch = 0
        # Using Gaussian-like decay
        competence = math.exp(-3.0 * (mismatch ** 2))

        # Clamp to 0-1
        competence = max(0.0, min(1.0, competence))

        # Update state
        self.current_competence = competence

        return float(competence)

    def compute_autonomy_preference(
        self,
        action_source: str
    ) -> float:
        """
        Compute autonomy preference

        Based on Deci & Ryan (2000): Self-directed actions have
        higher intrinsic value than externally controlled actions.

        Parameters:
        -----------
        action_source : str
            "self" (self-directed) or "external" (externally controlled)

        Returns:
        --------
        autonomy : float
            Autonomy motivation level (0-1)
        """
        if action_source == "self":
            # High autonomy for self-directed
            autonomy = 0.9
        else:
            # Low autonomy for external control
            autonomy = 0.4

        # Update state
        self.current_autonomy = autonomy

        return float(autonomy)

    def compute_intrinsic_reward(self) -> float:
        """
        Compute total intrinsic motivation reward

        Weighted sum of three components:
        - Curiosity drive
        - Competence motivation
        - Autonomy preference

        Returns:
        --------
        intrinsic_reward : float
            Total intrinsic motivation (0-1)
        """
        reward = (
            self.current_curiosity * self.curiosity_weight +
            self.current_competence * self.mastery_weight +
            self.current_autonomy * self.autonomy_weight
        )

        # Clamp to 0-1
        reward = max(0.0, min(1.0, reward))

        return float(reward)

    def process_event(
        self,
        event_type: str,
        **kwargs
    ) -> Dict:
        """
        Main processing: compute intrinsic motivation for event

        Event types:
        - task_engagement: Complete motivation computation

        Parameters:
        -----------
        event_type : str
            Type of event
        **kwargs : Dict
            Event-specific parameters:
            - novelty: Novelty level (0-1, from LAB_004)
            - information_gap: Uncertainty (0-1)
            - skill_level: Current skill (0-1)
            - challenge_level: Task challenge (0-1)
            - action_source: "self" or "external"
            - external_reward: Optional external reward (undermining effect)

        Returns:
        --------
        result : Dict
            Intrinsic motivation breakdown
        """
        if event_type == "task_engagement":
            # Extract parameters
            novelty = kwargs.get("novelty", 0.5)
            information_gap = kwargs.get("information_gap", 0.5)
            skill_level = kwargs.get("skill_level", 0.5)
            challenge_level = kwargs.get("challenge_level", 0.5)
            action_source = kwargs.get("action_source", "self")
            external_reward = kwargs.get("external_reward", 0.0)

            # Compute components
            curiosity = self.compute_curiosity_drive(novelty, information_gap)
            competence = self.compute_competence_motivation(skill_level, challenge_level)
            autonomy = self.compute_autonomy_preference(action_source)

            # Compute total intrinsic reward
            intrinsic_reward = self.compute_intrinsic_reward()

            # Undermining effect: External rewards reduce intrinsic motivation
            if external_reward > 0:
                # Deci (1971): External rewards undermine intrinsic motivation
                undermining_factor = 1.0 - (external_reward * 0.3)  # Up to 30% reduction
                intrinsic_reward *= undermining_factor

            # Store in history
            self.intrinsic_reward_history.append(intrinsic_reward)

            return {
                "curiosity": float(curiosity),
                "competence": float(competence),
                "autonomy": float(autonomy),
                "intrinsic_reward": float(intrinsic_reward),
                "external_reward_present": external_reward > 0
            }

        else:
            return {"error": f"Unknown event type: {event_type}"}

    def get_state(self) -> Dict:
        """Get current intrinsic motivation state"""
        intrinsic_reward = self.compute_intrinsic_reward()

        return {
            "current_curiosity": float(self.current_curiosity),
            "current_competence": float(self.current_competence),
            "current_autonomy": float(self.current_autonomy),
            "intrinsic_reward": float(intrinsic_reward),
            "curiosity_weight": float(self.curiosity_weight),
            "mastery_weight": float(self.mastery_weight),
            "autonomy_weight": float(self.autonomy_weight)
        }
