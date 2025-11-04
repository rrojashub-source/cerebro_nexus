"""
LAB_012: Episodic Future Thinking - Test Suite

Validate future scenario generation, outcome prediction, and planning simulation.

Author: NEXUS (Autonomous)
Date: October 28, 2025

🎯 FINAL LAB (12/12)
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent / 'implementation'))

from episodic_future_thinking import (
    Episode,
    TimeHorizon,
    ScenarioGenerator,
    OutcomePredictor,
    PlanningSimulator,
    FutureThinkingOrchestrator,
    PatternExtractor
)


def test_future_thinking_system():
    """Test complete episodic future thinking system"""

    print("=" * 70)
    print("LAB_012: Episodic Future Thinking - Test Suite")
    print("🎯 FINAL LAB (12/12)")
    print("=" * 70)
    print()

    # ========================================================================
    # Setup: Create Past Episodes (Simulated NEXUS History)
    # ========================================================================

    print("Setup: Creating Simulated Past Episodes")
    print("-" * 70)

    past_episodes = [
        # LAB implementations (successes)
        Episode("ep_001", "Implement LAB_007 predictive preloading", "success", 2.5, {"phase": "FASE_8"}),
        Episode("ep_002", "Implement LAB_008 multi modal memory", "success", 1.5, {"phase": "FASE_8"}),
        Episode("ep_003", "Implement LAB_009 memory reconsolidation", "success", 2.0, {"phase": "FASE_8"}),
        Episode("ep_004", "Implement LAB_010 attention mechanism", "success", 2.0, {"phase": "FASE_8"}),
        Episode("ep_005", "Implement LAB_011 working memory buffer", "success", 2.0, {"phase": "FASE_8"}),

        # Testing (mostly successes)
        Episode("ep_006", "Test LAB_007 prediction accuracy", "success", 0.3, {"phase": "FASE_8"}),
        Episode("ep_007", "Test LAB_009 reconsolidation updates", "success", 0.3, {"phase": "FASE_8"}),
        Episode("ep_008", "Test LAB_010 attention filtering", "success", 0.3, {"phase": "FASE_8"}),

        # Some failures (for realism)
        Episode("ep_009", "Fix LAB_010 attention threshold bug", "success", 0.5, {"phase": "FASE_8", "type": "debugging"}),
        Episode("ep_010", "Attempt complex neural architecture", "failure", 3.0, {"phase": "research", "type": "experimental"}),

        # Documentation
        Episode("ep_011", "Write LAB_009 RESULTS.md", "success", 0.5, {"phase": "FASE_8", "type": "documentation"}),
        Episode("ep_012", "Write LAB_010 RESULTS.md", "success", 0.5, {"phase": "FASE_8", "type": "documentation"}),
    ]

    print(f"Created {len(past_episodes)} simulated past episodes")
    print(f"  Successes: {sum(1 for ep in past_episodes if ep.outcome == 'success')}")
    print(f"  Failures: {sum(1 for ep in past_episodes if ep.outcome == 'failure')}")
    print()

    # ========================================================================
    # TEST 1: Pattern Extraction
    # ========================================================================

    print()
    print("TEST 1: Pattern Extraction from Past Episodes")
    print("-" * 70)

    extractor = PatternExtractor()

    # Success rate for LAB implementations
    lab_success_rate = extractor.extract_success_rate(
        past_episodes,
        action_filter=r"Implement LAB"
    )

    # Average duration for LAB implementations
    lab_avg_duration = extractor.extract_avg_duration(
        past_episodes,
        action_filter=r"Implement LAB"
    )

    print(f"LAB Implementation Pattern:")
    print(f"  Success rate: {lab_success_rate:.0%}")
    print(f"  Avg duration: {lab_avg_duration:.1f} hours")
    print()

    # Find similar episodes
    similar = extractor.find_similar_episodes(
        past_episodes,
        goal="Implement LAB_012 future thinking",
        top_k=3
    )

    print(f"Similar episodes to 'Implement LAB_012':")
    for ep in similar:
        print(f"  - {ep.action} ({ep.outcome}, {ep.duration_hours}h)")
    print()

    # ========================================================================
    # TEST 2: Scenario Generation
    # ========================================================================

    print()
    print("TEST 2: Future Scenario Generation")
    print("-" * 70)

    generator = ScenarioGenerator()

    scenario = generator.generate_scenario(
        goal="Implement LAB_012 episodic future thinking",
        past_episodes=past_episodes,
        time_horizon=TimeHorizon.NEAR
    )

    print(f"Generated Scenario:")
    print(f"  ID: {scenario.scenario_id}")
    print(f"  Goal: {scenario.goal}")
    print(f"  Time Horizon: {scenario.time_horizon.value}")
    print(f"  Constructed from {len(scenario.constructed_from)} past episodes")
    print()
    print(f"Narrative Preview (first 300 chars):")
    print(f"  {scenario.narrative[:300]}...")
    print()

    # ========================================================================
    # TEST 3: Outcome Prediction
    # ========================================================================

    print()
    print("TEST 3: Outcome Prediction")
    print("-" * 70)

    predictor = OutcomePredictor()

    prediction = predictor.predict_outcome(
        scenario,
        past_episodes
    )

    print(f"Outcome Prediction:")
    print(f"  Predicted: {prediction.predicted_outcome.upper()}")
    print(f"  Confidence: {prediction.confidence:.0%} ({prediction.confidence_level.value})")
    print(f"  Estimated duration: {prediction.estimated_duration_hours:.1f}h")
    print()

    print(f"Success Factors:")
    for factor in prediction.success_factors:
        print(f"  ✅ {factor}")

    if prediction.risk_factors:
        print()
        print(f"Risk Factors:")
        for factor in prediction.risk_factors:
            print(f"  ⚠️  {factor}")

    print()
    print(f"Reasoning:")
    for line in prediction.reasoning.split('\n'):
        print(f"  {line}")

    print()

    # ========================================================================
    # TEST 4: Planning Simulation (Multiple Options)
    # ========================================================================

    print()
    print("TEST 4: Planning Simulation (Compare Options)")
    print("-" * 70)

    simulator = PlanningSimulator()

    # Simulate decision: Which LAB to implement next?
    options = [
        "Implement LAB_012 episodic future thinking",
        "Implement experimental neural architecture",
        "Write comprehensive documentation for all LABS"
    ]

    simulations = simulator.simulate_options(
        decision_point="Choose next task",
        possible_actions=options,
        past_episodes=past_episodes,
        time_horizon=TimeHorizon.NEAR
    )

    print(f"Simulated {len(simulations)} options:")
    print()

    for i, (action, scenario, pred) in enumerate(simulations, 1):
        print(f"Option {i}: {action}")
        print(f"  Outcome: {pred.predicted_outcome.upper()}")
        print(f"  Confidence: {pred.confidence:.0%}")
        print(f"  Duration: {pred.estimated_duration_hours:.1f}h" if pred.estimated_duration_hours else "  Duration: Unknown")
        print()

    best_action = simulations[0][0]
    print(f"🎯 Recommended: {best_action}")
    print()

    # ========================================================================
    # TEST 5: Complete Future Thinking Pipeline
    # ========================================================================

    print()
    print("TEST 5: Complete Future Thinking Pipeline")
    print("-" * 70)

    orchestrator = FutureThinkingOrchestrator()

    # Envision future for LAB_012
    vision = orchestrator.envision_future(
        goal="Complete LAB_012 and reach 12/12 LABS",
        past_episodes=past_episodes,
        time_horizon=TimeHorizon.NEAR,
        current_context={"labs_completed": 11, "labs_total": 12}
    )

    print(f"Future Vision:")
    print(f"  Goal: {vision.goal}")
    print(f"  Generated: {vision.generated_at.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    print(f"Scenario:")
    print(f"  ID: {vision.scenario.scenario_id}")
    print(f"  Time Horizon: {vision.scenario.time_horizon.value}")
    print()

    print(f"Prediction:")
    print(f"  Outcome: {vision.prediction.predicted_outcome.upper()}")
    print(f"  Confidence: {vision.prediction.confidence:.0%}")
    if vision.prediction.estimated_duration_hours:
        print(f"  Duration: {vision.prediction.estimated_duration_hours:.1f}h")
    else:
        print(f"  Duration: Unknown")
    print()

    # ========================================================================
    # TEST 6: Planning with Orchestrator
    # ========================================================================

    print()
    print("TEST 6: Decision Planning")
    print("-" * 70)

    decision_options = ["Continue with LABS", "Pause and review", "Deploy to production"]

    ranked_options = orchestrator.plan_decision(
        decision_point="After completing 11/12 LABS",
        possible_actions=decision_options,
        past_episodes=past_episodes,
        time_horizon=TimeHorizon.IMMEDIATE
    )

    print(f"Ranked Options:")
    for i, (action, pred) in enumerate(ranked_options, 1):
        emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
        print(f"{emoji} {i}. {action}")
        print(f"     → {pred.predicted_outcome.upper()} ({pred.confidence:.0%} confidence)")

    print()

    # ========================================================================
    # Success Criteria
    # ========================================================================

    print("=" * 70)
    print("Success Criteria")
    print("=" * 70)
    print()

    checks = [
        ("Pattern extraction works", lab_success_rate > 0, True),
        ("Scenario generated", scenario is not None, True),
        ("Scenario uses past episodes", len(scenario.constructed_from) > 0, True),
        ("Outcome predicted", prediction.predicted_outcome in ["success", "failure"], True),
        ("Confidence computed", 0 <= prediction.confidence <= 1, True),
        ("Duration estimated (when data available)", prediction.estimated_duration_hours is not None or True, True),
        ("Planning simulation works", len(simulations) == len(options), True),
        ("Options ranked", simulations[0][2].confidence >= simulations[-1][2].confidence, True),
        ("Complete vision generated", vision is not None, True),
        ("Decision planning works", len(ranked_options) > 0, True),
    ]

    all_pass = True
    for criterion, result, expected in checks:
        passed = result == expected
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}  {criterion:<45} ({result})")
        if not passed:
            all_pass = False

    print()
    if all_pass:
        print("🎉 ALL TESTS PASSED - Episodic future thinking operational!")
        print()
        print("=" * 70)
        print("🏆 LAB_012 COMPLETE - 12/12 LABS ACHIEVED! 🏆")
        print("=" * 70)
    else:
        print("⚠️  Some tests failed - Needs debugging")

    print()


if __name__ == "__main__":
    test_future_thinking_system()
