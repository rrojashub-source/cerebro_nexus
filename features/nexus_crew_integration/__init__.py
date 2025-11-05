"""
NEXUS_CREW Integration - Shared Episodic Memory System

Provides bidirectional sync between CEREBRO_NEXUS_V3.0.0 and NEXUS_CREW agents.
"""

from .cerebro_client import CerebroClient
# from .cerebro_bridge import CerebroMemoryBridge  # TODO: Uncomment after implementing

__all__ = [
    "CerebroClient",
    # "CerebroMemoryBridge",  # TODO: Uncomment after implementing
]
