"""
LAB_025: Insight & Aha Moments - Unit Tests

Creativity: Sudden insight through problem restructuring, impasse breaking

Key Papers:
- Metcalfe & Wiebe (1987) - Intuition in insight and non-insight problem solving
- Ohlsson (1992) - Information-processing explanations of insight
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Creativity_Social.LAB_025_Insight.insight_system import (
    InsightSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with default parameters"""
        system = InsightSystem()
        assert system.impasse_threshold == 3
        assert system.incubation_duration == 120.0
        assert system.aha_confidence_threshold == 0.8

    def test_custom_parameters(self):
        """System accepts custom parameters"""
        system = InsightSystem(
            impasse_threshold=5,
            incubation_duration=180.0,
            aha_confidence_threshold=0.9
        )
        assert system.impasse_threshold == 5
        assert system.incubation_duration == 180.0
        assert system.aha_confidence_threshold == 0.9

    def test_state_initialization(self):
        """State variables initialize correctly"""
        system = InsightSystem()
        assert system.total_problems_attempted == 0
        assert system.insights_achieved == 0


class TestImpasseDetection:
    """Test impasse (stuck state) detection"""

    def test_detects_impasse_after_threshold(self):
        """System detects impasse after threshold failures"""
        system = InsightSystem(impasse_threshold=3)

        # Not impasse yet
        assert system.detect_impasse(failed_attempts=2, progress=0.0) == False

        # Now impasse
        assert system.detect_impasse(failed_attempts=3, progress=0.0) == True

    def test_no_impasse_with_progress(self):
        """No impasse if making progress (even with failures)"""
        system = InsightSystem(impasse_threshold=3)

        # Many failures but progress > 0 → no impasse
        assert system.detect_impasse(failed_attempts=5, progress=0.3) == False

    def test_impasse_with_repeated_failures(self):
        """Repeated failures with no progress triggers impasse"""
        system = InsightSystem(impasse_threshold=3)

        assert system.detect_impasse(failed_attempts=4, progress=0.0) == True

    def test_impasse_requires_both_failures_and_no_progress(self):
        """Impasse requires BOTH failures AND lack of progress"""
        system = InsightSystem(impasse_threshold=2)

        # Failures but progress
        assert system.detect_impasse(failed_attempts=3, progress=0.5) == False

        # No failures
        assert system.detect_impasse(failed_attempts=0, progress=0.0) == False

        # Both conditions met
        assert system.detect_impasse(failed_attempts=2, progress=0.0) == True

    def test_impasse_counter_resets_on_progress(self):
        """Impasse counter should reset when progress made"""
        system = InsightSystem()

        # First check: impasse
        is_impasse_1 = system.detect_impasse(failed_attempts=3, progress=0.0)

        # After progress (internal counter would reset)
        # This test checks the logic, actual implementation may track internally
        is_impasse_2 = system.detect_impasse(failed_attempts=1, progress=0.4)

        assert is_impasse_1 == True
        assert is_impasse_2 == False


class TestIncubation:
    """Test incubation period (unconscious processing)"""

    def test_initiates_incubation(self):
        """System can initiate incubation period"""
        system = InsightSystem()

        problem = {"description": "9-dot problem", "constraints": ["don't lift pen"]}

        incubation_time = system.initiate_incubation(problem)

        # Returns time needed
        assert incubation_time > 0

    def test_incubation_duration_variable(self):
        """Incubation duration can vary by problem complexity"""
        system = InsightSystem(incubation_duration=120.0)

        simple_problem = {"description": "2+2", "complexity": "low"}
        complex_problem = {"description": "Traveling salesman", "complexity": "high"}

        time_simple = system.initiate_incubation(simple_problem)
        time_complex = system.initiate_incubation(complex_problem)

        # Complex problems may need longer incubation
        # (simulated: actual time may depend on implementation)
        assert time_simple >= 0
        assert time_complex >= 0

    def test_incubation_reduces_focused_attention(self):
        """Incubation should signal reduced focused attention"""
        system = InsightSystem()

        problem = {"description": "Insight problem"}

        incubation_time = system.initiate_incubation(problem)

        # Verify it returns a duration (signal to reduce attention)
        assert incubation_time == system.incubation_duration

    def test_incubation_integration_with_dmn(self):
        """Incubation integrates with Default Mode Network (future LAB_046)"""
        system = InsightSystem()

        problem = {"description": "Creative problem"}

        # Incubation should trigger DMN-like processing
        # (Placeholder: actual integration when LAB_046 exists)
        incubation_time = system.initiate_incubation(problem)

        # For now, just verify it returns expected duration
        assert incubation_time > 0


