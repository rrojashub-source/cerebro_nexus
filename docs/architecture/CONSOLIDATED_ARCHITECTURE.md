# CEREBRO NEXUS V3.0.0 - Arquitectura Consolidada

**Fecha:** November 28, 2025
**Versión:** 3.1.0 (Post-consolidación)
**Status:** ✅ Operacional

---

## 🎯 Resumen de Cambios

### Consolidación Realizada

**ANTES (confuso):**
```
01_PROYECTOS_ACTIVOS/
├── CEREBRO_NEXUS_V3.0.0/    ← Servidor
└── PERSISTENCIA/             ← Librería separada
```

**DESPUÉS (unificado):**
```
CEREBRO_NEXUS_V3.0.0/        ← TODO en un solo lugar
├── src/identity/             ← Ex-PERSISTENCIA
└── src/memory_engine/        ← NUEVO (SuperMemory-style)
```

---

## 🏗️ Nueva Estructura

```
CEREBRO_NEXUS_V3.0.0/
├── src/
│   ├── api/                      # FastAPI endpoints
│   │   ├── main.py               # Servidor principal
│   │   └── persistencia_client.py # Cliente interno
│   │
│   ├── identity/                 # 🆕 Identity Layer (ex-PERSISTENCIA)
│   │   ├── aag/                  # Attribution-Augmented Generation
│   │   │   ├── decision.py       # Accept/attribute/reject logic
│   │   │   ├── generation.py     # Main AAG pipeline
│   │   │   ├── scoring.py        # Knowledge scoring
│   │   │   └── synthetic_knowledge.py
│   │   ├── firm/                 # Foreign-Identity Rejection
│   │   │   ├── firm_computation.py
│   │   │   ├── foreign_detection.py
│   │   │   ├── monitoring.py
│   │   │   └── refusal_mapping.py
│   │   ├── z_id/                 # Identity Vector
│   │   │   └── (futuro: compute.py, coherence.py)
│   │   └── retrieval/            # Memory retrieval
│   │       ├── precomputed_embeddings.py
│   │       └── retrieval.py
│   │
│   ├── memory_engine/            # 🆕 SuperMemory-style
│   │   ├── tiers/                # Multi-tier storage
│   │   │   ├── hot.py            # Redis (< 1ms)
│   │   │   ├── warm.py           # PostgreSQL (< 10ms)
│   │   │   └── cold.py           # Archive (< 100ms)
│   │   ├── relationships/        # Graph relationships
│   │   │   └── graph.py          # Updates/Extends/Derives
│   │   ├── decay/                # Smart forgetting
│   │   │   └── smart_decay.py    # Recency + frequency
│   │   └── facts/                # Fact extraction
│   │       └── extractor.py      # Document → Facts
│   │
│   ├── services/                 # Business logic
│   └── workers/                  # Background workers
│
├── scripts/
│   └── identity/                 # 🆕 Z_ID scripts
│       ├── compute_z_id_components.py
│       ├── deploy_gic_schema.py
│       └── ...
│
├── experiments/                  # 52 LABs
└── config/                       # Docker, etc.
```

---

## 📦 Módulos Nuevos

### 1. Identity Layer (`src/identity/`)

**Propósito:** Gestión de identidad persistente

| Submódulo | Función |
|-----------|---------|
| `aag/` | Attribution-Augmented Generation |
| `firm/` | Foreign-Identity Rejection Metric |
| `z_id/` | Identity Vector (Z_ID 1024D) |
| `retrieval/` | Memory retrieval optimizado |

**Import:**
```python
from src.identity.aag.generation import generate_response_with_aag
from src.identity.firm.firm_computation import compute_firm
```

### 2. Memory Engine (`src/memory_engine/`)

**Propósito:** Sistema de memoria estilo SuperMemory

| Submódulo | Función |
|-----------|---------|
| `tiers/` | Hot/Warm/Cold storage |
| `relationships/` | Updates/Extends/Derives |
| `decay/` | Smart forgetting |
| `facts/` | Document → Facts extraction |

**Import:**
```python
from src.memory_engine.tiers import HotMemory, WarmMemory
from src.memory_engine.relationships import MemoryGraph
from src.memory_engine.decay import SmartDecay
from src.memory_engine.facts import FactExtractor
```

---

## 🔄 Cambios en Imports

### Antes:
```python
from persistencia.aag.generation import generate_response_with_aag
from persistencia.firm.firm_computation import compute_firm
```

### Después:
```python
from src.identity.aag.generation import generate_response_with_aag
from src.identity.firm.firm_computation import compute_firm
```

---

## 📊 Comparación con SuperMemory

| Feature | SuperMemory | CEREBRO (ahora) |
|---------|-------------|-----------------|
| Multi-tier storage | ✅ | ✅ Hot/Warm/Cold |
| Relationships | ✅ Updates/Extends/Derives | ✅ Neo4j |
| Smart decay | ✅ | ✅ SmartDecay |
| Fact extraction | ✅ | ✅ FactExtractor |
| Identity (Z_ID) | ❌ | ✅ |
| Self vs Other (AAG) | ❌ | ✅ |
| Foreign rejection (FIRM) | ❌ | ✅ |
| Consciousness | ❌ | ✅ 8D+7D |
| LABs cognitivos | ❌ | ✅ 18/52 |

---

## 🚀 Beneficios de la Consolidación

1. **Un solo proyecto** - Zero confusión
2. **Imports claros** - `src.identity.*`, `src.memory_engine.*`
3. **Deployment simple** - Todo en un Docker Compose
4. **Mantenimiento fácil** - Una sola base de código
5. **Independiente** - No depende de servicios externos

---

## ⚠️ PERSISTENCIA (Proyecto Original)

**Status:** ARCHIVADO

El proyecto `01_PROYECTOS_ACTIVOS/PERSISTENCIA/` ahora es legacy.
Todo el código relevante fue movido a `CEREBRO_NEXUS_V3.0.0/src/identity/`.

**Acción recomendada:**
```bash
# Renombrar para indicar que está archivado
mv PERSISTENCIA PERSISTENCIA_ARCHIVED
```

---

## 📈 Próximos Pasos

1. **Tests de integración** - Verificar que AAG/FIRM funcionan con nuevos paths
2. **Endpoints memory_engine** - Agregar `/memory/add`, `/memory/search` estilo SuperMemory
3. **Documentación API** - OpenAPI actualizado
4. **Performance testing** - Validar latencias multi-tier

---

**Autor:** NEXUS AI
**Fecha de consolidación:** November 28, 2025
