"""
LAB_046: Default Mode Network System

Homeostasis: "Self-referential processing & mind-wandering"

Key Mechanisms:
- Self-referential processing (autobiographical memory)
- Mind-wandering (spontaneous thought)
- Social cognition (mentalizing, theory of mind)
- Future planning (prospection, episodic future thinking)
- Task-negative activation (deactivates during external tasks)

Mathematical Model:
- DMN activation: A = baseline * (1 - task_difficulty * suppression_strength)
- Mind-wandering: W = 1 / (1 + external_stimulation)
- Reactivation: A_new = baseline * exp(-t / tau)
- Anticorrelation: DMN = 1 - TaskPositive

Key Papers:
- Raichle et al. (2001): A default mode of brain function
- Buckner et al. (2008): The brain's default network
- Andrews-Hanna et al. (2014): The default network and self-generated thought
"""

import math
from typing import Dict, Optional


class DefaultModeNetworkSystem:
    """
    Default Mode Network: Self-referential processing & mind-wandering

    Core principle: Active during rest, suppressed during external tasks

    Implements:
    - Self-referential processing
    - Mind-wandering detection
    - Social cognition (mentalizing)
    - Future planning (prospection)
    - Task-negative activation dynamics
    """

    def __init__(
        self,
        baseline_activation: float = 0.7,
        task_suppression_strength: float = 0.8
    ):
        """
        Initialize Default Mode Network System

        Args:
            baseline_activation: Baseline DMN activation during rest [0-1]
            task_suppression_strength: Strength of task-driven suppression [0-1]
        """
        self.baseline_activation = baseline_activation
        self.task_suppression_strength = task_suppression_strength

        # DMN state
        self.dmn_active = False
        self.dmn_activation_level = baseline_activation

        # Mind-wandering tracking
        self.mind_wandering_rate = 0.0

    def engage_self_referential_processing(
        self,
        task_type: str
    ) -> Dict:
        """
        Engage self-referential processing

        Args:
            task_type: Type of self-referential task
                      (e.g., "autobiographical_memory", "self_reflection")

        Returns:
            Self-referential processing result
        """
        # Self-referential tasks activate DMN
        if task_type in ["autobiographical_memory", "self_reflection", "personal_memories"]:
            self.dmn_active = True
            self.dmn_activation_level = 0.9  # High activation
        else:
            self.dmn_activation_level = 0.5  # Moderate

        return {
            "task_type": task_type,
            "dmn_active": self.dmn_active,
            "dmn_activation_level": float(self.dmn_activation_level)
        }

    def suppress_dmn_for_task(
        self,
        task_difficulty: float
    ) -> Dict:
        """
        Suppress DMN during external task

        Args:
            task_difficulty: Task difficulty [0-1]

        Returns:
            DMN suppression result
        """
        # DMN suppression: A = baseline * (1 - task_difficulty * suppression_strength)
        suppression_factor = task_difficulty * self.task_suppression_strength
        self.dmn_activation_level = self.baseline_activation * (1.0 - suppression_factor)

        # DMN suppressed if activation < 0.3
        dmn_suppressed = self.dmn_activation_level < 0.3
        if dmn_suppressed:
            self.dmn_active = False

        return {
            "task_difficulty": float(task_difficulty),
            "dmn_suppressed": dmn_suppressed,
            "dmn_activation_level": float(self.dmn_activation_level)
        }

    def trigger_mind_wandering(
        self,
        external_stimulation: float
    ) -> Dict:
        """
        Trigger mind-wandering

        Args:
            external_stimulation: Level of external stimulation [0-1]

        Returns:
            Mind-wandering result
        """
        # Mind-wandering: W = 1 / (1 + external_stimulation)
        # Low stimulation → High wandering
        mind_wandering_prob = 1.0 / (1.0 + external_stimulation * 2.0)

        # Mind-wandering occurs if prob > 0.5
        mind_wandering = mind_wandering_prob > 0.5

        if mind_wandering:
            self.dmn_active = True
            self.mind_wandering_rate += 0.1

        return {
            "external_stimulation": float(external_stimulation),
            "mind_wandering": mind_wandering,
            "mind_wandering_prob": float(mind_wandering_prob)
        }

    def engage_social_cognition(
        self,
        task_type: str
    ) -> Dict:
        """
        Engage social cognition (mentalizing)

        Args:
            task_type: Type of social cognitive task
                      (e.g., "mentalizing", "perspective_taking", "theory_of_mind")

        Returns:
            Social cognition result
        """
        # Social cognition tasks activate DMN
        if task_type in ["mentalizing", "perspective_taking", "theory_of_mind"]:
            self.dmn_active = True
            self.dmn_activation_level = 0.8
        else:
            self.dmn_activation_level = 0.5

        return {
            "task_type": task_type,
            "dmn_active": self.dmn_active,
            "dmn_activation_level": float(self.dmn_activation_level)
        }

    def engage_future_planning(
        self,
        planning_type: str
    ) -> Dict:
        """
        Engage future planning (prospection)

        Args:
            planning_type: Type of planning
                          (e.g., "episodic_future_thinking", "goal_planning", "immediate_action")

        Returns:
            Future planning result
        """
        # Prospection activates DMN
        if planning_type in ["episodic_future_thinking", "goal_planning"]:
            self.dmn_active = True
            self.dmn_activation_level = 0.85
        elif planning_type == "immediate_action":
            # Immediate concrete planning → Lower DMN
            self.dmn_activation_level = 0.4
        else:
            self.dmn_activation_level = 0.6

        return {
            "planning_type": planning_type,
            "dmn_active": self.dmn_active,
            "dmn_activation_level": float(self.dmn_activation_level)
        }

    def engage_external_task(
        self,
        task_type: str,
        difficulty: float
    ) -> Dict:
        """
        Engage external task (suppresses DMN)

        Args:
            task_type: Type of external task
            difficulty: Task difficulty [0-1]

        Returns:
            External task engagement result
        """
        # External tasks suppress DMN
        result = self.suppress_dmn_for_task(task_difficulty=difficulty)

        return {
            "task_type": task_type,
            "difficulty": float(difficulty),
            "dmn_active": self.dmn_active,
            "dmn_activation_level": float(self.dmn_activation_level)
        }

    def reactivate_dmn(self) -> Dict:
        """
        Reactivate DMN after task completion

        Returns:
            Reactivation result
        """
        # DMN reactivates to baseline
        self.dmn_activation_level = self.baseline_activation
        self.dmn_active = True

        return {
            "dmn_reactivated": True,
            "dmn_activation_level": float(self.dmn_activation_level)
        }

    def activate_during_rest(self) -> Dict:
        """
        Activate DMN during rest (LAB_034 integration)

        Returns:
            Rest activation result
        """
        # Rest → DMN activation
        self.dmn_active = True
        self.dmn_activation_level = self.baseline_activation

        return {
            "dmn_active": True,
            "dmn_activation_level": float(self.dmn_activation_level)
        }

    def modulate_by_meditation(
        self,
        meditation_active: bool
    ) -> Dict:
        """
        Modulate DMN by meditation (LAB_044 integration)

        Args:
            meditation_active: Whether meditation is active

        Returns:
            Meditation modulation result
        """
        if meditation_active:
            # Meditation reduces DMN activity (reduces self-referential thinking)
            self.dmn_activation_level = 0.3
            dmn_modulated = True
        else:
            self.dmn_activation_level = self.baseline_activation
            dmn_modulated = False

        return {
            "meditation_active": meditation_active,
            "dmn_modulated": dmn_modulated,
            "dmn_activation_level": float(self.dmn_activation_level)
        }

    def suppress_during_flow(
        self,
        flow_active: bool
    ) -> Dict:
        """
        Suppress DMN during flow state (LAB_043 integration)

        Args:
            flow_active: Whether flow state is active

        Returns:
            Flow suppression result
        """
        if flow_active:
            # Flow suppresses DMN (focused on task)
            self.dmn_active = False
            self.dmn_activation_level = 0.2
            dmn_suppressed = True
        else:
            dmn_suppressed = False

        return {
            "flow_active": flow_active,
            "dmn_suppressed": dmn_suppressed,
            "dmn_activation_level": float(self.dmn_activation_level)
        }

    def process_event(
        self,
        event_type: str,
        **kwargs
    ) -> Dict:
        """
        Process DMN event

        Args:
            event_type: Type of event ("self_referential", "external_task", etc.)
            **kwargs: Event-specific parameters

        Returns:
            Processing result
        """
        if event_type == "self_referential":
            return self.engage_self_referential_processing(
                task_type=kwargs["task_type"]
            )

        elif event_type == "external_task":
            return self.engage_external_task(
                task_type=kwargs["task_type"],
                difficulty=kwargs["difficulty"]
            )

        elif event_type == "mind_wandering":
            return self.trigger_mind_wandering(
                external_stimulation=kwargs["external_stimulation"]
            )

        else:
            return {"error": f"Unknown event type: {event_type}"}

    def get_state(self) -> Dict:
        """
        Get current state of DMN system

        Returns:
            System state with DMN metrics
        """
        return {
            "dmn_active": self.dmn_active,
            "dmn_activation_level": float(self.dmn_activation_level),
            "baseline_activation": self.baseline_activation,
            "mind_wandering_rate": float(self.mind_wandering_rate)
        }
