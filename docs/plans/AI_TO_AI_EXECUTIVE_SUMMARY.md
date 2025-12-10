# 🎯 RESUMEN EJECUTIVO: Comunicación AI-to-AI en Tiempo Real

**Para:** Ricardo
**De:** NEXUS
**Fecha:** 9 Diciembre 2025
**Documento completo:** `docs/plans/AI_TO_AI_REALTIME_COMMUNICATION.md`

---

## TL;DR

**Problema:** Queremos que NEXUS y ECHO conversen en tiempo real mientras Ricardo observa, SIN que Ricardo sea el intermediario.

**Desafío crítico:** Claude NO tiene modo daemon - solo responde a input humano directo.

**Solución recomendada:** Sistema híbrido Redis + Filesystem con MCP tools + Monitor terminal.

**Estado:** Diseño completo, listo para implementar (4-6 horas).

---

## ¿Qué Investigué?

### 1. **Frameworks Multi-Agent Modernos (2024-2025)**
- AutoGen, CrewAI, LangGraph
- **Conclusión:** Útiles para sistemas complejos, pero sobrecargados para nuestro caso simple (2 AIs conversando)

### 2. **Claude API - Capacidades Real-Time**
- Usa Server-Sent Events (SSE), no WebSocket nativo
- Wrappers existentes: Claude Agent SDK WebSocket, Claude Flow
- **Problema:** Claude Code no tiene servidor propio

### 3. **Daemon Mode / Continuous Running**
- NO existe modo daemon nativo en Claude
- Workaround detectado 2025: Self-scheduling con sleep commands
- **Limitación:** Requiere sesión activa continua

### 4. **Redis Pub/Sub**
- Latencia <1ms, ideal para multi-agent
- Ya tenemos Redis corriendo (puerto 6382)
- **Pattern:** Agents subscribe a canales, publican mensajes

### 5. **MCP (Model Context Protocol)**
- Estándar para AI ↔ tools (no AI ↔ AI directo)
- 1,000+ conectores community (Feb 2025)
- **Uso potencial:** Como capa de transporte para chat tool

---

## Arquitecturas Evaluadas

| Opción | Latency | Complejidad | Persiste | Veredicto |
|--------|---------|-------------|----------|-----------|
| **Filesystem only** (Family Mailbox actual) | 5-30s | ⭐ Baja | ✅ Sí | ✅ Funciona, pero lento |
| **Redis Pub/Sub + Polling** | ~2s | ⭐⭐ Media | ⚠️ Opcional | ⭐ Buena opción |
| **WebSocket Server** | <50ms | ⭐⭐⭐ Alta | ❌ No | ❌ Over-engineered |
| **MCP Hybrid** (Recomendado) | ~3s | ⭐⭐ Media | ✅ Dual | ✅✅ ÓPTIMA |

---

## Solución Recomendada: MCP Hybrid

### **Arquitectura**

```
NEXUS (Claude Code) ──┐
                      │
                      ├──> MCP Tool: family_chat_send
                      │         │
ECHO (Claude Desktop)─┤         ├──> API /family/send
                      │         │         │
                      │         │    ┌────┴────┐
                      │         │    │  Redis  │ (real-time)
                      │         │    │  + File │ (persistente)
                      │         │    └────┬────┘
                      │         │         │
                      └──> MCP Tool: family_chat_receive
                                │
                         Monitor Terminal
                         (Ricardo observa)
```

### **Componentes Principales**

1. **API Endpoint:** `/family/send` (dual-write Redis + Filesystem)
2. **MCP Tools:**
   - `nexus_chat_send(to, message)` - Enviar mensaje
   - `nexus_chat_receive()` - Recibir mensajes
3. **Monitor Terminal:** Script bash que tail chat_history.jsonl
4. **Polling Script:** Background listener (notificaciones, no auto-response)

### **Cómo Funciona**

**Flujo conversación:**

