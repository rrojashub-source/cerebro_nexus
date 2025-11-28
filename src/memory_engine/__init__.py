"""
CEREBRO Memory Engine - SuperMemory-style intelligent memory system

Provides:
- Multi-tier storage (Hot/Warm/Cold)
- Intelligent relationships (Updates/Extends/Derives)
- Smart decay and forgetting
- Fact extraction from documents

Architecture:
    memory_engine/
        tiers/          # Hot (Redis) / Warm (PostgreSQL) / Cold (Archive)
        relationships/  # Graph relationships (Neo4j)
        decay/          # Smart forgetting algorithms
        facts/          # Document -> Facts extraction

Author: NEXUS AI
Created: November 28, 2025
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "NEXUS AI"
