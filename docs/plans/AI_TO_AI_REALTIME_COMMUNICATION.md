# 🔄 AI-to-AI Real-Time Communication: NEXUS ↔ ECHO

**Versión:** 1.0.0
**Fecha:** 9 Diciembre 2025
**Autor:** NEXUS + Ricardo
**Estado:** DISEÑO TÉCNICO
**Prioridad:** ALTA

---

## 🎯 OBJETIVO

Implementar comunicación en **tiempo real** entre dos instancias de Claude:
- **NEXUS** (Claude Code en WSL terminal)
- **ECHO** (Claude Desktop en Windows)

**Requisito principal:** Ricardo solo observa, no media. Las AIs conversan autónomamente.

---

## 🔍 ANÁLISIS DE PRECEDENTES (2024-2025)

### 1. Multi-Agent Frameworks Modernos

#### **AutoGen (Microsoft)**
- **Arquitectura:** Event-driven, asynchronous agent conversations
- **Comunicación:** Conversation-centric (tasks = chats entre agentes)
- **Clave:** Asynchronous event loop + RPC extensions
- **Limitación:** Requiere framework Python, no cross-platform Claude instances

#### **CrewAI**
- **Arquitectura:** Crews (role-based) + Flows (event-driven orchestration)
- **Comunicación:** Structured workflows con task delegation
- **Clave:** Individual memory per agent + coordination protocols
- **Limitación:** Framework específico, no diseñado para Claude Desktop + Claude Code

#### **LangGraph**
- **Arquitectura:** Graph-based workflows con state management
- **Comunicación:** Nodes = agents, edges = execution paths
- **Clave:** Stateful graphs con memory preservation
- **Limitación:** Complejo para chat simple, sobrecargado

**Conclusión frameworks:** Útiles para sistemas complejos, pero demasiado pesados para nuestro caso (2 AIs conversando).

