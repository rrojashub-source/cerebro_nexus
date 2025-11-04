"""
LAB_008: Emotional Contagion Engine

Spread emotional states across semantically related memories,
creating temporary affective overlays that bias future retrieval.

Based on neuroscience: Emotional contagion via limbic resonance
(ACC + insula), spreading patterns, and state-matching effects on memory.

Author: NEXUS (Autonomous)
Date: October 28, 2025
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple
import math
import numpy as np


# ============================================================================
# Data Structures
# ============================================================================

@dataclass
class EmotionalState:
    """8D Plutchik emotional state"""
    joy: float = 0.5
    trust: float = 0.5
    fear: float = 0.5
    surprise: float = 0.5
    sadness: float = 0.5
    disgust: float = 0.5
    anger: float = 0.5
    anticipation: float = 0.5

    @property
    def intensity(self) -> float:
        """Overall emotional intensity (0.0-1.0)"""
        # Distance from neutral (0.5)
        deviations = [abs(v - 0.5) for v in self.as_vector()]
        return np.mean(deviations) * 2.0  # Scale to 0-1

    @property
    def valence(self) -> float:
        """Emotional valence: positive (+1) to negative (-1)"""
        positive = (self.joy + self.trust + self.anticipation) / 3.0
        negative = (self.fear + self.sadness + self.anger + self.disgust) / 4.0
        return positive - negative

    def as_vector(self) -> np.ndarray:
        """Return as 8D vector"""
        return np.array([
            self.joy, self.trust, self.fear, self.surprise,
            self.sadness, self.disgust, self.anger, self.anticipation
        ])

    @staticmethod
    def from_vector(vec: np.ndarray) -> 'EmotionalState':
        """Create from 8D vector"""
        return EmotionalState(
            joy=vec[0], trust=vec[1], fear=vec[2], surprise=vec[3],
            sadness=vec[4], disgust=vec[5], anger=vec[6], anticipation=vec[7]
        )


@dataclass
class ContagionOverlay:
    """Temporary emotional overlay on an episode"""
    episode_id: str
    source_episode_id: str
    propagated_emotion: EmotionalState
    intensity: float
    created_at: datetime
    semantic_distance: int  # Hops from source

    def get_effective_emotion(self) -> Tuple[EmotionalState, float]:
        """
        Get emotion with temporal decay applied.

        Returns:
            (effective_emotion, effective_intensity)
        """
        # Temporal decay (half-life: 4 hours)
        hours_since = (datetime.now() - self.created_at).total_seconds() / 3600
        time_decay = math.exp(-hours_since / 4.0)

        # Apply decay to intensity
        effective_intensity = self.intensity * time_decay

        # Scale emotion
        emotion_vector = self.propagated_emotion.as_vector()
        # Interpolate toward neutral (0.5) based on decay
        neutral = np.full(8, 0.5)
        effective_vector = neutral + (emotion_vector - neutral) * time_decay

        return EmotionalState.from_vector(effective_vector), effective_intensity


# ============================================================================
# Emotional State Propagator
# ============================================================================

class EmotionalStatePropagator:
    """
    Spread emotional states across similarity graph.

    Algorithm:
    1. Start from episode with strong emotion
    2. Find semantically related episodes (similarity graph)
    3. Propagate emotion with decay (distance + time)
    4. Create temporary contagion overlays
    """

    def __init__(
        self,
        similarity_threshold: float = 0.7,
        max_hops: int = 2,
        intensity_threshold: float = 0.6,
        valence_boost: float = 1.5
    ):
        """
        Args:
            similarity_threshold: Minimum similarity for spreading
            max_hops: Maximum semantic distance for contagion
            intensity_threshold: Minimum emotion intensity to trigger spreading
            valence_boost: Boost factor for same-valence spreading
        """
        self.similarity_threshold = similarity_threshold
        self.max_hops = max_hops
        self.intensity_threshold = intensity_threshold
        self.valence_boost = valence_boost

        # Active contagion overlays: {episode_id: [ContagionOverlay, ...]}
        self.active_overlays: Dict[str, List[ContagionOverlay]] = {}

    def propagate_emotion(
        self,
        source_episode_id: str,
        source_emotion: EmotionalState,
        similarity_graph: Dict[str, List[Tuple[str, float]]]  # {ep_id: [(related_id, similarity), ...]}
    ) -> List[ContagionOverlay]:
        """
        Propagate emotion from source episode across graph.

        Args:
            source_episode_id: Episode with strong emotion
            source_emotion: Emotional state to propagate
            similarity_graph: Graph of related episodes

        Returns:
            List of created contagion overlays
        """
        # Check if emotion strong enough to spread
        if source_emotion.intensity < self.intensity_threshold:
            return []

        # BFS spreading with distance tracking
        overlays = []
        visited = {source_episode_id}
        queue = [(source_episode_id, 0, source_emotion, 1.0)]  # (id, distance, emotion, strength)

        while queue:
            current_id, distance, current_emotion, strength = queue.pop(0)

            # Stop at max hops
            if distance >= self.max_hops:
                continue

            # Get neighbors from similarity graph
            neighbors = similarity_graph.get(current_id, [])

            for neighbor_id, similarity in neighbors:
                if neighbor_id in visited:
                    continue

                # Check similarity threshold
                if similarity < self.similarity_threshold:
                    continue

                visited.add(neighbor_id)

                # Compute propagated emotion strength
                # Factors: similarity, distance decay, valence matching
                distance_decay = math.exp(-distance * 0.5)  # Decay rate: 0.5
                propagation_strength = similarity * distance_decay * strength

                # Valence boost (same-valence spreads easier)
                # Compare source vs neighbor emotion
                # (In practice, would need neighbor's existing emotion)
                # For now, assume neutral baseline

                # Create propagated emotion (attenuated)
                propagated_vector = source_emotion.as_vector()
                neutral = np.full(8, 0.5)
                attenuated_vector = neutral + (propagated_vector - neutral) * propagation_strength

                propagated_emotion = EmotionalState.from_vector(attenuated_vector)
                propagated_intensity = source_emotion.intensity * propagation_strength

                # Create contagion overlay
                overlay = ContagionOverlay(
                    episode_id=neighbor_id,
                    source_episode_id=source_episode_id,
                    propagated_emotion=propagated_emotion,
                    intensity=propagated_intensity,
                    created_at=datetime.now(),
                    semantic_distance=distance + 1
                )

                overlays.append(overlay)

                # Store overlay
                if neighbor_id not in self.active_overlays:
                    self.active_overlays[neighbor_id] = []
                self.active_overlays[neighbor_id].append(overlay)

                # Continue spreading (weakened)
                if propagation_strength > 0.1:  # Threshold for further spreading
                    queue.append((
                        neighbor_id,
                        distance + 1,
                        propagated_emotion,
                        propagation_strength * 0.7  # Further attenuation
                    ))

        return overlays

    def get_episode_contagion(
        self,
        episode_id: str
    ) -> Optional[Tuple[EmotionalState, float]]:
        """
        Get active emotional contagion for episode (with temporal decay).

        Args:
            episode_id: Episode to check

        Returns:
            (effective_emotion, effective_intensity) or None if no active contagion
        """
        if episode_id not in self.active_overlays:
            return None

        # Get all active overlays (may have multiple sources)
        overlays = self.active_overlays[episode_id]

        # Filter out expired overlays (intensity < 0.01 after decay)
        active = []
        for overlay in overlays:
            emotion, intensity = overlay.get_effective_emotion()
            if intensity >= 0.01:
                active.append((emotion, intensity))

        if not active:
            # Clean up
            del self.active_overlays[episode_id]
            return None

        # Update overlays list
        self.active_overlays[episode_id] = [
            o for o in overlays
            if o.get_effective_emotion()[1] >= 0.01
        ]

        # Combine multiple contagions (weighted average)
        total_intensity = sum(i for _, i in active)
        combined_vector = np.zeros(8)

        for emotion, intensity in active:
            weight = intensity / total_intensity
            combined_vector += emotion.as_vector() * weight

        combined_emotion = EmotionalState.from_vector(combined_vector)
        return combined_emotion, total_intensity

    def compute_retrieval_bias(
        self,
        episode_id: str,
        query_emotion: Optional[EmotionalState],
        base_score: float
    ) -> float:
        """
        Compute retrieval bias based on emotional contagion.

        Args:
            episode_id: Episode being retrieved
            query_emotion: Query's emotional context (if any)
            base_score: Base similarity/relevance score

        Returns:
            Adjusted score with contagion bias
        """
        # Get active contagion
        contagion = self.get_episode_contagion(episode_id)
        if contagion is None:
            return base_score

        episode_emotion, intensity = contagion

        # If no query emotion, no bias
        if query_emotion is None:
            return base_score

        # Compute emotional congruence (cosine similarity in emotion space)
        query_vec = query_emotion.as_vector()
        episode_vec = episode_emotion.as_vector()

        cos_sim = np.dot(query_vec, episode_vec) / (
            np.linalg.norm(query_vec) * np.linalg.norm(episode_vec) + 1e-8
        )

        # Normalize to 0-1
        emotional_congruence = (cos_sim + 1.0) / 2.0

        # Compute boost
        # High congruence + high intensity = strong boost
        boost_factor = 1.0 + (emotional_congruence * intensity * 0.3)

        return base_score * boost_factor

    def cleanup_expired_overlays(self):
        """Remove overlays with near-zero intensity after temporal decay"""
        to_remove = []

        for episode_id, overlays in self.active_overlays.items():
            # Check if any overlay still active
            active = [
                o for o in overlays
                if o.get_effective_emotion()[1] >= 0.01
            ]

            if not active:
                to_remove.append(episode_id)
            else:
                self.active_overlays[episode_id] = active

        for episode_id in to_remove:
            del self.active_overlays[episode_id]

    def get_stats(self) -> dict:
        """Get contagion statistics"""
        total_overlays = sum(len(overlays) for overlays in self.active_overlays.values())
        episodes_affected = len(self.active_overlays)

        # Compute average intensity
        intensities = []
        for overlays in self.active_overlays.values():
            for overlay in overlays:
                _, intensity = overlay.get_effective_emotion()
                intensities.append(intensity)

        avg_intensity = np.mean(intensities) if intensities else 0.0

        return {
            'episodes_affected': episodes_affected,
            'total_overlays': total_overlays,
            'avg_intensity': avg_intensity,
            'max_intensity': max(intensities) if intensities else 0.0
        }


# ============================================================================
# Main Emotional Contagion Engine
# ============================================================================

class EmotionalContagionEngine:
    """
    Main orchestrator for LAB_008.

    Integrates emotional state propagation with memory retrieval.
    """

    def __init__(
        self,
        similarity_threshold: float = 0.7,
        max_hops: int = 2,
        intensity_threshold: float = 0.6
    ):
        self.propagator = EmotionalStatePropagator(
            similarity_threshold=similarity_threshold,
            max_hops=max_hops,
            intensity_threshold=intensity_threshold
        )

    def on_episode_access(
        self,
        episode_id: str,
        emotion: EmotionalState,
        similarity_graph: Dict[str, List[Tuple[str, float]]]
    ) -> List[ContagionOverlay]:
        """
        Called when an episode is accessed.

        If emotion is strong, propagate to related episodes.

        Args:
            episode_id: Accessed episode
            emotion: Emotional state at access time
            similarity_graph: Graph of related episodes

        Returns:
            List of created contagion overlays
        """
        return self.propagator.propagate_emotion(
            episode_id,
            emotion,
            similarity_graph
        )

    def adjust_retrieval_scores(
        self,
        candidates: List[Tuple[str, float]],  # [(episode_id, base_score), ...]
        query_emotion: Optional[EmotionalState]
    ) -> List[Tuple[str, float]]:
        """
        Adjust retrieval scores based on emotional contagion.

        Args:
            candidates: List of (episode_id, score) tuples
            query_emotion: Query's emotional context

        Returns:
            Adjusted list of (episode_id, adjusted_score) tuples
        """
        adjusted = []

        for episode_id, base_score in candidates:
            adjusted_score = self.propagator.compute_retrieval_bias(
                episode_id,
                query_emotion,
                base_score
            )
            adjusted.append((episode_id, adjusted_score))

        # Re-sort by adjusted score
        adjusted.sort(key=lambda x: x[1], reverse=True)
        return adjusted

    def cleanup(self):
        """Periodic cleanup of expired overlays"""
        self.propagator.cleanup_expired_overlays()

    def get_stats(self) -> dict:
        """Get comprehensive statistics"""
        return {
            'propagator': self.propagator.get_stats()
        }


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    # This would be integrated with NEXUS API
    # See main.py for actual integration

    print("LAB_008: Emotional Contagion Engine")
    print("=" * 60)
    print()
    print("✅ Components implemented:")
    print("  [1] EmotionalState - 8D Plutchik representation")
    print("  [2] ContagionOverlay - Temporary emotional bias")
    print("  [3] EmotionalStatePropagator - BFS spreading algorithm")
    print("  [4] EmotionalContagionEngine - Main orchestrator")
    print()
    print("Ready for integration with NEXUS API.")
