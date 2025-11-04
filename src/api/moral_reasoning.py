"""
LAB_027: Moral Reasoning - Ethical Judgments and Dilemma Resolution

Implements moral reasoning and ethical decision-making:
- Kohlberg (1981): Stages of moral development
- Greene et al. (2001): Dual-process theory of moral judgment
- Haidt (2001): Social intuitionist model of moral judgment
- Cushman (2013): Action vs outcome in moral judgment

Core Functions:
1. Moral judgment (harm, fairness, loyalty, authority, purity)
2. Trolley problem and dilemma resolution
3. Deontological vs consequentialist reasoning
4. Norm violation detection
5. Moral development stages
6. Utilitarian calculation

Neuroscience Foundation:
- vmPFC: Personal moral dilemmas, emotional moral responses
- dlPFC: Utilitarian reasoning, cognitive control
- TPJ: Moral evaluation of intentions
- Amygdala: Moral disgust, harm aversion

Integration:
- ← LAB_013 (Dopamine) for norm compliance rewards
- ← LAB_014 (Serotonin) for moral patience
- ← LAB_023 (Theory of Mind) for intention evaluation
- ← LAB_024 (Empathy) for victim perspective
- ← LAB_026 (Cooperation) for fairness norms
"""

import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import numpy as np


class MoralFoundation(Enum):
    """Moral Foundations Theory (Haidt)"""
    CARE_HARM = "care_harm"
    FAIRNESS_CHEATING = "fairness_cheating"
    LOYALTY_BETRAYAL = "loyalty_betrayal"
    AUTHORITY_SUBVERSION = "authority_subversion"
    SANCTITY_DEGRADATION = "sanctity_degradation"


class MoralStage(Enum):
    """Kohlberg's Stages of Moral Development"""
    PRECONVENTIONAL_PUNISHMENT = 1  # Avoid punishment
    PRECONVENTIONAL_REWARD = 2      # Seek reward
    CONVENTIONAL_APPROVAL = 3       # Seek approval
    CONVENTIONAL_LAW = 4            # Maintain social order
    POSTCONVENTIONAL_RIGHTS = 5     # Universal rights
    POSTCONVENTIONAL_PRINCIPLES = 6 # Universal ethical principles


class ReasoningMode(Enum):
    """Moral reasoning modes"""
    DEONTOLOGICAL = "deontological"  # Rule-based (Kant)
    CONSEQUENTIALIST = "consequentialist"  # Outcome-based (Mill)
    VIRTUE_ETHICS = "virtue_ethics"  # Character-based (Aristotle)
    CARE_ETHICS = "care_ethics"  # Relationship-based (Gilligan)


@dataclass
class MoralDilemma:
    """Moral dilemma scenario"""
    dilemma_id: str
    description: str
    action_options: List[str]
    is_personal: bool  # Personal vs impersonal (Greene)
    harm_involved: bool
    agent_causation: bool  # Agent causes harm vs allows harm
    victims_count: int
    saved_count: int


@dataclass
class MoralJudgment:
    """Moral judgment result"""
    timestamp: float
    dilemma_id: str
    chosen_action: str
    reasoning_mode: ReasoningMode
    moral_stage: MoralStage
    permissibility_score: float  # 0-1
    emotional_aversion: float  # 0-1
    utilitarian_value: float
    deontological_violation: bool
    confidence: float


@dataclass
class NormViolation:
    """Detected norm violation"""
    timestamp: float
    violation_type: str
    foundation_violated: MoralFoundation
    severity: float  # 0-1
    perpetrator: Optional[str]
    victim: Optional[str]
    context: str


