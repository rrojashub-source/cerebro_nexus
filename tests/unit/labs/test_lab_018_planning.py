"""
LAB_018: Planning & Sequencing System - Unit Tests (Simplified Core)

Higher-Order Executive Function: Multi-step planning and temporal sequencing

Biological Foundation:
- Dorsolateral prefrontal cortex (dlPFC)
- Lateral frontal pole

Neurochemistry:
- Dopamine (LAB_013): Motivation for planning
- Acetylcholine (LAB_016): Attention to plan details
- Working Memory (LAB_011): Maintains plan steps

Key Papers:
- Koechlin & Hyafil (2007) - "Anterior prefrontal function"
- Badre & D'Esposito (2009) - "Rostro-caudal axis of frontal lobe"
"""

import pytest
import sys
from pathlib import Path

# Add experiments to path
experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Executive_Functions.LAB_018_Planning_Sequencing.planning_system import (
    PlanningSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with correct defaults"""
        system = PlanningSystem()

        assert system.baseline_planning_capacity == 0.6
        assert system.max_plan_depth == 5
        assert system.max_plan_length == 10

    def test_state_initialization(self):
        """State initializes correctly"""
        system = PlanningSystem()

        assert system.current_capacity == 0.6
        assert system.active_plan is None
        assert system.total_plans_created == 0

    def test_custom_parameters(self):
        """System accepts custom parameters"""
        system = PlanningSystem(
            baseline_planning_capacity=0.8,
            max_plan_depth=7
        )

        assert system.baseline_planning_capacity == 0.8
        assert system.max_plan_depth == 7


class TestPlanCreation:
    """Test plan generation"""

    def test_creates_plan_for_goal(self):
        """System creates plan for given goal"""
        system = PlanningSystem()

        plan = system.create_plan(
            goal="Complete task",
            constraints={"max_time": 3600}
        )

        assert plan is not None
        assert plan["goal"] == "Complete task"
        assert "steps" in plan

    def test_plan_respects_max_length(self):
        """Plan respects maximum length constraint"""
        system = PlanningSystem(max_plan_length=5)

        plan = system.create_plan("Complex goal", {})

        assert len(plan["steps"]) <= 5

    def test_tracks_plans_created(self):
        """System tracks number of plans created"""
        system = PlanningSystem()

        initial_count = system.total_plans_created

        system.create_plan("Goal A", {})
        system.create_plan("Goal B", {})

        assert system.total_plans_created == initial_count + 2


class TestActionSequencing:
    """Test action ordering"""

    def test_sequences_simple_actions(self):
        """Sequences actions without dependencies"""
        system = PlanningSystem()

        actions = [
            {"id": "a1", "deps": []},
            {"id": "a2", "deps": []},
            {"id": "a3", "deps": []}
        ]

        sequenced = system.sequence_actions(actions)

        assert len(sequenced) == 3

    def test_respects_dependencies(self):
        """Sequencing respects action dependencies"""
        system = PlanningSystem()

        actions = [
            {"id": "a1", "deps": []},
            {"id": "a2", "deps": ["a1"]},
            {"id": "a3", "deps": ["a2"]}
        ]

        sequenced = system.sequence_actions(actions)

        # a1 should come before a2, a2 before a3
        ids = [a["id"] for a in sequenced]
        assert ids.index("a1") < ids.index("a2")
        assert ids.index("a2") < ids.index("a3")


class TestDurationEstimation:
    """Test time estimation"""

    def test_estimates_duration(self):
        """Computes plan duration estimate"""
        system = PlanningSystem()

        plan = system.create_plan("Test goal", {"max_time": 7200})

        duration = system.estimate_duration(plan)

        assert duration > 0

    def test_duration_realistic(self):
        """Duration estimates are realistic"""
        system = PlanningSystem()

        plan = system.create_plan("Simple goal", {})

        duration = system.estimate_duration(plan)

        # Typical: 30min - 4 hours
        assert 1800 < duration < 14400


class TestExecutionMonitoring:
    """Test plan execution monitoring"""

    def test_detects_on_track(self):
        """Detects when plan is on track"""
        system = PlanningSystem()

        plan = system.create_plan("Goal", {})

        # Simulate good progress
        monitoring = system.monitor_execution(
            plan=plan,
            progress={"completed_steps": 2, "total_steps": 5}
        )

        assert monitoring["on_track"] is True

    def test_detects_deviation(self):
        """Detects when plan deviates"""
        system = PlanningSystem()

        plan = system.create_plan("Goal", {})

        # Simulate poor progress
        monitoring = system.monitor_execution(
            plan=plan,
            progress={"completed_steps": 1, "total_steps": 10}
        )

        # Should detect deviation (only 10% complete)
        assert monitoring["deviation_magnitude"] > 0


class TestReplanning:
    """Test plan revision"""

    def test_triggers_replanning(self):
        """System triggers replanning when needed"""
        system = PlanningSystem()

        original_plan = system.create_plan("Goal", {})

        new_plan = system.trigger_replanning(
            original_plan=original_plan,
            new_constraints={"max_time": 1800}
        )

        assert new_plan is not None
        assert system.replanning_count > 0


class TestDopamineIntegration:
    """Test dopamine modulation"""

    def test_high_dopamine_ambitious_plans(self):
        """High dopamine creates more ambitious plans"""
        system = PlanningSystem()

        capacity_low = system.integrate_dopamine(dopamine_level=0.3)
        capacity_high = system.integrate_dopamine(dopamine_level=0.9)

        assert capacity_high > capacity_low


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_event_complete_cycle(self):
        """process_event executes complete planning cycle"""
        system = PlanningSystem()

        result = system.process_event(
            goal="Implement feature",
            constraints={"max_time": 3600}
        )

        assert "plan" in result
        assert "quality" in result
        assert "estimated_duration" in result
