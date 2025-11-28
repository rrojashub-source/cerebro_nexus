"""
Synthetic External Knowledge Generation

Creates synthetic external knowledge for AAG testing.
"""

import numpy as np
import random


def create_synthetic_external_knowledge(my_episodes, n_samples=10):
    """
    Create synthetic external knowledge for AAG testing.

    Strategy:
    - Take MY episodes
    - Create 3 variations per episode (close, medium, far)
    - Assign synthetic Z_IDs at controlled distances
    - Repeat episodes cyclically if n_samples > 3*len(episodes)

    Args:
        my_episodes: List of MY episode dicts
        n_samples: Number of synthetic items to create (total)

    Returns:
        List of synthetic external knowledge items

    Raises:
        ValueError: If my_episodes is empty or n_samples <= 0
    """
    # Input validation
    if not my_episodes:
        raise ValueError("my_episodes cannot be empty")
    if n_samples <= 0:
        return []  # Return empty list for non-positive n_samples

    synthetic = []

    # Calculate how many episodes we need to sample
    # Each episode generates 3 variations (close, medium, far)
    n_episodes_needed = (n_samples + 2) // 3  # Ceiling division

    # Sample episodes, repeating if necessary
    if n_episodes_needed <= len(my_episodes):
        sampled = random.sample(my_episodes, n_episodes_needed)
    else:
        # Need to repeat episodes
        sampled = []
        full_cycles = n_episodes_needed // len(my_episodes)
        remainder = n_episodes_needed % len(my_episodes)

        for _ in range(full_cycles):
            sampled.extend(my_episodes)
        if remainder > 0:
            sampled.extend(random.sample(my_episodes, remainder))

    # Create variations for each sampled episode
    for ep in sampled:
        content = ep.get('content', '')

        # Variation 1: Close to MY identity (distance ~0.2)
        close = {
            'content': content,  # Same content (simplified)
            'attribution': 'external',
            'source_agent': 'synthetic_similar',
            'synthetic_z_id': np.random.randn(1024),  # Will be adjusted by test
            'distance_category': 'close'
        }

        # Variation 2: Medium distance (distance ~0.5)
        medium = {
            'content': content,  # Same content (simplified)
            'attribution': 'external',
            'source_agent': 'synthetic_medium',
            'synthetic_z_id': np.random.randn(1024),
            'distance_category': 'medium'
        }

        # Variation 3: Far from MY identity (distance ~0.8)
        far = {
            'content': content,  # Same content (simplified)
            'attribution': 'external',
            'source_agent': 'synthetic_far',
            'synthetic_z_id': np.random.randn(1024),
            'distance_category': 'far'
        }

        synthetic.extend([close, medium, far])

    # Trim to exact n_samples if we created too many
    return synthetic[:n_samples]
