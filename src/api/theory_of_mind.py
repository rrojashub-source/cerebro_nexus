"""
LAB_023: Theory of Mind - Mental State Attribution & Belief Reasoning

Implements mentalizing and perspective-taking:
- Premack & Woodruff (1978): Does the chimpanzee have a theory of mind?
- Baron-Cohen et al. (1985): False belief task
- Frith & Frith (2006): The neural basis of mentalizing
- Saxe & Kanwisher (2003): TPJ and theory of mind

Core Functions:
1. Mental state attribution (beliefs, desires, intentions)
2. False belief reasoning (understanding that others can be wrong)
3. Perspective taking (visual and conceptual)
4. Intention recognition from behavior
5. Recursive mentalizing (I think that you think that...)
6. Belief updating from evidence

Neuroscience Foundation:
- Temporoparietal junction (TPJ): Mental state attribution
- Medial prefrontal cortex (mPFC): Self-other distinction
- Superior temporal sulcus (STS): Biological motion, intention
- Precuneus: First-person perspective

Integration:
- → LAB_024 (Empathy) for emotional perspective
- ← LAB_001 (Emotional Salience) for social signals
- → LAB_025 (Social Hierarchy) for status inference
- ← LAB_022 (Goal Management) for intention recognition
"""

import time
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import numpy as np
from enum import Enum


class MentalState(Enum):
    """Types of mental states"""
    BELIEF = "belief"
    DESIRE = "desire"
    INTENTION = "intention"
    KNOWLEDGE = "knowledge"
    EMOTION = "emotion"


class BeliefType(Enum):
    """Belief categories"""
    TRUE_BELIEF = "true_belief"
    FALSE_BELIEF = "false_belief"
    UNCERTAIN = "uncertain"


@dataclass
class Agent:
    """Representation of another agent"""
    agent_id: str
    name: str
    beliefs: Dict[str, any] = field(default_factory=dict)
    desires: Dict[str, float] = field(default_factory=dict)  # Goal: strength
    intentions: List[str] = field(default_factory=list)
    knowledge_state: Dict[str, bool] = field(default_factory=dict)  # Fact: known?
    current_emotion: Optional[str] = None
    observed_actions: List[str] = field(default_factory=list)


@dataclass
class MentalStateAttribution:
    """Attribution of mental state to agent"""
    timestamp: float
    agent_id: str
    state_type: MentalState
    content: str
    confidence: float  # 0-1
    evidence: List[str] = field(default_factory=list)


@dataclass
class FalseBelief:
    """False belief scenario"""
    timestamp: float
    agent_id: str
    belief_content: str
    actual_truth: str
    recognized: bool  # Did we recognize it as false?


@dataclass
class PerspectiveTaking:
    """Perspective taking event"""
    timestamp: float
    own_perspective: str
    other_perspective: str
    difference_recognized: bool
    effort_level: float  # Cognitive cost


class BeliefTracker:
    """
    Tracks beliefs of self and others.

    Implements belief reasoning including false beliefs.
    """

    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.self_beliefs: Dict[str, any] = {}

    def register_agent(self, agent_id: str, name: str):
        """Register new agent to track"""
        self.agents[agent_id] = Agent(agent_id=agent_id, name=name)

    def update_self_belief(self, fact: str, value: any):
        """Update own belief about world"""
        self.self_beliefs[fact] = value

    def attribute_belief(
        self,
        agent_id: str,
        fact: str,
        believed_value: any,
        confidence: float,
        evidence: List[str]
    ) -> MentalStateAttribution:
        """
        Attribute a belief to another agent.

        Returns attribution.
        """
        if agent_id not in self.agents:
            self.register_agent(agent_id, f"Agent_{agent_id}")

        agent = self.agents[agent_id]
        agent.beliefs[fact] = believed_value

        attribution = MentalStateAttribution(
            timestamp=time.time(),
            agent_id=agent_id,
            state_type=MentalState.BELIEF,
            content=f"{fact}={believed_value}",
            confidence=confidence,
            evidence=evidence
        )

        return attribution

    def detect_false_belief(
        self,
        agent_id: str,
        fact: str
    ) -> Optional[FalseBelief]:
        """
        Detect if agent has false belief (belief differs from reality).

        Returns FalseBelief if detected.
        """
        if agent_id not in self.agents:
            return None

        agent = self.agents[agent_id]

        if fact not in agent.beliefs:
            return None

        # Compare agent's belief with our belief (reality)
        agent_belief = agent.beliefs[fact]
        actual_truth = self.self_beliefs.get(fact)

        if actual_truth is None:
            # We don't know truth
            return None

        if agent_belief != actual_truth:
            # Agent has false belief
            false_belief = FalseBelief(
                timestamp=time.time(),
                agent_id=agent_id,
                belief_content=str(agent_belief),
                actual_truth=str(actual_truth),
                recognized=True
            )
            return false_belief

        return None


