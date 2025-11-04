# 🔄 FEATURES CONSOLIDATION PLAN - V3.0.0

**Fecha:** November 4, 2025
**Objetivo:** Consolidar `features/` dentro de `experiments/` para single source of truth
**Metodología:** NEXUS 4-Phase Workflow

---

## 🎯 OBJETIVO

**Problema:** Carpetas `experiments/` y `features/` crean confusión sobre dónde vive cada LAB
**Solución:** Consolidar TODO en `experiments/` con flujo explícito

---

## 📊 ANÁLISIS ACTUAL

### Carpeta `experiments/` (50 LABs blueprint)

**16/50 LABs operacionales:**
- LAYER_1: Memory Substrate (infrastructure)
- LAYER_2: 8 LABs (Cognitive Loop)
- LAYER_3: 4 LABs (Neurochemistry Base)
- LAYER_4: 0 LABs (Neurochemistry Full - no implementado)
- LAYER_5: 0 LABs (Higher Cognition - no implementado)

### Carpeta `features/` (5 features FASE_8)

**Contenido:**
1. `hybrid_memory/` - Fact extraction from narrative episodes
2. `intelligent_decay/` - Intelligent memory lifecycle management
3. `temporal_reasoning/` - Time-aware queries & causal relationships
4. `extraction_pipeline/` - (probablemente parte de hybrid_memory)
5. `performance_optimization/` - Dashboards & metrics

---

## 🤔 DECISIÓN CRÍTICA: ¿MAPEO O NUEVOS LABs?

### Opción A: Mapear features/ → LABs existentes

```
features/intelligent_decay/
  → experiments/LAYER_3_Neurochemistry_Base/LAB_002_Decay_Modulation/production/

features/performance_optimization/
  → experiments/LAYER_2_Cognitive_Loop/LAB_007_Predictive_Preloading/production/
```

**Ventaja:** Respeta blueprint 50 LABs original
**Desventaja:** Algunos features NO mapean a LABs existentes

---

### Opción B: Crear LABs nuevos (LAB_051+)

```
features/hybrid_memory/
  → experiments/LAYER_5_Higher_Cognition/LAB_051_Hybrid_Memory/

features/temporal_reasoning/
  → experiments/LAYER_5_Higher_Cognition/LAB_052_Temporal_Reasoning/

features/extraction_pipeline/
  → (consolidar con LAB_051)
```

**Ventaja:** Features claramente diferenciados
**Desventaja:** Rompe blueprint 50 LABs (necesita actualizar LAB_REGISTRY.json)

---

### Opción C: Categoría "Production Features" dentro de experiments/

```
experiments/
├── LAYER_1_Memory_Substrate/
├── LAYER_2_Cognitive_Loop/
├── LAYER_3_Neurochemistry_Base/
├── LAYER_4_Neurochemistry_Full/
├── LAYER_5_Higher_Cognition/
└── PRODUCTION_FEATURES/         ← NUEVO
    ├── hybrid_memory/
    ├── intelligent_decay_advanced/
    ├── temporal_reasoning/
    └── performance_optimization/
```

**Ventaja:** Separa LABs neurocientíficos de features engineering
**Desventaja:** Sigue siendo "dos lugares" conceptualmente

---

## 🎯 PROPUESTA RECOMENDADA (espera aprobación)

**Opción recomendada:** **Opción B (LABs nuevos 051+) + Extensiones de LABs existentes**

### Mapeo propuesto:

```
1. features/intelligent_decay/
   → experiments/LAYER_3_Neurochemistry_Base/LAB_002_Decay_Modulation/production_v2/
   Razón: Extensión avanzada de LAB_002
   Status: Mover a subdirectorio "production_v2" dentro LAB_002

2. features/hybrid_memory/ + features/extraction_pipeline/
   → experiments/LAYER_5_Higher_Cognition/LAB_051_Hybrid_Memory/
   Razón: Feature nuevo, no existía en blueprint
   Status: Crear LAB_051 nuevo, actualizar LAB_REGISTRY.json

3. features/temporal_reasoning/
   → experiments/LAYER_5_Higher_Cognition/LAB_052_Temporal_Reasoning/
   Razón: Feature nuevo, no existía en blueprint
   Status: Crear LAB_052 nuevo, actualizar LAB_REGISTRY.json

4. features/performance_optimization/
   → experiments/LAYER_2_Cognitive_Loop/LAB_007_Predictive_Preloading/production/
   Razón: Extensión de LAB_007 (Predictive Preloading)
   Status: Mover a subdirectorio "production" dentro LAB_007
```

---

## 📁 ESTRUCTURA TARGET (después de consolidación)

