#!/bin/bash
#
# NEXUS Cerebro V3.0.0 - Systemd Uninstall Script
# Author: NEXUS AI + Ricardo
# Date: November 14, 2025
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SYSTEMD_DIR="/etc/systemd/system"
SERVICE_NAME="nexus-cerebro.service"

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}NEXUS Cerebro - Systemd Uninstall${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}✗ Este script debe ejecutarse con sudo${NC}"
    echo -e "  Uso: sudo bash $0"
    exit 1
fi

# Check if service exists
if [ ! -f "$SYSTEMD_DIR/$SERVICE_NAME" ]; then
    echo -e "${YELLOW}ℹ️  Service no está instalado${NC}"
    exit 0
fi

# Stop service if running
if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo -e "${YELLOW}🛑 Deteniendo servicio...${NC}"
    systemctl stop "$SERVICE_NAME"
    echo -e "${GREEN}✓ Servicio detenido${NC}"
fi

# Disable service
if systemctl is-enabled --quiet "$SERVICE_NAME"; then
    echo -e "${YELLOW}🔓 Deshabilitando autostart...${NC}"
    systemctl disable "$SERVICE_NAME"
    echo -e "${GREEN}✓ Autostart deshabilitado${NC}"
fi

# Remove service file
echo -e "${YELLOW}🗑️  Eliminando service file...${NC}"
rm -f "$SYSTEMD_DIR/$SERVICE_NAME"
echo -e "${GREEN}✓ Service file eliminado${NC}"

# Reload daemon
echo -e "${YELLOW}🔄 Recargando systemd daemon...${NC}"
systemctl daemon-reload
systemctl reset-failed
echo -e "${GREEN}✓ Daemon recargado${NC}"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Desinstalación completada${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}Nota:${NC} Los containers Docker NO fueron detenidos."
echo -e "Para detenerlos manualmente:"
echo -e "  cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/docker"
echo -e "  docker compose down"
echo ""
