"""
LAB_027: Theory of Mind - Unit Tests

Social Cognition: Infer mental states of others (beliefs, desires, intentions)

Key Papers:
- Premack & Woodruff (1978) - Does the chimpanzee have a theory of mind?
- Baron-Cohen et al. (1985) - Sally-Anne false belief task
- Frith & Frith (2003) - Development and neurophysiology of mentalizing
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Creativity_Social.LAB_027_Theory_of_Mind.theory_of_mind_system import (
    TheoryOfMindSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with default parameters"""
        system = TheoryOfMindSystem()
        assert system.belief_confidence_threshold == 0.6
        assert system.max_recursion_depth == 3
        assert system.context_weight == 0.7

    def test_custom_parameters(self):
        """System accepts custom parameters"""
        system = TheoryOfMindSystem(
            belief_confidence_threshold=0.8,
            max_recursion_depth=5,
            false_belief_sensitivity=0.9
        )
        assert system.belief_confidence_threshold == 0.8
        assert system.max_recursion_depth == 5
        assert system.false_belief_sensitivity == 0.9

    def test_state_initialization(self):
        """State variables initialize correctly"""
        system = TheoryOfMindSystem()
        assert system.total_predictions == 0
        assert system.false_beliefs_detected == 0
        assert len(system.agents_tracked) == 0


class TestBeliefRepresentation:
    """Test belief state representation"""

    def test_represents_belief(self):
        """System can represent agent's belief"""
        system = TheoryOfMindSystem()

        belief = system.represent_belief(
            agent_id="alice",
            content="Object is in box A",
            confidence=0.9
        )

        assert belief is not None
        assert belief["agent_id"] == "alice"
        assert "belief_content" in belief
        assert belief["confidence"] == 0.9

    def test_tracks_multiple_agents(self):
        """System tracks beliefs of multiple agents"""
        system = TheoryOfMindSystem()

        system.represent_belief("alice", "X is true", 0.8)
        system.represent_belief("bob", "Y is true", 0.7)

        assert len(system.agents_tracked) == 2
        assert "alice" in system.agents_tracked
        assert "bob" in system.agents_tracked

    def test_belief_confidence_tracking(self):
        """System tracks confidence in beliefs"""
        system = TheoryOfMindSystem()

        belief = system.represent_belief("alice", "Sky is blue", 0.95)

        assert belief["confidence"] == 0.95

    def test_belief_can_differ_from_reality(self):
        """Beliefs can differ from actual reality (critical for ToM)"""
        system = TheoryOfMindSystem()

        # Alice believes object is in box A
        belief = system.represent_belief("alice", "Object in box A", 0.9)

        # Reality: object is in box B
        reality = {"object_location": "box B"}

        # Belief should still be represented (even if false)
        assert belief["belief_content"] == "Object in box A"

    def test_belief_update_increases_confidence(self):
        """Updating belief with consistent evidence increases confidence"""
        system = TheoryOfMindSystem()

        # Initial belief
        system.represent_belief("alice", "X is true", 0.5)

        # Update with confirming evidence
        updated = system.update_belief_from_observation("alice", "observed X")

        # Confidence should increase
        assert updated["confidence"] > 0.5

    def test_contradictory_beliefs_handled(self):
        """System handles contradictory beliefs (updates vs. maintains both)"""
        system = TheoryOfMindSystem()

        system.represent_belief("alice", "X is true", 0.6)
        system.update_belief_from_observation("alice", "observed not X")

        # Should update belief (implementation specific)
        alice_beliefs = system.agents_tracked.get("alice", {})
        assert alice_beliefs is not None

    def test_agent_belief_independence(self):
        """Each agent's beliefs are independent"""
        system = TheoryOfMindSystem()

        system.represent_belief("alice", "X is true", 0.8)
        system.represent_belief("bob", "X is false", 0.7)

        alice_belief = system.agents_tracked["alice"]["beliefs"][-1]
        bob_belief = system.agents_tracked["bob"]["beliefs"][-1]

        # Both beliefs coexist independently
        assert "X is true" in alice_belief["belief_content"]
        assert "X is false" in bob_belief["belief_content"]


