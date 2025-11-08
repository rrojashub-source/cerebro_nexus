"""
LAB_017: GABA/Glutamate Balance - Test Suite

TDD (Test-Driven Development) approach:
1. RED: Write failing tests first
2. GREEN: Implement code to pass tests
3. REFACTOR: Optimize while keeping tests passing

Biological Inspiration:
- Excitatory (Glutamate) and Inhibitory (GABA) neurons
- Destexhe & Marder (2004) - "Excitation-inhibition balance"

Core Functions:
- Excitation/Inhibition (E/I) balance management
- Homeostatic control (auto-regulation toward optimal)
- Network gain modulation (signal amplification)
- Stability maintenance (prevents runaway activation)

Test Phases:
- Phase 1: Core E/I Tests (basic functionality)
- Phase 2: Integration Tests (with other LABs)
- Phase 3: Edge Cases & Homeostatic Control
"""

import pytest
import sys
from pathlib import Path

# Add experiments to path
experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_4_Neurochemistry_Full.LAB_017_GABA_Glutamate_Balance import GABAGlutamateSystem


# ============================================================================
# PHASE 1: CORE E/I BALANCE TESTS
# ============================================================================

class TestBasicEIBalance:
    """Test 1: Basic Excitation/Inhibition Levels"""

    def test_baseline_ei_ratio(self):
        """E/I ratio should start at configured baseline"""
        gaba_glut = GABAGlutamateSystem(
            baseline_glutamate=0.6,
            baseline_gaba=0.4
        )

        ei_ratio = gaba_glut.compute_ei_ratio()

        # Expected: 0.6 / 0.4 = 1.5
        assert ei_ratio == pytest.approx(1.5, rel=0.1)

    def test_excitation_increases_with_activation(self):
        """Activation should increase glutamate (excitation)"""
        gaba_glut = GABAGlutamateSystem(baseline_glutamate=0.5)

        initial_glutamate = gaba_glut.glutamate_level

        gaba_glut.update_excitation(activation=0.8, stress=0.3)

        assert gaba_glut.glutamate_level > initial_glutamate

    def test_inhibition_increases_with_stability_demand(self):
        """Stability demand should increase GABA (inhibition)"""
        gaba_glut = GABAGlutamateSystem(baseline_gaba=0.4)

        initial_gaba = gaba_glut.gaba_level

        gaba_glut.update_inhibition(stability_demand=0.9)

        assert gaba_glut.gaba_level > initial_gaba

    def test_stress_increases_excitation(self):
        """High stress should increase glutamate"""
        gaba_glut = GABAGlutamateSystem()

        initial_glutamate = gaba_glut.glutamate_level

        gaba_glut.update_excitation(activation=0.5, stress=0.9)

        assert gaba_glut.glutamate_level > initial_glutamate

    def test_levels_bounded(self):
        """Glutamate and GABA should be bounded [0, 1]"""
        gaba_glut = GABAGlutamateSystem()

        # Extreme activation
        for _ in range(20):
            gaba_glut.update_excitation(activation=1.0, stress=1.0)
            gaba_glut.update_inhibition(stability_demand=1.0)

        assert 0.0 <= gaba_glut.glutamate_level <= 1.0
        assert 0.0 <= gaba_glut.gaba_level <= 1.0


class TestEIRatioComputation:
    """Test 2: E/I Ratio Computation"""

    def test_ei_ratio_formula(self):
        """E/I ratio should follow glutamate / (gaba + epsilon)"""
        gaba_glut = GABAGlutamateSystem()

        # Manually set levels
        gaba_glut.glutamate_level = 0.8
        gaba_glut.gaba_level = 0.4

        ei_ratio = gaba_glut.compute_ei_ratio()

        # Expected: 0.8 / (0.4 + 0.01) ≈ 1.95
        expected = 0.8 / (0.4 + 0.01)
        assert ei_ratio == pytest.approx(expected, rel=0.05)

    def test_ei_ratio_increases_with_excitation(self):
        """Higher glutamate should increase E/I ratio"""
        gaba_glut = GABAGlutamateSystem()

        # Low excitation
        gaba_glut.glutamate_level = 0.4
        gaba_glut.gaba_level = 0.5
        ratio_low = gaba_glut.compute_ei_ratio()

        # High excitation
        gaba_glut.glutamate_level = 0.9
        gaba_glut.gaba_level = 0.5
        ratio_high = gaba_glut.compute_ei_ratio()

        assert ratio_high > ratio_low

    def test_ei_ratio_decreases_with_inhibition(self):
        """Higher GABA should decrease E/I ratio"""
        gaba_glut = GABAGlutamateSystem()

        # Low inhibition
        gaba_glut.glutamate_level = 0.7
        gaba_glut.gaba_level = 0.3
        ratio_low_gaba = gaba_glut.compute_ei_ratio()

        # High inhibition
        gaba_glut.glutamate_level = 0.7
        gaba_glut.gaba_level = 0.8
        ratio_high_gaba = gaba_glut.compute_ei_ratio()

        assert ratio_high_gaba < ratio_low_gaba


