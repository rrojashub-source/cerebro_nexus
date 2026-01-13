#!/bin/bash
# check-sync-size.sh
# Verificar tamaño total y recomendar exclusiones
# Version: 1.0.0
# Date: 2026-01-13

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=================================================="
echo "  OneDrive Sync Size Calculator"
echo "  Version: 1.0.0"
echo -e "==================================================${NC}"
echo ""

PROJECTS_DIR="/mnt/d/01_PROYECTOS_ACTIVOS"
ONEDRIVE_AVAILABLE_GB=817  # Actualizar según df -h

echo -e "${BLUE}1️⃣  Verificando espacio disponible en OneDrive:${NC}"
echo ""
ONEDRIVE_INFO=$(df -h /mnt/c/Users/ricar/OneDrive | tail -1)
echo "$ONEDRIVE_INFO"
ONEDRIVE_AVAILABLE=$(echo "$ONEDRIVE_INFO" | awk '{print $4}')
echo -e "Espacio disponible: ${GREEN}$ONEDRIVE_AVAILABLE${NC}"
echo ""

echo -e "${BLUE}2️⃣  Calculando tamaño de proyectos:${NC}"
echo ""
echo -e "${YELLOW}⏳ Calculando... (esto puede tardar varios minutos)${NC}"
echo ""

# Calcular tamaño total
TOTAL_SIZE=$(du -sh "$PROJECTS_DIR" 2>/dev/null | awk '{print $1}')
echo -e "Tamaño total de D:\01_PROYECTOS_ACTIVOS\: ${GREEN}$TOTAL_SIZE${NC}"
echo ""

echo -e "${BLUE}3️⃣  Calculando tamaño de carpetas a excluir:${NC}"
echo ""

EXCLUDE_TOTAL=0

# node_modules/
echo -e "${YELLOW}Calculando node_modules/...${NC}"
NODE_SIZE=$(find "$PROJECTS_DIR" -type d -name "node_modules" -exec du -sh {} + 2>/dev/null | awk '{sum+=$1} END {print sum}')
if [ ! -z "$NODE_SIZE" ]; then
    echo -e "  node_modules/: ${RED}~${NODE_SIZE}MB${NC}"
    EXCLUDE_TOTAL=$((EXCLUDE_TOTAL + NODE_SIZE))
else
    echo -e "  node_modules/: ${BLUE}no encontrado${NC}"
fi

# venv/
echo -e "${YELLOW}Calculando venv/...${NC}"
VENV_SIZE=$(find "$PROJECTS_DIR" -type d -name "venv" -o -name ".venv" -exec du -sh {} + 2>/dev/null | awk '{sum+=$1} END {print sum}')
if [ ! -z "$VENV_SIZE" ]; then
    echo -e "  venv/: ${RED}~${VENV_SIZE}MB${NC}"
    EXCLUDE_TOTAL=$((EXCLUDE_TOTAL + VENV_SIZE))
else
    echo -e "  venv/: ${BLUE}no encontrado${NC}"
fi

# volumes/
echo -e "${YELLOW}Calculando volumes/...${NC}"
VOL_SIZE=$(find "$PROJECTS_DIR" -type d -name "volumes" -exec du -sh {} + 2>/dev/null | awk '{sum+=$1} END {print sum}')
if [ ! -z "$VOL_SIZE" ]; then
    echo -e "  volumes/: ${RED}~${VOL_SIZE}MB${NC}"
    EXCLUDE_TOTAL=$((EXCLUDE_TOTAL + VOL_SIZE))
else
    echo -e "  volumes/: ${BLUE}no encontrado${NC}"
fi

# __pycache__/
echo -e "${YELLOW}Calculando __pycache__/...${NC}"
CACHE_SIZE=$(find "$PROJECTS_DIR" -type d -name "__pycache__" -exec du -sh {} + 2>/dev/null | awk '{sum+=$1} END {print sum}')
if [ ! -z "$CACHE_SIZE" ]; then
    echo -e "  __pycache__/: ${RED}~${CACHE_SIZE}MB${NC}"
    EXCLUDE_TOTAL=$((EXCLUDE_TOTAL + CACHE_SIZE))
else
    echo -e "  __pycache__/: ${BLUE}no encontrado${NC}"
fi

# dist/, build/
echo -e "${YELLOW}Calculando dist/ y build/...${NC}"
BUILD_SIZE=$(find "$PROJECTS_DIR" -type d \( -name "dist" -o -name "build" \) -exec du -sh {} + 2>/dev/null | awk '{sum+=$1} END {print sum}')
if [ ! -z "$BUILD_SIZE" ]; then
    echo -e "  dist/build/: ${RED}~${BUILD_SIZE}MB${NC}"
    EXCLUDE_TOTAL=$((EXCLUDE_TOTAL + BUILD_SIZE))
else
    echo -e "  dist/build/: ${BLUE}no encontrado${NC}"
fi

echo ""
echo -e "${BLUE}4️⃣  Resumen:${NC}"
echo ""

if [ $EXCLUDE_TOTAL -gt 0 ]; then
    EXCLUDE_GB=$((EXCLUDE_TOTAL / 1024))
    echo -e "Tamaño total a excluir: ${RED}~${EXCLUDE_GB}GB${NC}"
    echo ""
    echo -e "${GREEN}Si excluyes estas carpetas, solo sincronizarás:${NC}"
    echo -e "  Código fuente, docs, configs, scripts ✅"
    echo -e "  SIN: node_modules, venv, volumes, cache ❌"
    echo ""
    echo -e "${YELLOW}Nota: Laptop deberá regenerar dependencias:${NC}"
    echo -e "  npm install (para node_modules)"
    echo -e "  pip install (para venv)"
else
    echo -e "${YELLOW}No se encontraron carpetas grandes a excluir${NC}"
    echo -e "${YELLOW}Sync completo recomendado${NC}"
fi
echo ""

echo -e "${BLUE}5️⃣  Recomendación:${NC}"
echo ""

# Convertir TOTAL_SIZE a GB (aproximado)
TOTAL_GB=$(echo "$TOTAL_SIZE" | sed 's/G//' | sed 's/M/0.001*/' | bc 2>/dev/null || echo "?")

if [ "$TOTAL_GB" != "?" ]; then
    if (( $(echo "$TOTAL_GB < $ONEDRIVE_AVAILABLE_GB" | bc -l) )); then
        echo -e "${GREEN}✅ SYNC COMPLETO OK${NC}"
        echo -e "   Espacio suficiente en OneDrive"
        echo -e "   Tamaño: $TOTAL_SIZE vs Disponible: $ONEDRIVE_AVAILABLE"
    else
        echo -e "${YELLOW}⚠️  SYNC SELECTIVO RECOMENDADO${NC}"
        echo -e "   Excluir carpetas pesadas para ahorrar espacio"
        echo -e "   O sincronizar solo proyectos críticos"
    fi
else
    echo -e "${YELLOW}⚠️  No se pudo calcular tamaño exacto${NC}"
    echo -e "   Verificar manualmente: du -sh /mnt/d/01_PROYECTOS_ACTIVOS/"
fi
echo ""

echo -e "${BLUE}==================================================${NC}"
echo -e "${GREEN}Análisis completo${NC}"
echo ""
echo "📖 Siguiente paso:"
echo "  Leer: docs/ONEDRIVE_SYNC_SETUP.md"
echo "  Configurar sync según recomendación arriba"
echo ""
