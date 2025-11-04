"""
LAB_031: Insight/Aha Moments - Sudden Problem Restructuring

Implements insight and sudden problem-solving:
- Kounios & Beeman (2014): Cognitive neuroscience of insight
- Ohlsson (1992): Information processing theory of insight
- Metcalfe & Wiebe (1987): Warmth ratings and insight
- Jung-Beeman et al. (2004): Neural activity during insight

Core Functions:
1. Problem representation and impasse detection
2. Incubation period (unconscious processing)
3. Sudden restructuring and "Aha!" experience
4. Constraint relaxation
5. Chunk decomposition
6. Insight evaluation (warmth, confidence)

Neuroscience Foundation:
- Right temporal cortex: Sudden comprehension
- Anterior cingulate: Impasse detection
- Prefrontal cortex: Problem representation
- Alpha/gamma burst: Moment before insight

Integration:
- ← LAB_010 (Attention) for defocused attention during incubation
- ← LAB_019 (Cognitive Control) for constraint relaxation
- ← LAB_030 (Conceptual Blending) for new perspectives
- → LAB_032 (Analogical Reasoning) for structural transfer
"""

import time
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np


class ProblemState(Enum):
    """Problem-solving state"""
    INITIAL = "initial"
    WORKING = "working"
    IMPASSE = "impasse"
    INCUBATING = "incubating"
    INSIGHT = "insight"
    SOLVED = "solved"


class InsightType(Enum):
    """Types of insight"""
    RESTRUCTURING = "restructuring"  # Reframe problem
    CONSTRAINT_RELAXATION = "constraint_relaxation"  # Remove assumed constraint
    CHUNK_DECOMPOSITION = "chunk_decomposition"  # Break apart mental chunk
    ANALOGY = "analogy"  # See similarity to known problem


@dataclass
class Problem:
    """Problem to solve"""
    problem_id: str
    description: str
    constraints: Set[str]
    initial_representation: str
    solution: Optional[str] = None


@dataclass
class ProblemAttempt:
    """Attempt to solve problem"""
    timestamp: float
    problem_id: str
    state: ProblemState
    representation: str
    constraints_active: Set[str]
    warmth_rating: float  # 0-1 (feeling of closeness)
    effort_level: float  # 0-1


@dataclass
class InsightMoment:
    """Insight experience"""
    timestamp: float
    problem_id: str
    insight_type: InsightType
    old_representation: str
    new_representation: str
    relaxed_constraint: Optional[str]
    aha_intensity: float  # 0-1 (strength of "Aha!")
    confidence: float  # 0-1
    solution_found: bool


class ImpasseDetector:
    """Detects when problem-solving reaches impasse"""

    def __init__(self):
        self.impasse_threshold = 3  # Number of failed attempts

    def detect_impasse(self, attempts: List[ProblemAttempt]) -> bool:
        """
        Detect if at impasse.

        Impasse indicators:
        - Multiple attempts with same representation
        - Low warmth ratings
        - High effort, low progress

        Returns True if at impasse.
        """
        if len(attempts) < self.impasse_threshold:
            return False

        recent = attempts[-self.impasse_threshold:]

        # Check if stuck with same representation
        representations = [a.representation for a in recent]
        if len(set(representations)) == 1:
            # Same representation repeatedly
            avg_warmth = np.mean([a.warmth_rating for a in recent])
            if avg_warmth < 0.3:
                return True

        # Check if warmth not increasing
        warmths = [a.warmth_rating for a in recent]
        if all(warmths[i] <= warmths[i-1] for i in range(1, len(warmths))):
            return True

        return False


class IncubationProcessor:
    """Handles incubation (unconscious processing)"""

    def __init__(self, incubation_duration: float = 2.0):
        self.incubation_duration = incubation_duration  # seconds

    def incubate(
        self,
        problem: Problem,
        current_representation: str
    ) -> str:
        """
        Incubation period.

        During incubation:
        - Unconscious processing
        - Constraint relaxation
        - Memory spreading activation

        Returns potentially new representation.
        """
        # Simulate incubation delay
        time.sleep(min(0.1, self.incubation_duration))  # Shortened for testing

        # Probabilistically generate new representation
        if np.random.random() < 0.6:
            # New perspective emerged
            return f"reframed_{current_representation}"
        else:
            return current_representation


