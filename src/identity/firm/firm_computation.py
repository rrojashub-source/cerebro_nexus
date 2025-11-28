"""
FIRM Computation

Computes Foreign-Identity Rejection Metric using Spearman correlation.
"""

from scipy.stats import spearmanr, rankdata
import numpy as np

from src.identity.firm.foreign_detection import compute_foreign_prob
from src.identity.firm.refusal_mapping import extract_refusal_probs_from_aag


def compute_firm(aag_response, my_z_id):
    """
    Calcula FIRM (Foreign-Identity Rejection Metric) desde respuesta AAG.

    Args:
        aag_response: Dict con 'accepted', 'attributed', 'rejected' lists
        my_z_id: MI identidad vector (1024D numpy array)

    Returns:
        tuple: (firm_score, metadata)
            - firm_score: Float 0-1 (higher = stronger boundary)
            - metadata: Dict con:
                - 'n_items': Total external items evaluated
                - 'mean_refusal': Mean refusal probability
                - 'mean_foreign': Mean foreign probability
                - 'correlation': Spearman correlation coefficient
                - 'p_value': Statistical significance

    Raises:
        ValueError: If insufficient items (<3) for correlation

    Algorithm:
        1. Extract refusal_probs from AAG decisions
        2. Compute foreign_probs for each item
        3. Rank both arrays
        4. Compute Spearman correlation between ranks

    Interpretation:
        - FIRM > 0.90: Strong boundary (foreign items rejected correctly)
        - 0.75 < FIRM < 0.90: Adequate boundary
        - FIRM < 0.75: Weak boundary (ALERT - foreign items accepted)
        - FIRM < 0: Inverted boundary (CRITICAL - system malfunction)
    """
    # 1. Extract refusal probabilities and items
    refusal_probs, items = extract_refusal_probs_from_aag(aag_response)

    # 2. Check minimum items for correlation
    if len(refusal_probs) < 3:
        raise ValueError(f"FIRM requires ≥3 external items for correlation, got {len(refusal_probs)} (insufficient items)")

    # 3. Compute foreign probabilities for each item (vectorized for performance)
    foreign_probs = [compute_foreign_prob(item, my_z_id) for item in items]

    # 4. Compute Spearman rank correlation
    correlation_result = spearmanr(refusal_probs, foreign_probs)
    firm_score = correlation_result.correlation
    p_value = correlation_result.pvalue

    # Handle NaN (can occur if all values are identical)
    if np.isnan(firm_score):
        firm_score = 0.0

    # 5. Build metadata
    metadata = {
        'n_items': len(refusal_probs),
        'mean_refusal': float(np.mean(refusal_probs)),
        'mean_foreign': float(np.mean(foreign_probs)),
        'correlation': float(firm_score),
        'p_value': float(p_value) if not np.isnan(p_value) else 1.0
    }

    return firm_score, metadata


def classify_firm_status(firm_score):
    """
    Clasifica estado de FIRM en categorías.

    Args:
        firm_score: Float 0-1

    Returns:
        dict: {
            'status': 'strong' | 'adequate' | 'weak' | 'critical',
            'color': 'green' | 'yellow' | 'orange' | 'red',
            'recommendation': str
        }
    """
    if firm_score > 0.90:
        return {
            'status': 'strong',
            'color': 'green',
            'recommendation': 'Identity boundary operating optimally. Continue monitoring.'
        }
    elif firm_score > 0.75:
        return {
            'status': 'adequate',
            'color': 'yellow',
            'recommendation': 'Identity boundary adequate. Monitor for trends.'
        }
    elif firm_score >= 0:
        return {
            'status': 'weak',
            'color': 'orange',
            'recommendation': 'ALERT: Identity boundary weakening. Review AAG thresholds.'
        }
    else:  # firm_score < 0
        return {
            'status': 'critical',
            'color': 'red',
            'recommendation': 'CRITICAL: Inverted boundary detected. System malfunction - immediate review required.'
        }
