#!/bin/bash
# verify-onedrive-sync.sh
# Verificar sincronización entre D:\ y OneDrive
# Version: 1.0.0
# Date: 2026-01-13

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=================================================="
echo "  OneDrive Sync Verification Tool"
echo "  Version: 1.0.0"
echo "  Date: $(date)"
echo -e "==================================================${NC}"
echo ""

PROJECTS_DIR="/mnt/d/01_PROYECTOS_ACTIVOS"
ONEDRIVE_DIR="/mnt/c/Users/ricar/OneDrive/01_PROYECTOS_ACTIVOS"

# Verificar que directorios existan
if [ ! -d "$PROJECTS_DIR" ]; then
    echo -e "${RED}❌ D:\01_PROYECTOS_ACTIVOS\ no encontrado${NC}"
    exit 1
fi

if [ ! -d "$ONEDRIVE_DIR" ]; then
    echo -e "${YELLOW}⚠️  OneDrive\01_PROYECTOS_ACTIVOS\ no encontrado${NC}"
    echo -e "${YELLOW}   ¿OneDrive sync no configurado todavía?${NC}"
    exit 1
fi

echo -e "${BLUE}1️⃣  Verificando espacio en disco:${NC}"
echo ""
echo "D:\ espacio:"
df -h /mnt/d | tail -1
echo ""
echo "OneDrive espacio:"
df -h /mnt/c/Users/ricar/OneDrive | tail -1
echo ""

echo -e "${BLUE}2️⃣  Contando archivos:${NC}"
echo ""
echo -e "${YELLOW}Contando archivos en D:\... (puede tardar)${NC}"
PC_COUNT=$(find "$PROJECTS_DIR" -type f 2>/dev/null | wc -l)
echo -e "Archivos en D:\: ${GREEN}$PC_COUNT${NC}"
echo ""

echo -e "${YELLOW}Contando archivos en OneDrive... (puede tardar)${NC}"
OD_COUNT=$(find "$ONEDRIVE_DIR" -type f 2>/dev/null | wc -l)
echo -e "Archivos en OneDrive: ${GREEN}$OD_COUNT${NC}"
echo ""

DIFF=$((PC_COUNT - OD_COUNT))
if [ $PC_COUNT -eq $OD_COUNT ]; then
    echo -e "${GREEN}✅ Sincronización perfecta: mismo número de archivos${NC}"
elif [ $DIFF -gt 0 ]; then
    echo -e "${YELLOW}⚠️  PC tiene $DIFF archivos más que OneDrive${NC}"
    echo -e "${YELLOW}   Posiblemente sync en progreso o exclusiones configuradas${NC}"
else
    echo -e "${YELLOW}⚠️  OneDrive tiene $((-DIFF)) archivos más que PC${NC}"
    echo -e "${YELLOW}   Inusual - verificar manualmente${NC}"
fi
echo ""

echo -e "${BLUE}3️⃣  Verificando archivos críticos:${NC}"
echo ""

CRITICAL_FILES=(
    "CEREBRO_NEXUS_V3.0.0/README.md"
    "CEREBRO_NEXUS_V3.0.0/PROJECT_ID.md"
    "CEREBRO_NEXUS_V3.0.0/docs/ONEDRIVE_SYNC_SETUP.md"
    "NEXUS_SUITE/PROJECT_ID.md"
)

for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$PROJECTS_DIR/$file" ]; then
        if [ -f "$ONEDRIVE_DIR/$file" ]; then
            echo -e "  ✅ $file - ${GREEN}sincronizado${NC}"
        else
            echo -e "  ❌ $file - ${RED}NO sincronizado${NC}"
        fi
    else
        echo -e "  ⚠️  $file - ${YELLOW}no existe en PC${NC}"
    fi
done
echo ""

echo -e "${BLUE}4️⃣  Verificando exclusiones (carpetas NO sincronizadas):${NC}"
echo ""

EXCLUDED_DIRS=(
    "node_modules"
    "venv"
    ".venv"
    "volumes"
    "__pycache__"
    "dist"
    "build"
)

for dir in "${EXCLUDED_DIRS[@]}"; do
    PC_FOUND=$(find "$PROJECTS_DIR" -type d -name "$dir" 2>/dev/null | wc -l)
    OD_FOUND=$(find "$ONEDRIVE_DIR" -type d -name "$dir" 2>/dev/null | wc -l)

    if [ $PC_FOUND -gt 0 ] && [ $OD_FOUND -eq 0 ]; then
        echo -e "  ✅ $dir - ${GREEN}correctamente excluido (PC: $PC_FOUND, OneDrive: 0)${NC}"
    elif [ $PC_FOUND -gt 0 ] && [ $OD_FOUND -gt 0 ]; then
        echo -e "  ⚠️  $dir - ${YELLOW}NO excluido (PC: $PC_FOUND, OneDrive: $OD_FOUND)${NC}"
    else
        echo -e "  ℹ️  $dir - ${BLUE}no encontrado en PC${NC}"
    fi
done
echo ""

echo -e "${BLUE}5️⃣  Proyectos sincronizados:${NC}"
echo ""

PC_PROJECTS=$(ls -1 "$PROJECTS_DIR" 2>/dev/null | wc -l)
OD_PROJECTS=$(ls -1 "$ONEDRIVE_DIR" 2>/dev/null | wc -l)

echo -e "Proyectos en PC: ${GREEN}$PC_PROJECTS${NC}"
echo -e "Proyectos en OneDrive: ${GREEN}$OD_PROJECTS${NC}"
echo ""

if [ $PC_PROJECTS -eq $OD_PROJECTS ]; then
    echo -e "${GREEN}✅ Todos los proyectos sincronizados${NC}"
    echo ""
    echo "Proyectos:"
    ls -1 "$PROJECTS_DIR" | head -10
    if [ $PC_PROJECTS -gt 10 ]; then
        echo "... y $((PC_PROJECTS - 10)) más"
    fi
else
    echo -e "${YELLOW}⚠️  Diferencia en número de proyectos${NC}"
fi
echo ""

echo -e "${BLUE}==================================================${NC}"
echo -e "${GREEN}Verificación completa${NC}"
echo ""
echo "📊 Resumen:"
echo "  - Archivos PC: $PC_COUNT"
echo "  - Archivos OneDrive: $OD_COUNT"
echo "  - Diferencia: $DIFF"
echo "  - Proyectos PC: $PC_PROJECTS"
echo "  - Proyectos OneDrive: $OD_PROJECTS"
echo ""

if [ $PC_COUNT -eq $OD_COUNT ] && [ $PC_PROJECTS -eq $OD_PROJECTS ]; then
    echo -e "${GREEN}✅ TODO OK - Sincronización perfecta${NC}"
else
    echo -e "${YELLOW}⚠️  Revisar diferencias arriba${NC}"
fi
echo ""