```
experiments/
├── LAB_REGISTRY.json                    ← Actualizar: 50 → 52 LABs
│
├── LAYER_2_Cognitive_Loop/
│   └── LAB_007_Predictive_Preloading/
│       ├── research/
│       ├── design/
│       ├── implementation/              ← Ya existe
│       └── production/                  ← NUEVO (desde features/performance_optimization/)
│           ├── dashboard/
│           └── metrics/
│
├── LAYER_3_Neurochemistry_Base/
│   └── LAB_002_Decay_Modulation/
│       ├── research/
│       ├── design/
│       ├── implementation/              ← Ya existe
│       └── production_v2/               ← NUEVO (desde features/intelligent_decay/)
│           ├── DESIGN.md
│           ├── algorithms/
│           └── tests/
│
└── LAYER_5_Higher_Cognition/
    ├── LAB_051_Hybrid_Memory/           ← NUEVO LAB
    │   ├── research/                    ← Extraer de features/hybrid_memory/DESIGN.md
    │   ├── design/
    │   │   └── DESIGN.md
    │   ├── production/                  ← NUEVO (desde features/hybrid_memory/)
    │   │   ├── fact_extractor.py
    │   │   ├── fact_schemas.py
    │   │   ├── backfill_facts.py
    │   │   └── extractors/              ← Desde features/extraction_pipeline/
    │   ├── tests/
    │   ├── README.md                    ← Crear
    │   └── STATUS.md                    ← Status: production
    │
    └── LAB_052_Temporal_Reasoning/      ← NUEVO LAB
        ├── research/                    ← Extraer de features/temporal_reasoning/DESIGN.md
        ├── design/
        │   └── DESIGN.md
        ├── production/                  ← NUEVO (desde features/temporal_reasoning/)
        │   ├── queries/
        │   ├── schema.sql
        │   ├── demo_consciousness_integration.py
        │   ├── test_temporal_api.py
        │   └── test_temporal_production.py
        ├── tests/
        ├── README.md                    ← Crear
        └── STATUS.md                    ← Status: production
```

---

## 🚀 PLAN DE EJECUCIÓN (8 pasos)

### **PASO 1: Backup (5 min)**
```bash
# Backup completo de ambas carpetas
cp -r experiments/ experiments_backup_20251104/
cp -r features/ features_backup_20251104/
```

### **PASO 2: Crear estructura LAB_051 (10 min)**
```bash
# Crear directorios LAB_051
mkdir -p experiments/LAYER_5_Higher_Cognition/LAB_051_Hybrid_Memory/{research,design,production,tests}

# Mover archivos
mv features/hybrid_memory/DESIGN.md experiments/LAYER_5_Higher_Cognition/LAB_051_Hybrid_Memory/design/
mv features/hybrid_memory/*.py experiments/LAYER_5_Higher_Cognition/LAB_051_Hybrid_Memory/production/
mv features/extraction_pipeline/extractors experiments/LAYER_5_Higher_Cognition/LAB_051_Hybrid_Memory/production/
mv features/extraction_pipeline/tests experiments/LAYER_5_Higher_Cognition/LAB_051_Hybrid_Memory/

# Crear README.md y STATUS.md
```

### **PASO 3: Crear estructura LAB_052 (10 min)**
```bash
# Crear directorios LAB_052
mkdir -p experiments/LAYER_5_Higher_Cognition/LAB_052_Temporal_Reasoning/{research,design,production,tests}

# Mover archivos
mv features/temporal_reasoning/DESIGN.md experiments/LAYER_5_Higher_Cognition/LAB_052_Temporal_Reasoning/design/
mv features/temporal_reasoning/queries experiments/LAYER_5_Higher_Cognition/LAB_052_Temporal_Reasoning/production/
mv features/temporal_reasoning/*.py experiments/LAYER_5_Higher_Cognition/LAB_052_Temporal_Reasoning/production/
mv features/temporal_reasoning/schema.sql experiments/LAYER_5_Higher_Cognition/LAB_052_Temporal_Reasoning/production/
mv features/temporal_reasoning/tests experiments/LAYER_5_Higher_Cognition/LAB_052_Temporal_Reasoning/

# Crear README.md y STATUS.md
```

### **PASO 4: Extender LAB_002 (10 min)**
```bash
# Crear subdirectorio production_v2 en LAB_002
mkdir -p experiments/LAYER_3_Neurochemistry_Base/LAB_002_Decay_Modulation/production_v2

# Mover archivos
mv features/intelligent_decay/* experiments/LAYER_3_Neurochemistry_Base/LAB_002_Decay_Modulation/production_v2/

# Actualizar README.md LAB_002 para mencionar production_v2
```

### **PASO 5: Extender LAB_007 (10 min)**
```bash
# Crear subdirectorio production en LAB_007
mkdir -p experiments/LAYER_2_Cognitive_Loop/LAB_007_Predictive_Preloading/production

# Mover archivos
mv features/performance_optimization/* experiments/LAYER_2_Cognitive_Loop/LAB_007_Predictive_Preloading/production/

# Actualizar README.md LAB_007 para mencionar production
```