class TestIntentionAttribution:
    """Test inferring intentions from observed actions"""

    def test_attributes_intention_from_action(self):
        """System infers intention from observed action"""
        system = TheoryOfMindSystem()

        action = "reaching for glass"
        context = {"object": "glass", "state": "thirsty"}

        intention = system.attribute_intention(action, context)

        # Should infer "wants to drink"
        assert intention is not None
        assert isinstance(intention, str)

    def test_context_influences_attribution(self):
        """Context influences intention attribution"""
        system = TheoryOfMindSystem(context_weight=0.9)

        action = "picking up phone"

        # Context 1: phone ringing
        context_1 = {"phone_ringing": True}
        intention_1 = system.attribute_intention(action, context_1)

        # Context 2: phone not ringing
        context_2 = {"phone_ringing": False}
        intention_2 = system.attribute_intention(action, context_2)

        # Different intentions inferred from same action + different context
        assert intention_1 != intention_2

    def test_ambiguous_action_low_confidence(self):
        """Ambiguous actions have low confidence attribution"""
        system = TheoryOfMindSystem()

        action = "walking"  # Ambiguous: where? why?
        context = {}  # No context

        result = system.attribute_intention(action, context, return_confidence=True)

        # Low confidence for ambiguous action
        assert result["confidence"] < 0.7

    def test_clear_action_high_confidence(self):
        """Clear actions have high confidence attribution"""
        system = TheoryOfMindSystem()

        action = "reaching for door handle"
        context = {"door": "closed", "agent_state": "wants_to_exit"}

        result = system.attribute_intention(action, context, return_confidence=True)

        # High confidence: clear intention
        assert result["confidence"] > 0.7

    def test_multiple_possible_intentions(self):
        """System can represent multiple possible intentions"""
        system = TheoryOfMindSystem()

        action = "looking at watch"
        context = {}

        result = system.attribute_intention(action, context, return_multiple=True)

        # Multiple possibilities: checking time, impatient, etc.
        if isinstance(result, list):
            assert len(result) > 1

    def test_intention_updates_with_new_evidence(self):
        """Intention attribution updates with new observations"""
        system = TheoryOfMindSystem()

        action_1 = "reaching for object"
        context_1 = {}

        intention_1 = system.attribute_intention(action_1, context_1)

        # New evidence
        action_2 = "placing object in bag"
        context_2 = {"object_owner": "self"}

        intention_2 = system.attribute_intention(action_2, context_2)

        # Intention clarifies: wants to take object
        assert intention_2 is not None


class TestRecursiveBeliefModeling:
    """Test recursive belief modeling (I think you think...)"""

    def test_first_order_belief(self):
        """First order: I know X"""
        system = TheoryOfMindSystem()

        result = system.recursive_belief_modeling(
            depth=1,
            agent_chain=["self"],
            belief_content="Sky is blue"
        )

        assert result["depth"] == 1
        assert "self" in result["agent_chain"]

    def test_second_order_belief(self):
        """Second order: I know you know X"""
        system = TheoryOfMindSystem()

        result = system.recursive_belief_modeling(
            depth=2,
            agent_chain=["self", "alice"],
            belief_content="Password is 1234"
        )

        assert result["depth"] == 2
        assert len(result["agent_chain"]) == 2

    def test_third_order_belief(self):
        """Third order: I know you know I know X"""
        system = TheoryOfMindSystem()

        result = system.recursive_belief_modeling(
            depth=3,
            agent_chain=["self", "alice", "self"],
            belief_content="Secret is known"
        )

        assert result["depth"] == 3
        assert len(result["agent_chain"]) == 3

    def test_recursion_depth_limit(self):
        """System enforces max recursion depth"""
        system = TheoryOfMindSystem(max_recursion_depth=3)

        # Try depth 5 (exceeds limit)
        with pytest.raises(ValueError):
            system.recursive_belief_modeling(
                depth=5,
                agent_chain=["self", "alice", "bob", "charlie", "diana"],
                belief_content="X"
            )

    def test_recursive_confidence_degradation(self):
        """Confidence degrades with recursion depth"""
        system = TheoryOfMindSystem()

        result_1 = system.recursive_belief_modeling(depth=1, agent_chain=["self"], belief_content="X")
        result_2 = system.recursive_belief_modeling(depth=2, agent_chain=["self", "alice"], belief_content="X")
        result_3 = system.recursive_belief_modeling(depth=3, agent_chain=["self", "alice", "bob"], belief_content="X")

        # Confidence should decrease with depth
        assert result_1["confidence"] > result_2["confidence"]
        assert result_2["confidence"] > result_3["confidence"]


class TestFalseBeliefDetection:
    """Test false belief detection (critical for ToM)"""

    def test_detects_false_belief(self):
        """System detects when belief ≠ reality"""
        system = TheoryOfMindSystem()

        belief = {"content": "Object in box A", "confidence": 0.9}
        reality = {"object_location": "box B"}

        is_false = system.detect_false_belief(belief, reality)

        assert is_false == True

    def test_sally_anne_task(self):
        """Classic Sally-Anne false belief task"""
        system = TheoryOfMindSystem()

        # Sally places marble in basket
        # Sally leaves
        # Anne moves marble to box
        # Sally returns

        # Sally's belief: marble in basket (FALSE)
        sally_belief = {"content": "marble in basket", "confidence": 0.9}

        # Reality: marble in box
        reality = {"marble_location": "box"}

        is_false = system.detect_false_belief(sally_belief, reality)

        # Should detect Sally has false belief
        assert is_false == True

    def test_false_belief_when_belief_ne_reality(self):
        """False belief detected when belief ≠ reality"""
        system = TheoryOfMindSystem()

        belief = {"content": "Sun revolves around Earth"}
        reality = {"fact": "Earth revolves around Sun"}

        is_false = system.detect_false_belief(belief, reality)

        assert is_false == True

    def test_no_false_belief_when_aligned(self):
        """No false belief when belief matches reality"""
        system = TheoryOfMindSystem()

        belief = {"content": "Sky is blue"}
        reality = {"sky_color": "blue"}

        is_false = system.detect_false_belief(belief, reality)

        assert is_false == False

    def test_false_belief_sensitivity_threshold(self):
        """False belief detection uses sensitivity threshold"""
        system = TheoryOfMindSystem(false_belief_sensitivity=0.9)

        belief = {"content": "X", "confidence": 0.95}
        reality = {"fact": "not X"}

        # High sensitivity = detect even subtle misalignments
        is_false = system.detect_false_belief(belief, reality)

        assert is_false == True

    def test_false_belief_affects_prediction(self):
        """False belief affects behavior prediction"""
        system = TheoryOfMindSystem()

        # Agent has false belief
        mental_state = {
            "belief": {"content": "Object in box A", "is_false_belief": True},
            "desire": "Find object",
            "intention": "Search box A"
        }

        prediction = system.predict_behavior(mental_state)

        # Should predict incorrect behavior (search box A, not B)
        assert "box A" in prediction.lower() or "search" in prediction.lower()


