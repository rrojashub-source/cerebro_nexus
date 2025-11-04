-- ============================================================
-- INTELLIGENT DECAY SYSTEM - DECAY SCORING ALGORITHM
-- ============================================================
-- Created: October 27, 2025
-- Phase: FASE_8_UPGRADE Week 5-6
-- Purpose: Calculate decay scores for episodic memory retention
--
-- Inspired by: Mem0 (26% accuracy boost), MemGPT tiered memory
-- ============================================================

-- ============================================================
-- FUNCTION: calculate_decay_score
-- ============================================================
-- Calculates a composite decay score based on:
--   1. Importance factor (0.5 weight)
--   2. Recency factor (0.3 weight) - exponential decay
--   3. Access factor (0.2 weight) - frequency + recency of access
--
-- Returns: Float 0.0-1.0 (higher = more valuable, should retain)
-- ============================================================

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
    recency_boost FLOAT;
    frequency_boost FLOAT;
    decay_score FLOAT;
BEGIN
    -- ========================================
    -- 1. IMPORTANCE FACTOR
    -- ========================================
    -- Use existing importance_score (0.0-1.0)
    -- Default to 0.5 if not set
    importance_factor := COALESCE(ep_importance_score, 0.5);

    -- ========================================
    -- 2. RECENCY FACTOR (Exponential Decay)
    -- ========================================
    -- Calculate age in days
    age_days := EXTRACT(EPOCH FROM (NOW() - ep_created_at)) / 86400.0;

    -- Exponential decay with configurable half-life
    -- Formula: e^(-age_days / half_life_days)
    -- Result:
    --   Day 0: 1.0
    --   Day 90 (half-life): 0.5
    --   Day 180: 0.25
    --   Day 365: ~0.01
    recency_factor := EXP(-age_days / half_life_days);

    -- ========================================
    -- 3. ACCESS FACTOR
    -- ========================================
    -- Extract access tracking from metadata
    access_count := COALESCE(
        (ep_metadata->'access_tracking'->>'access_count')::INT,
        0
    );

    -- Calculate last_accessed_days
    IF ep_metadata->'access_tracking'->>'last_accessed' IS NOT NULL THEN
        last_accessed_days := EXTRACT(EPOCH FROM (
            NOW() - (ep_metadata->'access_tracking'->>'last_accessed')::TIMESTAMPTZ
        )) / 86400.0;
    ELSE
        -- Never accessed, use age
        last_accessed_days := age_days;
    END IF;

    -- Recency boost: Recently accessed = more valuable
    -- 30-day relevance window
    -- Formula: e^(-last_accessed_days / 30)
    recency_boost := EXP(-last_accessed_days / 30.0);

    -- Frequency boost: Frequently accessed = more valuable
    -- Saturates at 10 accesses (access_count / 10, capped at 1.0)
    frequency_boost := LEAST(1.0, access_count / 10.0);

    -- Combined access factor (average of recency and frequency)
    access_factor := (recency_boost + frequency_boost) / 2.0;

    -- ========================================
    -- 4. COMPOSITE DECAY SCORE
    -- ========================================
    -- Weighted combination of all factors
    -- Default weights: importance 50%, recency 30%, access 20%
    decay_score := (
        w_importance * importance_factor +
        w_recency * recency_factor +
        w_access * access_factor
    );

    -- Ensure result is in valid range [0.0, 1.0]
    decay_score := LEAST(1.0, GREATEST(0.0, decay_score));

    RETURN decay_score;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- ============================================================
-- COMMENTS
-- ============================================================
COMMENT ON FUNCTION nexus_memory.calculate_decay_score IS
'Calculates composite decay score for episodic memory retention.
Higher scores (closer to 1.0) indicate more valuable memories to retain.
Lower scores (closer to 0.0) indicate candidates for pruning.

Parameters:
- ep_importance_score: Original importance (0.0-1.0)
- ep_created_at: Episode creation timestamp
- ep_metadata: Episode metadata JSONB (must contain access_tracking)
- w_importance: Weight for importance factor (default 0.5)
- w_recency: Weight for recency factor (default 0.3)
- w_access: Weight for access factor (default 0.2)
- half_life_days: Decay half-life in days (default 90)

Returns: Float 0.0-1.0';

