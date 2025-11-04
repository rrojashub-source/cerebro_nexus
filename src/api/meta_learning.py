"""
LAB_036: Meta-Learning - Learning to Learn

Core: Harlow (1949) learning sets, MAML algorithm principles
Functions: Learning rate adaptation, task similarity detection, rapid acquisition
"""

import time
from typing import Dict, List
from dataclasses import dataclass
import numpy as np


@dataclass
class Task:
    task_id: str
    domain: str
    difficulty: float


@dataclass
class LearningExperience:
    task_id: str
    trials: int
    performance: float
    learning_rate_used: float


class MetaLearningSystem:
    def __init__(self):
        self.experiences: List[LearningExperience] = []
        self.base_lr = 0.1
        self.adapted_lrs: Dict[str, float] = {}

    def adapt_learning_rate(self, task: Task) -> float:
        """Adapt LR based on task similarity to past tasks"""
        similar_tasks = [e for e in self.experiences if e.task_id.startswith(task.domain)]

        if similar_tasks:
            # Higher LR for similar tasks (faster learning)
            avg_performance = np.mean([e.performance for e in similar_tasks[-5:]])
            adapted_lr = self.base_lr * (1.5 if avg_performance > 0.7 else 1.0)
        else:
            adapted_lr = self.base_lr

        return min(adapted_lr, 0.5)

    def learn_task(self, task: Task, trials: int = 10) -> LearningExperience:
        """Learn task with adapted parameters"""
        lr = self.adapt_learning_rate(task)

        # Simulate learning (performance improves with trials)
        performance = min(1.0, 0.3 + (trials * lr * 0.05))

        exp = LearningExperience(
            task_id=task.task_id,
            trials=trials,
            performance=performance,
            learning_rate_used=lr
        )

        self.experiences.append(exp)
        return exp

    def get_statistics(self) -> Dict:
        return {
            "total_tasks": len(self.experiences),
            "avg_performance": np.mean([e.performance for e in self.experiences]) if self.experiences else 0.0,
            "avg_lr": np.mean([e.learning_rate_used for e in self.experiences]) if self.experiences else 0.0,
        }


if __name__ == "__main__":
    print("🧠 LAB_036: Meta-Learning - Test")
    print("=" * 60)

    system = MetaLearningSystem()

    # Learn multiple tasks from same domain
    print("\n📚 Learning multiple tasks from 'vision' domain...")
    for i in range(5):
        task = Task(f"vision_task_{i}", "vision", 0.5)
        exp = system.learn_task(task)
        print(f"  Task {i}: LR={exp.learning_rate_used:.3f}, Performance={exp.performance:.3f}")

    # New domain
    print("\n🆕 New domain 'audio'...")
    task_new = Task("audio_task_0", "audio", 0.5)
    exp_new = system.learn_task(task_new)
    print(f"  Audio task: LR={exp_new.learning_rate_used:.3f}, Performance={exp_new.performance:.3f}")

    stats = system.get_statistics()
    print(f"\n📊 Stats: {stats}")
    print("\n✅ LAB_036 Complete!")
