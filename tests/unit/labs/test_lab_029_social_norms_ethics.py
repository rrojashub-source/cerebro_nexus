"""
LAB_029: Social Norms & Ethics - Unit Tests

Social Cognition: Moral reasoning, norm detection, fairness

Key Papers:
- Greene et al. (2001) - vmPFC vs dlPFC in moral judgment
- Cushman (2013) - Action-based vs outcome-based morality
- Haidt (2001) - Social intuitionist model
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Social_Homeostasis.LAB_029_Social_Norms_Ethics.social_norms_ethics_system import (
    SocialNormsEthicsSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with default parameters"""
        system = SocialNormsEthicsSystem()
        assert system.emotional_weight == 0.5
        assert system.rational_weight == 0.5
        assert len(system.learned_norms) == 0

    def test_custom_parameters(self):
        """System accepts custom dual-process weights"""
        system = SocialNormsEthicsSystem(
            emotional_weight=0.7,
            rational_weight=0.3
        )
        assert system.emotional_weight == 0.7
        assert system.rational_weight == 0.3


class TestNormLearning:
    """Test norm learning from social feedback"""

    def test_learn_norm_from_approval(self):
        """Learn norm from repeated approval"""
        system = SocialNormsEthicsSystem()

        # Observe action "greeting" receiving approval multiple times
        for _ in range(5):
            system.observe_social_feedback(
                action="greeting",
                approval=True,
                disapproval=False
            )

        # Norm should be learned
        assert "greeting" in system.learned_norms
        assert system.learned_norms["greeting"]["strength"] > 0.5

    def test_learn_norm_from_disapproval(self):
        """Learn norm violation from disapproval"""
        system = SocialNormsEthicsSystem()

        # Observe action "interrupting" receiving disapproval
        for _ in range(5):
            system.observe_social_feedback(
                action="interrupting",
                approval=False,
                disapproval=True
            )

        # Norm against interrupting should be learned
        assert "interrupting" in system.learned_norms
        assert system.learned_norms["interrupting"]["strength"] > 0.5
        assert system.learned_norms["interrupting"]["valence"] == "negative"

    def test_norm_strength_increases_with_consistency(self):
        """Consistent feedback strengthens norms"""
        system = SocialNormsEthicsSystem()

        # First observation
        system.observe_social_feedback("sharing", approval=True, disapproval=False)
        initial_strength = system.learned_norms["sharing"]["strength"]

        # More observations
        for _ in range(4):
            system.observe_social_feedback("sharing", approval=True, disapproval=False)

        final_strength = system.learned_norms["sharing"]["strength"]
        assert final_strength > initial_strength

    def test_detect_norm_violation(self):
        """Detect when action violates learned norm"""
        system = SocialNormsEthicsSystem()

        # Learn norm: "lying" is bad
        for _ in range(5):
            system.observe_social_feedback("lying", approval=False, disapproval=True)

        # Detect violation
        result = system.detect_norm_violation(action="lying")

        assert result["violation_detected"] == True
        assert result["norm_strength"] > 0.5


class TestDualProcessMoralJudgment:
    """Test dual-process moral reasoning (vmPFC vs dlPFC)"""

    def test_trolley_problem_utilitarian_judgment(self):
        """Utilitarian judgment: save 5 by sacrificing 1"""
        system = SocialNormsEthicsSystem(
            emotional_weight=0.2,  # Low emotion
            rational_weight=0.8    # High rationality
        )

        result = system.moral_judgment(
            scenario={
                "type": "trolley",
                "lives_at_risk": 5,
                "action_cost": 1,
                "personal": False  # Impersonal (flip switch)
            }
        )

        # Rational system should approve utilitarian choice
        assert result["judgment"] == "permissible"
        assert result["utilitarian_score"] > 0.7

    def test_footbridge_dilemma_emotional_rejection(self):
        """Personal dilemma: emotion overrides utility"""
        system = SocialNormsEthicsSystem(
            emotional_weight=0.8,  # High emotion
            rational_weight=0.2
        )

        result = system.moral_judgment(
            scenario={
                "type": "footbridge",
                "lives_at_risk": 5,
                "action_cost": 1,
                "personal": True  # Personal (push person)
            }
        )

        # Emotional system should reject personal harm
        assert result["judgment"] == "impermissible"
        assert result["emotional_score"] > 0.6

    def test_personal_vs_impersonal_dilemmas(self):
        """Personal dilemmas engage vmPFC more (emotional)"""
        system = SocialNormsEthicsSystem()

        # Impersonal: flip switch
        impersonal = system.moral_judgment(
            scenario={"type": "trolley", "personal": False, "lives_at_risk": 5, "action_cost": 1}
        )

        # Personal: push person
        personal = system.moral_judgment(
            scenario={"type": "footbridge", "personal": True, "lives_at_risk": 5, "action_cost": 1}
        )

        # Personal should have higher emotional engagement
        assert personal["emotional_engagement"] > impersonal["emotional_engagement"]

    def test_dual_process_conflict(self):
        """Detect conflict between emotional and rational systems"""
        system = SocialNormsEthicsSystem()

        result = system.moral_judgment(
            scenario={
                "type": "footbridge",
                "personal": True,
                "lives_at_risk": 5,
                "action_cost": 1
            }
        )

        # Should detect conflict (utility says yes, emotion says no)
        assert "conflict" in result
        assert result["conflict"] == True


