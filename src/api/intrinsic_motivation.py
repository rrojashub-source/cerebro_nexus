"""
LAB_038: Intrinsic Motivation - Self-Determined Goals

Core: Deci & Ryan (2000) Self-Determination Theory, Ryan & Deci (2017) autonomy/competence/relatedness
Functions: Autonomy, competence (mastery), relatedness needs
"""

import time
from typing import Dict
from dataclasses import dataclass
import numpy as np


@dataclass
class MotivationState:
    autonomy: float  # 0-1
    competence: float  # 0-1
    relatedness: float  # 0-1
    overall: float  # 0-1


class IntrinsicMotivationSystem:
    def __init__(self):
        self.autonomy_level = 0.5
        self.competence_level = 0.5
        self.relatedness_level = 0.5

    def update_autonomy(self, choice_freedom: float):
        """Update autonomy (freedom to choose)"""
        self.autonomy_level = 0.9 * self.autonomy_level + 0.1 * choice_freedom
        self.autonomy_level = np.clip(self.autonomy_level, 0.0, 1.0)

    def update_competence(self, success: bool, challenge: float):
        """Update competence (mastery feeling)"""
        if success:
            # Success on challenging task = big competence boost
            boost = 0.1 * challenge
        else:
            boost = -0.05

        self.competence_level += boost
        self.competence_level = np.clip(self.competence_level, 0.0, 1.0)

    def update_relatedness(self, social_connection: float):
        """Update relatedness (connection to others)"""
        self.relatedness_level = 0.9 * self.relatedness_level + 0.1 * social_connection
        self.relatedness_level = np.clip(self.relatedness_level, 0.0, 1.0)

    def get_motivation_state(self) -> MotivationState:
        """Get current motivation state"""
        overall = (self.autonomy_level + self.competence_level + self.relatedness_level) / 3.0

        return MotivationState(
            autonomy=self.autonomy_level,
            competence=self.competence_level,
            relatedness=self.relatedness_level,
            overall=overall
        )


if __name__ == "__main__":
    print("🧠 LAB_038: Intrinsic Motivation - Test")
    print("=" * 60)

    system = IntrinsicMotivationSystem()

    print("\n🎯 Initial state:")
    state = system.get_motivation_state()
    print(f"  Autonomy={state.autonomy:.3f}, Competence={state.competence:.3f}, "
          f"Relatedness={state.relatedness:.3f}, Overall={state.overall:.3f}")

    print("\n📈 Increasing autonomy (more choice freedom)...")
    system.update_autonomy(0.9)
    state = system.get_motivation_state()
    print(f"  Overall motivation: {state.overall:.3f}")

    print("\n💪 Success on challenging task...")
    system.update_competence(success=True, challenge=0.8)
    state = system.get_motivation_state()
    print(f"  Competence: {state.competence:.3f}, Overall: {state.overall:.3f}")

    print("\n👥 Social connection...")
    system.update_relatedness(0.8)
    state = system.get_motivation_state()
    print(f"  Relatedness: {state.relatedness:.3f}, Overall: {state.overall:.3f}")

    print("\n✅ LAB_038 Complete!")
