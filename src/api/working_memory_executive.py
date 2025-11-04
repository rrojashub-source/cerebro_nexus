"""
LAB_018: Working Memory Executive - Central Executive System

Implements Baddeley's central executive based on:
- Baddeley & Hitch (1974): Working memory model
- Baddeley (2000): Episodic buffer and central executive
- Miyake et al. (2000): Unity and diversity of executive functions
- Cowan (2001): Magical number 4 in working memory

Core Functions:
1. Dual-task coordination and resource allocation
2. Integration with phonological loop (LAB_011) and visuospatial sketchpad
3. Attention control and focus switching
4. Interference resolution
5. Executive load monitoring
6. Goal maintenance during distraction

Neuroscience Foundation:
- Dorsolateral PFC (dlPFC): Executive control, manipulation
- Ventrolateral PFC (vlPFC): Maintenance and retrieval
- Anterior cingulate cortex (ACC): Conflict monitoring
- Parietal cortex: Attention and storage

Integration:
- ← LAB_011 (Working Memory Buffer) for storage
- ← LAB_010 (Attention Mechanism) for selective attention
- → LAB_019 (Cognitive Control) for inhibition/updating
- ← LAB_016 (Acetylcholine) for sustained attention
"""

import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import numpy as np
from enum import Enum
import uuid


class ExecutiveMode(Enum):
    """Current executive operating mode"""
    IDLE = "idle"                    # No active tasks
    SINGLE_TASK = "single_task"      # Single task focus
    DUAL_TASK = "dual_task"          # Managing two tasks
    OVERLOADED = "overloaded"        # Exceeding capacity


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class CognitiveResource:
    """Available cognitive resources"""
    total_capacity: float = 100.0
    available: float = 100.0
    allocated: Dict[str, float] = field(default_factory=dict)


@dataclass
class ExecutiveTask:
    """Task managed by central executive"""
    task_id: str
    task_type: str
    priority: TaskPriority
    resource_demand: float  # 0-100
    start_time: float
    deadline: Optional[float] = None
    goal_representation: Optional[str] = None
    subgoals: List[str] = field(default_factory=list)
    completed: bool = False


@dataclass
class DualTaskPerformance:
    """Dual-task interference metrics"""
    timestamp: float
    task1_performance: float
    task2_performance: float
    interference_cost: float
    resource_conflict: float


@dataclass
class ExecutiveSignal:
    """Executive control event"""
    timestamp: float
    event_type: str
    task_id: str
    resource_allocation: float
    load_level: float


class ResourceAllocator:
    """
    Manages allocation of limited cognitive resources across tasks.

    Based on capacity theory (Kahneman, 1973):
    - Fixed total capacity
    - Tasks compete for resources
    - High priority tasks get preferential allocation
    """

    def __init__(self, total_capacity: float = 100.0):
        self.resources = CognitiveResource(total_capacity=total_capacity)
        self.allocation_history: deque = deque(maxlen=500)

    def allocate(
        self,
        task_id: str,
        demand: float,
        priority: TaskPriority
    ) -> Tuple[float, bool]:
        """
        Attempt to allocate resources to a task.

        Returns:
            - Amount allocated
            - Whether allocation was successful
        """
        # Priority modulates allocation
        priority_multiplier = priority.value / 4.0  # 0.25 to 1.0

        # Requested amount with priority boost
        requested = demand * priority_multiplier

        # Check availability
        if requested <= self.resources.available:
            # Full allocation
            self.resources.allocated[task_id] = requested
            self.resources.available -= requested

            self.allocation_history.append({
                "timestamp": time.time(),
                "task_id": task_id,
                "allocated": requested,
                "success": True
            })

            return requested, True
        else:
            # Partial allocation (give what's available)
            available = self.resources.available
            if available > 0:
                self.resources.allocated[task_id] = available
                self.resources.available = 0

                self.allocation_history.append({
                    "timestamp": time.time(),
                    "task_id": task_id,
                    "allocated": available,
                    "success": False
                })

                return available, False
            else:
                # No resources available
                return 0.0, False

    def release(self, task_id: str) -> float:
        """Release resources from a task"""
        if task_id in self.resources.allocated:
            allocated = self.resources.allocated[task_id]
            self.resources.available += allocated
            del self.resources.allocated[task_id]

            # Cap at total capacity
            self.resources.available = min(
                self.resources.available,
                self.resources.total_capacity
            )

            return allocated
        return 0.0

    def get_load(self) -> float:
        """Get current cognitive load (0-1)"""
        used = self.resources.total_capacity - self.resources.available
        load = used / self.resources.total_capacity
        return load

    def rebalance(self, active_tasks: List[ExecutiveTask]):
        """
        Rebalance resources based on current task priorities.
        Called when priorities change or new tasks arrive.
        """
        # Release all current allocations
        total_demand = sum(self.resources.allocated.values())
        self.resources.available = self.resources.total_capacity
        self.resources.allocated.clear()

        # Sort tasks by priority
        sorted_tasks = sorted(active_tasks, key=lambda t: t.priority.value, reverse=True)

        # Reallocate in priority order
        for task in sorted_tasks:
            self.allocate(task.task_id, task.resource_demand, task.priority)


