"""
LAB_037: Curiosity Drive System

Function: Information-seeking, exploration bonus, uncertainty reduction
Neuroscience Basis: LC-NE, ACC, dopamine, epistemic curiosity

Key Papers:
- Kidd & Hayden (2015) - The psychology and neuroscience of curiosity
- Gottlieb et al. (2013) - Information-seeking, curiosity, and attention
- Schmidhuber (1991) - Curiosity-driven learning
- Loewenstein (1994) - The psychology of curiosity: information-gap theory

Curiosity Drive Model:
- Information gap detection (uncertainty + prediction error)
- Inverted-U with uncertainty (moderate = peak curiosity)
- Exploration bonus (intrinsic reward for information-seeking)
- Explore vs exploit balance
- Bidirectional integration with LAB_036 (Intrinsic Motivation)
"""

from typing import Dict, List, Optional
import math


class CuriosityDriveSystem:
    """
    LAB_037: Curiosity Drive System

    Models information-seeking through:
    - Information gap detection (Loewenstein 1994)
    - Curiosity computation (inverted-U with uncertainty)
    - Exploration bonus (intrinsic reward)
    - Explore-exploit balance
    - Habituation (repeated exploration reduces novelty)

    Integration:
    - ← LAB_004 (Novelty Detection) - novelty amplifies curiosity
    - ← LAB_013 (Dopamine) - curiosity as reward signal
    - ↔ LAB_036 (Intrinsic Motivation) - bidirectional feedback
    - → LAB_015 (Norepinephrine) - arousal modulation

    Parameters:
    -----------
    exploration_bonus : float
        Base intrinsic reward for exploration (default: 0.1)
    uncertainty_threshold : float
        Threshold for triggering curiosity (default: 0.5)
    """

    def __init__(
        self,
        exploration_bonus: float = 0.1,
        uncertainty_threshold: float = 0.5
    ):
        # Configuration
        self.exploration_bonus = exploration_bonus
        self.uncertainty_threshold = uncertainty_threshold

        # State
        self.current_curiosity: float = 0.0

        # History
        self.exploration_history: List[Dict] = []
        self.explored_targets: Dict[str, int] = {}  # target_id → visit count

    def detect_information_gap(
        self,
        uncertainty: float,
        knowledge_level: float,
        prediction_error: Optional[float] = None
    ) -> float:
        """
        Detect information gap

        Based on Loewenstein (1994): Curiosity arises from perception
        of a gap in knowledge.

        Parameters:
        -----------
        uncertainty : float
            Uncertainty level (0-1)
        knowledge_level : float
            Current knowledge (0-1, higher = more knowledge)
        prediction_error : float, optional
            Prediction error as gap signal

        Returns:
        --------
        information_gap : float
            Size of information gap (0-1)
        """
        # Information gap = uncertainty + (1 - knowledge)
        # High uncertainty + low knowledge = large gap
        gap = (uncertainty + (1.0 - knowledge_level)) / 2.0

        # Prediction error amplifies gap
        if prediction_error is not None:
            gap = gap * (1.0 + prediction_error * 0.5)

        # Clamp to 0-1
        gap = max(0.0, min(1.0, gap))

        return float(gap)

    def compute_curiosity_level(
        self,
        uncertainty: float,
        novelty: float
    ) -> float:
        """
        Compute curiosity level

        Based on Kidd & Hayden (2015): Curiosity follows inverted-U
        with uncertainty. Moderate uncertainty = peak curiosity.

        Integration with LAB_004: novelty amplifies curiosity.

        Parameters:
        -----------
        uncertainty : float
            Uncertainty level (0-1)
        novelty : float
            Novelty level (0-1, from LAB_004)

        Returns:
        --------
        curiosity : float
            Curiosity level (0-1)
        """
        # Inverted-U with uncertainty
        # Peak at uncertainty = 0.5 (moderate)
        optimal_uncertainty = 0.5
        distance = abs(uncertainty - optimal_uncertainty)

        # Gaussian-like inverted-U
        uncertainty_factor = math.exp(-3.0 * (distance ** 2))

        # Zero uncertainty (certainty) should reduce curiosity
        # Add linear decay from zero
        if uncertainty < 0.3:
            uncertainty_factor *= (uncertainty / 0.3)  # Scale down for low uncertainty

        # Novelty amplifies curiosity (LAB_004 integration)
        # Zero novelty should drastically reduce curiosity (familiar = boring)
        # Non-linear scaling: novelty^1.5 for stronger effect at low end
        novelty_factor = novelty ** 1.2  # Power function: 0 novelty = 0 factor

        # Combined curiosity
        curiosity = uncertainty_factor * novelty_factor

        # Clamp to 0-1
        curiosity = max(0.0, min(1.0, curiosity))

        # Update state
        self.current_curiosity = curiosity

        return float(curiosity)

    def compute_exploration_bonus(
        self,
        action_novelty: float,
        information_gain: Optional[float] = None
    ) -> float:
        """
        Compute exploration bonus (intrinsic reward)

        Based on Schmidhuber (1991): Exploration of novel states
        provides intrinsic reward.

        Integration with LAB_013: Curiosity-driven reward signal.

        Parameters:
        -----------
        action_novelty : float
            Novelty of exploratory action (0-1)
        information_gain : float, optional
            Information gain from exploration (0-1)

        Returns:
        --------
        bonus : float
            Intrinsic reward for exploration
        """
        # Base bonus proportional to novelty
        bonus = self.exploration_bonus * action_novelty

        # Information gain amplifies bonus
        if information_gain is not None:
            bonus *= (1.0 + information_gain)

        # Clamp
        bonus = max(0.0, min(1.0, bonus))

        return float(bonus)

    def balance_explore_exploit(
        self,
        curiosity_level: float,
        task_value: float
    ) -> Dict:
        """
        Balance exploration vs exploitation

        High curiosity → explore
        High task value → exploit

        Parameters:
        -----------
        curiosity_level : float
            Current curiosity (0-1)
        task_value : float
            Value of exploitation task (0-1)

        Returns:
        --------
        result : Dict
            Decision and probabilities
        """
        # Softmax-like competition
        # explore_weight = curiosity
        # exploit_weight = task_value

        total = curiosity_level + task_value + 1e-9  # Avoid division by zero

        explore_prob = curiosity_level / total
        exploit_prob = task_value / total

        # Decision: choose action with higher probability
        if explore_prob > exploit_prob:
            action = "explore"
        else:
            action = "exploit"

        return {
            "action": action,
            "explore_probability": float(explore_prob),
            "exploit_probability": float(exploit_prob)
        }

    def process_event(
        self,
        event_type: str,
        **kwargs
    ) -> Dict:
        """
        Main processing: handle curiosity-driven events

        Event types:
        - exploration: Curiosity computation + exploration bonus
        - decision: Explore vs exploit decision

        Parameters:
        -----------
        event_type : str
            Type of event
        **kwargs : Dict
            Event-specific parameters

        Returns:
        --------
        result : Dict
            Event processing result
        """
        if event_type == "exploration":
            # Extract parameters
            uncertainty = kwargs.get("uncertainty", 0.5)
            novelty = kwargs.get("novelty", 0.5)
            information_gain = kwargs.get("information_gain", 0.0)
            intrinsic_motivation_level = kwargs.get("intrinsic_motivation_level", 0.5)
            target_id = kwargs.get("target_id", None)

            # Compute curiosity
            curiosity = self.compute_curiosity_level(uncertainty, novelty)

            # Bidirectional with LAB_036: Intrinsic motivation modulates curiosity
            if intrinsic_motivation_level > 0.5:
                # High intrinsic motivation amplifies curiosity
                modulation = 1.0 + (intrinsic_motivation_level - 0.5) * 0.5
                curiosity *= modulation
                curiosity = min(1.0, curiosity)

            # Habituation: Repeated exploration reduces effective novelty
            effective_novelty = novelty
            if target_id is not None:
                visit_count = self.explored_targets.get(target_id, 0)
                # Habituation factor: decays with visits
                habituation = math.exp(-0.3 * visit_count)
                effective_novelty = novelty * habituation

                # Update visit count
                self.explored_targets[target_id] = visit_count + 1

            # Compute exploration bonus
            bonus = self.compute_exploration_bonus(effective_novelty, information_gain)

            # Intrinsic reward (for LAB_013 dopamine integration)
            intrinsic_reward = curiosity * 0.5 + bonus * 0.5

            # Store in history
            self.exploration_history.append({
                "curiosity": curiosity,
                "bonus": bonus,
                "novelty": novelty,
                "effective_novelty": effective_novelty
            })

            return {
                "curiosity": float(curiosity),
                "exploration_bonus": float(bonus),
                "intrinsic_reward": float(intrinsic_reward),
                "effective_novelty": float(effective_novelty)
            }

        elif event_type == "decision":
            # Explore vs exploit decision
            curiosity_level = kwargs.get("curiosity_level", self.current_curiosity)
            task_value = kwargs.get("task_value", 0.5)

            result = self.balance_explore_exploit(curiosity_level, task_value)

            return result

        else:
            return {"error": f"Unknown event type: {event_type}"}

    def get_state(self) -> Dict:
        """Get current curiosity drive state"""
        return {
            "current_curiosity": float(self.current_curiosity),
            "exploration_bonus": float(self.exploration_bonus),
            "uncertainty_threshold": float(self.uncertainty_threshold),
            "total_explorations": len(self.exploration_history)
        }
