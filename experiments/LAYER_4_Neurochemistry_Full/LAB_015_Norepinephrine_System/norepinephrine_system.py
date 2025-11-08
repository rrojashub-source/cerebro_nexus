"""
LAB_015: Norepinephrine System

Arousal, stress response, focus width, and exploit-explore balance.

Biological Inspiration:
- Locus coeruleus (LC) noradrenergic neurons
- Noradrenergic projections to cortex, amygdala, hippocampus

Core Functions:
- Arousal modulation (inverted-U performance curve)
- Stress response (fight-or-flight activation)
- Focus width (narrow vs broad attention)
- Exploit vs explore (optimal arousal → exploit, extremes → explore)

Key Papers:
- Aston-Jones & Cohen (2005) - "An integrative theory of locus coeruleus-norepinephrine function"
- Yerkes & Dodson (1908) - "The relation of strength of stimulus to rapidity of habit-formation"
"""

from typing import Dict, List, Tuple
import numpy as np


class NorepinephrineSystem:
    """
    LAB_015: Norepinephrine arousal and performance modulation

    Biological inspiration: Locus coeruleus NE neurons

    Parameters:
    -----------
    baseline_arousal : float
        Baseline arousal level (default: 0.5, medium)
    optimal_range : Tuple[float, float]
        Optimal arousal range for peak performance (default: (0.5, 0.7))
    stress_sensitivity : float
        Stress response amplification (default: 0.8)
    decay_rate : float
        Arousal decay toward baseline (default: 0.92)
    novelty_boost : float
        Novelty-induced arousal boost (default: 0.3)
    history_window : int
        Size of arousal history buffer (default: 10)
    """

    def __init__(
        self,
        baseline_arousal: float = 0.5,
        optimal_range: Tuple[float, float] = (0.5, 0.7),
        stress_sensitivity: float = 0.8,
        decay_rate: float = 0.92,
        novelty_boost: float = 0.3,
        history_window: int = 10
    ):
        # Configuration
        self.baseline_arousal = baseline_arousal
        self.optimal_range = optimal_range
        self.stress_sensitivity = stress_sensitivity
        self.decay_rate = decay_rate
        self.novelty_boost = novelty_boost
        self.history_window = history_window

        # Compute optimal center
        self.optimal_center = (optimal_range[0] + optimal_range[1]) / 2.0

        # State
        self.current_arousal: float = baseline_arousal
        self.arousal_history: List[float] = []
        self.total_events: int = 0

    def update_arousal(self, task_urgency: float, stress: float, novelty: float) -> float:
        """
        Update arousal from task urgency, stress, and novelty

        Parameters:
        -----------
        task_urgency : float
            Task urgency level (0-1)
        stress : float
            Stress level (0-1)
        novelty : float
            Novelty level (0-1)

        Returns:
        --------
        arousal_level : float
            Updated arousal level (0-1)
        """
        # Decay toward baseline (arousal naturally decays)
        self.current_arousal = (self.current_arousal * self.decay_rate +
                                self.baseline_arousal * (1.0 - self.decay_rate))

        # Only add boosts if inputs exceed baseline threshold
        # Task urgency raises arousal (only if above baseline)
        if task_urgency > self.baseline_arousal:
            urgency_boost = (task_urgency - self.baseline_arousal) * 0.3
            self.current_arousal += urgency_boost

        # Stress strongly raises arousal
        stress_boost = stress * self.stress_sensitivity * 0.2
        self.current_arousal += stress_boost

        # Novelty moderately raises arousal
        novelty_boost_value = novelty * self.novelty_boost * 0.15
        self.current_arousal += novelty_boost_value

        # Clamp to [0, 1]
        self.current_arousal = max(0.0, min(1.0, self.current_arousal))

        # Update history
        self.arousal_history.append(self.current_arousal)
        if len(self.arousal_history) > self.history_window:
            self.arousal_history.pop(0)

        return self.current_arousal

    def compute_performance_multiplier(self) -> float:
        """
        Compute performance multiplier (inverted-U curve)

        Optimal arousal → maximum performance
        Too low/high arousal → degraded performance

        Returns:
        --------
        performance_multiplier : float
            Performance multiplier (0-1)
        """
        # Distance from optimal center
        optimal_distance = abs(self.current_arousal - self.optimal_center)

        # Inverted-U: performance = 1 - distance^2 (parabola)
        # Scale to make optimal range = 1.0
        performance = 1.0 - (optimal_distance / 0.5) ** 2

        # Clamp to [0, 1]
        performance = max(0.0, min(1.0, performance))

        return performance

    def compute_focus_width(self) -> float:
        """
        Compute focus width (attention breadth)

        High arousal → narrow focus (tunnel vision)
        Low arousal → broad focus (diffuse attention)

        Returns:
        --------
        focus_width : float
            Focus width (0-1, 0=narrow, 1=broad)
        """
        # Focus width inversely proportional to arousal
        # High arousal → narrow (low width)
        # Low arousal → broad (high width)
        focus_width = 1.0 - self.current_arousal

        return focus_width

    def get_exploit_vs_explore(self) -> float:
        """
        Compute exploration tendency

        Optimal arousal → exploit (focused task execution)
        Extreme arousal (low/high) → explore (search for alternatives)

        Returns:
        --------
        explore_tendency : float
            Exploration tendency (0-1)
            0 = pure exploitation
            1 = pure exploration
        """
        # Distance from optimal center
        optimal_distance = abs(self.current_arousal - self.optimal_center)

        # Exploration tendency increases with distance from optimal
        # At optimal → explore_tendency ≈ 0 (exploit)
        # At extremes → explore_tendency ≈ 1 (explore)

        # Scale distance to 0-1 range
        # Maximum distance from center = 0.6 (if center=0.6, max distance to 0 or 1 is 0.6)
        max_distance = max(self.optimal_center, 1.0 - self.optimal_center)
        explore_tendency = optimal_distance / max_distance

        # Clamp to [0, 1]
        explore_tendency = max(0.0, min(1.0, explore_tendency))

        return explore_tendency

    def compute_stress_response(self, stressor: float) -> float:
        """
        Compute stress response (fight-or-flight activation)

        High stress → high arousal activation

        Parameters:
        -----------
        stressor : float
            Stressor intensity (0-1)

        Returns:
        --------
        stress_response : float
            Stress response activation (0-1)
        """
        # Stress response = stressor * sensitivity
        stress_response = stressor * self.stress_sensitivity

        # Clamp to [0, 1]
        stress_response = max(0.0, min(1.0, stress_response))

        return stress_response

    def process_event(self, task_urgency: float, stress: float) -> Dict:
        """
        Main processing: update arousal, compute modulations

        Parameters:
        -----------
        task_urgency : float
            Task urgency level (0-1)
        stress : float
            Stress level (0-1)

        Returns:
        --------
        result : Dict
            {
                "arousal_level": float,
                "performance_multiplier": float,
                "focus_width": float,
                "explore_tendency": float,
                "stress_response": float
            }
        """
        # 1. Update arousal (using novelty=0 as default)
        self.update_arousal(task_urgency, stress, novelty=0.0)

        # 2. Compute performance multiplier (inverted-U)
        performance_multiplier = self.compute_performance_multiplier()

        # 3. Compute focus width
        focus_width = self.compute_focus_width()

        # 4. Compute exploit vs explore
        explore_tendency = self.get_exploit_vs_explore()

        # 5. Compute stress response
        stress_response = self.compute_stress_response(stress)

        # 6. Update event counter
        self.total_events += 1

        # 7. Return complete result
        return {
            "arousal_level": float(self.current_arousal),
            "performance_multiplier": float(performance_multiplier),
            "focus_width": float(focus_width),
            "explore_tendency": float(explore_tendency),
            "stress_response": float(stress_response)
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
                "performance_multiplier": float,
                "focus_width": float,
                "explore_tendency": float,
                "optimal_distance": float,
                "total_events": int
            }
        """
        # Current arousal
        arousal_level = self.current_arousal

        # Arousal statistics
        arousal_mean = np.mean(self.arousal_history) if self.arousal_history else self.baseline_arousal

        # Performance multiplier
        performance_multiplier = self.compute_performance_multiplier()

        # Focus width
        focus_width = self.compute_focus_width()

        # Explore tendency
        explore_tendency = self.get_exploit_vs_explore()

        # Optimal distance (how far from optimal)
        optimal_distance = abs(self.current_arousal - self.optimal_center)

        return {
            "arousal_level": float(arousal_level),
            "arousal_history": self.arousal_history.copy(),
            "arousal_mean": float(arousal_mean),
            "performance_multiplier": float(performance_multiplier),
            "focus_width": float(focus_width),
            "explore_tendency": float(explore_tendency),
            "optimal_distance": float(optimal_distance),
            "total_events": int(self.total_events)
        }
