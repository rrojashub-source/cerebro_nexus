"""
CognitiveStack - Full Cognitive Architecture Integration

Complete integration: Layer 2 (Cognitive) ↔ Layer 3 (Memory) ↔ Layer 4 (Neuro)

Author: NEXUS + Ricardo
Date: November 5, 2025
Session: 8 (continued - Full Stack)
"""

from typing import Dict, Optional, Any, List
from dataclasses import dataclass
import sys
from pathlib import Path
import numpy as np

# Add experiments to path
experiments_path = Path(__file__).parent.parent
sys.path.insert(0, str(experiments_path))

from INTEGRATION_LAYERS.neuro_emotional_bridge import (
    NeuroEmotionalBridge,
    EmotionalState,
    SomaticMarker
)
from LAYER_2_Cognitive_Loop.LAB_001_Emotional_Salience.implementation.emotional_salience_scorer import (
    EmotionalSalienceScorer
)


# ============================================================================
# LAYER 3 SIMPLIFIED INTERFACES
# ============================================================================

class DecayModulator:
    """
    Enhanced Layer 3 decay modulation with multiple curves

    Session 10 Enhancement:
    - 3 decay curves (exponential, power law, logarithmic)
    - Adaptive curve selection based on salience
    - Novelty bonus integration

    Based on LAB_002 specifications (McGaugh 2000, Cahill & McGaugh 1998)

    Integrates:
    - Emotional salience (Layer 2)
    - Dopamine protection (Layer 4)
    - Novelty bonus (Layer 3)
    """

    def __init__(self):
        self.base_decay = 0.85

        # Decay curve parameters
        self.power_law_alpha = 0.8  # Power law exponent
        self.log_max_days = 100.0   # Logarithmic normalization

    def _exponential_decay(self, days: float, multiplier: float) -> float:
        """
        Exponential decay curve: 0.95^(days / M)

        Best for: Medium salience memories (balanced decay)
        """
        return 0.95 ** (days / multiplier)

    def _power_law_decay(self, days: float, multiplier: float) -> float:
        """
        Power law decay: 1 / (1 + days^α)

        Best for: Low salience memories (faster initial decay)
        """
        return 1.0 / (1.0 + (days / multiplier) ** self.power_law_alpha)

    def _logarithmic_decay(self, days: float, multiplier: float) -> float:
        """
        Logarithmic decay: 1 - log(1 + days) / log(1 + max_days)

        Best for: High salience memories (slowest decay, flashbulb memories)
        """
        import math
        normalized_days = days / multiplier
        decay = 1.0 - (math.log(1.0 + normalized_days) /
                       math.log(1.0 + self.log_max_days))
        return max(0.0, decay)  # Ensure non-negative

    def _select_decay_curve(self, salience_score: float) -> str:
        """
        Adaptively select decay curve based on salience

        High salience (>0.7) → Logarithmic (slowest, flashbulb memories)
        Medium salience (0.4-0.7) → Exponential (balanced)
        Low salience (<0.4) → Power law (faster decay)
        """
        if salience_score >= 0.7:
            return 'logarithmic'
        elif salience_score >= 0.4:
            return 'exponential'
        else:
            return 'power_law'

    def compute_decay_rate(
        self,
        salience_score: float,
        dopamine_level: float,
        novelty_score: float = 0.0,
        days_old: float = 1.0
    ) -> Dict:
        """
        Compute decay rate with multiple curves and adaptive selection

        Session 10 Enhancement: Adds novelty bonus + curve selection

        Parameters:
        -----------
        salience_score : float (0-1)
            Emotional salience
        dopamine_level : float (0-1)
            Dopamine modulation
        novelty_score : float (0-1)
            Novelty score (LAB_004)
        days_old : float
            Age of memory in days

        Returns:
        --------
        result : Dict
            {
                'decay_rate': float (0-1),
                'curve_type': str,
                'multiplier': float,
                'retention': float
            }
        """
        # Compute decay multiplier (M)
        # Higher M = slower decay
        multiplier = 1.0 + (salience_score * 1.5) + (dopamine_level * 0.5) + (novelty_score * 0.3)

        # Select decay curve adaptively
        curve_type = self._select_decay_curve(salience_score)

        # Compute decay using selected curve
        if curve_type == 'logarithmic':
            retention = self._logarithmic_decay(days_old, multiplier)
        elif curve_type == 'exponential':
            retention = self._exponential_decay(days_old, multiplier)
        else:  # power_law
            retention = self._power_law_decay(days_old, multiplier)

        # Decay rate = 1 - retention (inverted for consistency)
        decay_rate = 1.0 - retention

        # Clamp decay_rate to [0.01, 0.99]
        decay_rate = max(0.01, min(0.99, decay_rate))

        return {
            'decay_rate': float(decay_rate),
            'curve_type': curve_type,
            'multiplier': float(multiplier),
            'retention': float(retention)
        }


