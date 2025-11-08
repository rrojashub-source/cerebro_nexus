"""
LAB_014: Serotonin System

Mood stability, impulse control, and temporal discounting.

Biological Inspiration:
- Raphe nuclei (serotonergic neurons)
- Serotonergic projections to PFC, amygdala, hippocampus

Core Functions:
- Mood stability (buffer against emotional fluctuations)
- Impulse control (patience vs impulsivity)
- Temporal discounting (future reward valuation)
- Social sensitivity (social reward modulation)

Key Papers:
- Dayan & Huys (2009) - "Serotonin in Affective Control"
- Crockett et al. (2012) - "Serotonin modulates behavioral reactions to unfairness"
"""

from typing import Dict, List
import numpy as np


class SerotoninSystem:
    """
    LAB_014: Serotonin mood stability and impulse control

    Biological inspiration: Raphe nuclei 5-HT neurons

    Parameters:
    -----------
    baseline_level : float
        Baseline serotonin level (default: 0.5, neutral)
    stability_factor : float
        Mood buffering strength (default: 0.7)
    patience_multiplier : float
        Impulse control multiplier (default: 1.5)
    social_sensitivity_gain : float
        Social context amplification (default: 0.3)
    adaptation_rate : float
        Speed of serotonin level changes (default: 0.1)
    history_window : int
        Size of level history buffer (default: 20)
    """

    def __init__(
        self,
        baseline_level: float = 0.5,
        stability_factor: float = 0.7,
        patience_multiplier: float = 1.5,
        social_sensitivity_gain: float = 0.3,
        adaptation_rate: float = 0.1,
        history_window: int = 20
    ):
        # Configuration
        self.baseline_level = baseline_level
        self.stability_factor = stability_factor
        self.patience_multiplier = patience_multiplier
        self.social_sensitivity_gain = social_sensitivity_gain
        self.adaptation_rate = adaptation_rate
        self.history_window = history_window

        # State
        self.current_level: float = baseline_level
        self.level_history: List[float] = []
        self.total_events: int = 0

    def update_level(self, outcome: float, social_context: float) -> float:
        """
        Update serotonin level from outcome and social context

        Parameters:
        -----------
        outcome : float
            Outcome valence (0-1)
        social_context : float
            Social context quality (0-1)
            0 = isolation/conflict, 1 = positive social

        Returns:
        --------
        serotonin_level : float
            Updated serotonin level (0-1)
        """
        # Combined signal: outcome modulated by social context
        # Positive social amplifies positive outcomes
        # Negative social dampens outcomes
        combined_signal = outcome * (0.5 + 0.5 * social_context)

        # Compute target level (what serotonin should move toward)
        target_level = combined_signal

        # Gradual adaptation toward target
        # High adaptation_rate = fast changes
        # Low adaptation_rate = slow, stable changes
        delta = (target_level - self.current_level) * self.adaptation_rate

        self.current_level += delta

        # Clamp to [0, 1]
        self.current_level = max(0.0, min(1.0, self.current_level))

        # Update history
        self.level_history.append(self.current_level)
        if len(self.level_history) > self.history_window:
            self.level_history.pop(0)

        return self.current_level

    def modulate_mood(self, current_mood: float, event_valence: float) -> float:
        """
        Buffer mood changes based on serotonin level

        High serotonin = strong buffering (stable mood)
        Low serotonin = weak buffering (volatile mood)

        Parameters:
        -----------
        current_mood : float
            Current mood state (0-1)
        event_valence : float
            Emotional event valence (-1 to +1)

        Returns:
        --------
        buffered_mood : float
            Mood after serotonin buffering (0-1)
        """
        # Buffering strength = serotonin_level * stability_factor
        # High serotonin → high buffering
        buffering_strength = self.current_level * self.stability_factor

        # Buffered change = raw change * (1 - buffering)
        # High buffering → small mood change
        buffered_change = event_valence * (1.0 - buffering_strength)

        new_mood = current_mood + buffered_change

        # Clamp to [0, 1]
        new_mood = max(0.0, min(1.0, new_mood))

        return new_mood

    def compute_impulse_control(self) -> float:
        """
        Compute impulse control (patience) from serotonin level

        High serotonin = high patience (can resist temptation)
        Low serotonin = low patience (impulsive)

        Returns:
        --------
        patience : float
            Impulse control strength (0-1)
        """
        # Patience = serotonin * multiplier
        # Scaled to 0-1 range
        patience = self.current_level * self.patience_multiplier

        # Clamp to [0, 1]
        patience = min(1.0, patience)

        return patience

    def compute_temporal_discount(self, delay: float) -> float:
        """
        Compute temporal discount rate (future devaluation)

        High serotonin = low discount rate (patient, values future)
        Low serotonin = high discount rate (impulsive, devalues future)

        Parameters:
        -----------
        delay : float
            Delay to reward (time units)

        Returns:
        --------
        discount_rate : float
            Temporal discount rate (0-1)
            0 = no discounting (fully patient)
            1 = maximum discounting (completely impulsive)
        """
        # Base discount inversely proportional to serotonin
        # High serotonin → low base discount
        # Low serotonin → high base discount
        base_discount = 1.0 - self.current_level

        # Normalized hyperbolic discounting
        # Formula: discount = base * (1 - 1/(1 + k*delay))
        # This ensures discount ∈ [0, base_discount]
        # k = 0.4 (discounting steepness - tuned for delay=10 baseline)
        k = 0.4
        discount_rate = base_discount * (1.0 - 1.0/(1.0 + k * delay))

        # Clamp to [0, 1]
        discount_rate = max(0.0, min(1.0, discount_rate))

        return discount_rate

    def compute_social_sensitivity(self) -> float:
        """
        Compute social reward sensitivity

        Serotonin modulates sensitivity to social rewards

        Returns:
        --------
        social_sensitivity : float
            Social sensitivity (0-1)
        """
        # Social sensitivity scales with serotonin
        # Moderate serotonin = optimal social sensitivity
        # Very low/high = reduced social sensitivity

        # Inverted-U curve centered at 0.6
        optimal_level = 0.6
        deviation = abs(self.current_level - optimal_level)

        # Sensitivity = 1 - deviation
        social_sensitivity = 1.0 - (deviation * 1.5)

        # Clamp to [0, 1]
        social_sensitivity = max(0.0, min(1.0, social_sensitivity))

        return social_sensitivity

    def process_event(self, outcome: float, social_context: float) -> Dict:
        """
        Main processing: update serotonin, compute modulations

        Parameters:
        -----------
        outcome : float
            Outcome valence (0-1)
        social_context : float
            Social context quality (0-1)

        Returns:
        --------
        result : Dict
            {
                "serotonin_level": float,
                "impulse_control": float,
                "mood_stability": float,
                "temporal_discount_rate": float,
                "social_sensitivity": float
            }
        """
        # 1. Update serotonin level
        self.update_level(outcome, social_context)

        # 2. Compute impulse control
        impulse_control = self.compute_impulse_control()

        # 3. Compute mood stability (from history variance)
        if len(self.level_history) >= 2:
            mood_variance = np.var(self.level_history)
            mood_stability = 1.0 / (1.0 + mood_variance)
        else:
            mood_stability = 1.0  # Maximally stable if no history

        # 4. Compute temporal discount (using delay=10 as baseline)
        temporal_discount_rate = self.compute_temporal_discount(delay=10.0)

        # 5. Compute social sensitivity
        social_sensitivity = self.compute_social_sensitivity()

        # 6. Update event counter
        self.total_events += 1

        # 7. Return complete result
        return {
            "serotonin_level": float(self.current_level),
            "impulse_control": float(impulse_control),
            "mood_stability": float(mood_stability),
            "temporal_discount_rate": float(temporal_discount_rate),
            "social_sensitivity": float(social_sensitivity)
        }

    def get_state(self) -> Dict:
        """
        Get current serotonin system state

        Returns:
        --------
        state : Dict
            {
                "serotonin_level": float,
                "level_history": List[float],
                "level_mean": float,
                "impulse_control": float,
                "mood_stability_index": float,
                "temporal_discount_baseline": float,
                "social_sensitivity": float,
                "total_events": int
            }
        """
        # Current level
        serotonin_level = self.current_level

        # Level statistics
        level_mean = np.mean(self.level_history) if self.level_history else self.baseline_level

        # Impulse control
        impulse_control = self.compute_impulse_control()

        # Mood stability
        if len(self.level_history) >= 2:
            mood_variance = np.var(self.level_history)
            mood_stability_index = 1.0 / (1.0 + mood_variance)
        else:
            mood_stability_index = 1.0

        # Temporal discount (baseline delay=10)
        temporal_discount_baseline = self.compute_temporal_discount(delay=10.0)

        # Social sensitivity
        social_sensitivity = self.compute_social_sensitivity()

        return {
            "serotonin_level": float(serotonin_level),
            "level_history": self.level_history.copy(),
            "level_mean": float(level_mean),
            "impulse_control": float(impulse_control),
            "mood_stability_index": float(mood_stability_index),
            "temporal_discount_baseline": float(temporal_discount_baseline),
            "social_sensitivity": float(social_sensitivity),
            "total_events": int(self.total_events)
        }
