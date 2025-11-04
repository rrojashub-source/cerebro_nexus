#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏥 HEALTH ENDPOINTS - FASE 1 COMPLETION ARIA CEREBRO
Endpoints comprehensivos de health check + circuit breaker monitoring

Integración con sistema API FastAPI para observabilidad completa
Fecha: 11 Agosto 2025
Autorizado por: Ricardo (Episode 477)
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse

# Importar optimizations
try:
    from ..optimization import (
        ComprehensiveHealthChecker, 
        create_health_checker,
        ServiceHealth,
        EliteCircuitBreaker
    )
    OPTIMIZATION_AVAILABLE = True
except ImportError:
    OPTIMIZATION_AVAILABLE = False

logger = logging.getLogger(__name__)

# Router para health endpoints
health_router = APIRouter(prefix="/health", tags=["Health & Monitoring"])

# Global health checker (se inicializa en startup)
global_health_checker: Optional[ComprehensiveHealthChecker] = None

async def get_health_checker() -> ComprehensiveHealthChecker:
    """Dependency para obtener health checker"""
    global global_health_checker
    
    if global_health_checker is None:
        if not OPTIMIZATION_AVAILABLE:
            raise HTTPException(
                status_code=500,
                detail="Health monitoring system not available"
            )
        
        # Inicializar con todos los servicios
        service_names = ['postgresql', 'redis', 'chroma', 'qdrant', 'neo4j']
        global_health_checker = await create_health_checker(service_names)
    
    return global_health_checker

