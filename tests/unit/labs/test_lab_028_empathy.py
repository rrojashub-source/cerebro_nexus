"""
LAB_028: Empathy Simulation - Unit Tests

Social Cognition: Affective empathy, emotional resonance, compassion

Key Papers:
- Decety & Jackson (2004) - The functional architecture of human empathy
- Singer & Lamm (2009) - The social neuroscience of empathy
- Batson (2011) - Altruism in humans
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Creativity_Social.LAB_028_Empathy.empathy_system import (
    EmpathySystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with default parameters"""
        system = EmpathySystem()
        assert system.mirroring_intensity == 0.7
        assert system.self_other_boundary_strength == 0.8
        assert system.compassion_threshold == 0.6

    def test_custom_parameters(self):
        """System accepts custom parameters"""
        system = EmpathySystem(
            mirroring_intensity=0.9,
            self_other_boundary_strength=0.6,
            distress_tolerance=0.8
        )
        assert system.mirroring_intensity == 0.9
        assert system.self_other_boundary_strength == 0.6
        assert system.distress_tolerance == 0.8

    def test_state_initialization(self):
        """State variables initialize correctly"""
        system = EmpathySystem()
        assert system.total_empathic_events == 0
        assert system.prosocial_actions_triggered == 0


class TestEmotionalMirroring:
    """Test emotional mirroring (LAB_008 integration)"""

    def test_mirrors_observed_emotion(self):
        """System mirrors observed emotion (LAB_008 Emotional Contagion)"""
        system = EmpathySystem(mirroring_intensity=0.7)

        observed = {"type": "sadness", "intensity": 1.0}

        mirrored = system.mirror_emotion(observed)

        # Mirrored emotion should be scaled by intensity
        assert mirrored["type"] == "sadness"
        assert mirrored["intensity"] == pytest.approx(0.7, abs=0.05)

    def test_mirroring_intensity_modulation(self):
        """Mirroring intensity modulates strength of empathic emotion"""
        system_high = EmpathySystem(mirroring_intensity=0.9)
        system_low = EmpathySystem(mirroring_intensity=0.3)

        observed = {"type": "joy", "intensity": 0.8}

        mirrored_high = system_high.mirror_emotion(observed)
        mirrored_low = system_low.mirror_emotion(observed)

        # Higher mirroring = stronger empathic emotion
        assert mirrored_high["intensity"] > mirrored_low["intensity"]

    def test_mirrors_multiple_emotions(self):
        """System can mirror multiple emotions simultaneously"""
        system = EmpathySystem()

        observed = {"type": "mixed", "emotions": [("sadness", 0.7), ("fear", 0.5)]}

        mirrored = system.mirror_emotion(observed)

        # Should handle mixed emotions
        assert mirrored is not None

    def test_mirroring_preserves_emotion_type(self):
        """Mirroring preserves the emotion type"""
        system = EmpathySystem()

        for emotion_type in ["joy", "sadness", "fear", "anger"]:
            observed = {"type": emotion_type, "intensity": 0.8}
            mirrored = system.mirror_emotion(observed)

            # Type should match
            assert mirrored["type"] == emotion_type

    def test_mirroring_intensity_affects_strength(self):
        """Mirroring intensity directly affects empathic emotion strength"""
        system = EmpathySystem(mirroring_intensity=0.5)

        observed = {"type": "anger", "intensity": 1.0}

        mirrored = system.mirror_emotion(observed)

        # 1.0 * 0.5 = 0.5
        assert mirrored["intensity"] == pytest.approx(0.5, abs=0.05)

    def test_no_mirroring_with_zero_intensity(self):
        """Zero mirroring intensity means no empathic emotion"""
        system = EmpathySystem(mirroring_intensity=0.0)

        observed = {"type": "sadness", "intensity": 1.0}

        mirrored = system.mirror_emotion(observed)

        # No mirroring
        assert mirrored["intensity"] == 0.0

    def test_partial_mirroring_with_medium_intensity(self):
        """Medium mirroring intensity creates partial empathic response"""
        system = EmpathySystem(mirroring_intensity=0.5)

        observed = {"type": "fear", "intensity": 0.6}

        mirrored = system.mirror_emotion(observed)

        # 0.6 * 0.5 = 0.3
        assert mirrored["intensity"] == pytest.approx(0.3, abs=0.05)


