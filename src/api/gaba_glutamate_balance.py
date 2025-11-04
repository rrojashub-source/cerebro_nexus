"""
LAB_017: GABA/Glutamate Balance - Excitation/Inhibition Homeostasis

Implements E/I balance based on:
- Yizhar et al. (2011): Neocortical excitation/inhibition balance
- Haider et al. (2006): Balanced cortical states
- Dehghani et al. (2016): E/I balance and oscillations

Core Functions:
1. Excitation/inhibition (E/I) ratio regulation
2. Oscillation generation and control
3. Gain modulation (signal amplification)
4. Seizure prevention (runaway excitation)
5. Homeostatic plasticity

Neuroscience Foundation:
- Glutamate: Primary excitatory neurotransmitter
- GABA: Primary inhibitory neurotransmitter
- Cortex: Delicate E/I balance required for function
- Hippocampus: Oscillations (theta, gamma) from E/I dynamics

Critical Balance:
- Balanced E/I → normal cognition, stable oscillations
- High E/Low I → hyperexcitability, seizures
- Low E/High I → hypoactivity, slow cognition
"""

import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import numpy as np
from enum import Enum
import warnings


class EIState(Enum):
    """E/I balance state"""
    HYPOACTIVE = "hypoactive"        # Too much inhibition
    BALANCED = "balanced"             # Healthy E/I ratio
    HYPERACTIVE = "hyperactive"       # Too much excitation
    SEIZURE_RISK = "seizure_risk"    # Critically high excitation


class OscillationBand(Enum):
    """Neural oscillation frequency bands"""
    DELTA = "delta"      # 0.5-4 Hz (deep sleep)
    THETA = "theta"      # 4-8 Hz (memory, navigation)
    ALPHA = "alpha"      # 8-13 Hz (relaxed awareness)
    BETA = "beta"        # 13-30 Hz (active thinking)
    GAMMA = "gamma"      # 30-100 Hz (binding, attention)


@dataclass
class EISignal:
    """E/I balance event"""
    timestamp: float
    glutamate_level: float  # Excitation (0-1)
    gaba_level: float       # Inhibition (0-1)
    ei_ratio: float         # E/I ratio
    state: EIState
    oscillation_power: Dict[str, float]  # Power in each band


@dataclass
class OscillationState:
    """Current oscillatory state"""
    dominant_band: OscillationBand
    frequency: float  # Hz
    amplitude: float
    coherence: float  # 0-1


@dataclass
class HomeostasisEvent:
    """Homeostatic regulation event"""
    timestamp: float
    trigger: str
    adjustment_type: str  # "increase_inhibition", "increase_excitation"
    magnitude: float


