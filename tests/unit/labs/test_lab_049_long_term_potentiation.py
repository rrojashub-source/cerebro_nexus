"""
LAB_049: Long-Term Potentiation (LTP) - Unit Tests

Neuroplasticity: "The cellular basis of learning and memory"

Key Papers:
- Bliss & Lømo (1973) - Long-lasting potentiation of synaptic transmission
- Malenka & Bear (2004) - LTP and LTD: an embarrassment of riches
- Lynch (2004) - Long-term potentiation and memory
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Neuroplasticity.LAB_049_Long_Term_Potentiation.ltp_system import (
    LTPSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with default LTP parameters"""
        system = LTPSystem()
        assert system.ltp_threshold == 0.7
        assert system.ltp_duration_hours == 24.0
        assert len(system.synapses) == 0

    def test_custom_ltp_threshold(self):
        """System accepts custom LTP threshold"""
        system = LTPSystem(ltp_threshold=0.8)
        assert system.ltp_threshold == 0.8

    def test_custom_ltp_duration(self):
        """System accepts custom LTP duration"""
        system = LTPSystem(ltp_duration_hours=48.0)
        assert system.ltp_duration_hours == 48.0


class TestLTPInduction:
    """Test LTP induction mechanisms"""

    def test_high_frequency_stimulation_induces_ltp(self):
        """High-frequency stimulation (tetanus) → LTP"""
        system = LTPSystem()

        system.create_synapse("A", "B", initial_strength=0.6)

        # High-frequency stimulation (100 Hz for 1 second)
        result = system.induce_ltp(
            pre_neuron="A",
            post_neuron="B",
            stimulation_frequency=100.0,  # Hz
            stimulation_duration=1.0  # seconds
        )

        assert result["ltp_induced"] == True
        synapse = system.synapses[("A", "B")]
        assert synapse.get("ltp_potentiated", False) == True

    def test_low_frequency_stimulation_no_ltp(self):
        """Low-frequency stimulation → no LTP"""
        system = LTPSystem()

        system.create_synapse("A", "B", initial_strength=0.6)

        # Low-frequency stimulation (1 Hz)
        result = system.induce_ltp(
            pre_neuron="A",
            post_neuron="B",
            stimulation_frequency=1.0,
            stimulation_duration=1.0
        )

        assert result["ltp_induced"] == False

    def test_hebbian_signal_facilitates_ltp(self):
        """Strong Hebbian signal lowers LTP threshold"""
        system = LTPSystem()

        system.create_synapse("A", "B", initial_strength=0.5)

        # With strong Hebbian signal (from LAB_048)
        result = system.induce_ltp(
            pre_neuron="A",
            post_neuron="B",
            stimulation_frequency=100.0,
            stimulation_duration=1.0,
            hebbian_signal=0.9  # Strong Hebbian signal
        )

        assert result["ltp_induced"] == True

    def test_tetanus_protocol_standard(self):
        """Standard tetanus protocol (100 Hz, 1 second) → LTP"""
        system = LTPSystem()

        system.create_synapse("A", "B", initial_strength=0.6)

        # Standard tetanus
        result = system.apply_tetanus("A", "B")

        assert result["ltp_induced"] == True
        synapse = system.synapses[("A", "B")]
        assert synapse["ltp_potentiated"] == True


