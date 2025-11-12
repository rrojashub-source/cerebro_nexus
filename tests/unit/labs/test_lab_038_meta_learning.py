"""
LAB_038: Meta-Learning - Unit Tests

Advanced Learning: Learning-to-learn, strategy adaptation

Key Papers:
- Harlow (1949) - The formation of learning sets
- Schmidhuber (2015) - Deep learning in neural networks: An overview
- Thrun & Pratt (1998) - Learning to learn
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Advanced_Learning.LAB_038_Meta_Learning.meta_learning_system import (
    MetaLearningSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with empty learning sets"""
        system = MetaLearningSystem()
        assert system.adaptation_rate == 0.1
        assert len(system.learning_sets) == 0
        assert len(system.learning_history) == 0

    def test_custom_adaptation_rate(self):
        """System accepts custom adaptation rate"""
        system = MetaLearningSystem(adaptation_rate=0.2)
        assert system.adaptation_rate == 0.2


class TestLearningSetFormation:
    """Test learning set formation (Harlow 1949)"""

    def test_learning_set_improves_with_practice(self):
        """Multiple trials on similar tasks improve performance (Harlow 1949)"""
        system = MetaLearningSystem()

        # Task type A, multiple trials
        outcomes = [
            {"success": False, "trials_to_solve": 10},
            {"success": True, "trials_to_solve": 8},
            {"success": True, "trials_to_solve": 5},
            {"success": True, "trials_to_solve": 3}
        ]

        learning_set = system.form_learning_set(task_type="pattern_recognition", outcomes=outcomes)

        # Should extract strategy + show improvement
        assert "strategy" in learning_set
        assert learning_set["improvement_detected"] == True
        assert learning_set["final_efficiency"] > learning_set["initial_efficiency"]

    def test_learning_set_generalizes_across_tasks(self):
        """Learning set allows generalization to similar tasks"""
        system = MetaLearningSystem()

        # Train on task type A
        outcomes_A = [
            {"success": True, "trials_to_solve": 5},
            {"success": True, "trials_to_solve": 3}
        ]
        system.form_learning_set(task_type="classification", outcomes=outcomes_A)

        # Apply to similar task type B
        result = system.select_learning_strategy(task_structure={"type": "classification", "complexity": 0.6})

        assert result["strategy_found"] == True
        assert result["task_type"] == "classification"

    def test_insufficient_data_no_learning_set(self):
        """Insufficient trials = no robust learning set"""
        system = MetaLearningSystem()

        # Only 1 trial
        outcomes = [{"success": True, "trials_to_solve": 5}]

        learning_set = system.form_learning_set(task_type="memory_task", outcomes=outcomes)

        # Should indicate insufficient data
        assert learning_set["sufficient_data"] == False


class TestStrategySelection:
    """Test optimal strategy selection for task"""

    def test_known_task_uses_learned_strategy(self):
        """Known task structure → use learned strategy"""
        system = MetaLearningSystem()

        # Train on task type
        outcomes = [
            {"success": True, "trials_to_solve": 4},
            {"success": True, "trials_to_solve": 2}
        ]
        system.form_learning_set(task_type="visual_discrimination", outcomes=outcomes)

        # Select strategy for same type
        strategy = system.select_learning_strategy(
            task_structure={"type": "visual_discrimination", "complexity": 0.5}
        )

        assert strategy["strategy_found"] == True
        assert strategy["source"] == "learned"

    def test_novel_task_exploratory_strategy(self):
        """Novel task structure → use exploratory strategy"""
        system = MetaLearningSystem()

        # No training

        strategy = system.select_learning_strategy(
            task_structure={"type": "novel_task", "complexity": 0.7}
        )

        assert strategy["strategy_found"] == False
        assert strategy["source"] == "exploratory"

    def test_strategy_efficiency_tracked(self):
        """Strategy selection tracks expected efficiency"""
        system = MetaLearningSystem()

        # Train with high efficiency
        outcomes = [
            {"success": True, "trials_to_solve": 2},
            {"success": True, "trials_to_solve": 1}
        ]
        system.form_learning_set(task_type="fast_task", outcomes=outcomes)

        strategy = system.select_learning_strategy(
            task_structure={"type": "fast_task", "complexity": 0.4}
        )

        assert "expected_efficiency" in strategy
        assert strategy["expected_efficiency"] > 0.7  # High efficiency