class OscillationGenerator:
    """
    Generates oscillations from E/I dynamics.

    E/I interactions produce rhythms:
    - Gamma (30-100 Hz): Fast E-I loops
    - Theta (4-8 Hz): Slower E-I cycles
    - Alpha (8-13 Hz): Inhibitory dominance
    """

    def __init__(self):
        self.oscillation_history: deque = deque(maxlen=1000)

    def compute_oscillation_power(
        self,
        glutamate: float,
        gaba: float,
        ei_ratio: float
    ) -> Dict[str, float]:
        """
        Compute power in different frequency bands based on E/I.

        Balanced E/I → strong gamma
        High I → strong alpha
        Moderate E/I → theta
        """
        powers = {}

        # Gamma (30-100 Hz): Peaks at balanced E/I
        # Strong E and I together → fast oscillations
        gamma_power = glutamate * gaba * 4.0
        gamma_power = min(1.0, gamma_power)
        powers["gamma"] = gamma_power

        # Beta (13-30 Hz): Active processing
        # Moderate E, moderate I
        beta_power = min(glutamate, gaba) * 1.5
        beta_power = min(1.0, beta_power)
        powers["beta"] = beta_power

        # Alpha (8-13 Hz): Inhibitory dominance
        # High GABA, moderate glutamate
        alpha_power = gaba * (1.0 - abs(ei_ratio - 0.8))
        alpha_power = min(1.0, alpha_power)
        powers["alpha"] = alpha_power

        # Theta (4-8 Hz): Moderate, balanced
        # E/I ratio near 1.0
        theta_power = 1.0 - abs(ei_ratio - 1.0)
        theta_power = min(1.0, theta_power * 0.7)
        powers["theta"] = theta_power

        # Delta (0.5-4 Hz): Low activity
        # Low E and I
        delta_power = (1.0 - glutamate) * (1.0 - gaba) * 0.5
        powers["delta"] = delta_power

        return powers

    def determine_dominant_band(self, powers: Dict[str, float]) -> Tuple[OscillationBand, float]:
        """Find dominant oscillation band"""
        max_band = max(powers.items(), key=lambda x: x[1])

        band_map = {
            "delta": OscillationBand.DELTA,
            "theta": OscillationBand.THETA,
            "alpha": OscillationBand.ALPHA,
            "beta": OscillationBand.BETA,
            "gamma": OscillationBand.GAMMA,
        }

        return band_map[max_band[0]], max_band[1]

    def compute_oscillation_coherence(self, powers: Dict[str, float]) -> float:
        """
        Compute coherence (how organized/synchronized oscillations are).

        High coherence → one dominant band
        Low coherence → noisy, mixed frequencies
        """
        # Normalized entropy measure
        total_power = sum(powers.values())

        if total_power == 0:
            return 0.0

        # Shannon entropy
        entropy = 0.0
        for power in powers.values():
            if power > 0:
                p = power / total_power
                entropy -= p * np.log2(p)

        # Max entropy for 5 bands
        max_entropy = np.log2(5)

        # Coherence = 1 - normalized_entropy
        coherence = 1.0 - (entropy / max_entropy)

        return coherence


class HomeostaticController:
    """
    Maintains E/I homeostasis through compensatory mechanisms.

    Too much E → upregulate GABA receptors, increase inhibition
    Too much I → upregulate AMPA receptors, increase excitation
    """

    def __init__(
        self,
        target_ei_ratio: float = 1.0,
        tolerance: float = 0.3
    ):
        self.target_ei_ratio = target_ei_ratio
        self.tolerance = tolerance

        self.homeostasis_history: deque = deque(maxlen=500)

        # Receptor sensitivity (homeostatic scaling)
        self.gaba_sensitivity = 1.0
        self.glutamate_sensitivity = 1.0

    def check_balance(self, ei_ratio: float) -> Tuple[bool, Optional[str]]:
        """
        Check if E/I is within acceptable range.

        Returns (is_balanced, corrective_action_needed)
        """
        deviation = abs(ei_ratio - self.target_ei_ratio)

        if deviation <= self.tolerance:
            return True, None

        # Determine corrective action
        if ei_ratio > self.target_ei_ratio + self.tolerance:
            # Too much excitation
            return False, "increase_inhibition"
        else:
            # Too much inhibition
            return False, "increase_excitation"

    def apply_homeostatic_correction(
        self,
        action: str,
        magnitude: float = 0.1
    ) -> HomeostasisEvent:
        """
        Apply homeostatic adjustment.

        This simulates long-term plasticity that maintains balance.
        """
        if action == "increase_inhibition":
            # Upregulate GABA receptors → more sensitive to inhibition
            self.gaba_sensitivity += magnitude
            self.gaba_sensitivity = min(2.0, self.gaba_sensitivity)

            # Downregulate glutamate receptors
            self.glutamate_sensitivity -= magnitude * 0.5
            self.glutamate_sensitivity = max(0.5, self.glutamate_sensitivity)

        elif action == "increase_excitation":
            # Upregulate glutamate receptors
            self.glutamate_sensitivity += magnitude
            self.glutamate_sensitivity = min(2.0, self.glutamate_sensitivity)

            # Downregulate GABA receptors
            self.gaba_sensitivity -= magnitude * 0.5
            self.gaba_sensitivity = max(0.5, self.gaba_sensitivity)

        event = HomeostasisEvent(
            timestamp=time.time(),
            trigger=action,
            adjustment_type=action,
            magnitude=magnitude
        )

        self.homeostasis_history.append(event)

        return event

    def apply_sensitivity(
        self,
        glutamate_raw: float,
        gaba_raw: float
    ) -> Tuple[float, float]:
        """
        Apply receptor sensitivity to raw neurotransmitter levels.

        Returns effective levels after homeostatic scaling.
        """
        effective_glu = glutamate_raw * self.glutamate_sensitivity
        effective_gaba = gaba_raw * self.gaba_sensitivity

        # Bounded 0-1
        effective_glu = min(1.0, effective_glu)
        effective_gaba = min(1.0, effective_gaba)

        return effective_glu, effective_gaba


