#!/bin/bash
#
# NEXUS Cerebro V3.0.0 - Systemd Installation Script
# Author: NEXUS AI + Ricardo
# Date: November 14, 2025
#
# This script installs NEXUS Cerebro as a systemd service for automatic startup.
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SERVICE_FILE="$SCRIPT_DIR/nexus-cerebro.service"
SYSTEMD_DIR="/etc/systemd/system"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}NEXUS Cerebro V3.0.0 - Systemd Setup${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if running as root/sudo
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}✗ Este script debe ejecutarse con sudo${NC}"
    echo -e "  Uso: sudo bash $0"
    exit 1
fi

# Verify service file exists
if [ ! -f "$SERVICE_FILE" ]; then
    echo -e "${RED}✗ Service file not found: $SERVICE_FILE${NC}"
    exit 1
fi

echo -e "${YELLOW}📁 Project root: $PROJECT_ROOT${NC}"
echo -e "${YELLOW}📄 Service file: $SERVICE_FILE${NC}"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker no está instalado${NC}"
    echo -e "  Por favor instala Docker primero: https://docs.docker.com/get-docker/"
    exit 1
fi

echo -e "${GREEN}✓ Docker encontrado: $(docker --version)${NC}"

# Check if docker compose is available
if ! docker compose version &> /dev/null; then
    echo -e "${RED}✗ Docker Compose no está disponible${NC}"
    echo -e "  Por favor instala Docker Compose v2+"
    exit 1
fi

echo -e "${GREEN}✓ Docker Compose encontrado: $(docker compose version)${NC}"
echo ""

# Backup existing service if present
if [ -f "$SYSTEMD_DIR/nexus-cerebro.service" ]; then
    echo -e "${YELLOW}⚠️  Service existente detectado, creando backup...${NC}"
    cp "$SYSTEMD_DIR/nexus-cerebro.service" "$SYSTEMD_DIR/nexus-cerebro.service.backup.$(date +%Y%m%d_%H%M%S)"
    echo -e "${GREEN}✓ Backup creado${NC}"
fi

# Copy service file
echo -e "${YELLOW}📋 Copiando service file a $SYSTEMD_DIR...${NC}"
cp "$SERVICE_FILE" "$SYSTEMD_DIR/nexus-cerebro.service"
echo -e "${GREEN}✓ Service file instalado${NC}"

# Set correct permissions
chmod 644 "$SYSTEMD_DIR/nexus-cerebro.service"
echo -e "${GREEN}✓ Permisos configurados${NC}"

# Reload systemd daemon
echo -e "${YELLOW}🔄 Recargando systemd daemon...${NC}"
systemctl daemon-reload
echo -e "${GREEN}✓ Daemon recargado${NC}"

# Enable service (autostart on boot)
echo -e "${YELLOW}🚀 Habilitando autostart...${NC}"
systemctl enable nexus-cerebro.service
echo -e "${GREEN}✓ Autostart habilitado${NC}"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Instalación completada exitosamente${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Comandos disponibles:"
echo -e ""
echo -e "  ${YELLOW}Iniciar servicio:${NC}"
echo -e "    sudo systemctl start nexus-cerebro"
echo -e ""
echo -e "  ${YELLOW}Detener servicio:${NC}"
echo -e "    sudo systemctl stop nexus-cerebro"
echo -e ""
echo -e "  ${YELLOW}Reiniciar servicio:${NC}"
echo -e "    sudo systemctl restart nexus-cerebro"
echo -e ""
echo -e "  ${YELLOW}Ver estado:${NC}"
echo -e "    sudo systemctl status nexus-cerebro"
echo -e ""
echo -e "  ${YELLOW}Ver logs:${NC}"
echo -e "    sudo journalctl -u nexus-cerebro -f"
echo -e ""
echo -e "  ${YELLOW}Deshabilitar autostart:${NC}"
echo -e "    sudo systemctl disable nexus-cerebro"
echo -e ""
echo -e "  ${YELLOW}Desinstalar:${NC}"
echo -e "    sudo bash $SCRIPT_DIR/uninstall.sh"
echo -e ""
echo -e "${YELLOW}¿Iniciar servicio ahora? (y/n)${NC}"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}🚀 Iniciando NEXUS Cerebro...${NC}"
    systemctl start nexus-cerebro

    # Wait a bit for startup
    sleep 3

    # Check status
    if systemctl is-active --quiet nexus-cerebro; then
        echo -e "${GREEN}✓ NEXUS Cerebro iniciado correctamente${NC}"
        echo ""
        echo -e "Verificando servicios:"
        docker ps --filter "name=nexus" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        echo ""
        echo -e "${GREEN}✓ API disponible en: http://localhost:8003${NC}"
        echo -e "${GREEN}✓ Docs: http://localhost:8003/docs${NC}"
    else
        echo -e "${RED}✗ Error al iniciar servicio${NC}"
        echo -e "Ver logs: sudo journalctl -u nexus-cerebro -n 50"
        exit 1
    fi
else
    echo -e "${YELLOW}ℹ️  Servicio no iniciado. Inicia manualmente:${NC}"
    echo -e "   sudo systemctl start nexus-cerebro"
fi

echo ""
echo -e "${GREEN}🧠 NEXUS Cerebro arrancará automáticamente en el próximo reinicio${NC}"
