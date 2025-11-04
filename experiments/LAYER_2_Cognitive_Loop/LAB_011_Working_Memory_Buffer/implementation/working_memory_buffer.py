"""
LAB_011: Working Memory Buffer

Limited-capacity "active workspace" for currently relevant memories.
Inspired by human working memory (dlPFC): ~7 items, fast access, smart eviction.

Based on neuroscience: Prefrontal cortex active maintenance, Miller's Law (7±2),
and AI KV cache mechanisms (2024-2025 research).

Author: NEXUS (Autonomous)
Date: October 28, 2025
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import time


# ============================================================================
# Data Structures
# ============================================================================

@dataclass
class WorkingMemoryItem:
    """Item in working memory buffer"""
    episode_id: str
    attention_weight: float  # From LAB_010 attention mechanism
    added_at: datetime
    last_accessed: datetime
    access_count: int = 0
    rehearsal_count: int = 0
    tags: List[str] = field(default_factory=list)

    def age_seconds(self) -> float:
        """Age since last access (seconds)"""
        return (datetime.now() - self.last_accessed).total_seconds()

    def access(self):
        """Mark item as accessed (updates LRU)"""
        self.last_accessed = datetime.now()
        self.access_count += 1

    def rehearse(self):
        """Rehearse item (reset decay, boost retention)"""
        self.last_accessed = datetime.now()
        self.rehearsal_count += 1


class EvictionStrategy(Enum):
    """Eviction policy strategies"""
    LRU = "lru"  # Least Recently Used
    ATTENTION = "attention"  # Lowest attention weight
    HYBRID = "hybrid"  # LRU + attention (weighted)


# ============================================================================
# Eviction Policies
# ============================================================================

class EvictionPolicy:
    """
    Determine which item to evict when buffer is full.

    Strategies:
    - LRU: Remove least recently accessed
    - Attention: Remove lowest attention weight
    - Hybrid: Weighted combination of LRU + attention
    """

    def __init__(self, strategy: EvictionStrategy = EvictionStrategy.HYBRID):
        self.strategy = strategy

    def select_victim(
        self,
        buffer: List[WorkingMemoryItem],
        new_item: WorkingMemoryItem
    ) -> int:
        """
        Select index of item to evict.

        Args:
            buffer: Current buffer contents
            new_item: Item trying to enter buffer

        Returns:
            Index of item to evict (or -1 if new_item shouldn't enter)
        """
        if not buffer:
            return -1

        if self.strategy == EvictionStrategy.LRU:
            return self._lru_victim(buffer)
        elif self.strategy == EvictionStrategy.ATTENTION:
            return self._attention_victim(buffer, new_item)
        else:  # HYBRID
            return self._hybrid_victim(buffer, new_item)

    def _lru_victim(self, buffer: List[WorkingMemoryItem]) -> int:
        """Least Recently Used - evict oldest last_accessed"""
        oldest_idx = 0
        oldest_time = buffer[0].last_accessed

        for i, item in enumerate(buffer):
            if item.last_accessed < oldest_time:
                oldest_time = item.last_accessed
                oldest_idx = i

        return oldest_idx

    def _attention_victim(
        self,
        buffer: List[WorkingMemoryItem],
        new_item: WorkingMemoryItem
    ) -> int:
        """
        Attention-based - evict lowest attention weight.

        If new_item has lower attention than all buffered items,
        don't admit it (return -1).
        """
        # Find item with minimum attention
        min_attention = min(item.attention_weight for item in buffer)

        # If new item has lower attention, don't admit it
        if new_item.attention_weight < min_attention:
            return -1

        # Otherwise evict item with lowest attention
        for i, item in enumerate(buffer):
            if item.attention_weight == min_attention:
                return i

        return 0  # Fallback

    def _hybrid_victim(
        self,
        buffer: List[WorkingMemoryItem],
        new_item: WorkingMemoryItem
    ) -> int:
        """
        Hybrid: Score = (1 - attention_weight) + age_normalized

        Evict item with highest score (low attention + old).
        """
        # Compute hybrid scores
        max_age = max(item.age_seconds() for item in buffer)

        scores = []
        for item in buffer:
            # Normalize age to 0-1
            age_normalized = item.age_seconds() / max_age if max_age > 0 else 0

            # Score: low attention + old → high score (bad)
            # Rehearsed items get bonus (lower score)
            rehearsal_bonus = 0.2 * min(item.rehearsal_count, 3)  # Max 0.6 bonus

            score = (1 - item.attention_weight) + age_normalized - rehearsal_bonus
            scores.append(score)

        # Evict highest score (unless new_item would score higher)
        max_score = max(scores)
        new_item_score = (1 - new_item.attention_weight)  # No age for new item

        if new_item_score > max_score:
            return -1  # Don't admit new item

        return scores.index(max_score)


# ============================================================================
# Working Memory Buffer
# ============================================================================

class WorkingMemoryBuffer:
    """
    Limited-capacity buffer for currently active memories.

    Inspired by human working memory (dlPFC):
    - Capacity: 7±2 items (Miller's Law)
    - Fast access: O(1) lookup
    - Smart eviction: Attention-based + LRU
    - Temporal decay: Unused items removed
    """

    def __init__(
        self,
        capacity: int = 7,
        eviction_strategy: EvictionStrategy = EvictionStrategy.HYBRID,
        decay_threshold_seconds: float = 60.0
    ):
        """
        Args:
            capacity: Buffer size (default: 7, Miller's Law)
            eviction_strategy: How to choose eviction victim
            decay_threshold_seconds: Auto-remove items older than this
        """
        self.capacity = capacity
        self.eviction_policy = EvictionPolicy(eviction_strategy)
        self.decay_threshold_seconds = decay_threshold_seconds

        # Buffer storage
        self.buffer: List[WorkingMemoryItem] = []

        # Fast lookup (episode_id -> buffer index)
        self._index: Dict[str, int] = {}

    def add(
        self,
        episode_id: str,
        attention_weight: float = 1.0,
        tags: Optional[List[str]] = None
    ) -> bool:
        """
        Add episode to working memory.

        If buffer full, evicts according to eviction policy.

        Args:
            episode_id: Episode to add
            attention_weight: Attention score (from LAB_010)
            tags: Optional tags for context

        Returns:
            True if added, False if rejected
        """
        # If already in buffer, refresh it
        if episode_id in self._index:
            self.refresh(episode_id)
            return True

        # Create new item
        new_item = WorkingMemoryItem(
            episode_id=episode_id,
            attention_weight=attention_weight,
            added_at=datetime.now(),
            last_accessed=datetime.now(),
            tags=tags or []
        )

        # If buffer has space, add directly
        if len(self.buffer) < self.capacity:
            self.buffer.append(new_item)
            self._rebuild_index()
            return True

        # Buffer full - evict victim
        victim_idx = self.eviction_policy.select_victim(self.buffer, new_item)

        if victim_idx == -1:
            # New item not worthy of admission
            return False

        # Evict victim and add new item
        self.buffer[victim_idx] = new_item
        self._rebuild_index()
        return True

    def get(self, episode_id: str) -> Optional[WorkingMemoryItem]:
        """
        Fast O(1) access to buffered item.

        Automatically updates last_accessed (LRU).
        """
        if episode_id not in self._index:
            return None

        idx = self._index[episode_id]
        item = self.buffer[idx]
        item.access()  # Update LRU

        return item

    def refresh(self, episode_id: str) -> bool:
        """
        Refresh (rehearse) an item - reset decay timer.

        Returns:
            True if item found and refreshed
        """
        item = self.get(episode_id)
        if item:
            item.rehearse()
            return True
        return False

    def remove(self, episode_id: str) -> bool:
        """
        Explicitly remove item from buffer.

        Returns:
            True if item found and removed
        """
        if episode_id not in self._index:
            return False

        idx = self._index[episode_id]
        self.buffer.pop(idx)
        self._rebuild_index()
        return True

    def decay_step(self) -> List[str]:
        """
        Remove items older than decay threshold.

        Returns:
            List of evicted episode IDs
        """
        evicted = []

        # Filter out decayed items
        new_buffer = []
        for item in self.buffer:
            if item.age_seconds() > self.decay_threshold_seconds:
                evicted.append(item.episode_id)
            else:
                new_buffer.append(item)

        self.buffer = new_buffer
        self._rebuild_index()

        return evicted

    def get_all(self) -> List[WorkingMemoryItem]:
        """Get all buffered items (sorted by attention weight descending)"""
        return sorted(self.buffer, key=lambda x: x.attention_weight, reverse=True)

    def get_episode_ids(self) -> List[str]:
        """Get all buffered episode IDs"""
        return [item.episode_id for item in self.buffer]

    def size(self) -> int:
        """Current buffer size"""
        return len(self.buffer)

    def is_full(self) -> bool:
        """Check if buffer is at capacity"""
        return len(self.buffer) >= self.capacity

    def clear(self):
        """Clear entire buffer"""
        self.buffer.clear()
        self._index.clear()

    def _rebuild_index(self):
        """Rebuild episode_id -> index mapping"""
        self._index = {
            item.episode_id: i
            for i, item in enumerate(self.buffer)
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get buffer statistics"""
        if not self.buffer:
            return {
                'size': 0,
                'capacity': self.capacity,
                'utilization': 0.0,
                'avg_attention': 0.0,
                'avg_age_seconds': 0.0
            }

        return {
            'size': len(self.buffer),
            'capacity': self.capacity,
            'utilization': len(self.buffer) / self.capacity,
            'avg_attention': sum(item.attention_weight for item in self.buffer) / len(self.buffer),
            'avg_age_seconds': sum(item.age_seconds() for item in self.buffer) / len(self.buffer),
            'total_accesses': sum(item.access_count for item in self.buffer),
            'total_rehearsals': sum(item.rehearsal_count for item in self.buffer)
        }


# ============================================================================
# Rehearsal Manager
# ============================================================================

class RehearsalManager:
    """
    Manage rehearsal (keeping items alive in working memory).

    Criteria for rehearsal:
    - High attention weight (important)
    - Frequently accessed (useful)
    - Task-relevant tags (contextual)
    """

    def __init__(
        self,
        attention_threshold: float = 0.7,
        access_threshold: int = 3
    ):
        """
        Args:
            attention_threshold: Rehearse if attention >= this
            access_threshold: Rehearse if access_count >= this
        """
        self.attention_threshold = attention_threshold
        self.access_threshold = access_threshold

    def should_rehearse(
        self,
        item: WorkingMemoryItem,
        task_tags: Optional[List[str]] = None
    ) -> bool:
        """
        Decide if item should be rehearsed.

        Args:
            item: Working memory item
            task_tags: Current task context tags

        Returns:
            True if item should be rehearsed
        """
        # High attention → rehearse
        if item.attention_weight >= self.attention_threshold:
            return True

        # Frequently accessed → rehearse
        if item.access_count >= self.access_threshold:
            return True

        # Task-relevant tags → rehearse
        if task_tags and item.tags:
            tag_overlap = len(set(item.tags) & set(task_tags))
            if tag_overlap > 0:
                return True

        return False

    def rehearse_buffer(
        self,
        buffer: WorkingMemoryBuffer,
        task_tags: Optional[List[str]] = None
    ) -> List[str]:
        """
        Rehearse items in buffer that meet criteria.

        Returns:
            List of rehearsed episode IDs
        """
        rehearsed = []

        for item in buffer.get_all():
            if self.should_rehearse(item, task_tags):
                buffer.refresh(item.episode_id)
                rehearsed.append(item.episode_id)

        return rehearsed


# ============================================================================
# Buffer Manager
# ============================================================================

class BufferManager:
    """
    Main orchestrator for working memory system.

    Coordinates:
    - Buffer updates from attention mechanism (LAB_010)
    - Rehearsal management
    - Temporal decay
    - Context extraction for downstream tasks
    """

    def __init__(
        self,
        capacity: int = 7,
        eviction_strategy: EvictionStrategy = EvictionStrategy.HYBRID,
        decay_threshold_seconds: float = 60.0
    ):
        self.buffer = WorkingMemoryBuffer(
            capacity=capacity,
            eviction_strategy=eviction_strategy,
            decay_threshold_seconds=decay_threshold_seconds
        )
        self.rehearsal_manager = RehearsalManager()

    def update_from_attention(
        self,
        attended_episodes: List[Tuple[str, float]]
    ):
        """
        Update buffer based on attention mechanism output (LAB_010).

        Args:
            attended_episodes: List of (episode_id, attention_weight) tuples
        """
        for episode_id, attention_weight in attended_episodes:
            self.buffer.add(episode_id, attention_weight)

    def get_active_context(self) -> List[str]:
        """
        Get all currently buffered episode IDs.

        Useful for providing context to LLM or other systems.
        """
        return self.buffer.get_episode_ids()

    def maintenance_step(self, task_tags: Optional[List[str]] = None):
        """
        Periodic maintenance: decay + rehearsal.

        Args:
            task_tags: Current task context for rehearsal decisions
        """
        # Temporal decay
        self.buffer.decay_step()

        # Rehearsal
        self.rehearsal_manager.rehearse_buffer(self.buffer, task_tags)

    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics"""
        return {
            'buffer': self.buffer.get_stats(),
            'contents': [
                {
                    'episode_id': item.episode_id,
                    'attention': item.attention_weight,
                    'age_seconds': item.age_seconds(),
                    'access_count': item.access_count,
                    'rehearsal_count': item.rehearsal_count
                }
                for item in self.buffer.get_all()
            ]
        }


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    print("LAB_011: Working Memory Buffer")
    print("=" * 60)
    print()
    print("✅ Components implemented:")
    print("  [1] WorkingMemoryItem - Buffer item with attention + age")
    print("  [2] EvictionPolicy - LRU, attention, hybrid strategies")
    print("  [3] WorkingMemoryBuffer - 7-item limited buffer")
    print("  [4] RehearsalManager - Keep important items alive")
    print("  [5] BufferManager - Main orchestrator")
    print()
    print("Ready for testing.")
