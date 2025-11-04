# 🐋 DOCKER MIGRATION PLAN - V3.0.0

**Fecha:** November 4, 2025 - 12:50 PM
**Objetivo:** Migrar Docker stack desde FASE_4 construcción a V3.0.0 estructura
**Metodología:** NEXUS 4-Phase Workflow

---

## 🔍 DIAGNÓSTICO INICIAL

### Problemas Identificados:

1. **Imagen Docker desactualizada**
   - Imagen actual: `docker_nexus_api:latest` (3h antigüedad)
   - Falta: `ENV PYTHONPATH=/app` (agregado después)
   - Solución: Rebuild forzado

2. **Volumes con paths incorrectos**
   - Actual: `./src:/app/src:ro` (relativo a `config/docker/`)
   - Real: `/mnt/d/.../config/docker/src` (NO EXISTE)
   - Correcto: `../../src:/app/src:ro` (relativo al root del proyecto)
   - Solución: Corregir paths relativos

3. **Procesos en background interfiriendo**
   - Background bash e87e59 (build running)
   - Background bash 53c25a (build running)
   - Solución: Kill all background processes

4. **prometheus.yml path incorrecto**
   - Ya corregido a: `../../config/monitoring/prometheus.yml`

---

## 📋 PLAN DE EJECUCIÓN (8 Pasos)

### **PASO 1: Limpieza**
- Matar procesos background
- Bajar todos los containers
- Limpiar imágenes viejas

### **PASO 2: Corregir docker-compose.yml**
- Cambiar volumes de `./src` a `../../src`
- Cambiar volumes de `./logs` a `../../logs`
- Verificar todos los paths relativos

### **PASO 3: Verificar Dockerfile**
- Confirmar `ENV PYTHONPATH=/app` existe
- Confirmar `COPY src/ ./src/` correcto

### **PASO 4: Build imagen nueva**
- Forzar rebuild: `docker-compose build --no-cache nexus_api`
- Verificar PYTHONPATH en imagen nueva
- Tag imagen como `latest`

### **PASO 5: Build embeddings worker**
- Mismo proceso que API
- Verificar módulos accesibles

### **PASO 6: Levantar servicios base**
- PostgreSQL (puerto 5437)
- Redis (puerto 6385)
- Neo4j (puerto 7474)
- Esperar health checks

### **PASO 7: Levantar servicios aplicación**
- API Master (puerto 8003)
- Embeddings Worker (puerto 9090)
- Prometheus (puerto 9091)
- Grafana (puerto 3001)

### **PASO 8: Verificación completa**
- Health check API: `curl http://localhost:8003/health`
- Contar episodios PostgreSQL
- Verificar logs sin errores
- Confirmar 7/7 containers healthy

---

## ✅ CRITERIOS DE ÉXITO

1. ✅ 7/7 containers corriendo
2. ✅ API responde en puerto 8003
3. ✅ Embeddings worker sin crash loop
4. ✅ PostgreSQL: 467+ episodios intactos
5. ✅ Neo4j: Grafo accesible
6. ✅ Redis: Cache funcionando
7. ✅ Prometheus + Grafana: Métricas visibles

---

## 🚨 ROLLBACK PLAN

**Si algo falla:**
1. Restaurar backup PostgreSQL: `nexus_db_backup_20251104.sql`
2. Restaurar backup Neo4j: `neo4j_data_20251104.tar.gz`
3. Restaurar backup Redis: `redis_data_20251104.tar.gz`

**Backups ubicados en:**
- Local: `/mnt/d/.../backups/`
- Z: drive: `/mnt/z/CEREBRO_V3_BACKUPS/20251104_docker_migration/`

---

## 📊 TIEMPO ESTIMADO

- Paso 1-3: 5 minutos (limpieza + correcciones)
- Paso 4-5: 3 minutos (build con cache)
- Paso 6-7: 2 minutos (servicios inician)
- Paso 8: 2 minutos (verificación)

**Total:** ~12 minutos

---

**Plan creado:** November 4, 2025 - 12:50 PM
**Status:** Ready para ejecución
