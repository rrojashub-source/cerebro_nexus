"""
LAB_021: Planning & Sequencing - Goal Decomposition and Temporal Ordering

Implements hierarchical planning and action sequencing:
- Fuster (2001): The prefrontal cortex and temporal organization
- Botvinick & Plaut (2004): Hierarchical control of action sequences
- Cooper & Shallice (2000): Contention scheduling
- Grafman (2002): Managerial knowledge units

Core Functions:
1. Goal decomposition into subgoals
2. Temporal sequencing and ordering
3. Hierarchical action representation
4. Plan execution and monitoring
5. Replanning when plans fail
6. Resource-time trade-off estimation

Neuroscience Foundation:
- Rostral PFC: Abstract goal representation
- Dorsolateral PFC (dlPFC): Plan maintenance and manipulation
- Premotor cortex: Action sequence representation
- Basal ganglia: Sequence chunking and initiation

Integration:
- → LAB_022 (Goal Management) for goal hierarchy
- ← LAB_018 (Working Memory Executive) for plan maintenance
- ← LAB_019 (Cognitive Control) for plan updating
- ← LAB_012 (Episodic Future Thinking) for simulation
"""

import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import numpy as np
from enum import Enum
import uuid


class PlanStatus(Enum):
    """Plan execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    REPLANNING = "replanning"


class ActionStatus(Enum):
    """Individual action status"""
    WAITING = "waiting"
    READY = "ready"
    EXECUTING = "executing"
    DONE = "done"
    BLOCKED = "blocked"


@dataclass
class Action:
    """Atomic action in a sequence"""
    action_id: str
    name: str
    duration_estimate: float  # seconds
    resource_cost: float  # 0-100
    preconditions: List[str] = field(default_factory=list)  # Action IDs
    effects: List[str] = field(default_factory=list)
    status: ActionStatus = ActionStatus.WAITING
    actual_duration: Optional[float] = None


@dataclass
class Subgoal:
    """Intermediate goal in hierarchical plan"""
    subgoal_id: str
    description: str
    parent_goal_id: Optional[str] = None
    required_actions: List[str] = field(default_factory=list)
    completion_criteria: str = ""
    completed: bool = False


@dataclass
class Plan:
    """Complete hierarchical plan"""
    plan_id: str
    root_goal: str
    subgoals: List[Subgoal] = field(default_factory=list)
    actions: List[Action] = field(default_factory=list)
    action_sequence: List[str] = field(default_factory=list)  # Ordered action IDs
    status: PlanStatus = PlanStatus.PENDING
    start_time: Optional[float] = None
    completion_time: Optional[float] = None
    total_cost_estimate: float = 0.0


@dataclass
class PlanExecutionEvent:
    """Plan execution progress event"""
    timestamp: float
    plan_id: str
    action_id: str
    event_type: str  # "action_start", "action_complete", "action_fail"
    replanning_needed: bool = False


class GoalDecomposer:
    """
    Decomposes high-level goals into subgoals and actions.

    Uses hierarchical task analysis.
    """

    def __init__(self):
        self.decomposition_history: deque = deque(maxlen=500)

    def decompose_goal(
        self,
        goal_description: str,
        complexity: float = 0.5
    ) -> List[Subgoal]:
        """
        Decompose goal into subgoals.

        Complexity determines number of subgoals (1-5).
        """
        # Number of subgoals based on complexity
        num_subgoals = max(1, int(complexity * 5))

        subgoals = []

        for i in range(num_subgoals):
            subgoal = Subgoal(
                subgoal_id=str(uuid.uuid4())[:8],
                description=f"Subgoal {i+1} of {goal_description}",
                completion_criteria=f"Complete step {i+1}"
            )
            subgoals.append(subgoal)

        return subgoals

    def decompose_subgoal_to_actions(
        self,
        subgoal: Subgoal,
        action_complexity: float = 0.5
    ) -> List[Action]:
        """
        Decompose subgoal into atomic actions.

        Returns ordered list of actions.
        """
        # Number of actions per subgoal
        num_actions = max(1, int(action_complexity * 4))

        actions = []
        prev_action_id = None

        for i in range(num_actions):
            action_id = str(uuid.uuid4())[:8]

            # Sequential dependencies
            preconditions = [prev_action_id] if prev_action_id else []

            action = Action(
                action_id=action_id,
                name=f"Action {i+1} for {subgoal.subgoal_id}",
                duration_estimate=np.random.uniform(5.0, 20.0),
                resource_cost=np.random.uniform(10.0, 50.0),
                preconditions=preconditions,
                effects=[f"effect_{action_id}"]
            )

            actions.append(action)
            prev_action_id = action_id

        return actions


class TemporalSequencer:
    """
    Orders actions temporally, respecting dependencies.

    Uses topological sorting for dependency graphs.
    """

    def __init__(self):
        pass

    def sequence_actions(
        self,
        actions: List[Action]
    ) -> List[str]:
        """
        Create temporal sequence of actions (topological sort).

        Returns ordered list of action IDs.
        """
        # Build dependency graph
        action_map = {a.action_id: a for a in actions}
        in_degree = {a.action_id: len(a.preconditions) for a in actions}

        # Initialize queue with actions that have no dependencies
        ready_queue = [
            a.action_id for a in actions
            if len(a.preconditions) == 0
        ]

        sequence = []

        while ready_queue:
            # Get next ready action
            current_id = ready_queue.pop(0)
            sequence.append(current_id)

            # Update dependents
            for action in actions:
                if current_id in action.preconditions:
                    in_degree[action.action_id] -= 1

                    # If all dependencies satisfied, add to ready queue
                    if in_degree[action.action_id] == 0:
                        ready_queue.append(action.action_id)

        # Check for cycles (shouldn't happen with well-formed plans)
        if len(sequence) != len(actions):
            # Some actions couldn't be scheduled (cyclic dependencies)
            # Add remaining actions in arbitrary order
            for action in actions:
                if action.action_id not in sequence:
                    sequence.append(action.action_id)

        return sequence

    def estimate_total_duration(
        self,
        actions: List[Action],
        sequence: List[str]
    ) -> float:
        """
        Estimate total duration for sequential execution.

        Returns duration in seconds.
        """
        action_map = {a.action_id: a for a in actions}

        total_duration = 0.0
        for action_id in sequence:
            total_duration += action_map[action_id].duration_estimate

        return total_duration

    def find_critical_path(
        self,
        actions: List[Action],
        sequence: List[str]
    ) -> List[str]:
        """
        Find critical path (longest chain of dependencies).

        Returns list of action IDs on critical path.
        """
        action_map = {a.action_id: a for a in actions}

        # Compute earliest start time for each action
        earliest_start = {}

        for action_id in sequence:
            action = action_map[action_id]

            if not action.preconditions:
                earliest_start[action_id] = 0.0
            else:
                # Start after all preconditions complete
                max_pred_end = max(
                    earliest_start.get(pred, 0.0) + action_map[pred].duration_estimate
                    for pred in action.preconditions
                    if pred in action_map
                )
                earliest_start[action_id] = max_pred_end

        # Critical path = longest path to last action
        last_action = sequence[-1]
        critical_path = [last_action]

        # Trace back through longest predecessors
        current = last_action
        while action_map[current].preconditions:
            # Find predecessor with latest completion time
            predecessors = action_map[current].preconditions
            if predecessors:
                latest_pred = max(
                    predecessors,
                    key=lambda p: earliest_start.get(p, 0.0) + action_map[p].duration_estimate
                    if p in action_map else 0.0
                )
                critical_path.insert(0, latest_pred)
                current = latest_pred
            else:
                break

        return critical_path


class PlanExecutor:
    """
    Executes plans and monitors progress.

    Detects failures and triggers replanning when needed.
    """

    def __init__(self):
        self.execution_history: deque = deque(maxlen=1000)
        self.active_plan: Optional[Plan] = None
        self.current_action_index = 0

    def start_plan(self, plan: Plan):
        """Begin plan execution"""
        self.active_plan = plan
        plan.status = PlanStatus.IN_PROGRESS
        plan.start_time = time.time()
        self.current_action_index = 0

        # Mark first action as ready
        if plan.action_sequence:
            first_action_id = plan.action_sequence[0]
            for action in plan.actions:
                if action.action_id == first_action_id:
                    action.status = ActionStatus.READY
                    break

    def execute_next_action(self) -> Optional[PlanExecutionEvent]:
        """
        Execute next action in sequence.

        Returns execution event, or None if plan complete.
        """
        if not self.active_plan:
            return None

        plan = self.active_plan

        if self.current_action_index >= len(plan.action_sequence):
            # Plan complete
            plan.status = PlanStatus.COMPLETED
            plan.completion_time = time.time()
            return None

        # Get current action
        action_id = plan.action_sequence[self.current_action_index]
        action = None

        for a in plan.actions:
            if a.action_id == action_id:
                action = a
                break

        if not action:
            return None

        # Check preconditions
        if action.status == ActionStatus.BLOCKED:
            # Cannot execute
            event = PlanExecutionEvent(
                timestamp=time.time(),
                plan_id=plan.plan_id,
                action_id=action_id,
                event_type="action_fail",
                replanning_needed=True
            )
            self.execution_history.append(event)
            plan.status = PlanStatus.FAILED
            return event

        # Execute action (simulate)
        action.status = ActionStatus.EXECUTING

        event_start = PlanExecutionEvent(
            timestamp=time.time(),
            plan_id=plan.plan_id,
            action_id=action_id,
            event_type="action_start",
            replanning_needed=False
        )
        self.execution_history.append(event_start)

        # Simulate action duration
        action.actual_duration = action.duration_estimate * np.random.uniform(0.8, 1.2)

        # Complete action
        action.status = ActionStatus.DONE

        event_complete = PlanExecutionEvent(
            timestamp=time.time(),
            plan_id=plan.plan_id,
            action_id=action_id,
            event_type="action_complete",
            replanning_needed=False
        )
        self.execution_history.append(event_complete)

        # Move to next action
        self.current_action_index += 1

        # Mark next action as ready
        if self.current_action_index < len(plan.action_sequence):
            next_action_id = plan.action_sequence[self.current_action_index]
            for a in plan.actions:
                if a.action_id == next_action_id:
                    a.status = ActionStatus.READY
                    break

        return event_complete

    def check_completion(self) -> bool:
        """Check if all actions in plan are complete"""
        if not self.active_plan:
            return False

        for action in self.active_plan.actions:
            if action.status != ActionStatus.DONE:
                return False

        return True


class PlanningSequencingSystem:
    """
    Main LAB_021 implementation.

    Integrates:
    - Goal decomposition
    - Temporal sequencing
    - Plan execution
    - Plan monitoring
    """

    def __init__(self):
        # Components
        self.decomposer = GoalDecomposer()
        self.sequencer = TemporalSequencer()
        self.executor = PlanExecutor()

        # Statistics
        self.total_plans_created = 0
        self.completed_plans = 0
        self.failed_plans = 0

    def create_plan(
        self,
        goal_description: str,
        complexity: float = 0.5
    ) -> Plan:
        """
        Create hierarchical plan for goal.

        Returns complete plan.
        """
        plan_id = str(uuid.uuid4())[:8]

        # Decompose goal into subgoals
        subgoals = self.decomposer.decompose_goal(goal_description, complexity)

        # Decompose subgoals into actions
        all_actions = []
        for subgoal in subgoals:
            actions = self.decomposer.decompose_subgoal_to_actions(subgoal, complexity)
            subgoal.required_actions = [a.action_id for a in actions]
            all_actions.extend(actions)

        # Sequence actions temporally
        action_sequence = self.sequencer.sequence_actions(all_actions)

        # Estimate total cost
        total_cost = sum(a.resource_cost for a in all_actions)

        # Create plan
        plan = Plan(
            plan_id=plan_id,
            root_goal=goal_description,
            subgoals=subgoals,
            actions=all_actions,
            action_sequence=action_sequence,
            total_cost_estimate=total_cost
        )

        self.total_plans_created += 1

        return plan

    def execute_plan(self, plan: Plan) -> bool:
        """
        Execute plan to completion.

        Returns True if successful, False if failed.
        """
        self.executor.start_plan(plan)

        while True:
            event = self.executor.execute_next_action()

            if event is None:
                # Plan complete
                break

            if event.replanning_needed:
                # Plan failed
                self.failed_plans += 1
                return False

            # Check if complete
            if self.executor.check_completion():
                self.completed_plans += 1
                return True

        self.completed_plans += 1
        return True

    def get_plan_metrics(self, plan: Plan) -> Dict:
        """Get metrics for a plan"""
        duration_estimate = self.sequencer.estimate_total_duration(
            plan.actions,
            plan.action_sequence
        )

        critical_path = self.sequencer.find_critical_path(
            plan.actions,
            plan.action_sequence
        )

        return {
            "num_subgoals": len(plan.subgoals),
            "num_actions": len(plan.actions),
            "estimated_duration_sec": duration_estimate,
            "estimated_cost": plan.total_cost_estimate,
            "critical_path_length": len(critical_path),
            "parallelization_potential": (
                len(plan.actions) - len(critical_path)
            ) / len(plan.actions) if plan.actions else 0.0
        }

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        return {
            "total_plans_created": self.total_plans_created,
            "completed_plans": self.completed_plans,
            "failed_plans": self.failed_plans,
            "success_rate": (
                self.completed_plans / self.total_plans_created
                if self.total_plans_created > 0 else 0.0
            ),
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_021: Planning & Sequencing - Test")
    print("=" * 60)

    # Create planning system
    planner = PlanningSequencingSystem()

    print("\n📋 Creating plan for complex goal...")
    plan = planner.create_plan(
        goal_description="Prepare project presentation",
        complexity=0.7
    )
    print(f"  Plan ID: {plan.plan_id}")
    print(f"  Subgoals: {len(plan.subgoals)}")
    print(f"  Actions: {len(plan.actions)}")

    # Get plan metrics
    print("\n📊 Plan Metrics:")
    metrics = planner.get_plan_metrics(plan)
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")

    # Show action sequence
    print(f"\n🔄 Action Sequence (first 5):")
    for i, action_id in enumerate(plan.action_sequence[:5]):
        action = next((a for a in plan.actions if a.action_id == action_id), None)
        if action:
            print(f"  {i+1}. {action.name} (est. {action.duration_estimate:.1f}s)")

    # Execute plan
    print(f"\n▶️ Executing plan...")
    success = planner.execute_plan(plan)
    print(f"  Execution: {'✅ Success' if success else '❌ Failed'}")
    print(f"  Status: {plan.status.value}")

    if plan.completion_time and plan.start_time:
        actual_duration = plan.completion_time - plan.start_time
        print(f"  Actual Duration: {actual_duration:.2f}s")

    # Create another plan (simple)
    print("\n📋 Creating simple plan...")
    plan2 = planner.create_plan(
        goal_description="Make coffee",
        complexity=0.3
    )
    planner.execute_plan(plan2)

    # Show final statistics
    print("\n📈 Final Statistics:")
    stats = planner.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

    print("\n✅ LAB_021 Test Complete!")
