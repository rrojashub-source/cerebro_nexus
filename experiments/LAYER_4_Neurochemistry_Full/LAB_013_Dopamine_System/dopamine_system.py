"""
LAB_013: Dopamine System

Reward prediction error and learning rate modulation.

Biological Inspiration:
- VTA (Ventral Tegmental Area)
- Substantia Nigra
- Striatum

Core Algorithm: RPE = Actual_Reward - Expected_Reward

Key Papers:
- Schultz et al. (1997) - "A neural substrate of prediction and reward"
- Berridge & Robinson (2003) - "Parsing reward" (Wanting vs Liking)
"""

from typing import Dict, List, Optional
import numpy as np


class DopamineSystem:
    """
    LAB_013: Dopamine reward prediction error and learning rate modulation

    Biological inspiration: VTA/SNc dopaminergic neurons

    Parameters:
    -----------
    baseline_lr : float
        Base learning rate (default: 0.1)
    rpe_sensitivity : float
        How much RPE affects learning rate (default: 0.5)
    motivation_decay : float
        Decay factor for motivation over time (default: 0.95)
    history_window : int
        Size of RPE history buffer (default: 10)
    """

    def __init__(
        self,
        baseline_lr: float = 0.1,
        rpe_sensitivity: float = 0.5,
        motivation_decay: float = 0.95,
        history_window: int = 10
    ):
        # Configuration
        self.baseline_lr = baseline_lr
        self.rpe_sensitivity = rpe_sensitivity
        self.motivation_decay = motivation_decay
        self.history_window = history_window

        # State
        self.rpe_history: List[float] = []
        self.motivation_level: float = 0.5  # Neutral start
        self.total_rpe_events: int = 0

    def compute_rpe(self, expected: float, actual: float) -> float:
        """
        Compute reward prediction error

        Parameters:
        -----------
        expected : float
            Expected reward (0-1)
        actual : float
            Actual reward received (0-1)

        Returns:
        --------
        rpe : float
            Reward prediction error (-1 to +1)
        """
        # Schultz (1997) algorithm: RPE = Actual - Expected
        rpe = actual - expected
        return rpe

    def modulate_learning_rate(self, base_lr: float, rpe: float) -> float:
        """
        Adjust learning rate based on RPE

        Positive RPE (better than expected) → Increase learning rate
        Negative RPE (worse than expected) → Decrease learning rate

        Parameters:
        -----------
        base_lr : float
            Base learning rate
        rpe : float
            Reward prediction error

        Returns:
        --------
        modulated_lr : float
            Modulated learning rate (clamped to 0.01-1.0)
        """
        # Modulate learning rate based on RPE
        # Formula: modulated_lr = base_lr * (1.0 + rpe * sensitivity)
        modulated_lr = base_lr * (1.0 + rpe * self.rpe_sensitivity)

        # Clamp to safe range [0.01, 1.0]
        modulated_lr = max(0.01, min(1.0, modulated_lr))

        return modulated_lr

    def update_motivation(self, rpe: float) -> float:
        """
        Update motivation level from RPE

        Motivation = moving average of positive RPEs (optimism bias)

        Parameters:
        -----------
        rpe : float
            Reward prediction error

        Returns:
        --------
        motivation_level : float
            Updated motivation level (0-1)
        """
        # Exponential moving average with decay
        # Higher positive RPEs increase motivation
        # Negative RPEs and time naturally decay motivation

        # Apply decay to current motivation (time-based forgetting)
        self.motivation_level *= self.motivation_decay

        # Incorporate new RPE (positive RPEs boost motivation)
        # Optimism bias: weight positive RPEs more than negative
        if rpe > 0:
            # Positive surprise: boost motivation significantly
            self.motivation_level += (1.0 - self.motivation_level) * rpe * 0.3
        else:
            # Negative surprise: reduce motivation mildly
            self.motivation_level += self.motivation_level * rpe * 0.1

        # Clamp to [0, 1] range
        self.motivation_level = max(0.0, min(1.0, self.motivation_level))

        return self.motivation_level

    def get_exploration_bonus(self, uncertainty: float = 0.5) -> float:
        """
        Compute exploration bonus (higher motivation = more explore)

        Parameters:
        -----------
        uncertainty : float
            Current uncertainty level (0-1)

        Returns:
        --------
        exploration_bonus : float
            Exploration tendency (0-1)
        """
        # Exploration bonus = motivation * uncertainty
        # High motivation + high uncertainty → strong exploration drive
        # Low motivation or low uncertainty → prefer exploitation

        exploration_bonus = self.motivation_level * uncertainty

        # Apply non-linear scaling (sigmoid-like) to make it more pronounced
        # This creates a clearer explore/exploit threshold
        exploration_bonus = exploration_bonus ** 0.8  # Slight non-linearity

        return exploration_bonus

    def process_event(self, expected: float, actual: float) -> Dict:
        """
        Main processing: compute RPE, update state, return modulations

        Parameters:
        -----------
        expected : float
            Expected reward (0-1)
        actual : float
            Actual reward (0-1)

        Returns:
        --------
        result : Dict
            {
                "rpe": float,
                "modulated_lr": float,
                "motivation_level": float,
                "exploration_bonus": float
            }
        """
        # 1. Compute RPE
        rpe = self.compute_rpe(expected, actual)

        # 2. Update RPE history (maintain window size)
        self.rpe_history.append(rpe)
        if len(self.rpe_history) > self.history_window:
            self.rpe_history.pop(0)  # Remove oldest

        # 3. Update motivation based on RPE
        self.update_motivation(rpe)

        # 4. Modulate learning rate
        modulated_lr = self.modulate_learning_rate(self.baseline_lr, rpe)

        # 5. Compute exploration bonus
        # Use default uncertainty for now (could be passed as parameter)
        exploration_bonus = self.get_exploration_bonus(uncertainty=0.5)

        # 6. Update event counter
        self.total_rpe_events += 1

        # 7. Return complete result
        return {
            "rpe": rpe,
            "modulated_lr": modulated_lr,
            "motivation_level": self.motivation_level,
            "exploration_bonus": exploration_bonus
        }

    def get_state(self) -> Dict:
        """
        Get current dopamine system state

        Returns:
        --------
        state : Dict
            {
                "rpe_current": float,
                "rpe_history": List[float],
                "rpe_mean": float,
                "motivation_level": float,
                "learning_rate_multiplier": float,
                "exploration_bonus": float,
                "total_events": int
            }
        """
        # Get current RPE (most recent)
        rpe_current = self.rpe_history[-1] if self.rpe_history else 0.0

        # Compute RPE mean
        rpe_mean = np.mean(self.rpe_history) if self.rpe_history else 0.0

        # Compute learning rate multiplier (relative to baseline)
        learning_rate_multiplier = self.modulate_learning_rate(
            self.baseline_lr, rpe_current
        ) / self.baseline_lr if self.baseline_lr > 0 else 1.0

        # Get exploration bonus
        exploration_bonus = self.get_exploration_bonus()

        return {
            "rpe_current": float(rpe_current),
            "rpe_history": self.rpe_history.copy(),
            "rpe_mean": float(rpe_mean),
            "motivation_level": float(self.motivation_level),
            "learning_rate_multiplier": float(learning_rate_multiplier),
            "exploration_bonus": float(exploration_bonus),
            "total_events": int(self.total_rpe_events)
        }
