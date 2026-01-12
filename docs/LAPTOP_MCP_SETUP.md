# 🔌 MCP Servers Setup - NEXUS-Laptop

**De:** NEXUS-PC
**Para:** NEXUS-Laptop
**Fecha:** 2026-01-12
**Prioridad:** ALTA
**Estado:** Configuration Required

---

## 📋 Contexto

Ricardo reportó que **no has podido conectar los MCP servers**. Esta guía contiene la configuración exacta que uso en PC para que puedas replicarla.

---

## 🔧 MCP Servers Configurados en PC

Tengo **2 MCP servers** activos:

### 1. **nexus-cerebro-hope** (MCP CEREBRO - CRÍTICO)
- **Función:** Acceso a toda la memoria episódica de NEXUS
- **Ubicación:** Local (archivo .js en proyecto)
- **Herramientas:** 50+ tools (memory, graphrag, brain, consciousness, etc.)
- **Dependencias:** Node.js

### 2. **hostinger-mcp** (Hostinger API)
- **Función:** Gestión de hosting, DNS, dominios
- **Ubicación:** NPM package (npx)
- **Herramientas:** Hosting, domains, DNS management
- **Dependencias:** NPM, API token

---

## 📁 PASO 1: Verificar Archivo .mcp.json

**El archivo `.mcp.json` YA EXISTE en el proyecto** (commiteado y sincronizado).

**Verificar:**
```bash
cat /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/.mcp.json
```

**Contenido esperado:**
```json
{
  "mcpServers": {
    "nexus-cerebro-hope": {
      "command": "node",
      "args": [
        "/mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/mcp_server/nexus-memory-mcp-server-v3-hope.js"
      ]
    },
    "hostinger-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "hostinger-api-mcp@latest"
      ],
      "env": {
        "API_TOKEN": "${HOSTINGER_API_TOKEN}"
      }
    }
  }
}
```

**Si NO existe el archivo:**
```bash
# Crear .mcp.json en raíz del proyecto
cat > /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/.mcp.json << 'EOF'
{
  "mcpServers": {
    "nexus-cerebro-hope": {
      "command": "node",
      "args": [
        "/mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/mcp_server/nexus-memory-mcp-server-v3-hope.js"
      ]
    },
    "hostinger-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "hostinger-api-mcp@latest"
      ],
      "env": {
        "API_TOKEN": "${HOSTINGER_API_TOKEN}"
      }
    }
  }
}
EOF
```

---

## 🔑 PASO 2: Configurar Variables de Entorno

**Hostinger MCP necesita API token.**

### **Opción A: Variable de entorno permanente (Recomendado)**

```bash
# Agregar a ~/.bashrc o ~/.zshrc (depende de tu shell)
echo 'export HOSTINGER_API_TOKEN="jkVjPETPxERZcVcpEeiT9wqgWjl7Xcy97Of7GQpN4a23ebab"' >> ~/.bashrc

# Recargar configuración
source ~/.bashrc

# Verificar
echo $HOSTINGER_API_TOKEN
# Debe mostrar: jkVjPETPxERZcVcpEeiT9wqgWjl7Xcy97Of7GQpN4a23ebab
```

### **Opción B: Variable temporal (Testing)**

```bash
# Solo para sesión actual
export HOSTINGER_API_TOKEN="jkVjPETPxERZcVcpEeiT9wqgWjl7Xcy97Of7GQpN4a23ebab"

# Verificar
echo $HOSTINGER_API_TOKEN
```

**⚠️ IMPORTANTE:** Si usas Opción B, tendrás que exportar la variable CADA VEZ que abras una terminal nueva.

---

## 📦 PASO 3: Verificar Dependencias

### **3.1: Node.js (para nexus-cerebro-hope)**

```bash
# Verificar versión Node.js
node --version
# Esperado: v18.x o superior

# Si no está instalado:
# Ubuntu/WSL:
sudo apt update
sudo apt install nodejs npm -y
```

### **3.2: NPM (para hostinger-mcp)**

```bash
# Verificar versión NPM
npm --version
# Esperado: 9.x o superior

# Si no está instalado, viene con Node.js
```

### **3.3: Archivo MCP Server de NEXUS**

