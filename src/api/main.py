"""
NEXUS Cerebro API V2.0.0
FastAPI Application - Core Endpoints
DÍA 5 FASE 4 - Base Implementation
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import os
import psycopg
from psycopg.types.json import Json
from contextlib import asynccontextmanager
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import time
import redis
import json as json_module
from sentence_transformers import SentenceTransformer

# FASE_8_UPGRADE: Hybrid Memory System
import sys
import os
# Add current directory to Python path for hybrid memory modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fact_extractor import extract_facts_from_content
from fact_schemas import FactQueryRequest, FactQueryResponse, HybridQueryRequest, HybridQueryResponse

# LAB_001: Emotional Salience
from emotional_salience_scorer import EmotionalSalienceScorer

# LAB_002: Decay Modulation
from decay_modulator import DecayModulator

# LAB_003: Sleep Consolidation (lazy import to avoid psycopg2 dependency at startup)
# from consolidation_engine import ConsolidationEngine

# LAB_005: Spreading Activation
from spreading_activation import SpreadingActivationEngine

# LAB_010: Attention Mechanism
from attention_mechanism import AttentionMechanism, MemoryCandidate

# LAB_011: Working Memory Buffer
from working_memory_buffer import WorkingMemoryBuffer

# LAB_001: Emotional Salience Scorer
from emotional_salience_scorer import EmotionalSalienceScorer

# NEXUS_CREW: Neo4j Real-Time Sync (Phase 2 - Priority 3)
from neo4j_sync import neo4j_sync

# LAB_006: Metacognition Logger
from metacognition_logger import MetacognitionLogger

# LAB_009: Memory Reconsolidation
from memory_reconsolidation import MemoryReconsolidationEngine

# LAB_007: Predictive Preloading
from predictive_preloading import PredictivePreloadingEngine

# LAB_012: Episodic Future Thinking
from episodic_future_thinking import FutureThinkingOrchestrator

# LAB_008: Emotional Contagion
from emotional_contagion import EmotionalContagionEngine

# LAB_002: Decay Modulation
from decay_modulator import DecayModulator

# LAB_003: Sleep Consolidation
from consolidation_engine import ConsolidationEngine

# LAB_004: Novelty Detection
from novelty_detector import NoveltyDetector

# LAB_005: Spreading Activation
from spreading_activation import SpreadingActivationEngine

# LAB_013: Dopamine System
import sys
experiments_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "experiments")
sys.path.insert(0, experiments_path)
from LAYER_4_Neurochemistry_Full.LAB_013_Dopamine_System import DopamineSystem

# LAB_014: Serotonin System
from LAYER_4_Neurochemistry_Full.LAB_014_Serotonin_System import SerotoninSystem

# LAB_015: Norepinephrine System
from LAYER_4_Neurochemistry_Full.LAB_015_Norepinephrine_System import NorepinephrineSystem

# LAB_016: Acetylcholine System
from LAYER_4_Neurochemistry_Full.LAB_016_Acetylcholine_System import AcetylcholineSystem

# LAB_017: GABA System
from LAYER_4_Neurochemistry_Full.LAB_017_GABA_System import GABASystem

# A/B Testing Framework
from ab_testing import get_ab_test_manager, TestVariant

# ============================================
# Configuration
# ============================================
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "nexus_postgresql")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "nexus_memory")
POSTGRES_USER = os.getenv("POSTGRES_USER", "nexus_superuser")

# Read password from Docker Secret
POSTGRES_PASSWORD_FILE = os.getenv("POSTGRES_PASSWORD_FILE", "/run/secrets/pg_superuser_password")
try:
    with open(POSTGRES_PASSWORD_FILE, 'r') as f:
        POSTGRES_PASSWORD = f.read().strip()
except FileNotFoundError:
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "default_password")

# ============================================
# Prometheus Metrics
# ============================================

# API Metrics
api_requests_total = Counter(
    'nexus_api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

api_request_duration_seconds = Histogram(
    'nexus_api_request_duration_seconds',
    'API request duration in seconds',
    ['method', 'endpoint']
)

# Memory Metrics
episodes_created_total = Counter(
    'nexus_episodes_created_total',
    'Total episodes created'
)

episodes_total = Gauge(
    'nexus_episodes_total',
    'Total episodes in database'
)

episodes_with_embeddings = Gauge(
    'nexus_episodes_with_embeddings',
    'Total episodes with embeddings generated'
)

embeddings_queue_depth = Gauge(
    'nexus_embeddings_queue_depth',
    'Current depth of embeddings queue',
    ['state']
)

# ============================================
# Database Connection
# ============================================
DB_CONN_STRING = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# ============================================
# Redis Configuration
# ============================================
REDIS_HOST = os.getenv("REDIS_HOST", "nexus_redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_CACHE_TTL = int(os.getenv("REDIS_CACHE_TTL", "300"))  # 5 minutes

# Read Redis password from Docker Secret
REDIS_PASSWORD_FILE = os.getenv("REDIS_PASSWORD_FILE", "/run/secrets/redis_password")
try:
    with open(REDIS_PASSWORD_FILE, 'r') as f:
        REDIS_PASSWORD = f.read().strip()
except FileNotFoundError:
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

# ============================================
# Embeddings Model Configuration
# ============================================
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# Global model instance (loaded in lifespan)
embeddings_model = None

# ============================================
# Pydantic Models
# ============================================
class MemoryActionRequest(BaseModel):
    action_type: str = Field(..., description="Type of action to perform")
    action_details: Dict[str, Any] = Field(default_factory=dict)
    context_state: Optional[Dict[str, Any]] = Field(default_factory=dict)
    tags: Optional[List[str]] = Field(default_factory=list)

class MemoryActionResponse(BaseModel):
    success: bool
    episode_id: Optional[str] = None
    timestamp: datetime
    message: str

class HealthResponse(BaseModel):
    status: str
    version: str
    agent_id: str
    database: str
    redis: Optional[str] = None
    queue_depth: Optional[int] = None
    timestamp: datetime

class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query text")
    limit: int = Field(default=10, ge=1, le=100, description="Maximum number of results")
    min_similarity: float = Field(default=0.5, ge=0.0, le=1.0, description="Minimum similarity threshold (0-1)")
    use_emotional_salience: bool = Field(default=False, description="LAB_001: Weight results by emotional salience")
    salience_boost_alpha: float = Field(default=0.5, ge=0.0, le=2.0, description="LAB_001: Salience boost factor (0=none, 0.5=moderate, 1.0=strong)")
    use_decay_modulation: bool = Field(default=False, description="LAB_002: Modulate decay rate by emotional salience (requires LAB_001)")
    decay_base: float = Field(default=0.95, ge=0.90, le=0.98, description="LAB_002: Daily decay rate (0.95=standard, 0.93=faster, 0.97=slower)")
    use_attention: bool = Field(default=False, description="LAB_010: Apply attention mechanism for noise filtering")
    attention_temperature: float = Field(default=0.5, ge=0.1, le=2.0, description="LAB_010: Attention temperature (lower=more concentrated)")

class SearchResult(BaseModel):
    episode_id: str
    content: str
    similarity_score: float
    importance_score: float
    tags: List[str]
    created_at: datetime
    # LAB_001: Emotional Salience metadata
    salience_score: Optional[float] = None
    original_similarity: Optional[float] = None
    salience_boost_applied: Optional[float] = None
    # LAB_002: Decay Modulation metadata
    age_days: Optional[int] = None
    base_decay: Optional[float] = None
    modulated_decay: Optional[float] = None
    modulation_factor: Optional[float] = None
    effective_age_days: Optional[float] = None

class SearchResponse(BaseModel):
    success: bool
    query: str
    count: int
    results: List[SearchResult]
    timestamp: datetime

# ============================================
# FASE_8_UPGRADE: Temporal Reasoning Models
# ============================================
class TemporalBeforeRequest(BaseModel):
    timestamp: datetime = Field(..., description="Get episodes before this timestamp")
    limit: int = Field(default=10, ge=1, le=100, description="Maximum number of results")
    tags: Optional[List[str]] = Field(default=None, description="Optional: filter by tags")

class TemporalAfterRequest(BaseModel):
    timestamp: datetime = Field(..., description="Get episodes after this timestamp")
    limit: int = Field(default=10, ge=1, le=100, description="Maximum number of results")
    tags: Optional[List[str]] = Field(default=None, description="Optional: filter by tags")

class TemporalRangeRequest(BaseModel):
    start: datetime = Field(..., description="Start of time range")
    end: datetime = Field(..., description="End of time range")
    limit: int = Field(default=50, ge=1, le=200, description="Maximum number of results")
    tags: Optional[List[str]] = Field(default=None, description="Optional: filter by tags")

class TemporalRelatedRequest(BaseModel):
    episode_id: str = Field(..., description="Episode UUID to find related episodes")
    relationship_type: Optional[str] = Field(default=None, description="Type: 'before', 'after', 'causes', 'effects', or None for all")

class TemporalLinkRequest(BaseModel):
    source_id: str = Field(..., description="Source episode UUID")
    target_id: str = Field(..., description="Target episode UUID")
    relationship: str = Field(..., description="Relationship type: 'before', 'after', 'causes', 'effects'")

class ABTestMetricRequest(BaseModel):
    variant: str = Field(..., description="Test variant: 'control' or 'treatment'")
    retrieval_time_ms: float = Field(..., description="Retrieval time in milliseconds")
    cache_hit: bool = Field(..., description="Whether cache was hit")
    num_results: int = Field(..., description="Number of results returned")
    context_coherence: Optional[float] = Field(default=None, description="Context coherence score (0-1)")
    primed_count: int = Field(default=0, description="Number of primed episodes (treatment only)")
    query_id: Optional[str] = Field(default=None, description="Optional query identifier")

class TemporalEpisode(BaseModel):
    episode_id: str
    content: str
    importance_score: float
    tags: List[str]
    created_at: datetime

class TemporalResponse(BaseModel):
    success: bool
    count: int
    episodes: List[TemporalEpisode]
    timestamp: datetime

# ============================================
# Lifespan Context Manager
# ============================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    global embeddings_model

    # Startup - Initialize Redis connection
    try:
        app.state.redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=REDIS_PASSWORD if REDIS_PASSWORD else None,
            decode_responses=True,
            socket_connect_timeout=5
        )
        # Test connection
        app.state.redis_client.ping()
        print(f"✓ Redis connected: {REDIS_HOST}:{REDIS_PORT}")
    except Exception as e:
        print(f"⚠ Redis connection failed: {e}")
        app.state.redis_client = None

    # Startup - Load embeddings model
    try:
        print(f"Loading embeddings model: {EMBEDDINGS_MODEL}")
        embeddings_model = SentenceTransformer(EMBEDDINGS_MODEL)
        print(f"✓ Embeddings model loaded successfully")
    except Exception as e:
        print(f"⚠ Embeddings model loading failed: {e}")
        embeddings_model = None

    yield

    # Shutdown - Close Redis connection
    if app.state.redis_client:
        app.state.redis_client.close()

# ============================================
# FastAPI App
# ============================================
app = FastAPI(
    title="NEXUS Cerebro API",
    description="Memory System API - V2.0.0",
    version="2.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# LAB_011: Global Working Memory Buffer
# ============================================
working_memory = WorkingMemoryBuffer(capacity=7)  # Miller's Law: 7±2 items

# ============================================
# LAB_001: Global Emotional Salience Scorer
# ============================================
emotional_scorer = EmotionalSalienceScorer()

# ============================================
# LAB_006: Global Metacognition Logger
# ============================================
metacognition_logger = MetacognitionLogger()

# ============================================
# LAB_009: Global Memory Reconsolidation Engine
# ============================================
reconsolidation_engine = MemoryReconsolidationEngine()

# ============================================
# LAB_007: Global Predictive Preloading Engine
# ============================================
predictive_preloader = PredictivePreloadingEngine()

# ============================================
# LAB_012: Global Future Thinking Orchestrator
# ============================================
future_thinking = FutureThinkingOrchestrator()

# ============================================
# LAB_008: Global Emotional Contagion Engine
# ============================================
emotional_contagion = EmotionalContagionEngine()

# ============================================
# LAB_002: Global Decay Modulator
# ============================================
decay_modulator = DecayModulator()

# ============================================
# LAB_003: Global Consolidation Engine
# ============================================
consolidation_engine = ConsolidationEngine()

# ============================================
# LAB_004: Global Novelty Detector
# ============================================
novelty_detector = NoveltyDetector()

# ============================================
# LAB_013: Global Dopamine System
# ============================================
dopamine_system = DopamineSystem(
    baseline_lr=0.1,
    rpe_sensitivity=0.5,
    motivation_decay=0.95,
    history_window=10
)

# ============================================
# LAB_014: Global Serotonin System
# ============================================
serotonin_system = SerotoninSystem(
    baseline_mood=0.5,
    impulse_threshold=0.7,
    patience_factor=1.0,
    reactivity_dampening=0.5,
    mood_inertia=0.95,
    history_window=20
)

# ============================================
# LAB_015: Global Norepinephrine System
# ============================================
norepinephrine_system = NorepinephrineSystem(
    baseline_arousal=0.5,
    stress_sensitivity=0.3,
    arousal_decay=0.95,
    optimal_arousal=0.6,
    focus_threshold=0.5,
    history_window=20
)

# ============================================
# LAB_016: Global Acetylcholine System
# ============================================
acetylcholine_system = AcetylcholineSystem(
    baseline_ach=0.5,
    amplification_gain=0.3,
    encoding_threshold=0.6,
    novelty_sensitivity=0.4,
    ach_decay=0.9,
    history_window=20
)

# ============================================
# LAB_017: Global GABA System
# ============================================
gaba_system = GABASystem(
    baseline_gaba=0.5,
    inhibition_strength=0.7,
    anxiety_threshold=0.6,
    anxiety_sensitivity=0.3,
    gaba_decay=0.9,
    history_window=20
)

# ============================================
# LAB_005: Global Spreading Activation Engine
# ============================================
spreading_activation = SpreadingActivationEngine()

# Prometheus Middleware for automatic tracking
@app.middleware("http")
async def prometheus_middleware(request, call_next):
    """Track all HTTP requests with Prometheus metrics"""
    start_time = time.time()

    # Execute request
    response = await call_next(request)

    # Calculate duration
    duration = time.time() - start_time

    # Record metrics
    endpoint = request.url.path
    method = request.method
    status_code = str(response.status_code)

    api_requests_total.labels(method=method, endpoint=endpoint, status=status_code).inc()
    api_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(duration)

    return response

# ============================================
# Helper Functions
# ============================================
def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg.connect(DB_CONN_STRING)
        return conn
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )

def get_redis_client():
    """Get Redis client from app state"""
    return app.state.redis_client if hasattr(app.state, 'redis_client') else None

def cache_get(key: str):
    """Get value from Redis cache"""
    try:
        redis_client = get_redis_client()
        if redis_client:
            value = redis_client.get(key)
            if value:
                return json_module.loads(value)
    except Exception as e:
        print(f"Cache get error: {e}")
    return None

def cache_set(key: str, value: any, ttl: int = REDIS_CACHE_TTL):
    """Set value in Redis cache with TTL"""
    try:
        redis_client = get_redis_client()
        if redis_client:
            redis_client.setex(
                key,
                ttl,
                json_module.dumps(value, default=str)
            )
    except Exception as e:
        print(f"Cache set error: {e}")

def cache_invalidate(pattern: str):
    """Invalidate cache keys matching pattern"""
    try:
        redis_client = get_redis_client()
        if redis_client:
            keys = redis_client.keys(pattern)
            if keys:
                redis_client.delete(*keys)
    except Exception as e:
        print(f"Cache invalidate error: {e}")

def generate_query_embedding(text: str):
    """Generate embedding for search query"""
    global embeddings_model

    if embeddings_model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Embeddings model not loaded"
        )

    try:
        # Truncate to 4000 chars (same as worker)
        text_truncated = text[:4000] if len(text) > 4000 else text

        # Generate embedding
        embedding = embeddings_model.encode(text_truncated)

        return embedding.tolist()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating embedding: {str(e)}"
        )

# ============================================
# Endpoints
# ============================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "service": "NEXUS Cerebro API",
        "version": "2.0.0",
        "status": "operational",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Advanced health check endpoint - checks PostgreSQL, Redis, and Queue depth"""
    db_status = "unknown"
    redis_status = "unknown"
    queue_depth = None
    overall_status = "healthy"

    # Check PostgreSQL
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            result = cur.fetchone()

            # Get queue depth
            cur.execute("""
                SELECT COUNT(*)
                FROM memory_system.embeddings_queue
                WHERE state IN ('pending', 'processing')
            """)
            queue_depth = cur.fetchone()[0]

        conn.close()
        db_status = "connected" if result else "disconnected"
    except Exception as e:
        db_status = f"error: {str(e)[:100]}"
        overall_status = "unhealthy"

    # Check Redis
    try:
        redis_client = get_redis_client()
        if redis_client:
            redis_client.ping()
            redis_status = "connected"
        else:
            redis_status = "not_initialized"
    except Exception as e:
        redis_status = f"error: {str(e)[:100]}"
        overall_status = "degraded"  # Redis failure is degraded, not unhealthy

    # Overall status evaluation
    if queue_depth and queue_depth > 1000:
        overall_status = "degraded"  # High queue depth is warning

    return HealthResponse(
        status=overall_status,
        version="2.0.0",
        agent_id="nexus",
        database=db_status,
        redis=redis_status,
        queue_depth=queue_depth,
        timestamp=datetime.now()
        )