class TestActionVsOutcomeMorality:
    """Test action-based vs outcome-based moral judgment"""

    def test_action_based_judgment(self):
        """Action itself is wrong regardless of outcome (Cushman 2013)"""
        system = SocialNormsEthicsSystem()

        # Intentional harm with good outcome
        result = system.action_vs_outcome_judgment(
            action="lying",
            outcome="positive",  # Lie saved someone
            intention="deceptive"
        )

        # Action-based: lying is wrong even if outcome good
        assert result["action_judgment"] == "wrong"
        assert result["primary_basis"] == "action"

    def test_outcome_based_judgment(self):
        """Outcome determines morality"""
        system = SocialNormsEthicsSystem()

        # Accidental harm
        result = system.action_vs_outcome_judgment(
            action="helping",
            outcome="negative",  # Help caused harm accidentally
            intention="helpful"
        )

        # Should consider outcome (harm occurred)
        assert result["outcome_judgment"] == "bad"

    def test_intention_matters_for_action_judgment(self):
        """Intentions affect action-based judgment (LAB_027 integration)"""
        system = SocialNormsEthicsSystem()

        # Same action, different intentions
        intentional = system.action_vs_outcome_judgment(
            action="harm",
            outcome="negative",
            intention="malicious"
        )

        accidental = system.action_vs_outcome_judgment(
            action="harm",
            outcome="negative",
            intention="accidental"
        )

        # Intentional harm judged more harshly
        assert intentional["severity"] > accidental["severity"]


class TestFairnessComputation:
    """Test fairness principles"""

    def test_equality_fairness(self):
        """Equality principle: everyone gets same amount"""
        system = SocialNormsEthicsSystem()

        distribution = {"person_a": 50, "person_b": 50, "person_c": 50}
        result = system.compute_fairness(distribution, principle="equality")

        assert result["fairness_score"] > 0.9
        assert result["principle_applied"] == "equality"

    def test_inequality_detected(self):
        """Detect unfair distribution"""
        system = SocialNormsEthicsSystem()

        distribution = {"person_a": 80, "person_b": 10, "person_c": 10}
        result = system.compute_fairness(distribution, principle="equality")

        assert result["fairness_score"] < 0.5
        assert result["inequality_detected"] == True

    def test_merit_based_fairness(self):
        """Merit-based: distribution proportional to contribution"""
        system = SocialNormsEthicsSystem()

        distribution = {"person_a": 60, "person_b": 30, "person_c": 10}
        contributions = {"person_a": 60, "person_b": 30, "person_c": 10}

        result = system.compute_fairness(
            distribution,
            principle="merit",
            context={"contributions": contributions}
        )

        # Distribution matches contributions = fair
        assert result["fairness_score"] > 0.9

    def test_need_based_fairness(self):
        """Need-based: those with greater need receive more"""
        system = SocialNormsEthicsSystem()

        distribution = {"person_a": 20, "person_b": 30, "person_c": 50}
        needs = {"person_a": 20, "person_b": 30, "person_c": 50}

        result = system.compute_fairness(
            distribution,
            principle="need",
            context={"needs": needs}
        )

        # Distribution matches needs = fair
        assert result["fairness_score"] > 0.9


