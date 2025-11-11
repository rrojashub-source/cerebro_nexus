"""
LAB_029: Social Norms & Ethics System

Function: Moral reasoning, norm detection, fairness computation
Neuroscience Basis: vmPFC (emotional/deontological), dlPFC (rational/utilitarian)

Key Papers:
- Greene et al. (2001) - Dual-process theory of moral judgment
- Cushman (2013) - Action-based vs outcome-based morality
- Haidt (2001) - Social intuitionist model of moral judgment

Dual-Process Architecture:
- System 1 (vmPFC): Fast, emotional, deontological
- System 2 (dlPFC): Slow, rational, utilitarian
"""

from typing import Dict, List, Optional, Any


class SocialNormsEthicsSystem:
    """
    LAB_029: Social Norms & Ethics System

    Models moral reasoning through:
    - Norm learning from social feedback (approval/disapproval)
    - Dual-process moral judgment (vmPFC vs dlPFC)
    - Action-based vs outcome-based morality
    - Fairness computation (equality, merit, need)
    - Integration with LAB_027 (intentions), LAB_028 (empathy), LAB_030 (perspective)

    Parameters:
    -----------
    emotional_weight : float
        Weight for emotional/deontological processing (default: 0.5)
    rational_weight : float
        Weight for rational/utilitarian processing (default: 0.5)
    """

    def __init__(
        self,
        emotional_weight: float = 0.5,
        rational_weight: float = 0.5
    ):
        # Dual-process weights
        self.emotional_weight = emotional_weight
        self.rational_weight = rational_weight

        # Learned norms
        self.learned_norms: Dict[str, Dict] = {}

        # Statistics
        self.total_moral_judgments: int = 0
        self.total_norm_observations: int = 0

    def observe_social_feedback(
        self,
        action: str,
        approval: bool,
        disapproval: bool
    ) -> Dict:
        """
        Learn norms from social feedback

        Based on Haidt (2001) social intuitionist model: we learn
        norms from observing approval/disapproval patterns.

        Parameters:
        -----------
        action : str
            Action being evaluated
        approval : bool
            Did observers approve?
        disapproval : bool
            Did observers disapprove?

        Returns:
        --------
        result : Dict
            Updated norm representation
        """
        # Initialize norm if new
        if action not in self.learned_norms:
            self.learned_norms[action] = {
                "strength": 0.0,
                "valence": "neutral",
                "observations": 0
            }

        # Update based on feedback
        norm = self.learned_norms[action]
        norm["observations"] += 1

        # Strengthen norm based on feedback
        learning_rate = 0.2

        if approval:
            norm["strength"] = min(1.0, norm["strength"] + learning_rate)
            norm["valence"] = "positive"
        elif disapproval:
            norm["strength"] = min(1.0, norm["strength"] + learning_rate)
            norm["valence"] = "negative"

        self.total_norm_observations += 1

        return {
            "action": action,
            "norm_strength": norm["strength"],
            "norm_valence": norm["valence"],
            "observations": norm["observations"]
        }

    def detect_norm_violation(self, action: str) -> Dict:
        """
        Detect if action violates learned norm

        Parameters:
        -----------
        action : str
            Action to evaluate

        Returns:
        --------
        result : Dict
            Violation detection result
        """
        if action not in self.learned_norms:
            return {
                "violation_detected": False,
                "norm_strength": 0.0,
                "reason": "no_learned_norm"
            }

        norm = self.learned_norms[action]

        # Violation = strong negative norm
        violation_detected = (
            norm["valence"] == "negative" and
            norm["strength"] > 0.5
        )

        return {
            "violation_detected": violation_detected,
            "norm_strength": norm["strength"],
            "norm_valence": norm["valence"]
        }

    def moral_judgment(
        self,
        scenario: Dict,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Dual-process moral judgment

        Based on Greene et al. (2001): Personal dilemmas engage vmPFC
        (emotional), impersonal dilemmas engage dlPFC (rational).

        System 1 (vmPFC): Emotional, deontological
        System 2 (dlPFC): Rational, utilitarian

        Parameters:
        -----------
        scenario : Dict
            Moral dilemma with keys:
            - type: str (trolley, footbridge, etc.)
            - personal: bool (requires direct physical harm?)
            - lives_at_risk: int
            - action_cost: int (lives lost if action taken)
        context : Dict, optional
            Additional context (relationship, empathy_level)

        Returns:
        --------
        result : Dict
            Moral judgment with emotional and rational scores
        """
        context = context or {}

        # Extract scenario parameters
        personal = scenario.get("personal", False)
        lives_at_risk = scenario.get("lives_at_risk", 0)
        action_cost = scenario.get("action_cost", 0)

        # System 1: Emotional judgment (vmPFC)
        # emotional_score = strength of emotional AVERSION (0-1, where 1 = strong rejection)
        # Personal harm triggers strong emotional aversion
        if personal:
            emotional_engagement = 0.9
            emotional_aversion = 0.8  # Strong aversion to personal harm
        else:
            emotional_engagement = 0.3
            emotional_aversion = 0.3  # Less emotional aversion

        # Empathy modulation (LAB_028 integration)
        empathy_level = context.get("empathy_level", 0.5)
        relationship = context.get("relationship", "stranger")

        # High empathy INCREASES aversion to harm
        # For personal dilemmas: high empathy amplifies aversion
        if personal:
            # Close relationship or high empathy increases aversion
            if relationship == "close":
                emotional_aversion = min(1.0, emotional_aversion * 1.3)
                emotional_engagement = min(1.0, emotional_engagement * 1.5)

            # High empathy increases aversion
            emotional_aversion = min(1.0, emotional_aversion * (1.0 + empathy_level * 0.5))
        else:
            # Impersonal dilemmas less affected by empathy
            emotional_aversion = min(1.0, emotional_aversion * (1.0 + empathy_level * 0.2))

        # emotional_score = aversion strength (for reporting)
        # For judgment calculation, we need to convert aversion to permissibility
        emotional_score = emotional_aversion
        emotional_permissibility = 1.0 - emotional_aversion

        # System 2: Rational judgment (dlPFC)
        # Utilitarian calculation: lives saved vs lives lost
        if action_cost > 0:
            utility_ratio = lives_at_risk / action_cost
            utilitarian_score = min(1.0, utility_ratio / 5.0)
        else:
            utilitarian_score = 1.0  # No cost = always rational to act

        # Combined judgment (weighted)
        emotional_weight_adjusted = self.emotional_weight
        rational_weight_adjusted = self.rational_weight

        # Personal dilemmas increase emotional weight
        if personal:
            emotional_weight_adjusted *= 1.5
            rational_weight_adjusted *= 0.7

        # Normalize weights
        total_weight = emotional_weight_adjusted + rational_weight_adjusted
        emotional_weight_norm = emotional_weight_adjusted / total_weight
        rational_weight_norm = rational_weight_adjusted / total_weight

        # Final judgment (use emotional_permissibility, not emotional_score)
        combined_score = (
            emotional_permissibility * emotional_weight_norm +
            utilitarian_score * rational_weight_norm
        )

        # Threshold for permissibility
        judgment = "permissible" if combined_score > 0.5 else "impermissible"

        # Detect conflict between systems (compare aversion vs utility)
        conflict = abs(emotional_aversion - (1.0 - utilitarian_score)) > 0.4

        self.total_moral_judgments += 1

        return {
            "judgment": judgment,
            "emotional_score": float(emotional_score),
            "utilitarian_score": float(utilitarian_score),
            "combined_score": float(combined_score),
            "emotional_engagement": float(emotional_engagement),
            "conflict": conflict
        }

    def action_vs_outcome_judgment(
        self,
        action: str,
        outcome: str,
        intention: str
    ) -> Dict:
        """
        Action-based vs outcome-based moral judgment

        Based on Cushman (2013): Action-based judgments focus on
        the action itself, outcome-based on consequences.

        Intentions matter for action-based judgments (LAB_027 integration).

        Parameters:
        -----------
        action : str
            Action performed
        outcome : str
            Outcome: "positive" or "negative"
        intention : str
            Intention: "helpful", "harmful", "malicious", "accidental", "deceptive"

        Returns:
        --------
        result : Dict
            Moral judgment with action and outcome evaluations
        """
        # Action-based judgment
        # Certain actions are inherently wrong regardless of outcome
        intrinsically_wrong_actions = ["lying", "harm", "stealing", "betrayal"]

        if action in intrinsically_wrong_actions:
            action_judgment = "wrong"
        else:
            action_judgment = "neutral"

        # Outcome-based judgment
        outcome_judgment = "good" if outcome == "positive" else "bad"

        # Intention modulates action judgment (LAB_027)
        intention_maliciousness = {
            "malicious": 1.0,
            "deceptive": 0.8,
            "harmful": 0.7,
            "accidental": 0.2,
            "helpful": 0.0
        }

        maliciousness = intention_maliciousness.get(intention, 0.5)

        # Calculate severity (more nuanced to differentiate intention levels)
        severity = 0.0

        # Base severity from action
        if action_judgment == "wrong":
            severity += 0.4
        else:
            severity += 0.1

        # Outcome contribution
        if outcome_judgment == "bad":
            severity += 0.2

        # Intention is the KEY differentiator (LAB_027)
        # Malicious intention dramatically increases severity
        severity += maliciousness * 0.6  # Higher weight for intention

        severity = min(1.0, severity)

        # Determine primary basis
        # Action-based if action inherently wrong OR intention malicious
        if action_judgment == "wrong" or maliciousness > 0.6:
            primary_basis = "action"
        else:
            primary_basis = "outcome"

        return {
            "action_judgment": action_judgment,
            "outcome_judgment": outcome_judgment,
            "primary_basis": primary_basis,
            "severity": float(severity),
            "intention_factor": float(maliciousness)
        }

    def compute_fairness(
        self,
        distribution: Dict[str, float],
        principle: str = "equality",
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Compute fairness of distribution

        Three principles:
        - Equality: Everyone gets same amount
        - Merit: Proportional to contribution
        - Need: Proportional to need

        Parameters:
        -----------
        distribution : Dict[str, float]
            Resource distribution per person
        principle : str
            Fairness principle: "equality", "merit", or "need"
        context : Dict, optional
            Additional context (contributions, needs)

        Returns:
        --------
        result : Dict
            Fairness evaluation
        """
        context = context or {}
        values = list(distribution.values())

        if principle == "equality":
            # Measure deviation from equal distribution
            mean_value = sum(values) / len(values)
            deviations = [abs(v - mean_value) for v in values]
            max_deviation = max(deviations)

            # Normalize by mean (relative inequality)
            if mean_value > 0:
                inequality = max_deviation / mean_value
            else:
                inequality = 0.0

            fairness_score = max(0.0, 1.0 - inequality)
            inequality_detected = inequality > 0.3

        elif principle == "merit":
            # Compare distribution to contributions
            contributions = context.get("contributions", {})

            if not contributions:
                return {"error": "Merit-based fairness requires contributions"}

            # Calculate correlation between distribution and contributions
            total_distributed = sum(distribution.values())
            total_contributed = sum(contributions.values())

            # Normalize both
            dist_norm = {k: v/total_distributed for k, v in distribution.items()}
            contrib_norm = {k: v/total_contributed for k, v in contributions.items()}

            # Measure alignment
            deviations = [abs(dist_norm[k] - contrib_norm.get(k, 0))
                         for k in distribution.keys()]

            fairness_score = max(0.0, 1.0 - sum(deviations) / len(deviations))
            inequality_detected = fairness_score < 0.7

        elif principle == "need":
            # Compare distribution to needs
            needs = context.get("needs", {})

            if not needs:
                return {"error": "Need-based fairness requires needs specification"}

            # Calculate correlation between distribution and needs
            total_distributed = sum(distribution.values())
            total_needs = sum(needs.values())

            # Normalize both
            dist_norm = {k: v/total_distributed for k, v in distribution.items()}
            needs_norm = {k: v/total_needs for k, v in needs.items()}

            # Measure alignment
            deviations = [abs(dist_norm[k] - needs_norm.get(k, 0))
                         for k in distribution.keys()]

            fairness_score = max(0.0, 1.0 - sum(deviations) / len(deviations))
            inequality_detected = fairness_score < 0.7

        else:
            return {"error": f"Unknown fairness principle: {principle}"}

        return {
            "fairness_score": float(fairness_score),
            "principle_applied": principle,
            "inequality_detected": inequality_detected
        }

    def care_ethics_weight(
        self,
        empathy_level: float,
        relationship: str
    ) -> float:
        """
        Compute care ethics weight based on empathy and relationship

        Integration with LAB_028 (Empathy): High empathy increases
        deontological bias (care ethics).

        Parameters:
        -----------
        empathy_level : float
            Empathy level (0-1)
        relationship : str
            Relationship type: "close", "acquaintance", "stranger"

        Returns:
        --------
        care_weight : float
            Care ethics weight (0-1)
        """
        # Base weight from empathy
        care_weight = empathy_level

        # Relationship modulation
        relationship_multiplier = {
            "close": 1.5,
            "acquaintance": 1.0,
            "stranger": 0.7
        }

        multiplier = relationship_multiplier.get(relationship, 1.0)
        care_weight *= multiplier

        # Cap at 1.0
        care_weight = min(1.0, care_weight)

        return float(care_weight)

    def evaluate_fairness_from_perspective(
        self,
        distribution: Dict[str, float],
        perspective_holder: str
    ) -> Dict:
        """
        Evaluate fairness from specific person's perspective

        Integration with LAB_030 (Perspective Taking): Different
        perspectives perceive fairness differently.

        Parameters:
        -----------
        distribution : Dict[str, float]
            Resource distribution
        perspective_holder : str
            Person whose perspective to take

        Returns:
        --------
        result : Dict
            Fairness evaluation from their perspective
        """
        # Get their share
        their_share = distribution.get(perspective_holder, 0)
        mean_share = sum(distribution.values()) / len(distribution)

        # Perceived fairness depends on relative position
        # If they get more than average: perceive as fair
        # If they get less than average: perceive as unfair

        relative_position = their_share / mean_share if mean_share > 0 else 1.0

        if relative_position >= 1.0:
            # Getting fair share or more
            perceived_fairness = 0.8
        elif relative_position >= 0.7:
            # Getting slightly less
            perceived_fairness = 0.6
        elif relative_position >= 0.5:
            # Getting significantly less
            perceived_fairness = 0.4
        else:
            # Getting much less
            perceived_fairness = 0.2

        return {
            "perspective_holder": perspective_holder,
            "their_share": float(their_share),
            "mean_share": float(mean_share),
            "relative_position": float(relative_position),
            "perceived_fairness": float(perceived_fairness)
        }

    def process_event(
        self,
        event_type: str,
        **kwargs
    ) -> Dict:
        """
        Main processing: handle different event types

        Event types:
        - moral_dilemma: Process moral judgment
        - norm_observation: Learn from social feedback
        - fairness_evaluation: Evaluate fairness

        Parameters:
        -----------
        event_type : str
            Type of event
        **kwargs : Dict
            Event-specific parameters

        Returns:
        --------
        result : Dict
            Event processing result
        """
        if event_type == "moral_dilemma":
            scenario = kwargs.get("scenario", {})
            context = kwargs.get("context", {})
            return self.moral_judgment(scenario, context)

        elif event_type == "norm_observation":
            action = kwargs.get("action", "")
            approval = kwargs.get("approval", False)
            disapproval = kwargs.get("disapproval", False)

            result = self.observe_social_feedback(action, approval, disapproval)
            result["norm_updated"] = True
            return result

        elif event_type == "fairness_evaluation":
            distribution = kwargs.get("distribution", {})
            principle = kwargs.get("principle", "equality")
            context = kwargs.get("context", {})

            return self.compute_fairness(distribution, principle, context)

        else:
            return {"error": f"Unknown event type: {event_type}"}

    def get_state(self) -> Dict:
        """Get current system state"""
        return {
            "learned_norms": dict(self.learned_norms),
            "emotional_weight": float(self.emotional_weight),
            "rational_weight": float(self.rational_weight),
            "total_moral_judgments": int(self.total_moral_judgments),
            "total_norm_observations": int(self.total_norm_observations)
        }