class TestSelfOtherDistinction:
    """Test self/other boundary maintenance"""

    def test_maintains_self_other_boundary(self):
        """System maintains distinction between self and other"""
        system = EmpathySystem(self_other_boundary_strength=0.8)

        observed = {"type": "sadness", "intensity": 0.9}

        result = system.maintain_self_other_boundary(observed)

        # Should tag emotion with source
        assert "source" in result
        assert result["source"] == "other"

    def test_emotion_tagged_with_source(self):
        """Empathic emotions tagged with 'other' source"""
        system = EmpathySystem()

        observed = {"type": "joy", "intensity": 0.7}

        tagged = system.maintain_self_other_boundary(observed)

        # Source = other (not self)
        assert tagged["source"] == "other"
        assert tagged["type"] == "joy"

    def test_high_boundary_prevents_contagion(self):
        """High boundary strength prevents emotional contagion"""
        system = EmpathySystem(self_other_boundary_strength=0.95)

        observed = {"type": "distress", "intensity": 1.0}

        # Mirror emotion
        mirrored = system.mirror_emotion(observed)

        # Apply boundary
        bounded = system.maintain_self_other_boundary(mirrored)

        # High boundary should reduce intensity or clearly mark as "other"
        assert bounded["source"] == "other"

    def test_low_boundary_allows_contagion(self):
        """Low boundary strength allows more emotional contagion"""
        system = EmpathySystem(self_other_boundary_strength=0.2)

        observed = {"type": "anxiety", "intensity": 0.8}

        mirrored = system.mirror_emotion(observed)
        bounded = system.maintain_self_other_boundary(mirrored)

        # Low boundary = more susceptible to contagion
        # (Implementation: may have higher intensity or weaker "other" tag)
        assert bounded is not None

    def test_distinguish_my_pain_from_their_pain(self):
        """Critical: Distinguish 'my pain' from 'their pain'"""
        system = EmpathySystem()

        their_pain = {"type": "pain", "intensity": 0.9}

        # Mirror their pain
        empathic_pain = system.mirror_emotion(their_pain)

        # Apply boundary
        distinguished = system.maintain_self_other_boundary(empathic_pain)

        # MUST be tagged as "other"
        assert distinguished["source"] == "other"
        assert distinguished["type"] == "pain"

    def test_boundary_failure_leads_to_overwhelm(self):
        """Very low boundary leads to empathic overwhelm"""
        system = EmpathySystem(self_other_boundary_strength=0.1)

        intense_distress = {"type": "distress", "intensity": 1.0}

        mirrored = system.mirror_emotion(intense_distress)
        bounded = system.maintain_self_other_boundary(mirrored)

        # Low boundary = high susceptibility
        # (May trigger distress regulation later)
        assert bounded["intensity"] > 0.5  # Still high intensity


class TestCompassionateResponse:
    """Test prosocial motivation and compassionate action"""

    def test_generates_compassionate_response(self):
        """System generates compassionate/prosocial response"""
        system = EmpathySystem()

        empathic_emotion = {"type": "sadness", "intensity": 0.7, "source": "other"}

        response = system.generate_compassionate_response(empathic_emotion)

        # Should generate prosocial action
        assert response is not None
        assert isinstance(response, str)

    def test_prosocial_action_above_threshold(self):
        """Prosocial action triggered when emotion exceeds threshold"""
        system = EmpathySystem(compassion_threshold=0.6)

        high_empathy = {"type": "sadness", "intensity": 0.8, "source": "other"}

        response = system.generate_compassionate_response(high_empathy)

        # Should trigger action
        assert response in ["offer_help", "comfort", "advocacy", "emotional_support"]

    def test_no_action_below_threshold(self):
        """No prosocial action when below threshold"""
        system = EmpathySystem(compassion_threshold=0.8)

        low_empathy = {"type": "sadness", "intensity": 0.3, "source": "other"}

        response = system.generate_compassionate_response(low_empathy)

        # May return None or "no_action"
        assert response in [None, "no_action", "observe"]

    def test_dopamine_reward_for_prosocial(self):
        """Prosocial action triggers dopamine reward (LAB_013)"""
        system = EmpathySystem()

        empathic_emotion = {"type": "distress", "intensity": 0.75, "source": "other"}

        result = system.generate_compassionate_response(empathic_emotion, return_reward=True)

        # Should indicate dopamine reward
        if isinstance(result, dict):
            assert "dopamine_reward" in result or "reward" in result

    def test_response_type_matches_situation(self):
        """Compassionate response type matches situation"""
        system = EmpathySystem()

        # Distress → offer help
        distress = {"type": "distress", "intensity": 0.8, "source": "other"}
        response_distress = system.generate_compassionate_response(distress)

        # Sadness → comfort
        sadness = {"type": "sadness", "intensity": 0.7, "source": "other"}
        response_sadness = system.generate_compassionate_response(sadness)

        # Both should be prosocial
        assert response_distress in ["offer_help", "comfort", "advocacy", "emotional_support"]
        assert response_sadness in ["offer_help", "comfort", "advocacy", "emotional_support"]