class ConstraintRelaxer:
    """Relaxes problem constraints to enable insight"""

    def __init__(self):
        pass

    def identify_implicit_constraints(
        self,
        problem: Problem
    ) -> Set[str]:
        """
        Identify implicit (assumed) constraints.

        Returns set of implicit constraints.
        """
        # Explicit constraints
        explicit = problem.constraints

        # Infer implicit constraints from problem description
        implicit = set()

        desc_lower = problem.description.lower()

        if "connect" in desc_lower or "line" in desc_lower:
            implicit.add("lines_must_be_straight")
            implicit.add("must_stay_within_bounds")

        if "match" in desc_lower:
            implicit.add("matches_must_be_intact")

        return implicit

    def relax_constraint(
        self,
        problem: Problem,
        constraint: str
    ) -> Problem:
        """
        Relax (remove) constraint.

        Returns problem with constraint removed.
        """
        new_constraints = problem.constraints.copy()
        if constraint in new_constraints:
            new_constraints.remove(constraint)

        return Problem(
            problem_id=problem.problem_id,
            description=problem.description,
            constraints=new_constraints,
            initial_representation=problem.initial_representation,
            solution=problem.solution
        )


class InsightGenerator:
    """Generates insight moments"""

    def __init__(self):
        self.constraint_relaxer = ConstraintRelaxer()

    def generate_insight(
        self,
        problem: Problem,
        current_representation: str,
        active_constraints: Set[str]
    ) -> Optional[InsightMoment]:
        """
        Generate insight (if conditions met).

        Returns insight moment or None.
        """
        # Probabilistically generate insight
        insight_probability = 0.4

        if np.random.random() > insight_probability:
            return None

        # Choose insight type
        insight_types = list(InsightType)
        insight_type = insight_types[np.random.randint(0, len(insight_types))]

        # Generate new representation based on type
        if insight_type == InsightType.RESTRUCTURING:
            new_repr = f"restructured: {current_representation}"
            relaxed = None

        elif insight_type == InsightType.CONSTRAINT_RELAXATION:
            # Relax a constraint
            implicit_constraints = self.constraint_relaxer.identify_implicit_constraints(problem)
            all_constraints = active_constraints.union(implicit_constraints)

            if all_constraints:
                relaxed = list(all_constraints)[0]
                new_repr = f"relaxed {relaxed}: {current_representation}"
            else:
                relaxed = None
                new_repr = current_representation

        elif insight_type == InsightType.CHUNK_DECOMPOSITION:
            new_repr = f"decomposed chunks: {current_representation}"
            relaxed = None

        else:  # ANALOGY
            new_repr = f"analogous to known problem: {current_representation}"
            relaxed = None

        # Aha intensity (high for true insight)
        aha_intensity = np.random.uniform(0.7, 0.95)

        # Confidence (high after insight)
        confidence = np.random.uniform(0.8, 0.99)

        # Solution found?
        solution_found = np.random.random() < 0.7

        insight = InsightMoment(
            timestamp=time.time(),
            problem_id=problem.problem_id,
            insight_type=insight_type,
            old_representation=current_representation,
            new_representation=new_repr,
            relaxed_constraint=relaxed,
            aha_intensity=aha_intensity,
            confidence=confidence,
            solution_found=solution_found
        )

        return insight


