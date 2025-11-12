"""
LAB_042: Meta-Learning - Unit Tests

Homeostasis: "Learning to learn"

Key Papers:
- Thrun & Pratt (1998) - Learning to Learn
- Schmidhuber (1987) - Evolutionary principles in self-referential learning
- Bengio et al. (1991) - Learning a synaptic learning rule
"""

import pytest
import sys
from pathlib import Path

experiments_path = Path(__file__).parent.parent.parent.parent / "experiments"
sys.path.insert(0, str(experiments_path))

from LAYER_5_Higher_Cognition.Advanced_Learning.LAB_042_Meta_Learning.meta_learning_system import (
    MetaLearningSystem
)


class TestInitialization:
    """Test system initialization"""

    def test_default_initialization(self):
        """System initializes with default meta-learning parameters"""
        system = MetaLearningSystem()
        assert system.base_learning_rate == 0.1
        assert len(system.domain_performance) == 0

    def test_custom_base_learning_rate(self):
        """System accepts custom base learning rate"""
        system = MetaLearningSystem(base_learning_rate=0.05)
        assert system.base_learning_rate == 0.05

    def test_custom_adaptation_rate(self):
        """System accepts custom adaptation rate"""
        system = MetaLearningSystem(adaptation_rate=0.2)
        assert system.adaptation_rate == 0.2


class TestLearningRateAdaptation:
    """Test learning rate adaptation mechanism"""

    def test_success_increases_learning_rate(self):
        """Success → Increase learning rate (faster learning)"""
        system = MetaLearningSystem()

        initial_lr = system.get_learning_rate(domain="task_A")

        # Signal success
        system.adapt_learning_rate(domain="task_A", success=True)

        final_lr = system.get_learning_rate(domain="task_A")

        assert final_lr > initial_lr

    def test_failure_decreases_learning_rate(self):
        """Failure → Decrease learning rate (more careful)"""
        system = MetaLearningSystem()

        initial_lr = system.get_learning_rate(domain="task_B")

        # Signal failure
        system.adapt_learning_rate(domain="task_B", success=False)

        final_lr = system.get_learning_rate(domain="task_B")

        assert final_lr < initial_lr

    def test_repeated_success_accelerates_learning(self):
        """Repeated success → Stronger learning rate boost"""
        system = MetaLearningSystem()

        initial_lr = system.get_learning_rate(domain="task_C")

        # Multiple successes
        for _ in range(5):
            system.adapt_learning_rate(domain="task_C", success=True)

        final_lr = system.get_learning_rate(domain="task_C")

        assert final_lr > initial_lr * 1.2

    def test_learning_rate_bounded(self):
        """Learning rate bounded [0.01, 1.0]"""
        system = MetaLearningSystem()

        # Many successes (should cap at 1.0)
        for _ in range(50):
            system.adapt_learning_rate(domain="task_D", success=True)

        lr = system.get_learning_rate(domain="task_D")

        assert lr <= 1.0

        # Many failures (should floor at 0.01)
        for _ in range(50):
            system.adapt_learning_rate(domain="task_E", success=False)

        lr = system.get_learning_rate(domain="task_E")

        assert lr >= 0.01


class TestTransferLearning:
    """Test knowledge transfer between domains"""

    def test_transfer_from_source_to_target(self):
        """Knowledge from source domain → Target domain"""
        system = MetaLearningSystem()

        # Learn in source domain
        system.learn_in_domain(domain="source", performance=0.9)

        # Transfer to target
        result = system.transfer_knowledge(
            source_domain="source",
            target_domain="target"
        )

        assert result["transfer_occurred"] == True
        assert result["transfer_strength"] > 0

    def test_high_performance_source_stronger_transfer(self):
        """High source performance → Stronger transfer"""
        system = MetaLearningSystem()

        # High performance source
        system.learn_in_domain(domain="source_high", performance=0.95)

        result_high = system.transfer_knowledge(
            source_domain="source_high",
            target_domain="target_1"
        )

        # Low performance source
        system.learn_in_domain(domain="source_low", performance=0.3)

        result_low = system.transfer_knowledge(
            source_domain="source_low",
            target_domain="target_2"
        )

        assert result_high["transfer_strength"] > result_low["transfer_strength"]

    def test_transfer_boosts_target_learning_rate(self):
        """Transfer → Boost target domain learning rate"""
        system = MetaLearningSystem()

        system.learn_in_domain(domain="source", performance=0.9)

        initial_target_lr = system.get_learning_rate(domain="target")

        system.transfer_knowledge(source_domain="source", target_domain="target")

        final_target_lr = system.get_learning_rate(domain="target")

        assert final_target_lr > initial_target_lr

    def test_no_transfer_without_source_knowledge(self):
        """No transfer if source domain has no knowledge"""
        system = MetaLearningSystem()

        result = system.transfer_knowledge(
            source_domain="unknown",
            target_domain="target"
        )

        assert result["transfer_occurred"] == False


class TestFewShotLearning:
    """Test learning from few examples"""

    def test_few_examples_can_learn(self):
        """Few examples (3-5) → Successful learning"""
        system = MetaLearningSystem()

        # Learn from few examples
        result = system.few_shot_learn(
            domain="new_task",
            examples=[0.8, 0.85, 0.9]
        )

        assert result["learned"] == True
        assert result["confidence"] > 0.5

    def test_more_examples_higher_confidence(self):
        """More examples → Higher confidence"""
        system = MetaLearningSystem()

        result_few = system.few_shot_learn(
            domain="task_few",
            examples=[0.7, 0.75]
        )

        result_many = system.few_shot_learn(
            domain="task_many",
            examples=[0.7, 0.75, 0.8, 0.85, 0.9]
        )

        assert result_many["confidence"] > result_few["confidence"]

    def test_consistent_examples_better_learning(self):
        """Consistent examples → Better learning"""
        system = MetaLearningSystem()

        # Consistent examples
        result_consistent = system.few_shot_learn(
            domain="task_consistent",
            examples=[0.8, 0.82, 0.81, 0.83]
        )

        # Inconsistent examples
        result_inconsistent = system.few_shot_learn(
            domain="task_inconsistent",
            examples=[0.2, 0.9, 0.3, 0.85]
        )

        assert result_consistent["confidence"] > result_inconsistent["confidence"]


