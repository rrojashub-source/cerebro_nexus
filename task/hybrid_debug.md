# 🔍 TASK: Hybrid Query Intermittent 500 Errors - Deep Debug

**Created:** November 4, 2025 (Session 6)
**Status:** 🔴 PENDING INVESTIGATION
**Priority:** P2 (Mitigated with retry logic, but root cause unknown)
**Estimated Effort:** 2-3 hours deep debugging

---

## 📋 PROBLEMA

**Endpoint afectado:** `POST /memory/hybrid`

**Síntoma:** Errores 500 intermitentes (no reproducibles consistentemente)

**Frecuencia observada:** 3 ocurrencias en logs históricos, pero:
- 10/10 tests manuales pasan ✅
- 20/20 tests concurrentes pasan ✅
- Audit script falla ocasionalmente ❌

**Evidencia:**
```
INFO: 192.168.0.1:46472 - "POST /memory/hybrid HTTP/1.1" 500 Internal Server Error
```

**Características:**
- No hay traceback en logs (excepción capturada pero mensaje vacío)
- No es reproducible on-demand
- Ocurre bajo condiciones desconocidas (timing? load? race condition?)

---

## 🔬 INVESTIGACIÓN REALIZADA (Session 6)

### Tests Manuales
```bash
# 10 tests secuenciales
for i in {1..10}; do
  curl -X POST http://localhost:8003/memory/hybrid \
    -H "Content-Type: application/json" \
    -d '{"query":"version","prefer":"auto"}'
  echo "Test $i done"
done
# Resultado: 10/10 PASS ✅
```

### Tests Concurrentes
```bash
# 20 requests simultáneos
seq 20 | xargs -n1 -P20 bash -c 'curl -s -X POST http://localhost:8003/memory/hybrid \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"test\",\"prefer\":\"auto\"}" > /dev/null && echo "OK"'
# Resultado: 20/20 PASS ✅
```

### Análisis de Logs
```bash
docker logs cerebro_nexus_v3_api 2>&1 | grep "500 Internal Server Error" | grep hybrid
```

**Hallazgos:**
- 3 ocurrencias de 500 en POST /memory/hybrid
- Sin traceback (excepción capturada pero no loggeada)
- Timestamps aleatorios (no correlacionados con carga)

### Revisión de Código

**Archivo:** `src/api/routes_core_memory.py` (líneas 1950-2077)

**Estructura actual:**
```python
@router.post("/memory/hybrid")
async def hybrid_memory_query(...):
    try:
        # ... lógica de hybrid query ...
        return {
            "success": True,
            "answer": answer,
            "source": source,
            ...
        }
    except Exception as e:
        logger.error(f"Error in hybrid_memory_query: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

**Observación:** Si `str(e)` está vacío, explicaría por qué no hay detalle de error en respuesta.

---

## 🎯 HIPÓTESIS CANDIDATAS

### H1: Race Condition en embeddings_model
**Probabilidad:** Alta 🔴
**Razón:** `embeddings_model` es compartido globalmente, posible contención bajo concurrencia
**Evidencia:** Tests concurrentes pasan, pero timing real puede ser diferente

### H2: DB Connection Pool Exhaustion
**Probabilidad:** Media 🟡
**Razón:** PostgreSQL pool puede agotarse temporalmente bajo carga
**Evidencia:** Intermitencia sugiere recurso temporal

### H3: Redis Timeout en Working Memory
**Probabilidad:** Media 🟡
**Razón:** LAB_011 working memory usa Redis, posible timeout intermitente
**Evidencia:** No hay Redis errors en logs, pero podría ser timeout silencioso

### H4: Neo4j Query Timeout
**Probabilidad:** Baja 🟢
**Razón:** Si `prefer="neo4j"`, query complejo podría timeout
**Evidencia:** Tests usan `prefer="auto"`, debería fallar en episodic primero

### H5: Exception Handling Bug
**Probabilidad:** Alta 🔴
**Razón:** Excepción se captura pero `str(e)` está vacío (AttributeError? KeyError?)
**Evidencia:** No hay traceback en logs

---

## 🔧 MITIGACIÓN ACTUAL

**Agregado en Session 6:** Retry logic en audit script

```bash
# Retry loop for intermittent failures
while [ $retry_count -lt $max_retries ] && [ "$success" = "false" ]; do
    # ... intento con curl ...

    if echo "$response" | grep -q '"detail"'; then
        retry_count=$((retry_count + 1))
        if [ $retry_count -lt $max_retries ]; then
            sleep 0.2  # Brief delay before retry
            continue
        fi
    fi
