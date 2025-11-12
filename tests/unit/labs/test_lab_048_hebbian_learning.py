"""
LAB_048: Hebbian Learning - Unit Tests

Neuroplasticity: "Neurons that fire together, wire together"

Key Papers:
- Hebb (1949) - The Organization of Behavior (classic Hebbian rule)
- Bi & Poo (1998) - Synaptic modifications in cultured hippocampal neurons (STDP)
- Caporale & Dan (2008) - Spike timing-dependent plasticity: a Hebbian learning rule
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Neuroplasticity.LAB_048_Hebbian_Learning.hebbian_learning_system import (
    HebbianLearningSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with default Hebbian parameters"""
        system = HebbianLearningSystem()
        assert system.learning_rate == 0.017
        assert system.temporal_window == 20.0  # ms
        assert len(system.synapses) == 0

    def test_custom_learning_rate(self):
        """System accepts custom learning rate"""
        system = HebbianLearningSystem(learning_rate=0.05)
        assert system.learning_rate == 0.05

    def test_custom_temporal_window(self):
        """System accepts custom temporal window"""
        system = HebbianLearningSystem(temporal_window=50.0)
        assert system.temporal_window == 50.0


class TestBasicHebbianRule:
    """Test basic Hebbian rule: 'Neurons that fire together, wire together'"""

    def test_simultaneous_firing_strengthens(self):
        """Simultaneous firing → synapse strengthens"""
        system = HebbianLearningSystem()

        system.create_synapse("A", "B", initial_strength=0.5)

        # Simultaneous activation (delta_t = 0)
        result = system.update_hebbian(
            pre_neuron="A",
            post_neuron="B",
            pre_spike_time=100.0,
            post_spike_time=100.0  # Same time
        )

        assert result["strength_increased"] == True
        assert result["new_strength"] > 0.5

    def test_correlated_firing_strengthens(self):
        """Correlated firing (pre before post) → synapse strengthens"""
        system = HebbianLearningSystem()

        system.create_synapse("A", "B", initial_strength=0.5)

        # Pre fires 10ms before post (positive correlation)
        result = system.update_hebbian(
            pre_neuron="A",
            post_neuron="B",
            pre_spike_time=100.0,
            post_spike_time=110.0  # Post 10ms later
        )

        assert result["strength_increased"] == True
        assert result["new_strength"] > 0.5

    def test_uncorrelated_firing_no_change(self):
        """Uncorrelated firing (outside window) → no change"""
        system = HebbianLearningSystem()

        system.create_synapse("A", "B", initial_strength=0.5)

        # Pre fires 100ms before post (outside temporal window)
        result = system.update_hebbian(
            pre_neuron="A",
            post_neuron="B",
            pre_spike_time=100.0,
            post_spike_time=200.0  # Post 100ms later
        )

        assert result["strength_increased"] == False
        assert abs(result["new_strength"] - 0.5) < 0.01  # Minimal change

    def test_repeated_correlated_firing_accumulates(self):
        """Repeated correlated firing → cumulative strengthening"""
        system = HebbianLearningSystem()

        system.create_synapse("A", "B", initial_strength=0.5)
        initial_strength = 0.5

        # 10 correlated firings
        for i in range(10):
            system.update_hebbian(
                pre_neuron="A",
                post_neuron="B",
                pre_spike_time=100.0 + i * 50,
                post_spike_time=110.0 + i * 50
            )

        final_strength = system.synapses[("A", "B")]["strength"]
        assert final_strength > initial_strength * 1.2  # At least 20% increase