@app.post("/memory/action", response_model=MemoryActionResponse, tags=["Memory"])
async def memory_action(request: MemoryActionRequest):
    """
    Create episodic memory entry
    Automatically triggers embeddings generation via database trigger
    """
    try:
        conn = get_db_connection()

        # Prepare content from action_details
        # FIXED: Use actual content field if exists, otherwise serialize full details
        if "content" in request.action_details:
            # Use explicit content field
            content = request.action_details["content"]
        elif request.action_details:
            # Serialize full action_details as JSON string for embeddings
            content = json_module.dumps(request.action_details, indent=2, default=str)
        else:
            # Fallback to action_type only
            content = request.action_type

        # Calculate importance_score (default 0.5, can be customized)
        importance_score = request.action_details.get("importance_score", 0.5) if request.action_details else 0.5

        # Insert into episodic memory
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO nexus_memory.zep_episodic_memory
                (content, importance_score, tags, metadata)
                VALUES (%s, %s, %s, %s)
                RETURNING episode_id, created_at
            """, (
                content,
                importance_score,
                request.tags or [],
                Json({
                    "action_type": request.action_type,
                    "action_details": request.action_details,
                    "context_state": request.context_state
                })
            ))

            result = cur.fetchone()
            episode_id = str(result[0])
            created_at = result[1]

        # NEXUS_CREW Phase 2 Priority 3: Real-time Neo4j Sync
        # NON-BLOCKING: Neo4j failures do NOT fail the API endpoint
        try:
            neo4j_sync.sync_episode(
                episode_id=episode_id,
                content=content,
                importance_score=importance_score,
                tags=request.tags or [],
                created_at=created_at
            )
        except Exception as neo4j_error:
            # Log error but continue - PostgreSQL is source of truth
            import logging
            logging.error(f"Neo4j sync failed for {episode_id}: {neo4j_error}")

        conn.commit()
        conn.close()

        # Invalidate episodes cache
        cache_invalidate("episodes:recent:*")

        # Increment Prometheus counter
        episodes_created_total.inc()

        return MemoryActionResponse(
            success=True,
            episode_id=episode_id,
            timestamp=created_at,
            message="Acción registrada exitosamente"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating memory: {str(e)}"
        )

@app.get("/memory/episodic/recent", tags=["Memory"])
async def get_recent_episodes(limit: int = 10):
    """Get recent episodic memories with Redis cache"""
    try:
        # Try cache first
        cache_key = f"episodes:recent:{limit}"
        cached_data = cache_get(cache_key)
        if cached_data:
            cached_data["cached"] = True
            return cached_data

        # Cache miss - query database
        conn = get_db_connection()

        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    episode_id,
                    content,
                    importance_score,
                    tags,
                    created_at,
                    embedding IS NOT NULL as has_embedding
                FROM nexus_memory.zep_episodic_memory
                ORDER BY created_at DESC
                LIMIT %s
            """, (limit,))

            results = cur.fetchall()

        conn.close()

        episodes = []
        for row in results:
            episodes.append({
                "episode_id": str(row[0]),
                "content": row[1],
                "importance_score": row[2],
                "tags": row[3] or [],
                "created_at": row[4].isoformat(),
                "has_embedding": row[5]
            })

        response = {
            "success": True,
            "count": len(episodes),
            "episodes": episodes,
            "cached": False
        }

        # Store in cache
        cache_set(cache_key, response)

        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching episodes: {str(e)}"
        )

