"""
LAB_050: Structural Plasticity - Unit Tests

Neuroplasticity: "Building and remodeling the brain"

Key Papers:
- Holtmaat & Svoboda (2009) - Experience-dependent structural synaptic plasticity
- Kasai et al. (2010) - Structural dynamics of dendritic spines in memory
- Fu & Zuo (2011) - Experience-dependent structural plasticity
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Neuroplasticity.LAB_050_Structural_Plasticity.structural_plasticity_system import (
    StructuralPlasticitySystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with default structural plasticity parameters"""
        system = StructuralPlasticitySystem()
        assert system.synaptogenesis_rate == 0.8
        assert system.synapse_elimination_rate == 0.05
        assert len(system.synapses) == 0

    def test_custom_synaptogenesis_rate(self):
        """System accepts custom synaptogenesis rate"""
        system = StructuralPlasticitySystem(synaptogenesis_rate=0.2)
        assert system.synaptogenesis_rate == 0.2

    def test_custom_elimination_rate(self):
        """System accepts custom elimination rate"""
        system = StructuralPlasticitySystem(synapse_elimination_rate=0.1)
        assert system.synapse_elimination_rate == 0.1


class TestSynaptogenesis:
    """Test new synapse formation"""

    def test_experience_drives_synaptogenesis(self):
        """High activity → new synapse formation"""
        system = StructuralPlasticitySystem()

        result = system.trigger_synaptogenesis(
            pre_neuron="A",
            post_neuron="B",
            activity_level=0.9
        )

        assert result["synapse_formed"] == True
        assert ("A", "B") in system.synapses

    def test_low_activity_no_synaptogenesis(self):
        """Low activity → no new synapses"""
        system = StructuralPlasticitySystem()

        result = system.trigger_synaptogenesis(
            pre_neuron="A",
            post_neuron="B",
            activity_level=0.1
        )

        assert result["synapse_formed"] == False

    def test_ltp_facilitates_synaptogenesis(self):
        """LTP (LAB_049) facilitates new synapse formation"""
        system = StructuralPlasticitySystem()

        result = system.trigger_synaptogenesis(
            pre_neuron="A",
            post_neuron="B",
            activity_level=0.6,
            ltp_active=True  # LAB_049 integration
        )

        assert result["synapse_formed"] == True

    def test_new_synapse_initial_strength(self):
        """Newly formed synapses start weak"""
        system = StructuralPlasticitySystem()

        system.trigger_synaptogenesis("A", "B", activity_level=0.9)

        synapse = system.synapses[("A", "B")]
        assert synapse["strength"] < 0.5  # Weak initial strength


class TestSynapseElimination:
    """Test synapse removal (complementary to pruning)"""

    def test_inactive_synapse_eliminated(self):
        """Long-term inactivity → synapse elimination"""
        system = StructuralPlasticitySystem()

        system.trigger_synaptogenesis("A", "B", activity_level=0.9)
        synapse_id = ("A", "B")

        # No activity for extended period
        result = system.eliminate_inactive_synapses(inactivity_days=30)

        assert synapse_id not in system.synapses

    def test_active_synapse_preserved(self):
        """Active synapses resist elimination"""
        system = StructuralPlasticitySystem()

        system.trigger_synaptogenesis("A", "B", activity_level=0.9)
        synapse_id = ("A", "B")

        # Maintain activity
        system.record_activity(synapse_id, activity=0.7)

        result = system.eliminate_inactive_synapses(inactivity_days=30)

        assert synapse_id in system.synapses

    def test_ltp_protects_from_elimination(self):
        """LTP-potentiated synapses resist elimination (LAB_049)"""
        system = StructuralPlasticitySystem()

        system.trigger_synaptogenesis("A", "B", activity_level=0.9)
        synapse_id = ("A", "B")

        # Mark as LTP-potentiated
        system.synapses[synapse_id]["ltp_potentiated"] = True

        result = system.eliminate_inactive_synapses(inactivity_days=30)

        assert synapse_id in system.synapses


