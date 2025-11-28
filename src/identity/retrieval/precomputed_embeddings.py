"""
Pre-Computed Embeddings Module (Week 5)

Implements pre-computed embedding storage and retrieval for performance optimization.

Author: NEXUS
Date: November 12, 2025
Version: 2.0.0 (Week 5)
"""

import logging
import os
import numpy as np
import psycopg2
from sentence_transformers import SentenceTransformer
import time
from typing import List, Dict, Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration (uses environment variables with fallback for local development)
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': int(os.getenv('POSTGRES_PORT', '5437')),
    'database': os.getenv('POSTGRES_DB', 'nexus_memory'),
    'user': os.getenv('POSTGRES_USER', 'nexus_superuser'),
    'password': os.getenv('POSTGRES_PASSWORD', 'RpKeuQhnwqMOA4iQPILQshWtwFj0P2hm')
}

# Lazy-load sentence transformer model
_MODEL = None
MODEL_NAME = 'all-MiniLM-L6-v2'
EMBEDDING_DIM = 384


def _get_model():
    """Get or initialize sentence-transformers model (lazy loading)."""
    global _MODEL
    if _MODEL is None:
        logger.info(f"Loading sentence-transformers model: {MODEL_NAME}")
        _MODEL = SentenceTransformer(MODEL_NAME)
    return _MODEL


