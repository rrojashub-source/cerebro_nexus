"""
LAB_010: Attention Mechanism

Selective attention for memory retrieval - attend to relevant memories,
suppress irrelevant noise.

Based on neuroscience: Prefrontal-parietal attention networks, salience detection,
top-down vs bottom-up attention (2024-2025 research).

Author: NEXUS (Autonomous)
Date: October 28, 2025
"""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple
import numpy as np


# ============================================================================
# Data Structures
# ============================================================================

@dataclass
class MemoryCandidate:
    """Memory candidate for attention scoring"""
    episode_id: str
    embedding: np.ndarray
    created_at: datetime
    importance_score: float = 0.5  # From LAB_004
    emotional_salience: float = 0.5  # From LAB_001
    tags: List[str] = None
    metadata: Dict = None


# ============================================================================
# Attention Scorer
# ============================================================================

class AttentionScorer:
    """
    Compute attention weights for memory candidates.

    Attention = f(semantic_similarity, recency, salience, context_match)

    Multi-factor attention inspired by:
    - Semantic: Transformer dot-product attention
    - Recency: Temporal decay (recent memories more attended)
    - Salience: Emotional/important memories boosted
    - Context: Tag/metadata alignment
    """

    def __init__(
        self,
        semantic_weight: float = 0.5,
        recency_weight: float = 0.2,
        salience_weight: float = 0.2,
        context_weight: float = 0.1,
        recency_halflife_days: float = 7.0
    ):
        """
        Args:
            semantic_weight: Weight for semantic similarity (0-1)
            recency_weight: Weight for recency bias
            salience_weight: Weight for importance/emotion
            context_weight: Weight for context matching
            recency_halflife_days: Recency decay half-life (days)
        """
        # Normalize weights
        total = semantic_weight + recency_weight + salience_weight + context_weight
        self.semantic_weight = semantic_weight / total
        self.recency_weight = recency_weight / total
        self.salience_weight = salience_weight / total
        self.context_weight = context_weight / total

        self.recency_halflife_days = recency_halflife_days

    def compute_semantic_scores(
        self,
        query_embedding: np.ndarray,
        candidates: List[MemoryCandidate]
    ) -> np.ndarray:
        """
        Compute semantic similarity scores (cosine similarity).

        Returns:
            Array of similarities (0-1)
        """
        similarities = []

        for candidate in candidates:
            # Cosine similarity
            sim = np.dot(query_embedding, candidate.embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(candidate.embedding) + 1e-8
            )

            # Normalize to 0-1
            sim = (sim + 1.0) / 2.0
            similarities.append(sim)

        return np.array(similarities)

    def compute_recency_scores(
        self,
        candidates: List[MemoryCandidate],
        current_time: Optional[datetime] = None
    ) -> np.ndarray:
        """
        Compute recency scores (exponential decay).

        Recent memories get higher attention.
        """
        if current_time is None:
            current_time = datetime.now(timezone.utc)

        recency_scores = []

        for candidate in candidates:
            # Days since creation
            days_ago = (current_time - candidate.created_at).total_seconds() / 86400

            # Exponential decay (half-life)
            recency = np.exp(-days_ago * np.log(2) / self.recency_halflife_days)

            recency_scores.append(recency)

        return np.array(recency_scores)

    def compute_salience_scores(
        self,
        candidates: List[MemoryCandidate]
    ) -> np.ndarray:
        """
        Compute salience scores (importance + emotional salience).

        Combines LAB_001 (emotional salience) + LAB_004 (importance).
        """
        salience_scores = []

        for candidate in candidates:
            # Average importance and emotional salience
            salience = (candidate.importance_score + candidate.emotional_salience) / 2.0
            salience_scores.append(salience)

        return np.array(salience_scores)

    def compute_context_scores(
        self,
        candidates: List[MemoryCandidate],
        query_context: Optional[Dict] = None
    ) -> np.ndarray:
        """
        Compute context matching scores (tags, metadata alignment).

        Args:
            query_context: Dict with 'tags', 'metadata' keys
        """
        if query_context is None:
            return np.ones(len(candidates))

        context_scores = []
        query_tags = set(query_context.get('tags', []))

        for candidate in candidates:
            score = 0.0

            # Tag overlap
            if candidate.tags and query_tags:
                candidate_tags = set(candidate.tags)
                overlap = len(query_tags & candidate_tags)
                tag_score = overlap / max(len(query_tags), 1)
                score += tag_score

            # Metadata match (simple: count matching keys)
            if candidate.metadata and 'metadata' in query_context:
                query_meta = query_context['metadata']
                matching_keys = set(candidate.metadata.keys()) & set(query_meta.keys())
                meta_score = len(matching_keys) / max(len(query_meta), 1)
                score += meta_score

            # Average (tag + metadata)
            context_scores.append(score / 2.0 if score > 0 else 0.0)

        # Normalize
        context_array = np.array(context_scores)
        if context_array.max() > 0:
            context_array = context_array / context_array.max()

        return context_array

    def compute_attention_weights(
        self,
        query_embedding: np.ndarray,
        candidates: List[MemoryCandidate],
        query_context: Optional[Dict] = None,
        temperature: float = 1.0
    ) -> np.ndarray:
        """
        Compute final attention weights (softmax normalized).

        Args:
            query_embedding: Query vector
            candidates: Memory candidates
            query_context: Optional context (tags, metadata)
            temperature: Softmax temperature (higher = more uniform)

        Returns:
            Attention weights (sum to 1.0)
        """
        if not candidates:
            return np.array([])

        # Compute individual factor scores
        semantic = self.compute_semantic_scores(query_embedding, candidates)
        recency = self.compute_recency_scores(candidates)
        salience = self.compute_salience_scores(candidates)
        context = self.compute_context_scores(candidates, query_context)

        # Weighted combination
        combined = (
            self.semantic_weight * semantic +
            self.recency_weight * recency +
            self.salience_weight * salience +
            self.context_weight * context
        )

        # Softmax normalization (with temperature)
        logits = combined / temperature
        exp_logits = np.exp(logits - np.max(logits))  # Numerical stability
        attention_weights = exp_logits / exp_logits.sum()

        return attention_weights

    def get_factor_breakdown(
        self,
        query_embedding: np.ndarray,
        candidates: List[MemoryCandidate],
        query_context: Optional[Dict] = None
    ) -> Dict[str, np.ndarray]:
        """Get breakdown of attention factors for analysis"""
        return {
            'semantic': self.compute_semantic_scores(query_embedding, candidates),
            'recency': self.compute_recency_scores(candidates),
            'salience': self.compute_salience_scores(candidates),
            'context': self.compute_context_scores(candidates, query_context)
        }


