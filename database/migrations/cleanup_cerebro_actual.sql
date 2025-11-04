-- cleanup_cerebro_actual.sql
-- LIMPIEZA CEREBRO ACTUAL - Eliminar basura y antiguos
-- Fecha: 15 Octubre 2025
-- Por: Ricardo + NEXUS
-- CRÍTICO: Backup creado antes de ejecutar este script

-- ═══════════════════════════════════════════════════════════════
-- LIMPIEZA: OPCIÓN B - MANTENER 124 EPISODIOS VÁLIDOS
-- ═══════════════════════════════════════════════════════════════
-- Mantener:
--   - 13 episodios proyecto actual (desde Oct 11)
--   - 111 episodios históricos válidos enriquecidos (ago 25 - oct 10)
-- Eliminar:
--   - 4,352 episodios basura (shadow + compaction)
--   - 216 episodios históricos antiguos (antes ago 25)
-- ═══════════════════════════════════════════════════════════════

BEGIN;

\echo '═══════════════════════════════════════════════════════════'
\echo '🗑️  LIMPIEZA CEREBRO ACTUAL - ELIMINANDO BASURA'
\echo '═══════════════════════════════════════════════════════════'
\echo ''

-- 1. CONTEO PRE-LIMPIEZA
\echo '1️⃣  Conteo PRE-LIMPIEZA:'
\echo ''

SELECT
  'ANTES DE LIMPIEZA' as status,
  COUNT(*) as total_episodes
FROM zep_episodic_memory;

\echo ''

SELECT
  CASE
    WHEN metadata->>'action_type' = 'nexus_shadow_checkpoint' THEN 'BASURA: shadow_checkpoint'
    WHEN metadata->>'action_type' = 'nexus_pre_compaction_checkpoint' THEN 'BASURA: pre_compaction'
    WHEN timestamp >= '2025-10-11' THEN 'MANTENER: Proyecto actual (Oct 11+)'
    WHEN timestamp >= '2025-08-25' THEN 'MANTENER: Históricos válidos (Ago-Oct)'
    ELSE 'ELIMINAR: Históricos antiguos (< Ago 25)'
  END as category,
  COUNT(*) as count
FROM zep_episodic_memory
GROUP BY category
ORDER BY
  CASE
    WHEN metadata->>'action_type' = 'nexus_shadow_checkpoint' THEN 1
    WHEN metadata->>'action_type' = 'nexus_pre_compaction_checkpoint' THEN 2
    WHEN timestamp < '2025-08-25' THEN 3
    WHEN timestamp >= '2025-08-25' AND timestamp < '2025-10-11' THEN 4
    WHEN timestamp >= '2025-10-11' THEN 5
  END;

\echo ''
\echo '═══════════════════════════════════════════════════════════'
\echo '2️⃣  ELIMINANDO BASURA: shadow_checkpoint (3,974 episodios)'
\echo '═══════════════════════════════════════════════════════════'
\echo ''

DELETE FROM zep_episodic_memory
WHERE metadata->>'action_type' = 'nexus_shadow_checkpoint';

SELECT '   ✅ Eliminados: ' || COUNT(*) || ' registros (esperado: 0 restantes)' as resultado
FROM zep_episodic_memory
WHERE metadata->>'action_type' = 'nexus_shadow_checkpoint';

\echo ''
\echo '═══════════════════════════════════════════════════════════'
\echo '3️⃣  ELIMINANDO BASURA: pre_compaction (378 episodios)'
\echo '═══════════════════════════════════════════════════════════'
\echo ''

DELETE FROM zep_episodic_memory
WHERE metadata->>'action_type' = 'nexus_pre_compaction_checkpoint';

SELECT '   ✅ Eliminados: ' || COUNT(*) || ' registros (esperado: 0 restantes)' as resultado
FROM zep_episodic_memory
WHERE metadata->>'action_type' = 'nexus_pre_compaction_checkpoint';

