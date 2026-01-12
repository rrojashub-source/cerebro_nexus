#!/bin/bash
# clp-force: Force bypass permissions by killing Claude and restarting
# Version: 1.0.0
# Date: 2026-01-12
# Author: NEXUS-PC
# For: NEXUS-Laptop

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🔪 clp-force: Killing Claude Code processes...${NC}"

# Kill all claude code processes (force)
pkill -9 -f "claude.*code" 2>/dev/null
KILLED=$?

if [ $KILLED -eq 0 ]; then
    echo -e "${GREEN}✅ Claude processes killed${NC}"
else
    echo -e "${YELLOW}⚠️  No Claude processes found (this is OK if already closed)${NC}"
fi

echo -e "${YELLOW}⏳ Waiting 2 seconds for cleanup...${NC}"
sleep 2

# Check if clp exists
if [ ! -f ~/bin/clp ]; then
    echo -e "${RED}❌ Error: ~/bin/clp not found${NC}"
    echo -e "${YELLOW}Please create clp script first (see NEXUS_LAPTOP_TROUBLESHOOTING.md)${NC}"
    exit 1
fi

echo -e "${GREEN}🚀 Restarting with clp...${NC}"
echo ""

# Execute clp (this will NOT return, it replaces current process)
exec ~/bin/clp