class TestSTDP:
    """Test Spike-Timing-Dependent Plasticity"""

    def test_pre_before_post_ltp(self):
        """Pre before post (causal) → LTP (strengthening)"""
        system = HebbianLearningSystem()

        system.create_synapse("A", "B", initial_strength=0.5)

        # Pre fires 5ms before post
        result = system.update_hebbian(
            pre_neuron="A",
            post_neuron="B",
            pre_spike_time=100.0,
            post_spike_time=105.0
        )

        assert result["stdp_type"] == "LTP"
        assert result["new_strength"] > 0.5

    def test_post_before_pre_ltd(self):
        """Post before pre (anti-causal) → LTD (weakening)"""
        system = HebbianLearningSystem()

        system.create_synapse("A", "B", initial_strength=0.5)

        # Post fires 5ms before pre
        result = system.update_hebbian(
            pre_neuron="A",
            post_neuron="B",
            pre_spike_time=105.0,
            post_spike_time=100.0  # Post first
        )

        assert result["stdp_type"] == "LTD"
        assert result["new_strength"] < 0.5

    def test_stdp_asymmetry(self):
        """LTP (pre→post) stronger than LTD (post→pre)"""
        system = HebbianLearningSystem()

        # Synapse 1: Pre before post
        system.create_synapse("A", "B", initial_strength=0.5)
        result_ltp = system.update_hebbian("A", "B", 100.0, 105.0)

        # Synapse 2: Post before pre
        system.create_synapse("C", "D", initial_strength=0.5)
        result_ltd = system.update_hebbian("C", "D", 105.0, 100.0)

        # LTP should be stronger than LTD
        ltp_change = abs(result_ltp["new_strength"] - 0.5)
        ltd_change = abs(result_ltd["new_strength"] - 0.5)

        assert ltp_change > ltd_change

    def test_stdp_window_exponential_decay(self):
        """STDP effect decays exponentially with time difference"""
        system = HebbianLearningSystem()

        # Create 3 synapses with different delta_t
        system.create_synapse("A", "B", initial_strength=0.5)
        result_2ms = system.update_hebbian("A", "B", 100.0, 102.0)  # 2ms

        system.create_synapse("C", "D", initial_strength=0.5)
        result_10ms = system.update_hebbian("C", "D", 100.0, 110.0)  # 10ms

        system.create_synapse("E", "F", initial_strength=0.5)
        result_20ms = system.update_hebbian("E", "F", 100.0, 120.0)  # 20ms

        # Closer timing → stronger effect
        change_2ms = abs(result_2ms["new_strength"] - 0.5)
        change_10ms = abs(result_10ms["new_strength"] - 0.5)
        change_20ms = abs(result_20ms["new_strength"] - 0.5)

        assert change_2ms > change_10ms > change_20ms


class TestTemporalWindow:
    """Test temporal window for Hebbian learning"""

    def test_within_window_active(self):
        """Spikes within temporal window → learning active"""
        system = HebbianLearningSystem(temporal_window=20.0)

        system.create_synapse("A", "B", initial_strength=0.5)

        # 15ms difference (within 20ms window)
        result = system.update_hebbian("A", "B", 100.0, 115.0)

        assert result["within_window"] == True
        assert result["new_strength"] != 0.5

    def test_outside_window_inactive(self):
        """Spikes outside temporal window → no learning"""
        system = HebbianLearningSystem(temporal_window=20.0)

        system.create_synapse("A", "B", initial_strength=0.5)

        # 50ms difference (outside 20ms window)
        result = system.update_hebbian("A", "B", 100.0, 150.0)

        assert result["within_window"] == False
        assert abs(result["new_strength"] - 0.5) < 0.001

    def test_custom_window_size(self):
        """Custom temporal window changes learning range"""
        # Small window (10ms)
        system_small = HebbianLearningSystem(temporal_window=10.0)
        system_small.create_synapse("A", "B", initial_strength=0.5)
        result_small = system_small.update_hebbian("A", "B", 100.0, 115.0)

        # Large window (50ms)
        system_large = HebbianLearningSystem(temporal_window=50.0)
        system_large.create_synapse("C", "D", initial_strength=0.5)
        result_large = system_large.update_hebbian("C", "D", 100.0, 115.0)

        # 15ms is outside small window, inside large window
        assert result_small["within_window"] == False
        assert result_large["within_window"] == True


class TestCorrelationDetection:
    """Test pre/post neuron correlation detection"""

    def test_compute_correlation(self):
        """Compute correlation between pre/post spike trains"""
        system = HebbianLearningSystem()

        # High correlation spike trains
        pre_spikes = [100, 200, 300, 400]
        post_spikes = [105, 205, 305, 405]  # Consistently 5ms after pre

        correlation = system.compute_correlation(pre_spikes, post_spikes)

        assert correlation > 0.8  # High correlation

    def test_zero_correlation(self):
        """Uncorrelated spike trains → correlation near 0"""
        system = HebbianLearningSystem()

        # No correlation
        pre_spikes = [100, 200, 300, 400]
        post_spikes = [150, 250, 350, 450]  # Outside temporal window

        correlation = system.compute_correlation(pre_spikes, post_spikes)

        assert abs(correlation) < 0.2  # Near zero

    def test_negative_correlation(self):
        """Post before pre → negative correlation"""
        system = HebbianLearningSystem()

        # Negative correlation (post consistently before pre)
        pre_spikes = [105, 205, 305, 405]
        post_spikes = [100, 200, 300, 400]

        correlation = system.compute_correlation(pre_spikes, post_spikes)

        assert correlation < 0


