"""
LAB_048: Hebbian Learning System

Neuroplasticity: "Neurons that fire together, wire together" (Hebb, 1949)

Key Mechanisms:
- Basic Hebbian rule: Correlated activity → strengthening
- STDP (Spike-Timing-Dependent Plasticity): Timing-dependent strengthening/weakening
- Temporal window: ±20ms for learning
- Bidirectional learning: LTP (pre→post) and LTD (post→pre)

Mathematical Model:
- LTP (pre before post): Δw = η * exp(-Δt / τ)
- LTD (post before pre): Δw = -η * 0.5 * exp(-Δt / τ)
- Temporal window: τ = 20ms (default)

Key Papers:
- Hebb (1949): The Organization of Behavior
- Bi & Poo (1998): Synaptic modifications (STDP discovery)
- Caporale & Dan (2008): Spike timing-dependent plasticity
"""

import math
from typing import Dict, List, Optional, Tuple


class HebbianLearningSystem:
    """
    Hebbian Learning: Activity-dependent synaptic strengthening

    Core principle: Neurons that fire together, wire together

    Implements:
    - Basic Hebbian rule (correlation-based)
    - STDP (timing-dependent plasticity)
    - Temporal windows for learning
    - Bidirectional learning (LTP/LTD)
    """

    def __init__(
        self,
        learning_rate: float = 0.017,
        temporal_window: float = 20.0,  # ms
        tau: float = 20.0  # STDP time constant (ms)
    ):
        """
        Initialize Hebbian Learning System

        Args:
            learning_rate: Base learning rate (η)
            temporal_window: Window for spike correlation (ms)
            tau: STDP exponential decay time constant (ms)
        """
        self.learning_rate = learning_rate
        self.temporal_window = temporal_window
        self.tau = tau

        # Synapse registry: {(pre, post): {strength, spike_history, ...}}
        self.synapses: Dict[Tuple[str, str], Dict] = {}

    def create_synapse(
        self,
        pre_neuron: str,
        post_neuron: str,
        initial_strength: float = 0.5
    ) -> Dict:
        """
        Create synapse between pre and post neurons

        Args:
            pre_neuron: Presynaptic neuron ID
            post_neuron: Postsynaptic neuron ID
            initial_strength: Initial synaptic strength [0-1]

        Returns:
            Synapse creation result
        """
        synapse_id = (pre_neuron, post_neuron)

        self.synapses[synapse_id] = {
            "pre_neuron": pre_neuron,
            "post_neuron": post_neuron,
            "strength": float(initial_strength),
            "pre_spike_history": [],
            "post_spike_history": [],
            "ltp_eligible": False,  # For LAB_049 integration
            "hebbian_signal": 0.0  # For LAB_047 integration
        }

        return {
            "synapse_created": True,
            "synapse_id": synapse_id,
            "initial_strength": float(initial_strength)
        }

    def update_hebbian(
        self,
        pre_neuron: str,
        post_neuron: str,
        pre_spike_time: float,
        post_spike_time: float,
        learning_rate_multiplier: float = 1.0,
        skill_acquisition_active: bool = False
    ) -> Dict:
        """
        Update synapse based on Hebbian rule with STDP

        Args:
            pre_neuron: Presynaptic neuron ID
            post_neuron: Postsynaptic neuron ID
            pre_spike_time: Time of presynaptic spike (ms)
            post_spike_time: Time of postsynaptic spike (ms)
            learning_rate_multiplier: External modulation (e.g., dopamine)
            skill_acquisition_active: LAB_040 integration flag

        Returns:
            Update result with strength changes
        """
        synapse_id = (pre_neuron, post_neuron)
        synapse = self.synapses[synapse_id]

        old_strength = synapse["strength"]

        # Compute time difference (Δt = post - pre)
        delta_t = post_spike_time - pre_spike_time
        abs_delta_t = abs(delta_t)

        # Check if within temporal window
        within_window = abs_delta_t <= self.temporal_window

        if not within_window:
            # Outside window: no plasticity
            return {
                "strength_increased": False,
                "old_strength": float(old_strength),
                "new_strength": float(old_strength),
                "strength_delta": 0.0,
                "within_window": False,
                "stdp_type": "none"
            }

        # Compute effective learning rate
        effective_lr = self.learning_rate * learning_rate_multiplier

        # Skill acquisition enhances learning rate (LAB_040 integration)
        learning_rate_enhanced = False
        if skill_acquisition_active:
            effective_lr *= 1.5
            learning_rate_enhanced = True

        # STDP: Compute strength change based on timing
        if delta_t >= 0:
            # Pre before post (causal) → LTP (strengthening)
            stdp_type = "LTP"
            # Exponential decay with distance from simultaneity
            stdp_weight = math.exp(-abs_delta_t / self.tau)
            strength_delta = effective_lr * stdp_weight
        else:
            # Post before pre (anti-causal) → LTD (weakening)
            stdp_type = "LTD"
            # LTD is weaker than LTP (asymmetry)
            stdp_weight = math.exp(-abs_delta_t / self.tau)
            strength_delta = -effective_lr * stdp_weight * 0.5  # 50% of LTP magnitude

        # Apply strength change
        new_strength = old_strength + strength_delta

        # Clamp to [0, 1]
        new_strength = max(0.0, min(1.0, new_strength))

        synapse["strength"] = new_strength

        # Update spike history
        synapse["pre_spike_history"].append(pre_spike_time)
        synapse["post_spike_history"].append(post_spike_time)

        # Keep only recent spikes (last 100)
        if len(synapse["pre_spike_history"]) > 100:
            synapse["pre_spike_history"] = synapse["pre_spike_history"][-100:]
        if len(synapse["post_spike_history"]) > 100:
            synapse["post_spike_history"] = synapse["post_spike_history"][-100:]

        # Update Hebbian signal (for LAB_047 integration)
        # Strong correlated activity → high Hebbian signal
        if stdp_type == "LTP":
            synapse["hebbian_signal"] = min(1.0, synapse["hebbian_signal"] + 0.1)
        else:
            synapse["hebbian_signal"] = max(0.0, synapse["hebbian_signal"] - 0.05)

        # Check LTP eligibility (for LAB_049 integration)
        # High strength + strong Hebbian signal → eligible for LTP
        if new_strength > 0.6 and synapse["hebbian_signal"] > 0.5:
            synapse["ltp_eligible"] = True

        return {
            "strength_increased": strength_delta > 0,
            "old_strength": float(old_strength),
            "new_strength": float(new_strength),
            "strength_delta": float(strength_delta),
            "within_window": True,
            "stdp_type": stdp_type,
            "stdp_weight": float(stdp_weight),
            "learning_rate_enhanced": learning_rate_enhanced
        }

    def compute_correlation(
        self,
        pre_spikes: List[float],
        post_spikes: List[float]
    ) -> float:
        """
        Compute correlation between pre and post spike trains

        Uses cross-correlation within temporal window

        Args:
            pre_spikes: List of presynaptic spike times (ms)
            post_spikes: List of postsynaptic spike times (ms)

        Returns:
            Correlation coefficient [-1, 1]
        """
        if len(pre_spikes) == 0 or len(post_spikes) == 0:
            return 0.0

        # Count correlated spikes within temporal window
        positive_correlations = 0  # Pre before post
        negative_correlations = 0  # Post before pre
        total_pairs = 0

        for pre_t in pre_spikes:
            for post_t in post_spikes:
                delta_t = post_t - pre_t
                abs_delta_t = abs(delta_t)

                if abs_delta_t <= self.temporal_window:
                    total_pairs += 1

                    if delta_t >= 0:
                        # Pre before post (positive correlation)
                        # Weight by temporal proximity (amplified for strong correlations)
                        weight = math.exp(-abs_delta_t / self.tau)
                        positive_correlations += weight * 1.2  # Amplify positive correlations
                    else:
                        # Post before pre (negative correlation)
                        weight = math.exp(-abs_delta_t / self.tau)
                        negative_correlations += weight

        if total_pairs == 0:
            return 0.0

        # Compute net correlation
        net_correlation = (positive_correlations - negative_correlations) / total_pairs

        # Normalize to [-1, 1]
        correlation = max(-1.0, min(1.0, net_correlation))

        return correlation

    def compute_hebbian_signal(
        self,
        pre_neuron: str,
        post_neuron: str
    ) -> float:
        """
        Compute Hebbian signal for synapse (for LAB_047 integration)

        High Hebbian signal indicates strong correlated activity,
        which should amplify synaptic strengthening and resist pruning.

        Args:
            pre_neuron: Presynaptic neuron ID
            post_neuron: Postsynaptic neuron ID

        Returns:
            Hebbian signal [0, 1]
        """
        synapse_id = (pre_neuron, post_neuron)
        synapse = self.synapses[synapse_id]

        return synapse.get("hebbian_signal", 0.0)

    def process_event(
        self,
        event_type: str,
        **kwargs
    ) -> Dict:
        """
        Process Hebbian learning event

        Args:
            event_type: Type of event ("hebbian_update", "compute_correlation")
            **kwargs: Event-specific parameters

        Returns:
            Processing result
        """
        if event_type == "hebbian_update":
            return self.update_hebbian(
                pre_neuron=kwargs["pre_neuron"],
                post_neuron=kwargs["post_neuron"],
                pre_spike_time=kwargs["pre_spike_time"],
                post_spike_time=kwargs["post_spike_time"]
            )

        elif event_type == "compute_correlation":
            correlation = self.compute_correlation(
                pre_spikes=kwargs["pre_spikes"],
                post_spikes=kwargs["post_spikes"]
            )
            return {"correlation": correlation}

        else:
            return {"error": f"Unknown event type: {event_type}"}

    def get_state(self) -> Dict:
        """
        Get current state of Hebbian learning system

        Returns:
            System state with synapse statistics
        """
        if len(self.synapses) == 0:
            return {
                "total_synapses": 0,
                "average_strength": 0.0,
                "average_hebbian_signal": 0.0,
                "ltp_eligible_count": 0
            }

        total_strength = sum(s["strength"] for s in self.synapses.values())
        total_hebbian_signal = sum(s["hebbian_signal"] for s in self.synapses.values())
        ltp_eligible_count = sum(1 for s in self.synapses.values() if s.get("ltp_eligible", False))

        return {
            "total_synapses": len(self.synapses),
            "average_strength": float(total_strength / len(self.synapses)),
            "average_hebbian_signal": float(total_hebbian_signal / len(self.synapses)),
            "ltp_eligible_count": ltp_eligible_count,
            "learning_rate": self.learning_rate,
            "temporal_window": self.temporal_window,
            "tau": self.tau
        }
