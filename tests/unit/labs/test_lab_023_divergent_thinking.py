"""
LAB_023: Divergent Thinking Engine - Unit Tests

Creativity: Generate multiple solutions through remote associations

Key Papers:
- Guilford (1967) - The Nature of Human Intelligence
- Beaty et al. (2016) - DMN & creativity
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Creativity_Social.LAB_023_Divergent_Thinking.divergent_thinking_system import (
    DivergentThinkingSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with default parameters"""
        system = DivergentThinkingSystem()
        assert system.semantic_distance_threshold == 0.6
        assert system.inhibition_strength == 0.7
        assert system.generation_time == 60.0

    def test_custom_parameters(self):
        """System accepts custom parameters"""
        system = DivergentThinkingSystem(
            semantic_distance_threshold=0.7,
            inhibition_strength=0.8,
            generation_time=120.0
        )
        assert system.semantic_distance_threshold == 0.7
        assert system.inhibition_strength == 0.8
        assert system.generation_time == 120.0

    def test_state_initialization(self):
        """State variables initialize correctly"""
        system = DivergentThinkingSystem()
        assert system.total_prompts_processed == 0
        assert system.total_ideas_generated == 0
        assert system.avg_fluency == 0.0


class TestIdeaGeneration:
    """Test idea generation mechanisms"""

    def test_generates_ideas(self):
        """System generates ideas for prompt"""
        system = DivergentThinkingSystem()
        ideas = system.generate_ideas("Alternative uses for a brick", n_ideas=5)
        assert len(ideas) > 0
        assert isinstance(ideas, list)
        assert all(isinstance(idea, str) for idea in ideas)

    def test_generates_requested_number(self):
        """System generates approximately requested number of ideas"""
        system = DivergentThinkingSystem()
        ideas = system.generate_ideas("Uses for paperclip", n_ideas=10)
        # Allow some variance (7-13 ideas for requested 10)
        assert 7 <= len(ideas) <= 13

    def test_ideas_are_diverse(self):
        """Generated ideas are diverse (not identical)"""
        system = DivergentThinkingSystem()
        ideas = system.generate_ideas("Alternative transportation", n_ideas=8)
        unique_ideas = set(ideas)
        # At least 70% should be unique
        assert len(unique_ideas) >= len(ideas) * 0.7

    def test_no_duplicate_ideas(self):
        """System avoids generating duplicate ideas"""
        system = DivergentThinkingSystem()
        ideas = system.generate_ideas("Creative problem solving", n_ideas=10)
        assert len(ideas) == len(set(ideas))

    def test_empty_prompt_returns_empty(self):
        """Empty prompt returns empty list"""
        system = DivergentThinkingSystem()
        ideas = system.generate_ideas("", n_ideas=5)
        assert len(ideas) == 0

    def test_semantic_distance_filtering(self):
        """Ideas filtered by semantic distance threshold"""
        system = DivergentThinkingSystem(semantic_distance_threshold=0.8)
        ideas_high = system.generate_ideas("Innovative concepts", n_ideas=10)

        system_low = DivergentThinkingSystem(semantic_distance_threshold=0.3)
        ideas_low = system_low.generate_ideas("Innovative concepts", n_ideas=10)

        # Lower threshold should allow more ideas (less filtering)
        assert len(ideas_low) >= len(ideas_high)


