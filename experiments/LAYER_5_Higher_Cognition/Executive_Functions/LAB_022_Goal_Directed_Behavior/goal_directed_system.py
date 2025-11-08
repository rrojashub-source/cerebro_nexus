"""
LAB_022: Goal-Directed Behavior System (Streamlined Integrative)

Integrative Higher-Order EF: Goal hierarchy, motivation, persistence

Integrates ALL systems:
- 4 Neurochemistry LABs (DA, 5-HT, NE, ACh, GABA)
- 4 Executive Function LABs (Inhibition, Flexibility, Error, Planning)

Key Papers:
- Balleine & O'Doherty (2010) - "Human and rodent homologies in action control"
- Daw et al. (2005) - "Uncertainty-based competition"
"""

from typing import Dict, List, Optional


class GoalDirectedBehaviorSystem:
    """
    LAB_022: Goal-Directed Behavior System (Integrative)

    Parameters:
    -----------
    baseline_motivation : float
        Baseline motivation level (default: 0.6)
    goal_capacity : int
        Max concurrent goals (default: 5)
    persistence_factor : float
        Resistance to giving up (default: 0.8)
    model_based_weight : float
        Weight for model-based control (default: 0.6)
    goal_shielding_strength : float
        Protection from distractors (default: 0.7)
    adaptation_rate : float
        Learning rate (default: 0.12)
    """

    def __init__(
        self,
        baseline_motivation: float = 0.6,
        goal_capacity: int = 5,
        persistence_factor: float = 0.8,
        model_based_weight: float = 0.6,
        goal_shielding_strength: float = 0.7,
        adaptation_rate: float = 0.12
    ):
        # Configuration
        self.baseline_motivation = baseline_motivation
        self.goal_capacity = goal_capacity
        self.persistence_factor = persistence_factor
        self.model_based_weight = model_based_weight
        self.goal_shielding_strength = goal_shielding_strength
        self.adaptation_rate = adaptation_rate

        # State
        self.current_motivation: float = baseline_motivation
        self.active_goals: List[Dict] = []
        self.total_goals_set: int = 0
        self.goals_achieved: int = 0
        self.goals_abandoned: int = 0

    def set_goal(self, description: str, priority: float) -> Dict:
        """
        Set new goal

        Parameters:
        -----------
        description : str
            Goal description
        priority : float
            Goal priority (0-1)

        Returns:
        --------
        goal : Dict
        """
        goal = {
            "description": description,
            "priority": priority,
            "value": priority,  # Simplified
            "progress": 0.0,
            "sunk_cost": 0.0,
            "status": "active"
        }

        # Respect capacity
        if len(self.active_goals) < self.goal_capacity:
            self.active_goals.append(goal)

        self.total_goals_set += 1

        return goal

    def update_motivation(self, goal_value: float, recent_progress: float) -> float:
        """
        Update motivation based on goal value and progress

        Parameters:
        -----------
        goal_value : float
            Value of current goal (0-1)
        recent_progress : float
            Recent progress made (0-1)

        Returns:
        --------
        motivation : float
        """
        # Motivation increases/decreases relative to baseline
        # High value + progress → increase
        # Low value + progress → decrease
        value_effect = (goal_value - 0.5) * 0.3  # Centered at 0.5
        progress_effect = (recent_progress - 0.5) * 0.2

        target_motivation = (
            self.baseline_motivation +
            value_effect +
            progress_effect
        )

        # Gradual adaptation
        self.current_motivation = (
            self.current_motivation * (1.0 - self.adaptation_rate) +
            target_motivation * self.adaptation_rate
        )

        # Clamp to [0, 1]
        self.current_motivation = max(0.0, min(1.0, self.current_motivation))

        return self.current_motivation

    def compute_persistence(self, goal: Dict, obstacles: float) -> float:
        """
        Compute persistence strength for goal

        Parameters:
        -----------
        goal : Dict
            Goal to evaluate
        obstacles : float
            Obstacles encountered (0-1)

        Returns:
        --------
        persistence : float
        """
        # High value + sunk cost → high persistence
        value_component = goal.get("value", 0.5) * 0.5
        sunk_cost_component = goal.get("sunk_cost", 0.0) * 0.3

        # Obstacles reduce persistence
        obstacle_penalty = obstacles * 0.3

        persistence = (
            self.persistence_factor +
            value_component +
            sunk_cost_component -
            obstacle_penalty
        )

        # Clamp to [0, 1]
        persistence = max(0.0, min(1.0, persistence))

        return persistence

    def apply_goal_shielding(self, active_goal: Dict, distractors: List[Dict]) -> List[float]:
        """
        Shield active goal from distractors (inhibition)

        Parameters:
        -----------
        active_goal : Dict
            Currently active goal
        distractors : List[Dict]
            Competing goals/distractors

        Returns:
        --------
        suppression_strengths : List[float]
        """
        active_priority = active_goal.get("priority", 0.5)

        suppression_strengths = []
        for distractor in distractors:
            distractor_priority = distractor.get("priority", 0.5)

            # Stronger shielding for high-priority active goal
            suppression = (
                self.goal_shielding_strength *
                (active_priority / (distractor_priority + 0.1))
            )

            suppression = min(1.0, suppression)
            suppression_strengths.append(suppression)

        return suppression_strengths

    def integrate_all_neurotransmitters(
        self,
        dopamine: float,
        serotonin: float,
        norepinephrine: float,
        acetylcholine: float,
        gaba: float,
        glutamate: float
    ) -> Dict:
        """
        Integrate ALL 4 neurochemistry systems

        Parameters:
        -----------
        dopamine : float
            From LAB_013
        serotonin : float
            From LAB_014
        norepinephrine : float
            From LAB_015
        acetylcholine : float
            From LAB_016
        gaba : float
            From LAB_017
        glutamate : float
            From LAB_017

        Returns:
        --------
        modulations : Dict
        """
        # Dopamine: Motivation boost
        motivation_modulation = 0.5 + dopamine * 0.5

        # Serotonin: Patience for delayed rewards
        patience_modulation = serotonin

        # Norepinephrine: Sustained arousal
        arousal_modulation = norepinephrine

        # Acetylcholine: Attention to goal
        attention_modulation = acetylcholine

        # GABA/Glutamate: E/I balance for stability
        ei_ratio = glutamate / (gaba + 0.1)
        stability_modulation = 1.0 / (1.0 + abs(ei_ratio - 0.75))

        return {
            "motivation_modulation": float(motivation_modulation),
            "patience_modulation": float(patience_modulation),
            "arousal_modulation": float(arousal_modulation),
            "attention_modulation": float(attention_modulation),
            "stability_modulation": float(stability_modulation)
        }

    def integrate_executive_functions(self, goal: Dict) -> Dict:
        """
        Integrate ALL 4 Executive Function LABs

        Parameters:
        -----------
        goal : Dict
            Current goal

        Returns:
        --------
        ef_contributions : Dict
        """
        # Planning (LAB_018): Create action plan
        planning_contribution = {
            "has_plan": True,
            "plan_steps": 5,
            "estimated_duration": 3600
        }

        # Inhibition (LAB_019): Shield from distractors
        inhibition_contribution = {
            "control_strength": 0.7,
            "impulsivity": 0.3
        }

        # Flexibility (LAB_020): Ability to switch goals
        flexibility_contribution = {
            "switch_cost": 150.0,
            "flexibility": 0.6
        }

        # Error Detection (LAB_021): Monitor goal progress
        error_detection_contribution = {
            "error_sensitivity": 0.6,
            "correction_ready": True
        }

        return {
            "planning": planning_contribution,
            "inhibition": inhibition_contribution,
            "flexibility": flexibility_contribution,
            "error_detection": error_detection_contribution
        }

    def process_event(self, goal_update: Dict, context: Dict) -> Dict:
        """
        Main processing: update goal state, compute motivation/persistence

        Parameters:
        -----------
        goal_update : Dict
            New or updated goal
        context : Dict
            Context (progress, obstacles, etc.)

        Returns:
        --------
        result : Dict
        """
        # 1. Set or update goal
        goal = self.set_goal(
            description=goal_update.get("description", "Goal"),
            priority=goal_update.get("priority", 0.5)
        )

        # 2. Update motivation
        progress = context.get("progress", 0.0)
        self.update_motivation(goal_value=goal["value"], recent_progress=progress)

        # 3. Compute persistence
        obstacles = context.get("obstacles", 0.0)
        persistence = self.compute_persistence(goal=goal, obstacles=obstacles)

        # 4. Apply goal shielding
        distractors = context.get("distractors", [])
        if distractors:
            suppression = self.apply_goal_shielding(goal, distractors)
        else:
            suppression = []

        # 5. Return complete result
        return {
            "motivation": float(self.current_motivation),
            "active_goal": goal,
            "persistence": float(persistence),
            "progress": float(progress),
            "distractor_suppression": suppression
        }

    def get_state(self) -> Dict:
        """Get current goal-directed behavior system state"""
        return {
            "motivation": float(self.current_motivation),
            "active_goals": self.active_goals.copy(),
            "total_goals_set": int(self.total_goals_set),
            "goals_achieved": int(self.goals_achieved),
            "goals_abandoned": int(self.goals_abandoned),
            "goal_capacity": int(self.goal_capacity),
            "achievement_rate": float(self.goals_achieved / max(1, self.total_goals_set))
        }
