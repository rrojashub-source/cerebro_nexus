"""
LAB_041: Transfer Learning - Unit Tests

Pattern Recognition: Generalization, analogical transfer, abstract learning

Key Papers:
- Gick & Holyoak (1980) - Analogical problem solving
- Thorndike & Woodworth (1901) - The influence of improvement in one mental function upon the efficiency of other functions
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Pattern_Recognition.LAB_041_Transfer_Learning.transfer_learning_system import (
    TransferLearningSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with empty transfer registry"""
        system = TransferLearningSystem()
        assert system.similarity_threshold == 0.6
        assert len(system.source_domains) == 0
        assert len(system.transfer_history) == 0

    def test_custom_similarity_threshold(self):
        """System accepts custom similarity threshold"""
        system = TransferLearningSystem(similarity_threshold=0.7)
        assert system.similarity_threshold == 0.7

    def test_transfer_registry_empty(self):
        """Transfer registry starts empty"""
        system = TransferLearningSystem()
        state = system.get_state()
        assert state["total_source_domains"] == 0


class TestAbstractStructureExtraction:
    """Test abstract structure extraction from examples"""

    def test_extract_structure_from_examples(self):
        """Extract abstract structure from concrete examples"""
        system = TransferLearningSystem()

        # Learn structure from examples in domain A
        examples = [
            {"obj1": "fortress", "obj2": "moat", "relation": "protects"},
            {"obj1": "castle", "obj2": "wall", "relation": "protects"},
            {"obj1": "city", "obj2": "army", "relation": "protects"}
        ]

        result = system.learn_from_domain(
            domain_name="defense",
            examples=examples
        )

        assert result["domain_learned"] == True
        assert "abstract_structure" in result
        assert result["abstract_structure"]["pattern"] == "X protects Y"

    def test_identify_relational_patterns(self):
        """Identify relational patterns across examples"""
        system = TransferLearningSystem()

        examples = [
            {"obj1": "sun", "obj2": "planet", "relation": "attracts"},
            {"obj1": "magnet", "obj2": "iron", "relation": "attracts"},
            {"obj1": "gravity", "obj2": "mass", "relation": "attracts"}
        ]

        result = system.learn_from_domain(
            domain_name="attraction",
            examples=examples
        )

        # Should identify relational pattern (X attracts Y)
        assert result["abstract_structure"]["pattern"] == "X attracts Y"
        assert result["abstract_structure"]["num_examples"] == 3

    def test_ignore_surface_features(self):
        """Abstract structure ignores surface features"""
        system = TransferLearningSystem()

        # Different surface features (colors, sizes) but same structure
        examples = [
            {"obj1": "red_ball", "obj2": "blue_ball", "relation": "collides"},
            {"obj1": "large_car", "obj2": "small_car", "relation": "collides"},
            {"obj1": "heavy_box", "obj2": "light_box", "relation": "collides"}
        ]

        result = system.learn_from_domain(
            domain_name="collision",
            examples=examples
        )

        # Structure should be abstract (ignoring colors, sizes)
        assert "red" not in result["abstract_structure"]["pattern"].lower()
        assert "large" not in result["abstract_structure"]["pattern"].lower()
        assert "collides" in result["abstract_structure"]["pattern"].lower()

    def test_build_abstract_schema(self):
        """Build abstract schema from multiple examples"""
        system = TransferLearningSystem()

        examples = [
            {"obj1": "teacher", "obj2": "student", "relation": "instructs"},
            {"obj1": "mentor", "obj2": "apprentice", "relation": "instructs"},
            {"obj1": "coach", "obj2": "athlete", "relation": "instructs"}
        ]

        result = system.learn_from_domain(
            domain_name="instruction",
            examples=examples
        )

        # Schema should be abstract and generalizable
        assert result["schema_built"] == True
        assert result["abstract_structure"]["generality"] > 0.7

    def test_multiple_domains_learned(self):
        """System can learn multiple source domains"""
        system = TransferLearningSystem()

        # Domain A
        system.learn_from_domain(
            domain_name="domain_A",
            examples=[{"obj1": "x", "obj2": "y", "relation": "causes"}]
        )

        # Domain B
        system.learn_from_domain(
            domain_name="domain_B",
            examples=[{"obj1": "a", "obj2": "b", "relation": "enables"}]
        )

        state = system.get_state()
        assert state["total_source_domains"] == 2

    def test_structural_similarity_computation(self):
        """Compute structural similarity between domains"""
        system = TransferLearningSystem()

        # Domain A: "X causes Y"
        system.learn_from_domain(
            domain_name="domain_A",
            examples=[{"obj1": "rain", "obj2": "flood", "relation": "causes"}]
        )

        # Compute similarity to new domain
        similarity = system.compute_structural_similarity(
            source_domain="domain_A",
            target_structure={"pattern": "X causes Y"}
        )

        assert similarity > 0.9  # High similarity (same structure)

    def test_domain_complexity_estimation(self):
        """Estimate domain complexity from examples"""
        system = TransferLearningSystem()

        # Simple domain (1 relation)
        simple_result = system.learn_from_domain(
            domain_name="simple",
            examples=[{"obj1": "a", "obj2": "b", "relation": "connects"}]
        )

        # Complex domain (multiple relations)
        complex_result = system.learn_from_domain(
            domain_name="complex",
            examples=[
                {"obj1": "a", "obj2": "b", "relation": "causes"},
                {"obj1": "b", "obj2": "c", "relation": "enables"},
                {"obj1": "c", "obj2": "d", "relation": "transforms"}
            ]
        )

        assert complex_result["complexity"] > simple_result["complexity"]


