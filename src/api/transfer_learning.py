"""
LAB_034: Transfer Learning - Knowledge Transfer Across Domains

Implements transfer learning mechanisms:
- Thorndike & Woodworth (1901): Transfer of training theory
- Barnett & Ceci (2002): Taxonomy of transfer
- Perkins & Salomon (1992): Transfer of learning
- Day & Goldstone (2012): Analogical transfer

Core Functions:
1. Near transfer (similar contexts)
2. Far transfer (distant contexts)
3. Positive vs negative transfer
4. Learning-to-learn (meta-learning readiness)
5. Catastrophic forgetting prevention
6. Transfer distance measurement

Neuroscience Foundation:
- Prefrontal cortex: Abstract rule extraction
- Hippocampus: Contextual binding and transfer
- Striatum: Procedural skill transfer
- Medial temporal lobe: Declarative memory transfer

Integration:
- ← LAB_009 (Memory Reconsolidation) for updating transferred knowledge
- ← LAB_032 (Analogical Reasoning) for far transfer
- → LAB_036 (Meta-Learning) for learning to transfer
"""

import time
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import numpy as np


class TransferType(Enum):
    """Types of transfer"""
    NEAR = "near"  # Similar context
    FAR = "far"  # Distant context
    POSITIVE = "positive"  # Helps learning
    NEGATIVE = "negative"  # Interferes with learning
    LATERAL = "lateral"  # Same level complexity
    VERTICAL = "vertical"  # Different level (simple→complex)


@dataclass
class Knowledge:
    """Knowledge unit"""
    knowledge_id: str
    domain: str
    content: str
    abstraction_level: int  # 0=concrete, higher=abstract
    acquisition_time: float
    strength: float  # 0-1


@dataclass
class TransferAttempt:
    """Attempt to transfer knowledge"""
    timestamp: float
    source_knowledge_id: str
    source_domain: str
    target_domain: str
    transfer_distance: float  # 0-1 (0=identical, 1=very different)
    transfer_type: TransferType
    success_rate: float  # 0-1
    interference: float  # 0-1 (negative transfer)


@dataclass
class LearningContext:
    """Context for learning"""
    context_id: str
    domain: str
    features: Set[str]
    difficulty: float  # 0-1


class DomainSimilarityComputer:
    """Computes similarity between domains for transfer"""

    def __init__(self):
        # Domain feature vectors (simplified)
        self.domain_features = {
            "mathematics": {"abstract", "logical", "quantitative", "symbolic"},
            "physics": {"abstract", "quantitative", "physical", "mathematical"},
            "biology": {"concrete", "observational", "systematic", "living"},
            "music": {"auditory", "temporal", "pattern", "creative"},
            "language": {"symbolic", "communicative", "grammatical", "semantic"},
            "chess": {"strategic", "spatial", "adversarial", "pattern"},
            "driving": {"motor", "spatial", "perceptual", "procedural"},
        }

    def compute_distance(self, domain_1: str, domain_2: str) -> float:
        """
        Compute transfer distance between domains.

        Near transfer: low distance (similar domains)
        Far transfer: high distance (distant domains)

        Returns distance (0-1).
        """
        if domain_1 == domain_2:
            return 0.0

        features_1 = self.domain_features.get(domain_1, set())
        features_2 = self.domain_features.get(domain_2, set())

        if not features_1 or not features_2:
            return 0.8  # Unknown domains = far

        # Jaccard distance
        intersection = len(features_1.intersection(features_2))
        union = len(features_1.union(features_2))

        similarity = intersection / union if union > 0 else 0.0
        distance = 1.0 - similarity

        return distance


class TransferMechanism:
    """Implements transfer mechanisms"""

    def __init__(self):
        self.domain_similarity = DomainSimilarityComputer()

    def attempt_transfer(
        self,
        knowledge: Knowledge,
        target_domain: str,
        target_context: LearningContext
    ) -> TransferAttempt:
        """
        Attempt to transfer knowledge to new domain/context.

        Returns transfer attempt.
        """
        # Compute transfer distance
        distance = self.domain_similarity.compute_distance(
            knowledge.domain,
            target_domain
        )

        # Determine transfer type
        if distance < 0.3:
            transfer_type = TransferType.NEAR
        else:
            transfer_type = TransferType.FAR

        # Success rate depends on:
        # - Distance (closer = better)
        # - Abstraction level (higher = better far transfer)
        # - Knowledge strength

        base_success = 1.0 - distance

        # Abstract knowledge transfers better (especially for far transfer)
        if transfer_type == TransferType.FAR:
            abstraction_bonus = knowledge.abstraction_level * 0.1
        else:
            abstraction_bonus = 0.0

        # Knowledge strength
        strength_factor = knowledge.strength

        success_rate = base_success + abstraction_bonus
        success_rate *= strength_factor
        success_rate = np.clip(success_rate, 0.0, 1.0)

        # Interference (negative transfer)
        # Higher for far transfer with low abstraction
        if transfer_type == TransferType.FAR and knowledge.abstraction_level < 2:
            interference = 0.3
        else:
            interference = 0.1

        attempt = TransferAttempt(
            timestamp=time.time(),
            source_knowledge_id=knowledge.knowledge_id,
            source_domain=knowledge.domain,
            target_domain=target_domain,
            transfer_distance=distance,
            transfer_type=transfer_type,
            success_rate=success_rate,
            interference=interference
        )

        return attempt

    def extract_abstract_principle(
        self,
        concrete_knowledge: Knowledge
    ) -> Knowledge:
        """
        Extract abstract principle from concrete knowledge.

        Abstract principles transfer better.

        Returns abstract knowledge.
        """
        abstract = Knowledge(
            knowledge_id=f"abstract_{concrete_knowledge.knowledge_id}",
            domain="general",  # Domain-independent
            content=f"abstract_principle_of_{concrete_knowledge.content}",
            abstraction_level=concrete_knowledge.abstraction_level + 1,
            acquisition_time=time.time(),
            strength=concrete_knowledge.strength * 0.8  # Slightly weaker initially
        )

        return abstract