class TestStabilityIndex:
    """Test 3: Stability Index Computation"""

    def test_optimal_ratio_gives_high_stability(self):
        """Being at optimal E/I ratio should give high stability"""
        gaba_glut = GABAGlutamateSystem(optimal_ratio=0.75)

        # Set E/I ratio = 0.75 (optimal)
        # If optimal = 0.75, set glutamate = 0.75 * (gaba + epsilon)
        # Let gaba = 0.5, then glutamate = 0.75 * (0.5 + 0.01) = 0.3825
        gaba_glut.glutamate_level = 0.38
        gaba_glut.gaba_level = 0.5

        stability = gaba_glut.compute_stability_index()

        # Near optimal → high stability (close to 1.0)
        assert stability > 0.8

    def test_extreme_imbalance_gives_low_stability(self):
        """Large deviation from optimal should give low stability"""
        gaba_glut = GABAGlutamateSystem(optimal_ratio=0.75)

        # Very high E/I ratio (extreme excitation)
        gaba_glut.glutamate_level = 0.95
        gaba_glut.gaba_level = 0.2

        stability = gaba_glut.compute_stability_index()

        # Far from optimal → low stability
        assert stability < 0.5

    def test_stability_scales_with_distance(self):
        """Stability should decrease as distance from optimal increases"""
        gaba_glut = GABAGlutamateSystem(optimal_ratio=0.75)

        # Slightly off optimal
        gaba_glut.glutamate_level = 0.4
        gaba_glut.gaba_level = 0.5
        stability_near = gaba_glut.compute_stability_index()

        # Far from optimal
        gaba_glut.glutamate_level = 0.9
        gaba_glut.gaba_level = 0.3
        stability_far = gaba_glut.compute_stability_index()

        assert stability_near > stability_far


class TestHomeostaticControl:
    """Test 4: Homeostatic Control Mechanism"""

    def test_high_ei_ratio_triggers_gaba_increase(self):
        """High E/I ratio should trigger homeostatic GABA increase"""
        gaba_glut = GABAGlutamateSystem(optimal_ratio=0.75)

        # Set high E/I ratio (too much excitation)
        gaba_glut.glutamate_level = 0.9
        gaba_glut.gaba_level = 0.3

        initial_gaba = gaba_glut.gaba_level

        # Apply homeostatic control
        gaba_glut.apply_homeostatic_control()

        # GABA should increase to reduce E/I ratio
        assert gaba_glut.gaba_level > initial_gaba

    def test_low_ei_ratio_triggers_glutamate_increase(self):
        """Low E/I ratio should trigger homeostatic glutamate increase"""
        gaba_glut = GABAGlutamateSystem(optimal_ratio=0.75)

        # Set low E/I ratio (too much inhibition)
        gaba_glut.glutamate_level = 0.3
        gaba_glut.gaba_level = 0.8

        initial_glutamate = gaba_glut.glutamate_level

        # Apply homeostatic control
        gaba_glut.apply_homeostatic_control()

        # Glutamate should increase to raise E/I ratio
        assert gaba_glut.glutamate_level > initial_glutamate

    def test_homeostatic_convergence(self):
        """Repeated homeostatic control should converge toward optimal"""
        gaba_glut = GABAGlutamateSystem(optimal_ratio=0.75)

        # Start with imbalance
        gaba_glut.glutamate_level = 0.9
        gaba_glut.gaba_level = 0.2

        initial_ei_ratio = gaba_glut.compute_ei_ratio()

        # Apply homeostatic control multiple times
        for _ in range(20):
            gaba_glut.apply_homeostatic_control()

        final_ei_ratio = gaba_glut.compute_ei_ratio()

        # Should move closer to optimal (0.75)
        initial_distance = abs(initial_ei_ratio - 0.75)
        final_distance = abs(final_ei_ratio - 0.75)

        assert final_distance < initial_distance