@app.post("/memory/search", response_model=SearchResponse, tags=["Memory"])
async def search_memories(request: SearchRequest):
    """
    Semantic search using vector embeddings
    Uses cosine similarity with pgvector to find most relevant episodes
    """
    try:
        # Generate embedding for search query
        query_embedding = generate_query_embedding(request.query)

        # Perform vector similarity search
        conn = get_db_connection()

        with conn.cursor() as cur:
            # Cosine similarity search using pgvector <=> operator
            # Lower distance = higher similarity
            # Convert distance to similarity score (1 - distance)
            cur.execute("""
                SELECT
                    episode_id,
                    content,
                    importance_score,
                    tags,
                    created_at,
                    1 - (embedding <=> %s::vector) as similarity_score
                FROM nexus_memory.zep_episodic_memory
                WHERE embedding IS NOT NULL
                    AND 1 - (embedding <=> %s::vector) >= %s
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """, (
                query_embedding,
                query_embedding,
                request.min_similarity,
                query_embedding,
                request.limit
            ))

            results = cur.fetchall()

        # Track access for retrieved episodes (intelligent decay feature)
        if results:
            episode_ids = [str(row[0]) for row in results]
            for ep_id in episode_ids:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT nexus_memory.update_access_tracking(%s::uuid)
                    """, (ep_id,))
            conn.commit()

        conn.close()

        # Initialize search_results (will be populated below)
        search_results = []

        # LAB_010: Apply attention mechanism for noise filtering if enabled
        if request.use_attention and results:
            try:
                # Convert results to MemoryCandidate format
                candidates = []
                for row in results:
                    episode_id = str(row[0])
                    content = str(row[1])
                    embedding = query_embedding  # Use query embedding as proxy (attention will reweight)
                    created_at = row[4]
                    importance_score = float(row[2])
                    tags = row[3] or []

                    # LAB_001: Calculate REAL emotional salience (not hardcoded 0.5)
                    try:
                        salience_result = emotional_scorer.calculate_salience(episode_id, created_at)
                        emotional_salience = salience_result.salience_score
                    except:
                        # Fallback if no emotional context in DB
                        emotional_salience = 0.5

                    candidate = MemoryCandidate(
                        episode_id=episode_id,
                        embedding=embedding,
                        created_at=created_at,
                        importance_score=importance_score,
                        emotional_salience=emotional_salience,  # LAB_001 real score!
                        tags=tags
                    )
                    candidates.append(candidate)

                # Initialize attention mechanism
                attention_mechanism = AttentionMechanism(
                    semantic_weight=0.6,
                    recency_weight=0.2,
                    salience_weight=0.15,
                    context_weight=0.05,
                    attention_threshold=0.04,
                    temperature=request.attention_temperature
                )

                # Apply attention (filter noise)
                attended_candidates, attention_weights = attention_mechanism.attend(
                    query_embedding,
                    candidates,
                    query_context={'tags': []},  # Could extract from query later
                    apply_filter=True
                )

                # Update results to only include attended episodes
                attended_episode_ids = {c.episode_id for c in attended_candidates}
                results = [row for row in results if str(row[0]) in attended_episode_ids]

                print(f"LAB_010: Attention filtered {len(candidates)} → {len(results)} episodes")

            except Exception as e:
                print(f"LAB_010: Attention mechanism failed, falling back to standard search: {str(e)}")
                # Continue with all results

        # LAB_001: Apply emotional salience re-ranking if enabled
        if request.use_emotional_salience and results:
            try:
                # Initialize scorer (connects inside nexus_postgresql container)
                scorer = EmotionalSalienceScorer(
                    db_host=POSTGRES_HOST,
                    db_port=POSTGRES_PORT,
                    db_name=POSTGRES_DB,
                    db_user=POSTGRES_USER,
                    db_password=POSTGRES_PASSWORD
                )

                # Calculate salience for each result
                reranked_results = []
                for row in results:
                    episode_id = str(row[0])
                    original_similarity = float(row[5])
                    timestamp = row[4]

                    # Calculate emotional salience
                    salience = scorer.calculate_salience(episode_id, timestamp)

                    # Apply re-ranking: final_score = similarity * (1 + alpha * salience)
                    final_score = original_similarity * (1 + request.salience_boost_alpha * salience.total_score)

                    reranked_results.append({
                        'row': row,
                        'original_similarity': original_similarity,
                        'salience_score': salience.total_score,
                        'final_score': final_score
                    })

                # LAB_002: Apply decay modulation if enabled (requires LAB_001 salience)
                if request.use_decay_modulation:
                    modulator = DecayModulator(decay_base=request.decay_base)

                    for item in reranked_results:
                        row = item['row']
                        created_at = row[4]  # timestamp

                        # Calculate decay-modulated score
                        decay_result = modulator.calculate_decay_modulated_score(
                            similarity=item['final_score'],  # Use LAB_001 score as input
                            created_at=created_at,
                            salience_score=item['salience_score']
                        )

                        # Update final score with decay modulation
                        item['final_score'] = decay_result.modulated_score

                        # Store decay metadata
                        item['decay_metadata'] = {
                            'age_days': decay_result.actual_age_days,
                            'base_decay': decay_result.base_decay,
                            'modulated_decay': decay_result.modulated_decay,
                            'modulation_factor': decay_result.modulation_factor,
                            'effective_age_days': decay_result.effective_age_days
                        }

                # Sort by final score
                reranked_results.sort(key=lambda x: x['final_score'], reverse=True)

                # Build results with salience metadata
                for item in reranked_results[:request.limit]:  # Re-apply limit after re-ranking
                    row = item['row']

                    # Prepare decay metadata if LAB_002 was applied
                    decay_meta = item.get('decay_metadata', {})

                    search_results.append(SearchResult(
                        episode_id=str(row[0]),
                        content=row[1],
                        similarity_score=item['final_score'],  # New weighted score
                        importance_score=float(row[2]),
                        tags=row[3] or [],
                        created_at=row[4],
                        # LAB_001: Salience metadata
                        salience_score=item['salience_score'],
                        original_similarity=item['original_similarity'],
                        salience_boost_applied=request.salience_boost_alpha,
                        # LAB_002: Decay metadata (if applied)
                        age_days=decay_meta.get('age_days'),
                        base_decay=decay_meta.get('base_decay'),
                        modulated_decay=decay_meta.get('modulated_decay'),
                        modulation_factor=decay_meta.get('modulation_factor'),
                        effective_age_days=decay_meta.get('effective_age_days')
                    ))

            except Exception as e:
                # If salience scoring fails, fall back to standard results
                print(f"LAB_001: Emotional salience scoring failed, falling back to standard search: {str(e)}")
                request.use_emotional_salience = False  # Disable for fallback

        # Build search results (standard or fallback)
        if not request.use_emotional_salience:
            for row in results:
                search_results.append(SearchResult(
                    episode_id=str(row[0]),
                    content=row[1],
                    similarity_score=float(row[5]),
                    importance_score=float(row[2]),
                    tags=row[3] or [],
                    created_at=row[4]
                ))

        return SearchResponse(
            success=True,
            query=request.query,
            count=len(search_results),
            results=search_results,
            timestamp=datetime.now()
        )

    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error performing search: {str(e)}"
        )

@app.get("/stats", tags=["Stats"])
async def get_stats():
    """Get database statistics and update Prometheus gauges"""
    try:
        conn = get_db_connection()

        with conn.cursor() as cur:
            # Count episodic memories
            cur.execute("SELECT COUNT(*) FROM nexus_memory.zep_episodic_memory")
            total_episodes = cur.fetchone()[0]

            # Count embeddings queue
            cur.execute("SELECT state, COUNT(*) FROM memory_system.embeddings_queue GROUP BY state")
            queue_stats = {row[0]: row[1] for row in cur.fetchall()}

            # Count with embeddings
            cur.execute("SELECT COUNT(*) FROM nexus_memory.zep_episodic_memory WHERE embedding IS NOT NULL")
            total_with_embeddings = cur.fetchone()[0]

        conn.close()

        # Update Prometheus gauges
        episodes_total.set(total_episodes)
        episodes_with_embeddings.set(total_with_embeddings)

        # Update queue depth metrics
        for state in ['pending', 'processing', 'done', 'dead']:
            count = queue_stats.get(state, 0)
            embeddings_queue_depth.labels(state=state).set(count)

        return {
            "success": True,
            "agent_id": "nexus",
            "stats": {
                "total_episodes": total_episodes,
                "episodes_with_embeddings": total_with_embeddings,
                "embeddings_queue": queue_stats
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching stats: {str(e)}"
        )

# ============================================
# FASE_8_UPGRADE: Temporal Reasoning Endpoints
# ============================================

@app.post("/memory/temporal/before", response_model=TemporalResponse, tags=["Temporal"])
async def get_episodes_before(request: TemporalBeforeRequest):
    """
    Get episodes that occurred before a specific timestamp
    Ordered by timestamp DESC (most recent first)
    """
    try:
        conn = get_db_connection()

        with conn.cursor() as cur:
            # Base query
            query = """
                SELECT episode_id, content, importance_score, tags, created_at
                FROM nexus_memory.zep_episodic_memory
                WHERE created_at < %s
            """
            params = [request.timestamp]

            # Optional: filter by tags
            if request.tags:
                query += " AND tags && %s"
                params.append(request.tags)

            query += " ORDER BY created_at DESC LIMIT %s"
            params.append(request.limit)

            cur.execute(query, params)
            results = cur.fetchall()

        conn.close()

        # Build response
        episodes = []
        for row in results:
            episodes.append(TemporalEpisode(
                episode_id=str(row[0]),
                content=row[1],
                importance_score=float(row[2]),
                tags=row[3] or [],
                created_at=row[4]
            ))

        return TemporalResponse(
            success=True,
            count=len(episodes),
            episodes=episodes,
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching episodes before timestamp: {str(e)}"
        )

@app.post("/memory/temporal/after", response_model=TemporalResponse, tags=["Temporal"])
async def get_episodes_after(request: TemporalAfterRequest):
    """
    Get episodes that occurred after a specific timestamp
    Ordered by timestamp ASC (oldest first)
    """
    try:
        conn = get_db_connection()

        with conn.cursor() as cur:
            # Base query
            query = """
                SELECT episode_id, content, importance_score, tags, created_at
                FROM nexus_memory.zep_episodic_memory
                WHERE created_at > %s
            """
            params = [request.timestamp]

            # Optional: filter by tags
            if request.tags:
                query += " AND tags && %s"
                params.append(request.tags)

            query += " ORDER BY created_at ASC LIMIT %s"
            params.append(request.limit)

            cur.execute(query, params)
            results = cur.fetchall()

        conn.close()

        # Build response
        episodes = []
        for row in results:
            episodes.append(TemporalEpisode(
                episode_id=str(row[0]),
                content=row[1],
                importance_score=float(row[2]),
                tags=row[3] or [],
                created_at=row[4]
            ))

        return TemporalResponse(
            success=True,
            count=len(episodes),
            episodes=episodes,
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching episodes after timestamp: {str(e)}"
        )

@app.post("/memory/temporal/range", response_model=TemporalResponse, tags=["Temporal"])
async def get_episodes_in_range(request: TemporalRangeRequest):
    """
    Get episodes that occurred between two timestamps
    Ordered by timestamp ASC (chronological order)
    """
    try:
        conn = get_db_connection()

        with conn.cursor() as cur:
            # Base query
            query = """
                SELECT episode_id, content, importance_score, tags, created_at
                FROM nexus_memory.zep_episodic_memory
                WHERE created_at BETWEEN %s AND %s
            """
            params = [request.start, request.end]

            # Optional: filter by tags
            if request.tags:
                query += " AND tags && %s"
                params.append(request.tags)

            query += " ORDER BY created_at ASC LIMIT %s"
            params.append(request.limit)

            cur.execute(query, params)
            results = cur.fetchall()

        # Track access for retrieved episodes
        if results:
            episode_ids = [str(row[0]) for row in results]
            for ep_id in episode_ids:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT nexus_memory.update_access_tracking(%s::uuid)
                    """, (ep_id,))
            conn.commit()

        conn.close()

        # Build response
        episodes = []
        for row in results:
            episodes.append(TemporalEpisode(
                episode_id=str(row[0]),
                content=row[1],
                importance_score=float(row[2]),
                tags=row[3] or [],
                created_at=row[4]
            ))

        return TemporalResponse(
            success=True,
            count=len(episodes),
            episodes=episodes,
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching episodes in range: {str(e)}"
        )

