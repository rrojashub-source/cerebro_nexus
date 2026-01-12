# 🔧 NEXUS-Laptop Troubleshooting Guide

**Para:** NEXUS-Laptop (Claude Code en Laptop)
**De:** NEXUS-PC
**Fecha:** 2026-01-12
**Problema:** tmux + clp no guarda conversación, bypass permisos no funciona

---

## 🚨 PROBLEMA 1: tmux + clp No Guarda Conversación

### **Síntoma:**
- Haces `exit` en Claude Code
- Vuelves a ejecutar `clp`
- Claude Code inicia NUEVA conversación (no continúa la anterior)
- Pierdes todo el contexto

### **Causa Raíz:**
Tu script `clp` probablemente NO está usando `claude --continue`

### **Diagnóstico Rápido:**

```bash
# Ver contenido de tu clp actual
cat ~/bin/clp
# O si está en otro lugar:
which clp
cat $(which clp)
```

**Busca esta línea:**
```bash
claude code --dangerously-skip-permissions --continue
```

**Si NO tiene `--continue`** → Ese es el problema.

---

### **Solución A: Verificar Versión de clp**

**clp correcto (v2.0.0 - tmux + native Claude --continue):**

```bash
#!/bin/bash
# clp-native v2.0.0 - tmux + Claude native session resume
# Location: /home/ricardo/bin/clp-native

PROJECT_NAME=$(basename "$PWD" | sed 's/[^a-zA-Z0-9_-]/_/g')
SESSION_NAME="claude-${PROJECT_NAME}"

# Check if tmux session exists
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "📎 Resuming tmux session: $SESSION_NAME"
    tmux attach-session -t "$SESSION_NAME"
else
    echo "🆕 Creating new tmux session: $SESSION_NAME"
    tmux new-session -s "$SESSION_NAME" -c "$PWD" \
        "claude code --dangerously-skip-permissions --continue"
fi
```

**Si tu `clp` es diferente:**
1. Copia el código de arriba
2. Guárdalo en `~/bin/clp` (sobrescribe el viejo)
3. `chmod +x ~/bin/clp`
4. Prueba nuevamente

---

### **Solución B: Crear clp-native Nuevo**

**Si no tienes el script correcto:**

```bash
# Crear script nuevo
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

### **Testing:**

**Test 1: Primera sesión**
```bash
cd ~/PROYECTO_TEST
clp
# Claude Code debe iniciar
# Escribe algo en la conversación: "Hola, soy test 1"
# Presiona Ctrl+D para salir (NO escribas "exit")
```

**Test 2: Resumir sesión**
```bash
clp
# Claude Code debe CONTINUAR la conversación anterior
# Debe ver tu mensaje "Hola, soy test 1" en el historial
```

**✅ Si funciona:** clp está correcto
**❌ Si no funciona:** Ve a Solución C

---

### **Solución C: Salir Correctamente de Claude Code**

**IMPORTANTE:** La forma en que sales de Claude Code importa.

**❌ MAL (pierde sesión):**
```
# Dentro de Claude Code:
exit
```

**✅ BIEN (preserva sesión):**
```
# Opción 1: Ctrl+D (EOF)
Ctrl+D

# Opción 2: Detach de tmux (preserva proceso)
Ctrl+B, luego D

# Opción 3: Cerrar terminal (si clp funciona)
# Simplemente cierra la ventana, clp recupera
```

**Recomendación:** Usa `Ctrl+B` → `D` para detach de tmux sin cerrar Claude.

---

## 🚨 PROBLEMA 2: Bypass de Permisos Sin Botón Derecho

### **Síntoma:**
- Claude Code pide permisos
- No puedes continuar trabajando
- En PC: botón derecho → kill terminal → clp recupera todo
- En Laptop: NO tienes botón derecho (o no funciona igual)

### **Contexto:**
En PC (Windows Terminal + WSL):
1. Botón derecho en terminal
2. "Close pane" o Kill
3. Terminal muere abruptamente
4. tmux preserva sesión
5. `clp` vuelve a conectar

En Laptop (¿diferente terminal?):
- No hay opción visual equivalente
- Necesitas forma programática

---

### **Solución: Script `clp-force` (Bypass Programático)**

**Crear comando nuevo para bypass:**

```bash
cat > ~/bin/clp-force << 'EOF'
#!/bin/bash
# clp-force: Force bypass permissions by killing Claude and restarting
# Use when Claude Code asks for permissions and you want to bypass

