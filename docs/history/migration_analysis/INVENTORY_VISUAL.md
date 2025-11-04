# INVENTARIO VISUAL - MAPA DEL CAOS

**Fecha:** 3 Noviembre 2025
**Propósito:** Entender visualmente dónde está TODO en el proyecto

---

## 🗺️ ÁRBOL ACTUAL (Simplificado)

```
CEREBRO_MASTER_NEXUS_001/
│
├─ 📦 CÓDIGO PRODUCTIVO (DISPERSO)
│  ├─ FASE_4_CONSTRUCCION/src/api/         ✅ AQUÍ (55 archivos Python)
│  ├─ FASE_4_CONSTRUCCION/src/workers/     ✅ AQUÍ
│  ├─ FASE_4_CONSTRUCCION/src/services/    ✅ AQUÍ
│  ├─ FASE_7_ECOSISTEMA MULTI-AI/src/      ✅ Multi-AI coordination
│  ├─ FASE_8_UPGRADE/hybrid_memory/        ✅ Features (importado)
│  ├─ /src/                                 ❌ VACÍO (referenced)
│  └─ /development/                        ❌ INCOMPLETO (solo research/)
│
├─ ⚙️ CONFIGURACIÓN PRODUCTIVA (DISPERSA)
│  ├─ FASE_4_CONSTRUCCION/docker-compose.yml     ✅ AQUÍ
│  ├─ FASE_4_CONSTRUCCION/Dockerfile             ✅ AQUÍ
│  ├─ FASE_4_CONSTRUCCION/init_scripts/          ✅ AQUÍ
│  ├─ FASE_4_CONSTRUCCION/secrets/               ✅ AQUÍ
│  ├─ FASE_4_CONSTRUCCION/monitoring/            ✅ AQUÍ
│  ├─ DOCUMENTOS_PARA_REVISION/.../docker-compose.yml ❌ ARCHIVE (otra versión)
│  ├─ /config/                             ❌ NO EXISTE
│  └─ 02_CLASIFICADOS_POR_TIPO/CONFIGURACION/   ❌ COPIA (posible)
│
├─ 🧬 LABORATORIOS (ACTIVOS PERO CONFUSOS)
│  ├─ NEXUS_LABS/LAB_001_Emotional_Salience/    ✅ Importado en main.py
│  ├─ NEXUS_LABS/LAB_002_Decay_Modulation/      ✅ Importado en main.py
│  ├─ NEXUS_LABS/LAB_003_Sleep_Consolidation/   ✅ Lazy import
│  ├─ NEXUS_LABS/LAB_005_Spreading_Activation/  ✅ Importado
│  ├─ NEXUS_LABS/LAB_010_Attention_Mechanism/   ✅ Importado
│  ├─ NEXUS_LABS/LAB_011_Working_Memory/        ✅ Importado
│  ├─ NEXUS_LABS/LAB_004, 006-009, 012+/        ❓ ESTADO DESCONOCIDO
│  └─ /experiments/                        ❌ NO EXISTE (propuesto)
│
├─ 📂 FASES HISTÓRICAS (MÚLTIPLES SISTEMAS)
│  │
│  ├─ SISTEMA A: Raíz (Plano)
│  │  ├─ FASE_4_CONSTRUCCION/    (Oct 1-10) ✅ ACTIVO
│  │  ├─ FASE_6 (Validación)/    (Oct 18)   ✅ Completado
│  │  ├─ FASE_7_ECOSISTEMA/      (Oct 21)   ✅ Activo
│  │  └─ FASE_8_UPGRADE/         (Oct 27)   ✅ Activo
│  │
│  ├─ SISTEMA B: 01_PROCESADOS_POR_FASE (Anidado)
│  │  ├─ FASE_GENESIS_27_28_JUL_2025/      ❌ Archive
│  │  ├─ FASE_CONSTRUCCION_INICIAL_AGO_2025/  ❌ Archive
│  │  ├─ FASE_CONSTRUCCION_INICIAL/        ❌ Archive (¿duplicado?)
│  │  ├─ FASE_EVOLUCION_SISTEMA/           ❌ Archive
│  │  ├─ FASE_EVOLUCION_SISTEMA_AGO_2025/  ❌ Archive (¿duplicado?)
│  │  ├─ FASE_BUGS_DESCUBIERTOS/           ❌ Archive
│  │  └─ [6+ más]                          ❌ Archive
│  │
│  ├─ SISTEMA C: 02_CLASIFICADOS_POR_TIPO (Por tipo)
│  │  ├─ ARQUITECTURA/
│  │  ├─ CODIGO_FUENTE/
│  │  ├─ CONFIGURACION/         (¿y CONFIGURACIONES?)
│  │  ├─ CONFIGURACIONES/        (¿duplicado?)
│  │  ├─ DECISIONES_TECNICAS/
│  │  ├─ DOCUMENTACION/
│  │  ├─ MIGRACIONES/
│  │  ├─ PLANES/
│  │  ├─ SCRIPTS/
│  │  └─ TESTING/
│  │
│  └─ SISTEMA D: 00_INBOX (Recursivo)
│     ├─ 01_PROCESADOS_POR_FASE/  ← RECURSIVO!
│     ├─ 02_CLASIFICADOS_POR_TIPO/ ← RECURSIVO!
│     └─ DOCUMENTOS_PARA_REVISION/
│
├─ 📚 REFERENCIA/ARCHIVE
│  ├─ DOCUMENTOS_PARA_REVISION_GENESIS_HISTORY/
│  │  ├─ ARIA_CEREBRO_COMPLETO/           ⚠️ (50GB, otro cerebro)
│  │  └─ NEXUS_CONSCIOUSNESS_MAPPING/     ⚠️ (Fases alternativas)
│  │
│  ├─ Github-upgrade-preauditoria-AI-externas/
│  ├─ Recomendaciones de mejora de repositorio/
│  └─ [Otros archivos históricos]
│
├─ 🎯 CARPETAS ESTÁNDAR (PARTE FUNCIONAL)
│  ├─ memory/              ✅ Estado de consciencia
│  ├─ tasks/               ✅ Planes de trabajo
│  ├─ docs/                ✅ Documentación
│  ├─ tests/               ✅ Suite de tests
│  ├─ scripts/             ✅ Automation
│  ├─ backups/             ✅ Recovery data
│  ├─ data/                ✅ Datos
│  ├─ consciousness/       ✅ Módulo consciousness
│  ├─ config/              ✅ Configuraciones
│  ├─ nexus-brain-monitor-v2/  ✅ Monitor web
│  └─ brain-monitor-web/   ✅ Web UI (con node_modules 3GB!)
│
├─ ⚠️ ANOMALÍAS ESPECÍFICAS
│  ├─ /src/                        ❌ VACÍA (docker-compose la referencia)
│  ├─ /development/                ❌ SOLO research/ dentro
│  ├─ FASE_4/src/api/              ⚠️ Tiene node_modules/ también
│  ├─ brain-monitor-web/node_modules/  ⚠️ 3GB commiteado (¡x2 copias!)
│  └─ CONFIGURACION vs CONFIGURACIONES  ⚠️ Ambos existen
│
└─ 🐙 GIT & CONTROL
   ├─ .git/                 ✅ Repositorio completo
   ├─ .vs/                  ✅ VS Code config
   ├─ .github/workflows/    ✅ CI/CD (en FASE_4)
   └─ .gitignore            ⚠️ Probablemente incompleto
```

