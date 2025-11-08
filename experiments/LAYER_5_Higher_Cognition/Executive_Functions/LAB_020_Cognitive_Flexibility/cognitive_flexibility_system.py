"""
LAB_020: Cognitive Flexibility System

Core Executive Function: Task switching and mental set shifting

Biological Inspiration:
- Dorsolateral prefrontal cortex (dlPFC) - Task set maintenance
- Anterior cingulate cortex (ACC) - Conflict detection
- Posterior parietal cortex - Attentional shifting

Core Functions:
- Task switching (mental set reconfiguration)
- Switch cost computation
- Perseveration detection
- Dopamine/ACh modulation

Key Papers:
- Monsell (2003) - "Task switching"
- Kehagia et al. (2010) - "Neuropsychopharmacology of cognitive flexibility"
"""

from typing import Dict, List, Tuple, Optional
import math


class CognitiveFlexibilitySystem:
    """
    LAB_020: Cognitive Flexibility System - Task switching

    Biological inspiration: dlPFC, ACC, posterior parietal

    Parameters:
    -----------
    baseline_flexibility : float
        Baseline switch capability (default: 0.5)
    switch_cost_base : float
        Base switch cost in milliseconds (default: 150.0)
    reconfiguration_speed : float
        Speed of mental set reconfiguration (default: 0.8)
    rule_encoding_strength : float
        Strength of rule learning (default: 0.7)
    adaptation_rate : float
        Learning rate for flexibility improvement (default: 0.15)
    history_window : int
        Size of task history buffer (default: 20)
    """

    def __init__(
        self,
        baseline_flexibility: float = 0.5,
        switch_cost_base: float = 150.0,
        reconfiguration_speed: float = 0.8,
        rule_encoding_strength: float = 0.7,
        adaptation_rate: float = 0.15,
        history_window: int = 20
    ):
        # Configuration
        self.baseline_flexibility = baseline_flexibility
        self.switch_cost_base = switch_cost_base
        self.reconfiguration_speed = reconfiguration_speed
        self.rule_encoding_strength = rule_encoding_strength
        self.adaptation_rate = adaptation_rate
        self.history_window = history_window

        # State
        self.current_flexibility: float = baseline_flexibility
        self.current_task_set: Optional[str] = None
        self.task_set_history: List[str] = []
        self.switch_count: int = 0
        self.successful_switches: int = 0
        self.total_switch_cost: float = 0.0

    def switch_task_set(self, new_task: str, preparation_time: float) -> Tuple[bool, float]:
        """
        Attempt to switch to new task set

        Parameters:
        -----------
        new_task : str
            New task identifier to switch to
        preparation_time : float
            Preparation time available (milliseconds)

        Returns:
        --------
        success : bool
            True if switch successful
        switch_cost : float
            Switch cost incurred (milliseconds)
        """
        # First task establishes baseline (no cost)
        if self.current_task_set is None:
            self.current_task_set = new_task
            self.task_set_history.append(new_task)
            return True, 0.0

        # Repeat same task (no switch, no cost)
        if new_task == self.current_task_set:
            self.task_set_history.append(new_task)
            if len(self.task_set_history) > self.history_window:
                self.task_set_history.pop(0)
            return True, 0.0

        # Actual task switch
        self.switch_count += 1

        # Compute preparedness from preparation time
        # 500ms preparation = 0.5 preparedness (linear for simplicity)
        preparedness = min(1.0, preparation_time / 1000.0)

        # Compute switch cost
        cost = self.compute_switch_cost(preparedness=preparedness)

        # Assume switch successful (in real brain, can fail with low flexibility)
        # For now, always successful
        success = True
        self.successful_switches += 1

        # Update state
        self.current_task_set = new_task
        self.task_set_history.append(new_task)
        if len(self.task_set_history) > self.history_window:
            self.task_set_history.pop(0)

        self.total_switch_cost += cost

        return success, cost

    def compute_switch_cost(self, preparedness: float) -> float:
        """
        Compute switch cost in milliseconds

        Switch cost formula (Monsell 2003):
        Cost = base_cost * (1.0 - preparedness * flexibility)

        Parameters:
        -----------
        preparedness : float
            How prepared for switch (0-1)

        Returns:
        --------
        switch_cost_ms : float
            Switch cost (milliseconds)
        """
        # Reduction factor from preparedness and flexibility
        reduction = preparedness * self.current_flexibility

        # Cost decreases with better preparedness and flexibility
        cost = self.switch_cost_base * (1.0 - reduction * 0.8)

        # Ensure non-negative
        cost = max(0.0, cost)

        return cost

    def update_flexibility(self, switch_frequency: float, success_rate: float) -> float:
        """
        Update flexibility based on practice and performance

        Parameters:
        -----------
        switch_frequency : float
            Frequency of switching (0-1, 1=always switching)
        success_rate : float
            Success rate of switches (0-1)

        Returns:
        --------
        new_flexibility : float
            Updated flexibility level
        """
        # Practice effect: high frequency + high success = improvement
        practice_effect = switch_frequency * success_rate

        # Target flexibility based on practice
        # Good practice (0.8*0.9=0.72) → target ~0.7
        # Poor practice (0.3*0.5=0.15) → target ~0.3
        target_flexibility = self.baseline_flexibility + (practice_effect - 0.5) * 0.4

        # Gradual adaptation toward target
        self.current_flexibility = (
            self.current_flexibility * (1.0 - self.adaptation_rate) +
            target_flexibility * self.adaptation_rate
        )

        # Clamp to [0, 1]
        self.current_flexibility = max(0.0, min(1.0, self.current_flexibility))

        return self.current_flexibility

    def integrate_dopamine(self, dopamine_level: float) -> float:
        """
        Modulate flexibility by dopamine level (inverted-U curve)

        Optimal dopamine (~0.6) = maximal flexibility
        Too low = rigid
        Too high = distractible

        Parameters:
        -----------
        dopamine_level : float
            Current dopamine level (0-1) from LAB_013

        Returns:
        --------
        modulated_flexibility : float
            Dopamine-modulated flexibility (0-1)
        """
        # Inverted-U curve: optimal at ~0.6
        optimal_da = 0.6

        # Distance from optimal
        distance = abs(dopamine_level - optimal_da)

        # Modulation factor: 1.0 at optimal, decreases with distance
        # Using Gaussian-like curve
        modulation_factor = math.exp(-3.0 * (distance ** 2))

        # Modulate current flexibility
        # At optimal DA: full flexibility
        # At extreme DA: reduced flexibility
        modulated_flexibility = self.current_flexibility * (0.5 + modulation_factor * 0.5)

        # Clamp to [0, 1]
        modulated_flexibility = max(0.0, min(1.0, modulated_flexibility))

        return modulated_flexibility

    def integrate_acetylcholine(self, ach_level: float) -> float:
        """
        Modulate rule encoding by acetylcholine level

        High ACh = faster rule learning and encoding
        Low ACh = slower encoding

        Parameters:
        -----------
        ach_level : float
            Current acetylcholine level (0-1) from LAB_016

        Returns:
        --------
        encoding_boost : float
            Acetylcholine-modulated encoding strength
        """
        # ACh directly modulates encoding strength
        # High ACh (0.8+) = strong boost
        # Low ACh (<0.3) = weak encoding

        # Linear modulation for simplicity
        # ach=0 → 0.5x encoding
        # ach=1 → 1.5x encoding
        modulation_factor = 0.5 + ach_level * 1.0

        encoding_boost = self.rule_encoding_strength * modulation_factor

        return encoding_boost

    def detect_perseveration(self) -> bool:
        """
        Detect perseveration (stuck in same task set)

        Perseveration = repeating same task despite signal to switch
        Indicator of poor cognitive flexibility

        Returns:
        --------
        perseverating : bool
            True if stuck in same task set
        """
        if len(self.task_set_history) < self.history_window // 2:
            return False

        # Check if recent history is dominated by single task (>80%)
        recent_history = self.task_set_history[-self.history_window:]
        if len(recent_history) == 0:
            return False

        # Count most frequent task
        from collections import Counter
        task_counts = Counter(recent_history)
        most_common_task, count = task_counts.most_common(1)[0]

        # If >80% of recent history is same task = perseveration
        perseveration_threshold = 0.8
        if count / len(recent_history) > perseveration_threshold:
            return True

        return False

    def process_event(self, new_task: str, preparation_time: float) -> Dict:
        """
        Main processing: switch task, compute metrics

        Parameters:
        -----------
        new_task : str
            New task to switch to
        preparation_time : float
            Preparation time available (milliseconds)

        Returns:
        --------
        result : Dict
            {
                "flexibility": float,
                "switch_cost_ms": float,
                "switch_success": bool,
                "perseveration_detected": bool
            }
        """
        # 1. Attempt task switch
        success, cost = self.switch_task_set(new_task=new_task, preparation_time=preparation_time)

        # 2. Compute switch frequency (switches / recent history)
        if len(self.task_set_history) >= 2:
            recent_switches = sum(
                1 for i in range(1, min(10, len(self.task_set_history)))
                if self.task_set_history[-i] != self.task_set_history[-i-1]
            )
            switch_frequency = recent_switches / min(10, len(self.task_set_history) - 1)
        else:
            switch_frequency = 0.0

        # 3. Compute success rate
        success_rate = self.successful_switches / max(1, self.switch_count)

        # 4. Update flexibility based on performance
        self.update_flexibility(switch_frequency=switch_frequency, success_rate=success_rate)

        # 5. Detect perseveration
        perseveration = self.detect_perseveration()

        # 6. Return complete result
        return {
            "flexibility": float(self.current_flexibility),
            "switch_cost_ms": float(cost),
            "switch_success": bool(success),
            "perseveration_detected": bool(perseveration)
        }

    def get_state(self) -> Dict:
        """
        Get current cognitive flexibility system state

        Returns:
        --------
        state : Dict
            {
                "flexibility": float,
                "current_task_set": str,
                "task_history": List[str],
                "switch_count": int,
                "successful_switches": int,
                "success_rate": float,
                "average_switch_cost_ms": float
            }
        """
        # Current flexibility
        flexibility = self.current_flexibility

        # Success rate
        success_rate = self.successful_switches / max(1, self.switch_count)

        # Average switch cost
        average_switch_cost = self.total_switch_cost / max(1, self.switch_count)

        return {
            "flexibility": float(flexibility),
            "current_task_set": self.current_task_set,
            "task_history": self.task_set_history.copy(),
            "switch_count": int(self.switch_count),
            "successful_switches": int(self.successful_switches),
            "success_rate": float(success_rate),
            "average_switch_cost_ms": float(average_switch_cost)
        }
