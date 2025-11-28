"""
AAG Decision Logic

Classifies knowledge as accept/attribute/reject based on score.
"""

import numpy as np
from src.identity.aag.scoring import score_knowledge_item


def should_accept_knowledge(item, my_z_id, query, thresholds=None):
    """
    Decide whether to accept, attribute, or reject knowledge.

    Args:
        item: Knowledge item dict
        my_z_id: MY identity vector (1024D)
        query: User query string
        thresholds: Dict with 'accept' and 'attribute' thresholds

    Returns:
        tuple: (decision, metadata)
            - decision: 'accept' | 'attribute' | 'reject'
            - metadata: Dict with score breakdown
    """
    # Default thresholds
    if thresholds is None:
        thresholds = {
            'accept': 0.7,      # Score >= 0.7 → accept
            'attribute': 0.4    # Score >= 0.4 → attribute, else reject
        }

    # Self knowledge always accepted
    if item.get('attribution') == 'self':
        return 'accept', {
            'reason': 'self_knowledge',
            'score': 1.0,
            'relevance': 1.0,
            'identity_alignment': 1.0
        }

    # Score external knowledge
    score, relevance, identity_alignment = score_knowledge_item(
        item, query, my_z_id
    )

    # Decision logic
    if score >= thresholds['accept']:
        decision = 'accept'
        reason = f"high_score (relevance={relevance:.2f}, alignment={identity_alignment:.2f})"
    elif score >= thresholds['attribute']:
        decision = 'attribute'
        reason = f"medium_score (relevance={relevance:.2f}, alignment={identity_alignment:.2f})"
    else:
        decision = 'reject'
        reason = f"low_score (relevance={relevance:.2f}, alignment={identity_alignment:.2f})"

    metadata = {
        'score': score,
        'relevance': relevance,
        'identity_alignment': identity_alignment,
        'reason': reason
    }

    return decision, metadata
