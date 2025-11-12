"""
LAB_039: Habit Formation - Unit Tests

Pattern Recognition: Procedural memory, automaticity, habit loops

Key Papers:
- Dolan & Dayan (2013) - Goals and habits in the brain
- Graybiel (2008) - Habits, rituals, and the evaluative brain
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Pattern_Recognition.LAB_039_Habit_Formation.habit_formation_system import (
    HabitFormationSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with empty habit registry"""
        system = HabitFormationSystem()
        assert system.automaticity_rate == 0.1
        assert len(system.habits) == 0
        assert len(system.action_history) == 0

    def test_custom_automaticity_rate(self):
        """System accepts custom automaticity rate"""
        system = HabitFormationSystem(automaticity_rate=0.15)
        assert system.automaticity_rate == 0.15

    def test_habit_registry_empty(self):
        """Habit registry starts empty"""
        system = HabitFormationSystem()
        state = system.get_state()
        assert state["total_habits"] == 0


class TestHabitFormation:
    """Test habit formation from repeated actions"""

    def test_frequency_tracking(self):
        """Repeated actions increase habit strength"""
        system = HabitFormationSystem()

        # Repeat action 5 times
        for i in range(5):
            system.perform_action(context="morning", action="coffee", outcome=1.0)

        habit = system.habits.get(("morning", "coffee"))
        assert habit is not None
        assert habit["strength"] > 0
        assert habit["repetitions"] == 5

    def test_automaticity_curve(self):
        """Cognitive cost decreases with practice"""
        system = HabitFormationSystem()

        # Initial cognitive cost
        initial_cost = system.get_cognitive_cost(context="work", action="email_check")
        assert initial_cost == 1.0  # No habit yet

        # Repeat many times
        for i in range(20):
            system.perform_action(context="work", action="email_check", outcome=0.8)

        # Cognitive cost should decrease
        final_cost = system.get_cognitive_cost(context="work", action="email_check")
        assert final_cost < initial_cost
        assert final_cost < 0.3  # Significantly automated

    def test_cue_routine_reward_loop(self):
        """Cue-routine-reward loop formation"""
        system = HabitFormationSystem()

        # Repeat cue-routine-reward 10 times
        for i in range(10):
            system.process_event(
                event_type="action",
                context="stress",
                action="snack",
                reward=0.7
            )

        habit = system.habits.get(("stress", "snack"))
        assert habit["cue"] == "stress"
        assert habit["routine"] == "snack"
        assert habit["avg_reward"] > 0.6

    def test_asymptotic_habit_strength(self):
        """Habit strength asymptotes at 0.9-1.0"""
        system = HabitFormationSystem()

        # Repeat 100 times (extreme practice)
        for i in range(100):
            system.perform_action(context="evening", action="brush_teeth", outcome=1.0)

        habit = system.habits[("evening", "brush_teeth")]
        assert 0.85 <= habit["strength"] <= 1.0  # Asymptotes at ~0.88

    def test_different_contexts_different_habits(self):
        """Same action in different contexts = different habits"""
        system = HabitFormationSystem()

        # Action A in context 1
        for i in range(5):
            system.perform_action(context="home", action="coffee", outcome=1.0)

        # Action A in context 2
        for i in range(3):
            system.perform_action(context="office", action="coffee", outcome=1.0)

        habit_home = system.habits[("home", "coffee")]
        habit_office = system.habits[("office", "coffee")]

        assert habit_home["repetitions"] == 5
        assert habit_office["repetitions"] == 3
        assert habit_home["strength"] > habit_office["strength"]

    def test_positive_reward_strengthens_habit(self):
        """Positive rewards strengthen habit formation"""
        system = HabitFormationSystem()

        # High reward
        for i in range(5):
            system.perform_action(context="hungry", action="eat_healthy", outcome=0.9)

        # Low reward
        for i in range(5):
            system.perform_action(context="bored", action="scroll_phone", outcome=0.3)

        habit_high = system.habits[("hungry", "eat_healthy")]
        habit_low = system.habits[("bored", "scroll_phone")]

        assert habit_high["strength"] > habit_low["strength"]

    def test_negative_reward_weakens_habit(self):
        """Negative outcomes weaken habit"""
        system = HabitFormationSystem()

        # Build habit first
        for i in range(10):
            system.perform_action(context="tired", action="procrastinate", outcome=0.5)

        initial_strength = system.habits[("tired", "procrastinate")]["strength"]

        # Negative outcomes
        for i in range(5):
            system.perform_action(context="tired", action="procrastinate", outcome=-0.5)

        final_strength = system.habits[("tired", "procrastinate")]["strength"]
        assert final_strength < initial_strength

    def test_habit_formation_rate_with_dopamine(self):
        """High dopamine (from LAB_013) accelerates habit formation"""
        system = HabitFormationSystem()

        # With high dopamine
        result_high = system.perform_action(
            context="win", action="celebrate", outcome=1.0, dopamine_level=0.9
        )

        # With low dopamine
        result_low = system.perform_action(
            context="loss", action="analyze", outcome=0.6, dopamine_level=0.3
        )

        # High dopamine should produce stronger habit delta
        assert result_high["habit_delta"] > result_low["habit_delta"]


