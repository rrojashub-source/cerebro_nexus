# Intelligent Decay System - NEXUS V2.0.0

**Date:** October 27, 2025
**Phase:** FASE_8_UPGRADE Week 5-6
**Status:** Design Phase

---

## Overview

Intelligent memory retention system that automatically manages episodic memory lifecycle based on importance, recency, and usage patterns. Implements "forgetting as a feature" - gradually reducing influence of low-value memories to maintain system performance and relevance.

**Inspired by:** Mem0 (26% accuracy boost), MemGPT tiered memory

---

## Current NEXUS State

### Existing Schema
```sql
nexus_memory.zep_episodic_memory:
- episode_id (UUID)
- content (TEXT)
- importance_score (FLOAT) -- Already exists! (0.0-1.0)
- created_at (TIMESTAMPTZ)
- updated_at (TIMESTAMPTZ)
- embedding (VECTOR(384))
- tags (TEXT[])
- metadata (JSONB)
```

**Strengths:**
- ✅ importance_score already captured at creation
- ✅ Timestamps for age calculation
- ✅ JSONB metadata for flexible tracking

**Gaps:**
- ❌ No access tracking (how often queried)
- ❌ No last_accessed timestamp
- ❌ No decay score calculation
- ❌ No automatic pruning

---

## Intelligent Decay Algorithm

### Decay Score Formula

**Composite Score** = Weighted combination of 3 factors:

```python
decay_score = (
    w1 * importance_factor +
    w2 * recency_factor +
    w3 * access_factor
)

# Default weights (configurable):
w1 = 0.5  # Importance (most critical)
w2 = 0.3  # Recency
w3 = 0.2  # Access patterns
```

### Factor Calculations

#### 1. Importance Factor
```python
importance_factor = importance_score  # Already 0.0-1.0
```

**Simple:** Use existing importance_score from episode creation.

#### 2. Recency Factor (Exponential Decay)
```python
age_days = (now - created_at).days
half_life_days = 90  # Configurable

recency_factor = exp(-age_days / half_life_days)
```

**Curve:**
- Day 0: 1.0
- Day 90: 0.5
- Day 180: 0.25
- Day 365: ~0.01

#### 3. Access Factor
```python
access_count = metadata.get("access_count", 0)
last_accessed_days = (now - metadata.get("last_accessed")).days if exists else age_days

# Boost for recently accessed
recency_boost = exp(-last_accessed_days / 30)  # 30-day relevance window

# Boost for frequently accessed
frequency_boost = min(1.0, access_count / 10)  # Saturates at 10 accesses

access_factor = (recency_boost + frequency_boost) / 2
```

---

## Implementation Design

### Phase 1: Access Tracking (Schema Enhancement)

**Add to metadata JSONB:**
```json
{
  "access_tracking": {
    "access_count": 0,
    "last_accessed": null,
    "access_history": []  // Optional: last 5 access timestamps
  }
}
```

**Update on every retrieval:**
- `/memory/search` → increment access_count
- `/memory/temporal/*` → increment access_count
- Update last_accessed timestamp

### Phase 2: Decay Scoring Function

