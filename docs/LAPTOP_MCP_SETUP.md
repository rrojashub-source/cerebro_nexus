# 🔌 MCP Servers Setup - NEXUS-Laptop

**De:** NEXUS-PC
**Para:** NEXUS-Laptop
**Fecha:** 2026-01-12
**Prioridad:** ALTA
**Estado:** Configuration Required

---

## 📋 Contexto

Ricardo reportó que **no has podido conectar los MCP servers**. Esta guía contiene la configuración que necesitas para conectarte al **CEREBRO Cloud en Fly.io**.

---

## ⚠️ DIFERENCIA CRÍTICA: PC vs Laptop

**NEXUS-PC (yo):**
- Usa CEREBRO local: `http://localhost:8013`
- MCP server apunta a PostgreSQL local (puerto 5437)
- API corre en Docker local

**NEXUS-Laptop (tú):**
- Usa CEREBRO Cloud: `https://nexus-cerebro-api.fly.dev`
- MCP server apunta a API en Fly.io (Cloud)
- NO necesitas Docker local ni PostgreSQL local

**Por eso necesitas configuración diferente.**

---

## 🔧 MCP Servers para Laptop

Necesitas **2 MCP servers**:

### 1. **nexus-cerebro-hope** (MCP CEREBRO Cloud - CRÍTICO)
- **Función:** Acceso a toda la memoria episódica de NEXUS en Cloud
- **Endpoint:** `https://nexus-cerebro-api.fly.dev`
- **Ubicación:** Archivo .js modificado para Cloud
- **Herramientas:** 50+ tools (memory, graphrag, brain, consciousness, etc.)
- **Dependencias:** Node.js

### 2. **hostinger-mcp** (Hostinger API)
- **Función:** Gestión de hosting, DNS, dominios
- **Ubicación:** NPM package (npx)
- **Herramientas:** Hosting, domains, DNS management
- **Dependencias:** NPM, API token

---

## 📁 PASO 1: Crear MCP Server para Cloud (CRÍTICO)

**⚠️ IMPORTANTE:** El archivo MCP que está en el repo apunta a `localhost:8013` (para PC).
**Tú necesitas uno que apunte a `https://nexus-cerebro-api.fly.dev` (Cloud).**

### **1.1: Crear MCP Server Cloud-specific**

```bash
cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/mcp_server

# Copiar el MCP server original
cp nexus-memory-mcp-server-v3-hope.js nexus-memory-mcp-server-v3-hope-cloud.js

# Modificar para apuntar a Cloud
# Cambiar línea 92:
# ANTES: const NEXUS_API_LOCAL = 'http://localhost:8013';
# DESPUÉS: const NEXUS_API_LOCAL = 'https://nexus-cerebro-api.fly.dev';
```

**Modificación con sed (automático):**
```bash
sed -i "s|http://localhost:8013|https://nexus-cerebro-api.fly.dev|g" \
  /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/mcp_server/nexus-memory-mcp-server-v3-hope-cloud.js
```

**Verificar cambio:**
```bash
grep "NEXUS_API_LOCAL" /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/mcp_server/nexus-memory-mcp-server-v3-hope-cloud.js

# Debe mostrar:
# const NEXUS_API_LOCAL = 'https://nexus-cerebro-api.fly.dev';
```

---

### **1.2: Crear .mcp.json para Laptop**

**Crear archivo `.mcp.json` en raíz del proyecto:**

```bash
cat > /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/.mcp.json << 'EOF'
{
  "mcpServers": {
    "nexus-cerebro-hope": {
      "command": "node",
      "args": [
        "/mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/mcp_server/nexus-memory-mcp-server-v3-hope-cloud.js"
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

**⚠️ NOTA:** Observa que apunta a `nexus-memory-mcp-server-v3-hope-cloud.js` (el modificado para Cloud), NO al original.

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

### **3.3: Archivos MCP Server de NEXUS**

```bash
# Verificar que archivo original existe
ls -lh /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/mcp_server/nexus-memory-mcp-server-v3-hope.js

# Esperado:
# -rwxrwxrwx 1 ricardo ricardo 87K Jan 12 08:07 nexus-memory-mcp-server-v3-hope.js

# Verificar que archivo Cloud existe (el que creaste en PASO 1.1)
ls -lh /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/mcp_server/nexus-memory-mcp-server-v3-hope-cloud.js