class TestSpineMorphology:
    """Test dendritic spine shape changes"""

    def test_spine_types(self):
        """Spines have distinct morphologies (mushroom, stubby, thin)"""
        system = StructuralPlasticitySystem()

        system.trigger_synaptogenesis("A", "B", activity_level=0.9)
        synapse = system.synapses[("A", "B")]

        assert synapse["spine_type"] in ["thin", "stubby", "mushroom"]

    def test_thin_spine_weak_synapse(self):
        """Thin spines → weak synapses"""
        system = StructuralPlasticitySystem()

        system.trigger_synaptogenesis("A", "B", activity_level=0.9)
        synapse = system.synapses[("A", "B")]

        # New synapses start as thin
        assert synapse["spine_type"] == "thin"
        assert synapse["strength"] < 0.4

    def test_activity_transforms_spine_to_mushroom(self):
        """High activity → thin → stubby → mushroom"""
        system = StructuralPlasticitySystem()

        system.trigger_synaptogenesis("A", "B", activity_level=0.9)
        synapse_id = ("A", "B")

        # Apply repeated high activity
        for _ in range(10):
            system.record_activity(synapse_id, activity=0.9)

        synapse = system.synapses[synapse_id]
        assert synapse["spine_type"] == "mushroom"

    def test_mushroom_spine_strong_synapse(self):
        """Mushroom spines → strong, stable synapses"""
        system = StructuralPlasticitySystem()

        system.trigger_synaptogenesis("A", "B", activity_level=0.9)
        synapse_id = ("A", "B")

        # Develop to mushroom
        for _ in range(10):
            system.record_activity(synapse_id, activity=0.9)

        synapse = system.synapses[synapse_id]
        assert synapse["spine_type"] == "mushroom"
        assert synapse["strength"] > 0.7

    def test_inactivity_reverts_spine_morphology(self):
        """Inactivity → mushroom → stubby → thin"""
        system = StructuralPlasticitySystem()

        system.trigger_synaptogenesis("A", "B", activity_level=0.9)
        synapse_id = ("A", "B")

        # Develop to mushroom
        for _ in range(10):
            system.record_activity(synapse_id, activity=0.9)

        assert system.synapses[synapse_id]["spine_type"] == "mushroom"

        # Apply inactivity
        for _ in range(10):
            system.record_activity(synapse_id, activity=0.1)

        synapse = system.synapses[synapse_id]
        assert synapse["spine_type"] in ["stubby", "thin"]


class TestActivityDependentFormation:
    """Test activity-dependent synapse formation"""

    def test_correlated_activity_forms_synapses(self):
        """Correlated pre/post activity → synaptogenesis"""
        system = StructuralPlasticitySystem()

        # Correlated activity (Hebbian)
        result = system.trigger_synaptogenesis(
            pre_neuron="A",
            post_neuron="B",
            activity_level=0.8,
            hebbian_correlation=0.9  # LAB_048 integration
        )

        assert result["synapse_formed"] == True

    def test_uncorrelated_activity_no_formation(self):
        """Uncorrelated activity → no synaptogenesis"""
        system = StructuralPlasticitySystem()

        result = system.trigger_synaptogenesis(
            pre_neuron="A",
            post_neuron="B",
            activity_level=0.8,
            hebbian_correlation=0.1  # Low correlation
        )

        assert result["synapse_formed"] == False


class TestDevelopmentalCriticalPeriod:
    """Test critical period effects on structural plasticity"""

    def test_critical_period_enhanced_synaptogenesis(self):
        """Critical period → enhanced synapse formation"""
        system = StructuralPlasticitySystem()

        result = system.trigger_synaptogenesis(
            pre_neuron="A",
            post_neuron="B",
            activity_level=0.6,
            critical_period=True
        )

        assert result["synapse_formed"] == True

    def test_critical_period_enhanced_elimination(self):
        """Critical period → enhanced pruning/elimination"""
        system = StructuralPlasticitySystem()

        system.trigger_synaptogenesis("A", "B", activity_level=0.9)

        # Eliminate with critical period active
        result = system.eliminate_inactive_synapses(
            inactivity_days=15,
            critical_period=True
        )

        # More aggressive elimination
        assert result["elimination_rate"] > 0.05