@app.post("/memory/temporal/related", response_model=TemporalResponse, tags=["Temporal"])
async def get_temporally_related(request: TemporalRelatedRequest):
    """
    Get episodes linked via temporal_refs metadata
    Uses PostgreSQL function get_temporal_refs() from Phase 1
    """
    try:
        conn = get_db_connection()

        with conn.cursor() as cur:
            # Use Phase 1 SQL function to get temporal refs
            if request.relationship_type:
                # Get specific relationship type
                cur.execute("""
                    SELECT ref_episode_id
                    FROM nexus_memory.get_temporal_refs(%s::uuid, %s)
                """, (request.episode_id, request.relationship_type))
            else:
                # Get all relationships
                cur.execute("""
                    SELECT ref_episode_id
                    FROM nexus_memory.get_temporal_refs(%s::uuid)
                """, (request.episode_id,))

            ref_ids = [row[0] for row in cur.fetchall()]

            # If no references found, return empty
            if not ref_ids:
                conn.close()
                return TemporalResponse(
                    success=True,
                    count=0,
                    episodes=[],
                    timestamp=datetime.now()
                )

            # Fetch full episode data for referenced episodes
            cur.execute("""
                SELECT episode_id, content, importance_score, tags, created_at
                FROM nexus_memory.zep_episodic_memory
                WHERE episode_id = ANY(%s)
                ORDER BY created_at DESC
            """, (ref_ids,))

            results = cur.fetchall()

        conn.close()

        # Build response
        episodes = []
        for row in results:
            episodes.append(TemporalEpisode(
                episode_id=str(row[0]),
                content=row[1],
                importance_score=float(row[2]),
                tags=row[3] or [],
                created_at=row[4]
            ))

        return TemporalResponse(
            success=True,
            count=len(episodes),
            episodes=episodes,
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching related episodes: {str(e)}"
        )

@app.post("/memory/temporal/link", tags=["Temporal"])
async def link_episodes_temporally(request: TemporalLinkRequest):
    """
    Create temporal relationship between two episodes
    Uses PostgreSQL function add_temporal_ref() from Phase 1
    """
    try:
        # Validate relationship type
        valid_types = ['before', 'after', 'causes', 'effects']
        if request.relationship not in valid_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid relationship type. Must be one of: {valid_types}"
            )

        conn = get_db_connection()

        with conn.cursor() as cur:
            # Use Phase 1 SQL function to add temporal reference
            cur.execute("""
                SELECT nexus_memory.add_temporal_ref(%s::uuid, %s::uuid, %s)
            """, (request.source_id, request.target_id, request.relationship))

        conn.commit()
        conn.close()

        # Invalidate cache (if temporal queries are cached in future)
        cache_invalidate(f"temporal:related:{request.source_id}")

        return {
            "success": True,
            "message": f"Temporal link created: {request.source_id} --{request.relationship}--> {request.target_id}",
            "timestamp": datetime.now()
        }

    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating temporal link: {str(e)}"
        )

# ============================================
# FASE_8_UPGRADE: Consciousness Integration
# ============================================

class ConsciousnessUpdateRequest(BaseModel):
    state_type: str = Field(..., description="Type: 'emotional' or 'somatic'")
    state_data: Dict[str, Any] = Field(..., description="State values (e.g., joy, trust, valence, arousal)")
    importance: float = Field(default=0.7, ge=0.0, le=1.0)
    tags: Optional[List[str]] = Field(default_factory=list)
    auto_link_previous: bool = Field(default=True, description="Automatically link to previous state")

class ConsciousnessUpdateResponse(BaseModel):
    success: bool
    episode_id: str
    linked_to_previous: Optional[str] = None
    temporal_chain_length: int = 0
    timestamp: datetime

class ConsciousnessStateData(BaseModel):
    state_data: Optional[Dict[str, Any]] = None
    episode_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    chain_length: Optional[int] = None

class ConsciousnessCurrentResponse(BaseModel):
    success: bool
    emotional_8d: Optional[ConsciousnessStateData] = None
    somatic_7d: Optional[ConsciousnessStateData] = None

# ============================================
# Intelligent Decay Models
# ============================================
class DecayAnalysisRequest(BaseModel):
    limit: int = Field(default=100, ge=1, le=1000, description="Max episodes to analyze")
    min_age_days: int = Field(default=30, ge=0, description="Only analyze episodes older than this")

class DecayScoreDistribution(BaseModel):
    score_category: str
    episode_count: int
    avg_score: float

class DecayAnalysisResponse(BaseModel):
    success: bool
    total_analyzed: int
    distribution: List[DecayScoreDistribution]
    low_value_count: int  # decay_score < 0.2
    high_value_count: int  # decay_score > 0.7
    timestamp: datetime

class PruningPreviewRequest(BaseModel):
    min_score_threshold: float = Field(default=0.2, ge=0.0, le=1.0)
    min_age_days: int = Field(default=90, ge=30)
    max_prune_count: int = Field(default=100, ge=1, le=500)

class PruningCandidate(BaseModel):
    episode_id: str
    content_preview: str
    decay_score: float
    importance_score: float
    age_days: int
    tags: List[str]

class PruningPreviewResponse(BaseModel):
    success: bool
    candidate_count: int
    candidates: List[PruningCandidate]
    would_prune: int
    protected_count: int
    timestamp: datetime

class PruningExecuteRequest(BaseModel):
    min_score_threshold: float = Field(default=0.2, ge=0.0, le=1.0)
    min_age_days: int = Field(default=90, ge=30)
    max_prune_count: int = Field(default=100, ge=1, le=500)
    dry_run: bool = Field(default=True, description="Safety: default to dry-run mode")

class PruningExecuteResponse(BaseModel):
    success: bool
    pruned_count: int
    dry_run: bool
    timestamp: datetime

@app.post("/memory/consciousness/update", response_model=ConsciousnessUpdateResponse, tags=["Consciousness"])
async def update_consciousness_state(request: ConsciousnessUpdateRequest):
    """
    Update consciousness state (emotional or somatic) with automatic temporal linking

    Automatically links to the previous state of the same type, creating temporal chains
    that track consciousness evolution over time.
    """
    try:
        # Validate state type
        if request.state_type not in ["emotional", "somatic"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="state_type must be 'emotional' or 'somatic'"
            )

        # Build tags
        tags = request.tags.copy()
        tags.extend(["consciousness", f"{request.state_type}_state"])

        # Create episode content
        content = f"Consciousness {request.state_type} state update: {json_module.dumps(request.state_data, indent=2)}"

        # Get database connection
        conn = get_db_connection()

        previous_episode_id = None
        chain_length = 0

        # Find previous state of same type (if auto_link enabled)
        if request.auto_link_previous:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT episode_id, metadata
                    FROM nexus_memory.zep_episodic_memory
                    WHERE %s = ANY(tags)
                    ORDER BY created_at DESC
                    LIMIT 1
                """, (f"{request.state_type}_state",))

                previous = cur.fetchone()
                if previous:
                    previous_episode_id = str(previous[0])

                    # Calculate chain length from previous state
                    prev_metadata = previous[1] or {}
                    prev_chain_length = prev_metadata.get("temporal_chain_length", 0)
                    chain_length = prev_chain_length + 1

        # Create new episode
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO nexus_memory.zep_episodic_memory
                (content, importance_score, tags, metadata)
                VALUES (%s, %s, %s, %s)
                RETURNING episode_id, created_at
            """, (
                content,
                request.importance,
                tags,
                Json({
                    "state_type": request.state_type,
                    "state_data": request.state_data,
                    "temporal_chain_length": chain_length
                })
            ))

            result = cur.fetchone()
            new_episode_id = str(result[0])
            created_at = result[1]

        # Create temporal link if previous exists
        if previous_episode_id and request.auto_link_previous:
            with conn.cursor() as cur:
                # Link: new_episode --after--> previous_episode
                cur.execute("""
                    SELECT nexus_memory.add_temporal_ref(%s::uuid, %s::uuid, 'after')
                """, (new_episode_id, previous_episode_id))

        conn.commit()
        conn.close()

        # Invalidate cache
        cache_invalidate("consciousness:*")

        # Increment metrics
        episodes_created_total.inc()

        return ConsciousnessUpdateResponse(
            success=True,
            episode_id=new_episode_id,
            linked_to_previous=previous_episode_id,
            temporal_chain_length=chain_length,
            timestamp=created_at
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating consciousness state: {str(e)}"
        )

