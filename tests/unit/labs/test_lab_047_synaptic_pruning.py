"""
LAB_047: Synaptic Pruning - Unit Tests

Neuroplasticity: Elimination of weak/unused synaptic connections

Key Papers:
- Hubel & Wiesel (1962) - Critical periods in visual cortex development
- Huttenlocher (1979) - Synaptic density changes during human brain development
- Paolicelli et al. (2011) - Synaptic pruning by microglia is necessary for normal brain development
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Neuroplasticity.LAB_047_Synaptic_Pruning.synaptic_pruning_system import (
    SynapticPruningSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with default pruning parameters"""
        system = SynapticPruningSystem()
        assert system.pruning_threshold == 0.3
        assert len(system.synapses) == 0
        assert len(system.pruning_history) == 0

    def test_custom_pruning_threshold(self):
        """System accepts custom pruning threshold"""
        system = SynapticPruningSystem(pruning_threshold=0.4)
        assert system.pruning_threshold == 0.4

    def test_synapse_registry_empty(self):
        """Synapse registry starts empty"""
        system = SynapticPruningSystem()
        state = system.get_state()
        assert state["total_synapses"] == 0


class TestSynapseCreation:
    """Test synapse creation and tracking"""

    def test_create_synapse(self):
        """Create synapse between neurons"""
        system = SynapticPruningSystem()

        result = system.create_synapse(
            pre_neuron="neuron_A",
            post_neuron="neuron_B",
            initial_strength=0.5
        )

        assert result["synapse_created"] == True
        assert result["synapse_id"] == ("neuron_A", "neuron_B")
        assert result["initial_strength"] == 0.5

    def test_synapse_strength_range(self):
        """Synapse strength constrained to 0-1"""
        system = SynapticPruningSystem()

        system.create_synapse("A", "B", initial_strength=0.8)
        synapse = system.synapses[("A", "B")]

        assert 0.0 <= synapse["strength"] <= 1.0

    def test_multiple_synapses(self):
        """System tracks multiple synapses"""
        system = SynapticPruningSystem()

        system.create_synapse("A", "B", initial_strength=0.5)
        system.create_synapse("B", "C", initial_strength=0.6)
        system.create_synapse("C", "D", initial_strength=0.7)

        assert len(system.synapses) == 3


class TestActivityDependentPruning:
    """Test activity-dependent synaptic pruning"""

    def test_low_activity_synapse_weakens(self):
        """Low activity → synapse weakens"""
        system = SynapticPruningSystem()

        system.create_synapse("A", "B", initial_strength=0.6)

        # Low activity (no stimulation)
        for _ in range(10):
            system.update_synapse_activity("A", "B", activity=0.1)

        synapse = system.synapses[("A", "B")]
        assert synapse["strength"] < 0.6  # Weakened

    def test_high_activity_synapse_strengthens(self):
        """High activity → synapse strengthens"""
        system = SynapticPruningSystem()

        system.create_synapse("A", "B", initial_strength=0.5)

        # High activity
        for _ in range(10):
            system.update_synapse_activity("A", "B", activity=0.9)

        synapse = system.synapses[("A", "B")]
        assert synapse["strength"] > 0.5  # Strengthened

    def test_pruning_below_threshold(self):
        """Synapse pruned when strength < threshold"""
        system = SynapticPruningSystem(pruning_threshold=0.3)

        system.create_synapse("A", "B", initial_strength=0.4)

        # Weaken synapse below threshold
        for _ in range(20):
            system.update_synapse_activity("A", "B", activity=0.05)

        # Apply pruning
        result = system.prune_weak_synapses()

        assert result["synapses_pruned"] >= 1
        assert ("A", "B") not in system.synapses  # Pruned

    def test_strong_synapses_survive_pruning(self):
        """Strong synapses survive pruning"""
        system = SynapticPruningSystem(pruning_threshold=0.3)

        system.create_synapse("A", "B", initial_strength=0.8)

        # High activity maintains strength
        for _ in range(10):
            system.update_synapse_activity("A", "B", activity=0.9)

        result = system.prune_weak_synapses()

        assert ("A", "B") in system.synapses  # Survived
        assert result["synapses_retained"] >= 1


