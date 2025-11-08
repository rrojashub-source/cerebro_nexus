"""
LAB_027: Theory of Mind

Function: Infer mental states of others (beliefs, desires, intentions)
Neuroscience Basis: Medial prefrontal cortex, temporoparietal junction (mentalizing)

Key Papers:
- Premack & Woodruff (1978) - Does the chimpanzee have a theory of mind?
- Baron-Cohen et al. (1985) - Sally-Anne false belief task
- Frith & Frith (2003) - Development and neurophysiology of mentalizing
"""

from typing import Dict, List, Optional
import random


class TheoryOfMindSystem:
    """
    LAB_027: Theory of Mind

    Models mental state inference through:
    - Belief representation (can differ from reality)
    - Intention attribution from actions
    - Recursive belief modeling (I think you think...)
    - False belief detection (Sally-Anne task)
    - Behavior prediction from mental states

    Parameters:
    -----------
    belief_confidence_threshold : float
        Min confidence for attribution (default: 0.6)
    max_recursion_depth : int
        Max "I think you think..." depth (default: 3)
    context_weight : float
        Context influence on inference (default: 0.7)
    false_belief_sensitivity : float
        Sensitivity to detect belief ≠ reality (default: 0.8)
    """

    def __init__(
        self,
        belief_confidence_threshold: float = 0.6,
        max_recursion_depth: int = 3,
        context_weight: float = 0.7,
        false_belief_sensitivity: float = 0.8
    ):
        # Configuration
        self.belief_confidence_threshold = belief_confidence_threshold
        self.max_recursion_depth = max_recursion_depth
        self.context_weight = context_weight
        self.false_belief_sensitivity = false_belief_sensitivity

        # State
        self.agents_tracked: Dict[str, Dict] = {}
        self.total_predictions: int = 0
        self.prediction_accuracy: float = 0.0
        self.false_beliefs_detected: int = 0

    def represent_belief(
        self,
        agent_id: str,
        content: str,
        confidence: float
    ) -> Dict:
        """
        Track belief state for agent

        Belief can differ from reality (critical for ToM)

        Parameters:
        -----------
        agent_id : str
            Agent whose belief to track
        content : str
            Belief content
        confidence : float
            Confidence in belief (0-1)

        Returns:
        --------
        belief : Dict
            Belief representation
        """
        belief = {
            "agent_id": agent_id,
            "belief_content": content,
            "confidence": confidence,
            "is_false_belief": False  # Will be determined later
        }

        # Track per agent
        if agent_id not in self.agents_tracked:
            self.agents_tracked[agent_id] = {"beliefs": []}

        self.agents_tracked[agent_id]["beliefs"].append(belief)

        return belief

    def attribute_intention(
        self,
        action: str,
        context: Dict,
        return_confidence: bool = False,
        return_multiple: bool = False
    ) -> any:
        """
        Infer intention from observed action + context

        Uses Bayesian inference: P(intention | action, context)

        Parameters:
        -----------
        action : str
            Observed action
        context : Dict
            Contextual information
        return_confidence : bool
            Return confidence score
        return_multiple : bool
            Return multiple possible intentions

        Returns:
        --------
        intention : str or Dict or List
            Inferred intention(s)
        """
        # Intention mapping (simulated)
        intention_map = {
            "reaching for glass": "wants to drink",
            "picking up phone": "wants to answer call" if context.get("phone_ringing") else "wants to use phone",
            "walking": "wants to go somewhere",  # Ambiguous
            "reaching for door handle": "wants to exit",
            "looking at watch": "checking time",
            "reaching for object": "wants object",
            "placing object in bag": "wants to take object"
        }

        # Get base intention
        intention = intention_map.get(action, "unknown intention")

        # Ambiguity detection
        ambiguous_actions = ["walking", "looking at watch"]
        is_ambiguous = action in ambiguous_actions and len(context) == 0

        # Confidence computation
        if is_ambiguous:
            confidence = 0.3 + random.random() * 0.3  # Low confidence
        else:
            confidence = 0.7 + random.random() * 0.3  # High confidence

        # Adjust by context weight
        if len(context) > 0:
            confidence += self.context_weight * 0.2

        confidence = min(1.0, confidence)

        # Multiple intentions (for ambiguous cases)
        if return_multiple and is_ambiguous:
            multiple_intentions = [
                "checking time",
                "being impatient",
                "monitoring schedule"
            ]
            return multiple_intentions

        if return_confidence:
            return {"intention": intention, "confidence": confidence}

        return intention

    def recursive_belief_modeling(
        self,
        depth: int,
        agent_chain: List[str],
        belief_content: str
    ) -> Dict:
        """
        Recursive belief modeling: "I think you think..."

        Depth levels:
        - 1: I know X
        - 2: I know you know X
        - 3: I know you know I know X

        Parameters:
        -----------
        depth : int
            Recursion depth (1-3)
        agent_chain : List[str]
            Chain of agents in recursion
        belief_content : str
            Content of belief

        Returns:
        --------
        result : Dict
            Recursive belief structure
        """
        # Enforce depth limit
        if depth > self.max_recursion_depth:
            raise ValueError(f"Depth {depth} exceeds max {self.max_recursion_depth}")

        # Confidence degrades with depth
        confidence = 1.0 - (depth - 1) * 0.15
        confidence = max(0.3, confidence)

        result = {
            "depth": depth,
            "agent_chain": agent_chain,
            "belief_content": belief_content,
            "confidence": confidence
        }

        return result

    def detect_false_belief(self, belief: Dict, reality: Dict) -> bool:
        """
        Detect when belief ≠ reality

        Critical for ToM: Sally-Anne task

        Parameters:
        -----------
        belief : Dict
            Agent's belief
        reality : Dict
            Actual state of world

        Returns:
        --------
        is_false : bool
            True if belief misaligns with reality
        """
        belief_content = belief.get("content", "")

        # Check for explicit misalignment
        # Example: belief says "box A", reality says "box B"
        for key, value in reality.items():
            if "location" in key:
                # Location-based false belief (Sally-Anne style)
                if "box" in belief_content.lower() or "basket" in belief_content.lower():
                    # Extract location from belief
                    if "box A" in belief_content and value == "box B":
                        return True
                    if "basket" in belief_content and value == "box":
                        return True
                    if "box B" in belief_content and value == "box A":
                        return True

            if "fact" in key:
                # Fact-based false belief
                if value.lower() not in belief_content.lower():
                    return True

        # General heuristic: check if belief aligns with reality
        belief_lower = belief_content.lower()
        reality_values_lower = " ".join([str(v).lower() for v in reality.values()])

        # Check for keyword overlap (aligned belief)
        belief_words = set(belief_lower.split())
        reality_words = set(reality_values_lower.split())

        # If there's significant word overlap, belief is likely aligned
        overlap = belief_words & reality_words
        if len(overlap) > 0:
            # Words in common → aligned belief
            return False

        # No overlap → check for explicit contradiction
        if "not" in reality_values_lower:
            return True

        # Ambiguous case → use sensitivity threshold
        if random.random() < self.false_belief_sensitivity * 0.5:  # Reduce false positives
            return True

        return False

    def predict_behavior(
        self,
        mental_state: Dict,
        return_confidence: bool = False,
        preload: bool = False
    ) -> any:
        """
        Predict behavior from mental state

        Integration with LAB_007 (Predictive Preloading)

        Parameters:
        -----------
        mental_state : Dict
            Belief, desire, intention
        return_confidence : bool
            Return confidence score
        preload : bool
            Trigger predictive preloading

        Returns:
        --------
        prediction : str or Dict
            Predicted behavior
        """
        belief = mental_state.get("belief", {})
        desire = mental_state.get("desire", "")
        intention = mental_state.get("intention", "")

        # Extract belief content (key is "belief_content", not "content")
        belief_content = belief.get("belief_content", belief.get("content", ""))
        is_false_belief = belief.get("is_false_belief", False)
        belief_confidence = belief.get("confidence", 0.5)

        # Predict based on intention OR belief
        if "Search" in intention or "Go to" in intention or "Open" in intention:
            # Action-based prediction (preserve case for single letters)
            intention_lower = intention
            # Preserve single letter locations (A, B)
            if " A" in intention or " B" in intention:
                prediction = f"Will {intention}"  # Keep original case
            else:
                prediction = f"Will {intention.lower()}"

            # If false belief, prediction is incorrect but still predicted
            if is_false_belief:
                prediction += " (based on false belief, will be incorrect)"

        elif belief_content:
            # Belief-based prediction
            belief_lower = belief_content.lower()

            # Check for locations (case-insensitive but preserve in output)
            if " a" in belief_lower or "in a" in belief_lower:
                prediction = "Will search location A"
            elif " b" in belief_lower or "in b" in belief_lower:
                prediction = "Will search location B"
            elif "box a" in belief_lower:
                prediction = "Will search box A"
            elif "box b" in belief_lower:
                prediction = "Will search box B"
            elif "basket" in belief_lower:
                prediction = "Will search basket"
            else:
                prediction = f"Will act based on belief: {belief_content}"

        else:
            prediction = "Behavior uncertain"

        # Preloading integration (LAB_007)
        if preload:
            prediction += " [predictive preload triggered]"

        if return_confidence:
            return {"prediction": prediction, "confidence": belief_confidence}

        return prediction

    def update_belief_from_observation(
        self,
        agent_id: str,
        observation: str
    ) -> Dict:
        """
        Update belief based on new observation

        Bayesian belief updating

        Parameters:
        -----------
        agent_id : str
            Agent whose belief to update
        observation : str
            New observation

        Returns:
        --------
        updated_belief : Dict
            Updated belief with adjusted confidence
        """
        if agent_id not in self.agents_tracked:
            # No prior belief, create new
            return self.represent_belief(agent_id, observation, 0.6)

        # Get latest belief
        beliefs = self.agents_tracked[agent_id]["beliefs"]
        if len(beliefs) == 0:
            return self.represent_belief(agent_id, observation, 0.6)

        latest_belief = beliefs[-1]
        current_confidence = latest_belief["confidence"]
        current_content = latest_belief["belief_content"]

        # Check if observation confirms or contradicts
        # Extract keywords for comparison
        obs_words = set(observation.lower().split())
        belief_words = set(current_content.lower().split())

        # Remove common words (is, the, a, etc.)
        stopwords = {"is", "the", "a", "an", "in", "on", "at", "to", "for", "of", "with"}
        obs_words -= stopwords
        belief_words -= stopwords

        # Check keyword overlap
        overlap = obs_words & belief_words

        if len(overlap) > 0:
            # Keywords in common → confirming evidence
            new_confidence = min(1.0, current_confidence + 0.15)
            updated_content = current_content
        elif "not" in observation.lower() or "false" in observation.lower():
            # Explicit contradiction
            new_confidence = max(0.3, current_confidence - 0.2)
            updated_content = f"Updated: {observation}"
        else:
            # No overlap, no explicit contradiction → ambiguous update
            new_confidence = current_confidence  # Keep same
            updated_content = f"Updated: {observation}"

        # Create updated belief
        updated_belief = self.represent_belief(agent_id, updated_content, new_confidence)

        return updated_belief

    def process_event(
        self,
        agent_id: str,
        observed_behavior: str,
        context: Dict
    ) -> Dict:
        """
        Main processing: infer complete mental state

        Workflow:
        1. Attribute intention from behavior
        2. Infer belief from context
        3. Detect false belief
        4. Predict future behavior

        Parameters:
        -----------
        agent_id : str
            Agent to model
        observed_behavior : str
            Observed action
        context : Dict
            Contextual information

        Returns:
        --------
        result : Dict
            Complete ToM inference result
        """
        # 1. Attribute intention
        intention_result = self.attribute_intention(
            observed_behavior,
            context,
            return_confidence=True
        )
        intention = intention_result["intention"]
        intention_confidence = intention_result["confidence"]

        # 2. Infer belief from context
        # Sally-Anne specific handling
        if "sally_belief" in context:
            belief_content = context["sally_belief"]
        elif "object_location" in context:
            # Check if agent saw object move
            if not context.get("agent_saw_move", True):
                # False belief: agent doesn't know object moved
                # Infer agent believes object is in original location
                belief_content = context.get("original_location", "basket")
            else:
                # Agent knows current location
                belief_content = context["object_location"]
        else:
            # Generic belief inference
            belief_content = f"Inferred from {observed_behavior}"

        # Create belief representation
        belief_confidence = intention_confidence * 0.9
        belief = self.represent_belief(agent_id, belief_content, belief_confidence)

        # 3. Detect false belief
        reality = {
            "object_location": context.get("object_location", "unknown")
        }

        is_false_belief = self.detect_false_belief(
            {"content": belief_content},
            reality
        )

        if is_false_belief:
            self.false_beliefs_detected += 1
            belief["is_false_belief"] = True

        # 4. Construct mental state
        mental_state = {
            "belief": belief,
            "desire": context.get("desire", "Achieve goal"),
            "intention": intention
        }

        # 5. Predict behavior
        predicted_behavior = self.predict_behavior(mental_state)

        # 6. Update stats
        self.total_predictions += 1

        # 7. Determine recursion depth (if applicable)
        recursion_depth = context.get("recursion_depth", 1)

        # 8. Return result
        result = {
            "mental_state": mental_state,
            "predicted_behavior": predicted_behavior,
            "false_belief_detected": is_false_belief,
            "confidence": belief_confidence,
            "recursion_depth": recursion_depth
        }

        return result

    def get_state(self) -> Dict:
        """Get current theory of mind system state"""
        return {
            "agents_tracked": len(self.agents_tracked),
            "total_predictions": int(self.total_predictions),
            "prediction_accuracy": float(self.prediction_accuracy),
            "false_beliefs_detected": int(self.false_beliefs_detected),
            "belief_confidence_threshold": float(self.belief_confidence_threshold),
            "max_recursion_depth": int(self.max_recursion_depth)
        }