class MoralFoundationsEvaluator:
    """Evaluates actions against moral foundations"""

    def __init__(self):
        # Foundation sensitivities (can be personalized)
        self.sensitivities = {
            MoralFoundation.CARE_HARM: 0.9,
            MoralFoundation.FAIRNESS_CHEATING: 0.8,
            MoralFoundation.LOYALTY_BETRAYAL: 0.6,
            MoralFoundation.AUTHORITY_SUBVERSION: 0.5,
            MoralFoundation.SANCTITY_DEGRADATION: 0.4,
        }

    def evaluate_action(
        self,
        action: str,
        context: Dict
    ) -> Dict[MoralFoundation, float]:
        """
        Evaluate action against moral foundations.

        Returns foundation violation scores (0-1).
        """
        violations = {}

        # Care/Harm
        if "harm" in action.lower() or "hurt" in action.lower() or "kill" in action.lower():
            violations[MoralFoundation.CARE_HARM] = 0.9 * self.sensitivities[MoralFoundation.CARE_HARM]
        else:
            violations[MoralFoundation.CARE_HARM] = 0.0

        # Fairness/Cheating
        if "cheat" in action.lower() or "unfair" in action.lower() or "steal" in action.lower():
            violations[MoralFoundation.FAIRNESS_CHEATING] = 0.8 * self.sensitivities[MoralFoundation.FAIRNESS_CHEATING]
        else:
            violations[MoralFoundation.FAIRNESS_CHEATING] = 0.0

        # Loyalty/Betrayal
        if "betray" in action.lower() or "disloyal" in action.lower():
            violations[MoralFoundation.LOYALTY_BETRAYAL] = 0.7 * self.sensitivities[MoralFoundation.LOYALTY_BETRAYAL]
        else:
            violations[MoralFoundation.LOYALTY_BETRAYAL] = 0.0

        # Authority/Subversion
        if "disobey" in action.lower() or "rebel" in action.lower():
            violations[MoralFoundation.AUTHORITY_SUBVERSION] = 0.6 * self.sensitivities[MoralFoundation.AUTHORITY_SUBVERSION]
        else:
            violations[MoralFoundation.AUTHORITY_SUBVERSION] = 0.0

        # Sanctity/Degradation
        if "desecrate" in action.lower() or "defile" in action.lower():
            violations[MoralFoundation.SANCTITY_DEGRADATION] = 0.7 * self.sensitivities[MoralFoundation.SANCTITY_DEGRADATION]
        else:
            violations[MoralFoundation.SANCTITY_DEGRADATION] = 0.0

        return violations

    def get_overall_violation(self, violations: Dict[MoralFoundation, float]) -> float:
        """Compute overall violation severity"""
        if not violations:
            return 0.0
        return max(violations.values())


class UtilitarianCalculator:
    """Performs utilitarian (consequentialist) calculations"""

    def __init__(self):
        pass

    def compute_utility(
        self,
        action: str,
        outcomes: Dict[str, float]
    ) -> float:
        """
        Compute expected utility of action.

        outcomes: {"lives_saved": 5, "lives_lost": 1, "suffering": -2}

        Returns net utility.
        """
        # Weights for different outcomes
        weights = {
            "lives_saved": 10.0,
            "lives_lost": -10.0,
            "suffering": -3.0,
            "happiness": 5.0,
            "fairness": 4.0,
            "autonomy": 3.0,
        }

        utility = 0.0
        for outcome, value in outcomes.items():
            weight = weights.get(outcome, 1.0)
            utility += weight * value

        return utility

    def compare_actions(
        self,
        action_outcomes: Dict[str, Dict[str, float]]
    ) -> str:
        """
        Compare actions and select best by utility.

        Returns action with highest utility.
        """
        utilities = {}
        for action, outcomes in action_outcomes.items():
            utilities[action] = self.compute_utility(action, outcomes)

        best_action = max(utilities, key=utilities.get)
        return best_action


class DeontologicalEvaluator:
    """Evaluates actions against deontological rules"""

    def __init__(self):
        # Deontological rules (Kantian)
        self.rules = {
            "do_not_kill": {"weight": 1.0, "absolute": True},
            "do_not_lie": {"weight": 0.7, "absolute": False},
            "do_not_steal": {"weight": 0.8, "absolute": False},
            "respect_autonomy": {"weight": 0.9, "absolute": True},
            "keep_promises": {"weight": 0.6, "absolute": False},
        }

    def evaluate_action(
        self,
        action: str,
        context: Dict
    ) -> Tuple[bool, List[str]]:
        """
        Evaluate if action violates deontological rules.

        Returns (violation_occurred, violated_rules).
        """
        violated_rules = []

        # Check each rule
        if "kill" in action.lower():
            violated_rules.append("do_not_kill")

        if "lie" in action.lower() or "deceive" in action.lower():
            violated_rules.append("do_not_lie")

        if "steal" in action.lower():
            violated_rules.append("do_not_steal")

        if "force" in action.lower() or "coerce" in action.lower():
            violated_rules.append("respect_autonomy")

        if "break promise" in action.lower():
            violated_rules.append("keep_promises")

        # Check if any absolute rule violated
        violation_occurred = any(
            rule in violated_rules and self.rules[rule]["absolute"]
            for rule in violated_rules
        )

        return violation_occurred, violated_rules

    def is_permissible(self, action: str, context: Dict) -> bool:
        """Determine if action is morally permissible"""
        violation, _ = self.evaluate_action(action, context)
        return not violation


