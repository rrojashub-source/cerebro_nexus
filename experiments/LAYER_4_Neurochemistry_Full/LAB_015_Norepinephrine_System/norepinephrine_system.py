"""
LAB_015: Norepinephrine System

Arousal, stress response, and focus modulation.

Biological Inspiration:
- Locus coeruleus (LC)
- Noradrenergic projections

Core Function: Arousal regulation & performance optimization

Key Papers:
- Aston-Jones & Cohen (2005) - "An integrative theory of locus coeruleus-norepinephrine function: adaptive gain and optimal performance"
- Yerkes & Dodson (1908) - "The relation of strength of stimulus to rapidity of habit-formation"
"""

from typing import Dict, List
import numpy as np


class NorepinephrineSystem:
    """
    LAB_015: Norepinephrine arousal and focus modulation

    Biological inspiration: Locus coeruleus noradrenergic neurons

    Parameters:
    -----------
    baseline_arousal : float
        Initial arousal level (default: 0.5, medium)
    stress_sensitivity : float
        How much stress events affect arousal (default: 0.3)
    arousal_decay : float
        Decay rate toward baseline (default: 0.95)
    optimal_arousal : float
        Peak performance arousal level (default: 0.6)
    focus_threshold : float
        Arousal threshold for high focus (default: 0.5)
    history_window : int
        Size of arousal history buffer (default: 20)
    """

    def __init__(
        self,
        baseline_arousal: float = 0.5,
        stress_sensitivity: float = 0.3,
        arousal_decay: float = 0.95,
        optimal_arousal: float = 0.6,
        focus_threshold: float = 0.5,
        history_window: int = 20
    ):
        # Configuration
        self.baseline_arousal = baseline_arousal
        self.stress_sensitivity = stress_sensitivity
        self.arousal_decay = arousal_decay
        self.optimal_arousal = optimal_arousal
        self.focus_threshold = focus_threshold
        self.history_window = history_window

        # State
        self.arousal_level: float = baseline_arousal
        self.arousal_history: List[float] = []
        self.total_events: int = 0

    def update_arousal(self, stress_event: float) -> float:
        """
        Update arousal level from stress event

        Arousal spikes quickly on stress, decays slowly toward baseline.
        Norepinephrine provides rapid response to salient/stressful stimuli.

        Parameters:
        -----------
        stress_event : float
            Stress intensity of event (-1 to +1)
            Positive = stress/arousal increase
            Negative = calming/arousal decrease

        Returns:
        --------
        arousal_level : float
            Updated arousal level (0-1)
        """
        # Decay toward baseline (homeostatic regulation)
        decay_delta = (self.baseline_arousal - self.arousal_level) * (1.0 - self.arousal_decay)
        self.arousal_level = self.arousal_level + decay_delta

        # Rapid arousal spike from stress event
        arousal_spike = stress_event * self.stress_sensitivity
        self.arousal_level = self.arousal_level + arousal_spike

        # Clamp to [0, 1]
        self.arousal_level = max(0.0, min(1.0, self.arousal_level))

        # Add to history
        self.arousal_history.append(self.arousal_level)
        if len(self.arousal_history) > self.history_window:
            self.arousal_history.pop(0)

        return self.arousal_level

    def compute_performance(self) -> Dict:
        """
        Compute performance efficiency based on arousal (Yerkes-Dodson Law)

        Inverted-U relationship:
        - Low arousal = poor performance (under-stimulated, distracted)
        - Optimal arousal = best performance (focused, efficient)
        - High arousal = poor performance (over-stimulated, anxious)

        Returns:
        --------
        result : Dict
            {
                "performance_efficiency": float (0-1),
                "is_optimal": bool,
                "deviation_from_optimal": float
            }
        """
        # Inverted-U curve: performance peaks at optimal_arousal
        # Use Gaussian-like function
        deviation = abs(self.arousal_level - self.optimal_arousal)

        # Performance peaks at optimal, drops with deviation
        # Max performance = 1.0 at optimal_arousal
        # Performance drops off sharply as arousal deviates
        performance_efficiency = np.exp(-6.0 * (deviation ** 2))

        # Check if within optimal zone (±0.1 of optimal)
        is_optimal = deviation < 0.1

        return {
            "performance_efficiency": float(performance_efficiency),
            "is_optimal": bool(is_optimal),
            "deviation_from_optimal": float(deviation)
        }

    def modulate_focus(self) -> float:
        """
        Modulate attentional focus based on arousal

        Low arousal = low focus (distracted, drowsy)
        Medium arousal = high focus (alert, concentrated)
        High arousal = scattered focus (anxious, overwhelmed)

        Returns:
        --------
        focus_strength : float
            Focus strength (0-1)
        """
        # Focus is highest at medium arousal, lower at extremes
        # Similar to performance curve but less sensitive
        deviation_from_medium = abs(self.arousal_level - 0.5)

        # Focus peaks at medium arousal (0.5), drops at extremes
        focus_strength = 1.0 - (2.0 * deviation_from_medium)
        focus_strength = max(0.0, focus_strength)

        return float(focus_strength)

    def get_alertness(self) -> float:
        """
        Get alertness level (directly proportional to arousal)

        High arousal = high alertness
        Low arousal = low alertness (drowsy)

        Returns:
        --------
        alertness : float
            Alertness level (0-1)
        """
        # Alertness is simply the arousal level
        # (norepinephrine directly increases wakefulness)
        return self.arousal_level

    def get_arousal_stability(self) -> float:
        """
        Compute arousal stability (inverse of arousal variance)

        Returns:
        --------
        stability : float
            Arousal stability score (0-1)
            Higher = more stable arousal
        """
        if len(self.arousal_history) < 2:
            return 1.0  # Maximally stable if no history

        # Compute variance of arousal history
        arousal_variance = np.var(self.arousal_history)

        # Stability = inverse of variance (normalized)
        stability = 1.0 / (1.0 + arousal_variance)

        return float(stability)

    def process_event(
        self,
        stress_event: float
    ) -> Dict:
        """
        Main processing: update arousal, compute performance, focus, alertness

        Parameters:
        -----------
        stress_event : float
            Stress intensity of event (-1 to +1)

        Returns:
        --------
        result : Dict
            {
                "arousal_level": float,
                "performance": Dict,
                "focus_strength": float,
                "alertness": float,
                "arousal_stability": float
            }
        """
        # 1. Update arousal from stress event
        self.update_arousal(stress_event)

        # 2. Compute performance (Yerkes-Dodson)
        performance = self.compute_performance()

        # 3. Modulate focus
        focus = self.modulate_focus()

        # 4. Get alertness
        alertness = self.get_alertness()

        # 5. Get arousal stability
        stability = self.get_arousal_stability()

        # 6. Update event counter
        self.total_events += 1

        # 7. Return complete result
        return {
            "arousal_level": float(self.arousal_level),
            "performance": performance,
            "focus_strength": float(focus),
            "alertness": float(alertness),
            "arousal_stability": float(stability)
        }

    def get_state(self) -> Dict:
        """
        Get current norepinephrine system state

        Returns:
        --------
        state : Dict
            {
                "arousal_level": float,
                "arousal_history": List[float],
                "arousal_mean": float,
                "arousal_stability": float,
                "performance_efficiency": float,
                "focus_strength": float,
                "alertness": float,
                "total_events": int
            }
        """
        # Current arousal
        arousal_current = self.arousal_level

        # Arousal statistics
        arousal_mean = np.mean(self.arousal_history) if self.arousal_history else self.baseline_arousal
        arousal_stability = self.get_arousal_stability()

        # Performance
        performance = self.compute_performance()

        # Focus & alertness
        focus = self.modulate_focus()
        alertness = self.get_alertness()

        return {
            "arousal_level": float(arousal_current),
            "arousal_history": self.arousal_history.copy(),
            "arousal_mean": float(arousal_mean),
            "arousal_stability": float(arousal_stability),
            "performance_efficiency": float(performance["performance_efficiency"]),
            "focus_strength": float(focus),
            "alertness": float(alertness),
            "total_events": int(self.total_events)
        }
