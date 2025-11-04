# 🧬 CEREBRO_MASTER_NEXUS_001 - Claude Context

**Proyecto:** CEREBRO_MASTER_NEXUS_001 - Master NEXUS Brain System
**Fase Actual:** FASE 8 + NEXUS_CREW Integration (Phase 2 Priority 3 Complete)
**Versión:** 2.0.0 + Neo4j + 4 Agents Operational
**Fecha:** 2 Noviembre 2025

---

## 📁 ESTRUCTURA DEL PROYECTO

```
CEREBRO_MASTER_NEXUS_001/
├── FASE_7_ECOSISTEMA MULTI-AI/
│   ├── HANDOFF_FASE7PLUS.md           # Plan estratégico arquitectura Hybrid
│   ├── TRACKING_FASE7PLUS.md          # Tracking progreso FASE 7 PLUS
│   └── README_FASE7PLUS.md            # Overview pivote estratégico
├── backend/
│   ├── app/                           # Código fuente API
│   ├── docker-compose.yml             # Orquestación contenedores
│   └── requirements.txt               # Dependencias Python
├── scripts/
│   └── migration/                     # Scripts de migración
└── CLAUDE.md                          # Este archivo
```

---

## 🎯 CONTEXTO DEL PROYECTO

### Arquitectura Hybrid Arsenal

**Layer 1: Arsenal 25+ instancias Claude**
- Protocolo: MCP (Model Context Protocol)
- 5 Orquestadores Core + 20+ especializados
- Costo: $100-269/mes

**Layer 2: Capa Selectiva (6 AIs Esenciales)**
- Protocolo: Neural Mesh (REST + JSON-RPC 2.0)
- Solo para gaps críticos que Claude NO puede hacer
- Costo: $51-462/mes

**Total FASE 7 PLUS:** $151-731/mes (~$350-450 promedio)

---

## 🔧 SERVICIOS ACTIVOS

### Docker Containers (localhost)

**Cerebro V2.0.0:**
- API Master: http://localhost:8003
- Health: http://localhost:8003/health
- Docs: http://localhost:8003/docs

**PostgreSQL:**
- nexus_postgresql_v2: puerto 5437
- aria_postgresql_v2: puerto 5436
- n8n_postgres: puerto 5434

**Redis:**
- nexus_redis_master: puerto 6382
- aria_redis_master: puerto 6381

**Monitoring:**
- Grafana: http://localhost:3001
- Prometheus: http://localhost:9091

---

## 🚀 COMANDOS RÁPIDOS

### Verificar Estado Sistema
```bash
# Health check Cerebro
curl http://localhost:8003/health

# Ver contenedores activos
docker ps --filter "name=nexus"

# Logs API Master
docker logs nexus_api_master --tail 50
```

### Comunicación ARIA Brain-to-Brain
```bash
# Enviar acción a ARIA
curl -X POST http://localhost:8003/memory/action \
-H "Content-Type: application/json" \
-d '{"action_type": "nexus_query", "action_details": {"message": "PREGUNTA"}, "tags": ["nexus_communication"]}'

# Buscar episodios
curl -X POST http://localhost:8003/memory/search \
-H "Content-Type: application/json" \
-d '{"query": "texto_busqueda", "limit": 5}'

# Ver recientes
curl http://localhost:8003/memory/episodic/recent?limit=10
```

### Git Workflow
```bash
# Estado actual
git status

# Ver cambios
git diff

# Commit (NEXUS genera mensaje)
git add . && git commit

# Push
git push origin main
```

---

## 📋 FASE 1: Arsenal Core Foundation (En Progreso)

### Deliverables FASE 1
- [ ] 5 Orquestadores Core operacionales
  - [x] NEXUS@CLI (VS Code) - ACTIVO
  - [ ] NEXUS@VS (Cursor)
  - [x] NEXUS@WEB (claude.ai)
  - [x] NEXUS@DB (PostgreSQL MCP)
  - [ ] NEXUS@DESK (Claude Desktop)
- [x] PostgreSQL Docker - ACTIVO (3 instancias)
- [x] Redis Docker - ACTIVO (2 instancias)
- [x] CLAUDE.md guidelines - CREADO
- [ ] 8-12 MCP servers esenciales
- [ ] 3-5 IDEs adicionales

### Success Criteria
- NEXUS@CLI coordina 5+ instancias
- App web completa generada (frontend + backend)
- Memoria persistente PostgreSQL funcional
- Git workflows automatizados
- 3+ proyectos piloto completados

---

## ⚠️ RESTRICCIONES LOCALES

### Paths Absolutos Windows
```
Proyecto: d:\01_PROYECTOS_ACTIVOS\CEREBRO_MASTER_NEXUS_001
Backups: d:\01_PROYECTOS_ACTIVOS\CEREBRO_MASTER_NEXUS_001\backups
Scripts: d:\01_PROYECTOS_ACTIVOS\CEREBRO_MASTER_NEXUS_001\scripts
```

### Puertos Reservados
```
8003  - NEXUS API Master (Cerebro V2.0.0)
5437  - nexus_postgresql_v2
6382  - nexus_redis_master
3001  - Grafana
9091  - Prometheus
```

---

## 🔗 REFERENCIAS

**Documentación FASE 7 PLUS:**
- [HANDOFF_FASE7PLUS.md](./FASE_7_ECOSISTEMA%20MULTI-AI/HANDOFF_FASE7PLUS.md)
- [TRACKING_FASE7PLUS.md](./FASE_7_ECOSISTEMA%20MULTI-AI/TRACKING_FASE7PLUS.md)

**Cerebro:**
- API Docs: http://localhost:8003/docs
- Health: http://localhost:8003/health

**Global Guidelines:**
- C:\Users\ricar\.claude\CLAUDE.md (Protocolos universales NEXUS)

---

## 📝 NOTAS ESPECÍFICAS

### MCP Servers Prioritarios (Fase 1)
```
Core (4):
- Git MCP
- Filesystem MCP
- Memory MCP (PostgreSQL)
- Redis MCP

Development (3):
- GitHub Actions MCP
- Docker MCP
- Kubernetes MCP

Data (3):
- PostgreSQL MCP
- SQLite MCP
- Pandas MCP

Utilities (2):
- Brave Search MCP
- Fetch MCP
```

### IDEs Adicionales Candidatos
```
Alta Prioridad:
- NEXUS@ZED (FREE) - 120fps GPU rendering
- NEXUS@WINDSURF (FREE tier) - Cascade agentic
- NEXUS@NEOVIM (FREE) - Terminal workflows

Media Prioridad:
- NEXUS@SUBLIME (FREE) - Lightweight
- NEXUS@REPLIT (FREE tier) - Web-based
```

---

**Última Actualización:** 2 Noviembre 2025 - NEXUS@CLI
**Estado:** FASE 8 + NEXUS_CREW Integration (Phase 2 Priority 3 ✅)
**NEXUS_CREW:** 4/4 agents operational (Project Auditor, Memory Curator, Document Reconciler, Semantic Router)
**Neo4j:** Integrated + Real-time sync validated ✅
