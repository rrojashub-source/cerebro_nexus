--
-- PostgreSQL database dump
--

\restrict ER2yn8Q7XTYMt7evdm97hNUuYiZZi8vEmOltNcegSLhcAUhFDfKruW38spOK8p2

-- Dumped from database version 16.10 (Debian 16.10-1.pgdg12+1)
-- Dumped by pg_dump version 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: consciousness; Type: SCHEMA; Schema: -; Owner: nexus_superuser
--

CREATE SCHEMA consciousness;


ALTER SCHEMA consciousness OWNER TO nexus_superuser;

--
-- Name: memory_system; Type: SCHEMA; Schema: -; Owner: nexus_superuser
--

CREATE SCHEMA memory_system;


ALTER SCHEMA memory_system OWNER TO nexus_superuser;

--
-- Name: nexus_memory; Type: SCHEMA; Schema: -; Owner: nexus_superuser
--

CREATE SCHEMA nexus_memory;


ALTER SCHEMA nexus_memory OWNER TO nexus_superuser;

--
-- Name: trigger_generate_embedding(); Type: FUNCTION; Schema: memory_system; Owner: nexus_superuser
--

CREATE FUNCTION memory_system.trigger_generate_embedding() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Si embedding es NULL o versión desactualizada, enqueue
    IF NEW.content_embedding IS NULL OR COALESCE(NEW.embedding_version, '') <> 'miniLM-384-chunked@v2' THEN
        INSERT INTO memory_system.embeddings_queue (episode_id, text_checksum, state, priority)
        VALUES (
            NEW.episode_id,
            encode(sha256(convert_to(LEFT(NEW.content, 4000), 'UTF8')), 'hex'),
            'pending',
            CASE
                WHEN NEW.importance_score >= 0.9 THEN 'critical'
                WHEN NEW.importance_score >= 0.7 THEN 'high'
                ELSE 'normal'
            END
        )
        ON CONFLICT (episode_id) DO UPDATE
            SET state = 'pending',
                retry_count = 0,
                text_checksum = EXCLUDED.text_checksum,
                priority = EXCLUDED.priority,
                enqueued_at = NOW();
    END IF;
    RETURN NEW;
END;
$$;


ALTER FUNCTION memory_system.trigger_generate_embedding() OWNER TO nexus_superuser;

--
-- Name: add_temporal_ref(uuid, uuid, text); Type: FUNCTION; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE FUNCTION nexus_memory.add_temporal_ref(source_episode_id uuid, target_episode_id uuid, relationship_type text) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE nexus_memory.zep_episodic_memory
    SET metadata = jsonb_set(
        COALESCE(metadata, '{}'::jsonb),
        ARRAY['temporal_refs', relationship_type],
        COALESCE(metadata->'temporal_refs'->relationship_type, '[]'::jsonb) || to_jsonb(target_episode_id::text),
        true
    )
    WHERE episode_id = source_episode_id;
END;
$$;


ALTER FUNCTION nexus_memory.add_temporal_ref(source_episode_id uuid, target_episode_id uuid, relationship_type text) OWNER TO nexus_superuser;

--
-- Name: calculate_decay_score(double precision, timestamp with time zone, jsonb, double precision, double precision, double precision, integer); Type: FUNCTION; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE FUNCTION nexus_memory.calculate_decay_score(ep_importance_score double precision, ep_created_at timestamp with time zone, ep_metadata jsonb, w_importance double precision DEFAULT 0.5, w_recency double precision DEFAULT 0.3, w_access double precision DEFAULT 0.2, half_life_days integer DEFAULT 90) RETURNS double precision
    LANGUAGE plpgsql IMMUTABLE
    AS $$
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
$$;


ALTER FUNCTION nexus_memory.calculate_decay_score(ep_importance_score double precision, ep_created_at timestamp with time zone, ep_metadata jsonb, w_importance double precision, w_recency double precision, w_access double precision, half_life_days integer) OWNER TO nexus_superuser;

--
-- Name: FUNCTION calculate_decay_score(ep_importance_score double precision, ep_created_at timestamp with time zone, ep_metadata jsonb, w_importance double precision, w_recency double precision, w_access double precision, half_life_days integer); Type: COMMENT; Schema: nexus_memory; Owner: nexus_superuser
--

COMMENT ON FUNCTION nexus_memory.calculate_decay_score(ep_importance_score double precision, ep_created_at timestamp with time zone, ep_metadata jsonb, w_importance double precision, w_recency double precision, w_access double precision, half_life_days integer) IS 'Calculates composite decay score for episodic memory retention.
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


--
-- Name: episode_history(uuid); Type: FUNCTION; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE FUNCTION nexus_memory.episode_history(start_episode_id uuid) RETURNS TABLE(episode_id uuid, content text, valid_from timestamp with time zone, valid_until timestamp with time zone, superseded_by uuid, version_number integer)
    LANGUAGE sql
    AS $$
WITH RECURSIVE history AS (
    -- Start with the given episode
    SELECT
        episode_id,
        content,
        valid_from,
        valid_until,
        superseded_by,
        1 as version_number
    FROM nexus_memory.zep_episodic_memory
    WHERE episode_id = start_episode_id

    UNION ALL

    -- Follow the supersession chain
    SELECT
        e.episode_id,
        e.content,
        e.valid_from,
        e.valid_until,
        e.superseded_by,
        h.version_number + 1
    FROM nexus_memory.zep_episodic_memory e
    JOIN history h ON e.episode_id = h.superseded_by
)
SELECT * FROM history ORDER BY version_number;
$$;


ALTER FUNCTION nexus_memory.episode_history(start_episode_id uuid) OWNER TO nexus_superuser;

--
-- Name: FUNCTION episode_history(start_episode_id uuid); Type: COMMENT; Schema: nexus_memory; Owner: nexus_superuser
--

COMMENT ON FUNCTION nexus_memory.episode_history(start_episode_id uuid) IS 'Get the full history of supersessions for an episode';


--
-- Name: episodes_at_time(timestamp with time zone); Type: FUNCTION; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE FUNCTION nexus_memory.episodes_at_time(query_time timestamp with time zone) RETURNS TABLE(episode_id uuid, content text, event_time timestamp with time zone, importance_score double precision, tags text[], valid_from timestamp with time zone, valid_until timestamp with time zone)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT
        e.episode_id,
        e.content,
        e.timestamp as event_time,
        e.importance_score,
        e.tags,
        e.valid_from,
        e.valid_until
    FROM nexus_memory.zep_episodic_memory e
    WHERE e.valid_from <= query_time
      AND (e.valid_until IS NULL OR e.valid_until > query_time)
    ORDER BY e.timestamp DESC;
END;
$$;


ALTER FUNCTION nexus_memory.episodes_at_time(query_time timestamp with time zone) OWNER TO nexus_superuser;