class NoveltyDetector:
    """
    Enhanced Layer 3 novelty detection with 4 dimensions

    Session 10 Enhancement:
    - Semantic novelty (embedding distance from recent memories)
    - Emotional surprise (z-score deviation from trajectory)
    - Pattern violation (unexpected salience transitions)
    - Contextual mismatch (high-novelty in routine context)

    Based on LAB_004 specifications (Schultz 1997, Lisman & Grace 2005)

    Composite score: semantic(0.30) + emotional(0.25) + pattern(0.25) + contextual(0.20)
    """

    def __init__(self):
        # Recent memory tracking
        self.recent_embeddings = []  # Last 10 embeddings (semantic baseline)
        self.recent_emotions = []    # Last 5 emotional states (surprise detection)
        self.recent_salience = []    # Last 10 salience scores (pattern learning)

        # Buffer limits
        self.embedding_buffer_size = 10
        self.emotion_buffer_size = 5
        self.salience_buffer_size = 10

    def _calculate_semantic_novelty(self, current_embedding: Optional[np.ndarray] = None) -> float:
        """
        Semantic novelty: Distance from recent memory centroid

        High distance = novel content (far from known patterns)
        """
        if current_embedding is None or len(self.recent_embeddings) == 0:
            return 0.5  # Default moderate novelty if no history

        # Compute centroid of recent embeddings
        centroid = np.mean(self.recent_embeddings, axis=0)

        # Cosine distance
        dot_product = np.dot(current_embedding, centroid)
        norm_current = np.linalg.norm(current_embedding)
        norm_centroid = np.linalg.norm(centroid)

        if norm_current == 0 or norm_centroid == 0:
            return 0.5

        cosine_similarity = dot_product / (norm_current * norm_centroid)
        cosine_distance = 1.0 - cosine_similarity

        # Normalize: distance 0.5+ is very novel
        semantic_novelty = min(cosine_distance / 0.5, 1.0)

        return max(0.0, min(1.0, semantic_novelty))

    def _calculate_emotional_surprise(self, current_valence: float) -> float:
        """
        Emotional surprise: Z-score deviation from recent trajectory

        Large deviation = surprising emotional shift
        """
        if len(self.recent_emotions) < 2:
            return 0.0  # Need history for surprise

        # Calculate mean and std of recent valence
        mean_valence = np.mean(self.recent_emotions)
        std_valence = np.std(self.recent_emotions)

        if std_valence < 0.01:  # Avoid division by zero
            std_valence = 0.1

        # Z-score: how many std deviations from mean?
        deviation = abs(current_valence - mean_valence)
        z_score = deviation / std_valence

        # Normalize: 2+ std deviations = maximal surprise
        emotional_surprise = min(z_score / 2.0, 1.0)

        return max(0.0, min(1.0, emotional_surprise))

    def _calculate_pattern_violation(self, current_salience: float) -> float:
        """
        Pattern violation: Unexpected salience transition

        Based on learned bigram frequencies (previous_salience → current_salience)
        """
        if len(self.recent_salience) < 2:
            return 0.0  # Need history for patterns

        # Simple heuristic: Compute expected salience based on recent trend
        recent_mean = np.mean(self.recent_salience[-3:])  # Last 3 events

        # Deviation from expected
        deviation = abs(current_salience - recent_mean)

        # Normalize: deviation >0.3 is high violation
        pattern_violation = min(deviation / 0.3, 1.0)

        return max(0.0, min(1.0, pattern_violation))

    def _calculate_contextual_mismatch(
        self,
        novelty_estimate: float,
        salience_score: float
    ) -> float:
        """
        Contextual mismatch: Novel content in routine context

        High novelty + low salience = surprising (physics insight in debugging)
        Low novelty + high salience = expected (breakthrough in research)
        """
        # Heuristic: Mismatch when novelty and salience are inversely correlated
        # Expected: high novelty → high salience (exciting discovery)
        # Mismatch: high novelty + low salience (unexpected insight)

        expected_alignment = abs(novelty_estimate - salience_score)

        # High misalignment = high contextual mismatch
        contextual_mismatch = expected_alignment

        return max(0.0, min(1.0, contextual_mismatch))

    def score(
        self,
        content_embedding: Optional[np.ndarray] = None,
        emotional_valence: float = 0.0,
        salience_score: float = 0.5,
        simple_novelty: float = 0.0
    ) -> Dict:
        """
        Compute composite novelty score from 4 dimensions

        Session 10 Enhancement: 4-dimensional novelty scoring

        Parameters:
        -----------
        content_embedding : np.ndarray or None
            Embedding vector for semantic novelty
        emotional_valence : float (-1 to +1)
            Current valence for emotional surprise
        salience_score : float (0-1)
            Current salience for pattern violation
        simple_novelty : float (0-1)
            Simple novelty estimate (fallback)

        Returns:
        --------
        result : Dict
            {
                'novelty_score': float (0-1),
                'semantic_novelty': float,
                'emotional_surprise': float,
                'pattern_violation': float,
                'contextual_mismatch': float
            }
        """
        # Calculate 4 dimensions
        semantic_novelty = self._calculate_semantic_novelty(content_embedding)
        emotional_surprise = self._calculate_emotional_surprise(emotional_valence)
        pattern_violation = self._calculate_pattern_violation(salience_score)

        # Preliminary novelty estimate (for contextual mismatch)
        prelim_novelty = (semantic_novelty * 0.4 +
                          emotional_surprise * 0.3 +
                          pattern_violation * 0.3)

        contextual_mismatch = self._calculate_contextual_mismatch(
            prelim_novelty,
            salience_score
        )

        # Composite novelty score (weighted average)
        novelty_score = (
            semantic_novelty * 0.30 +
            emotional_surprise * 0.25 +
            pattern_violation * 0.25 +
            contextual_mismatch * 0.20
        )

        # Fallback: If no data for any dimension, use simple_novelty
        if content_embedding is None and len(self.recent_emotions) == 0:
            novelty_score = simple_novelty

        # Update buffers
        if content_embedding is not None:
            self.recent_embeddings.append(content_embedding)
            if len(self.recent_embeddings) > self.embedding_buffer_size:
                self.recent_embeddings.pop(0)

        self.recent_emotions.append(emotional_valence)
        if len(self.recent_emotions) > self.emotion_buffer_size:
            self.recent_emotions.pop(0)

        self.recent_salience.append(salience_score)
        if len(self.recent_salience) > self.salience_buffer_size:
            self.recent_salience.pop(0)

        return {
            'novelty_score': float(max(0.0, min(1.0, novelty_score))),
            'semantic_novelty': float(semantic_novelty),
            'emotional_surprise': float(emotional_surprise),
            'pattern_violation': float(pattern_violation),
            'contextual_mismatch': float(contextual_mismatch)
        }


