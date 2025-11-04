"""
LAB_029: Divergent Thinking - Idea Generation and Creative Fluency

Implements divergent thinking and creative ideation:
- Guilford (1967): Structure of intellect, divergent production
- Torrance (1966): Torrance Tests of Creative Thinking
- Runco & Acar (2012): Divergent thinking as indicator of creativity
- Benedek et al. (2014): Neural correlates of creative cognition

Core Functions:
1. Alternative uses generation (Guilford's brick test)
2. Fluency measurement (quantity of ideas)
3. Flexibility measurement (category diversity)
4. Originality scoring (statistical rarity)
5. Elaboration (detail richness)
6. Remote associates test

Neuroscience Foundation:
- Prefrontal cortex: Idea generation control
- Temporal cortex: Semantic memory access
- Default mode network: Spontaneous ideation
- Reduced cognitive control allows broader associations

Integration:
- ← LAB_010 (Attention) for focused vs diffuse attention
- ← LAB_013 (Dopamine) for exploratory drive
- ← LAB_019 (Cognitive Control) for inhibition release
- → LAB_030 (Conceptual Blending) for combining ideas
"""

import time
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import numpy as np
from enum import Enum


class IdeaCategory(Enum):
    """Idea categories for flexibility scoring"""
    PHYSICAL = "physical"
    FUNCTIONAL = "functional"
    SOCIAL = "social"
    ABSTRACT = "abstract"
    AESTHETIC = "aesthetic"
    SYMBOLIC = "symbolic"


@dataclass
class Idea:
    """Generated idea"""
    content: str
    category: IdeaCategory
    originality_score: float  # 0-1 (1 = highly original)
    elaboration_level: int  # 0-5 (detail richness)
    timestamp: float


@dataclass
class DivergentSession:
    """Divergent thinking session"""
    session_id: str
    prompt: str
    ideas: List[Idea]
    duration: float
    fluency: int  # Total ideas
    flexibility: int  # Number of categories
    originality_avg: float  # Average originality
    elaboration_avg: float  # Average elaboration


@dataclass
class RemoteAssociate:
    """Remote associates problem"""
    word_1: str
    word_2: str
    word_3: str
    solution: Optional[str]
    timestamp: float
    solved: bool


class AlternativeUsesGenerator:
    """Generates alternative uses (Guilford's brick test)"""

    def __init__(self):
        # Knowledge base of objects and potential uses
        self.object_properties = {
            "brick": ["hard", "heavy", "rectangular", "stackable", "red"],
            "paperclip": ["bendable", "metal", "small", "pointed"],
            "shoe": ["wearable", "leather", "flexible", "hollow"],
            "bottle": ["hollow", "cylindrical", "transparent", "closeable"],
        }

        self.use_templates = {
            "hard": ["Use as hammer", "Use as weight", "Use for defense"],
            "hollow": ["Use as container", "Use as vessel", "Use as pipe"],
            "bendable": ["Reshape into tool", "Use as hook", "Form into shape"],
            "stackable": ["Build structure", "Create tower", "Make furniture"],
            "pointed": ["Use as pin", "Use to pierce", "Use for marking"],
        }

    def generate_uses(
        self,
        object_name: str,
        num_ideas: int = 10,
        allow_common: bool = True
    ) -> List[Idea]:
        """
        Generate alternative uses for object.

        Returns list of ideas with originality scores.
        """
        if object_name not in self.object_properties:
            # Generic generation
            properties = ["physical_object", "manipulable"]
        else:
            properties = self.object_properties[object_name]

        ideas = []
        used_uses = set()

        # Generate from properties
        for prop in properties:
            if prop in self.use_templates:
                for use_template in self.use_templates[prop]:
                    use = use_template.replace("Use", f"Use {object_name}")

                    if use in used_uses:
                        continue

                    used_uses.add(use)

                    # Categorize
                    category = self._categorize_use(use)

                    # Originality (lower for common uses)
                    originality = np.random.uniform(0.3, 0.9)
                    if not allow_common and originality < 0.5:
                        continue

                    # Elaboration (random for now)
                    elaboration = np.random.randint(1, 4)

                    ideas.append(Idea(
                        content=use,
                        category=category,
                        originality_score=originality,
                        elaboration_level=elaboration,
                        timestamp=time.time()
                    ))

                    if len(ideas) >= num_ideas:
                        break

            if len(ideas) >= num_ideas:
                break

        # Generate creative/unusual uses
        if len(ideas) < num_ideas:
            creative_uses = [
                f"Use {object_name} as art material",
                f"Use {object_name} as musical instrument",
                f"Use {object_name} in game/sport",
                f"Use {object_name} for scientific experiment",
                f"Use {object_name} as teaching tool",
            ]

            for use in creative_uses:
                if len(ideas) >= num_ideas:
                    break

                if use in used_uses:
                    continue

                ideas.append(Idea(
                    content=use,
                    category=IdeaCategory.ABSTRACT,
                    originality_score=np.random.uniform(0.7, 0.95),
                    elaboration_level=np.random.randint(2, 5),
                    timestamp=time.time()
                ))

        return ideas[:num_ideas]

    def _categorize_use(self, use: str) -> IdeaCategory:
        """Categorize use into category"""
        use_lower = use.lower()

        if any(word in use_lower for word in ["hammer", "weight", "build", "structure"]):
            return IdeaCategory.PHYSICAL
        elif any(word in use_lower for word in ["container", "holder", "vessel"]):
            return IdeaCategory.FUNCTIONAL
        elif any(word in use_lower for word in ["art", "decoration", "aesthetic"]):
            return IdeaCategory.AESTHETIC
        elif any(word in use_lower for word in ["teaching", "learning", "education"]):
            return IdeaCategory.SOCIAL
        else:
            return IdeaCategory.FUNCTIONAL


