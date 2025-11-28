"""
Smart Decay - Intelligent forgetting algorithm

Inspired by SuperMemory's decay system and neuroscience:
- Less relevant info gradually fades
- Important/frequent memories stay sharp
- Emotional memories decay slower

Author: NEXUS AI
Created: November 28, 2025
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import math
import logging

logger = logging.getLogger(__name__)


class SmartDecay:
    """
    Intelligent memory decay system.

    Calculates decay scores based on:
    - Time since last access (recency)
    - Number of accesses (frequency)
    - Importance score (relevance)
    - Emotional salience (memorability)
    """

    def __init__(
        self,
        recency_weight: float = 0.3,
        frequency_weight: float = 0.2,
        importance_weight: float = 0.3,
        emotional_weight: float = 0.2,
        half_life_days: int = 30
    ):
        """
        Initialize decay calculator.

        Args:
            recency_weight: Weight for time-based decay
            frequency_weight: Weight for access frequency
            importance_weight: Weight for importance score
            emotional_weight: Weight for emotional salience
            half_life_days: Days until memory strength halves
        """
        self.weights = {
            "recency": recency_weight,
            "frequency": frequency_weight,
            "importance": importance_weight,
            "emotional": emotional_weight
        }
        self.half_life_days = half_life_days

    def calculate_decay_score(
        self,
        created_at: datetime,
        last_accessed: Optional[datetime] = None,
        access_count: int = 1,
        importance_score: float = 0.5,
        emotional_salience: float = 0.5
    ) -> float:
        """
        Calculate decay score for a memory.

        Returns:
            Float 0-1 where 1 = fully retained, 0 = should forget
        """
        now = datetime.utcnow()

        # Recency score (exponential decay)
        days_since_access = (now - (last_accessed or created_at)).days
        recency_score = math.exp(-0.693 * days_since_access / self.half_life_days)

        # Frequency score (logarithmic, capped)
        frequency_score = min(1.0, math.log(access_count + 1) / math.log(100))

        # Importance already 0-1
        importance_score = max(0, min(1, importance_score))

        # Emotional salience already 0-1
        emotional_salience = max(0, min(1, emotional_salience))

        # Weighted combination
        decay_score = (
            self.weights["recency"] * recency_score +
            self.weights["frequency"] * frequency_score +
            self.weights["importance"] * importance_score +
            self.weights["emotional"] * emotional_salience
        )

        return max(0, min(1, decay_score))

    def should_archive(
        self,
        memory: Dict,
        threshold: float = 0.3
    ) -> bool:
        """
        Determine if memory should be moved to cold storage.

        Args:
            memory: Memory dict with metadata
            threshold: Score below which to archive

        Returns:
            True if should archive
        """
        score = self.calculate_decay_score(
            created_at=memory.get("created_at", datetime.utcnow()),
            last_accessed=memory.get("last_accessed"),
            access_count=memory.get("access_count", 1),
            importance_score=memory.get("importance_score", 0.5),
            emotional_salience=memory.get("emotional_salience", 0.5)
        )
        return score < threshold

    def should_forget(
        self,
        memory: Dict,
        threshold: float = 0.1
    ) -> bool:
        """
        Determine if memory should be permanently forgotten.

        This is more aggressive than archiving - use carefully.

        Args:
            memory: Memory dict with metadata
            threshold: Score below which to forget

        Returns:
            True if should forget
        """
        score = self.calculate_decay_score(
            created_at=memory.get("created_at", datetime.utcnow()),
            last_accessed=memory.get("last_accessed"),
            access_count=memory.get("access_count", 1),
            importance_score=memory.get("importance_score", 0.5),
            emotional_salience=memory.get("emotional_salience", 0.5)
        )
        return score < threshold

    def get_candidates_for_archival(
        self,
        memories: List[Dict],
        threshold: float = 0.3,
        limit: int = 100
    ) -> List[Dict]:
        """
        Get memories that should be archived.

        Args:
            memories: List of memory dicts
            threshold: Archive threshold
            limit: Max results

        Returns:
            List of memories to archive, sorted by decay score
        """
        candidates = []
        for memory in memories:
            score = self.calculate_decay_score(
                created_at=memory.get("created_at", datetime.utcnow()),
                last_accessed=memory.get("last_accessed"),
                access_count=memory.get("access_count", 1),
                importance_score=memory.get("importance_score", 0.5),
                emotional_salience=memory.get("emotional_salience", 0.5)
            )
            if score < threshold:
                memory["decay_score"] = score
                candidates.append(memory)

        # Sort by decay score (lowest first)
        candidates.sort(key=lambda x: x["decay_score"])
        return candidates[:limit]

    def boost_memory(
        self,
        memory: Dict,
        boost_factor: float = 1.5
    ) -> Dict:
        """
        Boost a memory's retention (anti-decay).

        Used when a memory is accessed or marked important.

        Args:
            memory: Memory dict
            boost_factor: Multiplier for importance

        Returns:
            Updated memory dict
        """
        memory["importance_score"] = min(
            1.0,
            memory.get("importance_score", 0.5) * boost_factor
        )
        memory["last_accessed"] = datetime.utcnow()
        memory["access_count"] = memory.get("access_count", 0) + 1
        return memory
