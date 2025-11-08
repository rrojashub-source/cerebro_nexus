"""
LAB_025: Insight & Aha Moments

Function: Sudden insight through problem restructuring, impasse breaking
Neuroscience Basis: Anterior cingulate cortex, right hemisphere (sudden reorganization)

Key Papers:
- Metcalfe & Wiebe (1987) - Intuition in insight and non-insight problem solving
- Ohlsson (1992) - Information-processing explanations of insight
"""

from typing import Dict, List, Tuple
import random


class InsightSystem:
    """
    LAB_025: Insight & Aha Moments

    Models sudden insight through:
    - Impasse detection (stuck state recognition)
    - Incubation (unconscious processing)
    - Problem restructuring (representation change)
    - Solution emergence (sudden clarity)
    - Aha signal (subjective insight feeling)

    Parameters:
    -----------
    impasse_threshold : int
        Failed attempts to trigger incubation (default: 3)
    incubation_duration : float
        Seconds for unconscious processing (default: 120.0)
    aha_confidence_threshold : float
        Confidence to signal insight (default: 0.8)
    restructuring_rate : float
        Rate of problem space exploration (default: 0.15)
    """

    def __init__(
        self,
        impasse_threshold: int = 3,
        incubation_duration: float = 120.0,
        aha_confidence_threshold: float = 0.8,
        restructuring_rate: float = 0.15
    ):
        # Configuration
        self.impasse_threshold = impasse_threshold
        self.incubation_duration = incubation_duration
        self.aha_confidence_threshold = aha_confidence_threshold
        self.restructuring_rate = restructuring_rate

        # State
        self.total_problems_attempted: int = 0
        self.insights_achieved: int = 0
        self.avg_solving_time: float = 0.0
        self.insight_success_rate: float = 0.0

    def detect_impasse(self, failed_attempts: int, progress: float) -> bool:
        """
        Recognize stuck state (impasse)

        Impasse = high failures + no progress
        Triggers need for incubation/restructuring

        Parameters:
        -----------
        failed_attempts : int
            Number of failed solving attempts
        progress : float
            Progress toward solution (0.0-1.0)

        Returns:
        --------
        is_impasse : bool
            True if stuck (impasse detected)
        """
        # Impasse requires BOTH:
        # 1. Failed attempts >= threshold
        # 2. No significant progress (< 0.2)

        if failed_attempts >= self.impasse_threshold and progress < 0.2:
            return True

        return False

    def initiate_incubation(self, problem: Dict) -> float:
        """
        Reduce focused attention, allow unconscious processing

        Incubation = step away from problem
        Integration with LAB_046 (DMN - Default Mode Network)

        Parameters:
        -----------
        problem : Dict
            Problem to incubate on

        Returns:
        --------
        incubation_time : float
            Recommended incubation duration (seconds)
        """
        # Base incubation time
        incubation_time = self.incubation_duration

        # Adjust by problem complexity (simulated)
        complexity = problem.get("complexity", "medium")
        if complexity == "high":
            incubation_time *= 1.5
        elif complexity == "low":
            incubation_time *= 0.5

        return incubation_time

    def restructure_problem(self, problem: Dict, approach: str) -> Dict:
        """
        Change problem representation

        Ohlsson (1992): Insight = removing mental blocks via restructuring

        Approaches:
        - constraint_relaxation: Remove limiting assumptions
        - analogy: Map to different domain (LAB_024)
        - decomposition: Break into subproblems

        Parameters:
        -----------
        problem : Dict
            Original problem representation
        approach : str
            Restructuring method

        Returns:
        --------
        restructured : Dict
            New problem representation
        """
        valid_approaches = ["constraint_relaxation", "analogy", "decomposition"]
        if approach not in valid_approaches:
            raise ValueError(f"Invalid approach: {approach}. Must be one of {valid_approaches}")

        restructured = problem.copy()
        restructured["restructured"] = True
        restructured["approach"] = approach

        if approach == "constraint_relaxation":
            # Remove or relax constraints
            original_constraints = problem.get("constraints", [])
            if len(original_constraints) > 0:
                # Relax one constraint
                relaxed = original_constraints.copy()
                relaxed.pop(0)  # Remove first constraint
                restructured["constraints"] = relaxed
                restructured["relaxed_constraints"] = [original_constraints[0]]
            else:
                restructured["relaxed_constraints"] = ["implicit_constraint"]

        elif approach == "analogy":
            # Map to analogous domain (uses LAB_024 conceptual blending)
            restructured["analogy"] = "mapped_to_analogous_domain"
            restructured["reframed"] = True
            restructured["blend"] = "source_target_mapping"

            # Example: Duncker radiation → fortress problem
            if "radiation" in problem.get("description", "").lower():
                restructured["analogy"] = "fortress_with_converging_paths"

        elif approach == "decomposition":
            # Break into subproblems
            restructured["subproblems"] = [
                {"part": 1, "description": "subproblem_1"},
                {"part": 2, "description": "subproblem_2"}
            ]
            restructured["parts"] = 2

        # Change representation (if applicable)
        if "representation" in problem:
            # Change from algebraic to geometric, etc.
            current_rep = problem["representation"]
            if current_rep == "algebraic":
                restructured["representation"] = "geometric"
            elif current_rep == "verbal":
                restructured["representation"] = "visual"
            else:
                restructured["representation"] = "reframed"

        return restructured

    def detect_solution_emergence(self, restructured: Dict, original: Dict) -> bool:
        """
        Check if restructuring revealed solution

        Sudden clarity = confidence spike

        Parameters:
        -----------
        restructured : Dict
            Problem after restructuring
        original : Dict
            Original problem state

        Returns:
        --------
        emerged : bool
            True if solution became clear
        """
        # Check confidence spike
        conf_original = original.get("confidence", 0.0)
        conf_restructured = restructured.get("confidence", 0.0)

        # Confidence must exceed threshold
        if conf_restructured < self.aha_confidence_threshold:
            return False

        # Large spike indicates insight
        confidence_increase = conf_restructured - conf_original
        if confidence_increase > 0.5:
            return True

        # Check explicit solution visibility
        if restructured.get("solution_visible", False):
            return True

        return False

    def generate_aha_signal(self, confidence: float) -> Dict:
        """
        Subjective insight feeling (Aha! moment)

        Integration with LAB_013 (Dopamine burst on reward)

        Parameters:
        -----------
        confidence : float
            Solution confidence (0.0-1.0)

        Returns:
        --------
        aha : Dict
            Aha signal with intensity
        """
        # Intensity proportional to confidence
        # High confidence = strong Aha
        # Low confidence = weak or no Aha
        intensity = max(0.0, (confidence - 0.5) * 2.0)  # Scale: 0.5 → 0, 1.0 → 1.0

        aha = {
            "intensity": intensity,
            "confidence": confidence
        }

        # Dopamine burst on strong Aha (LAB_013 integration)
        if intensity > 0.6:
            aha["dopamine_burst"] = True
            aha["reward_signal"] = intensity * 0.8

        return aha

    def compute_warmth(self, progress_history: List[float]) -> float:
        """
        Metcalfe & Wiebe (1987) warmth ratings

        Warmth = feeling of closeness to solution

        Patterns:
        - Analytic solving: gradual warmth increase
        - Insight solving: flat warmth then sudden spike

        Parameters:
        -----------
        progress_history : List[float]
            Progress values over time

        Returns:
        --------
        warmth : float
            Final warmth rating (0.0-1.0)
        """
        if len(progress_history) == 0:
            return 0.0

        # Final warmth = last progress value
        final_warmth = progress_history[-1]

        # Check trajectory shape (for distinguishing analytic vs insight)
        # Analytic: steady increase (low variance early, steady slope)
        # Insight: flat then spike (low early, high variance at end)

        # For now, return final warmth
        # (Advanced: compute trajectory variance to classify solving type)
        return final_warmth

    def process_event(self, problem: Dict) -> Dict:
        """
        Main processing: attempt insight solving

        Workflow:
        1. Check for impasse
        2. If impasse → incubate
        3. Restructure problem
        4. Check solution emergence
        5. Generate Aha if insight occurred

        Parameters:
        -----------
        problem : Dict
            Problem to solve

        Returns:
        --------
        result : Dict
            Complete insight solving result
        """
        # 1. Extract problem state
        attempts = problem.get("attempts", 0)
        progress = problem.get("progress", 0.0)

        # 2. Check impasse
        is_impasse = self.detect_impasse(attempts, progress)

        incubation_triggered = False
        if is_impasse:
            # Trigger incubation
            incubation_time = self.initiate_incubation(problem)
            incubation_triggered = True
        else:
            incubation_time = 0.0

        # 3. Restructure (try multiple approaches if impasse)
        restructured = None
        insight_occurred = False

        if is_impasse or attempts > 2:
            # Try restructuring
            # Randomly select approach (simulated)
            approaches = ["constraint_relaxation", "analogy", "decomposition"]
            approach = random.choice(approaches)

            try:
                restructured = self.restructure_problem(problem, approach=approach)

                # Simulate confidence after restructuring
                # If restructuring successful, confidence spikes
                if random.random() > 0.5:  # 50% chance of breakthrough
                    restructured["confidence"] = 0.85 + random.random() * 0.15
                    insight_occurred = True
                else:
                    restructured["confidence"] = 0.3 + random.random() * 0.2

            except ValueError:
                restructured = problem
        else:
            restructured = problem

        # 4. Check solution emergence
        if restructured:
            emerged = self.detect_solution_emergence(restructured, problem)
            if emerged:
                insight_occurred = True

        # 5. Generate Aha if insight occurred
        aha = None
        if insight_occurred:
            final_confidence = restructured.get("confidence", 0.5)
            aha = self.generate_aha_signal(final_confidence)

            # Update stats
            self.insights_achieved += 1

        # 6. Update state
        self.total_problems_attempted += 1

        # Update success rate
        if self.total_problems_attempted > 0:
            self.insight_success_rate = self.insights_achieved / self.total_problems_attempted

        # 7. Return result
        result = {
            "insight_occurred": insight_occurred,
            "restructured_problem": restructured,
            "incubation_triggered": incubation_triggered,
            "incubation_time": incubation_time
        }

        if insight_occurred and aha:
            result["aha_signal"] = aha
            result["aha_intensity"] = aha["intensity"]
            result["solution"] = "Solution found via restructuring"
            result["restructuring_type"] = restructured.get("approach", "unknown")

        return result

    def get_state(self) -> Dict:
        """Get current insight system state"""
        return {
            "total_problems": int(self.total_problems_attempted),
            "insights_achieved": int(self.insights_achieved),
            "insight_success_rate": float(self.insight_success_rate),
            "avg_solving_time": float(self.avg_solving_time),
            "impasse_threshold": int(self.impasse_threshold),
            "aha_confidence_threshold": float(self.aha_confidence_threshold)
        }