class TestNearTransfer:
    """Test near transfer (high similarity domains)"""

    def test_high_similarity_domains_easy_transfer(self):
        """High similarity domains → easy transfer"""
        system = TransferLearningSystem()

        # Learn source domain
        system.learn_from_domain(
            domain_name="source",
            examples=[{"obj1": "teacher", "obj2": "student", "relation": "instructs"}]
        )

        # Transfer to similar target domain
        transfer = system.transfer_knowledge(
            source_domain="source",
            target_domain="target",
            target_structure={"pattern": "X instructs Y"}
        )

        assert transfer["transfer_success"] == True
        assert transfer["similarity"] > 0.7
        assert transfer["transfer_type"] == "near"

    def test_similar_features_similar_relations(self):
        """Similar features + similar relations → high transfer"""
        system = TransferLearningSystem()

        # Source: "guitar playing"
        system.learn_from_domain(
            domain_name="guitar",
            examples=[{"obj1": "fingers", "obj2": "strings", "relation": "press"}]
        )

        # Target: "piano playing" (similar structure)
        transfer = system.transfer_knowledge(
            source_domain="guitar",
            target_domain="piano",
            target_structure={"pattern": "X press Y"}
        )

        assert transfer["transfer_success"] == True
        assert transfer["transfer_amount"] > 0.6

    def test_transfer_success_probability_high(self):
        """Near transfer → high success probability"""
        system = TransferLearningSystem()

        system.learn_from_domain(
            domain_name="source",
            examples=[{"obj1": "a", "obj2": "b", "relation": "causes"}]
        )

        transfer = system.transfer_knowledge(
            source_domain="source",
            target_domain="target",
            target_structure={"pattern": "X causes Y"}
        )

        assert transfer["success_probability"] > 0.8

    def test_quick_adaptation_to_target(self):
        """Near transfer allows quick adaptation"""
        system = TransferLearningSystem()

        system.learn_from_domain(
            domain_name="source",
            examples=[{"obj1": "a", "obj2": "b", "relation": "connects"}]
        )

        transfer = system.transfer_knowledge(
            source_domain="source",
            target_domain="target",
            target_structure={"pattern": "X connects Y"}
        )

        # Should adapt quickly (few examples needed)
        assert transfer["adaptation_cost"] < 0.3

    def test_transfer_preserves_structure(self):
        """Near transfer preserves abstract structure"""
        system = TransferLearningSystem()

        system.learn_from_domain(
            domain_name="source",
            examples=[{"obj1": "a", "obj2": "b", "relation": "transforms"}]
        )

        transfer = system.transfer_knowledge(
            source_domain="source",
            target_domain="target",
            target_structure={"pattern": "X transforms Y"}
        )

        assert transfer["structure_preserved"] == True

    def test_near_transfer_accumulates(self):
        """Multiple near transfers improve performance"""
        system = TransferLearningSystem()

        # Learn source
        system.learn_from_domain(
            domain_name="source",
            examples=[{"obj1": "a", "obj2": "b", "relation": "causes"}]
        )

        # First transfer
        transfer1 = system.transfer_knowledge(
            source_domain="source",
            target_domain="target1",
            target_structure={"pattern": "X causes Y"}
        )

        # Second transfer (should be easier)
        transfer2 = system.transfer_knowledge(
            source_domain="source",
            target_domain="target2",
            target_structure={"pattern": "X causes Y"}
        )

        # Second transfer should have lower adaptation cost
        assert transfer2["adaptation_cost"] <= transfer1["adaptation_cost"]

    def test_near_transfer_generalization(self):
        """Near transfer generalizes within domain"""
        system = TransferLearningSystem()

        system.learn_from_domain(
            domain_name="source",
            examples=[
                {"obj1": "a", "obj2": "b", "relation": "enables"},
                {"obj1": "c", "obj2": "d", "relation": "enables"}
            ]
        )

        transfer = system.transfer_knowledge(
            source_domain="source",
            target_domain="target",
            target_structure={"pattern": "X enables Y"}
        )

        assert transfer["generalization_score"] > 0.7


