"""
LAB_019: Cognitive Control - Inhibition, Shifting, and Updating

Implements Miyake's three core executive functions:
- Miyake et al. (2000): Unity and diversity of executive functions
- Diamond (2013): Executive functions taxonomy
- Miller & Cohen (2001): Integrative theory of PFC function
- Braver et al. (2007): Proactive vs reactive control

Core Functions:
1. Response inhibition (Stroop, Go/No-Go)
2. Cognitive flexibility/shifting (task set switching)
3. Working memory updating (monitoring and replacing)
4. Conflict monitoring and resolution
5. Proactive vs reactive control modes

Neuroscience Foundation:
- Dorsolateral PFC (dlPFC): Updating and maintenance
- Ventrolateral PFC (vlPFC): Inhibition
- Anterior cingulate cortex (ACC): Conflict monitoring
- Presupplementary motor area (pre-SMA): Response inhibition

Integration:
- ← LAB_018 (Working Memory Executive) for resource allocation
- → LAB_020 (Task Switching) for context changes
- ← LAB_017 (GABA/Glutamate) for inhibitory control
- → LAB_022 (Goal Management) for goal-directed behavior
"""

import time
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import numpy as np
from enum import Enum


class ControlMode(Enum):
    """Cognitive control mode"""
    PROACTIVE = "proactive"    # Anticipatory, goal-driven
    REACTIVE = "reactive"      # Stimulus-driven, corrective


class InhibitionType(Enum):
    """Types of inhibition"""
    RESPONSE = "response"              # Motor response suppression
    COGNITIVE = "cognitive"            # Thought suppression
    INTERFERENCE = "interference"      # Distractor filtering


@dataclass
class InhibitionEvent:
    """Record of inhibitory control"""
    timestamp: float
    inhibition_type: InhibitionType
    target_strength: float  # Prepotent response strength
    inhibition_strength: float
    success: bool  # Whether inhibition succeeded
    reaction_time: float


@dataclass
class ShiftingEvent:
    """Cognitive shifting/flexibility event"""
    timestamp: float
    from_task: str
    to_task: str
    switch_cost: float  # RT penalty
    reconfiguration_time: float
    success: bool


@dataclass
class UpdatingEvent:
    """Working memory updating event"""
    timestamp: float
    old_item: str
    new_item: str
    relevance_threshold: float
    update_latency: float


@dataclass
class ConflictSignal:
    """Conflict monitoring event"""
    timestamp: float
    conflict_type: str
    conflict_magnitude: float
    resolution_strategy: str
    resolution_time: float


class InhibitionController:
    """
    Implements response inhibition mechanisms.

    Based on:
    - Logan & Cowan (1984): On the ability to inhibit thought and action
    - Aron et al. (2007): Stop-signal task and inhibition
    """

    def __init__(self, baseline_inhibition: float = 0.7):
        self.baseline_inhibition = baseline_inhibition
        self.inhibition_history: deque = deque(maxlen=500)

        # Inhibitory control strength (trainable)
        self.inhibition_strength = baseline_inhibition

        # Stop-signal reaction time (SSRT) - measure of inhibitory speed
        self.ssrt = 250.0  # ms

    def attempt_inhibition(
        self,
        prepotent_response_strength: float,
        inhibition_type: InhibitionType,
        stimulus_onset_time: float
    ) -> Tuple[bool, InhibitionEvent]:
        """
        Attempt to inhibit a prepotent (automatic) response.

        Returns:
            - success (whether inhibition succeeded)
            - event record
        """
        # Time to initiate inhibition
        inhibition_onset = stimulus_onset_time + (self.ssrt / 1000.0)

        # Current time
        current_time = time.time()

        # Check if inhibition can occur in time
        time_available = current_time - stimulus_onset_time

        # Inhibition success depends on:
        # 1. Inhibitory strength vs response strength
        # 2. Whether enough time to inhibit

        effective_inhibition = self.inhibition_strength

        # Race model: inhibition vs response execution
        response_threshold_time = prepotent_response_strength * 0.5  # seconds

        if time_available < response_threshold_time:
            # Enough time to inhibit
            if effective_inhibition > prepotent_response_strength:
                success = True
            else:
                # Probabilistic based on ratio
                success_prob = effective_inhibition / (prepotent_response_strength + 0.1)
                success = np.random.random() < success_prob
        else:
            # Response already executed
            success = False

        # Reaction time (if successful)
        rt = inhibition_onset if success else time_available

        # Create event
        event = InhibitionEvent(
            timestamp=time.time(),
            inhibition_type=inhibition_type,
            target_strength=prepotent_response_strength,
            inhibition_strength=effective_inhibition,
            success=success,
            reaction_time=rt
        )

        self.inhibition_history.append(event)

        # Update inhibition strength based on success (learning)
        if success:
            self.inhibition_strength = min(1.0, self.inhibition_strength + 0.01)
        else:
            self.inhibition_strength = max(0.3, self.inhibition_strength - 0.01)

        return success, event

    def get_inhibitory_control_score(self) -> float:
        """
        Get current inhibitory control effectiveness (0-1).

        Based on recent success rate.
        """
        if not self.inhibition_history:
            return self.baseline_inhibition

        recent = list(self.inhibition_history)[-20:]
        success_count = sum(1 for e in recent if e.success)

        return success_count / len(recent)


