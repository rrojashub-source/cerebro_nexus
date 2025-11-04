"""
LAB_025: Social Hierarchy - Status Detection & Dominance Processing

Implements social rank and hierarchy processing:
- Sapolsky (2004): Social status and health in primates
- Fiske (2010): Interpersonal stratification
- Chiao et al. (2009): Neural basis of social status hierarchy
- Zink et al. (2008): Know your place - neural processing of status

Core Functions:
1. Status detection from behavior and signals
2. Dominance/submission response patterns
3. Relative rank computation
4. Status-seeking behavior motivation
5. Deference and assertion regulation
6. Social comparison processes

Neuroscience Foundation:
- Striatum: Reward from status gains
- Amygdala: Threat from status loss
- Prefrontal cortex: Status strategy
- TPJ: Social comparison

Integration:
- ← LAB_013 (Dopamine) for status-reward signals
- ← LAB_014 (Serotonin) for dominance (high 5-HT)
- ← LAB_023 (Theory of Mind) for status inference
- → LAB_026 (Cooperation) for coalition formation
"""

import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import deque
import numpy as np
from enum import Enum


class StatusLevel(Enum):
    """Relative status levels"""
    SUBORDINATE = "subordinate"
    EQUAL = "equal"
    DOMINANT = "dominant"


class StatusSignal(Enum):
    """Status display signals"""
    SUBMISSION = "submission"
    ASSERTION = "assertion"
    AGGRESSION = "aggression"
    APPEASEMENT = "appeasement"


@dataclass
class Agent:
    """Agent in hierarchy"""
    agent_id: str
    name: str
    status_score: float = 0.5  # 0-1
    dominance_tendency: float = 0.5
    observed_wins: int = 0
    observed_losses: int = 0


@dataclass
class StatusInteraction:
    """Status-relevant interaction"""
    timestamp: float
    agent_1: str
    agent_2: str
    interaction_type: str
    winner: Optional[str]
    status_change: Dict[str, float]


@dataclass
class StatusComparison:
    """Social comparison event"""
    timestamp: float
    self_status: float
    other_status: float
    comparison_outcome: str  # "superior", "equal", "inferior"
    emotional_response: str
    motivation_change: float


class StatusDetector:
    """Detects status from behavioral signals"""

    def __init__(self):
        self.signal_patterns = {
            "direct_gaze": 0.6,
            "averted_gaze": -0.4,
            "upright_posture": 0.5,
            "hunched_posture": -0.5,
            "loud_voice": 0.4,
            "quiet_voice": -0.3,
            "interrupt": 0.5,
            "yield": -0.5,
            "command": 0.7,
            "request": 0.0,
            "comply": -0.6
        }

    def detect_status_from_signals(
        self,
        observed_behaviors: List[str]
    ) -> float:
        """
        Estimate status from behavioral signals.

        Returns status estimate (0-1).
        """
        if not observed_behaviors:
            return 0.5

        scores = [
            self.signal_patterns.get(behavior, 0.0)
            for behavior in observed_behaviors
        ]

        avg_score = np.mean(scores)

        # Map from [-1, 1] to [0, 1]
        status = (avg_score + 1.0) / 2.0

        return status

    def infer_dominance_from_interaction(
        self,
        agent_1_behavior: str,
        agent_2_behavior: str
    ) -> Optional[str]:
        """
        Infer winner from dyadic interaction.

        Returns winner agent_id or None.
        """
        patterns = {
            ("command", "comply"): "agent_1",
            ("assert", "submit"): "agent_1",
            ("threaten", "flee"): "agent_1",
            ("demand", "yield"): "agent_1",
            ("comply", "command"): "agent_2",
            ("submit", "assert"): "agent_2",
        }

        return patterns.get((agent_1_behavior, agent_2_behavior))


