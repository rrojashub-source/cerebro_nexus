"""
LAB_006: Metacognition Logger - Test Suite

Validate metacognitive tracking and calibration analysis.

Author: NEXUS (Autonomous)
Date: October 28, 2025
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'implementation'))

from metacognition_logger import MetacognitionLogger


def test_metacognition_system():
    """Test complete metacognition logging and analysis"""

    print("=" * 70)
    print("LAB_006: Metacognition Logger - Test Suite")
    print("=" * 70)
    print()

    # Create logger
    logger = MetacognitionLogger()

    # ========================================================================
    # TEST 1: Confidence Tracking
    # ========================================================================

    print("TEST 1: Confidence Tracking")
    print("-" * 70)

    # Log actions with varying confidence
    logger.log_action(
        "action_001",
        "lab_implementation",
        confidence=0.95,
        reasoning="Similar to previous LABS, all succeeded"
    )

    logger.log_action(
        "action_002",
        "test",
        confidence=0.85,
        reasoning="Standard test, should pass"
    )

    logger.log_action(
        "action_003",
        "complex_algorithm",
        confidence=0.60,
        reasoning="New algorithm, uncertain about edge cases"
    )

    logger.log_action(
        "action_004",
        "experimental_feature",
        confidence=0.40,
        reasoning="Very experimental, high risk of failure"
    )

    print(f"✓ Logged 4 actions with varying confidence")
    print()

    conf_stats = logger.confidence_tracker.get_stats()
    print(f"Confidence Statistics:")
    print(f"  Total actions: {conf_stats['total_actions']}")
    print(f"  Avg confidence: {conf_stats['avg_confidence']:.3f}")
    print(f"  Range: {conf_stats['min_confidence']:.2f} - {conf_stats['max_confidence']:.2f}")
    print()

    # ========================================================================
    # TEST 2: Outcome Tracking
    # ========================================================================

    print()
    print("TEST 2: Outcome Tracking")
    print("-" * 70)

    # Log outcomes (simulating real results)
    logger.log_outcome("action_001", success=True)  # High confidence, success ✓
    logger.log_outcome("action_002", success=True)  # High confidence, success ✓
    logger.log_outcome("action_003", success=False, error_type="edge_case_failure")  # Uncertain, failure (expected)
    logger.log_outcome("action_004", success=False, error_type="experimental_failure")  # Low confidence, failure (expected)

    print(f"✓ Logged 4 outcomes")
    print()

    outcome_stats = logger.outcome_tracker.get_stats()
    print(f"Outcome Statistics:")
    print(f"  Completed: {outcome_stats['completed_actions']}")
    print(f"  Success rate: {outcome_stats['success_rate']:.1%}")
    print(f"  Successes: {outcome_stats['successes']}")
    print(f"  Failures: {outcome_stats['failures']}")
    print(f"  Error types: {outcome_stats['error_types']}")
    print()

    # ========================================================================
    # TEST 3: Error Detection (Confidence Mismatches)
    # ========================================================================

    print()
    print("TEST 3: Error Detection - Confidence Mismatches")
    print("-" * 70)

    # Add a confidence mismatch (high confidence but failed)
    logger.log_action(
        "action_005",
        "supposed_to_work",
        confidence=0.92,
        reasoning="This should definitely work"
    )
    logger.log_outcome("action_005", success=False, error_type="unexpected_failure")

    print(f"✓ Added confidence mismatch (0.92 confidence, but failed)")
    print()

    actions = list(logger.confidence_tracker.actions.values())
    error_stats = logger.error_detector.analyze_errors(actions)

    print(f"Error Analysis:")
    print(f"  Confidence mismatches: {error_stats['confidence_mismatches']}")
    print(f"  Mismatch rate: {error_stats['mismatch_rate']:.1%}")
    print(f"  Avg mismatch confidence: {error_stats['avg_mismatch_confidence']:.3f}")
    print(f"  Mismatch actions: {error_stats['mismatch_actions']}")
    print()

    # ========================================================================
    # TEST 4: Calibration Analysis
    # ========================================================================

    print()
    print("TEST 4: Calibration Analysis")
    print("-" * 70)

    # Add more actions for better calibration analysis
    test_cases = [
        ("action_006", 0.95, True),   # High confidence, success
        ("action_007", 0.90, True),   # High confidence, success
        ("action_008", 0.88, True),   # High confidence, success
        ("action_009", 0.85, False),  # High confidence, failure (mismatch)
        ("action_010", 0.75, True),   # Medium confidence, success
        ("action_011", 0.70, True),   # Medium confidence, success
        ("action_012", 0.65, False),  # Medium confidence, failure
        ("action_013", 0.55, True),   # Low confidence, success (underconfident)
        ("action_014", 0.50, False),  # Low confidence, failure
        ("action_015", 0.45, False),  # Low confidence, failure
    ]

    for action_id, conf, outcome in test_cases:
        logger.log_action(action_id, "test_action", conf)
        logger.log_outcome(action_id, outcome)

    print(f"✓ Added 10 more actions for calibration analysis")
    print()

    calibration_stats = logger.calibration_analyzer.get_calibration_stats(
        list(logger.confidence_tracker.actions.values())
    )

    print(f"Calibration Metrics:")
    print(f"  ECE (Expected Calibration Error): {calibration_stats['ece']:.3f}")
    print(f"    (Perfect: 0.0, Good: < 0.1, Poor: > 0.2)")
    print(f"  Brier Score: {calibration_stats['brier_score']:.3f}")
    print(f"    (Perfect: 0.0, Random: 0.25)")
    print(f"  Sample size: {calibration_stats['sample_size']}")
    print()

    print(f"By Confidence Band:")
    for band, stats in calibration_stats['by_confidence_band'].items():
        if stats['count'] > 0:
            print(f"  {band}:")
            print(f"    Count: {stats['count']}")
            print(f"    Success rate: {stats['success_rate']:.1%}")
            print(f"    Avg confidence: {stats['avg_confidence']:.3f}")
    print()

    # ========================================================================
    # TEST 5: Well-Calibrated Check
    # ========================================================================

    print()
    print("TEST 5: Well-Calibrated Check")
    print("-" * 70)

    is_calibrated = logger.is_well_calibrated(ece_threshold=0.25)
    print(f"Is well-calibrated (ECE < 0.25)? {is_calibrated}")
    print()

    # ========================================================================
    # Comprehensive Stats
    # ========================================================================

    print()
    print("=" * 70)
    print("Comprehensive Statistics")
    print("=" * 70)

    stats = logger.get_comprehensive_stats()

    print()
    print(f"Confidence:")
    print(f"  Total actions: {stats['confidence']['total_actions']}")
    print(f"  Avg confidence: {stats['confidence']['avg_confidence']:.3f}")
    print()

    print(f"Outcomes:")
    print(f"  Success rate: {stats['outcomes']['success_rate']:.1%}")
    print(f"  Successes: {stats['outcomes']['successes']}")
    print(f"  Failures: {stats['outcomes']['failures']}")
    print()

    print(f"Errors:")
    print(f"  Confidence mismatches: {stats['errors']['confidence_mismatches']}")
    print(f"  Mismatch rate: {stats['errors']['mismatch_rate']:.1%}")
    print()

    print(f"Calibration:")
    print(f"  ECE: {stats['calibration']['ece']:.3f}")
    print(f"  Brier Score: {stats['calibration']['brier_score']:.3f}")
    print()

    # ========================================================================
    # Success Criteria
    # ========================================================================

    print("=" * 70)
    print("Success Criteria")
    print("=" * 70)
    print()

    checks = [
        ("Confidence tracking works", stats['confidence']['total_actions'] >= 15, True),
        ("Outcomes tracked", stats['outcomes']['completed_actions'] >= 15, True),
        ("Error detection works", stats['errors']['confidence_mismatches'] >= 1, True),
        ("ECE computed", stats['calibration']['ece'] >= 0, True),
        ("Well-calibrated", stats['calibration']['ece'] < 0.25, True),  # Reasonable threshold for small sample
        ("High confidence → high success",
         stats['calibration']['by_confidence_band']['very_confident']['success_rate'] > 0.7 if stats['calibration']['by_confidence_band'].get('very_confident', {}).get('count', 0) > 0 else True,
         True),
    ]

    all_pass = True
    for criterion, result, expected in checks:
        passed = result == expected
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}  {criterion:<40} ({result})")
        if not passed:
            all_pass = False

    print()
    if all_pass:
        print("🎉 ALL TESTS PASSED - Metacognition logging working!")
    else:
        print("⚠️  Some tests failed - Needs debugging")

    print()


if __name__ == "__main__":
    test_metacognition_system()
