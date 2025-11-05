"""
LAB_016: Acetylcholine System

Attention amplification, learning enhancement, and encoding strength.

Biological Inspiration:
- Basal forebrain (nucleus basalis)
- Cholinergic projections to cortex/hippocampus

Core Function: Attention gating & encoding/recall modulation

Key Papers:
- Hasselmo, M. E. (2006). "The role of acetylcholine in learning and memory"
- Sarter, M., Parikh, V., & Howe, W. M. (2009). "Phasic acetylcholine release and the volume transmission hypothesis"
"""

from typing import Dict, List
import numpy as np


class AcetylcholineSystem:
    """
    LAB_016: Acetylcholine attention and encoding modulation

    Biological inspiration: Basal forebrain cholinergic neurons

    Parameters:
    -----------
    baseline_ach : float
        Initial ACh level (default: 0.5, medium)
    amplification_gain : float
        How much ACh amplifies attention (default: 0.3)
    encoding_threshold : float
        ACh threshold for strong encoding (default: 0.6)
    novelty_sensitivity : float
        How much novelty spikes ACh (default: 0.4)
    ach_decay : float
        Decay rate toward baseline (default: 0.9)
    history_window : int
        Size of ACh history buffer (default: 20)
    """

    def __init__(
        self,
        baseline_ach: float = 0.5,
        amplification_gain: float = 0.3,
        encoding_threshold: float = 0.6,
        novelty_sensitivity: float = 0.4,
        ach_decay: float = 0.9,
        history_window: int = 20
    ):
        # Configuration
        self.baseline_ach = baseline_ach
        self.amplification_gain = amplification_gain
        self.encoding_threshold = encoding_threshold
        self.novelty_sensitivity = novelty_sensitivity
        self.ach_decay = ach_decay
        self.history_window = history_window

        # State
        self.ach_level: float = baseline_ach
        self.ach_history: List[float] = []
        self.mode: str = "encoding"  # "encoding" or "recall"
        self.total_events: int = 0

    def update_ach(self, novelty: float, attention_demand: float) -> float:
        """
        Update ACh level from novelty and attention demand

        ACh spikes rapidly for novel stimuli and high attention demands.
        Decays slowly toward baseline.

        Parameters:
        -----------
        novelty : float
            Novelty score (0-1)
        attention_demand : float
            Attention demand (0-1)

        Returns:
        --------
        ach_level : float
            Updated ACh level (0-1)
        """
        # Decay toward baseline
        decay_delta = (self.baseline_ach - self.ach_level) * (1.0 - self.ach_decay)
        self.ach_level = self.ach_level + decay_delta

        # ACh spike from novelty (novel stimuli trigger ACh release)
        novelty_spike = novelty * self.novelty_sensitivity
        self.ach_level = self.ach_level + novelty_spike

        # ACh boost from attention demand
        attention_boost = attention_demand * 0.2  # Smaller than novelty
        self.ach_level = self.ach_level + attention_boost

        # Clamp to [0, 1]
        self.ach_level = max(0.0, min(1.0, self.ach_level))

        # Add to history
        self.ach_history.append(self.ach_level)
        if len(self.ach_history) > self.history_window:
            self.ach_history.pop(0)

        return self.ach_level

    def amplify_attention(self, base_attention: float) -> float:
        """
        Amplify attention signal based on ACh level

        High ACh = amplified attention (increased signal-to-noise ratio)
        Low ACh = baseline attention

        Parameters:
        -----------
        base_attention : float
            Base attention signal (0-1)

        Returns:
        --------
        amplified_attention : float
            Amplified attention signal (0-1)
        """
        # ACh boosts attention signal
        amplification = 1.0 + (self.ach_level * self.amplification_gain)
        amplified_attention = base_attention * amplification

        # Clamp to [0, 1]
        amplified_attention = max(0.0, min(1.0, amplified_attention))

        return float(amplified_attention)

    def modulate_encoding(self, base_encoding_strength: float) -> Dict:
        """
        Modulate encoding strength based on ACh level and mode

        High ACh during encoding mode = strong encoding
        Low ACh during recall mode = consolidation (no new encoding)

        Parameters:
        -----------
        base_encoding_strength : float
            Base encoding strength (0-1)

        Returns:
        --------
        result : Dict
            {
                "encoding_strength": float (0-1),
                "is_strong_encoding": bool,
                "mode": str
            }
        """
        if self.mode == "encoding":
            # High ACh during encoding = strong encoding
            encoding_multiplier = 1.0 + (self.ach_level * 0.5)
            encoding_strength = base_encoding_strength * encoding_multiplier
            encoding_strength = min(1.0, encoding_strength)
        else:
            # Recall mode: reduce encoding (consolidation phase)
            encoding_strength = base_encoding_strength * 0.3

        # Check if encoding is strong (above threshold)
        is_strong_encoding = (self.ach_level >= self.encoding_threshold) and (self.mode == "encoding")

        return {
            "encoding_strength": float(encoding_strength),
            "is_strong_encoding": bool(is_strong_encoding),
            "mode": self.mode
        }

    def compute_learning_readiness(self) -> Dict:
        """
        Compute learning readiness based on ACh level

        High ACh = ready to learn (plasticity enabled)
        Low ACh = consolidation mode (plasticity reduced)

        Returns:
        --------
        result : Dict
            {
                "learning_readiness": float (0-1),
                "is_ready_to_learn": bool,
                "plasticity_gate": float (0-1)
            }
        """
        # Learning readiness = ACh level (direct relationship)
        learning_readiness = self.ach_level

        # Ready to learn if ACh above encoding threshold
        is_ready_to_learn = self.ach_level >= self.encoding_threshold

        # Plasticity gate (controls synaptic plasticity)
        # High ACh = open gate (plasticity enabled)
        plasticity_gate = self.ach_level

        return {
            "learning_readiness": float(learning_readiness),
            "is_ready_to_learn": bool(is_ready_to_learn),
            "plasticity_gate": float(plasticity_gate)
        }

    def set_mode(self, mode: str) -> None:
        """
        Set encoding/recall mode

        Parameters:
        -----------
        mode : str
            "encoding" or "recall"
        """
        if mode not in ["encoding", "recall"]:
            raise ValueError(f"Invalid mode: {mode}. Must be 'encoding' or 'recall'.")
        self.mode = mode

    def get_ach_stability(self) -> float:
        """
        Compute ACh stability (inverse of ACh variance)

        Returns:
        --------
        stability : float
            ACh stability score (0-1)
            Higher = more stable ACh
        """
        if len(self.ach_history) < 2:
            return 1.0  # Maximally stable if no history

        # Compute variance of ACh history
        ach_variance = np.var(self.ach_history)

        # Stability = inverse of variance (normalized)
        stability = 1.0 / (1.0 + ach_variance)

        return float(stability)

    def process_stimulus(
        self,
        novelty: float,
        attention_demand: float,
        base_attention: float = 0.5,
        base_encoding_strength: float = 0.5
    ) -> Dict:
        """
        Main processing: update ACh, amplify attention, modulate encoding

        Parameters:
        -----------
        novelty : float
            Novelty score (0-1)
        attention_demand : float
            Attention demand (0-1)
        base_attention : float
            Base attention signal (default: 0.5)
        base_encoding_strength : float
            Base encoding strength (default: 0.5)

        Returns:
        --------
        result : Dict
            {
                "ach_level": float,
                "amplified_attention": float,
                "encoding": Dict,
                "learning_readiness": Dict,
                "ach_stability": float
            }
        """
        # 1. Update ACh from novelty and attention demand
        self.update_ach(novelty, attention_demand)

        # 2. Amplify attention
        amplified_attention = self.amplify_attention(base_attention)

        # 3. Modulate encoding
        encoding = self.modulate_encoding(base_encoding_strength)

        # 4. Compute learning readiness
        learning_readiness = self.compute_learning_readiness()

        # 5. Get ACh stability
        stability = self.get_ach_stability()

        # 6. Update event counter
        self.total_events += 1

        # 7. Return complete result
        return {
            "ach_level": float(self.ach_level),
            "amplified_attention": float(amplified_attention),
            "encoding": encoding,
            "learning_readiness": learning_readiness,
            "ach_stability": float(stability)
        }

    def get_state(self) -> Dict:
        """
        Get current acetylcholine system state

        Returns:
        --------
        state : Dict
            {
                "ach_level": float,
                "ach_history": List[float],
                "ach_mean": float,
                "ach_stability": float,
                "mode": str,
                "learning_readiness": float,
                "total_events": int
            }
        """
        # Current ACh
        ach_current = self.ach_level

        # ACh statistics
        ach_mean = np.mean(self.ach_history) if self.ach_history else self.baseline_ach
        ach_stability = self.get_ach_stability()

        # Learning readiness
        learning_readiness = self.compute_learning_readiness()

        return {
            "ach_level": float(ach_current),
            "ach_history": self.ach_history.copy(),
            "ach_mean": float(ach_mean),
            "ach_stability": float(ach_stability),
            "mode": self.mode,
            "learning_readiness": float(learning_readiness["learning_readiness"]),
            "total_events": int(self.total_events)
        }
