"""
LAB_026: Cooperation & Trust - Reciprocity and Coalition Formation

Implements cooperation and trust dynamics:
- Axelrod (1984): Evolution of cooperation, tit-for-tat
- Nowak & Sigmund (2005): Indirect reciprocity, reputation
- Trivers (1971): Reciprocal altruism theory
- Fehr & Gächter (2000): Cooperation and punishment in public goods

Core Functions:
1. Direct reciprocity tracking (tit-for-tat, generous tit-for-tat)
2. Indirect reciprocity and reputation systems
3. Trust computation and updating
4. Cooperation strategies (prisoner's dilemma, public goods)
5. Coalition formation and maintenance
6. Altruism vs self-interest trade-offs

Neuroscience Foundation:
- Ventral striatum: Trust rewards
- Anterior insula: Betrayal aversion
- TPJ: Fairness evaluation
- vmPFC: Value of cooperation

Integration:
- ← LAB_013 (Dopamine) for cooperation rewards
- ← LAB_023 (Theory of Mind) for intention inference
- ← LAB_025 (Social Hierarchy) for coalition power
- → LAB_027 (Moral Reasoning) for fairness norms
"""

import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import deque, defaultdict
from enum import Enum
import numpy as np


class CooperationStrategy(Enum):
    """Cooperation strategies"""
    TIT_FOR_TAT = "tit_for_tat"
    GENEROUS_TFT = "generous_tft"
    ALWAYS_COOPERATE = "always_cooperate"
    ALWAYS_DEFECT = "always_defect"
    PAVLOV = "pavlov"  # Win-stay, lose-shift
    RANDOM = "random"


class ActionType(Enum):
    """Social action types"""
    COOPERATE = "cooperate"
    DEFECT = "defect"
    HELP = "help"
    REFUSE = "refuse"
    SHARE = "share"
    HOARD = "hoard"


@dataclass
class InteractionRecord:
    """Record of social interaction"""
    timestamp: float
    agent_1: str
    agent_2: str
    agent_1_action: ActionType
    agent_2_action: ActionType
    agent_1_payoff: float
    agent_2_payoff: float
    cooperation_occurred: bool


@dataclass
class TrustRecord:
    """Trust level toward agent"""
    agent_id: str
    trust_level: float  # 0-1
    interactions_count: int
    cooperation_count: int
    defection_count: int
    last_interaction: float
    trust_trend: str  # "increasing", "stable", "decreasing"


@dataclass
class ReputationRecord:
    """Agent's reputation in community"""
    agent_id: str
    reputation_score: float  # 0-1
    observed_cooperations: int
    observed_defections: int
    indirect_reports: List[Tuple[str, bool]]  # (reporter_id, cooperated)
    last_updated: float


@dataclass
class Coalition:
    """Coalition of cooperating agents"""
    coalition_id: str
    members: List[str]
    created_at: float
    total_contributions: Dict[str, float]
    shared_resources: float
    cooperation_rate: float
    stability: float  # 0-1