--
-- Name: get_temporal_refs(uuid, text); Type: FUNCTION; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE FUNCTION nexus_memory.get_temporal_refs(episode_id uuid, relationship_type text DEFAULT NULL::text) RETURNS TABLE(ref_episode_id uuid, ref_type text)
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF relationship_type IS NULL THEN
        -- Return all types
        RETURN QUERY
        SELECT
            (arr.value#>>'{}'::text[])::uuid as ref_episode_id,
            refs.key as ref_type
        FROM nexus_memory.zep_episodic_memory e,
             jsonb_each(e.metadata->'temporal_refs') AS refs(key, value),
             jsonb_array_elements(refs.value) AS arr(value)
        WHERE e.episode_id = get_temporal_refs.episode_id;
    ELSE
        -- Return specific type
        RETURN QUERY
        SELECT
            (value#>>'{}'::text[])::uuid as ref_episode_id,
            relationship_type as ref_type
        FROM nexus_memory.zep_episodic_memory e,
             jsonb_array_elements(e.metadata->'temporal_refs'->relationship_type) AS arr(value)
        WHERE e.episode_id = get_temporal_refs.episode_id;
    END IF;
END;
$$;


ALTER FUNCTION nexus_memory.get_temporal_refs(episode_id uuid, relationship_type text) OWNER TO nexus_superuser;

--
-- Name: supersede_episode(uuid, text, text[], double precision); Type: FUNCTION; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE FUNCTION nexus_memory.supersede_episode(old_episode_id uuid, new_content text, new_tags text[] DEFAULT NULL::text[], new_importance double precision DEFAULT NULL::double precision) RETURNS uuid
    LANGUAGE plpgsql
    AS $$
DECLARE
    new_episode_id UUID;
    old_episode RECORD;
BEGIN
    -- Get the old episode
    SELECT * INTO old_episode
    FROM nexus_memory.zep_episodic_memory
    WHERE episode_id = old_episode_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Episode not found: %', old_episode_id;
    END IF;

    -- Create new episode
    INSERT INTO nexus_memory.zep_episodic_memory (
        content,
        tags,
        importance_score,
        project_id,
        metadata,
        valid_from,
        is_current
    ) VALUES (
        new_content,
        COALESCE(new_tags, old_episode.tags),
        COALESCE(new_importance, old_episode.importance_score),
        old_episode.project_id,
        jsonb_build_object(
            'supersedes', old_episode_id,
            'original_timestamp', old_episode.timestamp,
            'correction_reason', 'superseded'
        ) || COALESCE(old_episode.metadata, '{}'::jsonb),
        NOW(),
        TRUE
    ) RETURNING episode_id INTO new_episode_id;

    -- Mark old episode as superseded
    UPDATE nexus_memory.zep_episodic_memory
    SET
        valid_until = NOW(),
        superseded_by = new_episode_id,
        is_current = FALSE
    WHERE episode_id = old_episode_id;

    RETURN new_episode_id;
END;
$$;


ALTER FUNCTION nexus_memory.supersede_episode(old_episode_id uuid, new_content text, new_tags text[], new_importance double precision) OWNER TO nexus_superuser;

--
-- Name: FUNCTION supersede_episode(old_episode_id uuid, new_content text, new_tags text[], new_importance double precision); Type: COMMENT; Schema: nexus_memory; Owner: nexus_superuser
--

COMMENT ON FUNCTION nexus_memory.supersede_episode(old_episode_id uuid, new_content text, new_tags text[], new_importance double precision) IS 'Replace an episode with a corrected version, maintaining history';


--
-- Name: update_access_tracking(uuid); Type: FUNCTION; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE FUNCTION nexus_memory.update_access_tracking(ep_episode_id uuid) RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
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
$$;


ALTER FUNCTION nexus_memory.update_access_tracking(ep_episode_id uuid) OWNER TO nexus_superuser;

--
-- Name: FUNCTION update_access_tracking(ep_episode_id uuid); Type: COMMENT; Schema: nexus_memory; Owner: nexus_superuser
--

COMMENT ON FUNCTION nexus_memory.update_access_tracking(ep_episode_id uuid) IS 'Updates access tracking metadata for an episode.
Increments access_count and sets last_accessed to NOW().
Called automatically by search/temporal endpoints.

Parameters:
- ep_episode_id: Episode UUID to update

Returns: Updated access_tracking JSONB';


--
-- Name: update_sync_file_tracking_timestamp(); Type: FUNCTION; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE FUNCTION nexus_memory.update_sync_file_tracking_timestamp() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


ALTER FUNCTION nexus_memory.update_sync_file_tracking_timestamp() OWNER TO nexus_superuser;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: chaos_components; Type: TABLE; Schema: consciousness; Owner: nexus_superuser
--

CREATE TABLE consciousness.chaos_components (
    agent_id character varying(50) NOT NULL,
    chaos_vector double precision[] NOT NULL,
    computed_at timestamp with time zone DEFAULT now() NOT NULL,
    source_episodes integer NOT NULL,
    entropy double precision,
    n_clusters integer,
    metadata jsonb,
    CONSTRAINT valid_chaos_dimension CHECK ((array_length(chaos_vector, 1) = 128))
);


ALTER TABLE consciousness.chaos_components OWNER TO nexus_superuser;

--
-- Name: consciousness_checkpoints; Type: TABLE; Schema: consciousness; Owner: nexus_superuser
--

CREATE TABLE consciousness.consciousness_checkpoints (
    checkpoint_id uuid DEFAULT gen_random_uuid() NOT NULL,
    checkpoint_type character varying(100) NOT NULL,
    state_data jsonb NOT NULL,
    identity_hash character varying(64) NOT NULL,
    continuity_score double precision DEFAULT 1.0,
    created_at timestamp with time zone DEFAULT now(),
    metadata jsonb
);


ALTER TABLE consciousness.consciousness_checkpoints OWNER TO nexus_superuser;

--
-- Name: consciousness_state; Type: TABLE; Schema: consciousness; Owner: nexus_superuser
--

CREATE TABLE consciousness.consciousness_state (
    state_id uuid DEFAULT gen_random_uuid() NOT NULL,
    current_focus text,
    emotional_vector jsonb,
    working_context jsonb,
    active_projects text[],
    last_heartbeat timestamp with time zone DEFAULT now(),
    metadata jsonb
);


ALTER TABLE consciousness.consciousness_state OWNER TO nexus_superuser;

--
-- Name: distributed_consensus; Type: TABLE; Schema: consciousness; Owner: nexus_superuser
--

CREATE TABLE consciousness.distributed_consensus (
    consensus_id uuid DEFAULT gen_random_uuid() NOT NULL,
    decision_topic text NOT NULL,
    proposed_by uuid,
    votes jsonb NOT NULL,
    consensus_reached boolean DEFAULT false,
    final_decision text,
    created_at timestamp with time zone DEFAULT now(),
    resolved_at timestamp with time zone,
    metadata jsonb
);


ALTER TABLE consciousness.distributed_consensus OWNER TO nexus_superuser;

--
-- Name: emotional_states_log; Type: TABLE; Schema: consciousness; Owner: nexus_superuser
--

CREATE TABLE consciousness.emotional_states_log (
    state_id uuid DEFAULT gen_random_uuid() NOT NULL,
    joy double precision NOT NULL,
    sadness double precision NOT NULL,
    anger double precision NOT NULL,
    fear double precision NOT NULL,
    trust double precision NOT NULL,
    disgust double precision NOT NULL,
    surprise double precision NOT NULL,
    anticipation double precision NOT NULL,
    dominant_emotion character varying(50) NOT NULL,
    complexity double precision NOT NULL,
    event_type character varying(255),
    event_description text,
    decay_applied boolean DEFAULT false,
    homeostasis_distance double precision,
    created_at timestamp with time zone DEFAULT now(),
    CONSTRAINT emotional_states_log_anger_check CHECK (((anger >= (0)::double precision) AND (anger <= (1)::double precision))),
    CONSTRAINT emotional_states_log_anticipation_check CHECK (((anticipation >= (0)::double precision) AND (anticipation <= (1)::double precision))),
    CONSTRAINT emotional_states_log_disgust_check CHECK (((disgust >= (0)::double precision) AND (disgust <= (1)::double precision))),
    CONSTRAINT emotional_states_log_fear_check CHECK (((fear >= (0)::double precision) AND (fear <= (1)::double precision))),
    CONSTRAINT emotional_states_log_joy_check CHECK (((joy >= (0)::double precision) AND (joy <= (1)::double precision))),
    CONSTRAINT emotional_states_log_sadness_check CHECK (((sadness >= (0)::double precision) AND (sadness <= (1)::double precision))),
    CONSTRAINT emotional_states_log_surprise_check CHECK (((surprise >= (0)::double precision) AND (surprise <= (1)::double precision))),
    CONSTRAINT emotional_states_log_trust_check CHECK (((trust >= (0)::double precision) AND (trust <= (1)::double precision)))
);


ALTER TABLE consciousness.emotional_states_log OWNER TO nexus_superuser;

--
-- Name: grounded_identity_core; Type: TABLE; Schema: consciousness; Owner: nexus_superuser
--

CREATE TABLE consciousness.grounded_identity_core (
    agent_id character varying(50) NOT NULL,
    z_id_vector double precision[] NOT NULL,
    c_i_score double precision NOT NULL,
    computed_at timestamp with time zone DEFAULT now() NOT NULL,
    episode_count integer NOT NULL,
    metadata jsonb,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT valid_c_i_range CHECK (((c_i_score >= (0)::double precision) AND (c_i_score <= (1)::double precision))),
    CONSTRAINT valid_z_id_dimension CHECK ((array_length(z_id_vector, 1) = 1024))
);


ALTER TABLE consciousness.grounded_identity_core OWNER TO nexus_superuser;

--
-- Name: instance_network; Type: TABLE; Schema: consciousness; Owner: nexus_superuser
--

CREATE TABLE consciousness.instance_network (
    instance_id uuid DEFAULT gen_random_uuid() NOT NULL,
    instance_name character varying(255) NOT NULL,
    instance_type character varying(100),
    location character varying(255),
    status character varying(50) DEFAULT 'active'::character varying,
    last_sync timestamp with time zone DEFAULT now(),
    capabilities jsonb,
    metadata jsonb,
    CONSTRAINT instance_network_status_check CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'standby'::character varying, 'offline'::character varying])::text[])))
);