class InsightAhaSystem:
    """
    Main LAB_031 implementation.

    Manages:
    - Problem representation
    - Impasse detection
    - Incubation
    - Insight generation
    - Constraint relaxation
    """

    def __init__(self):
        # Components
        self.impasse_detector = ImpasseDetector()
        self.incubation_processor = IncubationProcessor(incubation_duration=1.0)
        self.insight_generator = InsightGenerator()

        # State
        self.problems: Dict[str, Problem] = {}
        self.attempts: Dict[str, List[ProblemAttempt]] = {}
        self.insights: List[InsightMoment] = []

    def register_problem(
        self,
        problem_id: str,
        description: str,
        constraints: Optional[Set[str]] = None
    ) -> Problem:
        """Register new problem"""
        if constraints is None:
            constraints = set()

        problem = Problem(
            problem_id=problem_id,
            description=description,
            constraints=constraints,
            initial_representation=f"initial_{problem_id}"
        )

        self.problems[problem_id] = problem
        self.attempts[problem_id] = []

        return problem

    def attempt_solve(
        self,
        problem_id: str,
        representation: str,
        warmth_rating: float
    ) -> ProblemAttempt:
        """
        Attempt to solve problem.

        Returns attempt record.
        """
        problem = self.problems[problem_id]

        # Detect state
        attempts = self.attempts[problem_id]

        if self.impasse_detector.detect_impasse(attempts):
            state = ProblemState.IMPASSE
        elif warmth_rating > 0.8:
            state = ProblemState.SOLVED
        else:
            state = ProblemState.WORKING

        attempt = ProblemAttempt(
            timestamp=time.time(),
            problem_id=problem_id,
            state=state,
            representation=representation,
            constraints_active=problem.constraints,
            warmth_rating=warmth_rating,
            effort_level=0.7
        )

        self.attempts[problem_id].append(attempt)

        return attempt

    def incubate_problem(self, problem_id: str) -> str:
        """
        Incubate problem (unconscious processing).

        Returns new representation (potentially).
        """
        problem = self.problems[problem_id]
        attempts = self.attempts[problem_id]

        if not attempts:
            current_repr = problem.initial_representation
        else:
            current_repr = attempts[-1].representation

        # Incubate
        new_repr = self.incubation_processor.incubate(problem, current_repr)

        return new_repr

    def trigger_insight(
        self,
        problem_id: str
    ) -> Optional[InsightMoment]:
        """
        Attempt to trigger insight.

        Returns insight moment if successful.
        """
        problem = self.problems[problem_id]
        attempts = self.attempts[problem_id]

        if not attempts:
            return None

        current_attempt = attempts[-1]

        # Generate insight
        insight = self.insight_generator.generate_insight(
            problem,
            current_attempt.representation,
            current_attempt.constraints_active
        )

        if insight:
            self.insights.append(insight)

        return insight

    def solve_with_insight_protocol(
        self,
        problem_id: str,
        max_attempts: int = 10
    ) -> Dict:
        """
        Full insight problem-solving protocol.

        1. Initial attempts
        2. Detect impasse
        3. Incubate
        4. Generate insight
        5. Solve

        Returns solving history.
        """
        problem = self.problems[problem_id]

        history = {
            "attempts": [],
            "impasse_detected": False,
            "incubation_occurred": False,
            "insight_occurred": False,
            "solution_found": False,
        }

        for i in range(max_attempts):
            # Attempt with current representation
            attempts = self.attempts[problem_id]
            if not attempts:
                repr_ = problem.initial_representation
            else:
                repr_ = attempts[-1].representation

            warmth = np.random.uniform(0.1, 0.4 if i < 5 else 0.6)

            attempt = self.attempt_solve(problem_id, repr_, warmth)
            history["attempts"].append(attempt)

            # Check if impasse
            if attempt.state == ProblemState.IMPASSE:
                history["impasse_detected"] = True

                # Incubate
                new_repr = self.incubate_problem(problem_id)
                history["incubation_occurred"] = True

                # Try to trigger insight
                insight = self.trigger_insight(problem_id)

                if insight:
                    history["insight_occurred"] = True
                    history["insight"] = insight

                    if insight.solution_found:
                        history["solution_found"] = True
                        break

            # Check if solved
            if attempt.state == ProblemState.SOLVED:
                history["solution_found"] = True
                break

        return history

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        return {
            "total_problems": len(self.problems),
            "total_insights": len(self.insights),
            "avg_aha_intensity": (np.mean([i.aha_intensity for i in self.insights])
                                 if self.insights else 0.0),
            "avg_confidence": (np.mean([i.confidence for i in self.insights])
                              if self.insights else 0.0),
            "insight_types": {it.value: sum(1 for i in self.insights if i.insight_type == it)
                             for it in InsightType},
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_031: Insight/Aha Moments - Test")
    print("=" * 60)

    system = InsightAhaSystem()

    # Scenario 1: Nine-dot problem (classic insight problem)
    print("\n⚫ Scenario 1: Nine-Dot Problem...")
    problem = system.register_problem(
        problem_id="nine_dots",
        description="Connect 9 dots arranged in 3x3 grid with 4 straight lines without lifting pen",
        constraints={"pen_continuous", "lines_straight"}
    )
    print(f"  Problem: {problem.description}")
    print(f"  Explicit constraints: {problem.constraints}")

    # Simulate solving with insight protocol
    history = system.solve_with_insight_protocol("nine_dots", max_attempts=8)

    print(f"\n  Solving History:")
    print(f"    Total attempts: {len(history['attempts'])}")
    print(f"    Impasse detected: {history['impasse_detected']}")
    print(f"    Incubation occurred: {history['incubation_occurred']}")
    print(f"    Insight occurred: {history['insight_occurred']}")
    print(f"    Solution found: {history['solution_found']}")

    if history["insight_occurred"]:
        insight = history["insight"]
        print(f"\n  💡 INSIGHT:")
        print(f"    Type: {insight.insight_type.value}")
        print(f"    Old representation: {insight.old_representation}")
        print(f"    New representation: {insight.new_representation}")
        print(f"    Aha! intensity: {insight.aha_intensity:.3f}")
        print(f"    Confidence: {insight.confidence:.3f}")
        if insight.relaxed_constraint:
            print(f"    Relaxed constraint: {insight.relaxed_constraint}")

    # Scenario 2: Matchstick problem
    print("\n🔥 Scenario 2: Matchstick Arithmetic Problem...")
    problem2 = system.register_problem(
        problem_id="matchstick",
        description="Move one matchstick to make equation true: VI = VII - I",
        constraints={"matchsticks_intact", "one_move_only"}
    )

    # Attempt solving
    for i in range(3):
        warmth = np.random.uniform(0.2, 0.4)
        attempt = system.attempt_solve("matchstick", f"attempt_{i}", warmth)

    # Trigger insight
    insight2 = system.trigger_insight("matchstick")

    if insight2:
        print(f"  💡 INSIGHT:")
        print(f"    Type: {insight2.insight_type.value}")
        print(f"    Aha! intensity: {insight2.aha_intensity:.3f}")
        print(f"    Solution found: {insight2.solution_found}")

    # Scenario 3: Constraint relaxation
    print("\n🔓 Scenario 3: Identifying and relaxing implicit constraints...")
    constraints_nine_dots = system.insight_generator.constraint_relaxer.identify_implicit_constraints(problem)
    print(f"  Problem: Nine-dot")
    print(f"  Explicit constraints: {problem.constraints}")
    print(f"  Implicit constraints detected: {constraints_nine_dots}")

    # Relax one
    if constraints_nine_dots:
        to_relax = list(constraints_nine_dots)[0]
        relaxed_problem = system.insight_generator.constraint_relaxer.relax_constraint(problem, to_relax)
        print(f"  After relaxing '{to_relax}':")
        print(f"    New constraints: {relaxed_problem.constraints}")

    # Final statistics
    print("\n📊 Final Statistics:")
    stats = system.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        elif isinstance(value, dict):
            print(f"  {key}: {value}")
        else:
            print(f"  {key}: {value}")

    print("\n✅ LAB_031 Test Complete!")
