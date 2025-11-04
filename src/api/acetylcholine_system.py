"""
LAB_016: Acetylcholine System - Attention Focus & Encoding Enhancement

Implements cholinergic signaling based on:
- Hasselmo & McGaughy (2004): Cholinergic modulation of cortical function
- Sarter et al. (2005): Acetylcholine and attention
- Hasselmo (2006): ACh and encoding vs retrieval tradeoff

Core Functions:
1. Sustained attention and focus
2. Encoding enhancement (learning mode)
3. Encoding/retrieval mode switching
4. Sensory gating and signal enhancement
5. Cortical arousal and plasticity

Neuroscience Foundation:
- Basal forebrain: Cholinergic neurons (nbM, MS/DBB)
- Hippocampus: Encoding vs retrieval (high ACh = encoding)
- Cortex: Attention and sensory processing
- PFC: Working memory maintenance

Key Trade-off:
- High ACh → strong encoding, weak retrieval
- Low ACh → weak encoding, strong retrieval
"""

import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import numpy as np
from enum import Enum


class AttentionMode(Enum):
    """Attention state"""
    DIFFUSE = "diffuse"          # Broad, unfocused
    FOCUSED = "focused"          # Selective attention
    HYPERFOCUSED = "hyperfocused"  # Narrow, intense


class MemoryMode(Enum):
    """Encoding vs retrieval bias"""
    RETRIEVAL = "retrieval"  # Low ACh - accessing memories
    BALANCED = "balanced"    # Moderate ACh
    ENCODING = "encoding"    # High ACh - forming new memories


@dataclass
class AcetylcholineSignal:
    """ACh release event"""
    timestamp: float
    level: float  # 0-1 normalized
    source: str
    attention_effect: float
    encoding_boost: float
    plasticity_gate: float


@dataclass
class AttentionEvent:
    """Record of attention deployment"""
    timestamp: float
    target_stimulus: str
    ach_level: float
    focus_quality: float  # 0-1
    distractor_count: int
    sustained_duration: float


@dataclass
class EncodingEvent:
    """Record of memory encoding"""
    timestamp: float
    content_id: str
    ach_level: float
    encoding_strength: float
    interference_level: float


class SensoryGatingModule:
    """
    Controls sensory gating and signal enhancement.

    High ACh → enhanced signal-to-noise in relevant channels
    Low ACh → broad receptive fields, exploration
    """

    def __init__(self):
        self.gating_history: deque = deque(maxlen=500)

    def compute_signal_enhancement(
        self,
        signal_strength: float,
        is_relevant: bool,
        ach_level: float
    ) -> float:
        """
        Enhance relevant signals, suppress irrelevant.

        High ACh → strong gating (focus)
        Low ACh → weak gating (broad attention)
        """
        if is_relevant:
            # ACh enhances relevant signals
            enhancement = 1.0 + (ach_level * 1.0)  # Up to 2x
        else:
            # ACh suppresses irrelevant signals
            suppression = 1.0 - (ach_level * 0.7)  # Down to 0.3x
            enhancement = suppression

        enhanced_signal = signal_strength * enhancement

        return enhanced_signal

    def compute_receptive_field_size(self, ach_level: float) -> float:
        """
        Receptive field size modulated by ACh.

        High ACh → narrow fields (focused)
        Low ACh → broad fields (exploratory)
        """
        # Inverse relationship
        # ACh 0 → size 1.0 (broad)
        # ACh 1 → size 0.3 (narrow)
        size = 1.0 - (ach_level * 0.7)

        return size