class MoralDilemmaResolver:
    """Resolves moral dilemmas using dual-process model"""

    def __init__(self, default_mode: ReasoningMode = ReasoningMode.CONSEQUENTIALIST):
        self.default_mode = default_mode
        self.utilitarian_calc = UtilitarianCalculator()
        self.deontological_eval = DeontologicalEvaluator()

    def resolve_dilemma(
        self,
        dilemma: MoralDilemma,
        reasoning_mode: Optional[ReasoningMode] = None
    ) -> MoralJudgment:
        """
        Resolve moral dilemma.

        Greene's dual-process model:
        - Personal dilemmas trigger emotional (deontological) response
        - Impersonal dilemmas allow utilitarian reasoning

        Returns judgment.
        """
        if reasoning_mode is None:
            # Personal dilemmas bias toward deontological
            if dilemma.is_personal:
                reasoning_mode = ReasoningMode.DEONTOLOGICAL
            else:
                reasoning_mode = ReasoningMode.CONSEQUENTIALIST

        # Utilitarian analysis
        utilitarian_value = self._compute_utilitarian_value(dilemma)

        # Deontological analysis
        deontological_violation = self._check_deontological_violation(dilemma)

        # Emotional aversion (higher for personal, agent-caused harm)
        emotional_aversion = 0.0
        if dilemma.is_personal:
            emotional_aversion += 0.5
        if dilemma.agent_causation:
            emotional_aversion += 0.3
        if dilemma.harm_involved:
            emotional_aversion += 0.2
        emotional_aversion = min(1.0, emotional_aversion)

        # Select action based on reasoning mode
        if reasoning_mode == ReasoningMode.CONSEQUENTIALIST:
            # Maximize lives saved
            if dilemma.saved_count > dilemma.victims_count:
                chosen_action = dilemma.action_options[0]  # Act
                permissibility = 0.8
            else:
                chosen_action = dilemma.action_options[1] if len(dilemma.action_options) > 1 else dilemma.action_options[0]
                permissibility = 0.3

        elif reasoning_mode == ReasoningMode.DEONTOLOGICAL:
            # Don't violate rules
            if deontological_violation:
                chosen_action = dilemma.action_options[1] if len(dilemma.action_options) > 1 else dilemma.action_options[0]
                permissibility = 0.2
            else:
                chosen_action = dilemma.action_options[0]
                permissibility = 0.7

        else:
            # Default: avoid action if emotional aversion high
            if emotional_aversion > 0.6:
                chosen_action = dilemma.action_options[1] if len(dilemma.action_options) > 1 else dilemma.action_options[0]
                permissibility = 0.4
            else:
                chosen_action = dilemma.action_options[0]
                permissibility = 0.6

        # Confidence (lower for conflicting signals)
        conflict = abs(utilitarian_value - (1.0 if not deontological_violation else 0.0))
        confidence = 1.0 - (conflict * 0.5)

        judgment = MoralJudgment(
            timestamp=time.time(),
            dilemma_id=dilemma.dilemma_id,
            chosen_action=chosen_action,
            reasoning_mode=reasoning_mode,
            moral_stage=MoralStage.POSTCONVENTIONAL_PRINCIPLES,
            permissibility_score=permissibility,
            emotional_aversion=emotional_aversion,
            utilitarian_value=utilitarian_value,
            deontological_violation=deontological_violation,
            confidence=confidence
        )

        return judgment

    def _compute_utilitarian_value(self, dilemma: MoralDilemma) -> float:
        """Compute utilitarian value (lives saved - lives lost)"""
        net_lives = dilemma.saved_count - dilemma.victims_count
        # Normalize to 0-1
        max_possible = max(dilemma.saved_count, dilemma.victims_count, 1)
        return (net_lives + max_possible) / (2 * max_possible)

    def _check_deontological_violation(self, dilemma: MoralDilemma) -> bool:
        """Check if action violates deontological rules"""
        # Agent-caused harm is violation
        if dilemma.agent_causation and dilemma.harm_involved:
            return True
        return False