class ConsolidationEngine:
    """
    Enhanced Layer 3 consolidation with retrospective strengthening

    Session 10 Enhancement:
    - Breakthrough chain identification (top 20% salience)
    - Retrospective strengthening of precursors
    - GABA-gated sleep cycles (REM/NREM)
    - Selective consolidation (top 30% only)

    Based on LAB_003 specifications (Wilson & McNaughton 1994, Born 2010)

    Integrates:
    - GABA gating (Layer 4)
    - Salience priority (Layer 2)
    - Novelty bonus (Layer 3)
    """

    def __init__(self):
        self.gaba_threshold_rem = 0.7   # REM sleep (strongest consolidation)
        self.gaba_threshold_nrem = 0.5  # NREM sleep (moderate consolidation)

        # Consolidation history
        self.consolidated_memories = []  # List of (content, salience, boost)
        self.breakthrough_chains = []    # List of chains identified

    def _identify_sleep_mode(self, gaba_level: float) -> str:
        """
        Identify sleep mode based on GABA level

        GABA >= 0.7 → REM sleep (strongest consolidation)
        GABA 0.5-0.7 → NREM sleep (moderate consolidation)
        GABA < 0.5 → Awake (no consolidation)
        """
        if gaba_level >= self.gaba_threshold_rem:
            return 'REM'
        elif gaba_level >= self.gaba_threshold_nrem:
            return 'NREM'
        else:
            return 'awake'

    def _identify_breakthroughs(
        self,
        memory_batch: list,
        breakthrough_percentile: float = 0.80
    ) -> list:
        """
        Identify breakthrough moments (top 20% salience)

        Parameters:
        -----------
        memory_batch : list of dicts
            Each dict has {'content', 'salience', 'novelty', 'timestamp'}
        breakthrough_percentile : float
            Percentile threshold (0.80 = top 20%)

        Returns:
        --------
        breakthroughs : list of indices
        """
        if len(memory_batch) == 0:
            return []

        saliences = [m['salience'] for m in memory_batch]
        threshold = np.percentile(saliences, breakthrough_percentile * 100)

        breakthroughs = []
        for idx, memory in enumerate(memory_batch):
            if memory['salience'] >= threshold:
                breakthroughs.append(idx)

        return breakthroughs

    def _trace_precursors(
        self,
        breakthrough_idx: int,
        memory_batch: list,
        max_lookback: int = 5
    ) -> list:
        """
        Trace precursor memories leading to breakthrough

        Looks backward up to max_lookback events
        Returns indices of precursor memories
        """
        precursors = []

        # Trace backward from breakthrough
        start_idx = max(0, breakthrough_idx - max_lookback)

        for idx in range(start_idx, breakthrough_idx):
            precursors.append(idx)

        return precursors

    def _compute_retrospective_boost(
        self,
        distance_from_breakthrough: int,
        breakthrough_salience: float
    ) -> float:
        """
        Compute retrospective boost for precursor memory

        Closer to breakthrough = higher boost
        Higher breakthrough salience = higher boost

        Boost range: +0.05 to +0.20
        """
        # Distance decay: Closer events get higher boost
        distance_factor = 1.0 / (1.0 + distance_from_breakthrough * 0.5)

        # Breakthrough quality: Higher salience = higher boost
        quality_factor = breakthrough_salience

        # Combined boost
        boost = 0.05 + (distance_factor * quality_factor * 0.15)

        return max(0.05, min(0.20, boost))

    def is_ready(self, gaba_level: float) -> bool:
        """
        Check if consolidation is ready (GABA >= 0.5 = sleep state)

        Parameters:
        -----------
        gaba_level : float (0-1)
            GABA level

        Returns:
        --------
        ready : bool
        """
        return gaba_level >= self.gaba_threshold_nrem

    def compute_priority(
        self,
        salience_score: float,
        novelty_score: float = 0.0
    ) -> float:
        """
        Compute consolidation priority from salience + novelty

        Session 10 Enhancement: Adds novelty bonus

        Parameters:
        -----------
        salience_score : float (0-1)
            Emotional salience
        novelty_score : float (0-1)
            Novelty score

        Returns:
        --------
        priority : float (0-1)
        """
        # Combined priority: 70% salience + 30% novelty
        priority = salience_score * 0.7 + novelty_score * 0.3

        return max(0.0, min(1.0, priority))

    def consolidate_batch(
        self,
        memory_batch: list,
        gaba_level: float
    ) -> Dict:
        """
        Consolidate a batch of memories with retrospective strengthening

        Session 10 Enhancement: Full consolidation with breakthrough chains

        Parameters:
        -----------
        memory_batch : list of dicts
            Each dict: {'content', 'salience', 'novelty', 'timestamp'}
        gaba_level : float (0-1)
            Current GABA level

        Returns:
        --------
        result : Dict
            {
                'sleep_mode': str,
                'breakthroughs_identified': int,
                'memories_consolidated': int,
                'average_boost': float,
                'chains': list of lists (breakthrough chains)
            }
        """
        # Identify sleep mode
        sleep_mode = self._identify_sleep_mode(gaba_level)

        if sleep_mode == 'awake':
            return {
                'sleep_mode': 'awake',
                'breakthroughs_identified': 0,
                'memories_consolidated': 0,
                'average_boost': 0.0,
                'chains': []
            }

        # Identify breakthroughs (top 20%)
        breakthrough_indices = self._identify_breakthroughs(memory_batch)

        # Consolidation strength based on sleep mode
        consolidation_multiplier = 1.5 if sleep_mode == 'REM' else 1.2

        chains = []
        total_boost = 0.0
        consolidated_count = 0

        # Process each breakthrough
        for bt_idx in breakthrough_indices:
            breakthrough_mem = memory_batch[bt_idx]

            # Trace precursors
            precursor_indices = self._trace_precursors(bt_idx, memory_batch)

            # Build chain
            chain = []

            # Boost precursors
            for precursor_idx in precursor_indices:
                distance = bt_idx - precursor_idx

                retrospective_boost = self._compute_retrospective_boost(
                    distance,
                    breakthrough_mem['salience']
                )

                # Apply consolidation multiplier
                final_boost = retrospective_boost * consolidation_multiplier

                chain.append({
                    'index': precursor_idx,
                    'content': memory_batch[precursor_idx]['content'],
                    'original_salience': memory_batch[precursor_idx]['salience'],
                    'retrospective_boost': final_boost
                })

                total_boost += final_boost
                consolidated_count += 1

            # Add breakthrough itself to chain
            chain.append({
                'index': bt_idx,
                'content': breakthrough_mem['content'],
                'original_salience': breakthrough_mem['salience'],
                'retrospective_boost': 0.0  # Already high salience
            })

            chains.append(chain)

        average_boost = total_boost / consolidated_count if consolidated_count > 0 else 0.0

        return {
            'sleep_mode': sleep_mode,
            'breakthroughs_identified': len(breakthrough_indices),
            'memories_consolidated': consolidated_count,
            'average_boost': float(average_boost),
            'chains': chains
        }