class CognitiveShifter:
    """
    Implements cognitive flexibility and task-set switching.

    Based on:
    - Monsell (2003): Task switching
    - Rogers & Monsell (1995): Switch cost
    """

    def __init__(self, baseline_switch_cost: float = 200.0):
        self.baseline_switch_cost = baseline_switch_cost  # ms
        self.shifting_history: deque = deque(maxlen=500)

        self.current_task_set: Optional[str] = None
        self.task_set_activation: Dict[str, float] = {}

    def switch_task_set(
        self,
        from_task: str,
        to_task: str,
        preparation_time: float = 0.0
    ) -> Tuple[float, ShiftingEvent]:
        """
        Switch from one task set to another.

        Returns:
            - switch_cost (ms)
            - event record
        """
        # Switch cost depends on:
        # 1. Task set inertia (old task still active)
        # 2. Preparation time (can reduce cost)

        # Get activation of old and new task sets
        old_activation = self.task_set_activation.get(from_task, 0.5)
        new_activation = self.task_set_activation.get(to_task, 0.1)

        # Switch cost = baseline + inertia - preparation benefit
        inertia_cost = old_activation * 150.0  # ms
        preparation_benefit = preparation_time * 100.0  # ms

        switch_cost = max(
            50.0,  # Minimum cost
            self.baseline_switch_cost + inertia_cost - preparation_benefit
        )

        # Reconfiguration time (time to activate new task set)
        reconfiguration = (1.0 - new_activation) * 300.0  # ms

        # Total time
        total_time = switch_cost + reconfiguration

        # Update task set activations
        # Old task decays
        self.task_set_activation[from_task] = old_activation * 0.5

        # New task activates
        self.task_set_activation[to_task] = min(1.0, new_activation + 0.4)

        # Update current
        self.current_task_set = to_task

        # Success determined by whether new task set activates sufficiently
        success = self.task_set_activation[to_task] > 0.6

        # Create event
        event = ShiftingEvent(
            timestamp=time.time(),
            from_task=from_task,
            to_task=to_task,
            switch_cost=switch_cost,
            reconfiguration_time=reconfiguration,
            success=success
        )

        self.shifting_history.append(event)

        return switch_cost, event

    def get_cognitive_flexibility(self) -> float:
        """
        Get current cognitive flexibility (0-1).

        Lower switch costs = higher flexibility.
        """
        if not self.shifting_history:
            return 0.5

        recent = list(self.shifting_history)[-10:]
        avg_switch_cost = np.mean([e.switch_cost for e in recent])

        # Map switch cost (50-500ms) to flexibility (1-0)
        flexibility = 1.0 - ((avg_switch_cost - 50.0) / 450.0)
        flexibility = max(0.0, min(1.0, flexibility))

        return flexibility


class WorkingMemoryUpdater:
    """
    Implements working memory updating mechanisms.

    Based on:
    - Morris & Jones (1990): Working memory updating
    - Ecker et al. (2010): Working memory updating
    """

    def __init__(self, relevance_threshold: float = 0.6):
        self.relevance_threshold = relevance_threshold
        self.updating_history: deque = deque(maxlen=500)

        self.current_contents: Dict[str, Any] = {}
        self.update_speed = 1.0  # Multiplier

    def should_update(
        self,
        new_item_relevance: float,
        current_load: float
    ) -> bool:
        """
        Determine if working memory should be updated with new information.

        Depends on:
        - Relevance of new information
        - Current working memory load
        """
        # Higher load → higher threshold (harder to update)
        adjusted_threshold = self.relevance_threshold + (current_load * 0.2)

        return new_item_relevance >= adjusted_threshold

    def update_item(
        self,
        item_id: str,
        old_item: Any,
        new_item: Any,
        new_relevance: float
    ) -> UpdatingEvent:
        """
        Update working memory contents.

        Returns event record.
        """
        # Update latency depends on update speed
        latency = (1.0 / self.update_speed) * 200.0  # ms

        # Perform update
        self.current_contents[item_id] = new_item

        # Create event
        event = UpdatingEvent(
            timestamp=time.time(),
            old_item=str(old_item),
            new_item=str(new_item),
            relevance_threshold=self.relevance_threshold,
            update_latency=latency
        )

        self.updating_history.append(event)

        # Improve update speed with practice
        self.update_speed = min(2.0, self.update_speed + 0.01)

        return event

    def get_updating_efficiency(self) -> float:
        """
        Get working memory updating efficiency (0-1).

        Based on update speed.
        """
        return min(1.0, self.update_speed / 2.0)


