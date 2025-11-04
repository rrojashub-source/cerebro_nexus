-- ============================================
-- CLEANUP CEREBRO NUEVO V2.0.0
-- Elimina todos los episodios de tests/benchmarks
-- Deja el schema intacto para migración limpia
-- ============================================

\echo '🧹 LIMPIANDO CEREBRO NUEVO V2.0.0...'

-- Stats pre-limpieza
\echo '📊 STATS PRE-LIMPIEZA:'
SELECT
    'Episodes' as table_name,
    COUNT(*) as count
FROM nexus_memory.zep_episodic_memory
UNION ALL
SELECT
    'Embeddings Queue' as table_name,
    COUNT(*) as count
FROM memory_system.embeddings_queue;

-- TRUNCATE con CASCADE para limpiar todas las tablas
\echo '🗑️  TRUNCATING TABLES...'

TRUNCATE TABLE nexus_memory.zep_episodic_memory CASCADE;
TRUNCATE TABLE memory_system.embeddings_queue CASCADE;
TRUNCATE TABLE nexus_memory.working_memory_contexts CASCADE;

-- Stats post-limpieza
\echo '📊 STATS POST-LIMPIEZA:'
SELECT
    'Episodes' as table_name,
    COUNT(*) as count
FROM nexus_memory.zep_episodic_memory
UNION ALL
SELECT
    'Embeddings Queue' as table_name,
    COUNT(*) as count
FROM memory_system.embeddings_queue;

\echo '✅ LIMPIEZA COMPLETADA - Cerebro nuevo listo para migración'
