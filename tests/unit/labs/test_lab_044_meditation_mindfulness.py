"""
LAB_044: Meditation/Mindfulness - Unit Tests

Homeostasis: "Awareness & emotional regulation"

Key Papers:
- Kabat-Zinn (2003) - Mindfulness-Based Stress Reduction
- Tang et al. (2015) - The neuroscience of mindfulness meditation
- Lutz et al. (2008) - Attention regulation and monitoring in meditation
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Advanced_Learning.LAB_044_Meditation_Mindfulness.meditation_system import (
    MeditationSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with default meditation parameters"""
        system = MeditationSystem()
        assert system.mindfulness_level == 0.0
        assert system.is_meditating == False

    def test_custom_breath_rate(self):
        """System accepts custom breath rate"""
        system = MeditationSystem(breath_rate=12)
        assert system.breath_rate == 12

    def test_custom_body_scan_duration(self):
        """System accepts custom body scan duration"""
        system = MeditationSystem(body_scan_duration=20)
        assert system.body_scan_duration == 20


class TestPresentMomentAwareness:
    """Test present-moment awareness"""

    def test_awareness_increases_with_practice(self):
        """Meditation practice → Increased awareness"""
        system = MeditationSystem()

        initial_awareness = system.mindfulness_level

        # Practice meditation
        system.practice_present_moment_awareness(duration_minutes=10)

        assert system.mindfulness_level > initial_awareness

    def test_longer_practice_stronger_awareness(self):
        """Longer practice → Stronger awareness"""
        system1 = MeditationSystem()
        system1.practice_present_moment_awareness(duration_minutes=5)

        system2 = MeditationSystem()
        system2.practice_present_moment_awareness(duration_minutes=30)

        assert system2.mindfulness_level > system1.mindfulness_level

    def test_awareness_decays_without_practice(self):
        """No practice → Awareness gradually decays"""
        system = MeditationSystem()

        system.practice_present_moment_awareness(duration_minutes=20)
        high_awareness = system.mindfulness_level

        # Simulate decay (days without practice)
        system.apply_awareness_decay(days=7)

        assert system.mindfulness_level < high_awareness


class TestNonJudgmentalObservation:
    """Test non-judgmental observation"""

    def test_nonjudgmental_stance_reduces_reactivity(self):
        """Non-judgmental observation → Reduced emotional reactivity"""
        system = MeditationSystem()

        result = system.practice_nonjudgmental_observation(
            emotional_intensity=0.8
        )

        assert result["reactivity_reduced"] == True
        assert result["acceptance_level"] > 0.5

    def test_judgment_increases_reactivity(self):
        """Judgmental stance → Increased reactivity"""
        system = MeditationSystem()

        result_nonjudgmental = system.practice_nonjudgmental_observation(
            emotional_intensity=0.8
        )

        result_judgmental = system.observe_with_judgment(
            emotional_intensity=0.8
        )

        assert result_nonjudgmental["acceptance_level"] > result_judgmental["acceptance_level"]

    def test_acceptance_correlates_with_mindfulness(self):
        """Higher mindfulness → Higher acceptance"""
        system = MeditationSystem()

        # Build mindfulness
        system.practice_present_moment_awareness(duration_minutes=30)

        result = system.practice_nonjudgmental_observation(emotional_intensity=0.7)

        assert result["acceptance_level"] > 0.7


class TestBreathAwareness:
    """Test breath awareness (anchor point)"""

    def test_breath_focus_calms_mind(self):
        """Breath awareness → Mental calm"""
        system = MeditationSystem()

        result = system.practice_breath_awareness(duration_minutes=10)

        assert result["calmness_level"] > 0.5

    def test_slower_breath_deeper_calm(self):
        """Slower breathing → Deeper calm"""
        system1 = MeditationSystem(breath_rate=18)  # Faster
        result1 = system1.practice_breath_awareness(duration_minutes=10)

        system2 = MeditationSystem(breath_rate=6)  # Slower
        result2 = system2.practice_breath_awareness(duration_minutes=10)

        assert result2["calmness_level"] > result1["calmness_level"]

    def test_breath_as_anchor_reduces_mind_wandering(self):
        """Breath anchor → Reduced mind wandering"""
        system = MeditationSystem()

        result = system.practice_breath_awareness(duration_minutes=15)

        assert result["mind_wandering"] < 0.3