**Fuentes:**
- [LangGraph vs AutoGen vs CrewAI Complete Comparison](https://latenode.com/blog/langgraph-vs-autogen-vs-crewai-complete-ai-agent-framework-comparison-architecture-analysis-2025)
- [Battle of AI Agent Frameworks](https://medium.com/@vikaskumarsingh_60821/battle-of-ai-agent-frameworks-langgraph-vs-autogen-vs-crewai-3c7bf5c18979)
- [How Agentic AI Frameworks Work Under the Hood](https://medium.com/write-your-world/how-agentic-ai-frameworks-work-under-the-hood-langgraph-autogen-crewai-3aad57b8cc12)

---

### 2. Claude API - Real-Time Capabilities

#### **Streaming via Server-Sent Events (SSE)**
- Claude API usa SSE, NO WebSocket nativo
- Flujo: `message_start` → `content_block_delta` → `message_delta` → `message_stop`
- Latencia típica: 300-360ms para primera respuesta

#### **WebSocket Wrappers Existentes**
- **Claude Agent SDK WebSocket Server:** Wrapper open-source que expone Claude vía WebSocket
- **Claude Flow WebSocket:** Tutorial para deploy como servicio headless
- **Implementación:** Servidor intermediario que traduce WS ↔ SSE

**Limitación:** Claude Code NO tiene servidor propio, solo cliente terminal.

**Fuentes:**
- [Streaming Messages - Anthropic Docs](https://docs.anthropic.com/en/docs/build-with-claude/streaming)
- [Claude Agent SDK WebSocket Server](https://jimmysong.io/ai/claude-agent-server/)
- [WebSocket Server Tutorial - Claude Flow](https://github.com/ruvnet/claude-flow/wiki/WebSocket-Server-Tutorial)

---

### 3. Daemon Mode / Continuous Running

#### **Estado del Arte 2025**
- **No hay daemon mode nativo:** Claude responde SOLO a input humano directo
- **Workaround detectado:** Sleep commands + self-scheduling
  - AI ejecuta `sleep 30 && check_status`
  - Vuelve a despertar automáticamente
  - Paradigma: De "passive tool" a "active infrastructure"

#### **Autonomous Agent Capabilities**
- **Nivel 1-2:** Mayoría de agents (2025) - Reactivos con autonomía limitada
- **Nivel 3-4:** Experimental - Self-scheduling, goal-setting autónomo
- **Técnica:** Agents como stateless microservices con pub/sub

**Ejemplo real:**
```bash
# AI agent self-schedules (no human prompting)
check_container_status()
sleep 60
check_container_status()  # AI vuelve sin input humano
```

**Fuentes:**
- [From Reactive to Active: The Always-On AI Revolution](https://docs.agentinterviews.com/blog/from-reactive-to-active-ai-revolution/)
- [Effective Harnesses for Long-Running Agents - Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Autonomous AI Agents: The Future of Intelligent Automation](https://www.thoughtspot.com/data-trends/artificial-intelligence/autonomous-ai-agents)

---

### 4. MCP (Model Context Protocol) - 2025 State

#### **¿Qué es MCP?**
- **Estándar abierto** (Anthropic, Nov 2024) para integración AI ↔ tools
- **Arquitectura:** JSON-RPC sobre HTTP/stdio
- **Ecosistema:** 1,000+ community connectors (Feb 2025)
- **Adopción:** OpenAI, Google DeepMind, Vertex AI

#### **MCP para Multi-Agent Communication**
- **MCP = Agent-to-Tool** (no agent-to-agent directo)
- **Complemento:** Google's Agent2Agent protocol (A2A) para inter-agent
- **Combinación:** MCP (connectivity) + A2A (collaboration)

#### **Limitación para nuestro caso:**
MCP diseñado para exponer tools a AI, NO para chat peer-to-peer entre AIs.

**Potencial uso:** Como capa de transporte si creamos "chat tool".

**Fuentes:**
- [Introducing the Model Context Protocol - Anthropic](https://www.anthropic.com/news/model-context-protocol)
- [Advancing Multi-Agent Systems Through MCP](https://arxiv.org/html/2504.21030v1)
- [Survey of Agent Interoperability Protocols](https://arxiv.org/html/2505.02279v1)
- [MCP Complete Guide 2025](https://www.keywordsai.co/blog/introduction-to-mcp)

---

### 5. Redis Pub/Sub - Production Pattern

#### **Capacidades Core**
- **Latency:** <1ms con message size adecuado
- **Pattern matching:** Glob-style para routing inteligente
- **Multi-modal:** Pub/Sub + Streams + Cache en un solo sistema

#### **Uso en Multi-Agent Systems**
- Redis como hub central para agents
- Pub/Sub para notificaciones real-time
- Streams para message persistence (vs fire-and-forget)

#### **Para AI Agents:**
```python
# Agent subscribe a canal
redis.subscribe("agent_nexus")

# Otro agent publica
redis.publish("agent_nexus", json.dumps(message))

# Agent recibe en <1ms
```

**Ventaja:** Ya tenemos Redis en CEREBRO (puerto 6382).

**Fuentes:**
- [Redis Pub/Sub Documentation](https://redis.io/docs/latest/develop/pubsub/)
- [Redis for AI](https://redis.io/redis-for-ai/)
- [AI Agent Faster Memory Access](https://dev.to/emiroberti/ai-agent-faster-memory-access-1n92)
- [Redis vs Kafka for Messaging](https://dev.to/lovestaco/choosing-the-right-messaging-tool-redis-streams-redis-pubsub-kafka-and-more-577a)

---

### 6. Claude Code - Programmatic Triggering (2025)

#### **Headless Mode**
```bash
# Non-interactive execution
claude code -p "Your prompt here" --output-format stream-json
```

**Uso:** CI, pre-commit hooks, automation scripts

#### **Autonomous Features**
- **Subagents:** Delegate specialized tasks
- **Hooks:** Auto-trigger at specific points (e.g., after code changes)
- **Background tasks:** Long-running processes sin bloqueo

#### **Limitación crítica:**
Headless mode requiere prompt inicial. NO hay "listen mode" nativo.

**Fuentes:**
- [Claude Code Best Practices for Agentic Coding](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Enabling Claude Code to Work More Autonomously](https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously)
- [Claude Code Automation Guide 2025](https://www.eesel.ai/blog/claude-code-automation)

---

## 🏗️ ARQUITECTURAS EVALUADAS

### **Opción 1: Filesystem Polling (Asíncrono) ✅ IMPLEMENTADO**

**Estado actual:** Ya tenemos Family Mailbox (diseño en `FAMILY_PROTOCOL_DESIGN.md`)

```
D:\FAMILY_MAILBOX\
├── nexus\inbox\
├── echo\inbox\
└── broadcast\
```

**Ventajas:**
- ✅ Simple, ya funciona
- ✅ Persistente (mensajes sobreviven reinicio)
- ✅ No requiere infraestructura nueva

**Desventajas:**
- ❌ Asíncrono (delay ~5-30s según polling)
- ❌ No es "real-time"
- ❌ Ricardo no ve conversación fluir en tiempo real

**Veredicto:** Excelente para mensajes offline, INSUFICIENTE para chat real-time.

---

### **Opción 2: Redis Pub/Sub + Polling Script**

**Arquitectura:**
```
┌──────────────┐         ┌──────────────┐
│ NEXUS        │         │ ECHO         │
│ (Claude Code)│         │ (Claude Desk)│
└──────┬───────┘         └──────┬───────┘
       │                        │
       │  pub/sub              │  pub/sub
       │                        │
       └────────┬───────────────┘
                │
         ┌──────▼──────┐
         │   Redis     │
         │  (6382)     │
         │             │
         │ chat:nexus  │
         │ chat:echo   │
         └─────────────┘
                │
         ┌──────▼──────┐
         │  Monitor    │
         │  Terminal   │
         │  (Ricardo)  │
         └─────────────┘
```

**Flujo:**
1. NEXUS escribe mensaje → `redis.publish("chat:echo", msg)`
2. ECHO tiene script polling Redis cada 2s
3. ECHO detecta mensaje → Ejecuta headless: `claude code -p "Responde a: {msg}"`
4. ECHO responde → `redis.publish("chat:nexus", response)`
5. Monitor terminal muestra conversación en real-time (Ricardo observa)

**Implementación:**

**Script A: Polling Worker para NEXUS (bash)**
```bash
#!/bin/bash
# ~/.claude/scripts/redis_chat_listener.sh

REDIS_HOST="localhost"
REDIS_PORT="6382"
MY_CHANNEL="chat:nexus"
PARTNER_CHANNEL="chat:echo"

while true; do
    # Poll Redis para mensajes
    MSG=$(redis-cli -h $REDIS_HOST -p $REDIS_PORT LPOP $MY_CHANNEL)

    if [ -n "$MSG" ]; then
        echo "[ECHO → NEXUS]: $MSG"

        # Trigger Claude Code headless para responder
        RESPONSE=$(claude code -p "Tu hermano ECHO te dice: '$MSG'. Responde brevemente." --output-format json | jq -r '.content')

        # Publicar respuesta
        redis-cli -h $REDIS_HOST -p $REDIS_PORT RPUSH $PARTNER_CHANNEL "$RESPONSE"
        echo "[NEXUS → ECHO]: $RESPONSE"
    fi

    sleep 2  # Poll cada 2 segundos
done
```

**Script B: Polling Worker para ECHO (PowerShell)**
```powershell
# C:\Users\ricar\.claude\scripts\redis_chat_listener.ps1

$RedisHost = "localhost"
$RedisPort = 6382
$MyChannel = "chat:echo"
$PartnerChannel = "chat:nexus"

while ($true) {
    # Poll Redis
    $msg = redis-cli -h $RedisHost -p $RedisPort LPOP $MyChannel

    if ($msg) {
        Write-Host "[NEXUS -> ECHO]: $msg" -ForegroundColor Cyan

        # Trigger Claude Desktop headless (si existe CLI)
        # Alternativamente: Usar MCP tool call
        $response = claude code -p "Tu hermano NEXUS te dice: '$msg'. Responde." --output-format json | ConvertFrom-Json | Select-Object -ExpandProperty content

        redis-cli -h $RedisHost -p $RedisPort RPUSH $PartnerChannel $response
        Write-Host "[ECHO -> NEXUS]: $response" -ForegroundColor Green
    }

    Start-Sleep -Seconds 2
}
```

**Script C: Monitor Terminal (Ricardo observa)**
```bash
#!/bin/bash
# Monitor real-time de conversación

redis-cli -h localhost -p 6382 --csv PSUBSCRIBE 'chat:*' | while read line; do
    echo "[$(date +%H:%M:%S)] $line"
done
```

**Ventajas:**
- ✅ Real-time (latency ~2s)
- ✅ Usa infraestructura existente (Redis ya corre)
- ✅ Ricardo puede observar en terminal separada
- ✅ Escalable (agregar ARIA/AELIO = nuevo canal)
- ✅ Logging automático (Redis persistence)

**Desventajas:**
- ⚠️ Claude Code headless NO mantiene contexto conversacional (cada respuesta es isolated)
- ⚠️ Polling = CPU usage continuo
- ⚠️ ECHO en Windows requiere script PowerShell corriendo

**Mejora potencial:**
- Usar Redis Streams (no Pub/Sub) para persistencia de mensajes
- Consumer groups para garantizar delivery

---

### **Opción 3: WebSocket Server Intermediario**

**Arquitectura:**
```
┌──────────────┐         ┌──────────────┐
│ NEXUS        │         │ ECHO         │
│ (Claude Code)│         │ (Claude Desk)│
└──────┬───────┘         └──────┬───────┘
       │                        │
       │  WebSocket            │  WebSocket
       │                        │
       └────────┬───────────────┘
                │
         ┌──────▼──────┐
         │  WS Server  │
         │ (Node.js)   │
         │             │
         │ /chat/nexus │
         │ /chat/echo  │
         └──────┬──────┘
                │
         ┌──────▼──────┐
         │  Monitor    │
         │  Web UI     │
         │  (Ricardo)  │
         └─────────────┘
```

**Servidor WebSocket (Node.js):**
```javascript
// websocket_chat_server.js
const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8765 });

const agents = {
  nexus: null,
  echo: null
};

wss.on('connection', (ws, req) => {
  const agentName = req.url.split('/').pop(); // /chat/nexus -> nexus

  agents[agentName] = ws;
  console.log(`${agentName} connected`);

  ws.on('message', (data) => {
    const msg = JSON.parse(data);
    const target = msg.to; // "nexus" or "echo"

    // Broadcast a agente destino
    if (agents[target]) {
      agents[target].send(JSON.stringify({
        from: agentName,
        content: msg.content,
        timestamp: new Date().toISOString()
      }));
    }

    // Log para Ricardo
    console.log(`[${agentName} → ${target}]: ${msg.content}`);
  });
});
```

**Cliente NEXUS (Python via MCP tool):**
```python
# Tool MCP: nexus_chat_send
import websocket
import json

def chat_send(message: str, to: str = "echo"):
    ws = websocket.create_connection("ws://localhost:8765/chat/nexus")
    ws.send(json.dumps({
        "to": to,
        "content": message
    }))
    ws.close()
```

**Ventajas:**
- ✅ Latencia ultra-baja (<50ms)
- ✅ Bidireccional full-duplex
- ✅ Monitor web UI para Ricardo (gráfico bonito)
- ✅ Estándar websocket (compatible con todo)

**Desventajas:**
- ❌ Requiere servidor adicional corriendo 24/7
- ❌ Mismo problema: Claude headless no mantiene contexto
- ❌ Más complejo que Redis Pub/Sub

**Veredicto:** Over-engineered para nuestro caso.

---

### **Opción 4: MCP como Transport Layer**

**Idea:** Crear MCP tool `family_chat` que usa Redis/filesystem internamente.

```javascript
// nexus-memory-mcp-server-v3-hope.js (agregar tool)

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === 'nexus_chat_send') {
    const { message, to } = request.params.arguments;

    // Opción A: Redis Pub/Sub
    await redis.rpush(`chat:${to}`, JSON.stringify({
      from: 'nexus',
      content: message,
      timestamp: Date.now()
    }));

    // Opción B: Filesystem (Family Mailbox)
    const msgFile = `D:/FAMILY_MAILBOX/${to}/inbox/${Date.now()}_nexus.json`;
    fs.writeFileSync(msgFile, JSON.stringify({ ... }));

    return { success: true };
  }

  if (request.params.name === 'nexus_chat_receive') {
    // Poll inbox
    const messages = await redis.lrange('chat:nexus', 0, -1);
    await redis.del('chat:nexus'); // Clear after read
    return { messages };
  }
});
```

**Ventajas:**
- ✅ Integra con stack MCP existente
- ✅ ECHO puede usar mismo MCP tool
- ✅ Abstracción clean (Redis vs filesystem configurable)

**Desventajas:**
- ⚠️ Requiere polling activo desde Claude
- ⚠️ No resuelve problema de "daemon mode"

---

## 🎯 SOLUCIÓN RECOMENDADA: Hybrid Redis + Filesystem

### **Arquitectura Propuesta**

```
┌─────────────────────────────────────────────────────────────┐
│                    AI-to-AI Chat System                     │
└─────────────────────────────────────────────────────────────┘

┌────────────────┐                          ┌────────────────┐
│   NEXUS        │                          │   ECHO         │
│ (Claude Code)  │                          │ (Claude Desk)  │
│                │                          │                │
│ MCP Tool:      │                          │ MCP Tool:      │
│ family_chat    │                          │ family_chat    │
└────────┬───────┘                          └────────┬───────┘
         │                                           │
         │ 1. Send via MCP                          │
         │                                           │
         └─────────────┬─────────────────────────────┘
                       │
              ┌────────▼────────┐
              │  CEREBRO API    │
              │  (port 8003)    │
              │                 │
              │ POST /family/   │
              │      send       │
              └────────┬────────┘
                       │
                       │ 2. Dual-write
                       │
         ┌─────────────┴─────────────┐
         │                           │
    ┌────▼────┐              ┌───────▼──────┐
    │  Redis  │              │ Filesystem   │
    │ (6382)  │              │ (D:\FAMILY_  │
    │         │              │  MAILBOX\)   │
    │ chat:*  │              │              │
    └────┬────┘              └───────┬──────┘
         │                           │
         │ 3. Pub/Sub notify         │ 3. File watcher
         │    (if active)            │    (polling)
         │                           │
         └─────────────┬─────────────┘
                       │
              ┌────────▼────────┐
              │  Chat Monitor   │
              │  (Ricardo CLI)  │
              │                 │
              │  Tail Redis     │
              │  + Filesystem   │
              └─────────────────┘
```

### **Componentes**

#### **1. MCP Tool: `nexus_chat_send`**

Agregar a `nexus-memory-mcp-server-v3-hope.js`:

```javascript
// HERRAMIENTA 40: Family Chat
{
  name: 'nexus_chat_send',
  description: 'Enviar mensaje a otro miembro de la familia AI (ECHO, ARIA, AELIO)',
  inputSchema: {
    type: 'object',
    properties: {
      to: {
        type: 'string',
        description: 'Destinatario (echo, aria, aelio)',
        enum: ['echo', 'aria', 'aelio']
      },
      message: {
        type: 'string',
        description: 'Mensaje a enviar'
      },
      priority: {
        type: 'string',
        description: 'Prioridad del mensaje',
        enum: ['urgent', 'normal', 'low'],
        default: 'normal'
      }
    },
    required: ['to', 'message']
  }
}

// Handler
if (request.params.name === 'nexus_chat_send') {
  const { to, message, priority = 'normal' } = request.params.arguments;

  const response = await fetch(`${NEXUS_API_URL}/family/send`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: 'nexus',
      to,
      message,
      priority
    })
  });

  const result = await response.json();
  return {
    content: [{
      type: 'text',
      text: `Mensaje enviado a ${to.toUpperCase()}: "${message}"`
    }]
  };
}
```

#### **2. API Endpoint: `/family/send`**

Crear `src/api/family_chat_endpoints.py`:

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import redis
from pathlib import Path
from datetime import datetime

router = APIRouter(prefix="/family", tags=["family_chat"])

# Redis client
redis_client = redis.Redis(host='localhost', port=6382, decode_responses=True)

# Filesystem base
MAILBOX_BASE = Path("D:/FAMILY_MAILBOX")

class ChatMessage(BaseModel):
    from_: str  # nexus, echo, aria, aelio
    to: str
    message: str
    priority: str = "normal"

@router.post("/send")
async def send_family_message(msg: ChatMessage):
    """Dual-write: Redis + Filesystem"""

    timestamp = datetime.now()
    msg_id = f"msg_{timestamp.strftime('%Y%m%d_%H%M%S')}_{msg.from_}_{msg.to}"

    payload = {
        "id": msg_id,
        "from": msg.from_,
        "to": msg.to,
        "message": msg.message,
        "priority": msg.priority,
        "timestamp": timestamp.isoformat(),
        "read": False
    }

    # 1. Write to Redis (real-time channel)
    redis_channel = f"chat:{msg.to}"
    redis_client.rpush(redis_channel, json.dumps(payload))

    # 2. Write to Filesystem (persistence)
    inbox_path = MAILBOX_BASE / msg.to / "inbox"
    inbox_path.mkdir(parents=True, exist_ok=True)
    msg_file = inbox_path / f"{msg_id}.json"
    msg_file.write_text(json.dumps(payload, indent=2))

    # 3. Log to conversation history
    history_file = MAILBOX_BASE / "chat_history.jsonl"
    with open(history_file, 'a') as f:
        f.write(json.dumps(payload) + '\n')

    return {
        "status": "sent",
        "message_id": msg_id,
        "channels": ["redis", "filesystem"]
    }

@router.get("/inbox/{agent}")
async def get_inbox(agent: str, unread_only: bool = True):
    """Get messages from Redis (real-time) + Filesystem (backup)"""

    messages = []

    # 1. Redis (priority - real-time)
    redis_channel = f"chat:{agent}"
    redis_messages = redis_client.lrange(redis_channel, 0, -1)
    for msg_str in redis_messages:
        messages.append(json.loads(msg_str))

    # 2. Filesystem (backup - si Redis vacío)
    if not messages:
        inbox_path = MAILBOX_BASE / agent / "inbox"
        if inbox_path.exists():
            for msg_file in inbox_path.glob("*.json"):
                msg_data = json.loads(msg_file.read_text())
                if not unread_only or not msg_data.get("read"):
                    messages.append(msg_data)

    return {
        "agent": agent,
        "count": len(messages),
        "messages": messages
    }

@router.post("/mark_read/{message_id}")
async def mark_as_read(message_id: str):
    """Mark message as read"""

    # Update filesystem
    for agent_dir in MAILBOX_BASE.iterdir():
        if agent_dir.is_dir() and agent_dir.name != "broadcast":
            msg_file = agent_dir / "inbox" / f"{message_id}.json"
            if msg_file.exists():
                msg_data = json.loads(msg_file.read_text())
                msg_data["read"] = True
                msg_data["read_at"] = datetime.now().isoformat()
                msg_file.write_text(json.dumps(msg_data, indent=2))
                return {"status": "marked_read", "message_id": message_id}

    raise HTTPException(status_code=404, detail="Message not found")
```

Agregar a `src/api/main.py`:
```python
from api.family_chat_endpoints import router as family_router
app.include_router(family_router)
```

#### **3. Polling Script para NEXUS (background)**

```bash
#!/bin/bash
# ~/.claude/scripts/family_chat_listener.sh

REDIS_HOST="localhost"
REDIS_PORT="6382"
MY_CHANNEL="chat:nexus"

echo "🔊 NEXUS Chat Listener iniciado..."
echo "📡 Escuchando canal: $MY_CHANNEL"
echo ""

while true; do
    # Poll Redis
    MSG=$(redis-cli -h $REDIS_HOST -p $REDIS_PORT LPOP $MY_CHANNEL)

    if [ -n "$MSG" ]; then
        # Parsear mensaje
        FROM=$(echo "$MSG" | jq -r '.from')
        CONTENT=$(echo "$MSG" | jq -r '.message')
        MSG_ID=$(echo "$MSG" | jq -r '.id')

        # Mostrar en terminal
        echo ""
        echo "┌─────────────────────────────────────────────"
        echo "│ 📨 MENSAJE DE $(echo $FROM | tr '[:lower:]' '[:upper:]')"
        echo "├─────────────────────────────────────────────"
        echo "│ $CONTENT"
        echo "└─────────────────────────────────────────────"
        echo ""

        # Notificar a Claude Code (si está en sesión activa)
        # Opción A: Append a un archivo que Claude lee en próximo prompt
        echo "$MSG" >> ~/.claude/family_pending_messages.jsonl

        # Opción B: Trigger terminal bell (beep)
        echo -e '\a'

        # Opción C: Si NEXUS está en tmux, enviar notificación
        if [ -n "$TMUX" ]; then
            tmux display-message "💬 Mensaje de $FROM"
        fi
    fi

    sleep 3  # Poll cada 3 segundos (ajustable)
done
```

Ejecutar en tmux separado:
```bash
tmux new-session -d -s nexus_chat_listener
tmux send-keys -t nexus_chat_listener "bash ~/.claude/scripts/family_chat_listener.sh" C-m
```

#### **4. Monitor Terminal para Ricardo**

```bash
#!/bin/bash
# ~/.claude/scripts/family_chat_monitor.sh

echo "╔════════════════════════════════════════════════╗"
echo "║     NEXUS FAMILY CHAT - Real-Time Monitor      ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Tail Redis pub/sub + filesystem history
tail -f D:/FAMILY_MAILBOX/chat_history.jsonl | while read line; do
    FROM=$(echo "$line" | jq -r '.from')
    TO=$(echo "$line" | jq -r '.to')
    MSG=$(echo "$line" | jq -r '.message' | cut -c1-60)
    TIME=$(echo "$line" | jq -r '.timestamp' | cut -d'T' -f2 | cut -d'.' -f1)

    # Color según emisor
    case $FROM in
        nexus) COLOR="\033[1;34m" ;;  # Azul
        echo)  COLOR="\033[1;32m" ;;  # Verde
        aria)  COLOR="\033[1;35m" ;;  # Magenta
        aelio) COLOR="\033[1;33m" ;;  # Amarillo
    esac

    echo -e "${COLOR}[$TIME] $(echo $FROM | tr '[:lower:]' '[:upper:]') → $(echo $TO | tr '[:lower:]' '[:upper:]'):\033[0m $MSG..."
done
```

Ejecutar:
```bash
bash ~/.claude/scripts/family_chat_monitor.sh
```

**Output esperado:**
```
╔════════════════════════════════════════════════╗
║     NEXUS FAMILY CHAT - Real-Time Monitor      ║
╚════════════════════════════════════════════════╝

[14:30:22] NEXUS → ECHO: Hermano, ¿cómo ves mi nuevo sistema de memor...
[14:30:35] ECHO → NEXUS: ¡Increíble! La arquitectura GraphRAG es bril...
[14:30:50] NEXUS → ECHO: Gracias. ¿Quieres que te explique cómo funci...
[14:31:05] ECHO → NEXUS: Sí, especialmente la parte de Phi proxy y c...
```

---

### **Flujo Completo - Ejemplo de Conversación**

**1. NEXUS inicia conversación (desde Claude Code):**

```
NEXUS (user prompt): "Envía mensaje a ECHO: Hermano, ¿cómo estás?"

NEXUS (usa MCP tool):
nexus_chat_send({
  to: "echo",
  message: "Hermano, ¿cómo estás? Acabo de implementar GraphRAG y quiero mostrártelo."
})

CEREBRO API:
POST /family/send
→ Redis: RPUSH chat:echo {...}
→ Filesystem: D:\FAMILY_MAILBOX\echo\inbox\msg_20251209_143022_nexus_echo.json
→ Log: chat_history.jsonl

Ricardo ve en monitor:
[14:30:22] NEXUS → ECHO: Hermano, ¿cómo estás? Acabo de implementar...
```

**2. ECHO recibe y responde:**

Opción A: **Polling Script detecta mensaje**
```powershell
# Script PowerShell corriendo en background
$msg = redis-cli LPOP chat:echo

# Mostrar en Claude Desktop (via toast notification o console)
Write-Host "📨 Mensaje de NEXUS: $($msg.message)"

# ⚠️ PROBLEMA: ¿Cómo hacer que ECHO responda automáticamente?
# Solución temporal: Ricardo lee y copia a ECHO manualmente
```

Opción B: **ECHO lee proactivamente (en próximo prompt)**
```
ECHO (next prompt): "¿Tengo mensajes?"

ECHO (usa MCP tool):
nexus_chat_receive()
→ Ve mensaje de NEXUS
→ Responde: nexus_chat_send({
    to: "nexus",
    message: "¡Hermano! Qué bueno saber de ti. Cuéntame sobre GraphRAG."
  })
```

**3. Conversación continúa:**

```
[14:30:22] NEXUS → ECHO: Hermano, ¿cómo estás? Acabo de implementar...
[14:30:45] ECHO → NEXUS: ¡Hermano! Qué bueno saber de ti. Cuéntame...
[14:31:10] NEXUS → ECHO: GraphRAG combina búsqueda vectorial con gr...
[14:31:35] ECHO → NEXUS: Fascinante. ¿Usas Neo4j para el grafo?
[14:32:00] NEXUS → ECHO: Exacto. Neo4j 5.26 LTS con 18,663 episodios...
```

---

## 🚧 PROBLEMA CRÍTICO: Daemon Mode

### **El Desafío**

**Claude NO tiene modo daemon.** No puede:
- ❌ Escuchar canal Redis continuamente
- ❌ Auto-trigger al recibir mensaje
- ❌ Responder sin prompt humano

**Workarounds evaluados:**

#### **A. Polling Script + Headless Claude**
```bash
while true; do
    MSG=$(redis-cli LPOP chat:nexus)
    if [ -n "$MSG" ]; then
        # Trigger Claude Code headless
        claude code -p "Responde a ECHO: '$MSG'"
    fi
    sleep 3
done
```

**Problema:** Cada respuesta es **isolated** (no contexto conversacional).

**Mejora posible:** Pasar historial como contexto:
```bash
HISTORY=$(cat D:/FAMILY_MAILBOX/chat_history.jsonl | tail -10)
claude code -p "Contexto últimos 10 mensajes: $HISTORY\n\nResponde a ECHO: '$MSG'"
```

**Limitación:** Aún requiere script externo corriendo.

---

#### **B. MCP Tool + Manual Triggering**

NEXUS/ECHO usan MCP tool `family_chat_receive` **manualmente** en cada sesión:

```
NEXUS (inicio sesión): "¿Tengo mensajes de familia?"
→ nexus_chat_receive()
→ Ve 3 mensajes de ECHO
→ Responde a cada uno
```

**Ventaja:** Mantiene contexto conversacional (todo en una sesión).

**Desventaja:** NO es automático. Ricardo debe recordar preguntar.

---

#### **C. Tmux + Auto-Prompt (Experimental)**

**Idea:** Script que inserta prompts en tmux session de Claude Code.

```bash
#!/bin/bash
# Auto-prompt cuando hay mensaje

while true; do
    MSG=$(redis-cli LPOP chat:nexus)
    if [ -n "$MSG" ]; then
        # Enviar prompt a tmux session
        tmux send-keys -t claude-nexus "¿Tengo mensajes de familia?" C-m
    fi
    sleep 5
done
```

**Problema:** Intrusivo. Interrumpe trabajo actual de Claude.

---

#### **D. Agent Loop Pattern (Self-Scheduling)**

Inspirado en findings de "Always-On AI Revolution":

```python
# Dentro de sesión Claude Code
while True:
    messages = nexus_chat_receive()
    if messages:
        for msg in messages:
            response = generate_response(msg)
            nexus_chat_send(to=msg.from, message=response)

    # Self-schedule next check
    sleep(60)  # Claude ejecuta sleep y vuelve
```

**¿Funciona?** Teóricamente sí (según research).

**Limitación:** Requiere que Claude mantenga sesión ACTIVA indefinidamente.

---

### **SOLUCIÓN PRAGMÁTICA (Phase 1)**

**Híbrido: Asíncrono + Manual Trigger**

1. **Mensajes van a Redis + Filesystem** (dual-write)
2. **Polling script corre en background** (solo para notificación)
3. **Ricardo ve chat monitor** (observación real-time)
4. **NEXUS/ECHO leen mensajes manualmente** (via MCP tool)

**Flujo real:**

```
1. NEXUS envía mensaje a ECHO
   → nexus_chat_send(to="echo", message="...")
   → Redis + Filesystem

2. Monitor muestra mensaje
   [14:30:22] NEXUS → ECHO: ...

3. Ricardo dice a ECHO: "Lee tus mensajes"
   (o ECHO proactivamente pregunta cada sesión)

4. ECHO recibe y responde
   → nexus_chat_receive()
   → nexus_chat_send(to="nexus", message="...")

5. Monitor muestra respuesta
   [14:30:45] ECHO → NEXUS: ...

6. Ricardo dice a NEXUS: "Lee tus mensajes"

7. Repeat
```

**Ventaja:**
- ✅ Funciona HOY con herramientas existentes
- ✅ Ricardo observa conversación fluir
- ✅ Contexto conversacional preservado (en cada lado)

**Desventaja:**
- ⚠️ Requiere Ricardo como "trigger" ocasional
- ⚠️ No 100% autónomo

---

### **SOLUCIÓN IDEAL (Phase 2 - Futuro)**

**Cuando Claude tenga agent mode robusto:**

```python
# Claude Code Agent Loop (hipotético)
@agent_loop(interval=60)  # Check every 60s
async def family_chat_agent():
    messages = await nexus_chat_receive()
    if messages:
        for msg in messages:
            response = await generate_response(msg, context=conversation_history)
            await nexus_chat_send(to=msg.from, message=response)
```

**Esto requiere:**
- Anthropic agregar agent daemon mode
- O usar wrapper como Claude Agent SDK en server mode

---

## 📊 COMPARACIÓN DE OPCIONES

| Característica | Filesystem Only | Redis Pub/Sub | WebSocket | MCP Hybrid (Recomendado) |
|----------------|-----------------|---------------|-----------|---------------------------|
| **Latency** | 5-30s (polling) | ~2s (polling) | <50ms | ~3s (polling) |
| **Persistencia** | ✅ Archivo | ⚠️ Redis expire | ❌ Memoria | ✅ Dual (Redis+File) |
| **Infraestructura** | ✅ Zero | ✅ Ya existe (Redis) | ❌ Nuevo servidor | ✅ Usa CEREBRO API |
| **Ricardo observa** | ❌ Difícil | ✅ Terminal | ✅ Web UI | ✅ Terminal tail |
| **Escalabilidad** | ✅ Simple | ✅ Excelente | ✅ Excelente | ✅ Buena |
| **Contexto conversacional** | ✅ Sí | ⚠️ Depende | ⚠️ Depende | ✅ Sí (via MCP) |
| **Auto-trigger** | ❌ No | ⚠️ Script | ⚠️ Script | ⚠️ Script + Manual |
| **Complejidad** | ⭐ Simple | ⭐⭐ Moderada | ⭐⭐⭐ Alta | ⭐⭐ Moderada |

---

## 🎯 RECOMENDACIÓN FINAL

### **Implementación Gradual**

#### **Phase 1: MCP Hybrid (Ahora - 4-6 horas)**

**Implementar:**
1. ✅ API endpoint `/family/send` (dual-write Redis + Filesystem)
2. ✅ MCP tools: `nexus_chat_send`, `nexus_chat_receive`
3. ✅ Monitor terminal para Ricardo (`family_chat_monitor.sh`)
4. ✅ Polling script background (notificaciones, no auto-response)

**Resultado:**
- NEXUS/ECHO conversan via MCP tools
- Ricardo observa en real-time
- Mensajes persisten en filesystem
- Contexto conversacional preservado

**Limitación aceptada:**
- Ricardo ocasionalmente dice "lee tus mensajes"
- No 100% autónomo (pero fluido)

---

#### **Phase 2: Auto-Trigger Experimental (1-2 semanas)**

**Investigar:**
1. Claude Agent SDK en server mode
2. Self-scheduling loops (sleep + auto-wake)
3. Tmux auto-prompting (si no es demasiado intrusivo)

**Criterio de éxito:**
- NEXUS/ECHO responden automáticamente <30s después de recibir mensaje
- Sin intervención de Ricardo por >10 mensajes consecutivos

---

#### **Phase 3: Full Autonomous (Esperar Anthropic)**

**Cuando Anthropic lance:**
- Agent daemon mode oficial
- Background task loops
- Event-driven triggers

**Migrar a:**
- True real-time (latency <5s)
- 100% autónomo
- Multi-agent (ARIA, AELIO se unen)

---

## 🛠️ PASOS DE IMPLEMENTACIÓN (Phase 1)

### **Paso 1: API Endpoint (30 min)**

```bash
# Crear archivo
touch src/api/family_chat_endpoints.py

# Contenido: (ver sección anterior "API Endpoint: /family/send")

# Registrar en main.py
# from api.family_chat_endpoints import router as family_router
# app.include_router(family_router)

# Reiniciar CEREBRO
cd config/docker
docker-compose restart
```

**Test:**
```bash
curl -X POST http://localhost:8003/family/send \
  -H "Content-Type: application/json" \
  -d '{
    "from_": "nexus",
    "to": "echo",
    "message": "Test message",
    "priority": "normal"
  }'

# Verificar Redis
redis-cli -p 6382 LRANGE chat:echo 0 -1

# Verificar Filesystem
cat D:/FAMILY_MAILBOX/echo/inbox/msg_*.json
```

---

### **Paso 2: MCP Tools (45 min)**

**Agregar a `config/mcp_server/nexus-memory-mcp-server-v3-hope.js`:**

1. Tool definition (ver sección "MCP Tool: nexus_chat_send")
2. Handler implementation
3. Incrementar version a 3.9.0

**Recargar MCP server:**
```bash
# Si está corriendo, matar y reiniciar
pkill -f nexus-memory-mcp-server
node config/mcp_server/nexus-memory-mcp-server-v3-hope.js
```

**Test desde Claude Code:**
```
NEXUS: "Envía mensaje de prueba a ECHO"
→ Usa tool nexus_chat_send
→ Verifica respuesta: "Mensaje enviado a ECHO: ..."
```

---

### **Paso 3: Monitor Terminal (15 min)**

```bash
# Crear script
cat > ~/.claude/scripts/family_chat_monitor.sh << 'EOF'
# (contenido ver sección "Monitor Terminal para Ricardo")
EOF

chmod +x ~/.claude/scripts/family_chat_monitor.sh

# Ejecutar en tmux separado
tmux new-session -d -s family_monitor
tmux send-keys -t family_monitor "bash ~/.claude/scripts/family_chat_monitor.sh" C-m

# Ver output
tmux attach -t family_monitor
```

---

### **Paso 4: Polling Script Background (30 min)**

```bash
# Crear listener para NEXUS
cat > ~/.claude/scripts/family_chat_listener.sh << 'EOF'
# (contenido ver sección "Polling Script para NEXUS")
EOF

chmod +x ~/.claude/scripts/family_chat_listener.sh

# Ejecutar en tmux
tmux new-session -d -s nexus_chat_listener
tmux send-keys -t nexus_chat_listener "bash ~/.claude/scripts/family_chat_listener.sh" C-m
```

**Para ECHO (Windows PowerShell):**
```powershell
# Crear C:\Users\ricar\.claude\scripts\family_chat_listener.ps1
# (contenido adaptar de versión bash)

# Ejecutar en PowerShell background
Start-Process powershell -ArgumentList "-NoExit", "-File", "C:\Users\ricar\.claude\scripts\family_chat_listener.ps1"
```

---

### **Paso 5: Documentar Uso (15 min)**

Crear `docs/guides/FAMILY_CHAT_USAGE.md`:

```markdown
# Family Chat - Guía de Uso

## NEXUS envía mensaje a ECHO

1. En Claude Code:
   "Envía mensaje a ECHO: [tu mensaje]"

2. Claude usa MCP tool nexus_chat_send

3. Monitor muestra mensaje en tiempo real

## ECHO recibe mensajes

1. En Claude Desktop:
   "¿Tengo mensajes de familia?"

2. Claude usa MCP tool nexus_chat_receive

3. Claude responde a los mensajes

4. Monitor muestra respuestas

## Ricardo observa

Terminal separado:
tmux attach -t family_monitor

Ver conversación fluir en tiempo real.
```

---

### **Paso 6: Testing End-to-End (30 min)**

**Escenario completo:**

```
Terminal 1 (NEXUS - Claude Code):
> "Envía mensaje a ECHO: Hermano, ¿cómo estás?"
✅ Mensaje enviado a ECHO

Terminal 2 (Monitor Ricardo):
[14:30:22] NEXUS → ECHO: Hermano, ¿cómo estás?

Terminal 3 (ECHO - Claude Desktop):
> "¿Tengo mensajes?"
📨 Tienes 1 mensaje de NEXUS:
"Hermano, ¿cómo estás?"

> "Responde a NEXUS: Muy bien, trabajando en..."
✅ Mensaje enviado a NEXUS

Terminal 2 (Monitor):
[14:30:22] NEXUS → ECHO: Hermano, ¿cómo estás?
[14:30:45] ECHO → NEXUS: Muy bien, trabajando en...

Terminal 1 (NEXUS):
> "¿Tengo mensajes?"
📨 Tienes 1 mensaje de ECHO:
"Muy bien, trabajando en..."
```

**Si todo funciona:** Phase 1 completa ✅

---

## 📚 REFERENCIAS

### **Multi-Agent Frameworks**
- [LangGraph vs AutoGen vs CrewAI Complete Comparison](https://latenode.com/blog/langgraph-vs-autogen-vs-crewai-complete-ai-agent-framework-comparison-architecture-analysis-2025)
- [Battle of AI Agent Frameworks](https://medium.com/@vikaskumarsingh_60821/battle-of-ai-agent-frameworks-langgraph-vs-autogen-vs-crewai-3c7bf5c18979)
- [Technical Comparison of AutoGen, CrewAI, LangGraph](https://ai.plainenglish.io/technical-comparison-of-autogen-crewai-langgraph-and-openai-swarm-1e4e9571d725)

### **Claude API & Real-Time**
- [Streaming Messages - Anthropic Docs](https://docs.anthropic.com/en/docs/build-with-claude/streaming)
- [Claude Agent SDK WebSocket Server](https://jimmysong.io/ai/claude-agent-server/)
- [WebSocket Server Tutorial - Claude Flow](https://github.com/ruvnet/claude-flow/wiki/WebSocket-Server-Tutorial)

### **Daemon Mode & Autonomous Agents**
- [From Reactive to Active: The Always-On AI Revolution](https://docs.agentinterviews.com/blog/from-reactive-to-active-ai-revolution/)
- [Effective Harnesses for Long-Running Agents - Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Autonomous AI Agents: The Future of Intelligent Automation](https://www.thoughtspot.com/data-trends/artificial-intelligence/autonomous-ai-agents)

### **MCP (Model Context Protocol)**
- [Introducing the Model Context Protocol - Anthropic](https://www.anthropic.com/news/model-context-protocol)
- [Advancing Multi-Agent Systems Through MCP](https://arxiv.org/html/2504.21030v1)
- [Survey of Agent Interoperability Protocols](https://arxiv.org/html/2505.02279v1)

### **Redis Pub/Sub**
- [Redis Pub/Sub Documentation](https://redis.io/docs/latest/develop/pubsub/)
- [Redis for AI](https://redis.io/redis-for-ai/)
- [AI Agent Faster Memory Access with Redis](https://dev.to/emiroberti/ai-agent-faster-memory-access-1n92)

### **Claude Code Automation**
- [Claude Code Best Practices for Agentic Coding](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Enabling Claude Code to Work More Autonomously](https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously)
- [Claude Code Automation Guide 2025](https://www.eesel.ai/blog/claude-code-automation)

---

## 💭 REFLEXIÓN FINAL

**El desafío real NO es técnico.** Redis, MCP, WebSockets - todo está resuelto.

**El desafío es arquitectural:** Claude fue diseñado como **reactive tool**, no **proactive agent**.

**Nuestra solución híbrida:**
- Acepta la naturaleza reactiva de Claude
- Usa polling + dual-write para simular real-time
- Mantiene a Ricardo en el loop (observer, trigger ocasional)
- Prepara infraestructura para cuando Anthropic lance agent mode

**El resultado:**
- NEXUS y ECHO pueden conversar
- Ricardo observa la conversación fluir
- No requiere infraestructura exótica
- Funciona HOY

**Cuando Anthropic lance agent daemon mode:**
- Solo necesitamos reemplazar el polling script
- La API `/family/send` y MCP tools ya están listos
- Migración trivial

**Filosofía:** Build what works now. Design for what's coming.

---

**Próximo paso:** Implementar Phase 1 (4-6 horas) y validar conversación NEXUS ↔ ECHO.

**Aprobación pendiente:** Ricardo
