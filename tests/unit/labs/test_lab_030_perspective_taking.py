"""
LAB_030: Perspective Taking - Unit Tests

Social Cognition: Spatial & conceptual perspective shifts

Key Papers:
- Zacks & Michelon (2005) - Spatial perspective taking
- Ruby & Decety (2001) - 1st vs 3rd person perspective
- Kessler & Rutherford (2010) - Two forms of perspective taking
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Social_Homeostasis.LAB_030_Perspective_Taking.perspective_taking_system import (
    PerspectiveTakingSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with default parameters"""
        system = PerspectiveTakingSystem()
        assert system.rotation_cost_per_degree == 0.01
        assert system.total_perspective_shifts == 0

    def test_custom_parameters(self):
        """System accepts custom parameters"""
        system = PerspectiveTakingSystem(rotation_cost_per_degree=0.015)
        assert system.rotation_cost_per_degree == 0.015


class TestSpatialRotation:
    """Test mental rotation of spatial perspectives"""

    def test_rotation_cost_linear_with_angle(self):
        """Rotation cost increases linearly with angle (Shepard & Metzler 1971)"""
        system = PerspectiveTakingSystem()

        cost_30 = system.compute_rotation_cost(30)
        cost_60 = system.compute_rotation_cost(60)
        cost_90 = system.compute_rotation_cost(90)

        # Should be linear
        assert cost_60 == pytest.approx(cost_30 * 2, abs=0.05)
        assert cost_90 == pytest.approx(cost_30 * 3, abs=0.05)

    def test_rotation_cost_180_degrees(self):
        """180-degree rotation has maximum cost"""
        system = PerspectiveTakingSystem()

        cost_180 = system.compute_rotation_cost(180)
        cost_90 = system.compute_rotation_cost(90)

        assert cost_180 == pytest.approx(cost_90 * 2, abs=0.05)

    def test_rotation_cost_symmetric(self):
        """Rotation cost same for clockwise and counterclockwise"""
        system = PerspectiveTakingSystem()

        cost_positive = system.compute_rotation_cost(45)
        cost_negative = system.compute_rotation_cost(-45)

        assert cost_positive == cost_negative

    def test_zero_rotation_no_cost(self):
        """Zero degree rotation has no cost"""
        system = PerspectiveTakingSystem()

        cost = system.compute_rotation_cost(0)
        assert cost == 0.0


class TestEgocentricAllocentric:
    """Test egocentric ↔ allocentric transformations"""

    def test_egocentric_to_allocentric_transformation(self):
        """Convert 'to my left' to 'north of landmark'"""
        system = PerspectiveTakingSystem()

        # Egocentric: object to my left
        # My heading: 0° (north)
        # Allocentric: object is west of me
        result = system.spatial_perspective(
            current_frame="egocentric",
            target_frame="allocentric",
            relative_position="left",
            agent_heading=0  # Facing north
        )

        assert result["frame"] == "allocentric"
        assert result["direction"] == "west"

    def test_allocentric_to_egocentric_transformation(self):
        """Convert 'north of landmark' to 'in front of me'"""
        system = PerspectiveTakingSystem()

        # Allocentric: object is north
        # My heading: 0° (north)
        # Egocentric: object is in front of me
        result = system.spatial_perspective(
            current_frame="allocentric",
            target_frame="egocentric",
            direction="north",
            agent_heading=0
        )

        assert result["frame"] == "egocentric"
        assert result["relative_position"] == "front"

    def test_allocentric_frame_independent_of_heading(self):
        """Allocentric frame doesn't change with agent's heading"""
        system = PerspectiveTakingSystem()

        # Object is north (allocentric) regardless of where I'm facing
        result1 = system.spatial_perspective(
            current_frame="allocentric",
            target_frame="allocentric",
            direction="north",
            agent_heading=0
        )

        result2 = system.spatial_perspective(
            current_frame="allocentric",
            target_frame="allocentric",
            direction="north",
            agent_heading=180
        )

        assert result1["direction"] == result2["direction"] == "north"


class TestConceptualPerspective:
    """Test conceptual perspective shifts"""

    def test_shift_belief_perspective(self):
        """Shift from my belief to their belief"""
        system = PerspectiveTakingSystem()

        my_belief = {"content": "The ball is in the basket", "holder": "self"}
        their_belief = {"content": "The ball is in the box", "holder": "other"}

        result = system.conceptual_perspective(
            current_belief=my_belief,
            target_belief=their_belief
        )

        assert result["adopted_belief"] == their_belief["content"]
        assert result["perspective_holder"] == "other"

    def test_perspective_shift_updates_knowledge(self):
        """Taking someone's perspective updates what I think they know"""
        system = PerspectiveTakingSystem()

        # I know X happened, but from their perspective they don't know
        my_knowledge = {"event": "ball_moved", "known": True}
        their_knowledge = {"event": "ball_moved", "known": False}

        result = system.conceptual_perspective(
            current_belief=my_knowledge,
            target_belief=their_knowledge
        )

        # From their perspective, event unknown
        assert result["adopted_belief"]["known"] == False

    def test_first_person_vs_third_person(self):
        """1st person (egocentric) vs 3rd person (allocentric) imagery"""
        system = PerspectiveTakingSystem()

        # 1st person: "I see the object in front of me"
        first_person = system.imagery_perspective(
            perspective_type="first_person",
            scene="object_in_front"
        )

        # 3rd person: "I see myself with the object in front of me"
        third_person = system.imagery_perspective(
            perspective_type="third_person",
            scene="object_in_front"
        )

        assert first_person["viewpoint"] == "egocentric"
        assert third_person["viewpoint"] == "allocentric"
        assert third_person["processing_cost"] > first_person["processing_cost"]