class IntentionRecognizer:
    """
    Infers intentions from observed actions.

    Based on inverse planning - inferring goals from behavior.
    """

    def __init__(self):
        self.intention_history: deque = deque(maxlen=500)

    def infer_intention(
        self,
        agent_id: str,
        observed_actions: List[str],
        context: Dict[str, any]
    ) -> Tuple[str, float]:
        """
        Infer agent's intention from actions.

        Returns:
            - inferred_intention
            - confidence
        """
        # Simple rule-based for now (could be probabilistic planning)

        if not observed_actions:
            return "unknown", 0.0

        # Pattern matching on action sequences
        action_sequence = " -> ".join(observed_actions[-3:])

        # Example patterns (would be learned in full system)
        patterns = {
            "move_to -> pick_up": ("obtain_object", 0.8),
            "look_at -> approach": ("investigate", 0.7),
            "reach_for -> grasp": ("take_possession", 0.85),
            "run_away -> hide": ("avoid_threat", 0.9),
        }

        for pattern, (intention, conf) in patterns.items():
            if pattern in action_sequence:
                return intention, conf

        # Default: low confidence guess
        return f"goal_related_to_{observed_actions[-1]}", 0.4


class PerspectiveTaker:
    """
    Takes perspectives of others (visual and conceptual).

    Implements Level 1 (what they see) and Level 2 (how they see it).
    """

    def __init__(self):
        self.perspective_history: deque = deque(maxlen=500)

    def compute_visual_perspective(
        self,
        own_view: Set[str],
        other_position: str,
        obstacles: List[str]
    ) -> Set[str]:
        """
        Compute what another agent can see from their position.

        Level 1 perspective taking.
        """
        # Simplified: assume position determines view
        # In reality would use geometric reasoning

        if other_position == "same":
            # Same position, same view
            return own_view
        elif other_position == "opposite":
            # Opposite side, reversed view
            # (oversimplified)
            return set([f"opposite_{item}" for item in own_view])
        else:
            # Different position, partial overlap
            # Filter by obstacles
            other_view = own_view.copy()
            for obstacle in obstacles:
                other_view.discard(obstacle)
            return other_view

    def take_conceptual_perspective(
        self,
        own_understanding: str,
        other_knowledge_level: float,
        topic: str
    ) -> Tuple[str, float]:
        """
        Understand how another conceptually understands something.

        Level 2 perspective taking.

        Returns:
            - estimated_understanding
            - effort_required
        """
        # Adjust own understanding based on other's knowledge
        if other_knowledge_level < 0.3:
            # Novice perspective
            estimated = f"simplified_{own_understanding}"
            effort = 0.7  # High effort to dumb down
        elif other_knowledge_level < 0.7:
            # Intermediate
            estimated = f"partial_{own_understanding}"
            effort = 0.4
        else:
            # Expert, similar to own
            estimated = own_understanding
            effort = 0.1

        return estimated, effort

    def recognize_perspective_difference(
        self,
        own_perspective: str,
        other_perspective: str
    ) -> PerspectiveTaking:
        """
        Recognize that self and other have different perspectives.

        Returns perspective taking event.
        """
        difference = (own_perspective != other_perspective)

        # Effort increases with difference
        if difference:
            effort = 0.6
        else:
            effort = 0.1

        event = PerspectiveTaking(
            timestamp=time.time(),
            own_perspective=own_perspective,
            other_perspective=other_perspective,
            difference_recognized=difference,
            effort_level=effort
        )

        self.perspective_history.append(event)

        return event