class DualTaskCoordinator:
    """
    Manages dual-task performance and interference.

    Based on:
    - Wickens (2002): Multiple resource theory
    - Pashler (1994): Dual-task interference
    """

    def __init__(self):
        self.performance_history: deque = deque(maxlen=500)

    def compute_interference(
        self,
        task1_demand: float,
        task2_demand: float,
        resource_overlap: float = 0.7
    ) -> float:
        """
        Compute dual-task interference.

        Higher overlap → more interference
        Higher demands → more interference
        """
        # Total demand
        total_demand = task1_demand + task2_demand

        # Interference increases with overlap
        interference = (total_demand * resource_overlap) / 100.0

        # Nonlinear increase (capacity limit)
        if total_demand > 100:
            # Exceeding capacity → severe interference
            interference *= (total_demand / 100.0) ** 2

        return min(1.0, interference)

    def compute_performance_decrement(
        self,
        single_task_performance: float,
        interference: float
    ) -> Tuple[float, float]:
        """
        Compute performance decrement due to dual-task interference.

        Returns performance for task1 and task2.
        """
        # Both tasks suffer from interference
        # Task 1 (primary) suffers less
        task1_perf = single_task_performance * (1.0 - interference * 0.6)

        # Task 2 (secondary) suffers more
        task2_perf = single_task_performance * (1.0 - interference * 0.9)

        return task1_perf, task2_perf

    def record_performance(
        self,
        task1_perf: float,
        task2_perf: float,
        interference: float,
        resource_conflict: float
    ):
        """Record dual-task performance"""
        perf = DualTaskPerformance(
            timestamp=time.time(),
            task1_performance=task1_perf,
            task2_performance=task2_perf,
            interference_cost=interference,
            resource_conflict=resource_conflict
        )
        self.performance_history.append(perf)


class GoalMaintainer:
    """
    Maintains goal representations in working memory.

    Prevents goal loss during distraction (O'Reilly & Frank, 2006).
    """

    def __init__(self, maintenance_capacity: int = 3):
        self.maintenance_capacity = maintenance_capacity
        self.active_goals: Dict[str, Dict[str, Any]] = {}

    def maintain_goal(
        self,
        task_id: str,
        goal_representation: str,
        importance: float
    ):
        """Add goal to maintenance buffer"""
        if len(self.active_goals) >= self.maintenance_capacity:
            # Evict lowest importance goal
            min_importance_task = min(
                self.active_goals.items(),
                key=lambda x: x[1]["importance"]
            )[0]

            if importance > self.active_goals[min_importance_task]["importance"]:
                del self.active_goals[min_importance_task]
            else:
                return  # Can't add new goal

        self.active_goals[task_id] = {
            "goal": goal_representation,
            "importance": importance,
            "start_time": time.time()
        }

    def retrieve_goal(self, task_id: str) -> Optional[str]:
        """Retrieve maintained goal"""
        if task_id in self.active_goals:
            return self.active_goals[task_id]["goal"]
        return None

    def release_goal(self, task_id: str):
        """Remove goal from maintenance"""
        if task_id in self.active_goals:
            del self.active_goals[task_id]

    def get_maintenance_load(self) -> float:
        """Get current goal maintenance load (0-1)"""
        return len(self.active_goals) / self.maintenance_capacity


