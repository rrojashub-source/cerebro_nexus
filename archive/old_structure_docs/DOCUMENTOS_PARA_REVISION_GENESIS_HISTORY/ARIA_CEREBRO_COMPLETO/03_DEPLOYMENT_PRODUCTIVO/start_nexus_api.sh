#!/bin/bash
# NEXUS Brain API Startup Script
# Puerto 8002, PostgreSQL 5436

echo "🧠 NEXUS Brain API - Iniciando..."

# Variables de entorno NEXUS
export CONFIG_FILE="config/config_nexus.yaml"
export DATABASE_URL="postgresql://nexus_user:nexus_secure_2025@localhost:5436/nexus_memory"
export REDIS_URL="redis://localhost:6379/1"
export ENVIRONMENT="development"

# Directorio base
cd /mnt/d/01_PROYECTOS_ACTIVOS/ARIA_CEREBRO_COMPLETO/03_DEPLOYMENT_PRODUCTIVO

# Crear directorio de logs si no existe
mkdir -p logs

# Activar venv NEXUS
source venv_nexus_api/bin/activate

# Verificar que config existe
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Error: $CONFIG_FILE no encontrado"
    exit 1
fi

echo "✅ Config: $CONFIG_FILE"
echo "✅ Database: PostgreSQL 5436"
echo "✅ API Port: 8002"
echo ""

# Arrancar API en background
nohup python -m memory_system.api.main > logs/nexus_8002.log 2>&1 &
API_PID=$!

echo "🚀 NEXUS API iniciado - PID: $API_PID"
echo "📋 Log: logs/nexus_8002.log"
echo ""
echo "Esperando startup (15 segundos)..."
sleep 15

# Verificar que arrancó
if curl -s http://localhost:8002/health > /dev/null; then
    echo "✅ NEXUS API operativo en puerto 8002"
else
    echo "⚠️ NEXUS API puede estar iniciando aún..."
    echo "Revisa: tail -f logs/nexus_8002.log"
fi