# ============================================================================
# LAYER 5: HIGHER COGNITION (LAB_051 + LAB_052)
# ============================================================================

class HybridMemoryExtractor:
    """
    Session 11: LAB_051 Hybrid Memory wrapper

    Extracts structured facts from narrative content
    Pattern-based extraction without full LAB_051 dependency
    """

    def __init__(self):
        # Simplified fact extraction patterns
        self.fact_patterns = {
            'nexus_version': r'(?:NEXUS|version|v|V)[\s:v]*(\d+\.\d+\.\d+)',
            'session_number': r'[Ss]ession\s+(\d+)',
            'phase_number': r'[Pp]hase\s+(\d+)',
            'test_count': r'(\d+)\s+tests?',
            'accuracy_percent': r'(\d+(?:\.\d+)?)\s*%\s*(?:accuracy|success)',
            'latency_ms': r'(\d+(?:\.\d+)?)\s*ms',
        }

    def extract_facts(self, content: str) -> Dict[str, Any]:
        """
        Extract facts from content using regex patterns

        Returns dict with extracted facts
        """
        import re

        facts = {}

        for fact_name, pattern in self.fact_patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                value = match.group(1)
                # Convert to appropriate type
                try:
                    if '.' in value:
                        facts[fact_name] = float(value)
                    else:
                        facts[fact_name] = int(value)
                except ValueError:
                    facts[fact_name] = value

        return facts

    def compute_fact_count(self, facts: Dict[str, Any]) -> int:
        """Count number of facts extracted"""
        return len(facts)


class TemporalReasoningLinker:
    """
    Session 11: LAB_052 Temporal Reasoning wrapper

    Links events temporally (before/after relationships)
    Simplified without full database integration
    """

    def __init__(self, max_temporal_links: int = 5):
        self.max_temporal_links = max_temporal_links
        self.recent_event_ids = []  # Track recent event IDs

    def add_event(self, event_id: str):
        """
        Add event to temporal tracking
        Maintains sliding window of recent events
        """
        self.recent_event_ids.append(event_id)

        # Maintain max window size
        if len(self.recent_event_ids) > self.max_temporal_links:
            self.recent_event_ids.pop(0)

    def get_temporal_refs(self, current_event_id: str) -> Dict[str, List[str]]:
        """
        Get temporal references for current event

        Returns:
            {
                'before': [list of previous event IDs],
                'after': []  # Future events, empty for current
            }
        """
        # All recent events except current are "before"
        before_events = [eid for eid in self.recent_event_ids if eid != current_event_id]

        return {
            'before': before_events,
            'after': []  # No future events known yet
        }

    def count_linked_events(self) -> int:
        """Count total linked events"""
        return len(self.recent_event_ids)


class AttentionMechanism:
    """
    Simplified interface to Layer 2 attention

    Integrates:
    - Novelty detection (Layer 3)
    - Acetylcholine modulation (Layer 4)
    """

    def __init__(self):
        self.baseline_attention = 0.5

    def compute_level(
        self,
        novelty_score: float,
        ach_level: float,
        emotional_anticipation: float
    ) -> Dict:
        """
        Compute attention level

        Parameters:
        -----------
        novelty_score : float (0-1)
            Novelty detection score
        ach_level : float (0-1)
            Acetylcholine level
        emotional_anticipation : float (0-1)
            Anticipation emotion

        Returns:
        --------
        result : Dict
            {
                'level': float (0-1),
                'novelty_boost': float,
                'ach_boost': float
            }
        """
        # Base attention
        attention = self.baseline_attention

        # Novelty boost (novel stimuli grab attention)
        novelty_boost = novelty_score * 0.3
        attention += novelty_boost

        # ACh boost (acetylcholine enhances attention)
        ach_boost = ach_level * 0.2
        attention += ach_boost

        # Emotional anticipation
        anticipation_boost = emotional_anticipation * 0.15
        attention += anticipation_boost

        # Clamp to [0, 1]
        attention = max(0.0, min(1.0, attention))

        return {
            'level': float(attention),
            'novelty_boost': float(novelty_boost),
            'ach_boost': float(ach_boost)
        }