class FluencyMeasure:
    """Measures ideational fluency"""

    def __init__(self):
        pass

    def compute_fluency(self, ideas: List[Idea], duration: float) -> Dict:
        """
        Compute fluency metrics.

        Returns fluency statistics.
        """
        total_ideas = len(ideas)
        ideas_per_minute = (total_ideas / duration) * 60.0 if duration > 0 else 0

        return {
            "total_ideas": total_ideas,
            "duration_seconds": duration,
            "ideas_per_minute": ideas_per_minute,
        }


class FlexibilityMeasure:
    """Measures cognitive flexibility in ideation"""

    def __init__(self):
        pass

    def compute_flexibility(self, ideas: List[Idea]) -> Dict:
        """
        Compute flexibility (number of different categories).

        Returns flexibility statistics.
        """
        categories = set(idea.category for idea in ideas)
        num_categories = len(categories)

        # Category distribution
        category_counts = defaultdict(int)
        for idea in ideas:
            category_counts[idea.category.value] += 1

        # Entropy (higher = more diverse)
        total = len(ideas)
        entropy = 0.0
        if total > 0:
            for count in category_counts.values():
                p = count / total
                if p > 0:
                    entropy -= p * np.log2(p)

        max_entropy = np.log2(len(IdeaCategory)) if len(IdeaCategory) > 0 else 1.0
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0.0

        return {
            "num_categories": num_categories,
            "category_distribution": dict(category_counts),
            "entropy": entropy,
            "normalized_entropy": normalized_entropy,
        }


class OriginalityScorer:
    """Scores originality of ideas"""

    def __init__(self):
        # Database of common ideas (in real system: large corpus)
        self.common_ideas = {
            "brick": [
                "use brick as doorstop",
                "use brick as weight",
                "use brick to build wall",
            ],
            "paperclip": [
                "use paperclip to hold papers",
                "use paperclip as bookmark",
            ],
        }

    def score_originality(
        self,
        idea: Idea,
        object_name: str,
        all_ideas: List[Idea]
    ) -> float:
        """
        Score originality (statistical rarity).

        Higher score = more unusual/creative.

        Returns originality score (0-1).
        """
        # Check if idea is common
        common_for_object = self.common_ideas.get(object_name, [])

        for common in common_for_object:
            if common.lower() in idea.content.lower():
                return np.random.uniform(0.1, 0.3)  # Low originality

        # Check if idea is unique in this session
        same_content = [i for i in all_ideas if i.content == idea.content]
        if len(same_content) > 1:
            return np.random.uniform(0.2, 0.4)  # Not unique

        # Check category rarity
        category_counts = defaultdict(int)
        for i in all_ideas:
            category_counts[i.category] += 1

        total = len(all_ideas)
        category_freq = category_counts[idea.category] / total if total > 0 else 0.5

        # Rare categories = more original
        rarity_score = 1.0 - category_freq

        # Combined originality
        originality = 0.5 + 0.5 * rarity_score

        return originality

    def update_originality_scores(
        self,
        ideas: List[Idea],
        object_name: str
    ) -> List[Idea]:
        """Update originality scores for all ideas in context"""
        for idea in ideas:
            idea.originality_score = self.score_originality(idea, object_name, ideas)

        return ideas

    def compute_originality(self, idea: Idea) -> float:
        """
        Compute originality for a single idea (API compatibility method).

        Returns the originality_score already calculated in the idea.
        """
        return idea.originality_score