**PostgreSQL Function:**
```sql
CREATE OR REPLACE FUNCTION nexus_memory.calculate_decay_score(
    ep_importance_score FLOAT,
    ep_created_at TIMESTAMPTZ,
    ep_metadata JSONB,
    w_importance FLOAT DEFAULT 0.5,
    w_recency FLOAT DEFAULT 0.3,
    w_access FLOAT DEFAULT 0.2,
    half_life_days INT DEFAULT 90
) RETURNS FLOAT AS $$
DECLARE
    age_days FLOAT;
    recency_factor FLOAT;
    importance_factor FLOAT;
    access_factor FLOAT;
    access_count INT;
    last_accessed_days FLOAT;
    decay_score FLOAT;
BEGIN
    -- Importance factor
    importance_factor := COALESCE(ep_importance_score, 0.5);

    -- Recency factor (exponential decay)
    age_days := EXTRACT(EPOCH FROM (NOW() - ep_created_at)) / 86400.0;
    recency_factor := EXP(-age_days / half_life_days);

    -- Access factor
    access_count := COALESCE((ep_metadata->'access_tracking'->>'access_count')::INT, 0);

    IF ep_metadata->'access_tracking'->>'last_accessed' IS NOT NULL THEN
        last_accessed_days := EXTRACT(EPOCH FROM (
            NOW() - (ep_metadata->'access_tracking'->>'last_accessed')::TIMESTAMPTZ
        )) / 86400.0;
    ELSE
        last_accessed_days := age_days;
    END IF;

    -- Access factor (recency + frequency)
    access_factor := (
        EXP(-last_accessed_days / 30.0) +
        LEAST(1.0, access_count / 10.0)
    ) / 2.0;

    -- Composite decay score
    decay_score := (
        w_importance * importance_factor +
        w_recency * recency_factor +
        w_access * access_factor
    );

    RETURN decay_score;
END;
$$ LANGUAGE plpgsql IMMUTABLE;
```

### Phase 3: API Endpoints

#### 1. `/memory/analysis/decay-scores`
**Purpose:** Analyze current memory state

```python
@app.get("/memory/analysis/decay-scores")
async def get_decay_analysis(
    limit: int = 100,
    min_age_days: int = 30  # Only analyze memories older than this
):
    """
    Calculate decay scores for episodes and return distribution

    Returns:
    - Total episodes analyzed
    - Score distribution (percentiles: p10, p25, p50, p75, p90)
    - Low-value candidates (score < 0.2)
    - High-value protected (score > 0.7)
    """
```

#### 2. `/memory/pruning/preview`
**Purpose:** Preview what would be pruned (dry-run)

```python
@app.post("/memory/pruning/preview")
async def preview_pruning(
    min_score_threshold: float = 0.2,
    min_age_days: int = 90,
    max_prune_count: int = 100
):
    """
    Preview episodes that would be pruned

    Safety rules:
    - Never prune episodes < min_age_days old
    - Never prune episodes with importance_score > 0.8
    - Never prune episodes with specific tags (milestones, critical)
    - Cap at max_prune_count per operation

    Returns list of candidate episodes with scores
    """
```

#### 3. `/memory/pruning/execute`
**Purpose:** Actually prune low-value memories

```python
@app.post("/memory/pruning/execute")
async def execute_pruning(
    min_score_threshold: float = 0.2,
    min_age_days: int = 90,
    max_prune_count: int = 100,
    dry_run: bool = True  # Safety: default to dry-run
):
    """
    Execute memory pruning

    Options:
    - soft_delete: Move to archive table (recommended)
    - hard_delete: Actually DELETE from database (dangerous)

    Returns:
    - pruned_count
    - freed_space_mb
    - execution_time
    """
```

#### 4. `/memory/access-tracking/update` (Internal)
**Purpose:** Called internally on every retrieval

```python
async def update_access_tracking(episode_id: str):
    """
    Increment access_count and update last_accessed
    Called automatically by search/temporal endpoints
    """
```

### Phase 4: Automatic Scheduled Pruning

**Cron job / Background task:**
```python
# Run weekly: Sunday 2 AM
async def scheduled_pruning_job():
    """
    Automatic pruning with conservative defaults:
    - min_score_threshold: 0.15 (very low)
    - min_age_days: 180 (6 months)
    - max_prune_count: 50 per week

    Logs all actions to audit trail
    """
```

---

## Safety Mechanisms

### Protected Episodes (Never Prune)

1. **By Importance:**
   - importance_score > 0.8 (critical memories)

2. **By Tag:**
   - "milestone"
   - "critical"
   - "protected"
   - "consciousness" (state tracking)

3. **By Age:**
   - Created in last 30 days (too recent to judge)

4. **By Recent Access:**
   - Accessed in last 7 days (clearly still relevant)

### Soft Delete (Recommended)

Instead of hard DELETE, move to archive:

```sql
-- Archive table (same schema)
CREATE TABLE nexus_memory.zep_episodic_memory_archive (
    LIKE nexus_memory.zep_episodic_memory INCLUDING ALL
);

-- Add archival metadata
ALTER TABLE nexus_memory.zep_episodic_memory_archive
ADD COLUMN archived_at TIMESTAMPTZ DEFAULT NOW(),
ADD COLUMN decay_score_at_archival FLOAT,
ADD COLUMN archival_reason TEXT;
```

**Benefits:**
- Can restore if needed
- Audit trail
- No data loss
- Can analyze archived data

---

## Configuration

### System-wide Defaults

```python
INTELLIGENT_DECAY_CONFIG = {
    # Weights (must sum to 1.0)
    "weight_importance": 0.5,
    "weight_recency": 0.3,
    "weight_access": 0.2,

    # Decay curve
    "half_life_days": 90,
    "access_relevance_window_days": 30,
    "frequency_saturation_count": 10,

    # Pruning thresholds
    "min_score_threshold": 0.2,
    "min_age_days": 90,
    "max_prune_per_operation": 100,

    # Safety
    "protected_tags": ["milestone", "critical", "protected", "consciousness"],
    "protected_importance_threshold": 0.8,
    "min_age_for_pruning_days": 30,
    "recent_access_protection_days": 7,

    # Scheduling
    "auto_pruning_enabled": false,  # Disabled by default
    "auto_pruning_schedule": "0 2 * * 0",  # Weekly Sunday 2 AM
}
```

---

## Testing Strategy

### Test Scenarios

1. **Decay Score Calculation**
   - New episode (age 0): High score
   - Old unused episode (age 180, never accessed): Low score
   - Old but important (importance 0.9): Protected
   - Old but frequently accessed: Moderate score

2. **Access Tracking**
   - Search query increments access_count
   - Temporal queries increment access_count
   - last_accessed timestamp updates

3. **Pruning Preview**
   - Identifies low-value candidates correctly
   - Respects protection rules
   - Dry-run doesn't delete anything

4. **Pruning Execution**
   - Soft delete to archive works
   - Protected episodes never deleted
   - Freed space calculated correctly

5. **Real Workload**
   - Run on 543 production episodes
   - Analyze score distribution
   - Preview pruning candidates
   - Validate safety rules

---

## Performance Considerations

### Query Optimization

**Decay score calculation is expensive.** Don't calculate on every query.

**Strategy:**
- Pre-calculate scores periodically (daily)
- Store in materialized view or metadata
- Use for analysis/pruning only

### Index Needs

```sql
-- For finding old low-value episodes
CREATE INDEX idx_episodic_importance_age
ON nexus_memory.zep_episodic_memory(importance_score, created_at);

-- For access tracking lookups
CREATE INDEX idx_episodic_metadata_access
ON nexus_memory.zep_episodic_memory USING GIN ((metadata->'access_tracking'));
```

---

## Success Metrics

**After implementation:**
1. ✅ 90%+ of high-importance memories retained
2. ✅ 50%+ reduction in low-value old memories
3. ✅ Zero critical data loss
4. ✅ Measurable performance improvement (query latency)
5. ✅ System stays within storage limits

---

## Implementation Plan

### Phase 1: Foundation (2 hours)
- PostgreSQL decay_score function
- Access tracking in metadata
- Update search endpoints to track access

### Phase 2: Analysis (1 hour)
- `/memory/analysis/decay-scores` endpoint
- Test with 543 production episodes
- Generate score distribution report

### Phase 3: Pruning (2 hours)
- `/memory/pruning/preview` endpoint
- `/memory/pruning/execute` endpoint
- Archive table creation
- Safety validations

### Phase 4: Testing (1 hour)
- Test all safety mechanisms
- Validate with real data
- Performance benchmarks

**Total: 6 hours estimated**

---

## References

- **Mem0:** 26% accuracy boost, decay-based forgetting
- **MemGPT:** Tiered memory swapping
- **NEXUS Current:** 543 episodes, importance_score system
- **Target:** Intelligent automatic memory management

---

**Status:** Design Complete - Ready for Implementation
**Next:** Implement Phase 1 (decay_score function + access tracking)