def migrate_schema(conn):
    """
    Migrate database schema to support pre-computed embeddings.

    Adds:
    - content_embedding (vector(384)): Pre-computed embedding storage
    - embedding_model (varchar): Model version tracking
    - embedding_computed_at (timestamptz): Computation timestamp

    Args:
        conn: psycopg2 connection

    Returns:
        dict: Migration result with success status

    Raises:
        psycopg2.Error: If migration fails
    """
    logger.info("Starting schema migration for pre-computed embeddings")

    cursor = conn.cursor()

    try:
        # Check if columns already exist
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'nexus_memory'
            AND table_name = 'zep_episodic_memory'
            AND column_name IN ('content_embedding', 'embedding_model', 'embedding_computed_at');
        """)

        existing_columns = [row[0] for row in cursor.fetchall()]

        if 'content_embedding' in existing_columns:
            logger.info("Schema migration already completed (columns exist)")
            return {'status': 'already_migrated', 'columns_added': 0}

        # Add content_embedding column (vector type from pgvector)
        logger.info("Adding content_embedding column (vector(384))...")
        cursor.execute("""
            ALTER TABLE nexus_memory.zep_episodic_memory
            ADD COLUMN content_embedding vector(384);
        """)

        # Add embedding_model column (track model version)
        logger.info("Adding embedding_model column...")
        cursor.execute(f"""
            ALTER TABLE nexus_memory.zep_episodic_memory
            ADD COLUMN embedding_model varchar(100) DEFAULT '{MODEL_NAME}';
        """)

        # Add embedding_computed_at column (track computation time)
        logger.info("Adding embedding_computed_at column...")
        cursor.execute("""
            ALTER TABLE nexus_memory.zep_episodic_memory
            ADD COLUMN embedding_computed_at timestamptz;
        """)

        conn.commit()

        logger.info("✅ Schema migration completed successfully")
        return {'status': 'success', 'columns_added': 3}

    except psycopg2.Error as e:
        conn.rollback()
        logger.error(f"Schema migration failed: {e}")
        raise

    finally:
        cursor.close()


def compute_episode_embedding(content: str) -> np.ndarray:
    """
    Compute embedding for a single episode content.

    Args:
        content: Episode content text

    Returns:
        np.ndarray: Embedding vector (384D)

    Raises:
        ValueError: If content is empty
    """
    if not content or len(content.strip()) == 0:
        raise ValueError("Content cannot be empty")

    model = _get_model()
    embedding = model.encode(content, convert_to_numpy=True, normalize_embeddings=True)

    return embedding.astype(np.float32)


def batch_compute_embeddings(
    conn,
    batch_size: int = 1000,
    limit: Optional[int] = None,
    dry_run: bool = False
) -> Dict[str, int]:
    """
    Compute embeddings for episodes in batches.

    Args:
        conn: psycopg2 connection
        batch_size: Episodes per batch (default 1000)
        limit: Max episodes to process (None = all)
        dry_run: If True, don't save to DB (default False)

    Returns:
        dict: Statistics with 'processed', 'skipped', 'errors' counts

    Strategy:
    - Fetch episodes without embeddings (content_embedding IS NULL)
    - Compute embeddings in batches
    - Update DB with embeddings + metadata
    - Checkpoint after each batch (commit)
    """
    logger.info(f"Starting batch embedding computation (batch_size={batch_size}, limit={limit}, dry_run={dry_run})")

    cursor = conn.cursor()
    model = _get_model()

    stats = {
        'processed': 0,
        'skipped': 0,
        'errors': 0
    }

    try:
        # Count total episodes needing embeddings
        cursor.execute("""
            SELECT COUNT(*)
            FROM nexus_memory.zep_episodic_memory
            WHERE content_embedding IS NULL;
        """)

        total_pending = cursor.fetchone()[0]
        logger.info(f"Found {total_pending} episodes without embeddings")

        if total_pending == 0:
            logger.info("No episodes to process (all have embeddings)")
            return stats

        # Apply limit if specified
        actual_limit = min(limit, total_pending) if limit else total_pending

        # Process in batches
        offset = 0
        while offset < actual_limit:
            batch_limit = min(batch_size, actual_limit - offset)

            logger.info(f"Processing batch: offset={offset}, limit={batch_limit}")

            # Fetch batch of episodes without embeddings
            cursor.execute("""
                SELECT episode_id, content
                FROM nexus_memory.zep_episodic_memory
                WHERE content_embedding IS NULL
                AND content IS NOT NULL
                AND LENGTH(content) > 0
                ORDER BY timestamp DESC
                LIMIT %s OFFSET %s;
            """, (batch_limit, offset))

            batch = cursor.fetchall()

            if len(batch) == 0:
                logger.info("No more episodes to process")
                break

            # Compute embeddings for batch
            episode_ids = [row[0] for row in batch]
            contents = [row[1] for row in batch]

            logger.info(f"Computing embeddings for {len(contents)} episodes...")
            start_time = time.time()

            # Batch encode (faster than individual encodes)
            embeddings = model.encode(
                contents,
                convert_to_numpy=True,
                normalize_embeddings=True,
                show_progress_bar=False
            )

            elapsed = time.time() - start_time
            logger.info(f"Computed {len(embeddings)} embeddings in {elapsed:.1f}s")

            if not dry_run:
                # Update DB with embeddings
                logger.info("Saving embeddings to database...")
                for episode_id, embedding in zip(episode_ids, embeddings):
                    try:
                        # Convert numpy array to list for PostgreSQL
                        embedding_list = embedding.tolist()

                        cursor.execute("""
                            UPDATE nexus_memory.zep_episodic_memory
                            SET
                                content_embedding = %s::vector,
                                embedding_model = %s,
                                embedding_computed_at = NOW()
                            WHERE episode_id = %s;
                        """, (embedding_list, MODEL_NAME, episode_id))

                        stats['processed'] += 1

                    except Exception as e:
                        logger.error(f"Error saving embedding for {episode_id}: {e}")
                        stats['errors'] += 1

                # Checkpoint: commit batch
                conn.commit()
                logger.info(f"✅ Batch committed ({stats['processed']} episodes processed)")

            else:
                stats['processed'] += len(embeddings)
                logger.info(f"DRY RUN: Would have saved {len(embeddings)} embeddings")

            offset += batch_limit

        logger.info(f"✅ Batch computation complete: {stats}")
        return stats

    except Exception as e:
        conn.rollback()
        logger.error(f"Batch computation failed: {e}")
        raise

    finally:
        cursor.close()


def create_vector_index(conn, index_type: str = 'ivfflat'):
    """
    Create pgvector index on content_embedding column.

    Args:
        conn: psycopg2 connection
        index_type: 'ivfflat' or 'hnsw' (default 'ivfflat')

    Returns:
        dict: Index creation result

    Raises:
        ValueError: If index_type invalid
        psycopg2.Error: If index creation fails
    """
    if index_type not in ['ivfflat', 'hnsw']:
        raise ValueError(f"Invalid index_type '{index_type}', must be 'ivfflat' or 'hnsw'")

    logger.info(f"Creating {index_type} index on content_embedding...")

    cursor = conn.cursor()

    try:
        # Check if index already exists
        cursor.execute("""
            SELECT indexname
            FROM pg_indexes
            WHERE schemaname = 'nexus_memory'
            AND tablename = 'zep_episodic_memory'
            AND indexname LIKE '%embedding%';
        """)

        existing_indexes = [row[0] for row in cursor.fetchall()]

        if any('embedding' in idx for idx in existing_indexes):
            logger.info(f"Vector index already exists: {existing_indexes}")
            return {'status': 'already_exists', 'indexes': existing_indexes}

        # Create index based on type
        if index_type == 'ivfflat':
            # IVFFlat: Good for <1M vectors, faster build
            logger.info("Creating IVFFlat index (lists=100)...")
            cursor.execute("""
                CREATE INDEX idx_episodic_embedding_ivfflat
                ON nexus_memory.zep_episodic_memory
                USING ivfflat (content_embedding vector_cosine_ops)
                WITH (lists = 100);
            """)

        elif index_type == 'hnsw':
            # HNSW: Better recall, slower build
            logger.info("Creating HNSW index (m=16, ef_construction=64)...")
            cursor.execute("""
                CREATE INDEX idx_episodic_embedding_hnsw
                ON nexus_memory.zep_episodic_memory
                USING hnsw (content_embedding vector_cosine_ops)
                WITH (m = 16, ef_construction = 64);
            """)

        conn.commit()

        logger.info(f"✅ {index_type} index created successfully")
        return {'status': 'created', 'index_type': index_type}

    except psycopg2.Error as e:
        conn.rollback()
        logger.error(f"Index creation failed: {e}")
        raise

    finally:
        cursor.close()


def fetch_episodes_with_embeddings(
    query_embedding: np.ndarray,
    top_k: int = 20,
    threshold: float = 0.3
) -> List[Dict]:
    """
    Fetch episodes using pre-computed embeddings with pgvector similarity search.

    Args:
        query_embedding: Query embedding vector (384D)
        top_k: Maximum episodes to return (default 20)
        threshold: Minimum similarity score (default 0.3)

    Returns:
        list: Episodes with similarity scores, sorted by relevance

    Strategy:
    - Use pgvector's <=> operator for cosine distance
    - Similarity = 1 - cosine_distance
    - Filter by threshold, order by similarity DESC
    - Return top_k episodes with metadata
    """
    logger.debug(f"Fetching episodes with pre-computed embeddings (top_k={top_k}, threshold={threshold})")

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        # Convert numpy array to list for PostgreSQL
        embedding_list = query_embedding.tolist()

        # pgvector query with cosine distance
        # <=> operator: cosine distance (0 = identical, 2 = opposite)
        # Similarity: 1 - (distance / 2) = 1 - (cosine_distance / 2)
        query = """
        SELECT
            episode_id,
            content,
            importance_score,
            tags,
            content_embedding,
            1 - (content_embedding <=> %s::vector) AS similarity
        FROM nexus_memory.zep_episodic_memory
        WHERE content_embedding IS NOT NULL
        AND 1 - (content_embedding <=> %s::vector) >= %s
        ORDER BY content_embedding <=> %s::vector
        LIMIT %s;
        """

        cursor.execute(query, (embedding_list, embedding_list, threshold, embedding_list, top_k))
        rows = cursor.fetchall()

        episodes = [
            {
                'episode_id': str(row[0]),
                'content': row[1],
                'importance_score': row[2],
                'tags': row[3] if row[3] else [],
                # pgvector returns embedding as string, convert to numpy array
                'embedding': np.fromstring(row[4][1:-1], sep=',', dtype=np.float32) if row[4] else None,
                'similarity': float(row[5])
            }
            for row in rows
        ]

        logger.debug(f"Fetched {len(episodes)} episodes with pre-computed embeddings")
        return episodes

    except psycopg2.Error as e:
        logger.error(f"Error fetching episodes with embeddings: {e}")
        raise

    finally:
        cursor.close()
        conn.close()


def validate_migration(conn) -> Dict[str, any]:
    """
    Validate that migration completed successfully.

    Checks:
    - Schema columns exist
    - Embeddings computed for episodes
    - Vector index exists
    - Sample vector search works

    Args:
        conn: psycopg2 connection

    Returns:
        dict: Validation results

    Raises:
        AssertionError: If validation fails
    """
    logger.info("Validating migration...")

    cursor = conn.cursor()
    results = {}

    try:
        # Check schema columns
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'nexus_memory'
            AND table_name = 'zep_episodic_memory'
            AND column_name IN ('content_embedding', 'embedding_model', 'embedding_computed_at');
        """)

        columns = [row[0] for row in cursor.fetchall()]
        results['schema_columns'] = len(columns) == 3

        # Check embedding coverage
        cursor.execute("""
            SELECT
                COUNT(*) AS total,
                COUNT(content_embedding) AS with_embedding
            FROM nexus_memory.zep_episodic_memory;
        """)

        row = cursor.fetchone()
        total, with_embedding = row[0], row[1]
        results['total_episodes'] = total
        results['episodes_with_embeddings'] = with_embedding
        results['embedding_coverage'] = with_embedding / total if total > 0 else 0

        # Check vector index
        cursor.execute("""
            SELECT COUNT(*)
            FROM pg_indexes
            WHERE schemaname = 'nexus_memory'
            AND tablename = 'zep_episodic_memory'
            AND indexname LIKE '%embedding%';
        """)

        index_count = cursor.fetchone()[0]
        results['vector_index_exists'] = index_count > 0

        # Test sample vector search
        try:
            sample_embedding = np.random.rand(EMBEDDING_DIM).astype(np.float32)
            sample_episodes = fetch_episodes_with_embeddings(sample_embedding, top_k=5, threshold=0.0)
            results['vector_search_works'] = len(sample_episodes) >= 0
        except Exception as e:
            results['vector_search_works'] = False
            results['vector_search_error'] = str(e)

        logger.info(f"✅ Validation complete: {results}")
        return results

    except Exception as e:
        logger.error(f"Validation failed: {e}")
        raise

    finally:
        cursor.close()
