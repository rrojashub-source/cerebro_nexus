"""
LAB_020: Task Switching - Context Switching and Reconfiguration

Implements task-set reconfiguration and switching costs:
- Monsell (2003): Task switching and executive control
- Rogers & Monsell (1995): Costs of a predictable switch
- Meiran (1996): Reconfiguration of processing mode
- Kiesel et al. (2010): Control and interference in task switching

Core Functions:
1. Task-set activation and deactivation
2. Switch cost computation (RT penalty)
3. Mixing cost (maintaining multiple task sets)
4. Backward inhibition (n-2 repetition cost)
5. Task-set inertia management
6. Preparation effects (CSI - cue-stimulus interval)

Neuroscience Foundation:
- Lateral PFC: Task-set representation
- Parietal cortex: Task-set activation
- Pre-SMA: Task-set reconfiguration
- Basal ganglia: Task-set selection and gating

Integration:
- ← LAB_019 (Cognitive Control) for shifting
- ← LAB_018 (Working Memory Executive) for task maintenance
- → LAB_022 (Goal Management) for task goals
- ← LAB_016 (Acetylcholine) for task-set focus
"""

import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import numpy as np
from enum import Enum


class SwitchType(Enum):
    """Type of task switch"""
    REPEAT = "repeat"          # Same task as previous
    SWITCH = "switch"          # Different task from previous
    N2_REPEAT = "n2_repeat"    # Same as n-2 (backward inhibition)


@dataclass
class TaskSet:
    """Representation of a task set"""
    task_id: str
    task_name: str
    activation_level: float = 0.0
    rules: Dict[str, str] = field(default_factory=dict)
    stimulus_response_mappings: Dict[str, str] = field(default_factory=dict)
    last_executed: Optional[float] = None


@dataclass
class SwitchEvent:
    """Task switch event record"""
    timestamp: float
    from_task: str
    to_task: str
    switch_type: SwitchType
    switch_cost: float  # ms
    mixing_cost: float  # ms
    preparation_time: float  # CSI
    residual_activation_interference: float


@dataclass
class ReconfigurationProcess:
    """Task-set reconfiguration event"""
    timestamp: float
    task_id: str
    reconfiguration_time: float  # ms
    components_reconfigured: List[str]
    completion_percentage: float


class TaskSetManager:
    """
    Manages activation and representation of task sets.

    Based on parallel distributed processing (PDP) models of task switching.
    """

    def __init__(self, max_active_sets: int = 3):
        self.max_active_sets = max_active_sets
        self.task_sets: Dict[str, TaskSet] = {}
        self.activation_decay_rate = 0.1  # per second

    def register_task_set(
        self,
        task_id: str,
        task_name: str,
        rules: Dict[str, str],
        sr_mappings: Dict[str, str]
    ):
        """Register new task set"""
        self.task_sets[task_id] = TaskSet(
            task_id=task_id,
            task_name=task_name,
            activation_level=0.0,
            rules=rules,
            stimulus_response_mappings=sr_mappings
        )

    def activate_task_set(self, task_id: str, activation: float = 1.0):
        """Activate a task set"""
        if task_id in self.task_sets:
            self.task_sets[task_id].activation_level = min(1.0, activation)
            self.task_sets[task_id].last_executed = time.time()

    def deactivate_task_set(self, task_id: str, amount: float = 0.5):
        """Deactivate (inhibit) a task set"""
        if task_id in self.task_sets:
            self.task_sets[task_id].activation_level *= (1.0 - amount)

    def decay_activations(self):
        """Natural decay of all task-set activations"""
        current_time = time.time()

        for task_set in self.task_sets.values():
            if task_set.last_executed:
                elapsed = current_time - task_set.last_executed
                decay = self.activation_decay_rate * elapsed

                task_set.activation_level = max(
                    0.0,
                    task_set.activation_level - decay
                )

    def get_activation(self, task_id: str) -> float:
        """Get current activation with decay applied"""
        self.decay_activations()

        if task_id in self.task_sets:
            return self.task_sets[task_id].activation_level
        return 0.0

    def get_active_tasks(self) -> List[str]:
        """Get list of currently active tasks (activation > 0.1)"""
        self.decay_activations()

        active = [
            task_id for task_id, task_set in self.task_sets.items()
            if task_set.activation_level > 0.1
        ]

        return active


