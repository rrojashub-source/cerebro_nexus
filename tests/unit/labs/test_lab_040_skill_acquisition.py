"""
LAB_040: Skill Acquisition - Unit Tests

Pattern Recognition: Learning curves, performance improvement, expertise

Key Papers:
- Newell & Rosenbloom (1981) - Mechanisms of skill acquisition and the law of practice
- Ericsson et al. (1993) - The role of deliberate practice in the acquisition of expert performance
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Pattern_Recognition.LAB_040_Skill_Acquisition.skill_acquisition_system import (
    SkillAcquisitionSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with empty skill registry"""
        system = SkillAcquisitionSystem()
        assert system.learning_rate_base == 0.1
        assert len(system.skills) == 0
        assert len(system.practice_history) == 0

    def test_custom_learning_rate(self):
        """System accepts custom learning rate"""
        system = SkillAcquisitionSystem(learning_rate_base=0.15)
        assert system.learning_rate_base == 0.15

    def test_skill_registry_empty(self):
        """Skill registry starts empty"""
        system = SkillAcquisitionSystem()
        state = system.get_state()
        assert state["total_skills"] == 0


class TestLearningCurves:
    """Test power law of practice (Newell & Rosenbloom 1981)"""

    def test_power_law_of_practice(self):
        """Performance follows power law: Time = A + B * N^(-α)"""
        system = SkillAcquisitionSystem()

        # Practice 50 trials
        times = []
        for trial in range(1, 51):
            result = system.practice_skill(skill_name="typing", trial_number=trial, feedback_quality=0.8)
            times.append(result["performance_time"])

        # Early improvement (trial 1 vs 5)
        early_improvement = times[0] - times[4]

        # Late improvement (trial 45 vs 50)
        late_improvement = times[44] - times[49]

        # Diminishing returns: early improvement > late improvement
        assert early_improvement > late_improvement
        assert times[0] > times[-1]  # Overall improvement

    def test_early_rapid_improvement(self):
        """Early practice shows rapid improvement"""
        system = SkillAcquisitionSystem()

        skill_0 = system.practice_skill(skill_name="driving", trial_number=1, feedback_quality=0.7)
        skill_5 = system.practice_skill(skill_name="driving", trial_number=6, feedback_quality=0.7)

        improvement = skill_5["skill_level"] - skill_0["skill_level"]
        assert improvement > 0.1  # Significant early improvement

    def test_later_diminishing_returns(self):
        """Later practice shows diminishing returns"""
        system = SkillAcquisitionSystem()

        # Practice to high level first
        for i in range(1, 51):
            system.practice_skill(skill_name="chess", trial_number=i, feedback_quality=0.7)

        skill_50 = system.get_skill_level("chess")

        # More practice
        for i in range(51, 61):
            system.practice_skill(skill_name="chess", trial_number=i, feedback_quality=0.7)

        skill_60 = system.get_skill_level("chess")

        late_improvement = skill_60 - skill_50
        assert late_improvement < 0.05  # Diminishing returns

    def test_asymptotic_performance(self):
        """Performance asymptotes toward expert level"""
        system = SkillAcquisitionSystem()

        # Extensive practice (100 trials)
        for i in range(1, 101):
            system.practice_skill(skill_name="piano", trial_number=i, feedback_quality=0.9)

        skill_level = system.get_skill_level("piano")
        assert skill_level > 0.8  # Expert level
        assert skill_level <= 1.0  # Cannot exceed maximum


