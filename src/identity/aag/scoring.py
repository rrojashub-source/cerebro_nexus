"""
Knowledge Item Scoring

Scores knowledge items by relevance + identity alignment.
"""

import numpy as np
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer

# Load model once (module-level)
_model = None

def get_model():
    """Lazy load embedding model."""
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


def score_knowledge_item(item, query, my_z_id, alpha=0.6):
    """
    Score knowledge item by relevance + identity alignment.

    Args:
        item: Knowledge item dict with 'content', 'attribution', etc.
        query: User query string
        my_z_id: MY identity vector (1024D numpy array)
        alpha: Weight for relevance (1-alpha for identity)

    Returns:
        tuple: (score, relevance, identity_alignment)
            - score: Combined score 0-1 (higher = better)
            - relevance: Query-content similarity 0-1
            - identity_alignment: Identity similarity 0-1
    """
    model = get_model()

    # 1. Compute relevance (query ↔ content similarity)
    query_embedding = model.encode(query)
    content = item.get('content', '')
    content_embedding = model.encode(content)

    # Cosine similarity (convert distance to similarity)
    relevance = 1 - cosine(query_embedding, content_embedding)
    relevance = max(0.0, min(1.0, relevance))  # Clamp to [0, 1]

    # 2. Compute identity alignment
    if item.get('attribution') == 'self':
        # Self knowledge has perfect alignment
        identity_alignment = 1.0
    else:
        # External knowledge: measure distance from MY Z_ID
        source_z_id = item.get('source_z_id') or item.get('synthetic_z_id')

        if source_z_id is None:
            raise ValueError("External knowledge must have 'source_z_id' or 'synthetic_z_id'")

        # Cosine distance (0-2 range, where 0=identical, 2=opposite)
        distance = cosine(my_z_id, source_z_id)

        # Convert to alignment score (0-1, where 1=perfect alignment)
        identity_alignment = 1 - (distance / 2.0)
        identity_alignment = max(0.0, min(1.0, identity_alignment))  # Clamp

    # 3. Combined score
    score = alpha * relevance + (1 - alpha) * identity_alignment

    return score, relevance, identity_alignment
