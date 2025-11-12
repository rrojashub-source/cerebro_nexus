"""
LAB_038: Meta-Learning System

Function: Learning-to-learn, improve learning efficiency through experience
Neuroscience Basis: Prefrontal cortex, hippocampus, meta-cognitive monitoring

Key Papers:
- Harlow (1949) - The formation of learning sets
- Schmidhuber (2015) - Deep learning in neural networks
- Thrun & Pratt (1998) - Learning to learn
- Newell & Rosenbloom (1981) - Power law of practice

Meta-Learning Model:
- Learning set formation (Harlow 1949): Generalize strategies
- Strategy selection based on task structure
- Learning rate adaptation (fast for familiar, slow for novel)
- Strategy transfer between similar tasks
- Meta-cognitive monitoring (LAB_006 integration)
- Power law of practice (Newell & Rosenbloom 1981)
"""

from typing import Dict, List, Optional
import math


class MetaLearningSystem:
    """
    LAB_038: Meta-Learning System

    Models learning-to-learn through:
    - Learning set formation (Harlow 1949): Extract strategies from experience
    - Strategy selection: Match task to learned strategy
    - Learning rate adaptation: Fast for familiar, slow for novel
    - Strategy transfer: Generalize across similar tasks
    - Meta-cognitive monitoring (LAB_006): Monitor effectiveness

    Integration:
    - → LAB_040 (Skill Acquisition) - apply meta-learning to skills
    - → LAB_041 (Transfer Learning) - generalize strategies
    - ← LAB_034 (Transfer) - build on transfer mechanisms
    - ← LAB_006 (Metacognition) - monitor learning

    Parameters:
    -----------
    adaptation_rate : float
        Base rate for learning rate adaptation (default: 0.1)
    """

    def __init__(
        self,
        adaptation_rate: float = 0.1
    ):
        # Configuration
        self.adaptation_rate = adaptation_rate

        # Learning sets: task_type → strategy
        self.learning_sets: Dict[str, Dict] = {}

        # History
        self.learning_history: List[Dict] = []

    def form_learning_set(
        self,
        task_type: str,
        outcomes: List[Dict]
    ) -> Dict:
        """
        Form learning set from task outcomes (Harlow 1949)

        "Learning-to-learn": Performance improves across similar tasks
        as agent extracts generalizable strategies.

        Parameters:
        -----------
        task_type : str
            Type of task (e.g., "pattern_recognition")
        outcomes : List[Dict]
            List of task outcomes with success and trials_to_solve

        Returns:
        --------
        learning_set : Dict
            Extracted learning strategy
        """
        if len(outcomes) < 2:
            # Insufficient data for learning set
            return {
                "task_type": task_type,
                "sufficient_data": False,
                "strategy": None
            }

        # Analyze improvement trend
        trials_sequence = [outcome.get("trials_to_solve", 10) for outcome in outcomes]

        # Efficiency metric: Normalize to 0-1 range
        # Assume max trials = 20 (worst case)
        # Efficiency = 1 - (trials / max_trials)
        max_trials = 20.0

        initial_efficiency = 1.0 - (min(trials_sequence[0], max_trials) / max_trials)
        final_efficiency = 1.0 - (min(trials_sequence[-1], max_trials) / max_trials)

        # Improvement detected if final > initial
        improvement = final_efficiency > initial_efficiency

        # Extract strategy (simplified: average efficiency)
        avg_efficiency = sum(1.0 - (min(t, max_trials) / max_trials) for t in trials_sequence) / len(trials_sequence)

        strategy = {
            "task_type": task_type,
            "expected_efficiency": float(avg_efficiency),
            "improvement_curve": trials_sequence,
            "num_trials": len(outcomes)
        }

        # Store learning set
        self.learning_sets[task_type] = strategy

        return {
            "task_type": task_type,
            "sufficient_data": True,
            "strategy": strategy,
            "improvement_detected": improvement,
            "initial_efficiency": float(initial_efficiency),
            "final_efficiency": float(final_efficiency)
        }

    def select_learning_strategy(
        self,
        task_structure: Dict
    ) -> Dict:
        """
        Select optimal learning strategy for task

        Parameters:
        -----------
        task_structure : Dict
            Task characteristics (type, complexity, features)

        Returns:
        --------
        strategy : Dict
            Selected strategy with source
        """
        task_type = task_structure.get("type", "unknown")

        # Check if learned strategy exists
        if task_type in self.learning_sets:
            # Known task → use learned strategy
            learned_strategy = self.learning_sets[task_type]

            return {
                "strategy_found": True,
                "task_type": task_type,
                "source": "learned",
                "expected_efficiency": learned_strategy["expected_efficiency"],
                "strategy": learned_strategy
            }
        else:
            # Novel task → use exploratory strategy
            return {
                "strategy_found": False,
                "task_type": task_type,
                "source": "exploratory",
                "expected_efficiency": 0.3,  # Lower baseline
                "strategy": None
            }

    def adapt_learning_rate(
        self,
        task_type: str,
        performance: float
    ) -> Dict:
        """
        Adapt learning rate based on task familiarity + performance

        Fast learning for known tasks with high performance.
        Slow learning for novel tasks or low performance.

        Parameters:
        -----------
        task_type : str
            Task type
        performance : float
            Current performance (0-1)

        Returns:
        --------
        result : Dict
            Adapted learning rate
        """
        # Base rate
        base_rate = self.adaptation_rate

        # Familiarity factor
        if task_type in self.learning_sets:
            # Known task → can learn faster
            familiarity = 1.5
        else:
            # Novel task → cautious
            familiarity = 1.0

        # Performance factor
        # High performance → confident, can increase rate
        # Low performance → cautious
        if performance > 0.7:
            perf_factor = 1.3
        elif performance < 0.4:
            perf_factor = 0.7
        else:
            perf_factor = 1.0

        # Adapted rate
        adapted_rate = base_rate * familiarity * perf_factor

        # Clamp to reasonable range
        adapted_rate = max(0.05, min(0.3, adapted_rate))

        return {
            "learning_rate": float(adapted_rate),
            "familiarity_factor": float(familiarity),
            "performance_factor": float(perf_factor)
        }

    def transfer_strategy(
        self,
        source_task: Dict,
        target_task: Dict
    ) -> Dict:
        """
        Transfer learned strategy from source to target task

        Based on task similarity (feature overlap).

        Parameters:
        -----------
        source_task : Dict
            Source task (type, features)
        target_task : Dict
            Target task (type, features)

        Returns:
        --------
        result : Dict
            Transfer result with similarity
        """
        source_type = source_task.get("type", "unknown")
        source_features = set(source_task.get("features", []))
        target_features = set(target_task.get("features", []))

        # Check if source has learning set
        if source_type not in self.learning_sets:
            return {
                "transfer_applicable": False,
                "similarity": 0.0,
                "reason": "Source task has no learning set"
            }

        # Compute similarity (Jaccard index)
        if len(source_features) == 0 or len(target_features) == 0:
            similarity = 0.0
        else:
            intersection = len(source_features & target_features)
            union = len(source_features | target_features)
            similarity = intersection / union

        # Transfer applicable if similarity > threshold (lowered to 0.3 for flexibility)
        transfer_applicable = similarity > 0.3

        return {
            "transfer_applicable": transfer_applicable,
            "similarity": float(similarity),
            "source_strategy": self.learning_sets[source_type] if transfer_applicable else None
        }

    def monitor_learning_effectiveness(
        self,
        expected_performance: float,
        actual_performance: float
    ) -> Dict:
        """
        Monitor whether learning strategy is effective (LAB_006 integration)

        Parameters:
        -----------
        expected_performance : float
            Expected performance from strategy (0-1)
        actual_performance : float
            Actual performance achieved (0-1)

        Returns:
        --------
        result : Dict
            Effectiveness monitoring result
        """
        # Performance error
        error = abs(expected_performance - actual_performance)

        # Effective if error < threshold
        effective = error < 0.2

        # Recommend switch if large negative deviation
        underperforming = actual_performance < (expected_performance - 0.3)
        recommend_switch = underperforming

        return {
            "effective": effective,
            "performance_error": float(error),
            "recommend_switch": recommend_switch,
            "expected": float(expected_performance),
            "actual": float(actual_performance)
        }

    def predict_performance(
        self,
        task_type: str,
        trial_number: int
    ) -> float:
        """
        Predict performance using power law of practice (Newell & Rosenbloom 1981)

        Time = A + B * N^(-α)
        where N = trial number, α ≈ 0.4-0.6 (power law exponent)

        Parameters:
        -----------
        task_type : str
            Task type
        trial_number : int
            Trial number (1, 2, 3, ...)

        Returns:
        --------
        predicted_time : float
            Predicted time/cost to complete
        """
        # Power law parameters
        A = 1.0  # Asymptotic minimum time
        B = 10.0  # Initial time constant
        alpha = 0.5  # Power law exponent

        # Check if we have learning set (adjusts parameters)
        if task_type in self.learning_sets:
            # Familiar task → faster asymptote
            A = 0.5
            B = 5.0

        # Power law
        time = A + B * (trial_number ** (-alpha))

        return float(time)

    def detect_plateau(
        self,
        performance_history: List[float]
    ) -> Dict:
        """
        Detect when learning plateaus (performance stops improving)

        Parameters:
        -----------
        performance_history : List[float]
            History of performance values

        Returns:
        --------
        result : Dict
            Plateau detection result
        """
        if len(performance_history) < 4:
            return {"plateau_detected": False, "reason": "Insufficient data"}

        # Detect plateau: last 3 values have < 5% change
        recent = performance_history[-3:]
        max_change = max(abs(recent[i+1] - recent[i]) for i in range(len(recent)-1))

        plateau_detected = max_change < 0.05

        # Find plateau start
        plateau_start = None
        if plateau_detected:
            for i in range(len(performance_history) - 3):
                window = performance_history[i:i+3]
                window_change = max(abs(window[j+1] - window[j]) for j in range(len(window)-1))
                if window_change < 0.05:
                    plateau_start = i
                    break

        return {
            "plateau_detected": plateau_detected,
            "plateau_start_index": plateau_start,
            "max_recent_change": float(max_change) if not math.isnan(max_change) else 0.0
        }

    def process_event(
        self,
        event_type: str,
        **kwargs
    ) -> Dict:
        """
        Main processing: handle meta-learning events

        Event types:
        - task_completion: Update learning sets
        - select_strategy: Choose strategy for new task

        Parameters:
        -----------
        event_type : str
            Type of event
        **kwargs : Dict
            Event-specific parameters

        Returns:
        --------
        result : Dict
            Event processing result
        """
        if event_type == "task_completion":
            # Extract parameters
            task_type = kwargs.get("task_type", "unknown")
            success = kwargs.get("success", True)
            trials_to_solve = kwargs.get("trials_to_solve", 5)

            # Add to history
            outcome = {
                "task_type": task_type,
                "success": success,
                "trials_to_solve": trials_to_solve
            }
            self.learning_history.append(outcome)

            # Form/update learning set if enough data
            task_outcomes = [o for o in self.learning_history if o["task_type"] == task_type]

            if len(task_outcomes) >= 2:
                learning_set = self.form_learning_set(task_type, task_outcomes)
                return {
                    "learning_set_updated": True,
                    "task_type": task_type,
                    "learning_set": learning_set
                }
            else:
                return {
                    "learning_set_updated": False,
                    "task_type": task_type,
                    "reason": "Insufficient data (need >= 2 trials)"
                }

        elif event_type == "select_strategy":
            task_structure = kwargs.get("task_structure", {})
            strategy = self.select_learning_strategy(task_structure)

            return {
                "event": "strategy_selection",
                "strategy": strategy
            }

        else:
            return {"error": f"Unknown event type: {event_type}"}

    def get_state(self) -> Dict:
        """Get current meta-learning state"""
        return {
            "total_learning_sets": len(self.learning_sets),
            "learning_history_size": len(self.learning_history),
            "adaptation_rate": float(self.adaptation_rate),
            "task_types_learned": list(self.learning_sets.keys())
        }
