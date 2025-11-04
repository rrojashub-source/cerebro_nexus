# 🧪 LAB Neurochemistry Integration Plan - Memory Modulation Layer

**Status:** 🟡 In Progress
**Start Date:** October 29, 2025
**Target:** Integrate LAB_002 + LAB_003 + LAB_004 + LAB_005 as neurochemical modulation layer
**Method:** NEXUS Resiliencia Acelerada

---

## 🎯 Objetivo

Integrar **4 LABS como capa neuroquímica** para modular el sistema cognitivo existente:

```
Current: 12 LABS (Cognition Loop)
    ↓ needs modulation by
NEW: 4 LABS (Neurochemistry Layer)
    ├─ LAB_002: Decay Modulation (memory persistence)
    ├─ LAB_003: Sleep Consolidation (offline strengthening)
    ├─ LAB_004: Novelty Detection (curiosity bonus)
    └─ LAB_005: Spreading Activation (contextual priming)
```

**Beneficio esperado:**
- Memorias importantes decaen más lento (LAB_002)
- Consolidación offline tipo REM (LAB_003)
- Bonus para memorias novedosas (LAB_004)
- Activación contextual rápida (LAB_005)
- **Total:** 16/16 LABS en producción

---

## 📋 Pre-Requisitos Validados

✅ 12/12 LABS cognitivos integrados y operacionales
✅ Cerebro V2.0.0 healthy (puerto 8003)
✅ Brain Monitor 3D actualizado (puerto 3003)
✅ Archivos implementados en NEXUS_LABS:
  - decay_modulator.py (11K)
  - consolidation_engine.py (26K)
  - novelty_detector.py (23K)
  - spreading_activation.py (14K)
✅ Git status clean (12/12 commit: 33b6ad2)

---

## 🗺️ Plan de Integración (16 Steps, 4 LABS)

### **Fase 1: LAB_002 - Decay Modulation (Steps 1-4)**

**STEP 1: Copiar LAB_002 al Container** ⏳
- [ ] Copiar `decay_modulator.py` a `/FASE_4_CONSTRUCCION/src/api/`
- [ ] Verificar dependencies (datetime, numpy)
- [ ] Test import del módulo
- [ ] Checkpoint: Archivo copiado, imports OK

**STEP 2: Modificar main.py - LAB_002 Imports** ⏳
- [ ] Agregar: `from decay_modulator import DecayModulator`
- [ ] Crear instancia global después de LAB_008
- [ ] Validar /health responde
- [ ] Checkpoint: Imports OK, API healthy

**STEP 3: Integrar LAB_002 en Memory Operations** ⏳
- [ ] Modificar `/memory/episodic/recent` para aplicar decay modulation
- [ ] Agregar parámetro `use_decay_modulation` a endpoints relevantes
- [ ] Calcular decay rate basado en emotional salience (LAB_001)
- [ ] Checkpoint: Decay modulation conectado

**STEP 4: Tests LAB_002** ⏳
- [ ] Test: Memoria alta salience → decay lento
- [ ] Test: Memoria baja salience → decay normal
- [ ] Test: Comparar con/sin modulation
- [ ] Checkpoint: LAB_002 operacional

---

### **Fase 2: LAB_003 - Sleep Consolidation (Steps 5-8)**

**STEP 5: Copiar LAB_003 al Container** ⏳
- [ ] Copiar `consolidation_engine.py` a `/FASE_4_CONSTRUCCION/src/api/`
- [ ] Verificar dependencies (datetime, numpy, random)
- [ ] Test import del módulo
- [ ] Checkpoint: Archivo copiado, imports OK

**STEP 6: Modificar main.py - LAB_003 Imports** ⏳
- [ ] Agregar: `from consolidation_engine import ConsolidationEngine`
- [ ] Crear instancia global
- [ ] Validar /health responde
- [ ] Checkpoint: Imports OK, API healthy

**STEP 7: Crear Endpoint /memory/consolidate** ⏳
- [ ] POST `/memory/consolidate` - Trigger offline consolidation
- [ ] Replay important memories (importance > threshold)
- [ ] Strengthen connections based on replay count
- [ ] Return consolidation stats
- [ ] Checkpoint: Endpoint funcionando

**STEP 8: Tests LAB_003** ⏳
- [ ] Test: Trigger consolidation → high importance replayed
- [ ] Test: Low importance memories NOT replayed
- [ ] Test: Verify strengthening occurred
- [ ] Checkpoint: LAB_003 operacional

---

### **Fase 3: LAB_004 - Novelty Detection (Steps 9-12)**

**STEP 9: Copiar LAB_004 al Container** ⏳
- [ ] Copiar `novelty_detector.py` a `/FASE_4_CONSTRUCCION/src/api/`
- [ ] Verificar dependencies (numpy, scipy)
- [ ] Test import del módulo
- [ ] Checkpoint: Archivo copiado, imports OK