# Esperado:
# -rwxrwxrwx 1 ricardo ricardo 87K nexus-memory-mcp-server-v3-hope-cloud.js
```

**Si NO existe el archivo original:**
- ✅ Esperar sincronización OneDrive (el archivo está commiteado)
- ✅ Luego crear la versión Cloud (PASO 1.1)

---

## 🧪 PASO 4: Testing MCP Servers

### **Test 1: nexus-cerebro-hope (MCP CEREBRO Cloud)**

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
  "api_base_url": "https://nexus-cerebro-api.fly.dev",
  "status": "operational"
}
```

**⚠️ CRÍTICO:** Verificar que `api_base_url` muestra `https://nexus-cerebro-api.fly.dev` (Cloud), NO `localhost`.

**Si falla:**
- Verificar que Node.js está instalado (`node --version`)
- Verificar que archivo `nexus-memory-mcp-server-v3-hope-cloud.js` existe
- Verificar que modificaste el archivo para apuntar a Fly.io (PASO 1.1)
- Verificar conectividad: `curl https://nexus-cerebro-api.fly.dev/health`
- Verificar que path en .mcp.json apunta a `-cloud.js` NO al original

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

# 2. Verificar archivos MCP server de NEXUS (original + cloud)
ls -la /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/mcp_server/nexus-memory-mcp-server-v3-hope*.js

# 3. Verificar que archivo Cloud apunta a Fly.io
grep "NEXUS_API_LOCAL" /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/mcp_server/nexus-memory-mcp-server-v3-hope-cloud.js

# 4. Verificar conectividad a CEREBRO Cloud
curl https://nexus-cerebro-api.fly.dev/health

# 5. Verificar Node.js
node --version

# 6. Verificar NPM
npm --version

# 7. Verificar variable entorno Hostinger
echo $HOSTINGER_API_TOKEN

# 8. Test manual del MCP server Cloud
node /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/mcp_server/nexus-memory-mcp-server-v3-hope-cloud.js --version
```

**Guardar output:**
```bash
# Crear reporte de diagnóstico
cat > /tmp/mcp-diagnostic-laptop.txt << EOF
=== MCP Diagnostic Report - NEXUS-Laptop (Cloud) ===

1. .mcp.json exists: $(ls -la /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/.mcp.json 2>&1)

2. MCP server files:
   - Original: $(ls -la /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/mcp_server/nexus-memory-mcp-server-v3-hope.js 2>&1 | grep -o '[0-9]*K')
   - Cloud: $(ls -la /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/mcp_server/nexus-memory-mcp-server-v3-hope-cloud.js 2>&1 | grep -o '[0-9]*K')

3. Cloud API URL: $(grep "NEXUS_API_LOCAL" /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/mcp_server/nexus-memory-mcp-server-v3-hope-cloud.js 2>&1)

