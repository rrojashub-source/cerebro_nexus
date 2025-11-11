"""
LAB_032: Energy Management System

Function: Track mental energy, ego depletion, compensatory control
Neuroscience Basis: Prefrontal cortex resource depletion, glucose metabolism

Key Papers:
- Baumeister et al. (1998) - Ego depletion and self-control
- Hockey (2013) - Compensatory control model
- Muraven & Baumeister (2000) - Self-control as limited resource

Ego Depletion Model:
- Mental energy is a limited resource
- Cognitive effort depletes energy
- Fatigue = 1 - energy
- Compensatory control: Increased effort when fatigued + task important
- Recovery: Exponential during rest
"""

from typing import Dict, Optional


class EnergyManagementSystem:
    """
    LAB_032: Energy Management System

    Models mental energy through:
    - Ego depletion (energy decreases with cognitive load)
    - Fatigue computation (inverse of energy)
    - Compensatory control (Hockey 2013): increased effort + focus narrowing
    - Recovery dynamics (exponential)
    - Integration with LAB_031 (circadian modulation)
    - Integration with LAB_019-020 (cognitive function impairment)

    Parameters:
    -----------
    starting_energy : float
        Initial energy level (0-1, default: 1.0 = full energy)
    depletion_rate : float
        Base rate of energy depletion per unit effort (default: 0.1)
    recovery_rate : float
        Base rate of recovery during rest (default: 0.3)
    """

    def __init__(
        self,
        starting_energy: float = 1.0,
        depletion_rate: float = 0.1,
        recovery_rate: float = 0.3
    ):
        # Energy state
        self.current_energy: float = starting_energy
        self.depletion_rate = depletion_rate
        self.recovery_rate = recovery_rate

        # Derived state
        self.fatigue_level: float = 1.0 - starting_energy

        # Statistics
        self.total_tasks_performed: int = 0
        self.total_energy_depleted: float = 0.0
        self.total_rest_time: float = 0.0

    def deplete_energy(
        self,
        task_difficulty: float,
        duration: float
    ) -> Dict:
        """
        Deplete energy through cognitive effort

        Based on Baumeister (1998): Self-control tasks deplete
        a limited mental resource.

        Depletion accelerates at low energy (fatigue effect).

        Parameters:
        -----------
        task_difficulty : float
            Task difficulty (0-1, where 1 = very difficult)
        duration : float
            Task duration in arbitrary time units

        Returns:
        --------
        result : Dict
            Depletion result with updated energy
        """
        # Depletion formula: difficulty × duration × fatigue_factor
        # Fatigue factor increases as energy drops (harder to maintain effort)
        fatigue_factor = 1.0 + (1.0 - self.current_energy) ** 0.5

        energy_depleted = (
            task_difficulty *
            duration *
            self.depletion_rate *
            fatigue_factor
        )

        # Apply depletion
        self.current_energy = max(0.0, self.current_energy - energy_depleted)

        # Update fatigue
        self.fatigue_level = 1.0 - self.current_energy

        # Statistics
        self.total_tasks_performed += 1
        self.total_energy_depleted += energy_depleted

        return {
            "energy_depleted": float(energy_depleted),
            "energy_after": float(self.current_energy),
            "fatigue_level": float(self.fatigue_level)
        }

    def compute_fatigue_level(self) -> float:
        """
        Compute current fatigue level

        Fatigue = 1 - energy (inverse relationship)

        Returns:
        --------
        fatigue : float
            Current fatigue level (0-1)
        """
        self.fatigue_level = 1.0 - self.current_energy
        return float(self.fatigue_level)

    def compensatory_effort(
        self,
        task_importance: float
    ) -> Dict:
        """
        Compute compensatory control under fatigue

        Based on Hockey (2013): Under fatigue, people increase
        effort to maintain performance on important tasks, but
        this causes focus narrowing (tunnel vision).

        Parameters:
        -----------
        task_importance : float
            Task importance (0-1, where 1 = very important)

        Returns:
        --------
        result : Dict
            Compensatory control parameters
        """
        fatigue = self.compute_fatigue_level()

        # Effort multiplier: increases with fatigue × importance
        # Up to 2x effort when fatigued on important tasks
        if fatigue > 0.5:
            base_effort_increase = (fatigue - 0.5) * 2.0  # 0 to 1.0
            effort_multiplier = 1.0 + (base_effort_increase * task_importance)
        else:
            effort_multiplier = 1.0

        # Focus narrowing: attention width decreases with fatigue
        # Full focus (1.0) when fresh, narrow focus (0.3) when fatigued
        focus_width = max(0.3, 1.0 - (fatigue * 0.7))

        return {
            "effort_multiplier": float(effort_multiplier),
            "focus_width": float(focus_width),
            "fatigue_level": float(fatigue)
        }

    def recover(
        self,
        duration: float,
        circadian_alertness: float = 0.5
    ) -> Dict:
        """
        Recover energy during rest

        Recovery follows exponential curve: energy += (1.0 - energy) * rate * duration
        Diminishing returns: harder to recover when already high energy.

        Parameters:
        -----------
        duration : float
            Rest duration in arbitrary time units
        circadian_alertness : float, optional
            Circadian alertness level (affects recovery rate, LAB_031 integration)

        Returns:
        --------
        result : Dict
            Recovery result with updated energy
        """
        # Circadian modulation of recovery
        # Better recovery during high circadian periods
        circadian_factor = 0.7 + (circadian_alertness * 0.6)  # 0.7 to 1.3

        # Exponential recovery
        # energy += (1.0 - energy) * rate * duration * circadian_factor
        energy_gap = 1.0 - self.current_energy
        recovery_amount = energy_gap * self.recovery_rate * duration * circadian_factor

        self.current_energy = min(1.0, self.current_energy + recovery_amount)

        # Update fatigue
        self.fatigue_level = 1.0 - self.current_energy

        # Statistics
        self.total_rest_time += duration

        return {
            "recovery_amount": float(recovery_amount),
            "energy_after": float(self.current_energy),
            "fatigue_level": float(self.fatigue_level)
        }

    def modulate_cognitive_functions(
        self,
        function: str,
        baseline: float
    ) -> Dict:
        """
        Modulate cognitive performance based on energy level

        Integration with LAB_019 (Cognitive Control) and LAB_020
        (Cognitive Flexibility): Low energy impairs PFC functions.

        Parameters:
        -----------
        function : str
            Cognitive function: "cognitive_control", "cognitive_flexibility", "working_memory"
        baseline : float
            Baseline performance level (0-1)

        Returns:
        --------
        result : Dict
            Modulated performance
        """
        fatigue = self.compute_fatigue_level()

        # Function-specific sensitivity to fatigue
        sensitivity = {
            "cognitive_control": 0.6,  # Sensitive (LAB_019)
            "cognitive_flexibility": 0.55,  # Moderately sensitive (LAB_020)
            "working_memory": 0.5,  # Moderately sensitive
            "simple_motor": 0.2  # Least sensitive
        }

        function_sensitivity = sensitivity.get(function, 0.5)

        # Performance impairment: increases with fatigue × sensitivity
        # At fatigue=1.0, performance can drop by up to sensitivity factor
        impairment = fatigue * function_sensitivity

        modulated_performance = baseline * (1.0 - impairment)

        # Clamp to reasonable range
        modulated_performance = max(0.0, min(1.0, modulated_performance))

        return {
            "baseline_performance": float(baseline),
            "modulated_performance": float(modulated_performance),
            "impairment": float(impairment),
            "fatigue_level": float(fatigue)
        }

    def apply_circadian_modulation(
        self,
        circadian_alertness: float
    ) -> Dict:
        """
        Apply circadian modulation to effective energy

        Integration with LAB_031 (Circadian Rhythm): Low circadian
        alertness reduces effective energy.

        Parameters:
        -----------
        circadian_alertness : float
            Circadian alertness level (0-1, from LAB_031)

        Returns:
        --------
        result : Dict
            Effective energy with circadian modulation
        """
        # Effective energy = base energy × circadian factor
        # Circadian factor ranges from 0.6 (low alertness) to 1.2 (high alertness)
        circadian_factor = 0.6 + (circadian_alertness * 0.6)

        effective_energy = self.current_energy * circadian_factor

        # Clamp to 0-1
        effective_energy = max(0.0, min(1.0, effective_energy))

        return {
            "base_energy": float(self.current_energy),
            "circadian_alertness": float(circadian_alertness),
            "circadian_factor": float(circadian_factor),
            "effective_energy": float(effective_energy)
        }

    def process_event(
        self,
        event_type: str,
        **kwargs
    ) -> Dict:
        """
        Main processing: handle different event types

        Event types:
        - perform_task: Deplete energy through task
        - rest: Recover energy
        - circadian_update: Apply circadian modulation

        Parameters:
        -----------
        event_type : str
            Type of event
        **kwargs : Dict
            Event-specific parameters

        Returns:
        --------
        result : Dict
            Event processing result
        """
        if event_type == "perform_task":
            task_difficulty = kwargs.get("task_difficulty", 0.5)
            duration = kwargs.get("duration", 1.0)
            importance = kwargs.get("importance", 0.5)

            # Deplete energy
            depletion_result = self.deplete_energy(task_difficulty, duration)

            # Compute compensatory control
            compensation = self.compensatory_effort(importance)

            return {
                **depletion_result,
                "effort_multiplier": compensation["effort_multiplier"],
                "focus_width": compensation["focus_width"]
            }

        elif event_type == "rest":
            duration = kwargs.get("duration", 1.0)
            circadian_alertness = kwargs.get("circadian_alertness", 0.5)

            return self.recover(duration, circadian_alertness)

        elif event_type == "circadian_update":
            circadian_alertness = kwargs.get("circadian_alertness", 0.5)
            return self.apply_circadian_modulation(circadian_alertness)

        else:
            return {"error": f"Unknown event type: {event_type}"}

    def get_state(self) -> Dict:
        """Get current energy management state"""
        return {
            "current_energy": float(self.current_energy),
            "fatigue_level": float(self.fatigue_level),
            "total_tasks_performed": int(self.total_tasks_performed),
            "total_energy_depleted": float(self.total_energy_depleted),
            "total_rest_time": float(self.total_rest_time)
        }