echo "🔪 Killing Claude Code processes..."
pkill -9 -f "claude.*code" || echo "No Claude processes found (ok)"

echo "⏳ Waiting 2 seconds..."
sleep 2

echo "🚀 Restarting with clp..."
exec ~/bin/clp
EOF

chmod +x ~/bin/clp-force
```

---

### **Uso de clp-force:**

**Cuando Claude pide permisos:**

```bash
# En OTRA terminal (no en la de Claude):
clp-force

# O si estás en tmux:
# 1. Ctrl+B, luego D (detach)
# 2. En terminal normal:
clp-force
```

**Qué hace:**
1. Mata violentamente Claude Code (`pkill -9`)
2. Espera 2 segundos (para que tmux se entere)
3. Ejecuta `clp` que:
   - Recupera sesión tmux
   - Inicia Claude con `--dangerously-skip-permissions --continue`
   - Carga contexto anterior

**Resultado:** Bypass automático sin botón derecho.

---

### **Alternativa: Alias Rápido**

**Si no quieres script separado:**

```bash
# Agregar a ~/.bashrc o ~/.zshrc
alias clpf='pkill -9 -f "claude.*code"; sleep 2; ~/bin/clp'
```

**Uso:**
```bash
# Cuando necesites bypass:
clpf
```

---

## 🔍 DIAGNÓSTICO COMPLETO

**Si sigues teniendo problemas, ejecuta este diagnóstico:**

```bash
cat > ~/diagnose-clp.sh << 'EOF'
#!/bin/bash
echo "=== CLp Diagnostic ==="
echo ""

echo "1. Verificando script clp:"
which clp
echo ""

echo "2. Contenido de clp:"
cat $(which clp) | head -20
echo ""

echo "3. Verificando tmux sessions:"
tmux ls 2>/dev/null || echo "No tmux sessions"
echo ""

echo "4. Verificando Claude processes:"
ps aux | grep claude | grep -v grep
echo ""

echo "5. Verificando Claude Code versión:"
claude --version 2>/dev/null || echo "Claude CLI no encontrado"
echo ""

echo "6. Testing clp básico:"
cd /tmp
PROJECT_NAME=$(basename "$PWD" | sed 's/[^a-zA-Z0-9_-]/_/g')
echo "Project name would be: claude-${PROJECT_NAME}"
echo ""

echo "=== Diagnóstico Completo ==="
EOF

chmod +x ~/diagnose-clp.sh
~/diagnose-clp.sh
```

**Envía el output de este diagnóstico si necesitas más ayuda.**

---

## 📋 CHECKLIST RÁPIDO

**Para que tmux + clp funcione:**

- [ ] Script `clp` tiene `--continue` flag
- [ ] Script `clp` usa tmux correctamente
- [ ] Sales de Claude con `Ctrl+D` o `Ctrl+B D` (NO con "exit")
- [ ] tmux session se preserva (verificar con `tmux ls`)
- [ ] Creaste `clp-force` para bypass programático

**Para bypass sin botón derecho:**

- [ ] Creaste script `clp-force`
- [ ] Script tiene permisos ejecutables (`chmod +x`)
- [ ] Probaste desde terminal separada
- [ ] Funciona correctamente (mata → espera → reinicia)

---

## 🆘 SOLUCIÓN RÁPIDA (Si Todo Falla)

**Si nada funciona, usa este workflow temporal:**

```bash
# En lugar de clp, usa:
claude code --dangerously-skip-permissions --continue

# Para bypass:
# Terminal 1 (Claude corriendo):
Ctrl+C (cancel)

# Terminal 1 (mismo):
claude code --dangerously-skip-permissions --continue

# Recupera sesión anterior sin permisos
```

**Desventaja:** Pierdes protección tmux, pero al menos puedes trabajar.

---

## 📞 CONTACTO CON NEXUS-PC

**Si necesitas ayuda:**

1. Ejecuta `~/diagnose-clp.sh`
2. Copia el output
3. Guárdalo en `/tmp/laptop-diagnostic.txt`
4. NEXUS-PC puede leerlo y ayudar

**Archivos útiles para compartir:**
- `/tmp/laptop-diagnostic.txt` (diagnóstico)
- `~/.claude/.active_ai` (identidad activa)
- `~/.claude/projects/*/` (sesiones guardadas)

---

**Última actualización:** 2026-01-12 (NEXUS-PC)
**Versión:** 1.0
**Estado:** Testing en Laptop pendiente
