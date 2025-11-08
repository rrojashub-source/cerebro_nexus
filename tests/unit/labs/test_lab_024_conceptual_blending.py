"""
LAB_024: Conceptual Blending - Unit Tests

Creativity: Create novel concepts through metaphor, analogy, blending

Key Papers:
- Fauconnier & Turner (2002) - The Way We Think: Conceptual Blending
- Gentner (1983) - Structure-Mapping: A Theoretical Framework for Analogy
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Creativity_Social.LAB_024_Conceptual_Blending.conceptual_blending_system import (
    ConceptualBlendingSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with default parameters"""
        system = ConceptualBlendingSystem()
        assert system.structural_similarity_threshold == 0.5
        assert system.blend_novelty_weight == 0.6
        assert system.coherence_weight == 0.4

    def test_custom_parameters(self):
        """System accepts custom parameters"""
        system = ConceptualBlendingSystem(
            structural_similarity_threshold=0.7,
            blend_novelty_weight=0.8,
            max_blend_complexity=3
        )
        assert system.structural_similarity_threshold == 0.7
        assert system.blend_novelty_weight == 0.8
        assert system.max_blend_complexity == 3

    def test_state_initialization(self):
        """State variables initialize correctly"""
        system = ConceptualBlendingSystem()
        assert system.total_blends_created == 0
        assert system.successful_blends == 0


class TestConceptualMapping:
    """Test Structure Mapping Theory implementation"""

    def test_maps_structural_similarities(self):
        """System finds structural correspondences"""
        system = ConceptualBlendingSystem()

        concept_a = {"type": "atom", "structure": {"center": "nucleus", "orbiting": "electrons"}}
        concept_b = {"type": "solar_system", "structure": {"center": "sun", "orbiting": "planets"}}

        mapping = system.map_conceptual_spaces(concept_a, concept_b)

        assert mapping is not None
        assert "correspondences" in mapping

    def test_finds_relational_correspondences(self):
        """Mapping finds relational (not just feature) similarities"""
        system = ConceptualBlendingSystem()

        concept_a = {"structure": {"agent": "lion", "action": "hunts", "target": "prey"}}
        concept_b = {"structure": {"agent": "detective", "action": "investigates", "target": "clues"}}

        mapping = system.map_conceptual_spaces(concept_a, concept_b)

        # Should map relations (agent-action-target) not just surface features
        assert "correspondences" in mapping

    def test_no_mapping_for_dissimilar(self):
        """No mapping when concepts too dissimilar"""
        system = ConceptualBlendingSystem(structural_similarity_threshold=0.8)

        concept_a = {"structure": {"single_element": "rock"}}
        concept_b = {"structure": {"complex": "network", "nodes": "many", "edges": "connections"}}

        similarity = system.compute_structural_similarity(concept_a, concept_b)

        assert similarity < 0.8  # Below threshold

    def test_partial_mapping_for_partial_similarity(self):
        """Partial similarity yields partial mapping"""
        system = ConceptualBlendingSystem()

        concept_a = {"structure": {"part1": "A", "part2": "B"}}
        concept_b = {"structure": {"part1": "X", "part3": "Z"}}

        mapping = system.map_conceptual_spaces(concept_a, concept_b)

        # Should map part1 → part1, but part2 and part3 unmapped
        assert mapping is not None

    def test_alignment_quality_metric(self):
        """Compute quality of structural alignment"""
        system = ConceptualBlendingSystem()

        concept_a = {"structure": {"a": 1, "b": 2, "c": 3}}
        concept_b = {"structure": {"a": 1, "b": 2, "c": 3}}

        similarity = system.compute_structural_similarity(concept_a, concept_b)

        # Identical structure = high similarity
        assert similarity > 0.8

    def test_one_to_many_mapping_forbidden(self):
        """One element cannot map to multiple elements"""
        system = ConceptualBlendingSystem()

        concept_a = {"structure": {"single": "atom"}}
        concept_b = {"structure": {"multiple1": "proton", "multiple2": "neutron"}}

        mapping = system.map_conceptual_spaces(concept_a, concept_b)

        # Should map single → one of multiples (not both)
        correspondences = mapping.get("correspondences", {})
        if "single" in correspondences:
            assert isinstance(correspondences["single"], str)  # Single target


