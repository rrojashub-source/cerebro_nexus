"""
LAB_022: Goal Management - Goal Hierarchy, Priority, and Conflict Resolution

Implements hierarchical goal structures and management:
- Austin & Vancouver (1996): Goal constructs in psychology
- Locke & Latham (2002): Building a practically useful theory of goal setting
- Kruglanski et al. (2002): Goal systems theory
- Shah & Kruglanski (2003): When opportunity knocks

Core Functions:
1. Hierarchical goal representation (supergoals/subgoals)
2. Goal prioritization and scheduling
3. Goal conflict detection and resolution
4. Goal shielding (protecting current goal)
5. Goal pursuit evaluation (progress monitoring)
6. Goal persistence vs disengagement

Neuroscience Foundation:
- Rostral PFC: Abstract goal representation, goal hierarchy
- Dorsolateral PFC (dlPFC): Goal maintenance
- Orbitofrontal cortex (OFC): Goal value evaluation
- ACC: Goal conflict monitoring

Integration:
- ← LAB_021 (Planning & Sequencing) for goal decomposition
- ← LAB_018 (Working Memory Executive) for goal maintenance
- ← LAB_013 (Dopamine) for goal-value signals
- ← LAB_019 (Cognitive Control) for goal switching
"""

import time
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import numpy as np
from enum import Enum
import uuid


class GoalStatus(Enum):
    """Goal status"""
    INACTIVE = "inactive"
    ACTIVE = "active"
    ACHIEVED = "achieved"
    ABANDONED = "abandoned"
    BLOCKED = "blocked"


class GoalType(Enum):
    """Goal abstraction level"""
    ABSTRACT = "abstract"      # High-level, long-term
    CONCRETE = "concrete"      # Specific, actionable
    SUPERGOAL = "supergoal"    # Meta-goal (goal for goals)


@dataclass
class Goal:
    """Individual goal representation"""
    goal_id: str
    description: str
    goal_type: GoalType
    priority: float  # 0-1
    value: float  # Expected value/reward (0-1)
    difficulty: float  # 0-1
    status: GoalStatus = GoalStatus.INACTIVE
    parent_goal_id: Optional[str] = None
    subgoal_ids: List[str] = field(default_factory=list)
    deadline: Optional[float] = None
    progress: float = 0.0  # 0-1
    activation_level: float = 0.0  # Current activation
    creation_time: float = field(default_factory=time.time)
    last_pursued: Optional[float] = None


@dataclass
class GoalConflict:
    """Goal conflict event"""
    timestamp: float
    goal_1_id: str
    goal_2_id: str
    conflict_type: str  # "resource", "timing", "incompatible"
    severity: float  # 0-1
    resolution_strategy: Optional[str] = None


@dataclass
class GoalPursuitEvent:
    """Goal pursuit progress event"""
    timestamp: float
    goal_id: str
    action_taken: str
    progress_delta: float
    effort_invested: float
    outcome: str  # "success", "partial", "failure"


class GoalHierarchyManager:
    """
    Manages hierarchical goal structures.

    Implements tree structure with parent-child relationships.
    """

    def __init__(self):
        self.goals: Dict[str, Goal] = {}
        self.root_goals: List[str] = []  # Top-level goals

    def add_goal(
        self,
        description: str,
        goal_type: GoalType,
        priority: float,
        value: float,
        difficulty: float,
        parent_goal_id: Optional[str] = None,
        deadline: Optional[float] = None
    ) -> str:
        """Add new goal to hierarchy"""
        goal_id = str(uuid.uuid4())[:8]

        goal = Goal(
            goal_id=goal_id,
            description=description,
            goal_type=goal_type,
            priority=priority,
            value=value,
            difficulty=difficulty,
            parent_goal_id=parent_goal_id,
            deadline=deadline
        )

        self.goals[goal_id] = goal

        # Update parent
        if parent_goal_id and parent_goal_id in self.goals:
            self.goals[parent_goal_id].subgoal_ids.append(goal_id)
        else:
            # Root goal
            self.root_goals.append(goal_id)

        return goal_id

    def get_goal(self, goal_id: str) -> Optional[Goal]:
        """Retrieve goal"""
        return self.goals.get(goal_id)

    def get_subgoals(self, goal_id: str) -> List[Goal]:
        """Get all subgoals of a goal"""
        goal = self.goals.get(goal_id)
        if not goal:
            return []

        return [self.goals[sid] for sid in goal.subgoal_ids if sid in self.goals]

    def get_ancestors(self, goal_id: str) -> List[Goal]:
        """Get all ancestor goals (parent, grandparent, ...)"""
        ancestors = []
        current = self.goals.get(goal_id)

        while current and current.parent_goal_id:
            parent = self.goals.get(current.parent_goal_id)
            if parent:
                ancestors.append(parent)
                current = parent
            else:
                break

        return ancestors

    def compute_hierarchical_value(self, goal_id: str) -> float:
        """
        Compute total value including subgoals.

        Value propagates up hierarchy.
        """
        goal = self.goals.get(goal_id)
        if not goal:
            return 0.0

        # Own value
        total_value = goal.value

        # Add subgoal values (discounted)
        subgoals = self.get_subgoals(goal_id)
        for subgoal in subgoals:
            total_value += self.compute_hierarchical_value(subgoal.goal_id) * 0.8

        return total_value


