"""
LAB_044-050: Homeostasis Systems - Regulatory Balance

Core: Sterling & Eyer (1988) allostasis, McEwen (2007) allostatic load
Functions: Circadian rhythms, energy management, stress regulation, allostatic load,
           homeostatic plasticity, sleep pressure, recovery mechanisms
"""

import time
from typing import Dict
from dataclasses import dataclass
import numpy as np
import math


@dataclass
class HomeostasisState:
    circadian_phase: float  # 0-24 hours
    energy_level: float  # 0-1
    stress_level: float  # 0-1
    allostatic_load: float  # 0-1 (cumulative stress)
    sleep_pressure: float  # 0-1
    recovery_rate: float  # 0-1


class HomeostasisSystem:
    """Unified homeostasis system (LABS 044-050)"""

    def __init__(self):
        # LAB_044: Circadian rhythm
        self.circadian_phase = 12.0  # Start at noon
        self.circadian_period = 24.0

        # LAB_045: Energy management
        self.energy_level = 1.0
        self.energy_consumption_rate = 0.02
        self.energy_recharge_rate = 0.05

        # LAB_046: Stress regulation
        self.stress_level = 0.3
        self.stress_recovery_rate = 0.1

        # LAB_047: Allostatic load
        self.allostatic_load = 0.0
        self.load_accumulation_rate = 0.01

        # LAB_048: Homeostatic plasticity
        self.plasticity_factor = 1.0

        # LAB_049: Sleep pressure
        self.sleep_pressure = 0.0
        self.sleep_pressure_rate = 0.05

        # LAB_050: Recovery mechanisms
        self.recovery_rate = 0.5

    def update(self, dt: float = 1.0):
        """Update all homeostatic systems"""
        # LAB_044: Circadian rhythm
        self.circadian_phase = (self.circadian_phase + dt) % self.circadian_period

        # LAB_045: Energy management
        is_night = 22 <= self.circadian_phase or self.circadian_phase <= 6
        if is_night:
            # Recharge during night
            self.energy_level = min(1.0, self.energy_level + self.energy_recharge_rate * dt)
        else:
            # Consume during day
            self.energy_level = max(0.0, self.energy_level - self.energy_consumption_rate * dt)

        # LAB_046: Stress regulation
        self.stress_level = max(0.0, self.stress_level - self.stress_recovery_rate * dt)

        # LAB_047: Allostatic load
        if self.stress_level > 0.7:
            # High stress accumulates load
            self.allostatic_load = min(1.0, self.allostatic_load + self.load_accumulation_rate * dt)
        else:
            # Low stress allows load to decrease
            self.allostatic_load = max(0.0, self.allostatic_load - 0.005 * dt)

        # LAB_048: Homeostatic plasticity
        # Adjust plasticity based on load
        self.plasticity_factor = 1.0 - (0.5 * self.allostatic_load)

        # LAB_049: Sleep pressure
        if not is_night:
            # Build pressure during day
            self.sleep_pressure = min(1.0, self.sleep_pressure + self.sleep_pressure_rate * dt)
        else:
            # Release during night
            self.sleep_pressure = max(0.0, self.sleep_pressure - 0.1 * dt)

        # LAB_050: Recovery rate
        self.recovery_rate = (self.energy_level * 0.5 + (1.0 - self.stress_level) * 0.5)

    def add_stressor(self, intensity: float):
        """Add stressor (LAB_046)"""
        self.stress_level = min(1.0, self.stress_level + intensity)

    def expend_energy(self, amount: float):
        """Expend energy (LAB_045)"""
        self.energy_level = max(0.0, self.energy_level - amount)

    def sleep(self, duration: float):
        """Sleep period (LAB_049)"""
        # Full recovery during sleep
        self.sleep_pressure = max(0.0, self.sleep_pressure - 0.5 * duration)
        self.energy_level = min(1.0, self.energy_level + 0.3 * duration)
        self.stress_level = max(0.0, self.stress_level - 0.2 * duration)

    def get_state(self) -> HomeostasisState:
        """Get current homeostasis state"""
        return HomeostasisState(
            circadian_phase=self.circadian_phase,
            energy_level=self.energy_level,
            stress_level=self.stress_level,
            allostatic_load=self.allostatic_load,
            sleep_pressure=self.sleep_pressure,
            recovery_rate=self.recovery_rate
        )

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        return {
            "circadian_phase": self.circadian_phase,
            "energy_level": self.energy_level,
            "stress_level": self.stress_level,
            "allostatic_load": self.allostatic_load,
            "sleep_pressure": self.sleep_pressure,
            "recovery_rate": self.recovery_rate,
            "plasticity_factor": self.plasticity_factor,
        }


if __name__ == "__main__":
    print("🧠 LAB_044-050: Homeostasis Systems - Test")
    print("=" * 60)

    system = HomeostasisSystem()

    print("\n☀️ Day simulation...")
    print(f"  Initial state: Energy={system.energy_level:.3f}, Stress={system.stress_level:.3f}")

    # Simulate day (12 hours)
    for hour in range(12):
        system.update(dt=1.0)

    print(f"  After 12 hours: Energy={system.energy_level:.3f}, Sleep pressure={system.sleep_pressure:.3f}")

    print("\n💥 Adding stressor...")
    system.add_stressor(0.5)
    print(f"  Stress level: {system.stress_level:.3f}")

    # More time passes
    for _ in range(6):
        system.update(dt=1.0)

    print(f"\n🌙 Night time (circadian phase: {system.circadian_phase:.1f}h)")
    print(f"  Energy recharging: {system.energy_level:.3f}")
    print(f"  Allostatic load: {system.allostatic_load:.3f}")

    print("\n😴 Sleep period...")
    system.sleep(duration=1.0)
    state = system.get_state()
    print(f"  After sleep: Energy={state.energy_level:.3f}, Stress={state.stress_level:.3f}, "
          f"Sleep pressure={state.sleep_pressure:.3f}")

    print("\n📊 Final Statistics:")
    stats = system.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value:.3f}")

    print("\n✅ LAB_044-050 Complete!")
    print("\n🎉 ALL 50 LABS IMPLEMENTED! 🎉")