class TestBodyScan:
    """Test body scan (somatic awareness)"""

    def test_body_scan_increases_somatic_awareness(self):
        """Body scan → Increased body awareness"""
        system = MeditationSystem()

        result = system.perform_body_scan(duration_minutes=20)

        assert result["somatic_awareness"] > 0.7

    def test_body_scan_releases_tension(self):
        """Body scan → Tension release"""
        system = MeditationSystem()

        result = system.perform_body_scan(
            duration_minutes=20,
            initial_tension=0.8
        )

        assert result["tension_after"] < 0.8

    def test_longer_scan_more_relaxation(self):
        """Longer body scan → More relaxation"""
        system1 = MeditationSystem()
        result1 = system1.perform_body_scan(duration_minutes=5, initial_tension=0.8)

        system2 = MeditationSystem()
        result2 = system2.perform_body_scan(duration_minutes=30, initial_tension=0.8)

        assert result2["tension_after"] < result1["tension_after"]


class TestEmotionalRegulation:
    """Test emotional regulation through mindfulness"""

    def test_mindfulness_regulates_negative_emotions(self):
        """Mindfulness → Regulation of negative emotions"""
        system = MeditationSystem()

        # Build mindfulness
        system.practice_present_moment_awareness(duration_minutes=20)

        result = system.regulate_emotion(
            emotion="fear",
            intensity=0.9
        )

        assert result["regulated_intensity"] < 0.9

    def test_higher_mindfulness_better_regulation(self):
        """Higher mindfulness → Better emotion regulation"""
        system_low = MeditationSystem()
        system_low.mindfulness_level = 0.3

        system_high = MeditationSystem()
        system_high.mindfulness_level = 0.9

        result_low = system_low.regulate_emotion(emotion="anger", intensity=0.8)
        result_high = system_high.regulate_emotion(emotion="anger", intensity=0.8)

        assert result_high["regulated_intensity"] < result_low["regulated_intensity"]

    def test_regulation_without_suppression(self):
        """Mindfulness regulates without suppression (acceptance-based)"""
        system = MeditationSystem()
        system.mindfulness_level = 0.8

        result = system.regulate_emotion(emotion="sadness", intensity=0.7)

        assert result["regulation_type"] == "acceptance"
        assert result["suppressed"] == False


class TestIntegration:
    """Test integration with other LABs"""

    def test_integration_with_stress_reduction(self):
        """LAB_033: Mindfulness reduces stress & allostatic load"""
        system = MeditationSystem()

        result = system.practice_present_moment_awareness(duration_minutes=20)

        assert result.get("stress_reduction", 0) > 0

    def test_integration_with_rest_recovery(self):
        """LAB_034: Meditation enhances rest quality"""
        system = MeditationSystem()

        system.is_meditating = True

        result = system.get_rest_quality_boost()

        assert result["rest_quality_multiplier"] > 1.0

    def test_integration_with_default_mode_network(self):
        """LAB_046: Meditation modulates DMN activity"""
        system = MeditationSystem()

        system.is_meditating = True

        result = system.get_dmn_modulation()

        assert result["dmn_modulated"] == True


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_meditation_event(self):
        """Process meditation session event"""
        system = MeditationSystem()

        result = system.process_event(
            event_type="meditate",
            duration_minutes=15
        )

        assert "mindfulness_level" in result

    def test_process_body_scan_event(self):
        """Process body scan event"""
        system = MeditationSystem()

        result = system.process_event(
            event_type="body_scan",
            duration_minutes=20
        )

        assert "somatic_awareness" in result


class TestGetState:
    """Test state retrieval"""

    def test_get_state_returns_meditation_metrics(self):
        """get_state returns meditation metrics"""
        system = MeditationSystem()

        system.practice_present_moment_awareness(duration_minutes=10)

        state = system.get_state()

        assert "mindfulness_level" in state
        assert "is_meditating" in state

    def test_get_state_serializable(self):
        """get_state returns JSON-serializable dict"""
        system = MeditationSystem()

        state = system.get_state()

        import json
        json_str = json.dumps(state)
        assert json_str is not None