class RemoteAssociatesTest:
    """Remote Associates Test (Mednick, 1962)"""

    def __init__(self):
        # RAT problems (word1, word2, word3) -> solution
        self.problems = [
            (("cottage", "swiss", "cake"), "cheese"),
            (("cream", "skate", "water"), "ice"),
            (("show", "life", "row"), "boat"),
            (("night", "wrist", "stop"), "watch"),
            (("duck", "fold", "dollar"), "bill"),
        ]

    def generate_problem(self) -> RemoteAssociate:
        """Generate RAT problem"""
        words, solution = self.problems[np.random.randint(0, len(self.problems))]

        return RemoteAssociate(
            word_1=words[0],
            word_2=words[1],
            word_3=words[2],
            solution=None,
            timestamp=time.time(),
            solved=False
        )

    def check_solution(
        self,
        problem: RemoteAssociate,
        proposed_solution: str
    ) -> bool:
        """Check if solution is correct"""
        # Find correct solution
        correct = None
        for words, solution in self.problems:
            if (words[0] == problem.word_1 and
                words[1] == problem.word_2 and
                words[2] == problem.word_3):
                correct = solution
                break

        if correct is None:
            return False

        return proposed_solution.lower().strip() == correct.lower().strip()

    def solve_problem(self, problem: RemoteAssociate) -> Optional[str]:
        """
        Attempt to solve RAT problem.

        Returns solution or None.
        """
        # Simple solver: check known problems
        for words, solution in self.problems:
            if (words[0] == problem.word_1 and
                words[1] == problem.word_2 and
                words[2] == problem.word_3):
                return solution

        return None