class TestNetworkGain:
    """Test 5: Network Gain Modulation"""

    def test_high_ei_ratio_increases_gain(self):
        """High E/I ratio should increase network gain (amplification)"""
        gaba_glut = GABAGlutamateSystem()

        # Low E/I ratio
        gaba_glut.glutamate_level = 0.4
        gaba_glut.gaba_level = 0.7
        gain_low = gaba_glut.compute_network_gain()

        # High E/I ratio
        gaba_glut.glutamate_level = 0.9
        gaba_glut.gaba_level = 0.3
        gain_high = gaba_glut.compute_network_gain()

        assert gain_high > gain_low

    def test_optimal_ei_gives_moderate_gain(self):
        """Optimal E/I ratio should give moderate network gain"""
        gaba_glut = GABAGlutamateSystem(optimal_ratio=0.75)

        # Set near optimal
        gaba_glut.glutamate_level = 0.38
        gaba_glut.gaba_level = 0.5

        gain = gaba_glut.compute_network_gain()

        # Should be moderate (around 0.7-0.8 range)
        assert 0.5 < gain < 1.2


class TestFullEventProcessing:
    """Test 6: Full Event Processing"""

    def test_process_event_returns_complete_state(self):
        """process_event should return all E/I outputs"""
        gaba_glut = GABAGlutamateSystem()

        result = gaba_glut.process_event(
            activation=0.7,
            stability_demand=0.5
        )

        # Verify all expected keys
        assert "glutamate_level" in result
        assert "gaba_level" in result
        assert "ei_ratio" in result
        assert "stability_index" in result
        assert "network_gain" in result

    def test_high_activation_increases_excitation(self):
        """High activation should increase glutamate level"""
        gaba_glut = GABAGlutamateSystem(baseline_glutamate=0.5)

        result = gaba_glut.process_event(activation=0.9, stability_demand=0.3)

        # Glutamate should be elevated
        assert result["glutamate_level"] > 0.5

    def test_high_stability_demand_increases_inhibition(self):
        """High stability demand should increase GABA level"""
        gaba_glut = GABAGlutamateSystem(baseline_gaba=0.4)

        result = gaba_glut.process_event(activation=0.5, stability_demand=0.9)

        # GABA should be elevated
        assert result["gaba_level"] > 0.4

    def test_event_counter(self):
        """Should correctly count total events"""
        gaba_glut = GABAGlutamateSystem()

        for i in range(6):
            gaba_glut.process_event(activation=0.5, stability_demand=0.5)

        assert gaba_glut.total_events == 6


# ============================================================================
# PHASE 2: INTEGRATION TESTS
# ============================================================================

class TestIntegrationWithStressSystems:
    """Test 7: Integration with Stress Systems (Norepinephrine)"""

    def test_stress_increases_excitation(self):
        """
        High stress should increase excitation (glutamate)

        Stress (NE) → increased glutamate → higher E/I ratio
        """
        gaba_glut = GABAGlutamateSystem()

        initial_glutamate = gaba_glut.glutamate_level

        # Simulate stress event (high activation + stress)
        gaba_glut.update_excitation(activation=0.6, stress=0.9)

        assert gaba_glut.glutamate_level > initial_glutamate


class TestIntegrationWithCalming:
    """Test 8: Integration with Calming Systems (Serotonin)"""

    def test_stability_demand_increases_inhibition(self):
        """
        Stability/calming need should increase inhibition (GABA)

        High serotonin → stability demand → increased GABA
        """
        gaba_glut = GABAGlutamateSystem()

        initial_gaba = gaba_glut.gaba_level

        # Simulate calming need (high stability demand)
        gaba_glut.update_inhibition(stability_demand=0.9)

        assert gaba_glut.gaba_level > initial_gaba


class TestSystemStability:
    """Test 9: System-Wide Stability Control"""

    def test_homeostatic_control_maintains_stability(self):
        """
        GABA/Glutamate should prevent runaway activation in other systems

        E/I balance acts as global stability regulator
        """
        gaba_glut = GABAGlutamateSystem(optimal_ratio=0.75)

        # Create imbalance
        gaba_glut.glutamate_level = 0.95
        gaba_glut.gaba_level = 0.25

        # Apply homeostasis multiple times (need more iterations for extreme imbalance)
        for _ in range(30):
            gaba_glut.apply_homeostatic_control()

        # Should converge toward optimal
        final_ei_ratio = gaba_glut.compute_ei_ratio()
        assert abs(final_ei_ratio - 0.75) < 0.3


# ============================================================================
# PHASE 3: EDGE CASES & HOMEOSTATIC CONTROL
# ============================================================================

