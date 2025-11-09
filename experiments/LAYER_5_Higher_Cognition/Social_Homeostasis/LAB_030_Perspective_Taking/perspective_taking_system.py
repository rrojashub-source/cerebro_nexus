"""
LAB_030: Perspective Taking System

Function: Spatial & conceptual perspective shifts (egocentric ↔ allocentric)
Neuroscience Basis: TPJ, precuneus, retrosplenial cortex

Key Papers:
- Zacks & Michelon (2005) - Spatial perspective taking
- Ruby & Decety (2001) - 1st vs 3rd person perspective
- Kessler & Rutherford (2010) - Two forms of perspective taking
"""

from typing import Dict, List, Optional, Any


class PerspectiveTakingSystem:
    """
    LAB_030: Perspective Taking System

    Models perspective transformation through:
    - Mental rotation of viewpoints (Shepard & Metzler 1971)
    - Egocentric ↔ allocentric frame conversion
    - Conceptual perspective shifts (beliefs, knowledge)
    - 1st person vs 3rd person imagery

    Parameters:
    -----------
    rotation_cost_per_degree : float
        Time cost per degree of mental rotation (default: 0.01s)
    """

    def __init__(self, rotation_cost_per_degree: float = 0.01):
        # Configuration
        self.rotation_cost_per_degree = rotation_cost_per_degree

        # State
        self.total_perspective_shifts: int = 0

    def compute_rotation_cost(self, angle_degrees: float) -> float:
        """
        Mental rotation cost (linear with angle)

        Based on Shepard & Metzler (1971): rotation time increases
        linearly with angle difference.

        Parameters:
        -----------
        angle_degrees : float
            Rotation angle (-180 to 180)

        Returns:
        --------
        cost : float
            Time cost in seconds
        """
        return abs(angle_degrees) * self.rotation_cost_per_degree

    def spatial_perspective(
        self,
        current_frame: str,
        target_frame: str,
        relative_position: Optional[str] = None,
        direction: Optional[str] = None,
        agent_heading: float = 0
    ) -> Dict:
        """
        Transform spatial perspective

        Egocentric frame: "front", "back", "left", "right" (relative to agent)
        Allocentric frame: "north", "south", "east", "west" (absolute)

        Parameters:
        -----------
        current_frame : str
            "egocentric" or "allocentric"
        target_frame : str
            "egocentric" or "allocentric"
        relative_position : str, optional
            Egocentric position (front, back, left, right)
        direction : str, optional
            Allocentric direction (north, south, east, west)
        agent_heading : float
            Agent's heading in degrees (0 = north, 90 = east, 180 = south, 270 = west)

        Returns:
        --------
        result : Dict
            Transformed spatial representation
        """
        result = {"frame": target_frame}

        if current_frame == "egocentric" and target_frame == "allocentric":
            # Egocentric → Allocentric
            # Convert relative position to absolute direction
            ego_to_allo = {
                "front": agent_heading,
                "back": (agent_heading + 180) % 360,
                "left": (agent_heading + 270) % 360,
                "right": (agent_heading + 90) % 360
            }

            if relative_position:
                angle = ego_to_allo.get(relative_position, agent_heading)
                result["direction"] = self._angle_to_cardinal(angle)

        elif current_frame == "allocentric" and target_frame == "egocentric":
            # Allocentric → Egocentric
            # Convert absolute direction to relative position
            cardinal_to_angle = {
                "north": 0,
                "east": 90,
                "south": 180,
                "west": 270
            }

            if direction:
                object_angle = cardinal_to_angle.get(direction, 0)
                relative_angle = (object_angle - agent_heading) % 360

                # Convert to relative position
                if 315 <= relative_angle or relative_angle < 45:
                    result["relative_position"] = "front"
                    result["visible"] = True
                elif 45 <= relative_angle < 135:
                    result["relative_position"] = "right"
                    result["visible"] = True
                elif 135 <= relative_angle < 225:
                    result["relative_position"] = "back"
                    result["visible"] = False  # Behind = not visible
                else:
                    result["relative_position"] = "left"
                    result["visible"] = True

        elif current_frame == "allocentric" and target_frame == "allocentric":
            # No transformation needed
            if direction:
                result["direction"] = direction

        return result

    def _angle_to_cardinal(self, angle: float) -> str:
        """Convert angle to cardinal direction"""
        angle = angle % 360
        if 315 <= angle or angle < 45:
            return "north"
        elif 45 <= angle < 135:
            return "east"
        elif 135 <= angle < 225:
            return "south"
        else:
            return "west"

    def conceptual_perspective(
        self,
        current_belief: Dict,
        target_belief: Dict
    ) -> Dict:
        """
        Shift conceptual perspective (beliefs, knowledge)

        Integration with LAB_027 (Theory of Mind): Represent what
        another person believes or knows.

        Parameters:
        -----------
        current_belief : Dict
            Current perspective (usually self)
        target_belief : Dict
            Target perspective (another person)

        Returns:
        --------
        result : Dict
            Adopted perspective
        """
        # Extract target belief content
        if isinstance(target_belief, dict):
            if "content" in target_belief:
                adopted_belief = target_belief["content"]
            elif "ball_location" in target_belief:
                adopted_belief = target_belief["ball_location"]
            elif "known" in target_belief:
                adopted_belief = target_belief
            else:
                adopted_belief = target_belief
        else:
            adopted_belief = target_belief

        result = {
            "adopted_belief": adopted_belief,
            "perspective_holder": target_belief.get("holder", "other")
        }

        return result

    def imagery_perspective(
        self,
        perspective_type: str,
        scene: str
    ) -> Dict:
        """
        1st person vs 3rd person imagery

        Based on Ruby & Decety (2001): 3rd person perspective
        requires additional processing (rotation).

        Parameters:
        -----------
        perspective_type : str
            "first_person" or "third_person"
        scene : str
            Scene description

        Returns:
        --------
        result : Dict
            Imagery representation with processing cost
        """
        if perspective_type == "first_person":
            # Egocentric viewpoint
            viewpoint = "egocentric"
            processing_cost = 0.1  # Base cost
        else:
            # Allocentric viewpoint (see myself from outside)
            viewpoint = "allocentric"
            processing_cost = 0.3  # Higher cost (mental rotation)

        result = {
            "viewpoint": viewpoint,
            "scene": scene,
            "processing_cost": processing_cost
        }

        return result

    def shift_perspective(
        self,
        current_viewpoint: Dict,
        target_viewpoint: Dict,
        context: Dict
    ) -> Dict:
        """
        Complete perspective shift process

        Parameters:
        -----------
        current_viewpoint : Dict
            Current perspective (position, heading)
        target_viewpoint : Dict
            Target perspective (position, heading)
        context : Dict
            Additional context (object locations, etc.)

        Returns:
        --------
        result : Dict
            Transformation result with cost
        """
        # Compute rotation cost
        current_heading = current_viewpoint.get("heading", 0)
        target_heading = target_viewpoint.get("heading", 0)
        rotation_angle = (target_heading - current_heading) % 360
        if rotation_angle > 180:
            rotation_angle = 360 - rotation_angle

        rotation_cost = self.compute_rotation_cost(rotation_angle)

        # Update statistics
        self.total_perspective_shifts += 1

        result = {
            "transformation_applied": True,
            "rotation_cost": rotation_cost,
            "perspective_holder": target_viewpoint.get("position", "other"),
            "target_heading": target_heading
        }

        return result

    def hold_multiple_perspectives(
        self,
        perspectives: List[Dict]
    ) -> List[Dict]:
        """
        Hold multiple perspectives simultaneously (working memory)

        Integration with LAB_011 (Working Memory): Capacity-limited.

        Parameters:
        -----------
        perspectives : List[Dict]
            List of perspectives to hold

        Returns:
        --------
        held_perspectives : List[Dict]
            Perspectives held in working memory
        """
        # Working memory capacity ~7 items (Miller's Law)
        max_capacity = 7
        return perspectives[:max_capacity]

    def process_event(
        self,
        event_type: str,
        **kwargs
    ) -> Dict:
        """
        Main processing: complete perspective shift

        Workflow:
        1. Identify shift type (spatial vs conceptual)
        2. Compute transformation
        3. Calculate cost
        4. Update statistics

        Parameters:
        -----------
        event_type : str
            "spatial_shift" or "conceptual_shift"
        **kwargs : Dict
            Event-specific parameters

        Returns:
        --------
        result : Dict
            Complete perspective shift result
        """
        if event_type == "spatial_shift":
            # Spatial perspective shift
            current_pos = kwargs.get("current_position", {})
            target_pos = kwargs.get("target_position", {})
            object_loc = kwargs.get("object_location", {})

            # Compute rotation
            current_heading = current_pos.get("heading", 0)
            target_heading = target_pos.get("heading", 0)
            rotation_angle = abs(target_heading - current_heading)
            if rotation_angle > 180:
                rotation_angle = 360 - rotation_angle

            rotation_cost = self.compute_rotation_cost(rotation_angle)

            # Update statistics
            self.total_perspective_shifts += 1

            result = {
                "transformed_view": {
                    "heading": target_heading,
                    "object_location": object_loc
                },
                "rotation_cost": rotation_cost,
                "perspective_type": "spatial"
            }

        elif event_type == "conceptual_shift":
            # Conceptual perspective shift
            my_belief = kwargs.get("my_belief", {})
            their_belief = kwargs.get("their_belief", {})

            adopted = self.conceptual_perspective(my_belief, their_belief)

            # Update statistics
            self.total_perspective_shifts += 1

            result = {
                "adopted_perspective": adopted,
                "perspective_type": "conceptual"
            }

        else:
            result = {"error": f"Unknown event type: {event_type}"}

        return result

    def get_state(self) -> Dict:
        """Get current perspective taking system state"""
        return {
            "total_perspective_shifts": int(self.total_perspective_shifts),
            "rotation_cost_per_degree": float(self.rotation_cost_per_degree)
        }