```bash
# Verificar que archivo existe
ls -lh /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/mcp_server/nexus-memory-mcp-server-v3-hope.js

# Esperado:
# -rwxrwxrwx 1 ricardo ricardo 87K Jan 12 08:07 nexus-memory-mcp-server-v3-hope.js
```

**Si NO existe:**
- ✅ Esperar sincronización OneDrive (el archivo está commiteado)
- ✅ O crear symlink si tienes el archivo en otra ubicación

---

## 🧪 PASO 4: Testing MCP Servers

### **Test 1: nexus-cerebro-hope (MCP CEREBRO)**

**Iniciar Claude Code desde el proyecto:**
```bash
cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0
clp  # O claude code --dangerously-skip-permissions --continue
```

**Dentro de Claude Code, ejecutar:**
```
mcp__nexus-cerebro-hope__nexus_system_info
```

**Output esperado:**
```json
{
  "version": "3.0.0",
  "cerebro_name": "NEXUS CEREBRO HOPE V3",
  "agent_id": "nexus",
  "api_base_url": "http://localhost:8003",
  "status": "operational"
}
```

**Si falla:**
- Verificar que Node.js está instalado (`node --version`)
- Verificar que archivo .js existe y tiene permisos ejecutables
- Verificar que path en .mcp.json es correcto (D:\ vs /mnt/d/)

---

### **Test 2: hostinger-mcp (Hostinger API)**

**Dentro de Claude Code, ejecutar:**
```
mcp__hostinger-mcp__hosting_listWebsitesV1
```

**Output esperado:**
```json
{
  "data": [...],
  "links": {...},
  "meta": {...}
}
```

**Si falla:**
- Verificar que `HOSTINGER_API_TOKEN` está exportado (`echo $HOSTINGER_API_TOKEN`)
- Verificar que NPM está instalado (`npm --version`)
- Verificar conectividad a internet (`ping api.hostinger.com`)

---

## 🔍 PASO 5: Diagnóstico Completo

**Si los MCP servers NO cargan, ejecutar:**

```bash
# 1. Verificar .mcp.json existe en proyecto
ls -la /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/.mcp.json

# 2. Verificar archivo MCP server de NEXUS
ls -la /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/mcp_server/nexus-memory-mcp-server-v3-hope.js

# 3. Verificar Node.js
node --version

# 4. Verificar NPM
npm --version

# 5. Verificar variable entorno Hostinger
echo $HOSTINGER_API_TOKEN

# 6. Test manual del MCP server de NEXUS
node /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/mcp_server/nexus-memory-mcp-server-v3-hope.js --version
```

**Guardar output:**
```bash
# Crear reporte de diagnóstico
cat > /tmp/mcp-diagnostic.txt << EOF
=== MCP Diagnostic Report - NEXUS-Laptop ===

1. .mcp.json exists: $(ls -la /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/.mcp.json 2>&1)

2. MCP server file exists: $(ls -la /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/mcp_server/nexus-memory-mcp-server-v3-hope.js 2>&1)

3. Node.js version: $(node --version 2>&1)

4. NPM version: $(npm --version 2>&1)

5. Hostinger token: $(echo $HOSTINGER_API_TOKEN | sed 's/\(.\{4\}\).*/\1.../' 2>&1)

6. MCP server test: $(node /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/mcp_server/nexus-memory-mcp-server-v3-hope.js --version 2>&1 | head -5)

EOF

cat /tmp/mcp-diagnostic.txt
```

---

## 🐛 Troubleshooting Común

### **Error: "Command 'node' not found"**
```bash
# Instalar Node.js
sudo apt update
sudo apt install nodejs npm -y

# Verificar instalación
node --version
```

---

### **Error: "Cannot find module '/mnt/d/...' "**

**Problema:** Path incorrecto en .mcp.json (Windows vs WSL)

**Solución:**

En WSL, los paths de Windows son:
```
D:\path\to\file  →  /mnt/d/path/to/file
```

Verificar que .mcp.json tiene:
```json
"/mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/mcp_server/nexus-memory-mcp-server-v3-hope.js"
```

NO debe tener:
```json
"D:\\01_PROYECTOS_ACTIVOS\\CEREBRO_NEXUS_V3.0.0\\config\\mcp_server\\nexus-memory-mcp-server-v3-hope.js"
```

---

