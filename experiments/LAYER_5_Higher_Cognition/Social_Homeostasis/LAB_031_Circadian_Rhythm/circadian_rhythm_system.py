"""
LAB_031: Circadian Rhythm Simulation

Function: Time-of-day effects, alertness cycles, sleep pressure
Neuroscience Basis: SCN (suprachiasmatic nucleus), pineal gland

Key Papers:
- Borbély (1982) - Two-process model of sleep regulation
- Dijk & Czeisler (1995) - Circadian and sleep-dependent control
- Schmidt et al. (2007) - Light entrainment of circadian phase

Two-Process Model:
- Process C: Circadian alertness (sinusoidal, 24h cycle, SCN-driven)
- Process S: Sleep pressure (homeostatic, builds during wake)
- Alertness = C - S
"""

from typing import Dict, Optional
import math


class CircadianRhythmSystem:
    """
    LAB_031: Circadian Rhythm Simulation

    Models circadian effects through:
    - Process C: Circadian oscillation (24-hour cycle)
    - Process S: Homeostatic sleep pressure (builds during wake)
    - Alertness computation: C - S
    - Time-of-day cognitive modulation
    - Light entrainment (phase shifts)

    Parameters:
    -----------
    starting_phase : float
        Starting circadian phase in hours (0-24, where 0 = midnight)
    initial_time_awake : float
        Initial time awake in hours (for Process S)
    circadian_amplitude : float
        Amplitude of circadian oscillation (default: 0.8)
    sleep_pressure_rate : float
        Rate of sleep pressure accumulation per hour (default: 0.01)
    """

    def __init__(
        self,
        starting_phase: float = 0.0,
        initial_time_awake: float = 0.0,
        circadian_amplitude: float = 0.8,
        sleep_pressure_rate: float = 0.05  # Increased from 0.01 to 0.05 (~5% per hour)
    ):
        # Circadian parameters
        self.circadian_phase: float = starting_phase  # Hours (0-24)
        self.circadian_amplitude = circadian_amplitude
        self.peak_phase_morning = 10.0  # Peak alertness ~10 AM
        self.peak_phase_evening = 21.0  # Secondary peak ~9 PM

        # Homeostatic parameters
        self.time_awake: float = initial_time_awake  # Hours
        self.sleep_pressure_rate = sleep_pressure_rate
        self.process_s: float = min(1.0, initial_time_awake * sleep_pressure_rate)

        # Statistics
        self.total_sleep_cycles: int = 0
        self.total_wake_hours: float = 0.0

    def update_circadian_phase(
        self,
        time_elapsed: float,
        light_exposure: float = 0.0
    ) -> float:
        """
        Update circadian phase (24-hour cycle)

        Phase advances naturally with time. Bright light can cause
        phase shifts (Schmidt et al. 2007).

        Parameters:
        -----------
        time_elapsed : float
            Hours elapsed since last update
        light_exposure : float
            Light intensity (0-1, where 1 = bright sunlight)

        Returns:
        --------
        new_phase : float
            Updated circadian phase (0-24)
        """
        # Natural phase advance
        self.circadian_phase += time_elapsed

        # Light entrainment (phase shift)
        if light_exposure > 0.5:  # Bright light
            # Light in early morning: advance phase
            # Light in late evening: delay phase
            if 0 <= self.circadian_phase < 6:
                # Night to early morning: delay (stay up later)
                phase_shift = -0.1 * light_exposure
            elif 6 <= self.circadian_phase < 12:
                # Morning: advance (wake earlier)
                phase_shift = 0.1 * light_exposure
            else:
                # Afternoon/evening: minimal effect
                phase_shift = 0.0

            self.circadian_phase += phase_shift

        # Wrap phase at 24 hours
        self.circadian_phase = self.circadian_phase % 24.0

        return self.circadian_phase

    def compute_process_c(self, phase: Optional[float] = None) -> float:
        """
        Compute Process C (Circadian alertness)

        Based on Borbély (1982): Circadian drive follows sinusoidal
        pattern with peaks at ~10 AM and ~9 PM.

        Uses true bimodal model with two Gaussian-like peaks:
        - Morning peak: ~10 AM (primary, highest)
        - Evening peak: ~21:00 (9 PM) (secondary, wake maintenance zone)
        - Trough: ~3 AM (lowest alertness)

        Parameters:
        -----------
        phase : float, optional
            Circadian phase in hours (uses current if not provided)

        Returns:
        --------
        process_c : float
            Circadian alertness (0-1)
        """
        if phase is None:
            phase = self.circadian_phase

        # Base circadian rhythm (single peak model for baseline)
        # Trough at 3 AM, peak at opposite side (15:00 / 3 PM)
        base_rad = (phase - 3.0) * (2 * math.pi / 24.0)
        base_rhythm = 0.5 + 0.5 * (-math.cos(base_rad))  # 0 at 3 AM, 1 at 3 PM

        # Morning peak contribution (Gaussian-like bump at 10 AM, broader to cover 8-12)
        morning_peak_center = 10.0
        morning_distance = min(abs(phase - morning_peak_center), abs(phase - morning_peak_center + 24), abs(phase - morning_peak_center - 24))
        morning_contribution = 0.9 * math.exp(-0.5 * (morning_distance / 4.0) ** 2)  # Broader (σ=4)

        # Evening peak contribution (Gaussian-like bump at 9 PM = 21:00)
        evening_peak_center = 21.0
        evening_distance = min(abs(phase - evening_peak_center), abs(phase - evening_peak_center + 24), abs(phase - evening_peak_center - 24))
        evening_contribution = 0.6 * math.exp(-0.5 * (evening_distance / 3.0) ** 2)

        # Combine: base rhythm (reduced) + prominent peaks
        combined = base_rhythm * 0.2 + morning_contribution + evening_contribution

        # Apply circadian amplitude
        process_c = combined * self.circadian_amplitude

        # Night suppression (2-6 AM especially low)
        if 0 <= phase < 6:
            night_factor = 0.5 if 2 <= phase < 5 else 0.7
            process_c *= night_factor

        # Clamp to 0-1
        process_c = max(0.0, min(1.0, process_c))

        return float(process_c)

    def compute_process_s(self) -> float:
        """
        Compute Process S (Homeostatic sleep pressure)

        Based on Borbély (1982): Sleep pressure builds linearly
        during wakefulness (~1% per hour) and dissipates during sleep.

        Returns:
        --------
        process_s : float
            Sleep pressure (0-1)
        """
        # Linear accumulation during wake
        self.process_s = min(1.0, self.time_awake * self.sleep_pressure_rate)

        return float(self.process_s)

    def compute_alertness(self) -> float:
        """
        Compute alertness (C - S)

        Alertness is the difference between circadian drive (C)
        and sleep pressure (S).

        Returns:
        --------
        alertness : float
            Current alertness level (can be negative if very tired)
        """
        process_c = self.compute_process_c()
        process_s = self.compute_process_s()

        alertness = process_c - process_s

        return float(alertness)

    def sleep(self, duration: float) -> Dict:
        """
        Process sleep period

        Sleep dissipates homeostatic pressure (Process S) and
        advances circadian phase.

        Parameters:
        -----------
        duration : float
            Sleep duration in hours

        Returns:
        --------
        result : Dict
            Sleep outcome (quality, recovery)
        """
        # Advance circadian phase during sleep
        self.update_circadian_phase(time_elapsed=duration)

        # Reset homeostatic pressure (exponential decay during sleep)
        # Most recovery in first few hours
        recovery_rate = 0.8  # 80% recovery per full sleep cycle
        cycles = duration / 8.0  # 8-hour full cycle

        self.process_s *= (1.0 - recovery_rate) ** cycles
        self.process_s = max(0.0, self.process_s)

        # Reset time awake
        self.time_awake = 0.0

        # Sleep quality depends on circadian alignment
        # Best sleep at night (phase 22-6), worst during day
        if 22 <= self.circadian_phase or self.circadian_phase < 6:
            sleep_quality = 0.9  # Good circadian alignment
        elif 6 <= self.circadian_phase < 12:
            sleep_quality = 0.4  # Morning (poor sleep)
        else:
            sleep_quality = 0.3  # Afternoon (worst sleep)

        self.total_sleep_cycles += 1

        return {
            "duration": float(duration),
            "sleep_quality": float(sleep_quality),
            "process_s_after": float(self.process_s),
            "phase_after": float(self.circadian_phase)
        }

    def time_of_day_effects(
        self,
        cognitive_task: str,
        baseline_performance: float = 1.0
    ) -> Dict:
        """
        Modulate cognitive performance by circadian alertness

        Different cognitive functions have different sensitivity
        to circadian effects (Dijk & Czeisler 1995).

        Parameters:
        -----------
        cognitive_task : str
            Task type: "working_memory", "attention", "simple_motor", "creativity"
        baseline_performance : float
            Baseline performance level (0-1)

        Returns:
        --------
        result : Dict
            Modulated performance with alertness effects
        """
        alertness = self.compute_alertness()

        # Task-specific sensitivity to alertness
        sensitivity = {
            "working_memory": 1.0,  # Highly sensitive
            "attention": 0.9,
            "executive_function": 0.8,
            "creativity": 0.5,  # Less sensitive (sometimes better when tired!)
            "simple_motor": 0.3  # Least sensitive
        }

        task_sensitivity = sensitivity.get(cognitive_task, 0.7)

        # Modulate performance based on alertness
        # Alertness ranges from ~-0.5 (very tired) to ~1.0 (peak)
        # Map to performance multiplier: 0.5 (tired) to 1.2 (alert)
        if alertness > 0:
            multiplier = 1.0 + (alertness * 0.2 * task_sensitivity)
        else:
            multiplier = 1.0 + (alertness * 0.8 * task_sensitivity)

        modulated_performance = baseline_performance * multiplier

        # Clamp to reasonable range
        modulated_performance = max(0.0, min(1.5, modulated_performance))

        return {
            "baseline_performance": float(baseline_performance),
            "modulated_performance": float(modulated_performance),
            "alertness": float(alertness),
            "task_sensitivity": float(task_sensitivity)
        }

    def should_trigger_sleep_consolidation(
        self,
        threshold: float = 0.6
    ) -> Dict:
        """
        Check if sleep consolidation should trigger (LAB_003 integration)

        High sleep pressure (Process S) triggers sleep consolidation
        in hippocampus.

        Parameters:
        -----------
        threshold : float
            Sleep pressure threshold for triggering (default: 0.6)

        Returns:
        --------
        result : Dict
            Consolidation trigger decision
        """
        process_s = self.compute_process_s()

        should_consolidate = process_s >= threshold

        return {
            "should_consolidate": should_consolidate,
            "sleep_pressure": float(process_s),
            "threshold": float(threshold),
            "circadian_phase": float(self.circadian_phase)
        }

    def process_event(
        self,
        event_type: str,
        **kwargs
    ) -> Dict:
        """
        Main processing: handle different event types

        Event types:
        - time_passage: Update phase and alertness
        - sleep: Process sleep period
        - wake: Reset after sleep

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
        if event_type == "time_passage":
            hours_elapsed = kwargs.get("hours_elapsed", 1.0)
            light_exposure = kwargs.get("light_exposure", 0.0)

            # Update phase
            new_phase = self.update_circadian_phase(hours_elapsed, light_exposure)

            # Update time awake
            self.time_awake += hours_elapsed
            self.total_wake_hours += hours_elapsed

            # Compute alertness
            alertness = self.compute_alertness()

            return {
                "new_phase": float(new_phase),
                "time_awake": float(self.time_awake),
                "process_c": float(self.compute_process_c()),
                "process_s": float(self.compute_process_s()),
                "alertness": float(alertness)
            }

        elif event_type == "sleep":
            duration = kwargs.get("duration", 8.0)
            return self.sleep(duration)

        elif event_type == "wake":
            # Just woke up
            self.time_awake = 0.0
            self.process_s = 0.0

            return {
                "time_awake": 0.0,
                "process_s": 0.0,
                "alertness": float(self.compute_alertness()),
                "circadian_phase": float(self.circadian_phase)
            }

        else:
            return {"error": f"Unknown event type: {event_type}"}

    def get_state(self) -> Dict:
        """Get current circadian rhythm state"""
        return {
            "circadian_phase": float(self.circadian_phase),
            "time_awake": float(self.time_awake),
            "process_c": float(self.compute_process_c()),
            "process_s": float(self.compute_process_s()),
            "alertness": float(self.compute_alertness()),
            "total_sleep_cycles": int(self.total_sleep_cycles),
            "total_wake_hours": float(self.total_wake_hours)
        }