class SwitchCostCalculator:
    """
    Computes switch costs and mixing costs.

    Based on:
    - Rogers & Monsell (1995): Asymmetric switch costs
    - Rubin & Meiran (2005): On the origins of switch cost
    """

    def __init__(self, baseline_switch_cost: float = 150.0):
        self.baseline_switch_cost = baseline_switch_cost  # ms

    def compute_switch_cost(
        self,
        prev_task_activation: float,
        new_task_activation: float,
        preparation_time: float,
        is_n2_repeat: bool = False
    ) -> Tuple[float, float]:
        """
        Compute switch cost and mixing cost.

        Returns:
            - switch_cost (ms)
            - mixing_cost (ms)
        """
        # Switch cost components:
        # 1. Task-set inertia (prev task still active)
        inertia_cost = prev_task_activation * 200.0

        # 2. Reconfiguration demand (new task not prepared)
        reconfiguration_cost = (1.0 - new_task_activation) * 250.0

        # 3. Preparation benefit (CSI effect)
        preparation_benefit = min(preparation_time * 100.0, 150.0)

        # Total switch cost
        switch_cost = max(
            0.0,
            self.baseline_switch_cost + inertia_cost + reconfiguration_cost - preparation_benefit
        )

        # Backward inhibition (n-2 repetition cost)
        if is_n2_repeat:
            # Returning to recently inhibited task → extra cost
            switch_cost += 80.0

        # Mixing cost (maintaining multiple task sets)
        # Even on repeat trials in mixed blocks
        active_task_sets = 2  # Assume dual-task context
        mixing_cost = (active_task_sets - 1) * 50.0

        return switch_cost, mixing_cost

    def compute_asymmetric_cost(
        self,
        task_a_difficulty: float,
        task_b_difficulty: float,
        direction: str  # "A_to_B" or "B_to_A"
    ) -> float:
        """
        Compute asymmetric switch cost.

        Switching from easy to hard: small cost
        Switching from hard to easy: large cost (residual interference)
        """
        if direction == "A_to_B":
            # A → B
            if task_b_difficulty > task_a_difficulty:
                # Easy → Hard: small additional cost
                return 20.0
            else:
                # Hard → Easy: large additional cost
                return 80.0
        else:
            # B → A
            if task_a_difficulty > task_b_difficulty:
                return 20.0
            else:
                return 80.0


class BackwardInhibitionTracker:
    """
    Tracks task history for backward inhibition (n-2 repetition cost).

    When switching A → B → A, returning to A incurs extra cost
    because A was recently inhibited.
    """

    def __init__(self):
        self.task_history: deque = deque(maxlen=10)

    def add_task(self, task_id: str):
        """Record executed task"""
        self.task_history.append({
            "task_id": task_id,
            "timestamp": time.time()
        })

    def is_n2_repeat(self, current_task: str) -> bool:
        """Check if current task matches n-2 (backward inhibition)"""
        if len(self.task_history) < 2:
            return False

        n2_task = self.task_history[-2]["task_id"]

        return current_task == n2_task

    def get_recent_tasks(self, n: int = 3) -> List[str]:
        """Get last n tasks"""
        recent = list(self.task_history)[-n:]
        return [entry["task_id"] for entry in recent]


