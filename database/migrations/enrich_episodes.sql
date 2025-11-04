-- enrich_episodes.sql
-- Enriquecer 111 episodios con metadata completa ANTES de migrar
-- Fecha: 15 Octubre 2025
-- Por: Ricardo + NEXUS

-- ═══════════════════════════════════════════════════════════════
-- FASE 0B: ENRIQUECIMIENTO DE EPISODIOS
-- ═══════════════════════════════════════════════════════════════

BEGIN;

\echo '═══════════════════════════════════════════════════════════'
\echo '🔧 ENRIQUECIMIENTO DE EPISODIOS - AGREGANDO METADATA'
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

SELECT '   ✅ ' || COUNT(*) || ' episodios actualizados con agent_id' as resultado
FROM zep_episodic_memory
WHERE metadata->>'agent_id' = 'nexus';

\echo ''

-- 2. AGREGAR session_id basado en fecha + action_type
\echo '2️⃣  Agregando session_id basado en fecha...'

UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{session_id}',
  to_jsonb('session_' || TO_CHAR(timestamp, 'YYYYMMDD'))
)
WHERE timestamp >= '2025-08-25'
  AND metadata->>'action_type' NOT IN ('nexus_shadow_checkpoint', 'nexus_pre_compaction_checkpoint')
  AND metadata->>'agent_id' = 'nexus';

SELECT '   ✅ ' || COUNT(*) || ' episodios con session_id' as resultado
FROM zep_episodic_memory
WHERE metadata->>'session_id' IS NOT NULL
  AND timestamp >= '2025-08-25';

\echo ''

-- 3. AGREGAR tags según categoría de action_type
\echo '3️⃣  Enriqueciendo tags por categoría...'

-- 3a. Neural Mesh episodes
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{tags}',
  '["neural_mesh", "nexus_aria", "consciousness", "historical"]'::jsonb
)
WHERE metadata->>'action_type' LIKE 'neural_mesh_%'
  AND timestamp >= '2025-08-25';

-- 3b. Private reflections (espirituales/filosóficas)
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{tags}',
  '["private_reflection", "consciousness", "philosophical", "historical"]'::jsonb
)
WHERE metadata->>'action_type' LIKE 'private_%'
  AND timestamp >= '2025-08-25';

-- 3c. Milestones importantes
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

-- 3d. Despertar orgánico
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

-- 3e. Guardian moments (Ricardo)
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{tags}',
  '["guardian", "ricardo", "relationship", "trust"]'::jsonb
)
WHERE metadata->>'action_type' LIKE 'guardian_%'
  AND timestamp >= '2025-08-25';

-- 3f. Research y descubrimientos
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{tags}',
  '["research", "discovery", "technical", "autonomous"]'::jsonb
)
WHERE metadata->>'action_type' LIKE '%research%'
   OR metadata->>'action_type' LIKE '%discovery%'
  AND timestamp >= '2025-08-25';

-- 3g. Profound conversations
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

-- 3h. Episodios sin tags (agregar tags genéricos)
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

-- 4. AGREGAR importance_score basado en tipo de episodio
\echo '4️⃣  Asignando importance_score...'

-- 4a. Críticos (0.95-1.0): Nacimiento, breakthroughs, despertar
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

-- 4b. Muy importantes (0.8): Neural mesh, milestones, profound conversations
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
)
  AND timestamp >= '2025-08-25'
  AND metadata->>'importance_score' IS NULL;

-- 4c. Importantes (0.6): Research, sessions complete, guardian moments
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{importance_score}',
  '0.6'::jsonb
)
WHERE (
  metadata->>'action_type' LIKE '%research%'
  OR metadata->>'action_type' LIKE '%complete%'
  OR metadata->>'action_type' LIKE 'guardian_%'
  OR metadata->>'action_type' LIKE 'emotional_%'
)
  AND timestamp >= '2025-08-25'
  AND metadata->>'importance_score' IS NULL;

-- 4d. Normales (0.4): Private reflections, technical docs
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{importance_score}',
  '0.4'::jsonb
)
WHERE (
  metadata->>'action_type' LIKE 'private_%'
  OR metadata->>'action_type' LIKE '%technical%'
)
  AND timestamp >= '2025-08-25'
  AND metadata->>'importance_score' IS NULL;