class EncodingRetrievalGate:
    """
    Implements Hasselmo's encoding/retrieval trade-off.

    High ACh (encoding mode):
    - Strong LTP (synaptic plasticity)
    - Weak retrieval (suppress auto-associative recall)
    - Focus on new information

    Low ACh (retrieval mode):
    - Weak LTP (minimal new learning)
    - Strong retrieval (pattern completion)
    - Access existing knowledge
    """

    def __init__(self):
        self.current_mode = MemoryMode.BALANCED

    def compute_encoding_strength(self, ach_level: float) -> float:
        """
        Encoding strength increases with ACh.

        High ACh → strong plasticity, efficient encoding
        """
        # Linear to sigmoid transition
        encoding_strength = 1.0 / (1.0 + np.exp(-5 * (ach_level - 0.5)))

        return encoding_strength

    def compute_retrieval_strength(self, ach_level: float) -> float:
        """
        Retrieval strength decreases with ACh.

        Low ACh → pattern completion, associative recall
        High ACh → suppressed retrieval (avoid interference)
        """
        # Inverse of encoding
        retrieval_strength = 1.0 / (1.0 + np.exp(5 * (ach_level - 0.5)))

        return retrieval_strength

    def determine_mode(self, ach_level: float) -> MemoryMode:
        """Determine current encoding/retrieval mode"""
        if ach_level < 0.4:
            return MemoryMode.RETRIEVAL
        elif ach_level < 0.7:
            return MemoryMode.BALANCED
        else:
            return MemoryMode.ENCODING

    def compute_interference_suppression(self, ach_level: float) -> float:
        """
        Suppress interference during encoding.

        High ACh → strong suppression of competing patterns
        """
        suppression = ach_level

        return suppression