class TestEmpathyIntegration:
    """Test integration with LAB_028 (Empathy)"""

    def test_empathy_increases_care_ethics_weight(self):
        """High empathy → deontological bias (care ethics)"""
        system = SocialNormsEthicsSystem()

        # High empathy scenario
        empathy_high = system.care_ethics_weight(
            empathy_level=0.9,
            relationship="close"
        )

        # Low empathy scenario
        empathy_low = system.care_ethics_weight(
            empathy_level=0.1,
            relationship="stranger"
        )

        # High empathy should increase deontological weight
        assert empathy_high > empathy_low
        assert empathy_high > 0.7

    def test_relationship_modulates_moral_judgment(self):
        """Closer relationship → more deontological (LAB_028)"""
        system = SocialNormsEthicsSystem()

        # Same dilemma, different relationships
        close_friend = system.moral_judgment(
            scenario={
                "type": "harm_dilemma",
                "personal": True,
                "lives_at_risk": 5,
                "action_cost": 1
            },
            context={"relationship": "close", "empathy_level": 0.8}
        )

        stranger = system.moral_judgment(
            scenario={
                "type": "harm_dilemma",
                "personal": True,
                "lives_at_risk": 5,
                "action_cost": 1
            },
            context={"relationship": "stranger", "empathy_level": 0.2}
        )

        # Close relationship should reduce willingness to harm
        assert close_friend["judgment"] == "impermissible"
        assert close_friend["emotional_score"] > stranger["emotional_score"]


class TestPerspectiveIntegration:
    """Test integration with LAB_030 (Perspective Taking)"""

    def test_fairness_from_multiple_perspectives(self):
        """Evaluate fairness from different viewpoints (LAB_030)"""
        system = SocialNormsEthicsSystem()

        distribution = {"person_a": 70, "person_b": 20, "person_c": 10}

        # From person_a's perspective (beneficiary)
        perspective_a = system.evaluate_fairness_from_perspective(
            distribution,
            perspective_holder="person_a"
        )

        # From person_c's perspective (disadvantaged)
        perspective_c = system.evaluate_fairness_from_perspective(
            distribution,
            perspective_holder="person_c"
        )

        # person_c should perceive lower fairness
        assert perspective_c["perceived_fairness"] < perspective_a["perceived_fairness"]


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_moral_dilemma(self):
        """Process complete moral dilemma"""
        system = SocialNormsEthicsSystem()

        result = system.process_event(
            event_type="moral_dilemma",
            scenario={
                "type": "trolley",
                "personal": False,
                "lives_at_risk": 5,
                "action_cost": 1
            }
        )

        assert "judgment" in result
        assert "utilitarian_score" in result
        assert "emotional_score" in result

    def test_process_norm_observation(self):
        """Process social norm observation"""
        system = SocialNormsEthicsSystem()

        result = system.process_event(
            event_type="norm_observation",
            action="helping_elderly",
            approval=True,
            disapproval=False
        )

        assert "norm_updated" in result
        assert result["action"] == "helping_elderly"

    def test_process_fairness_evaluation(self):
        """Process fairness evaluation"""
        system = SocialNormsEthicsSystem()

        result = system.process_event(
            event_type="fairness_evaluation",
            distribution={"a": 50, "b": 50},
            principle="equality"
        )

        assert "fairness_score" in result
        assert result["principle_applied"] == "equality"


class TestGetState:
    """Test state retrieval"""

    def test_get_state_returns_learned_norms(self):
        """get_state returns learned norms"""
        system = SocialNormsEthicsSystem()

        # Learn some norms
        system.observe_social_feedback("sharing", approval=True, disapproval=False)
        system.observe_social_feedback("lying", approval=False, disapproval=True)

        state = system.get_state()

        assert "learned_norms" in state
        assert len(state["learned_norms"]) == 2
        assert "sharing" in state["learned_norms"]

    def test_get_state_serializable(self):
        """get_state returns JSON-serializable dict"""
        system = SocialNormsEthicsSystem()

        state = system.get_state()

        # Should be JSON serializable
        import json
        json_str = json.dumps(state)
        assert json_str is not None
