"""
LAB_050: Structural Plasticity System

Neuroplasticity: "Building and remodeling the brain"

Key Mechanisms:
- Synaptogenesis: Formation of new synapses
- Synapse elimination: Removal of unused synapses
- Spine morphology: Changes in dendritic spine shape (thin → stubby → mushroom)
- Axonal sprouting: Growth of new axonal branches
- Homeostatic regulation: Balance synapse numbers

Mathematical Model:
- Formation rate: P(form) = η * f(activity) * f(correlation) * f(LTP)
- Elimination rate: P(elim) = λ * f(inactivity) * (1 - f(LTP))
- Spine transition: thin → stubby → mushroom (activity-dependent)
- Homeostasis: Target synapse density maintained

Key Papers:
- Holtmaat & Svoboda (2009): Experience-dependent structural plasticity
- Kasai et al. (2010): Dendritic spine dynamics
- Fu & Zuo (2011): Experience-dependent remodeling
"""

import math
import random
from typing import Dict, List, Optional, Tuple


class StructuralPlasticitySystem:
    """
    Structural Plasticity: Physical changes in synaptic connections

    Core principle: Experience reshapes brain structure

    Implements:
    - Synaptogenesis (new synapse formation)
    - Synapse elimination (structural removal)
    - Spine morphology dynamics (thin/stubby/mushroom)
    - Axonal sprouting
    """

    def __init__(
        self,
        synaptogenesis_rate: float = 0.8,
        synapse_elimination_rate: float = 0.05,
        target_synapse_density: int = 15,
        deterministic: bool = True
    ):
        """
        Initialize Structural Plasticity System

        Args:
            synaptogenesis_rate: Base rate of new synapse formation
            synapse_elimination_rate: Base rate of synapse removal
            target_synapse_density: Target number of synapses (homeostasis)
        """
        self.synaptogenesis_rate = synaptogenesis_rate
        self.synapse_elimination_rate = synapse_elimination_rate
        self.target_synapse_density = target_synapse_density
        self.deterministic = deterministic

        # Synapse registry
        self.synapses: Dict[Tuple[str, str], Dict] = {}

        # Axonal sprouting registry
        self.sprouting: Dict[Tuple[str, str], float] = {}  # (neuron, region) → potential

        # Activity history (for elimination decisions)
        self.activity_history: Dict[Tuple[str, str], List[float]] = {}

    def trigger_synaptogenesis(
        self,
        pre_neuron: str,
        post_neuron: str,
        activity_level: float,
        ltp_active: bool = False,
        hebbian_correlation: Optional[float] = None,
        critical_period: bool = False
    ) -> Dict:
        """
        Attempt to form new synapse

        Args:
            pre_neuron: Presynaptic neuron ID
            post_neuron: Postsynaptic neuron ID
            activity_level: Current activity level [0-1]
            ltp_active: LAB_049 integration (LTP facilitates formation)
            hebbian_correlation: LAB_048 integration (correlation required)
            critical_period: Enhanced plasticity window

        Returns:
            Synaptogenesis result
        """
        synapse_id = (pre_neuron, post_neuron)

        # Check if synapse already exists
        if synapse_id in self.synapses:
            return {
                "synapse_formed": False,
                "reason": "Synapse already exists"
            }

        # Compute formation probability
        base_prob = self.synaptogenesis_rate

        # Activity modulation
        if activity_level < 0.5:
            return {
                "synapse_formed": False,
                "reason": "Activity too low"
            }

        activity_factor = activity_level

        # LTP facilitates formation (LAB_049 integration)
        ltp_factor = 1.5 if ltp_active else 1.0

        # Hebbian correlation required (LAB_048 integration)
        if hebbian_correlation is not None:
            if hebbian_correlation < 0.5:
                return {
                    "synapse_formed": False,
                    "reason": "Insufficient correlation"
                }
            correlation_factor = hebbian_correlation
        else:
            correlation_factor = 1.0

        # Critical period enhancement
        critical_period_factor = 2.0 if critical_period else 1.0

        # Homeostatic regulation
        current_synapse_count = len(self.synapses)
        if current_synapse_count > self.target_synapse_density:
            homeostatic_downregulation = True
            homeostatic_factor = 0.3  # Strongly reduce formation
        else:
            homeostatic_downregulation = False
            homeostatic_factor = 1.0

        # Compute final probability
        formation_prob = (base_prob * activity_factor * ltp_factor *
                         correlation_factor * critical_period_factor * homeostatic_factor)

        # Stochastic or deterministic formation
        if self.deterministic:
            # Enhanced formation when synapse count is very low (homeostatic upregulation)
            deterministic_threshold = 0.3 if current_synapse_count < 10 else 0.5
            formation_occurs = formation_prob > deterministic_threshold
        else:
            formation_occurs = random.random() < formation_prob  # Stochastic for realism

        if formation_occurs:
            # Form new synapse
            # LTP-associated synapses start stronger (LAB_049 integration)
            initial_strength = 0.35 if ltp_active else 0.3

            self.synapses[synapse_id] = {
                "pre_neuron": pre_neuron,
                "post_neuron": post_neuron,
                "strength": initial_strength,
                "spine_type": "thin",  # New spines start thin
                "ltp_potentiated": ltp_active,
                "pruning_eligible": False,
                "activity_history": []
            }

            self.activity_history[synapse_id] = [activity_level]

            return {
                "synapse_formed": True,
                "initial_strength": 0.3,
                "spine_type": "thin",
                "homeostatic_downregulation": homeostatic_downregulation
            }
        else:
            return {
                "synapse_formed": False,
                "reason": "Stochastic formation failed",
                "formation_prob": float(formation_prob),
                "homeostatic_downregulation": homeostatic_downregulation
            }

    def eliminate_inactive_synapses(
        self,
        inactivity_days: int,
        critical_period: bool = False
    ) -> Dict:
        """
        Eliminate synapses based on inactivity

        Args:
            inactivity_days: Days of inactivity threshold
            critical_period: Enhanced elimination during critical period

        Returns:
            Elimination result
        """
        base_elimination_rate = self.synapse_elimination_rate

        # Critical period: more aggressive elimination
        if critical_period:
            elimination_rate = base_elimination_rate * 2.0
        else:
            elimination_rate = base_elimination_rate

        synapses_to_eliminate = []

        for synapse_id, synapse in self.synapses.items():
            # LTP-potentiated synapses resist elimination (LAB_049 integration)
            if synapse.get("ltp_potentiated", False):
                continue

            # Check if marked for pruning (LAB_047 integration)
            if synapse.get("pruning_eligible", False):
                synapses_to_eliminate.append(synapse_id)
                continue

            # Check activity history
            if synapse_id in self.activity_history:
                activity_records = self.activity_history[synapse_id]

                # If only 1 activity record (formation only, no subsequent activity) and long inactivity → eliminate
                if len(activity_records) == 1 and inactivity_days > 20:
                    synapses_to_eliminate.append(synapse_id)
                    continue

                recent_activity = activity_records[-10:]  # Last 10 activities

                if len(recent_activity) > 0:
                    avg_activity = sum(recent_activity) / len(recent_activity)

                    # If low activity, eliminate probabilistically or deterministically
                    if avg_activity < 0.3:
                        if self.deterministic:
                            eliminate_occurs = elimination_rate > 0.5 or avg_activity < 0.15
                        else:
                            eliminate_occurs = random.random() < elimination_rate

                        if eliminate_occurs:
                            synapses_to_eliminate.append(synapse_id)

        # Eliminate synapses
        for synapse_id in synapses_to_eliminate:
            del self.synapses[synapse_id]
            if synapse_id in self.activity_history:
                del self.activity_history[synapse_id]

        return {
            "synapses_eliminated": len(synapses_to_eliminate),
            "elimination_rate": float(elimination_rate)
        }

    def record_activity(
        self,
        synapse_id: Tuple[str, str],
        activity: float
    ) -> Dict:
        """
        Record synaptic activity (affects spine morphology and elimination)

        Args:
            synapse_id: Synapse identifier (pre, post)
            activity: Activity level [0-1]

        Returns:
            Activity recording result
        """
        if synapse_id not in self.synapses:
            return {
                "error": "Synapse does not exist"
            }

        synapse = self.synapses[synapse_id]

        # Update activity history
        if synapse_id not in self.activity_history:
            self.activity_history[synapse_id] = []
        self.activity_history[synapse_id].append(activity)

        # Keep last 20 activities
        if len(self.activity_history[synapse_id]) > 20:
            self.activity_history[synapse_id] = self.activity_history[synapse_id][-20:]

        # Update spine morphology based on activity
        recent_avg_activity = sum(self.activity_history[synapse_id][-5:]) / min(5, len(self.activity_history[synapse_id]))

        current_spine = synapse["spine_type"]

        # Activity-dependent spine transitions
        if recent_avg_activity > 0.7:
            # High activity → mature spine
            if current_spine == "thin":
                synapse["spine_type"] = "stubby"
                synapse["strength"] = min(1.0, synapse["strength"] + 0.15)
            elif current_spine == "stubby":
                synapse["spine_type"] = "mushroom"
                synapse["strength"] = min(1.0, synapse["strength"] + 0.3)
        elif recent_avg_activity < 0.3:
            # Low activity → immature spine
            if current_spine == "mushroom":
                synapse["spine_type"] = "stubby"
                synapse["strength"] = max(0.0, synapse["strength"] - 0.1)
            elif current_spine == "stubby":
                synapse["spine_type"] = "thin"
                synapse["strength"] = max(0.0, synapse["strength"] - 0.05)

        return {
            "activity_recorded": True,
            "spine_type": synapse["spine_type"],
            "strength": float(synapse["strength"])
        }

    def trigger_axonal_sprouting(
        self,
        neuron: str,
        target_region: str,
        activity_level: float
    ) -> Dict:
        """
        Trigger axonal growth towards target region

        Args:
            neuron: Neuron ID
            target_region: Target region ID
            activity_level: Current activity level [0-1]

        Returns:
            Sprouting result
        """
        sprouting_id = (neuron, target_region)

        if activity_level < 0.7:
            return {
                "sprouting_occurred": False,
                "reason": "Insufficient activity for sprouting"
            }

        # Increase synapse potential in target region
        if sprouting_id not in self.sprouting:
            self.sprouting[sprouting_id] = 0.0

        self.sprouting[sprouting_id] += 0.2

        return {
            "sprouting_occurred": True,
            "synapse_potential": float(self.sprouting[sprouting_id])
        }

    def get_synapse_potential(
        self,
        neuron: str,
        target_region: str
    ) -> float:
        """
        Get potential for forming synapses in target region

        Args:
            neuron: Neuron ID
            target_region: Target region ID

        Returns:
            Synapse potential [0-1]
        """
        sprouting_id = (neuron, target_region)
        return self.sprouting.get(sprouting_id, 0.0)

    def process_event(
        self,
        event_type: str,
        **kwargs
    ) -> Dict:
        """
        Process structural plasticity event

        Args:
            event_type: Type of event ("synaptogenesis", "eliminate_inactive", etc.)
            **kwargs: Event-specific parameters

        Returns:
            Processing result
        """
        if event_type == "synaptogenesis":
            return self.trigger_synaptogenesis(
                pre_neuron=kwargs["pre_neuron"],
                post_neuron=kwargs["post_neuron"],
                activity_level=kwargs["activity_level"],
                ltp_active=kwargs.get("ltp_active", False),
                hebbian_correlation=kwargs.get("hebbian_correlation", None),
                critical_period=kwargs.get("critical_period", False)
            )

        elif event_type == "eliminate_inactive":
            return self.eliminate_inactive_synapses(
                inactivity_days=kwargs["inactivity_days"],
                critical_period=kwargs.get("critical_period", False)
            )

        else:
            return {"error": f"Unknown event type: {event_type}"}

    def get_state(self) -> Dict:
        """
        Get current state of structural plasticity system

        Returns:
            System state with structural statistics
        """
        if len(self.synapses) == 0:
            return {
                "total_synapses": 0,
                "spine_type_distribution": {"thin": 0, "stubby": 0, "mushroom": 0},
                "synaptogenesis_rate": self.synaptogenesis_rate,
                "synapse_elimination_rate": self.synapse_elimination_rate
            }

        # Compute spine type distribution
        thin_count = sum(1 for s in self.synapses.values() if s["spine_type"] == "thin")
        stubby_count = sum(1 for s in self.synapses.values() if s["spine_type"] == "stubby")
        mushroom_count = sum(1 for s in self.synapses.values() if s["spine_type"] == "mushroom")

        return {
            "total_synapses": len(self.synapses),
            "spine_type_distribution": {
                "thin": thin_count,
                "stubby": stubby_count,
                "mushroom": mushroom_count
            },
            "synaptogenesis_rate": self.synaptogenesis_rate,
            "synapse_elimination_rate": self.synapse_elimination_rate,
            "target_synapse_density": self.target_synapse_density
        }
