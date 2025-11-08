"""
LAB_022: Goal-Directed Behavior System - Unit Tests (Streamlined Integrative)

Integrative Higher-Order EF: Goal hierarchy, motivation, persistence

Integrates:
- ALL 4 Neurochemistry LABs (DA, 5-HT, NE, ACh, GABA)
- ALL 4 Executive Function LABs (Inhibition, Flexibility, Error, Planning)

Key Papers:
- Balleine & O'Doherty (2010) - "Human and rodent homologies in action control"
- Daw et al. (2005) - "Uncertainty-based competition"
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Executive_Functions.LAB_022_Goal_Directed_Behavior.goal_directed_system import (
    GoalDirectedBehaviorSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes correctly"""
        system = GoalDirectedBehaviorSystem()
        assert system.baseline_motivation == 0.6
        assert system.goal_capacity == 5

    def test_state_initialization(self):
        """State initializes correctly"""
        system = GoalDirectedBehaviorSystem()
        assert system.current_motivation == 0.6
        assert system.active_goals == []


class TestGoalSetting:
    """Test goal setting and hierarchy"""

    def test_sets_goal(self):
        """System sets goal successfully"""
        system = GoalDirectedBehaviorSystem()
        goal = system.set_goal("Complete project", priority=0.8)
        assert goal is not None
        assert goal["description"] == "Complete project"

    def test_respects_capacity(self):
        """System respects max concurrent goals"""
        system = GoalDirectedBehaviorSystem(goal_capacity=3)
        for i in range(5):
            system.set_goal(f"Goal {i}", priority=0.5)
        assert len(system.active_goals) <= 3


class TestMotivationUpdate:
    """Test motivation dynamics"""

    def test_progress_increases_motivation(self):
        """Progress toward goal increases motivation"""
        system = GoalDirectedBehaviorSystem(baseline_motivation=0.5)
        initial_motivation = system.current_motivation
        system.update_motivation(goal_value=0.8, recent_progress=0.7)
        assert system.current_motivation > initial_motivation

    def test_lack_of_progress_decreases_motivation(self):
        """Lack of progress decreases motivation"""
        system = GoalDirectedBehaviorSystem(baseline_motivation=0.7)
        initial_motivation = system.current_motivation
        system.update_motivation(goal_value=0.3, recent_progress=0.1)
        assert system.current_motivation < initial_motivation


class TestPersistence:
    """Test persistence computation"""

    def test_high_value_increases_persistence(self):
        """High-value goals have higher persistence"""
        system = GoalDirectedBehaviorSystem()
        goal_low = {"value": 0.3, "sunk_cost": 0.2}
        goal_high = {"value": 0.9, "sunk_cost": 0.2}

        persist_low = system.compute_persistence(goal_low, obstacles=0.5)
        persist_high = system.compute_persistence(goal_high, obstacles=0.5)

        assert persist_high > persist_low


class TestGoalShielding:
    """Test goal shielding (distractor inhibition)"""

    def test_shields_from_distractors(self):
        """Active goal shields from distractors"""
        system = GoalDirectedBehaviorSystem()
        active_goal = {"priority": 0.9}
        distractors = [
            {"priority": 0.3},
            {"priority": 0.4}
        ]

        suppression = system.apply_goal_shielding(active_goal, distractors)
        assert len(suppression) == 2
        assert all(s > 0 for s in suppression)


class TestNeurochemistryIntegration:
    """Test integration with all 4 neurochemistry LABs"""

    def test_integrates_all_neurotransmitters(self):
        """System integrates all neurotransmitter modulations"""
        system = GoalDirectedBehaviorSystem()

        modulations = system.integrate_all_neurotransmitters(
            dopamine=0.7,
            serotonin=0.6,
            norepinephrine=0.5,
            acetylcholine=0.8,
            gaba=0.4,
            glutamate=0.6
        )

        assert "motivation_modulation" in modulations
        assert "patience_modulation" in modulations
        assert "arousal_modulation" in modulations


class TestExecutiveFunctionIntegration:
    """Test integration with all 4 Executive Function LABs"""

    def test_integrates_executive_functions(self):
        """System uses all executive functions"""
        system = GoalDirectedBehaviorSystem()

        goal = {"description": "Test goal", "priority": 0.8}
        ef_contributions = system.integrate_executive_functions(goal)

        assert "planning" in ef_contributions
        assert "inhibition" in ef_contributions
        assert "flexibility" in ef_contributions
        assert "error_detection" in ef_contributions


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_event_complete(self):
        """process_event executes complete cycle"""
        system = GoalDirectedBehaviorSystem()

        result = system.process_event(
            goal_update={"description": "Finish task", "priority": 0.7},
            context={"progress": 0.5}
        )

        assert "motivation" in result
        assert "active_goal" in result
        assert "persistence" in result
