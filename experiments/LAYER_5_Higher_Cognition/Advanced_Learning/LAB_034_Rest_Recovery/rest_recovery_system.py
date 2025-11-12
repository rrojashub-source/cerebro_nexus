"""
LAB_034: Rest/Recovery Cycles System

Homeostasis: "Sleep & mental restoration"

Key Mechanisms:
- Fatigue detection (mental energy depletion)
- Adenosine accumulation (sleep pressure)
- Rest triggering (automatic recovery mode)
- Resource restoration (energy, stress reduction)
- Circadian alignment (LAB_031 integration)

Mathematical Model:
- Energy depletion: ΔE = -intensity * duration * k
- Adenosine accumulation: A(t) = A0 + t * k_wake
- Recovery rate: ΔE = duration * quality * circadian_factor
- Sleep pressure: P = adenosine_level

Key Papers:
- Walker (2017): Why We Sleep
- Xie et al. (2013): Adenosine clearance during sleep
- McEwen (2006): Sleep deprivation & stress
- Tononi & Cirelli (2014): Synaptic homeostasis
"""

import math
from typing import Dict, Optional


class RestRecoverySystem:
    """
    Rest/Recovery Cycles: Sleep & mental restoration

    Core principle: Rest is essential for cognitive function

    Implements:
    - Fatigue detection
    - Adenosine accumulation (sleep pressure)
    - Rest triggering
    - Resource restoration
    """

    def __init__(
        self,
        fatigue_threshold: float = 0.7,
        initial_energy: float = 1.0
    ):
        """
        Initialize Rest/Recovery System

        Args:
            fatigue_threshold: Energy level triggering rest need
            initial_energy: Starting mental energy [0-1]
        """
        self.fatigue_threshold = fatigue_threshold
        self.mental_energy = initial_energy

        # Sleep pressure (adenosine)
        self.adenosine_level = 0.0  # [0-1]

        # Stress & allostatic load
        self.stress_level = 0.0  # [0-1]
        self.allostatic_load = 0.0  # [0-1]

        # Rest state
        self.is_resting = False

    def perform_cognitive_work(
        self,
        intensity: float,
        duration_minutes: float
    ) -> Dict:
        """
        Perform cognitive work (depletes energy, increases adenosine)

        Args:
            intensity: Work intensity [0-1]
            duration_minutes: Duration in minutes

        Returns:
            Work result with energy depletion
        """
        # Energy depletion
        depletion_rate = 0.01  # Base rate per minute
        energy_cost = intensity * duration_minutes * depletion_rate

        self.mental_energy = max(0.0, self.mental_energy - energy_cost)

        # Adenosine accumulation (proportional to intensity)
        adenosine_rate = 0.005  # Per minute
        adenosine_increase = intensity * duration_minutes * adenosine_rate
        self.adenosine_level = min(1.0, self.adenosine_level + adenosine_increase)

        # Stress accumulation (if energy low)
        if self.mental_energy < 0.3:
            stress_increase = intensity * 0.05
            self.stress_level = min(1.0, self.stress_level + stress_increase)
            self.allostatic_load = min(1.0, self.allostatic_load + stress_increase * 0.5)

        return {
            "work_completed": True,
            "mental_energy": float(self.mental_energy),
            "adenosine_level": float(self.adenosine_level),
            "stress_level": float(self.stress_level)
        }

    def simulate_wakefulness(
        self,
        hours: float
    ) -> Dict:
        """
        Simulate wakefulness (adenosine accumulation without work)

        Args:
            hours: Hours of wakefulness

        Returns:
            Wakefulness simulation result
        """
        # Adenosine builds during wakefulness
        adenosine_rate = 0.045  # Per hour (adjusted for 16h → 0.72 sleep pressure)
        adenosine_increase = hours * adenosine_rate

        self.adenosine_level = min(1.0, self.adenosine_level + adenosine_increase)

        return {
            "adenosine_level": float(self.adenosine_level),
            "sleep_pressure": float(self.get_sleep_pressure())
        }

    def needs_rest(self) -> bool:
        """
        Check if rest is needed

        Returns:
            True if rest needed, False otherwise
        """
        # Rest needed if:
        # 1. Energy below threshold
        # 2. High adenosine (sleep pressure)
        # 3. High stress

        energy_low = self.mental_energy < (1.0 - self.fatigue_threshold)
        adenosine_high = self.adenosine_level > 0.7
        stress_high = self.stress_level > 0.7

        return energy_low or adenosine_high or stress_high

    def trigger_rest_if_needed(self) -> Dict:
        """
        Trigger rest if needed (automatic detection)

        Returns:
            Rest trigger result
        """
        if self.needs_rest():
            # Auto-trigger rest
            self.is_resting = True
            return {
                "rest_triggered": True,
                "reason": "fatigue_threshold_reached",
                "mental_energy": float(self.mental_energy),
                "adenosine_level": float(self.adenosine_level)
            }
        else:
            return {
                "rest_triggered": False,
                "mental_energy": float(self.mental_energy)
            }

    def rest(
        self,
        duration_hours: float,
        sleep_quality: float = 0.8,
        circadian_alignment: bool = True,
        forced: bool = False
    ) -> Dict:
        """
        Rest/Sleep (restore resources)

        Args:
            duration_hours: Rest duration (hours)
            sleep_quality: Sleep quality [0-1]
            circadian_alignment: Sleep aligned with circadian rhythm
            forced: Force rest even if not needed

        Returns:
            Rest result with recovery
        """
        # Compute recovery rate
        base_recovery_rate = 0.12  # Per hour

        # Quality modulation
        quality_factor = sleep_quality

        # Circadian modulation (LAB_031 integration)
        circadian_factor = 1.2 if circadian_alignment else 0.7

        effective_recovery_rate = base_recovery_rate * quality_factor * circadian_factor

        # Restore mental energy
        energy_recovery = duration_hours * effective_recovery_rate
        self.mental_energy = min(1.0, self.mental_energy + energy_recovery)

        # Clear adenosine
        adenosine_clearance_rate = 0.15  # Per hour
        adenosine_cleared = duration_hours * adenosine_clearance_rate * sleep_quality
        self.adenosine_level = max(0.0, self.adenosine_level - adenosine_cleared)

        # Reduce stress
        stress_reduction_rate = 0.1  # Per hour
        stress_reduction = duration_hours * stress_reduction_rate * sleep_quality
        self.stress_level = max(0.0, self.stress_level - stress_reduction)

        # Reduce allostatic load (slower)
        load_reduction = stress_reduction * 0.5
        self.allostatic_load = max(0.0, self.allostatic_load - load_reduction)

        # Rest state
        self.is_resting = True

        return {
            "rest_occurred": True,
            "duration_hours": duration_hours,
            "recovery_rate": float(effective_recovery_rate),
            "mental_energy": float(self.mental_energy),
            "adenosine_level": float(self.adenosine_level),
            "stress_level": float(self.stress_level),
            "dmn_active": True  # LAB_046 integration - DMN active during rest
        }

    def get_sleep_pressure(self) -> float:
        """
        Compute sleep pressure (from adenosine)

        Returns:
            Sleep pressure [0-1]
        """
        return self.adenosine_level

    def get_stress_level(self) -> float:
        """
        Get current stress level

        Returns:
            Stress level [0-1]
        """
        return self.stress_level

    def get_allostatic_load(self) -> float:
        """
        Get cumulative allostatic load (LAB_033 integration)

        Returns:
            Allostatic load [0-1]
        """
        return self.allostatic_load

    def process_event(
        self,
        event_type: str,
        **kwargs
    ) -> Dict:
        """
        Process rest/recovery event

        Args:
            event_type: Type of event ("cognitive_work", "rest", etc.)
            **kwargs: Event-specific parameters

        Returns:
            Processing result
        """
        if event_type == "cognitive_work":
            return self.perform_cognitive_work(
                intensity=kwargs["intensity"],
                duration_minutes=kwargs["duration_minutes"]
            )

        elif event_type == "rest":
            return self.rest(
                duration_hours=kwargs["duration_hours"],
                sleep_quality=kwargs.get("sleep_quality", 0.8),
                circadian_alignment=kwargs.get("circadian_alignment", True)
            )

        else:
            return {"error": f"Unknown event type: {event_type}"}

    def get_state(self) -> Dict:
        """
        Get current state of rest/recovery system

        Returns:
            System state with metrics
        """
        return {
            "mental_energy": float(self.mental_energy),
            "adenosine_level": float(self.adenosine_level),
            "sleep_pressure": float(self.get_sleep_pressure()),
            "stress_level": float(self.stress_level),
            "allostatic_load": float(self.allostatic_load),
            "needs_rest": self.needs_rest(),
            "is_resting": self.is_resting,
            "fatigue_threshold": self.fatigue_threshold
        }
