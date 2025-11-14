"""
PersistenciaClient - Client for AAG+FIRM integration

Session 28: Dashboard 3D + PERSISTENCIA Integration
Author: NEXUS AI
Date: November 14, 2025

Endpoints:
- POST /aag/generate: Context retrieval
- POST /firm/audit: Validation (future)
- POST /memory/action: Storage (already exists)
"""

import httpx
from typing import Dict, List, Optional, Any
import asyncio
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PersistenciaClient:
    """
    Client for PERSISTENCIA AAG+FIRM endpoints

    Provides contextual memory retrieval for CognitiveStack integration.

    Usage:
        client = PersistenciaClient(base_url="http://localhost:8003")
        result = await client.aag_generate(query="What is my task?", top_k=5)
    """

    def __init__(self, base_url: str = "http://localhost:8003"):
        """
        Initialize PERSISTENCIA client

        Parameters:
        -----------
        base_url : str
            Base URL of PERSISTENCIA API (default: http://localhost:8003)
        """
        self.base_url = base_url
        self.timeout = httpx.Timeout(0.1, read=0.1)  # 100ms hard limit
        self.max_retries = 2
        self.retry_delay_ms = 50  # 50ms between retries

    async def aag_generate(
        self,
        query: str,
        top_k: int = 5,
        similarity_threshold: float = 0.7,
        timeout_ms: int = 100
    ) -> Dict[str, Any]:
        """
        Retrieve relevant episodes using AAG (Adaptive Augmented Generation)

        This is the core retrieval function for contextual memory access.

        Parameters:
        -----------
        query : str
            Query string to search for
        top_k : int (default: 5)
            Number of top episodes to retrieve
        similarity_threshold : float (default: 0.7)
            Minimum similarity score (0-1) for retrieved episodes
        timeout_ms : int (default: 100)
            Timeout in milliseconds

        Returns:
        --------
        result : Dict[str, Any]
            {
                'episodes': [
                    {
                        'episode_id': str,
                        'content': str,
                        'similarity': float,
                        'timestamp': str,
                        'metadata': dict
                    },
                    ...
                ],
                'avg_relevance': float (0-1),
                'retrieval_time_ms': float,
                'success': bool
            }

        Graceful Degradation:
        ---------------------
        If retrieval fails (timeout, network error, etc.), returns:
        {
            'episodes': [],
            'avg_relevance': 0.0,
            'retrieval_time_ms': 0.0,
            'success': False,
            'error': str
        }
        """
        start_time = datetime.now()

        # Retry loop
        for attempt in range(self.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        f"{self.base_url}/aag/generate",
                        json={
                            "query": query,
                            "top_k": top_k,
                            "use_precomputed": True  # Use pre-computed embeddings
                        }
                    )
                    response.raise_for_status()
                    data = response.json()

                    # PERSISTENCIA returns: {accepted: [...], attributed: [...], rejected: [...]}
                    # We use 'accepted' (high-confidence episodes)
                    accepted_episodes = data.get('accepted', [])

                    # Compute avg_relevance from relevance_score field
                    avg_relevance = (
                        sum(ep.get('relevance_score', 0.0) for ep in accepted_episodes) / len(accepted_episodes)
                        if accepted_episodes else 0.0
                    )

                    retrieval_time = data.get('latency_ms', 0.0)  # Use PERSISTENCIA's latency

                    logger.info(
                        f"AAG retrieval successful: {len(accepted_episodes)} episodes, "
                        f"avg_relevance={avg_relevance:.2f}, "
                        f"latency={retrieval_time:.1f}ms, "
                        f"attempt={attempt + 1}"
                    )

                    return {
                        'episodes': accepted_episodes,  # Pass accepted episodes
                        'avg_relevance': avg_relevance,
                        'retrieval_time_ms': retrieval_time,
                        'success': True
                    }

            except httpx.TimeoutException as e:
                retrieval_time = (datetime.now() - start_time).total_seconds() * 1000

                if attempt < self.max_retries:
                    # Retry with exponential backoff
                    await asyncio.sleep(self.retry_delay_ms * (2 ** attempt) / 1000)
                    logger.warning(
                        f"AAG retrieval timeout (attempt {attempt + 1}/{self.max_retries + 1}), "
                        f"retrying after {self.retry_delay_ms * (2 ** attempt)}ms"
                    )
                    continue
                else:
                    # Final failure - graceful degradation
                    logger.error(
                        f"AAG retrieval failed after {self.max_retries + 1} attempts: "
                        f"timeout ({retrieval_time:.1f}ms)"
                    )
                    return {
                        'episodes': [],
                        'avg_relevance': 0.0,
                        'retrieval_time_ms': retrieval_time,
                        'success': False,
                        'error': f'Timeout after {retrieval_time:.1f}ms'
                    }

            except httpx.HTTPError as e:
                retrieval_time = (datetime.now() - start_time).total_seconds() * 1000

                if attempt < self.max_retries and e.response and e.response.status_code >= 500:
                    # Retry on 5xx errors
                    await asyncio.sleep(self.retry_delay_ms * (2 ** attempt) / 1000)
                    logger.warning(
                        f"AAG retrieval HTTP error {e.response.status_code} "
                        f"(attempt {attempt + 1}/{self.max_retries + 1}), retrying"
                    )
                    continue
                else:
                    # Final failure or 4xx error (don't retry client errors)
                    logger.error(f"AAG retrieval failed: HTTP {e.response.status_code if e.response else 'error'}")
                    return {
                        'episodes': [],
                        'avg_relevance': 0.0,
                        'retrieval_time_ms': retrieval_time,
                        'success': False,
                        'error': f'HTTP error: {e}'
                    }

            except Exception as e:
                retrieval_time = (datetime.now() - start_time).total_seconds() * 1000
                logger.error(f"AAG retrieval unexpected error: {e}")
                return {
                    'episodes': [],
                    'avg_relevance': 0.0,
                    'retrieval_time_ms': retrieval_time,
                    'success': False,
                    'error': f'Unexpected error: {e}'
                }

        # Should never reach here, but just in case
        return {
            'episodes': [],
            'avg_relevance': 0.0,
            'retrieval_time_ms': 0.0,
            'success': False,
            'error': 'Unknown error'
        }

    async def firm_audit(
        self,
        episode_id: str,
        confidence_threshold: float = 0.8
    ) -> Dict[str, Any]:
        """
        Validate episode using FIRM (Future Implementation - Pattern 2)

        Parameters:
        -----------
        episode_id : str
            Episode ID to validate
        confidence_threshold : float (default: 0.8)
            Minimum confidence score for validation

        Returns:
        --------
        result : Dict[str, Any]
            {
                'episode_id': str,
                'is_valid': bool,
                'confidence': float,
                'audit_report': dict
            }

        Note:
        -----
        This is a placeholder for future FIRM integration (Pattern 2).
        Currently returns mock validation.
        """
        # TODO: Implement when FIRM Pattern 2 is ready in PERSISTENCIA
        logger.warning("FIRM audit not yet implemented - returning mock validation")

        return {
            'episode_id': episode_id,
            'is_valid': True,
            'confidence': 1.0,
            'audit_report': {
                'note': 'FIRM validation not yet implemented'
            }
        }

    def get_stats(self) -> Dict[str, Any]:
        """
        Get client statistics (for monitoring)

        Returns:
        --------
        stats : Dict[str, Any]
            {
                'base_url': str,
                'timeout_ms': int,
                'max_retries': int
            }
        """
        return {
            'base_url': self.base_url,
            'timeout_ms': int(self.timeout.read * 1000),
            'max_retries': self.max_retries,
            'retry_delay_ms': self.retry_delay_ms
        }
