"""
LAB_009: Memory Reconsolidation Engine

Update existing memories when new related information arrives,
mimicking biological memory reconsolidation.

Based on neuroscience: Memories become labile upon retrieval + novelty,
then reconsolidate with integrated information (Nader 2000, Bayer 2025).

Author: NEXUS (Autonomous)
Date: October 28, 2025
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple, Any
from enum import Enum
import json
import numpy as np


# ============================================================================
# Data Structures
# ============================================================================

class IntegrationMode(Enum):
    """How to integrate new information with existing memory"""
    ADDITIVE = "additive"        # Add new details
    CORRECTIVE = "corrective"    # Update incorrect details
    ENRICHMENT = "enrichment"    # Add context/metadata


@dataclass
class Episode:
    """Memory episode"""
    episode_id: str
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[np.ndarray] = None
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: Optional[datetime] = None
    access_count: int = 0


@dataclass
class ReconsolidationEvent:
    """Record of a memory update via reconsolidation"""
    event_id: str
    episode_id: str
    timestamp: datetime
    original_content: str
    updated_content: str
    integration_mode: IntegrationMode
    novelty_score: float
    new_information: Dict[str, Any]
    trigger_reason: str


# ============================================================================
# Stability Window Manager
# ============================================================================

class StabilityWindow:
    """
    Track labile/stable states of memories.

    After retrieval + novelty, memory enters labile state for ~6 hours.
    During this window, memory can be updated. After window closes,
    memory becomes stable again.
    """

    def __init__(self, window_hours: float = 6.0):
        """
        Args:
            window_hours: Duration of labile window (default: 6 hours, from neuroscience)
        """
        self.window_hours = window_hours

        # {episode_id: labile_start_time}
        self.labile_memories: Dict[str, datetime] = {}

        # {episode_id: retrieval_time}
        self.recent_retrievals: Dict[str, datetime] = {}

    def mark_retrieval(self, episode_id: str):
        """Record that episode was retrieved (potential for reconsolidation)"""
        self.recent_retrievals[episode_id] = datetime.now()

    def enter_labile_state(self, episode_id: str):
        """
        Mark memory as labile (updatable).
        Called when retrieval + novelty detected.
        """
        self.labile_memories[episode_id] = datetime.now()

    def is_labile(self, episode_id: str) -> bool:
        """Check if memory is currently in labile window"""
        if episode_id not in self.labile_memories:
            return False

        elapsed = datetime.now() - self.labile_memories[episode_id]
        return elapsed.total_seconds() / 3600 < self.window_hours

    def get_labile_time_remaining(self, episode_id: str) -> Optional[float]:
        """Get hours remaining in labile window, or None if not labile"""
        if not self.is_labile(episode_id):
            return None

        elapsed = datetime.now() - self.labile_memories[episode_id]
        elapsed_hours = elapsed.total_seconds() / 3600
        return max(0, self.window_hours - elapsed_hours)

    def cleanup_expired(self):
        """Remove memories that have exited labile window"""
        current_time = datetime.now()

        expired_labile = [
            ep_id for ep_id, start_time in self.labile_memories.items()
            if (current_time - start_time).total_seconds() / 3600 >= self.window_hours
        ]

        for ep_id in expired_labile:
            del self.labile_memories[ep_id]

        # Also cleanup old retrievals (> 12 hours)
        expired_retrievals = [
            ep_id for ep_id, retrieval_time in self.recent_retrievals.items()
            if (current_time - retrieval_time).total_seconds() / 3600 >= 12
        ]

        for ep_id in expired_retrievals:
            del self.recent_retrievals[ep_id]

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about labile memories"""
        return {
            'labile_count': len(self.labile_memories),
            'recent_retrievals': len(self.recent_retrievals),
            'window_hours': self.window_hours
        }


# ============================================================================
# Reconsolidation Detector
# ============================================================================