class TestUseItOrLoseIt:
    """Test 'use it or lose it' principle"""

    def test_unused_synapse_decay(self):
        """Unused synapse decays over time"""
        system = SynapticPruningSystem()

        system.create_synapse("A", "B", initial_strength=0.6)
        initial_strength = system.synapses[("A", "B")]["strength"]

        # No activity for extended period
        system.apply_decay(days=30)

        final_strength = system.synapses[("A", "B")]["strength"]
        assert final_strength < initial_strength

    def test_frequently_used_synapse_maintained(self):
        """Frequently used synapse maintains strength"""
        system = SynapticPruningSystem()

        system.create_synapse("A", "B", initial_strength=0.5)

        # Frequent use
        for _ in range(20):
            system.update_synapse_activity("A", "B", activity=0.8)

        synapse = system.synapses[("A", "B")]
        assert synapse["strength"] >= 0.5  # Maintained or strengthened

    def test_intermittent_use_slow_decay(self):
        """Intermittent use slows decay"""
        system = SynapticPruningSystem()

        # Synapse A: No use
        system.create_synapse("A", "B", initial_strength=0.6)

        # Synapse B: Intermittent use
        system.create_synapse("C", "D", initial_strength=0.6)
        system.update_synapse_activity("C", "D", activity=0.5)

        # Apply decay
        system.apply_decay(days=10)

        strength_no_use = system.synapses[("A", "B")]["strength"]
        strength_intermittent = system.synapses[("C", "D")]["strength"]

        assert strength_intermittent > strength_no_use


class TestCriticalPeriods:
    """Test critical period windows"""

    def test_critical_period_accelerated_pruning(self):
        """During critical period: accelerated pruning"""
        system = SynapticPruningSystem()

        system.create_synapse("A", "B", initial_strength=0.4)

        # Normal pruning
        result_normal = system.prune_weak_synapses(critical_period=False)

        # Reset
        system.synapses[("A", "B")] = {"strength": 0.4, "activity_history": []}

        # Critical period pruning
        result_critical = system.prune_weak_synapses(critical_period=True)

        # Critical period should prune more aggressively
        assert result_critical["pruning_rate"] > result_normal["pruning_rate"]

    def test_critical_period_strengthening(self):
        """During critical period: enhanced strengthening"""
        system = SynapticPruningSystem()

        system.create_synapse("A", "B", initial_strength=0.5)

        # Normal period strengthening
        system.update_synapse_activity("A", "B", activity=0.9, critical_period=False)
        normal_strength = system.synapses[("A", "B")]["strength"]

        # Reset
        system.synapses[("A", "B")]["strength"] = 0.5

        # Critical period strengthening
        system.update_synapse_activity("A", "B", activity=0.9, critical_period=True)
        critical_strength = system.synapses[("A", "B")]["strength"]

        # Critical period amplifies strengthening
        assert critical_strength > normal_strength


class TestHomeostaticRegulation:
    """Test homeostatic plasticity"""

    def test_excessive_pruning_prevention(self):
        """Prevent excessive pruning (maintain minimum connectivity)"""
        system = SynapticPruningSystem()

        # Create many weak synapses
        for i in range(20):
            system.create_synapse(f"A{i}", f"B{i}", initial_strength=0.25)

        # Prune
        result = system.prune_weak_synapses(min_retention_rate=0.3)

        # Should retain at least 30% (6 synapses)
        assert len(system.synapses) >= 6
        assert result["retention_rate"] >= 0.3

    def test_activity_scaling(self):
        """Scale activity to prevent runaway strengthening"""
        system = SynapticPruningSystem()

        system.create_synapse("A", "B", initial_strength=0.5)

        # Excessive activity
        for _ in range(50):
            system.update_synapse_activity("A", "B", activity=1.0, homeostatic_scaling=True)

        synapse = system.synapses[("A", "B")]
        # Should not exceed 1.0 due to homeostatic regulation
        assert synapse["strength"] <= 1.0