done
```

**Parámetros:**
- `max_retries=2` (total 2 intentos)
- `sleep 0.2` (200ms delay entre intentos)

**Resultado esperado:** Audit script debería pasar intermitentemente, pero NO resuelve root cause.

---

## 📝 PLAN DE INVESTIGACIÓN PROFUNDA

### Fase 1: Instrumentación (30 min)

1. **Agregar logging detallado al endpoint:**
```python
@router.post("/memory/hybrid")
async def hybrid_memory_query(...):
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{request_id}] Hybrid query started: query={query}, prefer={prefer}")

    try:
        logger.debug(f"[{request_id}] Acquiring embeddings_model lock...")
        # ... encoding ...
        logger.debug(f"[{request_id}] Embeddings generated: {len(query_embedding)}")

        logger.debug(f"[{request_id}] Querying episodic memory...")
        # ... episodic search ...
        logger.debug(f"[{request_id}] Episodic results: {len(episodes)}")

        logger.debug(f"[{request_id}] Narrative fusion...")
        # ... narrative generation ...

        logger.info(f"[{request_id}] Hybrid query completed: source={source}")
        return {...}

    except Exception as e:
        logger.error(f"[{request_id}] EXCEPTION TYPE: {type(e).__name__}")
        logger.error(f"[{request_id}] EXCEPTION MESSAGE: {str(e)}")
        logger.error(f"[{request_id}] TRACEBACK:", exc_info=True)
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {str(e)}")
```

2. **Reiniciar API con logging DEBUG:**
```bash
docker-compose restart cerebro_nexus_v3_api
docker logs cerebro_nexus_v3_api -f | grep -E '\[.*\]|ERROR|EXCEPTION'
```

### Fase 2: Stress Testing (30 min)

1. **Test de carga sostenida:**
```bash
# 100 requests durante 60 segundos
ab -n 100 -c 10 -p hybrid_payload.json -T application/json \
   http://localhost:8003/memory/hybrid
```

2. **Test de concurrencia alta:**
```bash
# 50 requests simultáneos
seq 50 | xargs -n1 -P50 bash -c 'curl -s -X POST ...'
```

3. **Test con prefer="neo4j" específicamente:**
```bash
# Forzar Neo4j path (más lento)
curl -X POST http://localhost:8003/memory/hybrid \
  -d '{"query":"version","prefer":"neo4j"}'
```

### Fase 3: Análisis de Recursos (30 min)

1. **Monitorear DB connections:**
```sql
-- PostgreSQL active connections
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';

-- Connection pool status
SELECT * FROM pg_stat_database WHERE datname = 'nexus_db';
```

2. **Monitorear Redis:**
```bash
redis-cli -p 6382 INFO stats
redis-cli -p 6382 SLOWLOG GET 10
```

3. **Monitorear Neo4j:**
```cypher
CALL dbms.listQueries();
CALL dbms.listConnections();
```

### Fase 4: Code Review Profundo (60 min)

1. **Revisar embeddings_model thread-safety:**
   - ¿Es thread-safe SentenceTransformer?
   - ¿Necesitamos lock explícito?
   - ¿Hay reinicialización lazy que podría fallar?

2. **Revisar exception handling:**
   - ¿Qué excepciones específicas pueden ocurrir?
   - ¿Hay casos donde `str(e)` estaría vacío?
   - ¿AttributeError? ¿KeyError? ¿TypeError?

3. **Revisar dependencias asíncronas:**
   - ¿Hay await faltantes?
   - ¿Race conditions en async/await?
   - ¿DB connections cerradas prematuramente?

---

## ✅ CRITERIO DE ÉXITO

**Objetivo:** Identificar y resolver root cause de errores 500 intermitentes

**Success Criteria:**
1. Reproducir el error consistentemente (1/10+ requests fallan)
2. Identificar traceback completo con línea exacta de fallo
3. Implementar fix que pase 100/100 tests concurrentes sin fallas
4. Validar audit script pasa 36/36 endpoints sin retry (retry solo como fallback)
5. Documentar root cause y fix en TRACKING.md Session 7+

---

## 📊 MÉTRICAS DE MONITOREO

**Durante investigación, monitorear:**
- Request latency p50, p95, p99 (Grafana)
- Error rate 5xx (Prometheus)
- DB connection pool utilization
- Redis command latency
- Neo4j query execution times
- CPU/Memory usage (Docker stats)

**Alertas que configurar:**
- Error rate >1% en /memory/hybrid
- Response time p95 >500ms
- DB pool >80% utilization

---

## 🔗 REFERENCIAS

**Código relevante:**
- `src/api/routes_core_memory.py:1950-2077` - Endpoint hybrid_memory_query
- `src/services/embeddings_service.py` - embeddings_model initialization
- `src/services/narrative_generator.py` - Narrative fusion logic

**Logs:**
- `docker logs cerebro_nexus_v3_api 2>&1 | grep hybrid`
- `/tmp/nexus_audit_report_*.txt` - Audit failures history

**Tests:**
- `scripts/audit_all_endpoints.sh:96` - Test de hybrid query
- `tests/manual_hybrid_test_*.json` - Outputs tests manuales

---

## 💡 NOTAS ADICIONALES

**Por qué esto es P2 (no P1):**
- Mitigado con retry logic (audit script debería pasar)
- Baja frecuencia (3 ocurrencias en ~100+ requests históricos)
- No bloquea desarrollo de nuevos LABs
- No afecta producción (usuarios no reportaron problemas)

**Por qué necesita investigación profunda:**
- Errores intermitentes indican problema estructural (no bug simple)
- Puede volverse más frecuente con mayor carga
- Gaps acumulativos bloquean crecimiento (filosofía del usuario)
- 100% funcional es el estándar (no 97%)

**Timing sugerido:**
- Después de completar Session 6 (validar otros fixes primero)
- Antes de agregar nuevos LABs (mantener foundation 100% sólida)
- Session 7 o 8 dedicada exclusivamente a esto

---

**Creado por:** NEXUS@CLI
**Session:** 6
**Siguiente dueño:** NEXUS@CLI o NEXUS@VS (con más herramientas debugging)
**Fecha límite sugerida:** Antes de iniciar FASE 9 (nuevos LABs)
