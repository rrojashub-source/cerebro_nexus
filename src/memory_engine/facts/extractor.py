"""
Fact Extractor - Converts documents/content into discrete facts

Inspired by SuperMemory's fact extraction:
- Breaks content into semantic chunks
- Extracts individual facts/assertions
- Creates embeddings for each fact
- Links facts to source document

This integrates with existing LAB_051 (Hybrid Memory) functionality.

Author: NEXUS AI
Created: November 28, 2025
"""

from typing import Dict, List, Optional, Any
import re
import logging

logger = logging.getLogger(__name__)


class FactExtractor:
    """
    Extracts discrete facts from documents and content.

    Works with:
    - Long-form text (articles, docs)
    - Structured data (JSON, YAML)
    - Conversations (chat logs)
    """

    def __init__(
        self,
        min_fact_length: int = 10,
        max_fact_length: int = 500,
        chunk_size: int = 1000,
        overlap: int = 100
    ):
        """
        Initialize fact extractor.

        Args:
            min_fact_length: Minimum characters for a fact
            max_fact_length: Maximum characters for a fact
            chunk_size: Size of initial content chunks
            overlap: Overlap between chunks
        """
        self.min_fact_length = min_fact_length
        self.max_fact_length = max_fact_length
        self.chunk_size = chunk_size
        self.overlap = overlap

    def extract_facts(
        self,
        content: str,
        source_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Extract facts from content.

        Args:
            content: Source text
            source_id: ID of source document
            metadata: Additional metadata

        Returns:
            List of fact dicts with content and metadata
        """
        facts = []

        # Step 1: Split into sentences
        sentences = self._split_into_sentences(content)

        # Step 2: Group into logical facts
        current_fact = []
        current_length = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # If adding this sentence exceeds max, save current fact
            if current_length + len(sentence) > self.max_fact_length and current_fact:
                fact_text = " ".join(current_fact)
                if len(fact_text) >= self.min_fact_length:
                    facts.append(self._create_fact(
                        fact_text, source_id, metadata, len(facts)
                    ))
                current_fact = []
                current_length = 0

            current_fact.append(sentence)
            current_length += len(sentence) + 1

        # Don't forget the last fact
        if current_fact:
            fact_text = " ".join(current_fact)
            if len(fact_text) >= self.min_fact_length:
                facts.append(self._create_fact(
                    fact_text, source_id, metadata, len(facts)
                ))

        logger.info(f"Extracted {len(facts)} facts from content")
        return facts

    def _split_into_sentences(self, content: str) -> List[str]:
        """Split content into sentences"""
        # Simple sentence splitting (can be improved with NLP)
        sentences = re.split(r'(?<=[.!?])\s+', content)
        return [s.strip() for s in sentences if s.strip()]

    def _create_fact(
        self,
        content: str,
        source_id: Optional[str],
        metadata: Optional[Dict],
        index: int
    ) -> Dict:
        """Create a fact dict"""
        return {
            "content": content,
            "source_id": source_id,
            "index": index,
            "metadata": metadata or {},
            "type": "fact",
            "length": len(content)
        }

    def extract_key_value_facts(
        self,
        content: str,
        source_id: Optional[str] = None
    ) -> List[Dict]:
        """
        Extract key-value style facts (e.g., "Name: John").

        Useful for structured info like profiles, settings, etc.
        """
        facts = []
        patterns = [
            r'(\w+[\w\s]*?):\s*(.+?)(?=\n|$)',  # Key: Value
            r'(\w+[\w\s]*?)\s*=\s*(.+?)(?=\n|$)',  # Key = Value
            r'(\w+[\w\s]*?)\s*is\s+(.+?)(?=[.!?\n]|$)',  # X is Y
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            for key, value in matches:
                key = key.strip()
                value = value.strip()
                if key and value and len(value) >= self.min_fact_length:
                    facts.append({
                        "content": f"{key}: {value}",
                        "key": key,
                        "value": value,
                        "source_id": source_id,
                        "type": "key_value_fact"
                    })

        return facts

    def chunk_document(
        self,
        content: str,
        source_id: Optional[str] = None
    ) -> List[Dict]:
        """
        Split document into overlapping chunks.

        Used for initial processing before fact extraction.
        """
        chunks = []
        start = 0
        content_length = len(content)

        while start < content_length:
            end = min(start + self.chunk_size, content_length)

            # Try to end at a sentence boundary
            if end < content_length:
                last_period = content.rfind('.', start, end)
                if last_period > start + self.chunk_size // 2:
                    end = last_period + 1

            chunk_text = content[start:end].strip()
            if chunk_text:
                chunks.append({
                    "content": chunk_text,
                    "source_id": source_id,
                    "start": start,
                    "end": end,
                    "type": "chunk"
                })

            start = end - self.overlap

        logger.info(f"Created {len(chunks)} chunks from document")
        return chunks