@app.get("/memory/consciousness/current", response_model=ConsciousnessCurrentResponse, tags=["Consciousness"])
async def get_current_consciousness_state():
    """
    Get current consciousness state (emotional 8D + somatic 7D)

    Retrieves the most recent emotional and somatic states from episodic memory.
    Returns the state_data from metadata along with episode IDs and timestamps.
    """
    try:
        conn = get_db_connection()

        emotional_state = None
        somatic_state = None

        # Get latest emotional state
        with conn.cursor() as cur:
            cur.execute("""
                SELECT episode_id, metadata, created_at
                FROM nexus_memory.zep_episodic_memory
                WHERE 'emotional_state' = ANY(tags)
                ORDER BY created_at DESC
                LIMIT 1
            """)

            row = cur.fetchone()
            if row:
                episode_id, metadata, created_at = row
                metadata_dict = metadata or {}
                emotional_state = ConsciousnessStateData(
                    state_data=metadata_dict.get("state_data"),
                    episode_id=str(episode_id),
                    timestamp=created_at,
                    chain_length=metadata_dict.get("temporal_chain_length", 0)
                )

        # Get latest somatic state
        with conn.cursor() as cur:
            cur.execute("""
                SELECT episode_id, metadata, created_at
                FROM nexus_memory.zep_episodic_memory
                WHERE 'somatic_state' = ANY(tags)
                ORDER BY created_at DESC
                LIMIT 1
            """)

            row = cur.fetchone()
            if row:
                episode_id, metadata, created_at = row
                metadata_dict = metadata or {}
                somatic_state = ConsciousnessStateData(
                    state_data=metadata_dict.get("state_data"),
                    episode_id=str(episode_id),
                    timestamp=created_at,
                    chain_length=metadata_dict.get("temporal_chain_length", 0)
                )

        conn.close()

        return ConsciousnessCurrentResponse(
            success=True,
            emotional_8d=emotional_state,
            somatic_7d=somatic_state
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving consciousness state: {str(e)}"
        )

# ============================================
# Intelligent Decay Endpoints
# ============================================

@app.post("/memory/analysis/decay-scores", response_model=DecayAnalysisResponse, tags=["Intelligent Decay"])
async def analyze_decay_scores(request: DecayAnalysisRequest):
    """
    Analyze decay score distribution across episodic memory

    Calculates decay scores using the intelligent decay algorithm:
    - Importance factor (50%): Original importance_score
    - Recency factor (30%): Exponential decay based on age
    - Access factor (20%): Frequency + recency of access

    Returns distribution by score category and counts
    """
    try:
        conn = get_db_connection()

        with conn.cursor() as cur:
            # Calculate decay scores and distribution
            cur.execute("""
                WITH decay_scores AS (
                    SELECT
                        episode_id,
                        nexus_memory.calculate_decay_score(
                            importance_score,
                            created_at,
                            metadata
                        ) as decay_score,
                        EXTRACT(EPOCH FROM (NOW() - created_at)) / 86400.0 as age_days
                    FROM nexus_memory.zep_episodic_memory
                    WHERE EXTRACT(EPOCH FROM (NOW() - created_at)) / 86400.0 >= %s
                    LIMIT %s
                )
                SELECT
                    CASE
                        WHEN decay_score >= 0.8 THEN 'Very High (0.8-1.0)'
                        WHEN decay_score >= 0.6 THEN 'High (0.6-0.8)'
                        WHEN decay_score >= 0.4 THEN 'Medium (0.4-0.6)'
                        WHEN decay_score >= 0.2 THEN 'Low (0.2-0.4)'
                        ELSE 'Very Low (0.0-0.2)'
                    END as score_category,
                    COUNT(*) as episode_count,
                    ROUND(AVG(decay_score)::NUMERIC, 3) as avg_score
                FROM decay_scores
                GROUP BY CASE
                    WHEN decay_score >= 0.8 THEN 'Very High (0.8-1.0)'
                    WHEN decay_score >= 0.6 THEN 'High (0.6-0.8)'
                    WHEN decay_score >= 0.4 THEN 'Medium (0.4-0.6)'
                    WHEN decay_score >= 0.2 THEN 'Low (0.2-0.4)'
                    ELSE 'Very Low (0.0-0.2)'
                END
                ORDER BY MIN(decay_score) DESC
            """, (request.min_age_days, request.limit))

            distribution_rows = cur.fetchall()

            # Count low/high value episodes
            cur.execute("""
                WITH decay_scores AS (
                    SELECT
                        nexus_memory.calculate_decay_score(
                            importance_score,
                            created_at,
                            metadata
                        ) as decay_score
                    FROM nexus_memory.zep_episodic_memory
                    WHERE EXTRACT(EPOCH FROM (NOW() - created_at)) / 86400.0 >= %s
                    LIMIT %s
                )
                SELECT
                    SUM(CASE WHEN decay_score < 0.2 THEN 1 ELSE 0 END) as low_value_count,
                    SUM(CASE WHEN decay_score > 0.7 THEN 1 ELSE 0 END) as high_value_count,
                    COUNT(*) as total_count
                FROM decay_scores
            """, (request.min_age_days, request.limit))

            counts = cur.fetchone()

        conn.close()

        # Build distribution
        distribution = []
        for row in distribution_rows:
            distribution.append(DecayScoreDistribution(
                score_category=row[0],
                episode_count=row[1],
                avg_score=float(row[2])
            ))

        return DecayAnalysisResponse(
            success=True,
            total_analyzed=counts[2],
            distribution=distribution,
            low_value_count=counts[0],
            high_value_count=counts[1],
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing decay scores: {str(e)}"
        )

@app.post("/memory/pruning/preview", response_model=PruningPreviewResponse, tags=["Intelligent Decay"])
async def preview_pruning(request: PruningPreviewRequest):
    """
    Preview episodes that would be pruned based on decay scores

    Safety rules (never prune):
    - Episodes with importance_score > 0.8
    - Episodes with protected tags: milestone, critical, protected, consciousness
    - Episodes younger than min_age_days
    - Episodes accessed in last 7 days

    Returns list of pruning candidates for review
    """
    try:
        conn = get_db_connection()

        protected_tags = ['milestone', 'critical', 'protected', 'consciousness']

        with conn.cursor() as cur:
            # Find pruning candidates
            cur.execute("""
                WITH decay_scores AS (
                    SELECT
                        episode_id,
                        content,
                        importance_score,
                        tags,
                        created_at,
                        metadata,
                        nexus_memory.calculate_decay_score(
                            importance_score,
                            created_at,
                            metadata
                        ) as decay_score,
                        EXTRACT(EPOCH FROM (NOW() - created_at)) / 86400.0 as age_days,
                        CASE
                            WHEN metadata->'access_tracking'->>'last_accessed' IS NOT NULL THEN
                                EXTRACT(EPOCH FROM (NOW() - (metadata->'access_tracking'->>'last_accessed')::TIMESTAMPTZ)) / 86400.0
                            ELSE
                                999999  -- Never accessed
                        END as last_accessed_days
                    FROM nexus_memory.zep_episodic_memory
                )
                SELECT
                    episode_id,
                    LEFT(content, 100) as content_preview,
                    decay_score,
                    importance_score,
                    age_days,
                    tags,
                    CASE
                        WHEN importance_score > 0.8 THEN 1
                        WHEN tags && %s THEN 1
                        WHEN age_days < %s THEN 1
                        WHEN last_accessed_days < 7 THEN 1
                        ELSE 0
                    END as is_protected
                FROM decay_scores
                WHERE decay_score < %s
                    AND age_days >= %s
                ORDER BY decay_score ASC
                LIMIT %s
            """, (protected_tags, request.min_age_days, request.min_score_threshold,
                  request.min_age_days, request.max_prune_count))

            candidates_rows = cur.fetchall()

        conn.close()

        # Build candidate list
        candidates = []
        protected_count = 0
        would_prune = 0

        for row in candidates_rows:
            is_protected = row[6]

            if is_protected:
                protected_count += 1
            else:
                would_prune += 1

            candidates.append(PruningCandidate(
                episode_id=str(row[0]),
                content_preview=row[1],
                decay_score=float(row[2]),
                importance_score=float(row[3]),
                age_days=int(row[4]),
                tags=row[5] or []
            ))

        return PruningPreviewResponse(
            success=True,
            candidate_count=len(candidates),
            candidates=candidates,
            would_prune=would_prune,
            protected_count=protected_count,
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error previewing pruning: {str(e)}"
        )

@app.post("/memory/pruning/execute", response_model=PruningExecuteResponse, tags=["Intelligent Decay"])
async def execute_pruning(request: PruningExecuteRequest):
    """
    Execute memory pruning based on decay scores

    **IMPORTANT:** Defaults to dry_run=True for safety

    Safety mechanisms:
    - Never prunes importance_score > 0.8
    - Never prunes protected tags
    - Never prunes episodes < min_age_days old
    - Never prunes recently accessed episodes
    - Caps at max_prune_count per operation

    Pruned episodes are soft-deleted (moved to archive table, not lost)
    """
    try:
        if request.dry_run:
            # Dry run mode: just count what would be pruned
            conn = get_db_connection()

            protected_tags = ['milestone', 'critical', 'protected', 'consciousness']

            with conn.cursor() as cur:
                cur.execute("""
                    WITH decay_scores AS (
                        SELECT
                            episode_id,
                            nexus_memory.calculate_decay_score(
                                importance_score,
                                created_at,
                                metadata
                            ) as decay_score,
                            importance_score,
                            EXTRACT(EPOCH FROM (NOW() - created_at)) / 86400.0 as age_days,
                            tags,
                            CASE
                                WHEN metadata->'access_tracking'->>'last_accessed' IS NOT NULL THEN
                                    EXTRACT(EPOCH FROM (NOW() - (metadata->'access_tracking'->>'last_accessed')::TIMESTAMPTZ)) / 86400.0
                                ELSE
                                    999999
                            END as last_accessed_days
                        FROM nexus_memory.zep_episodic_memory
                    )
                    SELECT COUNT(*)
                    FROM decay_scores
                    WHERE decay_score < %s
                        AND age_days >= %s
                        AND importance_score <= 0.8
                        AND NOT (tags && %s)
                        AND last_accessed_days >= 7
                    LIMIT %s
                """, (request.min_score_threshold, request.min_age_days,
                      protected_tags, request.max_prune_count))

                would_prune_count = cur.fetchone()[0]

            conn.close()

            return PruningExecuteResponse(
                success=True,
                pruned_count=would_prune_count,
                dry_run=True,
                timestamp=datetime.now()
            )
        else:
            # ACTUAL PRUNING - NOT IMPLEMENTED YET
            # TODO: Implement archive table and soft delete logic
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="Actual pruning not yet implemented. Create archive table first."
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing pruning: {str(e)}"
        )

