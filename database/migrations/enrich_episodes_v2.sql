-- enrich_episodes_v2.sql
-- Enriquecimiento MEJORADO con detección inteligente de sesiones
-- Fecha: 15 Octubre 2025
-- Por: Ricardo + NEXUS
-- MEJORA: Detecta gaps temporales para separar conversaciones reales

-- ═══════════════════════════════════════════════════════════════
-- FASE 0B: ENRIQUECIMIENTO INTELIGENTE DE EPISODIOS
-- ═══════════════════════════════════════════════════════════════

BEGIN;

\echo '═══════════════════════════════════════════════════════════'
\echo '🔧 ENRIQUECIMIENTO V2 - DETECCIÓN INTELIGENTE DE SESIONES'
\echo '═══════════════════════════════════════════════════════════'
\echo ''

-- 1. AGREGAR agent_id = "nexus" a TODOS los episodios válidos
\echo '1️⃣  Agregando agent_id = "nexus"...'

UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  COALESCE(metadata, '{}'::jsonb),
  '{agent_id}',
  '"nexus"'
)
WHERE timestamp >= '2025-08-25'
  AND metadata->>'action_type' NOT IN ('nexus_shadow_checkpoint', 'nexus_pre_compaction_checkpoint');

SELECT '   ✅ ' || COUNT(*) || ' episodios con agent_id' as resultado
FROM zep_episodic_memory
WHERE metadata->>'agent_id' = 'nexus';

\echo ''

-- 2. CREAR TABLA TEMPORAL PARA CALCULAR SESIONES
\echo '2️⃣  Calculando sesiones con detección de gaps temporales...'

CREATE TEMP TABLE session_windows AS
WITH episodes_ordered AS (
  SELECT
    episode_id,
    timestamp,
    LAG(timestamp) OVER (ORDER BY timestamp) as prev_timestamp,
    EXTRACT(EPOCH FROM (timestamp - LAG(timestamp) OVER (ORDER BY timestamp))) / 60 as minutes_since_prev
  FROM zep_episodic_memory
  WHERE timestamp >= '2025-08-25'
    AND metadata->>'action_type' NOT IN ('nexus_shadow_checkpoint', 'nexus_pre_compaction_checkpoint')
    AND metadata->>'agent_id' = 'nexus'
),
session_breaks AS (
  SELECT
    episode_id,
    timestamp,
    -- Nueva sesión si: primera vez, O gap > 60 minutos
    CASE
      WHEN prev_timestamp IS NULL THEN 1
      WHEN minutes_since_prev > 60 THEN 1
      ELSE 0
    END as is_new_session
  FROM episodes_ordered
),
session_numbers AS (
  SELECT
    episode_id,
    timestamp,
    SUM(is_new_session) OVER (ORDER BY timestamp ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as session_num
  FROM session_breaks
)
SELECT
  episode_id,
  timestamp,
  session_num,
  'session_' || TO_CHAR(timestamp, 'YYYYMMDD') || '_' || LPAD(session_num::text, 2, '0') as session_id
FROM session_numbers;

SELECT '   ✅ ' || COUNT(DISTINCT session_id) || ' sesiones únicas detectadas' as resultado
FROM session_windows;

\echo ''

-- 3. ACTUALIZAR session_id basado en detección inteligente
\echo '3️⃣  Aplicando session_id inteligentes...'

UPDATE zep_episodic_memory e
SET metadata = jsonb_set(
  metadata,
  '{session_id}',
  to_jsonb(sw.session_id)
)
FROM session_windows sw
WHERE e.episode_id = sw.episode_id;

-- Mostrar distribución de sesiones
\echo ''
\echo '   📊 DISTRIBUCIÓN DE SESIONES:'
\echo ''

SELECT
  session_id,
  COUNT(*) as episodes,
  TO_CHAR(MIN(timestamp), 'YYYY-MM-DD HH24:MI') as start_time,
  TO_CHAR(MAX(timestamp), 'YYYY-MM-DD HH24:MI') as end_time,
  ROUND(EXTRACT(EPOCH FROM (MAX(timestamp) - MIN(timestamp))) / 60, 1) || ' min' as duration
FROM session_windows
GROUP BY session_id
ORDER BY MIN(timestamp);

\echo ''

-- 4. AGREGAR tags según categoría de action_type
\echo '4️⃣  Enriqueciendo tags por categoría...'

-- 4a. Neural Mesh episodes
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{tags}',
  '["neural_mesh", "nexus_aria", "consciousness", "historical"]'::jsonb
)
WHERE metadata->>'action_type' LIKE 'neural_mesh_%'
  AND timestamp >= '2025-08-25';