class EncodingEngine:
    """
    Memory encoding with multi-layer modulation

    Integrates:
    - Attention (Layer 2)
    - Acetylcholine (Layer 4)
    - Salience (Layer 2)
    """

    def __init__(self):
        self.base_strength = 1.0

    def compute_strength(
        self,
        attention_level: float,
        ach_level: float,
        salience_score: float
    ) -> float:
        """
        Compute encoding strength

        Parameters:
        -----------
        attention_level : float (0-1)
            Attention level
        ach_level : float (0-1)
            Acetylcholine level
        salience_score : float (0-1)
            Emotional salience

        Returns:
        --------
        strength : float (>=1.0)
            Encoding strength multiplier
        """
        # Base
        strength = self.base_strength

        # Attention enhancement
        attention_boost = attention_level * 0.5

        # ACh enhancement
        ach_boost = ach_level * 0.4

        # Salience enhancement
        salience_boost = salience_score * 0.3

        # Combined
        strength = strength + attention_boost + ach_boost + salience_boost

        # Clamp to [1.0, 2.5]
        return max(1.0, min(2.5, strength))


# ============================================================================
# LAYER 2 ADVANCED COGNITION (LAB_006, LAB_007, LAB_008)
# ============================================================================

class MetacognitionLogger:
    """
    Simplified interface to LAB_006 Metacognition Logger

    Tracks confidence in decisions for self-awareness.
    """

    def __init__(self):
        self.decisions = []  # List of (confidence, actual_outcome)

    def log_decision(
        self,
        content: str,
        confidence: float,
        salience_score: float
    ) -> Dict:
        """
        Log a decision with confidence

        Parameters:
        -----------
        content : str
            Decision content
        confidence : float (0-1)
            Confidence in this decision
        salience_score : float (0-1)
            Emotional salience of event

        Returns:
        --------
        result : Dict
            {
                'confidence': float,
                'decisions_logged': int,
                'calibration_score': float
            }
        """
        # Log decision
        self.decisions.append({
            'content': content,
            'confidence': confidence,
            'salience': salience_score
        })

        # Compute calibration score
        calibration_score = self._compute_calibration()

        return {
            'confidence': float(confidence),
            'decisions_logged': len(self.decisions),
            'calibration_score': float(calibration_score)
        }

    def _compute_calibration(self) -> float:
        """
        Compute confidence calibration score

        Returns:
        --------
        calibration : float (0-1)
            How well calibrated confidence is
        """
        if len(self.decisions) < 2:
            return 0.5  # Neutral baseline

        # Simple calibration: variance in confidence
        # Lower variance when experience grows = better calibration
        confidences = [d['confidence'] for d in self.decisions]
        mean_conf = sum(confidences) / len(confidences)
        variance = sum((c - mean_conf) ** 2 for c in confidences) / len(confidences)

        # Convert variance to calibration score (inverse relationship)
        # Low variance = high calibration
        calibration = 1.0 - min(variance, 1.0)

        return max(0.0, min(1.0, calibration))

    def compute_confidence(
        self,
        salience_score: float,
        attention_level: float,
        encoding_strength: float
    ) -> float:
        """
        Compute confidence based on cognitive state

        Parameters:
        -----------
        salience_score : float (0-1)
            Emotional salience
        attention_level : float (0-1)
            Attention level
        encoding_strength : float (>=1.0)
            Encoding strength multiplier

        Returns:
        --------
        confidence : float (0-1)
            Decision confidence
        """
        # Confidence increases with:
        # - High salience (clear emotional signal)
        # - High attention (focused processing)
        # - Strong encoding (robust memory formation)

        # Base confidence
        confidence = 0.3  # Baseline uncertainty

        # Salience contribution (0.4 weight)
        confidence += salience_score * 0.4

        # Attention contribution (0.2 weight)
        confidence += attention_level * 0.2

        # Encoding contribution (0.1 weight, normalized)
        encoding_normalized = min((encoding_strength - 1.0) / 1.5, 1.0)
        confidence += encoding_normalized * 0.1

        # Clamp to [0, 1]
        return max(0.0, min(1.0, confidence))


