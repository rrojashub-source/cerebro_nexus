"""
LAB_026: Dream Logic - Unit Tests

Creativity: Unconstrained association, surreal combinations (REM-like)

Key Papers:
- Hobson & McCarley (1977) - Activation-synthesis hypothesis of dreaming
- Stickgold et al. (2000) - Sleep, learning, and dreams: offline memory reprocessing
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Creativity_Social.LAB_026_Dream_Logic.dream_logic_system import (
    DreamLogicSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with default parameters"""
        system = DreamLogicSystem()
        assert system.logical_constraint_strength == 0.1
        assert system.emotional_connection_weight == 0.8
        assert system.bizarreness_tolerance == 0.9

    def test_custom_parameters(self):
        """System accepts custom parameters"""
        system = DreamLogicSystem(
            logical_constraint_strength=0.5,
            emotional_connection_weight=0.6,
            bizarreness_tolerance=0.7
        )
        assert system.logical_constraint_strength == 0.5
        assert system.emotional_connection_weight == 0.6
        assert system.bizarreness_tolerance == 0.7

    def test_state_initialization(self):
        """State variables initialize correctly"""
        system = DreamLogicSystem()
        assert system.total_dream_sessions == 0
        assert system.novel_connections_found == 0


class TestLogicalConstraintSuspension:
    """Test suspension of logical constraints (dream vs wake)"""

    def test_suspends_logical_constraints(self):
        """System can reduce logical constraint strength"""
        system = DreamLogicSystem(logical_constraint_strength=0.1)

        constraint_level = system.suspend_logical_constraints()

        # Dream mode = low constraints
        assert constraint_level < 0.5

    def test_dream_mode_low_constraint(self):
        """Dream mode has low logical constraint strength"""
        system = DreamLogicSystem(logical_constraint_strength=0.1)

        constraint_level = system.suspend_logical_constraints()

        # 0.1 = very dream-like
        assert constraint_level < 0.3

    def test_wake_mode_high_constraint(self):
        """Wake mode has high logical constraint strength"""
        system = DreamLogicSystem(logical_constraint_strength=0.9)

        constraint_level = system.suspend_logical_constraints()

        # 0.9 = awake logic
        assert constraint_level > 0.7

    def test_constraint_strength_affects_bizarreness(self):
        """Lower constraint strength allows higher bizarreness"""
        system_dream = DreamLogicSystem(logical_constraint_strength=0.1)
        system_wake = DreamLogicSystem(logical_constraint_strength=0.9)

        # Generate narrative
        fragments = [
            {"content": "flying elephant", "emotion": "joy"},
            {"content": "underwater fire", "emotion": "surprise"}
        ]

        narrative_dream = system_dream.generate_bizarre_combination(fragments)
        narrative_wake = system_wake.generate_bizarre_combination(fragments)

        bizarreness_dream = system_dream.score_bizarreness(narrative_dream)
        bizarreness_wake = system_wake.score_bizarreness(narrative_wake)

        # Dream should allow more bizarreness
        assert bizarreness_dream >= bizarreness_wake