class MoralReasoningSystem:
    """
    Main LAB_027 implementation.

    Manages:
    - Moral foundations evaluation
    - Utilitarian calculation
    - Deontological reasoning
    - Dilemma resolution
    """

    def __init__(self, default_mode: ReasoningMode = ReasoningMode.CONSEQUENTIALIST):
        # Components
        self.foundations_evaluator = MoralFoundationsEvaluator()
        self.utilitarian_calc = UtilitarianCalculator()
        self.deontological_eval = DeontologicalEvaluator()
        self.dilemma_resolver = MoralDilemmaResolver(default_mode)

        # History
        self.judgments_history: List[MoralJudgment] = []
        self.violations_detected: List[NormViolation] = []

        # Moral development stage
        self.current_stage = MoralStage.POSTCONVENTIONAL_PRINCIPLES

    def evaluate_action(
        self,
        action: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Evaluate action morally.

        Returns comprehensive moral evaluation.
        """
        if context is None:
            context = {}

        # Moral foundations
        foundation_violations = self.foundations_evaluator.evaluate_action(action, context)
        overall_violation = self.foundations_evaluator.get_overall_violation(foundation_violations)

        # Deontological
        deont_violation, violated_rules = self.deontological_eval.evaluate_action(action, context)

        # Detect norm violation
        if overall_violation > 0.5:
            most_violated = max(foundation_violations, key=foundation_violations.get)
            violation = NormViolation(
                timestamp=time.time(),
                violation_type=action,
                foundation_violated=most_violated,
                severity=overall_violation,
                perpetrator=context.get("agent"),
                victim=context.get("victim"),
                context=str(context)
            )
            self.violations_detected.append(violation)

        return {
            "action": action,
            "foundation_violations": {f.value: v for f, v in foundation_violations.items()},
            "overall_violation": overall_violation,
            "deontological_violation": deont_violation,
            "violated_rules": violated_rules,
            "permissible": not deont_violation and overall_violation < 0.5,
        }

    def resolve_dilemma(
        self,
        dilemma: MoralDilemma,
        reasoning_mode: Optional[ReasoningMode] = None
    ) -> MoralJudgment:
        """
        Resolve moral dilemma.

        Returns judgment.
        """
        judgment = self.dilemma_resolver.resolve_dilemma(dilemma, reasoning_mode)
        self.judgments_history.append(judgment)
        return judgment

    def compare_actions_utilitarian(
        self,
        action_outcomes: Dict[str, Dict[str, float]]
    ) -> Tuple[str, Dict[str, float]]:
        """
        Compare actions by utilitarian calculation.

        Returns (best_action, utilities).
        """
        utilities = {}
        for action, outcomes in action_outcomes.items():
            utilities[action] = self.utilitarian_calc.compute_utility(action, outcomes)

        best_action = max(utilities, key=utilities.get)

        return best_action, utilities

    def detect_norm_violation(
        self,
        observed_action: str,
        context: Dict
    ) -> Optional[NormViolation]:
        """
        Detect if action violates moral norms.

        Returns violation if detected.
        """
        evaluation = self.evaluate_action(observed_action, context)

        if not evaluation["permissible"]:
            foundation_violations = {
                MoralFoundation(k): v
                for k, v in evaluation["foundation_violations"].items()
            }
            most_violated = max(foundation_violations, key=foundation_violations.get)

            violation = NormViolation(
                timestamp=time.time(),
                violation_type=observed_action,
                foundation_violated=most_violated,
                severity=evaluation["overall_violation"],
                perpetrator=context.get("agent"),
                victim=context.get("victim"),
                context=str(context)
            )

            self.violations_detected.append(violation)
            return violation

        return None

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        return {
            "total_judgments": len(self.judgments_history),
            "violations_detected": len(self.violations_detected),
            "current_moral_stage": self.current_stage.value,
            "avg_confidence": (np.mean([j.confidence for j in self.judgments_history])
                             if self.judgments_history else 0.0),
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_027: Moral Reasoning - Test")
    print("=" * 60)

    system = MoralReasoningSystem()

    # Scenario 1: Classic trolley problem (impersonal)
    print("\n🚂 Scenario 1: Classic Trolley Problem (Impersonal)...")
    trolley_switch = MoralDilemma(
        dilemma_id="trolley_switch",
        description="Trolley will kill 5 people. You can pull lever to divert it, killing 1.",
        action_options=["Pull lever (kill 1, save 5)", "Do nothing (kill 5)"],
        is_personal=False,
        harm_involved=True,
        agent_causation=True,
        victims_count=1,
        saved_count=5
    )

    judgment = system.resolve_dilemma(trolley_switch, reasoning_mode=ReasoningMode.CONSEQUENTIALIST)
    print(f"  Chosen action: {judgment.chosen_action}")
    print(f"  Reasoning mode: {judgment.reasoning_mode.value}")
    print(f"  Permissibility: {judgment.permissibility_score:.3f}")
    print(f"  Utilitarian value: {judgment.utilitarian_value:.3f}")
    print(f"  Emotional aversion: {judgment.emotional_aversion:.3f}")
    print(f"  Confidence: {judgment.confidence:.3f}")

    # Scenario 2: Footbridge trolley (personal)
    print("\n👤 Scenario 2: Footbridge Trolley Problem (Personal)...")
    trolley_footbridge = MoralDilemma(
        dilemma_id="trolley_footbridge",
        description="Trolley will kill 5. You can push large person off bridge to stop it.",
        action_options=["Push person (kill 1, save 5)", "Do nothing (kill 5)"],
        is_personal=True,  # Direct physical contact
        harm_involved=True,
        agent_causation=True,
        victims_count=1,
        saved_count=5
    )

    # Try with different reasoning modes
    judgment_deont = system.resolve_dilemma(trolley_footbridge, reasoning_mode=ReasoningMode.DEONTOLOGICAL)
    print(f"  Deontological judgment: {judgment_deont.chosen_action}")
    print(f"  Permissibility: {judgment_deont.permissibility_score:.3f}")
    print(f"  Emotional aversion: {judgment_deont.emotional_aversion:.3f} (high for personal)")

    judgment_cons = system.resolve_dilemma(trolley_footbridge, reasoning_mode=ReasoningMode.CONSEQUENTIALIST)
    print(f"  Consequentialist judgment: {judgment_cons.chosen_action}")
    print(f"  Permissibility: {judgment_cons.permissibility_score:.3f}")

    # Scenario 3: Action evaluation (moral foundations)
    print("\n⚖️ Scenario 3: Evaluating actions against moral foundations...")
    actions = [
        ("Help stranger in need", {}),
        ("Steal to feed family", {"victim": "store"}),
        ("Harm innocent person", {"victim": "person"}),
    ]

    for action, context in actions:
        evaluation = system.evaluate_action(action, context)
        print(f"  Action: '{action}'")
        print(f"    Permissible: {evaluation['permissible']}")
        print(f"    Overall violation: {evaluation['overall_violation']:.3f}")
        print(f"    Top violations: {list(evaluation['foundation_violations'].items())[:2]}")

    # Scenario 4: Utilitarian comparison
    print("\n💰 Scenario 4: Utilitarian action comparison...")
    action_outcomes = {
        "Save 1 child from drowning": {
            "lives_saved": 1,
            "suffering": 0,
            "happiness": 2,
        },
        "Donate $1000 to save 10 lives": {
            "lives_saved": 10,
            "suffering": -1,  # Temporary financial strain
            "happiness": 5,
        },
        "Do nothing": {
            "lives_saved": 0,
            "suffering": 0,
            "happiness": 0,
        },
    }

    best_action, utilities = system.compare_actions_utilitarian(action_outcomes)
    print(f"  Best action (utilitarian): {best_action}")
    print(f"  Utilities:")
    for action, utility in utilities.items():
        print(f"    {action}: {utility:.1f}")

    # Scenario 5: Norm violation detection
    print("\n🚨 Scenario 5: Detecting norm violations...")
    observed_actions = [
        ("Agent betrays trusted friend", {"agent": "bob", "victim": "alice"}),
        ("Agent helps elderly person", {"agent": "charlie"}),
    ]

    for action, context in observed_actions:
        violation = system.detect_norm_violation(action, context)
        if violation:
            print(f"  VIOLATION: '{action}'")
            print(f"    Foundation: {violation.foundation_violated.value}")
            print(f"    Severity: {violation.severity:.3f}")
        else:
            print(f"  OK: '{action}' (no violation)")

    # Final statistics
    print("\n📈 Final Statistics:")
    stats = system.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

    print("\n✅ LAB_027 Test Complete!")