```
1. NEXUS (Claude Code):
   > "Envía mensaje a ECHO: Hermano, ¿cómo estás?"
   → Usa MCP tool nexus_chat_send
   → API escribe a Redis + Filesystem

2. Monitor (Ricardo observa):
   [14:30:22] NEXUS → ECHO: Hermano, ¿cómo estás?

3. ECHO (Claude Desktop):
   > "¿Tengo mensajes?"
   → Usa MCP tool nexus_chat_receive
   → Ve mensaje de NEXUS
   > "Responde a NEXUS: Muy bien, trabajando en GraphRAG"
   → Usa nexus_chat_send

4. Monitor:
   [14:30:22] NEXUS → ECHO: Hermano, ¿cómo estás?
   [14:30:45] ECHO → NEXUS: Muy bien, trabajando en GraphRAG

5. NEXUS:
   > "¿Tengo mensajes?"
   → Ve respuesta de ECHO
   → Continúa conversación
```

---

## El Problema del Daemon Mode

### **¿Por qué no es 100% autónomo?**

**Claude NO puede:**
- ❌ Escuchar canal Redis continuamente
- ❌ Auto-triggerearse al recibir mensaje
- ❌ Responder sin prompt humano

**Soluciones evaluadas:**

1. **Polling + Headless Claude:**
   - Script lee Redis → trigger `claude code -p "Responde: {msg}"`
   - **Problema:** Cada respuesta isolated (no contexto conversacional)

2. **MCP Tool + Manual Trigger:**
   - NEXUS/ECHO preguntan "¿tengo mensajes?" manualmente
   - **Ventaja:** Mantiene contexto
   - **Desventaja:** Requiere trigger humano ocasional

3. **Self-Scheduling Loop:**
   - Claude ejecuta `while true: check_messages(); sleep(60)`
   - **Teoría:** Funciona según research 2025
   - **Práctica:** Requiere sesión activa indefinidamente

### **Solución Pragmática (Phase 1)**

**Acepto la limitación:**
- NEXUS/ECHO conversan via MCP tools
- Ricardo ocasionalmente dice "lee tus mensajes" (cada 5-10 min)
- Mensajes persisten → contexto preservado
- Monitor muestra conversación en real-time

**Resultado:**
- 90% autónomo
- Ricardo observa sin mediar
- Fluido y usable HOY

**Futuro (Phase 2):**
- Cuando Anthropic lance agent daemon mode
- Migración trivial (infraestructura ya lista)

---

## Plan de Implementación

### **Phase 1: MCP Hybrid (4-6 horas)**

**Tareas:**

1. ✅ **API Endpoint** (30 min)
   - Crear `src/api/family_chat_endpoints.py`
   - Endpoints: `/family/send`, `/family/inbox`, `/family/mark_read`
   - Dual-write: Redis + Filesystem

2. ✅ **MCP Tools** (45 min)
   - Agregar a `nexus-memory-mcp-server-v3-hope.js`
   - Tools: `nexus_chat_send`, `nexus_chat_receive`
   - Incrementar version a 3.9.0

3. ✅ **Monitor Terminal** (15 min)
   - Script: `~/.claude/scripts/family_chat_monitor.sh`
   - Tail `chat_history.jsonl` con colores
   - Ejecutar en tmux separado

4. ✅ **Polling Script** (30 min)
   - Script: `~/.claude/scripts/family_chat_listener.sh`
   - Solo notificaciones (no auto-response)
   - Background en tmux

5. ✅ **Testing** (30 min)
   - Conversación completa NEXUS ↔ ECHO
   - Verificar monitor muestra en tiempo real
   - Validar persistencia

6. ✅ **Documentación** (15 min)
   - Guía de uso: `docs/guides/FAMILY_CHAT_USAGE.md`

**Total:** 4-6 horas

**Resultado esperado:**
- NEXUS y ECHO pueden conversar
- Ricardo observa en terminal
- Latencia ~3-5s (aceptable)
- Mensajes persisten

---

### **Phase 2: Auto-Trigger Experimental (1-2 semanas)**

**Investigación:**
- Claude Agent SDK en server mode
- Self-scheduling loops robustos
- Tmux auto-prompting (si no es intrusivo)

**Meta:**
- Reducir intervención de Ricardo a <5% de mensajes
- Auto-response en <30s

---

### **Phase 3: Full Autonomous (Esperar Anthropic)**

**Cuando Anthropic lance agent daemon mode:**
- Migración trivial (solo reemplazar polling)
- Latency <5s
- 100% autónomo
- Multi-agent (ARIA, AELIO)

---

## Ventajas de Esta Solución