class WorkingMemoryExecutive:
    """
    Main LAB_018 implementation.

    Central executive system that:
    - Coordinates multiple tasks
    - Allocates cognitive resources
    - Maintains goals during interference
    - Monitors and resolves conflicts
    - Integrates with other WM components
    """

    def __init__(
        self,
        total_capacity: float = 100.0,
        overload_threshold: float = 0.85
    ):
        # Core parameters
        self.total_capacity = total_capacity
        self.overload_threshold = overload_threshold

        # Current state
        self.current_mode = ExecutiveMode.IDLE
        self.active_tasks: Dict[str, ExecutiveTask] = {}
        self.current_load = 0.0

        # Components
        self.resource_allocator = ResourceAllocator(total_capacity)
        self.dual_task_coordinator = DualTaskCoordinator()
        self.goal_maintainer = GoalMaintainer(maintenance_capacity=3)

        # History
        self.signal_history: deque = deque(maxlen=1000)

        # Statistics
        self.total_tasks = 0
        self.completed_tasks = 0
        self.failed_tasks = 0
        self.overload_events = 0

    def add_task(
        self,
        task_type: str,
        priority: TaskPriority,
        resource_demand: float,
        goal_representation: Optional[str] = None,
        deadline: Optional[float] = None
    ) -> Tuple[str, bool]:
        """
        Add new task to executive control.

        Returns:
            - task_id
            - success (whether resources could be allocated)
        """
        task_id = str(uuid.uuid4())[:8]

        # Create task
        task = ExecutiveTask(
            task_id=task_id,
            task_type=task_type,
            priority=priority,
            resource_demand=resource_demand,
            start_time=time.time(),
            deadline=deadline,
            goal_representation=goal_representation
        )

        # Attempt resource allocation
        allocated, success = self.resource_allocator.allocate(
            task_id,
            resource_demand,
            priority
        )

        if success:
            self.active_tasks[task_id] = task
            self.total_tasks += 1

            # Maintain goal if provided
            if goal_representation:
                importance = priority.value / 4.0
                self.goal_maintainer.maintain_goal(task_id, goal_representation, importance)

            # Update mode
            self._update_mode()

            # Create signal
            signal = ExecutiveSignal(
                timestamp=time.time(),
                event_type="task_added",
                task_id=task_id,
                resource_allocation=allocated,
                load_level=self.resource_allocator.get_load()
            )
            self.signal_history.append(signal)

            return task_id, True
        else:
            # Allocation failed
            self.failed_tasks += 1
            return task_id, False

    def complete_task(self, task_id: str):
        """Mark task as complete and release resources"""
        if task_id not in self.active_tasks:
            return

        task = self.active_tasks[task_id]
        task.completed = True

        # Release resources
        self.resource_allocator.release(task_id)

        # Release goal
        self.goal_maintainer.release_goal(task_id)

        # Remove from active
        del self.active_tasks[task_id]

        self.completed_tasks += 1

        # Update mode
        self._update_mode()

        # Create signal
        signal = ExecutiveSignal(
            timestamp=time.time(),
            event_type="task_completed",
            task_id=task_id,
            resource_allocation=0.0,
            load_level=self.resource_allocator.get_load()
        )
        self.signal_history.append(signal)

    def _update_mode(self):
        """Update executive mode based on current state"""
        active_count = len(self.active_tasks)
        load = self.resource_allocator.get_load()

        if active_count == 0:
            self.current_mode = ExecutiveMode.IDLE
        elif active_count == 1:
            self.current_mode = ExecutiveMode.SINGLE_TASK
        elif active_count == 2:
            self.current_mode = ExecutiveMode.DUAL_TASK
        else:
            self.current_mode = ExecutiveMode.DUAL_TASK

        # Check overload
        if load >= self.overload_threshold:
            self.current_mode = ExecutiveMode.OVERLOADED
            self.overload_events += 1

        self.current_load = load

    def simulate_dual_task_performance(
        self,
        baseline_performance: float = 0.9
    ) -> Optional[DualTaskPerformance]:
        """
        Simulate performance under current dual-task load.
        """
        if len(self.active_tasks) < 2:
            return None

        tasks = list(self.active_tasks.values())
        task1 = tasks[0]
        task2 = tasks[1]

        # Compute interference
        interference = self.dual_task_coordinator.compute_interference(
            task1.resource_demand,
            task2.resource_demand,
            resource_overlap=0.7
        )

        # Compute performance decrements
        task1_perf, task2_perf = self.dual_task_coordinator.compute_performance_decrement(
            baseline_performance,
            interference
        )

        # Resource conflict (both want same resources)
        conflict = min(task1.resource_demand, task2.resource_demand) / 100.0

        # Record
        self.dual_task_coordinator.record_performance(
            task1_perf,
            task2_perf,
            interference,
            conflict
        )

        return DualTaskPerformance(
            timestamp=time.time(),
            task1_performance=task1_perf,
            task2_performance=task2_perf,
            interference_cost=interference,
            resource_conflict=conflict
        )

    def get_executive_capacity(self) -> float:
        """Get remaining executive capacity (0-1)"""
        return self.resource_allocator.resources.available / self.total_capacity

    def get_statistics(self) -> Dict:
        """Get comprehensive system statistics"""
        return {
            "current_mode": self.current_mode.value,
            "current_load": self.current_load,
            "active_tasks": len(self.active_tasks),
            "executive_capacity_remaining": self.get_executive_capacity(),
            "total_tasks": self.total_tasks,
            "completed_tasks": self.completed_tasks,
            "failed_tasks": self.failed_tasks,
            "success_rate": (
                self.completed_tasks / self.total_tasks
                if self.total_tasks > 0 else 0.0
            ),
            "overload_events": self.overload_events,
            "goal_maintenance_load": self.goal_maintainer.get_maintenance_load(),
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_018: Working Memory Executive - Test")
    print("=" * 60)

    # Create executive system
    executive = WorkingMemoryExecutive(
        total_capacity=100.0,
        overload_threshold=0.85
    )

    print("\n📊 Initial State:")
    stats = executive.get_statistics()
    print(f"  Mode: {stats['current_mode']}")
    print(f"  Load: {stats['current_load']:.3f}")
    print(f"  Capacity: {stats['executive_capacity_remaining']:.3f}")

    # Scenario 1: Add single task
    print("\n📝 Adding single task...")
    task1_id, success = executive.add_task(
        task_type="memory_retrieval",
        priority=TaskPriority.HIGH,
        resource_demand=30.0,
        goal_representation="Retrieve quarterly sales data"
    )
    print(f"  Task ID: {task1_id}")
    print(f"  Success: {success}")
    print(f"  Mode: {executive.current_mode.value}")
    print(f"  Load: {executive.current_load:.3f}")

    # Scenario 2: Add second task (dual-task)
    print("\n📝 Adding second task (dual-task)...")
    task2_id, success = executive.add_task(
        task_type="mental_arithmetic",
        priority=TaskPriority.MEDIUM,
        resource_demand=40.0,
        goal_representation="Calculate project budget"
    )
    print(f"  Task ID: {task2_id}")
    print(f"  Mode: {executive.current_mode.value}")
    print(f"  Load: {executive.current_load:.3f}")

    # Scenario 3: Dual-task performance
    print("\n⚡ Dual-task performance analysis...")
    perf = executive.simulate_dual_task_performance()
    if perf:
        print(f"  Task 1 Performance: {perf.task1_performance:.3f}")
        print(f"  Task 2 Performance: {perf.task2_performance:.3f}")
        print(f"  Interference Cost: {perf.interference_cost:.3f}")
        print(f"  Resource Conflict: {perf.resource_conflict:.3f}")

    # Scenario 4: Complete task
    print("\n✅ Completing task 1...")
    executive.complete_task(task1_id)
    print(f"  Mode: {executive.current_mode.value}")
    print(f"  Load: {executive.current_load:.3f}")
    print(f"  Capacity restored: {executive.get_executive_capacity():.3f}")

    # Scenario 5: Overload
    print("\n⚠️ Testing overload scenario...")
    executive.add_task("task3", TaskPriority.HIGH, 35.0)
    executive.add_task("task4", TaskPriority.HIGH, 30.0)
    print(f"  Mode: {executive.current_mode.value}")
    print(f"  Load: {executive.current_load:.3f}")

    # Show final statistics
    print("\n📈 Final Statistics:")
    stats = executive.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

    print("\n✅ LAB_018 Test Complete!")