class TestPruningMetrics:
    """Test pruning efficiency metrics"""

    def test_compute_pruning_efficiency(self):
        """Compute pruning efficiency (% weak synapses removed)"""
        system = SynapticPruningSystem(pruning_threshold=0.3)

        # Create mix of strong and weak synapses
        system.create_synapse("A", "B", initial_strength=0.8)  # Strong
        system.create_synapse("C", "D", initial_strength=0.2)  # Weak
        system.create_synapse("E", "F", initial_strength=0.9)  # Strong
        system.create_synapse("G", "H", initial_strength=0.15)  # Weak

        result = system.prune_weak_synapses()

        assert "pruning_efficiency" in result
        assert result["pruning_efficiency"] > 0.5  # Pruned 50%+ of weak synapses

    def test_network_health_score(self):
        """Compute network health (avg synapse strength)"""
        system = SynapticPruningSystem()

        system.create_synapse("A", "B", initial_strength=0.7)
        system.create_synapse("C", "D", initial_strength=0.8)
        system.create_synapse("E", "F", initial_strength=0.9)

        health = system.compute_network_health()

        assert health > 0.7  # High average strength


class TestIntegration:
    """Test integration with other LABs"""

    def test_hebbian_learning_amplifies_strengthening(self):
        """LAB_048: Hebbian learning amplifies active synapses"""
        system = SynapticPruningSystem()

        system.create_synapse("A", "B", initial_strength=0.5)

        # With Hebbian signal (from LAB_048)
        result = system.update_synapse_activity(
            "A", "B",
            activity=0.8,
            hebbian_signal=0.9  # From LAB_048
        )

        # Hebbian learning should amplify strengthening
        assert result["strength_delta"] > 0.1

    def test_ltp_prevents_pruning(self):
        """LAB_049: LTP-potentiated synapses resist pruning"""
        system = SynapticPruningSystem(pruning_threshold=0.3)

        system.create_synapse("A", "B", initial_strength=0.25)  # Below threshold

        # Mark as LTP-potentiated (from LAB_049)
        system.synapses[("A", "B")]["ltp_potentiated"] = True

        result = system.prune_weak_synapses()

        # LTP-potentiated synapse should survive despite low strength
        assert ("A", "B") in system.synapses

    def test_skill_acquisition_reduces_pruning(self):
        """LAB_040: Active skill acquisition reduces pruning rate"""
        system = SynapticPruningSystem()

        # Create synapses
        system.create_synapse("A", "B", initial_strength=0.4)
        system.create_synapse("C", "D", initial_strength=0.35)

        # Prune with active skill acquisition signal (from LAB_040)
        result = system.prune_weak_synapses(skill_acquisition_active=True)

        # Skill acquisition should reduce pruning rate
        assert result["pruning_rate"] < 0.5  # Less aggressive


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_activity_event(self):
        """Process synapse activity update"""
        system = SynapticPruningSystem()

        system.create_synapse("A", "B", initial_strength=0.5)

        result = system.process_event(
            event_type="activity",
            pre_neuron="A",
            post_neuron="B",
            activity=0.8
        )

        assert "strength_updated" in result
        assert result["strength_updated"] == True

    def test_process_prune_event(self):
        """Process pruning event"""
        system = SynapticPruningSystem()

        system.create_synapse("A", "B", initial_strength=0.2)

        result = system.process_event(
            event_type="prune"
        )

        assert "synapses_pruned" in result


class TestGetState:
    """Test state retrieval"""

    def test_get_state_returns_synapses(self):
        """get_state returns synapse statistics"""
        system = SynapticPruningSystem()

        system.create_synapse("A", "B", initial_strength=0.6)
        system.create_synapse("C", "D", initial_strength=0.8)

        state = system.get_state()

        assert "total_synapses" in state
        assert state["total_synapses"] == 2
        assert "average_strength" in state

    def test_get_state_serializable(self):
        """get_state returns JSON-serializable dict"""
        system = SynapticPruningSystem()

        state = system.get_state()

        import json
        json_str = json.dumps(state)
        assert json_str is not None