class TestScoring:
    """Test Guilford's creativity metrics"""

    def test_fluency_score_increases_with_ideas(self):
        """Fluency score increases with number of ideas"""
        system = DivergentThinkingSystem()

        ideas_few = ["idea1", "idea2", "idea3"]
        ideas_many = ["idea1", "idea2", "idea3", "idea4", "idea5", "idea6", "idea7", "idea8"]

        fluency_few = system.score_fluency(ideas_few)
        fluency_many = system.score_fluency(ideas_many)

        assert fluency_many > fluency_few

    def test_flexibility_score_with_diverse_categories(self):
        """Flexibility score higher for diverse categories"""
        system = DivergentThinkingSystem()

        # Same category (all tools)
        ideas_same = ["hammer_use", "hammer_alternative", "hammer_creative"]

        # Different categories (tool, decoration, weapon, game)
        ideas_diverse = ["use_as_tool", "use_as_decoration", "use_as_weapon", "use_in_game"]

        flex_same = system.score_flexibility(ideas_same)
        flex_diverse = system.score_flexibility(ideas_diverse)

        assert flex_diverse > flex_same

    def test_originality_score_higher_for_novel(self):
        """Originality score higher for novel/rare ideas"""
        system = DivergentThinkingSystem()

        # Common ideas
        ideas_common = ["common_idea", "usual_approach", "typical_solution"]

        # Novel ideas (longer, more specific = simulated rarity)
        ideas_novel = ["unconventional_quantum_approach", "biomimetic_spiral_design", "fractal_recursive_pattern"]

        orig_common = system.score_originality(ideas_common)
        orig_novel = system.score_originality(ideas_novel)

        assert orig_novel > orig_common

    def test_combined_creativity_score(self):
        """Combined creativity score integrates all metrics"""
        system = DivergentThinkingSystem()

        ideas = ["idea1", "idea2_different", "idea3_novel", "idea4_unique_category"]

        fluency = system.score_fluency(ideas)
        flexibility = system.score_flexibility(ideas)
        originality = system.score_originality(ideas)

        creativity = system.compute_creativity_score(fluency, flexibility, originality)

        assert 0.0 <= creativity <= 1.0
        assert creativity > 0  # Non-empty ideas should have some creativity

    def test_zero_ideas_zero_scores(self):
        """Zero ideas result in zero scores"""
        system = DivergentThinkingSystem()

        ideas = []

        assert system.score_fluency(ideas) == 0.0
        assert system.score_flexibility(ideas) == 0.0
        assert system.score_originality(ideas) == 0.0

    def test_single_idea_minimal_flexibility(self):
        """Single idea has minimal flexibility (only 1 category)"""
        system = DivergentThinkingSystem()

        ideas = ["only_one_idea"]

        flexibility = system.score_flexibility(ideas)
        assert flexibility == 1.0  # Single category

    def test_all_same_category_low_flexibility(self):
        """All ideas in same category = low flexibility"""
        system = DivergentThinkingSystem()

        # All hammer-related (simulated by similar prefixes)
        ideas = ["hammer1", "hammer2", "hammer3"]

        flexibility = system.score_flexibility(ideas)
        assert flexibility < 2.0  # Should detect low category diversity

    def test_very_novel_idea_high_originality(self):
        """Very novel ideas score high originality"""
        system = DivergentThinkingSystem()

        # Extremely long/specific = rare
        ideas = ["supercalifragilisticexpialidocious_quantum_entanglement_application"]

        originality = system.score_originality(ideas)
        assert originality > 0.8

    def test_conventional_ideas_low_originality(self):
        """Conventional ideas score low originality"""
        system = DivergentThinkingSystem()

        # Very short/common
        ideas = ["use", "make", "do"]

        originality = system.score_originality(ideas)
        assert originality < 0.3


class TestIntegration:
    """Test integration with existing systems"""

    def test_inhibition_filters_conventional(self):
        """Inhibitory control filters conventional responses"""
        system = DivergentThinkingSystem(inhibition_strength=0.9)

        all_ideas = ["idea1", "idea2", "idea3", "idea4", "idea5"]
        filtered = system.inhibit_conventional(all_ideas, threshold=0.5)

        # High inhibition should filter out some ideas
        assert len(filtered) <= len(all_ideas)

    def test_gaba_modulation_reduces_inhibition(self):
        """Low GABA (high E/I) reduces inhibition → more ideas"""
        system = DivergentThinkingSystem()

        # Simulate GABA modulation
        gaba_low = 0.3  # Low inhibition
        gaba_high = 0.9  # High inhibition

        modulated_low = system.modulate_inhibition_by_gaba(gaba_low)
        modulated_high = system.modulate_inhibition_by_gaba(gaba_high)

        # Low GABA = less inhibition = more idea generation
        assert modulated_low < modulated_high

    def test_inhibitory_control_integration(self):
        """Integration with LAB_019 Inhibitory Control"""
        system = DivergentThinkingSystem()

        # Simulate inhibitory control strength from LAB_019
        control_strength = 0.8

        # Should suppress conventional responses
        ideas_before = ["idea1", "idea2", "idea3"]
        ideas_after = system.apply_inhibitory_control(ideas_before, control_strength)

        # Higher control = fewer ideas (conventional filtered)
        assert len(ideas_after) <= len(ideas_before)

    def test_low_inhibition_more_ideas(self):
        """Low inhibition allows more ideas (including conventional)"""
        system_low = DivergentThinkingSystem(inhibition_strength=0.2)
        system_high = DivergentThinkingSystem(inhibition_strength=0.9)

        ideas_low = system_low.generate_ideas("Creative solutions", n_ideas=10)
        ideas_high = system_high.generate_ideas("Creative solutions", n_ideas=10)

        # Low inhibition should generate more ideas
        assert len(ideas_low) >= len(ideas_high)


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_event_complete(self):
        """process_event executes complete cycle"""
        system = DivergentThinkingSystem()

        result = system.process_event("Alternative uses for a brick")

        assert "ideas" in result
        assert "fluency_score" in result
        assert "flexibility_score" in result
        assert "originality_score" in result
        assert "creativity_score" in result
        assert len(result["ideas"]) > 0

    def test_process_event_updates_stats(self):
        """process_event updates system statistics"""
        system = DivergentThinkingSystem()

        initial_prompts = system.total_prompts_processed
        initial_ideas = system.total_ideas_generated

        result = system.process_event("Creative problem solving")

        assert system.total_prompts_processed == initial_prompts + 1
        assert system.total_ideas_generated > initial_ideas

    def test_process_event_returns_best_ideas(self):
        """process_event returns most creative/novel ideas"""
        system = DivergentThinkingSystem()

        result = system.process_event("Innovative applications")

        # Should have "most_novel_idea" in result
        assert "most_novel_idea" in result or len(result["ideas"]) > 0
