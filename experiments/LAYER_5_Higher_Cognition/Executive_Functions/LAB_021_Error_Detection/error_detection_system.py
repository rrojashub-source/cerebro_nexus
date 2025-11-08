"""
LAB_021: Error Detection & Correction System

Monitoring Component: Performance monitoring and error processing

Biological Inspiration:
- Anterior cingulate cortex (ACC) - Conflict/error monitoring
- Medial prefrontal cortex (mPFC) - Performance monitoring
- Dopaminergic error signals (RPE)

Core Functions:
- Conflict detection (competing responses)
- Error detection (expected vs actual mismatch)
- Error-Related Negativity (ERN) computation
- Corrective signal generation (post-error slowing, control boost)
- Dopamine RPE integration
- Norepinephrine arousal modulation

Key Papers:
- Botvinick et al. (2001) - "Conflict monitoring and anterior cingulate cortex"
- Holroyd & Coles (2002) - "The neural basis of human error processing"
"""

from typing import Dict, List, Tuple, Optional


class ErrorDetectionSystem:
    """
    LAB_021: Error Detection & Correction System

    Biological inspiration: ACC, mPFC

    Parameters:
    -----------
    baseline_sensitivity : float
        Baseline error sensitivity (default: 0.6)
    conflict_threshold : float
        Conflict detection threshold (default: 0.5)
    error_learning_rate : float
        Learning from errors (default: 0.2)
    correction_strength : float
        Strength of corrective signal (default: 0.8)
    adaptation_rate : float
        Overall adaptation speed (default: 0.15)
    history_window : int
        History buffer size (default: 25)
    """

    def __init__(
        self,
        baseline_sensitivity: float = 0.6,
        conflict_threshold: float = 0.5,
        error_learning_rate: float = 0.2,
        correction_strength: float = 0.8,
        adaptation_rate: float = 0.15,
        history_window: int = 25
    ):
        # Configuration
        self.baseline_sensitivity = baseline_sensitivity
        self.conflict_threshold = conflict_threshold
        self.error_learning_rate = error_learning_rate
        self.correction_strength = correction_strength
        self.adaptation_rate = adaptation_rate
        self.history_window = history_window

        # State
        self.current_sensitivity: float = baseline_sensitivity
        self.conflict_level: float = 0.0
        self.errors_detected: int = 0
        self.corrections_applied: int = 0
        self.conflict_history: List[float] = []
        self.error_history: List[bool] = []

    def detect_conflict(self, response_a_strength: float, response_b_strength: float) -> float:
        """
        Detect conflict between competing response tendencies

        Conflict is high when responses are balanced (both strong)
        Conflict is low when one response dominates

        Formula (Botvinick 2001): min(a, b) / (max(a, b) + epsilon)

        Parameters:
        -----------
        response_a_strength : float
            Strength of response A (0-1)
        response_b_strength : float
            Strength of response B (0-1)

        Returns:
        --------
        conflict_level : float
            Conflict level (0-1)
        """
        epsilon = 0.01  # Prevent division by zero

        min_response = min(response_a_strength, response_b_strength)
        max_response = max(response_a_strength, response_b_strength)

        conflict = min_response / (max_response + epsilon)

        # Update conflict state
        self.conflict_level = conflict

        # Update history
        self.conflict_history.append(conflict)
        if len(self.conflict_history) > self.history_window:
            self.conflict_history.pop(0)

        return conflict

    def detect_error(
        self,
        actual_outcome: str,
        expected_outcome: str,
        confidence: float
    ) -> Tuple[bool, float]:
        """
        Detect error (mismatch between expected and actual outcome)

        Parameters:
        -----------
        actual_outcome : str
            What actually happened
        expected_outcome : str
            What was expected to happen
        confidence : float
            Confidence in expectation (0-1)

        Returns:
        --------
        error_detected : bool
            True if error detected
        error_magnitude : float
            Magnitude of error (0-1)
        """
        # Check for mismatch
        mismatch = (actual_outcome != expected_outcome)

        # Error magnitude modulated by confidence and sensitivity
        if mismatch:
            error_magnitude = confidence * self.current_sensitivity
        else:
            error_magnitude = 0.0

        # Error detected if magnitude above threshold (0.3)
        error_detected = (error_magnitude > 0.3)

        # Update state
        if error_detected:
            self.errors_detected += 1

        # Update history
        self.error_history.append(error_detected)
        if len(self.error_history) > self.history_window:
            self.error_history.pop(0)

        return error_detected, error_magnitude

    def compute_ern_amplitude(self, error_magnitude: float, sensitivity: float) -> float:
        """
        Compute Error-Related Negativity (ERN) amplitude

        ERN is EEG signal ~50-100ms after error
        Amplitude scales with error magnitude and sensitivity

        Parameters:
        -----------
        error_magnitude : float
            Error magnitude (0-1)
        sensitivity : float
            Detection sensitivity (0-1)

        Returns:
        --------
        ern_amplitude : float
            ERN amplitude (arbitrary units, typically 5-20)
        """
        # ERN scales with magnitude and sensitivity
        # Typical range: 5-20 arbitrary units
        ern_amplitude = error_magnitude * sensitivity * 20.0

        return ern_amplitude

    def trigger_correction(self, error_magnitude: float) -> Dict:
        """
        Trigger corrective signal after error

        Corrections include:
        - Control boost (increase cognitive control)
        - Post-error slowing (slower RT on next trial)

        Parameters:
        -----------
        error_magnitude : float
            Magnitude of detected error (0-1)

        Returns:
        --------
        correction : Dict
            {
                "control_boost": float (0-1),
                "post_error_slowing_ms": float (milliseconds)
            }
        """
        # Control boost scales with error magnitude and correction strength
        control_boost = error_magnitude * self.correction_strength

        # Post-error slowing (typical: 20-50ms)
        # Scales with error magnitude
        post_error_slowing = 20.0 + (error_magnitude * 30.0)

        # Update state
        self.corrections_applied += 1

        return {
            "control_boost": float(control_boost),
            "post_error_slowing_ms": float(post_error_slowing)
        }

    def integrate_dopamine_rpe(self, rpe: float) -> float:
        """
        Integrate dopamine reward prediction error as error signal

        Negative RPE = worse than expected = error
        Positive RPE = better than expected = no error

        Parameters:
        -----------
        rpe : float
            Reward prediction error from LAB_013 (-1 to +1)

        Returns:
        --------
        error_magnitude : float
            Error magnitude derived from RPE (0-1)
        """
        # Only negative RPE signals error
        if rpe < 0:
            error_magnitude = abs(rpe)
        else:
            error_magnitude = 0.0

        return error_magnitude

    def integrate_norepinephrine_arousal(
        self,
        baseline_arousal: float,
        error_detected: bool,
        error_magnitude: float
    ) -> float:
        """
        Compute arousal spike from error detection

        Error detection triggers norepinephrine release → arousal spike

        Parameters:
        -----------
        baseline_arousal : float
            Current baseline arousal from LAB_015 (0-1)
        error_detected : bool
            Whether error was detected
        error_magnitude : float
            Magnitude of error (0-1)

        Returns:
        --------
        arousal_boost : float
            Arousal boost magnitude (0-1)
        """
        if not error_detected:
            return 0.0

        # Arousal spike scales with error magnitude
        # Typical boost: 0.2-0.5
        arousal_boost = error_magnitude * 0.5

        return arousal_boost

    def update_sensitivity(self, error_frequency: float, correction_success_rate: float) -> float:
        """
        Update error detection sensitivity based on experience

        - Too many false alarms (high frequency, low success) → reduce sensitivity
        - Missed errors (low frequency, high success) → increase sensitivity
        - Optimal: balance detection vs false alarms

        Parameters:
        -----------
        error_frequency : float
            Frequency of error detections (0-1)
        correction_success_rate : float
            Success rate of corrections (0-1)

        Returns:
        --------
        new_sensitivity : float
            Updated sensitivity (0-1)
        """
        # False alarm indicator: high frequency but low correction success
        false_alarm_indicator = error_frequency * (1.0 - correction_success_rate)

        # Missed error indicator: low frequency but high correction success
        missed_error_indicator = (1.0 - error_frequency) * correction_success_rate

        # Adjust sensitivity
        target_sensitivity = (
            self.baseline_sensitivity
            - false_alarm_indicator * 0.3  # Reduce if false alarms
            + missed_error_indicator * 0.3  # Increase if missed errors
        )

        # Gradual adaptation
        self.current_sensitivity = (
            self.current_sensitivity * (1.0 - self.adaptation_rate) +
            target_sensitivity * self.adaptation_rate
        )

        # Clamp to [0, 1]
        self.current_sensitivity = max(0.0, min(1.0, self.current_sensitivity))

        return self.current_sensitivity

    def compute_post_error_slowing(self) -> float:
        """
        Compute post-error slowing magnitude

        Post-error slowing: slower RT on trial after error
        Typical: 20-50ms

        Returns:
        --------
        slowing_ms : float
            RT increase (milliseconds)
        """
        # Average of recent errors
        if len(self.error_history) > 0:
            recent_error_rate = sum(self.error_history[-5:]) / min(5, len(self.error_history))
        else:
            recent_error_rate = 0.0

        # Slowing scales with recent error rate
        slowing = 20.0 + (recent_error_rate * 30.0)

        return slowing

    def process_event(
        self,
        response_strengths: List[float],
        actual_outcome: str,
        expected_outcome: str,
        confidence: float
    ) -> Dict:
        """
        Main processing: detect conflict, error, trigger correction

        Parameters:
        -----------
        response_strengths : List[float]
            Strengths of competing responses [A, B]
        actual_outcome : str
            What actually happened
        expected_outcome : str
            What was expected
        confidence : float
            Confidence in expectation (0-1)

        Returns:
        --------
        result : Dict
            {
                "conflict_level": float,
                "error_detected": bool,
                "error_magnitude": float,
                "ern_amplitude": float,
                "correction": Dict
            }
        """
        # 1. Detect conflict between responses
        conflict = self.detect_conflict(
            response_a_strength=response_strengths[0],
            response_b_strength=response_strengths[1]
        )

        # 2. Detect error (expected vs actual)
        error_detected, error_magnitude = self.detect_error(
            actual_outcome=actual_outcome,
            expected_outcome=expected_outcome,
            confidence=confidence
        )

        # 3. Compute ERN amplitude
        ern_amplitude = self.compute_ern_amplitude(
            error_magnitude=error_magnitude,
            sensitivity=self.current_sensitivity
        )

        # 4. Trigger correction if error detected
        if error_detected:
            correction = self.trigger_correction(error_magnitude=error_magnitude)
        else:
            correction = {
                "control_boost": 0.0,
                "post_error_slowing_ms": 0.0
            }

        # 5. Update sensitivity based on recent history
        if len(self.error_history) >= 10:
            error_freq = sum(self.error_history[-10:]) / 10.0
            # Assume correction success = inverse of error frequency (simplified)
            correction_success = 1.0 - error_freq
            self.update_sensitivity(error_freq, correction_success)

        # 6. Return complete result
        return {
            "conflict_level": float(conflict),
            "error_detected": bool(error_detected),
            "error_magnitude": float(error_magnitude),
            "ern_amplitude": float(ern_amplitude),
            "correction": correction
        }

    def get_state(self) -> Dict:
        """
        Get current error detection system state

        Returns:
        --------
        state : Dict
            {
                "sensitivity": float,
                "conflict_level": float,
                "errors_detected": int,
                "corrections_applied": int,
                "detection_rate": float,
                "false_alarm_rate": float,
                "average_ern": float
            }
        """
        # Detection rate (proportion of history with errors)
        if len(self.error_history) > 0:
            detection_rate = sum(self.error_history) / len(self.error_history)
        else:
            detection_rate = 0.0

        # False alarm rate (simplified: assume 10% of detections are false)
        false_alarm_rate = detection_rate * 0.1

        # Average ERN from recent errors
        average_ern = 10.0 if detection_rate > 0 else 0.0

        return {
            "sensitivity": float(self.current_sensitivity),
            "conflict_level": float(self.conflict_level),
            "errors_detected": int(self.errors_detected),
            "corrections_applied": int(self.corrections_applied),
            "detection_rate": float(detection_rate),
            "false_alarm_rate": float(false_alarm_rate),
            "average_ern": float(average_ern)
        }
