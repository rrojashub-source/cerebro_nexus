-- ============================================
-- NEXUS CEREBRO MASTER - RBAC ROLES
-- Version: V2.0.0
-- Date: 15 Octubre 2025 - DÍA 2 FASE 4
-- ============================================
-- Propósito: Crear 4 roles PostgreSQL con RBAC
-- Security: Least privilege principle
-- ============================================

\echo '============================================'
\echo 'NEXUS CEREBRO V2.0.0 - RBAC Roles Creation'
\echo 'DÍA 2 FASE 4 - Security Hardening'
\echo '============================================'

-- ============================================
-- ROLE 1: nexus_app (Application - Read/Write)
-- ============================================
\echo ''
\echo 'Creating nexus_app role (Application Read/Write)...'

DO $$
DECLARE
  app_password TEXT;
BEGIN
  -- Read password from Docker Secret
  app_password := trim(pg_read_file('/run/secrets/pg_app_password'));

  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'nexus_app') THEN
    EXECUTE format('CREATE ROLE nexus_app WITH LOGIN PASSWORD %L', app_password);
    RAISE NOTICE 'Role nexus_app created';
  ELSE
    RAISE NOTICE 'Role nexus_app already exists';
  END IF;
END
$$;

-- Grant database connection
GRANT CONNECT ON DATABASE nexus_memory TO nexus_app;

\echo '✓ nexus_app role created (Read/Write access)'

-- ============================================
-- ROLE 2: nexus_worker (Worker - Write embeddings)
-- ============================================
\echo ''
\echo 'Creating nexus_worker role (Embeddings Worker)...'

DO $$
DECLARE
  worker_password TEXT;
BEGIN
  -- Read password from Docker Secret
  worker_password := trim(pg_read_file('/run/secrets/pg_worker_password'));

  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'nexus_worker') THEN
    EXECUTE format('CREATE ROLE nexus_worker WITH LOGIN PASSWORD %L', worker_password);
    RAISE NOTICE 'Role nexus_worker created';
  ELSE
    RAISE NOTICE 'Role nexus_worker already exists';
  END IF;
END
$$;

-- Grant database connection
GRANT CONNECT ON DATABASE nexus_memory TO nexus_worker;

\echo '✓ nexus_worker role created (Embeddings write access)'

-- ============================================
-- ROLE 3: nexus_ro (Read-Only - Reconciliation)
-- ============================================
\echo ''
\echo 'Creating nexus_ro role (Read-Only)...'

DO $$
DECLARE
  ro_password TEXT;
BEGIN
  -- Read password from Docker Secret
  ro_password := trim(pg_read_file('/run/secrets/pg_readonly_password'));

  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'nexus_ro') THEN
    EXECUTE format('CREATE ROLE nexus_ro WITH LOGIN PASSWORD %L', ro_password);
    RAISE NOTICE 'Role nexus_ro created';
  ELSE
    RAISE NOTICE 'Role nexus_ro already exists';
  END IF;
END
$$;

-- Grant database connection
GRANT CONNECT ON DATABASE nexus_memory TO nexus_ro;

\echo '✓ nexus_ro role created (Read-Only access)'

-- ============================================
-- VALIDATION
-- ============================================
\echo ''
\echo 'Validating RBAC roles...'

SELECT rolname, rolcanlogin, rolsuper
FROM pg_roles
WHERE rolname IN ('nexus_superuser', 'nexus_app', 'nexus_worker', 'nexus_ro')
ORDER BY rolname;

\echo ''
\echo '============================================'
\echo '✅ RBAC Roles created successfully:'
\echo '   - nexus_superuser (Owner - inherited from POSTGRES_USER)'
\echo '   - nexus_app (Read/Write application access)'
\echo '   - nexus_worker (Write embeddings queue)'
\echo '   - nexus_ro (Read-Only for reconciliation)'
\echo ''
\echo 'Next: 03_create_schemas.sql will create database schemas'
\echo 'Permissions will be granted after table creation'
\echo '============================================'