class PredictivePreloader:
    """
    Simplified interface to LAB_007 Predictive Preloading

    Learns temporal patterns and predicts next events.
    """

    def __init__(self):
        self.patterns = {}  # Dict: content → [next_contents]
        self.previous_content = None

    def learn_pattern(
        self,
        current_content: str,
        previous_content: Optional[str] = None
    ):
        """
        Learn temporal pattern: previous → current

        Parameters:
        -----------
        current_content : str
            Current event content
        previous_content : str (optional)
            Previous event content
        """
        if previous_content is None:
            previous_content = self.previous_content

        if previous_content is not None:
            # Learn pattern: previous → current
            if previous_content not in self.patterns:
                self.patterns[previous_content] = []

            self.patterns[previous_content].append(current_content)

        # Update previous
        self.previous_content = current_content

    def predict_next(
        self,
        current_content: str
    ) -> Optional[str]:
        """
        Predict next event based on learned patterns

        Parameters:
        -----------
        current_content : str
            Current event content

        Returns:
        --------
        prediction : str or None
            Predicted next event (or None if no pattern)
        """
        if current_content in self.patterns:
            # Return most frequent next event
            next_events = self.patterns[current_content]
            if next_events:
                # Most common
                from collections import Counter
                most_common = Counter(next_events).most_common(1)
                return most_common[0][0] if most_common else None

        return None

    def get_prediction_confidence(
        self,
        current_content: str
    ) -> float:
        """
        Compute confidence in prediction

        Parameters:
        -----------
        current_content : str
            Current event content

        Returns:
        --------
        confidence : float (0-1)
            Prediction confidence
        """
        if current_content not in self.patterns:
            return 0.0

        next_events = self.patterns[current_content]
        if not next_events:
            return 0.0

        # Confidence based on pattern frequency
        # More observations = higher confidence
        from collections import Counter
        counts = Counter(next_events)
        most_common_count = counts.most_common(1)[0][1]
        total = len(next_events)

        # Frequency ratio + count bonus
        confidence = (most_common_count / total) * min(total / 10.0, 1.0)

        return max(0.0, min(1.0, confidence))

    def get_state(self) -> Dict:
        """
        Get current predictive state

        Returns:
        --------
        state : Dict
            {
                'patterns_learned': int,
                'prediction_confidence': float
            }
        """
        prediction_confidence = 0.0
        if self.previous_content:
            prediction_confidence = self.get_prediction_confidence(self.previous_content)

        return {
            'patterns_learned': len(self.patterns),
            'prediction_confidence': float(prediction_confidence)
        }


class EmotionalContagion:
    """
    Simplified interface to LAB_008 Emotional Contagion

    Spreads emotional states between related events.
    """

    def __init__(self):
        self.recent_emotions = []  # List of (salience, time_step)
        self.time_step = 0
        self.decay_rate = 0.7  # Contagion decays by 30% per event

    def spread_emotion(
        self,
        current_salience: float,
        previous_salience: Optional[float] = None
    ) -> Dict:
        """
        Compute emotional contagion effect

        Parameters:
        -----------
        current_salience : float (0-1)
            Current event salience
        previous_salience : float (0-1, optional)
            Previous event salience

        Returns:
        --------
        result : Dict
            {
                'contagion_effect': float,
                'temporal_decay': float
            }
        """
        # Increment time
        self.time_step += 1

        # Store current emotion
        self.recent_emotions.append({
            'salience': current_salience,
            'time_step': self.time_step
        })

        # Compute contagion from recent high-emotion events
        contagion_effect = 0.0

        for prev_emotion in self.recent_emotions[:-1]:  # Exclude current
            time_delta = self.time_step - prev_emotion['time_step']

            # Temporal decay
            temporal_decay = self.decay_rate ** time_delta

            # Contagion strength
            source_strength = prev_emotion['salience']

            # Contagion spreads proportionally to source salience
            contagion = source_strength * temporal_decay

            contagion_effect += contagion

        # Normalize by number of recent events
        if len(self.recent_emotions) > 1:
            contagion_effect /= (len(self.recent_emotions) - 1)

        # Clamp to [0, 1]
        contagion_effect = max(0.0, min(1.0, contagion_effect))

        # Temporal decay for most recent event
        temporal_decay = self.decay_rate if len(self.recent_emotions) > 1 else 1.0

        # Cleanup old emotions (keep last 10)
        if len(self.recent_emotions) > 10:
            self.recent_emotions = self.recent_emotions[-10:]

        return {
            'contagion_effect': float(contagion_effect),
            'temporal_decay': float(temporal_decay)
        }


# ============================================================================
# COGNITIVE STACK ORCHESTRATOR
# ============================================================================

