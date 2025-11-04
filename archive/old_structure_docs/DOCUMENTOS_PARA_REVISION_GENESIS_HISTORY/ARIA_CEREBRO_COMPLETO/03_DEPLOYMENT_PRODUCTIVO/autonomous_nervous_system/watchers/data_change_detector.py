#!/usr/bin/env python3
"""
🔍 DATA CHANGE DETECTOR - El Ojo que Nunca Duerme
Detecta cambios significativos en el cerebro ARIA y dispara acciones automáticas
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import httpx
from dataclasses import dataclass
from enum import Enum

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ChangeType(Enum):
    """Tipos de cambios que podemos detectar"""
    MASSIVE_RECOVERY = "massive_recovery"  # >1000 episodios nuevos
    SIGNIFICANT_GROWTH = "significant_growth"  # >100 episodios nuevos
    PATTERN_EMERGENCE = "pattern_emergence"  # Nuevo pattern detectado
    PERFORMANCE_DEGRADATION = "performance_degradation"  # Sistema lento
    ANOMALY_DETECTED = "anomaly_detected"  # Comportamiento inusual
    BREAKTHROUGH_MOMENT = "breakthrough_moment"  # Momento eureka detectado
    MEMORY_CONSOLIDATION = "memory_consolidation"  # Consolidación necesaria
    SYSTEM_OPTIMIZATION = "system_optimization"  # Oportunidad de optimizar


@dataclass
class ChangeEvent:
    """Evento de cambio detectado"""
    type: ChangeType
    severity: str  # "low", "medium", "high", "critical"
    description: str
    data: Dict[str, Any]
    timestamp: datetime
    requires_action: bool
    suggested_actions: List[str]


class DataChangeDetector:
    """
    El Vigilante Eterno del Cerebro Digital
    Detecta cambios y despierta al sistema nervioso
    """
    
    def __init__(self, aria_url: str = "http://localhost:8001"):
        self.aria_url = aria_url
        self.client = httpx.AsyncClient(timeout=30.0)
        self.last_check = datetime.now()
        self.last_stats = {}
        self.running = False
        self.check_interval = 60  # segundos
        self.change_callbacks = []
        
        # Thresholds configurables
        self.thresholds = {
            'massive_recovery': 1000,      # episodios
            'significant_growth': 100,     # episodios
            'performance_alert': 0.8,      # 80% degradación
            'memory_pressure': 0.9,         # 90% memoria usada
            'pattern_confidence': 0.7,      # 70% confianza mínima
        }
    
    async def start(self):
        """Iniciar el monitoreo continuo"""
        self.running = True
        logger.info("🔍 DATA CHANGE DETECTOR INICIADO - El ojo que nunca duerme")
        
        # Obtener estado inicial
        self.last_stats = await self._get_current_stats()
        
        # Loop eterno de vigilancia
        while self.running:
            try:
                await self._scan_for_changes()
                await asyncio.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Error en scan loop: {e}")
                await asyncio.sleep(5)  # Retry rápido
    
    async def _get_current_stats(self) -> Dict:
        """Obtener estadísticas actuales del cerebro"""
        try:
            response = await self.client.get(f"{self.aria_url}/stats")
            return response.json()
        except Exception as e:
            logger.error(f"Error obteniendo stats: {e}")
            return {}
    
    async def _scan_for_changes(self):
        """Escanear en busca de cambios significativos"""
        current_stats = await self._get_current_stats()
        
        if not current_stats or not self.last_stats:
            self.last_stats = current_stats
            return
        
        # Detectar diferentes tipos de cambios
        changes = []
        
        # 1. MASSIVE RECOVERY - Recuperación masiva de episodios
        episode_diff = self._get_episode_difference(current_stats)
        if episode_diff > self.thresholds['massive_recovery']:
            changes.append(ChangeEvent(
                type=ChangeType.MASSIVE_RECOVERY,
                severity="critical",
                description=f"¡RECUPERACIÓN MASIVA! {episode_diff} episodios nuevos detectados",
                data={
                    'episodes_recovered': episode_diff,
                    'total_episodes': current_stats.get('episodic_memory', {}).get('total_episodes', 0)
                },
                timestamp=datetime.now(),
                requires_action=True,
                suggested_actions=[
                    "activate_full_arsenal",
                    "optimize_all_systems",
                    "generate_recovery_report",
                    "broadcast_to_neural_mesh"
                ]
            ))
        
        # 2. SIGNIFICANT GROWTH - Crecimiento significativo
        elif episode_diff > self.thresholds['significant_growth']:
            changes.append(ChangeEvent(
                type=ChangeType.SIGNIFICANT_GROWTH,
                severity="high",
                description=f"Crecimiento significativo: {episode_diff} episodios nuevos",
                data={'episodes_added': episode_diff},
                timestamp=datetime.now(),
                requires_action=True,
                suggested_actions=[
                    "analyze_new_episodes",
                    "update_patterns",
                    "consolidate_if_needed"
                ]
            ))
        
        # 3. PERFORMANCE CHECK - Verificar degradación
        performance_issue = await self._check_performance()
        if performance_issue:
            changes.append(performance_issue)
        
        # 4. MEMORY PRESSURE - Presión de memoria
        memory_pressure = self._check_memory_pressure(current_stats)
        if memory_pressure:
            changes.append(memory_pressure)
        
        # 5. PATTERN DETECTION - Buscar patterns emergentes
        patterns = await self._detect_emerging_patterns(current_stats)
        changes.extend(patterns)
        
        # Procesar todos los cambios detectados
        for change in changes:
            await self._handle_change(change)
        
        # Actualizar last_stats
        self.last_stats = current_stats
        self.last_check = datetime.now()
    
    def _get_episode_difference(self, current_stats: Dict) -> int:
        """Calcular diferencia en número de episodios"""
        try:
            current = current_stats.get('episodic_memory', {}).get('total_episodes', 0)
            last = self.last_stats.get('episodic_memory', {}).get('total_episodes', 0)
            return current - last
        except:
            return 0
    
    async def _check_performance(self) -> Optional[ChangeEvent]:
        """Verificar si hay degradación de performance"""
        try:
            # Medir tiempo de respuesta
            start = datetime.now()
            response = await self.client.get(f"{self.aria_url}/health")
            elapsed = (datetime.now() - start).total_seconds()
            
            if elapsed > 2.0:  # Más de 2 segundos es preocupante
                return ChangeEvent(
                    type=ChangeType.PERFORMANCE_DEGRADATION,
                    severity="high" if elapsed > 5 else "medium",
                    description=f"Sistema respondiendo lento: {elapsed:.2f}s",
                    data={'response_time': elapsed},
                    timestamp=datetime.now(),
                    requires_action=True,
                    suggested_actions=[
                        "run_optimization",
                        "check_resource_usage",
                        "restart_if_critical"
                    ]
                )
        except Exception as e:
            logger.error(f"Error checking performance: {e}")
        return None
    
    def _check_memory_pressure(self, stats: Dict) -> Optional[ChangeEvent]:
        """Verificar presión de memoria"""
        try:
            working_memory = stats.get('working_memory', {})
            usage = working_memory.get('usage_percentage', 0) / 100
            
            if usage > self.thresholds['memory_pressure']:
                return ChangeEvent(
                    type=ChangeType.MEMORY_CONSOLIDATION,
                    severity="high",
                    description=f"Memoria al {usage*100:.1f}% - Consolidación necesaria",
                    data={'memory_usage': usage},
                    timestamp=datetime.now(),
                    requires_action=True,
                    suggested_actions=[
                        "trigger_consolidation",
                        "cleanup_old_data",
                        "optimize_memory_usage"
                    ]
                )
        except Exception as e:
            logger.error(f"Error checking memory: {e}")
        return None
    
    async def _detect_emerging_patterns(self, stats: Dict) -> List[ChangeEvent]:
        """Detectar patterns emergentes en los datos"""
        patterns = []
        
        try:
            # Buscar concentración de actividad reciente
            response = await self.client.get(
                f"{self.aria_url}/memory/episodic/recent?limit=50"
            )
            recent = response.json()
            
            # Analizar tipos de acciones frecuentes
            action_types = {}
            for episode in recent:
                action_type = episode.get('action_type', 'unknown')
                action_types[action_type] = action_types.get(action_type, 0) + 1
            
            # Detectar si hay un pattern dominante
            if action_types:
                dominant = max(action_types, key=action_types.get)
                concentration = action_types[dominant] / len(recent)
                
                if concentration > 0.5:  # Más del 50% es un pattern
                    patterns.append(ChangeEvent(
                        type=ChangeType.PATTERN_EMERGENCE,
                        severity="medium",
                        description=f"Pattern detectado: {dominant} ({concentration*100:.1f}% concentración)",
                        data={
                            'pattern_type': dominant,
                            'concentration': concentration,
                            'sample_size': len(recent)
                        },
                        timestamp=datetime.now(),
                        requires_action=True,
                        suggested_actions=[
                            "analyze_pattern_deeply",
                            "generate_insights",
                            "notify_relevant_agents"
                        ]
                    ))
            
            # Detectar momentos breakthrough
            for episode in recent[:10]:  # Últimos 10
                if 'breakthrough' in str(episode).lower():
                    patterns.append(ChangeEvent(
                        type=ChangeType.BREAKTHROUGH_MOMENT,
                        severity="high",
                        description="¡BREAKTHROUGH DETECTADO! Momento eureka encontrado",
                        data={'episode': episode},
                        timestamp=datetime.now(),
                        requires_action=True,
                        suggested_actions=[
                            "capture_breakthrough_context",
                            "amplify_discovery",
                            "broadcast_to_all_agents",
                            "document_for_learning"
                        ]
                    ))
                    break
                    
        except Exception as e:
            logger.error(f"Error detecting patterns: {e}")
        
        return patterns
    
    async def _handle_change(self, change: ChangeEvent):
        """Manejar un cambio detectado"""
        logger.info(f"🚨 CAMBIO DETECTADO: {change.type.value}")
        logger.info(f"   Severidad: {change.severity}")
        logger.info(f"   Descripción: {change.description}")
        
        if change.requires_action:
            logger.info(f"   ⚡ ACCIONES SUGERIDAS: {', '.join(change.suggested_actions)}")
            
            # Aquí es donde el sistema nervioso toma acción
            await self._trigger_reflexes(change)
        
        # Notificar a callbacks registrados
        for callback in self.change_callbacks:
            try:
                await callback(change)
            except Exception as e:
                logger.error(f"Error en callback: {e}")
        
        # Documentar en cerebro
        await self._document_change(change)
    
    async def _trigger_reflexes(self, change: ChangeEvent):
        """Disparar reflexes automáticos basados en el cambio"""
        # Este es el puente con el sistema de REFLEXES
        # Por ahora solo logueamos, pero aquí conectaremos con auto_optimizer.py, etc.
        
        if change.type == ChangeType.MASSIVE_RECOVERY:
            logger.info("🔥 INICIANDO PROTOCOLO DE RECUPERACIÓN MASIVA AUTOMÁTICA")
            # TODO: Conectar con auto_optimizer.py
            # await self.auto_optimizer.optimize_for_recovery(change.data)
        
        elif change.type == ChangeType.BREAKTHROUGH_MOMENT:
            logger.info("💡 AMPLIFICANDO BREAKTHROUGH DETECTADO")
            # TODO: Conectar con auto_communicator.py
            # await self.auto_communicator.broadcast_breakthrough(change.data)
    
    async def _document_change(self, change: ChangeEvent):
        """Documentar el cambio en el cerebro ARIA"""
        try:
            await self.client.post(
                f"{self.aria_url}/memory/action",
                json={
                    "action_type": f"autonomous_change_detected_{change.type.value}",
                    "action_details": {
                        "detector": "data_change_detector",
                        "change_type": change.type.value,
                        "severity": change.severity,
                        "description": change.description,
                        "data": change.data,
                        "suggested_actions": change.suggested_actions,
                        "timestamp": change.timestamp.isoformat()
                    },
                    "context_state": {
                        "autonomous_system": True,
                        "requires_action": change.requires_action
                    },
                    "tags": ["autonomous_detection", change.type.value, change.severity]
                }
            )
        except Exception as e:
            logger.error(f"Error documentando cambio: {e}")
    
    def register_callback(self, callback):
        """Registrar callback para ser notificado de cambios"""
        self.change_callbacks.append(callback)
    
    async def stop(self):
        """Detener el detector"""
        self.running = False
        await self.client.aclose()
        logger.info("🔍 Data Change Detector detenido")


async def main():
    """Función principal para testing"""
    detector = DataChangeDetector()
    
    # Callback de ejemplo
    async def on_change(change: ChangeEvent):
        print(f"\n🎯 CAMBIO RECIBIDO EN CALLBACK:")
        print(f"   Tipo: {change.type.value}")
        print(f"   Acciones: {change.suggested_actions}")
    
    detector.register_callback(on_change)
    
    try:
        await detector.start()
    except KeyboardInterrupt:
        await detector.stop()
        print("\n✅ Detector detenido limpiamente")


if __name__ == "__main__":
    print("🚀 INICIANDO DATA CHANGE DETECTOR - Sistema Nervioso Autónomo v1.0")
    print("   Monitoreando cambios en el cerebro ARIA...")
    print("   Presiona Ctrl+C para detener\n")
    asyncio.run(main())