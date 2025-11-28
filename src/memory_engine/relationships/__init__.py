"""
Memory Relationships - Graph-based memory connections

Relationship types (inspired by SuperMemory):
- UPDATES: New info replaces old (contradiction)
- EXTENDS: New info adds to existing (supplementary)
- DERIVES: System infers new connections (emergent)
- TEMPORAL: Time-based relationships (before/after)

Author: NEXUS AI
Created: November 28, 2025
"""

from .graph import MemoryGraph, RelationType

__all__ = ["MemoryGraph", "RelationType"]
