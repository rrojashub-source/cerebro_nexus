"""
LAB_047: Synaptic Pruning System

Function: Elimination of weak/unused synaptic connections
Neuroscience Basis: Activity-dependent pruning, critical periods, homeostatic plasticity

Key Papers:
- Hubel & Wiesel (1962) - Critical periods in visual cortex development
- Huttenlocher (1979) - Synaptic density changes during human brain development
- Paolicelli et al. (2011) - Synaptic pruning by microglia

Synaptic Pruning Model:
- Activity-dependent: Low activity → weakening → pruning
- Use it or lose it: Unused synapses decay and are eliminated
- Critical periods: Windows of enhanced plasticity
- Homeostatic regulation: Prevent excessive pruning or strengthening
"""

from typing import Dict, List, Optional, Tuple
import math


class SynapticPruningSystem:
    """
    LAB_047: Synaptic Pruning System

    Models elimination of weak synapses through:
    - Activity-dependent strengthening/weakening
    - Pruning of synapses below threshold
    - Critical period modulation
    - Homeostatic regulation

    Integration:
    - LAB_048 (Hebbian Learning): Amplifies active synapses
    - LAB_049 (LTP): Potentiated synapses resist pruning
    - LAB_040 (Skill Acquisition): Active learning reduces pruning

    Parameters:
    -----------
    pruning_threshold : float
        Strength threshold below which synapses are pruned (default: 0.3)
    """

    def __init__(self, pruning_threshold: float = 0.3):
        self.pruning_threshold = pruning_threshold

        # Synapses registry: (pre_neuron, post_neuron) → synapse_data
        self.synapses: Dict[Tuple[str, str], Dict] = {}

        # Pruning history
        self.pruning_history: List[Dict] = []

    def create_synapse(
        self,
        pre_neuron: str,
        post_neuron: str,
        initial_strength: float = 0.5
    ) -> Dict:
        """Create synapse between neurons"""
        synapse_id = (pre_neuron, post_neuron)

        # Clamp strength to 0-1
        strength = max(0.0, min(1.0, initial_strength))

        self.synapses[synapse_id] = {
            "pre_neuron": pre_neuron,
            "post_neuron": post_neuron,
            "strength": strength,
            "activity_history": [],
            "ltp_potentiated": False,
            "last_activity_time": 0
        }

        return {
            "synapse_created": True,
            "synapse_id": synapse_id,
            "initial_strength": float(strength)
        }

    def update_synapse_activity(
        self,
        pre_neuron: str,
        post_neuron: str,
        activity: float,
        critical_period: bool = False,
        homeostatic_scaling: bool = False,
        hebbian_signal: Optional[float] = None
    ) -> Dict:
        """Update synapse based on activity"""
        synapse_id = (pre_neuron, post_neuron)

        if synapse_id not in self.synapses:
            return {"error": "Synapse not found"}

        synapse = self.synapses[synapse_id]
        old_strength = synapse["strength"]

        # Compute strength delta based on activity
        # High activity (>0.5) → strengthen
        # Low activity (<0.5) → weaken
        if activity > 0.5:
            # Strengthening
            base_delta = (activity - 0.5) * 0.1
        else:
            # Weakening
            base_delta = (activity - 0.5) * 0.05

        # Critical period modulation (amplify changes)
        if critical_period:
            base_delta *= 1.5

        # Hebbian learning amplification (LAB_048 integration)
        # Hebbian signal amplifies strengthening significantly
        if hebbian_signal is not None:
            base_delta *= (1.0 + hebbian_signal * 3.0)  # 3x amplification

        # Apply delta
        new_strength = old_strength + base_delta

        # Homeostatic scaling (prevent runaway strengthening)
        if homeostatic_scaling:
            # Asymptotic toward 1.0
            if new_strength > 0.9:
                new_strength = 0.9 + (new_strength - 0.9) * 0.3

        # Clamp to 0-1
        new_strength = max(0.0, min(1.0, new_strength))

        synapse["strength"] = new_strength
        synapse["activity_history"].append(activity)

        # Keep only last 10 activities
        if len(synapse["activity_history"]) > 10:
            synapse["activity_history"].pop(0)

        return {
            "strength_updated": True,
            "old_strength": float(old_strength),
            "new_strength": float(new_strength),
            "strength_delta": float(new_strength - old_strength)
        }

    def apply_decay(self, days: int) -> Dict:
        """Apply decay to all synapses (unused synapses weaken)"""
        # Decay rate: ~2% per day without activity
        base_decay_rate = 0.02 * days

        for synapse_id, synapse in self.synapses.items():
            # Check recent activity (last 10 activities)
            recent_activities = synapse.get("activity_history", [])

            if len(recent_activities) > 0:
                # Has recent activity → slower decay
                avg_recent_activity = sum(recent_activities) / len(recent_activities)
                # High activity (0.8) → 40% of decay, Low activity (0.2) → 80% of decay
                activity_factor = 0.4 + (1.0 - avg_recent_activity) * 0.6
            else:
                # No recent activity → full decay
                activity_factor = 1.0

            decay_rate = base_decay_rate * activity_factor

            # Exponential decay
            synapse["strength"] *= math.exp(-decay_rate)

        return {
            "days_decayed": days,
            "decay_rate": float(base_decay_rate),
            "synapses_affected": len(self.synapses)
        }

    def prune_weak_synapses(
        self,
        critical_period: bool = False,
        min_retention_rate: float = 0.0,
        skill_acquisition_active: bool = False
    ) -> Dict:
        """Prune synapses below threshold"""
        initial_count = len(self.synapses)

        # Adjust threshold based on context
        effective_threshold = self.pruning_threshold

        # Critical period: more aggressive pruning
        # Higher threshold = more synapses below threshold = more pruning
        if critical_period:
            effective_threshold *= 1.5  # Prune synapses < 0.45 (instead of < 0.3)

        # Active skill acquisition: less aggressive pruning
        # Lower threshold = fewer synapses below threshold = less pruning
        if skill_acquisition_active:
            effective_threshold *= 0.7

        # Identify weak synapses
        weak_synapses = []
        for synapse_id, synapse in self.synapses.items():
            # LTP-potentiated synapses resist pruning (LAB_049 integration)
            if synapse.get("ltp_potentiated", False):
                continue

            if synapse["strength"] < effective_threshold:
                weak_synapses.append(synapse_id)

        # Apply min retention rate (homeostatic regulation)
        if min_retention_rate > 0:
            max_prunable = int(initial_count * (1.0 - min_retention_rate))
            weak_synapses = weak_synapses[:max_prunable]

        # Prune synapses
        for synapse_id in weak_synapses:
            del self.synapses[synapse_id]

        pruned_count = len(weak_synapses)
        retained_count = len(self.synapses)

        pruning_rate = pruned_count / initial_count if initial_count > 0 else 0.0
        retention_rate = retained_count / initial_count if initial_count > 0 else 0.0

        # Compute pruning efficiency (% of weak synapses removed)
        total_weak = len([s for s in self.synapses.values() if s["strength"] < effective_threshold])
        pruning_efficiency = pruned_count / (pruned_count + total_weak) if (pruned_count + total_weak) > 0 else 1.0

        # Store in history
        self.pruning_history.append({
            "synapses_pruned": pruned_count,
            "synapses_retained": retained_count,
            "pruning_rate": pruning_rate,
            "critical_period": critical_period
        })

        return {
            "synapses_pruned": pruned_count,
            "synapses_retained": retained_count,
            "pruning_rate": float(pruning_rate),
            "retention_rate": float(retention_rate),
            "pruning_efficiency": float(pruning_efficiency)
        }

    def compute_network_health(self) -> float:
        """Compute network health (average synapse strength)"""
        if len(self.synapses) == 0:
            return 0.0

        total_strength = sum(s["strength"] for s in self.synapses.values())
        avg_strength = total_strength / len(self.synapses)

        return float(avg_strength)

    def process_event(self, event_type: str, **kwargs) -> Dict:
        """Main processing interface"""
        if event_type == "activity":
            pre_neuron = kwargs.get("pre_neuron", "")
            post_neuron = kwargs.get("post_neuron", "")
            activity = kwargs.get("activity", 0.5)
            critical_period = kwargs.get("critical_period", False)
            homeostatic_scaling = kwargs.get("homeostatic_scaling", False)
            hebbian_signal = kwargs.get("hebbian_signal", None)

            result = self.update_synapse_activity(
                pre_neuron, post_neuron, activity, critical_period, homeostatic_scaling, hebbian_signal
            )
            return result

        elif event_type == "prune":
            critical_period = kwargs.get("critical_period", False)
            min_retention_rate = kwargs.get("min_retention_rate", 0.0)
            skill_acquisition_active = kwargs.get("skill_acquisition_active", False)

            result = self.prune_weak_synapses(critical_period, min_retention_rate, skill_acquisition_active)
            return result

        else:
            return {"error": f"Unknown event type: {event_type}"}

    def get_state(self) -> Dict:
        """Get current system state"""
        if len(self.synapses) == 0:
            avg_strength = 0.0
        else:
            avg_strength = sum(s["strength"] for s in self.synapses.values()) / len(self.synapses)

        return {
            "total_synapses": len(self.synapses),
            "average_strength": float(avg_strength),
            "pruning_threshold": float(self.pruning_threshold),
            "pruning_history_size": len(self.pruning_history)
        }