class ReciprocityTracker:
    """Tracks reciprocity patterns"""

    def __init__(self):
        self.interaction_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.reciprocity_scores: Dict[str, float] = {}

    def record_interaction(
        self,
        partner_id: str,
        my_action: ActionType,
        partner_action: ActionType
    ):
        """Record interaction for reciprocity tracking"""
        self.interaction_history[partner_id].append({
            "timestamp": time.time(),
            "my_action": my_action,
            "partner_action": partner_action
        })

        # Update reciprocity score
        self._update_reciprocity_score(partner_id)

    def _update_reciprocity_score(self, partner_id: str):
        """
        Compute reciprocity score (0-1).

        High score = partner reciprocates cooperation.
        """
        history = self.interaction_history[partner_id]
        if len(history) < 2:
            self.reciprocity_scores[partner_id] = 0.5
            return

        reciprocations = 0
        opportunities = 0

        for i in range(1, len(history)):
            prev = history[i-1]
            curr = history[i]

            # If I cooperated last time
            if prev["my_action"] in [ActionType.COOPERATE, ActionType.HELP, ActionType.SHARE]:
                opportunities += 1
                # Did partner cooperate this time?
                if curr["partner_action"] in [ActionType.COOPERATE, ActionType.HELP, ActionType.SHARE]:
                    reciprocations += 1

        if opportunities == 0:
            score = 0.5
        else:
            score = reciprocations / opportunities

        self.reciprocity_scores[partner_id] = score

    def get_reciprocity_score(self, partner_id: str) -> float:
        """Get reciprocity score for partner"""
        return self.reciprocity_scores.get(partner_id, 0.5)

    def predict_next_action(
        self,
        partner_id: str,
        my_last_action: ActionType,
        strategy: CooperationStrategy = CooperationStrategy.TIT_FOR_TAT
    ) -> ActionType:
        """
        Predict partner's next action based on strategy.

        Returns predicted action.
        """
        if partner_id not in self.interaction_history or len(self.interaction_history[partner_id]) == 0:
            # No history, assume cooperation
            return ActionType.COOPERATE

        last_partner_action = self.interaction_history[partner_id][-1]["partner_action"]

        if strategy == CooperationStrategy.TIT_FOR_TAT:
            # Predict partner will mirror my last action
            if my_last_action in [ActionType.COOPERATE, ActionType.HELP, ActionType.SHARE]:
                return ActionType.COOPERATE
            else:
                return ActionType.DEFECT

        elif strategy == CooperationStrategy.GENEROUS_TFT:
            # Like tit-for-tat but occasionally forgive defection
            if my_last_action in [ActionType.COOPERATE, ActionType.HELP, ActionType.SHARE]:
                return ActionType.COOPERATE
            else:
                # 10% chance to forgive
                return ActionType.COOPERATE if np.random.random() < 0.1 else ActionType.DEFECT

        else:
            # Default: mirror their last action
            return last_partner_action


class TrustComputer:
    """Computes and updates trust levels"""

    def __init__(self, initial_trust: float = 0.5, learning_rate: float = 0.1):
        self.trust_records: Dict[str, TrustRecord] = {}
        self.initial_trust = initial_trust
        self.learning_rate = learning_rate

    def initialize_trust(self, agent_id: str):
        """Initialize trust record for new agent"""
        if agent_id not in self.trust_records:
            self.trust_records[agent_id] = TrustRecord(
                agent_id=agent_id,
                trust_level=self.initial_trust,
                interactions_count=0,
                cooperation_count=0,
                defection_count=0,
                last_interaction=time.time(),
                trust_trend="stable"
            )

    def update_trust(
        self,
        agent_id: str,
        cooperated: bool,
        magnitude: float = 1.0
    ) -> float:
        """
        Update trust based on interaction outcome.

        Trust increases with cooperation, decreases with defection.
        Uses asymmetric learning (negative events have stronger impact).

        Returns new trust level.
        """
        self.initialize_trust(agent_id)
        record = self.trust_records[agent_id]

        # Asymmetric learning: Betrayal hurts more than cooperation helps
        if cooperated:
            delta = self.learning_rate * magnitude * (1.0 - record.trust_level)
            record.cooperation_count += 1
        else:
            delta = -self.learning_rate * magnitude * 1.5 * record.trust_level
            record.defection_count += 1

        # Update trust
        record.trust_level = np.clip(record.trust_level + delta, 0.0, 1.0)
        record.interactions_count += 1
        record.last_interaction = time.time()

        # Update trend
        self._update_trust_trend(agent_id)

        return record.trust_level

    def _update_trust_trend(self, agent_id: str):
        """Update trust trend based on recent interactions"""
        record = self.trust_records[agent_id]

        if record.interactions_count < 5:
            record.trust_trend = "stable"
            return

        recent_coop_rate = record.cooperation_count / record.interactions_count

        if recent_coop_rate > 0.7:
            record.trust_trend = "increasing"
        elif recent_coop_rate < 0.3:
            record.trust_trend = "decreasing"
        else:
            record.trust_trend = "stable"

    def get_trust(self, agent_id: str) -> float:
        """Get current trust level"""
        self.initialize_trust(agent_id)
        return self.trust_records[agent_id].trust_level

    def should_cooperate(
        self,
        agent_id: str,
        cooperation_threshold: float = 0.5
    ) -> bool:
        """
        Decide if should cooperate based on trust.

        Returns True if trust >= threshold.
        """
        trust = self.get_trust(agent_id)
        return trust >= cooperation_threshold


