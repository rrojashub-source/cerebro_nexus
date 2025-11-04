"""
LAB_033: Metaphor Generation - Metaphorical Thinking

Implements metaphor understanding and generation:
- Lakoff & Johnson (1980): Metaphors We Live By
- Glucksberg (2003): Psychology of metaphor comprehension
- Bowdle & Gentner (2005): Career of metaphor theory
- Kövecses (2010): Conceptual metaphor theory

Core Functions:
1. Conceptual metaphor representation (source→target domain)
2. Metaphor generation from domain mappings
3. Metaphor comprehension and interpretation
4. Conventional vs novel metaphor distinction
5. Dead metaphor detection
6. Cross-domain mapping

Neuroscience Foundation:
- Left inferior frontal: Metaphor selection
- Right hemisphere: Novel metaphor processing
- Temporal cortex: Semantic integration
- Inferior parietal: Cross-domain mapping

Integration:
- ← LAB_030 (Conceptual Blending) for domain integration
- ← LAB_032 (Analogical Reasoning) for structural mapping
- ← LAB_029 (Divergent Thinking) for creative metaphors
"""

import time
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np


class MetaphorType(Enum):
    """Types of metaphors"""
    CONCEPTUAL = "conceptual"  # Systematic mapping (LIFE IS JOURNEY)
    NOVEL = "novel"  # Creative, unfamiliar
    CONVENTIONAL = "conventional"  # Common, entrenched
    DEAD = "dead"  # Literal meaning lost


class Domain(Enum):
    """Conceptual domains"""
    JOURNEY = "journey"
    WAR = "war"
    BUILDING = "building"
    CONTAINER = "container"
    MACHINE = "machine"
    ORGANISM = "organism"
    LIGHT = "light"
    DARKNESS = "darkness"
    TIME = "time"
    SPACE = "space"


@dataclass
class ConceptualMetaphor:
    """Conceptual metaphor (e.g., LOVE IS JOURNEY)"""
    metaphor_id: str
    target_domain: str  # Abstract concept (e.g., "love")
    source_domain: Domain  # Concrete domain (e.g., JOURNEY)
    mappings: Dict[str, str]  # source_concept -> target_concept
    entailments: List[str]  # Inferences (e.g., "lovers are travelers")
    conventionality: float  # 0-1 (1 = very conventional)


@dataclass
class MetaphoricalExpression:
    """Specific metaphorical expression"""
    expression: str
    underlying_metaphor: str  # Conceptual metaphor ID
    source_phrase: str
    target_phrase: str
    novelty: float  # 0-1 (1 = highly novel)
    comprehensibility: float  # 0-1


@dataclass
class MetaphorGeneration:
    """Generated metaphor"""
    timestamp: float
    target_concept: str
    source_domain: Domain
    generated_expression: str
    novelty_score: float
    aptness_score: float  # How well source fits target


class ConceptualMetaphorRepository:
    """Repository of conceptual metaphors"""

    def __init__(self):
        # Common conceptual metaphors (Lakoff & Johnson)
        self.metaphors = {
            "LIFE_IS_JOURNEY": ConceptualMetaphor(
                metaphor_id="LIFE_IS_JOURNEY",
                target_domain="life",
                source_domain=Domain.JOURNEY,
                mappings={
                    "traveler": "person",
                    "path": "life_course",
                    "destination": "goal",
                    "obstacles": "difficulties",
                    "vehicle": "means",
                },
                entailments=[
                    "People have life goals (destinations)",
                    "Life has direction (path)",
                    "Progress can be blocked (obstacles)",
                ],
                conventionality=0.95
            ),
            "ARGUMENT_IS_WAR": ConceptualMetaphor(
                metaphor_id="ARGUMENT_IS_WAR",
                target_domain="argument",
                source_domain=Domain.WAR,
                mappings={
                    "opponent": "debater",
                    "attack": "criticize",
                    "defend": "support",
                    "win": "convince",
                    "strategy": "argumentation_method",
                },
                entailments=[
                    "Arguments have winners and losers",
                    "Claims can be attacked or defended",
                ],
                conventionality=0.90
            ),
            "THEORIES_ARE_BUILDINGS": ConceptualMetaphor(
                metaphor_id="THEORIES_ARE_BUILDINGS",
                target_domain="theory",
                source_domain=Domain.BUILDING,
                mappings={
                    "foundation": "basic_assumptions",
                    "structure": "logical_framework",
                    "collapse": "refutation",
                    "solid": "well_supported",
                },
                entailments=[
                    "Theories need solid foundations",
                    "Theories can collapse under scrutiny",
                ],
                conventionality=0.85
            ),
            "MIND_IS_MACHINE": ConceptualMetaphor(
                metaphor_id="MIND_IS_MACHINE",
                target_domain="mind",
                source_domain=Domain.MACHINE,
                mappings={
                    "parts": "mental_faculties",
                    "breakdown": "mental_disorder",
                    "repair": "therapy",
                    "fuel": "motivation",
                },
                entailments=[
                    "Minds have components",
                    "Minds can malfunction",
                ],
                conventionality=0.80
            ),
        }

    def get_metaphor(self, metaphor_id: str) -> Optional[ConceptualMetaphor]:
        """Get conceptual metaphor by ID"""
        return self.metaphors.get(metaphor_id)

    def get_metaphors_for_target(self, target_domain: str) -> List[ConceptualMetaphor]:
        """Get all metaphors for target domain"""
        return [m for m in self.metaphors.values() if m.target_domain == target_domain]