class TestEdgeCases:
    """Test 10: Edge Cases"""

    def test_extreme_imbalance_recovery(self):
        """System should recover from extreme E/I imbalance"""
        gaba_glut = GABAGlutamateSystem()

        # Create extreme imbalance
        gaba_glut.glutamate_level = 0.98
        gaba_glut.gaba_level = 0.05

        initial_stability = gaba_glut.compute_stability_index()

        # Apply homeostasis
        for _ in range(25):
            gaba_glut.apply_homeostatic_control()

        final_stability = gaba_glut.compute_stability_index()

        # Stability should improve
        assert final_stability > initial_stability

    def test_zero_activation(self):
        """System should handle zero activation"""
        gaba_glut = GABAGlutamateSystem()

        result = gaba_glut.process_event(activation=0.0, stability_demand=0.5)

        # Should work normally
        assert 0.0 <= result["glutamate_level"] <= 1.0

    def test_zero_stability_demand(self):
        """System should handle zero stability demand"""
        gaba_glut = GABAGlutamateSystem()

        result = gaba_glut.process_event(activation=0.5, stability_demand=0.0)

        # Should work normally
        assert 0.0 <= result["gaba_level"] <= 1.0


class TestOscillatoryBehavior:
    """Test 11: Oscillatory Behavior Control"""

    def test_rapid_fluctuations_stabilize(self):
        """Rapid activation fluctuations should stabilize via homeostasis"""
        gaba_glut = GABAGlutamateSystem()

        # Rapid alternating high/low activation
        for i in range(30):
            activation = 1.0 if i % 2 == 0 else 0.0
            gaba_glut.process_event(activation=activation, stability_demand=0.5)

        # E/I ratio should remain stable (not oscillating wildly)
        ei_ratio = gaba_glut.compute_ei_ratio()
        assert 0.3 < ei_ratio < 2.0

    def test_sustained_high_activity_dampened(self):
        """Prolonged high activity should be dampened by homeostasis"""
        gaba_glut = GABAGlutamateSystem()

        initial_ei_ratio = gaba_glut.compute_ei_ratio()

        # Sustained high activation
        for _ in range(20):
            gaba_glut.process_event(activation=0.95, stability_demand=0.3)

        final_ei_ratio = gaba_glut.compute_ei_ratio()

        # Homeostasis should prevent extreme E/I ratio
        assert final_ei_ratio < 3.0  # Reasonable upper bound


class TestStatePersistence:
    """Test 12: State Persistence"""

    def test_get_state_returns_complete_state(self):
        """get_state should return all state variables"""
        gaba_glut = GABAGlutamateSystem()

        # Generate some history
        for i in range(5):
            gaba_glut.process_event(activation=0.6, stability_demand=0.5)

        state = gaba_glut.get_state()

        # Verify all expected keys
        assert "glutamate_level" in state
        assert "gaba_level" in state
        assert "glutamate_history" in state
        assert "gaba_history" in state
        assert "ei_ratio" in state
        assert "ei_ratio_mean" in state
        assert "stability_index" in state
        assert "network_gain" in state
        assert "total_events" in state

    def test_state_consistency(self):
        """State should be consistent across calls"""
        gaba_glut = GABAGlutamateSystem()

        gaba_glut.process_event(activation=0.7, stability_demand=0.5)

        state1 = gaba_glut.get_state()
        state2 = gaba_glut.get_state()

        # State should be identical if no new events
        assert state1["total_events"] == state2["total_events"]
        assert state1["glutamate_level"] == state2["glutamate_level"]
        assert state1["gaba_level"] == state2["gaba_level"]


class TestLongTermDynamics:
    """Test 13: Long-term Dynamics"""

    def test_prolonged_inhibition_recovers(self):
        """Prolonged high GABA should eventually rebalance"""
        gaba_glut = GABAGlutamateSystem()

        # Create high inhibition
        for _ in range(10):
            gaba_glut.update_inhibition(stability_demand=0.9)

        low_ei_ratio = gaba_glut.compute_ei_ratio()

        # Apply homeostasis
        for _ in range(20):
            gaba_glut.apply_homeostatic_control()

        final_ei_ratio = gaba_glut.compute_ei_ratio()

        # Should move toward optimal (increase E/I ratio)
        assert final_ei_ratio > low_ei_ratio


# ============================================================================
# FIXTURES & UTILITIES
# ============================================================================

@pytest.fixture
def fresh_gaba_glutamate():
    """Fixture: Fresh GABAGlutamateSystem instance"""
    return GABAGlutamateSystem(
        baseline_glutamate=0.6,
        baseline_gaba=0.4,
        optimal_ratio=0.75,
        homeostatic_gain=0.3,
        adaptation_rate=0.1,
        history_window=15
    )


@pytest.fixture
def imbalanced_system():
    """Fixture: System with E/I imbalance"""
    gaba_glut = GABAGlutamateSystem()

    # Create imbalance (high excitation)
    gaba_glut.glutamate_level = 0.9
    gaba_glut.gaba_level = 0.3

    return gaba_glut


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
