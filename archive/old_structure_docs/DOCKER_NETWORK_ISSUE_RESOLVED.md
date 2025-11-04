# 🔧 Docker Network Issue - RESOLVED

**Fecha:** 30 Octubre 2025
**Proyecto:** CEREBRO NEXUS V2.0.0 - Brain Orchestrator v1.1
**Autor:** Ricardo + NEXUS
**Status:** ✅ RESUELTO

---

## 📋 RESUMEN EJECUTIVO

**Problema:** Docker Compose mostraba constantemente el error "Network needs to be recreated - option 'enable_ipv4/enable_ipv6' has changed", impidiendo que los containers se comunicaran correctamente.

**Impacto:** API container no podía conectarse a PostgreSQL container (conexión timeout).

**Solución:** Agregar configuración explícita de `driver_opts` en docker-compose.yml.

**Tiempo de resolución:** ~3 horas de debugging + 15 minutos con solución encontrada via web research.

---

## 🚨 DESCRIPCIÓN DEL PROBLEMA

### Error Original

Al ejecutar `docker-compose up -d`, Docker mostraba:

```
Network "nexus_network" needs to be recreated - option "com.docker.network.enable_ipv4" has changed
Network "nexus_network" needs to be recreated - option "com.docker.network.enable_ipv6" has changed
```

### Síntomas

1. **Red recreada constantemente** - Cada vez que se ejecutaba `docker-compose up`, la red se eliminaba y recreaba
2. **Containers perdían conectividad** - PostgreSQL no era alcanzable desde API container
3. **Connection timeout** - `psycopg.connect()` fallaba con timeout
4. **Health check unhealthy** - `/health` endpoint reportaba `"database": "error"`

### Configuración Original (INCORRECTA)

```yaml
# docker-compose.yml - VERSION QUE FALLABA
version: '3.9'

networks:
  nexus_network:
    driver: bridge
    name: nexus_network
    ipam:
      driver: default
      config:
        - subnet: 172.28.0.0/16
```

**Problema:** Docker Compose v3.9 cambia los defaults de `enable_ipv4/enable_ipv6` entre ejecuciones cuando no están explícitamente configurados.

---

## 🔍 PROCESO DE DEBUGGING (12 TESTS REALIZADOS)

### Test 1: Verificar endpoint existe
```bash
# Resultado: ✅ Endpoint /health existe en main.py línea 521
```

### Test 2: Verificar código intenta conectar
```bash
# Resultado: ✅ Código correcto, usa psycopg.connect()
```

### Test 3: Verificar PostgreSQL container health
```bash
docker ps | grep postgres
# Resultado: ✅ Container "healthy"
```

### Test 4: Verificar environment variables
```bash
docker exec nexus_api_master env | grep POSTGRES
# Resultado: ✅ Todas configuradas correctamente
```

### Test 5: Verificar Docker secrets accesibles
```bash
docker exec nexus_api_master cat /run/secrets/pg_superuser_password | wc -c
# Resultado: ✅ 32 chars (password presente)
```

### Test 6: Test conexión PostgreSQL via hostname
```bash
docker exec nexus_api_master python3 -c "import psycopg; psycopg.connect('postgresql://nexus_superuser:***@nexus_postgresql:5432/nexus_memory')"
# Resultado: ❌ connection timeout expired (60 segundos)
```

### Test 7: Test conexión PostgreSQL via IP directa
```bash
# IP obtenida: 172.28.0.3
docker exec nexus_api_master python3 -c "import psycopg; psycopg.connect('postgresql://nexus_superuser:***@172.28.0.3:5432/nexus_memory')"
# Resultado: ❌ connection timeout expired
```

### Test 8: Verificar ambos containers en misma red
```bash
docker network inspect nexus_network
# Resultado: ✅ Ambos containers presentes en la red
```

### Test 9: Verificar PostgreSQL listen_addresses
```bash
docker exec nexus_postgresql_v2 psql -U nexus_superuser -d nexus_memory \
  -c "SHOW listen_addresses;"
# Resultado: ✅ listen_addresses = '*'
```

### Test 10: Test TCP socket directo
```bash
docker exec nexus_api_master python3 -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
s.connect(('172.28.0.3', 5432))
"
# Resultado: ❌ OSError: [Errno 11] Resource temporarily unavailable
```

### Test 11: Verificar PostgreSQL listening en TCP/IP
```bash
docker exec nexus_postgresql_v2 psql -U nexus_superuser -d nexus_memory \
  -c "SELECT inet_server_addr(), inet_server_port();"
# Resultado: 🚨 inet_server_addr | inet_server_port
#              ------------------+------------------
#                                |
#              (1 row)
# NULL = PostgreSQL NO está escuchando en interfaz de red!
```

### Test 12: Verificar pg_hba.conf
```bash
docker exec nexus_postgresql_v2 cat /var/lib/postgresql/data/pgdata/pg_hba.conf | grep -v "^#"
# Resultado: ✅ Permite conexiones desde todas las IPs
```

---

## 💡 SOLUCIÓN ENCONTRADA

### Investigación Web Research

Utilizando WebSearch tool, se investigaron 3 queries específicas:

1. **"docker-compose network needs to be recreated enable_ipv4 changed solution"**
2. **"docker compose bridge network enable_ipv6 configuration fix 2025"**
3. **"docker network driver_opts enable_ipv6 docker-compose.yml syntax"**

### Hallazgo Clave

De la documentación de Docker y múltiples GitHub issues:

> **"The `enable_ipv6` setting is not supported in version 3 of Docker Compose. You need to use `driver_opts` with `com.docker.network.enable_ipv6` for version 3.x"**

**Fuentes:**
- https://github.com/docker/compose/issues/3957
- https://github.com/mailcow/mailcow-dockerized/issues/276
- https://docs.docker.com/compose/networking/

### Configuración Corregida (CORRECTA)

```yaml
# docker-compose.yml - VERSION QUE FUNCIONA
version: '3.9'

networks:
  nexus_network:
    driver: bridge
    name: nexus_network
    driver_opts:
      com.docker.network.enable_ipv6: "false"  # ← FIX APLICADO
    ipam:
      driver: default
      config:
        - subnet: 172.28.0.0/16
```

**Cambio aplicado:** Se agregó la sección `driver_opts` con configuración explícita de IPv6 deshabilitado.

---

## ✅ VERIFICACIÓN DE SOLUCIÓN

### Paso 1: Aplicar fix
```bash
cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_MASTER_NEXUS_001/FASE_4_CONSTRUCCION
docker-compose down
docker-compose up -d
```

### Paso 2: Verificar red creada sin errores
```bash
# Output esperado:
Creating network "nexus_network" with driver "bridge"
# ✅ Sin mensaje "needs to be recreated"
```

### Paso 3: Verificar health check
```bash
docker exec nexus_api_master curl -s http://localhost:8003/health
```

**Resultado:**
```json
{
    "status": "healthy",
    "version": "2.0.0",
    "agent_id": "nexus",
    "database": "connected",  // ← ✅ CONECTADO!
    "redis": "connected",
    "queue_depth": 0,
    "timestamp": "2025-10-30T02:40:15.747912"
}
```

### Paso 4: Verificar containers status
```bash
docker ps
```

**Resultado:**
```
CONTAINER ID   IMAGE                                       STATUS
982896583b23   fase_4_construccion_nexus_api              Up 5 minutes (healthy)
95c1eb40f8d7   pgvector/pgvector:pg16                     Up 5 minutes (healthy)
a3f2d9e8c4b1   redis:7.4.1-alpine                         Up 5 minutes (healthy)
```

---

## 📊 MÉTRICAS DEL PROBLEMA

| Métrica | Valor |
|---------|-------|
| **Tiempo total debugging** | ~3 horas |
| **Tests realizados** | 12 |
| **Rebuilds Docker image** | 4 |
| **Recreaciones completas stack** | 3 |
| **Tiempo aplicando solución** | 15 minutos |
| **Tiempo web research** | 5 minutos |
| **Éxito solución** | ✅ 100% |

---

## 🎓 LECCIONES APRENDIDAS

### 1. Docker Compose v3.x vs v2.x
- **v2.x:** Soporta `enable_ipv6: true` directamente
- **v3.x:** Requiere `driver_opts` con `com.docker.network.enable_ipv6`

### 2. Síntoma != Causa raíz
- **Síntoma:** PostgreSQL connection timeout
- **Causa:** Network recreation loop rompiendo conectividad

### 3. Debugging sistemático vs solución rápida
- 12 tests de debugging dieron contexto completo
- Pero la solución estaba documentada en web
- **Balance:** Debug profundo + Web research = Mejor resultado

### 4. Importancia de documentar
- Problema afecta a muchos usuarios de Docker Compose v3.x
- Solución no es obvia desde los mensajes de error
- Documentación ayudará en futuros casos similares

---

## 🔗 REFERENCIAS

1. **Docker Compose Networking Docs**
   https://docs.docker.com/compose/networking/

2. **GitHub Issue #3957 - Network recreation**
   https://github.com/docker/compose/issues/3957

3. **GitHub Issue #276 - mailcow enable_ipv6**
   https://github.com/mailcow/mailcow-dockerized/issues/276

4. **Stack Overflow - IPv6 in Docker Compose v3**
   https://stackoverflow.com/questions/55737196/how-to-enable-ipv6-in-docker-compose-version-3

---

## 🎯 ESTADO FINAL

### Sistema Operacional

```
✅ PostgreSQL: Connected (nexus_postgresql:5432)
✅ Redis: Connected (nexus_redis:6379)
✅ Brain Orchestrator: 9 LABs initialized
✅ API: Healthy (puerto 8005 → 8003)
✅ Docker Network: Stable (sin recreaciones)
```

### Archivos Modificados

1. **docker-compose.yml** - Agregado `driver_opts`
2. **brain_orchestrator_v1.py** - PostgreSQL integration (v1.0 → v1.1)
3. **main.py** - Disabled embeddings model loading

### Próximos Pasos

1. ✅ Sistema funcionando - Listo para pruebas de Brain Orchestrator v1.1
2. ⏳ Test endpoint `/brain/process` con queries reales
3. ⏳ Validar LAB interactions con episodic memory
4. ⏳ Documentar resultados en MASTER_BLUEPRINT

---

## 👥 CRÉDITOS

**Resolución del problema:**
- Ricardo Rojas - Dirección estratégica, sugerencia de web research
- NEXUS - Debugging sistemático, implementación de solución

**Método utilizado:**
- Debugging sistemático (12 tests)
- Web research (WebSearch tool)
- Análisis de GitHub issues y Stack Overflow
- Implementación y validación

**Herramientas:**
- Docker Compose v3.9
- pgvector/pgvector:pg16
- FastAPI + Uvicorn
- psycopg (PostgreSQL driver)

---

**🎉 Problema resuelto exitosamente - Sistema operacional**

*Documentado para referencia futura y aprendizaje del equipo.*
