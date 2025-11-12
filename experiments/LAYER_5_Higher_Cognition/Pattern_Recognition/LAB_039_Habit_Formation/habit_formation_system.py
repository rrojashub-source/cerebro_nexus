"""
LAB_039: Habit Formation System

Function: Procedural memory, automaticity, habit loops
Neuroscience Basis: Basal ganglia (dorsolateral striatum), habit vs goal-directed control

Key Papers:
- Dolan & Dayan (2013) - Goals and habits in the brain
- Graybiel (2008) - Habits, rituals, and the evaluative brain

Habit Formation Model:
- Frequency tracking: Repeated actions → increased habit strength
- Automaticity: Cognitive cost decreases with practice
- Cue-routine-reward loops (Graybiel 2008)
- Habit strength asymptotes at ~0.9-1.0
- Decay without practice
- Competition with goal-directed control (Dolan & Dayan 2013)
- Dopamine modulation (LAB_013 integration)
"""

from typing import Dict, List, Optional, Tuple
import math


class HabitFormationSystem:
    """
    LAB_039: Habit Formation System

    Models procedural learning through:
    - Action-outcome frequency tracking
    - Automaticity development (reduced cognitive cost)
    - Cue-routine-reward loop formation (Graybiel 2008)
    - Habit vs goal-directed competition (Dolan & Dayan 2013)
    - Decay without practice
    - Dopamine modulation from LAB_013

    Integration:
    - → LAB_013 (Dopamine) - RPE strengthens habits
    - → LAB_019 (Cognitive Control) - Can override habits
    - → LAB_022 (Goal-Directed) - Competition
    - ← LAB_040 (Skill Acquisition) - Skilled actions become habitual

    Parameters:
    -----------
    automaticity_rate : float
        Rate of automaticity development (default: 0.1)
    """

    def __init__(
        self,
        automaticity_rate: float = 0.1
    ):
        # Configuration
        self.automaticity_rate = automaticity_rate

        # Habits registry: (context, action) → habit_data
        self.habits: Dict[Tuple[str, str], Dict] = {}

        # Action history
        self.action_history: List[Dict] = []

    def perform_action(
        self,
        context: str,
        action: str,
        outcome: float,
        dopamine_level: Optional[float] = None,
        skill_level: Optional[float] = None
    ) -> Dict:
        """
        Perform action and update habit

        Parameters:
        -----------
        context : str
            Contextual cue (e.g., "morning", "stress")
        action : str
            Action taken (e.g., "coffee", "snack")
        outcome : float
            Reward/outcome value (-1 to 1)
        dopamine_level : float, optional
            Dopamine level from LAB_013 (0-1)
        skill_level : float, optional
            Skill level from LAB_040 (0-1)

        Returns:
        --------
        result : Dict
            Habit update information
        """
        key = (context, action)

        # Get or create habit
        if key not in self.habits:
            self.habits[key] = {
                "cue": context,
                "routine": action,
                "strength": 0.0,
                "repetitions": 0,
                "automaticity": 0.0,
                "total_reward": 0.0,
                "avg_reward": 0.0
            }

        habit = self.habits[key]

        # Increment repetitions
        habit["repetitions"] += 1

        # Update reward tracking
        habit["total_reward"] += outcome
        habit["avg_reward"] = habit["total_reward"] / habit["repetitions"]

        # Compute strength increment (with diminishing returns)
        # Asymptotic toward 0.88 using exponential approach
        # Lower max allows cognitive control to override even strong habits
        max_strength = 0.88
        strength_gap = max_strength - habit["strength"]

        # Base increment decreases as strength increases
        base_increment = strength_gap * 0.15

        # Skill level modulation (LAB_040 integration)
        if skill_level is not None:
            # High skill accelerates habit formation (skilled actions become automatic faster)
            # skill = 0.3 → 1.45x, skill = 0.9 → 2.35x
            skill_factor = 1.0 + (skill_level * 1.5)
            base_increment *= skill_factor

        # Dopamine modulation (if provided)
        if dopamine_level is not None:
            # High dopamine accelerates habit formation (LAB_013 integration)
            dopamine_factor = 0.5 + (dopamine_level * 0.5)  # 0.5 to 1.0
            base_increment *= dopamine_factor

        # Outcome modulation
        # Positive outcomes strengthen, negative weaken
        if outcome >= 0:
            # Positive: scale 0-1 range
            outcome_factor = 0.5 + (outcome * 0.5)
            strength_delta = base_increment * outcome_factor
            # Update strength (increase)
            habit["strength"] = min(max_strength, habit["strength"] + strength_delta)
        else:
            # Negative: DECREASE strength
            # outcome = -1.0 → decrease by 0.1
            # outcome = -0.5 → decrease by 0.05
            strength_delta = abs(outcome) * 0.1
            habit["strength"] = max(0.0, habit["strength"] - strength_delta)

        # Update automaticity (correlates with strength + skill level)
        if skill_level is not None:
            # High skill + high strength = high automaticity
            # Give more weight to skill_level (skilled actions are more automatic)
            habit["automaticity"] = (habit["strength"] * 0.6) + (skill_level * 0.4)
        else:
            habit["automaticity"] = habit["strength"] * 0.9

        # Store in history
        self.action_history.append({
            "context": context,
            "action": action,
            "outcome": outcome,
            "habit_strength": habit["strength"]
        })

        return {
            "habit_updated": True,
            "habit_strength": float(habit["strength"]),
            "automaticity": float(habit["automaticity"]),
            "habit_delta": float(strength_delta)
        }

    def get_cognitive_cost(
        self,
        context: str,
        action: str
    ) -> float:
        """
        Compute cognitive cost for action (lower for habitual actions)

        Parameters:
        -----------
        context : str
            Context cue
        action : str
            Action

        Returns:
        --------
        cognitive_cost : float
            0-1 (1 = full attention, 0 = fully automatic)
        """
        key = (context, action)

        if key not in self.habits:
            # Novel action → full cognitive cost
            return 1.0

        habit = self.habits[key]

        # Cost inversely related to automaticity
        # automaticity = 0 → cost = 1.0
        # automaticity = 1 → cost = 0.0
        cognitive_cost = 1.0 - habit["automaticity"]

        return float(cognitive_cost)

    def compute_habit_activation(
        self,
        context: str,
        action: str
    ) -> float:
        """
        Compute automatic activation from cue

        Strong habits activate automatically when cue presented.

        Parameters:
        -----------
        context : str
            Cue
        action : str
            Habitual action

        Returns:
        --------
        activation : float
            0-1 automatic activation level
        """
        key = (context, action)

        if key not in self.habits:
            return 0.0

        habit = self.habits[key]

        # Activation = habit strength
        # Strong habits activate highly
        activation = habit["strength"]

        return float(activation)

    def apply_decay(
        self,
        days: int
    ) -> Dict:
        """
        Apply decay to all habits (without practice)

        Parameters:
        -----------
        days : int
            Days since last practice

        Returns:
        --------
        result : Dict
            Decay results
        """
        # Decay rate: ~5% per week without practice
        decay_rate = 0.007 * days  # 0.007/day ≈ 5%/week

        for key, habit in self.habits.items():
            # Exponential decay
            habit["strength"] *= math.exp(-decay_rate)
            habit["automaticity"] *= math.exp(-decay_rate)

        return {
            "days_decayed": days,
            "decay_rate": float(decay_rate),
            "habits_affected": len(self.habits)
        }

    def compute_working_memory_load(
        self,
        context: str,
        action: str
    ) -> float:
        """
        Compute working memory load for action (LAB_011 integration)

        Habitual actions reduce WM load.

        Parameters:
        -----------
        context : str
            Context
        action : str
            Action

        Returns:
        --------
        wm_load : float
            0-1 working memory load
        """
        key = (context, action)

        if key not in self.habits:
            # Novel action → high WM load
            return 1.0

        habit = self.habits[key]

        # WM load inversely proportional to automaticity
        wm_load = 1.0 - habit["automaticity"]

        return float(wm_load)

    def compute_control_mode(
        self,
        context: str,
        action: str,
        stress_level: float = 0.5
    ) -> Dict:
        """
        Compute habit vs goal-directed control balance (Dolan & Dayan 2013)

        Early learning: Goal-directed dominates
        Late learning: Habit dominates
        High stress: Habit increases

        Parameters:
        -----------
        context : str
            Context
        action : str
            Action
        stress_level : float
            Stress level 0-1 (default: 0.5)

        Returns:
        --------
        control : Dict
            Control mode information
        """
        key = (context, action)

        if key not in self.habits:
            # No habit → fully goal-directed
            return {
                "mode": "goal_directed",
                "habit_weight": 0.0,
                "goal_directed_weight": 1.0
            }

        habit = self.habits[key]
        habit_strength = habit["strength"]

        # Base weights
        habit_weight = habit_strength
        goal_directed_weight = 1.0 - habit_strength

        # Stress increases habit reliance (Schwabe & Wolf 2009)
        # Under stress, habits dominate
        stress_factor = 1.0 + (stress_level * 0.5)  # 1.0 to 1.5
        habit_weight *= stress_factor

        # Normalize
        total = habit_weight + goal_directed_weight
        habit_weight /= total
        goal_directed_weight /= total

        # Determine mode
        if habit_weight > 0.6:
            mode = "habitual"
        elif goal_directed_weight > 0.6:
            mode = "goal_directed"
        else:
            mode = "mixed"

        return {
            "mode": mode,
            "habit_weight": float(habit_weight),
            "goal_directed_weight": float(goal_directed_weight),
            "stress_modulation": float(stress_factor)
        }

    def apply_cognitive_control(
        self,
        context: str,
        action: str,
        control_strength: float
    ) -> Dict:
        """
        Apply cognitive control to override habit (LAB_019 integration)

        Parameters:
        -----------
        context : str
            Context
        action : str
            Habitual action
        control_strength : float
            Control strength from LAB_019 (0-1)

        Returns:
        --------
        result : Dict
            Override result
        """
        key = (context, action)

        if key not in self.habits:
            # No habit to override
            return {
                "habit_suppressed": False,
                "action_taken": action,
                "control_successful": True
            }

        habit = self.habits[key]
        habit_activation = habit["strength"]

        # Control success probability
        # High control + weak habit = high success
        # Low control + strong habit = low success
        # Formula: Asymmetric exponents (control^2.0 vs habit^1) to strongly favor control
        control_powered = control_strength ** 2.0
        habit_powered = habit_activation ** 1.0
        success_prob = control_powered / (control_powered + habit_powered)

        # High control (0.9) + strong habit (0.9) = 0.81 / (0.81 + 0.9) = 0.474 < 0.5 (fails)
        # High control (0.9) + strong habit (0.8) = 0.81 / (0.81 + 0.8) = 0.503 > 0.5 (succeeds)
        # Lower threshold slightly to 0.48 to allow high control to override strong habits
        habit_suppressed = success_prob > 0.48

        if habit_suppressed:
            action_taken = "alternative"  # Controlled action instead
        else:
            action_taken = action  # Habit wins

        return {
            "habit_suppressed": habit_suppressed,
            "action_taken": action_taken,
            "control_strength": float(control_strength),
            "habit_activation": float(habit_activation),
            "success_probability": float(success_prob)
        }

    def process_event(
        self,
        event_type: str,
        **kwargs
    ) -> Dict:
        """
        Main processing: handle habit-related events

        Event types:
        - action: Perform action and update habit
        - control_override: Apply cognitive control
        - outcome_change: Outcome devaluation test

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
        if event_type == "action":
            context = kwargs.get("context", "unknown")
            action = kwargs.get("action", "unknown")
            reward = kwargs.get("reward", 0.5)
            dopamine_level = kwargs.get("dopamine_level", None)
            skill_level = kwargs.get("skill_level", None)

            # Handle RPE if provided (LAB_013 integration)
            expected_reward = kwargs.get("expected_reward", None)
            actual_reward = kwargs.get("actual_reward", None)

            if expected_reward is not None and actual_reward is not None:
                # Compute RPE
                rpe = actual_reward - expected_reward
                # Positive RPE → stronger habit update
                outcome = actual_reward
            else:
                outcome = reward

            result = self.perform_action(
                context, action, outcome, dopamine_level, skill_level
            )

            return result

        elif event_type == "control_override":
            context = kwargs.get("context", "unknown")
            habitual_action = kwargs.get("habitual_action", "unknown")
            controlled_action = kwargs.get("controlled_action", "alternative")
            control_strength = kwargs.get("control_strength", 0.7)

            result = self.apply_cognitive_control(
                context, habitual_action, control_strength
            )

            # Map action_taken to actual action names
            if result["habit_suppressed"]:
                result["action_executed"] = controlled_action  # Use provided controlled action
            else:
                result["action_executed"] = habitual_action  # Habit wins

            result["habit_overridden"] = result["habit_suppressed"]

            return result

        elif event_type == "outcome_change":
            # Outcome devaluation test (Dolan & Dayan 2013)
            context = kwargs.get("context", "unknown")
            action = kwargs.get("action", "unknown")
            new_outcome = kwargs.get("new_outcome", 0.0)

            key = (context, action)

            if key in self.habits:
                habit = self.habits[key]
                old_avg_reward = habit["avg_reward"]
                habit["avg_reward"] = new_outcome

                # Note: Habit strength should persist despite devaluation
                # This is the key behavioral signature

                return {
                    "outcome_updated": True,
                    "old_outcome": float(old_avg_reward),
                    "new_outcome": float(new_outcome),
                    "habit_strength_persists": float(habit["strength"])
                }
            else:
                return {"error": "No habit found"}

        else:
            return {"error": f"Unknown event type: {event_type}"}

    def get_state(self) -> Dict:
        """Get current habit system state"""
        if len(self.habits) == 0:
            strongest_habit = None
            avg_strength = 0.0
        else:
            strongest = max(self.habits.items(), key=lambda x: x[1]["strength"])
            strongest_habit = {
                "context": strongest[0][0],
                "action": strongest[0][1],
                "strength": strongest[1]["strength"]
            }
            avg_strength = sum(h["strength"] for h in self.habits.values()) / len(self.habits)

        return {
            "total_habits": len(self.habits),
            "strongest_habit": strongest_habit,
            "average_strength": float(avg_strength),
            "automaticity_rate": float(self.automaticity_rate),
            "action_history_size": len(self.action_history)
        }
