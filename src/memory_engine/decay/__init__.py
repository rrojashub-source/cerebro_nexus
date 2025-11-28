"""
Smart Decay - Intelligent memory forgetting system

Implements brain-inspired decay:
- Recency bias (recent > old)
- Access frequency (frequent > rare)
- Importance weighting (important > trivial)
- Emotional salience (emotional > neutral)

Author: NEXUS AI
Created: November 28, 2025
"""

from .smart_decay import SmartDecay

__all__ = ["SmartDecay"]