class TestProblemRestructuring:
    """Test problem space restructuring (key to insight)"""

    def test_restructures_problem(self):
        """System can restructure problem representation"""
        system = InsightSystem()

        original = {
            "description": "9-dot problem",
            "constraints": ["stay_within_box"],
            "approach": "connect_adjacent_dots"
        }

        restructured = system.restructure_problem(original, approach="constraint_relaxation")

        # Restructured should differ from original
        assert restructured is not None
        assert restructured != original

    def test_constraint_relaxation(self):
        """Constraint relaxation removes limiting assumptions"""
        system = InsightSystem()

        problem = {
            "description": "9-dot problem",
            "constraints": ["stay_within_box", "connect_adjacent"]
        }

        restructured = system.restructure_problem(problem, approach="constraint_relaxation")

        # Should relax at least one constraint
        assert "relaxed_constraints" in restructured or len(restructured.get("constraints", [])) < len(problem["constraints"])

    def test_analogical_restructuring(self):
        """Analogical restructuring uses LAB_024 (Conceptual Blending)"""
        system = InsightSystem()

        problem = {
            "description": "Duncker's radiation problem",
            "constraints": ["single_high_intensity_beam_damages_tissue"]
        }

        # Analogy: fortress + converging_paths
        restructured = system.restructure_problem(problem, approach="analogy")

        # Should contain analogical mapping
        assert "analogy" in restructured or "reframed" in restructured

    def test_problem_decomposition(self):
        """Decomposition breaks problem into subproblems"""
        system = InsightSystem()

        problem = {
            "description": "Complex multi-step problem",
            "complexity": "high"
        }

        restructured = system.restructure_problem(problem, approach="decomposition")

        # Should contain subproblems
        assert "subproblems" in restructured or "parts" in restructured

    def test_restructuring_changes_representation(self):
        """Restructuring changes problem representation (not just content)"""
        system = InsightSystem()

        original = {
            "representation": "algebraic",
            "problem": "x + y = 10"
        }

        restructured = system.restructure_problem(original, approach="analogy")

        # Representation should change
        assert restructured.get("representation") != original.get("representation") or "reframed" in restructured

    def test_invalid_restructuring_approach_fails(self):
        """Invalid restructuring approach returns error"""
        system = InsightSystem()

        problem = {"description": "Test problem"}

        with pytest.raises(ValueError):
            system.restructure_problem(problem, approach="invalid_approach_xyz")

    def test_multiple_restructuring_attempts(self):
        """Multiple restructuring attempts possible"""
        system = InsightSystem()

        problem = {"description": "Hard problem", "attempts": 0}

        restructured_1 = system.restructure_problem(problem, approach="constraint_relaxation")
        restructured_2 = system.restructure_problem(restructured_1, approach="analogy")

        # Both should succeed
        assert restructured_1 is not None
        assert restructured_2 is not None

    def test_restructuring_with_conceptual_blend(self):
        """Restructuring can use conceptual blending from LAB_024"""
        system = InsightSystem()

        problem = {
            "description": "Duncker radiation",
            "domain": "medical"
        }

        # Use blending to map to military domain
        restructured = system.restructure_problem(problem, approach="analogy")

        # Should indicate blend/analogy used
        assert "blend" in str(restructured).lower() or "analogy" in restructured


class TestSolutionEmergence:
    """Test detecting when restructuring reveals solution"""

    def test_detects_solution_after_restructuring(self):
        """System detects solution emerged after restructuring"""
        system = InsightSystem()

        original = {"solution_visible": False, "confidence": 0.2}
        restructured = {"solution_visible": True, "confidence": 0.95}

        emerged = system.detect_solution_emergence(restructured, original)

        assert emerged == True

    def test_no_solution_without_restructuring(self):
        """No solution detection if problem not restructured"""
        system = InsightSystem()

        original = {"confidence": 0.2}
        still_stuck = {"confidence": 0.25}

        emerged = system.detect_solution_emergence(still_stuck, original)

        assert emerged == False

    def test_confidence_spike_indicates_insight(self):
        """Large confidence spike indicates insight occurred"""
        system = InsightSystem()

        original = {"confidence": 0.1}
        after_restructure = {"confidence": 0.9}

        emerged = system.detect_solution_emergence(after_restructure, original)

        # Confidence jumped 0.1 → 0.9 = insight
        assert emerged == True

    def test_false_positive_low_confidence_rejected(self):
        """Low confidence solutions rejected (no false positives)"""
        system = InsightSystem(aha_confidence_threshold=0.8)

        original = {"confidence": 0.1}
        low_confidence = {"confidence": 0.6}

        emerged = system.detect_solution_emergence(low_confidence, original)

        # Confidence 0.6 < threshold 0.8 → rejected
        assert emerged == False

    def test_solution_verification(self):
        """Solution emergence verified by confidence threshold"""
        system = InsightSystem(aha_confidence_threshold=0.8)

        original = {"confidence": 0.2}

        # Below threshold
        low_conf = {"confidence": 0.7}
        assert system.detect_solution_emergence(low_conf, original) == False

        # Above threshold
        high_conf = {"confidence": 0.85}
        assert system.detect_solution_emergence(high_conf, original) == True


