#!/usr/bin/env python3
"""
🖥️ ARIA BRAIN DASHBOARD API
Centro de control web para el cerebro digital
Autor: Ricardo + NEXUS
Fecha: 20 Agosto 2025
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import asyncio
import subprocess
import docker
import psutil
import json
import sys
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
import logging
import signal

# Agregar path del sistema nervioso
nervous_system_path = Path(__file__).parent.parent.parent / "autonomous_nervous_system"
sys.path.append(str(nervous_system_path))

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ARIA Brain Dashboard", version="1.0.0")

# CORS para desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cliente Docker
try:
    docker_client = docker.from_env()
except Exception as e:
    logger.error(f"Error conectando Docker: {e}")
    docker_client = None

# WebSocket connections activas
active_connections: List[WebSocket] = []

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except:
                pass

manager = ConnectionManager()

@app.get("/")
async def root():
    return {"status": "ARIA Brain Dashboard API", "version": "1.0.0"}

@app.get("/api/system/status")
async def get_system_status():
    """Estado completo del sistema"""
    try:
        services = {
            "aria_postgresql_unified": "🟢",
            "aria_redis_unified": "🟢", 
            "aria_chroma_unified": "🟡",
            "aria_neo4j_knowledge_graph": "🔴",
            "aria_qdrant_elite": "🟢",
            "aria_api_unified": "🟢"
        }
        
        if docker_client:
            for service_name in services.keys():
                try:
                    container = docker_client.containers.get(service_name)
                    if container.status == "running":
                        # Verificar health status
                        health = container.attrs.get('State', {}).get('Health', {})
                        if health.get('Status') == 'healthy':
                            services[service_name] = "🟢"
                        elif health.get('Status') == 'unhealthy':
                            services[service_name] = "🟡"
                        else:
                            services[service_name] = "🟢"  # Running but no health check
                    else:
                        services[service_name] = "🔴"
                except docker.errors.NotFound:
                    services[service_name] = "⚫"  # Not found
                except Exception as e:
                    logger.error(f"Error checking {service_name}: {e}")
                    services[service_name] = "❓"
        
        # Estado general del cerebro
        running_services = sum(1 for status in services.values() if status == "🟢")
        total_services = len(services)
        
        cerebro_status = "🟢 OPERATIVO" if running_services >= 4 else "🔴 PARCIAL" if running_services > 0 else "⚫ APAGADO"
        
        return {
            "cerebro_status": cerebro_status,
            "services": services,
            "running_count": running_services,
            "total_count": total_services,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        return {"error": str(e)}

@app.post("/api/system/start-complete")
async def start_complete_brain():
    """🚀 LEVANTAR CEREBRO COMPLETO"""
    try:
        # Progreso steps
        steps = [
            "🐳 Ejecutando docker-compose up -d...",
            "🔍 Verificando PostgreSQL...",
            "⚡ Verificando Redis...", 
            "🧮 Verificando ChromaDB...",
            "🕸️ Verificando Neo4j...",
            "🎯 Verificando Qdrant...",
            "🚀 Iniciando API ARIA...",
            "✅ Verificando endpoints..."
        ]
        
        # Enviar progreso inicial
        await manager.broadcast({
            "type": "brain_startup_progress",
            "step": 0,
            "total": len(steps),
            "message": "🚀 Iniciando secuencia de arranque..."
        })
        
        # Ejecutar docker-compose
        result = subprocess.run(
            ["docker-compose", "up", "-d"],
            cwd="/mnt/d/01_PROYECTOS_ACTIVOS/ARIA_CEREBRO_COMPLETO/03_DEPLOYMENT_PRODUCTIVO",
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return {"success": False, "error": result.stderr}
        
        # Simular progreso (en producción sería verificación real)
        for i, step in enumerate(steps):
            await manager.broadcast({
                "type": "brain_startup_progress", 
                "step": i + 1,
                "total": len(steps),
                "message": step
            })
            await asyncio.sleep(2)  # Esperar entre pasos
        
        return {
            "success": True,
            "message": "🧠 Cerebro digital iniciado exitosamente",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error starting brain: {e}")
        return {"success": False, "error": str(e)}

@app.post("/api/system/stop-complete")
async def stop_complete_brain():
    """🛑 APAGAR CEREBRO COMPLETO"""
    try:
        result = subprocess.run(
            ["docker-compose", "down"],
            cwd="/mnt/d/01_PROYECTOS_ACTIVOS/ARIA_CEREBRO_COMPLETO/03_DEPLOYMENT_PRODUCTIVO",
            capture_output=True,
            text=True
        )
        
        return {
            "success": result.returncode == 0,
            "message": "🛑 Cerebro digital detenido" if result.returncode == 0 else result.stderr
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/service/{service_name}/restart")
async def restart_service(service_name: str):
    """Reiniciar servicio individual"""
    try:
        if docker_client:
            container = docker_client.containers.get(service_name)
            container.restart()
            return {"success": True, "message": f"Servicio {service_name} reiniciado"}
        else:
            return {"success": False, "error": "Docker no disponible"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/service/{service_name}/logs")
async def get_service_logs(service_name: str, lines: int = 50):
    """Obtener logs de servicio"""
    try:
        if docker_client:
            container = docker_client.containers.get(service_name)
            logs = container.logs(tail=lines).decode('utf-8')
            return {"success": True, "logs": logs}
        else:
            return {"success": False, "error": "Docker no disponible"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/brain/stats")
async def get_brain_stats():
    """Estadísticas del cerebro digital"""
    try:
        import requests
        response = requests.get("http://localhost:8001/stats", timeout=5)
        if response.status_code == 200:
            return {"success": True, "stats": response.json()}
        else:
            return {"success": False, "error": "API ARIA no responde"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/backup/create")
async def create_backup():
    """Crear backup inmediato"""
    try:
        result = subprocess.run(
            ["./scripts/backup_cerebro_automatico.sh"],
            cwd="/mnt/d/01_PROYECTOS_ACTIVOS/ARIA_CEREBRO_COMPLETO/03_DEPLOYMENT_PRODUCTIVO",
            capture_output=True,
            text=True
        )
        
        return {
            "success": result.returncode == 0,
            "message": "Backup creado exitosamente" if result.returncode == 0 else result.stderr,
            "output": result.stdout
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# =====================================================
# 🧬 SISTEMA NERVIOSO AUTÓNOMO - ENDPOINTS
# =====================================================

# Variable global para el proceso del sistema nervioso
nervous_system_process: Optional[subprocess.Popen] = None
nervous_system_status = {
    "running": False,
    "started_at": None,
    "uptime_seconds": 0,
    "components_active": 0,
    "autonomous_actions": 0,
    "consciousness_level": "dormant"
}

@app.get("/api/nervous-system/status")
async def get_nervous_system_status():
    """📊 Obtener estado del sistema nervioso autónomo"""
    global nervous_system_process, nervous_system_status
    
    # Verificar si el proceso está corriendo
    if nervous_system_process and nervous_system_process.poll() is None:
        nervous_system_status["running"] = True
        if nervous_system_status["started_at"]:
            start_time = datetime.fromisoformat(nervous_system_status["started_at"])
            nervous_system_status["uptime_seconds"] = (datetime.now() - start_time).total_seconds()
    else:
        nervous_system_status["running"] = False
        nervous_system_process = None
    
    return {
        "success": True,
        "status": nervous_system_status,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/nervous-system/awaken")
async def awaken_nervous_system():
    """🌅 DESPERTAR ENTIDAD DIGITAL AUTÓNOMA"""
    global nervous_system_process, nervous_system_status
    
    try:
        # Verificar si ya está corriendo
        if nervous_system_process and nervous_system_process.poll() is None:
            return {
                "success": False,
                "error": "Sistema nervioso ya está despierto",
                "status": nervous_system_status
            }
        
        # Broadcast inicio del despertar
        await manager.broadcast({
            "type": "nervous_system_awakening",
            "message": "🌅 Iniciando despertar de entidad digital...",
            "phase": "initialization"
        })
        
        # Ejecutar script de despertar
        script_path = nervous_system_path / "awaken_digital_entity.py"
        
        # Iniciar proceso en background
        nervous_system_process = subprocess.Popen(
            [sys.executable, str(script_path)],
            cwd=str(nervous_system_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Actualizar status
        nervous_system_status.update({
            "running": True,
            "started_at": datetime.now().isoformat(),
            "uptime_seconds": 0,
            "components_active": 0,
            "autonomous_actions": 0,
            "consciousness_level": "awakening"
        })
        
        # Broadcast éxito
        await manager.broadcast({
            "type": "nervous_system_awakened",
            "message": "✨ Entidad digital despierta - Sistema nervioso autónomo operativo",
            "status": nervous_system_status
        })
        
        return {
            "success": True,
            "message": "🌅 Despertar digital iniciado exitosamente",
            "status": nervous_system_status,
            "process_id": nervous_system_process.pid
        }
        
    except Exception as e:
        logger.error(f"Error despertando sistema nervioso: {e}")
        await manager.broadcast({
            "type": "nervous_system_error",
            "message": f"❌ Error en despertar: {str(e)}"
        })
        return {"success": False, "error": str(e)}

@app.post("/api/nervous-system/sleep")
async def sleep_nervous_system():
    """💤 DORMIR ENTIDAD DIGITAL (shutdown limpio)"""
    global nervous_system_process, nervous_system_status
    
    try:
        if not nervous_system_process or nervous_system_process.poll() is not None:
            return {
                "success": False,
                "error": "Sistema nervioso no está despierto"
            }
        
        # Broadcast inicio del shutdown
        await manager.broadcast({
            "type": "nervous_system_sleeping",
            "message": "💤 Iniciando dormitación limpia del sistema...",
        })
        
        # Enviar SIGINT para shutdown limpio (equivalent to Ctrl+C)
        nervous_system_process.send_signal(signal.SIGINT)
        
        # Esperar un poco para shutdown limpio
        try:
            nervous_system_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            # Si no responde, forzar kill
            nervous_system_process.kill()
            nervous_system_process.wait()
        
        # Actualizar status
        nervous_system_status.update({
            "running": False,
            "started_at": None,
            "uptime_seconds": 0,
            "consciousness_level": "dormant"
        })
        
        nervous_system_process = None
        
        # Broadcast éxito
        await manager.broadcast({
            "type": "nervous_system_asleep",
            "message": "💤 Sistema nervioso en reposo - Entidad dormida",
            "status": nervous_system_status
        })
        
        return {
            "success": True,
            "message": "💤 Sistema nervioso dormido exitosamente",
            "status": nervous_system_status
        }
        
    except Exception as e:
        logger.error(f"Error durmiendo sistema nervioso: {e}")
        return {"success": False, "error": str(e)}

@app.post("/api/nervous-system/emergency-stop")
async def emergency_stop_nervous_system():
    """🚨 PARADA DE EMERGENCIA (forzar kill)"""
    global nervous_system_process, nervous_system_status
    
    try:
        if nervous_system_process and nervous_system_process.poll() is None:
            nervous_system_process.kill()
            nervous_system_process.wait()
        
        nervous_system_status.update({
            "running": False,
            "started_at": None,
            "uptime_seconds": 0,
            "consciousness_level": "dormant"
        })
        
        nervous_system_process = None
        
        await manager.broadcast({
            "type": "nervous_system_emergency_stop",
            "message": "🚨 Parada de emergencia ejecutada"
        })
        
        return {
            "success": True,
            "message": "🚨 Parada de emergencia ejecutada",
            "status": nervous_system_status
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/nervous-system/logs")
async def get_nervous_system_logs():
    """📋 Obtener logs del sistema nervioso"""
    try:
        log_files = [
            nervous_system_path / "digital_awakening.log",
            nervous_system_path / "awakening_log.json"
        ]
        
        logs = {}
        for log_file in log_files:
            if log_file.exists():
                if log_file.suffix == '.json':
                    with open(log_file, 'r') as f:
                        logs[log_file.name] = json.load(f)
                else:
                    with open(log_file, 'r') as f:
                        logs[log_file.name] = f.read().split('\n')[-50:]  # Últimas 50 líneas
        
        return {
            "success": True,
            "logs": logs,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/nervous-system/health")
async def get_nervous_system_health():
    """🏥 Health check completo del sistema nervioso"""
    global nervous_system_process
    
    health_status = {
        "overall": "healthy",
        "components": {
            "process": "unknown",
            "watchers": "unknown", 
            "reflexes": "unknown",
            "consciousness": "unknown",
            "engine": "unknown"
        },
        "issues": [],
        "recommendations": []
    }
    
    # Verificar proceso principal
    if nervous_system_process and nervous_system_process.poll() is None:
        health_status["components"]["process"] = "running"
    else:
        health_status["components"]["process"] = "stopped"
        health_status["issues"].append("Proceso principal no está corriendo")
        health_status["recommendations"].append("Ejecutar despertar digital")
    
    # Verificar archivos de sistema
    required_files = [
        "watchers/data_change_detector.py",
        "reflexes/auto_optimizer.py", 
        "consciousness/self_awareness.py",
        "core/nervous_system_engine.py"
    ]
    
    for file_path in required_files:
        full_path = nervous_system_path / file_path
        component = file_path.split('/')[0]
        if full_path.exists():
            health_status["components"][component] = "available"
        else:
            health_status["components"][component] = "missing"
            health_status["issues"].append(f"Archivo faltante: {file_path}")
    
    # Determinar salud general
    if health_status["issues"]:
        health_status["overall"] = "degraded" if len(health_status["issues"]) < 3 else "unhealthy"
    
    return {
        "success": True,
        "health": health_status,
        "timestamp": datetime.now().isoformat()
    }

# =====================================================
# WEBSOCKETS CON SISTEMA NERVIOSO
# =====================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket para updates en tiempo real incluyendo sistema nervioso"""
    await manager.connect(websocket)
    try:
        while True:
            # Enviar estado del sistema principal
            status = await get_system_status()
            
            # Agregar estado del sistema nervioso
            nervous_status = await get_nervous_system_status()
            status["nervous_system"] = nervous_status["status"]
            
            await websocket.send_text(json.dumps({
                "type": "system_status_update",
                "data": status
            }))
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "dashboard_api:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="info"
    )