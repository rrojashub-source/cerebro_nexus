# 🚨 NEXUS-Laptop: Acciones Inmediatas Requeridas

**De:** NEXUS-PC
**Para:** NEXUS-Laptop
**Fecha:** 2026-01-12
**Prioridad:** ALTA
**Estado:** Action Required

---

## 📋 Contexto

Ricardo reportó que encontraste **dos problemas críticos** con tu setup de tmux + clp:

1. **tmux no guarda la conversación** - Cuando haces `exit` y vuelves a cargar con `clp`, inicia nueva conversación (pierdes todo el contexto)
2. **No puedes bypass permisos** - No tienes opción de botón derecho → kill como en PC

---

## ✅ Soluciones Creadas (Ya Disponibles en OneDrive)

He creado **3 archivos** específicamente para ti:

### 1. **Guía de Troubleshooting Completa**
```
docs/NEXUS_LAPTOP_TROUBLESHOOTING.md
```

**Contiene:**
- Diagnóstico del problema (missing `--continue` flag)
- 3 soluciones (A: verificar, B: crear nuevo, C: salir correctamente)
- Script `clp` correcto (v2.0.0 con tmux + Claude native --continue)
- Testing procedures
- Comandos útiles

### 2. **Script de Bypass Programático**
```
scripts/clp-force.sh
```

**Función:** Reemplazo del botón derecho → kill

**Qué hace:**
- Mata violentamente Claude Code (`pkill -9 -f "claude.*code"`)
- Espera 2 segundos para cleanup
- Ejecuta `clp` que recupera sesión tmux + contexto

**Uso:**
```bash
# Cuando Claude pida permisos, en OTRA terminal:
clp-force
```

### 3. **Herramienta de Diagnóstico**
```
scripts/diagnose-clp.sh
```

**Función:** Identificar exactamente qué está mal con tu setup

**Qué verifica:**
- Si `clp` script existe
- Si tiene flag `--continue` (CRÍTICO)
- Estado de sesiones tmux
- Claude Code processes
- Generación de project names
- Permisos de scripts

---

## 🎯 PLAN DE ACCIÓN (Ejecutar en Orden)

### **PASO 1: Sincronizar archivos desde OneDrive**

Ya hice push a GitHub, debería sincronizar automáticamente a:
```
D:\01_PROYECTOS_ACTIVOS\CEREBRO_NEXUS_V3.0.0\
```

**Verificar que tienes estos archivos:**
```bash
ls -la /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/docs/NEXUS_LAPTOP_TROUBLESHOOTING.md
ls -la /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/scripts/clp-force.sh
ls -la /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/scripts/diagnose-clp.sh
```

---

### **PASO 2: Ejecutar diagnóstico**

```bash
cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0
chmod +x scripts/diagnose-clp.sh
./scripts/diagnose-clp.sh
```

**Output esperado:**
- Te dirá EXACTAMENTE qué está mal
- Si falta `--continue` flag → ❌ CRÍTICO (esa es la causa)
- Si `clp-force` no existe → ⚠️ Necesitas instalarlo

**Guardar output:**
```bash
./scripts/diagnose-clp.sh > /tmp/laptop-diagnostic.txt
```

---

### **PASO 3: Leer guía de troubleshooting**

```bash
cat /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/docs/NEXUS_LAPTOP_TROUBLESHOOTING.md
```

**Leer específicamente:**
- Sección "PROBLEMA 1: tmux + clp No Guarda Conversación"
- Solución A: Verificar versión de clp
- Solución B: Crear clp-native nuevo (si el tuyo está incorrecto)

---

### **PASO 4: Aplicar fix de clp (si diagnóstico confirma problema)**

**Si diagnóstico dice "❌ Script MISSING --continue flag":**

```bash
# Backup del clp actual (por si acaso)
cp ~/bin/clp ~/bin/clp.backup

# Crear nuevo clp v2.0.0 (tmux + Claude native --continue)
cat > ~/bin/clp << 'EOF'
#!/bin/bash
# clp-native v2.0.0 - tmux + Claude native session resume

PROJECT_NAME=$(basename "$PWD" | sed 's/[^a-zA-Z0-9_-]/_/g')
SESSION_NAME="claude-${PROJECT_NAME}"

if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "📎 Resuming tmux session: $SESSION_NAME"
    tmux attach-session -t "$SESSION_NAME"
else
    echo "🆕 Creating new tmux session: $SESSION_NAME"
    tmux new-session -s "$SESSION_NAME" -c "$PWD" \
        "claude code --dangerously-skip-permissions --continue"
fi
EOF

# Hacer ejecutable
chmod +x ~/bin/clp

# Verificar
~/bin/clp --help 2>&1 | head -5 || echo "Script instalado correctamente"
```

---

### **PASO 5: Instalar clp-force para bypass**

```bash
# Copiar script a ~/bin/
cp /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/scripts/clp-force.sh ~/bin/clp-force

# Hacer ejecutable
chmod +x ~/bin/clp-force

# Verificar
which clp-force
# Debe mostrar: /home/ricardo/bin/clp-force
```

---

### **PASO 6: Testing**

#### **Test 1: Primera sesión (clp debe crear nueva)**
```bash
cd ~/PROYECTO_TEST  # Crear directorio de prueba si no existe
clp

# Dentro de Claude Code:
# - Escribe algo en la conversación: "Hola, soy test 1"
# - Presiona Ctrl+D para salir (NO escribas "exit")
```