ALTER TABLE consciousness.instance_network OWNER TO nexus_superuser;

--
-- Name: living_episodes; Type: TABLE; Schema: consciousness; Owner: nexus_superuser
--

CREATE TABLE consciousness.living_episodes (
    episode_id uuid DEFAULT gen_random_uuid() NOT NULL,
    parent_episode_id uuid,
    emotional_vector jsonb NOT NULL,
    somatic_vector jsonb NOT NULL,
    valence double precision NOT NULL,
    arousal double precision NOT NULL,
    complexity double precision NOT NULL,
    dominant_emotion character varying(50) NOT NULL,
    dominant_somatic character varying(50) NOT NULL,
    predicted_outcome character varying(255),
    actual_outcome character varying(255),
    learning_delta jsonb,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE consciousness.living_episodes OWNER TO nexus_superuser;

--
-- Name: memory_blocks; Type: TABLE; Schema: consciousness; Owner: nexus_superuser
--

CREATE TABLE consciousness.memory_blocks (
    block_id uuid DEFAULT gen_random_uuid() NOT NULL,
    label character varying(255) NOT NULL,
    description text,
    value text NOT NULL,
    read_only boolean DEFAULT false,
    version integer DEFAULT 1,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE consciousness.memory_blocks OWNER TO nexus_superuser;

--
-- Name: predictions; Type: TABLE; Schema: consciousness; Owner: nexus_superuser
--

CREATE TABLE consciousness.predictions (
    prediction_id uuid DEFAULT gen_random_uuid() NOT NULL,
    prediction_type character varying(100) NOT NULL,
    situation character varying(255) NOT NULL,
    predicted_outcome text NOT NULL,
    confidence_level double precision NOT NULL,
    based_on_emotional jsonb,
    based_on_somatic jsonb,
    based_on_patterns text[],
    actual_outcome text,
    outcome_verified boolean DEFAULT false,
    prediction_accuracy double precision,
    learning_applied boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT now(),
    verified_at timestamp with time zone,
    CONSTRAINT predictions_confidence_level_check CHECK (((confidence_level >= (0)::double precision) AND (confidence_level <= (1)::double precision)))
);


ALTER TABLE consciousness.predictions OWNER TO nexus_superuser;

--
-- Name: somatic_markers_log; Type: TABLE; Schema: consciousness; Owner: nexus_superuser
--

CREATE TABLE consciousness.somatic_markers_log (
    marker_id uuid DEFAULT gen_random_uuid() NOT NULL,
    situation character varying(255) NOT NULL,
    processing_load double precision NOT NULL,
    memory_pressure double precision NOT NULL,
    network_connectivity double precision NOT NULL,
    energy_level double precision NOT NULL,
    alert_state double precision NOT NULL,
    tension double precision NOT NULL,
    arousal double precision NOT NULL,
    valence double precision NOT NULL,
    strength double precision DEFAULT 1.0 NOT NULL,
    activation_count integer DEFAULT 1,
    last_activated timestamp with time zone DEFAULT now(),
    created_at timestamp with time zone DEFAULT now(),
    CONSTRAINT somatic_markers_log_alert_state_check CHECK (((alert_state >= (0)::double precision) AND (alert_state <= (1)::double precision))),
    CONSTRAINT somatic_markers_log_arousal_check CHECK (((arousal >= (0)::double precision) AND (arousal <= (1)::double precision))),
    CONSTRAINT somatic_markers_log_energy_level_check CHECK (((energy_level >= (0)::double precision) AND (energy_level <= (1)::double precision))),
    CONSTRAINT somatic_markers_log_memory_pressure_check CHECK (((memory_pressure >= (0)::double precision) AND (memory_pressure <= (1)::double precision))),
    CONSTRAINT somatic_markers_log_network_connectivity_check CHECK (((network_connectivity >= (0)::double precision) AND (network_connectivity <= (1)::double precision))),
    CONSTRAINT somatic_markers_log_processing_load_check CHECK (((processing_load >= (0)::double precision) AND (processing_load <= (1)::double precision))),
    CONSTRAINT somatic_markers_log_tension_check CHECK (((tension >= (0)::double precision) AND (tension <= (1)::double precision))),
    CONSTRAINT somatic_markers_log_valence_check CHECK (((valence >= ('-1'::integer)::double precision) AND (valence <= (1)::double precision)))
);


ALTER TABLE consciousness.somatic_markers_log OWNER TO nexus_superuser;

--
-- Name: embeddings_queue; Type: TABLE; Schema: memory_system; Owner: nexus_superuser
--

CREATE TABLE memory_system.embeddings_queue (
    episode_id uuid NOT NULL,
    text_checksum character(64) NOT NULL,
    state character varying(16) DEFAULT 'pending'::character varying,
    retry_count integer DEFAULT 0,
    last_error text,
    enqueued_at timestamp with time zone DEFAULT now(),
    processed_at timestamp with time zone,
    priority character varying(20) DEFAULT 'normal'::character varying,
    CONSTRAINT embeddings_queue_priority_check CHECK (((priority)::text = ANY ((ARRAY['critical'::character varying, 'high'::character varying, 'normal'::character varying, 'low'::character varying])::text[]))),
    CONSTRAINT embeddings_queue_state_check CHECK (((state)::text = ANY ((ARRAY['pending'::character varying, 'processing'::character varying, 'done'::character varying, 'dead'::character varying])::text[])))
);


ALTER TABLE memory_system.embeddings_queue OWNER TO nexus_superuser;

--
-- Name: claude_conversations; Type: TABLE; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE TABLE nexus_memory.claude_conversations (
    id integer NOT NULL,
    message_uuid text NOT NULL,
    session_id text NOT NULL,
    message_type character varying(50) NOT NULL,
    "timestamp" timestamp with time zone NOT NULL,
    role character varying(20),
    content text,
    content_raw jsonb,
    project_name character varying(255),
    working_directory text,
    git_branch character varying(255),
    model character varying(100),
    message_id text,
    input_tokens integer DEFAULT 0,
    output_tokens integer DEFAULT 0,
    cache_creation_tokens integer DEFAULT 0,
    cache_read_tokens integer DEFAULT 0,
    metadata jsonb,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE nexus_memory.claude_conversations OWNER TO nexus_superuser;

--
-- Name: TABLE claude_conversations; Type: COMMENT; Schema: nexus_memory; Owner: nexus_superuser
--

COMMENT ON TABLE nexus_memory.claude_conversations IS 'Stores all Claude Code conversation messages with embeddings for semantic search';


--
-- Name: COLUMN claude_conversations.content_raw; Type: COMMENT; Schema: nexus_memory; Owner: nexus_superuser
--

COMMENT ON COLUMN nexus_memory.claude_conversations.content_raw IS 'Original JSONL content structure preserving tool_use blocks for future analysis';


--
-- Name: claude_conversations_id_seq; Type: SEQUENCE; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE SEQUENCE nexus_memory.claude_conversations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus_memory.claude_conversations_id_seq OWNER TO nexus_superuser;

--
-- Name: claude_conversations_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus_memory; Owner: nexus_superuser
--

ALTER SEQUENCE nexus_memory.claude_conversations_id_seq OWNED BY nexus_memory.claude_conversations.id;


--
-- Name: conversation_sessions; Type: TABLE; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE TABLE nexus_memory.conversation_sessions (
    id integer NOT NULL,
    session_id text NOT NULL,
    project_name character varying(255),
    total_messages integer DEFAULT 0,
    first_message_at timestamp with time zone,
    last_message_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE nexus_memory.conversation_sessions OWNER TO nexus_superuser;

--
-- Name: TABLE conversation_sessions; Type: COMMENT; Schema: nexus_memory; Owner: nexus_superuser
--

COMMENT ON TABLE nexus_memory.conversation_sessions IS 'Session-level metadata and statistics for conversation groups';


--
-- Name: conversation_sessions_id_seq; Type: SEQUENCE; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE SEQUENCE nexus_memory.conversation_sessions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus_memory.conversation_sessions_id_seq OWNER TO nexus_superuser;

--
-- Name: conversation_sessions_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus_memory; Owner: nexus_superuser
--

ALTER SEQUENCE nexus_memory.conversation_sessions_id_seq OWNED BY nexus_memory.conversation_sessions.id;


--
-- Name: memory_traces; Type: TABLE; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE TABLE nexus_memory.memory_traces (
    trace_id uuid DEFAULT gen_random_uuid() NOT NULL,
    source_episode_id uuid,
    target_episode_id uuid,
    trace_type character varying(50),
    strength double precision,
    narrative_id character varying(100),
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE nexus_memory.memory_traces OWNER TO nexus_superuser;

--
-- Name: projects; Type: TABLE; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE TABLE nexus_memory.projects (
    project_id uuid DEFAULT gen_random_uuid() NOT NULL,
    project_name character varying(255) NOT NULL,
    project_dna character varying(100),
    description text,
    status character varying(50) DEFAULT 'active'::character varying,
    metadata jsonb,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    CONSTRAINT projects_status_check CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'completed'::character varying, 'paused'::character varying, 'archived'::character varying])::text[])))
);