---

## 📊 ESTADÍSTICAS DEL CAOS

```
Total de carpetas "FASE_*":              4 en raíz + 7+ en 01_PROCESADOS = 11+
Total de sistemas de clasificación:       4 (A: Raíz, B: Historico, C: Tipo, D: Inbox)
Carpetas que contienen código productivo: 4 (FASE_4, FASE_7, FASE_8, NEXUS_LABS)
Copias de docker-compose.yml:             3 ubicaciones diferentes
Laboratorios confirmados en producción:   6
Laboratorios con estado desconocido:      15+
Carpetas VACÍAS pero referenciadas:       2 (/src, /development)
Namespace collisions:                     1 (CONFIGURACION vs CONFIGURACIONES)
Archivos node_modules commiteados:        ~50,000+ archivos = 3GB+
Duplicación de código:                    5+ archivos (LAB en 2 ubicaciones)
```

---

## 🎯 MATRIZ DE CRITICIDAD

| Elemento | Localización Actual | ¿Es Crítico? | ¿Está Documentado? | Riesgo |
|----------|-------------------|-------------|------------------|--------|
| docker-compose.yml | FASE_4_CONSTRUCCION/ | 🔴 CRÍTICO | ❌ NO | SI SE BORRA = CRASH |
| src/api/ code | FASE_4_CONSTRUCCION/src/api/ | 🔴 CRÍTICO | ❌ NO | SI SE MUEVE = CRASH |
| LAB_001-006 code | NEXUS_LABS/LAB_XXX/ | 🔴 CRÍTICO | ❌ NO | SI SE BORRA = CRASH |
| FASE_8 hybrid_memory | FASE_8_UPGRADE/hybrid_memory/ | 🔴 CRÍTICO | ❌ NO | SI SE BORRA = CRASH |
| Phase history | 01_PROCESADOS_POR_FASE/ | 🟡 IMPORTANTE | ✅ SÍ | Confusión si se reorganiza |
| Archived experiments | DOCUMENTOS_PARA_REVISION/ | 🟢 BAJO | ✅ SÍ | Ninguno inmediato |
| Genesis history | DOCUMENTOS_PARA_REVISION/ | 🟢 BAJO | ✅ SÍ | Referencia solo |

