# 🔍 AUDITORÍA MULTI-MODELO - INSTRUCCIONES

**Proyecto:** CEREBRO_MASTER_NEXUS_001
**Fecha Creación:** 14 Octubre 2025
**Propósito:** Validación cruzada arquitectura por 3 modelos externos

---

## 📋 WORKFLOW COMPLETO

### **PASO 1: Copiar Prompt (Ricardo)**

1. Abrir `PROMPT_AUDITORIA_EXTERNA.md`
2. Copiar TODO el contenido (desde "# AUDITORÍA ARQUITECTÓNICA" hasta el final)
3. Pegar en cada modelo:
   - **ChatGPT:** https://chat.openai.com/ (GPT-4 o superior)
   - **Grok:** https://x.com/i/grok (X.AI)
   - **Copilot:** GitHub Copilot Chat (VSCode o GitHub)

### **PASO 2: Guardar Respuestas (Ricardo)**

Para cada modelo:
1. Copiar TODA la respuesta completa
2. Abrir archivo correspondiente en `RESPUESTAS/`:
   - `01_CHATGPT_RESPONSE.md`
   - `02_GROK_RESPONSE.md`
   - `03_COPILOT_RESPONSE.md`
3. Pegar en sección "RESPUESTA COMPLETA"
4. Actualizar fecha consulta
5. Cambiar status de "⏳ PENDIENTE RESPUESTA" a "✅ RESPUESTA RECIBIDA"

### **PASO 3: Análisis Comparativo (NEXUS)**

Cuando tengas las 3 respuestas:
1. Avisarme: "Nexus, tengo las 3 respuestas listas"
2. Yo analizaré:
   - **Coincidencias:** Issues detectados por 2+ modelos = CRÍTICOS
   - **Divergencias:** Issues únicos = INVESTIGAR
   - **Consenso:** Si 3 aprueban = CONFIANZA ALTA
3. Crearé: `ANALISIS_COMPARATIVO.md` con:
   - Issues por prioridad (basado en coincidencias)
   - Recomendaciones únicas valiosas
   - Plan de acción integrado

### **PASO 4: Actualizar Arquitectura (NEXUS + Ricardo)**

Si encontramos blind spots críticos:
1. Actualizar `CEREBRO_MASTER_ARCHITECTURE.md`
2. Documentar cambios en `CHANGELOG_ARQUITECTURA.md`
3. Sincronizar al cerebro (puerto 8002)

---

## 📁 ESTRUCTURA DE CARPETA

```
AUDITORIA_MULTI_MODELO/
│
├── README.md                           # ← Estás aquí
├── PROMPT_AUDITORIA_EXTERNA.md         # ← Copiar y pegar en modelos
│
├── RESPUESTAS/
│   ├── 01_CHATGPT_RESPONSE.md          # ← Guardar respuesta ChatGPT aquí
│   ├── 02_GROK_RESPONSE.md             # ← Guardar respuesta Grok aquí
│   └── 03_COPILOT_RESPONSE.md          # ← Guardar respuesta Copilot aquí
│
└── ANALISIS_COMPARATIVO.md             # ← NEXUS creará esto después
```

---

## 🎯 QUÉ ESPERAMOS ENCONTRAR

**Best Case:**
- 3 modelos aprueban arquitectura = Alta confianza
- Solo issues menores o ya conocidos
- Proceder a FASE 4 (Construcción) directamente

**Likely Case:**
- 2-3 blind spots críticos detectados
- Algunas recomendaciones de mejora
- Actualizar arquitectura antes de construir

**Worst Case:**
- Múltiples issues críticos coincidentes
- Anti-patterns fundamentales
- Rediseñar partes de la arquitectura

---

## 📊 MÉTRICAS DE EVALUACIÓN

Después de análisis comparativo, evaluaremos:

| Métrica | Descripción | Acción |
|---------|-------------|--------|
| **Coincidencias 3/3** | Todos detectan mismo issue | CRÍTICO - Arreglar antes de construir |
| **Coincidencias 2/3** | Dos modelos coinciden | ALTO - Investigar y probablemente arreglar |
| **Único valioso** | Solo 1 modelo, pero argumento sólido | MEDIO - Evaluar caso por caso |
| **Único dudoso** | Solo 1 modelo, argumento débil | BAJO - Documentar pero no bloquea |
| **Aprobación unánime** | 3 modelos aprueban decisión | CONFIANZA ALTA - Continuar |

---

## ⏱️ TIEMPO ESTIMADO

- **Ricardo consultas:** 30 minutos (10 min por modelo)
- **NEXUS análisis:** 1 hora (comparación + recomendaciones)
- **Updates arquitectura:** 1-2 horas (si hay cambios críticos)

**Total:** 2.5 - 3.5 horas

---

## 🚨 IMPORTANTE

1. **NO editar PROMPT_AUDITORIA_EXTERNA.md** - ya está optimizado
2. **Copiar prompt COMPLETO** en cada modelo (no resumir)
3. **Guardar respuestas COMPLETAS** (no solo resumen)
4. **Avisar a NEXUS** cuando tengas las 3 respuestas

---

## 📞 SIGUIENTE PASO

**Ricardo:** Abre `PROMPT_AUDITORIA_EXTERNA.md` y empieza las consultas cuando estés listo.

**Avisarme cuando:**
- Tengas 1 respuesta lista (para verificar que guardaste bien)
- Tengas las 3 respuestas completas (para análisis comparativo)
- Encuentres algún problema en el proceso

---

**🎯 AUDITORÍA MULTI-MODELO LISTA PARA EJECUTAR** ✨

**Creado por:** NEXUS Terminal
**Fecha:** 14 Octubre 2025
