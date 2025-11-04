# 🧬 CEREBRO_NEXUS_V3.0.0 - Claude Context

**Proyecto:** CEREBRO_NEXUS_V3.0.0 - Master NEXUS Brain System (Reorganized)
**Fase Actual:** MIGRATION - Session 1 (Foundation)
**Versión:** 3.0.0
**Fecha:** 3 Noviembre 2025

---

## 🎯 CONTEXTO CRÍTICO

**ESTO ES UNA MIGRACIÓN EN PROGRESO**

- **Origen:** CEREBRO_MASTER_NEXUS_001 (V2.0.0) - Funcional pero caótico
- **Destino:** CEREBRO_NEXUS_V3.0.0 (este proyecto) - Limpio y mantenible
- **Método:** Manual + AI colaborativa (zero risk)
- **Estado:** 🟡 Session 1 - Fundación completa, esperando primera carpeta

---

## 📁 ESTRUCTURA DEL PROYECTO

```
CEREBRO_NEXUS_V3.0.0/
├── INBOX/                     # ⚠️ TEMPORAL - Staging de migración (se elimina al finalizar)
├── src/                       # Código productivo
├── config/                    # Configuraciones (Docker, secrets)
├── database/                  # Migraciones y schema
├── experiments/               # LABs validados en producción
├── features/                  # Features integradas (de FASE_8)
├── tests/                     # Test suite
├── scripts/                   # Automation
├── docs/                      # Documentación centralizada
├── memory/                    # Dynamic state (NEXUS)
├── tasks/                     # External plans
└── archive/                   # Fases históricas (read-only)
```

---

## 🔧 SERVICIOS ACTIVOS (Heredados de V2.0.0)

**NOTA:** Estos servicios corren en CEREBRO_MASTER_NEXUS_001, NO aquí (todavía)

### Docker Containers (localhost)

**Cerebro V2.0.0:**
- API Master: http://localhost:8003
- Health: http://localhost:8003/health
- Docs: http://localhost:8003/docs

**PostgreSQL:**
- nexus_postgresql_v2: puerto 5437
- aria_postgresql_v2: puerto 5438

**Redis:**
- nexus_redis_master: puerto 6382
- aria_redis_master: puerto 6381

**Monitoring:**
- Grafana: http://localhost:3001
- Prometheus: http://localhost:9091

---

## 🚀 COMANDOS RÁPIDOS

### Verificar Estado Migración
```bash
# Ver progreso migración
cat MIGRATION_MANIFEST.md

# Ver decisiones tomadas
cat DECISIONES.LOG

# Ver log de sesiones
cat TRACKING.md

# Git log
git log --oneline
```

### Validación (Cuando aplique)
```bash
# Después de migrar Docker configs:
cd config/docker
docker-compose up

# Después de migrar API:
curl http://localhost:8003/health

# Después de migrar LABs:
python -c "from experiments.LAB_001.implementation import EmotionalSalienceScorer"
```

### Git Workflow
```bash
# Estado actual
git status

# Ver cambios
git diff

# Commit después de sesión
git add .
git commit -m "feat(migration): Session X - [descripción]"

# Ver historial
git log --oneline --graph
```

---

## 📋 WORKFLOW DE MIGRACIÓN (Manual + AI)

### Rol de NEXUS (Claude):

**Decisiones AUTÓNOMAS (Nivel 1 - Técnico):**
- Clasificar archivos por tipo (.py → src/, docker-compose → config/)
- Organizar estructura interna de carpetas
- Actualizar imports en código
- Merge de documentación técnica
- Nombrar carpetas (snake_case, lógica)

**Decisiones BLOQUEANTES (Nivel 2 - Estratégico):**
- ¿Producción o legacy? (cuando no es claro)
- ¿LAB activo o experimental? (sin evidencia)
- ¿Eliminar algo potencialmente crítico?
- Conflictos documentales (2 fuentes contradictorias)

### Rol de Ricardo:

**Durante migración:**
- Copiar carpetas de V2.0.0 → `INBOX/[CARPETA]/` (una por una)
- Avisar a NEXUS: "Copiada: [CARPETA_X]"
- Aprobar decisiones bloqueantes (cuando NEXUS pregunte)
- Validar resultado de cada sesión
- INBOX/ queda vacía después de cada carpeta procesada

**Después de migración:**
- Testing completo funcionalidad
- Deployment desde V3.0.0
- Archivar V2.0.0 (cuando V3.0.0 validado)

---

## ⚠️ RESTRICCIONES CRÍTICAS