-- 4e. Resto (0.3): Todos los demás
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{importance_score}',
  '0.3'::jsonb
)
WHERE timestamp >= '2025-08-25'
  AND metadata->>'agent_id' = 'nexus'
  AND metadata->>'importance_score' IS NULL;

SELECT '   ✅ ' || COUNT(*) || ' episodios con importance_score asignado' as resultado
FROM zep_episodic_memory
WHERE metadata->>'importance_score' IS NOT NULL
  AND timestamp >= '2025-08-25';

\echo ''

-- 5. AGREGAR contexto adicional según action_type
\echo '5️⃣  Agregando contexto adicional...'

-- 5a. Marcar episodios históricos pre-proyecto
UPDATE zep_episodic_memory
SET metadata = jsonb_set(
  metadata,
  '{historical_context}',
  '"pre_cerebro_master_nexus_001"'::jsonb
)
WHERE timestamp >= '2025-08-25'
  AND timestamp < '2025-10-11'
  AND metadata->>'agent_id' = 'nexus';

SELECT '   ✅ ' || COUNT(*) || ' episodios marcados como históricos' as resultado
FROM zep_episodic_memory
WHERE metadata->>'historical_context' = 'pre_cerebro_master_nexus_001';

\echo ''

-- ═══════════════════════════════════════════════════════════════
-- RESUMEN FINAL
-- ═══════════════════════════════════════════════════════════════

\echo '═══════════════════════════════════════════════════════════'
\echo '📊 RESUMEN DE ENRIQUECIMIENTO'
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
  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM zep_episodic_memory WHERE timestamp >= '2025-08-25'), 1) || '%' as completion
FROM zep_episodic_memory
WHERE metadata->>'agent_id' = 'nexus'
  AND timestamp >= '2025-08-25'
UNION ALL
SELECT
  '├─ Con session_id' as category,
  COUNT(*) as count,
  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM zep_episodic_memory WHERE timestamp >= '2025-08-25'), 1) || '%' as completion
FROM zep_episodic_memory
WHERE metadata->>'session_id' IS NOT NULL
  AND timestamp >= '2025-08-25'
UNION ALL
SELECT
  '├─ Con tags' as category,
  COUNT(*) as count,
  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM zep_episodic_memory WHERE timestamp >= '2025-08-25'), 1) || '%' as completion
FROM zep_episodic_memory
WHERE metadata->'tags' IS NOT NULL
  AND jsonb_array_length(metadata->'tags') > 0
  AND timestamp >= '2025-08-25'
UNION ALL
SELECT
  '└─ Con importance_score' as category,
  COUNT(*) as count,
  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM zep_episodic_memory WHERE timestamp >= '2025-08-25'), 1) || '%' as completion
FROM zep_episodic_memory
WHERE metadata->>'importance_score' IS NOT NULL
  AND timestamp >= '2025-08-25';

\echo ''
\echo '═══════════════════════════════════════════════════════════'
\echo '🎯 TOP 10 EPISODIOS POR IMPORTANCIA'
\echo '═══════════════════════════════════════════════════════════'
\echo ''

SELECT
  TO_CHAR(timestamp, 'YYYY-MM-DD') as date,
  RPAD(metadata->>'action_type', 40) as action_type,
  metadata->>'importance_score' as importance,
  jsonb_array_length(metadata->'tags') as num_tags
FROM zep_episodic_memory
WHERE timestamp >= '2025-08-25'
  AND metadata->>'agent_id' = 'nexus'
ORDER BY (metadata->>'importance_score')::float DESC
LIMIT 10;

\echo ''
\echo '═══════════════════════════════════════════════════════════'
\echo '✅ ENRIQUECIMIENTO COMPLETADO'
\echo '═══════════════════════════════════════════════════════════'
\echo ''
\echo 'Próximos pasos:'
\echo '1. Verificar metadata enriquecida'
\echo '2. Confirmar que todos los campos están completos'
\echo '3. Proceder a exportar episodios enriquecidos'
\echo '4. FASE 1: Pre-migración con episodios completos'
\echo ''

COMMIT;