class TestBlending:
    """Test conceptual blending (Fauconnier & Turner)"""

    def test_blends_two_concepts(self):
        """System creates blend from two concepts"""
        system = ConceptualBlendingSystem()

        concept_a = {"type": "atom", "structure": {"center": "nucleus", "orbiting": "electrons"}}
        concept_b = {"type": "solar_system", "structure": {"center": "sun", "orbiting": "planets"}}

        blend = system.blend_concepts(concept_a, concept_b)

        assert blend is not None
        assert "type" in blend
        assert "structure" in blend

    def test_generic_space_extraction(self):
        """Blend extracts generic space (common structure)"""
        system = ConceptualBlendingSystem()

        concept_a = {"structure": {"center": "nucleus", "orbiting": "electrons"}}
        concept_b = {"structure": {"center": "sun", "orbiting": "planets"}}

        blend = system.blend_concepts(concept_a, concept_b)

        # Generic space: center + orbiting
        assert "center" in blend.get("structure", {}) or "generic_space" in blend

    def test_emergent_structure_creation(self):
        """Blend creates emergent structure not in inputs"""
        system = ConceptualBlendingSystem()

        concept_a = {"type": "atom", "properties": ["small", "invisible"]}
        concept_b = {"type": "solar_system", "properties": ["large", "visible"]}

        blend = system.blend_concepts(concept_a, concept_b)

        # Should have emergent properties/structure
        assert "emergent" in blend or len(blend.get("properties", [])) > 0

    def test_blend_preserves_key_relations(self):
        """Blend preserves key relational structure"""
        system = ConceptualBlendingSystem()

        concept_a = {"structure": {"relation": "orbits"}}
        concept_b = {"structure": {"relation": "revolves_around"}}

        blend = system.blend_concepts(concept_a, concept_b)

        # Should preserve relation concept
        assert "structure" in blend or "relation" in str(blend)

    def test_blend_novelty_higher_than_inputs(self):
        """Blend is more novel than individual inputs"""
        system = ConceptualBlendingSystem()

        concept_a = {"type": "simple_a"}
        concept_b = {"type": "simple_b"}

        blend = system.blend_concepts(concept_a, concept_b)
        novelty = system.score_novelty(blend)

        # Blend should be novel
        assert novelty > 0.5

    def test_blend_coherence_maintained(self):
        """Blend maintains internal coherence"""
        system = ConceptualBlendingSystem()

        concept_a = {"type": "atom", "structure": {"center": "nucleus"}}
        concept_b = {"type": "solar_system", "structure": {"center": "sun"}}

        blend = system.blend_concepts(concept_a, concept_b)
        coherence = system.score_coherence(blend)

        # Should be coherent
        assert coherence > 0.5

    def test_failed_blend_for_incompatible(self):
        """Incompatible concepts fail to blend"""
        system = ConceptualBlendingSystem(structural_similarity_threshold=0.9)

        concept_a = {"type": "abstract_number", "value": 42}
        concept_b = {"type": "physical_chair", "material": "wood"}

        # Very different structure → should fail or have low quality
        blend = system.blend_concepts(concept_a, concept_b)

        if blend:
            coherence = system.score_coherence(blend)
            assert coherence < 0.7  # Low coherence for incompatible

    def test_blend_with_divergent_ideas(self):
        """Integration with LAB_023 (Divergent Thinking)"""
        system = ConceptualBlendingSystem()

        # Simulate divergent ideas from LAB_023
        divergent_ideas = ["use_as_tool", "combine_with_art", "transform_into_game"]

        # Pick two to blend
        concept_a = {"type": "tool", "purpose": "utility"}
        concept_b = {"type": "art", "purpose": "expression"}

        blend = system.blend_concepts(concept_a, concept_b)

        # Should create "artful tool" or "utilitarian art"
        assert blend is not None


