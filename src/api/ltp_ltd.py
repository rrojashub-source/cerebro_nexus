"""
LAB_039: Long-Term Potentiation (LTP) & LAB_040: Long-Term Depression (LTD)

Core: Bliss & Lømo (1973) LTP discovery, Bear & Malenka (1994) LTP/LTD mechanisms
Functions: Synaptic strengthening (LTP), synaptic weakening (LTD), threshold detection
"""

import time
from typing import Dict
from dataclasses import dataclass
import numpy as np


@dataclass
class Synapse:
    synapse_id: str
    strength: float  # 0-1
    last_active: float


class LTPLTDSystem:
    def __init__(self):
        self.synapses: Dict[str, Synapse] = {}
        self.ltp_threshold = 0.7  # High activity = LTP
        self.ltd_threshold = 0.3  # Low activity = LTD

    def create_synapse(self, synapse_id: str) -> Synapse:
        """Create synapse with baseline strength"""
        synapse = Synapse(synapse_id, strength=0.5, last_active=time.time())
        self.synapses[synapse_id] = synapse
        return synapse

    def stimulate(self, synapse_id: str, intensity: float) -> str:
        """Stimulate synapse, trigger LTP or LTD"""
        if synapse_id not in self.synapses:
            self.create_synapse(synapse_id)

        synapse = self.synapses[synapse_id]

        if intensity >= self.ltp_threshold:
            # LTP: strengthen synapse
            synapse.strength = min(1.0, synapse.strength + 0.1)
            result = "LTP"
        elif intensity <= self.ltd_threshold:
            # LTD: weaken synapse
            synapse.strength = max(0.0, synapse.strength - 0.1)
            result = "LTD"
        else:
            result = "No change"

        synapse.last_active = time.time()
        return result

    def get_statistics(self) -> Dict:
        return {
            "total_synapses": len(self.synapses),
            "avg_strength": np.mean([s.strength for s in self.synapses.values()]) if self.synapses else 0.0,
        }


if __name__ == "__main__":
    print("🧠 LAB_039/040: LTP & LTD - Test")
    print("=" * 60)

    system = LTPLTDSystem()

    print("\n⚡ High-frequency stimulation (LTP)...")
    for i in range(3):
        result = system.stimulate("syn_1", intensity=0.9)
        strength = system.synapses["syn_1"].strength
        print(f"  Stim {i+1}: {result}, Strength={strength:.3f}")

    print("\n🔽 Low-frequency stimulation (LTD)...")
    for i in range(3):
        result = system.stimulate("syn_2", intensity=0.2)
        strength = system.synapses["syn_2"].strength
        print(f"  Stim {i+1}: {result}, Strength={strength:.3f}")

    print(f"\n📊 Stats: {system.get_statistics()}")
    print("\n✅ LAB_039/040 Complete!")