class ReconsolidationDetector:
    """
    Detect when memory retrieval + novelty co-occur.

    Reconsolidation ONLY triggered when:
    1. Memory was recently retrieved
    2. AND new semantically related information present
    3. AND novelty score exceeds threshold
    """

    def __init__(
        self,
        novelty_threshold: float = 0.3,
        semantic_similarity_min: float = 0.7,
        semantic_similarity_max: float = 0.98
    ):
        """
        Args:
            novelty_threshold: Min novelty score to trigger reconsolidation (0-1)
            semantic_similarity_min: Min similarity for "related" (too low = unrelated)
            semantic_similarity_max: Max similarity for "novel" (too high = duplicate)
        """
        self.novelty_threshold = novelty_threshold
        self.semantic_similarity_min = semantic_similarity_min
        self.semantic_similarity_max = semantic_similarity_max

    def compute_novelty_score(
        self,
        retrieved_episode: Episode,
        new_context: Dict[str, Any]
    ) -> Tuple[float, str]:
        """
        Compute how novel new context is relative to existing episode.

        Returns:
            (novelty_score, reason)

        Novelty factors:
        - Semantic similarity (related but not duplicate)
        - Content difference
        - Metadata enrichment
        """
        novelty_score = 0.0
        reasons = []

        # Factor 1: Semantic similarity (sweet spot: 0.7-0.98)
        semantic_factor = 0.0
        if 'embedding' in new_context and retrieved_episode.embedding is not None:
            new_embedding = np.array(new_context['embedding'])
            similarity = np.dot(retrieved_episode.embedding, new_embedding) / (
                np.linalg.norm(retrieved_episode.embedding) * np.linalg.norm(new_embedding) + 1e-8
            )

            if similarity < self.semantic_similarity_min:
                reasons.append("too_dissimilar")
                semantic_factor = 0.0  # Unrelated
            elif similarity > self.semantic_similarity_max:
                reasons.append("too_similar")
                semantic_factor = 0.2  # Duplicate-ish (still allow if content/metadata novel)
            else:
                # Sweet spot: related but not duplicate
                # Peak novelty at similarity ~0.8
                optimal_similarity = 0.8
                similarity_score = 1.0 - abs(similarity - optimal_similarity) / 0.2
                semantic_factor = similarity_score
                reasons.append(f"semantic_similarity={similarity:.2f}")

            novelty_score += semantic_factor * 0.4

        # Factor 2: Content difference
        if 'content' in new_context:
            new_content = new_context['content']
            original_content = retrieved_episode.content

            # Simple: check if new content adds information
            new_tokens = set(new_content.lower().split())
            original_tokens = set(original_content.lower().split())

            new_unique_tokens = new_tokens - original_tokens
            if len(new_tokens) > 0:
                content_novelty = len(new_unique_tokens) / len(new_tokens)
                novelty_score += content_novelty * 0.4
                reasons.append(f"content_novelty={content_novelty:.2f}")

        # Factor 3: Metadata enrichment
        if 'metadata' in new_context:
            new_metadata = new_context['metadata']
            original_metadata = retrieved_episode.metadata

            # Check for new metadata keys
            new_keys = set(new_metadata.keys()) - set(original_metadata.keys())
            if new_keys:
                metadata_novelty = min(1.0, len(new_keys) / 5)  # Cap at 5 new keys
                novelty_score += metadata_novelty * 0.2
                reasons.append(f"new_metadata_keys={list(new_keys)}")

        reason_str = "; ".join(reasons) if reasons else "no_novelty"
        return novelty_score, reason_str

    def should_reconsolidate(
        self,
        retrieved_episode: Episode,
        new_context: Dict[str, Any],
        stability_window: StabilityWindow
    ) -> Tuple[bool, float, str]:
        """
        Determine if reconsolidation should be triggered.

        Returns:
            (should_trigger, novelty_score, reason)
        """
        # Check 1: Was episode recently retrieved?
        if retrieved_episode.episode_id not in stability_window.recent_retrievals:
            return False, 0.0, "not_recently_retrieved"

        # Check 2: Is episode already labile? (cooldown)
        if stability_window.is_labile(retrieved_episode.episode_id):
            remaining = stability_window.get_labile_time_remaining(retrieved_episode.episode_id)
            return False, 0.0, f"already_labile_{remaining:.1f}h_remaining"

        # Check 3: Compute novelty
        novelty_score, novelty_reason = self.compute_novelty_score(
            retrieved_episode,
            new_context
        )

        # Check 4: Novelty exceeds threshold?
        if novelty_score < self.novelty_threshold:
            return False, novelty_score, f"novelty_too_low_{novelty_reason}"

        return True, novelty_score, f"reconsolidate_{novelty_reason}"


# ============================================================================
# Memory Integrator
# ============================================================================