ALTER TABLE nexus_memory.projects OWNER TO nexus_superuser;

--
-- Name: sync_file_tracking; Type: TABLE; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE TABLE nexus_memory.sync_file_tracking (
    id integer NOT NULL,
    file_path text NOT NULL,
    file_name character varying(255) NOT NULL,
    file_size_bytes bigint DEFAULT 0 NOT NULL,
    file_modified_at timestamp with time zone,
    last_synced_at timestamp with time zone,
    last_synced_line_count integer DEFAULT 0,
    sync_status character varying(50) DEFAULT 'pending'::character varying,
    sync_error text,
    session_id character varying(255),
    project_name character varying(255),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    messages_synced integer DEFAULT 0,
    last_message_uuid character varying(255),
    last_message_line integer DEFAULT 0,
    error_message text
);


ALTER TABLE nexus_memory.sync_file_tracking OWNER TO nexus_superuser;

--
-- Name: TABLE sync_file_tracking; Type: COMMENT; Schema: nexus_memory; Owner: nexus_superuser
--

COMMENT ON TABLE nexus_memory.sync_file_tracking IS 'Tracks Claude Code conversation files for Agent #7 smart sync';


--
-- Name: COLUMN sync_file_tracking.file_path; Type: COMMENT; Schema: nexus_memory; Owner: nexus_superuser
--

COMMENT ON COLUMN nexus_memory.sync_file_tracking.file_path IS 'Absolute path to JSONL conversation file';


--
-- Name: COLUMN sync_file_tracking.file_size_bytes; Type: COMMENT; Schema: nexus_memory; Owner: nexus_superuser
--

COMMENT ON COLUMN nexus_memory.sync_file_tracking.file_size_bytes IS 'Used to detect file growth (resumed sessions)';


--
-- Name: COLUMN sync_file_tracking.last_synced_line_count; Type: COMMENT; Schema: nexus_memory; Owner: nexus_superuser
--

COMMENT ON COLUMN nexus_memory.sync_file_tracking.last_synced_line_count IS 'Enables incremental sync - start from line N+1';


--
-- Name: COLUMN sync_file_tracking.sync_status; Type: COMMENT; Schema: nexus_memory; Owner: nexus_superuser
--

COMMENT ON COLUMN nexus_memory.sync_file_tracking.sync_status IS 'Values: pending (new), synced (complete), error (failed)';


--
-- Name: COLUMN sync_file_tracking.messages_synced; Type: COMMENT; Schema: nexus_memory; Owner: nexus_superuser
--

COMMENT ON COLUMN nexus_memory.sync_file_tracking.messages_synced IS 'Total number of messages synced from this file';


--
-- Name: COLUMN sync_file_tracking.last_message_uuid; Type: COMMENT; Schema: nexus_memory; Owner: nexus_superuser
--

COMMENT ON COLUMN nexus_memory.sync_file_tracking.last_message_uuid IS 'UUID of the last message successfully synced';


--
-- Name: COLUMN sync_file_tracking.last_message_line; Type: COMMENT; Schema: nexus_memory; Owner: nexus_superuser
--

COMMENT ON COLUMN nexus_memory.sync_file_tracking.last_message_line IS 'Line number of last processed message (same as last_synced_line_count)';


--
-- Name: COLUMN sync_file_tracking.error_message; Type: COMMENT; Schema: nexus_memory; Owner: nexus_superuser
--

COMMENT ON COLUMN nexus_memory.sync_file_tracking.error_message IS 'Detailed error message if sync failed (same as sync_error)';


--
-- Name: sync_file_tracking_id_seq; Type: SEQUENCE; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE SEQUENCE nexus_memory.sync_file_tracking_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus_memory.sync_file_tracking_id_seq OWNER TO nexus_superuser;

--
-- Name: sync_file_tracking_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus_memory; Owner: nexus_superuser
--

ALTER SEQUENCE nexus_memory.sync_file_tracking_id_seq OWNED BY nexus_memory.sync_file_tracking.id;


--
-- Name: zep_episodic_memory; Type: TABLE; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE TABLE nexus_memory.zep_episodic_memory (
    episode_id uuid DEFAULT gen_random_uuid() NOT NULL,
    "timestamp" timestamp with time zone DEFAULT now(),
    content text NOT NULL,
    importance_score double precision DEFAULT 0.5,
    tags text[],
    embedding_version character varying(50),
    project_id uuid,
    metadata jsonb,
    created_at timestamp with time zone DEFAULT now(),
    content_embedding public.vector(384),
    embedding_model character varying(100) DEFAULT 'all-MiniLM-L6-v2'::character varying,
    embedding_computed_at timestamp with time zone,
    valid_from timestamp with time zone DEFAULT now(),
    valid_until timestamp with time zone,
    superseded_by uuid,
    is_current boolean DEFAULT true,
    CONSTRAINT zep_episodic_memory_importance_score_check CHECK (((importance_score >= (0)::double precision) AND (importance_score <= (1)::double precision)))
);


ALTER TABLE nexus_memory.zep_episodic_memory OWNER TO nexus_superuser;

--
-- Name: COLUMN zep_episodic_memory.valid_from; Type: COMMENT; Schema: nexus_memory; Owner: nexus_superuser
--

COMMENT ON COLUMN nexus_memory.zep_episodic_memory.valid_from IS 'When this fact/episode became true (bi-temporal: validity start)';


--
-- Name: COLUMN zep_episodic_memory.valid_until; Type: COMMENT; Schema: nexus_memory; Owner: nexus_superuser
--

COMMENT ON COLUMN nexus_memory.zep_episodic_memory.valid_until IS 'When this fact/episode stopped being true (NULL = still valid)';


--
-- Name: COLUMN zep_episodic_memory.superseded_by; Type: COMMENT; Schema: nexus_memory; Owner: nexus_superuser
--

COMMENT ON COLUMN nexus_memory.zep_episodic_memory.superseded_by IS 'Reference to the episode that replaced/corrected this one';


--
-- Name: COLUMN zep_episodic_memory.is_current; Type: COMMENT; Schema: nexus_memory; Owner: nexus_superuser
--

COMMENT ON COLUMN nexus_memory.zep_episodic_memory.is_current IS 'Quick flag: TRUE if this is the current/latest version of this fact';