class TestLTPTypes:
    """Test Early-phase LTP (E-LTP) vs Late-phase LTP (L-LTP)"""

    def test_early_phase_ltp_short_duration(self):
        """E-LTP (single tetanus) → 1-3 hours duration"""
        system = LTPSystem()

        system.create_synapse("A", "B", initial_strength=0.6)

        # Single tetanus → E-LTP
        system.apply_tetanus("A", "B", protocol="single")

        synapse = system.synapses[("A", "B")]
        assert synapse["ltp_phase"] == "early"
        assert synapse["ltp_duration_hours"] <= 3.0

    def test_late_phase_ltp_long_duration(self):
        """L-LTP (spaced tetanus + protein synthesis) → >3 hours"""
        system = LTPSystem()

        system.create_synapse("A", "B", initial_strength=0.6)

        # Spaced tetanus + protein synthesis → L-LTP
        system.apply_tetanus("A", "B", protocol="spaced", protein_synthesis=True)

        synapse = system.synapses[("A", "B")]
        assert synapse["ltp_phase"] == "late"
        assert synapse["ltp_duration_hours"] > 3.0

    def test_protein_synthesis_required_for_late_ltp(self):
        """L-LTP requires protein synthesis"""
        system = LTPSystem()

        system.create_synapse("A", "B", initial_strength=0.6)

        # Spaced tetanus WITHOUT protein synthesis → E-LTP only
        system.apply_tetanus("A", "B", protocol="spaced", protein_synthesis=False)

        synapse = system.synapses[("A", "B")]
        assert synapse["ltp_phase"] == "early"  # Cannot transition to late

    def test_transition_early_to_late_ltp(self):
        """E-LTP can transition to L-LTP with protein synthesis"""
        system = LTPSystem()

        system.create_synapse("A", "B", initial_strength=0.6)

        # First: E-LTP
        system.apply_tetanus("A", "B", protocol="single")
        assert system.synapses[("A", "B")]["ltp_phase"] == "early"

        # Then: Additional stimulation + protein synthesis → L-LTP
        system.apply_tetanus("A", "B", protocol="spaced", protein_synthesis=True)
        assert system.synapses[("A", "B")]["ltp_phase"] == "late"


class TestLTPMagnitude:
    """Test LTP strength amplification"""

    def test_ltp_amplifies_synaptic_strength(self):
        """LTP induction → significant strength increase"""
        system = LTPSystem()

        system.create_synapse("A", "B", initial_strength=0.5)
        initial_strength = 0.5

        system.apply_tetanus("A", "B")

        synapse = system.synapses[("A", "B")]
        final_strength = synapse["strength"]

        # LTP should increase strength by at least 50%
        assert final_strength > initial_strength * 1.5

    def test_ltp_magnitude_dose_dependent(self):
        """Stronger stimulation → larger LTP magnitude"""
        system = LTPSystem()

        # Weak stimulation
        system.create_synapse("A", "B", initial_strength=0.5)
        system.induce_ltp("A", "B", stimulation_frequency=100.0, stimulation_duration=0.5)
        strength_weak = system.synapses[("A", "B")]["strength"]

        # Strong stimulation
        system.create_synapse("C", "D", initial_strength=0.5)
        system.induce_ltp("C", "D", stimulation_frequency=100.0, stimulation_duration=2.0)
        strength_strong = system.synapses[("C", "D")]["strength"]

        assert strength_strong > strength_weak

    def test_ltp_saturation_at_upper_bound(self):
        """LTP saturates at maximum strength (1.0)"""
        system = LTPSystem()

        system.create_synapse("A", "B", initial_strength=0.9)

        # Multiple tetanus
        for _ in range(5):
            system.apply_tetanus("A", "B")

        synapse = system.synapses[("A", "B")]
        assert synapse["strength"] <= 1.0