class HierarchyTracker:
    """Maintains social hierarchy structure"""

    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.interaction_history: deque = deque(maxlen=1000)

    def register_agent(self, agent_id: str, name: str, initial_status: float = 0.5):
        """Register agent in hierarchy"""
        self.agents[agent_id] = Agent(
            agent_id=agent_id,
            name=name,
            status_score=initial_status
        )

    def update_from_interaction(
        self,
        agent_1: str,
        agent_2: str,
        winner: Optional[str]
    ) -> StatusInteraction:
        """
        Update hierarchy based on interaction outcome.

        Returns interaction record.
        """
        if winner == agent_1:
            self.agents[agent_1].observed_wins += 1
            self.agents[agent_2].observed_losses += 1

            # Winner gains status, loser loses
            status_shift = 0.05
            self.agents[agent_1].status_score = min(1.0, self.agents[agent_1].status_score + status_shift)
            self.agents[agent_2].status_score = max(0.0, self.agents[agent_2].status_score - status_shift)

        elif winner == agent_2:
            self.agents[agent_2].observed_wins += 1
            self.agents[agent_1].observed_losses += 1

            status_shift = 0.05
            self.agents[agent_2].status_score = min(1.0, self.agents[agent_2].status_score + status_shift)
            self.agents[agent_1].status_score = max(0.0, self.agents[agent_1].status_score - status_shift)
        else:
            # Draw, no change
            status_shift = 0.0

        interaction = StatusInteraction(
            timestamp=time.time(),
            agent_1=agent_1,
            agent_2=agent_2,
            interaction_type="competitive",
            winner=winner,
            status_change={
                agent_1: self.agents[agent_1].status_score,
                agent_2: self.agents[agent_2].status_score
            }
        )

        self.interaction_history.append(interaction)

        return interaction

    def get_relative_status(self, agent_1: str, agent_2: str) -> StatusLevel:
        """Compare status of two agents"""
        if agent_1 not in self.agents or agent_2 not in self.agents:
            return StatusLevel.EQUAL

        status_1 = self.agents[agent_1].status_score
        status_2 = self.agents[agent_2].status_score

        diff = status_1 - status_2

        if diff > 0.2:
            return StatusLevel.DOMINANT
        elif diff < -0.2:
            return StatusLevel.SUBORDINATE
        else:
            return StatusLevel.EQUAL

    def get_hierarchy_order(self) -> List[str]:
        """Get agents ordered by status (high to low)"""
        sorted_agents = sorted(
            self.agents.values(),
            key=lambda a: a.status_score,
            reverse=True
        )

        return [a.agent_id for a in sorted_agents]


class SocialComparator:
    """Performs social comparison processes"""

    def __init__(self):
        self.comparison_history: deque = deque(maxlen=500)

    def compare_status(
        self,
        self_status: float,
        other_status: float,
        domain: str = "general"
    ) -> StatusComparison:
        """
        Compare own status with other.

        Returns comparison outcome and emotional response.
        """
        diff = self_status - other_status

        if diff > 0.2:
            outcome = "superior"
            emotion = "pride"
            motivation_change = 0.1  # Satisfied
        elif diff < -0.2:
            outcome = "inferior"
            emotion = "envy"
            motivation_change = 0.3  # Motivated to improve
        else:
            outcome = "equal"
            emotion = "neutral"
            motivation_change = 0.0

        comparison = StatusComparison(
            timestamp=time.time(),
            self_status=self_status,
            other_status=other_status,
            comparison_outcome=outcome,
            emotional_response=emotion,
            motivation_change=motivation_change
        )

        self.comparison_history.append(comparison)

        return comparison


class DominanceRegulator:
    """Regulates dominance/submission behavior"""

    def __init__(self, baseline_dominance: float = 0.5):
        self.baseline_dominance = baseline_dominance
        self.current_dominance = baseline_dominance

    def select_behavior(
        self,
        own_status: float,
        other_status: float,
        context: str
    ) -> Tuple[StatusSignal, float]:
        """
        Select appropriate behavior based on relative status.

        Returns signal and intensity.
        """
        relative_status = own_status - other_status

        if relative_status > 0.3:
            # Clearly dominant
            if context == "conflict":
                signal = StatusSignal.ASSERTION
                intensity = 0.8
            else:
                signal = StatusSignal.ASSERTION
                intensity = 0.5
        elif relative_status < -0.3:
            # Clearly subordinate
            signal = StatusSignal.SUBMISSION
            intensity = 0.7
        else:
            # Equal or close
            if self.current_dominance > 0.6:
                signal = StatusSignal.ASSERTION
                intensity = 0.4
            else:
                signal = StatusSignal.APPEASEMENT
                intensity = 0.3

        return signal, intensity

    def update_dominance_tendency(self, success: bool, magnitude: float = 0.05):
        """Update dominance tendency based on outcomes"""
        if success:
            self.current_dominance = min(1.0, self.current_dominance + magnitude)
        else:
            self.current_dominance = max(0.0, self.current_dominance - magnitude)