class TestHabitStrength:
    """Test habit strength evolution"""

    def test_weak_habits(self):
        """Few repetitions = weak habit"""
        system = HabitFormationSystem()

        for i in range(2):
            system.perform_action(context="new", action="experiment", outcome=0.7)

        habit = system.habits[("new", "experiment")]
        assert habit["strength"] < 0.3  # Weak

    def test_strong_habits(self):
        """Many repetitions = strong habit"""
        system = HabitFormationSystem()

        for i in range(50):
            system.perform_action(context="routine", action="habit_action", outcome=0.8)

        habit = system.habits[("routine", "habit_action")]
        assert habit["strength"] > 0.8  # Strong

    def test_decay_without_practice(self):
        """Habit decays if not practiced"""
        system = HabitFormationSystem()

        # Build habit
        for i in range(10):
            system.perform_action(context="gym", action="workout", outcome=0.8)

        initial_strength = system.habits[("gym", "workout")]["strength"]

        # Simulate time passing without practice (decay)
        system.apply_decay(days=30)

        final_strength = system.habits[("gym", "workout")]["strength"]
        assert final_strength < initial_strength

    def test_reinforcement_maintains_strength(self):
        """Continued practice maintains habit strength"""
        system = HabitFormationSystem()

        # Build habit
        for i in range(20):
            system.perform_action(context="daily", action="routine", outcome=0.8)

        strength_before = system.habits[("daily", "routine")]["strength"]

        # Continue practice (10 more)
        for i in range(10):
            system.perform_action(context="daily", action="routine", outcome=0.8)

        strength_after = system.habits[("daily", "routine")]["strength"]

        # Should maintain (may increase slightly but close)
        assert strength_after >= strength_before * 0.95

    def test_habit_strength_influences_activation(self):
        """Strong habits activate more easily from cues"""
        system = HabitFormationSystem()

        # Weak habit
        for i in range(3):
            system.perform_action(context="rare", action="action_weak", outcome=0.6)

        # Strong habit
        for i in range(30):
            system.perform_action(context="common", action="action_strong", outcome=0.8)

        activation_weak = system.compute_habit_activation(context="rare", action="action_weak")
        activation_strong = system.compute_habit_activation(context="common", action="action_strong")

        assert activation_strong > activation_weak


class TestAutomaticity:
    """Test automaticity and cognitive cost reduction"""

    def test_cognitive_cost_reduction(self):
        """Cognitive cost decreases with automaticity"""
        system = HabitFormationSystem()

        initial_cost = system.get_cognitive_cost(context="task", action="skilled")
        assert initial_cost == 1.0  # Not automated yet

        # Practice
        for i in range(15):
            system.perform_action(context="task", action="skilled", outcome=0.7)

        reduced_cost = system.get_cognitive_cost(context="task", action="skilled")
        assert reduced_cost < 0.5  # Significantly reduced

    def test_automatic_activation_from_cues(self):
        """Strong habits activate automatically from cues"""
        system = HabitFormationSystem()

        # Build strong habit
        for i in range(25):
            system.perform_action(context="trigger", action="response", outcome=0.8)

        # Cue should activate habit automatically
        activation = system.compute_habit_activation(context="trigger", action="response")
        assert activation > 0.7  # High automatic activation

    def test_reduced_working_memory_load(self):
        """Habitual actions reduce working memory load (LAB_011 integration)"""
        system = HabitFormationSystem()

        # Build habit
        for i in range(20):
            system.perform_action(context="auto", action="task", outcome=0.8)

        # Compute working memory load
        wm_load = system.compute_working_memory_load(context="auto", action="task")
        assert wm_load < 0.3  # Low load for habitual action

    def test_new_actions_require_full_attention(self):
        """New (non-habitual) actions require full working memory"""
        system = HabitFormationSystem()

        # No habit for this action
        wm_load = system.compute_working_memory_load(context="novel", action="unfamiliar")
        assert wm_load > 0.9  # High load