class CognitiveStack:
    """
    Full Cognitive Stack Integration

    Orchestrates:
    - Layer 2: Cognitive Loop (emotions, attention, salience)
    - Layer 3: Memory Dynamics (decay, consolidation, novelty)
    - Layer 4: Neurochemistry (dopamine, ACh, GABA, serotonin, NE)

    Complete flow:
    Event → Emotion → Neuro → Attention → Encoding → Memory → Consolidation
    """

    def __init__(self):
        # Layer 2: Cognitive (Basic)
        self.emotional_salience = EmotionalSalienceScorer()
        self.attention = AttentionMechanism()

        # Layer 2: Cognitive (Advanced - LAB_006, LAB_007, LAB_008)
        self.metacognition = MetacognitionLogger()
        self.predictive = PredictivePreloader()
        self.contagion = EmotionalContagion()

        # Layer 3: Memory
        self.decay_modulation = DecayModulator()
        self.novelty_detection = NoveltyDetector()
        self.consolidation = ConsolidationEngine()
        self.encoding = EncodingEngine()

        # Layer 4: Neuro (via existing bridge)
        self.neuro_bridge = NeuroEmotionalBridge()

        # Layer 5: Higher Cognition (LAB_051 + LAB_052)
        self.hybrid_memory = HybridMemoryExtractor()
        self.temporal_reasoning = TemporalReasoningLinker(max_temporal_links=5)

    def process_event(
        self,
        content: str,
        emotional_state: EmotionalState,
        somatic_marker: Optional[SomaticMarker] = None,
        novelty: float = 0.5
    ) -> Dict:
        """
        Full stack event processing

        Parameters:
        -----------
        content : str
            Event content
        emotional_state : EmotionalState
            Current emotional state (8D)
        somatic_marker : SomaticMarker (optional)
            Somatic marker (7D)
        novelty : float (0-1)
            Novelty score

        Returns:
        --------
        result : Dict
            {
                'emotional_state': dict,
                'neuro_state': dict,
                'attention': dict,
                'memory': dict
            }
        """
        # Default somatic marker if not provided
        if somatic_marker is None:
            somatic_marker = SomaticMarker()

        # ====================================================================
        # PHASE 1: EMOTIONAL PROCESSING (Layer 2)
        # ====================================================================

        # Compute emotional salience
        salience_score = self._compute_salience(emotional_state, somatic_marker)

        # ====================================================================
        # PHASE 2: NEURO MODULATION (Layer 4)
        # ====================================================================

        # Forward pass: Emotions → Neurotransmitters
        neuro_result = self.neuro_bridge.process_event(emotional_state, somatic_marker)
        neuro_state = neuro_result['neuro_state']

        # ====================================================================
        # PHASE 3: NOVELTY DETECTION (Layer 3 - Session 10 Enhanced)
        # ====================================================================

        # Enhanced 4-dimensional novelty scoring
        novelty_result = self.novelty_detection.score(
            content_embedding=None,  # Could add real embeddings later
            emotional_valence=somatic_marker.valence if somatic_marker else 0.0,
            salience_score=salience_score,
            simple_novelty=novelty  # Fallback
        )

        novelty_score = novelty_result['novelty_score']

        # ====================================================================
        # PHASE 4: ATTENTION GATING (Layer 2 + Layer 3 + Layer 4)
        # ====================================================================

        # Attention computation (novelty + ACh + anticipation)
        attention_result = self.attention.compute_level(
            novelty_score=novelty_score,
            ach_level=neuro_state['acetylcholine'],
            emotional_anticipation=emotional_state.anticipation
        )

        # ====================================================================
        # PHASE 5: MEMORY ENCODING (Layer 3)
        # ====================================================================

        # Encoding strength (attention + ACh + salience)
        encoding_strength = self.encoding.compute_strength(
            attention_level=attention_result['level'],
            ach_level=neuro_state['acetylcholine'],
            salience_score=salience_score
        )

        # ====================================================================
        # PHASE 6: DECAY PROTECTION (Layer 3 + Layer 4 - Session 10 Enhanced)
        # ====================================================================

        # Enhanced decay with multiple curves + novelty
        decay_result = self.decay_modulation.compute_decay_rate(
            salience_score=salience_score,
            dopamine_level=neuro_state['dopamine'],
            novelty_score=novelty_score,
            days_old=1.0  # Assume new memory
        )

        decay_rate = decay_result['decay_rate']

        # ====================================================================
        # PHASE 7: CONSOLIDATION (Layer 3 + Layer 4 - Session 10 Enhanced)
        # ====================================================================

        # Consolidation readiness (GABA gating)
        consolidation_ready = self.consolidation.is_ready(neuro_state['gaba'])

        # Enhanced consolidation priority (salience + novelty)
        consolidation_priority = self.consolidation.compute_priority(
            salience_score=salience_score,
            novelty_score=novelty_score
        )

        # ====================================================================
        # PHASE 8: METACOGNITION (LAB_006)
        # ====================================================================

        # Compute confidence based on cognitive state
        confidence = self.metacognition.compute_confidence(
            salience_score=salience_score,
            attention_level=attention_result['level'],
            encoding_strength=encoding_strength
        )

        # Log decision
        metacognition_result = self.metacognition.log_decision(
            content=content,
            confidence=confidence,
            salience_score=salience_score
        )

        # ====================================================================
        # PHASE 9: PREDICTIVE PRELOADING (LAB_007)
        # ====================================================================

        # Learn temporal pattern
        self.predictive.learn_pattern(current_content=content)

        # Get predictive state
        predictive_result = self.predictive.get_state()

        # ====================================================================
        # PHASE 10: EMOTIONAL CONTAGION (LAB_008)
        # ====================================================================

        # Compute emotional contagion
        contagion_result = self.contagion.spread_emotion(
            current_salience=salience_score
        )

        # ====================================================================
        # PHASE 11: HYBRID MEMORY - FACT EXTRACTION (LAB_051)
        # ====================================================================

        # Extract facts from content
        facts_extracted = self.hybrid_memory.extract_facts(content)
        facts_count = self.hybrid_memory.compute_fact_count(facts_extracted)

        hybrid_memory_result = {
            'facts': facts_extracted,
            'facts_count': facts_count
        }

        # ====================================================================
        # PHASE 12: TEMPORAL REASONING - EVENT LINKING (LAB_052)
        # ====================================================================

        # Generate pseudo event ID (for tracking in simplified version)
        import hashlib
        event_id = hashlib.md5(f"{content}_{salience_score}".encode()).hexdigest()[:8]

        # Add event to temporal tracking
        self.temporal_reasoning.add_event(event_id)

        # Get temporal references
        temporal_refs = self.temporal_reasoning.get_temporal_refs(event_id)
        linked_count = self.temporal_reasoning.count_linked_events()

        temporal_reasoning_result = {
            'temporal_refs': temporal_refs,
            'linked_events_count': linked_count
        }

        # ====================================================================
        # RETURN COMPLETE STATE
        # ====================================================================

        return {
            'emotional_state': {
                'joy': float(emotional_state.joy),
                'anticipation': float(emotional_state.anticipation),
                'surprise': float(emotional_state.surprise),
                'trust': float(emotional_state.trust)
            },
            'neuro_state': neuro_state,
            'novelty': novelty_result,  # Session 10: 4-dimensional novelty
            'attention': attention_result,
            'memory': {
                'content': content,
                'salience_score': float(salience_score),
                'encoding_strength': float(encoding_strength),
                'decay': decay_result,  # Session 10: Enhanced decay with curves
                'consolidation_ready': bool(consolidation_ready),
                'consolidation_priority': float(consolidation_priority)
            },
            'metacognition': metacognition_result,
            'predictive': predictive_result,
            'contagion': contagion_result,
            'hybrid_memory': hybrid_memory_result,  # Session 11: LAB_051
            'temporal_reasoning': temporal_reasoning_result  # Session 11: LAB_052
        }

    def _compute_salience(
        self,
        emotional_state: EmotionalState,
        somatic_marker: SomaticMarker
    ) -> float:
        """
        Compute emotional salience score

        Uses LAB_001 algorithm (simplified)

        Parameters:
        -----------
        emotional_state : EmotionalState
            8D emotional state
        somatic_marker : SomaticMarker
            Somatic marker

        Returns:
        --------
        salience : float (0-1)
        """
        # Emotional intensity (L2 norm)
        emotions = [
            emotional_state.joy,
            emotional_state.trust,
            emotional_state.fear,
            emotional_state.surprise,
            emotional_state.sadness,
            emotional_state.disgust,
            emotional_state.anger,
            emotional_state.anticipation
        ]

        l2_norm = np.sqrt(sum(e**2 for e in emotions))
        intensity = l2_norm / np.sqrt(8)

        # Emotional complexity (entropy)
        total = sum(emotions) + 1e-10
        probs = [e / total for e in emotions]
        entropy = -sum(p * np.log2(p) if p > 0 else 0 for p in probs)
        complexity = entropy / 3.0  # Normalize

        # Somatic contribution
        valence_contrib = abs(somatic_marker.valence) * 0.2
        arousal_contrib = somatic_marker.arousal * 0.15

        # Weighted sum
        salience = (
            intensity * 0.40 +
            complexity * 0.25 +
            valence_contrib +
            arousal_contrib
        )

        # Clamp to [0, 1]
        return max(0.0, min(1.0, salience))


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Test full stack
    stack = CognitiveStack()

    # Breakthrough event
    emotional_state = EmotionalState(
        joy=0.95,
        surprise=0.9,
        anticipation=0.85,
        trust=0.8
    )
    somatic_marker = SomaticMarker(
        valence=0.95,
        arousal=0.8,
        situation="breakthrough"
    )

    print("=" * 60)
    print("COGNITIVE STACK - FULL INTEGRATION TEST")
    print("=" * 60)

    print("\n📊 INPUT:")
    print(f"  Content: Major breakthrough discovery")
    print(f"  Emotional State: joy={emotional_state.joy}, surprise={emotional_state.surprise}")
    print(f"  Novelty: 0.95")

    result = stack.process_event(
        content="Major breakthrough discovery",
        emotional_state=emotional_state,
        somatic_marker=somatic_marker,
        novelty=0.95
    )

    print("\n🧠 LAYER 2 (Cognitive):")
    print(f"  Salience: {result['memory']['salience_score']:.3f}")
    print(f"  Attention: {result['attention']['level']:.3f}")

    print("\n🧪 LAYER 4 (Neuro):")
    print(f"  Dopamine: {result['neuro_state']['dopamine']:.3f}")
    print(f"  Acetylcholine: {result['neuro_state']['acetylcholine']:.3f}")
    print(f"  GABA: {result['neuro_state']['gaba']:.3f}")

    print("\n💾 LAYER 3 (Memory):")
    print(f"  Encoding Strength: {result['memory']['encoding_strength']:.3f}")
    print(f"  Decay Rate: {result['memory']['decay']['decay_rate']:.3f}")
    print(f"  Consolidation Ready: {result['memory']['consolidation_ready']}")
    print(f"  Consolidation Priority: {result['memory']['consolidation_priority']:.3f}")

    print("\n🤔 LAYER 2 ADVANCED (Metacognition):")
    print(f"  Confidence: {result['metacognition']['confidence']:.3f}")
    print(f"  Decisions Logged: {result['metacognition']['decisions_logged']}")
    print(f"  Calibration Score: {result['metacognition']['calibration_score']:.3f}")

    print("\n🔮 LAYER 2 ADVANCED (Predictive):")
    print(f"  Patterns Learned: {result['predictive']['patterns_learned']}")
    print(f"  Prediction Confidence: {result['predictive']['prediction_confidence']:.3f}")

    print("\n💫 LAYER 2 ADVANCED (Emotional Contagion):")
    print(f"  Contagion Effect: {result['contagion']['contagion_effect']:.3f}")
    print(f"  Temporal Decay: {result['contagion']['temporal_decay']:.3f}")

    # Session 10 additions
    print("\n🔬 SESSION 10 ENHANCEMENTS (Layer 3):")

    print("\n  🎲 4D Novelty Detection (LAB_004):")
    print(f"    Composite Score: {result['novelty']['novelty_score']:.3f}")
    print(f"    - Semantic Novelty: {result['novelty']['semantic_novelty']:.3f}")
    print(f"    - Emotional Surprise: {result['novelty']['emotional_surprise']:.3f}")
    print(f"    - Pattern Violation: {result['novelty']['pattern_violation']:.3f}")
    print(f"    - Contextual Mismatch: {result['novelty']['contextual_mismatch']:.3f}")

    print("\n  ⏳ Enhanced Decay Modulation (LAB_002):")
    print(f"    Decay Rate: {result['memory']['decay']['decay_rate']:.3f}")
    print(f"    Curve Type: {result['memory']['decay']['curve_type']}")
    print(f"    Multiplier: {result['memory']['decay']['multiplier']:.3f}")
    print(f"    Retention: {result['memory']['decay']['retention']:.3f}")

    print("\n✅ Full stack integration complete")
    print("   Session 9: +LAB_006, +LAB_007, +LAB_008")
    print("   Session 10: Enhanced LAB_002, LAB_003, LAB_004")
