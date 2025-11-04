# 🔧 LAB Cluster Integration Plan - Cognition Loop

**Status:** 🟡 In Progress
**Start Date:** October 29, 2025
**Target:** Integrate LAB_001 + LAB_006 + LAB_011 as cognitive system
**Method:** NEXUS Resiliencia Acelerada (cluster approach)

---

## 🎯 Objetivo

Integrar **3 LABS como sistema cognitivo** para crear el "Cognition Loop" mínimo funcional:

```
LAB_001 (Emotional Salience)
    ↓ feeds real salience to
LAB_010 (Attention - already integrated)
    ↓ attended memories go to
LAB_011 (Working Memory Buffer)
    ↓ working memory context back to
LAB_010 (Attention knows focus)
    ↑
LAB_006 (Metacognition)
    └─ observes and validates entire loop
```

**Beneficio esperado:**
- Attention con salience REAL (no hardcoded 0.5)
- Working memory da contexto a búsquedas
- Metacognition mide accuracy del cluster
- **Emergent properties:** El sistema "aprende" qué memoria es útil

---

## 📋 Pre-Requisitos Validados

✅ LAB_010 (Attention) ya integrado y operacional
✅ Cerebro operacional (puerto 8003)
✅ LAB_001, LAB_006, LAB_011 implementados en NEXUS_LABS
✅ Patrón de integración probado (LAB_010 exitoso)
✅ Git status clean (LAB_010 commiteado)

---

## 🗺️ Plan de Integración (12 Steps, 3 LABS)

### **Fase 1: LAB_011 - Working Memory Buffer (Steps 1-4)**

**STEP 1: Copiar LAB_011 al Container** ⏳
- [ ] Copiar `working_memory_buffer.py` a `/FASE_4_CONSTRUCCION/src/api/`
- [ ] Verificar dependencies (collections, datetime)
- [ ] Test import del módulo
- [ ] Checkpoint: Archivo copiado, imports OK

**STEP 2: Modificar main.py - LAB_011 Imports** ⏳
- [ ] Agregar: `from working_memory_buffer import WorkingMemoryBuffer`
- [ ] Crear instancia global después de app init
- [ ] Validar /health responde
- [ ] Checkpoint: Imports OK, API healthy

**STEP 3: Crear Endpoint /memory/working** ⏳
- [ ] POST `/memory/working/add` - Agregar item a buffer
- [ ] GET `/memory/working/items` - Ver items actuales
- [ ] POST `/memory/working/clear` - Limpiar buffer
- [ ] GET `/memory/working/stats` - Stats (capacity, count)
- [ ] Checkpoint: Endpoints funcionando

**STEP 4: Tests LAB_011** ⏳
- [ ] Test: Add 3 items → buffer size = 3
- [ ] Test: Add 10 items → buffer size = 7 (capacity limit)
- [ ] Test: Get items → devuelve en orden correcto
- [ ] Test: Clear → buffer vacío
- [ ] Checkpoint: LAB_011 operacional

---

### **Fase 2: LAB_001 - Emotional Salience (Steps 5-8)**

**STEP 5: Copiar LAB_001 al Container** ⏳
- [ ] Copiar `emotional_salience_scorer.py` a `/FASE_4_CONSTRUCCION/src/api/`
- [ ] Verificar dependencies (re, datetime)
- [ ] Test import del módulo
- [ ] Checkpoint: Archivo copiado, imports OK

**STEP 6: Modificar main.py - LAB_001 Imports** ⏳
- [ ] Agregar: `from emotional_salience_scorer import EmotionalSalienceScorer`
- [ ] Crear instancia global
- [ ] Validar /health responde
- [ ] Checkpoint: Imports OK, API healthy

**STEP 7: Integrar LAB_001 → LAB_010 Connection** ⏳
- [ ] Modificar `/memory/search` con LAB_001 integration:
  - Si `use_attention=true`, calcular salience real con LAB_001
  - Actualizar `candidate.emotional_salience` (no hardcoded 0.5)
  - Pasar salience a LAB_010 attention scoring
- [ ] Checkpoint: LAB_001 conectado a LAB_010

**STEP 8: Tests LAB_001 + LAB_010 Integration** ⏳
- [ ] Test: Search con emotional keywords ("urgent", "critical")
- [ ] Verificar: Salience boost visible en logs
- [ ] Test: Comparar attention con/sin emotional salience
- [ ] Checkpoint: Integration LAB_001 + LAB_010 funciona

---

### **Fase 3: LAB_006 - Metacognition Logger (Steps 9-11)**

**STEP 9: Copiar LAB_006 al Container** ⏳
- [ ] Copiar `metacognition_logger.py` a `/FASE_4_CONSTRUCCION/src/api/`
- [ ] Verificar dependencies (dataclasses, datetime, statistics)
- [ ] Test import del módulo
- [ ] Checkpoint: Archivo copiado, imports OK

**STEP 10: Modificar main.py - LAB_006 Imports** ⏳
- [ ] Agregar: `from metacognition_logger import MetacognitionLogger`
- [ ] Crear instancia global
- [ ] Validar /health responde
- [ ] Checkpoint: Imports OK, API healthy

