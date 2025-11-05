"""
NeuroEmotionalBridge

Bidirectional integration between Layer 2 (Emotional 8D) and Layer 4 (Neurotransmitters)

Author: NEXUS + Ricardo
Date: November 5, 2025
Session: 8
"""

from typing import Dict, Optional
from dataclasses import dataclass
import sys
from pathlib import Path

# Add experiments to path
experiments_path = Path(__file__).parent.parent
sys.path.insert(0, str(experiments_path))

from LAYER_4_Neurochemistry_Full.LAB_013_Dopamine_System import DopamineSystem
from LAYER_4_Neurochemistry_Full.LAB_014_Serotonin_System import SerotoninSystem
from LAYER_4_Neurochemistry_Full.LAB_015_Norepinephrine_System import NorepinephrineSystem
from LAYER_4_Neurochemistry_Full.LAB_016_Acetylcholine_System import AcetylcholineSystem
from LAYER_4_Neurochemistry_Full.LAB_017_GABA_System import GABASystem


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class EmotionalState:
    """Plutchik 8D emotional state"""
    joy: float = 0.0
    trust: float = 0.0
    fear: float = 0.0
    surprise: float = 0.0
    sadness: float = 0.0
    disgust: float = 0.0
    anger: float = 0.0
    anticipation: float = 0.0


@dataclass
class SomaticMarker:
    """Damasio somatic marker (simplified)"""
    valence: float = 0.0
    arousal: float = 0.0
    situation: str = "neutral"


# ============================================================================
# NEURO-EMOTIONAL BRIDGE
# ============================================================================