class ReputationSystem:
    """Manages indirect reciprocity through reputation"""

    def __init__(self):
        self.reputations: Dict[str, ReputationRecord] = {}

    def initialize_reputation(self, agent_id: str):
        """Initialize reputation for new agent"""
        if agent_id not in self.reputations:
            self.reputations[agent_id] = ReputationRecord(
                agent_id=agent_id,
                reputation_score=0.5,
                observed_cooperations=0,
                observed_defections=0,
                indirect_reports=[],
                last_updated=time.time()
            )

    def observe_interaction(
        self,
        agent_id: str,
        cooperated: bool
    ):
        """
        Observe agent's behavior (indirect reciprocity).

        Updates reputation based on observed cooperation/defection.
        """
        self.initialize_reputation(agent_id)
        record = self.reputations[agent_id]

        if cooperated:
            record.observed_cooperations += 1
        else:
            record.observed_defections += 1

        self._update_reputation_score(agent_id)

    def receive_reputation_report(
        self,
        agent_id: str,
        reporter_id: str,
        cooperated: bool
    ):
        """
        Receive reputation report from another agent.

        Implements gossip and social learning.
        """
        self.initialize_reputation(agent_id)
        record = self.reputations[agent_id]

        record.indirect_reports.append((reporter_id, cooperated))

        # Keep only recent 50 reports
        if len(record.indirect_reports) > 50:
            record.indirect_reports = record.indirect_reports[-50:]

        self._update_reputation_score(agent_id)

    def _update_reputation_score(self, agent_id: str):
        """
        Update reputation score from observations and reports.

        Direct observations weighted more than indirect reports.
        """
        record = self.reputations[agent_id]

        # Direct observations (weight 0.7)
        total_direct = record.observed_cooperations + record.observed_defections
        if total_direct > 0:
            direct_score = record.observed_cooperations / total_direct
        else:
            direct_score = 0.5

        # Indirect reports (weight 0.3)
        if len(record.indirect_reports) > 0:
            indirect_coops = sum(1 for _, coop in record.indirect_reports if coop)
            indirect_score = indirect_coops / len(record.indirect_reports)
        else:
            indirect_score = 0.5

        # Weighted combination
        record.reputation_score = 0.7 * direct_score + 0.3 * indirect_score
        record.last_updated = time.time()

    def get_reputation(self, agent_id: str) -> float:
        """Get agent's reputation score"""
        self.initialize_reputation(agent_id)
        return self.reputations[agent_id].reputation_score


class CoalitionManager:
    """Manages coalition formation and maintenance"""

    def __init__(self):
        self.coalitions: Dict[str, Coalition] = {}
        self.agent_coalitions: Dict[str, str] = {}  # agent_id -> coalition_id
        self.coalition_counter = 0

    def form_coalition(
        self,
        founding_members: List[str],
        initial_contributions: Optional[Dict[str, float]] = None
    ) -> Coalition:
        """
        Form new coalition.

        Returns coalition object.
        """
        coalition_id = f"coalition_{self.coalition_counter:03d}"
        self.coalition_counter += 1

        if initial_contributions is None:
            initial_contributions = {member: 0.0 for member in founding_members}

        coalition = Coalition(
            coalition_id=coalition_id,
            members=founding_members.copy(),
            created_at=time.time(),
            total_contributions=initial_contributions,
            shared_resources=sum(initial_contributions.values()),
            cooperation_rate=1.0,  # Initial optimism
            stability=1.0
        )

        self.coalitions[coalition_id] = coalition

        # Register members
        for member in founding_members:
            self.agent_coalitions[member] = coalition_id

        return coalition

    def add_member(
        self,
        coalition_id: str,
        new_member: str,
        initial_contribution: float = 0.0
    ):
        """Add member to coalition"""
        if coalition_id not in self.coalitions:
            return

        coalition = self.coalitions[coalition_id]
        coalition.members.append(new_member)
        coalition.total_contributions[new_member] = initial_contribution
        coalition.shared_resources += initial_contribution

        self.agent_coalitions[new_member] = coalition_id

    def contribute_to_coalition(
        self,
        agent_id: str,
        amount: float
    ):
        """Agent contributes resources to their coalition"""
        if agent_id not in self.agent_coalitions:
            return

        coalition_id = self.agent_coalitions[agent_id]
        coalition = self.coalitions[coalition_id]

        coalition.total_contributions[agent_id] += amount
        coalition.shared_resources += amount

    def defect_from_coalition(
        self,
        agent_id: str
    ):
        """Agent defects from coalition (free-riding or leaving)"""
        if agent_id not in self.agent_coalitions:
            return

        coalition_id = self.agent_coalitions[agent_id]
        coalition = self.coalitions[coalition_id]

        # Leaving impacts stability
        coalition.stability *= 0.8

        # Remove member
        coalition.members.remove(agent_id)
        del self.agent_coalitions[agent_id]

    def compute_coalition_stability(self, coalition_id: str) -> float:
        """
        Compute coalition stability.

        Stability depends on:
        - Cooperation rate
        - Equality of contributions
        - Member count
        """
        if coalition_id not in self.coalitions:
            return 0.0

        coalition = self.coalitions[coalition_id]

        if len(coalition.members) == 0:
            return 0.0

        # Equality of contributions (Gini coefficient)
        contributions = list(coalition.total_contributions.values())
        if sum(contributions) == 0:
            equality = 0.5
        else:
            # Higher variance = lower equality
            mean_contrib = np.mean(contributions)
            std_contrib = np.std(contributions)
            if mean_contrib == 0:
                equality = 0.5
            else:
                cv = std_contrib / mean_contrib  # Coefficient of variation
                equality = 1.0 / (1.0 + cv)

        # Member count (larger = more stable, up to a point)
        size_factor = min(1.0, len(coalition.members) / 5.0)

        # Combined stability
        stability = 0.4 * coalition.cooperation_rate + 0.4 * equality + 0.2 * size_factor

        coalition.stability = stability

        return stability