class TestLearningRateAdaptation:
    """Test learning rate adaptation based on task familiarity"""

    def test_fast_learning_for_known_tasks(self):
        """Known task type → fast learning rate"""
        system = MetaLearningSystem()

        # Train on task
        outcomes = [{"success": True, "trials_to_solve": 3}] * 3
        system.form_learning_set(task_type="familiar_task", outcomes=outcomes)

        # Adapt learning rate for same type
        result = system.adapt_learning_rate(
            task_type="familiar_task",
            performance=0.8
        )

        assert result["learning_rate"] > system.adaptation_rate  # Faster

    def test_slow_learning_for_novel_tasks(self):
        """Novel task → slow, cautious learning rate"""
        system = MetaLearningSystem()

        # No training on this task type

        result = system.adapt_learning_rate(
            task_type="novel_task",
            performance=0.5
        )

        assert result["learning_rate"] <= system.adaptation_rate  # Slower/baseline

    def test_performance_modulates_learning_rate(self):
        """High performance → can increase learning rate"""
        system = MetaLearningSystem()

        outcomes = [{"success": True, "trials_to_solve": 2}] * 3
        system.form_learning_set(task_type="task_A", outcomes=outcomes)

        high_perf = system.adapt_learning_rate(task_type="task_A", performance=0.9)
        low_perf = system.adapt_learning_rate(task_type="task_A", performance=0.3)

        # High performance allows faster learning
        assert high_perf["learning_rate"] > low_perf["learning_rate"]


class TestStrategyTransfer:
    """Test strategy transfer between similar tasks"""

    def test_transfer_from_similar_task(self):
        """Strategy from similar task transfers"""
        system = MetaLearningSystem()

        # Train on source task
        outcomes = [{"success": True, "trials_to_solve": 3}] * 3
        system.form_learning_set(task_type="source_task", outcomes=outcomes)

        # Transfer to target task (similar - 2 of 3 features in common)
        result = system.transfer_strategy(
            source_task={"type": "source_task", "features": ["visual", "discrimination", "spatial"]},
            target_task={"type": "target_task", "features": ["visual", "discrimination", "temporal"]}
        )

        assert result["transfer_applicable"] == True
        assert result["similarity"] >= 0.5  # 2/4 = 0.5

    def test_no_transfer_for_dissimilar_tasks(self):
        """No transfer for dissimilar tasks"""
        system = MetaLearningSystem()

        # Train on source
        outcomes = [{"success": True, "trials_to_solve": 3}] * 2
        system.form_learning_set(task_type="visual_task", outcomes=outcomes)

        # Try transfer to very different task
        result = system.transfer_strategy(
            source_task={"type": "visual_task", "features": ["visual"]},
            target_task={"type": "auditory_task", "features": ["auditory", "sequence"]}
        )

        assert result["transfer_applicable"] == False
        assert result["similarity"] < 0.3

    def test_similarity_based_transfer(self):
        """Transfer strength depends on task similarity"""
        system = MetaLearningSystem()

        outcomes = [{"success": True, "trials_to_solve": 2}] * 3
        system.form_learning_set(task_type="base_task", outcomes=outcomes)

        # High similarity transfer
        high_sim = system.transfer_strategy(
            source_task={"type": "base_task", "features": ["A", "B", "C"]},
            target_task={"type": "similar_task", "features": ["A", "B", "D"]}
        )

        # Low similarity transfer
        low_sim = system.transfer_strategy(
            source_task={"type": "base_task", "features": ["A", "B", "C"]},
            target_task={"type": "different_task", "features": ["X", "Y", "Z"]}
        )

        assert high_sim["similarity"] > low_sim["similarity"]