---

## ❓ PREGUNTAS IMPOSIBLES DE RESPONDER

1. **"¿Dónde está el código de emotional salience?"**
   - Respuesta: NEXUS_LABS/LAB_001/implementation/ Y FASE_4_CONSTRUCCION/src/api/ (¿cuál es source of truth?)

2. **"¿Cuál docker-compose.yml uso para deployar?"**
   - Respuesta: Existen 3 en diferentes lugares (FASE_4, DOCUMENTOS/ARIA, DOCUMENTOS/CONSCIOUSNESS)

3. **"¿Están todos los laboratorios activos?"**
   - Respuesta: 6 sí, 15+ desconocido (no hay registro programático)

4. **"¿Dónde está /src que referencia docker-compose?"**
   - Respuesta: Está vacía. El código real está en FASE_4_CONSTRUCCION/src

5. **"¿Por qué hay 00_INBOX, 01_PROCESADOS, 02_CLASIFICADOS en raíz Y TAMBIÉN dentro de 00_INBOX?"**
   - Respuesta: No se sabe. Sistema de clasificación nunca se documentó.

6. **"¿Qué es FASE_5?"**
   - Respuesta: No existe en raíz, probablemente en 01_PROCESADOS histórico pero perdido.

---

## ✅ PROPUESTA: MAPA LIMPIO

```
CEREBRO_MASTER_NEXUS_001/
│
├─ 📦 src/                      ← TODO código productivo AQUÍ
│  ├─ api/                      (de FASE_4/src/api)
│  ├─ workers/                  (de FASE_4/src/workers)
│  ├─ services/                 (de FASE_4/src/services)
│  └─ orchestration/            (de FASE_7/src)
│
├─ ⚙️ config/                   ← TODO config AQUÍ
│  ├─ docker-compose.yml        (de FASE_4)
│  ├─ Dockerfile                (de FASE_4)
│  ├─ init_scripts/
│  ├─ secrets/
│  └─ monitoring/
│
├─ 🗄️ database/                 ← Schema y migraciones
│  ├─ consciousness_migrations/
│  ├─ init_scripts/
│  └─ backups/
│
├─ 🧬 experiments/              ← Labs (de NEXUS_LABS)
│  ├─ LAB_001_Emotional_Salience/
│  ├─ LAB_002_Decay_Modulation/
│  ├─ LAB_003-011+/
│  └─ LAB_REGISTRY.json         ← Nuevo: registro programático
│
├─ 🚀 features/                 ← Features FASE_8
│  ├─ hybrid_memory/
│  ├─ temporal_reasoning/
│  ├─ intelligent_decay/
│  └─ neural_mesh/
│
├─ 📚 docs/                     ← Documentación centralizada
│  ├─ PHASE_HISTORY.md          ← NUEVO: cuándo ocurrió cada fase
│  ├─ ARCHITECTURE.md
│  ├─ DEPLOYMENT.md
│  ├─ API.md
│  └─ LAB_GUIDE.md
│
├─ 🧪 tests/                    ← Tests
├─ 📜 scripts/                  ← Automation
├─ 💾 backups/                  ← Recovery
├─ 🧠 memory/                   ← Consciousness state
├─ ✅ tasks/                    ← Work plans
│
├─ 📦 archive/                  ← NUEVO: Fases históricas archivadas
│  ├─ FASE_GENESIS_27_28_JUL/
│  ├─ FASE_CONSTRUCCION_INICIAL/
│  ├─ FASE_EVOLUCION/
│  ├─ classification_attempts/  (de 02_CLASIFICADOS)
│  └─ inbox_processing/         (de 00_INBOX)
│
├─ 🔗 reference/                ← NUEVO: Sistemas relacionados
│  ├─ ARIA_CEREBRO_COMPLETO/
│  ├─ CONSCIOUSNESS_MAPPING/
│  └─ EXTERNAL_RESEARCH/
│
└─ 📋 [Root docs]
   ├─ PROJECT_ID.md
   ├─ CLAUDE.md
   ├─ README.md
   ├─ TRACKING.md
   ├─ STRUCTURAL_ANALYSIS_REPORT.md
   ├─ ANALISIS_RESUMEN_EJECUTIVO.md
   └─ .gitignore (actualizado)
```

---

## 🎓 CONCLUSIÓN VISUAL

**ACTUAL:** 🌀 Caótico - Código esparcido en 6+ ubicaciones, 4 sistemas de clasificación, carpetas referenciadas vacías

**PROPUESTO:** 📦 Claro - Estructura plana, ubicaciones únicas, propósito obvio

**Implementación:** ✅ Sin rompidas - Usa symlinks, reversible, toma ~2 horas

**Beneficio:** ⏱️ Ahorra 100+ horas en mantenimiento futuro