class ReconfigurationEngine:
    """
    Implements task-set reconfiguration process.

    Reconfiguration involves:
    - Activating new stimulus-response mappings
    - Inhibiting old mappings
    - Loading new task rules
    - Adjusting attention weights
    """

    def __init__(self, base_reconfig_time: float = 200.0):
        self.base_reconfig_time = base_reconfig_time  # ms
        self.reconfiguration_history: deque = deque(maxlen=500)

    def reconfigure(
        self,
        task_id: str,
        current_activation: float,
        preparation_time: float
    ) -> ReconfigurationProcess:
        """
        Execute task-set reconfiguration.

        Returns reconfiguration process event.
        """
        # Reconfiguration time depends on:
        # 1. Current activation (higher = faster)
        # 2. Preparation time (more prep = less online reconfig)

        activation_benefit = current_activation * 100.0  # ms saved
        preparation_benefit = preparation_time * 50.0  # ms saved

        reconfig_time = max(
            50.0,  # Minimum
            self.base_reconfig_time - activation_benefit - preparation_benefit
        )

        # Components to reconfigure
        components = [
            "stimulus_response_mappings",
            "task_rules",
            "attention_weights",
            "response_criteria"
        ]

        # Completion percentage (can be partial if insufficient time)
        if preparation_time > 0.3:
            completion = 1.0  # Full preparation
        else:
            completion = min(1.0, preparation_time / 0.3)

        process = ReconfigurationProcess(
            timestamp=time.time(),
            task_id=task_id,
            reconfiguration_time=reconfig_time,
            components_reconfigured=components,
            completion_percentage=completion
        )

        self.reconfiguration_history.append(process)

        return process