class TestFarTransfer:
    """Test far transfer (low similarity domains)"""

    def test_low_similarity_domains_hard_transfer(self):
        """Low similarity domains → hard transfer"""
        system = TransferLearningSystem()

        # Source: physical domain
        system.learn_from_domain(
            domain_name="physics",
            examples=[{"obj1": "force", "obj2": "motion", "relation": "causes"}]
        )

        # Target: social domain (different features, similar relation)
        transfer = system.transfer_knowledge(
            source_domain="physics",
            target_domain="social",
            target_structure={"pattern": "X influences Y"},
            similarity_override=0.3
        )

        assert transfer["transfer_type"] == "far"
        assert transfer["success_probability"] < 0.5

    def test_different_features_similar_relations(self):
        """Different features but similar relations → possible transfer"""
        system = TransferLearningSystem()

        # Source: "water flow"
        system.learn_from_domain(
            domain_name="water",
            examples=[{"obj1": "pressure", "obj2": "flow", "relation": "drives"}]
        )

        # Target: "electricity" (different objects, similar relation)
        transfer = system.transfer_knowledge(
            source_domain="water",
            target_domain="electricity",
            target_structure={"pattern": "X drives Y"},
            similarity_override=0.25
        )

        # Transfer possible but requires explicit analogy
        assert transfer["transfer_success"] == True
        assert transfer["requires_explicit_analogy"] == True

    def test_transfer_success_probability_low(self):
        """Far transfer → low success probability"""
        system = TransferLearningSystem()

        system.learn_from_domain(
            domain_name="source",
            examples=[{"obj1": "a", "obj2": "b", "relation": "causes"}]
        )

        transfer = system.transfer_knowledge(
            source_domain="source",
            target_domain="target",
            target_structure={"pattern": "X influences Y"},
            similarity_override=0.2
        )

        assert transfer["success_probability"] < 0.4

    def test_requires_explicit_analogy(self):
        """Far transfer requires explicit analogy (LAB_024 integration)"""
        system = TransferLearningSystem()

        system.learn_from_domain(
            domain_name="source",
            examples=[{"obj1": "a", "obj2": "b", "relation": "causes"}]
        )

        transfer = system.transfer_knowledge(
            source_domain="source",
            target_domain="target",
            target_structure={"pattern": "X affects Y"},
            similarity_override=0.25
        )

        # Far transfer needs LAB_024 (Conceptual Blending) for analogy
        assert transfer["requires_explicit_analogy"] == True
        assert transfer["lab_024_required"] == True

    def test_far_transfer_adaptation_cost_high(self):
        """Far transfer has high adaptation cost"""
        system = TransferLearningSystem()

        system.learn_from_domain(
            domain_name="source",
            examples=[{"obj1": "a", "obj2": "b", "relation": "enables"}]
        )

        transfer = system.transfer_knowledge(
            source_domain="source",
            target_domain="target",
            target_structure={"pattern": "X facilitates Y"},
            similarity_override=0.2
        )

        # High adaptation cost (many examples needed)
        assert transfer["adaptation_cost"] > 0.7

    def test_far_transfer_requires_meta_learning(self):
        """Far transfer benefits from meta-learning (LAB_038)"""
        system = TransferLearningSystem()

        system.learn_from_domain(
            domain_name="source",
            examples=[{"obj1": "a", "obj2": "b", "relation": "causes"}]
        )

        # Without meta-learning
        transfer_without = system.transfer_knowledge(
            source_domain="source",
            target_domain="target1",
            target_structure={"pattern": "X affects Y"},
            similarity_override=0.2,
            meta_learning_signal=None
        )

        # With meta-learning signal (from LAB_038)
        transfer_with = system.transfer_knowledge(
            source_domain="source",
            target_domain="target2",
            target_structure={"pattern": "X affects Y"},
            similarity_override=0.2,
            meta_learning_signal=0.9
        )

        # Meta-learning improves far transfer
        assert transfer_with["success_probability"] > transfer_without["success_probability"]

    def test_far_transfer_structural_mapping(self):
        """Far transfer requires structural mapping"""
        system = TransferLearningSystem()

        system.learn_from_domain(
            domain_name="source",
            examples=[{"obj1": "a", "obj2": "b", "relation": "transforms"}]
        )

        transfer = system.transfer_knowledge(
            source_domain="source",
            target_domain="target",
            target_structure={"pattern": "X converts Y"},
            similarity_override=0.25
        )

        assert transfer["structural_mapping_required"] == True