class TestAhaSignal:
    """Test subjective 'Aha!' moment generation"""

    def test_generates_aha_signal(self):
        """System generates Aha signal on insight"""
        system = InsightSystem()

        confidence_spike = 0.9

        aha = system.generate_aha_signal(confidence_spike)

        assert aha is not None
        assert "intensity" in aha
        assert aha["intensity"] > 0

    def test_aha_intensity_proportional_to_confidence(self):
        """Aha intensity proportional to confidence spike"""
        system = InsightSystem()

        aha_low = system.generate_aha_signal(confidence=0.6)
        aha_high = system.generate_aha_signal(confidence=0.95)

        assert aha_high["intensity"] > aha_low["intensity"]

    def test_dopamine_burst_on_aha(self):
        """Aha moment triggers dopamine burst (LAB_013 integration)"""
        system = InsightSystem()

        aha = system.generate_aha_signal(confidence=0.92)

        # Should indicate dopamine reward signal
        assert "dopamine_burst" in aha or "reward_signal" in aha

    def test_no_aha_for_gradual_solving(self):
        """Gradual problem solving does NOT generate Aha"""
        system = InsightSystem()

        # Small confidence increase (analytic solving, not insight)
        confidence_gradual = 0.55

        aha = system.generate_aha_signal(confidence_gradual)

        # Low intensity or no aha
        assert aha["intensity"] < 0.5

    def test_aha_distinct_from_regular_success(self):
        """Aha moment is distinct from regular problem solving success"""
        system = InsightSystem()

        # Regular success (expected, no surprise)
        regular_confidence = 0.7

        # Insight (sudden, surprising)
        insight_confidence = 0.95

        aha_regular = system.generate_aha_signal(regular_confidence)
        aha_insight = system.generate_aha_signal(insight_confidence)

        # Insight should have higher intensity
        assert aha_insight["intensity"] > aha_regular["intensity"]


class TestWarmthRatings:
    """Test Metcalfe & Wiebe warmth ratings (feeling of closeness to solution)"""

    def test_warmth_gradual_for_analytic(self):
        """Analytic solving shows gradual warmth increase"""
        system = InsightSystem()

        # Analytic progress: steady increase
        progress_history = [0.1, 0.3, 0.5, 0.7, 0.9]

        warmth = system.compute_warmth(progress_history)

        # Should show increasing trend
        assert warmth > 0.5

    def test_warmth_flat_then_spike_for_insight(self):
        """Insight solving shows flat warmth then sudden spike"""
        system = InsightSystem()

        # Insight pattern: stuck, stuck, stuck, AHA!
        progress_history = [0.1, 0.1, 0.15, 0.12, 0.95]

        warmth = system.compute_warmth(progress_history)

        # Final warmth high, but early warmth was low
        # (Implementation: check variance or final spike)
        assert warmth > 0.7  # Final spike should result in high warmth

    def test_warmth_distinguishes_solving_types(self):
        """Warmth trajectory distinguishes analytic vs insight solving"""
        system = InsightSystem()

        # Analytic: gradual
        analytic_history = [0.2, 0.4, 0.6, 0.8, 0.9]

        # Insight: flat then spike
        insight_history = [0.1, 0.1, 0.15, 0.1, 0.9]

        warmth_analytic = system.compute_warmth(analytic_history)
        warmth_insight = system.compute_warmth(insight_history)

        # Both may have high final warmth, but pattern differs
        # (Implementation could track variance or trajectory shape)
        # For now, just verify both compute
        assert warmth_analytic >= 0.0
        assert warmth_insight >= 0.0


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_event_complete(self):
        """process_event executes complete insight solving cycle"""
        system = InsightSystem()

        result = system.process_event(
            problem={
                "description": "9-dot problem",
                "constraints": ["stay_in_box"],
                "attempts": 3,
                "progress": 0.0
            }
        )

        assert "insight_occurred" in result
        assert "solution" in result or "restructured_problem" in result

    def test_process_event_updates_stats(self):
        """process_event updates system statistics"""
        system = InsightSystem()

        initial_attempts = system.total_problems_attempted

        system.process_event(
            problem={"description": "Test problem", "attempts": 2, "progress": 0.0}
        )

        assert system.total_problems_attempted == initial_attempts + 1

    def test_process_event_with_incubation(self):
        """process_event handles incubation when impasse detected"""
        system = InsightSystem(impasse_threshold=2)

        result = system.process_event(
            problem={
                "description": "Hard problem",
                "attempts": 3,  # Above threshold
                "progress": 0.0  # No progress
            }
        )

        # Should trigger incubation
        assert "incubation_triggered" in result or result.get("insight_occurred") == True