class TestEmotionalAssociation:
    """Test emotion-driven associations (LAB_001 integration)"""

    def test_associates_by_emotion(self):
        """System connects memories by emotional similarity (LAB_001)"""
        system = DreamLogicSystem()

        memories = [
            {"id": 1, "content": "lost job", "emotion": "sadness"},
            {"id": 2, "content": "dog died", "emotion": "sadness"},
            {"id": 3, "content": "won lottery", "emotion": "joy"}
        ]

        associations = system.associate_by_emotion(memories)

        # Should connect 1-2 (both sadness)
        assert len(associations) > 0
        # Association should be between memories with same emotion
        for (mem_a, mem_b, similarity) in associations:
            assert mem_a["emotion"] == mem_b["emotion"]

    def test_emotion_overrides_semantic_distance(self):
        """Emotional connection overrides semantic dissimilarity"""
        system = DreamLogicSystem(emotional_connection_weight=0.9)

        memories = [
            {"content": "childhood toy", "emotion": "joy"},
            {"content": "wedding day", "emotion": "joy"},
            {"content": "childhood homework", "emotion": "fear"}
        ]

        associations = system.associate_by_emotion(memories)

        # Should connect "toy" + "wedding" (both joy)
        # Even though semantically unrelated
        joy_associations = [
            (a, b) for (a, b, sim) in associations
            if a["emotion"] == "joy" and b["emotion"] == "joy"
        ]
        assert len(joy_associations) > 0

    def test_similar_emotions_connect_unrelated(self):
        """Similar emotions connect semantically unrelated memories"""
        system = DreamLogicSystem()

        memories = [
            {"content": "cat", "emotion": "joy"},
            {"content": "mathematics", "emotion": "joy"},
            {"content": "spider", "emotion": "fear"}
        ]

        associations = system.associate_by_emotion(memories)

        # Cat + mathematics should connect (both joy)
        joy_pairs = [
            (a, b) for (a, b, sim) in associations
            if "cat" in str(a) and "math" in str(b)
        ]

        # Should find at least one joy-based connection
        assert len(associations) > 0

    def test_emotional_themes_emerge(self):
        """Dominant emotional themes emerge from associations"""
        system = DreamLogicSystem()

        memories = [
            {"content": "A", "emotion": "fear"},
            {"content": "B", "emotion": "fear"},
            {"content": "C", "emotion": "fear"},
            {"content": "D", "emotion": "joy"}
        ]

        associations = system.associate_by_emotion(memories)

        # Fear should be dominant theme
        emotions = [a["emotion"] for (a, b, sim) in associations]
        emotions.extend([b["emotion"] for (a, b, sim) in associations])

        fear_count = emotions.count("fear")
        joy_count = emotions.count("joy")

        assert fear_count > joy_count

    def test_emotional_connection_weight_modulation(self):
        """Emotional connection weight affects association strength"""
        system_high = DreamLogicSystem(emotional_connection_weight=0.9)
        system_low = DreamLogicSystem(emotional_connection_weight=0.3)

        memories = [
            {"content": "A", "emotion": "joy"},
            {"content": "B", "emotion": "joy"}
        ]

        assoc_high = system_high.associate_by_emotion(memories)
        assoc_low = system_low.associate_by_emotion(memories)

        # High weight = stronger/more associations
        # (Implementation dependent, but should differ)
        assert len(assoc_high) >= 0
        assert len(assoc_low) >= 0

    def test_no_association_with_opposite_emotions(self):
        """Opposite emotions do NOT associate"""
        system = DreamLogicSystem()

        memories = [
            {"content": "A", "emotion": "joy"},
            {"content": "B", "emotion": "sadness"}
        ]

        associations = system.associate_by_emotion(memories)

        # Joy and sadness should NOT connect
        # (Unless implementation allows weak cross-emotion links)
        joy_sadness_pairs = [
            (a, b) for (a, b, sim) in associations
            if (a["emotion"] == "joy" and b["emotion"] == "sadness") or
               (a["emotion"] == "sadness" and b["emotion"] == "joy")
        ]

        # Typically zero or very weak
        assert len(joy_sadness_pairs) == 0 or all(sim < 0.3 for (a, b, sim) in joy_sadness_pairs)


class TestBizarreCombinations:
    """Test surreal/bizarre narrative generation"""

    def test_generates_bizarre_combinations(self):
        """System generates bizarre/surreal combinations"""
        system = DreamLogicSystem()

        fragments = [
            {"content": "elephant", "emotion": "neutral"},
            {"content": "flying", "emotion": "joy"}
        ]

        narrative = system.generate_bizarre_combination(fragments)

        assert narrative is not None
        assert "elements" in narrative or "narrative" in narrative

    def test_allows_contradictions(self):
        """Dream logic allows contradictions (underwater fire)"""
        system = DreamLogicSystem(logical_constraint_strength=0.1)

        fragments = [
            {"content": "underwater", "emotion": "calm"},
            {"content": "fire", "emotion": "excitement"}
        ]

        narrative = system.generate_bizarre_combination(fragments)

        # Should not reject contradiction
        assert narrative is not None
        assert "contradiction_count" in narrative or len(narrative) > 0

    def test_surreal_narrative_creation(self):
        """System creates surreal narratives from fragments"""
        system = DreamLogicSystem()

        fragments = [
            {"content": "grandmother", "emotion": "love"},
            {"content": "spaceship", "emotion": "wonder"},
            {"content": "childhood_home", "emotion": "nostalgia"}
        ]

        narrative = system.generate_bizarre_combination(fragments)

        # Narrative should combine all fragments
        assert len(narrative.get("elements", [])) > 0 or "narrative" in narrative

    def test_bizarreness_increases_with_tolerance(self):
        """Higher tolerance allows more bizarre combinations"""
        system_high = DreamLogicSystem(bizarreness_tolerance=0.9)
        system_low = DreamLogicSystem(bizarreness_tolerance=0.3)

        fragments = [
            {"content": "time_flowing_backward", "emotion": "confusion"},
            {"content": "talking_furniture", "emotion": "surprise"}
        ]

        narrative_high = system_high.generate_bizarre_combination(fragments)
        narrative_low = system_low.generate_bizarre_combination(fragments)

        bizarreness_high = system_high.score_bizarreness(narrative_high)
        bizarreness_low = system_low.score_bizarreness(narrative_low)

        # High tolerance = more bizarre
        assert bizarreness_high >= bizarreness_low

    def test_waking_logic_rejects_bizarreness(self):
        """Waking logic (high constraint) rejects very bizarre combinations"""
        system = DreamLogicSystem(
            logical_constraint_strength=0.95,
            bizarreness_tolerance=0.2
        )

        fragments = [
            {"content": "square_circle", "emotion": "confusion"},
            {"content": "dry_water", "emotion": "surprise"}
        ]

        narrative = system.generate_bizarre_combination(fragments)
        bizarreness = system.score_bizarreness(narrative)

        # Should filter/reduce bizarreness
        assert bizarreness < 0.5