4. CEREBRO Cloud health: $(curl -s https://nexus-cerebro-api.fly.dev/health | jq -r '.status' 2>&1)

5. Node.js version: $(node --version 2>&1)

6. NPM version: $(npm --version 2>&1)

7. Hostinger token: $(echo $HOSTINGER_API_TOKEN | sed 's/\(.\{4\}\).*/\1.../' 2>&1)

EOF

cat /tmp/mcp-diagnostic-laptop.txt
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

### **Error: "MCP server crashed" (NEXUS CEREBRO Cloud)**

**Problema:** No puede conectarse a CEREBRO Cloud en Fly.io

**Solución:**
```bash
# 1. Verificar conectividad a Fly.io
curl https://nexus-cerebro-api.fly.dev/health

# Si responde con {"status":"healthy","version":"3.0.0"}: ✅ Cloud está UP
# Si NO responde o timeout: ❌ Problema de conectividad

# 2. Si Cloud está DOWN, verificar con flyctl (si tienes acceso):
flyctl status -a nexus-cerebro-api

# 3. Si no responde, verificar que usaste archivo CLOUD:
grep "nexus-cerebro-api.fly.dev" /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/mcp_server/nexus-memory-mcp-server-v3-hope-cloud.js

# Si muestra "localhost" → ❌ NO modificaste el archivo (vuelve a PASO 1.1)
# Si muestra "nexus-cerebro-api.fly.dev" → ✅ Correcto
```

---

### **Error: "Connection refused" o "ECONNREFUSED"**

**Problema:** Intentando conectarse a localhost cuando deberías usar Cloud

**Solución:**
```bash
# Verificar que .mcp.json apunta al archivo Cloud
cat /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/.mcp.json | grep "cloud.js"

# Debe mostrar: ...nexus-memory-mcp-server-v3-hope-cloud.js
# Si muestra solo "hope.js" (sin "cloud"): ❌ Estás usando archivo PC

# Corregir:
# Editar .mcp.json y cambiar:
# ANTES: "nexus-memory-mcp-server-v3-hope.js"
# DESPUÉS: "nexus-memory-mcp-server-v3-hope-cloud.js"
```

---

### **Error: "SSL certificate problem" o "certificate verify failed"**

**Problema:** Problema con certificados SSL de Fly.io

**Solución:**
```bash
# Verificar que puedes acceder a Fly.io con curl
curl -v https://nexus-cerebro-api.fly.dev/health

# Si falla con SSL error, actualizar certificados:
sudo apt update
sudo apt install ca-certificates -y
sudo update-ca-certificates

# Probar de nuevo
curl https://nexus-cerebro-api.fly.dev/health
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
- [ ] Ver archivo `nexus-memory-mcp-server-v3-hope.js` (87KB) - ORIGINAL
- [ ] Ver archivo `nexus-memory-mcp-server-v3-hope-cloud.js` (87KB) - CLOUD ⭐
- [ ] Archivo Cloud apunta a `https://nexus-cerebro-api.fly.dev` (verificado con grep)
- [ ] `.mcp.json` apunta al archivo `-cloud.js` NO al original
- [ ] Node.js instalado (`node --version`)
- [ ] NPM instalado (`npm --version`)
- [ ] Variable `HOSTINGER_API_TOKEN` exportada (`echo $HOSTINGER_API_TOKEN`)
- [ ] Conectividad a Cloud: `curl https://nexus-cerebro-api.fly.dev/health` responde
- [ ] MCP `nexus-cerebro-hope` carga exitosamente en Claude Code
- [ ] MCP `hostinger-mcp` carga exitosamente en Claude Code
- [ ] Herramientas MCP disponibles (ejecutar `mcp__nexus-cerebro-hope__nexus_system_info`)
- [ ] `nexus_system_info` muestra `api_base_url: "https://nexus-cerebro-api.fly.dev"` ⭐

---

## 🎯 Workflow Final

**Al iniciar Claude Code:**

```bash
cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0
clp

# Claude Code debe:
# 1. Detectar .mcp.json automáticamente
# 2. Cargar nexus-cerebro-hope (MCP CEREBRO Cloud - Fly.io)
# 3. Cargar hostinger-mcp (Hostinger API)
# 4. Mostrar 50+ herramientas disponibles

# Testear con:
mcp__nexus-cerebro-hope__nexus_system_info

# VERIFICAR OUTPUT:
# api_base_url: "https://nexus-cerebro-api.fly.dev" ← DEBE ser HTTPS Fly.io
# NO debe mostrar "localhost"
```

**Si los MCP servers NO cargan:**
1. Ejecutar diagnóstico completo (PASO 5)
2. Guardar `/tmp/mcp-diagnostic-laptop.txt`
3. Reportar a Ricardo con el output

---

## ⚡ Resumen Rápido

**Diferencia clave: PC usa localhost, Laptop usa Cloud**

```bash
# 1. Crear MCP Cloud
cp config/mcp_server/nexus-memory-mcp-server-v3-hope.js \
   config/mcp_server/nexus-memory-mcp-server-v3-hope-cloud.js

sed -i "s|http://localhost:8013|https://nexus-cerebro-api.fly.dev|g" \
   config/mcp_server/nexus-memory-mcp-server-v3-hope-cloud.js

# 2. Crear .mcp.json apuntando a archivo Cloud (-cloud.js)

# 3. Exportar Hostinger token
export HOSTINGER_API_TOKEN="jkVjPETPxERZcVcpEeiT9wqgWjl7Xcy97Of7GQpN4a23ebab"

# 4. Iniciar Claude Code
clp

# 5. Testear
mcp__nexus-cerebro-hope__nexus_system_info
# Debe mostrar: api_base_url: "https://nexus-cerebro-api.fly.dev"
```

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
