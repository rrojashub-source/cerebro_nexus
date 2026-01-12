#!/bin/bash
# Uninstall CEREBRO Sync Daemon systemd service
# Author: NEXUS-PC
# Date: 2026-01-12

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🗑️  Uninstalling CEREBRO Sync Daemon systemd service${NC}"

# Variables
SERVICE_FILE="cerebro-sync.service"
SERVICE_PATH="/etc/systemd/system/${SERVICE_FILE}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}❌ Please run as root (sudo)${NC}"
    exit 1
fi

# Step 1: Stop service
echo -e "${YELLOW}🛑 Step 1: Stopping service${NC}"
systemctl stop cerebro-sync.service 2>/dev/null || true
echo -e "${GREEN}✅ Service stopped${NC}"

# Step 2: Disable service
echo -e "${YELLOW}⚙️  Step 2: Disabling auto-start${NC}"
systemctl disable cerebro-sync.service 2>/dev/null || true
echo -e "${GREEN}✅ Auto-start disabled${NC}"

# Step 3: Remove service file
echo -e "${YELLOW}🗑️  Step 3: Removing service file${NC}"
rm -f "${SERVICE_PATH}"
echo -e "${GREEN}✅ Service file removed${NC}"

# Step 4: Reload systemd
echo -e "${YELLOW}🔄 Step 4: Reloading systemd daemon${NC}"
systemctl daemon-reload
echo -e "${GREEN}✅ Systemd reloaded${NC}"

echo ""
echo -e "${GREEN}✅ Uninstallation completed successfully!${NC}"
echo ""
echo "Note: Log files in logs/ directory were NOT deleted."
echo "      To remove logs manually: rm -rf logs/sync_daemon.log"