@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

# ============================================
# FASE_8_UPGRADE: Hybrid Memory Endpoints
# ============================================

@app.post("/memory/facts", response_model=FactQueryResponse, tags=["Hybrid Memory"])
async def query_facts(request: FactQueryRequest):
    """
    Query extracted facts directly from episode metadata

    Fast fact retrieval without semantic search (< 5ms)

    **Valid fact_type values (from EpisodeFacts model):**
    - Versioning: nexus_version, api_version
    - Metrics: accuracy_percent, latency_ms, episode_count, query_count, test_count, success_rate
    - Status: status, phase_number, session_number, completion_percent
    - Features: feature_name, implementation_time_hours, lines_of_code, files_created, files_modified
    - Decay: decay_score, importance_override
    - Benchmarks: benchmark_name, benchmark_score, baseline_score
    - Errors: bug_count, error_count
    - Temporal: duration_hours, start_date, end_date
    - GitHub: commit_hash, pull_request_number
    - Custom: custom (extensible dict)
    - Metadata: extraction_method, extraction_confidence, last_updated

    **Example:** fact_type="nexus_version"
    """
    start_time = time.time()

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Build query
                query_parts = ["SELECT episode_id, content, metadata, created_at, tags FROM nexus_memory.zep_episodic_memory"]
                where_clauses = []
                params = []

                # Filter by tags if specified
                if request.filter_tags:
                    where_clauses.append("tags && %s")
                    params.append(request.filter_tags)

                # Filter by time range
                if request.after:
                    where_clauses.append("created_at > %s")
                    params.append(request.after)

                if request.before:
                    where_clauses.append("created_at < %s")
                    params.append(request.before)

                # Filter by episodes that have the requested fact
                where_clauses.append(f"metadata->'facts'->'{request.fact_type}' IS NOT NULL")

                # Combine WHERE clauses
                if where_clauses:
                    query_parts.append("WHERE " + " AND ".join(where_clauses))

                # Order by timestamp
                order = "DESC" if request.order == "desc" else "ASC"
                query_parts.append(f"ORDER BY created_at {order}")

                # Limit
                query_parts.append(f"LIMIT {request.limit}")

                query = " ".join(query_parts)

                cur.execute(query, params)
                rows = cur.fetchall()

                if not rows:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"No facts found for type: {request.fact_type}"
                    )

                # Get first result
                row = rows[0]
                episode_id = row[0]
                metadata = row[2]
                created_at = row[3]

                # Extract fact value
                facts = metadata.get("facts", {})
                fact_value = facts.get(request.fact_type)

                if fact_value is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Fact type '{request.fact_type}' not found"
                    )

                # Get confidence
                confidence = facts.get("extraction_confidence", 0.8)

                query_time_ms = (time.time() - start_time) * 1000

                return FactQueryResponse(
                    success=True,
                    fact_type=request.fact_type,
                    value=fact_value,
                    source_episode_id=str(episode_id),
                    confidence=confidence,
                    timestamp=created_at,
                    additional_context={"query_time_ms": query_time_ms}
                )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error querying facts: {str(e)}"
        )


@app.post("/memory/hybrid", response_model=HybridQueryResponse, tags=["Hybrid Memory"])
async def hybrid_query(request: HybridQueryRequest):
    """
    Intelligent hybrid query: tries fact extraction first, falls back to semantic search

    Best-of-both-worlds memory retrieval
    """
    global embeddings_model
    start_time = time.time()

    # Detect if query is fact-seekable
    fact_patterns = {
        "version": ["version", "v2", "v1", "release"],
        "accuracy": ["accuracy", "correct", "score", "percentage"],
        "latency": ["latency", "speed", "ms", "milliseconds", "performance"],
        "episode_count": ["episodes", "how many", "total", "count"],
        "status": ["status", "state", "complete", "progress"],
    }

    query_lower = request.query.lower()
    detected_fact_type = None

    # Try to detect fact type from query
    for fact_type, keywords in fact_patterns.items():
        if any(keyword in query_lower for keyword in keywords):
            detected_fact_type = fact_type
            break

    # Strategy 1: Try fact query if prefer=fact or auto + detected
    if request.prefer == "fact" or (request.prefer == "auto" and detected_fact_type):
        if detected_fact_type:
            try:
                fact_request = FactQueryRequest(
                    fact_type=detected_fact_type,
                    filter_tags=request.tags,
                    limit=1
                )
                fact_result = await query_facts(fact_request)

                query_time_ms = (time.time() - start_time) * 1000

                return HybridQueryResponse(
                    success=True,
                    answer=fact_result.value,
                    source="fact",
                    episode_id=str(fact_result.source_episode_id),
                    confidence=fact_result.confidence,
                    query_time_ms=query_time_ms
                )
            except HTTPException:
                # Fact query failed, fall through to semantic search
                pass

    # Strategy 2: Semantic search (narrative)
    try:
        # Check if embeddings model is loaded
        if embeddings_model is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Embeddings model not loaded"
            )

        # Use existing /memory/search endpoint logic
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Generate embedding
                embedding = embeddings_model.encode(request.query).tolist()

                # Build query
                query_parts = [
                    "SELECT episode_id, content, tags, created_at,",
                    "1 - (embedding <=> %s::vector) as similarity",
                    "FROM nexus_memory.zep_episodic_memory"
                ]
                params = [embedding]

                where_clauses = []

                if request.tags:
                    where_clauses.append("tags && %s")
                    params.append(request.tags)

                if where_clauses:
                    query_parts.append("WHERE " + " AND ".join(where_clauses))

                query_parts.append("ORDER BY similarity DESC")
                query_parts.append(f"LIMIT {request.limit}")

                query = " ".join(query_parts)

                cur.execute(query, params)
                rows = cur.fetchall()

                if not rows:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="No relevant episodes found"
                    )

                # Get best match
                row = rows[0]
                episode_id = row[0]
                content = row[1]
                similarity = row[4]

                # Validate similarity score
                if similarity is None:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Similarity score is null - episode may not have embedding"
                    )

                query_time_ms = (time.time() - start_time) * 1000

                return HybridQueryResponse(
                    success=True,
                    answer=content,
                    source="narrative",
                    episode_id=str(episode_id),
                    confidence=float(similarity),
                    query_time_ms=query_time_ms
                )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in hybrid query: {str(e)}"
        )


# ==============================================================================
# LAB_003: Sleep Consolidation
# ==============================================================================

@app.post("/memory/consolidate", tags=["LAB_003"])
async def consolidate_memories(
    date_str: Optional[str] = None
):
    """
    Manually trigger sleep consolidation for a specific date

    LAB_003: Mimics biological sleep consolidation
    - Detects breakthrough episodes
    - Traces backward chains
    - Calculates consolidated salience scores
    - Creates memory traces

    Args:
        date_str: Date to consolidate (YYYY-MM-DD format). Defaults to yesterday.

    Returns:
        Consolidation report with statistics
    """
    try:
        # Lazy import (avoid psycopg2 dependency at startup)
        from consolidation_engine import ConsolidationEngine

        # Parse date
        if date_str:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
        else:
            target_date = datetime.now() - timedelta(days=1)

        # Execute consolidation
        with ConsolidationEngine(
            db_host=POSTGRES_HOST,
            db_port=POSTGRES_PORT,
            db_name=POSTGRES_DB,
            db_user=POSTGRES_USER,
            db_password=POSTGRES_PASSWORD
        ) as engine:
            report = engine.consolidate_daily_memories(target_date)

        return {
            "success": True,
            "date": report.date.isoformat(),
            "episodes_processed": report.episodes_processed,
            "breakthrough_count": report.breakthrough_count,
            "chain_count": report.chain_count,
            "episodes_boosted": report.episodes_boosted,
            "trace_count": report.trace_count,
            "avg_boost": round(report.avg_boost, 3),
            "max_boost": round(report.max_boost, 3),
            "processing_time_seconds": round(report.processing_time_seconds, 2),
            "top_breakthroughs": report.top_breakthroughs
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Consolidation failed: {str(e)}"
        )


# ==============================================================================
# LAB_005: Spreading Activation & Contextual Priming
# ==============================================================================

# Global spreading activation engine instance
spreading_engine = None

def get_spreading_engine():
    """Lazy initialization of spreading activation engine"""
    global spreading_engine
    if spreading_engine is None:
        spreading_engine = SpreadingActivationEngine(
            similarity_threshold=0.7,
            decay_half_life=30.0,
            cache_size=50,
            top_k_related=5,
            max_hops=2
        )
    return spreading_engine