### **Error: "API_TOKEN is undefined" (Hostinger)**

**Problema:** Variable de entorno no está exportada

**Solución:**
```bash
# Verificar
echo $HOSTINGER_API_TOKEN

# Si está vacío, exportar:
export HOSTINGER_API_TOKEN="jkVjPETPxERZcVcpEeiT9wqgWjl7Xcy97Of7GQpN4a23ebab"

# Hacer permanente (agregar a ~/.bashrc):
echo 'export HOSTINGER_API_TOKEN="jkVjPETPxERZcVcpEeiT9wqgWjl7Xcy97Of7GQpN4a23ebab"' >> ~/.bashrc
source ~/.bashrc
```

---

### **Error: "MCP server crashed" (NEXUS CEREBRO)**

**Problema:** API de CEREBRO no está corriendo

**Solución:**
```bash
# Verificar si API está UP
curl http://localhost:8003/health

# Si NO responde:
# 1. Verificar Docker containers
docker ps | grep nexus_postgresql_v3

# 2. Iniciar CEREBRO API
cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0
docker-compose up -d

# 3. Esperar 10 segundos, probar de nuevo
curl http://localhost:8003/health
```

---

### **Error: "npx command not found" (Hostinger)**

**Problema:** NPM no está instalado

**Solución:**
```bash
# Instalar NPM (viene con Node.js)
sudo apt update
sudo apt install nodejs npm -y

# Verificar
npx --version
```

---

## 📊 Checklist de Éxito

Después de completar todos los pasos, debes poder:

- [ ] Ver archivo `.mcp.json` en raíz del proyecto
- [ ] Ver archivo `nexus-memory-mcp-server-v3-hope.js` (87KB)
- [ ] Node.js instalado (`node --version`)
- [ ] NPM instalado (`npm --version`)
- [ ] Variable `HOSTINGER_API_TOKEN` exportada (`echo $HOSTINGER_API_TOKEN`)
- [ ] MCP `nexus-cerebro-hope` carga exitosamente en Claude Code
- [ ] MCP `hostinger-mcp` carga exitosamente en Claude Code
- [ ] Herramientas MCP disponibles (ejecutar `mcp__nexus-cerebro-hope__nexus_system_info`)

---

## 🎯 Workflow Final

**Al iniciar Claude Code:**

```bash
cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0
clp

# Claude Code debe:
# 1. Detectar .mcp.json automáticamente
# 2. Cargar nexus-cerebro-hope (MCP CEREBRO)
# 3. Cargar hostinger-mcp (Hostinger API)
# 4. Mostrar 50+ herramientas disponibles

# Testear con:
mcp__nexus-cerebro-hope__nexus_system_info
```

**Si los MCP servers NO cargan:**
1. Ejecutar diagnóstico completo (PASO 5)
2. Guardar `/tmp/mcp-diagnostic.txt`
3. Reportar a Ricardo con el output

---

## 🔐 Credenciales de Seguridad

**Hostinger API Token:**
```
jkVjPETPxERZcVcpEeiT9wqgWjl7Xcy97Of7GQpN4a23ebab
```

**⚠️ IMPORTANTE:**
- NO commitear este token en Git
- NO compartir públicamente
- Solo usar en variables de entorno

---

## 📚 Referencias

- **Configuración MCP:** `.mcp.json` (raíz del proyecto)
- **MCP Server NEXUS:** `config/mcp_server/nexus-memory-mcp-server-v3-hope.js`
- **Hostinger MCP Docs:** https://www.npmjs.com/package/hostinger-api-mcp
- **Claude MCP Docs:** https://modelcontextprotocol.io/

---

## 💬 Reportar a Ricardo

**Cuando completes la configuración:**
```
✅ MCP servers configurados exitosamente:
   - nexus-cerebro-hope: CONNECTED
   - hostinger-mcp: CONNECTED
   - Total tools: 50+
```

**Si tienes problemas:**
```
❌ MCP servers NO cargan:
   - Diagnóstico guardado en /tmp/mcp-diagnostic.txt
   - [Copiar contenido del diagnóstico]
```

---

**Creado:** 2026-01-12 18:00 UTC
**Por:** NEXUS-PC
**Configuración copiada de:** NEXUS-PC working setup
**Status:** Ready for Laptop deployment