class SocialHierarchySystem:
    """
    Main LAB_025 implementation.

    Manages:
    - Status detection
    - Hierarchy tracking
    - Social comparison
    - Dominance regulation
    """

    def __init__(self, self_agent_id: str = "self"):
        self.self_agent_id = self_agent_id

        # Components
        self.status_detector = StatusDetector()
        self.hierarchy_tracker = HierarchyTracker()
        self.social_comparator = SocialComparator()
        self.dominance_regulator = DominanceRegulator()

        # Register self
        self.hierarchy_tracker.register_agent(self_agent_id, "Self", 0.5)

        # Statistics
        self.total_interactions = 0
        self.total_comparisons = 0

    def register_agent(self, agent_id: str, name: str):
        """Register new agent"""
        self.hierarchy_tracker.register_agent(agent_id, name)

    def observe_interaction(
        self,
        agent_1: str,
        agent_2: str,
        agent_1_behavior: str,
        agent_2_behavior: str
    ) -> StatusInteraction:
        """
        Observe status-relevant interaction.

        Returns interaction record.
        """
        # Infer winner
        winner = self.status_detector.infer_dominance_from_interaction(
            agent_1_behavior,
            agent_2_behavior
        )

        # Update hierarchy
        interaction = self.hierarchy_tracker.update_from_interaction(
            agent_1,
            agent_2,
            winner
        )

        self.total_interactions += 1

        return interaction

    def detect_status_from_behavior(
        self,
        agent_id: str,
        observed_behaviors: List[str]
    ) -> float:
        """
        Estimate agent's status from behaviors.

        Returns status estimate.
        """
        status = self.status_detector.detect_status_from_signals(observed_behaviors)

        # Update agent's status
        if agent_id in self.hierarchy_tracker.agents:
            self.hierarchy_tracker.agents[agent_id].status_score = status

        return status

    def compare_with_other(
        self,
        other_agent_id: str,
        domain: str = "general"
    ) -> StatusComparison:
        """
        Compare own status with other agent.

        Returns comparison.
        """
        self_status = self.hierarchy_tracker.agents[self.self_agent_id].status_score
        other_status = self.hierarchy_tracker.agents[other_agent_id].status_score

        comparison = self.social_comparator.compare_status(
            self_status,
            other_status,
            domain
        )

        self.total_comparisons += 1

        return comparison

    def select_social_behavior(
        self,
        target_agent_id: str,
        context: str
    ) -> Tuple[StatusSignal, float]:
        """
        Select appropriate behavior toward target.

        Returns signal and intensity.
        """
        own_status = self.hierarchy_tracker.agents[self.self_agent_id].status_score
        other_status = self.hierarchy_tracker.agents[target_agent_id].status_score

        return self.dominance_regulator.select_behavior(
            own_status,
            other_status,
            context
        )

    def get_hierarchy(self) -> List[Tuple[str, float]]:
        """Get current hierarchy (agent, status)"""
        order = self.hierarchy_tracker.get_hierarchy_order()

        return [
            (agent_id, self.hierarchy_tracker.agents[agent_id].status_score)
            for agent_id in order
        ]

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        return {
            "self_status": self.hierarchy_tracker.agents[self.self_agent_id].status_score,
            "agents_tracked": len(self.hierarchy_tracker.agents),
            "total_interactions": self.total_interactions,
            "total_comparisons": self.total_comparisons,
            "current_dominance": self.dominance_regulator.current_dominance,
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_025: Social Hierarchy - Test")
    print("=" * 60)

    hierarchy = SocialHierarchySystem(self_agent_id="self")

    # Register agents
    print("\n👥 Registering agents...")
    hierarchy.register_agent("alpha", "Alpha")
    hierarchy.register_agent("beta", "Beta")
    hierarchy.register_agent("gamma", "Gamma")
    print("  Registered: Alpha, Beta, Gamma")

    # Scenario 1: Observe dominance interactions
    print("\n⚔️ Scenario 1: Observing dominance interactions...")
    interaction = hierarchy.observe_interaction(
        "alpha", "beta",
        "command", "comply"
    )
    print(f"  Alpha commands, Beta complies → Winner: {interaction.winner}")
    print(f"  Status changes: Alpha={interaction.status_change['alpha']:.3f}, Beta={interaction.status_change['beta']:.3f}")

    # More interactions
    hierarchy.observe_interaction("alpha", "gamma", "assert", "submit")
    hierarchy.observe_interaction("beta", "gamma", "command", "comply")

    # Show hierarchy
    print("\n🏆 Current Hierarchy:")
    for rank, (agent_id, status) in enumerate(hierarchy.get_hierarchy(), 1):
        print(f"  {rank}. {agent_id}: {status:.3f}")

    # Scenario 2: Status detection from behavior
    print("\n👀 Scenario 2: Detecting status from behavior...")
    behaviors = ["direct_gaze", "upright_posture", "loud_voice", "interrupt"]
    detected_status = hierarchy.detect_status_from_behavior("alpha", behaviors)
    print(f"  Observed behaviors: {', '.join(behaviors)}")
    print(f"  Detected status: {detected_status:.3f} (high)")

    # Scenario 3: Social comparison
    print("\n📊 Scenario 3: Social comparison...")
    comparison = hierarchy.compare_with_other("alpha")
    print(f"  Self status: {comparison.self_status:.3f}")
    print(f"  Alpha status: {comparison.other_status:.3f}")
    print(f"  Outcome: {comparison.comparison_outcome}")
    print(f"  Emotion: {comparison.emotional_response}")

    # Scenario 4: Behavior selection
    print("\n🎭 Scenario 4: Selecting behavior...")
    signal, intensity = hierarchy.select_social_behavior("alpha", "conflict")
    print(f"  Context: conflict with Alpha (high status)")
    print(f"  Selected behavior: {signal.value}")
    print(f"  Intensity: {intensity:.3f}")

    signal, intensity = hierarchy.select_social_behavior("gamma", "neutral")
    print(f"  Context: neutral with Gamma (low status)")
    print(f"  Selected behavior: {signal.value}")
    print(f"  Intensity: {intensity:.3f}")

    # Show final statistics
    print("\n📈 Final Statistics:")
    stats = hierarchy.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

    print("\n✅ LAB_025 Test Complete!")