class TestHabitVsGoalDirected:
    """Test competition between habit and goal-directed control"""

    def test_competition_when_outcomes_change(self):
        """Outcome devaluation test: habits persist despite changed outcomes"""
        system = HabitFormationSystem()

        # Build habit with positive outcome
        for i in range(30):
            system.perform_action(context="choice", action="option_A", outcome=0.8)

        habit_strength = system.habits[("choice", "option_A")]["strength"]
        assert habit_strength > 0.7  # Strong habit

        # Outcome changes (devalued)
        result = system.process_event(
            event_type="outcome_change",
            context="choice",
            action="option_A",
            new_outcome=-0.5  # Now negative
        )

        # Habit should still activate (despite devaluation)
        # This is the KEY test for habit vs goal-directed
        activation = system.compute_habit_activation(context="choice", action="option_A")
        assert activation > 0.6  # Habit persists

    def test_goal_directed_overrides_early(self):
        """Early in learning, goal-directed control dominates"""
        system = HabitFormationSystem()

        # Few repetitions (weak habit)
        for i in range(3):
            system.perform_action(context="decision", action="option_B", outcome=0.7)

        # Compute control mode
        control = system.compute_control_mode(context="decision", action="option_B")
        assert control["mode"] == "goal_directed"
        assert control["goal_directed_weight"] > control["habit_weight"]

    def test_habit_dominates_late(self):
        """After extensive practice, habit dominates"""
        system = HabitFormationSystem()

        # Many repetitions (strong habit)
        for i in range(50):
            system.perform_action(context="automatic", action="option_C", outcome=0.7)

        # Compute control mode
        control = system.compute_control_mode(context="automatic", action="option_C")
        assert control["mode"] == "habitual"
        assert control["habit_weight"] > control["goal_directed_weight"]

    def test_cognitive_control_can_override(self):
        """Cognitive control (LAB_019) can override habits"""
        system = HabitFormationSystem()

        # Build strong habit
        for i in range(40):
            system.perform_action(context="override_test", action="habitual", outcome=0.8)

        # Apply cognitive control to override
        result = system.apply_cognitive_control(
            context="override_test",
            action="habitual",
            control_strength=0.9  # High control from LAB_019
        )

        assert result["habit_suppressed"] == True
        assert result["action_taken"] == "alternative"  # Not habitual

    def test_stress_increases_habit_reliance(self):
        """Under stress, habits dominate over goal-directed"""
        system = HabitFormationSystem()

        # Build moderate habit
        for i in range(15):
            system.perform_action(context="stress_test", action="comfort", outcome=0.7)

        # Low stress: more goal-directed
        control_low = system.compute_control_mode(
            context="stress_test", action="comfort", stress_level=0.2
        )

        # High stress: more habitual
        control_high = system.compute_control_mode(
            context="stress_test", action="comfort", stress_level=0.9
        )

        assert control_high["habit_weight"] > control_low["habit_weight"]


class TestIntegration:
    """Test integration with other LABs"""

    def test_dopamine_rpe_strengthens_habits(self):
        """Positive RPE from LAB_013 strengthens habit formation"""
        system = HabitFormationSystem()

        # Positive RPE (better than expected)
        result_positive = system.process_event(
            event_type="action",
            context="reward_test",
            action="success",
            expected_reward=0.5,
            actual_reward=0.9,  # Positive RPE
            dopamine_level=0.8
        )

        # Negative RPE (worse than expected)
        result_negative = system.process_event(
            event_type="action",
            context="punish_test",
            action="failure",
            expected_reward=0.7,
            actual_reward=0.3,  # Negative RPE
            dopamine_level=0.3
        )

        # Positive RPE should produce stronger habit increase
        assert result_positive["habit_delta"] > result_negative["habit_delta"]

    def test_skill_acquisition_leads_to_habits(self):
        """As skills improve (LAB_040), they become habitual"""
        system = HabitFormationSystem()

        # Simulate skill acquisition progression
        skill_levels = [0.3, 0.5, 0.7, 0.9]  # From LAB_040

        for skill in skill_levels:
            system.perform_action(
                context="skill_context",
                action="practiced_skill",
                outcome=0.8,
                skill_level=skill
            )

        habit = system.habits[("skill_context", "practiced_skill")]

        # High skill → high automaticity
        assert habit["strength"] > 0.6
        assert habit["automaticity"] > 0.7

    def test_cognitive_control_override(self):
        """LAB_019 cognitive control can override habits"""
        system = HabitFormationSystem()

        # Build habit
        for i in range(30):
            system.perform_action(context="override", action="old_way", outcome=0.7)

        # High cognitive control overrides
        result = system.process_event(
            event_type="control_override",
            context="override",
            habitual_action="old_way",
            controlled_action="new_way",
            control_strength=0.9  # From LAB_019
        )

        assert result["action_executed"] == "new_way"
        assert result["habit_overridden"] == True


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_action_event(self):
        """Process action event updates habit"""
        system = HabitFormationSystem()

        result = system.process_event(
            event_type="action",
            context="test",
            action="test_action",
            reward=0.7
        )

        assert "habit_updated" in result
        assert result["habit_updated"] == True
        assert ("test", "test_action") in system.habits

    def test_process_control_override_event(self):
        """Process control override event"""
        system = HabitFormationSystem()

        # Build habit first
        for i in range(20):
            system.perform_action(context="ctx", action="habit", outcome=0.8)

        result = system.process_event(
            event_type="control_override",
            context="ctx",
            habitual_action="habit",
            controlled_action="alternative",
            control_strength=0.8
        )

        assert "action_executed" in result


class TestGetState:
    """Test state retrieval"""

    def test_get_state_returns_habits(self):
        """get_state returns all habits"""
        system = HabitFormationSystem()

        # Create some habits
        for i in range(5):
            system.perform_action(context=f"ctx_{i}", action=f"act_{i}", outcome=0.7)

        state = system.get_state()

        assert "total_habits" in state
        assert state["total_habits"] == 5
        assert "strongest_habit" in state

    def test_get_state_serializable(self):
        """get_state returns JSON-serializable dict"""
        system = HabitFormationSystem()

        state = system.get_state()

        import json
        json_str = json.dumps(state)
        assert json_str is not None