class TestMetaCognitionIntegration:
    """Test integration with LAB_006 (Metacognition)"""

    def test_monitor_learning_effectiveness(self):
        """Monitor whether learning strategy is effective"""
        system = MetaLearningSystem()

        # Strategy working well
        result_good = system.monitor_learning_effectiveness(
            expected_performance=0.8,
            actual_performance=0.85
        )

        assert result_good["effective"] == True
        assert result_good["performance_error"] < 0.1

        # Strategy not working
        result_bad = system.monitor_learning_effectiveness(
            expected_performance=0.8,
            actual_performance=0.4
        )

        assert result_bad["effective"] == False
        assert result_bad["performance_error"] > 0.3

    def test_switch_strategy_on_failure(self):
        """Switch strategy when current one fails"""
        system = MetaLearningSystem()

        # Initial strategy failing
        switch_result = system.monitor_learning_effectiveness(
            expected_performance=0.7,
            actual_performance=0.3
        )

        assert switch_result["effective"] == False
        assert switch_result["recommend_switch"] == True


class TestLearningCurveModeling:
    """Test learning curve modeling (power law)"""

    def test_power_law_of_practice(self):
        """Learning follows power law (Newell & Rosenbloom 1981)"""
        system = MetaLearningSystem()

        # Simulate practice trials
        trials = [1, 2, 5, 10, 20, 50]
        times = []

        for trial in trials:
            time = system.predict_performance(
                task_type="practice_task",
                trial_number=trial
            )
            times.append(time)

        # Times should decrease (improvement)
        assert times[0] > times[-1]

        # Rate of improvement should slow (diminishing returns)
        early_improvement = times[0] - times[1]
        late_improvement = times[-2] - times[-1]
        assert early_improvement > late_improvement

    def test_learning_plateau_detection(self):
        """Detect when learning plateaus"""
        system = MetaLearningSystem()

        # Simulate plateau (performance stops improving)
        performance_history = [0.3, 0.5, 0.7, 0.85, 0.87, 0.87, 0.88]

        result = system.detect_plateau(performance_history)

        assert result["plateau_detected"] == True
        assert result["plateau_start_index"] >= 3  # Around trial 4-5


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_task_completion(self):
        """Process task completion to update learning sets"""
        system = MetaLearningSystem()

        result = system.process_event(
            event_type="task_completion",
            task_type="test_task",
            success=True,
            trials_to_solve=5,
            complexity=0.6
        )

        assert "learning_set_updated" in result
        assert len(system.learning_history) > 0

    def test_process_strategy_selection(self):
        """Process strategy selection request"""
        system = MetaLearningSystem()

        # Train first
        for i in range(3):
            system.process_event(
                event_type="task_completion",
                task_type="trained_task",
                success=True,
                trials_to_solve=3 - i
            )

        # Select strategy
        result = system.process_event(
            event_type="select_strategy",
            task_structure={"type": "trained_task", "complexity": 0.5}
        )

        assert "strategy" in result
        assert result["strategy"]["strategy_found"] == True


class TestGetState:
    """Test state retrieval"""

    def test_get_state_returns_learning_sets(self):
        """get_state returns all learning sets"""
        system = MetaLearningSystem()

        # Add learning sets
        outcomes = [{"success": True, "trials_to_solve": 3}] * 2
        system.form_learning_set(task_type="task_A", outcomes=outcomes)

        state = system.get_state()

        assert "total_learning_sets" in state
        assert state["total_learning_sets"] == 1
        assert "learning_history_size" in state

    def test_get_state_serializable(self):
        """get_state returns JSON-serializable dict"""
        system = MetaLearningSystem()

        state = system.get_state()

        import json
        json_str = json.dumps(state)
        assert json_str is not None