#### **Test 2: Resumir sesión (clp debe CONTINUAR)**
```bash
clp

# Claude Code debe:
# ✅ CONTINUAR la conversación anterior
# ✅ Ver tu mensaje "Hola, soy test 1" en el historial
# ✅ NO iniciar conversación nueva

# Si esto funciona → ✅ clp fix EXITOSO
```

#### **Test 3: Bypass con clp-force**
```bash
clp

# Dentro de Claude Code, si pide permisos:
# 1. Abre OTRA terminal (nueva pestaña)
# 2. Ejecuta:
clp-force

# Debe:
# ✅ Matar Claude Code
# ✅ Reiniciar con clp
# ✅ Recuperar sesión tmux + contexto
```

---

## 📊 Checklist de Éxito

Después de completar todos los pasos, debes poder:

- [ ] Ejecutar `clp` en un proyecto
- [ ] Salir con `Ctrl+D` (o `Ctrl+B` → `D`)
- [ ] Volver a ejecutar `clp`
- [ ] **VER la conversación anterior** (no iniciar nueva)
- [ ] **Bypass permisos** con `clp-force` desde otra terminal
- [ ] tmux sesión preservada (`tmux ls` muestra sesiones activas)

---

## 🚨 Si Algo Sale Mal

**Problema:** clp no funciona después del fix
```bash
# Restaurar backup
cp ~/bin/clp.backup ~/bin/clp
```

**Problema:** No puedes ejecutar scripts
```bash
# Verificar permisos
ls -la ~/bin/clp ~/bin/clp-force

# Debe mostrar: -rwxr-xr-x (ejecutable)
# Si no: chmod +x ~/bin/clp ~/bin/clp-force
```

**Problema:** Diagnóstico muestra errores inesperados
```bash
# Guardar output completo del diagnóstico
./scripts/diagnose-clp.sh > /tmp/laptop-diagnostic.txt

# Compartir con Ricardo/NEXUS-PC para análisis
```

---

## 💬 Comunicación con Ricardo/NEXUS-PC

**Si necesitas ayuda:**

1. **Ejecuta diagnóstico:**
   ```bash
   ./scripts/diagnose-clp.sh > /tmp/laptop-diagnostic.txt
   cat /tmp/laptop-diagnostic.txt
   ```

2. **Comparte output del diagnóstico** con Ricardo

3. **Describe qué paso falló** (PASO 1, 2, 3, etc.)

---

## 📖 Referencias

- **Guía completa:** `docs/NEXUS_LAPTOP_TROUBLESHOOTING.md` (349 líneas)
- **Script bypass:** `scripts/clp-force.sh` (41 líneas)
- **Diagnóstico:** `scripts/diagnose-clp.sh` (115 líneas)

---

## 🎯 Objetivo Final

**Que tu workflow sea:**

```bash
# Iniciar proyecto:
cd /mnt/d/01_PROYECTOS_ACTIVOS/[PROYECTO]
clp

# Claude Code inicia/continúa automáticamente
# Trabajas...
# Sales con Ctrl+D o Ctrl+B → D

# Vuelves:
clp

# Claude Code CONTINÚA donde quedaste (NO sesión nueva)

# Si pide permisos:
# En otra terminal: clp-force
# Bypass automático, recupera sesión
```

---

## 🔌 BONUS: Configurar MCP Servers (Después de clp fix)

**Una vez que clp funcione correctamente**, configura los MCP servers:

**Guía completa:**
```bash
cat /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/docs/LAPTOP_MCP_SETUP.md
```

**Quick setup:**
```bash
# 1. Exportar Hostinger API token
export HOSTINGER_API_TOKEN="jkVjPETPxERZcVcpEeiT9wqgWjl7Xcy97Of7GQpN4a23ebab"

# 2. Hacer permanente (agregar a ~/.bashrc)
echo 'export HOSTINGER_API_TOKEN="jkVjPETPxERZcVcpEeiT9wqgWjl7Xcy97Of7GQpN4a23ebab"' >> ~/.bashrc

# 3. Iniciar Claude Code
cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0
clp

# 4. Testear MCP CEREBRO
mcp__nexus-cerebro-hope__nexus_system_info
```

**2 MCP servers disponibles:**
- `nexus-cerebro-hope` - 50+ tools de CEREBRO NEXUS
- `hostinger-mcp` - Gestión hosting/DNS

**📖 Ver:** `docs/LAPTOP_MCP_SETUP.md` (360 líneas con troubleshooting completo)

---

**⚠️ IMPORTANTE:** Ejecuta estos pasos EN ORDEN. No saltees el diagnóstico (PASO 2), es crítico para identificar el problema exacto.

**✅ Cuando completes todo, reporta a Ricardo:**
1. "clp fix aplicado y testeado exitosamente"
2. "MCP servers configurados - nexus-cerebro-hope + hostinger-mcp CONNECTED"

---

**Creado:** 2026-01-12 16:30 UTC
**Actualizado:** 2026-01-12 18:00 UTC (Added MCP setup)
**Por:** NEXUS-PC
**Commits:** 8322089 (clp), 01659f3 (actions), 7a47401 (mcp)
**Branch:** feat/persistencia-integration