class TestIntegration:
    """Test integration with other LABs"""

    def test_integration_with_pruning(self):
        """LAB_047: Structural elimination complements functional pruning"""
        system = StructuralPlasticitySystem()

        system.trigger_synaptogenesis("A", "B", activity_level=0.9)
        synapse_id = ("A", "B")

        # Mark for pruning (from LAB_047)
        system.synapses[synapse_id]["pruning_eligible"] = True

        result = system.eliminate_inactive_synapses(inactivity_days=20)

        assert synapse_id not in system.synapses

    def test_integration_with_hebbian(self):
        """LAB_048: Hebbian signal drives synaptogenesis"""
        system = StructuralPlasticitySystem()

        result = system.trigger_synaptogenesis(
            pre_neuron="A",
            post_neuron="B",
            activity_level=0.7,
            hebbian_correlation=0.9
        )

        assert result["synapse_formed"] == True

    def test_integration_with_ltp(self):
        """LAB_049: LTP stabilizes new synapses"""
        system = StructuralPlasticitySystem()

        system.trigger_synaptogenesis("A", "B", activity_level=0.9, ltp_active=True)
        synapse = system.synapses[("A", "B")]

        # LTP-associated synapses form as more mature
        assert synapse["strength"] > 0.3


class TestHomeostasis:
    """Test homeostatic regulation of synapse numbers"""

    def test_excessive_synaptogenesis_downregulated(self):
        """Too many synapses → reduced formation rate"""
        system = StructuralPlasticitySystem()

        # Form many synapses
        for i in range(20):
            system.trigger_synaptogenesis(f"A{i}", "B", activity_level=0.9)

        # Attempt more formation (should be downregulated)
        result = system.trigger_synaptogenesis("A_new", "B", activity_level=0.9)

        assert result.get("homeostatic_downregulation", False) == True

    def test_insufficient_synapses_enhanced_formation(self):
        """Too few synapses → enhanced formation"""
        system = StructuralPlasticitySystem()

        # Empty network → enhanced formation
        result = system.trigger_synaptogenesis(
            pre_neuron="A",
            post_neuron="B",
            activity_level=0.6  # Lower threshold
        )

        assert result["synapse_formed"] == True


class TestAxonalSprouting:
    """Test axonal growth and branching"""

    def test_activity_drives_sprouting(self):
        """High activity → axonal sprouting (new potential connections)"""
        system = StructuralPlasticitySystem()

        result = system.trigger_axonal_sprouting(
            neuron="A",
            target_region="B_region",
            activity_level=0.9
        )

        assert result["sprouting_occurred"] == True

    def test_sprouting_increases_synapse_potential(self):
        """Sprouting → more potential synapses"""
        system = StructuralPlasticitySystem()

        initial_potential = system.get_synapse_potential("A", "B_region")

        system.trigger_axonal_sprouting("A", "B_region", activity_level=0.9)

        final_potential = system.get_synapse_potential("A", "B_region")

        assert final_potential > initial_potential


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_synaptogenesis_event(self):
        """Process synaptogenesis event"""
        system = StructuralPlasticitySystem()

        result = system.process_event(
            event_type="synaptogenesis",
            pre_neuron="A",
            post_neuron="B",
            activity_level=0.9
        )

        assert "synapse_formed" in result

    def test_process_elimination_event(self):
        """Process synapse elimination event"""
        system = StructuralPlasticitySystem()

        result = system.process_event(
            event_type="eliminate_inactive",
            inactivity_days=30
        )

        assert "synapses_eliminated" in result


class TestGetState:
    """Test state retrieval"""

    def test_get_state_returns_structural_stats(self):
        """get_state returns structural plasticity statistics"""
        system = StructuralPlasticitySystem()

        system.trigger_synaptogenesis("A", "B", activity_level=0.9)

        state = system.get_state()

        assert "total_synapses" in state
        assert "spine_type_distribution" in state
        assert "synaptogenesis_rate" in state

    def test_get_state_serializable(self):
        """get_state returns JSON-serializable dict"""
        system = StructuralPlasticitySystem()

        state = system.get_state()

        import json
        json_str = json.dumps(state)
        assert json_str is not None