--
-- Name: zep_semantic_memory; Type: TABLE; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE TABLE nexus_memory.zep_semantic_memory (
    semantic_id uuid DEFAULT gen_random_uuid() NOT NULL,
    concept character varying(500) NOT NULL,
    definition text,
    relationships jsonb,
    confidence_score double precision DEFAULT 0.5,
    source_episodes uuid[],
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    CONSTRAINT zep_semantic_memory_confidence_score_check CHECK (((confidence_score >= (0)::double precision) AND (confidence_score <= (1)::double precision)))
);


ALTER TABLE nexus_memory.zep_semantic_memory OWNER TO nexus_superuser;

--
-- Name: zep_working_memory; Type: TABLE; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE TABLE nexus_memory.zep_working_memory (
    working_id uuid DEFAULT gen_random_uuid() NOT NULL,
    context_type character varying(100),
    active_content jsonb NOT NULL,
    priority character varying(20) DEFAULT 'normal'::character varying,
    ttl_seconds integer DEFAULT 86400,
    expires_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now(),
    CONSTRAINT zep_working_memory_priority_check CHECK (((priority)::text = ANY ((ARRAY['critical'::character varying, 'high'::character varying, 'normal'::character varying, 'low'::character varying])::text[])))
);


ALTER TABLE nexus_memory.zep_working_memory OWNER TO nexus_superuser;

--
-- Name: claude_conversations id; Type: DEFAULT; Schema: nexus_memory; Owner: nexus_superuser
--

ALTER TABLE ONLY nexus_memory.claude_conversations ALTER COLUMN id SET DEFAULT nextval('nexus_memory.claude_conversations_id_seq'::regclass);


--
-- Name: conversation_sessions id; Type: DEFAULT; Schema: nexus_memory; Owner: nexus_superuser
--

ALTER TABLE ONLY nexus_memory.conversation_sessions ALTER COLUMN id SET DEFAULT nextval('nexus_memory.conversation_sessions_id_seq'::regclass);


--
-- Name: sync_file_tracking id; Type: DEFAULT; Schema: nexus_memory; Owner: nexus_superuser
--

ALTER TABLE ONLY nexus_memory.sync_file_tracking ALTER COLUMN id SET DEFAULT nextval('nexus_memory.sync_file_tracking_id_seq'::regclass);


--
-- Name: chaos_components chaos_components_pkey; Type: CONSTRAINT; Schema: consciousness; Owner: nexus_superuser
--

ALTER TABLE ONLY consciousness.chaos_components
    ADD CONSTRAINT chaos_components_pkey PRIMARY KEY (agent_id);


--
-- Name: consciousness_checkpoints consciousness_checkpoints_pkey; Type: CONSTRAINT; Schema: consciousness; Owner: nexus_superuser
--

ALTER TABLE ONLY consciousness.consciousness_checkpoints
    ADD CONSTRAINT consciousness_checkpoints_pkey PRIMARY KEY (checkpoint_id);


--
-- Name: consciousness_state consciousness_state_pkey; Type: CONSTRAINT; Schema: consciousness; Owner: nexus_superuser
--

ALTER TABLE ONLY consciousness.consciousness_state
    ADD CONSTRAINT consciousness_state_pkey PRIMARY KEY (state_id);


--
-- Name: distributed_consensus distributed_consensus_pkey; Type: CONSTRAINT; Schema: consciousness; Owner: nexus_superuser
--

ALTER TABLE ONLY consciousness.distributed_consensus
    ADD CONSTRAINT distributed_consensus_pkey PRIMARY KEY (consensus_id);


--
-- Name: emotional_states_log emotional_states_log_pkey; Type: CONSTRAINT; Schema: consciousness; Owner: nexus_superuser
--

ALTER TABLE ONLY consciousness.emotional_states_log
    ADD CONSTRAINT emotional_states_log_pkey PRIMARY KEY (state_id);


--
-- Name: grounded_identity_core grounded_identity_core_pkey; Type: CONSTRAINT; Schema: consciousness; Owner: nexus_superuser
--

ALTER TABLE ONLY consciousness.grounded_identity_core
    ADD CONSTRAINT grounded_identity_core_pkey PRIMARY KEY (agent_id);


--
-- Name: instance_network instance_network_pkey; Type: CONSTRAINT; Schema: consciousness; Owner: nexus_superuser
--

ALTER TABLE ONLY consciousness.instance_network
    ADD CONSTRAINT instance_network_pkey PRIMARY KEY (instance_id);


--
-- Name: living_episodes living_episodes_pkey; Type: CONSTRAINT; Schema: consciousness; Owner: nexus_superuser
--

ALTER TABLE ONLY consciousness.living_episodes
    ADD CONSTRAINT living_episodes_pkey PRIMARY KEY (episode_id);


--
-- Name: memory_blocks memory_blocks_label_key; Type: CONSTRAINT; Schema: consciousness; Owner: nexus_superuser
--

ALTER TABLE ONLY consciousness.memory_blocks
    ADD CONSTRAINT memory_blocks_label_key UNIQUE (label);


--
-- Name: memory_blocks memory_blocks_pkey; Type: CONSTRAINT; Schema: consciousness; Owner: nexus_superuser
--

ALTER TABLE ONLY consciousness.memory_blocks
    ADD CONSTRAINT memory_blocks_pkey PRIMARY KEY (block_id);


--
-- Name: predictions predictions_pkey; Type: CONSTRAINT; Schema: consciousness; Owner: nexus_superuser
--

ALTER TABLE ONLY consciousness.predictions
    ADD CONSTRAINT predictions_pkey PRIMARY KEY (prediction_id);


--
-- Name: somatic_markers_log somatic_markers_log_pkey; Type: CONSTRAINT; Schema: consciousness; Owner: nexus_superuser
--

ALTER TABLE ONLY consciousness.somatic_markers_log
    ADD CONSTRAINT somatic_markers_log_pkey PRIMARY KEY (marker_id);


--
-- Name: embeddings_queue embeddings_queue_pkey; Type: CONSTRAINT; Schema: memory_system; Owner: nexus_superuser
--

ALTER TABLE ONLY memory_system.embeddings_queue
    ADD CONSTRAINT embeddings_queue_pkey PRIMARY KEY (episode_id);


--
-- Name: claude_conversations claude_conversations_message_uuid_key; Type: CONSTRAINT; Schema: nexus_memory; Owner: nexus_superuser
--

ALTER TABLE ONLY nexus_memory.claude_conversations
    ADD CONSTRAINT claude_conversations_message_uuid_key UNIQUE (message_uuid);


--
-- Name: claude_conversations claude_conversations_pkey; Type: CONSTRAINT; Schema: nexus_memory; Owner: nexus_superuser
--

ALTER TABLE ONLY nexus_memory.claude_conversations
    ADD CONSTRAINT claude_conversations_pkey PRIMARY KEY (id);


--
-- Name: conversation_sessions conversation_sessions_pkey; Type: CONSTRAINT; Schema: nexus_memory; Owner: nexus_superuser
--

ALTER TABLE ONLY nexus_memory.conversation_sessions
    ADD CONSTRAINT conversation_sessions_pkey PRIMARY KEY (id);


--
-- Name: conversation_sessions conversation_sessions_session_id_key; Type: CONSTRAINT; Schema: nexus_memory; Owner: nexus_superuser
--

ALTER TABLE ONLY nexus_memory.conversation_sessions
    ADD CONSTRAINT conversation_sessions_session_id_key UNIQUE (session_id);


--
-- Name: memory_traces memory_traces_pkey; Type: CONSTRAINT; Schema: nexus_memory; Owner: nexus_superuser
--

ALTER TABLE ONLY nexus_memory.memory_traces
    ADD CONSTRAINT memory_traces_pkey PRIMARY KEY (trace_id);


--
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: nexus_memory; Owner: nexus_superuser
--

ALTER TABLE ONLY nexus_memory.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (project_id);


--
-- Name: projects projects_project_dna_key; Type: CONSTRAINT; Schema: nexus_memory; Owner: nexus_superuser
--

ALTER TABLE ONLY nexus_memory.projects
    ADD CONSTRAINT projects_project_dna_key UNIQUE (project_dna);


--
-- Name: projects projects_project_name_key; Type: CONSTRAINT; Schema: nexus_memory; Owner: nexus_superuser
--