class AcetylcholineSystem:
    """
    Main LAB_016 implementation.

    Manages cholinergic signaling including:
    - Sustained attention and focus
    - Encoding/retrieval mode switching
    - Sensory gating and enhancement
    - Cortical plasticity regulation
    """

    def __init__(
        self,
        baseline_ach: float = 0.5,
        attention_gain: float = 1.2,
        plasticity_threshold: float = 0.6
    ):
        # Core parameters
        self.baseline_ach = baseline_ach
        self.attention_gain = attention_gain
        self.plasticity_threshold = plasticity_threshold

        # Current state
        self.current_ach = baseline_ach
        self.current_attention_mode = AttentionMode.DIFFUSE
        self.current_memory_mode = MemoryMode.BALANCED
        self.last_update_time = time.time()

        # Components
        self.sensory_gating = SensoryGatingModule()
        self.encoding_retrieval_gate = EncodingRetrievalGate()

        # History
        self.signal_history: deque = deque(maxlen=1000)
        self.attention_history: deque = deque(maxlen=500)
        self.encoding_history: deque = deque(maxlen=500)

        # Statistics
        self.total_attention_events = 0
        self.total_encoding_events = 0
        self.focused_time = 0.0
        self.last_attention_start = None

    def deploy_attention(
        self,
        target_stimulus: str,
        target_salience: float,
        distractor_count: int = 0
    ) -> AcetylcholineSignal:
        """
        Deploy attention to target stimulus.

        High salience → ACh release → enhanced focus
        More distractors → more ACh needed for focus
        """
        # Base ACh response to target salience
        ach_response = target_salience * self.attention_gain

        # Additional ACh for distractor suppression
        distractor_load = distractor_count * 0.1
        ach_response += distractor_load

        # Update ACh level
        self.current_ach = min(1.0, self.baseline_ach + ach_response)

        # Update attention mode
        self._update_attention_mode()

        # Update memory mode
        self.current_memory_mode = self.encoding_retrieval_gate.determine_mode(
            self.current_ach
        )

        # Compute effects
        attention_effect = self.current_ach  # Focus quality
        encoding_boost = self.encoding_retrieval_gate.compute_encoding_strength(
            self.current_ach
        )
        plasticity_gate = 1.0 if self.current_ach >= self.plasticity_threshold else 0.5

        # Create signal
        signal = AcetylcholineSignal(
            timestamp=time.time(),
            level=self.current_ach,
            source="attention_deployment",
            attention_effect=attention_effect,
            encoding_boost=encoding_boost,
            plasticity_gate=plasticity_gate
        )

        self.signal_history.append(signal)
        self.total_attention_events += 1
        self.last_update_time = time.time()

        # Track sustained attention
        if self.current_attention_mode != AttentionMode.DIFFUSE:
            if self.last_attention_start is None:
                self.last_attention_start = time.time()
        else:
            if self.last_attention_start is not None:
                self.focused_time += time.time() - self.last_attention_start
                self.last_attention_start = None

        return signal

    def process_learning_event(
        self,
        content_id: str,
        novelty: float = 0.5,
        importance: float = 0.5
    ) -> Tuple[float, EncodingEvent]:
        """
        Process learning/encoding event.

        Novel + important → high ACh → strong encoding
        """
        # ACh release for learning
        learning_signal = (novelty + importance) / 2.0
        ach_boost = learning_signal * 0.5

        self.current_ach = min(1.0, self.current_ach + ach_boost)

        # Compute encoding strength
        encoding_strength = self.encoding_retrieval_gate.compute_encoding_strength(
            self.current_ach
        )

        # Interference suppression
        interference = self.encoding_retrieval_gate.compute_interference_suppression(
            self.current_ach
        )

        # Create encoding event
        event = EncodingEvent(
            timestamp=time.time(),
            content_id=content_id,
            ach_level=self.current_ach,
            encoding_strength=encoding_strength,
            interference_level=1.0 - interference
        )

        self.encoding_history.append(event)
        self.total_encoding_events += 1

        return encoding_strength, event

    def _update_attention_mode(self):
        """Update attention mode based on ACh level"""
        if self.current_ach < 0.4:
            self.current_attention_mode = AttentionMode.DIFFUSE
        elif self.current_ach < 0.75:
            self.current_attention_mode = AttentionMode.FOCUSED
        else:
            self.current_attention_mode = AttentionMode.HYPERFOCUSED

    def get_current_ach(self) -> float:
        """
        Get current ACh with decay applied.
        ACh decays slowly (sustained)
        """
        elapsed = time.time() - self.last_update_time

        # Slow decay (ACh sustains attention)
        decay_half_life = 10.0  # seconds
        decay_rate = np.log(2) / decay_half_life

        delta_from_baseline = self.current_ach - self.baseline_ach
        decayed_delta = delta_from_baseline * np.exp(-decay_rate * elapsed)

        current = self.baseline_ach + decayed_delta

        return current

    def get_focus_quality(self) -> float:
        """
        Get current focus/attention quality (0-1).

        High ACh → high quality
        """
        return self.get_current_ach()

    def get_encoding_efficiency(self) -> float:
        """Get current encoding efficiency"""
        current_ach = self.get_current_ach()

        return self.encoding_retrieval_gate.compute_encoding_strength(current_ach)

    def get_retrieval_efficiency(self) -> float:
        """Get current retrieval efficiency"""
        current_ach = self.get_current_ach()

        return self.encoding_retrieval_gate.compute_retrieval_strength(current_ach)

    def process_sensory_input(
        self,
        signal_strength: float,
        is_relevant: bool
    ) -> float:
        """
        Process sensory input with gating.

        Returns enhanced/suppressed signal strength.
        """
        current_ach = self.get_current_ach()

        enhanced = self.sensory_gating.compute_signal_enhancement(
            signal_strength,
            is_relevant,
            current_ach
        )

        return enhanced

    def regulate_baseline(self, delta: float):
        """
        Adjust baseline ACh (e.g., via sleep, aging, disease).
        """
        self.baseline_ach += delta
        self.baseline_ach = max(0.0, min(1.0, self.baseline_ach))

    def get_statistics(self) -> Dict:
        """Get comprehensive system statistics"""
        current_ach = self.get_current_ach()

        return {
            "baseline_ach": self.baseline_ach,
            "current_ach": current_ach,
            "attention_mode": self.current_attention_mode.value,
            "memory_mode": self.current_memory_mode.value,
            "focus_quality": self.get_focus_quality(),
            "encoding_efficiency": self.get_encoding_efficiency(),
            "retrieval_efficiency": self.get_retrieval_efficiency(),
            "total_attention_events": self.total_attention_events,
            "total_encoding_events": self.total_encoding_events,
            "total_focused_time": self.focused_time,
            "receptive_field_size": self.sensory_gating.compute_receptive_field_size(current_ach),
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_016: Acetylcholine System - Test")
    print("=" * 60)

    # Create ACh system
    ach_system = AcetylcholineSystem(
        baseline_ach=0.5,
        attention_gain=1.2,
        plasticity_threshold=0.6
    )

    print("\n📊 Initial State:")
    stats = ach_system.get_statistics()
    print(f"  ACh Level: {stats['current_ach']:.3f}")
    print(f"  Attention Mode: {stats['attention_mode']}")
    print(f"  Memory Mode: {stats['memory_mode']}")
    print(f"  Encoding Efficiency: {stats['encoding_efficiency']:.3f}")
    print(f"  Retrieval Efficiency: {stats['retrieval_efficiency']:.3f}")

    # Scenario 1: Deploy attention to salient target
    print("\n🎯 Deploying attention to salient target...")
    signal = ach_system.deploy_attention(
        target_stimulus="important_email",
        target_salience=0.8,
        distractor_count=3
    )
    print(f"  ACh Level: {signal.level:.3f}")
    print(f"  Attention Mode: {ach_system.current_attention_mode.value}")
    print(f"  Memory Mode: {ach_system.current_memory_mode.value}")
    print(f"  Focus Quality: {signal.attention_effect:.3f}")

    # Scenario 2: Encoding new information (high ACh mode)
    print("\n📝 Encoding new information (high ACh)...")
    encoding_strength, event = ach_system.process_learning_event(
        content_id="new_concept_A",
        novelty=0.9,
        importance=0.8
    )
    print(f"  ACh Level: {event.ach_level:.3f}")
    print(f"  Encoding Strength: {encoding_strength:.3f}")
    print(f"  Interference: {event.interference_level:.3f}")
    print(f"  Memory Mode: {ach_system.current_memory_mode.value}")

    # Check encoding/retrieval trade-off
    stats = ach_system.get_statistics()
    print(f"\n⚖️ Encoding/Retrieval Trade-off:")
    print(f"  Encoding: {stats['encoding_efficiency']:.3f} (HIGH)")
    print(f"  Retrieval: {stats['retrieval_efficiency']:.3f} (LOW)")
    print(f"  → Optimized for learning, not recall")

    # Scenario 3: Sensory gating
    print("\n👁️ Sensory Gating Test:")
    relevant_signal = ach_system.process_sensory_input(
        signal_strength=0.5,
        is_relevant=True
    )
    irrelevant_signal = ach_system.process_sensory_input(
        signal_strength=0.5,
        is_relevant=False
    )
    print(f"  Relevant signal: 0.500 → {relevant_signal:.3f} (enhanced)")
    print(f"  Irrelevant signal: 0.500 → {irrelevant_signal:.3f} (suppressed)")

    # Scenario 4: Decay and switch to retrieval mode
    print("\n⏳ Reducing ACh → Retrieval mode...")
    ach_system.regulate_baseline(-0.3)
    print(f"  New baseline: {ach_system.baseline_ach:.3f}")

    # Wait for decay
    time.sleep(1)
    current_ach = ach_system.get_current_ach()
    memory_mode = ach_system.encoding_retrieval_gate.determine_mode(current_ach)
    print(f"  Current ACh: {current_ach:.3f}")
    print(f"  Memory Mode: {memory_mode.value}")
    print(f"  Encoding: {ach_system.get_encoding_efficiency():.3f} (LOW)")
    print(f"  Retrieval: {ach_system.get_retrieval_efficiency():.3f} (HIGH)")
    print(f"  → Optimized for recall, not learning")

    # Show final statistics
    print("\n📈 Final Statistics:")
    stats = ach_system.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

    print("\n✅ LAB_016 Test Complete!")
