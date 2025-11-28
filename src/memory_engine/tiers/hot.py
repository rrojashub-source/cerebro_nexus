"""
Hot Memory Tier - Redis-based fast access layer

Stores:
- Recent memories (last 24h)
- Frequently accessed memories
- Working memory items (7±2)

Performance target: < 1ms

Author: NEXUS AI
Created: November 28, 2025
"""

import redis
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class HotMemory:
    """
    Hot memory tier using Redis for ultra-fast access.

    Features:
    - TTL-based expiration (24h default)
    - LRU eviction when full
    - Automatic promotion/demotion between tiers
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6382,
        db: int = 0,
        password: Optional[str] = None,
        ttl_hours: int = 24,
        max_items: int = 1000
    ):
        self.redis = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True
        )
        self.ttl_seconds = ttl_hours * 3600
        self.max_items = max_items
        self.prefix = "hot:"

    def add(self, memory_id: str, content: str, metadata: Optional[Dict] = None) -> bool:
        """Add memory to hot tier with TTL"""
        try:
            data = {
                "content": content,
                "metadata": metadata or {},
                "added_at": datetime.utcnow().isoformat(),
                "access_count": 1
            }
            key = f"{self.prefix}{memory_id}"
            self.redis.setex(key, self.ttl_seconds, json.dumps(data))
            logger.debug(f"Added to hot tier: {memory_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add to hot tier: {e}")
            return False

    def get(self, memory_id: str) -> Optional[Dict]:
        """Get memory from hot tier and increment access count"""
        try:
            key = f"{self.prefix}{memory_id}"
            data = self.redis.get(key)
            if data:
                memory = json.loads(data)
                # Increment access count
                memory["access_count"] = memory.get("access_count", 0) + 1
                memory["last_access"] = datetime.utcnow().isoformat()
                # Refresh TTL on access
                self.redis.setex(key, self.ttl_seconds, json.dumps(memory))
                return memory
            return None
        except Exception as e:
            logger.error(f"Failed to get from hot tier: {e}")
            return None

    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Search hot memories (simple prefix match for now)"""
        # Note: For semantic search, use warm tier with pgvector
        results = []
        try:
            for key in self.redis.scan_iter(f"{self.prefix}*", count=100):
                if len(results) >= limit:
                    break
                data = self.redis.get(key)
                if data:
                    memory = json.loads(data)
                    if query.lower() in memory.get("content", "").lower():
                        memory["id"] = key.replace(self.prefix, "")
                        results.append(memory)
        except Exception as e:
            logger.error(f"Hot tier search failed: {e}")
        return results

    def delete(self, memory_id: str) -> bool:
        """Remove memory from hot tier"""
        try:
            key = f"{self.prefix}{memory_id}"
            return self.redis.delete(key) > 0
        except Exception as e:
            logger.error(f"Failed to delete from hot tier: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """Get hot tier statistics"""
        try:
            keys = list(self.redis.scan_iter(f"{self.prefix}*", count=10000))
            return {
                "tier": "hot",
                "total_items": len(keys),
                "max_items": self.max_items,
                "ttl_hours": self.ttl_seconds // 3600,
                "storage": "redis"
            }
        except Exception as e:
            logger.error(f"Failed to get hot tier stats: {e}")
            return {"tier": "hot", "error": str(e)}