### NUNCA Tocar V2.0.0 Original

```
Path Original (NO TOCAR):
D:\01_PROYECTOS_ACTIVOS\CEREBRO_MASTER_NEXUS_001

Path Nuevo (Trabajar aquí):
D:\01_PROYECTOS_ACTIVOS\CEREBRO_NEXUS_V3.0.0
```

**Método:** COPIAR (no cortar) siempre

### Una Carpeta a la Vez

**NO hacer migraciones masivas**
- Procesar carpeta por carpeta
- Validar después de sesiones críticas
- Git commit por sesión

### Documentar TODO

**MIGRATION_MANIFEST.md:** Registro de movimientos
**DECISIONES.LOG:** Justificaciones técnicas + estratégicas
**TRACKING.md:** Log por sesión

---

## 🎓 FILOSOFÍA DE LA MIGRACIÓN

### "Function over history. Logic over legacy."

**Principios:**
1. **Ubicación por función, no por historia** - Código productivo en src/, no en "FASE_4"
2. **Claridad sobre nostalgia** - Archivar fases históricas, no mezclarlas
3. **Pruebas sobre velocidad** - Validar después de cambios críticos
4. **Documentación obligatoria** - Cada decisión registrada
5. **Reversibilidad siempre** - Git commit por sesión, rollback instantáneo

---

## 📊 MIGRACIÓN PROGRESS

**Sesión 1 (Nov 3):** ✅ Fundación completa
- Estructura de carpetas creada
- Archivos base documentados
- Git inicializado
- Listo para primera carpeta

**Sesión 2 (Pending):** Docker & Configs
**Sesión 3 (Pending):** Core API
**Sesión 4 (Pending):** Database
**Sesión 5 (Pending):** LABs Operacionales
**Sesión 6 (Pending):** Features FASE_8
**Sesión 7 (Pending):** Archive Historical

---

## 🔗 INTEGRATION WITH NEXUS ECOSYSTEM

### After Migration Complete:

**Dependencies:**
- NEXUS_CREW agents will read from V3.0.0
- Brain Monitor will point to V3.0.0
- ARIA Brain-to-Brain communication unchanged
- PostgreSQL/Redis/Neo4j unchanged

**Updates needed:**
- Docker paths in docker-compose.yml
- Import statements in API code
- Documentation references
- CI/CD pipelines (if any)

---

## 📖 DOCUMENTATION HIERARCHY

**Read BEFORE working:**
1. `PROJECT_ID.md` - Complete specification
2. `CLAUDE.md` - This file (context)
3. `MIGRATION_MANIFEST.md` - What's been migrated
4. `DECISIONES.LOG` - Why decisions were made
5. `TRACKING.md` - Session history

**Update AFTER working:**
1. `MIGRATION_MANIFEST.md` - Add new movements
2. `DECISIONES.LOG` - Add new decisions
3. `TRACKING.md` - Add session summary
4. Git commit

---

## 🆘 TROUBLESHOOTING

**Issue: "No sé dónde ubicar este archivo"**
- Leer contenido completo
- Buscar imports/referencias
- Verificar última modificación (recent = activo)
- Si ambiguo → Decisión BLOQUEANTE (preguntar Ricardo)

**Issue: "Código roto después de mover"**
- Revisar imports (paths cambiaron)
- Actualizar referencias en docker-compose.yml
- Verificar PYTHONPATH si es necesario

**Issue: "Git conflict"**
- No debería pasar (single developer)
- Si pasa: `git status` → resolver → `git add` → `git commit`

**Issue: "Quiero revertir sesión"**
```bash
git log --oneline
git revert <commit_hash>
```

---

## 🎯 PRÓXIMOS PASOS

**Ahora mismo (Session 1):**
- ✅ Estructura creada
- ✅ Documentación base completa
- ✅ Git inicializado
- 🟡 **Esperando primera carpeta de Ricardo**

**Cuando llegue primera carpeta:**
1. NEXUS lee estructura completa
2. NEXUS analiza contenido (README, código, configs)
3. NEXUS clasifica: producción / config / docs / legacy
4. NEXUS ubica en carpetas lógicas
5. NEXUS documenta en MIGRATION_MANIFEST
6. NEXUS reporta: "✅ Completado, listo para siguiente"

---

**Project Owner:** Ricardo
**Created:** November 3, 2025
**Status:** 🟡 In migration (Session 1)
**Maintained by:** NEXUS@CLI + Ricardo

---

**"Zero risk. Incremental progress. Documentation always."**