class ConflictMonitor:
    """
    Monitors and resolves cognitive conflicts.

    Based on:
    - Botvinick et al. (2001): Conflict monitoring and ACC
    - Carter & van Veen (2007): ACC and conflict detection
    """

    def __init__(self, conflict_threshold: float = 0.5):
        self.conflict_threshold = conflict_threshold
        self.conflict_history: deque = deque(maxlen=500)

        self.control_adjustment = 0.5  # How much to adjust control after conflict

    def detect_conflict(
        self,
        response_option_1: float,
        response_option_2: float
    ) -> Tuple[bool, float]:
        """
        Detect response conflict.

        Conflict occurs when multiple responses are similarly activated.

        Returns:
            - is_conflict
            - conflict_magnitude (0-1)
        """
        # Conflict = similarity of competing responses
        conflict = min(response_option_1, response_option_2)

        is_conflict = conflict >= self.conflict_threshold

        return is_conflict, conflict

    def resolve_conflict(
        self,
        conflict_magnitude: float,
        conflict_type: str,
        control_mode: ControlMode
    ) -> ConflictSignal:
        """
        Resolve detected conflict.

        Returns conflict signal for control adjustment.
        """
        # Resolution strategy depends on control mode
        if control_mode == ControlMode.PROACTIVE:
            # Proactive: Increase sustained control
            strategy = "sustained_control_boost"
            resolution_time = 100.0  # Fast, prepared
        else:
            # Reactive: Post-conflict adjustment
            strategy = "reactive_adjustment"
            resolution_time = 200.0 + (conflict_magnitude * 100.0)  # Slower

        # Create conflict signal
        signal = ConflictSignal(
            timestamp=time.time(),
            conflict_type=conflict_type,
            conflict_magnitude=conflict_magnitude,
            resolution_strategy=strategy,
            resolution_time=resolution_time
        )

        self.conflict_history.append(signal)

        # Adjust control based on conflict history
        self._adjust_control()

        return signal

    def _adjust_control(self):
        """Adjust control parameters based on recent conflict"""
        if len(self.conflict_history) < 5:
            return

        recent = list(self.conflict_history)[-5:]
        avg_conflict = np.mean([s.conflict_magnitude for s in recent])

        # High recent conflict → increase control
        if avg_conflict > 0.7:
            self.conflict_threshold = max(0.3, self.conflict_threshold - 0.05)
        else:
            # Low conflict → can relax control
            self.conflict_threshold = min(0.8, self.conflict_threshold + 0.02)

    def get_conflict_rate(self) -> float:
        """Get recent conflict detection rate"""
        if not self.conflict_history:
            return 0.0

        recent = list(self.conflict_history)[-20:]
        return len(recent) / 20.0


