"""
Memory Graph - Neo4j-based relationship management

Implements SuperMemory-style relationship types:
- UPDATES: Contradicts/replaces existing memory
- EXTENDS: Adds information without contradiction
- DERIVES: Inferred connection from patterns

Author: NEXUS AI
Created: November 28, 2025
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class RelationType(Enum):
    """Types of relationships between memories"""
    UPDATES = "updates"      # New info replaces old
    EXTENDS = "extends"      # New info adds to existing
    DERIVES = "derives"      # System infers connection
    TEMPORAL = "temporal"    # Time-based (before/after)
    CAUSAL = "causal"        # Cause-effect relationship
    SIMILAR = "similar"      # Semantic similarity


class MemoryGraph:
    """
    Graph-based memory relationship manager.

    Uses Neo4j to track relationships between memories,
    enabling rich contextual retrieval and inference.
    """

    def __init__(
        self,
        uri: str = "bolt://localhost:7687",
        user: str = "neo4j",
        password: str = "nexus_neo4j_2024"
    ):
        self.uri = uri
        self.user = user
        self.password = password
        self._driver = None

    def _get_driver(self):
        """Get Neo4j driver (lazy initialization)"""
        if self._driver is None:
            try:
                from neo4j import GraphDatabase
                self._driver = GraphDatabase.driver(
                    self.uri,
                    auth=(self.user, self.password)
                )
            except Exception as e:
                logger.error(f"Failed to connect to Neo4j: {e}")
                raise
        return self._driver

    def connect(
        self,
        source_id: str,
        target_id: str,
        relation_type: RelationType,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Create relationship between two memories.

        Args:
            source_id: Source memory ID
            target_id: Target memory ID
            relation_type: Type of relationship
            metadata: Additional relationship data

        Returns:
            True if successful
        """
        try:
            driver = self._get_driver()
            with driver.session() as session:
                result = session.run("""
                    MATCH (s:Episode {episode_id: $source_id})
                    MATCH (t:Episode {episode_id: $target_id})
                    MERGE (s)-[r:%s]->(t)
                    SET r.created_at = datetime(),
                        r.metadata = $metadata
                    RETURN r
                """ % relation_type.value.upper(), {
                    "source_id": source_id,
                    "target_id": target_id,
                    "metadata": metadata or {}
                })
                return result.single() is not None
        except Exception as e:
            logger.error(f"Failed to create relationship: {e}")
            return False

    def get_related(
        self,
        memory_id: str,
        relation_type: Optional[RelationType] = None,
        direction: str = "both",
        limit: int = 10
    ) -> List[Dict]:
        """
        Get memories related to a given memory.

        Args:
            memory_id: Source memory ID
            relation_type: Filter by relationship type (optional)
            direction: "in", "out", or "both"
            limit: Max results

        Returns:
            List of related memories with relationship info
        """
        try:
            driver = self._get_driver()
            with driver.session() as session:
                # Build direction pattern
                if direction == "out":
                    pattern = "(s)-[r]->(t)"
                elif direction == "in":
                    pattern = "(s)<-[r]-(t)"
                else:
                    pattern = "(s)-[r]-(t)"

                # Build relation filter
                rel_filter = ""
                if relation_type:
                    rel_filter = f"AND type(r) = '{relation_type.value.upper()}'"

                result = session.run(f"""
                    MATCH {pattern}
                    WHERE s.episode_id = $memory_id {rel_filter}
                    RETURN t.episode_id as id,
                           t.content as content,
                           type(r) as relation,
                           r.metadata as metadata
                    LIMIT $limit
                """, {"memory_id": memory_id, "limit": limit})

                return [dict(record) for record in result]
        except Exception as e:
            logger.error(f"Failed to get related memories: {e}")
            return []

    def infer_relationships(self, memory_id: str) -> List[Dict]:
        """
        Automatically infer DERIVES relationships based on patterns.

        Uses semantic similarity and temporal proximity to find
        potential connections.
        """
        # TODO: Implement inference logic
        logger.info(f"Relationship inference not yet implemented: {memory_id}")
        return []

    def mark_as_updated(self, old_id: str, new_id: str) -> bool:
        """
        Mark old memory as updated by new memory.

        Creates UPDATES relationship and marks old as not latest.
        """
        try:
            driver = self._get_driver()
            with driver.session() as session:
                session.run("""
                    MATCH (old:Episode {episode_id: $old_id})
                    MATCH (new:Episode {episode_id: $new_id})
                    MERGE (new)-[:UPDATES]->(old)
                    SET old.is_latest = false,
                        new.is_latest = true
                """, {"old_id": old_id, "new_id": new_id})
                return True
        except Exception as e:
            logger.error(f"Failed to mark as updated: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """Get graph statistics"""
        try:
            driver = self._get_driver()
            with driver.session() as session:
                result = session.run("""
                    MATCH (n:Episode)
                    WITH count(n) as nodes
                    MATCH ()-[r]->()
                    RETURN nodes, count(r) as relationships
                """)
                record = result.single()
                return {
                    "nodes": record["nodes"] if record else 0,
                    "relationships": record["relationships"] if record else 0,
                    "storage": "neo4j"
                }
        except Exception as e:
            logger.error(f"Failed to get graph stats: {e}")
            return {"error": str(e)}
