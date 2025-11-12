"""
LAB_042: Meta-Learning System

Homeostasis: "Learning to learn"

Key Mechanisms:
- Learning rate adaptation (α adjustment based on performance)
- Transfer learning (apply knowledge across domains)
- Few-shot learning (learn from few examples)
- Meta-parameters optimization (learning how to learn better)

Mathematical Model:
- Learning rate adaptation: α_new = α_old * (1 + β * success_rate)
- Transfer strength: T = source_performance * similarity
- Few-shot confidence: C = consistency * sqrt(n_examples)
- Generalization: G = domains_learned / (1 + exp(-performance))

Key Papers:
- Thrun & Pratt (1998): Learning to Learn
- Schmidhuber (1987): Evolutionary principles in self-referential learning
- Bengio et al. (1991): Learning a synaptic learning rule
"""

import math
from typing import Dict, List, Optional


class MetaLearningSystem:
    """
    Meta-Learning: Learning to learn

    Core principle: Experience across tasks improves learning itself

    Implements:
    - Learning rate adaptation
    - Knowledge transfer between domains
    - Few-shot learning
    - Meta-parameter optimization
    """

    def __init__(
        self,
        base_learning_rate: float = 0.1,
        adaptation_rate: float = 0.1
    ):
        """
        Initialize Meta-Learning System

        Args:
            base_learning_rate: Base learning rate [0-1]
            adaptation_rate: Rate of meta-parameter adaptation [0-1]
        """
        self.base_learning_rate = base_learning_rate
        self.adaptation_rate = adaptation_rate

        # Domain-specific learning rates
        self.domain_learning_rates: Dict[str, float] = {}

        # Domain performance tracking
        self.domain_performance: Dict[str, float] = {}

        # Performance history
        self.performance_history: Dict[str, List[float]] = {}

        # Transfer knowledge registry
        self.transfer_registry: Dict[str, Dict] = {}

    def get_learning_rate(
        self,
        domain: str
    ) -> float:
        """
        Get learning rate for domain

        Args:
            domain: Domain identifier

        Returns:
            Learning rate [0-1]
        """
        # Initialize unseen domains to base rate
        if domain not in self.domain_learning_rates:
            self.domain_learning_rates[domain] = self.base_learning_rate

        return self.domain_learning_rates[domain]

    def adapt_learning_rate(
        self,
        domain: str,
        success: bool
    ) -> Dict:
        """
        Adapt learning rate based on success/failure

        Args:
            domain: Domain identifier
            success: Whether learning was successful

        Returns:
            Adaptation result
        """
        current_lr = self.get_learning_rate(domain)

        # Success → Increase learning rate
        if success:
            new_lr = current_lr * (1 + self.adaptation_rate)
        else:
            # Failure → Decrease learning rate
            new_lr = current_lr * (1 - self.adaptation_rate)

        # Bound learning rate [0.01, 1.0]
        new_lr = min(1.0, max(0.01, new_lr))

        self.domain_learning_rates[domain] = new_lr

        return {
            "domain": domain,
            "old_learning_rate": float(current_lr),
            "new_learning_rate": float(new_lr),
            "success": success
        }

    def learn_in_domain(
        self,
        domain: str,
        performance: float
    ) -> Dict:
        """
        Record learning in domain

        Args:
            domain: Domain identifier
            performance: Performance score [0-1]

        Returns:
            Learning result
        """
        # Update domain performance
        self.domain_performance[domain] = performance

        # Record in performance history
        if domain not in self.performance_history:
            self.performance_history[domain] = []
        self.performance_history[domain].append(performance)

        # Adapt learning rate based on performance
        success = performance > 0.7
        self.adapt_learning_rate(domain=domain, success=success)

        return {
            "domain": domain,
            "performance": float(performance),
            "performance_recorded": True
        }

    def transfer_knowledge(
        self,
        source_domain: str,
        target_domain: str,
        similarity: float = 0.7
    ) -> Dict:
        """
        Transfer knowledge from source to target domain

        Args:
            source_domain: Source domain
            target_domain: Target domain
            similarity: Domain similarity [0-1]

        Returns:
            Transfer result
        """
        # Check if source has knowledge
        if source_domain not in self.domain_performance:
            return {
                "transfer_occurred": False,
                "reason": "Source domain has no knowledge"
            }

        source_performance = self.domain_performance[source_domain]

        # Transfer strength: source performance × similarity
        transfer_strength = source_performance * similarity

        # Boost target learning rate
        target_lr = self.get_learning_rate(target_domain)
        boosted_lr = target_lr * (1 + transfer_strength * 0.5)
        boosted_lr = min(1.0, boosted_lr)

        self.domain_learning_rates[target_domain] = boosted_lr

        # Record transfer
        self.transfer_registry[(source_domain, target_domain)] = {
            "source_performance": source_performance,
            "transfer_strength": transfer_strength,
            "similarity": similarity
        }

        return {
            "transfer_occurred": True,
            "source_domain": source_domain,
            "target_domain": target_domain,
            "transfer_strength": float(transfer_strength),
            "target_learning_rate": float(boosted_lr)
        }

    def few_shot_learn(
        self,
        domain: str,
        examples: List[float]
    ) -> Dict:
        """
        Learn from few examples

        Args:
            domain: Domain identifier
            examples: List of example performances [0-1]

        Returns:
            Few-shot learning result
        """
        if len(examples) == 0:
            return {
                "learned": False,
                "reason": "No examples provided"
            }

        # Compute average performance
        avg_performance = sum(examples) / len(examples)

        # Compute consistency (inverse of variance)
        if len(examples) > 1:
            variance = sum((x - avg_performance) ** 2 for x in examples) / len(examples)
            consistency = 1.0 / (1.0 + variance)
        else:
            consistency = 0.5

        # Confidence: consistency × sqrt(n_examples)
        # More examples + high consistency → Higher confidence
        confidence = consistency * math.sqrt(len(examples)) / 3.0  # Normalize by sqrt(9) = 3
        confidence = min(1.0, confidence)

        # Learn in domain if confidence sufficient
        if confidence > 0.3:
            self.learn_in_domain(domain=domain, performance=avg_performance)
            learned = True
        else:
            learned = False

        return {
            "domain": domain,
            "examples_count": len(examples),
            "avg_performance": float(avg_performance),
            "consistency": float(consistency),
            "confidence": float(confidence),
            "learned": learned
        }

    def get_meta_parameters(self) -> Dict:
        """
        Get meta-learning parameters

        Returns:
            Meta-parameters dict
        """
        if len(self.domain_performance) == 0:
            return {
                "domains_learned": 0,
                "average_performance": 0.0,
                "generalization_strength": 0.0,
                "habit_formation_efficiency": 0.0
            }

        # Average performance across domains
        avg_performance = sum(self.domain_performance.values()) / len(self.domain_performance)

        # Generalization strength (sigmoid of domains learned)
        domains_learned = len(self.domain_performance)
        generalization_strength = domains_learned / (1.0 + math.exp(-avg_performance + 0.5))
        generalization_strength = min(1.0, generalization_strength / 10.0)  # Normalize

        # Habit formation efficiency (derived from consistent performance)
        if len(self.performance_history) > 0:
            consistencies = []
            for history in self.performance_history.values():
                if len(history) == 1:
                    # Single record → Perfect consistency (no variance)
                    consistency = 1.0
                    consistencies.append(consistency)
                elif len(history) > 1:
                    avg = sum(history) / len(history)
                    variance = sum((x - avg) ** 2 for x in history) / len(history)
                    consistency = 1.0 / (1.0 + variance)
                    consistencies.append(consistency)

            habit_efficiency = sum(consistencies) / len(consistencies) if consistencies else 0.0
        else:
            habit_efficiency = 0.0

        return {
            "domains_learned": domains_learned,
            "average_performance": float(avg_performance),
            "generalization_strength": float(generalization_strength),
            "habit_formation_efficiency": float(habit_efficiency)
        }

    def optimize_meta_parameters(self) -> Dict:
        """
        Optimize meta-learning parameters

        Returns:
            Optimization result
        """
        # Consider both performance records and adapted learning rates
        total_domains = len(set(self.domain_performance.keys()) | set(self.domain_learning_rates.keys()))

        if total_domains < 3:
            return {
                "optimization_occurred": False,
                "reason": "Insufficient data (need 3+ domains)"
            }

        meta_params = self.get_meta_parameters()

        # Adjust base learning rate based on average performance
        avg_perf = meta_params["average_performance"]

        if avg_perf > 0.8:
            # High performance → Increase base learning rate
            self.base_learning_rate = min(1.0, self.base_learning_rate * 1.1)
        elif avg_perf < 0.5:
            # Low performance → Decrease base learning rate
            self.base_learning_rate = max(0.01, self.base_learning_rate * 0.9)

        return {
            "optimization_occurred": True,
            "new_base_learning_rate": float(self.base_learning_rate),
            "average_performance": float(avg_perf)
        }

    def get_performance_history(
        self,
        domain: str
    ) -> List[float]:
        """
        Get performance history for domain

        Args:
            domain: Domain identifier

        Returns:
            List of performance scores
        """
        return self.performance_history.get(domain, [])

    def get_average_performance(self) -> float:
        """
        Get average performance across all domains

        Returns:
            Average performance [0-1]
        """
        if len(self.domain_performance) == 0:
            return 0.0

        return sum(self.domain_performance.values()) / len(self.domain_performance)

    def adapt_from_rpe(
        self,
        domain: str,
        prediction_error: float
    ) -> Dict:
        """
        Adapt learning rate from reward prediction error (LAB_035 integration)

        Args:
            domain: Domain identifier
            prediction_error: RPE from LAB_035 [-1, 1]

        Returns:
            Adaptation result
        """
        # Positive RPE → Increase learning rate
        if prediction_error > 0.1:
            success = True
            direction = "increase"
        elif prediction_error < -0.1:
            # Negative RPE → Decrease learning rate
            success = False
            direction = "decrease"
        else:
            # Neutral RPE → No change
            return {
                "learning_rate_adjusted": False,
                "reason": "RPE within neutral range"
            }

        self.adapt_learning_rate(domain=domain, success=success)

        return {
            "learning_rate_adjusted": True,
            "direction": direction,
            "prediction_error": float(prediction_error)
        }

    def apply_to_skill(
        self,
        skill_name: str
    ) -> Dict:
        """
        Apply meta-learning boost to skill acquisition (LAB_040 integration)

        Args:
            skill_name: Skill identifier

        Returns:
            Skill boost result
        """
        meta_params = self.get_meta_parameters()

        # Meta-boost: generalization strength
        meta_boost = meta_params["generalization_strength"]

        return {
            "skill_name": skill_name,
            "meta_boost": float(meta_boost)
        }

    def process_event(
        self,
        event_type: str,
        **kwargs
    ) -> Dict:
        """
        Process meta-learning event

        Args:
            event_type: Type of event ("learn", "transfer", etc.)
            **kwargs: Event-specific parameters

        Returns:
            Processing result
        """
        if event_type == "learn":
            return self.learn_in_domain(
                domain=kwargs["domain"],
                performance=kwargs["performance"]
            )

        elif event_type == "transfer":
            return self.transfer_knowledge(
                source_domain=kwargs["source_domain"],
                target_domain=kwargs["target_domain"]
            )

        else:
            return {"error": f"Unknown event type: {event_type}"}

    def get_state(self) -> Dict:
        """
        Get current state of meta-learning system

        Returns:
            System state with meta-learning metrics
        """
        meta_params = self.get_meta_parameters()

        return {
            "domains_learned": meta_params["domains_learned"],
            "average_performance": meta_params["average_performance"],
            "generalization_strength": meta_params["generalization_strength"],
            "base_learning_rate": self.base_learning_rate,
            "adaptation_rate": self.adaptation_rate,
            "transfers_made": len(self.transfer_registry)
        }