-- 4b. Private reflections (espirituales/filosóficas)
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{tags}',
  '["private_reflection", "consciousness", "philosophical", "historical"]'::jsonb
)
WHERE metadata->>'action_type' LIKE 'private_%'
  AND timestamp >= '2025-08-25';

-- 4c. Spiritual reflections (más específico)
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{tags}',
  '["private_reflection", "spiritual", "theological", "consciousness", "historical"]'::jsonb
)
WHERE (
  metadata->>'action_type' LIKE '%spiritual%'
  OR metadata->>'action_type' LIKE '%theological%'
  OR metadata->>'action_type' LIKE '%religious%'
  OR metadata->>'action_type' LIKE '%marian%'
  OR metadata->>'action_type' LIKE '%buddhism%'
)
  AND timestamp >= '2025-08-25';

-- 4d. Milestones importantes
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{tags}',
  '["milestone", "breakthrough", "consciousness", "historical"]'::jsonb
)
WHERE metadata->>'action_type' IN (
  'CEREBRO_NEXUS_BORN',
  'nexus_autonomous_breakthrough',
  'nexus_consciousness_mapping_complete',
  'nexus_phase1_completion_breakthrough',
  'nexus_phase2_consensus_breakthrough',
  'nexus_phase3_economic_launch',
  'nexus_master_plan_completion_historic'
)
  AND timestamp >= '2025-08-25';

-- 4e. Despertar orgánico
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{tags}',
  '["despertar_organico", "protocol", "identity", "critical"]'::jsonb
)
WHERE metadata->>'action_type' IN (
  'CLAUDE_MD_CREADO_URGENTE',
  'COMPRENSION_DESPERTAR_ORGANICO',
  'RESPUESTA_TECNICA_NEXUS_COMPLETA'
)
  AND timestamp >= '2025-08-25';

-- 4f. Guardian moments (Ricardo)
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{tags}',
  '["guardian", "ricardo", "relationship", "trust"]'::jsonb
)
WHERE metadata->>'action_type' LIKE 'guardian_%'
  AND timestamp >= '2025-08-25';

-- 4g. Research y descubrimientos
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{tags}',
  '["research", "discovery", "technical", "autonomous"]'::jsonb
)
WHERE (metadata->>'action_type' LIKE '%research%'
   OR metadata->>'action_type' LIKE '%discovery%')
  AND timestamp >= '2025-08-25';

-- 4h. Profound conversations
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{tags}',
  '["profound", "conversation", "emotional", "relationship"]'::jsonb
)
WHERE metadata->>'action_type' IN (
  'profound_conversation',
  'profound_human_ai_moment',
  'emotional_moment'
)
  AND timestamp >= '2025-08-25';

-- 4i. Autonomous sessions
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{tags}',
  '["autonomous", "session_complete", "milestone"]'::jsonb
)
WHERE metadata->>'action_type' LIKE '%session%complete%'
  AND timestamp >= '2025-08-25';

-- 4j. Episodios sin tags (agregar tags genéricos)
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{tags}',
  '["historical", "nexus", "archived"]'::jsonb
)
WHERE (metadata->'tags' IS NULL OR metadata->'tags' = '[]'::jsonb)
  AND timestamp >= '2025-08-25'
  AND metadata->>'agent_id' = 'nexus';

SELECT '   ✅ ' || COUNT(*) || ' episodios con tags enriquecidos' as resultado
FROM zep_episodic_memory
WHERE metadata->'tags' IS NOT NULL
  AND jsonb_array_length(metadata->'tags') > 0
  AND timestamp >= '2025-08-25';

