"""
LAB_028: Empathy Simulation

Function: Affective empathy, emotional resonance, compassion
Neuroscience Basis: Anterior insula, anterior cingulate cortex (emotional mirroring)

Key Papers:
- Decety & Jackson (2004) - The functional architecture of human empathy
- Singer & Lamm (2009) - The social neuroscience of empathy
- Batson (2011) - Altruism in humans
"""

from typing import Dict, Optional


class EmpathySystem:
    """
    LAB_028: Empathy Simulation

    Models empathic cognition through:
    - Emotional mirroring (LAB_008)
    - Self/other boundary maintenance
    - Compassionate response generation (LAB_013)
    - Empathic distress regulation (LAB_014)
    - Empathy type distinction (cognitive/affective/compassionate)

    Parameters:
    -----------
    mirroring_intensity : float
        How strongly to mirror emotions (default: 0.7)
    self_other_boundary_strength : float
        Prevent emotional contagion (default: 0.8)
    compassion_threshold : float
        Threshold for prosocial action (default: 0.6)
    distress_tolerance : float
        Max vicarious suffering before regulation (default: 0.7)
    """

    def __init__(
        self,
        mirroring_intensity: float = 0.7,
        self_other_boundary_strength: float = 0.8,
        compassion_threshold: float = 0.6,
        distress_tolerance: float = 0.7
    ):
        # Configuration
        self.mirroring_intensity = mirroring_intensity
        self.self_other_boundary_strength = self_other_boundary_strength
        self.compassion_threshold = compassion_threshold
        self.distress_tolerance = distress_tolerance

        # State
        self.total_empathic_events: int = 0
        self.prosocial_actions_triggered: int = 0
        self.avg_empathic_accuracy: float = 0.0
        self.distress_regulation_count: int = 0

    def mirror_emotion(self, observed_emotion: Dict) -> Dict:
        """
        Simulate other's emotion internally

        Integration with LAB_008 (Emotional Contagion)
        Formula: empathic_emotion = observed * mirroring_intensity

        Parameters:
        -----------
        observed_emotion : Dict
            Observed emotion with type and intensity

        Returns:
        --------
        mirrored : Dict
            Empathic emotion (scaled by mirroring intensity)
        """
        emotion_type = observed_emotion.get("type", "neutral")
        intensity = observed_emotion.get("intensity", 0.5)

        # Apply mirroring intensity
        mirrored_intensity = intensity * self.mirroring_intensity

        mirrored = {
            "type": emotion_type,
            "intensity": mirrored_intensity
        }

        # Handle mixed emotions
        if "emotions" in observed_emotion:
            mirrored["emotions"] = [
                (emo, intens * self.mirroring_intensity)
                for (emo, intens) in observed_emotion["emotions"]
            ]

        return mirrored

    def maintain_self_other_boundary(self, emotion: Dict) -> Dict:
        """
        Distinguish "their pain" from "my pain"

        Critical for preventing emotional overwhelm
        Adds "source" tag to emotion

        Parameters:
        -----------
        emotion : Dict
            Empathic emotion to tag

        Returns:
        --------
        tagged : Dict
            Emotion with source tag ("self" or "other")
        """
        tagged = emotion.copy()

        # Tag as "other" (empathic emotion, not self-generated)
        tagged["source"] = "other"

        # Boundary strength modulates intensity
        # High boundary = clear distinction (may reduce intensity slightly)
        # Low boundary = blurred distinction (higher susceptibility)
        if self.self_other_boundary_strength > 0.8:
            # Strong boundary: Slightly reduce intensity to maintain distinction
            tagged["intensity"] = emotion["intensity"] * 0.95
        elif self.self_other_boundary_strength < 0.3:
            # Weak boundary: Emotion feels more like "mine"
            tagged["intensity"] = emotion["intensity"] * 1.1  # Slightly amplified
            tagged["boundary_strength"] = "weak"

        return tagged

    def generate_compassionate_response(
        self,
        empathic_emotion: Dict,
        return_reward: bool = False
    ) -> any:
        """
        Generate prosocial motivation and action

        Integration with LAB_013 (Dopamine - prosocial reward)

        Parameters:
        -----------
        empathic_emotion : Dict
            Empathic emotion to respond to
        return_reward : bool
            Return dopamine reward signal

        Returns:
        --------
        response : str or Dict
            Compassionate action or None
        """
        intensity = empathic_emotion.get("intensity", 0.0)
        emotion_type = empathic_emotion.get("type", "neutral")

        # Check if above compassion threshold
        if intensity < self.compassion_threshold:
            return "no_action" if not return_reward else None

        # Select prosocial action based on emotion type
        response_map = {
            "sadness": "comfort",
            "distress": "offer_help",
            "pain": "offer_help",
            "fear": "comfort",
            "anxiety": "emotional_support",
            "anger": "advocacy"
        }

        action = response_map.get(emotion_type, "emotional_support")

        # Update state
        self.prosocial_actions_triggered += 1

        if return_reward:
            # Dopamine reward for prosocial action (LAB_013)
            return {
                "action": action,
                "dopamine_reward": 0.6 + intensity * 0.3,
                "reward": True
            }

        return action

    def regulate_empathic_distress(
        self,
        distress_level: float,
        serotonin_level: Optional[float] = None
    ) -> float:
        """
        Prevent empathic burnout

        Integration with LAB_014 (Serotonin - emotion regulation)
        If distress > tolerance → reduce mirroring

        Parameters:
        -----------
        distress_level : float
            Current empathic distress (0-1)
        serotonin_level : float, optional
            Serotonin level for modulation

        Returns:
        --------
        regulated_distress : float
            Regulated distress level
        """
        # Check if above tolerance
        if distress_level <= self.distress_tolerance:
            return distress_level

        # Distress above tolerance → regulate
        self.distress_regulation_count += 1

        # Regulation strength
        regulation_strength = 0.3

        # Modulate by serotonin if provided (LAB_014)
        if serotonin_level is not None:
            # Higher serotonin = better regulation
            regulation_strength += serotonin_level * 0.2

        # Apply regulation
        regulated = distress_level * (1.0 - regulation_strength)

        # Ensure within bounds
        regulated = max(0.0, min(1.0, regulated))

        return regulated

    def distinguish_empathy_types(self, situation: Dict) -> str:
        """
        Distinguish empathy types

        Types:
        - Cognitive empathy: Understand what they feel (LAB_027 ToM)
        - Affective empathy: Feel what they feel (this LAB)
        - Compassionate empathy: Motivated to help (cognitive + affective + prosocial)

        Parameters:
        -----------
        situation : Dict
            Situation requiring empathy

        Returns:
        --------
        empathy_type : str
            Type of empathy required
        """
        situation_type = situation.get("type", "affective")
        requires = situation.get("requires", "")

        # Determine type based on requirements
        if "understanding" in requires or "mental_state" in requires:
            return "cognitive"
        elif "helping" in requires or "motivation" in requires:
            return "compassionate"
        elif "feeling" in requires or "resonance" in requires:
            return "affective"
        else:
            # Default to situation type
            return situation_type

    def compute_empathic_accuracy(self, mirrored: Dict, actual: Dict) -> float:
        """
        Measure how well mirroring matches actual emotion

        Parameters:
        -----------
        mirrored : Dict
            Empathic emotion (mirrored)
        actual : Dict
            Actual emotion of other person

        Returns:
        --------
        accuracy : float
            Empathic accuracy (0-1)
        """
        # Type match
        type_match = 1.0 if mirrored["type"] == actual["type"] else 0.0

        # Intensity match
        intensity_diff = abs(mirrored["intensity"] - actual["intensity"])
        intensity_accuracy = 1.0 - intensity_diff

        # Combined accuracy
        accuracy = (type_match * 0.7) + (intensity_accuracy * 0.3)

        return max(0.0, min(1.0, accuracy))

    def process_event(
        self,
        observed_emotion: Dict,
        agent_id: str
    ) -> Dict:
        """
        Main processing: complete empathy cycle

        Workflow:
        1. Mirror observed emotion
        2. Maintain self/other boundary
        3. Compute empathic distress
        4. Regulate if necessary
        5. Generate compassionate response

        Parameters:
        -----------
        observed_emotion : Dict
            Observed emotion with type and intensity
        agent_id : str
            Agent being empathized with

        Returns:
        --------
        result : Dict
            Complete empathy processing result
        """
        # 1. Mirror emotion (LAB_008)
        empathic_emotion = self.mirror_emotion(observed_emotion)

        # 2. Maintain self/other boundary
        bounded_emotion = self.maintain_self_other_boundary(empathic_emotion)

        # 3. Compute empathic distress
        distress_level = bounded_emotion["intensity"]
        if bounded_emotion["type"] in ["distress", "pain", "suffering"]:
            distress_level *= 1.2  # Amplify for distressing emotions

        # 4. Regulate empathic distress if necessary
        regulation_active = False
        if distress_level > self.distress_tolerance:
            distress_level = self.regulate_empathic_distress(distress_level)
            regulation_active = True

        # 5. Generate compassionate response
        prosocial_motivation = distress_level if distress_level > self.compassion_threshold else 0.0
        compassionate_action = None

        if prosocial_motivation > 0:
            compassionate_action = self.generate_compassionate_response(bounded_emotion)

        # 6. Update state
        self.total_empathic_events += 1

        # 7. Construct result
        result = {
            "empathic_emotion": bounded_emotion,
            "self_other_distinction": self.self_other_boundary_strength,
            "prosocial_motivation": prosocial_motivation,
            "empathic_distress_level": distress_level,
            "regulation_active": regulation_active
        }

        if compassionate_action:
            result["compassionate_action"] = compassionate_action

        return result

    def get_state(self) -> Dict:
        """Get current empathy system state"""
        return {
            "total_empathic_events": int(self.total_empathic_events),
            "prosocial_actions_triggered": int(self.prosocial_actions_triggered),
            "avg_empathic_accuracy": float(self.avg_empathic_accuracy),
            "distress_regulation_count": int(self.distress_regulation_count),
            "mirroring_intensity": float(self.mirroring_intensity),
            "self_other_boundary_strength": float(self.self_other_boundary_strength)
        }
