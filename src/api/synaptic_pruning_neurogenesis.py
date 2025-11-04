"""
LAB_042: Synaptic Pruning & LAB_043: Neurogenesis

Core: Huttenlocher (1979) pruning in development, Altman & Das (1965) adult neurogenesis
Functions: Eliminate weak synapses, generate new neurons
"""

import time
from typing import Dict, List
from dataclasses import dataclass
import numpy as np


@dataclass
class Neuron:
    neuron_id: str
    birth_time: float
    strength: float
    age: float


class SynapticPruningNeurogenesisSystem:
    def __init__(self):
        self.neurons: Dict[str, Neuron] = {}
        self.pruning_threshold = 0.2  # Weak neurons pruned
        self.neurogenesis_rate = 0.1  # New neuron generation rate
        self.neuron_counter = 0

    def add_neuron(self, strength: float = 0.5) -> Neuron:
        """Neurogenesis: Add new neuron"""
        neuron_id = f"neuron_{self.neuron_counter}"
        self.neuron_counter += 1

        neuron = Neuron(neuron_id, time.time(), strength, 0.0)
        self.neurons[neuron_id] = neuron
        return neuron

    def prune_weak_neurons(self) -> List[str]:
        """Synaptic pruning: Remove weak neurons"""
        pruned = []

        for nid, neuron in list(self.neurons.items()):
            if neuron.strength < self.pruning_threshold:
                del self.neurons[nid]
                pruned.append(nid)

        return pruned

    def age_neurons(self, dt: float = 0.1):
        """Age neurons (strength decays slightly)"""
        for neuron in self.neurons.values():
            neuron.age += dt
            neuron.strength *= 0.99  # Slow decay

    def homeostatic_regulation(self):
        """Maintain neuron count through neurogenesis"""
        target_count = 10

        if len(self.neurons) < target_count:
            # Generate new neurons
            needed = target_count - len(self.neurons)
            for _ in range(int(needed * self.neurogenesis_rate) + 1):
                self.add_neuron()

    def get_statistics(self) -> Dict:
        return {
            "total_neurons": len(self.neurons),
            "avg_strength": np.mean([n.strength for n in self.neurons.values()]) if self.neurons else 0.0,
            "avg_age": np.mean([n.age for n in self.neurons.values()]) if self.neurons else 0.0,
        }


if __name__ == "__main__":
    print("🧠 LAB_042/043: Synaptic Pruning & Neurogenesis - Test")
    print("=" * 60)

    system = SynapticPruningNeurogenesisSystem()

    print("\n🌱 Creating initial neurons...")
    for i in range(10):
        strength = np.random.uniform(0.1, 0.9)
        system.add_neuron(strength)

    print(f"  Initial: {len(system.neurons)} neurons")

    print("\n⏳ Aging neurons...")
    for _ in range(5):
        system.age_neurons()

    print("\n✂️ Pruning weak neurons...")
    pruned = system.prune_weak_neurons()
    print(f"  Pruned {len(pruned)} neurons: {pruned[:3]}...")

    print("\n🆕 Neurogenesis (homeostatic regulation)...")
    system.homeostatic_regulation()
    print(f"  After neurogenesis: {len(system.neurons)} neurons")

    stats = system.get_statistics()
    print(f"\n📊 Final stats: {stats}")
    print("\n✅ LAB_042/043 Complete!")