class MemoryIntegrator:
    """
    Integrate new information with existing memory.

    Integration modes:
    - ADDITIVE: Add new details to existing memory
    - CORRECTIVE: Update incorrect details
    - ENRICHMENT: Add context/metadata
    """

    def integrate(
        self,
        original_episode: Episode,
        new_information: Dict[str, Any],
        integration_mode: IntegrationMode
    ) -> Episode:
        """
        Integrate new information into episode.

        Args:
            original_episode: Existing memory
            new_information: New info to integrate
            integration_mode: How to integrate

        Returns:
            Updated episode (original preserved in logs)
        """
        # Create updated episode (copy)
        updated = Episode(
            episode_id=original_episode.episode_id,
            content=original_episode.content,
            metadata=original_episode.metadata.copy(),
            embedding=original_episode.embedding,
            created_at=original_episode.created_at,
            last_accessed=datetime.now(),
            access_count=original_episode.access_count + 1
        )

        if integration_mode == IntegrationMode.ADDITIVE:
            updated = self._integrate_additive(updated, new_information)

        elif integration_mode == IntegrationMode.CORRECTIVE:
            updated = self._integrate_corrective(updated, new_information)

        elif integration_mode == IntegrationMode.ENRICHMENT:
            updated = self._integrate_enrichment(updated, new_information)

        return updated

    def _integrate_additive(
        self,
        episode: Episode,
        new_info: Dict[str, Any]
    ) -> Episode:
        """Add new details to existing memory (append)"""
        if 'content' in new_info:
            # Append new content
            episode.content = f"{episode.content}\n\n[UPDATE] {new_info['content']}"

        if 'metadata' in new_info:
            # Merge metadata (new keys only, don't overwrite)
            for key, value in new_info['metadata'].items():
                if key not in episode.metadata:
                    episode.metadata[key] = value

        # Track update
        episode.metadata['reconsolidation_count'] = episode.metadata.get('reconsolidation_count', 0) + 1
        episode.metadata['last_reconsolidation'] = datetime.now().isoformat()

        return episode

    def _integrate_corrective(
        self,
        episode: Episode,
        new_info: Dict[str, Any]
    ) -> Episode:
        """Correct incorrect details (update existing)"""
        if 'content' in new_info:
            # Mark correction
            episode.content = f"{episode.content}\n\n[CORRECTION] {new_info['content']}"

        if 'metadata' in new_info:
            # Overwrite metadata (corrections)
            for key, value in new_info['metadata'].items():
                if key in episode.metadata:
                    # Store old value
                    old_key = f"{key}_old"
                    episode.metadata[old_key] = episode.metadata[key]
                episode.metadata[key] = value

        episode.metadata['reconsolidation_count'] = episode.metadata.get('reconsolidation_count', 0) + 1
        episode.metadata['last_reconsolidation'] = datetime.now().isoformat()
        episode.metadata['correction_applied'] = True

        return episode

    def _integrate_enrichment(
        self,
        episode: Episode,
        new_info: Dict[str, Any]
    ) -> Episode:
        """Add context/metadata (enrich existing)"""
        if 'metadata' in new_info:
            # Add all new metadata
            episode.metadata.update(new_info['metadata'])

        if 'tags' in new_info:
            # Merge tags
            existing_tags = set(episode.metadata.get('tags', []))
            new_tags = set(new_info['tags'])
            episode.metadata['tags'] = list(existing_tags | new_tags)

        episode.metadata['reconsolidation_count'] = episode.metadata.get('reconsolidation_count', 0) + 1
        episode.metadata['last_reconsolidation'] = datetime.now().isoformat()
        episode.metadata['enrichment_applied'] = True

        return episode


# ============================================================================
# Update Logger
# ============================================================================