-- ============================================================
-- HELPER FUNCTION: update_access_tracking
-- ============================================================
-- Updates access_tracking metadata when an episode is retrieved
-- Increments access_count and updates last_accessed timestamp
-- ============================================================

CREATE OR REPLACE FUNCTION nexus_memory.update_access_tracking(
    ep_episode_id UUID
) RETURNS JSONB AS $$
DECLARE
    current_metadata JSONB;
    current_count INT;
    updated_metadata JSONB;
BEGIN
    -- Get current metadata
    SELECT metadata INTO current_metadata
    FROM nexus_memory.zep_episodic_memory
    WHERE episode_id = ep_episode_id;

    IF current_metadata IS NULL THEN
        current_metadata := '{}'::JSONB;
    END IF;

    -- Get current access count
    current_count := COALESCE(
        (current_metadata->'access_tracking'->>'access_count')::INT,
        0
    );

    -- Build updated access_tracking
    updated_metadata := jsonb_set(
        COALESCE(current_metadata, '{}'::JSONB),
        '{access_tracking}',
        jsonb_build_object(
            'access_count', current_count + 1,
            'last_accessed', NOW()::TEXT
        )
    );

    -- Update the episode
    UPDATE nexus_memory.zep_episodic_memory
    SET metadata = updated_metadata
    WHERE episode_id = ep_episode_id;

    RETURN updated_metadata->'access_tracking';
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION nexus_memory.update_access_tracking IS
'Updates access tracking metadata for an episode.
Increments access_count and sets last_accessed to NOW().
Called automatically by search/temporal endpoints.

Parameters:
- ep_episode_id: Episode UUID to update

Returns: Updated access_tracking JSONB';

-- ============================================================
-- USAGE EXAMPLES
-- ============================================================

-- Example 1: Calculate decay score for a specific episode
-- SELECT
--     episode_id,
--     importance_score,
--     created_at,
--     nexus_memory.calculate_decay_score(
--         importance_score,
--         created_at,
--         metadata
--     ) as decay_score
-- FROM nexus_memory.zep_episodic_memory
-- WHERE episode_id = 'YOUR-EPISODE-ID';

-- Example 2: Find low-value episodes (decay_score < 0.2)
-- SELECT
--     episode_id,
--     LEFT(content, 80) as content_preview,
--     importance_score,
--     AGE(NOW(), created_at) as age,
--     nexus_memory.calculate_decay_score(
--         importance_score,
--         created_at,
--         metadata
--     ) as decay_score
-- FROM nexus_memory.zep_episodic_memory
-- WHERE nexus_memory.calculate_decay_score(
--         importance_score,
--         created_at,
--         metadata
--     ) < 0.2
-- ORDER BY decay_score ASC
-- LIMIT 20;

-- Example 3: Update access tracking when retrieving episode
-- SELECT nexus_memory.update_access_tracking('YOUR-EPISODE-ID'::UUID);

-- Example 4: Decay score distribution analysis
-- SELECT
--     CASE
--         WHEN decay_score >= 0.8 THEN 'Very High (0.8-1.0)'
--         WHEN decay_score >= 0.6 THEN 'High (0.6-0.8)'
--         WHEN decay_score >= 0.4 THEN 'Medium (0.4-0.6)'
--         WHEN decay_score >= 0.2 THEN 'Low (0.2-0.4)'
--         ELSE 'Very Low (0.0-0.2)'
--     END as score_category,
--     COUNT(*) as episode_count,
--     ROUND(AVG(decay_score)::NUMERIC, 3) as avg_score
-- FROM (
--     SELECT
--         nexus_memory.calculate_decay_score(
--             importance_score,
--             created_at,
--             metadata
--         ) as decay_score
--     FROM nexus_memory.zep_episodic_memory
-- ) scores
-- GROUP BY score_category
-- ORDER BY
--     CASE score_category
--         WHEN 'Very High (0.8-1.0)' THEN 1
--         WHEN 'High (0.6-0.8)' THEN 2
--         WHEN 'Medium (0.4-0.6)' THEN 3
--         WHEN 'Low (0.2-0.4)' THEN 4
--         WHEN 'Very Low (0.0-0.2)' THEN 5
--     END;

-- ============================================================
-- END OF DECAY SCORING ALGORITHM
-- ============================================================