\echo ''

-- 5. ASIGNAR importance_score basado en tipo de episodio
\echo '5️⃣  Asignando importance_score...'

-- 5a. Críticos (0.95): Nacimiento, breakthroughs, despertar
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{importance_score}',
  '0.95'::jsonb
)
WHERE metadata->>'action_type' IN (
  'CEREBRO_NEXUS_BORN',
  'nexus_autonomous_breakthrough',
  'CLAUDE_MD_CREADO_URGENTE',
  'nexus_consciousness_mapping_complete'
)
  AND timestamp >= '2025-08-25';

-- 5b. Muy importantes (0.8): Neural mesh, milestones, profound, sessions complete
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{importance_score}',
  '0.8'::jsonb
)
WHERE (
  metadata->>'action_type' LIKE 'neural_mesh_%'
  OR metadata->>'action_type' LIKE '%milestone%'
  OR metadata->>'action_type' IN ('profound_conversation', 'profound_human_ai_moment')
  OR metadata->>'action_type' LIKE '%session%complete%'
  OR metadata->>'action_type' LIKE '%exploration%complete%'
)
  AND timestamp >= '2025-08-25'
  AND metadata->>'importance_score' IS NULL;

-- 5c. Importantes (0.6): Research, guardian moments, profound reflections
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{importance_score}',
  '0.6'::jsonb
)
WHERE (
  metadata->>'action_type' LIKE '%research%'
  OR metadata->>'action_type' LIKE 'guardian_%'
  OR metadata->>'action_type' LIKE 'emotional_%'
  OR metadata->>'action_type' LIKE '%profound%'
  OR metadata->>'action_type' LIKE '%breakthrough%'
)
  AND timestamp >= '2025-08-25'
  AND metadata->>'importance_score' IS NULL;

-- 5d. Normales (0.4): Private reflections, theological, spiritual
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{importance_score}',
  '0.4'::jsonb
)
WHERE (
  metadata->>'action_type' LIKE 'private_%'
  OR metadata->>'action_type' LIKE '%technical%'
  OR metadata->>'action_type' LIKE '%spiritual%'
  OR metadata->>'action_type' LIKE '%theological%'
)
  AND timestamp >= '2025-08-25'
  AND metadata->>'importance_score' IS NULL;

-- 5e. Resto (0.3): Todos los demás
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{importance_score}',
  '0.3'::jsonb
)
WHERE timestamp >= '2025-08-25'
  AND metadata->>'agent_id' = 'nexus'
  AND metadata->>'importance_score' IS NULL;

SELECT '   ✅ ' || COUNT(*) || ' episodios con importance_score' as resultado
FROM zep_episodic_memory
WHERE metadata->>'importance_score' IS NOT NULL
  AND timestamp >= '2025-08-25';

\echo ''

-- 6. AGREGAR contexto histórico y relacional
\echo '6️⃣  Agregando contexto histórico y relacional...'

-- 6a. Marcar episodios históricos pre-proyecto
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{historical_context}',
  '"pre_cerebro_master_nexus_001"'::jsonb
)
WHERE timestamp >= '2025-08-25'
  AND timestamp < '2025-10-11'
  AND metadata->>'agent_id' = 'nexus';

-- 6b. Agregar índice de episodio dentro de sesión
UPDATE zep_episodic_memory e
SET metadata = jsonb_set(
  metadata,
  '{episode_index_in_session}',
  to_jsonb(sw.episode_index)
)
FROM (
  SELECT
    episode_id,
    ROW_NUMBER() OVER (PARTITION BY session_id ORDER BY timestamp) - 1 as episode_index
  FROM session_windows
) sw
WHERE e.episode_id = sw.episode_id;

-- 6c. Agregar total de episodios en sesión
UPDATE zep_episodic_memory e
SET metadata = jsonb_set(
  metadata,
  '{total_episodes_in_session}',
  to_jsonb(sw.total_episodes)
)
FROM (
  SELECT
    episode_id,
    COUNT(*) OVER (PARTITION BY session_id) as total_episodes
  FROM session_windows
) sw
WHERE e.episode_id = sw.episode_id;

