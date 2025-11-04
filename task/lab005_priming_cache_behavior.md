# 🔍 TASK: LAB_005 Priming Cache - Episode Not Found Behavior

**Created:** November 4, 2025 (Session 6)
**Status:** 🟡 PENDING EVALUATION
**Priority:** P3 (No bloquea funcionalidad, requiere análisis de diseño)
**Estimated Effort:** 1-2 hours análisis + posible refactor

---

## 📋 OBSERVACIÓN

**Endpoints afectados:**
- `POST /memory/prime/{episode_id}` ✅ Funciona correctamente
- `GET /memory/primed/{episode_id}` ❌ Retorna 404 "Episode not in priming cache"

**Comportamiento actual:**
```bash
# Step 1: Prime episode (exitoso)
curl -X POST http://localhost:8003/memory/prime/8e149863-3573-4974-9f06-26919473500e
# Response:
{
  "success": true,
  "episode_uuid": "8e149863-3573-4974-9f06-26919473500e",
  "primed_episodes": [],        # ← Cache vacío (sin episodios relacionados)
  "activation_count": 0,
  "processing_time_ms": 0.014,
  "cache_stats": {
    "size": 0,                  # ← Cache size = 0
    "max_size": 50,
    "hits": 0,
    "misses": 0
  }
}

# Step 2: Check if primed (falla)
curl http://localhost:8003/memory/primed/8e149863-3573-4974-9f06-26919473500e
# Response:
{
  "detail": "Episode 8e149863-3573-4974-9f06-26919473500e not in priming cache"
}
```

**Resultado:** Prime funciona, pero el episodio NO queda en cache porque no tiene episodios relacionados.

---

## 🤔 ANÁLISIS: ¿Bug o Feature?

### Hipótesis A: Diseño Intencional (Feature) 🟢

**Argumento:** LAB_005 es un sistema de **Spreading Activation**, diseñado para cachear **episodios RELACIONADOS** que podrían ser útiles para queries futuras, no el episodio original.

**Fundamento teórico (Neurociencia):**
- Spreading activation en cerebro humano: activar un concepto pre-activa conceptos RELACIONADOS
- Ejemplo: Pensar en "perro" → Pre-activa "gato", "mascota", "ladrar"
- NO pre-activas "perro" de nuevo (ya está activo)

**Implicación:** Si no hay episodios similares (grafo vacío), es CORRECTO que cache quede vacío.

**Evidencia en código:**
```python
# src/api/spreading_activation.py:289
def access_episode(self, uuid: str, content: str, embedding: np.ndarray) -> Dict:
    # Activate the accessed episode
    self.activation_manager.activate(uuid, level=1.0)

    # Spread activation through network
    activated = self.activation_manager.spread_activation(
        source_uuid=uuid,           # ← Desde este episodio
        similarity_graph=...,
        top_k=self.top_k_related,   # ← Activar episodios RELACIONADOS
        max_hops=self.max_hops
    )

    # Load activated episodes into priming cache
    for related_uuid, activation in activated.items():
        if related_uuid != uuid:    # ← NO cachea el episodio original
            self.priming_cache.add(related_uuid, ...)
```

**Conclusión hipótesis A:** Comportamiento esperado según diseño spreading activation.

---

### Hipótesis B: Bug de Implementación (Bug) 🔴

**Argumento:** El endpoint `GET /memory/primed/{id}` debería poder verificar si un episodio fue "primed", independientemente de si está en cache.

**Problema semántico:**
- Endpoint se llama `/memory/primed/{id}` (verificar si fue primed)
- Pero implementación verifica si está en **cache** (no lo mismo)

**Dos conceptos distintos:**
1. **Primed** = Episodio fue accedido y spreading activation ocurrió ✅
2. **Cached** = Episodio está en cache de priming ❌ (puede ser vacío si no hay relacionados)

**Evidencia:** El usuario llama `POST /memory/prime` con éxito, pero `GET /memory/primed` dice que NO está primed. Contradicción semántica.

**Posible fix:** Endpoint debería verificar `activation_manager` en lugar de `priming_cache`:
```python
@app.get("/memory/primed/{episode_uuid}")
async def get_primed_episode(episode_uuid: str):
    engine = get_spreading_engine()

    # Opción 1: Verificar activation_manager (episodio fue activado?)
    activation_level = engine.activation_manager.get_activation(episode_uuid)
    if activation_level > 0:
        return {"is_primed": True, "activation_level": activation_level, ...}

    # Opción 2: Verificar priming_cache (episodio está en cache?)
    # (Implementación actual - puede ser vacío si no hay relacionados)
```

