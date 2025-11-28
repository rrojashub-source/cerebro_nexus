"""
Fact Extraction - Document to Facts converter

Transforms long-form content into discrete facts:
- Documents -> Semantic chunks
- Chunks -> Individual facts
- Facts -> Embeddings + Relationships

Author: NEXUS AI
Created: November 28, 2025
"""

from .extractor import FactExtractor

__all__ = ["FactExtractor"]