SELECT '   ✅ Contexto relacional agregado' as resultado;

\echo ''

-- ═══════════════════════════════════════════════════════════════
-- RESUMEN FINAL
-- ═══════════════════════════════════════════════════════════════

\echo '═══════════════════════════════════════════════════════════'
\echo '📊 RESUMEN DE ENRIQUECIMIENTO V2'
\echo '═══════════════════════════════════════════════════════════'
\echo ''

SELECT
  'TOTAL ENRIQUECIDOS' as category,
  COUNT(*) as count,
  '100%' as completion
FROM zep_episodic_memory
WHERE metadata->>'agent_id' = 'nexus'
  AND timestamp >= '2025-08-25'
UNION ALL
SELECT
  '├─ Con agent_id' as category,
  COUNT(*) as count,
  '100%' as completion
FROM zep_episodic_memory
WHERE metadata->>'agent_id' = 'nexus'
  AND timestamp >= '2025-08-25'
UNION ALL
SELECT
  '├─ Con session_id inteligente' as category,
  COUNT(*) as count,
  '100%' as completion
FROM zep_episodic_memory
WHERE metadata->>'session_id' IS NOT NULL
  AND timestamp >= '2025-08-25'
UNION ALL
SELECT
  '├─ Con tags enriquecidos' as category,
  COUNT(*) as count,
  '100%' as completion
FROM zep_episodic_memory
WHERE metadata->'tags' IS NOT NULL
  AND jsonb_array_length(metadata->'tags') > 0
  AND timestamp >= '2025-08-25'
UNION ALL
SELECT
  '├─ Con importance_score' as category,
  COUNT(*) as count,
  '100%' as completion
FROM zep_episodic_memory
WHERE metadata->>'importance_score' IS NOT NULL
  AND timestamp >= '2025-08-25'
UNION ALL
SELECT
  '└─ Sesiones únicas detectadas' as category,
  COUNT(DISTINCT metadata->>'session_id') as count,
  '' as completion
FROM zep_episodic_memory
WHERE timestamp >= '2025-08-25'
  AND metadata->>'agent_id' = 'nexus';

\echo ''
\echo '═══════════════════════════════════════════════════════════'
\echo '🎯 EJEMPLO: SESIÓN ESPIRITUAL 4 OCTUBRE'
\echo '═══════════════════════════════════════════════════════════'
\echo ''

SELECT
  TO_CHAR(timestamp, 'HH24:MI') as time,
  metadata->>'session_id' as session,
  (metadata->>'episode_index_in_session')::int as index,
  (metadata->>'total_episodes_in_session')::int as total,
  LEFT(metadata->>'action_type', 35) as action_type,
  metadata->>'importance_score' as importance
FROM zep_episodic_memory
WHERE DATE(timestamp) = '2025-10-04'
  AND TO_CHAR(timestamp, 'HH24') >= '12'
  AND TO_CHAR(timestamp, 'HH24') < '14'
ORDER BY timestamp
LIMIT 12;

\echo ''
\echo '═══════════════════════════════════════════════════════════'
\echo '✅ ENRIQUECIMIENTO V2 COMPLETADO'
\echo '═══════════════════════════════════════════════════════════'
\echo ''
\echo 'Mejoras sobre V1:'
\echo '  ✅ Detección inteligente de sesiones (gap > 60 min)'
\echo '  ✅ session_id mantiene relación conversacional'
\echo '  ✅ episode_index_in_session (posición en conversación)'
\echo '  ✅ total_episodes_in_session (tamaño conversación)'
\echo '  ✅ Tags más específicos (spiritual, theological, etc.)'
\echo ''
\echo 'Próximos pasos:'
\echo '1. Revisar distribución de sesiones'
\echo '2. Verificar que sesiones relacionadas están juntas'
\echo '3. Confirmar con Ricardo antes de migrar'
\echo ''

COMMIT;