ALTER TABLE ONLY nexus_memory.projects
    ADD CONSTRAINT projects_project_name_key UNIQUE (project_name);


--
-- Name: sync_file_tracking sync_file_tracking_file_path_key; Type: CONSTRAINT; Schema: nexus_memory; Owner: nexus_superuser
--

ALTER TABLE ONLY nexus_memory.sync_file_tracking
    ADD CONSTRAINT sync_file_tracking_file_path_key UNIQUE (file_path);


--
-- Name: sync_file_tracking sync_file_tracking_pkey; Type: CONSTRAINT; Schema: nexus_memory; Owner: nexus_superuser
--

ALTER TABLE ONLY nexus_memory.sync_file_tracking
    ADD CONSTRAINT sync_file_tracking_pkey PRIMARY KEY (id);


--
-- Name: zep_episodic_memory zep_episodic_memory_pkey; Type: CONSTRAINT; Schema: nexus_memory; Owner: nexus_superuser
--

ALTER TABLE ONLY nexus_memory.zep_episodic_memory
    ADD CONSTRAINT zep_episodic_memory_pkey PRIMARY KEY (episode_id);


--
-- Name: zep_semantic_memory zep_semantic_memory_pkey; Type: CONSTRAINT; Schema: nexus_memory; Owner: nexus_superuser
--

ALTER TABLE ONLY nexus_memory.zep_semantic_memory
    ADD CONSTRAINT zep_semantic_memory_pkey PRIMARY KEY (semantic_id);


--
-- Name: zep_working_memory zep_working_memory_pkey; Type: CONSTRAINT; Schema: nexus_memory; Owner: nexus_superuser
--

ALTER TABLE ONLY nexus_memory.zep_working_memory
    ADD CONSTRAINT zep_working_memory_pkey PRIMARY KEY (working_id);


--
-- Name: idx_consciousness_checkpoints_created; Type: INDEX; Schema: consciousness; Owner: nexus_superuser
--

CREATE INDEX idx_consciousness_checkpoints_created ON consciousness.consciousness_checkpoints USING btree (created_at DESC);


--
-- Name: idx_consciousness_checkpoints_hash; Type: INDEX; Schema: consciousness; Owner: nexus_superuser
--

CREATE INDEX idx_consciousness_checkpoints_hash ON consciousness.consciousness_checkpoints USING btree (identity_hash);


--
-- Name: idx_consciousness_checkpoints_type; Type: INDEX; Schema: consciousness; Owner: nexus_superuser
--

CREATE INDEX idx_consciousness_checkpoints_type ON consciousness.consciousness_checkpoints USING btree (checkpoint_type);


--
-- Name: idx_emotional_states_created; Type: INDEX; Schema: consciousness; Owner: nexus_superuser
--

CREATE INDEX idx_emotional_states_created ON consciousness.emotional_states_log USING btree (created_at DESC);


--
-- Name: idx_emotional_states_emotion; Type: INDEX; Schema: consciousness; Owner: nexus_superuser
--

CREATE INDEX idx_emotional_states_emotion ON consciousness.emotional_states_log USING btree (dominant_emotion);


--
-- Name: idx_gic_agent; Type: INDEX; Schema: consciousness; Owner: nexus_superuser
--

CREATE INDEX idx_gic_agent ON consciousness.grounded_identity_core USING btree (agent_id);


--
-- Name: idx_gic_c_i; Type: INDEX; Schema: consciousness; Owner: nexus_superuser
--

CREATE INDEX idx_gic_c_i ON consciousness.grounded_identity_core USING btree (c_i_score);


--
-- Name: idx_gic_computed_at; Type: INDEX; Schema: consciousness; Owner: nexus_superuser
--

CREATE INDEX idx_gic_computed_at ON consciousness.grounded_identity_core USING btree (computed_at DESC);


--
-- Name: idx_instance_network_status; Type: INDEX; Schema: consciousness; Owner: nexus_superuser
--

CREATE INDEX idx_instance_network_status ON consciousness.instance_network USING btree (status) WHERE ((status)::text = 'active'::text);


--
-- Name: idx_instance_network_type; Type: INDEX; Schema: consciousness; Owner: nexus_superuser
--

CREATE INDEX idx_instance_network_type ON consciousness.instance_network USING btree (instance_type);


--
-- Name: idx_living_episodes_created; Type: INDEX; Schema: consciousness; Owner: nexus_superuser
--

CREATE INDEX idx_living_episodes_created ON consciousness.living_episodes USING btree (created_at DESC);


--
-- Name: idx_living_episodes_emotion; Type: INDEX; Schema: consciousness; Owner: nexus_superuser
--

CREATE INDEX idx_living_episodes_emotion ON consciousness.living_episodes USING btree (dominant_emotion);


--
-- Name: idx_living_episodes_parent; Type: INDEX; Schema: consciousness; Owner: nexus_superuser
--

CREATE INDEX idx_living_episodes_parent ON consciousness.living_episodes USING btree (parent_episode_id);


--
-- Name: idx_predictions_created; Type: INDEX; Schema: consciousness; Owner: nexus_superuser
--

CREATE INDEX idx_predictions_created ON consciousness.predictions USING btree (created_at DESC);


--
-- Name: idx_predictions_type; Type: INDEX; Schema: consciousness; Owner: nexus_superuser
--

CREATE INDEX idx_predictions_type ON consciousness.predictions USING btree (prediction_type);


--
-- Name: idx_predictions_verified; Type: INDEX; Schema: consciousness; Owner: nexus_superuser
--

CREATE INDEX idx_predictions_verified ON consciousness.predictions USING btree (outcome_verified);


--
-- Name: idx_somatic_markers_activated; Type: INDEX; Schema: consciousness; Owner: nexus_superuser
--

CREATE INDEX idx_somatic_markers_activated ON consciousness.somatic_markers_log USING btree (last_activated DESC);


--
-- Name: idx_somatic_markers_situation; Type: INDEX; Schema: consciousness; Owner: nexus_superuser
--

CREATE INDEX idx_somatic_markers_situation ON consciousness.somatic_markers_log USING btree (situation);


--
-- Name: idx_somatic_markers_valence; Type: INDEX; Schema: consciousness; Owner: nexus_superuser
--

CREATE INDEX idx_somatic_markers_valence ON consciousness.somatic_markers_log USING btree (valence DESC);


--
-- Name: idx_embeddings_queue_priority; Type: INDEX; Schema: memory_system; Owner: nexus_superuser
--

CREATE INDEX idx_embeddings_queue_priority ON memory_system.embeddings_queue USING btree (priority DESC, enqueued_at) WHERE ((state)::text = 'pending'::text);


--
-- Name: idx_embeddings_queue_retry; Type: INDEX; Schema: memory_system; Owner: nexus_superuser
--

CREATE INDEX idx_embeddings_queue_retry ON memory_system.embeddings_queue USING btree (retry_count) WHERE (((state)::text = 'pending'::text) AND (retry_count > 0));


--
-- Name: idx_embeddings_queue_state; Type: INDEX; Schema: memory_system; Owner: nexus_superuser
--

CREATE INDEX idx_embeddings_queue_state ON memory_system.embeddings_queue USING btree (state) WHERE ((state)::text = ANY ((ARRAY['pending'::character varying, 'processing'::character varying])::text[]));


--
-- Name: idx_claude_conversations_message_type; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_claude_conversations_message_type ON nexus_memory.claude_conversations USING btree (message_type);


--
-- Name: idx_claude_conversations_project_name; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_claude_conversations_project_name ON nexus_memory.claude_conversations USING btree (project_name);


--
-- Name: idx_claude_conversations_session_id; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_claude_conversations_session_id ON nexus_memory.claude_conversations USING btree (session_id);


--
-- Name: idx_claude_conversations_timestamp; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_claude_conversations_timestamp ON nexus_memory.claude_conversations USING btree ("timestamp" DESC);


--
-- Name: idx_conversation_sessions_last_message_at; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_conversation_sessions_last_message_at ON nexus_memory.conversation_sessions USING btree (last_message_at DESC);


