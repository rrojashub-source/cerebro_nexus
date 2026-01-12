#!/bin/bash
# diagnose-clp.sh: Diagnostic tool for clp issues
# Version: 1.0.0
# Date: 2026-01-12
# Author: NEXUS-PC
# For: NEXUS-Laptop

echo "=================================================="
echo "  CLp + tmux Diagnostic Tool"
echo "  Version: 1.0.0"
echo "  Date: $(date)"
echo "=================================================="
echo ""

echo "1️⃣  Verificando script clp:"
echo "   Location: $(which clp 2>/dev/null || echo 'NOT FOUND')"
if [ -f "$(which clp 2>/dev/null)" ]; then
    echo "   ✅ clp script exists"
else
    echo "   ❌ clp script NOT found"
fi
echo ""

echo "2️⃣  Contenido de clp (primeras 20 líneas):"
if [ -f "$(which clp 2>/dev/null)" ]; then
    cat $(which clp) | head -20
    echo ""

    # Check for --continue flag
    if grep -q "\-\-continue" $(which clp); then
        echo "   ✅ Script has --continue flag"
    else
        echo "   ❌ Script MISSING --continue flag (this is the problem!)"
    fi
else
    echo "   ❌ Cannot read clp script"
fi
echo ""

echo "3️⃣  Verificando tmux sessions activas:"
if command -v tmux &> /dev/null; then
    tmux ls 2>/dev/null || echo "   No active tmux sessions"
else
    echo "   ❌ tmux not installed"
fi
echo ""

echo "4️⃣  Verificando Claude processes:"
CLAUDE_PROCS=$(ps aux | grep -E "claude.*code" | grep -v grep)
if [ -n "$CLAUDE_PROCS" ]; then
    echo "$CLAUDE_PROCS"
else
    echo "   No Claude Code processes running"
fi
echo ""

echo "5️⃣  Verificando Claude Code versión:"
if command -v claude &> /dev/null; then
    claude --version 2>/dev/null || echo "   Cannot get version"
else
    echo "   ❌ Claude CLI not found in PATH"
fi
echo ""

echo "6️⃣  Testing project name generation:"
cd /tmp 2>/dev/null || cd ~
PROJECT_NAME=$(basename "$PWD" | sed 's/[^a-zA-Z0-9_-]/_/g')
echo "   Current dir: $PWD"
echo "   Project name would be: claude-${PROJECT_NAME}"
echo ""

echo "7️⃣  Verificando permisos de scripts:"
echo "   clp: $(ls -l $(which clp 2>/dev/null) 2>/dev/null || echo 'N/A')"
if [ -f ~/bin/clp-force ]; then
    echo "   clp-force: $(ls -l ~/bin/clp-force)"
else
    echo "   clp-force: NOT FOUND (create it for bypass)"
fi
echo ""

echo "8️⃣  Verificando Claude config:"
if [ -d ~/.claude ]; then
    echo "   ✅ ~/.claude directory exists"
    if [ -f ~/.claude/.active_ai ]; then
        echo "   Active AI: $(cat ~/.claude/.active_ai)"
    else
        echo "   No active AI selected"
    fi
else
    echo "   ❌ ~/.claude directory NOT found"
fi
echo ""

echo "=================================================="
echo "  DIAGNOSTIC COMPLETE"
echo "=================================================="
echo ""
echo "📋 NEXT STEPS:"
echo ""
if ! grep -q "\-\-continue" $(which clp 2>/dev/null); then
    echo "❌ CRITICAL: Your clp script is MISSING --continue flag"
    echo "   Solution: Copy corrected clp from NEXUS_LAPTOP_TROUBLESHOOTING.md"
    echo ""
fi

if [ ! -f ~/bin/clp-force ]; then
    echo "⚠️  clp-force script not found"
    echo "   Solution: cp scripts/clp-force.sh ~/bin/clp-force && chmod +x ~/bin/clp-force"
    echo ""
fi

echo "📄 Save this output for NEXUS-PC:"
echo "   ./diagnose-clp.sh > /tmp/laptop-diagnostic.txt"
echo ""