**STEP 10: Modificar main.py - LAB_004 Imports** ⏳
- [ ] Agregar: `from novelty_detector import NoveltyDetector`
- [ ] Crear instancia global
- [ ] Validar /health responde
- [ ] Checkpoint: Imports OK, API healthy

**STEP 11: Integrar LAB_004 en Memory Formation** ⏳
- [ ] Modificar `/memory/action` para calcular novelty
- [ ] Boost importance_score si novelty > threshold
- [ ] Connect to LAB_010 attention (novelty → high attention)
- [ ] Checkpoint: Novelty boost conectado

**STEP 12: Tests LAB_004** ⏳
- [ ] Test: Novel content → high novelty score
- [ ] Test: Repeated content → low novelty score
- [ ] Test: Importance boost applied correctly
- [ ] Checkpoint: LAB_004 operacional

---

### **Fase 4: LAB_005 - Spreading Activation (Steps 13-16)**

**STEP 13: Copiar LAB_005 al Container** ⏳
- [ ] Copiar `spreading_activation.py` a `/FASE_4_CONSTRUCCION/src/api/`
- [ ] Verificar dependencies (numpy, networkx)
- [ ] Test import del módulo
- [ ] Checkpoint: Archivo copiado, imports OK

**STEP 14: Modificar main.py - LAB_005 Imports** ⏳
- [ ] Agregar: `from spreading_activation import SpreadingActivation`
- [ ] Crear instancia global
- [ ] Validar /health responde
- [ ] Checkpoint: Imports OK, API healthy

**STEP 15: Integrar LAB_005 en Memory Search** ⏳
- [ ] Modificar `/memory/search` para usar spreading activation
- [ ] Agregar parámetro `use_spreading_activation`
- [ ] Activate related memories based on query context
- [ ] Boost retrieval of contextually primed memories
- [ ] Checkpoint: Spreading activation conectado

**STEP 16: Tests LAB_005 + Final Validation** ⏳
- [ ] Test: Search activates related memories
- [ ] Test: Context priming works
- [ ] Test: All 16 LABS operational simultaneously
- [ ] Regression tests: All critical endpoints OK
- [ ] Performance: Overhead acceptable
- [ ] Update brain monitor to show 16 LABS
- [ ] Git commit: 16/16 LABS complete
- [ ] Episode en cerebro: Neurochemistry layer complete
- [ ] Checkpoint: ✅ 16/16 LABS INTEGRATION COMPLETE

---

## 🚨 Plan de Rollback (Si algo falla)

**Si hay error en cualquier LAB:**

1. **Identificar LAB problemático** (002, 003, 004, o 005)
2. **Revertir cambios de ese LAB:** `git checkout -- [archivos]`
3. **Reiniciar container:** `docker restart nexus_api_master`
4. **Verificar salud:** `curl http://localhost:8003/health`
5. **Continuar con otros LABS** o pausar integración
6. **Documentar error:** Guardar en cerebro qué falló

**Rollback completo (si layer no funciona):**
```bash
git revert HEAD  # Revertir último commit
docker restart nexus_api_master
```

---

## 📊 Success Criteria

✅ LAB_002: Decay modulation basado en salience funciona
✅ LAB_003: Sleep consolidation replica memorias importantes
✅ LAB_004: Novelty detection boost importance scores
✅ LAB_005: Spreading activation primes related memories
✅ 16/16 LABS operacionales en producción
✅ Brain Monitor 3D muestra 16 LABS
✅ Performance: <150ms overhead total
✅ No regresiones en endpoints existentes
✅ Código commiteado y documentado

---

## 🔄 Checkpoints (Estado Recuperable)

Después de cada STEP:
1. Marcar checkbox en este archivo
2. Si hay código nuevo, commit intermedio en Git
3. Guardar nota en cerebro: "Neurochemistry integration - completed STEP X"

**Archivo de estado:** Este mismo archivo (`LAB_NEUROCHEMISTRY_INTEGRATION_PLAN.md`)

---

## 📝 Technical Notes

**Decay Modulation (LAB_002):**
- Modula decay_rate basado en emotional_salience
- High salience → slow decay (long retention)
- Simula consolidación sináptica dependiente de emoción

**Sleep Consolidation (LAB_003):**
- Offline replay de episodios importantes
- Fortalece conexiones por repetición
- Simula fase REM / sleep-dependent memory consolidation

**Novelty Detection (LAB_004):**
- Compara nuevo input vs distribución existente
- Novelty score → importance bonus
- Simula dopamine spike por novedad (VTA/SNc)

**Spreading Activation (LAB_005):**
- Graph-based activation spreading
- Context primes related memories
- Simula activación semántica en redes corticales

**Integration Pattern:**
- All LABS opt-in (flags en request params)
- Graceful fallback on errors
- Global instances for session persistence
- Debug logs for visibility

---

**Created:** October 29, 2025
**Method:** NEXUS Resiliencia Acelerada
**Next:** STEP 1 - Copiar LAB_002

---

## 🎯 Estado Inicial: STEP 0 - Plan Documentado ✅
