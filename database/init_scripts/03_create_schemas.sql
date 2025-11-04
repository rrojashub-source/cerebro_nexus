-- ============================================
-- NEXUS CEREBRO MASTER - SCHEMAS CREATION
-- Version: V2.0.0
-- Date: 15 Octubre 2025 - DÍA 2 FASE 4
-- ============================================
-- Propósito: Crear schemas organizacionales
-- Arquitectura: 3-layer memory system
-- ============================================

\echo '============================================'
\echo 'NEXUS CEREBRO V2.0.0 - Schemas Creation'
\echo 'DÍA 2 FASE 4 - Database Structure'
\echo '============================================'

-- ============================================
-- SCHEMA 1: nexus_memory (Memory Layers)
-- ============================================
\echo ''
\echo 'Creating schema: nexus_memory (Memory layers - episodic, working, semantic)...'

CREATE SCHEMA IF NOT EXISTS nexus_memory;

-- Grant usage to application roles
GRANT USAGE ON SCHEMA nexus_memory TO nexus_app, nexus_worker, nexus_ro;

\echo '✓ Schema nexus_memory created'

-- ============================================
-- SCHEMA 2: memory_system (System Management)
-- ============================================
\echo ''
\echo 'Creating schema: memory_system (System management - queue, reconciliation)...'

CREATE SCHEMA IF NOT EXISTS memory_system;

-- Grant usage to application roles
GRANT USAGE ON SCHEMA memory_system TO nexus_app, nexus_worker, nexus_ro;

\echo '✓ Schema memory_system created'

-- ============================================
-- SCHEMA 3: consciousness (Consciousness Layer)
-- ============================================
\echo ''
\echo 'Creating schema: consciousness (Consciousness - checkpoints, state)...'

CREATE SCHEMA IF NOT EXISTS consciousness;

-- Grant usage to application roles
GRANT USAGE ON SCHEMA consciousness TO nexus_app, nexus_worker, nexus_ro;

\echo '✓ Schema consciousness created'

-- ============================================
-- VALIDATION
-- ============================================
\echo ''
\echo 'Validating schemas...'

SELECT nspname AS schema_name, nspowner::regrole AS owner
FROM pg_namespace
WHERE nspname IN ('nexus_memory', 'memory_system', 'consciousness')
ORDER BY nspname;

\echo ''
\echo '============================================'
\echo '✅ Schemas created successfully:'
\echo '   - nexus_memory (Episodic, Working, Semantic memory)'
\echo '   - memory_system (Embeddings queue, Reconciliation)'
\echo '   - consciousness (Checkpoints, State, Distributed consensus)'
\echo ''
\echo 'Next: DÍA 3 will create tables within these schemas'
\echo 'RBAC permissions: Usage granted to nexus_app, nexus_worker, nexus_ro'
\echo '============================================'