@health_router.get("/", response_model=Dict[str, Any])
async def basic_health_check():
    """
    Health check básico - compatible con Docker healthcheck
    
    Returns:
        Status básico del sistema
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "aria_cerebro_unified",
        "version": "2.0.0-elite"
    }

@health_router.get("/comprehensive", response_model=Dict[str, Any])
async def comprehensive_health_check(
    health_checker: ComprehensiveHealthChecker = Depends(get_health_checker)
):
    """
    Health check comprehensivo con todos los servicios y métricas
    
    Returns:
        Reporte completo de salud del sistema
    """
    try:
        health_report = await health_checker.comprehensive_health_check()
        
        # Determinar HTTP status code basado en health
        overall_status = health_report.get('overall_status', 'unknown')
        
        if overall_status == ServiceHealth.HEALTHY.value:
            status_code = status.HTTP_200_OK
        elif overall_status == ServiceHealth.DEGRADED.value:
            status_code = status.HTTP_200_OK  # 200 but with warnings
        elif overall_status == ServiceHealth.UNHEALTHY.value:
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        
        return JSONResponse(
            content=health_report,
            status_code=status_code
        )
        
    except Exception as e:
        logger.error(f"Comprehensive health check failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Health check system error: {str(e)}"
        )

@health_router.get("/services", response_model=Dict[str, Any])
async def services_health(
    health_checker: ComprehensiveHealthChecker = Depends(get_health_checker)
):
    """
    Health check específico de servicios individuales
    
    Returns:
        Estado de cada servicio por separado
    """
    try:
        full_report = await health_checker.comprehensive_health_check()
        
        return {
            "timestamp": full_report.get("timestamp"),
            "services": full_report.get("services", {}),
            "services_count": len(full_report.get("services", {})),
            "healthy_services": len([
                s for s in full_report.get("services", {}).values() 
                if s.get("status") == ServiceHealth.HEALTHY.value
            ])
        }
        
    except Exception as e:
        logger.error(f"Services health check failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Services health check error: {str(e)}"
        )

@health_router.get("/circuit-breakers", response_model=Dict[str, Any])
async def circuit_breakers_status(
    health_checker: ComprehensiveHealthChecker = Depends(get_health_checker)
):
    """
    Estado de todos los circuit breakers
    
    Returns:
        Status detallado de cada circuit breaker
    """
    try:
        circuit_breakers_status = {}
        
        for name, breaker in health_checker.circuit_breakers.items():
            circuit_breakers_status[name] = breaker.get_status()
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "circuit_breakers": circuit_breakers_status,
            "total_breakers": len(circuit_breakers_status),
            "open_breakers": len([
                status for status in circuit_breakers_status.values()
                if status.get("state") == "open"
            ]),
            "half_open_breakers": len([
                status for status in circuit_breakers_status.values()
                if status.get("state") == "half_open"
            ])
        }
        
    except Exception as e:
        logger.error(f"Circuit breakers status failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Circuit breakers status error: {str(e)}"
        )

@health_router.post("/circuit-breakers/{service_name}/reset")
async def reset_circuit_breaker(
    service_name: str,
    health_checker: ComprehensiveHealthChecker = Depends(get_health_checker)
):
    """
    Reset manual de un circuit breaker específico
    
    Args:
        service_name: Nombre del servicio cuyo circuit breaker resetear
        
    Returns:
        Confirmación del reset
    """
    try:
        if service_name not in health_checker.circuit_breakers:
            raise HTTPException(
                status_code=404,
                detail=f"Circuit breaker for '{service_name}' not found"
            )
        
        breaker = health_checker.circuit_breakers[service_name]
        old_status = breaker.get_status()
        
        await breaker.reset()
        new_status = breaker.get_status()
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "service_name": service_name,
            "action": "reset",
            "old_state": old_status.get("state"),
            "new_state": new_status.get("state"),
            "success": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Circuit breaker reset failed for {service_name}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Circuit breaker reset error: {str(e)}"
        )

@health_router.get("/metrics", response_model=Dict[str, Any])
async def system_metrics(
    health_checker: ComprehensiveHealthChecker = Depends(get_health_checker)
):
    """
    Métricas de performance y sistema
    
    Returns:
        Métricas detalladas de performance
    """
    try:
        full_report = await health_checker.comprehensive_health_check()
        
        return {
            "timestamp": full_report.get("timestamp"),
            "system_info": full_report.get("system_info", {}),
            "performance_metrics": full_report.get("performance_metrics", {}),
            "check_duration_ms": full_report.get("check_duration_ms", 0),
            "alerts_count": len(full_report.get("alerts", [])),
            "recommendations_count": len(full_report.get("recommendations", []))
        }
        
    except Exception as e:
        logger.error(f"System metrics failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"System metrics error: {str(e)}"
        )

@health_router.get("/alerts", response_model=Dict[str, Any])
async def current_alerts(
    health_checker: ComprehensiveHealthChecker = Depends(get_health_checker)
):
    """
    Alertas activas del sistema
    
    Returns:
        Lista de alertas y recomendaciones actuales
    """
    try:
        full_report = await health_checker.comprehensive_health_check()
        
        alerts = full_report.get("alerts", [])
        recommendations = full_report.get("recommendations", [])
        
        # Clasificar alertas por severity
        critical_alerts = [a for a in alerts if a.startswith("CRITICAL:")]
        warning_alerts = [a for a in alerts if a.startswith("WARNING:")]
        
        return {
            "timestamp": full_report.get("timestamp"),
            "total_alerts": len(alerts),
            "critical_alerts": critical_alerts,
            "warning_alerts": warning_alerts,
            "recommendations": recommendations,
            "overall_status": full_report.get("overall_status", "unknown")
        }
        
    except Exception as e:
        logger.error(f"Alerts check failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Alerts check error: {str(e)}"
        )

@health_router.get("/trend", response_model=Dict[str, Any])
async def health_trend(
    health_checker: ComprehensiveHealthChecker = Depends(get_health_checker)
):
    """
    Tendencia de salud del sistema basada en historia
    
    Returns:
        Análisis de tendencias de salud
    """
    try:
        trend_data = health_checker.get_health_trend()
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "trend_analysis": trend_data,
            "health_history_available": len(health_checker.health_history),
            "max_history_size": health_checker.max_history
        }
        
    except Exception as e:
        logger.error(f"Health trend analysis failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Health trend error: {str(e)}"
        )

@health_router.get("/readiness", response_model=Dict[str, Any])
async def readiness_probe(
    health_checker: ComprehensiveHealthChecker = Depends(get_health_checker)
):
    """
    Kubernetes-style readiness probe
    Verifica si el sistema está listo para recibir tráfico
    
    Returns:
        Status de readiness para load balancer
    """
    try:
        full_report = await health_checker.comprehensive_health_check()
        
        # Sistema ready si servicios críticos están healthy
        critical_services = [
            service for service, health in full_report.get("services", {}).items()
            if health.get("critical", False)
        ]
        
        critical_healthy = all(
            full_report.get("services", {}).get(service, {}).get("status") == ServiceHealth.HEALTHY.value
            for service in critical_services
        )
        
        # No ready si hay circuit breakers críticos abiertos
        open_critical_breakers = 0
        for name, breaker_status in full_report.get("circuit_breakers", {}).items():
            if (breaker_status.get("state") == "open" and 
                name in ['postgresql', 'redis']):  # Servicios críticos
                open_critical_breakers += 1
        
        ready = critical_healthy and open_critical_breakers == 0
        
        response = {
            "timestamp": datetime.utcnow().isoformat(),
            "ready": ready,
            "critical_services_healthy": critical_healthy,
            "open_critical_breakers": open_critical_breakers,
            "overall_status": full_report.get("overall_status")
        }
        
        status_code = status.HTTP_200_OK if ready else status.HTTP_503_SERVICE_UNAVAILABLE
        
        return JSONResponse(
            content=response,
            status_code=status_code
        )
        
    except Exception as e:
        logger.error(f"Readiness probe failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Readiness probe error: {str(e)}"
        )

@health_router.get("/liveness", response_model=Dict[str, Any])
async def liveness_probe():
    """
    Kubernetes-style liveness probe
    Verifica si el proceso está vivo y funcionando
    
    Returns:
        Status básico de liveness para restart decisions
    """
    try:
        # Liveness simple - si podemos responder, estamos vivos
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "alive": True,
            "process_healthy": True,
            "optimization_system": OPTIMIZATION_AVAILABLE
        }
        
    except Exception as e:
        logger.error(f"Liveness probe failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Liveness probe error: {str(e)}"
        )

# Función para inicializar health checker en startup
async def initialize_health_system():
    """Inicializar sistema de health monitoring en startup de la aplicación"""
    global global_health_checker
    
    if OPTIMIZATION_AVAILABLE:
        try:
            service_names = ['postgresql', 'redis', 'chroma', 'qdrant', 'neo4j']
            global_health_checker = await create_health_checker(service_names)
            logger.info("✅ Health monitoring system initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize health system: {e}")
    else:
        logger.warning("⚠️ Health optimization system not available")

# Función para cleanup en shutdown
async def shutdown_health_system():
    """Cleanup del sistema de health monitoring"""
    global global_health_checker
    
    if global_health_checker:
        # Cleanup si necesario
        logger.info("🔒 Health monitoring system shutdown")


# Testing/example usage
if __name__ == "__main__":
    print("🏥 Health Endpoints module loaded successfully")
    print("Available endpoints:")
    print("  GET  /health/                    - Basic health check")
    print("  GET  /health/comprehensive       - Full health report")
    print("  GET  /health/services            - Services status")
    print("  GET  /health/circuit-breakers    - Circuit breakers status")
    print("  POST /health/circuit-breakers/{service}/reset - Reset breaker")
    print("  GET  /health/metrics             - System metrics")
    print("  GET  /health/alerts              - Active alerts")
    print("  GET  /health/trend               - Health trends")
    print("  GET  /health/readiness           - Readiness probe")
    print("  GET  /health/liveness            - Liveness probe")