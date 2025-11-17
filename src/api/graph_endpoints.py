"""
Graph Algorithms API Endpoints

RESTful API for advanced graph algorithms on episodic memory graph.

Endpoints:
- POST /graph/community_detection - Detect communities in graph
- POST /graph/centrality - Calculate centrality measures
- GET /graph/important_episodes - Find most important episodes
- POST /graph/shortest_path - Find shortest path between episodes
- GET /graph/insights - Get overall graph insights
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal
import logging
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.graph_algorithms import GraphAlgorithms

logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/graph", tags=["Graph Algorithms"])

# Initialize graph algorithms service (singleton)
graph_algo = None


def get_graph_algo() -> GraphAlgorithms:
    """Get or create GraphAlgorithms instance"""
    global graph_algo
    if graph_algo is None:
        graph_algo = GraphAlgorithms()
    return graph_algo


# ==================== Request/Response Models ====================

class CommunityDetectionRequest(BaseModel):
    """Request for community detection"""
    algorithm: Literal["louvain", "label_propagation"] = Field(
        default="louvain",
        description="Algorithm to use for community detection"
    )
    min_size: int = Field(
        default=3,
        ge=1,
        description="Minimum community size to return"
    )


class CommunityDetectionResponse(BaseModel):
    """Response for community detection"""
    communities: List[Dict] = Field(
        description="List of detected communities"
    )
    total_communities: int = Field(
        description="Total number of communities found"
    )


class CentralityRequest(BaseModel):
    """Request for centrality calculation"""
    measure: Literal["pagerank", "betweenness", "degree"] = Field(
        default="pagerank",
        description="Centrality measure to calculate"
    )
    top_n: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Number of top nodes to return"
    )


class CentralityResponse(BaseModel):
    """Response for centrality calculation"""
    rankings: List[Dict] = Field(
        description="List of episodes with centrality scores"
    )
    measure: str = Field(
        description="Centrality measure used"
    )


class ImportantEpisodesResponse(BaseModel):
    """Response for important episodes"""
    episodes: List[Dict] = Field(
        description="List of important episodes"
    )
    measure: str = Field(
        description="Measure used to determine importance"
    )


class ShortestPathRequest(BaseModel):
    """Request for shortest path"""
    from_episode_id: str = Field(
        description="Source episode UUID"
    )
    to_episode_id: str = Field(
        description="Target episode UUID"
    )


class ShortestPathResponse(BaseModel):
    """Response for shortest path"""
    path: List[str] = Field(
        description="List of episode IDs in path"
    )
    distance: int = Field(
        description="Number of hops in path"
    )
    relationships: List[str] = Field(
        description="Relationship types in path"
    )


class GraphInsightsResponse(BaseModel):
    """Response for graph insights"""
    stats: Dict = Field(
        description="Graph statistics"
    )
    top_communities: List[Dict] = Field(
        description="Top communities by size"
    )
    top_central_nodes: List[Dict] = Field(
        description="Top nodes by degree centrality"
    )


# ==================== Endpoints ====================

@router.post(
    "/community_detection",
    response_model=CommunityDetectionResponse,
    summary="Detect Communities",
    description="Detect communities in the graph using modularity-based clustering"
)
async def detect_communities(request: CommunityDetectionRequest):
    """
    Detect communities in the episodic memory graph.

    Uses Label Propagation algorithm (Louvain-like) to identify
    groups of related episodes.

    **Example Response:**
    ```json
    {
        "communities": [
            {
                "community_id": 0,
                "size": 15,
                "episodes": ["uuid1", "uuid2", ...],
                "modularity": 0.42
            }
        ],
        "total_communities": 5
    }
    ```
    """
    try:
        algo = get_graph_algo()
        communities = algo.detect_communities(
            algorithm=request.algorithm,
            min_size=request.min_size
        )

        return CommunityDetectionResponse(
            communities=communities,
            total_communities=len(communities)
        )

    except Exception as e:
        logger.error(f"❌ Community detection failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/centrality",
    response_model=CentralityResponse,
    summary="Calculate Centrality",
    description="Calculate centrality measures (PageRank, Betweenness, Degree)"
)
async def calculate_centrality(request: CentralityRequest):
    """
    Calculate centrality measures for episodes.

    Supported measures:
    - **pagerank**: Importance based on connections (Google's algorithm)
    - **betweenness**: Episodes that bridge different parts of graph
    - **degree**: Simple count of connections

    **Example Response:**
    ```json
    {
        "rankings": [
            {
                "episode_id": "uuid123",
                "pagerank": 0.85,
                "rank": 1
            }
        ],
        "measure": "pagerank"
    }
    ```
    """
    try:
        algo = get_graph_algo()

        if request.measure == "pagerank":
            rankings = algo.calculate_pagerank(top_n=request.top_n)
        elif request.measure == "betweenness":
            rankings = algo.calculate_betweenness_centrality(top_n=request.top_n)
        elif request.measure == "degree":
            rankings = algo.find_important_episodes(
                top_n=request.top_n,
                measure="degree"
            )
        else:
            raise ValueError(f"Unknown measure: {request.measure}")

        return CentralityResponse(
            rankings=rankings,
            measure=request.measure
        )

    except Exception as e:
        logger.error(f"❌ Centrality calculation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/important_episodes",
    response_model=ImportantEpisodesResponse,
    summary="Find Important Episodes",
    description="Find most important episodes based on centrality"
)
async def get_important_episodes(
    limit: int = Query(default=20, ge=1, le=100, description="Number of episodes to return"),
    measure: Literal["pagerank", "betweenness", "degree"] = Query(
        default="degree",
        description="Centrality measure to use"
    )
):
    """
    Find most important episodes in the graph.

    Returns episodes with highest centrality scores, including
    content preview and reason for importance.

    **Example Response:**
    ```json
    {
        "episodes": [
            {
                "episode_id": "uuid123",
                "importance_score": 15.0,
                "rank": 1,
                "content": "Episode content preview...",
                "reason": "High degree centrality (15 connections)"
            }
        ],
        "measure": "degree"
    }
    ```
    """
    try:
        algo = get_graph_algo()
        episodes = algo.find_important_episodes(
            top_n=limit,
            measure=measure
        )

        return ImportantEpisodesResponse(
            episodes=episodes,
            measure=measure
        )

    except Exception as e:
        logger.error(f"❌ Important episodes search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/shortest_path",
    response_model=ShortestPathResponse,
    summary="Find Shortest Path",
    description="Find shortest path between two episodes"
)
async def find_shortest_path(request: ShortestPathRequest):
    """
    Find shortest path between two episodes in the graph.

    Returns the sequence of episodes and relationship types
    connecting them.

    **Example Response:**
    ```json
    {
        "path": ["uuid1", "uuid2", "uuid3"],
        "distance": 2,
        "relationships": ["SIMILAR", "TEMPORAL"]
    }
    ```

    Returns 404 if no path exists.
    """
    try:
        algo = get_graph_algo()
        path_data = algo.find_shortest_path(
            from_episode_id=request.from_episode_id,
            to_episode_id=request.to_episode_id
        )

        if not path_data:
            raise HTTPException(
                status_code=404,
                detail=f"No path found between episodes"
            )

        return ShortestPathResponse(
            path=path_data['path'],
            distance=path_data['distance'],
            relationships=path_data['relationships']
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Shortest path search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/insights",
    response_model=GraphInsightsResponse,
    summary="Get Graph Insights",
    description="Get comprehensive graph statistics and insights"
)
async def get_graph_insights():
    """
    Get comprehensive insights about the graph structure.

    Includes:
    - Basic statistics (nodes, relationships, density)
    - Top communities
    - Most central nodes
    - Relationship type distribution

    **Example Response:**
    ```json
    {
        "stats": {
            "total_nodes": 1000,
            "total_relationships": 5000,
            "avg_degree": 5.0,
            "density": 0.005,
            "relationship_types": {"SIMILAR": 3000, "TEMPORAL": 2000},
            "largest_component_size": 950
        },
        "top_communities": [...],
        "top_central_nodes": [...]
    }
    ```
    """
    try:
        algo = get_graph_algo()

        # Get basic stats
        stats = algo.analyze_graph_structure()

        # Get top communities
        communities = algo.detect_communities(min_size=5)
        top_communities = communities[:5]  # Top 5

        # Get top central nodes
        top_nodes = algo.find_important_episodes(top_n=10, measure="degree")

        return GraphInsightsResponse(
            stats=stats,
            top_communities=top_communities,
            top_central_nodes=top_nodes
        )

    except Exception as e:
        logger.error(f"❌ Graph insights failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Health check for graph service
@router.get(
    "/health",
    summary="Graph Service Health",
    description="Check if graph service is healthy"
)
async def health_check():
    """
    Check if Neo4j connection is healthy.

    **Example Response:**
    ```json
    {
        "status": "healthy",
        "neo4j_connected": true,
        "total_nodes": 1000
    }
    ```
    """
    try:
        algo = get_graph_algo()
        stats = algo.analyze_graph_structure()

        return {
            "status": "healthy",
            "neo4j_connected": True,
            "total_nodes": stats['total_nodes'],
            "total_relationships": stats['total_relationships']
        }

    except Exception as e:
        logger.error(f"❌ Graph health check failed: {e}")
        return {
            "status": "unhealthy",
            "neo4j_connected": False,
            "error": str(e)
        }