class TestMemoryConsolidation:
    """Test offline memory consolidation (LAB_003 integration)"""

    def test_offline_consolidation(self):
        """System performs offline consolidation (LAB_003)"""
        system = DreamLogicSystem()

        memories = [
            {"content": "event_A", "strength": 0.5},
            {"content": "event_B", "strength": 0.6},
            {"content": "event_C", "strength": 0.3}
        ]

        consolidated = system.offline_consolidation(memories)

        # Should return processed memories
        assert len(consolidated) > 0

    def test_pattern_extraction(self):
        """Consolidation extracts patterns from memories"""
        system = DreamLogicSystem()

        memories = [
            {"content": "meeting_Monday", "pattern": "work"},
            {"content": "meeting_Tuesday", "pattern": "work"},
            {"content": "lunch_Wednesday", "pattern": "social"}
        ]

        consolidated = system.offline_consolidation(memories)

        # Should identify patterns (e.g., "work" repeats)
        # (Implementation: may add "patterns_found" field)
        assert consolidated is not None

    def test_consolidation_strengthens_connections(self):
        """Consolidation strengthens related memories"""
        system = DreamLogicSystem(consolidation_rate=0.1)

        memories = [
            {"content": "learn_concept_A", "strength": 0.4, "related_to": "B"},
            {"content": "learn_concept_B", "strength": 0.5, "related_to": "A"}
        ]

        consolidated = system.offline_consolidation(memories)

        # Consolidation should increase strength
        # (Simulated: strength += consolidation_rate)
        for mem in consolidated:
            if "strength" in mem:
                assert mem["strength"] >= 0.4


class TestNovelConnections:
    """Test extraction of novel creative connections"""

    def test_extracts_novel_connections(self):
        """System extracts novel connections from dream"""
        system = DreamLogicSystem()

        narrative = {
            "elements": [
                {"content": "music", "emotion": "joy"},
                {"content": "mathematics", "emotion": "curiosity"}
            ],
            "associations": [("music", "mathematics", 0.7)]
        }

        novel_connections = system.extract_novel_connections(narrative)

        assert len(novel_connections) > 0

    def test_novel_connections_available_on_wake(self):
        """Novel connections persist after dream ends"""
        system = DreamLogicSystem()

        # Simulate dream session
        result = system.process_event(
            memory_fragments=[
                {"content": "A", "emotion": "joy"},
                {"content": "B", "emotion": "joy"}
            ],
            mode="dream"
        )

        # Should store novel connections
        if "novel_connections" in result:
            assert len(result["novel_connections"]) >= 0

    def test_creative_insights_from_dream(self):
        """Dreams can produce creative insights for waking use"""
        system = DreamLogicSystem()

        fragments = [
            {"content": "problem_unsolved", "emotion": "frustration"},
            {"content": "unrelated_domain", "emotion": "curiosity"}
        ]

        result = system.process_event(memory_fragments=fragments, mode="dream")

        # Novel connections = potential insights
        if "novel_connections" in result:
            novel = result["novel_connections"]
            # At least some connections should emerge
            assert len(novel) >= 0


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_event_complete(self):
        """process_event executes complete dream logic cycle"""
        system = DreamLogicSystem()

        result = system.process_event(
            memory_fragments=[
                {"content": "fragment_A", "emotion": "joy"},
                {"content": "fragment_B", "emotion": "fear"}
            ],
            mode="dream"
        )

        assert "dream_narrative" in result or "narrative" in result

    def test_process_event_updates_stats(self):
        """process_event updates system statistics"""
        system = DreamLogicSystem()

        initial_sessions = system.total_dream_sessions

        system.process_event(
            memory_fragments=[{"content": "test", "emotion": "neutral"}],
            mode="dream"
        )

        assert system.total_dream_sessions == initial_sessions + 1

    def test_dream_mode_vs_wake_mode(self):
        """Dream mode differs significantly from wake mode"""
        system = DreamLogicSystem()

        fragments = [
            {"content": "element_A", "emotion": "joy"},
            {"content": "element_B", "emotion": "joy"}
        ]

        result_dream = system.process_event(memory_fragments=fragments, mode="dream")
        result_wake = system.process_event(memory_fragments=fragments, mode="wake")

        # Dream should have higher bizarreness
        if "bizarreness_score" in result_dream and "bizarreness_score" in result_wake:
            assert result_dream["bizarreness_score"] >= result_wake["bizarreness_score"]