class CooperationTrustSystem:
    """
    Main LAB_026 implementation.

    Manages:
    - Reciprocity tracking
    - Trust computation
    - Reputation systems
    - Coalition formation
    """

    def __init__(self, self_agent_id: str = "self"):
        self.self_agent_id = self_agent_id

        # Components
        self.reciprocity_tracker = ReciprocityTracker()
        self.trust_computer = TrustComputer()
        self.reputation_system = ReputationSystem()
        self.coalition_manager = CoalitionManager()

        # Interaction history
        self.interaction_history: deque = deque(maxlen=1000)

        # Statistics
        self.total_interactions = 0
        self.total_cooperations = 0
        self.total_defections = 0

    def interact(
        self,
        partner_id: str,
        my_action: ActionType,
        partner_action: ActionType,
        my_payoff: float,
        partner_payoff: float
    ) -> InteractionRecord:
        """
        Record social interaction.

        Returns interaction record.
        """
        cooperated = my_action in [ActionType.COOPERATE, ActionType.HELP, ActionType.SHARE]
        partner_cooperated = partner_action in [ActionType.COOPERATE, ActionType.HELP, ActionType.SHARE]

        # Update reciprocity tracker
        self.reciprocity_tracker.record_interaction(partner_id, my_action, partner_action)

        # Update trust
        self.trust_computer.update_trust(partner_id, partner_cooperated)

        # Update reputation (observe partner's behavior)
        self.reputation_system.observe_interaction(partner_id, partner_cooperated)

        # Create record
        interaction = InteractionRecord(
            timestamp=time.time(),
            agent_1=self.self_agent_id,
            agent_2=partner_id,
            agent_1_action=my_action,
            agent_2_action=partner_action,
            agent_1_payoff=my_payoff,
            agent_2_payoff=partner_payoff,
            cooperation_occurred=cooperated and partner_cooperated
        )

        self.interaction_history.append(interaction)

        # Update statistics
        self.total_interactions += 1
        if cooperated:
            self.total_cooperations += 1
        else:
            self.total_defections += 1

        return interaction

    def decide_action(
        self,
        partner_id: str,
        strategy: CooperationStrategy = CooperationStrategy.TIT_FOR_TAT,
        trust_threshold: float = 0.5
    ) -> ActionType:
        """
        Decide whether to cooperate or defect.

        Returns action.
        """
        # Get trust level
        trust = self.trust_computer.get_trust(partner_id)

        # Get reputation
        reputation = self.reputation_system.get_reputation(partner_id)

        # Combined trust-reputation score
        trust_rep_score = 0.6 * trust + 0.4 * reputation

        # Strategy-based decision
        if strategy == CooperationStrategy.ALWAYS_COOPERATE:
            return ActionType.COOPERATE

        elif strategy == CooperationStrategy.ALWAYS_DEFECT:
            return ActionType.DEFECT

        elif strategy == CooperationStrategy.TIT_FOR_TAT:
            # Cooperate if trust above threshold
            if trust_rep_score >= trust_threshold:
                return ActionType.COOPERATE
            else:
                return ActionType.DEFECT

        elif strategy == CooperationStrategy.GENEROUS_TFT:
            # More forgiving
            if trust_rep_score >= trust_threshold * 0.8:
                return ActionType.COOPERATE
            else:
                # Occasionally cooperate even with low trust (forgiveness)
                return ActionType.COOPERATE if np.random.random() < 0.1 else ActionType.DEFECT

        elif strategy == CooperationStrategy.PAVLOV:
            # Win-stay, lose-shift
            # If last interaction was profitable, repeat; otherwise switch
            history = list(self.reciprocity_tracker.interaction_history.get(partner_id, []))
            if len(history) > 0:
                last = history[-1]
                # If we cooperated and got cooperation back, or defected and they defected
                # (mutual cooperation or mutual defection), stay
                if (last["my_action"] == ActionType.COOPERATE and
                    last["partner_action"] == ActionType.COOPERATE):
                    return ActionType.COOPERATE
                elif (last["my_action"] == ActionType.DEFECT and
                      last["partner_action"] == ActionType.DEFECT):
                    return ActionType.DEFECT
                else:
                    # Switch
                    return ActionType.DEFECT if last["my_action"] == ActionType.COOPERATE else ActionType.COOPERATE
            else:
                return ActionType.COOPERATE

        else:
            # Default: trust-based
            return ActionType.COOPERATE if trust_rep_score >= trust_threshold else ActionType.DEFECT

    def form_coalition_with(
        self,
        partners: List[str],
        my_contribution: float
    ) -> Coalition:
        """
        Form coalition with partners.

        Returns coalition.
        """
        members = [self.self_agent_id] + partners
        contributions = {self.self_agent_id: my_contribution}

        # Initialize partners with zero contribution
        for partner in partners:
            contributions[partner] = 0.0

        coalition = self.coalition_manager.form_coalition(members, contributions)

        return coalition

    def evaluate_cooperation_value(
        self,
        partner_id: str,
        cooperation_benefit: float,
        defection_benefit: float,
        partner_cooperation_prob: float
    ) -> float:
        """
        Evaluate expected value of cooperation vs defection.

        Returns expected value difference (positive = cooperate better).
        """
        # Expected value of cooperation
        ev_cooperate = partner_cooperation_prob * cooperation_benefit + \
                      (1 - partner_cooperation_prob) * 0.0

        # Expected value of defection
        ev_defect = defection_benefit

        return ev_cooperate - ev_defect

    def get_trust_report(self, agent_id: str) -> Dict:
        """Get comprehensive trust report for agent"""
        trust = self.trust_computer.get_trust(agent_id)
        reputation = self.reputation_system.get_reputation(agent_id)
        reciprocity = self.reciprocity_tracker.get_reciprocity_score(agent_id)

        trust_record = self.trust_computer.trust_records.get(agent_id)

        return {
            "agent_id": agent_id,
            "trust_level": trust,
            "reputation_score": reputation,
            "reciprocity_score": reciprocity,
            "interactions_count": trust_record.interactions_count if trust_record else 0,
            "cooperation_rate": (trust_record.cooperation_count / trust_record.interactions_count
                               if trust_record and trust_record.interactions_count > 0 else 0.0),
            "trust_trend": trust_record.trust_trend if trust_record else "unknown"
        }

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        return {
            "total_interactions": self.total_interactions,
            "total_cooperations": self.total_cooperations,
            "total_defections": self.total_defections,
            "cooperation_rate": (self.total_cooperations / self.total_interactions
                               if self.total_interactions > 0 else 0.0),
            "agents_tracked": len(self.trust_computer.trust_records),
            "active_coalitions": len(self.coalition_manager.coalitions),
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_026: Cooperation & Trust - Test")
    print("=" * 60)

    system = CooperationTrustSystem(self_agent_id="self")

    # Scenario 1: Tit-for-tat cooperation
    print("\n🤝 Scenario 1: Tit-for-tat with trustworthy partner...")
    partner = "alice"

    for round_num in range(5):
        # Decide action
        my_action = system.decide_action(partner, strategy=CooperationStrategy.TIT_FOR_TAT)

        # Simulate partner cooperating
        partner_action = ActionType.COOPERATE

        # Interaction payoffs (prisoner's dilemma)
        if my_action == ActionType.COOPERATE and partner_action == ActionType.COOPERATE:
            my_payoff, partner_payoff = 3.0, 3.0
        elif my_action == ActionType.COOPERATE and partner_action == ActionType.DEFECT:
            my_payoff, partner_payoff = 0.0, 5.0
        elif my_action == ActionType.DEFECT and partner_action == ActionType.COOPERATE:
            my_payoff, partner_payoff = 5.0, 0.0
        else:
            my_payoff, partner_payoff = 1.0, 1.0

        interaction = system.interact(partner, my_action, partner_action, my_payoff, partner_payoff)

        trust = system.trust_computer.get_trust(partner)
        print(f"  Round {round_num + 1}: Me={my_action.value}, Partner={partner_action.value}, "
              f"Trust={trust:.3f}, Payoff={my_payoff:.1f}")

    # Scenario 2: Trust breakdown after betrayal
    print("\n💔 Scenario 2: Trust breakdown after betrayal...")
    betrayer = "bob"

    # Initial cooperation
    for _ in range(3):
        system.interact(betrayer, ActionType.COOPERATE, ActionType.COOPERATE, 3.0, 3.0)

    trust_before = system.trust_computer.get_trust(betrayer)
    print(f"  Trust before betrayal: {trust_before:.3f}")

    # Betrayal
    system.interact(betrayer, ActionType.COOPERATE, ActionType.DEFECT, 0.0, 5.0)

    trust_after = system.trust_computer.get_trust(betrayer)
    print(f"  Trust after betrayal: {trust_after:.3f}")

    # Decision changes
    next_action = system.decide_action(betrayer, strategy=CooperationStrategy.TIT_FOR_TAT)
    print(f"  Next action toward betrayer: {next_action.value}")

    # Scenario 3: Reputation and indirect reciprocity
    print("\n📢 Scenario 3: Reputation and indirect reciprocity...")
    stranger = "charlie"

    # Observe stranger cooperating with others
    for _ in range(4):
        system.reputation_system.observe_interaction(stranger, cooperated=True)

    # Receive positive report
    system.reputation_system.receive_reputation_report(stranger, "alice", cooperated=True)

    reputation = system.reputation_system.get_reputation(stranger)
    print(f"  Stranger's reputation: {reputation:.3f}")

    # Decision based on reputation
    action = system.decide_action(stranger, strategy=CooperationStrategy.TIT_FOR_TAT, trust_threshold=0.5)
    print(f"  Action toward stranger (based on reputation): {action.value}")

    # Scenario 4: Coalition formation
    print("\n👥 Scenario 4: Coalition formation...")
    coalition = system.form_coalition_with(["alice", "charlie"], my_contribution=10.0)
    print(f"  Coalition formed: {coalition.coalition_id}")
    print(f"  Members: {', '.join(coalition.members)}")

    # Members contribute
    system.coalition_manager.contribute_to_coalition("alice", 8.0)
    system.coalition_manager.contribute_to_coalition("charlie", 12.0)

    stability = system.coalition_manager.compute_coalition_stability(coalition.coalition_id)
    print(f"  Coalition stability: {stability:.3f}")
    print(f"  Total resources: {coalition.shared_resources:.1f}")

    # Scenario 5: Cooperation value calculation
    print("\n💰 Scenario 5: Evaluating cooperation value...")
    partner_coop_prob = system.trust_computer.get_trust("alice")
    value_diff = system.evaluate_cooperation_value(
        "alice",
        cooperation_benefit=3.0,
        defection_benefit=1.5,
        partner_cooperation_prob=partner_coop_prob
    )
    print(f"  Partner cooperation probability: {partner_coop_prob:.3f}")
    print(f"  Expected value difference (coop - defect): {value_diff:.3f}")
    print(f"  Recommendation: {'COOPERATE' if value_diff > 0 else 'DEFECT'}")

    # Final statistics
    print("\n📈 Final Statistics:")
    stats = system.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

    # Trust reports
    print("\n📊 Trust Reports:")
    for agent_id in ["alice", "bob", "charlie"]:
        report = system.get_trust_report(agent_id)
        print(f"  {agent_id}: Trust={report['trust_level']:.3f}, "
              f"Reputation={report['reputation_score']:.3f}, "
              f"Reciprocity={report['reciprocity_score']:.3f}, "
              f"Trend={report['trust_trend']}")

    print("\n✅ LAB_026 Test Complete!")