class RecursiveMentalizer:
    """
    Handles recursive mentalizing (I think that you think that...).

    Depth of recursion indicates ToM sophistication.
    """

    def __init__(self, max_depth: int = 3):
        self.max_depth = max_depth

    def mentalize_recursive(
        self,
        depth: int,
        agent_chain: List[str],
        belief_content: str
    ) -> Tuple[str, float]:
        """
        Construct recursive mental state attribution.

        Example:
        - Depth 0: "X is true"
        - Depth 1: "Agent A believes X"
        - Depth 2: "I believe that Agent A believes X"
        - Depth 3: "Agent B believes that I believe that Agent A believes X"

        Returns:
            - recursive_statement
            - cognitive_cost
        """
        if depth == 0:
            return belief_content, 0.1

        if depth > self.max_depth:
            # Too deep, fail
            return "too_complex", 1.0

        # Build recursive structure
        statement = belief_content
        for i in range(depth):
            agent = agent_chain[i] if i < len(agent_chain) else "someone"
            statement = f"{agent} believes that ({statement})"

        # Cost increases exponentially with depth
        cost = 0.2 * (2 ** depth)
        cost = min(1.0, cost)

        return statement, cost


class TheoryOfMindSystem:
    """
    Main LAB_023 implementation.

    Integrates:
    - Belief tracking (including false beliefs)
    - Intention recognition
    - Perspective taking
    - Recursive mentalizing
    """

    def __init__(self, max_recursion: int = 3):
        # Components
        self.belief_tracker = BeliefTracker()
        self.intention_recognizer = IntentionRecognizer()
        self.perspective_taker = PerspectiveTaker()
        self.recursive_mentalizer = RecursiveMentalizer(max_recursion)

        # History
        self.attribution_history: deque = deque(maxlen=1000)
        self.false_belief_history: deque = deque(maxlen=500)

        # Statistics
        self.total_attributions = 0
        self.false_beliefs_detected = 0
        self.perspective_takings = 0

    def register_agent(self, agent_id: str, name: str):
        """Register agent to track"""
        self.belief_tracker.register_agent(agent_id, name)

    def observe_world(self, fact: str, value: any):
        """Update own knowledge of world"""
        self.belief_tracker.update_self_belief(fact, value)

    def attribute_mental_state(
        self,
        agent_id: str,
        state_type: MentalState,
        content: str,
        evidence: List[str],
        confidence: float = 0.7
    ) -> MentalStateAttribution:
        """
        Attribute mental state to agent.

        Returns attribution.
        """
        if state_type == MentalState.BELIEF:
            # Parse content as fact=value
            if "=" in content:
                fact, value = content.split("=", 1)
                attribution = self.belief_tracker.attribute_belief(
                    agent_id, fact, value, confidence, evidence
                )
            else:
                # Generic belief
                attribution = MentalStateAttribution(
                    timestamp=time.time(),
                    agent_id=agent_id,
                    state_type=state_type,
                    content=content,
                    confidence=confidence,
                    evidence=evidence
                )
        else:
            # Other mental states
            attribution = MentalStateAttribution(
                timestamp=time.time(),
                agent_id=agent_id,
                state_type=state_type,
                content=content,
                confidence=confidence,
                evidence=evidence
            )

        self.attribution_history.append(attribution)
        self.total_attributions += 1

        return attribution

    def recognize_false_belief(
        self,
        agent_id: str,
        fact: str
    ) -> Optional[FalseBelief]:
        """
        Detect if agent has false belief.

        Classic ToM test (Sally-Anne task).
        """
        false_belief = self.belief_tracker.detect_false_belief(agent_id, fact)

        if false_belief:
            self.false_belief_history.append(false_belief)
            self.false_beliefs_detected += 1

        return false_belief

    def infer_intention_from_actions(
        self,
        agent_id: str,
        observed_actions: List[str],
        context: Dict[str, any]
    ) -> Tuple[str, float]:
        """
        Infer agent's intention from behavior.

        Returns intention and confidence.
        """
        intention, confidence = self.intention_recognizer.infer_intention(
            agent_id,
            observed_actions,
            context
        )

        # Store as attribution
        self.attribute_mental_state(
            agent_id,
            MentalState.INTENTION,
            intention,
            evidence=[f"observed: {', '.join(observed_actions)}"],
            confidence=confidence
        )

        return intention, confidence

    def take_visual_perspective(
        self,
        agent_id: str,
        other_position: str,
        obstacles: List[str]
    ) -> Set[str]:
        """
        Compute what agent can see from their position.

        Returns set of visible items.
        """
        # Assume we know our own view
        own_view = set(["item_A", "item_B", "item_C"])  # Placeholder

        other_view = self.perspective_taker.compute_visual_perspective(
            own_view,
            other_position,
            obstacles
        )

        self.perspective_takings += 1

        return other_view

    def mentalize_recursive(
        self,
        depth: int,
        agents: List[str],
        belief: str
    ) -> Tuple[str, float]:
        """
        Recursive mentalizing.

        Returns statement and cognitive cost.
        """
        return self.recursive_mentalizer.mentalize_recursive(
            depth,
            agents,
            belief
        )

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        return {
            "total_attributions": self.total_attributions,
            "false_beliefs_detected": self.false_beliefs_detected,
            "perspective_takings": self.perspective_takings,
            "agents_tracked": len(self.belief_tracker.agents),
            "avg_attribution_confidence": (
                np.mean([a.confidence for a in list(self.attribution_history)])
                if self.attribution_history else 0.0
            ),
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_023: Theory of Mind - Test")
    print("=" * 60)

    # Create ToM system
    tom = TheoryOfMindSystem(max_recursion=3)

    # Register agents
    print("\n👥 Registering agents...")
    tom.register_agent("alice", "Alice")
    tom.register_agent("bob", "Bob")
    print("  Registered: Alice, Bob")

    # Scenario 1: False belief (Sally-Anne task)
    print("\n🎭 Scenario: False Belief Task...")
    print("  Setup: Ball is in basket_A")
    tom.observe_world("ball_location", "basket_A")

    print("  Alice believes ball is in basket_A")
    tom.attribute_mental_state(
        "alice",
        MentalState.BELIEF,
        "ball_location=basket_A",
        evidence=["alice saw ball placed"],
        confidence=0.9
    )

    print("  Alice leaves room")
    print("  Ball moved to basket_B")
    tom.observe_world("ball_location", "basket_B")

    print("\n  Question: Where does Alice think the ball is?")
    false_belief = tom.recognize_false_belief("alice", "ball_location")
    if false_belief:
        print(f"  ✅ Recognized false belief!")
        print(f"     Alice believes: {false_belief.belief_content}")
        print(f"     Reality: {false_belief.actual_truth}")

    # Scenario 2: Intention recognition
    print("\n🎯 Scenario: Intention Recognition...")
    actions = ["move_to", "pick_up", "carry"]
    intention, conf = tom.infer_intention_from_actions(
        "bob",
        actions,
        context={}
    )
    print(f"  Observed: {' -> '.join(actions)}")
    print(f"  Inferred Intention: {intention}")
    print(f"  Confidence: {conf:.2f}")

    # Scenario 3: Perspective taking
    print("\n👀 Scenario: Visual Perspective Taking...")
    other_view = tom.take_visual_perspective(
        "alice",
        other_position="opposite",
        obstacles=["item_B"]
    )
    print(f"  Own view: {{item_A, item_B, item_C}}")
    print(f"  Alice's view (opposite): {other_view}")

    # Scenario 4: Recursive mentalizing
    print("\n🔄 Scenario: Recursive Mentalizing...")
    for depth in range(4):
        statement, cost = tom.mentalize_recursive(
            depth,
            ["Alice", "Bob", "I"],
            "the treasure is hidden"
        )
        print(f"  Depth {depth}: {statement}")
        print(f"    Cognitive cost: {cost:.2f}")

    # Show final statistics
    print("\n📈 Final Statistics:")
    stats = tom.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

    print("\n✅ LAB_023 Test Complete!")