class TestLTPDecay:
    """Test LTP decay over time"""

    def test_early_ltp_decays_after_3_hours(self):
        """E-LTP decays after 1-3 hours"""
        system = LTPSystem()

        system.create_synapse("A", "B", initial_strength=0.6)
        system.apply_tetanus("A", "B", protocol="single")

        # Simulate 4 hours passing
        system.apply_decay(hours=4.0)

        synapse = system.synapses[("A", "B")]
        # E-LTP should be significantly decayed
        assert synapse["ltp_strength"] < 0.5

    def test_late_ltp_persists_24_hours(self):
        """L-LTP persists for 24+ hours"""
        system = LTPSystem()

        system.create_synapse("A", "B", initial_strength=0.6)
        system.apply_tetanus("A", "B", protocol="spaced", protein_synthesis=True)

        initial_strength = system.synapses[("A", "B")]["ltp_strength"]

        # Simulate 24 hours passing
        system.apply_decay(hours=24.0)

        synapse = system.synapses[("A", "B")]
        # L-LTP should be minimally decayed
        assert synapse["ltp_strength"] > initial_strength * 0.8  # <20% decay

    def test_ltp_decay_rate_phase_dependent(self):
        """E-LTP decays faster than L-LTP"""
        system = LTPSystem()

        # E-LTP synapse
        system.create_synapse("A", "B", initial_strength=0.6)
        system.apply_tetanus("A", "B", protocol="single")
        early_initial = system.synapses[("A", "B")]["ltp_strength"]

        # L-LTP synapse
        system.create_synapse("C", "D", initial_strength=0.6)
        system.apply_tetanus("C", "D", protocol="spaced", protein_synthesis=True)
        late_initial = system.synapses[("C", "D")]["ltp_strength"]

        # Apply same decay time
        system.apply_decay(hours=6.0)

        early_final = system.synapses[("A", "B")]["ltp_strength"]
        late_final = system.synapses[("C", "D")]["ltp_strength"]

        # E-LTP should decay more
        early_decay_pct = (early_initial - early_final) / early_initial
        late_decay_pct = (late_initial - late_final) / late_initial

        assert early_decay_pct > late_decay_pct


class TestLTD:
    """Test Long-Term Depression (LTD)"""

    def test_low_frequency_stimulation_induces_ltd(self):
        """Low-frequency stimulation (1 Hz) → LTD"""
        system = LTPSystem()

        system.create_synapse("A", "B", initial_strength=0.6)

        result = system.induce_ltd(
            pre_neuron="A",
            post_neuron="B",
            stimulation_frequency=1.0,
            stimulation_duration=15.0  # 15 minutes
        )

        assert result["ltd_induced"] == True

    def test_ltd_weakens_synaptic_strength(self):
        """LTD induction → synaptic weakening"""
        system = LTPSystem()

        system.create_synapse("A", "B", initial_strength=0.6)
        initial_strength = 0.6

        system.induce_ltd("A", "B", 1.0, 15.0)

        synapse = system.synapses[("A", "B")]
        final_strength = synapse["strength"]

        assert final_strength < initial_strength

    def test_ltd_prevents_ltp_induction(self):
        """Active LTD prevents LTP induction"""
        system = LTPSystem()

        system.create_synapse("A", "B", initial_strength=0.6)

        # First: Induce LTD
        system.induce_ltd("A", "B", 1.0, 15.0)

        # Then: Try to induce LTP
        result = system.induce_ltp("A", "B", 100.0, 1.0)

        # LTP should fail or be attenuated
        assert result["ltp_magnitude"] < 0.5  # Attenuated


class TestIntegration:
    """Test integration with other LABs"""

    def test_integration_with_hebbian_learning(self):
        """LAB_048: Hebbian signal facilitates LTP induction"""
        system = LTPSystem()

        system.create_synapse("A", "B", initial_strength=0.5)

        # Strong Hebbian signal reduces LTP threshold
        result = system.induce_ltp(
            "A", "B", 80.0, 1.0,
            hebbian_signal=0.9
        )

        assert result["ltp_induced"] == True

    def test_integration_with_synaptic_pruning(self):
        """LAB_047: LTP-potentiated synapses resist pruning"""
        system = LTPSystem()

        system.create_synapse("A", "B", initial_strength=0.6)
        system.apply_tetanus("A", "B")

        # Verify pruning resistance flag is set
        synapse = system.synapses[("A", "B")]
        assert synapse["ltp_potentiated"] == True
        assert synapse.get("resists_pruning", False) == True

    def test_integration_with_skill_acquisition(self):
        """LAB_040: Skill acquisition modulates LTP threshold"""
        system = LTPSystem()

        system.create_synapse("A", "B", initial_strength=0.5)

        # During skill acquisition: enhanced LTP induction
        result = system.induce_ltp(
            "A", "B", 80.0, 1.0,
            skill_acquisition_active=True
        )

        assert result["ltp_induced"] == True
        assert result["threshold_modulated"] == True