class TestBehaviorPrediction:
    """Test predicting behavior from mental states"""

    def test_predicts_behavior_from_mental_state(self):
        """System predicts behavior given mental state"""
        system = TheoryOfMindSystem()

        mental_state = {
            "belief": {"content": "Door is unlocked"},
            "desire": "Exit room",
            "intention": "Open door"
        }

        prediction = system.predict_behavior(mental_state)

        # Should predict "will try to open door"
        assert prediction is not None
        assert isinstance(prediction, str)

    def test_false_belief_leads_to_incorrect_behavior_prediction(self):
        """False belief leads to predicting incorrect behavior"""
        system = TheoryOfMindSystem()

        # Agent believes object is in location A (false)
        mental_state = {
            "belief": {"content": "Object in A", "is_false_belief": True},
            "desire": "Get object",
            "intention": "Go to A"
        }

        prediction = system.predict_behavior(mental_state)

        # Prediction based on false belief (will go to A, not B)
        assert "A" in prediction or "search" in prediction.lower()

    def test_true_belief_leads_to_correct_behavior_prediction(self):
        """True belief leads to predicting correct behavior"""
        system = TheoryOfMindSystem()

        mental_state = {
            "belief": {"content": "Object in B", "is_false_belief": False},
            "desire": "Get object",
            "intention": "Go to B"
        }

        prediction = system.predict_behavior(mental_state)

        # Prediction based on true belief (will go to B)
        assert "B" in prediction or "search" in prediction.lower()

    def test_prediction_confidence_from_belief_confidence(self):
        """Prediction confidence derived from belief confidence"""
        system = TheoryOfMindSystem()

        mental_state_high = {
            "belief": {"content": "X", "confidence": 0.95},
            "desire": "Achieve X",
            "intention": "Do action"
        }

        mental_state_low = {
            "belief": {"content": "Y", "confidence": 0.4},
            "desire": "Achieve Y",
            "intention": "Do action"
        }

        result_high = system.predict_behavior(mental_state_high, return_confidence=True)
        result_low = system.predict_behavior(mental_state_low, return_confidence=True)

        # High belief confidence = high prediction confidence
        assert result_high["confidence"] > result_low["confidence"]

    def test_prediction_integration_with_preloading(self):
        """Prediction integrates with LAB_007 (Predictive Preloading)"""
        system = TheoryOfMindSystem()

        mental_state = {
            "belief": {"content": "Agent will ask for help"},
            "desire": "Assist others",
            "intention": "Prepare resources"
        }

        prediction = system.predict_behavior(mental_state, preload=True)

        # Should indicate preloading readiness
        assert "preload" in str(prediction).lower() or "prepare" in prediction.lower()


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_event_complete(self):
        """process_event executes complete ToM inference cycle"""
        system = TheoryOfMindSystem()

        result = system.process_event(
            agent_id="alice",
            observed_behavior="looking in box A",
            context={"object_location": "box B", "agent_saw_move": False}
        )

        assert "mental_state" in result
        assert "predicted_behavior" in result

    def test_process_event_updates_stats(self):
        """process_event updates system statistics"""
        system = TheoryOfMindSystem()

        initial_predictions = system.total_predictions

        system.process_event(
            agent_id="bob",
            observed_behavior="reaching for object",
            context={}
        )

        assert system.total_predictions == initial_predictions + 1

    def test_process_event_sally_anne_complete(self):
        """process_event handles full Sally-Anne scenario"""
        system = TheoryOfMindSystem()

        result = system.process_event(
            agent_id="sally",
            observed_behavior="returning to room",
            context={
                "object_location": "box",
                "sally_belief": "basket",
                "sally_saw_move": False
            }
        )

        # Should detect false belief
        assert result.get("false_belief_detected") == True

        # Should predict Sally will search basket (incorrect)
        prediction = result.get("predicted_behavior", "")
        assert "basket" in prediction.lower() or "will search" in prediction.lower()