**STEP 11: Crear Endpoint /metacognition** ⏳
- [ ] POST `/metacognition/log` - Log prediction con confidence
- [ ] GET `/metacognition/calibration` - Ver ECE score
- [ ] GET `/metacognition/stats` - Stats completas
- [ ] POST `/metacognition/reset` - Reset logger
- [ ] Checkpoint: Endpoints funcionando

---

### **Fase 4: Integration Testing y Documentation (Step 12)**

**STEP 12: Tests de Cluster Completo** ⏳
- [ ] Test 1: Search → LAB_010 attention → LAB_001 salience → resultados
- [ ] Test 2: Working memory context → attention prioriza items del buffer
- [ ] Test 3: Metacognition valida accuracy de attention
- [ ] Test 4: Regression tests (otros endpoints OK)
- [ ] Performance: Overhead aceptable
- [ ] Documentación: TRACKING.md actualizado
- [ ] Git commit: Cluster completo
- [ ] Episode en cerebro: Cluster integration complete
- [ ] Checkpoint: ✅ CLUSTER INTEGRATION COMPLETE

---

## 🚨 Plan de Rollback (Si algo falla)

**Si hay error en cualquier LAB:**

1. **Identificar LAB problemático** (1, 6, u 11)
2. **Revertir cambios de ese LAB:** `git checkout -- [archivos]`
3. **Reiniciar container:** `docker restart nexus_api_master`
4. **Verificar salud:** `curl http://localhost:8003/health`
5. **Continuar con otros LABS** o pausar integración
6. **Documentar error:** Guardar en cerebro qué falló

**Rollback completo (si cluster no funciona):**
```bash
git revert HEAD  # Revertir último commit
docker restart nexus_api_master
```

---

## 📊 Success Criteria

✅ LAB_011: Working memory buffer funciona (7-item capacity)
✅ LAB_001: Emotional salience calcula scores reales
✅ LAB_010 + LAB_001: Attention usa salience real (no 0.5 hardcoded)
✅ LAB_006: Metacognition logger mide calibration
✅ Cluster integrado: Search usa todo el loop
✅ Performance: <100ms overhead total
✅ No regresiones en otros endpoints
✅ Código commiteado y documentado

---

## 🔄 Checkpoints (Estado Recuperable)

Después de cada STEP:
1. Marcar checkbox en este archivo
2. Si hay código nuevo, commit intermedio en Git
3. Guardar nota en cerebro: "LAB Cluster integration - completed STEP X"

**Archivo de estado:** Este mismo archivo (`LAB_CLUSTER_INTEGRATION_PLAN.md`)

---

## 📝 Technical Notes

**Working Memory Buffer:**
- 7-item capacity (Miller's Law)
- FIFO eviction
- Timestamps para recency
- IDs únicos por item

**Emotional Salience:**
- Pattern matching (8 emotions)
- Intensity scoring (0.0-1.0)
- Emotional keywords detection
- Feeds to LAB_010 attention

**Metacognition:**
- Confidence calibration (ECE)
- Prediction logging
- Self-awareness metrics
- Validates cluster accuracy

**Integration Pattern:**
- All LABS opt-in (flags)
- Graceful fallback on errors
- Inline instantiation (dynamic params)
- Debug logs for visibility

---

**Created:** October 29, 2025
**Method:** NEXUS Resiliencia Acelerada
**Next:** STEP 1 - Copiar LAB_011

---

## 🎯 Estado Final: ✅ CLUSTER INTEGRATION COMPLETE

**Fecha:** October 29, 2025 03:25 UTC
**Status:** ✅ **SUCCESS** - Cognition Loop operacional

### Resumen Ejecución

**3 LABS Integrados:**
1. ✅ LAB_011 (Working Memory Buffer) - 7-item capacity, HYBRID eviction
2. ✅ LAB_001 (Emotional Salience) - Connected to LAB_010 attention
3. ✅ LAB_006 (Metacognition Logger) - ECE calibration functional

**Archivos Modificados:**
- `working_memory_buffer.py` (new, 17K)
- `metacognition_logger.py` (new, 16K)
- `emotional_salience_scorer.py` (already existed, 15K)
- `main.py` (+330 lines approx)
  - 4 LAB_011 endpoints
  - LAB_001 → LAB_010 connection
  - 4 LAB_006 endpoints

**Tests Exitosos:**
- ✅ Working memory: 3/7 items tracked, avg_attention 0.9
- ✅ Emotional salience: Connected to attention mechanism
- ✅ Metacognition: Actions logged, ECE calculated (0.4 sample)
- ✅ Cluster loop: Search → Attention → Working memory → Metacognition
- ✅ Regression tests: All critical endpoints OK

**Bugs Encontrados y Resueltos:**
- ❌ LAB_011 endpoints used `.items` instead of `.buffer` → ✅ Fixed
- ❌ LAB_001 API call used wrong method name → ✅ Fixed to `calculate_salience()`

**Performance:**
- No significant overhead detected
- All opt-in features (no breaking changes)
- Graceful fallbacks working

---

## 🎯 Estado Inicial: STEP 0 - Plan Documentado ✅