class TestCooperativity:
    """Test LTP cooperativity (multiple inputs)"""

    def test_multiple_inputs_cooperate_for_ltp(self):
        """Multiple weak inputs can cooperate to induce LTP"""
        system = LTPSystem()

        # Create 3 weak inputs to neuron B
        system.create_synapse("A1", "B", initial_strength=0.4)
        system.create_synapse("A2", "B", initial_strength=0.4)
        system.create_synapse("A3", "B", initial_strength=0.4)

        # Simultaneous stimulation of all 3
        result = system.induce_ltp_cooperative(
            pre_neurons=["A1", "A2", "A3"],
            post_neuron="B",
            stimulation_frequency=100.0,
            stimulation_duration=1.0
        )

        assert result["ltp_induced"] == True

    def test_single_weak_input_insufficient(self):
        """Single weak input cannot induce LTP alone"""
        system = LTPSystem()

        system.create_synapse("A", "B", initial_strength=0.3)

        result = system.induce_ltp("A", "B", 100.0, 1.0)

        assert result["ltp_induced"] == False


class TestAssociativity:
    """Test LTP associativity (Hebbian coincidence)"""

    def test_associative_ltp(self):
        """Weak input + strong input → both potentiated"""
        system = LTPSystem()

        # Weak input
        system.create_synapse("Weak", "B", initial_strength=0.3)
        # Strong input
        system.create_synapse("Strong", "B", initial_strength=0.8)

        # Simultaneous activation
        result = system.induce_ltp_associative(
            weak_pre="Weak",
            strong_pre="Strong",
            post_neuron="B",
            stimulation_frequency=100.0,
            stimulation_duration=1.0
        )

        # Both should be potentiated
        assert result["weak_input_potentiated"] == True
        assert result["strong_input_potentiated"] == True


class TestInputSpecificity:
    """Test LTP input specificity"""

    def test_ltp_is_input_specific(self):
        """LTP only affects stimulated pathway"""
        system = LTPSystem()

        # Two inputs to same neuron
        system.create_synapse("A", "C", initial_strength=0.5)
        system.create_synapse("B", "C", initial_strength=0.5)

        # Only stimulate A→C
        system.apply_tetanus("A", "C")

        # A→C should be potentiated, B→C should not
        synapse_A_C = system.synapses[("A", "C")]
        synapse_B_C = system.synapses[("B", "C")]

        assert synapse_A_C["ltp_potentiated"] == True
        assert synapse_B_C.get("ltp_potentiated", False) == False


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_ltp_induction_event(self):
        """Process LTP induction event"""
        system = LTPSystem()

        system.create_synapse("A", "B", initial_strength=0.6)

        result = system.process_event(
            event_type="induce_ltp",
            pre_neuron="A",
            post_neuron="B",
            stimulation_frequency=100.0,
            stimulation_duration=1.0
        )

        assert "ltp_induced" in result

    def test_process_ltd_induction_event(self):
        """Process LTD induction event"""
        system = LTPSystem()

        system.create_synapse("A", "B", initial_strength=0.6)

        result = system.process_event(
            event_type="induce_ltd",
            pre_neuron="A",
            post_neuron="B",
            stimulation_frequency=1.0,
            stimulation_duration=15.0
        )

        assert "ltd_induced" in result


class TestGetState:
    """Test state retrieval"""

    def test_get_state_returns_ltp_statistics(self):
        """get_state returns LTP/LTD statistics"""
        system = LTPSystem()

        system.create_synapse("A", "B", initial_strength=0.6)
        system.apply_tetanus("A", "B")

        state = system.get_state()

        assert "total_synapses" in state
        assert "ltp_potentiated_count" in state
        assert "average_ltp_strength" in state

    def test_get_state_serializable(self):
        """get_state returns JSON-serializable dict"""
        system = LTPSystem()

        state = system.get_state()

        import json
        json_str = json.dumps(state)
        assert json_str is not None
