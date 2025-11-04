"""
LAB_037: Curiosity Drive - Information-Seeking Motivation

Core: Berlyne (1960) curiosity theory, Schmidhuber (1991) curiosity-driven learning
Functions: Prediction error curiosity, novelty bonus, exploration vs exploitation
"""

import time
from typing import Dict, List
from dataclasses import dataclass
import numpy as np


@dataclass
class Observation:
    obs_id: str
    features: Dict[str, float]
    novelty: float
    prediction_error: float


class CuriosityDriveSystem:
    def __init__(self):
        self.observations: List[Observation] = []
        self.seen_features: Dict[str, int] = {}
        self.baseline_curiosity = 0.5

    def compute_novelty(self, features: Dict[str, float]) -> float:
        """Novelty = inverse of familiarity"""
        familiarity = 0.0
        for feat, val in features.items():
            familiarity += self.seen_features.get(feat, 0) / 10.0

        novelty = 1.0 / (1.0 + familiarity)
        return novelty

    def compute_prediction_error(self, features: Dict[str, float]) -> float:
        """Prediction error drives curiosity (Schmidhuber)"""
        # Simulate prediction error (higher for novel patterns)
        return np.random.uniform(0.3, 0.8) if len(self.observations) < 5 else np.random.uniform(0.1, 0.4)

    def generate_curiosity_bonus(self, obs_id: str, features: Dict[str, float]) -> float:
        """Generate intrinsic reward from curiosity"""
        novelty = self.compute_novelty(features)
        pred_error = self.compute_prediction_error(features)

        # Curiosity bonus combines novelty and prediction error
        curiosity_bonus = self.baseline_curiosity * (0.5 * novelty + 0.5 * pred_error)

        # Record observation
        obs = Observation(obs_id, features, novelty, pred_error)
        self.observations.append(obs)

        # Update seen features
        for feat in features:
            self.seen_features[feat] = self.seen_features.get(feat, 0) + 1

        return curiosity_bonus

    def get_statistics(self) -> Dict:
        return {
            "observations": len(self.observations),
            "avg_novelty": np.mean([o.novelty for o in self.observations]) if self.observations else 0.0,
            "avg_prediction_error": np.mean([o.prediction_error for o in self.observations]) if self.observations else 0.0,
        }


if __name__ == "__main__":
    print("🧠 LAB_037: Curiosity Drive - Test")
    print("=" * 60)

    system = CuriosityDriveSystem()

    print("\n🔍 Exploring environment...")
    observations = [
        {"color": "red", "shape": "circle"},
        {"color": "blue", "shape": "square"},
        {"color": "red", "shape": "circle"},  # Repeat
        {"color": "green", "shape": "triangle"},  # Novel
    ]

    for i, obs_features in enumerate(observations):
        bonus = system.generate_curiosity_bonus(f"obs_{i}", obs_features)
        novelty = system.observations[-1].novelty
        print(f"  Obs {i}: {obs_features} → Curiosity bonus={bonus:.3f}, Novelty={novelty:.3f}")

    stats = system.get_statistics()
    print(f"\n📊 Stats: {stats}")
    print("\n✅ LAB_037 Complete!")
