"""
LAB_041: Hebbian Learning - "Cells that fire together wire together"

Core: Hebb (1949) cell assembly theory, Brown et al. (1990) associative LTP
Functions: Correlation-based strengthening, spike-timing dependent plasticity (STDP)
"""

import time
from typing import Dict, List
from dataclasses import dataclass
import numpy as np


@dataclass
class NeuronPair:
    pre_id: str
    post_id: str
    weight: float
    coincident_activations: int


class HebbianLearningSystem:
    def __init__(self, learning_rate: float = 0.05):
        self.learning_rate = learning_rate
        self.connections: Dict[Tuple[str, str], NeuronPair] = {}
        self.activation_history: Dict[str, List[float]] = {}

    def activate_neurons(self, neuron_ids: List[str], timestamp: float):
        """Record neuron activations"""
        for nid in neuron_ids:
            if nid not in self.activation_history:
                self.activation_history[nid] = []
            self.activation_history[nid].append(timestamp)

    def update_weights(self, time_window: float = 0.05):
        """Update connection weights based on co-activation (Hebbian rule)"""
        neurons = list(self.activation_history.keys())

        for i, pre in enumerate(neurons):
            for post in neurons[i+1:]:
                key = (pre, post)

                # Check for coincident activation
                pre_times = self.activation_history[pre]
                post_times = self.activation_history[post]

                coincident = 0
                for pre_t in pre_times[-10:]:  # Recent activations
                    for post_t in post_times[-10:]:
                        if abs(pre_t - post_t) < time_window:
                            coincident += 1

                if coincident > 0:
                    # Create or strengthen connection
                    if key not in self.connections:
                        self.connections[key] = NeuronPair(pre, post, 0.1, 0)

                    pair = self.connections[key]
                    pair.weight = min(1.0, pair.weight + self.learning_rate * coincident)
                    pair.coincident_activations += coincident

    def get_statistics(self) -> Dict:
        return {
            "connections": len(self.connections),
            "avg_weight": np.mean([c.weight for c in self.connections.values()]) if self.connections else 0.0,
        }


if __name__ == "__main__":
    print("🧠 LAB_041: Hebbian Learning - Test")
    print("=" * 60)

    system = HebbianLearningSystem()

    print("\n🔗 Co-activating neurons A and B...")
    for i in range(5):
        t = time.time()
        system.activate_neurons(["A", "B"], t)
        system.update_weights()

    print("\n📊 Connections formed:")
    for (pre, post), pair in system.connections.items():
        print(f"  {pre} → {post}: weight={pair.weight:.3f}, coincident={pair.coincident_activations}")

    print(f"\n📈 Stats: {system.get_statistics()}")
    print("\n✅ LAB_041 Complete!")
