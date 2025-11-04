#!/bin/bash
# 🚀 ARIA BRAIN DASHBOARD - SCRIPT DE INICIO
# Inicia tanto backend como frontend del dashboard
# Autor: Ricardo + NEXUS
# Fecha: 20 Agosto 2025

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Banner
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════╗"
echo "║          🧠 ARIA BRAIN DASHBOARD                ║"
echo "║            Sistema de Control Web               ║"
echo "║              v1.0 - Aug 2025                    ║"
echo "╚══════════════════════════════════════════════════╝"
echo -e "${NC}"

# Verificar que estamos en el directorio correcto
if [ ! -d "$BACKEND_DIR" ] || [ ! -d "$FRONTEND_DIR" ]; then
    error "Directorio incorrecto. Ejecutar desde: dashboard/"
fi

# Verificar dependencias del sistema
log "🔍 Verificando dependencias del sistema..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    error "Python3 no está instalado"
fi

# Verificar Node.js
if ! command -v node &> /dev/null; then
    error "Node.js no está instalado"
fi

# Verificar npm
if ! command -v npm &> /dev/null; then
    error "npm no está instalado"
fi

success "Dependencias del sistema verificadas"

# Verificar estado del cerebro ARIA
log "🧠 Verificando estado del cerebro ARIA..."
if curl -s http://localhost:8001/health > /dev/null 2>&1; then
    success "Cerebro ARIA está operativo (puerto 8001)"
else
    warning "Cerebro ARIA no está disponible - dashboard funcionará en modo limitado"
fi

# Función para verificar si un puerto está en uso
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # Puerto en uso
    else
        return 1  # Puerto libre
    fi
}

# Verificar puertos
log "🔌 Verificando puertos disponibles..."

if check_port 8002; then
    warning "Puerto 8002 ya está en uso - intentando detener proceso existente..."
    pkill -f "dashboard_api" || true
    sleep 2
fi

if check_port 3000; then
    warning "Puerto 3000 ya está en uso - el frontend puede no iniciar correctamente"
fi

# Instalar dependencias del backend
log "📦 Instalando dependencias del backend..."
cd "$BACKEND_DIR"

if [ ! -f "requirements.txt" ]; then
    cat > requirements.txt << EOF
fastapi==0.104.1
uvicorn==0.24.0
websockets==12.0
docker==6.1.3
psutil==5.9.6
requests==2.31.0
python-multipart==0.0.6
EOF
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    log "🐍 Creando entorno virtual Python..."
    python3 -m venv venv
fi

# Activar entorno virtual e instalar dependencias
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1
success "Dependencias del backend instaladas"

# Instalar dependencias del frontend
log "📦 Instalando dependencias del frontend..."
cd "$FRONTEND_DIR"

if [ ! -d "node_modules" ]; then
    log "⬬ Ejecutando npm install..."
    npm install > /dev/null 2>&1
fi
success "Dependencias del frontend instaladas"

# Crear logs directory
mkdir -p "$SCRIPT_DIR/logs"

# Función para limpiar procesos al salir
cleanup() {
    log "🧹 Limpiando procesos..."
    
    # Matar backend
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    
    # Matar frontend
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    # Buscar y matar cualquier proceso restante
    pkill -f "dashboard_api" 2>/dev/null || true
    pkill -f "react-scripts start" 2>/dev/null || true
    
    success "Procesos terminados"
    exit 0
}

# Configurar trap para limpieza
trap cleanup EXIT SIGINT SIGTERM

# Iniciar backend
log "🚀 Iniciando backend (puerto 8002)..."
cd "$BACKEND_DIR"
source venv/bin/activate
python dashboard_api.py > "$SCRIPT_DIR/logs/backend.log" 2>&1 &
BACKEND_PID=$!
sleep 3

# Verificar que el backend se inició correctamente
if kill -0 $BACKEND_PID 2>/dev/null; then
    if curl -s http://localhost:8002/ > /dev/null 2>&1; then
        success "Backend iniciado correctamente en http://localhost:8002"
    else
        error "Backend no responde en puerto 8002"
    fi
else
    error "Error al iniciar backend - revisar logs/backend.log"
fi

# Iniciar frontend
log "🎨 Iniciando frontend (puerto 3000)..."
cd "$FRONTEND_DIR"
npm start > "$SCRIPT_DIR/logs/frontend.log" 2>&1 &
FRONTEND_PID=$!

# Esperar a que el frontend se inicie
log "⏳ Esperando que el frontend se inicie..."
sleep 10

# Verificar frontend
if kill -0 $FRONTEND_PID 2>/dev/null; then
    success "Frontend iniciado correctamente"
else
    warning "Frontend puede estar iniciándose aún..."
fi

# Mostrar información
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════╗"
echo "║              ✅ DASHBOARD INICIADO               ║"
echo "╠══════════════════════════════════════════════════╣"
echo "║  🔗 Frontend: http://localhost:3000              ║"
echo "║  🔧 Backend:  http://localhost:8002              ║"
echo "║  📖 API Docs: http://localhost:8002/docs         ║"
echo "║  🧠 ARIA API: http://localhost:8001              ║"
echo "╠══════════════════════════════════════════════════╣"
echo "║  📁 Logs:     dashboard/logs/                    ║"
echo "║  🛑 Detener:  Ctrl+C                            ║"
echo "╚══════════════════════════════════════════════════╝"
echo -e "${NC}"

log "🎯 Dashboard listo - abriendo navegador..."

# Abrir navegador (solo en entornos con GUI)
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3000 2>/dev/null || true
elif command -v open &> /dev/null; then
    open http://localhost:3000 2>/dev/null || true
fi

log "📊 Presiona Ctrl+C para detener el dashboard"

# Mantener el script corriendo
while true; do
    # Verificar que ambos procesos sigan activos
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        error "Backend se detuvo inesperadamente - revisar logs/backend.log"
    fi
    
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        warning "Frontend se detuvo - esto es normal en desarrollo"
    fi
    
    sleep 10
done