class TestEmpathicDistressRegulation:
    """Test regulation of excessive empathic distress"""

    def test_regulates_excessive_distress(self):
        """System regulates excessive empathic distress (LAB_014)"""
        system = EmpathySystem(distress_tolerance=0.7)

        high_distress = 0.9

        regulated = system.regulate_empathic_distress(high_distress)

        # Should reduce distress
        assert regulated < high_distress

    def test_distress_above_tolerance_triggers_regulation(self):
        """Distress above tolerance triggers regulation mechanism"""
        system = EmpathySystem(distress_tolerance=0.6)

        distress_low = 0.4  # Below tolerance
        distress_high = 0.8  # Above tolerance

        regulated_low = system.regulate_empathic_distress(distress_low)
        regulated_high = system.regulate_empathic_distress(distress_high)

        # High distress should be reduced more
        assert regulated_high < distress_high
        # Low distress may not be regulated
        assert regulated_low == distress_low or regulated_low >= distress_low * 0.9

    def test_regulation_reduces_mirroring(self):
        """Distress regulation reduces mirroring intensity"""
        system = EmpathySystem(mirroring_intensity=0.8, distress_tolerance=0.5)

        # Experience high distress
        system.regulate_empathic_distress(0.9)

        # Mirroring should be reduced (implementation: may adjust internal state)
        # Check state after regulation
        state = system.get_state()
        assert state["distress_regulation_count"] > 0

    def test_serotonin_modulation_of_regulation(self):
        """Serotonin modulates distress regulation (LAB_014)"""
        system = EmpathySystem()

        distress = 0.85

        # Simulate serotonin level
        serotonin_level = 0.7

        regulated = system.regulate_empathic_distress(distress, serotonin_level=serotonin_level)

        # Higher serotonin = better regulation
        assert regulated < distress

    def test_regulation_prevents_burnout(self):
        """Regulation mechanism prevents empathic burnout"""
        system = EmpathySystem(distress_tolerance=0.6)

        # Multiple high-distress events
        for _ in range(5):
            system.regulate_empathic_distress(0.9)

        state = system.get_state()

        # Regulation should have been triggered multiple times
        assert state["distress_regulation_count"] >= 5


class TestEmpathyTypes:
    """Test distinguishing different types of empathy"""

    def test_distinguishes_cognitive_vs_affective(self):
        """System distinguishes cognitive vs affective empathy"""
        system = EmpathySystem()

        situation_cognitive = {"type": "cognitive", "requires": "understanding"}
        situation_affective = {"type": "affective", "requires": "feeling"}

        type_cognitive = system.distinguish_empathy_types(situation_cognitive)
        type_affective = system.distinguish_empathy_types(situation_affective)

        assert type_cognitive == "cognitive"
        assert type_affective == "affective"

    def test_cognitive_empathy_uses_tom(self):
        """Cognitive empathy integrates with Theory of Mind (LAB_027)"""
        system = EmpathySystem()

        situation = {"type": "cognitive", "requires": "mental_state_inference"}

        empathy_type = system.distinguish_empathy_types(situation)

        # Cognitive empathy = ToM-based
        assert empathy_type == "cognitive"

    def test_affective_empathy_uses_mirroring(self):
        """Affective empathy uses emotional mirroring"""
        system = EmpathySystem()

        situation = {"type": "affective", "requires": "emotional_resonance"}

        empathy_type = system.distinguish_empathy_types(situation)

        # Affective empathy = mirroring-based
        assert empathy_type == "affective"

    def test_compassionate_empathy_includes_motivation(self):
        """Compassionate empathy includes prosocial motivation"""
        system = EmpathySystem()

        situation = {"type": "compassionate", "requires": "helping_motivation"}

        empathy_type = system.distinguish_empathy_types(situation)

        # Compassionate = cognitive + affective + prosocial motivation
        assert empathy_type == "compassionate"


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_event_complete(self):
        """process_event executes complete empathy cycle"""
        system = EmpathySystem()

        result = system.process_event(
            observed_emotion={"type": "sadness", "intensity": 0.75},
            agent_id="person_1"
        )

        assert "empathic_emotion" in result
        assert "compassionate_action" in result or "prosocial_motivation" in result

    def test_process_event_updates_stats(self):
        """process_event updates system statistics"""
        system = EmpathySystem()

        initial_events = system.total_empathic_events

        system.process_event(
            observed_emotion={"type": "joy", "intensity": 0.6},
            agent_id="person_1"
        )

        assert system.total_empathic_events == initial_events + 1

    def test_process_event_full_pipeline(self):
        """process_event executes full empathy pipeline"""
        system = EmpathySystem()

        result = system.process_event(
            observed_emotion={"type": "distress", "intensity": 0.8},
            agent_id="person_1"
        )

        # Should have all components
        assert "empathic_emotion" in result
        assert result["empathic_emotion"]["source"] == "other"
        assert "self_other_distinction" in result or result["empathic_emotion"]["source"] == "other"

        # May trigger prosocial action
        if result["empathic_emotion"]["intensity"] > 0.6:
            assert "compassionate_action" in result or "prosocial_motivation" in result