# ============================================================================
# Attention Filter
# ============================================================================

class AttentionFilter:
    """
    Filter low-attention memories (noise suppression).

    Removes candidates with very low attention (< threshold).
    """

    def filter_by_attention(
        self,
        candidates: List[MemoryCandidate],
        attention_weights: np.ndarray,
        threshold: float = 0.01  # 1% attention minimum
    ) -> Tuple[List[MemoryCandidate], np.ndarray]:
        """
        Filter candidates below attention threshold.

        Args:
            candidates: Memory candidates
            attention_weights: Attention scores (sum to 1.0)
            threshold: Minimum attention to keep

        Returns:
            (filtered_candidates, filtered_weights)
        """
        # Find indices above threshold
        keep_indices = np.where(attention_weights >= threshold)[0]

        # Filter candidates and weights
        filtered_candidates = [candidates[i] for i in keep_indices]
        filtered_weights = attention_weights[keep_indices]

        # Re-normalize weights (should sum to 1.0 again)
        if filtered_weights.sum() > 0:
            filtered_weights = filtered_weights / filtered_weights.sum()

        return filtered_candidates, filtered_weights

    def get_top_k(
        self,
        candidates: List[MemoryCandidate],
        attention_weights: np.ndarray,
        k: int = 10
    ) -> Tuple[List[MemoryCandidate], np.ndarray]:
        """
        Get top-K by attention weight.

        Args:
            candidates: Memory candidates
            attention_weights: Attention scores
            k: Number to keep

        Returns:
            (top_k_candidates, top_k_weights)
        """
        # Sort by attention (descending)
        sorted_indices = np.argsort(attention_weights)[::-1]

        # Take top K
        top_k_indices = sorted_indices[:k]

        top_k_candidates = [candidates[i] for i in top_k_indices]
        top_k_weights = attention_weights[top_k_indices]

        # Re-normalize
        if top_k_weights.sum() > 0:
            top_k_weights = top_k_weights / top_k_weights.sum()

        return top_k_candidates, top_k_weights