class DivergentThinkingSystem:
    """
    Main LAB_029 implementation.

    Manages:
    - Alternative uses generation
    - Fluency measurement
    - Flexibility measurement
    - Originality scoring
    - Remote associates
    """

    def __init__(self):
        # Components (nombres cortos para API compatibility)
        self.generator = AlternativeUsesGenerator()
        self.fluency = FluencyMeasure()
        self.flexibility = FlexibilityMeasure()
        self.originality = OriginalityScorer()
        self.rat_test = RemoteAssociatesTest()

        # History
        self.sessions: List[DivergentSession] = []
        self.session_counter = 0

    def generate_ideas(
        self,
        prompt: str,
        object_name: str,
        num_ideas: int = 10,
        time_limit: Optional[float] = None
    ) -> DivergentSession:
        """
        Generate ideas for prompt (e.g., alternative uses).

        Returns divergent session with metrics.
        """
        start_time = time.time()

        # Generate ideas
        ideas = self.generator.generate_uses(object_name, num_ideas)

        # Update originality scores in context
        ideas = self.originality.update_originality_scores(ideas, object_name)

        end_time = time.time()
        duration = end_time - start_time

        # Compute metrics
        fluency_metrics = self.fluency.compute_fluency(ideas, duration)
        flexibility_metrics = self.flexibility.compute_flexibility(ideas)

        # Average originality and elaboration
        originality_avg = np.mean([i.originality_score for i in ideas]) if ideas else 0.0
        elaboration_avg = np.mean([i.elaboration_level for i in ideas]) if ideas else 0.0

        # Create session
        session = DivergentSession(
            session_id=f"session_{self.session_counter:03d}",
            prompt=prompt,
            ideas=ideas,
            duration=duration,
            fluency=fluency_metrics["total_ideas"],
            flexibility=flexibility_metrics["num_categories"],
            originality_avg=originality_avg,
            elaboration_avg=elaboration_avg
        )

        self.sessions.append(session)
        self.session_counter += 1

        return session

    def test_remote_associates(self) -> RemoteAssociate:
        """
        Administer Remote Associates Test.

        Returns RAT problem.
        """
        problem = self.rat_test.generate_problem()

        # Attempt to solve
        solution = self.rat_test.solve_problem(problem)

        if solution:
            problem.solution = solution
            problem.solved = True

        return problem

    def compare_sessions(
        self,
        session_1_id: str,
        session_2_id: str
    ) -> Dict:
        """Compare two divergent thinking sessions"""
        session_1 = next((s for s in self.sessions if s.session_id == session_1_id), None)
        session_2 = next((s for s in self.sessions if s.session_id == session_2_id), None)

        if not session_1 or not session_2:
            return {}

        return {
            "fluency_diff": session_2.fluency - session_1.fluency,
            "flexibility_diff": session_2.flexibility - session_1.flexibility,
            "originality_diff": session_2.originality_avg - session_1.originality_avg,
            "elaboration_diff": session_2.elaboration_avg - session_1.elaboration_avg,
        }

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        if not self.sessions:
            return {
                "total_sessions": 0,
                "avg_fluency": 0.0,
                "avg_flexibility": 0.0,
                "avg_originality": 0.0,
            }

        return {
            "total_sessions": len(self.sessions),
            "avg_fluency": np.mean([s.fluency for s in self.sessions]),
            "avg_flexibility": np.mean([s.flexibility for s in self.sessions]),
            "avg_originality": np.mean([s.originality_avg for s in self.sessions]),
            "avg_elaboration": np.mean([s.elaboration_avg for s in self.sessions]),
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_029: Divergent Thinking - Test")
    print("=" * 60)

    system = DivergentThinkingSystem()

    # Scenario 1: Alternative uses test
    print("\n🧱 Scenario 1: Alternative Uses Test (Guilford's Brick)...")
    session = system.generate_ideas(
        prompt="Generate alternative uses for a brick",
        object_name="brick",
        num_ideas=8
    )

    print(f"  Session: {session.session_id}")
    print(f"  Duration: {session.duration:.3f}s")
    print(f"\n  Generated Ideas:")
    for i, idea in enumerate(session.ideas[:5], 1):
        print(f"    {i}. {idea.content}")
        print(f"       Category: {idea.category.value}, "
              f"Originality: {idea.originality_score:.3f}, "
              f"Elaboration: {idea.elaboration_level}")

    # Scenario 2: Fluency metrics
    print(f"\n📊 Scenario 2: Fluency Metrics...")
    fluency_metrics = system.fluency_measure.compute_fluency(session.ideas, session.duration)
    print(f"  Total ideas: {fluency_metrics['total_ideas']}")
    print(f"  Ideas per minute: {fluency_metrics['ideas_per_minute']:.1f}")

    # Scenario 3: Flexibility metrics
    print(f"\n🔄 Scenario 3: Flexibility Metrics...")
    flexibility_metrics = system.flexibility_measure.compute_flexibility(session.ideas)
    print(f"  Number of categories: {flexibility_metrics['num_categories']}")
    print(f"  Category distribution: {flexibility_metrics['category_distribution']}")
    print(f"  Normalized entropy: {flexibility_metrics['normalized_entropy']:.3f}")

    # Scenario 4: Originality scoring
    print(f"\n✨ Scenario 4: Originality Analysis...")
    print(f"  Average originality: {session.originality_avg:.3f}")
    print(f"  Most original ideas:")
    sorted_ideas = sorted(session.ideas, key=lambda x: x.originality_score, reverse=True)
    for i, idea in enumerate(sorted_ideas[:3], 1):
        print(f"    {i}. {idea.content} (originality: {idea.originality_score:.3f})")

    # Scenario 5: Remote Associates Test
    print(f"\n🔗 Scenario 5: Remote Associates Test...")
    problem = system.test_remote_associates()
    print(f"  Problem: {problem.word_1}, {problem.word_2}, {problem.word_3}")
    print(f"  Solution: {problem.solution}")
    print(f"  Solved: {problem.solved}")

    # Verify solution
    is_correct = system.rat_test.check_solution(problem, problem.solution)
    print(f"  Verified: {is_correct}")

    # Scenario 6: Multiple sessions comparison
    print(f"\n📈 Scenario 6: Comparing sessions...")
    session2 = system.generate_ideas(
        prompt="Generate alternative uses for a paperclip",
        object_name="paperclip",
        num_ideas=10
    )

    comparison = system.compare_sessions(session.session_id, session2.session_id)
    print(f"  Session 1 (brick): Fluency={session.fluency}, Flexibility={session.flexibility}")
    print(f"  Session 2 (paperclip): Fluency={session2.fluency}, Flexibility={session2.flexibility}")
    print(f"  Differences:")
    print(f"    Fluency: {comparison['fluency_diff']:+d}")
    print(f"    Flexibility: {comparison['flexibility_diff']:+d}")
    print(f"    Originality: {comparison['originality_diff']:+.3f}")

    # Final statistics
    print("\n📊 Final Statistics:")
    stats = system.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

    print("\n✅ LAB_029 Test Complete!")