class MetaphorGenerator:
    """Generates metaphorical expressions"""

    def __init__(self, repository: ConceptualMetaphorRepository):
        self.repository = repository

    def generate_from_conceptual_metaphor(
        self,
        metaphor_id: str,
        target_element: str
    ) -> Optional[MetaphoricalExpression]:
        """
        Generate expression from conceptual metaphor.

        Returns metaphorical expression.
        """
        metaphor = self.repository.get_metaphor(metaphor_id)
        if not metaphor:
            return None

        # Find corresponding source element
        source_element = None
        for source, target in metaphor.mappings.items():
            if target == target_element:
                source_element = source
                break

        if not source_element:
            return None

        # Generate expression
        expression = f"X is {source_element}"  # Template
        source_phrase = source_element
        target_phrase = target_element

        # Novelty (lower for conventional metaphors)
        novelty = 1.0 - metaphor.conventionality + np.random.uniform(-0.1, 0.1)
        novelty = np.clip(novelty, 0.0, 1.0)

        # Comprehensibility (higher for conventional)
        comprehensibility = metaphor.conventionality

        return MetaphoricalExpression(
            expression=expression,
            underlying_metaphor=metaphor_id,
            source_phrase=source_phrase,
            target_phrase=target_phrase,
            novelty=novelty,
            comprehensibility=comprehensibility
        )

    def generate_novel_metaphor(
        self,
        target_concept: str,
        source_domain: Domain
    ) -> MetaphorGeneration:
        """
        Generate novel metaphor for target using source domain.

        Returns metaphor generation.
        """
        # Generate metaphorical expression (creative)
        expressions = [
            f"{target_concept} is a {source_domain.value}",
            f"{target_concept} flows like {source_domain.value}",
            f"{target_concept} mirrors {source_domain.value}",
        ]

        expression = expressions[np.random.randint(0, len(expressions))]

        # Novelty (high for novel metaphors)
        novelty = np.random.uniform(0.7, 0.95)

        # Aptness (how well it fits)
        # In real system: compute semantic similarity
        aptness = np.random.uniform(0.5, 0.9)

        return MetaphorGeneration(
            timestamp=time.time(),
            target_concept=target_concept,
            source_domain=source_domain,
            generated_expression=expression,
            novelty_score=novelty,
            aptness_score=aptness
        )


class MetaphorComprehension:
    """Comprehends and interprets metaphors"""

    def __init__(self, repository: ConceptualMetaphorRepository):
        self.repository = repository

    def comprehend_metaphor(
        self,
        expression: str,
        target_hint: Optional[str] = None
    ) -> Dict:
        """
        Comprehend metaphorical expression.

        Returns interpretation.
        """
        # Simple pattern matching (in real system: NLP)
        expression_lower = expression.lower()

        # Try to identify underlying conceptual metaphor
        for metaphor in self.repository.metaphors.values():
            # Check if any source mapping appears in expression
            for source_term, target_term in metaphor.mappings.items():
                if source_term.lower() in expression_lower:
                    # Found match
                    return {
                        "understood": True,
                        "conceptual_metaphor": metaphor.metaphor_id,
                        "source_domain": metaphor.source_domain.value,
                        "target_domain": metaphor.target_domain,
                        "interpretation": f"'{expression}' uses {metaphor.source_domain.value} to understand {metaphor.target_domain}",
                        "conventionality": metaphor.conventionality,
                    }

        # Novel metaphor (not in repository)
        return {
            "understood": False,
            "conceptual_metaphor": None,
            "interpretation": "Novel metaphor requiring creative interpretation",
        }