class GABAGlutamateSystem:
    """
    Main LAB_017 implementation.

    Manages E/I balance including:
    - Glutamate (excitation) and GABA (inhibition) levels
    - E/I ratio monitoring and regulation
    - Oscillation generation
    - Homeostatic plasticity
    - Seizure prevention
    """

    def __init__(
        self,
        baseline_glutamate: float = 0.5,
        baseline_gaba: float = 0.5,
        seizure_threshold: float = 3.0
    ):
        # Core parameters
        self.baseline_glutamate = baseline_glutamate
        self.baseline_gaba = baseline_gaba
        self.seizure_threshold = seizure_threshold

        # Current state
        self.current_glutamate = baseline_glutamate
        self.current_gaba = baseline_gaba
        self.current_ei_ratio = baseline_glutamate / baseline_gaba if baseline_gaba > 0 else 1.0
        self.current_state = EIState.BALANCED
        self.last_update_time = time.time()

        # Components
        self.oscillation_generator = OscillationGenerator()
        self.homeostatic_controller = HomeostaticController()

        # History
        self.signal_history: deque = deque(maxlen=1000)

        # Statistics
        self.total_homeostatic_corrections = 0
        self.time_in_balance = 0.0
        self.time_imbalanced = 0.0
        self.last_state_change = time.time()

    def process_excitatory_input(self, magnitude: float) -> EISignal:
        """
        Process excitatory input (glutamate release).

        Increases network excitation.
        """
        # Add glutamate
        self.current_glutamate += magnitude
        self.current_glutamate = min(1.0, self.current_glutamate)

        return self._update_state("excitatory_input")

    def process_inhibitory_input(self, magnitude: float) -> EISignal:
        """
        Process inhibitory input (GABA release).

        Increases network inhibition.
        """
        # Add GABA
        self.current_gaba += magnitude
        self.current_gaba = min(1.0, self.current_gaba)

        return self._update_state("inhibitory_input")

    def process_cognitive_load(self, load: float) -> EISignal:
        """
        Process cognitive load.

        High load → increase excitation (active processing)
        Also triggers compensatory inhibition
        """
        # Glutamate increases with load
        glu_increase = load * 0.5

        # GABA increases proportionally (homeostatic response)
        gaba_increase = load * 0.4

        self.current_glutamate += glu_increase
        self.current_gaba += gaba_increase

        # Bounded
        self.current_glutamate = min(1.0, self.current_glutamate)
        self.current_gaba = min(1.0, self.current_gaba)

        return self._update_state("cognitive_load")

    def _update_state(self, source: str) -> EISignal:
        """
        Update E/I state after changes.

        Computes E/I ratio, checks balance, generates oscillations.
        """
        # Apply homeostatic sensitivity
        effective_glu, effective_gaba = self.homeostatic_controller.apply_sensitivity(
            self.current_glutamate,
            self.current_gaba
        )

        # Compute E/I ratio
        if effective_gaba > 0:
            ei_ratio = effective_glu / effective_gaba
        else:
            ei_ratio = 10.0  # Very high (all excitation, no inhibition)

        self.current_ei_ratio = ei_ratio

        # Determine state
        if ei_ratio >= self.seizure_threshold:
            new_state = EIState.SEIZURE_RISK
            warnings.warn("⚠️ SEIZURE RISK: E/I ratio critically high!")
        elif ei_ratio > 1.5:
            new_state = EIState.HYPERACTIVE
        elif ei_ratio < 0.5:
            new_state = EIState.HYPOACTIVE
        else:
            new_state = EIState.BALANCED

        # Track time in each state
        if new_state != self.current_state:
            elapsed = time.time() - self.last_state_change

            if self.current_state == EIState.BALANCED:
                self.time_in_balance += elapsed
            else:
                self.time_imbalanced += elapsed

            self.last_state_change = time.time()

        self.current_state = new_state

        # Check if homeostatic correction needed
        is_balanced, action = self.homeostatic_controller.check_balance(ei_ratio)

        if not is_balanced and action:
            self.homeostatic_controller.apply_homeostatic_correction(action, magnitude=0.05)
            self.total_homeostatic_corrections += 1

        # Generate oscillations
        oscillation_powers = self.oscillation_generator.compute_oscillation_power(
            effective_glu,
            effective_gaba,
            ei_ratio
        )

        # Create signal
        signal = EISignal(
            timestamp=time.time(),
            glutamate_level=effective_glu,
            gaba_level=effective_gaba,
            ei_ratio=ei_ratio,
            state=new_state,
            oscillation_power=oscillation_powers
        )

        self.signal_history.append(signal)
        self.last_update_time = time.time()

        return signal

    def decay_activity(self):
        """
        Natural decay of glutamate and GABA back to baseline.

        Called periodically (e.g., during rest).
        """
        decay_rate = 0.1

        # Decay toward baseline
        self.current_glutamate += (self.baseline_glutamate - self.current_glutamate) * decay_rate
        self.current_gaba += (self.baseline_gaba - self.current_gaba) * decay_rate

    def get_gain_modulation(self) -> float:
        """
        Get current gain (signal amplification).

        Balanced E/I → optimal gain
        Imbalanced → poor gain control
        """
        # Gain is best when balanced (E/I ratio near 1.0)
        deviation = abs(self.current_ei_ratio - 1.0)

        # Gaussian-like: peak at 1.0, drops off with deviation
        gain = np.exp(-(deviation ** 2) / 0.5)

        return gain

    def get_oscillation_state(self) -> OscillationState:
        """Get current oscillatory state"""
        if not self.signal_history:
            return OscillationState(
                dominant_band=OscillationBand.THETA,
                frequency=6.0,
                amplitude=0.0,
                coherence=0.0
            )

        latest_signal = self.signal_history[-1]
        powers = latest_signal.oscillation_power

        dominant_band, amplitude = self.oscillation_generator.determine_dominant_band(powers)
        coherence = self.oscillation_generator.compute_oscillation_coherence(powers)

        # Map band to center frequency
        freq_map = {
            OscillationBand.DELTA: 2.0,
            OscillationBand.THETA: 6.0,
            OscillationBand.ALPHA: 10.0,
            OscillationBand.BETA: 20.0,
            OscillationBand.GAMMA: 40.0,
        }

        return OscillationState(
            dominant_band=dominant_band,
            frequency=freq_map[dominant_band],
            amplitude=amplitude,
            coherence=coherence
        )

    def get_statistics(self) -> Dict:
        """Get comprehensive system statistics"""
        osc_state = self.get_oscillation_state()

        total_time = self.time_in_balance + self.time_imbalanced
        balance_ratio = (self.time_in_balance / total_time) if total_time > 0 else 0.5

        return {
            "glutamate_level": self.current_glutamate,
            "gaba_level": self.current_gaba,
            "ei_ratio": self.current_ei_ratio,
            "ei_state": self.current_state.value,
            "gain_modulation": self.get_gain_modulation(),
            "dominant_oscillation": osc_state.dominant_band.value,
            "oscillation_frequency": osc_state.frequency,
            "oscillation_amplitude": osc_state.amplitude,
            "oscillation_coherence": osc_state.coherence,
            "total_homeostatic_corrections": self.total_homeostatic_corrections,
            "time_in_balance_ratio": balance_ratio,
            "glutamate_sensitivity": self.homeostatic_controller.glutamate_sensitivity,
            "gaba_sensitivity": self.homeostatic_controller.gaba_sensitivity,
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_017: GABA/Glutamate Balance - Test")
    print("=" * 60)

    # Create E/I system
    ei_system = GABAGlutamateSystem(
        baseline_glutamate=0.5,
        baseline_gaba=0.5,
        seizure_threshold=3.0
    )

    print("\n📊 Initial State:")
    stats = ei_system.get_statistics()
    print(f"  Glutamate: {stats['glutamate_level']:.3f}")
    print(f"  GABA: {stats['gaba_level']:.3f}")
    print(f"  E/I Ratio: {stats['ei_ratio']:.3f}")
    print(f"  State: {stats['ei_state']}")
    print(f"  Dominant Oscillation: {stats['dominant_oscillation']} @ {stats['oscillation_frequency']:.1f} Hz")

    # Scenario 1: Moderate cognitive load (balanced)
    print("\n🧠 Processing moderate cognitive load...")
    signal = ei_system.process_cognitive_load(load=0.6)
    print(f"  Glutamate: {signal.glutamate_level:.3f}")
    print(f"  GABA: {signal.gaba_level:.3f}")
    print(f"  E/I Ratio: {signal.ei_ratio:.3f}")
    print(f"  State: {signal.state.value}")

    osc_state = ei_system.get_oscillation_state()
    print(f"  Oscillation: {osc_state.dominant_band.value} ({osc_state.frequency:.1f} Hz)")
    print(f"  Power: {osc_state.amplitude:.3f}, Coherence: {osc_state.coherence:.3f}")

    # Scenario 2: Strong excitatory input (imbalance)
    print("\n⚡ Strong excitatory input (creating imbalance)...")
    signal = ei_system.process_excitatory_input(magnitude=0.5)
    print(f"  Glutamate: {signal.glutamate_level:.3f}")
    print(f"  GABA: {signal.gaba_level:.3f}")
    print(f"  E/I Ratio: {signal.ei_ratio:.3f}")
    print(f"  State: {signal.state.value}")
    print(f"  Gain: {ei_system.get_gain_modulation():.3f}")

    # Scenario 3: Homeostatic correction
    print("\n🔄 Homeostatic correction (automatic)...")
    # Process another imbalanced input
    signal = ei_system.process_excitatory_input(magnitude=0.3)
    stats = ei_system.get_statistics()
    print(f"  Homeostatic Corrections: {stats['total_homeostatic_corrections']}")
    print(f"  GABA Sensitivity: {stats['gaba_sensitivity']:.3f} (upregulated)")
    print(f"  Glutamate Sensitivity: {stats['glutamate_sensitivity']:.3f}")

    # Scenario 4: Compensatory inhibition
    print("\n🛡️ Adding compensatory inhibition...")
    signal = ei_system.process_inhibitory_input(magnitude=0.4)
    print(f"  E/I Ratio: {signal.ei_ratio:.3f} (restored toward balance)")
    print(f"  State: {signal.state.value}")

    # Scenario 5: Natural decay
    print("\n⏳ Natural decay (rest period)...")
    for _ in range(10):
        ei_system.decay_activity()
    print(f"  Glutamate: {ei_system.current_glutamate:.3f} (decaying)")
    print(f"  GABA: {ei_system.current_gaba:.3f} (decaying)")

    # Show final statistics
    print("\n📈 Final Statistics:")
    stats = ei_system.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

    print("\n✅ LAB_017 Test Complete!")
