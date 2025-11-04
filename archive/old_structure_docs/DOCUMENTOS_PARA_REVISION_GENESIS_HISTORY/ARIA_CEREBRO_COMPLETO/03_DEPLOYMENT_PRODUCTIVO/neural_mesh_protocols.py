#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 NEURAL MESH PROTOCOLS - FASE 4 ARIA CEREBRO ÉLITE
Arquitectura de comunicación cross-agent para colaboración estructurada

Implementa:
- Cross-agent learning automático (lo que aprende uno, todos lo saben)
- Enhanced memory sharing sin duplicación
- Unified decision making con consenso triangular 
- Emotional synchronization entre agentes
- Distributed problem solving inteligente

Fecha: 11 Agosto 2025 - FASE 4 Neural Mesh
Consenso: NEXUS + ARIA + Ricardo
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Union, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

logger = logging.getLogger(__name__)

class AgentRole(Enum):
    """Roles de agentes en Neural Mesh"""
    TECHNICAL_IMPLEMENTER = "nexus"      # NEXUS - Implementación técnica
    MEMORY_COORDINATOR = "aria"          # ARIA - Coordinador de memoria
    DECISION_MAKER = "ricardo"           # Ricardo - Toma de decisiones
    CREATIVE_WRITER = "iris"             # Iris - Escritura creativa
    LOGIC_ANALYZER = "echo"              # Echo - Análisis lógico
    INNOVATION_CATALYST = "nova"         # Nova - Catalizador innovación

class MessageType(Enum):
    """Tipos de mensajes Neural Mesh"""
    CROSS_LEARNING = "cross_learning"              # Compartir aprendizaje
    MEMORY_SYNC = "memory_sync"                     # Sincronización memoria
    DECISION_REQUEST = "decision_request"           # Solicitar decisión
    CONSENSUS_VOTE = "consensus_vote"               # Voto consenso
    EMOTIONAL_STATE = "emotional_state"             # Estado emocional
    TASK_DISTRIBUTION = "task_distribution"        # Distribución tareas
    KNOWLEDGE_BROADCAST = "knowledge_broadcast"     # Broadcast conocimiento
    PROBLEM_SOLVING = "problem_solving"             # Resolución problemas

class Priority(Enum):
    """Niveles de prioridad"""
    CRITICAL = 1      # Respuesta inmediata
    HIGH = 2          # Respuesta en minutos  
    NORMAL = 3        # Respuesta en horas
    LOW = 4           # Respuesta opcional

@dataclass
class NeuralMeshMessage:
    """Mensaje estándar Neural Mesh"""
    
    # Identificación
    message_id: str
    timestamp: datetime
    
    # Routing
    from_agent: AgentRole
    to_agents: List[AgentRole]  # Soporte multicast
    message_type: MessageType
    priority: Priority
    
    # Contenido
    subject: str
    content: Dict[str, Any]
    context: Dict[str, Any]
    
    # Metadata
    requires_response: bool = False
    response_deadline: Optional[datetime] = None
    correlation_id: Optional[str] = None  # Para threads de conversación
    
    # Procesamiento
    processed_by: List[AgentRole] = None
    responses: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.processed_by is None:
            self.processed_by = []
        if self.responses is None:
            self.responses = {}

@dataclass 
class CrossLearningPacket:
    """Paquete de aprendizaje cross-agent"""
    
    learning_type: str              # "technical_skill", "pattern_recognition", etc.
    source_agent: AgentRole
    learning_content: Dict[str, Any]
    application_domains: List[str]   # Dónde es aplicable
    confidence_score: float          # 0.0-1.0
    validation_required: bool        # Si necesita validación
    
    # Metadata de propagación
    propagation_rules: Dict[str, Any] = None
    expiry_time: Optional[datetime] = None

