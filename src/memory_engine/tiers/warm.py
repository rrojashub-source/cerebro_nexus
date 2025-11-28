"""
Warm Memory Tier - PostgreSQL-based standard episodic memory

Stores:
- All episodic memories
- Semantic embeddings (pgvector)
- Full metadata and relationships

Performance target: < 10ms

Author: NEXUS AI
Created: November 28, 2025
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
import numpy as np

logger = logging.getLogger(__name__)


class WarmMemory:
    """
    Warm memory tier using PostgreSQL + pgvector.

    Features:
    - Full episodic storage
    - Semantic search with embeddings
    - Rich metadata support
    - Relationship tracking
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5437,
        database: str = "nexus_memory",
        user: str = "nexus",
        password: str = "nexus_secure_2024"
    ):
        self.conn_params = {
            "host": host,
            "port": port,
            "database": database,
            "user": user,
            "password": password
        }

    def _get_connection(self):
        """Get database connection"""
        return psycopg2.connect(**self.conn_params)

    def add(
        self,
        content: str,
        embedding: Optional[List[float]] = None,
        metadata: Optional[Dict] = None,
        tags: Optional[List[str]] = None
    ) -> Optional[str]:
        """Add memory to warm tier"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO nexus_memory.zep_episodic_memory
                        (content, content_embedding, tags, metadata, created_at)
                        VALUES (%s, %s, %s, %s, NOW())
                        RETURNING episode_id
                    """, (
                        content,
                        embedding,
                        tags or [],
                        metadata or {}
                    ))
                    result = cur.fetchone()
                    conn.commit()
                    episode_id = str(result[0])
                    logger.debug(f"Added to warm tier: {episode_id}")
                    return episode_id
        except Exception as e:
            logger.error(f"Failed to add to warm tier: {e}")
            return None

    def get(self, memory_id: str) -> Optional[Dict]:
        """Get memory by ID"""
        try:
            with self._get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                        SELECT episode_id, content, tags, metadata,
                               importance_score, created_at
                        FROM nexus_memory.zep_episodic_memory
                        WHERE episode_id = %s
                    """, (memory_id,))
                    result = cur.fetchone()
                    return dict(result) if result else None
        except Exception as e:
            logger.error(f"Failed to get from warm tier: {e}")
            return None

    def search_semantic(
        self,
        query_embedding: List[float],
        limit: int = 10,
        threshold: float = 0.7
    ) -> List[Dict]:
        """Semantic search using pgvector"""
        try:
            with self._get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                        SELECT
                            episode_id,
                            content,
                            tags,
                            metadata,
                            importance_score,
                            created_at,
                            1 - (content_embedding <=> %s::vector) as similarity
                        FROM nexus_memory.zep_episodic_memory
                        WHERE content_embedding IS NOT NULL
                            AND 1 - (content_embedding <=> %s::vector) >= %s
                        ORDER BY content_embedding <=> %s::vector
                        LIMIT %s
                    """, (query_embedding, query_embedding, threshold, query_embedding, limit))
                    return [dict(row) for row in cur.fetchall()]
        except Exception as e:
            logger.error(f"Warm tier semantic search failed: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """Get warm tier statistics"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT
                            COUNT(*) as total,
                            COUNT(content_embedding) as with_embeddings
                        FROM nexus_memory.zep_episodic_memory
                    """)
                    result = cur.fetchone()
                    return {
                        "tier": "warm",
                        "total_items": result[0],
                        "with_embeddings": result[1],
                        "storage": "postgresql"
                    }
        except Exception as e:
            logger.error(f"Failed to get warm tier stats: {e}")
            return {"tier": "warm", "error": str(e)}
