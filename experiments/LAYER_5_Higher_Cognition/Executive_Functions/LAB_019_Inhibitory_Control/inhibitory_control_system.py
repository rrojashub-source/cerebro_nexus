"""
LAB_019: Inhibitory Control System

Core Executive Function: Suppression of prepotent (automatic) responses

Biological Inspiration:
- Right inferior frontal gyrus (rIFG) - Stop-signal processing
- Pre-supplementary motor area (pre-SMA) - Response inhibition
- Orbitofrontal cortex (OFC) - Impulse control

Core Functions:
- Response inhibition (stop-signal paradigm)
- Conflict resolution
- Impulsivity reduction
- Serotonin modulation

Key Papers:
- Aron et al. (2014) - "Frontosubthalamic circuits for stopping and suppression"
- Bari & Robbins (2013) - "Inhibition and impulsivity: Behavioral and neural basis"
"""

from typing import Dict, List
import random


class InhibitoryControlSystem:
    """
    LAB_019: Inhibitory Control System - Response suppression

    Biological inspiration: rIFG, pre-SMA, OFC

    Parameters:
    -----------
    baseline_control : float
        Baseline inhibition strength (default: 0.5)
    control_gain : float
        Control amplification factor (default: 2.0)
    conflict_sensitivity : float
        Sensitivity to response conflict (default: 0.8)
    adaptation_rate : float
        Learning rate for control adaptation (default: 0.1)
    history_window : int
        Size of control history buffer (default: 15)
    base_rt : float
        Base reaction time for SSRT computation (default: 400ms)
    """

    def __init__(
        self,
        baseline_control: float = 0.5,
        control_gain: float = 2.0,
        conflict_sensitivity: float = 0.8,
        adaptation_rate: float = 0.1,
        history_window: int = 15,
        base_rt: float = 400.0
    ):
        # Configuration
        self.baseline_control = baseline_control
        self.control_gain = control_gain
        self.conflict_sensitivity = conflict_sensitivity
        self.adaptation_rate = adaptation_rate
        self.history_window = history_window
        self.base_rt = base_rt  # Base reaction time (ms)

        # State
        self.current_control_strength: float = baseline_control
        self.control_history: List[float] = []
        self.total_inhibitions: int = 0
        self.successful_inhibitions: int = 0

    def update_control_strength(self, response_conflict: float, prepotency: float) -> float:
        """
        Update control strength based on response conflict and prepotency

        Parameters:
        -----------
        response_conflict : float
            Level of conflict between competing responses (0-1)
        prepotency : float
            Strength of automatic/prepotent response (0-1)

        Returns:
        --------
        control_strength : float
            Updated control strength (0-1)
        """
        # Conflict increases control demand
        conflict_boost = response_conflict * self.conflict_sensitivity * 0.3

        # High prepotency also demands more control
        prepotency_demand = prepotency * 0.2

        # Adapt control strength toward baseline + boosts
        target_control = self.baseline_control + conflict_boost + prepotency_demand

        # Gradual adaptation (not instant)
        self.current_control_strength = (
            self.current_control_strength * (1.0 - self.adaptation_rate) +
            target_control * self.adaptation_rate
        )

        # Clamp to [0, 1]
        self.current_control_strength = max(0.0, min(1.0, self.current_control_strength))

        # Update history
        self.control_history.append(self.current_control_strength)
        if len(self.control_history) > self.history_window:
            self.control_history.pop(0)

        return self.current_control_strength

    def attempt_inhibition(self, prepotency: float, control_available: float) -> bool:
        """
        Attempt to inhibit prepotent response (Stop-Signal Paradigm)

        Parameters:
        -----------
        prepotency : float
            Strength of automatic response to inhibit (0-1)
        control_available : float
            Available control strength (0-1)

        Returns:
        --------
        success : bool
            True if inhibition successful, False if failed
        """
        # Track attempt
        self.total_inhibitions += 1

        # Special case: zero prepotency is always successfully inhibited
        if prepotency <= 0.0:
            self.successful_inhibitions += 1
            return True

        # Inhibition success probability
        # High control vs low prepotency = high success
        # Low control vs high prepotency = low success
        inhibition_strength = control_available * self.control_gain

        # Success probability: exponential relationship for stronger effect
        # Squared ratio makes extreme imbalances more deterministic
        ratio = inhibition_strength / (prepotency + 0.1)
        success_probability = min(1.0, ratio ** 1.5)  # Power > 1 for sharper curve

        # Stochastic outcome (like real inhibition)
        success = random.random() < success_probability

        if success:
            self.successful_inhibitions += 1

        return success

    def compute_ssrt(self) -> float:
        """
        Compute Stop-Signal Reaction Time (SSRT)

        SSRT measures speed of inhibition:
        - Low SSRT = fast stopping (good control)
        - High SSRT = slow stopping (poor control)

        Returns:
        --------
        ssrt : float
            Stop-signal reaction time (milliseconds)
        """
        # SSRT inversely proportional to control strength
        # Formula: base_rt * (1.0 - control_strength)
        ssrt = self.base_rt * (1.0 - self.current_control_strength)

        return ssrt

    def integrate_serotonin(self, serotonin_level: float) -> float:
        """
        Modulate control strength by serotonin level

        High serotonin = strong impulse control
        Low serotonin = weak impulse control, high impulsivity

        Parameters:
        -----------
        serotonin_level : float
            Current serotonin level (0-1) from LAB_014

        Returns:
        --------
        modulated_control : float
            Serotonin-modulated control strength (0-1)
        """
        # Serotonin modulates control bidirectionally
        # Low serotonin (<0.5) weakens control
        # High serotonin (>0.5) strengthens control
        # Formula: baseline * (0.5 + serotonin * gain_factor)
        gain_factor = 1.0  # Realistic modulation strength

        modulation_factor = 0.5 + serotonin_level * gain_factor
        modulated_control = self.current_control_strength * modulation_factor

        # Clamp to [0, 1]
        modulated_control = max(0.0, min(1.0, modulated_control))

        return modulated_control

    def compute_impulsivity(self) -> float:
        """
        Compute impulsivity index (inverse of control)

        High control = low impulsivity
        Low control = high impulsivity

        Returns:
        --------
        impulsivity : float
            Impulsivity index (0-1)
        """
        # Impulsivity is inverse of control
        impulsivity = 1.0 - self.current_control_strength

        return impulsivity

    def get_success_rate(self) -> float:
        """
        Compute inhibition success rate

        Returns:
        --------
        success_rate : float
            Proportion of successful inhibitions (0-1)
        """
        if self.total_inhibitions == 0:
            return 0.0

        success_rate = self.successful_inhibitions / self.total_inhibitions
        return success_rate

    def process_event(self, response_conflict: float, prepotency: float) -> Dict:
        """
        Main processing: update control, compute metrics

        Parameters:
        -----------
        response_conflict : float
            Conflict level between competing responses (0-1)
        prepotency : float
            Automatic response strength (0-1)

        Returns:
        --------
        result : Dict
            {
                "control_strength": float,
                "ssrt": float (milliseconds),
                "impulsivity": float,
                "inhibition_success_rate": float
            }
        """
        # 1. Update control strength based on conflict
        self.update_control_strength(response_conflict, prepotency)

        # 2. Attempt inhibition (if there's prepotency to inhibit)
        if prepotency > 0.1:  # Only attempt if meaningful prepotency
            self.attempt_inhibition(prepotency, self.current_control_strength)

        # 3. Compute SSRT
        ssrt = self.compute_ssrt()

        # 4. Compute impulsivity
        impulsivity = self.compute_impulsivity()

        # 5. Get success rate
        success_rate = self.get_success_rate()

        # 6. Return complete result
        return {
            "control_strength": float(self.current_control_strength),
            "ssrt": float(ssrt),
            "impulsivity": float(impulsivity),
            "inhibition_success_rate": float(success_rate)
        }

    def get_state(self) -> Dict:
        """
        Get current inhibitory control system state

        Returns:
        --------
        state : Dict
            {
                "control_strength": float,
                "control_history": List[float],
                "total_inhibitions": int,
                "successful_inhibitions": int,
                "success_rate": float,
                "average_ssrt": float
            }
        """
        # Current control strength
        control_strength = self.current_control_strength

        # Success rate
        success_rate = self.get_success_rate()

        # Average SSRT (approximate from current control)
        average_ssrt = self.compute_ssrt()

        return {
            "control_strength": float(control_strength),
            "control_history": self.control_history.copy(),
            "total_inhibitions": int(self.total_inhibitions),
            "successful_inhibitions": int(self.successful_inhibitions),
            "success_rate": float(success_rate),
            "average_ssrt": float(average_ssrt)
        }