# ============================================================================
# Attention Analyzer
# ============================================================================

class AttentionAnalyzer:
    """Analyze attention distribution patterns"""

    def compute_concentration(
        self,
        attention_weights: np.ndarray
    ) -> Dict[str, float]:
        """
        Compute attention concentration metrics.

        Good attention: Concentrated on few relevant memories (Pareto: 80/20)
        Poor attention: Uniform (no discrimination)
        """
        if len(attention_weights) == 0:
            return {'entropy': 0.0, 'top_20_percent_mass': 0.0}

        # Sort descending
        sorted_weights = np.sort(attention_weights)[::-1]

        # Top 20% mass (Pareto principle)
        top_20_count = max(1, int(len(sorted_weights) * 0.2))
        top_20_mass = sorted_weights[:top_20_count].sum()

        # Entropy (normalized)
        # Low entropy = concentrated, High entropy = uniform
        entropy = -np.sum(attention_weights * np.log(attention_weights + 1e-10))
        max_entropy = np.log(len(attention_weights))
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0

        return {
            'entropy': normalized_entropy,  # 0 (concentrated) to 1 (uniform)
            'top_20_percent_mass': top_20_mass,
            'gini_coefficient': self._compute_gini(sorted_weights)
        }

    def _compute_gini(self, sorted_values: np.ndarray) -> float:
        """Gini coefficient (0 = perfect equality, 1 = perfect inequality)"""
        n = len(sorted_values)
        if n == 0:
            return 0.0

        cumsum = np.cumsum(sorted_values)
        return (n + 1 - 2 * cumsum.sum() / cumsum[-1]) / n


# ============================================================================
# Main Attention Mechanism
# ============================================================================

class AttentionMechanism:
    """
    Main orchestrator for LAB_010.

    Attention-weighted memory retrieval with noise suppression.
    """

    def __init__(
        self,
        semantic_weight: float = 0.6,
        recency_weight: float = 0.2,
        salience_weight: float = 0.15,
        context_weight: float = 0.05,
        attention_threshold: float = 0.15,
        temperature: float = 0.5
    ):
        self.scorer = AttentionScorer(
            semantic_weight=semantic_weight,
            recency_weight=recency_weight,
            salience_weight=salience_weight,
            context_weight=context_weight
        )
        self.filter = AttentionFilter()
        self.analyzer = AttentionAnalyzer()
        self.attention_threshold = attention_threshold
        self.temperature = temperature

    def attend(
        self,
        query_embedding: np.ndarray,
        candidates: List[MemoryCandidate],
        query_context: Optional[Dict] = None,
        top_k: Optional[int] = None,
        apply_filter: bool = True
    ) -> Tuple[List[MemoryCandidate], np.ndarray]:
        """
        Compute attention and return attended memories.

        Args:
            query_embedding: Query vector
            candidates: Memory candidates
            query_context: Optional context
            top_k: If set, return top-K only
            apply_filter: Whether to filter low-attention

        Returns:
            (attended_candidates, attention_weights)
        """
        # Compute attention weights
        attention_weights = self.scorer.compute_attention_weights(
            query_embedding,
            candidates,
            query_context,
            temperature=self.temperature
        )

        # Filter low-attention
        if apply_filter:
            candidates, attention_weights = self.filter.filter_by_attention(
                candidates,
                attention_weights,
                threshold=self.attention_threshold
            )

        # Top-K if requested
        if top_k is not None:
            candidates, attention_weights = self.filter.get_top_k(
                candidates,
                attention_weights,
                k=top_k
            )

        return candidates, attention_weights

    def get_attention_stats(
        self,
        attention_weights: np.ndarray
    ) -> Dict[str, float]:
        """Get attention distribution statistics"""
        return self.analyzer.compute_concentration(attention_weights)


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    print("LAB_010: Attention Mechanism")
    print("=" * 60)
    print()
    print("✅ Components implemented:")
    print("  [1] AttentionScorer - Multi-factor attention")
    print("  [2] AttentionFilter - Noise suppression")
    print("  [3] AttentionAnalyzer - Distribution metrics")
    print("  [4] AttentionMechanism - Main orchestrator")
    print()
    print("Ready for testing.")
