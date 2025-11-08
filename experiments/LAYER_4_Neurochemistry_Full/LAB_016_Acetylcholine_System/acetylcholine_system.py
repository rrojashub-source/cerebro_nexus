"""
LAB_016: Acetylcholine System

Attention amplification, learning enhancement, and encoding strength.

Biological Inspiration:
- Basal forebrain cholinergic neurons (nucleus basalis)
- Cholinergic projections to cortex and hippocampus

Core Functions:
- Attention amplification (enhances signal-to-noise)
- Encoding strength (high ACh → strong memory formation)
- Learning rate modulation (ACh gates plasticity)
- Stimulus selectivity (enhances relevant, suppresses irrelevant)

Key Papers:
- Hasselmo (2006) - "The role of acetylcholine in learning and memory"
- Sarter et al. (2009) - "Phasic acetylcholine release and the volume transmission hypothesis"
"""

from typing import Dict, List
import numpy as np


class AcetylcholineSystem:
    """
    LAB_016: Acetylcholine attention and encoding modulation

    Biological inspiration: Basal forebrain cholinergic neurons

    Parameters:
    -----------
    baseline_level : float
        Baseline ACh level (default: 0.5, medium)
    attention_gain : float
        Attention amplification multiplier (default: 2.0)
    encoding_boost : float
        Encoding strength boost multiplier (default: 1.5)
    selectivity_factor : float
        Stimulus selectivity strength (default: 0.8)
    history_window : int
        Size of ACh history buffer (default: 10)
    """

    def __init__(
        self,
        baseline_level: float = 0.5,
        attention_gain: float = 2.0,
        encoding_boost: float = 1.5,
        selectivity_factor: float = 0.8,
        history_window: int = 10
    ):
        # Configuration
        self.baseline_level = baseline_level
        self.attention_gain = attention_gain
        self.encoding_boost = encoding_boost
        self.selectivity_factor = selectivity_factor
        self.history_window = history_window

        # State
        self.current_level: float = baseline_level
        self.level_history: List[float] = []
        self.total_events: int = 0

    def update_level(self, attention_demand: float, learning_context: bool) -> float:
        """
        Update ACh level from attention demand and learning context

        Parameters:
        -----------
        attention_demand : float
            Attention demand level (0-1)
        learning_context : bool
            Whether in learning/encoding context (True) or not (False)

        Returns:
        --------
        ach_level : float
            Updated ACh level (0-1)
        """
        # Decay toward baseline (gradual return to baseline without stimulation)
        decay_rate = 0.85
        self.current_level = (self.current_level * decay_rate +
                             self.baseline_level * (1.0 - decay_rate))

        # Learning context strongly activates ACh
        if learning_context:
            learning_boost = 0.3
            self.current_level += learning_boost

        # Attention demand moderately activates ACh
        attention_boost = attention_demand * 0.2
        self.current_level += attention_boost

        # Clamp to [0, 1]
        self.current_level = max(0.0, min(1.0, self.current_level))

        # Update history
        self.level_history.append(self.current_level)
        if len(self.level_history) > self.history_window:
            self.level_history.pop(0)

        return self.current_level

    def compute_encoding_strength(self, base_strength: float) -> float:
        """
        Compute memory encoding strength boost

        High ACh → strong memory formation

        Parameters:
        -----------
        base_strength : float
            Base encoding strength (0-1)

        Returns:
        --------
        encoding_strength : float
            Boosted encoding strength (0-1)
        """
        # Encoding boost with non-linear scaling (squared ACh for gentler low-ACh boost)
        # At low ACh (0.2): boost_factor = 1.0 + 0.04 * 1.5 = 1.06 (minimal)
        # At high ACh (0.9): boost_factor = 1.0 + 0.81 * 1.5 = 2.215 (strong)
        boost_factor = 1.0 + (self.current_level ** 2) * self.encoding_boost
        encoding_strength = base_strength * boost_factor

        # Clamp to [0, 1]
        encoding_strength = max(0.0, min(1.0, encoding_strength))

        return encoding_strength

    def compute_attention_gain(self, stimulus_relevance: float) -> float:
        """
        Compute attention amplification gain

        High ACh + high relevance → strong amplification
        High ACh + low relevance → suppression

        Parameters:
        -----------
        stimulus_relevance : float
            Stimulus relevance (0-1, 0=irrelevant, 1=highly relevant)

        Returns:
        --------
        attention_gain : float
            Attention amplification gain (≥1.0)
        """
        # Gain scales with both ACh and stimulus relevance
        # Relevant stimuli amplified, irrelevant suppressed
        relevance_modulation = stimulus_relevance * self.selectivity_factor

        # Gain = 1.0 + (ach_level * relevance_modulation * attention_gain)
        gain = 1.0 + (self.current_level * relevance_modulation * self.attention_gain)

        # Minimum gain of 1.0 (no suppression below baseline)
        gain = max(1.0, gain)

        return gain

    def compute_learning_rate_modulation(self, base_lr: float) -> float:
        """
        Compute learning rate modulation (plasticity gating)

        High ACh → high plasticity (increased LR)
        Low ACh → low plasticity (reduced LR)

        Parameters:
        -----------
        base_lr : float
            Base learning rate

        Returns:
        --------
        modulated_lr : float
            ACh-modulated learning rate
        """
        # Learning rate scales with ACh level
        # lr_modulation = base_lr * (0.5 + 1.5 * ach_level)
        # This gives range [0.5x, 2.0x] of base_lr
        modulation_factor = 0.5 + 1.5 * self.current_level
        modulated_lr = base_lr * modulation_factor

        return modulated_lr

    def compute_snr_enhancement(self) -> float:
        """
        Compute signal-to-noise ratio enhancement

        High ACh → improved SNR (noise suppression)

        Returns:
        --------
        snr_enhancement : float
            SNR enhancement factor (0-1)
        """
        # SNR enhancement directly proportional to ACh level
        snr_enhancement = self.current_level

        return snr_enhancement

    def process_event(self, attention_demand: float, learning: bool) -> Dict:
        """
        Main processing: update ACh, compute modulations

        Parameters:
        -----------
        attention_demand : float
            Attention demand level (0-1)
        learning : bool
            Whether in learning context (True) or not (False)

        Returns:
        --------
        result : Dict
            {
                "ach_level": float,
                "attention_gain": float,
                "encoding_strength": float,
                "learning_rate_modulation": float,
                "snr_enhancement": float
            }
        """
        # 1. Update ACh level
        self.update_level(attention_demand, learning)

        # 2. Compute attention gain (using mid-relevance baseline)
        attention_gain = self.compute_attention_gain(stimulus_relevance=0.5)

        # 3. Compute encoding strength (using mid-strength baseline)
        encoding_strength = self.compute_encoding_strength(base_strength=0.5)

        # 4. Compute learning rate modulation (using baseline LR=0.1)
        learning_rate_modulation = self.compute_learning_rate_modulation(base_lr=0.1)

        # 5. Compute SNR enhancement
        snr_enhancement = self.compute_snr_enhancement()

        # 6. Update event counter
        self.total_events += 1

        # 7. Return complete result
        return {
            "ach_level": float(self.current_level),
            "attention_gain": float(attention_gain),
            "encoding_strength": float(encoding_strength),
            "learning_rate_modulation": float(learning_rate_modulation),
            "snr_enhancement": float(snr_enhancement)
        }

    def get_state(self) -> Dict:
        """
        Get current acetylcholine system state

        Returns:
        --------
        state : Dict
            {
                "ach_level": float,
                "level_history": List[float],
                "level_mean": float,
                "attention_gain": float,
                "encoding_strength": float,
                "learning_rate_modulation": float,
                "snr_enhancement": float,
                "total_events": int
            }
        """
        # Current level
        ach_level = self.current_level

        # Level statistics
        level_mean = np.mean(self.level_history) if self.level_history else self.baseline_level

        # Current modulations (using baseline values)
        attention_gain = self.compute_attention_gain(stimulus_relevance=0.5)
        encoding_strength = self.compute_encoding_strength(base_strength=0.5)
        learning_rate_modulation = self.compute_learning_rate_modulation(base_lr=0.1)
        snr_enhancement = self.compute_snr_enhancement()

        return {
            "ach_level": float(ach_level),
            "level_history": self.level_history.copy(),
            "level_mean": float(level_mean),
            "attention_gain": float(attention_gain),
            "encoding_strength": float(encoding_strength),
            "learning_rate_modulation": float(learning_rate_modulation),
            "snr_enhancement": float(snr_enhancement),
            "total_events": int(self.total_events)
        }