class TestNegativeTransfer:
    """Test negative transfer (interference from source)"""

    def test_interference_from_source_domain(self):
        """Source domain interferes with target learning"""
        system = TransferLearningSystem()

        # Source with misleading pattern
        system.learn_from_domain(
            domain_name="source",
            examples=[{"obj1": "a", "obj2": "b", "relation": "blocks"}]
        )

        # Target with opposite pattern
        transfer = system.transfer_knowledge(
            source_domain="source",
            target_domain="target",
            target_structure={"pattern": "X enables Y"},
            similarity_override=0.5,
            detect_interference=True
        )

        # Negative transfer detected
        assert transfer["negative_transfer"] == True

    def test_misleading_similarities(self):
        """Misleading surface similarities cause negative transfer"""
        system = TransferLearningSystem()

        # Source: "baseball" (hit ball with bat)
        system.learn_from_domain(
            domain_name="baseball",
            examples=[{"obj1": "bat", "obj2": "ball", "relation": "hits"}]
        )

        # Target: "golf" (different technique despite similar objects)
        transfer = system.transfer_knowledge(
            source_domain="baseball",
            target_domain="golf",
            target_structure={"pattern": "X swings Y"},
            similarity_override=0.6,
            detect_interference=True
        )

        # Misleading similarity (both have bat/club, ball)
        assert transfer["negative_transfer"] == True

    def test_performance_worse_than_baseline(self):
        """Negative transfer → performance worse than no transfer"""
        system = TransferLearningSystem()

        system.learn_from_domain(
            domain_name="source",
            examples=[{"obj1": "a", "obj2": "b", "relation": "opposes"}]
        )

        transfer = system.transfer_knowledge(
            source_domain="source",
            target_domain="target",
            target_structure={"pattern": "X supports Y"},
            similarity_override=0.5,
            detect_interference=True
        )

        # Performance penalty
        assert transfer["performance_delta"] < 0  # Worse than baseline

    def test_unlearning_required(self):
        """Negative transfer requires unlearning"""
        system = TransferLearningSystem()

        system.learn_from_domain(
            domain_name="source",
            examples=[{"obj1": "a", "obj2": "b", "relation": "destroys"}]
        )

        transfer = system.transfer_knowledge(
            source_domain="source",
            target_domain="target",
            target_structure={"pattern": "X builds Y"},
            similarity_override=0.5,
            detect_interference=True
        )

        # Unlearning needed to recover
        assert transfer["unlearning_required"] == True
        assert transfer["unlearning_cost"] > 0.5


