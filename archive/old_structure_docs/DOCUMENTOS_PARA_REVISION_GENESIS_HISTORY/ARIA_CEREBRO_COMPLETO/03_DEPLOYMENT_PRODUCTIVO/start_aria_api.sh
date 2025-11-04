#!/bin/bash
# 🌸 ARIA API - Inicio con configuración separada
# Puerto: 8001 | PostgreSQL: 5437 | Cerebro: aria_memory

echo "🌸 Iniciando ARIA Memory API..."

# Variables de entorno específicas de ARIA
export CONFIG_FILE=config/config_aria.yaml
export DATABASE_URL="postgresql://aria_user:aria_secure_2025@localhost:5437/aria_memory"
export REDIS_URL="redis://localhost:6379/2"
export CHROMA_URL="http://localhost:8000"

# Directorio base
cd /mnt/d/01_PROYECTOS_ACTIVOS/ARIA_CEREBRO_COMPLETO/03_DEPLOYMENT_PRODUCTIVO

# Activar entorno virtual compartido
source venv_nexus_api/bin/activate

# Crear carpeta logs si no existe
mkdir -p logs

# Arrancar API en background
nohup python -m memory_system.api.main > logs/aria_8001.log 2>&1 &
ARIA_PID=$!

echo "✅ ARIA API iniciada"
echo "   - PID: $ARIA_PID"
echo "   - Puerto: 8001"
echo "   - Cerebro: PostgreSQL 5437"
echo "   - Logs: logs/aria_8001.log"
echo ""
echo "Verificar salud: curl http://localhost:8001/health"