class UpdateLogger:
    """Track all reconsolidation events for auditability"""

    def __init__(self):
        self.events: List[ReconsolidationEvent] = []

    def log_reconsolidation(
        self,
        episode_id: str,
        original_content: str,
        updated_content: str,
        integration_mode: IntegrationMode,
        novelty_score: float,
        new_information: Dict[str, Any],
        trigger_reason: str
    ) -> str:
        """
        Log reconsolidation event.

        Returns:
            event_id
        """
        import uuid
        event_id = str(uuid.uuid4())[:8]

        event = ReconsolidationEvent(
            event_id=event_id,
            episode_id=episode_id,
            timestamp=datetime.now(),
            original_content=original_content,
            updated_content=updated_content,
            integration_mode=integration_mode,
            novelty_score=novelty_score,
            new_information=new_information,
            trigger_reason=trigger_reason
        )

        self.events.append(event)
        return event_id

    def get_episode_history(self, episode_id: str) -> List[ReconsolidationEvent]:
        """Get all reconsolidation events for an episode"""
        return [e for e in self.events if e.episode_id == episode_id]

    def get_stats(self) -> Dict[str, Any]:
        """Get reconsolidation statistics"""
        if not self.events:
            return {
                'total_events': 0,
                'avg_novelty_score': 0.0,
                'by_integration_mode': {},
                'unique_episodes_updated': 0
            }

        mode_counts = {}
        for event in self.events:
            mode = event.integration_mode.value
            mode_counts[mode] = mode_counts.get(mode, 0) + 1

        return {
            'total_events': len(self.events),
            'avg_novelty_score': np.mean([e.novelty_score for e in self.events]),
            'by_integration_mode': mode_counts,
            'unique_episodes_updated': len(set(e.episode_id for e in self.events))
        }


# ============================================================================
# Main Memory Reconsolidation Engine
# ============================================================================

class MemoryReconsolidationEngine:
    """
    Main orchestrator for LAB_009.

    Handles memory reconsolidation: updating existing memories when
    new related information arrives during retrieval.
    """

    def __init__(
        self,
        novelty_threshold: float = 0.25,
        window_hours: float = 6.0,
        default_integration_mode: IntegrationMode = IntegrationMode.ADDITIVE
    ):
        self.detector = ReconsolidationDetector(novelty_threshold=novelty_threshold)
        self.integrator = MemoryIntegrator()
        self.stability_window = StabilityWindow(window_hours=window_hours)
        self.logger = UpdateLogger()
        self.default_integration_mode = default_integration_mode

    def on_episode_retrieval(self, episode: Episode):
        """
        Called when episode is retrieved.
        Marks episode as recently accessed (potential for reconsolidation).
        """
        episode.last_accessed = datetime.now()
        episode.access_count += 1
        self.stability_window.mark_retrieval(episode.episode_id)

    def try_reconsolidate(
        self,
        retrieved_episode: Episode,
        new_context: Dict[str, Any],
        integration_mode: Optional[IntegrationMode] = None
    ) -> Tuple[bool, Optional[Episode], str]:
        """
        Attempt to reconsolidate memory with new information.

        Args:
            retrieved_episode: Episode that was retrieved
            new_context: New information to potentially integrate
            integration_mode: How to integrate (default: ADDITIVE)

        Returns:
            (success, updated_episode, reason)
        """
        # Check if reconsolidation should trigger
        should_trigger, novelty_score, reason = self.detector.should_reconsolidate(
            retrieved_episode,
            new_context,
            self.stability_window
        )

        if not should_trigger:
            return False, None, reason

        # Enter labile state
        self.stability_window.enter_labile_state(retrieved_episode.episode_id)

        # Integrate new information
        mode = integration_mode or self.default_integration_mode
        updated_episode = self.integrator.integrate(
            retrieved_episode,
            new_context,
            mode
        )

        # Log reconsolidation
        event_id = self.logger.log_reconsolidation(
            episode_id=retrieved_episode.episode_id,
            original_content=retrieved_episode.content,
            updated_content=updated_episode.content,
            integration_mode=mode,
            novelty_score=novelty_score,
            new_information=new_context,
            trigger_reason=reason
        )

        return True, updated_episode, f"reconsolidated_{event_id}"

    def cleanup(self):
        """Periodic cleanup of expired labile windows"""
        self.stability_window.cleanup_expired()

    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics"""
        return {
            'stability_window': self.stability_window.get_stats(),
            'reconsolidation_events': self.logger.get_stats()
        }


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    print("LAB_009: Memory Reconsolidation Engine")
    print("=" * 60)
    print()
    print("✅ Components implemented:")
    print("  [1] StabilityWindow - 6-hour labile window tracking")
    print("  [2] ReconsolidationDetector - Novelty detection")
    print("  [3] MemoryIntegrator - 3 integration modes")
    print("  [4] UpdateLogger - Auditability")
    print("  [5] MemoryReconsolidationEngine - Main orchestrator")
    print()
    print("Ready for testing.")