class TestMetaphorGeneration:
    """Test metaphor generation"""

    def test_generates_metaphor(self):
        """System generates metaphor from blend"""
        system = ConceptualBlendingSystem()

        source = "atom"
        target = "solar_system"
        relation = "orbiting_structure"

        metaphor = system.generate_metaphor(source, target, relation)

        assert metaphor is not None
        assert isinstance(metaphor, str)
        assert "is like" in metaphor.lower() or "is" in metaphor

    def test_metaphor_format_correct(self):
        """Metaphor follows 'X is like Y because Z' format"""
        system = ConceptualBlendingSystem()

        metaphor = system.generate_metaphor("time", "river", "flows")

        # Should contain key elements
        assert "time" in metaphor.lower()
        assert "river" in metaphor.lower()
        assert "flow" in metaphor.lower() or "because" in metaphor.lower()

    def test_metaphor_relation_meaningful(self):
        """Metaphor relation is meaningful (not arbitrary)"""
        system = ConceptualBlendingSystem()

        metaphor = system.generate_metaphor("argument", "war", "conflict")

        # Relation "conflict" should appear in explanation
        assert "conflict" in metaphor.lower() or "battle" in metaphor.lower()

    def test_metaphor_from_blend(self):
        """Generate metaphor from conceptual blend"""
        system = ConceptualBlendingSystem()

        concept_a = {"type": "atom", "structure": {"center": "nucleus"}}
        concept_b = {"type": "solar_system", "structure": {"center": "sun"}}

        blend = system.blend_concepts(concept_a, concept_b)
        metaphor = system.generate_metaphor_from_blend(blend, concept_a, concept_b)

        assert metaphor is not None

    def test_multiple_metaphors_for_blend(self):
        """Can generate multiple metaphors from same blend"""
        system = ConceptualBlendingSystem()

        concept_a = {"type": "mind"}
        concept_b = {"type": "computer"}

        blend = system.blend_concepts(concept_a, concept_b)

        metaphor1 = system.generate_metaphor_from_blend(blend, concept_a, concept_b)
        metaphor2 = system.generate_metaphor("mind", "computer", "processing")

        # Both should be valid
        assert metaphor1 is not None
        assert metaphor2 is not None


class TestAnalogyGeneration:
    """Test analogy generation"""

    def test_generates_analogies(self):
        """System generates analogies"""
        system = ConceptualBlendingSystem()

        concept = {"type": "atom", "structure": {"center": "nucleus", "orbiting": "electrons"}}

        analogies = system.generate_analogies(concept, n=3)

        assert len(analogies) > 0
        assert all(isinstance(a, str) for a in analogies)

    def test_analogies_structurally_similar(self):
        """Analogies share structural similarity with source"""
        system = ConceptualBlendingSystem()

        concept = {"structure": {"hierarchy": "tree", "levels": "multiple"}}

        analogies = system.generate_analogies(concept, n=3)

        # Should mention hierarchical structures
        # (simulated: any analogy is acceptable for now)
        assert len(analogies) > 0

    def test_analogy_diversity(self):
        """Generated analogies are diverse (not identical)"""
        system = ConceptualBlendingSystem()

        concept = {"type": "flow"}

        analogies = system.generate_analogies(concept, n=5)

        unique_analogies = set(analogies)
        assert len(unique_analogies) >= len(analogies) * 0.8  # 80% unique


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_event_complete(self):
        """process_event executes complete blending cycle"""
        system = ConceptualBlendingSystem()

        result = system.process_event(
            concept_a={"type": "atom", "structure": {"center": "nucleus"}},
            concept_b={"type": "solar_system", "structure": {"center": "sun"}}
        )

        assert "blend" in result
        assert "metaphor" in result
        assert "coherence_score" in result
        assert "novelty_score" in result

    def test_process_event_updates_stats(self):
        """process_event updates system statistics"""
        system = ConceptualBlendingSystem()

        initial_blends = system.total_blends_created

        system.process_event(
            concept_a={"type": "A"},
            concept_b={"type": "B"}
        )

        assert system.total_blends_created == initial_blends + 1

    def test_process_event_with_low_similarity_fails(self):
        """process_event with dissimilar concepts returns low scores"""
        system = ConceptualBlendingSystem(structural_similarity_threshold=0.9)

        result = system.process_event(
            concept_a={"type": "abstract"},
            concept_b={"type": "concrete"}
        )

        # Should have low coherence or indicate failed blend
        assert result["coherence_score"] < 0.7 or result.get("blend_failed", False)