class TaskSwitchingSystem:
    """
    Main LAB_020 implementation.

    Manages task switching including:
    - Task-set activation/deactivation
    - Switch cost computation
    - Mixing cost tracking
    - Backward inhibition
    - Reconfiguration processes
    - Preparation effects (CSI)
    """

    def __init__(self):
        # Components
        self.task_manager = TaskSetManager()
        self.switch_calculator = SwitchCostCalculator()
        self.backward_inhibition = BackwardInhibitionTracker()
        self.reconfig_engine = ReconfigurationEngine()

        # History
        self.switch_history: deque = deque(maxlen=1000)

        # Statistics
        self.total_switches = 0
        self.total_repeats = 0
        self.n2_repeats = 0
        self.avg_switch_cost = 0.0
        self.avg_mixing_cost = 0.0

    def register_task(
        self,
        task_id: str,
        task_name: str,
        rules: Dict[str, str],
        sr_mappings: Dict[str, str]
    ):
        """Register new task set"""
        self.task_manager.register_task_set(task_id, task_name, rules, sr_mappings)

    def execute_task(
        self,
        task_id: str,
        preparation_time: float = 0.0
    ) -> Tuple[SwitchType, SwitchEvent]:
        """
        Execute task (with potential switch).

        Returns:
            - switch_type
            - switch_event
        """
        # Get recent task history
        recent = self.backward_inhibition.get_recent_tasks(n=2)

        # Determine switch type
        if not recent:
            switch_type = SwitchType.REPEAT  # First task
            prev_task = None
        else:
            prev_task = recent[-1]

            if task_id == prev_task:
                switch_type = SwitchType.REPEAT
                self.total_repeats += 1
            else:
                # Check for n-2 repetition (backward inhibition)
                if self.backward_inhibition.is_n2_repeat(task_id):
                    switch_type = SwitchType.N2_REPEAT
                    self.n2_repeats += 1
                else:
                    switch_type = SwitchType.SWITCH

                self.total_switches += 1

        # Get activations
        prev_activation = 0.0
        if prev_task:
            prev_activation = self.task_manager.get_activation(prev_task)

        new_activation = self.task_manager.get_activation(task_id)

        # Compute costs
        switch_cost, mixing_cost = self.switch_calculator.compute_switch_cost(
            prev_activation,
            new_activation,
            preparation_time,
            is_n2_repeat=(switch_type == SwitchType.N2_REPEAT)
        )

        # For repeats, switch cost = 0
        if switch_type == SwitchType.REPEAT:
            switch_cost = 0.0

        # Execute reconfiguration
        reconfig = self.reconfig_engine.reconfigure(
            task_id,
            new_activation,
            preparation_time
        )

        # Update activations
        # Activate new task
        self.task_manager.activate_task_set(task_id, activation=1.0)

        # Deactivate previous task (inhibition)
        if prev_task and prev_task != task_id:
            self.task_manager.deactivate_task_set(prev_task, amount=0.6)

        # Record task execution
        self.backward_inhibition.add_task(task_id)

        # Residual activation interference
        residual_interference = prev_activation if prev_task else 0.0

        # Create switch event
        event = SwitchEvent(
            timestamp=time.time(),
            from_task=prev_task if prev_task else "none",
            to_task=task_id,
            switch_type=switch_type,
            switch_cost=switch_cost,
            mixing_cost=mixing_cost,
            preparation_time=preparation_time,
            residual_activation_interference=residual_interference
        )

        self.switch_history.append(event)

        # Update running averages
        self._update_statistics(switch_cost, mixing_cost)

        return switch_type, event

    def _update_statistics(self, switch_cost: float, mixing_cost: float):
        """Update running statistics"""
        total_events = len(self.switch_history)

        if total_events > 0:
            self.avg_switch_cost = (
                (self.avg_switch_cost * (total_events - 1) + switch_cost) /
                total_events
            )

            self.avg_mixing_cost = (
                (self.avg_mixing_cost * (total_events - 1) + mixing_cost) /
                total_events
            )

    def get_statistics(self) -> Dict:
        """Get comprehensive system statistics"""
        return {
            "total_switches": self.total_switches,
            "total_repeats": self.total_repeats,
            "n2_repeats": self.n2_repeats,
            "switch_rate": (
                self.total_switches / (self.total_switches + self.total_repeats)
                if (self.total_switches + self.total_repeats) > 0 else 0.0
            ),
            "avg_switch_cost_ms": self.avg_switch_cost,
            "avg_mixing_cost_ms": self.avg_mixing_cost,
            "active_task_sets": len(self.task_manager.get_active_tasks()),
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_020: Task Switching - Test")
    print("=" * 60)

    # Create task switching system
    switcher = TaskSwitchingSystem()

    # Register tasks
    print("\n📝 Registering tasks...")
    switcher.register_task(
        task_id="task_A",
        task_name="Letter Classification",
        rules={"type": "categorize_letters"},
        sr_mappings={"vowel": "left", "consonant": "right"}
    )
    switcher.register_task(
        task_id="task_B",
        task_name="Number Classification",
        rules={"type": "categorize_numbers"},
        sr_mappings={"odd": "left", "even": "right"}
    )
    print("  Registered: task_A (Letter), task_B (Number)")

    # Scenario 1: First task (no switch)
    print("\n1️⃣ Execute task_A (first trial)...")
    switch_type, event = switcher.execute_task("task_A", preparation_time=0.5)
    print(f"  Switch Type: {switch_type.value}")
    print(f"  Switch Cost: {event.switch_cost:.0f}ms")
    print(f"  Mixing Cost: {event.mixing_cost:.0f}ms")

    # Scenario 2: Repeat same task (no switch cost)
    print("\n2️⃣ Execute task_A again (repeat)...")
    switch_type, event = switcher.execute_task("task_A", preparation_time=0.5)
    print(f"  Switch Type: {switch_type.value}")
    print(f"  Switch Cost: {event.switch_cost:.0f}ms (should be ~0)")

    # Scenario 3: Switch to different task
    print("\n3️⃣ Execute task_B (switch)...")
    switch_type, event = switcher.execute_task("task_B", preparation_time=0.1)
    print(f"  Switch Type: {switch_type.value}")
    print(f"  Switch Cost: {event.switch_cost:.0f}ms (penalty)")
    print(f"  Residual Interference: {event.residual_activation_interference:.3f}")

    # Scenario 4: Switch back to A (n-2 repetition / backward inhibition)
    print("\n4️⃣ Execute task_A again (n-2 repeat / backward inhibition)...")
    switch_type, event = switcher.execute_task("task_A", preparation_time=0.1)
    print(f"  Switch Type: {switch_type.value}")
    print(f"  Switch Cost: {event.switch_cost:.0f}ms (extra penalty)")

    # Scenario 5: Effect of preparation time
    print("\n5️⃣ Testing preparation effect...")
    print("  Switch with minimal prep (50ms):")
    _, event1 = switcher.execute_task("task_B", preparation_time=0.05)
    print(f"    Cost: {event1.switch_cost:.0f}ms")

    print("  Switch with good prep (800ms):")
    _, event2 = switcher.execute_task("task_A", preparation_time=0.8)
    print(f"    Cost: {event2.switch_cost:.0f}ms (reduced)")

    # Show final statistics
    print("\n📈 Final Statistics:")
    stats = switcher.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

    print("\n✅ LAB_020 Test Complete!")
