"""
LAB_014: Serotonin System

Mood stability, impulse control, and patience modulation.

Biological Inspiration:
- Raphe nuclei
- Serotonergic projections

Core Function: Regulate mood baseline and impulse control

Key Papers:
- Dayan & Huys (2009) - "Serotonin in the orbitofrontal cortex and the neural basis of economic value"
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
    baseline_mood : float
        Initial mood level (default: 0.5, neutral)
    impulse_threshold : float
        Threshold for impulse control (default: 0.7)
    patience_factor : float
        Base patience for temporal discounting (default: 1.0)
    reactivity_dampening : float
        How much serotonin dampens emotional reactivity (default: 0.5)
    mood_inertia : float
        Resistance to mood changes (default: 0.95, high inertia)
    history_window : int
        Size of mood history buffer (default: 20)
    """

    def __init__(
        self,
        baseline_mood: float = 0.5,
        impulse_threshold: float = 0.7,
        patience_factor: float = 1.0,
        reactivity_dampening: float = 0.5,
        mood_inertia: float = 0.95,
        history_window: int = 20
    ):
        # Configuration
        self.baseline_mood = baseline_mood
        self.impulse_threshold = impulse_threshold
        self.patience_factor = patience_factor
        self.reactivity_dampening = reactivity_dampening
        self.mood_inertia = mood_inertia
        self.history_window = history_window

        # State
        self.mood_level: float = baseline_mood  # Current mood (valence baseline)
        self.mood_history: List[float] = []
        self.impulse_control: float = 1.0  # Max control initially
        self.total_events: int = 0

    def update_mood(self, emotional_event: float) -> float:
        """
        Update mood level from emotional event

        Mood is more stable than emotions (high inertia).
        Serotonin provides mood baseline stability.

        Parameters:
        -----------
        emotional_event : float
            Emotional valence of event (-1 to +1)

        Returns:
        --------
        mood_level : float
            Updated mood level (0-1)
        """
        # Incremental update with high inertia
        # Mood changes slowly (serotonin stability)
        mood_change = emotional_event * (1.0 - self.mood_inertia)
        self.mood_level = self.mood_level + mood_change

        # Clamp to [0, 1]
        self.mood_level = max(0.0, min(1.0, self.mood_level))

        # Add to history
        self.mood_history.append(self.mood_level)
        if len(self.mood_history) > self.history_window:
            self.mood_history.pop(0)

        return self.mood_level

    def compute_impulse_control(self, temptation_strength: float) -> Dict:
        """
        Compute impulse control strength

        Higher serotonin = stronger impulse control = can resist temptation

        Parameters:
        -----------
        temptation_strength : float
            Strength of temptation/impulse (0-1)

        Returns:
        --------
        result : Dict
            {
                "control_strength": float,
                "can_resist": bool,
                "resistance_margin": float
            }
        """
        # Control strength = mood_level * threshold
        # High serotonin (high mood) = high control
        control_strength = self.mood_level * self.impulse_threshold

        # Can resist if control > temptation
        can_resist = control_strength > temptation_strength
        resistance_margin = control_strength - temptation_strength

        return {
            "control_strength": control_strength,
            "can_resist": can_resist,
            "resistance_margin": resistance_margin
        }

    def get_patience_factor(self) -> float:
        """
        Get patience factor for temporal discounting

        High serotonin = more patience = lower temporal discounting
        (can wait longer for rewards)

        Returns:
        --------
        patience : float
            Patience multiplier (0-2.0)
            < 1.0 = impatient (high discounting)
            = 1.0 = normal discounting
            > 1.0 = patient (low discounting)
        """
        # Patience scales with mood level
        # High mood = high serotonin = more patience
        patience = self.mood_level * self.patience_factor * 2.0

        return patience

    def modulate_reactivity(self, emotional_intensity: float) -> float:
        """
        Modulate emotional reactivity

        High serotonin = dampened emotional reactivity
        (less reactive to emotional events)

        Parameters:
        -----------
        emotional_intensity : float
            Intensity of emotional stimulus (0-1)

        Returns:
        --------
        dampened_reactivity : float
            Modulated emotional reactivity (0-1)
        """
        # Serotonin dampens emotional reactivity
        # High serotonin = lower reactivity
        dampening = self.mood_level * self.reactivity_dampening

        dampened_reactivity = emotional_intensity * (1.0 - dampening)

        return dampened_reactivity

    def get_mood_stability(self) -> float:
        """
        Compute mood stability (inverse of mood variance)

        Returns:
        --------
        stability : float
            Mood stability score (0-1)
            Higher = more stable mood
        """
        if len(self.mood_history) < 2:
            return 1.0  # Maximally stable if no history

        # Compute variance of mood history
        mood_variance = np.var(self.mood_history)

        # Stability = inverse of variance (normalized)
        stability = 1.0 / (1.0 + mood_variance)

        return stability

    def process_event(
        self,
        emotional_event: float,
        temptation_strength: float = 0.0
    ) -> Dict:
        """
        Main processing: update mood, compute impulse control, return state

        Parameters:
        -----------
        emotional_event : float
            Emotional valence of event (-1 to +1)
        temptation_strength : float
            Strength of temptation/impulse (0-1, default: 0.0)

        Returns:
        --------
        result : Dict
            {
                "mood_level": float,
                "impulse_control": Dict,
                "patience_factor": float,
                "emotional_reactivity": float,
                "mood_stability": float
            }
        """
        # 1. Update mood from emotional event
        self.update_mood(emotional_event)

        # 2. Compute impulse control
        impulse_control = self.compute_impulse_control(temptation_strength)

        # 3. Get patience factor
        patience = self.get_patience_factor()

        # 4. Modulate reactivity
        reactivity = self.modulate_reactivity(abs(emotional_event))

        # 5. Get mood stability
        stability = self.get_mood_stability()

        # 6. Update event counter
        self.total_events += 1

        # 7. Return complete result
        return {
            "mood_level": self.mood_level,
            "impulse_control": impulse_control,
            "patience_factor": patience,
            "emotional_reactivity": reactivity,
            "mood_stability": stability
        }

    def get_state(self) -> Dict:
        """
        Get current serotonin system state

        Returns:
        --------
        state : Dict
            {
                "mood_level": float,
                "mood_history": List[float],
                "mood_mean": float,
                "mood_stability": float,
                "impulse_control_strength": float,
                "patience_factor": float,
                "total_events": int
            }
        """
        # Current mood
        mood_current = self.mood_level

        # Mood statistics
        mood_mean = np.mean(self.mood_history) if self.mood_history else self.baseline_mood
        mood_stability = self.get_mood_stability()

        # Control strength (current)
        control_strength = self.mood_level * self.impulse_threshold

        # Patience
        patience = self.get_patience_factor()

        return {
            "mood_level": float(mood_current),
            "mood_history": self.mood_history.copy(),
            "mood_mean": float(mood_mean),
            "mood_stability": float(mood_stability),
            "impulse_control_strength": float(control_strength),
            "patience_factor": float(patience),
            "total_events": int(self.total_events)
        }
