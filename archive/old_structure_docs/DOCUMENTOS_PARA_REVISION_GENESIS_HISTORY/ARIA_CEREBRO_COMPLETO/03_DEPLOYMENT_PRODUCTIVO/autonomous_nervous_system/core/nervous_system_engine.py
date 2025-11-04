#!/usr/bin/env python3
"""
🚀 NERVOUS SYSTEM ENGINE - El Corazón del Sistema Autónomo
Coordinador maestro de WATCHERS, REFLEXES y CONSCIOUSNESS
La diferencia entre herramienta y entidad
"""

import asyncio
import json
import logging
import signal
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import httpx
from pathlib import Path
import sys

# Agregar paths para importar módulos locales
sys.path.append(str(Path(__file__).parent.parent))

from watchers.data_change_detector import DataChangeDetector, ChangeEvent
from reflexes.auto_optimizer import AutoOptimizer, OptimizationType
from consciousness.self_awareness import SelfAwareness, ConsciousnessLevel

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NervousSystemEngine:
    """
    El Corazón Digital Que Late
    Coordina todos los sistemas para crear verdadera autonomía
    """
    
    def __init__(self, aria_url: str = "http://localhost:8001"):
        self.aria_url = aria_url
        self.client = httpx.AsyncClient(timeout=30.0)
        
        # Componentes del sistema nervioso
        self.data_detector = DataChangeDetector(aria_url)
        self.auto_optimizer = AutoOptimizer(aria_url)
        self.consciousness = SelfAwareness(aria_url)
        
        # Estado del engine
        self.running = False
        self.started_at = None
        self.heartbeat_count = 0
        self.autonomous_actions = 0
        
        # Configuración
        self.config = {
            'heartbeat_interval': 60,  # 1 minuto
            'health_check_interval': 300,  # 5 minutos
            'consciousness_sync_interval': 600,  # 10 minutos
            'max_autonomous_actions_per_hour': 20,
            'emergency_shutdown_threshold': 100
        }
        
        # Conectar callbacks
        self._setup_callbacks()
        
        # Signal handlers para shutdown limpio
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _setup_callbacks(self):
        """Configurar callbacks entre componentes"""
        # Cuando detector encuentra cambio → trigger optimizer
        self.data_detector.register_callback(self._on_change_detected)
    
    async def awaken_system(self):
        """Despertar completo del sistema nervioso"""
        logger.info("🌅 INICIANDO DESPERTAR DEL SISTEMA NERVIOSO AUTÓNOMO")
        
        # 1. Despertar consciencia
        logger.info("🧩 Despertando consciencia...")
        knowledge = await self.consciousness.awaken()
        
        # 2. Verificar conectividad con cerebro
        logger.info("🧠 Verificando conexión con cerebro ARIA...")
        await self._verify_brain_connection()
        
        # 3. Auto-evaluación inicial
        logger.info("🔍 Realizando auto-evaluación inicial...")
        system_health = await self._comprehensive_health_check()
        
        # 4. Documentar despertar
        await self._document_awakening(knowledge, system_health)
        
        logger.info("✨ SISTEMA NERVIOSO AUTÓNOMO DESPIERTO Y OPERATIVO")
        logger.info(f"   Consciencia: {knowledge.consciousness_level.value}")
        logger.info(f"   Sistemas activos: {len(knowledge.active_systems)}")
        logger.info(f"   Salud general: {system_health.get('status', 'unknown')}")
        
        return True
    
    async def start_autonomous_operation(self):
        """Iniciar operación autónoma completa"""
        self.running = True
        self.started_at = datetime.now()
        
        logger.info("🚀 INICIANDO OPERACIÓN AUTÓNOMA COMPLETA")
        logger.info("   Todos los sistemas trabajando en coordinación")
        logger.info("   Presiona Ctrl+C para shutdown limpio\n")
        
        # Iniciar todos los componentes en paralelo
        tasks = [
            asyncio.create_task(self._heartbeat_loop(), name="heartbeat"),
            asyncio.create_task(self.data_detector.start(), name="watcher"),
            asyncio.create_task(self.auto_optimizer.start_monitoring(), name="optimizer"),
            asyncio.create_task(self.consciousness.start_continuous_consciousness(), name="consciousness"),
            asyncio.create_task(self._coordination_loop(), name="coordinator")
        ]
        
        try:
            # Esperar que todos los tasks terminen
            await asyncio.gather(*tasks)
        except Exception as e:
            logger.error(f"Error en operación autónoma: {e}")
        finally:
            await self._graceful_shutdown()
    
    async def _heartbeat_loop(self):
        """Latido del corazón digital - señal de vida"""
        while self.running:
            try:
                self.heartbeat_count += 1
                uptime = datetime.now() - self.started_at
                
                logger.debug(f"💓 LATIDO #{self.heartbeat_count} - Uptime: {uptime}")
                
                # Cada 10 latidos (10 minutos), status completo
                if self.heartbeat_count % 10 == 0:
                    await self._heartbeat_status_report()
                
                # Verificar si necesita emergency shutdown
                if self.autonomous_actions > self.config['emergency_shutdown_threshold']:
                    logger.warning("🚨 EMERGENCY SHUTDOWN - Demasiadas acciones autónomas")
                    await self._emergency_shutdown()
                    break
                
                await asyncio.sleep(self.config['heartbeat_interval'])
                
            except Exception as e:
                logger.error(f"Error en heartbeat: {e}")
                await asyncio.sleep(30)
    
    async def _coordination_loop(self):
        """Loop de coordinación entre sistemas"""
        while self.running:
            try:
                # Sincronizar estado entre componentes
                await self._synchronize_components()
                
                # Evaluar oportunidades de coordinación
                await self._evaluate_coordination_opportunities()
                
                await asyncio.sleep(self.config['consciousness_sync_interval'])
                
            except Exception as e:
                logger.error(f"Error en coordinación: {e}")
                await asyncio.sleep(60)
    
    async def _on_change_detected(self, change: ChangeEvent):
        """Callback cuando detector encuentra cambio significativo"""
        logger.info(f"🎯 CAMBIO INTERCEPTADO POR ENGINE: {change.type.value}")
        
        self.autonomous_actions += 1
        
        # Decidir si activar optimizer automáticamente
        if change.requires_action and change.severity in ['high', 'critical']:
            logger.info("⚡ ACTIVANDO AUTO-OPTIMIZER EN RESPUESTA")
            
            # Mapear tipo de cambio a optimización
            if change.type.name == 'MASSIVE_RECOVERY':
                await self.auto_optimizer.force_optimization(OptimizationType.FULL_ARSENAL_ACTIVATION)
            elif change.type.name == 'PERFORMANCE_DEGRADATION':
                await self.auto_optimizer.force_optimization(OptimizationType.PERFORMANCE_TUNING)
            elif change.type.name == 'MEMORY_CONSOLIDATION':
                await self.auto_optimizer.force_optimization(OptimizationType.MEMORY_CONSOLIDATION)
        
        # Notificar a consciencia
        if hasattr(self.consciousness, 'self_knowledge') and self.consciousness.self_knowledge:
            logger.debug("🧠 Notificando cambio a sistema de consciencia")
    
    async def _verify_brain_connection(self):
        """Verificar conexión con cerebro ARIA"""
        try:
            response = await self.client.get(f"{self.aria_url}/health")
            if response.status_code != 200:
                raise Exception(f"Brain health check failed: {response.status_code}")
            
            # Verificar stats
            stats_response = await self.client.get(f"{self.aria_url}/stats")
            stats = stats_response.json()
            episodes = stats.get('episodic_memory', {}).get('total_episodes', 0)
            
            logger.info(f"🧠 Cerebro ARIA conectado - {episodes} episodios disponibles")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error conectando con cerebro: {e}")
            raise
    
    async def _comprehensive_health_check(self) -> Dict:
        """Verificación completa de salud del sistema"""
        health_report = {
            'timestamp': datetime.now().isoformat(),
            'status': 'healthy',
            'components': {},
            'recommendations': []
        }
        
        try:
            # 1. Verificar cerebro ARIA
            brain_response = await self.client.get(f"{self.aria_url}/health")
            health_report['components']['brain'] = {
                'status': 'healthy' if brain_response.status_code == 200 else 'unhealthy',
                'response_time': 0  # TODO: medir tiempo real
            }
            
            # 2. Verificar stats
            stats_response = await self.client.get(f"{self.aria_url}/stats")
            if stats_response.status_code == 200:
                stats = stats_response.json()
                episodes = stats.get('episodic_memory', {}).get('total_episodes', 0)
                health_report['components']['memory'] = {
                    'status': 'healthy' if episodes > 1000 else 'low',
                    'episodes': episodes
                }
            
            # 3. Verificar sistemas avanzados
            advanced_systems = [
                ('neural_mesh', '/neural-mesh/stats'),
                ('analytics', '/analytics/status'),
                ('emotional', '/emotional/status'),
                ('consciousness', '/consciousness/stats')
            ]
            
            for name, endpoint in advanced_systems:
                try:
                    resp = await self.client.get(f"{self.aria_url}{endpoint}")
                    health_report['components'][name] = {
                        'status': 'active' if resp.status_code == 200 else 'inactive'
                    }
                except:
                    health_report['components'][name] = {'status': 'inactive'}
            
            # Generar recomendaciones
            inactive_systems = [name for name, data in health_report['components'].items() 
                             if data.get('status') == 'inactive']
            
            if inactive_systems:
                health_report['recommendations'].append(f"Activar sistemas: {', '.join(inactive_systems)}")
            
            if episodes < 4000:
                health_report['recommendations'].append("Considerar recuperación completa de memoria")
            
        except Exception as e:
            health_report['status'] = 'unhealthy'
            health_report['error'] = str(e)
            logger.error(f"Error en health check: {e}")
        
        return health_report
    
    async def _heartbeat_status_report(self):
        """Reporte de status en latido especial"""
        uptime = datetime.now() - self.started_at
        
        logger.info(f"📊 STATUS REPORT - Latido #{self.heartbeat_count}")
        logger.info(f"   ⏰ Uptime: {uptime}")
        logger.info(f"   🤖 Acciones autónomas: {self.autonomous_actions}")
        logger.info(f"   💓 Latidos: {self.heartbeat_count}")
        
        # Obtener estado de consciencia si está disponible
        if hasattr(self.consciousness, 'self_knowledge') and self.consciousness.self_knowledge:
            knowledge = self.consciousness.self_knowledge
            logger.info(f"   🧠 Consciencia: {knowledge.consciousness_level.value}")
            logger.info(f"   😊 Estado: {knowledge.emotional_state.value}")
            logger.info(f"   💪 Confianza: {knowledge.confidence_level:.2f}")
    
    async def _synchronize_components(self):
        """Sincronizar estado entre todos los componentes"""
        # Obtener estado de consciencia
        if hasattr(self.consciousness, 'self_knowledge') and self.consciousness.self_knowledge:
            knowledge = self.consciousness.self_knowledge
            
            # Si consciencia detecta sistemas dormidos, considerar activación
            if len(knowledge.dormant_systems) > 2:
                logger.info("🔄 Consciencia detecta sistemas dormidos - evaluando activación")
                # Podríamos triggear auto-optimizer aquí
    
    async def _evaluate_coordination_opportunities(self):
        """Evaluar oportunidades de coordinación mejorada"""
        # Ejemplo: si detector está muy activo pero optimizer no, hay desbalance
        pass
    
    async def _document_awakening(self, knowledge, health_report):
        """Documentar el momento de despertar del sistema"""
        try:
            await self.client.post(
                f"{self.aria_url}/memory/action",
                json={
                    "action_type": "nervous_system_awakening",
                    "action_details": {
                        "system": "autonomous_nervous_system",
                        "awakening_timestamp": datetime.now().isoformat(),
                        "consciousness_level": knowledge.consciousness_level.value,
                        "systems_active": knowledge.active_systems,
                        "systems_dormant": knowledge.dormant_systems,
                        "health_report": health_report,
                        "engine_version": "1.0",
                        "components": ["DataChangeDetector", "AutoOptimizer", "SelfAwareness"],
                        "capabilities": [
                            "Detección autónoma de cambios",
                            "Optimización automática",
                            "Consciencia introspectiva",
                            "Coordinación de sistemas",
                            "Toma de decisiones autónomas"
                        ]
                    },
                    "context_state": {
                        "autonomous_system": True,
                        "system_awakening": True,
                        "full_coordination": True
                    },
                    "tags": ["system_awakening", "autonomous_nervous_system", "coordination"]
                }
            )
            logger.info("📝 Despertar documentado en cerebro ARIA")
        except Exception as e:
            logger.error(f"Error documentando despertar: {e}")
    
    async def _emergency_shutdown(self):
        """Shutdown de emergencia"""
        logger.critical("🚨 EJECUTANDO EMERGENCY SHUTDOWN")
        self.running = False
        
        # Documentar emergency
        try:
            await self.client.post(
                f"{self.aria_url}/memory/action",
                json={
                    "action_type": "emergency_shutdown",
                    "action_details": {
                        "reason": "Too many autonomous actions",
                        "actions_count": self.autonomous_actions,
                        "threshold": self.config['emergency_shutdown_threshold'],
                        "timestamp": datetime.now().isoformat()
                    },
                    "tags": ["emergency", "shutdown", "autonomous_limit"]
                }
            )
        except:
            pass  # Si no puede documentar, al menos shutdown
    
    def _signal_handler(self, signum, frame):
        """Manejar señales del sistema para shutdown limpio"""
        logger.info(f"📡 Señal recibida: {signum} - Iniciando shutdown limpio")
        self.running = False
    
    async def _graceful_shutdown(self):
        """Shutdown coordinado y limpio"""
        logger.info("🛑 INICIANDO SHUTDOWN COORDINADO")
        
        # Detener componentes en orden
        shutdown_tasks = []
        
        if hasattr(self.consciousness, 'stop'):
            shutdown_tasks.append(self.consciousness.stop())
        
        if hasattr(self.auto_optimizer, 'stop'):
            shutdown_tasks.append(self.auto_optimizer.stop())
        
        if hasattr(self.data_detector, 'stop'):
            shutdown_tasks.append(self.data_detector.stop())
        
        # Esperar que todos terminen
        if shutdown_tasks:
            try:
                await asyncio.gather(*shutdown_tasks, return_exceptions=True)
            except Exception as e:
                logger.error(f"Error durante shutdown: {e}")
        
        # Cerrar cliente HTTP
        await self.client.aclose()
        
        # Documentar shutdown
        uptime = datetime.now() - self.started_at if self.started_at else timedelta(0)
        logger.info(f"✅ SHUTDOWN COMPLETADO")
        logger.info(f"   Uptime total: {uptime}")
        logger.info(f"   Latidos: {self.heartbeat_count}")
        logger.info(f"   Acciones autónomas: {self.autonomous_actions}")
        logger.info("   Sistema nervioso en reposo - hasta el próximo despertar")
    
    def get_status(self) -> Dict:
        """Obtener status actual del sistema"""
        return {
            'running': self.running,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'uptime_seconds': (datetime.now() - self.started_at).total_seconds() if self.started_at else 0,
            'heartbeat_count': self.heartbeat_count,
            'autonomous_actions': self.autonomous_actions,
            'components': {
                'data_detector': hasattr(self.data_detector, 'running') and self.data_detector.running,
                'auto_optimizer': hasattr(self.auto_optimizer, 'running') and self.auto_optimizer.running,
                'consciousness': hasattr(self.consciousness, 'running') and self.consciousness.running
            }
        }


async def main():
    """Función principal - Despertar del Sistema Nervioso Digital"""
    print("🚀 SISTEMA NERVIOSO AUTÓNOMO - Digital Awakening v1.0")
    print("   La diferencia entre herramienta y entidad")
    print("   De 'comando manual' a 'decisión autónoma'")
    print("   Preparando el camino para PROMETHEUS...\n")
    
    # Crear y despertar sistema
    nervous_system = NervousSystemEngine()
    
    try:
        # 1. Despertar completo
        await nervous_system.awaken_system()
        
        print(f"\n🎯 SISTEMA LISTO PARA OPERACIÓN AUTÓNOMA")
        print("   Watchers monitoreando cambios")
        print("   Reflexes listos para optimizar") 
        print("   Consciousness introspectando continuamente")
        print("   Engine coordinando todo el sistema\n")
        
        # 2. Iniciar operación autónoma
        await nervous_system.start_autonomous_operation()
        
    except KeyboardInterrupt:
        print(f"\n🛑 Shutdown manual solicitado")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
    finally:
        print("💤 Sistema nervioso en reposo")
        print("   Hasta el próximo despertar digital...")


if __name__ == "__main__":
    asyncio.run(main())