class TestMetaParameters:
    """Test meta-parameter optimization"""

    def test_meta_parameters_track_learning_history(self):
        """Meta-parameters adapt based on learning history"""
        system = MetaLearningSystem()

        # Learn across multiple domains
        system.learn_in_domain(domain="A", performance=0.9)
        system.learn_in_domain(domain="B", performance=0.85)
        system.learn_in_domain(domain="C", performance=0.95)

        meta_params = system.get_meta_parameters()

        assert meta_params["domains_learned"] == 3
        assert meta_params["average_performance"] > 0.8

    def test_meta_learning_rate_optimization(self):
        """Meta-learning optimizes base learning rate"""
        system = MetaLearningSystem()

        initial_base_lr = system.base_learning_rate

        # Experience varied success rates across 3+ domains
        for _ in range(10):
            system.adapt_learning_rate(domain="task_X", success=True)
            system.adapt_learning_rate(domain="task_Y", success=False)
            system.adapt_learning_rate(domain="task_Z", success=True)

        # Meta-learning should optimize base_learning_rate
        result = system.optimize_meta_parameters()

        assert result["optimization_occurred"] == True

    def test_generalization_strength_increases(self):
        """More domains learned → Stronger generalization"""
        system = MetaLearningSystem()

        # Learn in multiple domains
        for i in range(10):
            system.learn_in_domain(domain=f"domain_{i}", performance=0.8)

        meta_params = system.get_meta_parameters()

        assert meta_params["generalization_strength"] > 0.5


class TestPerformanceTracking:
    """Test performance tracking across domains"""

    def test_track_domain_performance(self):
        """Track performance per domain"""
        system = MetaLearningSystem()

        system.learn_in_domain(domain="task_A", performance=0.9)

        assert "task_A" in system.domain_performance
        assert system.domain_performance["task_A"] > 0

    def test_performance_history_recorded(self):
        """Performance history recorded over time"""
        system = MetaLearningSystem()

        system.learn_in_domain(domain="task_B", performance=0.5)
        system.learn_in_domain(domain="task_B", performance=0.7)
        system.learn_in_domain(domain="task_B", performance=0.9)

        history = system.get_performance_history(domain="task_B")

        assert len(history) >= 3
        assert history[-1] > history[0]  # Improving

    def test_average_performance_computed(self):
        """Average performance across all domains"""
        system = MetaLearningSystem()

        system.learn_in_domain(domain="A", performance=0.8)
        system.learn_in_domain(domain="B", performance=0.9)
        system.learn_in_domain(domain="C", performance=0.7)

        avg = system.get_average_performance()

        expected = (0.8 + 0.9 + 0.7) / 3
        assert abs(avg - expected) < 0.01


class TestIntegration:
    """Test integration with other LABs"""

    def test_integration_with_rpe(self):
        """LAB_035: RPE drives meta-learning adaptation"""
        system = MetaLearningSystem()

        # Positive RPE → Increase learning rate
        result = system.adapt_from_rpe(
            domain="task_A",
            prediction_error=0.5  # Positive RPE
        )

        assert result["learning_rate_adjusted"] == True
        assert result["direction"] == "increase"

    def test_integration_with_skill_acquisition(self):
        """LAB_040: Skill learning benefits from meta-learning"""
        system = MetaLearningSystem()

        # Meta-learning boosts skill acquisition
        system.learn_in_domain(domain="skill_base", performance=0.9)

        result = system.apply_to_skill(skill_name="related_skill")

        assert result["meta_boost"] > 0

    def test_integration_with_habit_formation(self):
        """LAB_036: Meta-learning accelerates habit formation"""
        system = MetaLearningSystem()

        # Multiple habit formations → Better meta-learning
        for i in range(5):
            system.learn_in_domain(domain=f"habit_{i}", performance=0.85)

        meta_params = system.get_meta_parameters()

        assert meta_params["habit_formation_efficiency"] > 0.7


class TestProcessEvent:
    """Test main processing interface"""

    def test_process_learning_event(self):
        """Process learning event"""
        system = MetaLearningSystem()

        result = system.process_event(
            event_type="learn",
            domain="task_A",
            performance=0.8
        )

        assert "performance_recorded" in result

    def test_process_transfer_event(self):
        """Process knowledge transfer event"""
        system = MetaLearningSystem()

        system.learn_in_domain(domain="source", performance=0.9)

        result = system.process_event(
            event_type="transfer",
            source_domain="source",
            target_domain="target"
        )

        assert "transfer_occurred" in result


class TestGetState:
    """Test state retrieval"""

    def test_get_state_returns_meta_learning_metrics(self):
        """get_state returns meta-learning metrics"""
        system = MetaLearningSystem()

        system.learn_in_domain(domain="A", performance=0.8)

        state = system.get_state()

        assert "domains_learned" in state
        assert "average_performance" in state
        assert "base_learning_rate" in state

    def test_get_state_serializable(self):
        """get_state returns JSON-serializable dict"""
        system = MetaLearningSystem()

        state = system.get_state()

        import json
        json_str = json.dumps(state)
        assert json_str is not None