class PriorityScheduler:
    """
    Schedules goals based on priority, value, deadline.

    Implements utility-based scheduling.
    """

    def __init__(self):
        self.schedule_history: deque = deque(maxlen=500)

    def compute_urgency(self, goal: Goal) -> float:
        """
        Compute goal urgency (0-1).

        Based on deadline proximity.
        """
        if not goal.deadline:
            return 0.3  # Default moderate urgency

        time_remaining = goal.deadline - time.time()

        if time_remaining <= 0:
            # Past deadline
            return 1.0

        # Urgency increases as deadline approaches
        # Asymptotic approach to 1.0
        urgency = 1.0 - np.exp(-5.0 / (time_remaining / 3600.0 + 1.0))

        return urgency

    def compute_utility(self, goal: Goal) -> float:
        """
        Compute expected utility of pursuing goal.

        Utility = Value * (1 - Difficulty) * (Priority + Urgency)
        """
        urgency = self.compute_urgency(goal)

        # Expected value (discounted by difficulty)
        expected_value = goal.value * (1.0 - goal.difficulty * 0.5)

        # Weighted by priority and urgency
        utility = expected_value * (goal.priority + urgency)

        return utility

    def select_goal(self, active_goals: List[Goal]) -> Optional[Goal]:
        """
        Select highest-utility goal to pursue.

        Returns selected goal or None.
        """
        if not active_goals:
            return None

        # Compute utility for each goal
        utilities = [(goal, self.compute_utility(goal)) for goal in active_goals]

        # Select max utility
        selected_goal, max_utility = max(utilities, key=lambda x: x[1])

        return selected_goal


class ConflictResolver:
    """
    Detects and resolves goal conflicts.

    Based on goal systems theory (Kruglanski et al., 2002).
    """

    def __init__(self):
        self.conflict_history: deque = deque(maxlen=500)

    def detect_conflicts(
        self,
        goal_1: Goal,
        goal_2: Goal,
        resource_constraint: float = 1.0
    ) -> Optional[GoalConflict]:
        """
        Detect if two goals conflict.

        Returns conflict if detected, None otherwise.
        """
        # Type 1: Resource conflict
        # Both goals require more than available resources
        combined_demand = (goal_1.difficulty + goal_2.difficulty)

        if combined_demand > resource_constraint:
            severity = (combined_demand - resource_constraint) / resource_constraint

            conflict = GoalConflict(
                timestamp=time.time(),
                goal_1_id=goal_1.goal_id,
                goal_2_id=goal_2.goal_id,
                conflict_type="resource",
                severity=min(1.0, severity)
            )

            return conflict

        # Type 2: Timing conflict (overlapping deadlines)
        if goal_1.deadline and goal_2.deadline:
            time_overlap = abs(goal_1.deadline - goal_2.deadline)

            if time_overlap < 3600:  # Within 1 hour
                severity = 1.0 - (time_overlap / 3600.0)

                conflict = GoalConflict(
                    timestamp=time.time(),
                    goal_1_id=goal_1.goal_id,
                    goal_2_id=goal_2.goal_id,
                    conflict_type="timing",
                    severity=severity
                )

                return conflict

        return None

    def resolve_conflict(
        self,
        conflict: GoalConflict,
        goal_1: Goal,
        goal_2: Goal
    ) -> Tuple[str, str]:
        """
        Resolve conflict between two goals.

        Returns:
            - resolution_strategy
            - selected_goal_id
        """
        # Strategy 1: Priority-based selection
        if abs(goal_1.priority - goal_2.priority) > 0.3:
            if goal_1.priority > goal_2.priority:
                strategy = "prioritize_high_priority"
                selected = goal_1.goal_id
            else:
                strategy = "prioritize_high_priority"
                selected = goal_2.goal_id

        # Strategy 2: Value-based selection
        elif abs(goal_1.value - goal_2.value) > 0.3:
            if goal_1.value > goal_2.value:
                strategy = "prioritize_high_value"
                selected = goal_1.goal_id
            else:
                strategy = "prioritize_high_value"
                selected = goal_2.goal_id

        # Strategy 3: Deadline-driven (urgency)
        elif goal_1.deadline and goal_2.deadline:
            if goal_1.deadline < goal_2.deadline:
                strategy = "prioritize_urgent"
                selected = goal_1.goal_id
            else:
                strategy = "prioritize_urgent"
                selected = goal_2.goal_id

        else:
            # Default: random or first goal
            strategy = "default_first"
            selected = goal_1.goal_id

        conflict.resolution_strategy = strategy
        self.conflict_history.append(conflict)

        return strategy, selected