class CognitiveControlSystem:
    """
    Main LAB_019 implementation.

    Integrates three core executive functions:
    1. Inhibition
    2. Shifting
    3. Updating

    Plus conflict monitoring and control mode regulation.
    """

    def __init__(
        self,
        control_mode: ControlMode = ControlMode.REACTIVE
    ):
        # Core parameters
        self.control_mode = control_mode

        # Components
        self.inhibition_controller = InhibitionController()
        self.cognitive_shifter = CognitiveShifter()
        self.wm_updater = WorkingMemoryUpdater()
        self.conflict_monitor = ConflictMonitor()

        # Statistics
        self.total_inhibitions = 0
        self.successful_inhibitions = 0
        self.total_shifts = 0
        self.total_updates = 0
        self.total_conflicts = 0

    def inhibit_response(
        self,
        prepotent_strength: float,
        inhibition_type: InhibitionType,
        onset_time: float
    ) -> Tuple[bool, InhibitionEvent]:
        """Execute inhibitory control"""
        self.total_inhibitions += 1

        success, event = self.inhibition_controller.attempt_inhibition(
            prepotent_strength,
            inhibition_type,
            onset_time
        )

        if success:
            self.successful_inhibitions += 1

        return success, event

    def shift_task(
        self,
        from_task: str,
        to_task: str,
        prep_time: float = 0.0
    ) -> Tuple[float, ShiftingEvent]:
        """Execute cognitive shift"""
        self.total_shifts += 1

        return self.cognitive_shifter.switch_task_set(from_task, to_task, prep_time)

    def update_working_memory(
        self,
        item_id: str,
        old_item: Any,
        new_item: Any,
        relevance: float,
        current_load: float
    ) -> Optional[UpdatingEvent]:
        """Update working memory if appropriate"""
        if self.wm_updater.should_update(relevance, current_load):
            self.total_updates += 1
            return self.wm_updater.update_item(item_id, old_item, new_item, relevance)
        return None

    def monitor_conflict(
        self,
        option1_activation: float,
        option2_activation: float,
        conflict_type: str
    ) -> Optional[ConflictSignal]:
        """Monitor and resolve conflict"""
        is_conflict, magnitude = self.conflict_monitor.detect_conflict(
            option1_activation,
            option2_activation
        )

        if is_conflict:
            self.total_conflicts += 1
            return self.conflict_monitor.resolve_conflict(
                magnitude,
                conflict_type,
                self.control_mode
            )

        return None

    def set_control_mode(self, mode: ControlMode):
        """Switch between proactive and reactive control"""
        self.control_mode = mode

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        return {
            "control_mode": self.control_mode.value,
            "inhibitory_control_score": self.inhibition_controller.get_inhibitory_control_score(),
            "cognitive_flexibility": self.cognitive_shifter.get_cognitive_flexibility(),
            "updating_efficiency": self.wm_updater.get_updating_efficiency(),
            "conflict_rate": self.conflict_monitor.get_conflict_rate(),
            "total_inhibitions": self.total_inhibitions,
            "successful_inhibitions": self.successful_inhibitions,
            "inhibition_success_rate": (
                self.successful_inhibitions / self.total_inhibitions
                if self.total_inhibitions > 0 else 0.0
            ),
            "total_shifts": self.total_shifts,
            "total_updates": self.total_updates,
            "total_conflicts": self.total_conflicts,
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_019: Cognitive Control - Test")
    print("=" * 60)

    # Create cognitive control system
    control = CognitiveControlSystem(control_mode=ControlMode.REACTIVE)

    print("\n📊 Initial State:")
    stats = control.get_statistics()
    print(f"  Control Mode: {stats['control_mode']}")
    print(f"  Inhibitory Control: {stats['inhibitory_control_score']:.3f}")
    print(f"  Cognitive Flexibility: {stats['cognitive_flexibility']:.3f}")

    # Scenario 1: Response inhibition (Stroop-like)
    print("\n🛑 Testing response inhibition...")
    onset = time.time()
    success, event = control.inhibit_response(
        prepotent_strength=0.8,
        inhibition_type=InhibitionType.RESPONSE,
        onset_time=onset
    )
    print(f"  Prepotent Response: 0.800")
    print(f"  Inhibition Strength: {event.inhibition_strength:.3f}")
    print(f"  Success: {success}")
    print(f"  Reaction Time: {event.reaction_time*1000:.0f}ms")

    # Scenario 2: Task shifting
    print("\n🔄 Testing task shifting...")
    switch_cost, shift_event = control.shift_task(
        from_task="Task_A",
        to_task="Task_B",
        prep_time=0.2
    )
    print(f"  Switch Cost: {switch_cost:.0f}ms")
    print(f"  Reconfiguration: {shift_event.reconfiguration_time:.0f}ms")
    print(f"  Success: {shift_event.success}")

    # Scenario 3: Working memory updating
    print("\n📝 Testing WM updating...")
    update_event = control.update_working_memory(
        item_id="item_1",
        old_item="Old Information",
        new_item="New Relevant Information",
        relevance=0.9,
        current_load=0.3
    )
    if update_event:
        print(f"  Updated: {update_event.old_item} → {update_event.new_item}")
        print(f"  Latency: {update_event.update_latency:.0f}ms")

    # Scenario 4: Conflict monitoring
    print("\n⚠️ Testing conflict monitoring...")
    conflict_signal = control.monitor_conflict(
        option1_activation=0.7,
        option2_activation=0.6,
        conflict_type="response_competition"
    )
    if conflict_signal:
        print(f"  Conflict Detected: {conflict_signal.conflict_magnitude:.3f}")
        print(f"  Resolution Strategy: {conflict_signal.resolution_strategy}")
        print(f"  Resolution Time: {conflict_signal.resolution_time:.0f}ms")

    # Scenario 5: Multiple inhibitions (learning)
    print("\n🎯 Testing inhibitory learning (10 trials)...")
    for i in range(10):
        onset = time.time()
        success, _ = control.inhibit_response(
            prepotent_strength=0.7,
            inhibition_type=InhibitionType.COGNITIVE,
            onset_time=onset
        )
    stats = control.get_statistics()
    print(f"  Final Inhibition Success Rate: {stats['inhibition_success_rate']:.3f}")
    print(f"  Inhibitory Control Score: {stats['inhibitory_control_score']:.3f}")

    # Show final statistics
    print("\n📈 Final Statistics:")
    stats = control.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

    print("\n✅ LAB_019 Test Complete!")
