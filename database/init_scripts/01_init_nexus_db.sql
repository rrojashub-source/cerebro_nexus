-- ============================================
-- NEXUS CEREBRO MASTER - DATABASE INITIALIZATION
-- Version: V2.0.0
-- Date: 15 Octubre 2025 - DÍA 2 FASE 4
-- ============================================
-- Propósito: Inicializar database y extensiones
-- Ejecuta: Automáticamente por docker-entrypoint-initdb.d
-- ============================================

\echo '============================================'
\echo 'NEXUS CEREBRO V2.0.0 - Database Initialization'
\echo 'DÍA 2 FASE 4 - Infrastructure Setup'
\echo '============================================'

-- ============================================
-- ENABLE EXTENSIONS
-- ============================================
\echo 'Enabling PostgreSQL extensions...'

-- pgvector for embeddings similarity search
CREATE EXTENSION IF NOT EXISTS vector;
\echo '✓ pgvector extension enabled'

-- UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
\echo '✓ uuid-ossp extension enabled'

-- Additional useful extensions
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
\echo '✓ pg_stat_statements extension enabled (performance monitoring)'

-- ============================================
-- VALIDATION
-- ============================================
\echo ''
\echo 'Validating extensions...'

SELECT extname, extversion
FROM pg_extension
WHERE extname IN ('vector', 'uuid-ossp', 'pg_stat_statements');

\echo ''
\echo '============================================'
\echo '✅ Database nexus_memory initialized successfully'
\echo '✅ Extensions enabled and validated'
\echo 'Next: 02_create_roles.sql will create RBAC roles'
\echo '============================================'