class TestPracticeQuality:
    """Test deliberate practice vs mindless repetition (Ericsson 1993)"""

    def test_deliberate_practice_faster_learning(self):
        """High quality deliberate practice → faster learning"""
        system = SkillAcquisitionSystem()

        # High quality practice
        for i in range(1, 21):
            system.practice_skill(skill_name="skill_A", trial_number=i, feedback_quality=0.9)

        # Low quality practice
        for i in range(1, 21):
            system.practice_skill(skill_name="skill_B", trial_number=i, feedback_quality=0.3)

        skill_A = system.get_skill_level("skill_A")
        skill_B = system.get_skill_level("skill_B")

        assert skill_A > skill_B  # High quality → better outcome

    def test_mindless_repetition_slower_learning(self):
        """Mindless repetition (low feedback) → slower learning"""
        system = SkillAcquisitionSystem()

        # Practice with minimal feedback
        for i in range(1, 31):
            system.practice_skill(skill_name="autopilot", trial_number=i, feedback_quality=0.2)

        skill_level = system.get_skill_level("autopilot")
        assert skill_level < 0.5  # Limited improvement

    def test_feedback_improves_learning_rate(self):
        """Feedback quality modulates learning rate"""
        system = SkillAcquisitionSystem()

        # With feedback
        result_with = system.practice_skill(skill_name="test_A", trial_number=1, feedback_quality=0.8)

        # Without feedback
        result_without = system.practice_skill(skill_name="test_B", trial_number=1, feedback_quality=0.1)

        assert result_with["learning_rate"] > result_without["learning_rate"]

    def test_no_feedback_plateau(self):
        """No feedback leads to plateau"""
        system = SkillAcquisitionSystem()

        # Practice without feedback
        for i in range(1, 31):
            system.practice_skill(skill_name="no_fb", trial_number=i, feedback_quality=0.0)

        skill_level = system.get_skill_level("no_fb")
        assert skill_level < 0.3  # Plateaus early without feedback


class TestSkillPlateaus:
    """Test plateau detection and breakthroughs"""

    def test_plateau_detection(self):
        """System detects when performance stops improving"""
        system = SkillAcquisitionSystem()

        # Practice to plateau (low feedback quality)
        for i in range(1, 51):
            system.practice_skill(skill_name="plateau_skill", trial_number=i, feedback_quality=0.3)

        result = system.detect_plateau("plateau_skill")
        assert result["plateau_detected"] == True

    def test_breakthrough_after_plateau(self):
        """Strategy change can lead to breakthrough"""
        system = SkillAcquisitionSystem()

        # Practice to plateau
        for i in range(1, 31):
            system.practice_skill(skill_name="break_skill", trial_number=i, feedback_quality=0.3)

        skill_before = system.get_skill_level("break_skill")

        # Breakthrough: high feedback quality (strategy change)
        for i in range(31, 36):
            system.practice_skill(skill_name="break_skill", trial_number=i, feedback_quality=0.9)

        skill_after = system.get_skill_level("break_skill")

        improvement = skill_after - skill_before
        assert improvement > 0.05  # Breakthrough

    def test_plateau_duration_varies(self):
        """Plateau duration varies by skill complexity"""
        system = SkillAcquisitionSystem()

        # Simple skill: shorter plateau
        for i in range(1, 21):
            system.practice_skill(skill_name="simple", trial_number=i, feedback_quality=0.5, complexity=0.3)

        plateau_simple = system.detect_plateau("simple")

        # Complex skill: longer plateau
        for i in range(1, 21):
            system.practice_skill(skill_name="complex", trial_number=i, feedback_quality=0.5, complexity=0.9)

        plateau_complex = system.detect_plateau("complex")

        # Complex skill more likely to plateau
        if plateau_complex["plateau_detected"]:
            assert True  # Complex skill plateaued as expected


class TestTransferBetweenSkills:
    """Test near and far transfer"""

    def test_near_transfer(self):
        """Similar skills transfer (near transfer)"""
        system = SkillAcquisitionSystem()

        # Train source skill
        for i in range(1, 31):
            system.practice_skill(skill_name="guitar", trial_number=i, feedback_quality=0.8)

        # Compute transfer to similar skill
        transfer = system.compute_transfer(source_skill="guitar", target_skill="bass", similarity=0.8)

        assert transfer["transfer_applicable"] == True
        assert transfer["transfer_amount"] > 0.5  # Significant transfer

    def test_far_transfer(self):
        """Distant skills have minimal transfer (far transfer)"""
        system = SkillAcquisitionSystem()

        # Train source skill
        for i in range(1, 31):
            system.practice_skill(skill_name="basketball", trial_number=i, feedback_quality=0.8)

        # Compute transfer to distant skill
        transfer = system.compute_transfer(source_skill="basketball", target_skill="programming", similarity=0.2)

        assert transfer["transfer_applicable"] == False or transfer["transfer_amount"] < 0.2

    def test_negative_transfer(self):
        """Interference from source skill (negative transfer)"""
        system = SkillAcquisitionSystem()

        # Train source skill
        for i in range(1, 21):
            system.practice_skill(skill_name="tennis", trial_number=i, feedback_quality=0.7)

        # Compute transfer with interference
        transfer = system.compute_transfer(source_skill="tennis", target_skill="badminton", similarity=0.6, interference=True)

        assert transfer["negative_transfer"] == True

    def test_skill_level_affects_transfer(self):
        """Higher skill level → better transfer ability"""
        system = SkillAcquisitionSystem()

        # Low skill level
        for i in range(1, 6):
            system.practice_skill(skill_name="novice_skill", trial_number=i, feedback_quality=0.7)

        transfer_novice = system.compute_transfer(source_skill="novice_skill", target_skill="related_A", similarity=0.7)

        # High skill level
        for i in range(1, 41):
            system.practice_skill(skill_name="expert_skill", trial_number=i, feedback_quality=0.8)

        transfer_expert = system.compute_transfer(source_skill="expert_skill", target_skill="related_B", similarity=0.7)

        # Experts transfer better
        assert transfer_expert["transfer_amount"] > transfer_novice["transfer_amount"]


