"""
AAG Response Generation

Orchestrates full AAG pipeline: retrieve → score → classify → generate.
"""

import numpy as np
from src.identity.aag.synthetic_knowledge import create_synthetic_external_knowledge
from src.identity.aag.decision import should_accept_knowledge


def generate_response_with_aag(query, my_z_id, mode='test', my_episodes=None, n_synthetic=10, top_k=20, use_precomputed=False, external_dbs=None):
    """
    Generate response using AAG (Attribution-Augmented Generation).

    Week 4 Update: Supports both 'production' (real DB) and 'test' (synthetic) modes.
    Week 5 Update: Supports pre-computed embeddings for faster retrieval.
    Week 5 Update: Supports external agent databases for multi-agent retrieval.

    Args:
        query: User query string (e.g., "how to debug code")
        my_z_id: MY identity vector (1024D numpy array)
        mode: 'production' (real memory retrieval) or 'test' (synthetic knowledge)
        my_episodes: List of MY episode dicts (required for mode='test')
        n_synthetic: Number of synthetic external items (mode='test' only, default: 10)
        top_k: Number of episodes to retrieve (mode='production' only, default: 20)
        use_precomputed: Use pre-computed embeddings (Week 5, default False for backward compatibility)
        external_dbs: List of external agent database configs (Week 6+, optional, default None)

    Returns:
        dict with:
            - response: Generated response text
            - accepted: List of accepted knowledge items (score >= 0.7)
            - attributed: List of attributed knowledge items (0.4 <= score < 0.7)
            - rejected: List of rejected knowledge items (score < 0.4)
            - stats: Dict with n_accepted, n_attributed, n_rejected

    Example (test mode - Week 3 behavior):
        >>> my_z_id = np.random.randn(1024)
        >>> my_episodes = [
        ...     {'content': 'Implemented TDD workflow', 'importance': 0.9, 'tags': ['technical']},
        ...     {'content': 'Debugged memory leak', 'importance': 0.85, 'tags': ['debugging']}
        ... ]
        >>> result = generate_response_with_aag("debugging tips", my_z_id, mode='test',
        ...                                     my_episodes=my_episodes, n_synthetic=15)
        >>> result['stats']
        {'n_accepted': 2, 'n_attributed': 8, 'n_rejected': 7}

    Example (production mode - Week 4):
        >>> my_z_id = load_z_id_from_gic('nexus')
        >>> result = generate_response_with_aag("How to implement TDD?", my_z_id,
        ...                                     mode='production', top_k=20)
        >>> result['stats']
        {'n_accepted': 15, 'n_attributed': 3, 'n_rejected': 2}

    Example (production mode with pre-computed - Week 5):
        >>> my_z_id = load_z_id_from_gic('nexus')
        >>> result = generate_response_with_aag("How to implement TDD?", my_z_id,
        ...                                     mode='production', top_k=20, use_precomputed=True)
        >>> result['stats']
        {'n_accepted': 18, 'n_attributed': 2, 'n_rejected': 0}
    """
    # Input validation
    if mode not in ['production', 'test']:
        raise ValueError(f"mode must be 'production' or 'test', got '{mode}'")

    if not query or not query.strip():
        raise ValueError("query cannot be empty")

    # Mode-specific knowledge retrieval
    if mode == 'production':
        # Week 4+5: Retrieve from real database (with optional pre-computed embeddings)
        from src.identity.retrieval.retrieval import retrieve_self_episodes, retrieve_external_episodes

        # Retrieve self episodes (Week 5: use_precomputed parameter)
        self_episodes_raw = retrieve_self_episodes(
            my_z_id,
            query,
            top_k=top_k,
            use_precomputed=use_precomputed
        )

        # Convert to knowledge items format
        my_knowledge = [
            {
                'content': ep['content'],
                'attribution': ep['attribution'],
                'importance': ep['importance'],
                'tags': ep.get('tags', []),
                'z_id': ep['z_id'].tolist() if hasattr(ep['z_id'], 'tolist') else ep['z_id'],
                'relevance_score': ep['relevance_score']
            }
            for ep in self_episodes_raw
        ]

        # Retrieve external episodes (Week 5+: supports external_dbs parameter)
        external_knowledge = retrieve_external_episodes(
            query=query,
            exclude_agent_ids=['nexus'],
            top_k=top_k,
            use_precomputed=use_precomputed,
            external_dbs=external_dbs  # Week 6+: Pass external agent configs
        )

        # Combine
        all_knowledge = my_knowledge + external_knowledge

    elif mode == 'test':
        # Week 3 behavior: Use provided episodes + synthetic knowledge
        if my_episodes is None:
            raise ValueError("my_episodes is required for mode='test'")

        # 1. Convert my episodes to knowledge items
        my_knowledge = [
            {
                'content': ep.get('content', ''),
                'attribution': 'self',
                'importance': ep.get('importance', 0.5),
                'tags': ep.get('tags', [])
            }
            for ep in my_episodes
        ]

        # 2. Generate synthetic external knowledge
        synthetic_knowledge = []
        if n_synthetic > 0:
            synthetic_knowledge = create_synthetic_external_knowledge(
                my_episodes,
                n_samples=n_synthetic
            )

        # 3. Combine all knowledge
        all_knowledge = my_knowledge + synthetic_knowledge

    # 4. Classify each item using AAG decision logic
    accepted = []
    attributed = []
    rejected = []

    for item in all_knowledge:
        decision, metadata = should_accept_knowledge(item, my_z_id, query)

        # Add metadata to item for transparency
        item_with_metadata = item.copy()
        item_with_metadata['aag_metadata'] = metadata

        if decision == 'accept':
            accepted.append(item_with_metadata)
        elif decision == 'attribute':
            attributed.append(item_with_metadata)
        else:  # reject
            rejected.append(item_with_metadata)

    # 5. Generate response (placeholder for now)
    response_text = f"Processed {len(all_knowledge)} knowledge items for query: '{query}'"

    # 6. Return structured response
    return {
        'response': response_text,
        'accepted': accepted,
        'attributed': attributed,
        'rejected': rejected,
        'stats': {
            'n_accepted': len(accepted),
            'n_attributed': len(attributed),
            'n_rejected': len(rejected)
        }
    }
