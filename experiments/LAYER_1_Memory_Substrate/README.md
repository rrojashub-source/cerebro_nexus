# Layer 1: Memory Substrate

**Status:** ✅ Operational
**Implementation Date:** October 2025
**Purpose:** Neural data storage foundation

---

## Overview

Layer 1 provides the **persistent storage infrastructure** for all cognitive LABs. It mimics biological neural storage through three complementary technologies.

---

## Components

### PostgreSQL 16 (Port 5437)
**Role:** Long-term episodic memory storage

- **Database:** `nexus_memory` schema
- **Main Table:** `zep_episodic_memory`
- **Records:** 467+ episodes
- **Extensions:** pgvector for semantic search
- **Performance:** <10ms semantic search (p95)

**Biological Analogy:** Cortical long-term memory

### pgvector Extension
**Role:** Semantic similarity search

- **Embedding Model:** all-MiniLM-L6-v2 (384 dimensions)
- **Index Type:** HNSW (Hierarchical Navigable Small World)
- **Search Method:** Cosine similarity
- **Accuracy:** 90%+ retrieval accuracy

**Biological Analogy:** Semantic memory networks

### Redis 7 (Port 6382)
**Role:** Working memory cache & activation buffer

- **Capacity:** 7±2 items (Miller's Law)
- **TTL:** 300s default
- **Purpose:** Short-term context, query cache, embeddings queue
- **Performance:** <1ms cache hits

**Biological Analogy:** Working memory (prefrontal cortex)

---

## Architecture

```
┌──────────────────────────────────────────┐
│          Cognitive LABs (Layer 2+)       │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│              Redis Cache                  │
│           (Working Memory)                │
│             Port 6382                     │
└──────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────┐
│         PostgreSQL + pgvector             │
│        (Long-term Storage)                │
│             Port 5437                     │
└──────────────────────────────────────────┘
```

---

## Key Features

### Episodic Memory Storage
- **UUID-based episodes** with timestamps
- **JSON metadata** for flexible attributes
- **Vector embeddings** for semantic search
- **Tag system** for categorization

### Semantic Search
- **Vector similarity** using pgvector
- **HNSW indexing** for fast retrieval
- **Cosine similarity** scoring
- **<10ms response time** (avg 7-10ms)

### Working Memory Cache
- **7-item buffer** (cognitive limit)
- **FIFO eviction** policy
- **Redis-backed** for speed
- **TTL management** for freshness

---

## Performance Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| **Semantic Search p95** | <200ms | 59ms ✅ |
| **Semantic Search avg** | <100ms | 32ms ✅ |
| **Cache Hit Ratio** | >80% | ~75% 🟡 |
| **Embeddings Success** | 100% | 100% ✅ |
| **Episodes Stored** | Unlimited | 467+ ✅ |

---

## Docker Services

### nexus_postgresql_v2
```yaml
Image: postgres:16
Port: 5437
Extensions: pgvector
Schema: nexus_memory
User: nexus_superuser
```

### nexus_redis_master
```yaml
Image: redis:7.4.1
Port: 6382
Persistence: AOF + RDB
Max Memory: 256MB
Eviction: allkeys-lru
```

---

## Health Checks

```bash
# PostgreSQL
docker exec -it nexus_postgresql_v2 psql -U nexus_superuser -d nexus_db \
  -c "SELECT COUNT(*) FROM nexus_memory.zep_episodic_memory;"

# Redis
docker exec -it nexus_redis_master redis-cli -p 6382 PING

# API health (includes DB checks)
curl http://localhost:8003/health
```

---

## Backup Strategy

### PostgreSQL Backups
- **Location:** `/mnt/z/NEXUS_BACKUPS/`
- **Frequency:** Daily automatic
- **Retention:** 30 days
- **Method:** `pg_dump`

### Redis Persistence
- **AOF:** Enabled (fsync every second)
- **RDB:** Enabled (save 900 1, 300 10, 60 10000)
- **Backup:** Snapshots in `/mnt/z/NEXUS_BACKUPS/redis/`

---

## Database Schema

### Main Table: zep_episodic_memory

```sql
CREATE TABLE nexus_memory.zep_episodic_memory (
    episode_id UUID PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    agent_id UUID,
    action_type VARCHAR(50),
    action_details JSONB,
    context JSONB,
    reasoning JSONB,
    embedding VECTOR(384),  -- pgvector
    tags TEXT[],
    confidence_score FLOAT,
    session_id UUID,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- HNSW Index for fast similarity search
CREATE INDEX idx_zep_episodic_memory_embedding_cosine
ON nexus_memory.zep_episodic_memory
USING hnsw (embedding vector_cosine_ops);
```

---

## Integration with Upper Layers

### Layer 2 (Cognitive LABs)
- **LAB_010 (Attention)** → Query cache in Redis
- **LAB_011 (Working Memory)** → 7-item buffer in Redis
- **LAB_009 (Reconsolidation)** → Update episodes in PostgreSQL

### Layer 3 (Neurochemistry)
- **LAB_002 (Decay)** → Modulate importance scores
- **LAB_003 (Sleep)** → Consolidate important episodes
- **LAB_005 (Spreading)** → Prime related memories in cache

---

## Troubleshooting

### PostgreSQL Connection Issues
```bash
# Check container status
docker ps | grep nexus_postgresql_v2

# View logs
docker logs nexus_postgresql_v2 --tail 50

# Restart
docker restart nexus_postgresql_v2
```

### Redis Connection Issues
```bash
# Check status
docker exec -it nexus_redis_master redis-cli -p 6382 INFO

# Clear cache
docker exec -it nexus_redis_master redis-cli -p 6382 FLUSHDB
```

### Slow Queries
```bash
# Rebuild HNSW index
docker exec -it nexus_postgresql_v2 psql -U nexus_superuser -d nexus_db \
  -c "REINDEX INDEX CONCURRENTLY idx_zep_episodic_memory_embedding_cosine;"
```

---

**Maintained by:** Ricardo + NEXUS
**Last Updated:** November 4, 2025
**Status:** ✅ Production-ready
