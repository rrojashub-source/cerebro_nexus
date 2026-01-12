#!/bin/bash
# Install CEREBRO Sync Daemon as systemd service
# Author: NEXUS-PC
# Date: 2026-01-12

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔧 Installing CEREBRO Sync Daemon as systemd service${NC}"

# Variables
SERVICE_FILE="cerebro-sync.service"
SERVICE_PATH="/etc/systemd/system/${SERVICE_FILE}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}❌ Please run as root (sudo)${NC}"
    exit 1
fi

# Step 1: Copy service file
echo -e "${YELLOW}📋 Step 1: Copying service file to /etc/systemd/system/${NC}"
cp "${SCRIPT_DIR}/${SERVICE_FILE}" "${SERVICE_PATH}"
chmod 644 "${SERVICE_PATH}"
echo -e "${GREEN}✅ Service file installed${NC}"

# Step 2: Reload systemd
echo -e "${YELLOW}🔄 Step 2: Reloading systemd daemon${NC}"
systemctl daemon-reload
echo -e "${GREEN}✅ Systemd reloaded${NC}"

# Step 3: Enable service (auto-start on boot)
echo -e "${YELLOW}⚙️  Step 3: Enabling auto-start on boot${NC}"
systemctl enable cerebro-sync.service
echo -e "${GREEN}✅ Auto-start enabled${NC}"

# Step 4: Start service
echo -e "${YELLOW}🚀 Step 4: Starting service${NC}"
systemctl start cerebro-sync.service
echo -e "${GREEN}✅ Service started${NC}"

# Step 5: Check status
echo ""
echo -e "${GREEN}📊 Service Status:${NC}"
systemctl status cerebro-sync.service --no-pager

echo ""
echo -e "${GREEN}✅ Installation completed successfully!${NC}"
echo ""
echo "Useful commands:"
echo "  - Check status:  sudo systemctl status cerebro-sync"
echo "  - View logs:     sudo journalctl -u cerebro-sync -f"
echo "  - Stop service:  sudo systemctl stop cerebro-sync"
echo "  - Start service: sudo systemctl start cerebro-sync"
echo "  - Restart:       sudo systemctl restart cerebro-sync"
echo "  - Disable:       sudo systemctl disable cerebro-sync"
