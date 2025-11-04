"""
LAB_006: Metacognition Logger

Track NEXUS's own cognitive processes: confidence levels, error detection,
calibration metrics, and reasoning traces.

Based on neuroscience: Prefrontal metacognition (dmPFC, frontopolar cortex)
and AI metacognitive monitoring (2024-2025 research).

Author: NEXUS (Autonomous)
Date: October 28, 2025
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import numpy as np


# ============================================================================
# Data Structures
# ============================================================================

class ConfidenceBand(Enum):
    """Confidence level bands"""
    VERY_CONFIDENT = "very_confident"    # 0.9-1.0
    CONFIDENT = "confident"              # 0.7-0.9
    UNCERTAIN = "uncertain"              # 0.5-0.7
    VERY_UNCERTAIN = "very_uncertain"    # 0.0-0.5


@dataclass
class Action:
    """Logged action with metacognitive data"""
    action_id: str
    action_type: str
    confidence: float  # 0.0-1.0
    reasoning: Optional[str]
    timestamp: datetime
    outcome: Optional[bool] = None  # True = success, False = failure, None = pending
    error_type: Optional[str] = None


# ============================================================================
# Confidence Tracker
# ============================================================================

class ConfidenceTracker:
    """
    Track confidence levels for each action/decision.

    Confidence should predict success: high confidence → high success rate.
    """

    def __init__(self):
        # {action_id: Action}
        self.actions: Dict[str, Action] = {}

    def log_action(
        self,
        action_id: str,
        action_type: str,
        confidence: float,
        reasoning: Optional[str] = None
    ) -> Action:
        """
        Log an action with confidence level.

        Args:
            action_id: Unique identifier
            action_type: Type of action (e.g., "lab_implementation", "test", "decision")
            confidence: 0.0-1.0 (subjective confidence in success)
            reasoning: Why this confidence level?

        Returns:
            Created Action object
        """
        # Validate confidence
        confidence = max(0.0, min(1.0, confidence))

        action = Action(
            action_id=action_id,
            action_type=action_type,
            confidence=confidence,
            reasoning=reasoning,
            timestamp=datetime.now()
        )

        self.actions[action_id] = action
        return action

    def get_confidence_band(self, confidence: float) -> ConfidenceBand:
        """Categorize confidence into bands"""
        if confidence >= 0.9:
            return ConfidenceBand.VERY_CONFIDENT
        elif confidence >= 0.7:
            return ConfidenceBand.CONFIDENT
        elif confidence >= 0.5:
            return ConfidenceBand.UNCERTAIN
        else:
            return ConfidenceBand.VERY_UNCERTAIN

    def get_stats(self) -> Dict[str, Any]:
        """Get confidence statistics"""
        if not self.actions:
            return {
                'total_actions': 0,
                'avg_confidence': 0.0
            }

        confidences = [a.confidence for a in self.actions.values()]

        return {
            'total_actions': len(self.actions),
            'avg_confidence': np.mean(confidences),
            'std_confidence': np.std(confidences),
            'min_confidence': min(confidences),
            'max_confidence': max(confidences)
        }


# ============================================================================
# Outcome Tracker
# ============================================================================

class OutcomeTracker:
    """
    Track actual outcomes of actions.

    Enables calibration analysis: Were high-confidence actions actually successful?
    """

    def __init__(self, confidence_tracker: ConfidenceTracker):
        self.confidence_tracker = confidence_tracker

    def log_outcome(
        self,
        action_id: str,
        success: bool,
        error_type: Optional[str] = None
    ) -> bool:
        """
        Log outcome of an action.

        Args:
            action_id: Action to update
            success: True if action succeeded
            error_type: If failed, what type of error? (optional)

        Returns:
            True if action found and updated
        """
        if action_id not in self.confidence_tracker.actions:
            return False

        action = self.confidence_tracker.actions[action_id]
        action.outcome = success
        action.error_type = error_type

        return True

    def get_completed_actions(self) -> List[Action]:
        """Get actions with known outcomes"""
        return [
            a for a in self.confidence_tracker.actions.values()
            if a.outcome is not None
        ]

    def get_success_rate(self) -> float:
        """Overall success rate"""
        completed = self.get_completed_actions()
        if not completed:
            return 0.0

        successes = sum(1 for a in completed if a.outcome)
        return successes / len(completed)

    def get_stats(self) -> Dict[str, Any]:
        """Get outcome statistics"""
        completed = self.get_completed_actions()

        if not completed:
            return {
                'completed_actions': 0,
                'success_rate': 0.0,
                'pending_actions': len(self.confidence_tracker.actions)
            }

        successes = sum(1 for a in completed if a.outcome)
        failures = len(completed) - successes

        # Error type breakdown
        error_types = {}
        for action in completed:
            if not action.outcome and action.error_type:
                error_types[action.error_type] = error_types.get(action.error_type, 0) + 1

        return {
            'completed_actions': len(completed),
            'success_rate': successes / len(completed),
            'successes': successes,
            'failures': failures,
            'error_types': error_types,
            'pending_actions': len(self.confidence_tracker.actions) - len(completed)
        }


# ============================================================================
# Error Detector
# ============================================================================

class ErrorDetector:
    """
    Detect and categorize errors.

    Error categories:
    - confidence_mismatch: High confidence but failed
    - unexpected_failure: Should have succeeded based on context
    - known_limitation: Expected difficulty area
    """

    def detect_confidence_mismatch(
        self,
        action: Action,
        threshold: float = 0.8
    ) -> bool:
        """
        Detect if high-confidence action failed.

        This is the most important metacognitive error:
        "I was confident, but I was wrong."
        """
        return (
            action.outcome is not None and
            not action.outcome and
            action.confidence >= threshold
        )

    def analyze_errors(
        self,
        actions: List[Action]
    ) -> Dict[str, Any]:
        """
        Analyze all errors.

        Returns:
            {
                'confidence_mismatches': int,
                'mismatch_rate': float,
                'avg_mismatch_confidence': float
            }
        """
        completed = [a for a in actions if a.outcome is not None]

        if not completed:
            return {
                'confidence_mismatches': 0,
                'mismatch_rate': 0.0,
                'avg_mismatch_confidence': 0.0
            }

        mismatches = [a for a in completed if self.detect_confidence_mismatch(a)]

        return {
            'confidence_mismatches': len(mismatches),
            'mismatch_rate': len(mismatches) / len(completed),
            'avg_mismatch_confidence': np.mean([a.confidence for a in mismatches]) if mismatches else 0.0,
            'mismatch_actions': [a.action_id for a in mismatches]
        }


# ============================================================================
# Calibration Analyzer
# ============================================================================

class CalibrationAnalyzer:
    """
    Analyze confidence calibration.

    Perfect calibration: 0.9 confidence → 90% success rate
    Overconfident: 0.9 confidence → 70% success rate
    Underconfident: 0.5 confidence → 80% success rate
    """

    def compute_expected_calibration_error(
        self,
        actions: List[Action],
        num_bins: int = 10
    ) -> float:
        """
        Compute Expected Calibration Error (ECE).

        ECE = average |confidence - accuracy| across confidence bins.

        Perfect calibration: ECE = 0
        Poor calibration: ECE > 0.1

        Args:
            actions: List of completed actions
            num_bins: Number of confidence bins (default: 10)

        Returns:
            ECE score (0.0-1.0, lower is better)
        """
        completed = [a for a in actions if a.outcome is not None]

        if not completed:
            return 0.0

        # Create bins
        bins = np.linspace(0, 1, num_bins + 1)
        bin_errors = []
        bin_counts = []

        for i in range(num_bins):
            bin_min, bin_max = bins[i], bins[i + 1]

            # Actions in this bin
            bin_actions = [
                a for a in completed
                if bin_min <= a.confidence < bin_max or (i == num_bins - 1 and a.confidence == 1.0)
            ]

            if not bin_actions:
                continue

            # Bin confidence (average)
            bin_conf = np.mean([a.confidence for a in bin_actions])

            # Bin accuracy (success rate)
            bin_acc = sum(1 for a in bin_actions if a.outcome) / len(bin_actions)

            # Error
            bin_error = abs(bin_conf - bin_acc)

            bin_errors.append(bin_error)
            bin_counts.append(len(bin_actions))

        if not bin_errors:
            return 0.0

        # Weighted average
        total = sum(bin_counts)
        ece = sum(err * count / total for err, count in zip(bin_errors, bin_counts))

        return ece

    def compute_brier_score(self, actions: List[Action]) -> float:
        """
        Compute Brier Score.

        Brier = average (confidence - outcome)^2

        Perfect predictions: Brier = 0
        Random: Brier = 0.25
        """
        completed = [a for a in actions if a.outcome is not None]

        if not completed:
            return 0.0

        scores = [(a.confidence - (1 if a.outcome else 0)) ** 2 for a in completed]
        return np.mean(scores)

    def analyze_by_confidence_band(
        self,
        actions: List[Action]
    ) -> Dict[str, Dict[str, float]]:
        """
        Analyze success rate by confidence band.

        Expected:
        - Very confident (0.9-1.0): ~90% success
        - Confident (0.7-0.9): ~80% success
        - Uncertain (0.5-0.7): ~60% success
        - Very uncertain (0.0-0.5): ~40% success
        """
        completed = [a for a in actions if a.outcome is not None]

        bands = {
            'very_confident': [],
            'confident': [],
            'uncertain': [],
            'very_uncertain': []
        }

        for action in completed:
            if action.confidence >= 0.9:
                bands['very_confident'].append(action)
            elif action.confidence >= 0.7:
                bands['confident'].append(action)
            elif action.confidence >= 0.5:
                bands['uncertain'].append(action)
            else:
                bands['very_uncertain'].append(action)

        results = {}
        for band_name, band_actions in bands.items():
            if not band_actions:
                results[band_name] = {
                    'count': 0,
                    'success_rate': 0.0,
                    'avg_confidence': 0.0
                }
            else:
                successes = sum(1 for a in band_actions if a.outcome)
                results[band_name] = {
                    'count': len(band_actions),
                    'success_rate': successes / len(band_actions),
                    'avg_confidence': np.mean([a.confidence for a in band_actions])
                }

        return results

    def get_calibration_stats(self, actions: List[Action]) -> Dict[str, Any]:
        """Get comprehensive calibration statistics"""
        completed = [a for a in actions if a.outcome is not None]

        if not completed:
            return {
                'ece': 0.0,
                'brier_score': 0.0,
                'by_confidence_band': {}
            }

        return {
            'ece': self.compute_expected_calibration_error(completed),
            'brier_score': self.compute_brier_score(completed),
            'by_confidence_band': self.analyze_by_confidence_band(completed),
            'sample_size': len(completed)
        }


# ============================================================================
# Main Metacognition Logger
# ============================================================================

class MetacognitionLogger:
    """
    Main orchestrator for LAB_006.

    Logs confidence, outcomes, detects errors, analyzes calibration.
    """

    def __init__(self):
        self.confidence_tracker = ConfidenceTracker()
        self.outcome_tracker = OutcomeTracker(self.confidence_tracker)
        self.error_detector = ErrorDetector()
        self.calibration_analyzer = CalibrationAnalyzer()

    def log_action(
        self,
        action_id: str,
        action_type: str,
        confidence: float,
        reasoning: Optional[str] = None
    ) -> Action:
        """Log an action with confidence"""
        return self.confidence_tracker.log_action(
            action_id,
            action_type,
            confidence,
            reasoning
        )

    def log_outcome(
        self,
        action_id: str,
        success: bool,
        error_type: Optional[str] = None
    ) -> bool:
        """Log outcome of action"""
        return self.outcome_tracker.log_outcome(action_id, success, error_type)

    def get_comprehensive_stats(self) -> Dict[str, Any]:
        """Get all metacognition statistics"""
        actions = list(self.confidence_tracker.actions.values())

        return {
            'confidence': self.confidence_tracker.get_stats(),
            'outcomes': self.outcome_tracker.get_stats(),
            'errors': self.error_detector.analyze_errors(actions),
            'calibration': self.calibration_analyzer.get_calibration_stats(actions)
        }

    def is_well_calibrated(self, ece_threshold: float = 0.1) -> bool:
        """Check if system is well-calibrated (ECE < threshold)"""
        stats = self.get_comprehensive_stats()
        ece = stats['calibration']['ece']
        return ece < ece_threshold


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    print("LAB_006: Metacognition Logger")
    print("=" * 60)
    print()
    print("✅ Components implemented:")
    print("  [1] ConfidenceTracker - Log actions with confidence")
    print("  [2] OutcomeTracker - Track success/failure")
    print("  [3] ErrorDetector - Detect confidence mismatches")
    print("  [4] CalibrationAnalyzer - ECE + Brier score")
    print("  [5] MetacognitionLogger - Main orchestrator")
    print()
    print("Ready for testing.")