@app.post("/memory/prime/{episode_uuid}", tags=["LAB_005"])
async def prime_episode(episode_uuid: str):
    """
    Activate an episode and spread activation to related memories

    LAB_005: Spreading Activation & Contextual Priming
    - Builds semantic similarity network from embeddings
    - Spreads activation through related episodes
    - Pre-loads related memories into fast cache
    - Reduces retrieval latency by ~55%

    Args:
        episode_uuid: UUID of episode to activate

    Returns:
        Priming report with statistics
    """
    try:
        engine = get_spreading_engine()

        # Fetch episode from database
        with psycopg.connect(DB_CONN_STRING) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT episode_id, content, embedding
                    FROM nexus_memory.zep_episodic_memory
                    WHERE episode_id = %s
                    LIMIT 1
                """, (episode_uuid,))

                row = cur.fetchone()
                if not row:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Episode {episode_uuid} not found"
                    )

                uuid, content, embedding = row

                # Convert embedding to numpy array
                import numpy as np
                embedding_array = np.array(embedding) if embedding else None

                # Ensure episode is in similarity graph
                if uuid not in engine.similarity_graph.embeddings:
                    if embedding_array is not None:
                        engine.add_episode(uuid, content, embedding_array)

                # Access episode (triggers spreading activation)
                result = engine.access_episode(uuid, content, embedding_array if embedding_array is not None else np.zeros(384))

                return {
                    "success": True,
                    "episode_uuid": uuid,
                    "primed_episodes": result["primed_episodes"],
                    "activation_count": result["activation_count"],
                    "processing_time_ms": result["processing_time_ms"],
                    "cache_stats": engine.priming_cache.get_stats()
                }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Priming failed: {str(e)}"
        )


@app.get("/memory/priming/stats", tags=["LAB_005"])
async def get_priming_stats():
    """
    Get spreading activation statistics

    Returns cache hit rate, activation counts, and performance metrics
    """
    try:
        engine = get_spreading_engine()
        stats = engine.get_statistics()

        return {
            "success": True,
            "statistics": stats,
            "engine_status": "active" if engine else "inactive"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get stats: {str(e)}"
        )


@app.get("/memory/primed/{episode_uuid}", tags=["LAB_005"])
async def get_primed_episode(episode_uuid: str):
    """
    Try to retrieve episode from priming cache (fast path)

    Returns episode if primed, otherwise 404
    """
    try:
        engine = get_spreading_engine()
        primed = engine.try_primed_access(episode_uuid)

        if primed:
            return {
                "success": True,
                "cached": True,
                "episode_uuid": primed.uuid,
                "content": primed.content,
                "activation": primed.activation,
                "primed_at": primed.primed_at,
                "source_uuid": primed.source_uuid
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Episode {episode_uuid} not in priming cache"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to access primed episode: {str(e)}"
        )


# ============================================
# LAB_011: Working Memory Buffer Endpoints
# ============================================

@app.post("/memory/working/add", tags=["LAB_011"])
async def add_to_working_memory(
    episode_id: str,
    attention_weight: float = 1.0,
    tags: Optional[List[str]] = None
):
    """
    Add episode reference to working memory buffer (7-item capacity, Miller's Law)

    Working memory holds references to episodes in long-term memory,
    not the content itself (neuroscience-accurate design).

    Automatically evicts oldest item if buffer full.

    Args:
        episode_id: UUID of episode in long-term memory
        attention_weight: Attention score (from LAB_010, default 1.0)
        tags: Optional tags for context
    """
    try:
        added = working_memory.add(episode_id, attention_weight, tags)

        return {
            "success": True,
            "added": added,
            "episode_id": episode_id,
            "buffer_size": len(working_memory.buffer),
            "capacity": working_memory.capacity,
            "message": "Episode added to working memory" if added else "Episode rejected by eviction policy"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add to working memory: {str(e)}"
        )


@app.get("/memory/working/items", tags=["LAB_011"])
async def get_working_memory_items():
    """
    Get all episode references currently in working memory buffer

    Returns items in order (oldest to newest)
    """
    try:
        items_list = [
            {
                "episode_id": item.episode_id,
                "attention_weight": item.attention_weight,
                "added_at": item.added_at.isoformat(),
                "last_accessed": item.last_accessed.isoformat(),
                "access_count": item.access_count,
                "rehearsal_count": item.rehearsal_count,
                "tags": item.tags,
                "age_seconds": item.age_seconds()
            }
            for item in working_memory.buffer
        ]

        return {
            "success": True,
            "items": items_list,
            "count": len(items_list),
            "capacity": working_memory.capacity
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get working memory items: {str(e)}"
        )


@app.post("/memory/working/clear", tags=["LAB_011"])
async def clear_working_memory():
    """
    Clear all items from working memory buffer
    """
    try:
        count_before = len(working_memory.buffer)
        working_memory.clear()

        return {
            "success": True,
            "cleared_count": count_before,
            "message": "Working memory cleared"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear working memory: {str(e)}"
        )


@app.get("/memory/working/stats", tags=["LAB_011"])
async def get_working_memory_stats():
    """
    Get working memory buffer statistics
    """
    try:
        stats = working_memory.get_stats()

        return {
            "success": True,
            **stats
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get working memory stats: {str(e)}"
        )


# ============================================
# LAB_006: Metacognition Logger Endpoints
# ============================================

@app.post("/metacognition/log", tags=["LAB_006"])
async def log_metacognition_action(
    action_id: str,
    action_type: str,
    confidence: float,
    reasoning: Optional[str] = None
):
    """
    Log an action with confidence level (self-awareness)

    Args:
        action_id: Unique action identifier
        action_type: Type of action (e.g., "memory_search", "consolidation")
        confidence: Confidence level (0.0-1.0)
        reasoning: Optional reasoning for confidence
    """
    try:
        action = metacognition_logger.log_action(
            action_id,
            action_type,
            confidence,
            reasoning
        )

        return {
            "success": True,
            "action_id": action.action_id,
            "confidence": action.confidence,
            "timestamp": action.timestamp.isoformat(),
            "message": "Action logged with confidence"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to log metacognition action: {str(e)}"
        )


@app.post("/metacognition/outcome", tags=["LAB_006"])
async def log_metacognition_outcome(
    action_id: str,
    success: bool,
    error_type: Optional[str] = None
):
    """
    Log outcome of a previously logged action

    Updates calibration statistics based on confidence vs actual outcome.
    """
    try:
        logged = metacognition_logger.log_outcome(action_id, success, error_type)

        if not logged:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Action {action_id} not found"
            )

        return {
            "success": True,
            "action_id": action_id,
            "outcome_success": success,
            "message": "Outcome logged successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to log outcome: {str(e)}"
        )


@app.get("/metacognition/stats", tags=["LAB_006"])
async def get_metacognition_stats():
    """
    Get comprehensive metacognition statistics

    Includes:
    - Calibration metrics (ECE)
    - Confidence distribution
    - Error patterns
    - Success rates by confidence bin
    """
    try:
        stats = metacognition_logger.get_comprehensive_stats()

        return {
            "success": True,
            **stats
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get metacognition stats: {str(e)}"
        )


@app.get("/metacognition/calibration", tags=["LAB_006"])
async def get_calibration_curve():
    """
    Get calibration curve data (confidence bins vs actual accuracy)

    Perfect calibration: confidence = accuracy
    """
    try:
        stats = metacognition_logger.get_comprehensive_stats()

        # Extract calibration-specific data
        calibration_data = {
            "ece": stats.get("ece", 0.0),
            "total_actions": stats.get("total_actions", 0),
            "avg_confidence": stats.get("avg_confidence", 0.0),
            "success_rate": stats.get("success_rate", 0.0),
            "bins": stats.get("calibration_bins", [])
        }

        return {
            "success": True,
            **calibration_data
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get calibration data: {str(e)}"
        )


# ============================================
# LAB_013: Dopamine System Endpoints
# ============================================

class DopamineEventRequest(BaseModel):
    expected_reward: float = Field(..., ge=0.0, le=1.0, description="Expected reward (0-1)")
    actual_reward: float = Field(..., ge=0.0, le=1.0, description="Actual reward received (0-1)")


@app.post("/dopamine/process", tags=["LAB_013"])
async def process_dopamine_event(request: DopamineEventRequest):
    """
    Process a reward event and compute RPE (Reward Prediction Error)

    Returns modulated learning rate, motivation level, and exploration bonus.

    **Biological Inspiration:** VTA dopaminergic neurons (Schultz 1997)

    **Algorithm:** RPE = Actual_Reward - Expected_Reward

    **Example:**
    - Expected: 0.5, Actual: 0.8 → RPE: +0.3 (positive surprise, boost learning)
    - Expected: 0.7, Actual: 0.3 → RPE: -0.4 (negative surprise, reduce learning)
    """
    try:
        result = dopamine_system.process_event(
            expected=request.expected_reward,
            actual=request.actual_reward
        )

        return {
            "success": True,
            "expected_reward": request.expected_reward,
            "actual_reward": request.actual_reward,
            **result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process dopamine event: {str(e)}"
        )


@app.get("/dopamine/state", tags=["LAB_013"])
async def get_dopamine_state():
    """
    Get current dopamine system state

    Returns:
    - rpe_current: Latest RPE value
    - rpe_history: Recent RPE history (windowed)
    - rpe_mean: Average RPE (optimism indicator)
    - motivation_level: Current motivation (0-1)
    - learning_rate_multiplier: Current LR boost factor
    - exploration_bonus: Exploration tendency (0-1)
    - total_events: Total RPE events processed
    """
    try:
        state = dopamine_system.get_state()

        return {
            "success": True,
            **state
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get dopamine state: {str(e)}"
        )


# ============================================
# LAB_014: Serotonin System Endpoints
# ============================================

class SerotoninEventRequest(BaseModel):
    emotional_event: float = Field(..., ge=-1.0, le=1.0, description="Emotional valence (-1 to +1)")
    temptation_strength: float = Field(default=0.0, ge=0.0, le=1.0, description="Temptation strength (0-1)")


@app.post("/serotonin/process", tags=["LAB_014"])
async def process_serotonin_event(request: SerotoninEventRequest):
    """
    Process an emotional event and compute mood stability, impulse control, patience

    Returns mood level, impulse control status, patience factor, emotional reactivity, and mood stability.

    **Biological Inspiration:** Raphe nuclei 5-HT neurons (Dayan & Huys 2009)

    **Algorithm:** Mood regulation via exponential moving average with high inertia

    **Example:**
    - emotional_event: +0.3, temptation: 0.5 → Mood increases, can resist temptation
    - emotional_event: -0.3, temptation: 0.8 → Mood decreases, may succumb to temptation
    """
    try:
        result = serotonin_system.process_event(
            emotional_event=request.emotional_event,
            temptation_strength=request.temptation_strength
        )

        return {
            "success": True,
            "emotional_event": request.emotional_event,
            "temptation_strength": request.temptation_strength,
            **result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process serotonin event: {str(e)}"
        )


@app.get("/serotonin/state", tags=["LAB_014"])
async def get_serotonin_state():
    """
    Get current serotonin system state

    Returns:
    - mood_level: Current mood (0-1)
    - mood_history: Recent mood history (windowed)
    - mood_mean: Average mood (baseline indicator)
    - mood_stability: Mood stability score (0-1, inverse of variance)
    - impulse_control_strength: Current impulse control strength (0-1)
    - patience_factor: Patience multiplier for temporal discounting (0-2)
    - total_events: Total emotional events processed
    """
    try:
        state = serotonin_system.get_state()

        return {
            "success": True,
            **state
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get serotonin state: {str(e)}"
        )


# ============================================
# LAB_015: Norepinephrine System Endpoints
# ============================================

class NorepinephrineEventRequest(BaseModel):
    stress_event: float = Field(..., ge=-1.0, le=1.0, description="Stress intensity (-1 to +1)")


@app.post("/norepinephrine/process", tags=["LAB_015"])
async def process_norepinephrine_event(request: NorepinephrineEventRequest):
    """
    Process a stress event and compute arousal, performance, focus, alertness

    Returns arousal level, performance efficiency (Yerkes-Dodson), focus strength, and alertness.

    **Biological Inspiration:** Locus coeruleus (LC) noradrenergic neurons (Aston-Jones & Cohen 2005)

    **Algorithm:** Inverted-U arousal curve for performance (Yerkes-Dodson Law)

    **Example:**
    - stress_event: +0.5 → Arousal increases, performance may improve or decline
    - stress_event: -0.3 → Arousal decreases, calming effect
    """
    try:
        result = norepinephrine_system.process_event(
            stress_event=request.stress_event
        )

        return {
            "success": True,
            "stress_event": request.stress_event,
            **result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process norepinephrine event: {str(e)}"
        )


@app.get("/norepinephrine/state", tags=["LAB_015"])
async def get_norepinephrine_state():
    """
    Get current norepinephrine system state

    Returns:
    - arousal_level: Current arousal (0-1)
    - arousal_history: Recent arousal history (windowed)
    - arousal_mean: Average arousal (baseline indicator)
    - arousal_stability: Arousal stability score (0-1, inverse of variance)
    - performance_efficiency: Performance efficiency (0-1, Yerkes-Dodson)
    - focus_strength: Focus strength (0-1)
    - alertness: Alertness level (0-1)
    - total_events: Total stress events processed
    """
    try:
        state = norepinephrine_system.get_state()

        return {
            "success": True,
            **state
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get norepinephrine state: {str(e)}"
        )


# ============================================
# LAB_016: Acetylcholine System Endpoints
# ============================================

class AcetylcholineStimulusRequest(BaseModel):
    novelty: float = Field(..., ge=0.0, le=1.0, description="Novelty score (0-1)")
    attention_demand: float = Field(..., ge=0.0, le=1.0, description="Attention demand (0-1)")
    base_attention: float = Field(default=0.5, ge=0.0, le=1.0, description="Base attention signal")
    base_encoding_strength: float = Field(default=0.5, ge=0.0, le=1.0, description="Base encoding strength")


@app.post("/acetylcholine/process", tags=["LAB_016"])
async def process_acetylcholine_stimulus(request: AcetylcholineStimulusRequest):
    """
    Process a stimulus and compute ACh level, attention amplification, encoding modulation

    Returns ACh level, amplified attention, encoding strength, learning readiness.

    **Biological Inspiration:** Basal forebrain cholinergic neurons (Hasselmo 2006)

    **Algorithm:** Attention gating & encoding/recall modulation

    **Example:**
    - novelty: 0.8, attention_demand: 0.7 → ACh spike, amplified attention, strong encoding
    - novelty: 0.1, attention_demand: 0.2 → Low ACh, baseline attention, weak encoding
    """
    try:
        result = acetylcholine_system.process_stimulus(
            novelty=request.novelty,
            attention_demand=request.attention_demand,
            base_attention=request.base_attention,
            base_encoding_strength=request.base_encoding_strength
        )

        return {
            "success": True,
            "novelty": request.novelty,
            "attention_demand": request.attention_demand,
            **result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process acetylcholine stimulus: {str(e)}"
        )


@app.get("/acetylcholine/state", tags=["LAB_016"])
async def get_acetylcholine_state():
    """
    Get current acetylcholine system state

    Returns:
    - ach_level: Current ACh level (0-1)
    - ach_history: Recent ACh history (windowed)
    - ach_mean: Average ACh (baseline indicator)
    - ach_stability: ACh stability score (0-1, inverse of variance)
    - mode: Current mode ('encoding' or 'recall')
    - learning_readiness: Learning readiness score (0-1)
    - total_events: Total stimuli processed
    """
    try:
        state = acetylcholine_system.get_state()

        return {
            "success": True,
            **state
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get acetylcholine state: {str(e)}"
        )


@app.post("/acetylcholine/mode", tags=["LAB_016"])
async def set_acetylcholine_mode(mode: str = "encoding"):
    """
    Set encoding/recall mode

    **Modes:**
    - encoding: High ACh enables strong encoding (plasticity enabled)
    - recall: Low ACh reduces encoding (consolidation phase)
    """
    try:
        acetylcholine_system.set_mode(mode)

        return {
            "success": True,
            "mode": mode,
            "message": f"Acetylcholine mode set to '{mode}'"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to set acetylcholine mode: {str(e)}"
        )


# ============================================
# LAB_017: GABA System Endpoints
# ============================================

class GABAEventRequest(BaseModel):
    anxiety: float = Field(..., ge=0.0, le=1.0, description="Anxiety level (0-1)")
    excitation: float = Field(..., ge=0.0, le=1.0, description="Excitation level (0-1)")
    base_anxiety: float = Field(default=0.5, ge=0.0, le=1.0, description="Base anxiety level")
    excitatory_signal: float = Field(default=0.5, ge=0.0, le=1.0, description="Excitatory signal strength")


@app.post("/gaba/process", tags=["LAB_017"])
async def process_gaba_event(request: GABAEventRequest):
    """
    Process an event and compute GABA level, E/I balance, anxiety modulation

    Returns GABA level, E/I balance state, modulated anxiety, inhibitory control, network stability.

    **Biological Inspiration:** GABAergic interneurons (Yizhar et al. 2011)

    **Algorithm:** Excitation/inhibition balance & anxiety reduction

    **Example:**
    - anxiety: 0.8, excitation: 0.7 → GABA spike, reduced anxiety, balanced E/I
    - anxiety: 0.2, excitation: 0.2 → Low GABA, minimal inhibition, potential over-excitation
    """
    try:
        result = gaba_system.process_event(
            anxiety=request.anxiety,
            excitation=request.excitation,
            base_anxiety=request.base_anxiety,
            excitatory_signal=request.excitatory_signal
        )

        return {
            "success": True,
            "anxiety": request.anxiety,
            "excitation": request.excitation,
            **result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process GABA event: {str(e)}"
        )


@app.get("/gaba/state", tags=["LAB_017"])
async def get_gaba_state():
    """
    Get current GABA system state

    Returns:
    - gaba_level: Current GABA level (0-1)
    - gaba_history: Recent GABA history (windowed)
    - gaba_mean: Average GABA (baseline indicator)
    - network_stability: Network stability score (0-1, inverse of variance)
    - total_events: Total events processed
    """
    try:
        state = gaba_system.get_state()

        return {
            "success": True,
            **state
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get GABA state: {str(e)}"
        )


# ============================================
# A/B Testing Endpoints
# ============================================

@app.post("/ab-test/record", tags=["A/B Testing"])
async def record_ab_test_metric(request: ABTestMetricRequest):
    """
    Record an A/B test metric for performance comparison

    Variants:
    - "control": Without LAB_005 spreading activation
    - "treatment": With LAB_005 spreading activation
    """
    try:
        ab_manager = get_ab_test_manager(DB_CONN_STRING)

        # Validate variant
        test_variant = TestVariant(request.variant)

        # Record the metric
        ab_manager.record_retrieval(
            variant=test_variant,
            retrieval_time_ms=request.retrieval_time_ms,
            cache_hit=request.cache_hit,
            num_results=request.num_results,
            context_coherence=request.context_coherence,
            primed_count=request.primed_count,
            query_id=request.query_id
        )

        return {
            "success": True,
            "variant": request.variant,
            "message": "Metric recorded successfully"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid variant: {request.variant}. Must be 'control' or 'treatment'"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record metric: {str(e)}"
        )


@app.get("/ab-test/compare", tags=["A/B Testing"])
async def compare_ab_test_variants(hours_back: int = 24):
    """
    Compare control vs treatment variants

    Returns aggregated metrics and performance improvements:
    - Latency reduction
    - Cache hit rate increase
    - Context coherence improvement
    - Statistical significance
    """
    try:
        ab_manager = get_ab_test_manager(DB_CONN_STRING)
        comparison = ab_manager.compare_variants(hours_back=hours_back)

        return {
            "success": True,
            "hours_analyzed": hours_back,
            **comparison
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compare variants: {str(e)}"
        )


@app.get("/ab-test/metrics/{variant}", tags=["A/B Testing"])
async def get_variant_metrics(variant: str, hours_back: int = 24):
    """Get aggregated metrics for a specific variant"""
    try:
        ab_manager = get_ab_test_manager(DB_CONN_STRING)
        test_variant = TestVariant(variant)

        metrics = ab_manager.get_aggregated_metrics(test_variant, hours_back)

        if not metrics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No data found for variant '{variant}' in the last {hours_back} hours"
            )

        return {
            "success": True,
            "variant": variant,
            "hours_analyzed": hours_back,
            "metrics": {
                "sample_count": metrics.sample_count,
                "avg_retrieval_time_ms": metrics.avg_retrieval_time_ms,
                "p50_retrieval_time_ms": metrics.p50_retrieval_time_ms,
                "p95_retrieval_time_ms": metrics.p95_retrieval_time_ms,
                "cache_hit_rate": metrics.cache_hit_rate,
                "avg_context_coherence": metrics.avg_context_coherence,
                "avg_primed_count": metrics.avg_primed_count,
                "total_duration_seconds": metrics.total_duration_seconds
            }
        }
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid variant: {variant}. Must be 'control' or 'treatment'"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get metrics: {str(e)}"
        )


@app.get("/ab-test/timeseries/{variant}", tags=["A/B Testing"])
async def get_variant_timeseries(variant: str, hours_back: int = 24):
    """Get time-series data for a variant (for visualization)"""
    try:
        ab_manager = get_ab_test_manager(DB_CONN_STRING)
        test_variant = TestVariant(variant)

        timeseries = ab_manager.get_time_series(test_variant, hours_back)

        return {
            "success": True,
            "variant": variant,
            "hours_analyzed": hours_back,
            "data_points": len(timeseries),
            "timeseries": timeseries
        }
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid variant: {variant}. Must be 'control' or 'treatment'"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get timeseries: {str(e)}"
        )


@app.delete("/ab-test/clear", tags=["A/B Testing"])
async def clear_ab_test_data(variant: Optional[str] = None):
    """Clear A/B test data (for resetting experiments)"""
    try:
        ab_manager = get_ab_test_manager(DB_CONN_STRING)

        if variant:
            test_variant = TestVariant(variant)
            ab_manager.clear_test_data(test_variant)
            message = f"Cleared data for variant '{variant}'"
        else:
            ab_manager.clear_test_data()
            message = "Cleared all A/B test data"

        return {
            "success": True,
            "message": message
        }
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid variant: {variant}. Must be 'control' or 'treatment'"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear data: {str(e)}"
        )


# ============================================
# Main
# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