class NeuroEmotionalBridge:
    """
    Bidirectional integration between emotions and neurotransmitters

    Forward Pass: Emotions → Neurotransmitters
    Backward Pass: Neurotransmitters → Emotions

    Architecture:
    ─────────────────────────────────────────────────────────────
    Layer 2 (Emotional 8D)   ←→   Layer 4 (Neurotransmitters)
    ─────────────────────────────────────────────────────────────
    • joy                    ←→    • dopamine
    • trust                  ←→    • serotonin
    • fear                   ←→    • norepinephrine
    • surprise               ←→    • (multiple)
    • sadness                ←→    • serotonin (-)
    • disgust                ←→    • (minimal)
    • anger                  ←→    • GABA (-), NE
    • anticipation           ←→    • dopamine, ACh

    Somatic 7D:
    • arousal                ←→    • norepinephrine
    • valence                ←→    • serotonin
    • anxiety                ←→    • GABA
    ─────────────────────────────────────────────────────────────
    """

    # Mapping weights (tunable)
    MAX_MODULATION = 0.3  # Max 30% change per cycle (prevent runaway)

    def __init__(self):
        """
        Initialize bridge with Layer 4 neurotransmitter systems
        """
        # Initialize neurotransmitter systems
        self.neuro_systems = {
            'dopamine': DopamineSystem(baseline_lr=0.1),
            'serotonin': SerotoninSystem(baseline_mood=0.5),
            'norepinephrine': NorepinephrineSystem(baseline_arousal=0.3),
            'acetylcholine': AcetylcholineSystem(baseline_ach=0.5),
            'gaba': GABASystem(baseline_gaba=0.5)
        }

        # Forward pass weights
        self.forward_weights = {
            # Dopamine mapping
            'joy_to_dopamine': 0.4,
            'anticipation_to_dopamine': 0.3,

            # Serotonin mapping
            'trust_to_serotonin': 0.5,
            'sadness_to_serotonin': -0.3,  # Depletion

            # Norepinephrine mapping
            'fear_to_norepinephrine': 0.6,
            'arousal_to_norepinephrine': 0.4,

            # Acetylcholine mapping
            'anticipation_to_acetylcholine': 0.5,
            'surprise_to_acetylcholine': 0.3,

            # GABA mapping (compensatory)
            'anger_to_gaba': 0.4,
            'anxiety_to_gaba': 0.5
        }

        # Backward pass weights
        self.backward_weights = {
            # Dopamine → Emotions
            'dopamine_to_joy': 0.3,
            'dopamine_to_anticipation': 0.2,

            # Serotonin → Emotions
            'serotonin_to_trust': 0.4,
            'serotonin_to_sadness': -0.3,  # Reduction

            # Norepinephrine → Emotions
            'norepinephrine_to_fear': 0.5,  # Only if > 0.7

            # Acetylcholine → Emotions
            'acetylcholine_to_anticipation': 0.2,

            # GABA → Emotions
            'gaba_to_fear': -0.4,  # Reduction (calming)
            'gaba_to_anger': -0.3   # Reduction (calming)
        }

    # ========================================================================
    # FORWARD PASS: Emotions → Neurotransmitters
    # ========================================================================

    def forward_pass(
        self,
        emotional_state: EmotionalState,
        somatic_marker: SomaticMarker
    ) -> Dict[str, float]:
        """
        Forward pass: Emotions → Neurotransmitters

        Parameters:
        -----------
        emotional_state : EmotionalState
            Current Plutchik 8D emotional state
        somatic_marker : SomaticMarker
            Current Damasio somatic marker

        Returns:
        --------
        neuro_state : Dict[str, float]
            Neurotransmitter levels (0-1)
        """
        # 1. Dopamine modulation (reward/motivation)
        dopamine_level = self._compute_dopamine(emotional_state)

        # 2. Serotonin modulation (mood stability)
        serotonin_level = self._compute_serotonin(emotional_state, somatic_marker)

        # 3. Norepinephrine modulation (arousal)
        norepinephrine_level = self._compute_norepinephrine(emotional_state, somatic_marker)

        # 4. Acetylcholine modulation (attention)
        acetylcholine_level = self._compute_acetylcholine(emotional_state)

        # 5. GABA modulation (inhibitory control)
        gaba_level = self._compute_gaba(emotional_state, somatic_marker)

        return {
            'dopamine': dopamine_level,
            'serotonin': serotonin_level,
            'norepinephrine': norepinephrine_level,
            'acetylcholine': acetylcholine_level,
            'gaba': gaba_level
        }

    def _compute_dopamine(self, emotional_state: EmotionalState) -> float:
        """
        Joy + Anticipation → Dopamine

        Parameters:
        -----------
        emotional_state : EmotionalState
            Emotional state

        Returns:
        --------
        dopamine_level : float (0-1)
        """
        # Baseline motivation
        baseline = 0.4

        joy_contrib = emotional_state.joy * self.forward_weights['joy_to_dopamine']
        anticipation_contrib = emotional_state.anticipation * self.forward_weights['anticipation_to_dopamine']

        dopamine_level = baseline + joy_contrib + anticipation_contrib

        # Clamp to [0, 1]
        return max(0.0, min(1.0, dopamine_level))

    def _compute_serotonin(
        self,
        emotional_state: EmotionalState,
        somatic_marker: SomaticMarker
    ) -> float:
        """
        Trust (+) + Sadness (-) + Valence → Serotonin

        Parameters:
        -----------
        emotional_state : EmotionalState
            Emotional state
        somatic_marker : SomaticMarker
            Somatic marker

        Returns:
        --------
        serotonin_level : float (0-1)
        """
        # Baseline
        baseline = 0.5

        # Trust boosts serotonin
        trust_boost = emotional_state.trust * self.forward_weights['trust_to_serotonin']

        # Sadness depletes serotonin
        sadness_drain = emotional_state.sadness * self.forward_weights['sadness_to_serotonin']  # Negative

        # Valence contribution
        valence_contrib = somatic_marker.valence * 0.2  # Positive valence → serotonin

        serotonin_level = baseline + trust_boost + sadness_drain + valence_contrib

        # Clamp to [0, 1]
        return max(0.0, min(1.0, serotonin_level))

    def _compute_norepinephrine(
        self,
        emotional_state: EmotionalState,
        somatic_marker: SomaticMarker
    ) -> float:
        """
        Fear + Arousal → Norepinephrine

        Parameters:
        -----------
        emotional_state : EmotionalState
            Emotional state
        somatic_marker : SomaticMarker
            Somatic marker

        Returns:
        --------
        norepinephrine_level : float (0-1)
        """
        # Baseline arousal
        baseline = 0.3

        fear_contrib = emotional_state.fear * self.forward_weights['fear_to_norepinephrine']
        arousal_contrib = somatic_marker.arousal * self.forward_weights['arousal_to_norepinephrine']

        norepinephrine_level = baseline + fear_contrib + arousal_contrib

        # Clamp to [0, 1]
        return max(0.0, min(1.0, norepinephrine_level))

    def _compute_acetylcholine(self, emotional_state: EmotionalState) -> float:
        """
        Anticipation + Surprise → Acetylcholine (attention gating)

        Parameters:
        -----------
        emotional_state : EmotionalState
            Emotional state

        Returns:
        --------
        acetylcholine_level : float (0-1)
        """
        # Baseline attention
        baseline = 0.3

        anticipation_contrib = emotional_state.anticipation * self.forward_weights['anticipation_to_acetylcholine']
        surprise_contrib = emotional_state.surprise * self.forward_weights['surprise_to_acetylcholine']

        acetylcholine_level = baseline + anticipation_contrib + surprise_contrib

        # Clamp to [0, 1]
        return max(0.0, min(1.0, acetylcholine_level))

    def _compute_gaba(
        self,
        emotional_state: EmotionalState,
        somatic_marker: SomaticMarker
    ) -> float:
        """
        Anger + Anxiety → GABA spike (compensatory inhibition)

        Parameters:
        -----------
        emotional_state : EmotionalState
            Emotional state
        somatic_marker : SomaticMarker
            Somatic marker

        Returns:
        --------
        gaba_level : float (0-1)
        """
        # Baseline
        baseline = 0.5

        # Anger triggers GABA (need inhibitory control)
        anger_contrib = emotional_state.anger * self.forward_weights['anger_to_gaba']

        # Anxiety (high arousal + negative valence) → GABA spike
        anxiety = somatic_marker.arousal if somatic_marker.valence < 0 else 0.0
        anxiety_contrib = anxiety * self.forward_weights['anxiety_to_gaba']

        gaba_level = baseline + anger_contrib + anxiety_contrib

        # Clamp to [0, 1]
        return max(0.0, min(1.0, gaba_level))

    # ========================================================================
    # BACKWARD PASS: Neurotransmitters → Emotions
    # ========================================================================

    def backward_pass(self) -> Dict[str, float]:
        """
        Backward pass: Neurotransmitters → Emotional modulation

        Returns:
        --------
        emotional_modulation : Dict[str, float]
            Changes to apply to emotional state
        """
        modulation = {}

        # 1. Dopamine → Joy + Anticipation
        dopamine_level = self.neuro_systems['dopamine'].motivation_level
        modulation['joy_boost'] = self._clamp_modulation(
            dopamine_level * self.backward_weights['dopamine_to_joy']
        )
        modulation['anticipation_boost'] = self._clamp_modulation(
            dopamine_level * self.backward_weights['dopamine_to_anticipation']
        )

        # 2. Serotonin → Trust + Sadness reduction
        serotonin_level = self.neuro_systems['serotonin'].mood_level
        modulation['trust_boost'] = self._clamp_modulation(
            serotonin_level * self.backward_weights['serotonin_to_trust']
        )
        modulation['sadness_reduction'] = self._clamp_modulation(
            serotonin_level * self.backward_weights['serotonin_to_sadness']
        )

        # 3. Norepinephrine → Fear (only if excessive, Yerkes-Dodson breakdown)
        norepinephrine_level = self.neuro_systems['norepinephrine'].arousal_level
        if norepinephrine_level > 0.7:  # Excessive arousal
            modulation['fear_boost'] = self._clamp_modulation(
                (norepinephrine_level - 0.7) * self.backward_weights['norepinephrine_to_fear']
            )

        # 4. Acetylcholine → Anticipation
        acetylcholine_level = self.neuro_systems['acetylcholine'].ach_level

        modulation['anticipation_boost_ach'] = self._clamp_modulation(
            acetylcholine_level * self.backward_weights['acetylcholine_to_anticipation']
        )

        # 5. GABA → Fear reduction + Anger reduction (calming)
        gaba_level = self.neuro_systems['gaba'].gaba_level
        modulation['fear_reduction'] = self._clamp_modulation(
            gaba_level * self.backward_weights['gaba_to_fear']
        )
        modulation['anger_reduction'] = self._clamp_modulation(
            gaba_level * self.backward_weights['gaba_to_anger']
        )

        return modulation

    def _clamp_modulation(self, value: float) -> float:
        """
        Clamp modulation to prevent runaway feedback

        Parameters:
        -----------
        value : float
            Raw modulation value

        Returns:
        --------
        clamped_value : float
            Value clamped to [-MAX_MODULATION, +MAX_MODULATION]
        """
        return max(-self.MAX_MODULATION, min(self.MAX_MODULATION, value))

    # ========================================================================
    # FULL INTEGRATION CYCLE
    # ========================================================================

    def process_event(
        self,
        emotional_state: EmotionalState,
        somatic_marker: SomaticMarker
    ) -> Dict:
        """
        Full bidirectional integration cycle

        1. Forward pass: Emotions → Neurotransmitters
        2. Process neurotransmitter systems internally
        3. Backward pass: Neurotransmitters → Emotional modulation

        Parameters:
        -----------
        emotional_state : EmotionalState
            Current emotional state
        somatic_marker : SomaticMarker
            Current somatic marker

        Returns:
        --------
        result : Dict
            {
                'neuro_state': Dict[str, float],
                'emotional_modulation': Dict[str, float]
            }
        """
        # 1. Forward pass
        neuro_state = self.forward_pass(emotional_state, somatic_marker)

        # 2. Update neurotransmitter systems (simulate processing)
        # Dopamine
        self.neuro_systems['dopamine'].motivation_level = neuro_state['dopamine']

        # Serotonin
        self.neuro_systems['serotonin'].mood_level = neuro_state['serotonin']

        # Norepinephrine
        self.neuro_systems['norepinephrine'].arousal_level = neuro_state['norepinephrine']

        # Acetylcholine (set ach_level)
        self.neuro_systems['acetylcholine'].ach_level = neuro_state['acetylcholine']

        # GABA
        self.neuro_systems['gaba'].gaba_level = neuro_state['gaba']

        # 3. Backward pass
        emotional_modulation = self.backward_pass()

        return {
            'neuro_state': neuro_state,
            'emotional_modulation': emotional_modulation
        }

    # ========================================================================
    # STATE INSPECTION
    # ========================================================================

    def get_neuro_state(self) -> Dict[str, float]:
        """
        Get current neurotransmitter levels

        Returns:
        --------
        neuro_state : Dict[str, float]
        """
        return {
            'dopamine': self.neuro_systems['dopamine'].motivation_level,
            'serotonin': self.neuro_systems['serotonin'].mood_level,
            'norepinephrine': self.neuro_systems['norepinephrine'].arousal_level,
            'acetylcholine': self.neuro_systems['acetylcholine'].ach_level,
            'gaba': self.neuro_systems['gaba'].gaba_level
        }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Test bridge
    bridge = NeuroEmotionalBridge()

    # Simulate positive emotional event (breakthrough)
    emotional_state = EmotionalState(
        joy=0.9,
        anticipation=0.85,
        trust=0.8
    )
    somatic_marker = SomaticMarker(
        valence=0.9,
        arousal=0.7,
        situation="breakthrough"
    )

    print("=" * 60)
    print("NEURO-EMOTIONAL BRIDGE TEST")
    print("=" * 60)

    print("\n📊 INPUT:")
    print(f"  Emotional State:")
    print(f"    Joy: {emotional_state.joy:.2f}")
    print(f"    Anticipation: {emotional_state.anticipation:.2f}")
    print(f"    Trust: {emotional_state.trust:.2f}")
    print(f"  Somatic Marker:")
    print(f"    Valence: {somatic_marker.valence:.2f}")
    print(f"    Arousal: {somatic_marker.arousal:.2f}")

    # Process event
    result = bridge.process_event(emotional_state, somatic_marker)

    print("\n🧪 NEUROTRANSMITTER LEVELS (Forward Pass):")
    for neuro_type, level in result['neuro_state'].items():
        print(f"  {neuro_type.capitalize()}: {level:.3f}")

    print("\n⚡ EMOTIONAL MODULATION (Backward Pass):")
    for modulation_type, value in result['emotional_modulation'].items():
        sign = "+" if value >= 0 else ""
        print(f"  {modulation_type}: {sign}{value:.3f}")

    print("\n✅ Integration complete")
