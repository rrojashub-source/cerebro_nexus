"""
LAYER_5F: Creativity & Social Cognition

6 LABs implementing higher-order cognitive functions:
- Creativity: Divergent thinking, conceptual blending, insight, dream logic
- Social Cognition: Theory of mind, empathy simulation

Operational LABs: 6/6 (100%)
"""

from .LAB_023_Divergent_Thinking import DivergentThinkingSystem
from .LAB_024_Conceptual_Blending import ConceptualBlendingSystem
from .LAB_025_Insight import InsightSystem
from .LAB_026_Dream_Logic import DreamLogicSystem
from .LAB_027_Theory_of_Mind import TheoryOfMindSystem
from .LAB_028_Empathy import EmpathySystem

__all__ = [
    "DivergentThinkingSystem",
    "ConceptualBlendingSystem",
    "InsightSystem",
    "DreamLogicSystem",
    "TheoryOfMindSystem",
    "EmpathySystem"
]
