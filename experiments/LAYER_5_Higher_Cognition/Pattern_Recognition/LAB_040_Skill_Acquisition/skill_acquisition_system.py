"""
LAB_040: Skill Acquisition System

Function: Learning curves, performance improvement, expertise
Neuroscience Basis: Cerebellum (motor coordination), Motor cortex (skill execution), Basal ganglia (proceduralization)

Key Papers:
- Newell & Rosenbloom (1981) - Mechanisms of skill acquisition and the law of practice
- Ericsson et al. (1993) - The role of deliberate practice in the acquisition of expert performance

Skill Acquisition Model:
- Power Law of Practice: Time = A + B * N^(-α)
- Deliberate practice: High feedback quality → faster learning
- Plateau detection: Performance stops improving
- Transfer learning: Near transfer (high similarity) vs far transfer (low similarity)
- Integration with LAB_038 (Meta-Learning), LAB_039 (Habit Formation), LAB_041 (Transfer Learning)
"""

from typing import Dict, List, Optional
import math


class SkillAcquisitionSystem:
    """
    LAB_040: Skill Acquisition System

    Models skill learning through:
    - Power Law of Practice (Newell & Rosenbloom 1981): Time = A + B * N^(-α)
    - Deliberate practice quality modulation (Ericsson 1993)
    - Plateau detection (performance stops improving)
    - Near/far transfer between related skills
    - Integration with LAB_038 (Meta-Learning), LAB_039 (Habit Formation)

    Integration:
    - ← LAB_038 (Meta-Learning) - Optimizes learning rate
    - → LAB_039 (Habit Formation) - Skilled actions become habitual
    - → LAB_041 (Transfer Learning) - Transfer between skills
    - → LAB_050 (Structural Plasticity) - Long-term skill drives structural changes

    Parameters:
    -----------
    learning_rate_base : float
        Base learning rate (default: 0.1)
    """

    def __init__(
        self,
        learning_rate_base: float = 0.1
    ):
        # Configuration
        self.learning_rate_base = learning_rate_base

        # Skills registry: skill_name → skill_data
        self.skills: Dict[str, Dict] = {}

        # Practice history
        self.practice_history: List[Dict] = []

    def practice_skill(
        self,
        skill_name: str,
        trial_number: int,
        feedback_quality: float,
        complexity: float = 0.5,
        meta_learning_signal: Optional[float] = None
    ) -> Dict:
        """
        Practice skill and update learning curve

        Power Law of Practice (Newell & Rosenbloom 1981):
        Time(N) = A + B * N^(-α)

        Where:
        - N = trial number
        - A = asymptote (expert minimum time)
        - B = initial cost (novice time - A)
        - α = learning rate exponent

        Parameters:
        -----------
        skill_name : str
            Name of skill being practiced
        trial_number : int
            Trial/practice session number (1, 2, 3, ...)
        feedback_quality : float
            Quality of feedback received (0-1)
            High quality (0.8-1.0) = deliberate practice
            Low quality (0.0-0.3) = mindless repetition
        complexity : float, optional
            Skill complexity (0-1, default: 0.5)
            Affects plateau duration
        meta_learning_signal : float, optional
            Meta-learning optimization from LAB_038 (0-1)
            Amplifies learning rate

        Returns:
        --------
        result : Dict
            Practice result with performance_time, skill_level, learning_rate
        """
        # Get or create skill
        if skill_name not in self.skills:
            self.skills[skill_name] = {
                "name": skill_name,
                "skill_level": 0.0,
                "trials": 0,
                "total_practice": 0,
                "complexity": complexity,
                "performance_history": [],
                "plateau_window": []
            }

        skill = self.skills[skill_name]
        skill["trials"] = trial_number
        skill["total_practice"] += 1
        skill["complexity"] = complexity

        # Compute effective learning rate (modulated by feedback quality and meta-learning)
        # Base alpha for Power Law (Newell & Rosenbloom 1981: typical α = 0.3-0.5)
        # Use 0.5 as base (upper bound for strong convergence)
        alpha_base = 0.5

        # Feedback quality modulation (Ericsson 1993)
        # High feedback (0.8-1.0) → faster learning (higher alpha)
        # Low feedback (0.0-0.3) → slower learning (lower alpha)
        # Range: 0.15 to 1.4 (allows alpha > 0.5 for high feedback, but low feedback stays <0.2)
        feedback_factor = 0.15 + (feedback_quality * 1.25)
        alpha = alpha_base * feedback_factor

        # Meta-learning signal modulation (LAB_038 integration)
        if meta_learning_signal is not None:
            # Meta-learning amplifies learning rate
            # meta = 0.9 → 1.9x amplification
            meta_factor = 1.0 + meta_learning_signal
            alpha *= meta_factor

        # Effective learning rate for output
        effective_learning_rate = alpha

        # Power Law of Practice: Time = A + B * N^(-α)
        # A = asymptote (expert minimum time) = 1.0
        # B = initial cost (novice time - A) = 10.0
        # α = learning rate exponent (0.3-0.5 typical)
        A = 1.0  # Expert asymptote
        B = 10.0  # Novice starting point

        # Compute performance time for this trial
        performance_time = A + B * (trial_number ** (-alpha))

        # Convert time to skill level (inverse relationship)
        # Lower time → higher skill
        # Skill approaches 1.0 as time approaches A (expert asymptote)
        max_time = A + B  # Trial 1 time (11.0)
        # Normalize: skill = (max_time - time) / (max_time - A)
        # When time = A → skill = 1.0
        # When time = max_time → skill = 0.0
        skill_level = (max_time - performance_time) / (max_time - A)
        skill_level = max(0.0, min(1.0, skill_level))  # Clamp 0-1

        # Update skill level
        skill["skill_level"] = skill_level

        # Track performance history for plateau detection
        skill["performance_history"].append({
            "trial": trial_number,
            "performance_time": performance_time,
            "skill_level": skill_level
        })

        # Maintain plateau detection window (last 10 trials)
        skill["plateau_window"].append(skill_level)
        if len(skill["plateau_window"]) > 10:
            skill["plateau_window"].pop(0)

        # Store in practice history
        self.practice_history.append({
            "skill_name": skill_name,
            "trial_number": trial_number,
            "performance_time": performance_time,
            "skill_level": skill_level,
            "feedback_quality": feedback_quality
        })

        return {
            "skill_updated": True,
            "performance_time": float(performance_time),
            "skill_level": float(skill_level),
            "learning_rate": float(effective_learning_rate)
        }

    def get_skill_level(
        self,
        skill_name: str
    ) -> float:
        """
        Get current skill level

        Parameters:
        -----------
        skill_name : str
            Name of skill

        Returns:
        --------
        skill_level : float
            Current skill level (0-1)
        """
        if skill_name not in self.skills:
            return 0.0

        return float(self.skills[skill_name]["skill_level"])

    def detect_plateau(
        self,
        skill_name: str
    ) -> Dict:
        """
        Detect if skill has plateaued (performance stops improving)

        Plateau criteria:
        - Last 5+ trials show improvement < 0.01
        - Complexity affects plateau likelihood

        Parameters:
        -----------
        skill_name : str
            Name of skill

        Returns:
        --------
        result : Dict
            plateau_detected (bool)
        """
        if skill_name not in self.skills:
            return {"plateau_detected": False, "reason": "Skill not found"}

        skill = self.skills[skill_name]
        plateau_window = skill["plateau_window"]

        # Need at least 5 trials to detect plateau
        if len(plateau_window) < 5:
            return {"plateau_detected": False, "reason": "Insufficient data"}

        # Compute improvement over last 5 trials
        recent_levels = plateau_window[-5:]
        improvement = recent_levels[-1] - recent_levels[0]

        # Plateau threshold (affected by complexity)
        # Complex skills plateau more easily
        complexity = skill["complexity"]
        plateau_threshold = 0.01 * (1.0 + complexity)  # 0.01 to 0.02

        # Detect plateau
        plateau_detected = improvement < plateau_threshold

        return {
            "plateau_detected": plateau_detected,
            "improvement": float(improvement),
            "threshold": float(plateau_threshold),
            "complexity": float(complexity)
        }

    def compute_transfer(
        self,
        source_skill: str,
        target_skill: str,
        similarity: float,
        interference: bool = False
    ) -> Dict:
        """
        Compute transfer learning between skills

        Near transfer: High similarity (0.7-1.0) → significant transfer
        Far transfer: Low similarity (0.0-0.3) → minimal transfer
        Negative transfer: Interference=True → performance worse than baseline

        Parameters:
        -----------
        source_skill : str
            Source skill (trained)
        target_skill : str
            Target skill (new)
        similarity : float
            Similarity between skills (0-1)
        interference : bool
            If True, source skill interferes (negative transfer)

        Returns:
        --------
        result : Dict
            transfer_applicable (bool), transfer_amount (float), negative_transfer (bool)
        """
        # Get source skill level
        if source_skill not in self.skills:
            return {
                "transfer_applicable": False,
                "transfer_amount": 0.0,
                "negative_transfer": False,
                "reason": "Source skill not found"
            }

        source_level = self.skills[source_skill]["skill_level"]

        # Compute transfer amount
        # Transfer = source_skill_level * similarity
        # Higher source skill + higher similarity → better transfer
        transfer_amount = source_level * similarity

        # Near transfer threshold: similarity > 0.6
        near_transfer = similarity > 0.6
        transfer_applicable = near_transfer

        # Negative transfer (interference)
        negative_transfer = False
        if interference:
            # Source skill interferes with target
            # Reduces transfer by 50%
            transfer_amount *= -0.5
            negative_transfer = True
            transfer_applicable = False  # Not beneficial

        # Far transfer: similarity < 0.3 → minimal transfer
        if similarity < 0.3 and not interference:
            transfer_applicable = False

        return {
            "transfer_applicable": transfer_applicable,
            "transfer_amount": float(transfer_amount),
            "negative_transfer": negative_transfer,
            "source_skill_level": float(source_level),
            "similarity": float(similarity)
        }

    def process_event(
        self,
        event_type: str,
        **kwargs
    ) -> Dict:
        """
        Main processing: handle skill-related events

        Event types:
        - practice: Practice skill and update learning curve
        - transfer: Compute transfer between skills

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
        if event_type == "practice":
            skill_name = kwargs.get("skill_name", "unknown")
            trial_number = kwargs.get("trial_number", 1)
            feedback_quality = kwargs.get("feedback_quality", 0.5)
            complexity = kwargs.get("complexity", 0.5)
            meta_learning_signal = kwargs.get("meta_learning_signal", None)

            result = self.practice_skill(
                skill_name, trial_number, feedback_quality, complexity, meta_learning_signal
            )

            return result

        elif event_type == "transfer":
            source_skill = kwargs.get("source_skill", "unknown")
            target_skill = kwargs.get("target_skill", "unknown")
            similarity = kwargs.get("similarity", 0.5)
            interference = kwargs.get("interference", False)

            result = self.compute_transfer(
                source_skill, target_skill, similarity, interference
            )

            return result

        else:
            return {"error": f"Unknown event type: {event_type}"}

    def get_state(self) -> Dict:
        """Get current skill system state"""
        if len(self.skills) == 0:
            highest_skill = None
            avg_skill_level = 0.0
        else:
            highest = max(self.skills.items(), key=lambda x: x[1]["skill_level"])
            highest_skill = {
                "name": highest[0],
                "skill_level": highest[1]["skill_level"]
            }
            avg_skill_level = sum(s["skill_level"] for s in self.skills.values()) / len(self.skills)

        return {
            "total_skills": len(self.skills),
            "highest_skill": highest_skill,
            "average_skill_level": float(avg_skill_level),
            "learning_rate_base": float(self.learning_rate_base),
            "practice_history_size": len(self.practice_history)
        }