class CatastrophicForgettingPrevention:
    """Prevents catastrophic forgetting during transfer"""

    def __init__(self):
        self.knowledge_importance = {}  # knowledge_id -> importance

    def compute_importance(
        self,
        knowledge: Knowledge,
        usage_frequency: int
    ) -> float:
        """
        Compute importance of knowledge (for forgetting prevention).

        Important knowledge should be protected.

        Returns importance (0-1).
        """
        # Importance factors:
        # - Usage frequency
        # - Abstraction level (abstract = more important)
        # - Strength

        freq_score = min(1.0, usage_frequency / 10.0)
        abstraction_score = min(1.0, knowledge.abstraction_level / 5.0)
        strength_score = knowledge.strength

        importance = 0.4 * freq_score + 0.3 * abstraction_score + 0.3 * strength_score

        self.knowledge_importance[knowledge.knowledge_id] = importance

        return importance

    def should_protect(
        self,
        knowledge_id: str,
        protection_threshold: float = 0.6
    ) -> bool:
        """
        Determine if knowledge should be protected from forgetting.

        Returns True if should protect.
        """
        importance = self.knowledge_importance.get(knowledge_id, 0.5)
        return importance >= protection_threshold


class TransferLearningSystem:
    """
    Main LAB_034 implementation.

    Manages:
    - Knowledge transfer across domains
    - Near and far transfer
    - Abstract principle extraction
    - Catastrophic forgetting prevention
    """

    def __init__(self):
        # Components
        self.transfer_mechanism = TransferMechanism()
        self.forgetting_prevention = CatastrophicForgettingPrevention()

        # State
        self.knowledge_base: Dict[str, Knowledge] = {}
        self.transfer_history: List[TransferAttempt] = []
        self.usage_counts: Dict[str, int] = {}

    def acquire_knowledge(
        self,
        knowledge_id: str,
        domain: str,
        content: str,
        abstraction_level: int = 0
    ) -> Knowledge:
        """Acquire new knowledge"""
        knowledge = Knowledge(
            knowledge_id=knowledge_id,
            domain=domain,
            content=content,
            abstraction_level=abstraction_level,
            acquisition_time=time.time(),
            strength=1.0
        )

        self.knowledge_base[knowledge_id] = knowledge
        self.usage_counts[knowledge_id] = 0

        return knowledge

    def transfer_knowledge(
        self,
        knowledge_id: str,
        target_domain: str,
        target_context: LearningContext
    ) -> TransferAttempt:
        """
        Transfer knowledge to new domain/context.

        Returns transfer attempt.
        """
        knowledge = self.knowledge_base.get(knowledge_id)
        if not knowledge:
            return None

        # Attempt transfer
        attempt = self.transfer_mechanism.attempt_transfer(
            knowledge,
            target_domain,
            target_context
        )

        self.transfer_history.append(attempt)

        # Update usage
        self.usage_counts[knowledge_id] += 1

        return attempt

    def generalize_knowledge(
        self,
        knowledge_id: str
    ) -> Knowledge:
        """
        Generalize knowledge to abstract principle.

        Returns abstract knowledge.
        """
        concrete = self.knowledge_base.get(knowledge_id)
        if not concrete:
            return None

        abstract = self.transfer_mechanism.extract_abstract_principle(concrete)

        # Add to knowledge base
        self.knowledge_base[abstract.knowledge_id] = abstract
        self.usage_counts[abstract.knowledge_id] = 0

        return abstract

    def protect_important_knowledge(self):
        """
        Identify and protect important knowledge from forgetting.

        Returns protected knowledge IDs.
        """
        protected = []

        for k_id, knowledge in self.knowledge_base.items():
            usage = self.usage_counts.get(k_id, 0)

            # Compute importance
            importance = self.forgetting_prevention.compute_importance(knowledge, usage)

            # Check if should protect
            if self.forgetting_prevention.should_protect(k_id):
                protected.append(k_id)

        return protected

    def get_transfer_statistics(self) -> Dict:
        """Get transfer statistics"""
        if not self.transfer_history:
            return {
                "total_transfers": 0,
                "near_transfers": 0,
                "far_transfers": 0,
                "avg_success_rate": 0.0,
                "avg_interference": 0.0,
            }

        near = [t for t in self.transfer_history if t.transfer_type == TransferType.NEAR]
        far = [t for t in self.transfer_history if t.transfer_type == TransferType.FAR]

        return {
            "total_transfers": len(self.transfer_history),
            "near_transfers": len(near),
            "far_transfers": len(far),
            "avg_success_rate": np.mean([t.success_rate for t in self.transfer_history]),
            "avg_success_near": np.mean([t.success_rate for t in near]) if near else 0.0,
            "avg_success_far": np.mean([t.success_rate for t in far]) if far else 0.0,
            "avg_interference": np.mean([t.interference for t in self.transfer_history]),
        }