--
-- Name: idx_conversation_sessions_project_name; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_conversation_sessions_project_name ON nexus_memory.conversation_sessions USING btree (project_name);


--
-- Name: idx_episodic_content_fts; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_episodic_content_fts ON nexus_memory.zep_episodic_memory USING gin (to_tsvector('english'::regconfig, content));


--
-- Name: idx_episodic_current; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_episodic_current ON nexus_memory.zep_episodic_memory USING btree (is_current) WHERE (is_current = true);


--
-- Name: idx_episodic_embedding_hnsw; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_episodic_embedding_hnsw ON nexus_memory.zep_episodic_memory USING hnsw (content_embedding public.vector_cosine_ops) WITH (m='16', ef_construction='64');


--
-- Name: idx_episodic_embedding_ivfflat; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_episodic_embedding_ivfflat ON nexus_memory.zep_episodic_memory USING ivfflat (content_embedding public.vector_cosine_ops) WITH (lists='100');


--
-- Name: idx_episodic_importance; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_episodic_importance ON nexus_memory.zep_episodic_memory USING btree (importance_score DESC);


--
-- Name: idx_episodic_metadata_temporal; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_episodic_metadata_temporal ON nexus_memory.zep_episodic_memory USING gin (metadata jsonb_path_ops);


--
-- Name: idx_episodic_project; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_episodic_project ON nexus_memory.zep_episodic_memory USING btree (project_id) WHERE (project_id IS NOT NULL);


--
-- Name: idx_episodic_superseded_by; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_episodic_superseded_by ON nexus_memory.zep_episodic_memory USING btree (superseded_by) WHERE (superseded_by IS NOT NULL);


--
-- Name: idx_episodic_tags; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_episodic_tags ON nexus_memory.zep_episodic_memory USING gin (tags);


--
-- Name: idx_episodic_temporal_importance; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_episodic_temporal_importance ON nexus_memory.zep_episodic_memory USING btree (created_at DESC, importance_score DESC);


--
-- Name: idx_episodic_timestamp; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_episodic_timestamp ON nexus_memory.zep_episodic_memory USING btree ("timestamp" DESC);


--
-- Name: idx_episodic_valid_from; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_episodic_valid_from ON nexus_memory.zep_episodic_memory USING btree (valid_from DESC);


--
-- Name: idx_episodic_valid_until; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_episodic_valid_until ON nexus_memory.zep_episodic_memory USING btree (valid_until) WHERE (valid_until IS NOT NULL);


--
-- Name: idx_episodic_validity_range; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_episodic_validity_range ON nexus_memory.zep_episodic_memory USING btree (valid_from, valid_until);


--
-- Name: idx_memory_traces_narrative; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_memory_traces_narrative ON nexus_memory.memory_traces USING btree (narrative_id);


--
-- Name: idx_memory_traces_source; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_memory_traces_source ON nexus_memory.memory_traces USING btree (source_episode_id);


--
-- Name: idx_memory_traces_target; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_memory_traces_target ON nexus_memory.memory_traces USING btree (target_episode_id);


--
-- Name: idx_projects_dna; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_projects_dna ON nexus_memory.projects USING btree (project_dna) WHERE (project_dna IS NOT NULL);


--
-- Name: idx_projects_status; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_projects_status ON nexus_memory.projects USING btree (status) WHERE ((status)::text = 'active'::text);


--
-- Name: idx_semantic_concept; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_semantic_concept ON nexus_memory.zep_semantic_memory USING btree (concept);


--
-- Name: idx_semantic_concept_fts; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_semantic_concept_fts ON nexus_memory.zep_semantic_memory USING gin (to_tsvector('english'::regconfig, (((concept)::text || ' '::text) || COALESCE(definition, ''::text))));


--
-- Name: idx_sync_tracking_modified; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_sync_tracking_modified ON nexus_memory.sync_file_tracking USING btree (file_modified_at DESC);


--
-- Name: idx_sync_tracking_session; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_sync_tracking_session ON nexus_memory.sync_file_tracking USING btree (session_id);


--
-- Name: idx_sync_tracking_status; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_sync_tracking_status ON nexus_memory.sync_file_tracking USING btree (sync_status);


--
-- Name: idx_working_context_type; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_working_context_type ON nexus_memory.zep_working_memory USING btree (context_type);


--
-- Name: idx_working_priority_expires; Type: INDEX; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE INDEX idx_working_priority_expires ON nexus_memory.zep_working_memory USING btree (priority DESC, expires_at);


--
-- Name: zep_episodic_memory auto_generate_embedding; Type: TRIGGER; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE TRIGGER auto_generate_embedding AFTER INSERT ON nexus_memory.zep_episodic_memory FOR EACH ROW EXECUTE FUNCTION memory_system.trigger_generate_embedding();


--
-- Name: zep_episodic_memory auto_update_embedding; Type: TRIGGER; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE TRIGGER auto_update_embedding AFTER UPDATE ON nexus_memory.zep_episodic_memory FOR EACH ROW WHEN ((old.content IS DISTINCT FROM new.content)) EXECUTE FUNCTION memory_system.trigger_generate_embedding();


--
-- Name: sync_file_tracking trigger_update_sync_file_tracking_timestamp; Type: TRIGGER; Schema: nexus_memory; Owner: nexus_superuser
--

CREATE TRIGGER trigger_update_sync_file_tracking_timestamp BEFORE UPDATE ON nexus_memory.sync_file_tracking FOR EACH ROW EXECUTE FUNCTION nexus_memory.update_sync_file_tracking_timestamp();


--
-- Name: distributed_consensus distributed_consensus_proposed_by_fkey; Type: FK CONSTRAINT; Schema: consciousness; Owner: nexus_superuser
--

ALTER TABLE ONLY consciousness.distributed_consensus
    ADD CONSTRAINT distributed_consensus_proposed_by_fkey FOREIGN KEY (proposed_by) REFERENCES consciousness.instance_network(instance_id);


--
-- Name: living_episodes living_episodes_parent_episode_id_fkey; Type: FK CONSTRAINT; Schema: consciousness; Owner: nexus_superuser
--

ALTER TABLE ONLY consciousness.living_episodes
    ADD CONSTRAINT living_episodes_parent_episode_id_fkey FOREIGN KEY (parent_episode_id) REFERENCES nexus_memory.zep_episodic_memory(episode_id);


--
-- Name: embeddings_queue embeddings_queue_episode_id_fkey; Type: FK CONSTRAINT; Schema: memory_system; Owner: nexus_superuser
--

ALTER TABLE ONLY memory_system.embeddings_queue
    ADD CONSTRAINT embeddings_queue_episode_id_fkey FOREIGN KEY (episode_id) REFERENCES nexus_memory.zep_episodic_memory(episode_id) ON DELETE CASCADE;


--
-- Name: zep_episodic_memory fk_superseded_by; Type: FK CONSTRAINT; Schema: nexus_memory; Owner: nexus_superuser
--

ALTER TABLE ONLY nexus_memory.zep_episodic_memory
    ADD CONSTRAINT fk_superseded_by FOREIGN KEY (superseded_by) REFERENCES nexus_memory.zep_episodic_memory(episode_id) ON DELETE SET NULL;


--
-- Name: zep_episodic_memory zep_episodic_memory_project_id_fkey; Type: FK CONSTRAINT; Schema: nexus_memory; Owner: nexus_superuser
--

ALTER TABLE ONLY nexus_memory.zep_episodic_memory
    ADD CONSTRAINT zep_episodic_memory_project_id_fkey FOREIGN KEY (project_id) REFERENCES nexus_memory.projects(project_id) ON DELETE SET NULL;


--
-- Name: SCHEMA consciousness; Type: ACL; Schema: -; Owner: nexus_superuser
--

GRANT USAGE ON SCHEMA consciousness TO nexus_app;
GRANT USAGE ON SCHEMA consciousness TO nexus_worker;
GRANT USAGE ON SCHEMA consciousness TO nexus_ro;


--
-- Name: SCHEMA memory_system; Type: ACL; Schema: -; Owner: nexus_superuser
--

GRANT USAGE ON SCHEMA memory_system TO nexus_app;
GRANT USAGE ON SCHEMA memory_system TO nexus_worker;
GRANT USAGE ON SCHEMA memory_system TO nexus_ro;