class GoalPursuitMonitor:
    """
    Monitors goal pursuit progress.

    Decides when to persist vs disengage.
    """

    def __init__(self):
        self.pursuit_history: deque = deque(maxlen=1000)
        self.disengagement_threshold = 0.3  # Pr(success) below which to quit

    def evaluate_progress(
        self,
        goal: Goal,
        recent_outcomes: List[str]
    ) -> float:
        """
        Evaluate progress toward goal.

        Returns probability of success (0-1).
        """
        # Based on recent outcomes and current progress
        if not recent_outcomes:
            # No history, use difficulty as prior
            return 1.0 - goal.difficulty

        # Count successes
        success_count = sum(1 for o in recent_outcomes if o == "success")
        success_rate = success_count / len(recent_outcomes)

        # Bayesian update: combine prior (difficulty) with observed rate
        prior = 1.0 - goal.difficulty
        likelihood = success_rate

        # Simple weighted average (could be full Bayes)
        posterior = 0.3 * prior + 0.7 * likelihood

        return posterior

    def should_persist(
        self,
        goal: Goal,
        success_probability: float,
        effort_invested: float
    ) -> bool:
        """
        Decide whether to persist or disengage.

        Based on expected value and sunk cost.
        """
        # Expected value of continuing
        expected_value = goal.value * success_probability

        # Consider sunk cost (tendency to persist if invested)
        sunk_cost_bias = effort_invested * 0.2  # Weak effect

        # Persist if expected value + bias > threshold
        persist_score = expected_value + sunk_cost_bias

        return persist_score > self.disengagement_threshold


