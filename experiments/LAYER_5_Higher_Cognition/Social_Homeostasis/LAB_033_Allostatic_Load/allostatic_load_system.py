"""
LAB_033: Allostatic Load System

Function: Cumulative stress tracking, stress effects on cognition
Neuroscience Basis: HPA axis, prefrontal cortex, amygdala

Key Papers:
- McEwen (2000) - Allostasis and allostatic load
- Arnsten (2009) - Stress impairs prefrontal cortex functions
- Sapolsky (2004) - Why zebras don't get ulcers

Allostatic Load Model:
- Load accumulates with stressors (acute + chronic)
- Slow decay (chronic stress recovery takes time)
- Inverted-U performance: optimal at moderate stress
- PFC impairment at load > 0.6
- Amygdala reactivity enhancement under stress
- Wide integration: affects cognition, emotion, memory
"""

from typing import Dict, Optional


class AllostaticLoadSystem:
    """
    LAB_033: Allostatic Load System

    Models cumulative stress through:
    - Stress accumulation (acute + chronic stressors)
    - Slow decay (chronic recovery)
    - Inverted-U performance curve (Yerkes-Dodson)
    - PFC impairment at high load (Arnsten 2009)
    - Amygdala reactivity enhancement
    - Integration with LAB_001 (emotional salience)
    - Integration with LAB_011 (working memory)
    - Integration with LAB_015 (norepinephrine)
    - Integration with LAB_018-021 (executive functions)
    - Integration with LAB_032 (energy depletion)

    Parameters:
    -----------
    starting_load : float
        Initial allostatic load (0-1, default: 0.0)
    accumulation_rate : float
        Rate of stress accumulation (default: 0.1)
    decay_rate : float
        Rate of stress decay per time unit (default: 0.02, slow)
    pfc_impairment_threshold : float
        Load threshold for PFC impairment (default: 0.6)
    """

    def __init__(
        self,
        starting_load: float = 0.0,
        accumulation_rate: float = 0.1,
        decay_rate: float = 0.03,  # Increased from 0.02 to 0.03 (faster recovery)
        pfc_impairment_threshold: float = 0.65  # Increased from 0.6 to 0.65
    ):
        # Stress state
        self.current_load: float = starting_load
        self.accumulation_rate = accumulation_rate
        self.decay_rate = decay_rate
        self.pfc_impairment_threshold = pfc_impairment_threshold

        # Statistics
        self.total_stressors_experienced: int = 0
        self.peak_load_reached: float = starting_load

    def accumulate_stress(
        self,
        stressor_intensity: float,
        stressor_type: str = "acute"
    ) -> Dict:
        """
        Accumulate allostatic load from stressor

        Based on McEwen (2000): Repeated stressors accumulate
        allostatic load, increasing wear and tear on body/brain.

        Parameters:
        -----------
        stressor_intensity : float
            Stressor intensity (0-1, where 1 = severe)
        stressor_type : str
            "acute" or "chronic"

        Returns:
        --------
        result : Dict
            Updated load with stress response
        """
        # Accumulation
        load_increase = stressor_intensity * self.accumulation_rate

        self.current_load = min(1.0, self.current_load + load_increase)

        # Update statistics
        self.total_stressors_experienced += 1
        if self.current_load > self.peak_load_reached:
            self.peak_load_reached = self.current_load

        # Acute stressors trigger norepinephrine spike (LAB_015 integration)
        norepinephrine_spike = False
        if stressor_type == "acute" and stressor_intensity > 0.6:
            norepinephrine_spike = True

        return {
            "load_increase": float(load_increase),
            "load_after": float(self.current_load),
            "norepinephrine_spike": norepinephrine_spike
        }

    def decay_stress(self, time_units: float) -> Dict:
        """
        Decay allostatic load over time (chronic recovery)

        Based on McEwen (2000): Recovery from chronic stress
        is slow, unlike acute stress recovery.

        Parameters:
        -----------
        time_units : float
            Time units of rest/recovery

        Returns:
        --------
        result : Dict
            Updated load after decay
        """
        # Exponential decay (slow)
        decay_factor = (1.0 - self.decay_rate) ** time_units

        self.current_load *= decay_factor

        # Clamp to 0
        self.current_load = max(0.0, self.current_load)

        return {
            "decay_factor": float(decay_factor),
            "load_after": float(self.current_load)
        }

    def compute_stress_effects(self) -> Dict:
        """
        Compute stress effects on performance (inverted-U)

        Based on Yerkes-Dodson Law: Performance follows
        inverted-U curve with arousal/stress.

        Optimal zone: 0.3 - 0.6 load
        Under-aroused: < 0.3
        Over-aroused: > 0.6

        Returns:
        --------
        result : Dict
            Performance modulation and stress state
        """
        load = self.current_load

        # Inverted-U curve
        if load < 0.3:
            # Under-aroused: suboptimal
            performance_multiplier = 0.6 + (load * 1.0)  # 0.6 to 0.9
        elif load < 0.6:
            # Optimal zone: peak performance
            # Peak at 0.45
            distance_from_peak = abs(load - 0.45)
            performance_multiplier = 1.0 - (distance_from_peak * 0.3)
        else:
            # Over-aroused: impaired (steeper decline)
            performance_multiplier = 1.0 - ((load - 0.6) * 1.6)  # Declines rapidly

        # Clamp to reasonable range
        performance_multiplier = max(0.2, min(1.2, performance_multiplier))

        return {
            "current_load": float(load),
            "performance_multiplier": float(performance_multiplier),
            "zone": "under" if load < 0.3 else ("optimal" if load < 0.6 else "over")
        }

    def pfc_impairment(self) -> Dict:
        """
        Assess prefrontal cortex impairment under stress

        Based on Arnsten (2009): Stress impairs PFC functions
        when allostatic load exceeds threshold (~0.6).

        Returns:
        --------
        result : Dict
            PFC impairment status
        """
        load = self.current_load

        # PFC impaired when load > threshold
        pfc_impaired = load > self.pfc_impairment_threshold

        if pfc_impaired:
            # Impairment level increases with load above threshold
            impairment_level = (load - self.pfc_impairment_threshold) / (1.0 - self.pfc_impairment_threshold)
        else:
            impairment_level = 0.0

        return {
            "pfc_impaired": pfc_impaired,
            "impairment_level": float(impairment_level),
            "threshold": float(self.pfc_impairment_threshold)
        }

    def modulate_cognitive_function(
        self,
        function: str,
        baseline: float
    ) -> Dict:
        """
        Modulate cognitive function performance under stress

        Integration with LAB_018-021: Executive functions
        impaired under high allostatic load.

        Parameters:
        -----------
        function : str
            Cognitive function: "cognitive_control", "cognitive_flexibility",
            "error_monitoring", "planning"
        baseline : float
            Baseline performance (0-1)

        Returns:
        --------
        result : Dict
            Modulated performance
        """
        pfc_status = self.pfc_impairment()

        if pfc_status["pfc_impaired"]:
            # PFC-dependent functions impaired
            impairment = pfc_status["impairment_level"]

            # Function-specific sensitivity
            sensitivity = {
                "cognitive_control": 0.7,  # LAB_019
                "cognitive_flexibility": 0.6,  # LAB_020
                "error_monitoring": 0.65,  # LAB_021
                "planning": 0.6  # LAB_018
            }

            function_sensitivity = sensitivity.get(function, 0.5)

            # Apply impairment
            modulated_performance = baseline * (1.0 - impairment * function_sensitivity)
        else:
            # No impairment, slight boost from optimal stress
            stress_effects = self.compute_stress_effects()
            modulated_performance = baseline * stress_effects["performance_multiplier"]

        # Clamp
        modulated_performance = max(0.0, min(1.0, modulated_performance))

        return {
            "baseline_performance": float(baseline),
            "modulated_performance": float(modulated_performance),
            "pfc_impaired": pfc_status["pfc_impaired"]
        }

    def amygdala_reactivity(self) -> Dict:
        """
        Compute amygdala reactivity level under stress

        Based on Arnsten (2009): High stress enhances amygdala
        reactivity (emotional hypervigilance).

        Returns:
        --------
        result : Dict
            Amygdala reactivity level
        """
        load = self.current_load

        # Reactivity increases with load
        # Normal (1.0) at low stress, up to 2.0x at high stress
        if load < 0.5:
            reactivity_level = 1.0
        else:
            # Enhanced reactivity above 0.5
            reactivity_level = 1.0 + ((load - 0.5) * 2.0)

        # Clamp
        reactivity_level = max(1.0, min(2.0, reactivity_level))

        return {
            "reactivity_level": float(reactivity_level),
            "current_load": float(load)
        }

    def modulate_emotional_response(
        self,
        baseline_salience: float
    ) -> Dict:
        """
        Modulate emotional salience under stress

        Integration with LAB_001 (Emotional Salience):
        Stress amplifies emotional reactions.

        Parameters:
        -----------
        baseline_salience : float
            Baseline emotional salience (0-1)

        Returns:
        --------
        result : Dict
            Modulated emotional salience
        """
        amygdala_status = self.amygdala_reactivity()

        # Amplify salience by amygdala reactivity
        modulated_salience = baseline_salience * amygdala_status["reactivity_level"]

        # Clamp
        modulated_salience = max(0.0, min(1.0, modulated_salience))

        return {
            "baseline_salience": float(baseline_salience),
            "modulated_salience": float(modulated_salience),
            "amygdala_reactivity": amygdala_status["reactivity_level"]
        }

    def modulate_working_memory_capacity(
        self,
        baseline_capacity: int
    ) -> Dict:
        """
        Modulate working memory capacity under stress

        Integration with LAB_011 (Working Memory):
        High stress reduces WM capacity.

        Parameters:
        -----------
        baseline_capacity : int
            Baseline WM capacity (e.g., 7 items)

        Returns:
        --------
        result : Dict
            Modulated WM capacity
        """
        load = self.current_load

        # WM capacity reduces with high load
        if load < 0.5:
            # Minimal reduction
            capacity_reduction = 0
        elif load < 0.7:
            # Moderate reduction
            capacity_reduction = int((load - 0.5) * 5)  # Up to 1 item lost
        else:
            # Severe reduction
            capacity_reduction = int(1 + (load - 0.7) * 10)  # Up to 4 items lost

        modulated_capacity = max(3, baseline_capacity - capacity_reduction)

        return {
            "baseline_capacity": baseline_capacity,
            "modulated_capacity": modulated_capacity,
            "capacity_reduction": capacity_reduction
        }

    def compute_energy_depletion_modifier(self) -> Dict:
        """
        Compute energy depletion modifier under stress

        Integration with LAB_032 (Energy Management):
        High stress accelerates energy depletion.

        Returns:
        --------
        result : Dict
            Energy depletion multiplier
        """
        load = self.current_load

        # Stress increases depletion rate
        if load < 0.5:
            depletion_multiplier = 1.0
        else:
            # Increased depletion above 0.5
            depletion_multiplier = 1.0 + ((load - 0.5) * 0.6)  # Up to 1.3x

        return {
            "depletion_multiplier": float(depletion_multiplier),
            "current_load": float(load)
        }

    def is_recovered(self, recovery_threshold: float = 0.3) -> Dict:
        """
        Check if recovered from allostatic load

        Parameters:
        -----------
        recovery_threshold : float
            Load threshold for considering recovered (default: 0.3)

        Returns:
        --------
        result : Dict
            Recovery status
        """
        recovered = self.current_load < recovery_threshold

        return {
            "recovered": recovered,
            "current_load": float(self.current_load),
            "threshold": float(recovery_threshold)
        }

    def process_event(
        self,
        event_type: str,
        **kwargs
    ) -> Dict:
        """
        Main processing: handle different event types

        Event types:
        - stressor: Accumulate load from stressor
        - recovery: Decay load during rest
        - cognitive_task: Perform task with stress modulation

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
        if event_type == "stressor":
            intensity = kwargs.get("intensity", 0.5)
            stressor_type = kwargs.get("stressor_type", "acute")

            return self.accumulate_stress(intensity, stressor_type)

        elif event_type == "recovery":
            duration = kwargs.get("duration", 1.0)
            return self.decay_stress(duration)

        elif event_type == "cognitive_task":
            function = kwargs.get("function", "cognitive_control")
            baseline = kwargs.get("baseline", 0.8)

            return self.modulate_cognitive_function(function, baseline)

        else:
            return {"error": f"Unknown event type: {event_type}"}

    def get_state(self) -> Dict:
        """Get current allostatic load state"""
        pfc_status = self.pfc_impairment()
        stress_effects = self.compute_stress_effects()

        return {
            "current_load": float(self.current_load),
            "pfc_impaired": pfc_status["pfc_impaired"],
            "performance_level": stress_effects["performance_multiplier"],
            "stress_zone": stress_effects["zone"],
            "peak_load_reached": float(self.peak_load_reached),
            "total_stressors_experienced": int(self.total_stressors_experienced)
        }