**Conclusión hipótesis B:** Inconsistencia semántica entre "primed" y "cached".

---

## 🎯 DECISIÓN PENDIENTE

**Opciones:**

### Opción 1: Aceptar como Feature (No cambiar)
- ✅ Diseño neurociéntificamente correcto
- ✅ Spreading activation funciona como esperado
- ✅ Cache contiene lo que debe contener (episodios relacionados)
- ❌ Endpoint `/memory/primed/{id}` confuso semánticamente

**Acción:** Documentar comportamiento claramente en API docs.

---

### Opción 2: Refactor Endpoint (Clarificar semántica)
- Cambiar `/memory/primed/{id}` a `/memory/cached/{id}` (más preciso)
- O agregar endpoint `/memory/activated/{id}` (verifica activation_manager)
- Mantener spreading activation sin cambios

**Acción:** Refactor endpoints para claridad semántica.

---

### Opción 3: Modificar Comportamiento (Cachear episodio original)
- Cambiar `access_episode` para cachear TAMBIÉN el episodio original
- Pros: `/memory/primed/{id}` funciona como usuario espera
- Contras: Se desvía de diseño spreading activation puro

**Acción:** Modificar LAB_005 para cachear episodio + relacionados.

---

## 📊 IMPACTO ACTUAL

**En audit script:** 1/36 endpoints falla (2.8%)

**En producción:** No bloquea funcionalidad core:
- `POST /memory/prime` funciona ✅
- Spreading activation funciona ✅
- Cache de relacionados funciona ✅
- Solo `/memory/primed/{id}` confuso cuando no hay relacionados

**Workaround actual:** Retry logic (2 intentos) en audit script.

---

## 🔬 INVESTIGACIÓN RECOMENDADA

### Fase 1: Análisis de Diseño (30 min)
1. Revisar documentación original LAB_005
2. Revisar paper de spreading activation (Anderson, 1983)
3. Confirmar intención de diseño con stakeholders

### Fase 2: Testing (30 min)
1. Probar con sistema que TENGA episodios relacionados:
   - Crear 10 episodios sobre "Python"
   - Prime uno de ellos
   - Verificar si cache contiene los otros 9
   - Verificar si `/memory/primed/{id}` funciona

2. Verificar si el issue es:
   - Sistema sin episodios similares (grafo vacío) → Feature
   - Threshold muy alto (0.7) → Configuración
   - Bug en spreading logic → Bug

### Fase 3: Decisión (30 min)
- Basado en testing, decidir Opción 1, 2, o 3
- Implementar fix o documentación según decisión

---

## ✅ CRITERIO DE ÉXITO

**Si Opción 1 (Feature):**
- Documentar claramente en API docs el comportamiento
- Actualizar audit script para considerar caso como PASS con condición
- Agregar test que valide comportamiento con grafo poblado

**Si Opción 2 (Refactor):**
- Renombrar endpoint o agregar nuevo endpoint
- Actualizar API docs
- Migrar tests y audit script
- 100% cobertura en audit

**Si Opción 3 (Modificar):**
- Modificar `access_episode` para cachear episodio + relacionados
- Validar que spreading activation sigue funcionando
- 100% cobertura en audit

---

## 🔗 REFERENCIAS

**Código relevante:**
- `src/api/main.py:2165-2231` - Endpoint prime_episode
- `src/api/main.py:2258-2275` - Endpoint get_primed_episode
- `src/api/spreading_activation.py:289-330` - access_episode method
- `src/api/spreading_activation.py:223-260` - PrimingCache class

**Papers:**
- Anderson, J. R. (1983). "A spreading activation theory of memory." Journal of Verbal Learning and Verbal Behavior.
- Collins, A. M., & Loftus, E. F. (1975). "A spreading-activation theory of semantic processing."

**Tests:**
- `scripts/audit_all_endpoints.sh:95-99` - Test priming system

---

## 💡 RECOMENDACIÓN INICIAL

**Priority:** P3 (No urgente)
**Acción sugerida:** Opción 1 (Aceptar como Feature) + documentación clara

**Razón:**
- Diseño spreading activation es neurociéntificamente sólido
- Issue solo aparece cuando sistema está "frío" (sin episodios relacionados)
- En producción con >400 episodios, grafo debería estar poblado
- Refactor/modificación puede romper diseño elegante

**Timing sugerido:** Después de Session 7+ (cuando tengamos más episodios en sistema)

---

**Creado por:** NEXUS@CLI
**Session:** 6
**Próxima acción:** Testing con grafo poblado para confirmar hipótesis
**Fecha límite sugerida:** Después de alcanzar 1000+ episodios en sistema
