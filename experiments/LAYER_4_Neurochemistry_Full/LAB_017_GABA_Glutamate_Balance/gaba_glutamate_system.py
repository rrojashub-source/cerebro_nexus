"""
LAB_017: GABA/Glutamate Balance

Excitation/Inhibition (E/I) balance and homeostatic control.

Biological Inspiration:
- Excitatory (Glutamate) and Inhibitory (GABA) neurons
- E/I balance crucial for network stability

Core Functions:
- Excitation/Inhibition balance management
- Homeostatic control (auto-regulation toward optimal)
- Network gain modulation (signal amplification)
- Stability maintenance (prevents runaway activation)

Key Papers:
- Destexhe & Marder (2004) - "Excitation-inhibition balance"
- Isaacson & Scanziani (2011) - "How inhibition shapes cortical activity"
"""

from typing import Dict, List, Tuple
import numpy as np


class GABAGlutamateSystem:
    """
    LAB_017: GABA/Glutamate E/I balance and homeostatic control

    Biological inspiration: Excitatory and inhibitory neurons

    Parameters:
    -----------
    baseline_glutamate : float
        Baseline glutamate (excitation) level (default: 0.6)
    baseline_gaba : float
        Baseline GABA (inhibition) level (default: 0.4)
    optimal_ratio : float
        Optimal E/I ratio (default: 0.75)
    homeostatic_gain : float
        Homeostatic correction strength (default: 0.3)
    adaptation_rate : float
        Speed of level adjustments (default: 0.1)
    history_window : int
        Size of history buffer (default: 15)
    """

    def __init__(
        self,
        baseline_glutamate: float = 0.6,
        baseline_gaba: float = 0.4,
        optimal_ratio: float = 0.75,
        homeostatic_gain: float = 0.3,
        adaptation_rate: float = 0.1,
        history_window: int = 15
    ):
        # Configuration
        self.baseline_glutamate = baseline_glutamate
        self.baseline_gaba = baseline_gaba
        self.optimal_ratio = optimal_ratio
        self.homeostatic_gain = homeostatic_gain
        self.adaptation_rate = adaptation_rate
        self.history_window = history_window

        # Epsilon to prevent division by zero
        self.epsilon = 0.01

        # State
        self.glutamate_level: float = baseline_glutamate
        self.gaba_level: float = baseline_gaba
        self.glutamate_history: List[float] = []
        self.gaba_history: List[float] = []
        self.total_events: int = 0

    def update_excitation(self, activation: float, stress: float) -> float:
        """
        Update glutamate (excitation) from activation and stress

        Parameters:
        -----------
        activation : float
            Activation level (0-1)
        stress : float
            Stress level (0-1)

        Returns:
        --------
        glutamate_level : float
            Updated glutamate level (0-1)
        """
        # Activation increases excitation
        activation_boost = activation * 0.2

        # Stress strongly increases excitation
        stress_boost = stress * 0.3

        # Update level
        self.glutamate_level += activation_boost + stress_boost

        # Clamp to [0, 1]
        self.glutamate_level = max(0.0, min(1.0, self.glutamate_level))

        # Update history
        self.glutamate_history.append(self.glutamate_level)
        if len(self.glutamate_history) > self.history_window:
            self.glutamate_history.pop(0)

        return self.glutamate_level

    def update_inhibition(self, stability_demand: float) -> float:
        """
        Update GABA (inhibition) from stability demand

        Parameters:
        -----------
        stability_demand : float
            Stability/calming need (0-1)

        Returns:
        --------
        gaba_level : float
            Updated GABA level (0-1)
        """
        # Stability demand increases inhibition
        stability_boost = stability_demand * 0.25

        # Update level
        self.gaba_level += stability_boost

        # Clamp to [0, 1]
        self.gaba_level = max(0.0, min(1.0, self.gaba_level))

        # Update history
        self.gaba_history.append(self.gaba_level)
        if len(self.gaba_history) > self.history_window:
            self.gaba_history.pop(0)

        return self.gaba_level

    def compute_ei_ratio(self) -> float:
        """
        Compute Excitation/Inhibition ratio

        E/I = glutamate / (gaba + epsilon)

        Returns:
        --------
        ei_ratio : float
            E/I ratio
        """
        ei_ratio = self.glutamate_level / (self.gaba_level + self.epsilon)
        return ei_ratio

    def compute_stability_index(self) -> float:
        """
        Compute stability index (how close to optimal E/I ratio)

        Stability = 1 - |ei_ratio - optimal_ratio| / optimal_ratio

        Returns:
        --------
        stability_index : float
            Stability index (0-1, 1=perfectly stable)
        """
        ei_ratio = self.compute_ei_ratio()

        # Distance from optimal (normalized)
        distance = abs(ei_ratio - self.optimal_ratio) / self.optimal_ratio

        # Stability = 1 - distance (clamped to [0, 1])
        stability_index = 1.0 - distance
        stability_index = max(0.0, min(1.0, stability_index))

        return stability_index

    def apply_homeostatic_control(self) -> Tuple[float, float]:
        """
        Apply homeostatic control to move E/I ratio toward optimal

        High E/I → increase GABA (dampen excitation)
        Low E/I → increase Glutamate (increase excitation)

        Returns:
        --------
        (glutamate_level, gaba_level) : Tuple[float, float]
            Updated levels after homeostatic correction
        """
        ei_ratio = self.compute_ei_ratio()

        # Error from optimal
        error = ei_ratio - self.optimal_ratio

        # Homeostatic correction (direct proportional control)
        # Stronger correction for larger errors
        correction_strength = self.homeostatic_gain * self.adaptation_rate

        if error > 0:
            # E/I too high → increase GABA (inhibition)
            # The larger the error, the more GABA we add
            gaba_increment = error * correction_strength
            self.gaba_level += gaba_increment
        else:
            # E/I too low → increase Glutamate (excitation)
            # The larger the negative error, the more glutamate we add
            glut_increment = abs(error) * correction_strength
            self.glutamate_level += glut_increment

        # Clamp levels
        self.glutamate_level = max(0.0, min(1.0, self.glutamate_level))
        self.gaba_level = max(0.0, min(1.0, self.gaba_level))

        return (self.glutamate_level, self.gaba_level)

    def compute_network_gain(self) -> float:
        """
        Compute network gain (signal amplification)

        High E/I ratio → high gain (amplification)
        Low E/I ratio → low gain (dampening)

        Returns:
        --------
        network_gain : float
            Network amplification gain (0-2)
        """
        ei_ratio = self.compute_ei_ratio()

        # Gain scales with E/I ratio (normalized to 0-2 range)
        # At optimal (0.75): gain ≈ 0.75
        # Higher E/I: higher gain (up to 2.0)
        network_gain = min(2.0, ei_ratio)

        return network_gain

    def process_event(self, activation: float, stability_demand: float) -> Dict:
        """
        Main processing: update E/I levels, apply homeostasis, compute outputs

        Parameters:
        -----------
        activation : float
            Activation level (0-1)
        stability_demand : float
            Stability/calming need (0-1)

        Returns:
        --------
        result : Dict
            {
                "glutamate_level": float,
                "gaba_level": float,
                "ei_ratio": float,
                "stability_index": float,
                "network_gain": float
            }
        """
        # 1. Update excitation (assuming no stress for basic event)
        self.update_excitation(activation, stress=0.0)

        # 2. Update inhibition
        self.update_inhibition(stability_demand)

        # 3. Apply homeostatic control
        self.apply_homeostatic_control()

        # 4. Compute E/I ratio
        ei_ratio = self.compute_ei_ratio()

        # 5. Compute stability index
        stability_index = self.compute_stability_index()

        # 6. Compute network gain
        network_gain = self.compute_network_gain()

        # 7. Update event counter
        self.total_events += 1

        # 8. Return complete result
        return {
            "glutamate_level": float(self.glutamate_level),
            "gaba_level": float(self.gaba_level),
            "ei_ratio": float(ei_ratio),
            "stability_index": float(stability_index),
            "network_gain": float(network_gain)
        }

    def get_state(self) -> Dict:
        """
        Get current GABA/Glutamate system state

        Returns:
        --------
        state : Dict
            {
                "glutamate_level": float,
                "gaba_level": float,
                "glutamate_history": List[float],
                "gaba_history": List[float],
                "ei_ratio": float,
                "ei_ratio_mean": float,
                "stability_index": float,
                "network_gain": float,
                "total_events": int
            }
        """
        # Current levels
        glutamate_level = self.glutamate_level
        gaba_level = self.gaba_level

        # E/I ratio
        ei_ratio = self.compute_ei_ratio()

        # E/I ratio statistics
        if self.glutamate_history and self.gaba_history:
            # Compute historical E/I ratios
            historical_ratios = [
                g / (b + self.epsilon)
                for g, b in zip(self.glutamate_history, self.gaba_history)
            ]
            ei_ratio_mean = np.mean(historical_ratios)
        else:
            ei_ratio_mean = ei_ratio

        # Stability index
        stability_index = self.compute_stability_index()

        # Network gain
        network_gain = self.compute_network_gain()

        return {
            "glutamate_level": float(glutamate_level),
            "gaba_level": float(gaba_level),
            "glutamate_history": self.glutamate_history.copy(),
            "gaba_history": self.gaba_history.copy(),
            "ei_ratio": float(ei_ratio),
            "ei_ratio_mean": float(ei_ratio_mean),
            "stability_index": float(stability_index),
            "network_gain": float(network_gain),
            "total_events": int(self.total_events)
        }