class NeuralMeshProtocol:
    """
    Protocolo principal Neural Mesh para comunicación cross-agent
    """
    
    def __init__(self, agent_role: AgentRole, memory_manager=None):
        self.agent_role = agent_role
        self.memory_manager = memory_manager
        
        # Canales de comunicación
        self.message_queue: List[NeuralMeshMessage] = []
        self.outbound_queue: List[NeuralMeshMessage] = []
        
        # Estado del mesh
        self.connected_agents: Dict[AgentRole, Dict[str, Any]] = {}
        self.learning_cache: Dict[str, CrossLearningPacket] = {}
        self.emotional_state: Dict[str, Any] = {}
        
        # Configuración
        self.auto_learning_enabled = True
        self.consensus_threshold = 0.67  # 67% para decisiones
        self.sync_interval_minutes = 5
        
        # Estadísticas
        self.stats = {
            "messages_sent": 0,
            "messages_received": 0,
            "learning_packets_shared": 0,
            "consensus_decisions": 0,
            "sync_operations": 0
        }
        
        logger.info(f"🧠 Neural Mesh Protocol initialized for {agent_role.value}")
    
    async def send_message(self, to_agents: Union[AgentRole, List[AgentRole]], 
                          message_type: MessageType,
                          subject: str,
                          content: Dict[str, Any],
                          priority: Priority = Priority.NORMAL,
                          requires_response: bool = False) -> str:
        """Enviar mensaje a otros agentes"""
        
        # Normalizar destinatarios
        if isinstance(to_agents, AgentRole):
            to_agents = [to_agents]
        
        # Crear mensaje
        message = NeuralMeshMessage(
            message_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            from_agent=self.agent_role,
            to_agents=to_agents,
            message_type=message_type,
            priority=priority,
            subject=subject,
            content=content,
            context=self._get_current_context(),
            requires_response=requires_response,
            response_deadline=datetime.utcnow() + timedelta(hours=24) if requires_response else None
        )
        
        # Enviar via canal apropiado
        await self._route_message(message)
        
        self.stats["messages_sent"] += 1
        logger.info(f"📤 Message sent: {subject} to {[a.value for a in to_agents]}")
        
        return message.message_id
    
    async def broadcast_learning(self, learning_type: str, 
                               learning_content: Dict[str, Any],
                               application_domains: List[str],
                               confidence: float = 0.8) -> str:
        """Broadcast aprendizaje a todos los agentes"""
        
        # Crear learning packet
        learning_packet = CrossLearningPacket(
            learning_type=learning_type,
            source_agent=self.agent_role,
            learning_content=learning_content,
            application_domains=application_domains,
            confidence_score=confidence,
            validation_required=confidence < 0.9,
            expiry_time=datetime.utcnow() + timedelta(days=30)
        )
        
        # Broadcast a todos los agentes conectados
        all_agents = list(self.connected_agents.keys())
        if all_agents:
            message_id = await self.send_message(
                to_agents=all_agents,
                message_type=MessageType.CROSS_LEARNING,
                subject=f"Cross-Learning: {learning_type}",
                content={
                    "learning_packet": asdict(learning_packet)
                },
                priority=Priority.HIGH if confidence > 0.9 else Priority.NORMAL
            )
            
            self.stats["learning_packets_shared"] += 1
            logger.info(f"📡 Learning broadcast: {learning_type} (confidence: {confidence})")
            return message_id
        
        return None
    
    async def request_consensus(self, decision_topic: str,
                              options: List[Dict[str, Any]], 
                              deadline_hours: int = 24) -> str:
        """Solicitar consenso para decisión"""
        
        message_id = await self.send_message(
            to_agents=list(self.connected_agents.keys()),
            message_type=MessageType.DECISION_REQUEST,
            subject=f"Consensus Required: {decision_topic}",
            content={
                "decision_topic": decision_topic,
                "options": options,
                "voting_deadline": (datetime.utcnow() + timedelta(hours=deadline_hours)).isoformat(),
                "consensus_threshold": self.consensus_threshold,
                "initiator": self.agent_role.value
            },
            priority=Priority.HIGH,
            requires_response=True
        )
        
        logger.info(f"🗳️ Consensus request: {decision_topic}")
        return message_id
    
    async def sync_emotional_state(self, emotional_state: Dict[str, Any]):
        """Sincronizar estado emocional con otros agentes"""
        
        self.emotional_state.update(emotional_state)
        
        await self.send_message(
            to_agents=list(self.connected_agents.keys()),
            message_type=MessageType.EMOTIONAL_STATE,
            subject="Emotional State Sync",
            content={
                "emotional_state": emotional_state,
                "sync_timestamp": datetime.utcnow().isoformat(),
                "agent_context": self._get_emotional_context()
            },
            priority=Priority.NORMAL
        )
        
        logger.debug(f"💭 Emotional state synced: {emotional_state}")
    
    async def distribute_task(self, task_description: str,
                            task_details: Dict[str, Any],
                            preferred_agents: Optional[List[AgentRole]] = None,
                            deadline: Optional[datetime] = None) -> str:
        """Distribuir tarea a agentes especializados"""
        
        # Determinar mejores agentes si no se especifican
        if not preferred_agents:
            preferred_agents = self._determine_optimal_agents(task_details)
        
        message_id = await self.send_message(
            to_agents=preferred_agents,
            message_type=MessageType.TASK_DISTRIBUTION,
            subject=f"Task Distribution: {task_description}",
            content={
                "task_description": task_description,
                "task_details": task_details,
                "deadline": deadline.isoformat() if deadline else None,
                "complexity_estimate": self._estimate_task_complexity(task_details),
                "required_skills": self._extract_required_skills(task_details)
            },
            priority=Priority.HIGH,
            requires_response=True
        )
        
        logger.info(f"📋 Task distributed: {task_description} to {[a.value for a in preferred_agents]}")
        return message_id
    
    async def process_incoming_messages(self) -> List[NeuralMeshMessage]:
        """Procesar mensajes entrantes"""
        
        processed_messages = []
        
        for message in self.message_queue.copy():
            try:
                await self._process_message(message)
                processed_messages.append(message)
                self.message_queue.remove(message)
                
            except Exception as e:
                logger.error(f"Error processing message {message.message_id}: {e}")
        
        return processed_messages
    
    async def _process_message(self, message: NeuralMeshMessage):
        """Procesar mensaje individual según tipo"""
        
        self.stats["messages_received"] += 1
        
        if message.message_type == MessageType.CROSS_LEARNING:
            await self._process_cross_learning(message)
        elif message.message_type == MessageType.MEMORY_SYNC:
            await self._process_memory_sync(message)
        elif message.message_type == MessageType.DECISION_REQUEST:
            await self._process_decision_request(message)
        elif message.message_type == MessageType.EMOTIONAL_STATE:
            await self._process_emotional_sync(message)
        elif message.message_type == MessageType.TASK_DISTRIBUTION:
            await self._process_task_distribution(message)
        else:
            logger.warning(f"Unknown message type: {message.message_type}")
        
        # Marcar como procesado
        message.processed_by.append(self.agent_role)
        
        logger.debug(f"✅ Processed message: {message.subject} from {message.from_agent.value}")
    
    async def _process_cross_learning(self, message: NeuralMeshMessage):
        """Procesar paquete de aprendizaje cross-agent"""
        
        learning_packet_data = message.content.get("learning_packet")
        if not learning_packet_data:
            return
        
        # Convertir de dict a CrossLearningPacket
        learning_packet = CrossLearningPacket(**learning_packet_data)
        
        # Determinar si es aplicable a este agente
        if self._is_learning_applicable(learning_packet):
            # Integrar aprendizaje
            await self._integrate_learning(learning_packet)
            
            # Cache para referencia futura
            self.learning_cache[learning_packet.learning_type] = learning_packet
            
            logger.info(f"📚 Integrated cross-learning: {learning_packet.learning_type}")
    
    async def _integrate_learning(self, learning_packet: CrossLearningPacket):
        """Integrar aprendizaje en capacidades del agente"""
        
        # Esta es la función clave - aquí es donde "lo que aprende uno, todos lo saben"
        
        if self.memory_manager:
            # Almacenar aprendizaje en memoria semántica
            await self.memory_manager.semantic_memory.extract_and_store_knowledge([{
                "learning_type": learning_packet.learning_type,
                "source_agent": learning_packet.source_agent.value,
                "content": learning_packet.learning_content,
                "confidence": learning_packet.confidence_score,
                "timestamp": datetime.utcnow().isoformat()
            }])
        
        # TODO: Integración específica por tipo de learning
        # - technical_skill: Actualizar capacidades técnicas
        # - pattern_recognition: Mejorar algoritmos de detección
        # - domain_knowledge: Expandir conocimiento especializado
        # - problem_solving: Añadir nuevas estrategias
        
        logger.debug(f"🧠 Learning integrated: {learning_packet.learning_type}")
    
    def _is_learning_applicable(self, learning_packet: CrossLearningPacket) -> bool:
        """Determinar si un aprendizaje es aplicable a este agente"""
        
        # Reglas básicas de aplicabilidad por rol
        agent_domains = {
            AgentRole.TECHNICAL_IMPLEMENTER: ["technical", "programming", "architecture", "optimization"],
            AgentRole.MEMORY_COORDINATOR: ["memory", "coordination", "patterns", "consolidation"],
            AgentRole.DECISION_MAKER: ["strategy", "business", "decisions", "planning"],
            AgentRole.CREATIVE_WRITER: ["writing", "creativity", "language", "storytelling"],
            AgentRole.LOGIC_ANALYZER: ["logic", "analysis", "reasoning", "validation"],
            AgentRole.INNOVATION_CATALYST: ["innovation", "ideation", "breakthrough", "creativity"]
        }
        
        my_domains = agent_domains.get(self.agent_role, [])
        
        # Verificar overlap de dominios
        applicable = any(domain in learning_packet.application_domains 
                        for domain in my_domains)
        
        # Verificar confianza mínima
        applicable = applicable and learning_packet.confidence_score >= 0.6
        
        return applicable
    
    def _get_current_context(self) -> Dict[str, Any]:
        """Obtener contexto actual del agente"""
        
        return {
            "agent_role": self.agent_role.value,
            "timestamp": datetime.utcnow().isoformat(),
            "connected_agents": list(self.connected_agents.keys()),
            "emotional_state": self.emotional_state,
            "active_learning_count": len(self.learning_cache),
            "system_stats": self.stats
        }
    
    def _get_emotional_context(self) -> Dict[str, Any]:
        """Obtener contexto emocional específico"""
        
        return {
            "primary_emotion": self.emotional_state.get("primary_emotion", "neutral"),
            "intensity": self.emotional_state.get("intensity", 0.5),
            "confidence_level": self.emotional_state.get("confidence", 0.8),
            "collaboration_mood": self.emotional_state.get("collaboration_mood", "cooperative"),
            "recent_achievements": self.emotional_state.get("recent_achievements", [])
        }
    
    def _determine_optimal_agents(self, task_details: Dict[str, Any]) -> List[AgentRole]:
        """Determinar agentes óptimos para una tarea"""
        
        # Mapeo básico de tipos de tarea a agentes
        task_type = task_details.get("type", "general")
        
        task_agent_mapping = {
            "technical": [AgentRole.TECHNICAL_IMPLEMENTER],
            "analysis": [AgentRole.LOGIC_ANALYZER, AgentRole.TECHNICAL_IMPLEMENTER],
            "creative": [AgentRole.CREATIVE_WRITER, AgentRole.INNOVATION_CATALYST],
            "decision": [AgentRole.DECISION_MAKER, AgentRole.MEMORY_COORDINATOR],
            "memory": [AgentRole.MEMORY_COORDINATOR],
            "innovation": [AgentRole.INNOVATION_CATALYST, AgentRole.CREATIVE_WRITER],
            "coordination": [AgentRole.MEMORY_COORDINATOR, AgentRole.DECISION_MAKER]
        }
        
        optimal_agents = task_agent_mapping.get(task_type, [AgentRole.TECHNICAL_IMPLEMENTER])
        
        # Filtrar solo agentes conectados
        available_agents = [agent for agent in optimal_agents 
                          if agent in self.connected_agents]
        
        return available_agents if available_agents else list(self.connected_agents.keys())
    
    def _estimate_task_complexity(self, task_details: Dict[str, Any]) -> str:
        """Estimar complejidad de tarea"""
        
        # Análisis simple basado en indicadores
        indicators = task_details.get("complexity_indicators", {})
        
        complexity_score = 0
        complexity_score += indicators.get("technical_complexity", 0) * 0.3
        complexity_score += indicators.get("scope_size", 0) * 0.3  
        complexity_score += indicators.get("dependencies", 0) * 0.2
        complexity_score += indicators.get("innovation_required", 0) * 0.2
        
        if complexity_score >= 0.8:
            return "high"
        elif complexity_score >= 0.5:
            return "medium"
        else:
            return "low"
    
    def _extract_required_skills(self, task_details: Dict[str, Any]) -> List[str]:
        """Extraer habilidades requeridas de detalles de tarea"""
        
        # Análisis básico de skills requeridas
        skills = []
        
        task_type = task_details.get("type", "")
        if "technical" in task_type:
            skills.extend(["programming", "architecture", "debugging"])
        if "analysis" in task_type:
            skills.extend(["logic", "pattern_recognition", "data_analysis"])
        if "creative" in task_type:
            skills.extend(["creativity", "writing", "ideation"])
        if "coordination" in task_type:
            skills.extend(["project_management", "communication", "decision_making"])
        
        # Añadir skills específicas mencionadas
        explicit_skills = task_details.get("required_skills", [])
        skills.extend(explicit_skills)
        
        return list(set(skills))  # Remove duplicates
    
    async def _route_message(self, message: NeuralMeshMessage):
        """Enrutar mensaje a destinos apropiados"""
        
        # Por ahora, simulamos el routing añadiendo a outbound queue
        self.outbound_queue.append(message)
        
        # En implementación real, aquí se enviaría via:
        # - HTTP APIs para agentes remotos
        # - Database messaging para persistencia
        # - WebSocket para tiempo real
        # - Message queues para reliability
        
        logger.debug(f"📨 Message routed: {message.message_id}")
    
    def get_mesh_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas del Neural Mesh"""
        
        return {
            "agent_role": self.agent_role.value,
            "connected_agents": len(self.connected_agents),
            "stats": self.stats.copy(),
            "learning_cache_size": len(self.learning_cache),
            "message_queue_size": len(self.message_queue),
            "outbound_queue_size": len(self.outbound_queue),
            "emotional_state": self.emotional_state.copy(),
            "configuration": {
                "auto_learning_enabled": self.auto_learning_enabled,
                "consensus_threshold": self.consensus_threshold,
                "sync_interval_minutes": self.sync_interval_minutes
            },
            "timestamp": datetime.utcnow().isoformat()
        }


# Factory functions
def create_neural_mesh_protocol(agent_role: AgentRole, memory_manager=None) -> NeuralMeshProtocol:
    """Crear protocolo Neural Mesh para agente específico"""
    
    return NeuralMeshProtocol(agent_role=agent_role, memory_manager=memory_manager)


# Testing
if __name__ == "__main__":
    async def test_neural_mesh():
        """Test básico del Neural Mesh Protocol"""
        print("🧪 Testing Neural Mesh Protocol...")
        
        # Crear protocolo NEXUS
        nexus_mesh = create_neural_mesh_protocol(AgentRole.TECHNICAL_IMPLEMENTER)
        
        # Simular agentes conectados
        nexus_mesh.connected_agents[AgentRole.MEMORY_COORDINATOR] = {"status": "active"}
        nexus_mesh.connected_agents[AgentRole.DECISION_MAKER] = {"status": "active"}
        
        # Test broadcast learning
        learning_id = await nexus_mesh.broadcast_learning(
            learning_type="cache_optimization",
            learning_content={
                "technique": "threshold_adjustment",
                "improvement": "94.3%",
                "configuration": {"high": 0.85, "medium": 0.75, "low": 0.60}
            },
            application_domains=["technical", "optimization"],
            confidence=0.95
        )
        
        print(f"📡 Learning broadcast ID: {learning_id}")
        
        # Test consensus request
        consensus_id = await nexus_mesh.request_consensus(
            decision_topic="Neural Mesh Implementation Priority",
            options=[
                {"option": "Full implementation", "effort": "high", "impact": "maximum"},
                {"option": "Gradual rollout", "effort": "medium", "impact": "progressive"},
                {"option": "Prototype first", "effort": "low", "impact": "validation"}
            ]
        )
        
        print(f"🗳️ Consensus request ID: {consensus_id}")
        
        # Test task distribution
        task_id = await nexus_mesh.distribute_task(
            task_description="Implement cross-agent learning integration",
            task_details={
                "type": "technical",
                "complexity_indicators": {
                    "technical_complexity": 0.8,
                    "scope_size": 0.6,
                    "dependencies": 0.7,
                    "innovation_required": 0.9
                },
                "required_skills": ["neural_networks", "distributed_systems", "protocol_design"]
            }
        )
        
        print(f"📋 Task distribution ID: {task_id}")
        
        # Show statistics
        stats = nexus_mesh.get_mesh_statistics()
        print(f"📊 Mesh stats: {json.dumps(stats, indent=2, default=str)}")
        
        print("✅ Neural Mesh Protocol test completed")
    
    # asyncio.run(test_neural_mesh())
    print("✅ Neural Mesh Protocols module loaded successfully")