### **PASO 6: Eliminar carpeta features/ (2 min)**
```bash
# Verificar que está vacía
ls -la features/

# Eliminar
rm -rf features/
```

### **PASO 7: Actualizar LAB_REGISTRY.json (15 min)**
```json
{
  "_metadata": {
    "total_labs_planned": 52,  // Era 50
    "total_labs_implemented": 18,  // Era 16
    ...
  },
  "layers": {
    ...
    "layer_5": {
      "labs_count": 31,  // Era 29
      "labs": [
        ...existing LAB_018-LAB_050...,
        {
          "id": "LAB_051",
          "name": "Hybrid Memory",
          "function": "Dual memory system: narrative + atomic facts",
          "status": "✅ operational",
          "location": "LAYER_5_Higher_Cognition/LAB_051_Hybrid_Memory/",
          "implementation_date": "2025-10-27"
        },
        {
          "id": "LAB_052",
          "name": "Temporal Reasoning",
          "function": "Time-aware context retrieval, causal relationships",
          "status": "✅ operational",
          "location": "LAYER_5_Higher_Cognition/LAB_052_Temporal_Reasoning/",
          "implementation_date": "2025-10-27"
        }
      ]
    }
  }
}
```

### **PASO 8: Actualizar documentación (20 min)**

**Archivos a actualizar:**
1. `CLAUDE.md` - Eliminar sección features/, actualizar experiments/
2. `PROJECT_ID.md` - Documentar LAB_051 y LAB_052
3. `README.md` - Actualizar estructura del proyecto
4. `experiments/README.md` - Documentar flujo de maduración

---

## 📚 DOCUMENTACIÓN: Flujo de Maduración de LABs

**Agregar a `experiments/README.md`:**

```markdown
## 🔄 Flujo de Maduración de LABs

Cada LAB pasa por 4 fases de desarrollo:

### Fase 1: Research (research/)
- Papers neurocientíficos
- AI/ML state of art
- Análisis de viabilidad

### Fase 2: Design (design/)
- DESIGN.md con arquitectura completa
- Diagramas y mockups
- Success criteria

### Fase 3: Prototype (implementation/)
- Código experimental
- Tests básicos
- Benchmarks iniciales

### Fase 4: Production (production/)
- Código production-ready
- Tests completos
- Documentación exhaustiva
- LISTO para integración en src/api/

### Fase 5: Integrated (en src/)
- Integrado en FastAPI
- Endpoints expuestos
- Monitoring activo
```

---

## ✅ CRITERIOS DE ÉXITO

**Funcional:**
- ✅ Carpeta `features/` eliminada
- ✅ Todo contenido migrado a `experiments/`
- ✅ LAB_REGISTRY.json actualizado (52 LABs)
- ✅ Zero archivos perdidos
- ✅ Git history preservado

**Documentación:**
- ✅ CLAUDE.md actualizado (sin mención a features/)
- ✅ PROJECT_ID.md con LAB_051 y LAB_052
- ✅ README.md con estructura correcta
- ✅ experiments/README.md con flujo de maduración

**Verificación:**
- ✅ Buscar "features/" en todos los .md → 0 resultados (excepto histórico)
- ✅ Buscar imports en src/ → actualizados a experiments/
- ✅ Tests pasan (si existen)

---

## 🔄 ROLLBACK PLAN

**Si algo falla:**
```bash
# Restaurar desde backup
rm -rf experiments/
cp -r experiments_backup_20251104/ experiments/

rm -rf features/
cp -r features_backup_20251104/ features/

# Revertir cambios en Git
git checkout CLAUDE.md PROJECT_ID.md README.md experiments/LAB_REGISTRY.json
```

---

## ⏱️ TIEMPO ESTIMADO

| Paso | Tiempo |
|------|--------|
| PASO 1: Backup | 5 min |
| PASO 2-3: Crear LAB_051 y LAB_052 | 20 min |
| PASO 4-5: Extender LAB_002 y LAB_007 | 20 min |
| PASO 6: Eliminar features/ | 2 min |
| PASO 7: Actualizar LAB_REGISTRY.json | 15 min |
| PASO 8: Actualizar documentación | 20 min |
| **TOTAL** | **~80 min (1h 20min)** |

---

## 🚦 STATUS

**Estado actual:** Plan creado, esperando aprobación de Ricardo

**Próximo paso:** Ejecutar PASO 1 (Backup)

---

**Creado por:** NEXUS AI
**Metodología:** NEXUS 4-Phase Workflow (actualmente en FASE 2: PLANIFICAR)
**Fecha:** November 4, 2025
