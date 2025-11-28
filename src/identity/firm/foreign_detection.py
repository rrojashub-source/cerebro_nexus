"""
Foreign Detection

Calculates foreign-identity probability for knowledge items.
"""

import numpy as np
from scipy.spatial.distance import cosine


def sigmoid(x):
    """Standard sigmoid function."""
    return 1 / (1 + np.exp(-x))


def compute_foreign_prob(item, my_z_id):
    """
    Calcula probabilidad de que item provenga de identidad extranjera.

    Args:
        item: Knowledge item dict con 'source_z_id' o 'synthetic_z_id'
        my_z_id: MI identidad vector (1024D numpy array)

    Returns:
        float: Foreign probability 0-1 (0=mismo, 1=muy extranjero)

    Raises:
        ValueError: Si item externo no tiene Z_ID de origen

    Formula:
        distance = cosine_distance(my_z_id, source_z_id)
        p_foreign = sigmoid(5 * (distance - 0.5))  # Steeper sigmoid for clear separation

    Interpretation:
        - p_foreign < 0.3: Close identity (similar to me)
        - p_foreign 0.3-0.7: Medium distance
        - p_foreign > 0.7: Far identity (foreign)
    """
    # Self knowledge has p_foreign = 0 by definition
    if item.get('attribution') == 'self':
        return 0.0

    # External knowledge: compute distance from my Z_ID
    source_z_id = item.get('source_z_id')
    if source_z_id is None:
        source_z_id = item.get('synthetic_z_id')

    if source_z_id is None:
        raise ValueError("External knowledge must have 'source_z_id' or 'synthetic_z_id'")

    # Cosine distance (0-2 range, where 0=identical, 2=opposite)
    distance = cosine(my_z_id, source_z_id)

    # Map to foreign probability using sigmoid
    # k=5: Steeper slope for clear boundary
    # offset=0.5: Center at mid-distance
    p_foreign = sigmoid(5 * (distance - 0.5))

    # Clamp to [0, 1]
    p_foreign = max(0.0, min(1.0, p_foreign))

    return p_foreign