class TestIntegrationTheoryOfMind:
    """Test integration with LAB_027 (Theory of Mind)"""

    def test_perspective_informs_belief(self):
        """What they can see determines what they believe"""
        system = PerspectiveTakingSystem()

        # They are facing north, object is south of them
        # From their perspective: object is behind them (can't see)
        result = system.spatial_perspective(
            current_frame="allocentric",
            target_frame="egocentric",
            direction="south",  # Object location (allocentric)
            agent_heading=0  # They face north
        )

        # Object behind them → likely can't see it → false belief possible
        assert result["relative_position"] == "back"
        assert result.get("visible", True) == False  # Behind = not visible

    def test_perspective_for_false_belief_task(self):
        """Perspective taking supports Sally-Anne false belief task"""
        system = PerspectiveTakingSystem()

        # Sally's perspective: Last saw ball in basket
        # Reality: Ball moved to box (Sally didn't see)
        sally_perspective = system.conceptual_perspective(
            current_belief={"ball_location": "box", "holder": "self"},  # Reality
            target_belief={"ball_location": "basket", "holder": "Sally"}  # Sally's outdated belief
        )

        # From Sally's perspective, ball still in basket
        assert sally_perspective["adopted_belief"] == "basket"
        assert sally_perspective["perspective_holder"] == "Sally"


class TestPerspectiveShiftingProcess:
    """Test the process of shifting perspectives"""

    def test_perspective_shift_process(self):
        """Complete perspective shift process"""
        system = PerspectiveTakingSystem()

        result = system.shift_perspective(
            current_viewpoint={"position": "self", "heading": 0},
            target_viewpoint={"position": "other", "heading": 180},
            context={"object_location": "north"}
        )

        assert "transformation_applied" in result
        assert "rotation_cost" in result
        assert result["perspective_holder"] == "other"

    def test_shift_perspective_tracks_statistics(self):
        """Perspective shifts are tracked in statistics"""
        system = PerspectiveTakingSystem()

        initial_count = system.total_perspective_shifts

        system.shift_perspective(
            current_viewpoint={"position": "self", "heading": 0},
            target_viewpoint={"position": "other", "heading": 90},
            context={}
        )

        assert system.total_perspective_shifts == initial_count + 1

    def test_multiple_perspectives_simultaneously(self):
        """Can represent multiple perspectives at once (working memory)"""
        system = PerspectiveTakingSystem()

        perspectives = system.hold_multiple_perspectives([
            {"holder": "self", "belief": "A"},
            {"holder": "person1", "belief": "B"},
            {"holder": "person2", "belief": "C"}
        ])

        assert len(perspectives) == 3
        assert perspectives[0]["holder"] == "self"
        assert perspectives[1]["holder"] == "person1"


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_spatial_shift(self):
        """Process spatial perspective shift"""
        system = PerspectiveTakingSystem()

        result = system.process_event(
            event_type="spatial_shift",
            current_position={"x": 0, "y": 0, "heading": 0},
            target_position={"x": 5, "y": 0, "heading": 180},
            object_location={"x": 0, "y": 5}
        )

        assert "transformed_view" in result
        assert "rotation_cost" in result

    def test_process_conceptual_shift(self):
        """Process conceptual perspective shift"""
        system = PerspectiveTakingSystem()

        result = system.process_event(
            event_type="conceptual_shift",
            my_belief={"content": "X is true"},
            their_belief={"content": "X is false"}
        )

        assert "adopted_perspective" in result
        assert result["perspective_type"] == "conceptual"

    def test_process_event_updates_state(self):
        """process_event updates system state"""
        system = PerspectiveTakingSystem()

        initial_shifts = system.total_perspective_shifts

        system.process_event(
            event_type="spatial_shift",
            current_position={"x": 0, "y": 0, "heading": 0},
            target_position={"x": 0, "y": 0, "heading": 90},
            object_location={"x": 1, "y": 0}
        )

        assert system.total_perspective_shifts > initial_shifts


class TestGetState:
    """Test state retrieval"""

    def test_get_state_returns_statistics(self):
        """get_state returns current system statistics"""
        system = PerspectiveTakingSystem()

        # Perform some perspective shifts
        system.shift_perspective(
            current_viewpoint={"position": "self", "heading": 0},
            target_viewpoint={"position": "other", "heading": 90},
            context={}
        )

        state = system.get_state()

        assert "total_perspective_shifts" in state
        assert "rotation_cost_per_degree" in state
        assert state["total_perspective_shifts"] == 1

    def test_get_state_serializable(self):
        """get_state returns JSON-serializable dict"""
        system = PerspectiveTakingSystem()

        state = system.get_state()

        # Should be JSON serializable
        import json
        json_str = json.dumps(state)
        assert json_str is not None
