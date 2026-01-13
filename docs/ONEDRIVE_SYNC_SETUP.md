# 📦 OneDrive Sync Completo - D:\01_PROYECTOS_ACTIVOS\

**Fecha:** 2026-01-13
**Por:** NEXUS-PC + Ricardo
**Objetivo:** Sincronizar automáticamente TODOS los proyectos entre PC y Laptop vía OneDrive

---

## 🎯 OBJETIVO FINAL

```
PC (Home Base):
D:\01_PROYECTOS_ACTIVOS\
├─ CEREBRO_NEXUS_V3.0.0
├─ NEXUS_SUITE
├─ PDF_SUITE
├─ [22 proyectos total]
└─ ... (trabajas aquí normalmente)

        ↓ OneDrive Sync Automático ↓

OneDrive Cloud (2TB):
OneDrive\01_PROYECTOS_ACTIVOS\
├─ [Espejo automático de D:\]
├─ Sincronización continua
└─ Backup en tiempo real

        ↓ OneDrive Sync Automático ↓

Laptop (Remote):
D:\01_PROYECTOS_ACTIVOS\ (vía OneDrive)
├─ Todos los proyectos disponibles
├─ Cambios sincronizados automáticamente
└─ CEREBRO Cloud (Fly.io) para PostgreSQL
```

---

## 📋 PLAN DE IMPLEMENTACIÓN

### **FASE 1: Preparación (PC)**

#### **PASO 1.1: Verificar Espacio Disponible**

**En Windows PowerShell (PC):**
```powershell
# Verificar tamaño de D:\01_PROYECTOS_ACTIVOS\
Get-ChildItem -Path "D:\01_PROYECTOS_ACTIVOS" -Recurse -File |
  Measure-Object -Property Length -Sum |
  Select-Object @{Name="Size(GB)";Expression={[math]::Round($_.Sum/1GB,2)}}

# Verificar espacio disponible en OneDrive
# (Actual: 817GB disponibles de 1.9TB)
```

**Verificación desde WSL:**
```bash
# Tamaño aproximado (puede tardar):
du -sh /mnt/d/01_PROYECTOS_ACTIVOS/

# OneDrive disponible:
df -h /mnt/c/Users/ricar/OneDrive | tail -1
```

**Decisión:**
- Si `D:\01_PROYECTOS_ACTIVOS\` < 800GB → ✅ Sync completo OK
- Si > 800GB → ⚠️ Sync selectivo (excluir carpetas pesadas)

---

#### **PASO 1.2: Crear Lista de Exclusiones**

**Carpetas a EXCLUIR de sync (para ahorrar espacio):**

```
# Carpetas grandes y regenerables:
**/node_modules/          # NPM dependencies (regenerables con npm install)
**/venv/                  # Python virtual envs (regenerables)
**/.venv/                 # Python virtual envs alternativo
**/volumes/               # Docker volumes (solo PC necesita)
**/.docker/               # Docker cache (solo PC)

# Build artifacts (regenerables):
**/dist/                  # Build output
**/build/                 # Build output
**/__pycache__/           # Python cache
**/.pytest_cache/         # Pytest cache
**/.mypy_cache/           # Mypy cache

# Logs masivos:
**/logs/*.log             # Log files individuales OK, carpetas masivas NO

# Bases de datos locales (PC usa Docker, Laptop usa Cloud):
**/*.db                   # SQLite databases
**/*.sqlite               # SQLite databases
**/data/postgresql/       # PostgreSQL data directory

# Temporales:
**/.tmp/
**/temp/
**/tmp/

