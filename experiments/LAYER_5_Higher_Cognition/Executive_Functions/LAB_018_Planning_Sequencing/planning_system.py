"""
LAB_018: Planning & Sequencing System (Simplified Core)

Higher-Order Executive Function: Multi-step planning and temporal sequencing

Biological Inspiration:
- Dorsolateral prefrontal cortex (dlPFC) - Plan maintenance
- Lateral frontal pole - Goal hierarchy

Core Functions:
- Goal decomposition into steps
- Action sequencing with dependencies
- Duration estimation
- Execution monitoring
- Replanning

Key Papers:
- Koechlin & Hyafil (2007) - "Anterior prefrontal function"
- Badre & D'Esposito (2009) - "Rostro-caudal axis of frontal lobe"
"""

from typing import Dict, List, Optional


class PlanningSystem:
    """
    LAB_018: Planning & Sequencing System (Simplified)

    Parameters:
    -----------
    baseline_planning_capacity : float
        Baseline planning ability (default: 0.6)
    max_plan_depth : int
        Maximum goal hierarchy depth (default: 5)
    max_plan_length : int
        Maximum action sequence length (default: 10)
    sequencing_precision : float
        Temporal ordering accuracy (default: 0.8)
    replanning_threshold : float
        When to trigger replanning (default: 0.3)
    adaptation_rate : float
        Learning rate (default: 0.1)
    """

    def __init__(
        self,
        baseline_planning_capacity: float = 0.6,
        max_plan_depth: int = 5,
        max_plan_length: int = 10,
        sequencing_precision: float = 0.8,
        replanning_threshold: float = 0.3,
        adaptation_rate: float = 0.1
    ):
        # Configuration
        self.baseline_planning_capacity = baseline_planning_capacity
        self.max_plan_depth = max_plan_depth
        self.max_plan_length = max_plan_length
        self.sequencing_precision = sequencing_precision
        self.replanning_threshold = replanning_threshold
        self.adaptation_rate = adaptation_rate

        # State
        self.current_capacity: float = baseline_planning_capacity
        self.active_plan: Optional[Dict] = None
        self.plan_history: List[Dict] = []
        self.total_plans_created: int = 0
        self.successful_plans: int = 0
        self.replanning_count: int = 0

    def create_plan(self, goal: str, constraints: Dict) -> Dict:
        """
        Create hierarchical plan for goal

        Parameters:
        -----------
        goal : str
            High-level goal description
        constraints : Dict
            Constraints (max_time, max_actions, etc.)

        Returns:
        --------
        plan : Dict
            {
                "goal": str,
                "steps": List[Dict],
                "total_steps": int,
                "created_at": float
            }
        """
        # Decompose goal into steps (simplified)
        num_steps = min(
            int(self.current_capacity * 10),
            self.max_plan_length
        )

        steps = []
        for i in range(num_steps):
            step = {
                "id": f"step_{i+1}",
                "description": f"Action {i+1} for {goal}",
                "duration_estimate": 300 + (i * 100),  # seconds
                "deps": [f"step_{i}"] if i > 0 else [],
                "status": "pending"
            }
            steps.append(step)

        plan = {
            "goal": goal,
            "steps": steps,
            "total_steps": num_steps,
            "created_at": 0.0,  # Timestamp
            "status": "active"
        }

        # Update state
        self.active_plan = plan
        self.total_plans_created += 1

        return plan

    def sequence_actions(self, actions: List[Dict]) -> List[Dict]:
        """
        Order actions respecting dependencies (topological sort simplified)

        Parameters:
        -----------
        actions : List[Dict]
            Unordered actions with dependencies

        Returns:
        --------
        sequenced : List[Dict]
            Actions in execution order
        """
        # Simple topological sort
        sequenced = []
        remaining = actions.copy()

        while remaining:
            # Find action with all dependencies satisfied
            for action in remaining:
                deps_satisfied = all(
                    dep in [a["id"] for a in sequenced]
                    for dep in action.get("deps", [])
                )

                if deps_satisfied:
                    sequenced.append(action)
                    remaining.remove(action)
                    break

        return sequenced

    def estimate_duration(self, plan: Dict) -> float:
        """
        Estimate total plan duration

        Parameters:
        -----------
        plan : Dict
            Plan with steps

        Returns:
        --------
        duration : float
            Estimated duration (seconds)
        """
        # Sum all step durations (simplified - assumes sequential)
        total_duration = sum(
            step.get("duration_estimate", 300)
            for step in plan.get("steps", [])
        )

        return total_duration

    def monitor_execution(self, plan: Dict, progress: Dict) -> Dict:
        """
        Monitor plan execution and detect deviations

        Parameters:
        -----------
        plan : Dict
            Active plan
        progress : Dict
            Current progress (completed_steps, total_steps)

        Returns:
        --------
        monitoring : Dict
            {
                "on_track": bool,
                "deviation_magnitude": float,
                "should_replan": bool
            }
        """
        completed = progress.get("completed_steps", 0)
        total = progress.get("total_steps", plan.get("total_steps", 1))

        # Completion rate
        completion_rate = completed / total if total > 0 else 0.0

        # Expected: should be at least 40% complete after starting
        expected_rate = 0.4
        deviation = max(0.0, expected_rate - completion_rate)

        # On track if deviation below threshold
        on_track = (deviation < self.replanning_threshold)
        should_replan = not on_track

        return {
            "on_track": on_track,
            "deviation_magnitude": float(deviation),
            "should_replan": should_replan
        }

    def trigger_replanning(self, original_plan: Dict, new_constraints: Dict) -> Dict:
        """
        Create revised plan

        Parameters:
        -----------
        original_plan : Dict
            Original plan
        new_constraints : Dict
            Updated constraints

        Returns:
        --------
        new_plan : Dict
            Revised plan
        """
        # Create new plan with updated constraints
        new_plan = self.create_plan(
            goal=original_plan["goal"],
            constraints=new_constraints
        )

        # Mark as replanning
        new_plan["is_replan"] = True

        # Update state
        self.replanning_count += 1

        return new_plan

    def integrate_dopamine(self, dopamine_level: float) -> float:
        """
        Modulate planning capacity by dopamine

        High dopamine = more ambitious plans
        Low dopamine = conservative plans

        Parameters:
        -----------
        dopamine_level : float
            Current dopamine level (0-1) from LAB_013

        Returns:
        --------
        modulated_capacity : float
            Dopamine-modulated planning capacity (0-1)
        """
        # Linear modulation for simplicity
        # dopamine=0.3 → 0.7x capacity
        # dopamine=0.9 → 1.3x capacity
        modulation_factor = 0.7 + (dopamine_level * 0.6)

        modulated_capacity = self.current_capacity * modulation_factor

        # Clamp to [0, 1]
        modulated_capacity = max(0.0, min(1.0, modulated_capacity))

        return modulated_capacity

    def integrate_acetylcholine(self, ach_level: float) -> float:
        """
        Modulate sequencing precision by acetylcholine

        High ACh = better attention to plan details

        Parameters:
        -----------
        ach_level : float
            Current acetylcholine level (0-1) from LAB_016

        Returns:
        --------
        precision_boost : float
            Acetylcholine-modulated sequencing precision (0-1)
        """
        # ACh boosts precision
        # ach=0 → 0.5x precision
        # ach=1 → 1.5x precision
        modulation_factor = 0.5 + (ach_level * 1.0)

        precision_boost = self.sequencing_precision * modulation_factor

        # Clamp to [0, 1]
        precision_boost = max(0.0, min(1.0, precision_boost))

        return precision_boost

    def compute_plan_quality(self, plan: Dict) -> float:
        """
        Evaluate plan quality

        Parameters:
        -----------
        plan : Dict
            Plan to evaluate

        Returns:
        --------
        quality : float
            Quality score (0-1)
        """
        # Simplified quality scoring
        num_steps = plan.get("total_steps", 0)

        # Good plans have 3-8 steps
        if 3 <= num_steps <= 8:
            quality = 0.8
        elif num_steps < 3:
            quality = 0.5  # Too simple
        else:
            quality = 0.6  # Too complex

        return quality

    def process_event(self, goal: str, constraints: Dict) -> Dict:
        """
        Main processing: create plan, evaluate

        Parameters:
        -----------
        goal : str
            High-level goal
        constraints : Dict
            Planning constraints

        Returns:
        --------
        result : Dict
            {
                "plan": Dict,
                "quality": float,
                "estimated_duration": float,
                "fits_in_working_memory": bool
            }
        """
        # 1. Create plan
        plan = self.create_plan(goal=goal, constraints=constraints)

        # 2. Evaluate quality
        quality = self.compute_plan_quality(plan)

        # 3. Estimate duration
        duration = self.estimate_duration(plan)

        # 4. Check if fits in working memory (7±2 items)
        fits_in_wm = plan.get("total_steps", 0) <= 9

        # 5. Return complete result
        return {
            "plan": plan,
            "quality": float(quality),
            "estimated_duration": float(duration),
            "fits_in_working_memory": bool(fits_in_wm)
        }

    def get_state(self) -> Dict:
        """
        Get current planning system state

        Returns:
        --------
        state : Dict
            {
                "capacity": float,
                "active_plan": Dict or None,
                "total_plans_created": int,
                "successful_plans": int,
                "replanning_count": int,
                "success_rate": float
            }
        """
        # Success rate
        success_rate = (
            self.successful_plans / max(1, self.total_plans_created)
        )

        return {
            "capacity": float(self.current_capacity),
            "active_plan": self.active_plan,
            "total_plans_created": int(self.total_plans_created),
            "successful_plans": int(self.successful_plans),
            "replanning_count": int(self.replanning_count),
            "success_rate": float(success_rate)
        }
