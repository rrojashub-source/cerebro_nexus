"""
LAB_049: Long-Term Potentiation (LTP) System

Neuroplasticity: "The cellular basis of learning and memory"

Key Mechanisms:
- LTP induction: High-frequency stimulation (tetanus, 100 Hz)
- E-LTP (Early-phase): 1-3 hours, no protein synthesis required
- L-LTP (Late-phase): >3 hours, requires protein synthesis
- LTD (Long-Term Depression): Low-frequency stimulation (1 Hz)
- Cooperativity: Multiple inputs can cooperate
- Associativity: Weak + strong inputs potentiated together
- Input specificity: Only stimulated pathways potentiated

Mathematical Model:
- LTP magnitude: Δw = η * f(frequency) * f(duration) * f(Hebbian)
- E-LTP decay: exp(-t / τ_early) where τ_early = 2 hours
- L-LTP decay: exp(-t / τ_late) where τ_late = 24 hours
- LTD magnitude: Δw = -η * f(frequency) * f(duration)

Key Papers:
- Bliss & Lømo (1973): Long-lasting potentiation
- Malenka & Bear (2004): LTP and LTD mechanisms
- Lynch (2004): LTP and memory
"""

import math
from typing import Dict, List, Optional, Tuple


class LTPSystem:
    """
    Long-Term Potentiation: Persistent synaptic strengthening

    Core principle: High-frequency activity → lasting potentiation

    Implements:
    - LTP induction (tetanus protocols)
    - E-LTP vs L-LTP (phase-dependent persistence)
    - LTD (long-term depression)
    - Cooperativity and associativity
    """

    def __init__(
        self,
        ltp_threshold: float = 0.7,
        ltp_duration_hours: float = 24.0,
        ltp_magnitude: float = 0.5,
        ltd_magnitude: float = 0.2
    ):
        """
        Initialize LTP System

        Args:
            ltp_threshold: Minimum strength for LTP induction
            ltp_duration_hours: Default LTP persistence (hours)
            ltp_magnitude: Magnitude of LTP effect
            ltd_magnitude: Magnitude of LTD effect
        """
        self.ltp_threshold = ltp_threshold
        self.ltp_duration_hours = ltp_duration_hours
        self.ltp_magnitude = ltp_magnitude
        self.ltd_magnitude = ltd_magnitude

        # Synapse registry
        self.synapses: Dict[Tuple[str, str], Dict] = {}

        # Phase-specific decay constants (hours)
        self.tau_early_ltp = 2.0  # E-LTP decays in ~2 hours
        self.tau_late_ltp = 120.0  # L-LTP decays in ~120 hours (5 days)

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
            "ltp_potentiated": False,
            "ltp_phase": None,  # "early" or "late"
            "ltp_strength": 0.0,  # Additional strength from LTP
            "ltp_duration_hours": 0.0,
            "ltd_active": False,
            "resists_pruning": False  # For LAB_047 integration
        }

        return {
            "synapse_created": True,
            "synapse_id": synapse_id,
            "initial_strength": float(initial_strength)
        }

    def induce_ltp(
        self,
        pre_neuron: str,
        post_neuron: str,
        stimulation_frequency: float,  # Hz
        stimulation_duration: float,  # seconds
        hebbian_signal: Optional[float] = None,
        skill_acquisition_active: bool = False,
        ignore_weak_threshold: bool = False
    ) -> Dict:
        """
        Induce LTP through high-frequency stimulation

        Args:
            pre_neuron: Presynaptic neuron ID
            post_neuron: Postsynaptic neuron ID
            stimulation_frequency: Stimulation frequency (Hz)
            stimulation_duration: Stimulation duration (seconds)
            hebbian_signal: LAB_048 integration (facilitates LTP)
            skill_acquisition_active: LAB_040 integration flag

        Returns:
            LTP induction result
        """
        synapse_id = (pre_neuron, post_neuron)
        synapse = self.synapses[synapse_id]

        # Check if LTD is active (prevents LTP)
        if synapse.get("ltd_active", False):
            return {
                "ltp_induced": False,
                "reason": "LTD active, prevents LTP",
                "ltp_magnitude": 0.0
            }

        # Compute effective threshold (modulated by external factors)
        effective_threshold = self.ltp_threshold

        # Hebbian signal lowers threshold (LAB_048 integration)
        threshold_modulated = False
        if hebbian_signal is not None and hebbian_signal > 0.6:
            effective_threshold *= 0.8  # 20% reduction
            threshold_modulated = True

        # Skill acquisition lowers threshold (LAB_040 integration)
        if skill_acquisition_active:
            effective_threshold *= 0.85
            threshold_modulated = True

        # Check if stimulation is strong enough for LTP
        # High-frequency (>50 Hz) and sufficient duration (>0.5s)
        if stimulation_frequency < 50.0:
            return {
                "ltp_induced": False,
                "reason": "Frequency too low",
                "ltp_magnitude": 0.0,
                "threshold_modulated": threshold_modulated
            }

        if stimulation_duration < 0.5:
            return {
                "ltp_induced": False,
                "reason": "Duration too short",
                "ltp_magnitude": 0.0,
                "threshold_modulated": threshold_modulated
            }

        # Check if synapse meets strength threshold
        # (weak synapses harder to potentiate)
        # Exception: Associative LTP allows weak inputs
        if not ignore_weak_threshold and synapse["strength"] <= 0.3:
            return {
                "ltp_induced": False,
                "reason": "Synapse too weak",
                "ltp_magnitude": 0.0,
                "threshold_modulated": threshold_modulated
            }

        # Compute LTP magnitude (frequency and duration dependent)
        frequency_factor = min(1.0, stimulation_frequency / 100.0)  # Normalize to 100 Hz
        duration_factor = min(1.0, stimulation_duration / 1.0)  # Normalize to 1 second
        hebbian_factor = 1.0 + (hebbian_signal if hebbian_signal else 0.0) * 0.5

        ltp_magnitude = self.ltp_magnitude * frequency_factor * duration_factor * hebbian_factor

        # Apply LTP
        synapse["ltp_potentiated"] = True
        synapse["ltp_phase"] = "early"  # Default to E-LTP
        synapse["ltp_strength"] = ltp_magnitude
        synapse["ltp_duration_hours"] = 2.0  # E-LTP: 2 hours
        synapse["strength"] = min(1.0, synapse["strength"] + ltp_magnitude)
        synapse["resists_pruning"] = True  # LAB_047 integration

        return {
            "ltp_induced": True,
            "ltp_magnitude": float(ltp_magnitude),
            "ltp_phase": "early",
            "threshold_modulated": threshold_modulated
        }

    def apply_tetanus(
        self,
        pre_neuron: str,
        post_neuron: str,
        protocol: str = "single",
        protein_synthesis: bool = False
    ) -> Dict:
        """
        Apply tetanus protocol (standard LTP induction)

        Args:
            pre_neuron: Presynaptic neuron ID
            post_neuron: Postsynaptic neuron ID
            protocol: "single" (E-LTP) or "spaced" (L-LTP potential)
            protein_synthesis: Enable protein synthesis (required for L-LTP)

        Returns:
            Tetanus result
        """
        synapse_id = (pre_neuron, post_neuron)
        synapse = self.synapses[synapse_id]

        # Single tetanus: 100 Hz, 1 second → E-LTP
        if protocol == "single":
            result = self.induce_ltp(pre_neuron, post_neuron, 100.0, 1.0)
            return result

        # Spaced tetanus: Multiple bursts → potential for L-LTP
        elif protocol == "spaced":
            # Apply multiple tetani
            result = self.induce_ltp(pre_neuron, post_neuron, 100.0, 1.0)

            if result["ltp_induced"] and protein_synthesis:
                # Transition to L-LTP (requires protein synthesis)
                synapse["ltp_phase"] = "late"
                synapse["ltp_duration_hours"] = 24.0  # L-LTP: 24+ hours
                synapse["ltp_strength"] *= 1.5  # L-LTP is stronger
                synapse["strength"] = min(1.0, synapse["strength"] + synapse["ltp_strength"] * 0.3)

                return {
                    "ltp_induced": True,
                    "ltp_phase": "late",
                    "ltp_magnitude": float(synapse["ltp_strength"]),
                    "protein_synthesis_enabled": True
                }

            return result

        else:
            return {"error": f"Unknown protocol: {protocol}"}

    def induce_ltd(
        self,
        pre_neuron: str,
        post_neuron: str,
        stimulation_frequency: float,
        stimulation_duration: float
    ) -> Dict:
        """
        Induce LTD through low-frequency stimulation

        Args:
            pre_neuron: Presynaptic neuron ID
            post_neuron: Postsynaptic neuron ID
            stimulation_frequency: Stimulation frequency (Hz, typically 1 Hz)
            stimulation_duration: Stimulation duration (seconds, typically 15 min)

        Returns:
            LTD induction result
        """
        synapse_id = (pre_neuron, post_neuron)
        synapse = self.synapses[synapse_id]

        # Check if low-frequency (1-3 Hz) and long duration (>10 min)
        if stimulation_frequency > 3.0:
            return {
                "ltd_induced": False,
                "reason": "Frequency too high for LTD"
            }

        if stimulation_duration < 10.0:  # 10 minutes (assuming duration in minutes)
            return {
                "ltd_induced": False,
                "reason": "Duration too short for LTD"
            }

        # Compute LTD magnitude
        ltd_magnitude = self.ltd_magnitude

        # Apply LTD (weakening)
        synapse["ltd_active"] = True
        synapse["strength"] = max(0.0, synapse["strength"] - ltd_magnitude)

        # LTD prevents LTP induction
        synapse["ltp_potentiated"] = False
        synapse["ltp_phase"] = None

        return {
            "ltd_induced": True,
            "ltd_magnitude": float(ltd_magnitude),
            "new_strength": float(synapse["strength"])
        }

    def apply_decay(
        self,
        hours: float
    ) -> Dict:
        """
        Apply time-based decay to LTP/LTD

        Args:
            hours: Hours elapsed

        Returns:
            Decay result
        """
        for synapse_id, synapse in self.synapses.items():
            if synapse["ltp_potentiated"]:
                # Determine decay constant based on phase
                if synapse["ltp_phase"] == "early":
                    tau = self.tau_early_ltp  # 2 hours
                else:  # "late"
                    tau = self.tau_late_ltp  # 24 hours

                # Exponential decay
                decay_factor = math.exp(-hours / tau)
                synapse["ltp_strength"] *= decay_factor

                # Remove LTP if strength drops below threshold
                if synapse["ltp_strength"] < 0.1:
                    synapse["ltp_potentiated"] = False
                    synapse["ltp_phase"] = None
                    synapse["resists_pruning"] = False

            if synapse["ltd_active"]:
                # LTD decays over ~6 hours
                decay_factor = math.exp(-hours / 6.0)
                if decay_factor < 0.1:
                    synapse["ltd_active"] = False

        return {
            "hours_decayed": hours,
            "synapses_affected": len(self.synapses)
        }

    def induce_ltp_cooperative(
        self,
        pre_neurons: List[str],
        post_neuron: str,
        stimulation_frequency: float,
        stimulation_duration: float
    ) -> Dict:
        """
        Cooperative LTP: Multiple weak inputs cooperate to induce LTP

        Args:
            pre_neurons: List of presynaptic neuron IDs
            post_neuron: Postsynaptic neuron ID
            stimulation_frequency: Stimulation frequency (Hz)
            stimulation_duration: Stimulation duration (seconds)

        Returns:
            Cooperative LTP result
        """
        # Compute combined strength of all inputs
        combined_strength = sum(
            self.synapses[(pre, post_neuron)]["strength"]
            for pre in pre_neurons
            if (pre, post_neuron) in self.synapses
        )

        # If combined strength exceeds threshold, induce LTP in all
        if combined_strength > self.ltp_threshold:
            for pre in pre_neurons:
                if (pre, post_neuron) in self.synapses:
                    self.induce_ltp(pre, post_neuron, stimulation_frequency, stimulation_duration)

            return {
                "ltp_induced": True,
                "cooperative": True,
                "combined_strength": float(combined_strength),
                "num_inputs": len(pre_neurons)
            }
        else:
            return {
                "ltp_induced": False,
                "reason": "Combined strength below threshold",
                "combined_strength": float(combined_strength)
            }

    def induce_ltp_associative(
        self,
        weak_pre: str,
        strong_pre: str,
        post_neuron: str,
        stimulation_frequency: float,
        stimulation_duration: float
    ) -> Dict:
        """
        Associative LTP: Weak input paired with strong input → both potentiated

        Args:
            weak_pre: Weak presynaptic neuron ID
            strong_pre: Strong presynaptic neuron ID
            post_neuron: Postsynaptic neuron ID
            stimulation_frequency: Stimulation frequency (Hz)
            stimulation_duration: Stimulation duration (seconds)

        Returns:
            Associative LTP result
        """
        weak_synapse_id = (weak_pre, post_neuron)
        strong_synapse_id = (strong_pre, post_neuron)

        weak_synapse = self.synapses[weak_synapse_id]
        strong_synapse = self.synapses[strong_synapse_id]

        # Strong input drives postsynaptic depolarization
        if strong_synapse["strength"] > 0.6:
            # Weak input can "piggyback" on strong input (ignore weak threshold)
            result_weak = self.induce_ltp(weak_pre, post_neuron, stimulation_frequency, stimulation_duration, ignore_weak_threshold=True)
            result_strong = self.induce_ltp(strong_pre, post_neuron, stimulation_frequency, stimulation_duration)

            return {
                "ltp_induced": True,
                "associative": True,
                "weak_input_potentiated": result_weak["ltp_induced"],
                "strong_input_potentiated": result_strong["ltp_induced"]
            }
        else:
            return {
                "ltp_induced": False,
                "reason": "Strong input insufficient",
                "weak_input_potentiated": False,
                "strong_input_potentiated": False
            }

    def process_event(
        self,
        event_type: str,
        **kwargs
    ) -> Dict:
        """
        Process LTP/LTD event

        Args:
            event_type: Type of event ("induce_ltp", "induce_ltd", etc.)
            **kwargs: Event-specific parameters

        Returns:
            Processing result
        """
        if event_type == "induce_ltp":
            return self.induce_ltp(
                pre_neuron=kwargs["pre_neuron"],
                post_neuron=kwargs["post_neuron"],
                stimulation_frequency=kwargs["stimulation_frequency"],
                stimulation_duration=kwargs["stimulation_duration"]
            )

        elif event_type == "induce_ltd":
            return self.induce_ltd(
                pre_neuron=kwargs["pre_neuron"],
                post_neuron=kwargs["post_neuron"],
                stimulation_frequency=kwargs["stimulation_frequency"],
                stimulation_duration=kwargs["stimulation_duration"]
            )

        else:
            return {"error": f"Unknown event type: {event_type}"}

    def get_state(self) -> Dict:
        """
        Get current state of LTP system

        Returns:
            System state with LTP/LTD statistics
        """
        if len(self.synapses) == 0:
            return {
                "total_synapses": 0,
                "ltp_potentiated_count": 0,
                "ltd_active_count": 0,
                "average_strength": 0.0,
                "average_ltp_strength": 0.0
            }

        ltp_count = sum(1 for s in self.synapses.values() if s["ltp_potentiated"])
        ltd_count = sum(1 for s in self.synapses.values() if s.get("ltd_active", False))
        total_strength = sum(s["strength"] for s in self.synapses.values())
        total_ltp_strength = sum(s["ltp_strength"] for s in self.synapses.values() if s["ltp_potentiated"])

        return {
            "total_synapses": len(self.synapses),
            "ltp_potentiated_count": ltp_count,
            "ltd_active_count": ltd_count,
            "average_strength": float(total_strength / len(self.synapses)),
            "average_ltp_strength": float(total_ltp_strength / ltp_count) if ltp_count > 0 else 0.0,
            "ltp_threshold": self.ltp_threshold,
            "ltp_duration_hours": self.ltp_duration_hours
        }