# Git objects (sync .git/ metadata OK, pero no objects grandes):
**/.git/objects/pack/*.pack  # Git packfiles grandes
```

**Total esperado a excluir:** ~30-50% del espacio (estimado)

---

#### **PASO 1.3: Identificar Proyectos Críticos (Prioridad Alta)**

**Proyectos que DEBEN sincronizarse completos (sin exclusiones):**

```
CEREBRO_NEXUS_V3.0.0/     # Memoria persistente (CRÍTICO)
├─ docs/                  # ✅ Sync
├─ config/                # ✅ Sync
├─ scripts/               # ✅ Sync
├─ systemd/               # ✅ Sync
└─ .git/                  # ✅ Sync (metadata)

NEXUS_SUITE/              # Suite production (CRÍTICO)
├─ docs/                  # ✅ Sync
├─ src/                   # ✅ Sync
├─ tests/                 # ✅ Sync
└─ .git/                  # ✅ Sync
```

**Proyectos con exclusiones OK:**
```
PDF_SUITE/
├─ src/                   # ✅ Sync
├─ node_modules/          # ❌ Excluir (npm install en Laptop)
└─ dist/                  # ❌ Excluir (regenerable)

NEXUS_CREW/
├─ src/                   # ✅ Sync
├─ venv/                  # ❌ Excluir (pip install en Laptop)
└─ __pycache__/           # ❌ Excluir (regenerable)
```

---

### **FASE 2: Configuración OneDrive (PC - Windows GUI)**

#### **PASO 2.1: Abrir Configuración OneDrive**

**En Windows (PC):**

1. **Click derecho en ícono OneDrive** (bandeja sistema, esquina inferior derecha)
   - Si no ves el ícono → Windows search: "OneDrive"

2. **Seleccionar: "Settings" o "Configuración"**

3. **Ir a pestaña: "Backup" o "Copia de seguridad"**

---

#### **PASO 2.2: Agregar D:\01_PROYECTOS_ACTIVOS\ a OneDrive**

**Opción A: Usar "Choose folders" (Recomendado)**

1. **En OneDrive Settings → Tab "Account" → "Choose folders"**

2. **Click "Add folder"**

3. **Navegar a:** `D:\01_PROYECTOS_ACTIVOS\`

4. **Seleccionar carpeta completa**

5. **Click "Select Folder" o "Seleccionar"**

6. **OneDrive comenzará a sincronizar** (puede tardar minutos/horas dependiendo del tamaño)

---

**Opción B: Mover D:\ dentro de OneDrive (Alternativa)**

**⚠️ Solo si quieres que D:\01_PROYECTOS_ACTIVOS\ VIVA dentro de OneDrive:**

```powershell
# En PowerShell como Administrador:

# 1. Mover carpeta a OneDrive
Move-Item -Path "D:\01_PROYECTOS_ACTIVOS" -Destination "C:\Users\ricar\OneDrive\01_PROYECTOS_ACTIVOS"

# 2. Crear symbolic link en D:\
New-Item -ItemType SymbolicLink -Path "D:\01_PROYECTOS_ACTIVOS" -Target "C:\Users\ricar\OneDrive\01_PROYECTOS_ACTIVOS"
```

**Ventaja Opción B:** Garantiza que TODO pasa por OneDrive (sync perfecto)
**Desventaja Opción B:** Requiere mover archivos (riesgo si falla)

**Recomendación:** Usar Opción A primero (más seguro)

---

#### **PASO 2.3: Excluir Carpetas Pesadas**

**Después de que OneDrive inicie sync:**

**Método 1: OneDrive GUI (Individual)**

1. **Navegar a:** `C:\Users\ricar\OneDrive\01_PROYECTOS_ACTIVOS\[PROYECTO]\node_modules\`

2. **Click derecho en carpeta** → "Free up space"
   - Esto marca la carpeta como "Online-only" (no descarga en PC, pero está en cloud)

3. **Repetir para:**
   - Cada `node_modules/`
   - Cada `venv/`
   - Cada `volumes/`
   - Cada `dist/`, `build/`, `__pycache__/`

**Método 2: PowerShell Script (Batch)**

```powershell
# Script para marcar carpetas como Online-only (sin descargar localmente)
# IMPORTANTE: Esto NO evita que se suban a cloud, solo que NO se descarguen en otros dispositivos

$excludeFolders = @(
    "node_modules",
    "venv",
    ".venv",
    "volumes",
    "__pycache__",
    "dist",
    "build"
)

Get-ChildItem -Path "C:\Users\ricar\OneDrive\01_PROYECTOS_ACTIVOS" -Recurse -Directory |
  Where-Object { $excludeFolders -contains $_.Name } |
  ForEach-Object {
    Write-Host "Marcando como Online-only: $($_.FullName)"
    # Usar attrib +U para Files On-Demand
    attrib +U "$($_.FullName)" /S /D
  }
```

**⚠️ IMPORTANTE:**
- "Free up space" NO evita subir a cloud (ya está subido)
- Solo evita DESCARGAR en otros dispositivos
- Para NO SUBIR ciertas carpetas, usa `.onedriveignore` (ver Paso 2.4)

---

#### **PASO 2.4: Crear .onedriveignore (Evitar Subir Carpetas)**

**⚠️ OneDrive NO soporta `.onedriveignore` nativamente como Git**

**Alternativa 1: Usar File Attributes (Windows)**

```powershell
# Marcar carpetas como "Offline" ANTES de que OneDrive las detecte:
$excludeFolders = @("node_modules", "venv", "volumes", "__pycache__", "dist")

Get-ChildItem -Path "D:\01_PROYECTOS_ACTIVOS" -Recurse -Directory |
  Where-Object { $excludeFolders -contains $_.Name } |
  ForEach-Object {
    # Marcar como System + Hidden (OneDrive puede ignorar)
    $_.Attributes = 'Hidden,System'
  }
```

**Alternativa 2: Configurar OneDrive Settings**

1. **OneDrive Settings → "Advanced" → "Files On-Demand"**
2. Habilitar "Save space and download files as you use them"
3. OneDrive sincroniza METADATA pero no archivos completos (ahorra espacio)

**Alternativa 3: Crear script de exclusión manual**

```bash
# En WSL, crear lista de exclusiones:
cat > /mnt/d/01_PROYECTOS_ACTIVOS/.onedrive-exclude << 'EOF'
# OneDrive Exclusion List (manual reference)
node_modules/
venv/
.venv/
volumes/
.docker/
dist/
build/
__pycache__/
.pytest_cache/
.mypy_cache/
logs/*.log
*.db
*.sqlite
data/postgresql/
.tmp/
temp/
tmp/
.git/objects/pack/*.pack
EOF
```

**Luego usar este script para mover esas carpetas fuera de sync:**

```bash
#!/bin/bash
# move-excluded-from-sync.sh

PROJECTS_DIR="/mnt/d/01_PROYECTOS_ACTIVOS"
EXCLUDED_DIR="/mnt/d/01_PROYECTOS_ACTIVOS_LOCAL_ONLY"

mkdir -p "$EXCLUDED_DIR"

# Mover node_modules/ a local-only
find "$PROJECTS_DIR" -type d -name "node_modules" | while read dir; do
    rel_path="${dir#$PROJECTS_DIR/}"
    mkdir -p "$EXCLUDED_DIR/$(dirname "$rel_path")"
    mv "$dir" "$EXCLUDED_DIR/$rel_path"
    # Crear symlink para que proyectos funcionen
    ln -s "$EXCLUDED_DIR/$rel_path" "$dir"
done

echo "Carpetas excluidas movidas a $EXCLUDED_DIR"
```

**Ventaja:** OneDrive NO sincroniza los archivos reales (solo symlinks metadata)
**Desventaja:** Laptop NO tendrá esas carpetas (debe regenerarlas)

---

### **FASE 3: Verificación (PC)**

#### **PASO 3.1: Monitorear Progreso de Sync**

**OneDrive muestra progreso en:**
1. Ícono OneDrive (bandeja sistema) → "Syncing X files..."
2. Barra de progreso en configuración

**En WSL, verificar archivos sincronizándose:**
```bash
# Ver archivos en OneDrive:
ls -lah /mnt/c/Users/ricar/OneDrive/01_PROYECTOS_ACTIVOS/

# Comparar con D:\:
diff -r /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/ \
         /mnt/c/Users/ricar/OneDrive/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/ \
         --brief | head -20
```

**Tiempo estimado sync inicial:**
- Proyectos pequeños (<1GB): 10-30 min
- Proyectos medianos (1-10GB): 1-3 horas
- Proyectos grandes (>10GB): 3-12 horas

---

#### **PASO 3.2: Verificar Exclusiones Funcionan**

```bash
# Verificar que node_modules/ NO se sincronizó:
find /mnt/c/Users/ricar/OneDrive/01_PROYECTOS_ACTIVOS/ -type d -name "node_modules" | wc -l
# Esperado: 0 (si exclusiones funcionaron)

# Verificar que src/ SÍ se sincronizó:
find /mnt/c/Users/ricar/OneDrive/01_PROYECTOS_ACTIVOS/ -type d -name "src" | wc -l
# Esperado: >0 (proyectos con src/)
```

---

### **FASE 4: Configuración Laptop**

#### **PASO 4.1: Esperar Sync Completo en PC**

**ANTES de configurar Laptop:**
- ✅ Verificar que OneDrive en PC terminó sync inicial
- ✅ Verificar que archivos están en OneDrive cloud (web.onedrive.com)
- ✅ Verificar que exclusiones funcionan

---

#### **PASO 4.2: Configurar OneDrive en Laptop**

**En Laptop (Windows):**

1. **Iniciar sesión en OneDrive** (misma cuenta: ricardo@...)

2. **OneDrive Settings → "Choose folders"**

3. **Seleccionar:** `01_PROYECTOS_ACTIVOS` (completo)

4. **OneDrive descargará automáticamente** archivos desde cloud

---

#### **PASO 4.3: Configurar Files On-Demand (Laptop)**

**Para ahorrar espacio en Laptop:**

1. **OneDrive Settings → "Advanced"**

2. **Habilitar: "Files On-Demand"**
   - Archivos se descargan solo cuando los abres
   - Ahorra espacio en SSD de Laptop

3. **Marcar proyectos CRÍTICOS como "Always keep on this device":**
   - `CEREBRO_NEXUS_V3.0.0/` → Click derecho → "Always keep on this device"
   - `NEXUS_SUITE/` → Idem

4. **Dejar otros proyectos como "Online-only":**
   - Se descargan on-demand cuando los necesites

---

#### **PASO 4.4: Regenerar Dependencias en Laptop**

**Para proyectos con node_modules/ o venv/ excluidos:**

```bash
# En Laptop:
cd D:\01_PROYECTOS_ACTIVOS\PDF_SUITE\

# Regenerar node_modules:
npm install

# Para proyectos Python:
cd D:\01_PROYECTOS_ACTIVOS\NEXUS_CREW\
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

### **FASE 5: Testing y Validación**

#### **PASO 5.1: Test Sync PC → Laptop**

**En PC:**
```bash
# Crear archivo de prueba:
echo "Test sync PC → Laptop $(date)" > /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/TEST_SYNC_PC.txt

# OneDrive sincroniza automáticamente (esperar 30-60 segundos)
```

**En Laptop (después de 1-2 minutos):**
```bash
# Verificar que archivo existe:
cat D:\01_PROYECTOS_ACTIVOS\CEREBRO_NEXUS_V3.0.0\TEST_SYNC_PC.txt
# Esperado: "Test sync PC → Laptop [fecha]"
```

---

#### **PASO 5.2: Test Sync Laptop → PC**

**En Laptop:**
```bash
# Crear archivo de prueba:
echo "Test sync Laptop → PC $(date)" > D:\01_PROYECTOS_ACTIVOS\CEREBRO_NEXUS_V3.0.0\TEST_SYNC_LAPTOP.txt

# OneDrive sincroniza automáticamente (esperar 30-60 segundos)
```

**En PC (después de 1-2 minutos):**
```bash
# Verificar que archivo existe:
cat /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/TEST_SYNC_LAPTOP.txt
# Esperado: "Test sync Laptop → PC [fecha]"
```

---

#### **PASO 5.3: Test Conflictos (Edición Simultánea)**

**Simular conflicto:**

**En PC:**
```bash
echo "Versión PC" > /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/TEST_CONFLICT.txt
```

**En Laptop (ANTES de que sync llegue desde PC):**
```bash
echo "Versión Laptop" > D:\01_PROYECTOS_ACTIVOS\CEREBRO_NEXUS_V3.0.0\TEST_CONFLICT.txt
```

**Resultado esperado:**
- OneDrive detecta conflicto
- Crea `TEST_CONFLICT - copia en conflicto.txt` en ambos dispositivos
- RESOLVER MANUALMENTE: Revisar ambas versiones, quedarte con una, borrar la otra

**Regla para evitar conflictos:**
- PC = escritura principal
- Laptop = lectura mayormente, edits ocasionales
- Comunicar cuando editarás en Laptop

---

### **FASE 6: Workflow Post-Setup**

#### **Workflow Normal PC:**

```bash
# 1. Trabajar normalmente en D:\
cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0
# ... hacer cambios ...

# 2. Commit a Git (opcional pero recomendado)
git add .
git commit -m "feat: nueva feature"
git push origin main

# 3. OneDrive sincroniza AUTOMÁTICAMENTE (sin hacer nada)
# Esperar 30-60 segundos
# Laptop ya tiene los cambios
```

---

#### **Workflow Normal Laptop:**

```bash
# 1. OneDrive YA sincronizó cambios desde PC
cd D:\01_PROYECTOS_ACTIVOS\CEREBRO_NEXUS_V3.0.0

# 2. Trabajar con archivos actualizados
# ... leer, editar, ejecutar ...

# 3. Si haces cambios:
git add .
git commit -m "fix: corrección desde Laptop"
git push origin main

# 4. OneDrive sincroniza AUTOMÁTICAMENTE a PC
# PC verá cambios en 30-60 segundos
```

---

### **FASE 7: Mantenimiento**

#### **Limpieza Periódica (Mensual)**

```bash
# Verificar espacio usado en OneDrive:
df -h /mnt/c/Users/ricar/OneDrive

# Limpiar archivos temporales antes de sync:
find /mnt/d/01_PROYECTOS_ACTIVOS/ -name "*.log" -size +100M -delete
find /mnt/d/01_PROYECTOS_ACTIVOS/ -name "*.tmp" -delete
find /mnt/d/01_PROYECTOS_ACTIVOS/ -type d -name "__pycache__" -exec rm -rf {} +
```

---

#### **Verificar Sincronización (Semanal)**

```bash
# Script de verificación:
#!/bin/bash
# verify-onedrive-sync.sh

PROJECTS_DIR="/mnt/d/01_PROYECTOS_ACTIVOS"
ONEDRIVE_DIR="/mnt/c/Users/ricar/OneDrive/01_PROYECTOS_ACTIVOS"

echo "Verificando sincronización OneDrive..."

# Comparar número de archivos:
PC_COUNT=$(find "$PROJECTS_DIR" -type f | wc -l)
OD_COUNT=$(find "$ONEDRIVE_DIR" -type f | wc -l)

echo "Archivos en D:\: $PC_COUNT"
echo "Archivos en OneDrive: $OD_COUNT"

if [ $PC_COUNT -eq $OD_COUNT ]; then
    echo "✅ Sincronización OK"
else
    echo "⚠️ Diferencia detectada: $((PC_COUNT - OD_COUNT)) archivos"
fi

# Verificar archivos críticos:
CRITICAL_FILES=(
    "CEREBRO_NEXUS_V3.0.0/README.md"
    "NEXUS_SUITE/PROJECT_ID.md"
)

for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$ONEDRIVE_DIR/$file" ]; then
        echo "✅ $file sincronizado"
    else
        echo "❌ $file NO sincronizado"
    fi
done
```

---

## 🎯 CHECKLIST FINAL

### **Setup Completo Cuando:**

- [ ] OneDrive sincroniza D:\01_PROYECTOS_ACTIVOS\ en PC
- [ ] Exclusiones configuradas (node_modules, venv, volumes)
- [ ] OneDrive sincroniza en Laptop
- [ ] Files On-Demand habilitado en Laptop
- [ ] Test PC → Laptop exitoso
- [ ] Test Laptop → PC exitoso
- [ ] Test conflictos entendido
- [ ] Workflow documentado
- [ ] Script de verificación funcionando

---

## 📊 VENTAJAS FINALES

### **PC:**
- ✅ Trabajas en D:\ como siempre (zero cambios)
- ✅ Backup automático en cloud (2TB)
- ✅ Git + OneDrive funcionan juntos

### **Laptop:**
- ✅ Todos los proyectos disponibles automáticamente
- ✅ Cambios sincronizados en tiempo real (~60 segundos)
- ✅ Files On-Demand ahorra espacio en SSD

### **Ambos:**
- ✅ Zero configuración manual de sync
- ✅ Compatible con Git workflow
- ✅ Acceso desde cualquier dispositivo (móvil, web)

---

## ⚠️ TROUBLESHOOTING

### **Problema: OneDrive no sincroniza**

**Verificar:**
```bash
# OneDrive está corriendo:
ps aux | grep -i onedrive

# Espacio suficiente:
df -h /mnt/c/Users/ricar/OneDrive
```

**Soluciones:**
1. Reiniciar OneDrive (bandeja sistema → Exit → Iniciar OneDrive)
2. Verificar conexión a Internet
3. Verificar que carpeta no esté marcada como "Offline"

---

### **Problema: Sync muy lento**

**Causas:**
- Archivos muy grandes (>1GB)
- Muchos archivos pequeños (>100k archivos)
- Conexión lenta

**Soluciones:**
1. Pausar sync de proyectos no críticos
2. Usar Files On-Demand (solo metadata sync)
3. Excluir más carpetas (node_modules, dist, logs)

---

### **Problema: Conflictos frecuentes**

**Causa:** Edición simultánea PC + Laptop

**Solución:**
- Establecer regla: PC = escritura, Laptop = lectura
- O comunicar antes de editar en Laptop
- Usar Git branches para edits en Laptop

---

## 📖 REFERENCIAS

**OneDrive Official Docs:**
- Files On-Demand: https://support.microsoft.com/en-us/office/save-disk-space-with-onedrive-files-on-demand-0e6860d3-d9f3-4971-b321-7092438fb38e
- Sync Settings: https://support.microsoft.com/en-us/office/sync-files-with-onedrive-in-windows-615391c4-2bd3-4aae-a42a-858262e42a49

**Este Documento:**
- Creado: 2026-01-13
- Por: NEXUS-PC + Ricardo
- Ubicación: `docs/ONEDRIVE_SYNC_SETUP.md`

---

**🎯 SIGUIENTE PASO: Ejecutar FASE 2 (Configuración OneDrive en PC)**