class MetaphorGenerationSystem:
    """
    Main LAB_033 implementation.

    Manages:
    - Conceptual metaphor repository
    - Metaphor generation
    - Metaphor comprehension
    """

    def __init__(self):
        # Components
        self.repository = ConceptualMetaphorRepository()
        self.generator = MetaphorGenerator(self.repository)
        self.comprehension = MetaphorComprehension(self.repository)

        # History
        self.generated_metaphors: List[MetaphorGeneration] = []
        self.expressions: List[MetaphoricalExpression] = []

    def generate_conventional_metaphor(
        self,
        metaphor_id: str,
        target_element: str
    ) -> Optional[MetaphoricalExpression]:
        """
        Generate conventional metaphorical expression.

        Returns expression.
        """
        expression = self.generator.generate_from_conceptual_metaphor(
            metaphor_id,
            target_element
        )

        if expression:
            self.expressions.append(expression)

        return expression

    def generate_novel_metaphor(
        self,
        target_concept: str,
        source_domain: Domain
    ) -> MetaphorGeneration:
        """
        Generate novel metaphor.

        Returns generated metaphor.
        """
        metaphor = self.generator.generate_novel_metaphor(target_concept, source_domain)
        self.generated_metaphors.append(metaphor)

        return metaphor

    def interpret_metaphor(self, expression: str) -> Dict:
        """
        Interpret metaphorical expression.

        Returns interpretation.
        """
        return self.comprehension.comprehend_metaphor(expression)

    def list_conceptual_metaphors(self) -> List[str]:
        """List all conceptual metaphors in repository"""
        return list(self.repository.metaphors.keys())

    def get_metaphor_details(self, metaphor_id: str) -> Optional[Dict]:
        """Get details of conceptual metaphor"""
        metaphor = self.repository.get_metaphor(metaphor_id)
        if not metaphor:
            return None

        return {
            "id": metaphor.metaphor_id,
            "target_domain": metaphor.target_domain,
            "source_domain": metaphor.source_domain.value,
            "mappings": metaphor.mappings,
            "entailments": metaphor.entailments,
            "conventionality": metaphor.conventionality,
        }

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics"""
        return {
            "conceptual_metaphors": len(self.repository.metaphors),
            "generated_novel": len(self.generated_metaphors),
            "generated_conventional": len(self.expressions),
            "avg_novelty": (np.mean([m.novelty_score for m in self.generated_metaphors])
                           if self.generated_metaphors else 0.0),
            "avg_aptness": (np.mean([m.aptness_score for m in self.generated_metaphors])
                           if self.generated_metaphors else 0.0),
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_033: Metaphor Generation - Test")
    print("=" * 60)

    system = MetaphorGenerationSystem()

    # Scenario 1: List conceptual metaphors
    print("\n📚 Scenario 1: Conceptual Metaphors in Repository...")
    metaphors = system.list_conceptual_metaphors()
    print(f"  Total: {len(metaphors)}")
    for m_id in metaphors:
        details = system.get_metaphor_details(m_id)
        print(f"  • {m_id}: {details['target_domain']} IS {details['source_domain']}")

    # Scenario 2: Examine LIFE IS JOURNEY metaphor
    print("\n🛤️ Scenario 2: LIFE IS JOURNEY Metaphor Details...")
    details = system.get_metaphor_details("LIFE_IS_JOURNEY")
    print(f"  Target domain: {details['target_domain']}")
    print(f"  Source domain: {details['source_domain']}")
    print(f"  Conventionality: {details['conventionality']:.3f}")
    print(f"\n  Mappings:")
    for source, target in details['mappings'].items():
        print(f"    {source} → {target}")
    print(f"\n  Entailments:")
    for ent in details['entailments']:
        print(f"    • {ent}")

    # Scenario 3: Generate conventional metaphorical expression
    print("\n💬 Scenario 3: Generating Conventional Expression...")
    expression = system.generate_conventional_metaphor(
        "ARGUMENT_IS_WAR",
        "criticize"
    )
    if expression:
        print(f"  Expression: '{expression.expression}'")
        print(f"  Source: {expression.source_phrase} (from {expression.underlying_metaphor})")
        print(f"  Target: {expression.target_phrase}")
        print(f"  Novelty: {expression.novelty:.3f}")
        print(f"  Comprehensibility: {expression.comprehensibility:.3f}")

    # Scenario 4: Generate novel metaphor
    print("\n✨ Scenario 4: Generating Novel Metaphor...")
    novel = system.generate_novel_metaphor("consciousness", Domain.LIGHT)
    print(f"  Generated: '{novel.generated_expression}'")
    print(f"  Target: {novel.target_concept}")
    print(f"  Source domain: {novel.source_domain.value}")
    print(f"  Novelty: {novel.novelty_score:.3f}")
    print(f"  Aptness: {novel.aptness_score:.3f}")

    # Generate another
    novel2 = system.generate_novel_metaphor("memory", Domain.CONTAINER)
    print(f"\n  Generated: '{novel2.generated_expression}'")
    print(f"  Novelty: {novel2.novelty_score:.3f}")

    # Scenario 5: Comprehend metaphor
    print("\n🔍 Scenario 5: Comprehending Metaphorical Expressions...")

    test_expressions = [
        "She attacked every weak point in my argument",
        "His theory collapsed under scrutiny",
        "Consciousness is a dancing flame",  # Novel
    ]

    for expr in test_expressions:
        interpretation = system.interpret_metaphor(expr)
        print(f"\n  Expression: '{expr}'")
        print(f"  Understood: {interpretation.get('understood', 'unknown')}")
        if interpretation.get('conceptual_metaphor'):
            print(f"  Conceptual metaphor: {interpretation['conceptual_metaphor']}")
            print(f"  Source domain: {interpretation['source_domain']}")
            print(f"  Target domain: {interpretation['target_domain']}")
            print(f"  Conventionality: {interpretation['conventionality']:.3f}")
        else:
            print(f"  Interpretation: {interpretation.get('interpretation', 'Unknown')}")

    # Final statistics
    print("\n📊 Final Statistics:")
    stats = system.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

    print("\n✅ LAB_033 Test Complete!")