class TestIntegration:
    """Test integration with other LABs"""

    def test_conceptual_blending_for_analogies(self):
        """LAB_024: Conceptual blending generates analogies"""
        system = TransferLearningSystem()

        system.learn_from_domain(
            domain_name="source",
            examples=[{"obj1": "fortress", "obj2": "moat", "relation": "protects"}]
        )

        transfer = system.transfer_knowledge(
            source_domain="source",
            target_domain="target",
            target_structure={"pattern": "X defends Y"},
            similarity_override=0.4,
            use_conceptual_blending=True  # LAB_024
        )

        # LAB_024 should help with far transfer via analogy
        assert transfer["conceptual_blend_used"] == True
        assert transfer["analogy_generated"] == True

    def test_meta_learning_optimizes_transfer(self):
        """LAB_038: Meta-learning optimizes transfer strategies"""
        system = TransferLearningSystem()

        system.learn_from_domain(
            domain_name="source",
            examples=[{"obj1": "a", "obj2": "b", "relation": "causes"}]
        )

        # With meta-learning signal
        transfer = system.transfer_knowledge(
            source_domain="source",
            target_domain="target",
            target_structure={"pattern": "X affects Y"},
            similarity_override=0.3,
            meta_learning_signal=0.9  # From LAB_038
        )

        # Meta-learning should improve transfer
        assert transfer["meta_learning_applied"] == True
        assert transfer["success_probability"] > 0.5  # Boosted

    def test_skill_transfer_between_domains(self):
        """LAB_040: Skill acquisition enables domain transfer"""
        system = TransferLearningSystem()

        system.learn_from_domain(
            domain_name="source",
            examples=[{"obj1": "guitar", "obj2": "strings", "relation": "play"}]
        )

        # Transfer with skill level from LAB_040
        transfer = system.transfer_knowledge(
            source_domain="source",
            target_domain="target",
            target_structure={"pattern": "X play Y"},
            similarity_override=0.7,
            source_skill_level=0.9  # From LAB_040
        )

        # High skill level facilitates transfer
        assert transfer["skill_facilitated"] == True
        assert transfer["transfer_amount"] > 0.7

    def test_semantic_similarity_detection(self):
        """LAB_005: Semantic clustering detects domain similarity"""
        system = TransferLearningSystem()

        system.learn_from_domain(
            domain_name="source",
            examples=[{"obj1": "a", "obj2": "b", "relation": "causes"}]
        )

        # Compute similarity using LAB_005
        transfer = system.transfer_knowledge(
            source_domain="source",
            target_domain="target",
            target_structure={"pattern": "X causes Y"},
            use_semantic_clustering=True  # LAB_005
        )

        # LAB_005 should detect semantic similarity
        assert transfer["semantic_similarity_computed"] == True


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_learn_event(self):
        """Process learning event"""
        system = TransferLearningSystem()

        result = system.process_event(
            event_type="learn",
            domain_name="test_domain",
            examples=[{"obj1": "a", "obj2": "b", "relation": "causes"}]
        )

        assert "domain_learned" in result
        assert result["domain_learned"] == True

    def test_process_transfer_event(self):
        """Process transfer event"""
        system = TransferLearningSystem()

        # Learn first
        system.learn_from_domain(
            domain_name="source",
            examples=[{"obj1": "a", "obj2": "b", "relation": "causes"}]
        )

        # Transfer
        result = system.process_event(
            event_type="transfer",
            source_domain="source",
            target_domain="target",
            target_structure={"pattern": "X causes Y"}
        )

        assert "transfer_success" in result


class TestGetState:
    """Test state retrieval"""

    def test_get_state_returns_domains(self):
        """get_state returns all source domains"""
        system = TransferLearningSystem()

        # Learn some domains
        system.learn_from_domain(
            domain_name="domain_A",
            examples=[{"obj1": "a", "obj2": "b", "relation": "causes"}]
        )
        system.learn_from_domain(
            domain_name="domain_B",
            examples=[{"obj1": "c", "obj2": "d", "relation": "enables"}]
        )

        state = system.get_state()

        assert "total_source_domains" in state
        assert state["total_source_domains"] == 2
        assert "transfer_history_size" in state

    def test_get_state_serializable(self):
        """get_state returns JSON-serializable dict"""
        system = TransferLearningSystem()

        state = system.get_state()

        import json
        json_str = json.dumps(state)
        assert json_str is not None