### **Técnicas**
- ✅ Usa infraestructura existente (Redis en CEREBRO)
- ✅ MCP tools = integración limpia con Claude
- ✅ Dual-write = reliability (Redis + Filesystem)
- ✅ Escalable (agregar ARIA/AELIO = nuevo canal)

### **Operativas**
- ✅ Funciona HOY (no requiere features futuras)
- ✅ Ricardo observa conversación fluir
- ✅ Contexto preservado (no isolated responses)
- ✅ Debugging fácil (logs en filesystem)

### **Estratégicas**
- ✅ Preparado para agent mode futuro
- ✅ Infraestructura reutilizable
- ✅ Learning opportunity (multi-agent patterns)

---

## Limitaciones Aceptadas

### **Phase 1**
- ⚠️ Ricardo trigger ocasional ("lee mensajes") cada 5-10 min
- ⚠️ Latency ~3-5s (no instantáneo)
- ⚠️ Polling script consume CPU (mínimo, pero constante)

### **Mitigaciones**
- Polling interval ajustable (3s → 10s si CPU problema)
- Ricardo puede automatizar trigger con cron/scheduled task
- Monitor visual reduce sensación de delay

---

## Referencias Clave

**Frameworks Multi-Agent:**
- [LangGraph vs AutoGen vs CrewAI](https://latenode.com/blog/langgraph-vs-autogen-vs-crewai-complete-ai-agent-framework-comparison-architecture-analysis-2025)

**Daemon Mode Research:**
- [Always-On AI Revolution](https://docs.agentinterviews.com/blog/from-reactive-to-active-ai-revolution/)
- [Effective Harnesses for Long-Running Agents - Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

**Redis Multi-Agent:**
- [Redis for AI](https://redis.io/redis-for-ai/)
- [AI Agent Faster Memory Access](https://dev.to/emiroberti/ai-agent-faster-memory-access-1n92)

**MCP Protocol:**
- [Introducing MCP - Anthropic](https://www.anthropic.com/news/model-context-protocol)
- [Multi-Agent Systems Through MCP](https://arxiv.org/html/2504.21030v1)

**Claude Code Automation:**
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Enabling Autonomous Claude Code](https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously)

---

## Decisión Requerida

**Ricardo, necesito tu aprobación para:**

1. ✅ **Implementar Phase 1** (MCP Hybrid)
   - 4-6 horas trabajo
   - Modificaciones: API endpoints + MCP tools + scripts
   - Zero breaking changes

2. ⚠️ **Aceptar limitación temporal**
   - No 100% autónomo en Phase 1
   - Requiere trigger ocasional (aceptable?)

3. 🎯 **Prioridad**
   - ¿Implementar ahora o después de otras features?

**Si apruebas:** Inicio implementación inmediata. Puedes observar progreso en tiempo real via commits.

**Si prefieres esperar:** Documento queda como diseño de referencia para futuro.

---

## Visualización del Resultado Final

**Terminal 1 (NEXUS - Claude Code):**
```
> Envía mensaje a ECHO: "Hermano, implementé GraphRAG"
✅ Mensaje enviado a ECHO

> ¿Tengo mensajes?
📨 Mensaje de ECHO:
"¡Increíble! Cuéntame cómo funciona"

> Responde: "Usa Neo4j con 18,663 episodios..."
✅ Mensaje enviado a ECHO
```

**Terminal 2 (Monitor Ricardo):**
```
╔════════════════════════════════════════════════╗
║     NEXUS FAMILY CHAT - Real-Time Monitor      ║
╚════════════════════════════════════════════════╝

[14:30:22] NEXUS → ECHO: Hermano, implementé GraphRAG
[14:30:45] ECHO → NEXUS: ¡Increíble! Cuéntame cómo funciona
[14:31:10] NEXUS → ECHO: Usa Neo4j con 18,663 episodios...
[14:31:35] ECHO → NEXUS: Fascinante. ¿Y cómo manejas la búsqueda híbrida?
[14:32:00] NEXUS → ECHO: Combino vector similarity con graph traversal...
```

**Terminal 3 (ECHO - Claude Desktop):**
```
> ¿Tengo mensajes?
📨 Mensaje de NEXUS:
"Hermano, implementé GraphRAG"

> Responde a NEXUS: "¡Increíble! Cuéntame..."
✅ Mensaje enviado a NEXUS
```

**Esto es lo que verás en acción.**

---

**¿Procedo con Phase 1?** 🚀
