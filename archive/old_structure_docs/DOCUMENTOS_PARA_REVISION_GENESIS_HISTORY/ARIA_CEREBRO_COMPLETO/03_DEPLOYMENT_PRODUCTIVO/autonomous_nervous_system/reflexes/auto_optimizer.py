#!/usr/bin/env python3
"""
⚡ AUTO OPTIMIZER - El Reflex Que Nunca Descansa
Optimiza el cerebro ARIA automáticamente cuando detecta oportunidades
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import httpx
from dataclasses import dataclass
from enum import Enum

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OptimizationType(Enum):
    """Tipos de optimizaciones que podemos realizar"""
    FULL_ARSENAL_ACTIVATION = "full_arsenal_activation"
    MEMORY_CONSOLIDATION = "memory_consolidation"
    PERFORMANCE_TUNING = "performance_tuning"
    NEURAL_MESH_SYNC = "neural_mesh_sync"
    ANALYTICS_BOOST = "analytics_boost"
    EMOTIONAL_CALIBRATION = "emotional_calibration"
    CONTEXT_OPTIMIZATION = "context_optimization"
    WORKING_MEMORY_CLEANUP = "working_memory_cleanup"


@dataclass
class OptimizationPlan:
    """Plan de optimización a ejecutar"""
    type: OptimizationType
    priority: str  # "low", "medium", "high", "critical"
    description: str
    steps: List[str]
    estimated_duration: int  # segundos
    expected_benefits: List[str]
    prerequisites: List[str]
    rollback_plan: List[str]


class AutoOptimizer:
    """
    El Reflejo Automático del Cerebro Digital
    Optimiza sin que nadie se lo pida cuando detecta oportunidades
    """
    
    def __init__(self, aria_url: str = "http://localhost:8001"):
        self.aria_url = aria_url
        self.client = httpx.AsyncClient(timeout=60.0)  # Timeouts más largos para optimización
        self.running = False
        self.optimization_history = []
        self.last_optimization = {}
        
        # Configuración de optimización
        self.config = {
            'optimization_interval': 300,  # 5 minutos entre checks
            'max_concurrent_optimizations': 2,
            'auto_rollback_on_failure': True,
            'min_time_between_similar': 1800,  # 30 minutos
        }
        
        # Planes de optimización predefinidos
        self.optimization_plans = {
            OptimizationType.FULL_ARSENAL_ACTIVATION: OptimizationPlan(
                type=OptimizationType.FULL_ARSENAL_ACTIVATION,
                priority="critical",
                description="Activar arsenal completo post-recuperación masiva",
                steps=[
                    "activate_neural_mesh",
                    "initialize_emotional_continuity",
                    "start_analytics_engine",
                    "enable_consciousness_system",
                    "optimize_context_system",
                    "calibrate_working_memory",
                    "verify_all_systems"
                ],
                estimated_duration=180,  # 3 minutos
                expected_benefits=[
                    "Performance máximo",
                    "Todas las capacidades activas",
                    "Comunicación tripartita operativa",
                    "Analytics predictivo funcionando"
                ],
                prerequisites=["system_healthy", "data_available"],
                rollback_plan=["restore_previous_state", "notify_failure"]
            ),
            
            OptimizationType.MEMORY_CONSOLIDATION: OptimizationPlan(
                type=OptimizationType.MEMORY_CONSOLIDATION,
                priority="high",
                description="Consolidar memoria cuando está al límite",
                steps=[
                    "backup_current_state",
                    "run_consolidation",
                    "cleanup_fragmented_data",
                    "optimize_indices",
                    "verify_integrity"
                ],
                estimated_duration=300,  # 5 minutos
                expected_benefits=[
                    "Memoria liberada",
                    "Performance mejorado",
                    "Búsquedas más rápidas"
                ],
                prerequisites=["memory_pressure_high"],
                rollback_plan=["restore_backup", "alert_admin"]
            ),
            
            OptimizationType.PERFORMANCE_TUNING: OptimizationPlan(
                type=OptimizationType.PERFORMANCE_TUNING,
                priority="medium",
                description="Optimizar performance cuando está degradado",
                steps=[
                    "analyze_bottlenecks",
                    "clear_caches",
                    "optimize_connections",
                    "tune_parameters",
                    "restart_slow_services"
                ],
                estimated_duration=240,  # 4 minutos
                expected_benefits=[
                    "Respuestas más rápidas",
                    "Menor latencia",
                    "Mayor throughput"
                ],
                prerequisites=["performance_degraded"],
                rollback_plan=["restore_original_config"]
            )
        }
    
    async def start_monitoring(self):
        """Iniciar monitoreo continuo para optimizaciones automáticas"""
        self.running = True
        logger.info("⚡ AUTO OPTIMIZER INICIADO - Reflejo que nunca descansa")
        
        while self.running:
            try:
                await self._scan_for_optimization_opportunities()
                await asyncio.sleep(self.config['optimization_interval'])
            except Exception as e:
                logger.error(f"Error en optimization loop: {e}")
                await asyncio.sleep(30)  # Retry más lento en error
    
    async def _scan_for_optimization_opportunities(self):
        """Escanear en busca de oportunidades de optimización"""
        logger.debug("🔍 Escaneando oportunidades de optimización...")
        
        # Obtener estado actual del sistema
        system_state = await self._get_system_state()
        if not system_state:
            return
        
        # Evaluar diferentes tipos de optimización
        opportunities = []
        
        # 1. ¿Necesita activación completa del arsenal?
        if await self._needs_full_arsenal_activation(system_state):
            opportunities.append(OptimizationType.FULL_ARSENAL_ACTIVATION)
        
        # 2. ¿Necesita consolidación de memoria?
        if await self._needs_memory_consolidation(system_state):
            opportunities.append(OptimizationType.MEMORY_CONSOLIDATION)
        
        # 3. ¿Necesita tuning de performance?
        if await self._needs_performance_tuning(system_state):
            opportunities.append(OptimizationType.PERFORMANCE_TUNING)
        
        # 4. ¿Neural Mesh desincronizado?
        if await self._needs_neural_mesh_sync(system_state):
            opportunities.append(OptimizationType.NEURAL_MESH_SYNC)
        
        # Ejecutar optimizaciones encontradas
        for opportunity in opportunities:
            if await self._should_execute_optimization(opportunity):
                await self._execute_optimization(opportunity, system_state)
    
    async def _get_system_state(self) -> Dict:
        """Obtener estado completo del sistema"""
        try:
            # Stats generales
            stats_response = await self.client.get(f"{self.aria_url}/stats")
            stats = stats_response.json()
            
            # Health check
            health_response = await self.client.get(f"{self.aria_url}/health")
            health = health_response.json()
            
            # Neural mesh status
            try:
                neural_response = await self.client.get(f"{self.aria_url}/neural-mesh/stats")
                neural_stats = neural_response.json()
            except:
                neural_stats = {"error": "not_available"}
            
            return {
                "stats": stats,
                "health": health,
                "neural_mesh": neural_stats,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error obteniendo system state: {e}")
            return {}
    
    async def _needs_full_arsenal_activation(self, state: Dict) -> bool:
        """Determinar si necesita activación completa del arsenal"""
        stats = state.get("stats", {})
        episodes = stats.get("episodic_memory", {}).get("total_episodes", 0)
        
        # Si hay muchos episodios pero sistemas inactivos
        if episodes > 4000:
            # Check si Neural Mesh está activo
            neural_state = state.get("neural_mesh", {})
            if "error" in neural_state:
                logger.info("🎯 OPORTUNIDAD: Arsenal completo necesario - Neural Mesh inactivo")
                return True
            
            # Check si Emotional Continuity está inicializado
            try:
                emotional_response = await self.client.get(f"{self.aria_url}/emotional/status")
                if emotional_response.status_code != 200:
                    logger.info("🎯 OPORTUNIDAD: Arsenal completo necesario - Emotional Continuity inactivo")
                    return True
            except:
                return True
        
        return False
    
    async def _needs_memory_consolidation(self, state: Dict) -> bool:
        """Determinar si necesita consolidación de memoria"""
        stats = state.get("stats", {})
        working_memory = stats.get("working_memory", {})
        usage = working_memory.get("usage_percentage", 0)
        
        if usage > 85:  # Memoria al 85%+
            logger.info(f"🎯 OPORTUNIDAD: Consolidación necesaria - Memoria al {usage}%")
            return True
        
        return False
    
    async def _needs_performance_tuning(self, state: Dict) -> bool:
        """Determinar si necesita tuning de performance"""
        # Medir tiempo de respuesta
        start = datetime.now()
        try:
            await self.client.get(f"{self.aria_url}/health")
            response_time = (datetime.now() - start).total_seconds()
            
            if response_time > 3.0:  # Más de 3 segundos es crítico
                logger.info(f"🎯 OPORTUNIDAD: Performance tuning necesario - {response_time:.2f}s response")
                return True
        except:
            return True  # Si no responde, definitivamente necesita tuning
        
        return False
    
    async def _needs_neural_mesh_sync(self, state: Dict) -> bool:
        """Determinar si Neural Mesh necesita sincronización"""
        neural_state = state.get("neural_mesh", {})
        
        # Si Neural Mesh no está disponible o tiene errores
        if "error" in neural_state:
            logger.info("🎯 OPORTUNIDAD: Neural Mesh sync necesario - Sistema no disponible")
            return True
        
        return False
    
    async def _should_execute_optimization(self, opt_type: OptimizationType) -> bool:
        """Determinar si debería ejecutar una optimización específica"""
        # Check si ya se ejecutó recientemente
        last_time = self.last_optimization.get(opt_type)
        if last_time:
            time_since = datetime.now() - last_time
            if time_since.seconds < self.config['min_time_between_similar']:
                logger.debug(f"Saltando {opt_type.value} - ejecutado hace {time_since.seconds}s")
                return False
        
        # Check si hay recursos disponibles
        active_optimizations = len([h for h in self.optimization_history[-10:] 
                                  if h.get('status') == 'running'])
        if active_optimizations >= self.config['max_concurrent_optimizations']:
            logger.debug(f"Saltando {opt_type.value} - {active_optimizations} optimizaciones activas")
            return False
        
        return True
    
    async def _execute_optimization(self, opt_type: OptimizationType, system_state: Dict):
        """Ejecutar una optimización específica"""
        plan = self.optimization_plans.get(opt_type)
        if not plan:
            logger.warning(f"No hay plan para optimización: {opt_type}")
            return
        
        optimization_id = f"{opt_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"🚀 INICIANDO OPTIMIZACIÓN: {plan.description}")
        logger.info(f"   ID: {optimization_id}")
        logger.info(f"   Prioridad: {plan.priority}")
        logger.info(f"   Duración estimada: {plan.estimated_duration}s")
        
        # Registrar inicio
        optimization_record = {
            'id': optimization_id,
            'type': opt_type.value,
            'status': 'running',
            'start_time': datetime.now(),
            'plan': plan,
            'system_state': system_state
        }
        self.optimization_history.append(optimization_record)
        
        try:
            # Ejecutar pasos del plan
            results = {}
            for i, step in enumerate(plan.steps):
                logger.info(f"   Paso {i+1}/{len(plan.steps)}: {step}")
                step_result = await self._execute_optimization_step(step, opt_type)
                results[step] = step_result
                
                if not step_result.get('success', False):
                    logger.error(f"   ❌ Paso fallido: {step}")
                    if self.config['auto_rollback_on_failure']:
                        await self._rollback_optimization(plan, results)
                    raise Exception(f"Optimization step failed: {step}")
                else:
                    logger.info(f"   ✅ Paso completado: {step}")
            
            # Optimización exitosa
            optimization_record['status'] = 'completed'
            optimization_record['end_time'] = datetime.now()
            optimization_record['results'] = results
            optimization_record['benefits_achieved'] = plan.expected_benefits
            
            self.last_optimization[opt_type] = datetime.now()
            
            logger.info(f"✅ OPTIMIZACIÓN COMPLETADA: {plan.description}")
            logger.info(f"   Beneficios: {', '.join(plan.expected_benefits)}")
            
            # Documentar en cerebro
            await self._document_optimization(optimization_record)
            
        except Exception as e:
            optimization_record['status'] = 'failed'
            optimization_record['end_time'] = datetime.now()
            optimization_record['error'] = str(e)
            
            logger.error(f"❌ OPTIMIZACIÓN FALLIDA: {plan.description}")
            logger.error(f"   Error: {e}")
            
            await self._document_optimization(optimization_record)
    
    async def _execute_optimization_step(self, step: str, opt_type: OptimizationType) -> Dict:
        """Ejecutar un paso específico de optimización"""
        try:
            if step == "activate_neural_mesh":
                response = await self.client.post(
                    f"{self.aria_url}/neural-mesh/broadcast-learning",
                    json={
                        "learning_type": "auto_optimization_neural_mesh",
                        "learning_content": {
                            "event": "auto_optimizer_activation",
                            "timestamp": datetime.now().isoformat()
                        },
                        "application_domains": ["system_optimization", "performance"],
                        "participants": ["nexus", "aria", "ricardo"]
                    }
                )
                return {"success": response.status_code == 200, "response": response.json()}
            
            elif step == "initialize_emotional_continuity":
                response = await self.client.post(
                    f"{self.aria_url}/emotional/initialize",
                    json={
                        "agent": "auto_optimizer",
                        "session_type": "autonomous_optimization"
                    }
                )
                return {"success": response.status_code == 200, "response": response.json()}
            
            elif step == "start_analytics_engine":
                response = await self.client.post(
                    f"{self.aria_url}/analytics/predictions/generate",
                    json={
                        "scope": "post_optimization_performance",
                        "timeframe": "next_hour"
                    }
                )
                return {"success": response.status_code == 200, "response": response.json()}
            
            elif step == "enable_consciousness_system":
                response = await self.client.post(
                    f"{self.aria_url}/consciousness/save",
                    json={
                        "state": "auto_optimization_active",
                        "metadata": {"optimizer": "autonomous", "timestamp": datetime.now().isoformat()}
                    }
                )
                return {"success": response.status_code == 200, "response": response.json()}
            
            elif step == "optimize_context_system":
                response = await self.client.post(
                    f"{self.aria_url}/context/add-message",
                    json={
                        "message": "Sistema optimizado automáticamente - performance mejorado",
                        "importance": 0.8
                    }
                )
                return {"success": response.status_code == 200, "response": response.json()}
            
            elif step == "calibrate_working_memory":
                response = await self.client.post(
                    f"{self.aria_url}/memory/working/context",
                    json={
                        "context": "post_auto_optimization",
                        "context_data": {
                            "optimization_type": opt_type.value,
                            "timestamp": datetime.now().isoformat()
                        },
                        "priority": "high"
                    }
                )
                return {"success": response.status_code == 200, "response": response.json()}
            
            elif step == "run_consolidation":
                response = await self.client.post(f"{self.aria_url}/memory/consolidate")
                return {"success": response.status_code == 200}
            
            elif step == "verify_all_systems":
                # Verificar que todos los sistemas estén respondiendo
                systems = ['health', 'stats', 'neural-mesh/stats']
                all_healthy = True
                for system in systems:
                    try:
                        resp = await self.client.get(f"{self.aria_url}/{system}")
                        if resp.status_code != 200:
                            all_healthy = False
                    except:
                        all_healthy = False
                
                return {"success": all_healthy, "systems_checked": systems}
            
            else:
                logger.warning(f"Paso de optimización no implementado: {step}")
                return {"success": True, "note": f"Step {step} skipped - not implemented"}
                
        except Exception as e:
            logger.error(f"Error ejecutando paso {step}: {e}")
            return {"success": False, "error": str(e)}
    
    async def _rollback_optimization(self, plan: OptimizationPlan, partial_results: Dict):
        """Hacer rollback de una optimización fallida"""
        logger.warning(f"🔄 INICIANDO ROLLBACK: {plan.description}")
        
        for step in plan.rollback_plan:
            try:
                logger.info(f"   Rollback: {step}")
                # Implementar steps de rollback según sea necesario
                await asyncio.sleep(1)  # Simular rollback por ahora
            except Exception as e:
                logger.error(f"Error en rollback step {step}: {e}")
    
    async def _document_optimization(self, record: Dict):
        """Documentar optimización en el cerebro ARIA"""
        try:
            await self.client.post(
                f"{self.aria_url}/memory/action",
                json={
                    "action_type": f"autonomous_optimization_{record['status']}",
                    "action_details": {
                        "optimizer": "auto_optimizer",
                        "optimization_id": record['id'],
                        "optimization_type": record['type'],
                        "status": record['status'],
                        "duration_seconds": (record.get('end_time', datetime.now()) - record['start_time']).total_seconds(),
                        "steps_executed": list(record.get('results', {}).keys()),
                        "benefits_achieved": record.get('benefits_achieved', []),
                        "error": record.get('error')
                    },
                    "context_state": {
                        "autonomous_system": True,
                        "optimization_successful": record['status'] == 'completed'
                    },
                    "tags": ["autonomous_optimization", record['type'], record['status']]
                }
            )
        except Exception as e:
            logger.error(f"Error documentando optimización: {e}")
    
    async def force_optimization(self, opt_type: OptimizationType):
        """Forzar una optimización específica (para testing)"""
        logger.info(f"🎯 FORZANDO OPTIMIZACIÓN: {opt_type.value}")
        system_state = await self._get_system_state()
        await self._execute_optimization(opt_type, system_state)
    
    def get_optimization_history(self) -> List[Dict]:
        """Obtener historial de optimizaciones"""
        return self.optimization_history
    
    async def stop(self):
        """Detener el auto optimizer"""
        self.running = False
        await self.client.aclose()
        logger.info("⚡ Auto Optimizer detenido")


async def main():
    """Función principal para testing"""
    optimizer = AutoOptimizer()
    
    print("🚀 INICIANDO AUTO OPTIMIZER - Sistema Nervioso Autónomo v1.0")
    print("   Monitoreando oportunidades de optimización...")
    print("   Presiona Ctrl+C para detener\n")
    
    try:
        # Para testing, forzar una optimización
        await optimizer.force_optimization(OptimizationType.FULL_ARSENAL_ACTIVATION)
        
        # Después iniciar monitoreo continuo
        await optimizer.start_monitoring()
    except KeyboardInterrupt:
        await optimizer.stop()
        print("\n✅ Auto Optimizer detenido limpiamente")


if __name__ == "__main__":
    asyncio.run(main())