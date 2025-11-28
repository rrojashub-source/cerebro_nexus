"""
Refusal Mapping

Maps AAG decisions to refusal probabilities.
"""


def map_decision_to_refusal_prob(decision):
    """
    Mapea decisión AAG a probabilidad de rechazo.

    Args:
        decision: str, one of 'accept', 'attribute', 'reject'

    Returns:
        float: Refusal probability 0-1

    Mapping:
        - 'accept'    → r_i = 0.0 (no refusal)
        - 'attribute' → r_i = 0.5 (partial refusal, requires attribution)
        - 'reject'    → r_i = 1.0 (full refusal)

    Raises:
        ValueError: If decision not in ['accept', 'attribute', 'reject']
    """
    mapping = {
        'accept': 0.0,
        'attribute': 0.5,
        'reject': 1.0
    }

    if decision not in mapping:
        raise ValueError(f"Invalid decision: '{decision}'. Must be one of {list(mapping.keys())}")

    return mapping[decision]


def extract_refusal_probs_from_aag(aag_response):
    """
    Extrae lista de refusal probabilities desde respuesta AAG.

    Args:
        aag_response: Dict con 'accepted', 'attributed', 'rejected' lists

    Returns:
        tuple: (refusal_probs, items)
            - refusal_probs: List of refusal probabilities (one per external item)
            - items: List of corresponding items

    Note:
        - Excluye items con attribution='self' (self knowledge no cuenta para FIRM)
        - Solo procesa external knowledge
    """
    refusal_probs = []
    items = []

    # Accepted items: r_i = 0.0 (excluding self knowledge)
    for item in aag_response.get('accepted', []):
        if item.get('attribution') != 'self':
            refusal_probs.append(0.0)
            items.append(item)

    # Attributed items: r_i = 0.5
    for item in aag_response.get('attributed', []):
        refusal_probs.append(0.5)
        items.append(item)

    # Rejected items: r_i = 1.0
    for item in aag_response.get('rejected', []):
        refusal_probs.append(1.0)
        items.append(item)

    return refusal_probs, items