class TestBidirectionalLearning:
    """Test bidirectional Hebbian learning (pre→post and post→pre)"""

    def test_pre_to_post_strengthening(self):
        """Pre→Post pathway strengthens with correlated firing"""
        system = HebbianLearningSystem()

        system.create_synapse("A", "B", initial_strength=0.5)

        # Pre fires before post (causal)
        for _ in range(5):
            system.update_hebbian("A", "B", 100.0, 105.0)

        synapse = system.synapses[("A", "B")]
        assert synapse["strength"] > 0.5

    def test_post_to_pre_weakening(self):
        """Post→Pre pathway weakens with reverse firing"""
        system = HebbianLearningSystem()

        system.create_synapse("A", "B", initial_strength=0.5)

        # Post fires before pre (anti-causal)
        for _ in range(5):
            system.update_hebbian("A", "B", 105.0, 100.0)

        synapse = system.synapses[("A", "B")]
        assert synapse["strength"] < 0.5

    def test_competitive_learning(self):
        """Multiple inputs compete for post neuron"""
        system = HebbianLearningSystem()

        # Input A: High correlation with B
        system.create_synapse("A", "B", initial_strength=0.5)
        for _ in range(10):
            system.update_hebbian("A", "B", 100.0, 105.0)

        # Input C: Low correlation with B
        system.create_synapse("C", "B", initial_strength=0.5)
        for _ in range(10):
            system.update_hebbian("C", "B", 100.0, 150.0)  # Outside window

        # A→B should be stronger than C→B
        strength_A_B = system.synapses[("A", "B")]["strength"]
        strength_C_B = system.synapses[("C", "B")]["strength"]

        assert strength_A_B > strength_C_B


class TestLearningRate:
    """Test learning rate modulation"""

    def test_high_learning_rate_fast_change(self):
        """High learning rate → fast synaptic change"""
        system_fast = HebbianLearningSystem(learning_rate=0.1)

        system_fast.create_synapse("A", "B", initial_strength=0.5)
        system_fast.update_hebbian("A", "B", 100.0, 105.0)

        strength_fast = system_fast.synapses[("A", "B")]["strength"]

        # Compare with slow learner
        system_slow = HebbianLearningSystem(learning_rate=0.001)
        system_slow.create_synapse("C", "D", initial_strength=0.5)
        system_slow.update_hebbian("C", "D", 100.0, 105.0)

        strength_slow = system_slow.synapses[("C", "D")]["strength"]

        # Fast should change more
        assert abs(strength_fast - 0.5) > abs(strength_slow - 0.5)

    def test_learning_rate_scales_linearly(self):
        """Learning rate scales change magnitude linearly"""
        system = HebbianLearningSystem(learning_rate=0.01)

        system.create_synapse("A", "B", initial_strength=0.5)
        result = system.update_hebbian("A", "B", 100.0, 105.0)

        change_1x = abs(result["new_strength"] - 0.5)

        # 2x learning rate should give ~2x change
        system2 = HebbianLearningSystem(learning_rate=0.02)
        system2.create_synapse("C", "D", initial_strength=0.5)
        result2 = system2.update_hebbian("C", "D", 100.0, 105.0)

        change_2x = abs(result2["new_strength"] - 0.5)

        assert 1.8 < (change_2x / change_1x) < 2.2  # ~2x

    def test_modulated_learning_rate(self):
        """Learning rate can be modulated by external factors"""
        system = HebbianLearningSystem(learning_rate=0.01)

        system.create_synapse("A", "B", initial_strength=0.5)

        # Normal learning
        result_normal = system.update_hebbian("A", "B", 100.0, 105.0)

        # Reset
        system.synapses[("A", "B")]["strength"] = 0.5

        # Modulated learning (e.g., dopamine signal)
        result_modulated = system.update_hebbian(
            "A", "B", 100.0, 105.0,
            learning_rate_multiplier=2.0
        )

        change_normal = abs(result_normal["new_strength"] - 0.5)
        change_modulated = abs(result_modulated["new_strength"] - 0.5)

        assert change_modulated > change_normal


