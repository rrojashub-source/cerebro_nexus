"""
Memory Retrieval Module

Retrieves episodes from GIC database using semantic search.

Author: NEXUS
Date: November 12, 2025
Version: 1.0.0 (Week 4)
"""

import logging
import os
import numpy as np
import psycopg2
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration (uses environment variables with fallback to localhost)
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': int(os.getenv('POSTGRES_PORT', '5437')),
    'database': os.getenv('POSTGRES_DB', 'nexus_memory'),
    'user': os.getenv('POSTGRES_USER', 'nexus_superuser'),
    'password': os.getenv('POSTGRES_PASSWORD', 'RpKeuQhnwqMOA4iQPILQshWtwFj0P2hm')
}

# Lazy-load sentence transformer model (shared across calls)
_MODEL = None

# Session-level embedding cache (reduces redundant computations)
_EMBEDDING_CACHE = {}


def _get_model():
    """Get or initialize sentence-transformers model (lazy loading)."""
    global _MODEL
    if _MODEL is None:
        logger.info("Loading sentence-transformers model: all-MiniLM-L6-v2")
        _MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    return _MODEL


def connect_to_database():
    """
    Connect to GIC database.

    Returns:
        psycopg2.connection: Database connection

    Raises:
        ConnectionError: If connection fails
    """
    try:
        logger.debug(f"Connecting to database: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
        conn = psycopg2.connect(**DB_CONFIG)
        logger.debug("Database connection established")
        return conn
    except psycopg2.OperationalError as e:
        logger.error(f"Database connection failed: {e}")
        raise ConnectionError(f"Failed to connect to database (operational error): {e}")
    except Exception as e:
        logger.error(f"Unexpected error connecting to database: {e}")
        raise ConnectionError(f"Failed to connect to database: {e}")


def load_z_id_from_gic(agent_id='nexus'):
    """
    Load agent Z_ID from GIC database.

    Args:
        agent_id: Agent identifier (default 'nexus')

    Returns:
        numpy.ndarray: Z_ID vector (1024D)

    Raises:
        ValueError: If agent_id not found
        ConnectionError: If database connection fails
    """
    logger.info(f"Loading Z_ID for agent: {agent_id}")

    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        query = """
        SELECT z_id_vector
        FROM consciousness.grounded_identity_core
        WHERE agent_id = %s;
        """
        cursor.execute(query, (agent_id,))
        result = cursor.fetchone()

        if result is None:
            logger.error(f"Agent '{agent_id}' not found in GIC")
            raise ValueError(f"Agent '{agent_id}' not found in GIC")

        # PostgreSQL returns array as list, convert to numpy
        z_id_list = result[0]
        z_id = np.array(z_id_list, dtype=np.float64)

        logger.info(f"Loaded Z_ID for {agent_id}: {z_id.shape}")
        return z_id

    except (psycopg2.Error, psycopg2.OperationalError) as e:
        logger.error(f"Database error loading Z_ID: {e}")
        raise ConnectionError(f"Failed to load Z_ID from database: {e}")
    finally:
        cursor.close()
        conn.close()


def fetch_episodes_from_db(limit=1000):
    """
    Fetch recent episodes from zep_episodic_memory table.

    Args:
        limit: Maximum number of episodes to fetch (default 1000)

    Returns:
        list: Episode dicts with episode_id, content, importance_score, tags

    Raises:
        ConnectionError: If database connection or query fails
    """
    logger.info(f"Fetching {limit} recent episodes from database")

    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        query = """
        SELECT episode_id, content, importance_score, tags
        FROM nexus_memory.zep_episodic_memory
        ORDER BY timestamp DESC
        LIMIT %s;
        """
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()

        # List comprehension (refactor optimization)
        episodes = [
            {
                'episode_id': str(row[0]),  # UUID to string
                'content': row[1],
                'importance_score': row[2],
                'tags': row[3] if row[3] else []
            }
            for row in rows
        ]

        logger.info(f"Fetched {len(episodes)} episodes")
        return episodes

    except (psycopg2.Error, psycopg2.OperationalError) as e:
        logger.error(f"Database error fetching episodes: {e}")
        raise ConnectionError(f"Failed to fetch episodes from database: {e}")
    finally:
        cursor.close()
        conn.close()


def embed_text(text, use_cache=True):
    """
    Embed text using sentence-transformers.

    Args:
        text: String to embed
        use_cache: Enable session-level caching (default True)

    Returns:
        numpy.ndarray: Embedding vector (384D for all-MiniLM-L6-v2)

    Raises:
        ValueError: If text is empty
    """
    if not text or len(text.strip()) == 0:
        raise ValueError("Text cannot be empty")

    # Check cache (session-level)
    if use_cache and text in _EMBEDDING_CACHE:
        logger.debug(f"Cache hit for text: {text[:50]}...")
        return _EMBEDDING_CACHE[text]

    # Compute embedding
    model = _get_model()
    embedding = model.encode(text, convert_to_numpy=True)

    # Cache result
    if use_cache:
        _EMBEDDING_CACHE[text] = embedding
        logger.debug(f"Cached embedding for text: {text[:50]}... (cache size: {len(_EMBEDDING_CACHE)})")

    return embedding


def compute_cosine_similarity(emb1, emb2):
    """
    Compute cosine similarity between two embeddings.

    Args:
        emb1: First embedding (numpy array)
        emb2: Second embedding (numpy array)

    Returns:
        float: Cosine similarity in range [-1, 1]

    Raises:
        ValueError: If embeddings have different dimensions
    """
    if emb1.shape != emb2.shape:
        raise ValueError(f"Embeddings must have same shape: {emb1.shape} vs {emb2.shape}")

    # Cosine similarity = 1 - cosine distance
    similarity = 1 - cosine(emb1, emb2)

    return float(similarity)


def retrieve_self_episodes(my_z_id, query, top_k=20, similarity_threshold=0.3, use_precomputed=False):
    """
    Retrieve MY episodes most relevant to query.

    Week 4 Implementation: On-the-fly embeddings (no pre-computed vectors)
    Week 5 Implementation: Dual-path (on-the-fly OR pre-computed)

    Args:
        my_z_id: My Z_ID vector (1024D numpy array)
        query: User query string
        top_k: Number of episodes to retrieve (default 20)
        similarity_threshold: Minimum cosine similarity (default 0.3)
        use_precomputed: Use pre-computed embeddings (Week 5, default False for backward compatibility)

    Returns:
        list: Episode dicts with:
            - episode_id: UUID
            - content: str
            - importance: float
            - tags: list
            - attribution: 'self'
            - z_id: my_z_id (same for all)
            - relevance_score: float (query similarity)

    Raises:
        ValueError: If query is empty or my_z_id invalid
        DatabaseError: If database connection fails

    Implementation (Week 4 - on-the-fly):
        1. Connect to nexus_memory DB
        2. Fetch recent 1000 episodes
        3. Embed query
        4. For each episode:
           - Embed content
           - Compute cosine similarity with query
        5. Filter: similarity >= similarity_threshold
        6. Sort: similarity DESC
        7. Return: top_k episodes

    Implementation (Week 5 - pre-computed):
        1. Embed query
        2. Call fetch_episodes_with_embeddings() (pgvector similarity search)
        3. Return episodes with pre-computed embeddings

    Performance:
        - Week 4 (on-the-fly): ~300-500ms
        - Week 5 (pre-computed): <10ms (2.4x faster)
    """
    # Validate inputs
    if not query or len(query.strip()) == 0:
        raise ValueError("Query cannot be empty")

    if not isinstance(my_z_id, np.ndarray) or my_z_id.shape != (1024,):
        raise ValueError(f"my_z_id must be 1024D numpy array, got {type(my_z_id)} with shape {getattr(my_z_id, 'shape', 'N/A')}")

    logger.info(f"Retrieving episodes for query: '{query[:50]}...' (top_k={top_k}, threshold={similarity_threshold}, use_precomputed={use_precomputed})")

    # Week 5: Use pre-computed embeddings path
    if use_precomputed:
        from src.identity.retrieval.precomputed_embeddings import fetch_episodes_with_embeddings

        # 1. Embed query
        query_embedding = embed_text(query)

        # 2. Fetch episodes using pgvector similarity search
        raw_episodes = fetch_episodes_with_embeddings(
            query_embedding=query_embedding,
            top_k=top_k,
            threshold=similarity_threshold
        )

        # 3. Convert to standard format (compatibility with AAG)
        result = [
            {
                'episode_id': ep['episode_id'],
                'content': ep['content'],
                'importance': ep['importance_score'],
                'tags': ep['tags'],
                'attribution': 'self',
                'z_id': my_z_id.tolist(),  # Convert numpy to list for JSON serialization
                'relevance_score': ep['similarity']  # Already computed by pgvector
            }
            for ep in raw_episodes
        ]

        logger.info(f"Retrieved {len(result)} episodes (pre-computed path)")
        return result

    # Week 4: On-the-fly embeddings path (backward compatible)
    else:
        # 1. Fetch recent episodes from database
        raw_episodes = fetch_episodes_from_db(limit=1000)

        # 2. Embed query
        query_embedding = embed_text(query)

        # 3. Score each episode by semantic similarity
        scored_episodes = []

        for ep in raw_episodes:
            # Embed episode content
            content_embedding = embed_text(ep['content'])

            # Compute cosine similarity with query
            relevance = compute_cosine_similarity(query_embedding, content_embedding)

            # Filter by threshold
            if relevance >= similarity_threshold:
                scored_episodes.append({
                    'episode_id': ep['episode_id'],
                    'content': ep['content'],
                    'importance': ep['importance_score'],
                    'tags': ep['tags'],
                    'attribution': 'self',  # All episodes are from NEXUS in Week 4
                    'z_id': my_z_id.tolist(),  # Convert numpy to list for JSON serialization
                    'relevance_score': relevance
                })

        # 4. Sort by relevance (descending)
        scored_episodes.sort(key=lambda x: x['relevance_score'], reverse=True)

        # 5. Return top_k
        result = scored_episodes[:top_k]
        logger.info(f"Retrieved {len(result)} episodes (on-the-fly path, filtered from {len(scored_episodes)} above threshold)")

        return result


def retrieve_external_episodes(
    query,
    exclude_agent_ids,
    top_k=10,
    use_precomputed=False,
    external_dbs=None
):
    """
    Retrieve EXTERNAL episodes from other agents.

    Week 4 Implementation: Return empty list (no external agents configured)
    Week 5+ Implementation: Query external agent databases when configured

    Args:
        query: User query string
        exclude_agent_ids: List of agent IDs to exclude (e.g., ['nexus'])
        top_k: Number of episodes to retrieve
        use_precomputed: Use pre-computed embeddings (Week 5, default False)
        external_dbs: List of external database configs (Week 6+, optional)
                     Example: [{'host': 'localhost', 'port': 8001, 'database': 'aria_memory',
                               'user': 'aria_superuser', 'password': '...', 'agent_id': 'aria'}]

    Returns:
        list: Episode dicts with:
            - episode_id: UUID
            - content: str
            - importance: float
            - tags: list
            - attribution: 'external' (always for external agents)
            - agent_id: Source agent ID (e.g., 'aria')
            - z_id: External agent's Z_ID (loaded from their GIC)
            - relevance_score: float (query similarity)

    Behavior:
        - If external_dbs is None or empty: Return [] (Week 4-5 behavior)
        - If external_dbs provided: Query each database and aggregate results (Week 6+)
        - Supports both on-the-fly and pre-computed paths
        - Gracefully handles connection errors (skip unavailable agents)

    Week 5+ Implementation:
        - Add agent_id column to episodes table
        - Filter: WHERE agent_id NOT IN (exclude_agent_ids)
        - Same semantic search as retrieve_self_episodes()
    """
    # Week 4-5: No external agents configured yet
    if external_dbs is None or len(external_dbs) == 0:
        logger.debug("No external agents configured, returning empty list")
        return []

    # Week 6+: Query external agents
    logger.info(f"Querying {len(external_dbs)} external agents for query: '{query[:50]}...'")

    all_external_episodes = []

    for db_config in external_dbs:
        agent_id = db_config.get('agent_id', 'unknown')

        # Skip if in exclude list
        if agent_id in exclude_agent_ids:
            logger.debug(f"Skipping agent '{agent_id}' (in exclude list)")
            continue

        try:
            # Connect to external agent DB
            logger.debug(f"Connecting to external agent '{agent_id}' at {db_config.get('host')}:{db_config.get('port')}")
            conn = psycopg2.connect(
                host=db_config.get('host'),
                port=db_config.get('port'),
                database=db_config.get('database'),
                user=db_config.get('user'),
                password=db_config.get('password')
            )

            # Load external agent's Z_ID (for AAG alignment checks)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT z_id_vector
                FROM consciousness.grounded_identity_core
                WHERE agent_id = %s;
            """, (agent_id,))
            result = cursor.fetchone()

            if result is None:
                logger.warning(f"Agent '{agent_id}' not found in GIC, skipping")
                cursor.close()
                conn.close()
                continue

            external_z_id = np.array(result[0], dtype=np.float64)
            logger.debug(f"Loaded Z_ID for external agent '{agent_id}': {external_z_id.shape}")

            # Query episodes from external agent
            if use_precomputed:
                # Use pre-computed embeddings path (Week 5+)
                from src.identity.retrieval.precomputed_embeddings import fetch_episodes_with_embeddings

                query_embedding = embed_text(query)

                # Note: This assumes external agent DB has same schema as NEXUS
                # In Week 6+, external DBs should have pre-computed embeddings too
                raw_episodes = fetch_episodes_with_embeddings(
                    query_embedding=query_embedding,
                    top_k=top_k,
                    threshold=0.3
                )
            else:
                # Use on-the-fly embeddings path (Week 4 fallback)
                cursor.execute("""
                    SELECT episode_id, content, importance_score, tags
                    FROM zep_episodic_memory
                    WHERE agent_id = %s
                    ORDER BY timestamp DESC
                    LIMIT 1000;
                """, (agent_id,))

                rows = cursor.fetchall()

                # Score episodes on-the-fly
                query_embedding = embed_text(query)
                scored_episodes = []

                for row in rows:
                    content_embedding = embed_text(row[1])  # content
                    relevance = compute_cosine_similarity(query_embedding, content_embedding)

                    if relevance >= 0.3:  # threshold
                        scored_episodes.append({
                            'episode_id': str(row[0]),
                            'content': row[1],
                            'importance_score': row[2],
                            'tags': row[3] if row[3] else [],
                            'similarity': relevance
                        })

                # Sort and limit
                scored_episodes.sort(key=lambda x: x['similarity'], reverse=True)
                raw_episodes = scored_episodes[:top_k]

            # Convert to standard format
            for ep in raw_episodes:
                all_external_episodes.append({
                    'episode_id': ep['episode_id'],
                    'content': ep['content'],
                    'importance': ep.get('importance_score', 0.5),
                    'tags': ep.get('tags', []),
                    'attribution': 'external',  # Mark as external
                    'agent_id': agent_id,  # Source agent
                    'z_id': external_z_id.tolist(),  # External agent's identity (convert numpy to list for JSON serialization)
                    'relevance_score': ep.get('similarity', 0.0)
                })

            logger.info(f"Retrieved {len(raw_episodes)} episodes from agent '{agent_id}'")

            cursor.close()
            conn.close()

        except psycopg2.Error as e:
            logger.error(f"Database error querying agent '{agent_id}': {e}")
            continue
        except Exception as e:
            logger.error(f"Unexpected error querying agent '{agent_id}': {e}")
            continue

    # Sort all external episodes by relevance
    all_external_episodes.sort(key=lambda x: x['relevance_score'], reverse=True)

    # Return top_k across all agents
    result = all_external_episodes[:top_k]
    logger.info(f"Retrieved {len(result)} total external episodes from {len(external_dbs)} agents")

    return result