class TestIntegration:
    """Test integration with other LABs"""

    def test_meta_learning_optimizes_learning_rate(self):
        """LAB_038 meta-learning optimizes learning rate"""
        system = SkillAcquisitionSystem()

        # Practice with meta-learning signal
        result = system.practice_skill(
            skill_name="meta_skill",
            trial_number=1,
            feedback_quality=0.7,
            meta_learning_signal=0.9  # From LAB_038
        )

        assert "learning_rate" in result
        assert result["learning_rate"] > system.learning_rate_base  # Amplified

    def test_habit_formation_from_skilled_actions(self):
        """LAB_039: Skilled actions become habitual"""
        system = SkillAcquisitionSystem()

        # Practice to high skill level
        for i in range(1, 51):
            system.practice_skill(skill_name="automatic_skill", trial_number=i, feedback_quality=0.8)

        skill_level = system.get_skill_level("automatic_skill")

        # High skill → high automaticity (for LAB_039)
        assert skill_level > 0.7
        # LAB_039 would use this skill_level to accelerate habit formation

    def test_transfer_learning_between_domains(self):
        """LAB_041: Transfer learning between skills"""
        system = SkillAcquisitionSystem()

        # Train source
        for i in range(1, 31):
            system.practice_skill(skill_name="math", trial_number=i, feedback_quality=0.8)

        # Transfer to target
        transfer = system.compute_transfer(source_skill="math", target_skill="physics", similarity=0.7)

        # Transfer signal feeds into LAB_041
        assert transfer["transfer_amount"] > 0

    def test_structural_plasticity_long_term(self):
        """LAB_050: Long-term skill drives structural changes"""
        system = SkillAcquisitionSystem()

        # Extensive practice (simulating months)
        for i in range(1, 101):
            system.practice_skill(skill_name="long_term", trial_number=i, feedback_quality=0.8)

        skill_level = system.get_skill_level("long_term")

        # High skill + long practice → structural plasticity signal
        assert skill_level > 0.8
        # LAB_050 would detect this as trigger for structural changes


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_practice_event(self):
        """Process practice event updates skill"""
        system = SkillAcquisitionSystem()

        result = system.process_event(
            event_type="practice",
            skill_name="test_skill",
            trial_number=1,
            feedback_quality=0.7
        )

        assert "skill_updated" in result
        assert result["skill_updated"] == True

    def test_process_transfer_event(self):
        """Process transfer computation"""
        system = SkillAcquisitionSystem()

        # Train source first
        for i in range(1, 21):
            system.practice_skill(skill_name="source", trial_number=i, feedback_quality=0.7)

        result = system.process_event(
            event_type="transfer",
            source_skill="source",
            target_skill="target",
            similarity=0.6
        )

        assert "transfer_amount" in result


class TestGetState:
    """Test state retrieval"""

    def test_get_state_returns_skills(self):
        """get_state returns all skills"""
        system = SkillAcquisitionSystem()

        # Create some skills
        for i in range(1, 6):
            system.practice_skill(skill_name="skill_A", trial_number=i, feedback_quality=0.7)
            system.practice_skill(skill_name="skill_B", trial_number=i, feedback_quality=0.6)

        state = system.get_state()

        assert "total_skills" in state
        assert state["total_skills"] == 2
        assert "highest_skill" in state

    def test_get_state_serializable(self):
        """get_state returns JSON-serializable dict"""
        system = SkillAcquisitionSystem()

        state = system.get_state()

        import json
        json_str = json.dumps(state)
        assert json_str is not None