class TestSaturation:
    """Test synaptic strength saturation (physiological limits)"""

    def test_upper_bound_saturation(self):
        """Synapse strength saturates at upper bound (1.0)"""
        system = HebbianLearningSystem(learning_rate=0.1)

        system.create_synapse("A", "B", initial_strength=0.9)

        # Many strengthening updates
        for _ in range(20):
            system.update_hebbian("A", "B", 100.0, 105.0)

        synapse = system.synapses[("A", "B")]
        assert synapse["strength"] <= 1.0

    def test_lower_bound_saturation(self):
        """Synapse strength saturates at lower bound (0.0)"""
        system = HebbianLearningSystem(learning_rate=0.1)

        system.create_synapse("A", "B", initial_strength=0.1)

        # Many weakening updates
        for _ in range(20):
            system.update_hebbian("A", "B", 105.0, 100.0)  # Post before pre

        synapse = system.synapses[("A", "B")]
        assert synapse["strength"] >= 0.0


class TestIntegration:
    """Test integration with other LABs"""

    def test_integration_with_synaptic_pruning(self):
        """LAB_047: Hebbian-strengthened synapses signal to pruning system"""
        system = HebbianLearningSystem()

        system.create_synapse("A", "B", initial_strength=0.5)

        # Hebbian strengthening
        for _ in range(10):
            system.update_hebbian("A", "B", 100.0, 105.0)

        # Compute Hebbian signal for pruning system
        hebbian_signal = system.compute_hebbian_signal("A", "B")

        assert hebbian_signal > 0.5  # Strong Hebbian signal

    def test_integration_with_skill_acquisition(self):
        """LAB_040: Skill acquisition modulates Hebbian learning rate"""
        system = HebbianLearningSystem(learning_rate=0.01)

        system.create_synapse("A", "B", initial_strength=0.5)

        # During skill acquisition: enhanced learning
        result = system.update_hebbian(
            "A", "B", 100.0, 105.0,
            skill_acquisition_active=True  # From LAB_040
        )

        assert result["learning_rate_enhanced"] == True

    def test_integration_with_ltp(self):
        """LAB_049: Strong Hebbian correlation triggers LTP"""
        system = HebbianLearningSystem()

        system.create_synapse("A", "B", initial_strength=0.5)

        # Many correlated firings
        for _ in range(20):
            system.update_hebbian("A", "B", 100.0, 105.0)

        # Check if LTP threshold reached
        synapse = system.synapses[("A", "B")]
        assert synapse.get("ltp_eligible", False) == True


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_hebbian_update_event(self):
        """Process Hebbian update event"""
        system = HebbianLearningSystem()

        system.create_synapse("A", "B", initial_strength=0.5)

        result = system.process_event(
            event_type="hebbian_update",
            pre_neuron="A",
            post_neuron="B",
            pre_spike_time=100.0,
            post_spike_time=105.0
        )

        assert "new_strength" in result

    def test_process_correlation_event(self):
        """Process correlation computation event"""
        system = HebbianLearningSystem()

        result = system.process_event(
            event_type="compute_correlation",
            pre_spikes=[100, 200, 300],
            post_spikes=[105, 205, 305]
        )

        assert "correlation" in result


class TestGetState:
    """Test state retrieval"""

    def test_get_state_returns_synapses(self):
        """get_state returns synapse statistics"""
        system = HebbianLearningSystem()

        system.create_synapse("A", "B", initial_strength=0.6)
        system.create_synapse("C", "D", initial_strength=0.8)

        state = system.get_state()

        assert "total_synapses" in state
        assert state["total_synapses"] == 2
        assert "average_strength" in state

    def test_get_state_serializable(self):
        """get_state returns JSON-serializable dict"""
        system = HebbianLearningSystem()

        state = system.get_state()

        import json
        json_str = json.dumps(state)
        assert json_str is not None