class GoalManagementSystem:
    """
    Main LAB_022 implementation.

    Manages:
    - Goal hierarchy
    - Goal prioritization
    - Conflict resolution
    - Goal pursuit monitoring
    - Goal activation/deactivation
    """

    def __init__(self):
        # Components
        self.hierarchy = GoalHierarchyManager()
        self.scheduler = PriorityScheduler()
        self.conflict_resolver = ConflictResolver()
        self.pursuit_monitor = GoalPursuitMonitor()

        # Current state
        self.active_goal_id: Optional[str] = None

        # Statistics
        self.total_goals = 0
        self.achieved_goals = 0
        self.abandoned_goals = 0
        self.total_conflicts = 0

    def add_goal(
        self,
        description: str,
        goal_type: GoalType,
        priority: float,
        value: float,
        difficulty: float,
        parent_goal_id: Optional[str] = None,
        deadline: Optional[float] = None
    ) -> str:
        """Add new goal"""
        goal_id = self.hierarchy.add_goal(
            description, goal_type, priority, value,
            difficulty, parent_goal_id, deadline
        )
        self.total_goals += 1
        return goal_id

    def select_goal_to_pursue(self) -> Optional[str]:
        """
        Select next goal to pursue based on utility.

        Returns goal ID.
        """
        # Get all active goals
        active_goals = [
            goal for goal in self.hierarchy.goals.values()
            if goal.status in [GoalStatus.ACTIVE, GoalStatus.INACTIVE]
        ]

        if not active_goals:
            return None

        # Check for conflicts
        if len(active_goals) >= 2:
            for i in range(len(active_goals)):
                for j in range(i + 1, len(active_goals)):
                    conflict = self.conflict_resolver.detect_conflicts(
                        active_goals[i],
                        active_goals[j]
                    )
                    if conflict:
                        self.total_conflicts += 1
                        # Resolve
                        _, selected_id = self.conflict_resolver.resolve_conflict(
                            conflict,
                            active_goals[i],
                            active_goals[j]
                        )
                        return selected_id

        # No conflicts, select by utility
        selected_goal = self.scheduler.select_goal(active_goals)

        return selected_goal.goal_id if selected_goal else None

    def pursue_goal(
        self,
        goal_id: str,
        effort: float,
        outcome: str
    ) -> GoalPursuitEvent:
        """
        Pursue goal with effort, observe outcome.

        Returns pursuit event.
        """
        goal = self.hierarchy.get_goal(goal_id)
        if not goal:
            raise ValueError(f"Goal {goal_id} not found")

        # Update status
        goal.status = GoalStatus.ACTIVE
        goal.last_pursued = time.time()

        # Update progress based on outcome
        if outcome == "success":
            progress_delta = 0.2 * (1.0 - goal.difficulty)  # Harder goals progress slower
        elif outcome == "partial":
            progress_delta = 0.1
        else:
            progress_delta = 0.0

        goal.progress = min(1.0, goal.progress + progress_delta)

        # Check if achieved
        if goal.progress >= 1.0:
            goal.status = GoalStatus.ACHIEVED
            self.achieved_goals += 1

        # Record event
        event = GoalPursuitEvent(
            timestamp=time.time(),
            goal_id=goal_id,
            action_taken="generic_action",
            progress_delta=progress_delta,
            effort_invested=effort,
            outcome=outcome
        )

        return event

    def evaluate_goal_persistence(
        self,
        goal_id: str,
        recent_outcomes: List[str],
        total_effort: float
    ) -> bool:
        """
        Decide whether to continue pursuing goal.

        Returns True to persist, False to abandon.
        """
        goal = self.hierarchy.get_goal(goal_id)
        if not goal:
            return False

        # Evaluate success probability
        success_prob = self.pursuit_monitor.evaluate_progress(goal, recent_outcomes)

        # Decide persistence
        persist = self.pursuit_monitor.should_persist(
            goal,
            success_prob,
            total_effort
        )

        if not persist:
            goal.status = GoalStatus.ABANDONED
            self.abandoned_goals += 1

        return persist

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        return {
            "total_goals": self.total_goals,
            "achieved_goals": self.achieved_goals,
            "abandoned_goals": self.abandoned_goals,
            "achievement_rate": (
                self.achieved_goals / self.total_goals
                if self.total_goals > 0 else 0.0
            ),
            "abandonment_rate": (
                self.abandoned_goals / self.total_goals
                if self.total_goals > 0 else 0.0
            ),
            "total_conflicts": self.total_conflicts,
            "active_goal_id": self.active_goal_id,
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_022: Goal Management - Test")
    print("=" * 60)

    # Create goal management system
    gm = GoalManagementSystem()

    # Add hierarchical goals
    print("\n🎯 Adding hierarchical goals...")
    root_goal = gm.add_goal(
        description="Complete PhD",
        goal_type=GoalType.ABSTRACT,
        priority=0.9,
        value=0.95,
        difficulty=0.8,
        deadline=time.time() + 86400 * 365 * 4  # 4 years
    )
    print(f"  Root Goal: {root_goal} (Complete PhD)")

    subgoal1 = gm.add_goal(
        description="Pass qualifying exam",
        goal_type=GoalType.CONCRETE,
        priority=0.95,
        value=0.7,
        difficulty=0.6,
        parent_goal_id=root_goal,
        deadline=time.time() + 86400 * 30  # 30 days
    )
    print(f"  Subgoal 1: {subgoal1} (Qualifying exam)")

    subgoal2 = gm.add_goal(
        description="Publish 3 papers",
        goal_type=GoalType.CONCRETE,
        priority=0.8,
        value=0.8,
        difficulty=0.7,
        parent_goal_id=root_goal,
        deadline=time.time() + 86400 * 365 * 3  # 3 years
    )
    print(f"  Subgoal 2: {subgoal2} (Publish papers)")

    # Add conflicting goal
    conflict_goal = gm.add_goal(
        description="Learn guitar",
        goal_type=GoalType.CONCRETE,
        priority=0.5,
        value=0.6,
        difficulty=0.5,
        deadline=time.time() + 86400 * 60  # 60 days
    )
    print(f"  Conflicting Goal: {conflict_goal} (Learn guitar)")

    # Select goal to pursue
    print("\n🔍 Selecting goal to pursue...")
    selected = gm.select_goal_to_pursue()
    selected_goal = gm.hierarchy.get_goal(selected)
    if selected_goal:
        print(f"  Selected: {selected_goal.description}")
        print(f"  Priority: {selected_goal.priority:.3f}")
        print(f"  Value: {selected_goal.value:.3f}")

    # Pursue goal with varying outcomes
    print("\n▶️ Pursuing goal (5 attempts)...")
    outcomes = []
    for i in range(5):
        outcome = np.random.choice(
            ["success", "partial", "failure"],
            p=[0.6, 0.3, 0.1]
        )
        event = gm.pursue_goal(selected, effort=0.2, outcome=outcome)
        outcomes.append(outcome)
        print(f"  Attempt {i+1}: {outcome} → Progress {selected_goal.progress:.2f}")

    # Evaluate persistence
    print("\n🤔 Evaluating persistence...")
    persist = gm.evaluate_goal_persistence(selected, outcomes, total_effort=1.0)
    print(f"  Persist: {persist}")
    print(f"  Goal Status: {selected_goal.status.value}")

    # Show final statistics
    print("\n📈 Final Statistics:")
    stats = gm.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

    print("\n✅ LAB_022 Test Complete!")