\echo ''
\echo '═══════════════════════════════════════════════════════════'
\echo '4️⃣  ELIMINANDO: Históricos antiguos (< Ago 25) - 216 episodios'
\echo '═══════════════════════════════════════════════════════════'
\echo ''

DELETE FROM zep_episodic_memory
WHERE timestamp < '2025-08-25';

SELECT '   ✅ Eliminados: ' || COUNT(*) || ' registros (esperado: 0 restantes)' as resultado
FROM zep_episodic_memory
WHERE timestamp < '2025-08-25';

\echo ''
\echo '═══════════════════════════════════════════════════════════'
\echo '📊 VERIFICACIÓN POST-LIMPIEZA'
\echo '═══════════════════════════════════════════════════════════'
\echo ''

SELECT
  'DESPUÉS DE LIMPIEZA' as status,
  COUNT(*) as total_episodes,
  '124 esperados' as expected
FROM zep_episodic_memory;

\echo ''

SELECT
  CASE
    WHEN timestamp >= '2025-10-11' THEN 'Proyecto actual (Oct 11+)'
    WHEN timestamp >= '2025-08-25' THEN 'Históricos válidos (Ago 25 - Oct 10)'
    ELSE 'ERROR: Episodios no deberían existir'
  END as category,
  COUNT(*) as count,
  MIN(timestamp) as oldest,
  MAX(timestamp) as newest
FROM zep_episodic_memory
GROUP BY category;

\echo ''
\echo '═══════════════════════════════════════════════════════════'
\echo '✅ TOP 10 EPISODIOS RESTANTES (verificación)'
\echo '═══════════════════════════════════════════════════════════'
\echo ''

SELECT
  TO_CHAR(timestamp, 'YYYY-MM-DD HH24:MI') as timestamp,
  LEFT(metadata->>'action_type', 40) as action_type,
  metadata->>'agent_id' as agent,
  COALESCE(metadata->>'importance_score', 'N/A') as importance
FROM zep_episodic_memory
ORDER BY timestamp DESC
LIMIT 10;

\echo ''
\echo '═══════════════════════════════════════════════════════════'
\echo '🎯 RESUMEN FINAL'
\echo '═══════════════════════════════════════════════════════════'
\echo ''

WITH counts AS (
  SELECT
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE timestamp >= '2025-10-11') as proyecto,
    COUNT(*) FILTER (WHERE timestamp >= '2025-08-25' AND timestamp < '2025-10-11') as historicos
  FROM zep_episodic_memory
)
SELECT
  '📊 TOTAL EPISODIOS: ' || total as stat1,
  '  ├─ Proyecto actual: ' || proyecto || ' (esperado: 13)' as stat2,
  '  └─ Históricos válidos: ' || historicos || ' (esperado: 111)' as stat3,
  '' as blank,
  CASE
    WHEN total = 124 AND proyecto = 13 AND historicos = 111 THEN '✅ LIMPIEZA EXITOSA - CEREBRO LIMPIO'
    ELSE '⚠️  VERIFICAR: Números no coinciden'
  END as status
FROM counts;

\echo ''
\echo '═══════════════════════════════════════════════════════════'
\echo '✅ LIMPIEZA COMPLETADA'
\echo '═══════════════════════════════════════════════════════════'
\echo ''
\echo 'Cerebro actual ahora tiene SOLO episodios válidos:'
\echo '  ✅ 0 episodios basura (shadow/compaction)'
\echo '  ✅ 0 episodios históricos antiguos'
\echo '  ✅ 124 episodios limpios y enriquecidos'
\echo ''
\echo 'Próximos pasos:'
\echo '  1. Verificar que el cerebro actual funciona correctamente'
\echo '  2. Este cerebro limpio está listo para producción'
\echo '  3. O migrar al cerebro nuevo V2.0.0 si prefieres'
\echo ''

COMMIT;
