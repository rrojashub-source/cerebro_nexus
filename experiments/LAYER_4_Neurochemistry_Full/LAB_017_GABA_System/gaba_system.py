"""
LAB_017: GABA System

Inhibitory control, excitation/inhibition balance, anxiety modulation.

Biological Inspiration:
- GABAergic interneurons (cortex, amygdala)
- Main inhibitory neurotransmitter in CNS

Core Function: E/I balance & anxiety reduction

Key Papers:
- Yizhar, O. et al. (2011). "Neocortical excitation/inhibition balance in information processing"
- Luscher, B. et al. (2011). "The GABAergic deficit hypothesis of major depressive disorder"
"""

from typing import Dict, List
import numpy as np


class GABASystem:
    """
    LAB_017: GABA inhibitory control and anxiety modulation

    Biological inspiration: GABAergic interneurons

    Parameters:
    -----------
    baseline_gaba : float
        Initial GABA level (default: 0.5, medium)
    inhibition_strength : float
        How much GABA inhibits excitation (default: 0.7)
    anxiety_threshold : float
        GABA threshold for calm state (default: 0.6)
    anxiety_sensitivity : float
        How much anxiety spikes GABA (default: 0.3)
    gaba_decay : float
        Decay rate toward baseline (default: 0.9)
    history_window : int
        Size of GABA history buffer (default: 20)
    """

    def __init__(
        self,
        baseline_gaba: float = 0.5,
        inhibition_strength: float = 0.7,
        anxiety_threshold: float = 0.6,
        anxiety_sensitivity: float = 0.3,
        gaba_decay: float = 0.9,
        history_window: int = 20
    ):
        # Configuration
        self.baseline_gaba = baseline_gaba
        self.inhibition_strength = inhibition_strength
        self.anxiety_threshold = anxiety_threshold
        self.anxiety_sensitivity = anxiety_sensitivity
        self.gaba_decay = gaba_decay
        self.history_window = history_window

        # State
        self.gaba_level: float = baseline_gaba
        self.gaba_history: List[float] = []
        self.total_events: int = 0

    def update_gaba(self, anxiety: float, excitation: float) -> float:
        """
        Update GABA level from anxiety and excitation

        GABA increases when anxiety or excitation is high
        (body's compensatory mechanism to restore balance)

        Parameters:
        -----------
        anxiety : float
            Anxiety level (0-1)
        excitation : float
            Excitation level (0-1)

        Returns:
        --------
        gaba_level : float
            Updated GABA level (0-1)
        """
        # Decay toward baseline
        decay_delta = (self.baseline_gaba - self.gaba_level) * (1.0 - self.gaba_decay)
        self.gaba_level = self.gaba_level + decay_delta

        # GABA spike from anxiety (body tries to calm down)
        anxiety_spike = anxiety * self.anxiety_sensitivity
        self.gaba_level = self.gaba_level + anxiety_spike

        # GABA boost from excitation (body tries to inhibit)
        excitation_boost = excitation * 0.2  # Smaller than anxiety
        self.gaba_level = self.gaba_level + excitation_boost

        # Clamp to [0, 1]
        self.gaba_level = max(0.0, min(1.0, self.gaba_level))

        # Add to history
        self.gaba_history.append(self.gaba_level)
        if len(self.gaba_history) > self.history_window:
            self.gaba_history.pop(0)

        return self.gaba_level

    def compute_ei_balance(self, excitation: float) -> Dict:
        """
        Compute excitation/inhibition balance

        E/I ratio = excitation / inhibition
        Healthy ratio: ~1.0 to 1.5
        High ratio: runaway excitation (anxiety, seizures)
        Low ratio: over-inhibition (lethargy)

        Parameters:
        -----------
        excitation : float
            Excitation level (0-1)

        Returns:
        --------
        result : Dict
            {
                "inhibition": float (0-1),
                "ei_ratio": float,
                "is_balanced": bool,
                "balance_state": str
            }
        """
        # Inhibition proportional to GABA
        inhibition = self.gaba_level * self.inhibition_strength

        # E/I ratio (handle division by zero)
        if inhibition < 0.01:
            ei_ratio = 10.0  # Very high (runaway excitation)
        else:
            ei_ratio = excitation / inhibition

        # Check if balanced (healthy range: 1.0 to 1.5)
        is_balanced = 1.0 <= ei_ratio <= 1.5

        # Balance state
        if ei_ratio < 1.0:
            balance_state = "over_inhibited"
        elif ei_ratio <= 1.5:
            balance_state = "balanced"
        else:
            balance_state = "over_excited"

        return {
            "inhibition": float(inhibition),
            "ei_ratio": float(ei_ratio),
            "is_balanced": bool(is_balanced),
            "balance_state": balance_state
        }

    def modulate_anxiety(self, base_anxiety: float) -> Dict:
        """
        Modulate anxiety based on GABA level

        High GABA = reduced anxiety (calming inhibition)
        Low GABA = high anxiety (lack of inhibition)

        Parameters:
        -----------
        base_anxiety : float
            Base anxiety level (0-1)

        Returns:
        --------
        result : Dict
            {
                "modulated_anxiety": float (0-1),
                "is_calm": bool,
                "anxiety_reduction": float
            }
        """
        # GABA reduces anxiety
        anxiety_reduction = self.gaba_level * 0.5
        modulated_anxiety = base_anxiety * (1.0 - anxiety_reduction)

        # Clamp to [0, 1]
        modulated_anxiety = max(0.0, min(1.0, modulated_anxiety))

        # Calm if GABA above threshold
        is_calm = self.gaba_level >= self.anxiety_threshold

        return {
            "modulated_anxiety": float(modulated_anxiety),
            "is_calm": bool(is_calm),
            "anxiety_reduction": float(anxiety_reduction)
        }

    def compute_inhibitory_control(self, excitatory_signal: float) -> Dict:
        """
        Compute inhibitory suppression of excitation

        Net signal = excitation - inhibition
        High GABA = strong suppression

        Parameters:
        -----------
        excitatory_signal : float
            Excitatory signal strength (0-1)

        Returns:
        --------
        result : Dict
            {
                "inhibition": float (0-1),
                "net_signal": float (0-1),
                "suppression_ratio": float
            }
        """
        # Inhibition proportional to GABA
        inhibition = self.gaba_level * self.inhibition_strength

        # Net signal (excitation - inhibition, clamped)
        net_signal = excitatory_signal - inhibition
        net_signal = max(0.0, min(1.0, net_signal))

        # Suppression ratio (how much was suppressed)
        if excitatory_signal < 0.01:
            suppression_ratio = 0.0
        else:
            suppression_ratio = inhibition / excitatory_signal
            suppression_ratio = min(1.0, suppression_ratio)

        return {
            "inhibition": float(inhibition),
            "net_signal": float(net_signal),
            "suppression_ratio": float(suppression_ratio)
        }

    def get_network_stability(self) -> float:
        """
        Compute network stability (inverse of GABA variance)

        Returns:
        --------
        stability : float
            Network stability score (0-1)
            Higher = more stable GABA
        """
        if len(self.gaba_history) < 2:
            return 1.0  # Maximally stable if no history

        # Compute variance of GABA history
        gaba_variance = np.var(self.gaba_history)

        # Stability = inverse of variance (normalized)
        stability = 1.0 / (1.0 + gaba_variance)

        return float(stability)

    def process_event(
        self,
        anxiety: float,
        excitation: float,
        base_anxiety: float = 0.5,
        excitatory_signal: float = 0.5
    ) -> Dict:
        """
        Main processing: update GABA, compute E/I balance, modulate anxiety

        Parameters:
        -----------
        anxiety : float
            Anxiety level (0-1)
        excitation : float
            Excitation level (0-1)
        base_anxiety : float
            Base anxiety level (default: 0.5)
        excitatory_signal : float
            Excitatory signal strength (default: 0.5)

        Returns:
        --------
        result : Dict
            {
                "gaba_level": float,
                "ei_balance": Dict,
                "anxiety": Dict,
                "inhibitory_control": Dict,
                "network_stability": float
            }
        """
        # 1. Update GABA from anxiety and excitation
        self.update_gaba(anxiety, excitation)

        # 2. Compute E/I balance
        ei_balance = self.compute_ei_balance(excitation)

        # 3. Modulate anxiety
        anxiety_result = self.modulate_anxiety(base_anxiety)

        # 4. Compute inhibitory control
        inhibitory_control = self.compute_inhibitory_control(excitatory_signal)

        # 5. Get network stability
        stability = self.get_network_stability()

        # 6. Update event counter
        self.total_events += 1

        # 7. Return complete result
        return {
            "gaba_level": float(self.gaba_level),
            "ei_balance": ei_balance,
            "anxiety": anxiety_result,
            "inhibitory_control": inhibitory_control,
            "network_stability": float(stability)
        }

    def get_state(self) -> Dict:
        """
        Get current GABA system state

        Returns:
        --------
        state : Dict
            {
                "gaba_level": float,
                "gaba_history": List[float],
                "gaba_mean": float,
                "network_stability": float,
                "total_events": int
            }
        """
        # Current GABA
        gaba_current = self.gaba_level

        # GABA statistics
        gaba_mean = np.mean(self.gaba_history) if self.gaba_history else self.baseline_gaba
        network_stability = self.get_network_stability()

        return {
            "gaba_level": float(gaba_current),
            "gaba_history": self.gaba_history.copy(),
            "gaba_mean": float(gaba_mean),
            "network_stability": float(network_stability),
            "total_events": int(self.total_events)
        }
