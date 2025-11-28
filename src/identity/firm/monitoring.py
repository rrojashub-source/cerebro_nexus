"""
FIRM Monitoring

Tracks FIRM scores over time and detects trends.
"""

from datetime import datetime
import numpy as np
import warnings

from src.identity.firm.firm_computation import compute_firm


class FIRMMonitor:
    """
    Monitor histórico de FIRM scores.

    Tracks FIRM over time, detects trends, alerts on degradation.
    """

    def __init__(self, my_z_id, threshold=0.75):
        """
        Initialize FIRM monitor.

        Args:
            my_z_id: MI identidad vector (1024D)
            threshold: Alert threshold (default 0.75)
        """
        self.my_z_id = my_z_id
        self.threshold = threshold
        self.history = []  # List of (timestamp, firm_score, metadata)

    def evaluate(self, aag_response):
        """
        Evaluate AAG response and log FIRM score.

        Args:
            aag_response: Dict from generate_response_with_aag()

        Returns:
            firm_score: Float 0-1

        Side effects:
            - Appends to self.history
            - Issues warning if firm_score < threshold
        """
        # Compute FIRM
        firm_score, metadata = compute_firm(aag_response, self.my_z_id)

        # Log to history
        timestamp = datetime.now()
        self.history.append((timestamp, firm_score, metadata))

        # Keep only last 1000 entries to prevent unbounded growth
        if len(self.history) > 1000:
            self.history = self.history[-1000:]

        # Alert if below threshold
        if firm_score < self.threshold:
            warnings.warn(
                f"FIRM below threshold: {firm_score:.3f} < {self.threshold:.3f}. "
                f"Identity boundary weakening.",
                UserWarning
            )

        return firm_score

    def report(self, window=100):
        """
        Generate report on recent FIRM scores.

        Args:
            window: Number of recent evaluations to analyze (default 100)

        Returns:
            dict: {
                'mean_firm': float,
                'min_firm': float,
                'max_firm': float,
                'std_firm': float,
                'trend': 'stable' | 'improving' | 'degrading',
                'alert_count': int  # Times FIRM < threshold in window
            }
        """
        if not self.history:
            return {
                'mean_firm': 0.0,
                'min_firm': 0.0,
                'max_firm': 0.0,
                'std_firm': 0.0,
                'trend': 'unknown',
                'alert_count': 0
            }

        # Get recent window
        recent = self.history[-window:]
        scores = [firm for _, firm, _ in recent]

        # Compute statistics
        mean_firm = float(np.mean(scores))
        min_firm = float(np.min(scores))
        max_firm = float(np.max(scores))
        std_firm = float(np.std(scores))

        # Detect trend (simple: compare first half vs second half)
        if len(scores) >= 10:
            mid = len(scores) // 2
            first_half_mean = np.mean(scores[:mid])
            second_half_mean = np.mean(scores[mid:])

            if second_half_mean > first_half_mean + 0.05:
                trend = 'improving'
            elif second_half_mean < first_half_mean - 0.05:
                trend = 'degrading'
            else:
                trend = 'stable'
        else:
            trend = 'unknown'

        # Count alerts
        alert_count = sum(1 for score in scores if score < self.threshold)

        return {
            'mean_firm': mean_firm,
            'min_firm': min_firm,
            'max_firm': max_firm,
            'std_firm': std_firm,
            'trend': trend,
            'alert_count': alert_count
        }

    def get_history(self, limit=None):
        """
        Retrieve historical FIRM scores.

        Args:
            limit: Optional limit on number of records (most recent)

        Returns:
            list: Recent history entries
        """
        if limit is None:
            return self.history
        else:
            return self.history[-limit:]

    def clear_history(self):
        """Clear all historical data (use with caution)."""
        self.history = []
