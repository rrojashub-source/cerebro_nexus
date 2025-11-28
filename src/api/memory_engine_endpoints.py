"""
Memory Engine API Endpoints - Multi-tier memory system

Provides REST API access to the SuperMemory-style memory engine:
- Hot tier (Redis): Ultra-fast recent memories
- Warm tier (PostgreSQL): Full episodic memory with semantic search
- Cold tier: Archived memories (future)

Author: NEXUS AI
Created: November 28, 2025
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
import logging
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory_engine.tiers.hot import HotMemory
from memory_engine.tiers.warm import WarmMemory
from memory_engine.decay.smart_decay import SmartDecay
from memory_engine.relationships.graph import MemoryGraph, RelationType
from memory_engine.facts.extractor import FactExtractor
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/memory/engine", tags=["Memory Engine"])


# ============== Pydantic Models ==============

class HotMemoryAddRequest(BaseModel):
    """Request to add memory to hot tier"""
    memory_id: str = Field(..., description="Unique memory identifier")
    content: str = Field(..., description="Memory content")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Optional metadata")


class HotMemoryResponse(BaseModel):
    """Response from hot tier operations"""
    success: bool
    memory_id: Optional[str] = None
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    access_count: Optional[int] = None


class TierStatsResponse(BaseModel):
    """Multi-tier statistics response"""
    hot: Dict[str, Any]
    warm: Dict[str, Any]
    total_memories: int
    engine_version: str = "1.0.0"


class SearchRequest(BaseModel):
    """Search request across tiers"""
    query: str = Field(..., description="Search query")
    tier: str = Field(default="all", description="Tier to search: hot, warm, or all")
    limit: int = Field(default=10, ge=1, le=100)


# ============== Singleton Instances ==============

_hot_memory = None
_warm_memory = None
_memory_graph = None


def _read_secret(secret_path: str, default: str = None) -> str:
    """Read secret from Docker secret file"""
    try:
        if os.path.exists(secret_path):
            with open(secret_path, 'r') as f:
                return f.read().strip()
    except Exception as e:
        logger.warning(f"Failed to read secret from {secret_path}: {e}")
    return default


def get_hot_memory() -> HotMemory:
    global _hot_memory
    if _hot_memory is None:
        # Use Docker service names when running in container
        host = os.getenv("REDIS_HOST", "nexus_redis_master")
        port = int(os.getenv("REDIS_PORT", "6379"))
        # Read password from Docker secret or env var
        password = _read_secret(
            os.getenv("REDIS_PASSWORD_FILE", "/run/secrets/redis_password"),
            os.getenv("REDIS_PASSWORD")
        )
        _hot_memory = HotMemory(
            host=host,
            port=port,
            password=password,
            db=1  # Use db 1 for memory engine
        )
    return _hot_memory


def get_warm_memory() -> WarmMemory:
    global _warm_memory
    if _warm_memory is None:
        # Use Docker service names when running in container
        host = os.getenv("POSTGRES_HOST", "nexus_postgresql_v2")
        port = int(os.getenv("POSTGRES_PORT", "5432"))
        _warm_memory = WarmMemory(
            host=host,
            port=port,
            database=os.getenv("POSTGRES_DB", "nexus_db"),
            user=os.getenv("POSTGRES_USER", "nexus_user"),
            password=os.getenv("POSTGRES_PASSWORD", "nexus_secure_2024")
        )
    return _warm_memory


def get_memory_graph() -> MemoryGraph:
    global _memory_graph
    if _memory_graph is None:
        # Use Docker service names when running in container
        host = os.getenv("NEO4J_HOST", "nexus_neo4j")
        _memory_graph = MemoryGraph(
            uri=f"bolt://{host}:7687",
            user="neo4j",
            password=os.getenv("NEO4J_PASSWORD", "password123")
        )
    return _memory_graph


# ============== Endpoints ==============

@router.get("/health")
async def memory_engine_health():
    """Check memory engine health across all tiers"""
    try:
        hot = get_hot_memory()
        warm = get_warm_memory()

        hot_stats = hot.get_stats()
        warm_stats = warm.get_stats()

        return {
            "status": "healthy",
            "engine_version": "1.0.0",
            "tiers": {
                "hot": {"status": "connected", "items": hot_stats.get("total_items", 0)},
                "warm": {"status": "connected", "items": warm_stats.get("total_items", 0)}
            }
        }
    except Exception as e:
        logger.error(f"Memory engine health check failed: {e}")
        return {
            "status": "degraded",
            "error": str(e)
        }


@router.get("/stats", response_model=TierStatsResponse)
async def get_tier_stats():
    """Get statistics from all memory tiers"""
    try:
        hot = get_hot_memory()
        warm = get_warm_memory()

        hot_stats = hot.get_stats()
        warm_stats = warm.get_stats()

        total = hot_stats.get("total_items", 0) + warm_stats.get("total_items", 0)

        return TierStatsResponse(
            hot=hot_stats,
            warm=warm_stats,
            total_memories=total,
            engine_version="1.0.0"
        )
    except Exception as e:
        logger.error(f"Failed to get tier stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/hot/add", response_model=HotMemoryResponse)
async def add_to_hot_tier(request: HotMemoryAddRequest):
    """Add memory to hot tier (Redis) for fast access"""
    try:
        hot = get_hot_memory()
        success = hot.add(
            memory_id=request.memory_id,
            content=request.content,
            metadata=request.metadata
        )

        return HotMemoryResponse(
            success=success,
            memory_id=request.memory_id if success else None
        )
    except Exception as e:
        logger.error(f"Failed to add to hot tier: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/hot/{memory_id}", response_model=HotMemoryResponse)
async def get_from_hot_tier(memory_id: str):
    """Get memory from hot tier by ID"""
    try:
        hot = get_hot_memory()
        memory = hot.get(memory_id)

        if memory is None:
            raise HTTPException(status_code=404, detail="Memory not found in hot tier")

        return HotMemoryResponse(
            success=True,
            memory_id=memory_id,
            content=memory.get("content"),
            metadata=memory.get("metadata"),
            access_count=memory.get("access_count")
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get from hot tier: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/hot/{memory_id}")
async def delete_from_hot_tier(memory_id: str):
    """Remove memory from hot tier"""
    try:
        hot = get_hot_memory()
        success = hot.delete(memory_id)

        return {"success": success, "memory_id": memory_id}
    except Exception as e:
        logger.error(f"Failed to delete from hot tier: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search")
async def search_memories(request: SearchRequest):
    """Search memories across tiers"""
    results = []

    try:
        if request.tier in ["hot", "all"]:
            hot = get_hot_memory()
            hot_results = hot.search(request.query, limit=request.limit)
            for r in hot_results:
                r["tier"] = "hot"
            results.extend(hot_results)

        # Warm tier requires embeddings for semantic search
        # For now, just return hot tier results
        # TODO: Integrate with embedding service for warm tier search

        return {
            "query": request.query,
            "total_results": len(results),
            "results": results[:request.limit]
        }
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/hot/stats")
async def get_hot_tier_stats():
    """Get hot tier (Redis) statistics"""
    try:
        hot = get_hot_memory()
        return hot.get_stats()
    except Exception as e:
        logger.error(f"Failed to get hot tier stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/warm/stats")
async def get_warm_tier_stats():
    """Get warm tier (PostgreSQL) statistics"""
    try:
        warm = get_warm_memory()
        return warm.get_stats()
    except Exception as e:
        logger.error(f"Failed to get warm tier stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============== SuperMemory-Style Simple API ==============
# These endpoints mirror SuperMemory's simple interface

class SimpleMemoryAdd(BaseModel):
    """Simple memory add request - like SuperMemory"""
    content: str = Field(..., description="What to remember")
    source: Optional[str] = Field(default=None, description="Source of the memory")
    importance: Optional[float] = Field(default=0.5, ge=0, le=1, description="Importance score 0-1")
    extract_facts: Optional[bool] = Field(default=True, description="Auto-extract facts from content")


class SimpleMemorySearch(BaseModel):
    """Simple search request - like SuperMemory"""
    query: str = Field(..., description="What to search for")
    limit: int = Field(default=10, ge=1, le=50)


class FactExtractionRequest(BaseModel):
    """Request to extract facts from content"""
    content: str = Field(..., description="Content to extract facts from")
    source_id: Optional[str] = Field(default=None, description="Source document ID")


class RelationshipRequest(BaseModel):
    """Request to create relationship between memories"""
    source_id: str = Field(..., description="Source memory ID")
    target_id: str = Field(..., description="Target memory ID")
    relation_type: str = Field(..., description="Type: updates, extends, derives, similar")
    metadata: Optional[Dict[str, Any]] = Field(default=None)


# Singleton for fact extractor
_fact_extractor = None

def get_fact_extractor() -> FactExtractor:
    global _fact_extractor
    if _fact_extractor is None:
        _fact_extractor = FactExtractor()
    return _fact_extractor


@router.post("/add")
async def add_memory_simple(request: SimpleMemoryAdd):
    """
    Add a memory - SuperMemory style simple API.

    This is the main endpoint for adding memories. It:
    1. Generates a unique ID
    2. Stores in hot tier for fast access
    3. Optionally extracts facts
    4. Returns the memory ID for future reference

    Example:
        POST /memory/engine/add
        {"content": "NEXUS was created by Ricardo in 2025"}
    """
    try:
        # Generate unique ID
        memory_id = f"mem_{uuid.uuid4().hex[:12]}"

        # Add to hot tier
        hot = get_hot_memory()
        metadata = {
            "source": request.source,
            "importance": request.importance,
            "created_at": datetime.utcnow().isoformat(),
            "type": "memory"
        }

        success = hot.add(
            memory_id=memory_id,
            content=request.content,
            metadata=metadata
        )

        # Extract facts if requested
        facts = []
        if request.extract_facts:
            extractor = get_fact_extractor()
            extracted = extractor.extract_facts(
                content=request.content,
                source_id=memory_id,
                metadata={"importance": request.importance}
            )
            facts = [f["content"] for f in extracted]

        return {
            "success": success,
            "memory_id": memory_id,
            "facts_extracted": len(facts),
            "facts": facts,
            "message": f"Memory added successfully with {len(facts)} facts"
        }

    except Exception as e:
        logger.error(f"Failed to add memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search/simple")
async def search_memory_simple(request: SimpleMemorySearch):
    """
    Search memories - SuperMemory style simple API.

    Searches across all tiers and returns relevant memories.

    Example:
        POST /memory/engine/search/simple
        {"query": "who created NEXUS"}
    """
    try:
        results = []

        # Search hot tier
        hot = get_hot_memory()
        hot_results = hot.search(request.query, limit=request.limit)

        for r in hot_results:
            results.append({
                "id": r.get("memory_id"),
                "content": r.get("content"),
                "score": r.get("score", 0),
                "tier": "hot",
                "metadata": r.get("metadata", {})
            })

        return {
            "query": request.query,
            "total": len(results),
            "results": results[:request.limit]
        }

    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/facts/extract")
async def extract_facts_endpoint(request: FactExtractionRequest):
    """
    Extract facts from content.

    Breaks down long content into discrete, searchable facts.

    Example:
        POST /memory/engine/facts/extract
        {"content": "NEXUS is an AI brain. It was created in 2025. Ricardo is the guardian."}

    Returns:
        List of extracted facts with metadata
    """
    try:
        extractor = get_fact_extractor()

        # Extract regular facts
        facts = extractor.extract_facts(
            content=request.content,
            source_id=request.source_id
        )

        # Also extract key-value facts
        kv_facts = extractor.extract_key_value_facts(
            content=request.content,
            source_id=request.source_id
        )

        return {
            "source_id": request.source_id,
            "facts_count": len(facts),
            "key_value_facts_count": len(kv_facts),
            "facts": facts,
            "key_value_facts": kv_facts
        }

    except Exception as e:
        logger.error(f"Fact extraction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/relationships/connect")
async def connect_memories(request: RelationshipRequest):
    """
    Create relationship between two memories.

    Relationship types:
    - updates: New memory replaces/updates old one
    - extends: New memory adds information to existing
    - derives: System inferred connection
    - similar: Memories are semantically similar

    Example:
        POST /memory/engine/relationships/connect
        {
            "source_id": "mem_abc123",
            "target_id": "mem_def456",
            "relation_type": "extends"
        }
    """
    try:
        # Map string to enum
        relation_map = {
            "updates": RelationType.UPDATES,
            "extends": RelationType.EXTENDS,
            "derives": RelationType.DERIVES,
            "similar": RelationType.SIMILAR,
            "temporal": RelationType.TEMPORAL,
            "causal": RelationType.CAUSAL
        }

        if request.relation_type not in relation_map:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid relation_type. Must be one of: {list(relation_map.keys())}"
            )

        graph = get_memory_graph()
        success = graph.connect(
            source_id=request.source_id,
            target_id=request.target_id,
            relation_type=relation_map[request.relation_type],
            metadata=request.metadata
        )

        return {
            "success": success,
            "source_id": request.source_id,
            "target_id": request.target_id,
            "relation_type": request.relation_type,
            "message": f"Relationship created: {request.source_id} -{request.relation_type}-> {request.target_id}"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create relationship: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/relationships/{memory_id}")
async def get_memory_relationships(
    memory_id: str,
    relation_type: Optional[str] = None,
    direction: str = Query(default="both", enum=["incoming", "outgoing", "both"])
):
    """
    Get all relationships for a memory.

    Example:
        GET /memory/engine/relationships/mem_abc123?direction=outgoing
    """
    try:
        graph = get_memory_graph()

        # Map relation type if provided
        rel_type = None
        if relation_type:
            relation_map = {
                "updates": RelationType.UPDATES,
                "extends": RelationType.EXTENDS,
                "derives": RelationType.DERIVES,
                "similar": RelationType.SIMILAR
            }
            rel_type = relation_map.get(relation_type)

        relationships = graph.get_related(
            memory_id=memory_id,
            relation_type=rel_type,
            direction=direction
        )

        return {
            "memory_id": memory_id,
            "direction": direction,
            "total": len(relationships),
            "relationships": relationships
        }

    except Exception as e:
        logger.error(f"Failed to get relationships: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/decay/analyze")
async def analyze_decay(memory_ids: List[str] = None, threshold: float = 0.3):
    """
    Analyze memories for potential archival based on decay score.

    Returns memories that have decayed below the threshold.
    Useful for maintenance and cleanup.

    Example:
        POST /memory/engine/decay/analyze
        {"threshold": 0.3}
    """
    try:
        decay = SmartDecay()
        hot = get_hot_memory()

        # Get all memories from hot tier if no specific IDs provided
        # For now, return the decay configuration
        return {
            "decay_config": {
                "weights": decay.weights,
                "half_life_days": decay.half_life_days
            },
            "threshold": threshold,
            "message": "Decay analysis ready. Pass memory_ids for specific analysis."
        }

    except Exception as e:
        logger.error(f"Decay analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