# Example usage and testing
if __name__ == "__main__":
    print("🧠 LAB_034: Transfer Learning - Test")
    print("=" * 60)

    system = TransferLearningSystem()

    # Scenario 1: Near transfer (mathematics → physics)
    print("\n📐 Scenario 1: Near Transfer (Mathematics → Physics)...")

    # Acquire mathematical knowledge
    math_knowledge = system.acquire_knowledge(
        "pythagorean_theorem",
        "mathematics",
        "a² + b² = c² for right triangles",
        abstraction_level=2
    )
    print(f"  Acquired: {math_knowledge.content}")
    print(f"  Domain: {math_knowledge.domain}")
    print(f"  Abstraction level: {math_knowledge.abstraction_level}")

    # Transfer to physics
    physics_context = LearningContext(
        context_id="vector_problems",
        domain="physics",
        features={"quantitative", "spatial", "mathematical"},
        difficulty=0.6
    )

    transfer = system.transfer_knowledge(
        "pythagorean_theorem",
        "physics",
        physics_context
    )

    print(f"\n  Transfer attempt:")
    print(f"    Target domain: {transfer.target_domain}")
    print(f"    Transfer distance: {transfer.transfer_distance:.3f}")
    print(f"    Transfer type: {transfer.transfer_type.value}")
    print(f"    Success rate: {transfer.success_rate:.3f}")
    print(f"    Interference: {transfer.interference:.3f}")

    # Scenario 2: Far transfer (chess → business strategy)
    print("\n♟️ Scenario 2: Far Transfer (Chess → Business)...")

    chess_knowledge = system.acquire_knowledge(
        "chess_strategy",
        "chess",
        "Control center, develop pieces early",
        abstraction_level=1  # Concrete strategy
    )

    business_context = LearningContext(
        context_id="business_planning",
        domain="business",
        features={"strategic", "adversarial", "planning"},
        difficulty=0.7
    )

    transfer2 = system.transfer_knowledge(
        "chess_strategy",
        "business",
        business_context
    )

    print(f"  Knowledge: {chess_knowledge.content}")
    print(f"  Transfer distance: {transfer2.transfer_distance:.3f} (far)")
    print(f"  Transfer type: {transfer2.transfer_type.value}")
    print(f"  Success rate: {transfer2.success_rate:.3f} (lower than near)")
    print(f"  Interference: {transfer2.interference:.3f} (higher)")

    # Scenario 3: Abstract principle extraction
    print("\n🔼 Scenario 3: Extracting Abstract Principle...")

    abstract_chess = system.generalize_knowledge("chess_strategy")

    print(f"  Original (concrete): {chess_knowledge.content}")
    print(f"    Abstraction level: {chess_knowledge.abstraction_level}")
    print(f"\n  Abstract principle: {abstract_chess.content}")
    print(f"    Abstraction level: {abstract_chess.abstraction_level}")
    print(f"    Domain: {abstract_chess.domain} (domain-independent)")

    # Try transferring abstract version
    transfer3 = system.transfer_knowledge(
        abstract_chess.knowledge_id,
        "business",
        business_context
    )

    print(f"\n  Transfer of abstract principle:")
    print(f"    Success rate: {transfer3.success_rate:.3f} (higher with abstraction!)")
    print(f"    Interference: {transfer3.interference:.3f}")

    # Scenario 4: Catastrophic forgetting prevention
    print("\n🛡️ Scenario 4: Protecting Important Knowledge...")

    # Use knowledge multiple times
    for _ in range(5):
        system.transfer_knowledge("pythagorean_theorem", "physics", physics_context)

    protected = system.protect_important_knowledge()

    print(f"  Protected knowledge ({len(protected)} items):")
    for k_id in protected:
        knowledge = system.knowledge_base[k_id]
        usage = system.usage_counts[k_id]
        importance = system.forgetting_prevention.knowledge_importance[k_id]
        print(f"    • {k_id}: usage={usage}, importance={importance:.3f}")

    # Final statistics
    print("\n📊 Transfer Statistics:")
    stats = system.get_transfer_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")
        else:
            print(f"  {key}: {value}")

    print("\n✅ LAB_034 Test Complete!")