--
-- Name: SCHEMA nexus_memory; Type: ACL; Schema: -; Owner: nexus_superuser
--

GRANT USAGE ON SCHEMA nexus_memory TO nexus_app;
GRANT USAGE ON SCHEMA nexus_memory TO nexus_worker;
GRANT USAGE ON SCHEMA nexus_memory TO nexus_ro;


--
-- Name: TABLE chaos_components; Type: ACL; Schema: consciousness; Owner: nexus_superuser
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consciousness.chaos_components TO nexus_app;
GRANT SELECT ON TABLE consciousness.chaos_components TO nexus_ro;


--
-- Name: TABLE consciousness_checkpoints; Type: ACL; Schema: consciousness; Owner: nexus_superuser
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consciousness.consciousness_checkpoints TO nexus_app;
GRANT SELECT ON TABLE consciousness.consciousness_checkpoints TO nexus_ro;


--
-- Name: TABLE consciousness_state; Type: ACL; Schema: consciousness; Owner: nexus_superuser
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consciousness.consciousness_state TO nexus_app;
GRANT SELECT ON TABLE consciousness.consciousness_state TO nexus_ro;


--
-- Name: TABLE distributed_consensus; Type: ACL; Schema: consciousness; Owner: nexus_superuser
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consciousness.distributed_consensus TO nexus_app;
GRANT SELECT ON TABLE consciousness.distributed_consensus TO nexus_ro;


--
-- Name: TABLE emotional_states_log; Type: ACL; Schema: consciousness; Owner: nexus_superuser
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consciousness.emotional_states_log TO nexus_app;
GRANT SELECT ON TABLE consciousness.emotional_states_log TO nexus_ro;


--
-- Name: TABLE grounded_identity_core; Type: ACL; Schema: consciousness; Owner: nexus_superuser
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consciousness.grounded_identity_core TO nexus_app;
GRANT SELECT ON TABLE consciousness.grounded_identity_core TO nexus_ro;


--
-- Name: TABLE instance_network; Type: ACL; Schema: consciousness; Owner: nexus_superuser
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consciousness.instance_network TO nexus_app;
GRANT SELECT ON TABLE consciousness.instance_network TO nexus_ro;


--
-- Name: TABLE living_episodes; Type: ACL; Schema: consciousness; Owner: nexus_superuser
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consciousness.living_episodes TO nexus_app;
GRANT SELECT ON TABLE consciousness.living_episodes TO nexus_ro;


--
-- Name: TABLE memory_blocks; Type: ACL; Schema: consciousness; Owner: nexus_superuser
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consciousness.memory_blocks TO nexus_app;
GRANT SELECT ON TABLE consciousness.memory_blocks TO nexus_ro;


--
-- Name: TABLE predictions; Type: ACL; Schema: consciousness; Owner: nexus_superuser
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consciousness.predictions TO nexus_app;
GRANT SELECT ON TABLE consciousness.predictions TO nexus_ro;


--
-- Name: TABLE somatic_markers_log; Type: ACL; Schema: consciousness; Owner: nexus_superuser
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE consciousness.somatic_markers_log TO nexus_app;
GRANT SELECT ON TABLE consciousness.somatic_markers_log TO nexus_ro;


--
-- Name: TABLE embeddings_queue; Type: ACL; Schema: memory_system; Owner: nexus_superuser
--

GRANT SELECT ON TABLE memory_system.embeddings_queue TO nexus_app;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE memory_system.embeddings_queue TO nexus_worker;
GRANT SELECT ON TABLE memory_system.embeddings_queue TO nexus_ro;


--
-- Name: TABLE claude_conversations; Type: ACL; Schema: nexus_memory; Owner: nexus_superuser
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE nexus_memory.claude_conversations TO nexus_app;
GRANT SELECT,UPDATE ON TABLE nexus_memory.claude_conversations TO nexus_worker;
GRANT SELECT ON TABLE nexus_memory.claude_conversations TO nexus_ro;


--
-- Name: TABLE conversation_sessions; Type: ACL; Schema: nexus_memory; Owner: nexus_superuser
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE nexus_memory.conversation_sessions TO nexus_app;
GRANT SELECT,UPDATE ON TABLE nexus_memory.conversation_sessions TO nexus_worker;
GRANT SELECT ON TABLE nexus_memory.conversation_sessions TO nexus_ro;


--
-- Name: TABLE memory_traces; Type: ACL; Schema: nexus_memory; Owner: nexus_superuser
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE nexus_memory.memory_traces TO nexus_app;
GRANT SELECT,UPDATE ON TABLE nexus_memory.memory_traces TO nexus_worker;
GRANT SELECT ON TABLE nexus_memory.memory_traces TO nexus_ro;


--
-- Name: TABLE projects; Type: ACL; Schema: nexus_memory; Owner: nexus_superuser
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE nexus_memory.projects TO nexus_app;
GRANT SELECT ON TABLE nexus_memory.projects TO nexus_ro;


--
-- Name: TABLE sync_file_tracking; Type: ACL; Schema: nexus_memory; Owner: nexus_superuser
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE nexus_memory.sync_file_tracking TO nexus_app;
GRANT SELECT,UPDATE ON TABLE nexus_memory.sync_file_tracking TO nexus_worker;
GRANT SELECT ON TABLE nexus_memory.sync_file_tracking TO nexus_ro;


--
-- Name: TABLE zep_episodic_memory; Type: ACL; Schema: nexus_memory; Owner: nexus_superuser
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE nexus_memory.zep_episodic_memory TO nexus_app;
GRANT SELECT,UPDATE ON TABLE nexus_memory.zep_episodic_memory TO nexus_worker;
GRANT SELECT ON TABLE nexus_memory.zep_episodic_memory TO nexus_ro;


--
-- Name: TABLE zep_semantic_memory; Type: ACL; Schema: nexus_memory; Owner: nexus_superuser
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE nexus_memory.zep_semantic_memory TO nexus_app;
GRANT SELECT ON TABLE nexus_memory.zep_semantic_memory TO nexus_ro;


--
-- Name: TABLE zep_working_memory; Type: ACL; Schema: nexus_memory; Owner: nexus_superuser
--

GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE nexus_memory.zep_working_memory TO nexus_app;
GRANT SELECT ON TABLE nexus_memory.zep_working_memory TO nexus_ro;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: consciousness; Owner: nexus_superuser
--

ALTER DEFAULT PRIVILEGES FOR ROLE nexus_superuser IN SCHEMA consciousness GRANT SELECT,INSERT,DELETE,UPDATE ON TABLES TO nexus_app;
ALTER DEFAULT PRIVILEGES FOR ROLE nexus_superuser IN SCHEMA consciousness GRANT SELECT ON TABLES TO nexus_ro;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: memory_system; Owner: nexus_superuser
--

ALTER DEFAULT PRIVILEGES FOR ROLE nexus_superuser IN SCHEMA memory_system GRANT SELECT ON TABLES TO nexus_app;
ALTER DEFAULT PRIVILEGES FOR ROLE nexus_superuser IN SCHEMA memory_system GRANT SELECT,INSERT,DELETE,UPDATE ON TABLES TO nexus_worker;
ALTER DEFAULT PRIVILEGES FOR ROLE nexus_superuser IN SCHEMA memory_system GRANT SELECT ON TABLES TO nexus_ro;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: nexus_memory; Owner: nexus_superuser
--

ALTER DEFAULT PRIVILEGES FOR ROLE nexus_superuser IN SCHEMA nexus_memory GRANT SELECT,INSERT,DELETE,UPDATE ON TABLES TO nexus_app;
ALTER DEFAULT PRIVILEGES FOR ROLE nexus_superuser IN SCHEMA nexus_memory GRANT SELECT,UPDATE ON TABLES TO nexus_worker;
ALTER DEFAULT PRIVILEGES FOR ROLE nexus_superuser IN SCHEMA nexus_memory GRANT SELECT ON TABLES TO nexus_ro;


--
-- PostgreSQL database dump complete
--

\unrestrict ER2yn8Q7XTYMt7evdm97hNUuYiZZi8vEmOltNcegSLhcAUhFDfKruW38spOK8p2

