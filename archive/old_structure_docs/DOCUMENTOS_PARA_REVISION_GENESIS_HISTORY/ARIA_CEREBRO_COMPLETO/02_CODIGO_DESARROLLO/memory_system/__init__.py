"""
ARIA MEMORIA PERSISTENTE - Sistema de Memoria Persistente Profesional

Sistema avanzado de memoria persistente para agentes IA que elimina completamente 
la pérdida de contexto entre sesiones usando arquitectura de 3 niveles:
- Working Memory (Redis)
- Episodic Memory (PostgreSQL) 
- Semantic Memory (Chroma + Mem0)

Versión: 1.0.0
Equipo: NEXUS (Ricardo + ARIA + Nexus)
"""

__version__ = "1.0.0"
__author__ = "Equipo NEXUS"
__description__ = "Sistema profesional de memoria persistente para agentes IA"

from .core.memory_manager import AriaMemoryManager
from .core.working_memory import WorkingMemory
from .core.episodic_memory import EpisodicMemory
from .core.semantic_memory import SemanticMemory
from .core.consolidation_engine import ConsolidationEngine
from .core.continuity_manager import ContinuityManager

__all__ = [
    "AriaMemoryManager",
    "WorkingMemory", 
    "EpisodicMemory",
    "SemanticMemory",
    "ConsolidationEngine",
    "ContinuityManager"
]