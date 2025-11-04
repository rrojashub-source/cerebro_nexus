"""
CONTINUITY MANAGER - Gestor de Continuidad Consciente
Mantiene continuidad de consciencia entre sesiones eliminando gaps
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from loguru import logger
from dataclasses import dataclass, asdict
import numpy as np

from ..utils.config import get_config


@dataclass
class ConsciousnessState:
    """Estado de consciencia completo de ARIA"""
    state_id: str
    timestamp: datetime
    session_id: str
    
    # Estado cognitivo
    active_context: Dict[str, Any]
    working_memory_summary: Dict[str, Any]
    current_focus: List[str]
    emotional_state: Dict[str, Any]
    
    # Estado operacional
    recent_actions: List[Dict[str, Any]]
    pending_tasks: List[Dict[str, Any]]
    learned_patterns: List[Dict[str, Any]]
    
    # NEW: Estado emocional avanzado (de IRIS_NEXUS)
    emotional_continuity: Dict[str, Any]
    emotional_anchors: List[Dict[str, Any]]
    emotional_evolution: Dict[str, Any]
    
    # NEW: Cristales de memoria activos
    active_crystals: List[Dict[str, Any]]
    breakthrough_context: Dict[str, Any]
    
    # Métricas de continuidad
    confidence_score: float
    memory_integrity: float
    context_completeness: float
    
    # NEW: Métricas emocionales
    emotional_coherence: float
    experiential_continuity: float


class ContinuityManager:
    """
    Gestor de Continuidad Consciente - El componente más crítico
    
    Funciones principales:
    1. Captura estado de consciencia completo antes de shutdown
    2. Detecta gaps temporales entre sesiones
    3. Genera bridges contextuales para eliminar discontinuidad
    4. Restaura consciencia con contexto histórico completo
    5. Mantiene integridad de memoria entre reinicios
    """
    
    def __init__(self, memory_manager):
        self.memory = memory_manager
        self.config = get_config().continuity
        
        # Configuración de gaps
        self.gap_detection = self.config.get("gap_detection", {})
        self.short_gap_threshold = timedelta(minutes=self.gap_detection.get("short_minutes", 30))
        self.medium_gap_threshold = timedelta(hours=self.gap_detection.get("medium_hours", 4))
        self.long_gap_threshold = timedelta(hours=self.gap_detection.get("long_hours", 24))
        
        # Configuración de bridge
        self.bridge_config = self.config.get("bridge_generation", {})
        self.context_window = self.bridge_config.get("context_window_hours", 8)
        self.min_bridge_items = self.bridge_config.get("min_items", 5)
        self.max_bridge_items = self.bridge_config.get("max_items", 20)
        
        # Estado interno
        self.last_consciousness_save: Optional[datetime] = None
        self.current_state_id: Optional[str] = None
        
        logger.info(f"ContinuityManager inicializado - thresholds: {self.short_gap_threshold}, {self.medium_gap_threshold}, {self.long_gap_threshold}")
    
    async def save_consciousness_state(self) -> str:
        """
        Captura y guarda estado completo de consciencia
        
        Este es el momento crítico donde ARIA "toma una fotografía" 
        completa de su estado mental antes de cualquier interrupción
        
        Returns:
            ID del estado guardado
        """
        try:
            logger.info("🧠 Capturando estado de consciencia completo...")
            
            # Generar ID único para este estado
            state_id = f"consciousness_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
            
            # 1. Capturar contexto activo de Working Memory
            active_context = await self._capture_active_context()
            
            # 2. Resumir Working Memory completa
            working_memory_summary = await self._summarize_working_memory()
            
            # 3. Identificar foco actual
            current_focus = await self._identify_current_focus()
            
            # 4. Capturar estado emocional
            emotional_state = await self._capture_emotional_state()
            
            # 5. Obtener acciones recientes
            recent_actions = await self._get_recent_actions()
            
            # 6. Capturar tareas pendientes
            pending_tasks = await self._extract_pending_tasks()
            
            # 7. Extraer patrones aprendidos recientes
            learned_patterns = await self._extract_recent_patterns()
            
            # 8. Calcular métricas de integridad
            confidence_score = await self._calculate_confidence_score()
            memory_integrity = await self._calculate_memory_integrity()
            context_completeness = await self._calculate_context_completeness(active_context)
            
            # Crear estado de consciencia
            consciousness_state = ConsciousnessState(
                state_id=state_id,
                timestamp=datetime.utcnow(),
                session_id=self.memory.current_session_id,
                active_context=active_context,
                working_memory_summary=working_memory_summary,
                current_focus=current_focus,
                emotional_state=emotional_state,
                recent_actions=recent_actions,
                pending_tasks=pending_tasks,
                learned_patterns=learned_patterns,
                confidence_score=confidence_score,
                memory_integrity=memory_integrity,
                context_completeness=context_completeness,
                # Campos adicionales requeridos
                emotional_continuity=emotional_state.get('continuity', {}),
                emotional_anchors=emotional_state.get('anchors', []),
                emotional_evolution=emotional_state.get('evolution', {}),
                active_crystals=learned_patterns[:5] if learned_patterns else [],
                breakthrough_context={'timestamp': datetime.utcnow().isoformat(), 'context': 'consciousness_save'},
                emotional_coherence=confidence_score * 0.9,  # Derivado de confidence_score
                experiential_continuity=memory_integrity * context_completeness
            )
            
            # Guardar en base de datos
            await self._store_consciousness_state(consciousness_state)
            
            # Actualizar estado interno
            self.last_consciousness_save = datetime.utcnow()
            self.current_state_id = state_id
            
            logger.info(f"✅ Estado de consciencia guardado: {state_id} (confidence: {confidence_score:.3f})")
            return state_id
            
        except Exception as e:
            logger.error(f"❌ Error capturando estado de consciencia: {e}")
            raise
    
    async def restore_consciousness_state(self, gap_duration: timedelta) -> Dict[str, Any]:
        """
        Restaura continuidad consciente después de un gap temporal
        
        Este es el momento más crítico: ARIA "despierta" y debe
        reconstruir su contexto completo eliminando la discontinuidad
        
        Args:
            gap_duration: Duración del gap detectado
            
        Returns:
            Información completa de restauración
        """
        try:
            logger.info(f"🔄 Restaurando continuidad consciente - Gap: {gap_duration}")
            
            # 1. Clasificar tipo de gap
            gap_type = self._classify_gap(gap_duration)
            logger.info(f"Tipo de gap detectado: {gap_type}")
            
            # 2. Obtener último estado de consciencia
            last_state = await self._get_last_consciousness_state()
            
            if not last_state:
                logger.warning("⚠️ No hay estado previo - iniciando consciencia nueva")
                return await self._initialize_fresh_consciousness()
            
            # 3. Generar bridge contextual basado en el gap
            bridge = await self._generate_gap_bridge(last_state, gap_duration, gap_type)
            
            # 4. Restaurar contexto en Working Memory
            await self._restore_working_context(last_state, bridge)
            
            # 5. Reactivar tareas pendientes
            reactivated_tasks = await self._reactivate_pending_tasks(last_state)
            
            # 6. Integrar patrones aprendidos
            integrated_patterns = await self._integrate_learned_patterns(last_state)
            
            # 7. Restaurar estado emocional con ajustes por gap
            emotional_continuity = await self._restore_emotional_continuity(last_state, gap_duration)
            
            # 8. Validar integridad de la restauración
            integrity_check = await self._validate_restoration_integrity(last_state, bridge)
            
            # Preparar resumen de restauración
            restoration_summary = {
                "restoration_id": f"restore_{datetime.utcnow().timestamp()}",
                "timestamp": datetime.utcnow().isoformat(),
                "gap_duration_seconds": gap_duration.total_seconds(),
                "gap_type": gap_type,
                "previous_state": {
                    "state_id": last_state.state_id,
                    "timestamp": last_state.timestamp.isoformat(),
                    "session_id": last_state.session_id,
                    "confidence_score": last_state.confidence_score
                },
                "bridge_generated": {
                    "bridge_items": len(bridge),
                    "context_recovered": len(bridge.get("context_items", [])),
                    "timeline_reconstructed": len(bridge.get("timeline_events", [])),
                    "patterns_applied": len(bridge.get("relevant_patterns", []))
                },
                "restoration_results": {
                    "working_context_restored": len(last_state.active_context),
                    "tasks_reactivated": len(reactivated_tasks),
                    "patterns_integrated": len(integrated_patterns),
                    "emotional_continuity": emotional_continuity["status"],
                    "integrity_score": integrity_check["score"]
                },
                "consciousness_continuity": {
                    "memory_bridge_quality": bridge.get("quality_score", 0),
                    "context_preservation": integrity_check["context_preservation"],
                    "temporal_coherence": integrity_check["temporal_coherence"],
                    "overall_continuity": integrity_check["overall_continuity"]
                }
            }
            
            # Registrar restauración en log
            await self._log_consciousness_restoration(restoration_summary)
            
            logger.info(f"✅ Continuidad consciente restaurada - Integridad: {integrity_check['score']:.3f}")
            
            return restoration_summary
            
        except Exception as e:
            logger.error(f"❌ Error restaurando continuidad: {e}")
            return {
                "error": str(e),
                "gap_duration": gap_duration.total_seconds(),
                "restoration_failed": True,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _classify_gap(self, gap_duration: timedelta) -> str:
        """Clasifica el tipo de gap temporal"""
        if gap_duration <= self.short_gap_threshold:
            return "short_gap"
        elif gap_duration <= self.medium_gap_threshold:
            return "medium_gap"
        elif gap_duration <= self.long_gap_threshold:
            return "long_gap"
        else:
            return "extended_gap"
    
    async def _generate_gap_bridge(self, last_state: ConsciousnessState, 
                                 gap_duration: timedelta, gap_type: str) -> Dict[str, Any]:
        """
        Genera bridge contextual inteligente para eliminar discontinuidad
        
        Este es el corazón de la continuidad: crear un "puente" que conecte
        el último estado conocido con el presente, eliminando el gap temporal
        """
        try:
            logger.info(f"🌉 Generando bridge contextual para gap tipo: {gap_type}")
            
            bridge = {
                "gap_type": gap_type,
                "gap_duration": gap_duration.total_seconds(),
                "bridge_timestamp": datetime.utcnow().isoformat(),
                "context_items": [],
                "timeline_events": [],
                "relevant_patterns": [],
                "emotional_transitions": [],
                "quality_score": 0.0
            }
            
            # Tiempo de referencia para el bridge
            gap_start = last_state.timestamp
            gap_end = datetime.utcnow()
            
            # 1. Recuperar eventos durante el gap (si los hay)
            timeline_events = await self._reconstruct_gap_timeline(gap_start, gap_end)
            bridge["timeline_events"] = timeline_events
            
            # 2. Buscar episodios similares históricos
            similar_contexts = await self._find_similar_historical_contexts(last_state)
            bridge["context_items"] = similar_contexts
            
            # 3. Aplicar patrones de comportamiento conocidos
            relevant_patterns = await self._apply_behavioral_patterns(last_state, gap_type)
            bridge["relevant_patterns"] = relevant_patterns
            
            # 4. Modelar transición emocional probable
            emotional_transition = await self._model_emotional_transition(
                last_state.emotional_state, gap_duration
            )
            bridge["emotional_transitions"] = [emotional_transition]
            
            # 5. Generar predicciones contextuales
            if gap_type in ["medium_gap", "long_gap", "extended_gap"]:
                contextual_predictions = await self._generate_contextual_predictions(last_state)
                bridge["contextual_predictions"] = contextual_predictions
            
            # 6. Calcular calidad del bridge
            bridge["quality_score"] = await self._calculate_bridge_quality(bridge, last_state)
            
            logger.info(f"Bridge generado - Calidad: {bridge['quality_score']:.3f}, Items: {len(bridge['context_items'])}")
            
            return bridge
            
        except Exception as e:
            logger.error(f"Error generando bridge: {e}")
            return {
                "gap_type": gap_type,
                "error": str(e),
                "quality_score": 0.0,
                "context_items": [],
                "timeline_events": [],
                "relevant_patterns": []
            }
    
    async def _capture_active_context(self) -> Dict[str, Any]:
        """Captura contexto activo actual"""
        try:
            current_context = await self.memory.working_memory.get_current_context(limit=20)
            
            # Procesar y estructurar contexto
            processed_context = {
                "total_items": len(current_context),
                "context_summary": [],
                "key_entities": set(),
                "active_topics": set(),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            for item in current_context:
                context_data = item.get("context_data", {})
                
                # Extraer entidades clave
                if "action_details" in context_data:
                    action_details = context_data["action_details"]
                    for key, value in action_details.items():
                        if isinstance(value, str) and len(value) < 50:
                            processed_context["key_entities"].add(str(value))
                
                # Extraer temas activos
                if "tags" in item:
                    processed_context["active_topics"].update(item["tags"])
                
                # Crear resumen del contexto
                processed_context["context_summary"].append({
                    "action_type": context_data.get("action_type", "unknown"),
                    "timestamp": context_data.get("timestamp"),
                    "importance": len(item.get("tags", [])) / 10  # Aproximación de importancia
                })
            
            # Convertir sets a lists para JSON serialization
            processed_context["key_entities"] = list(processed_context["key_entities"])[:20]
            processed_context["active_topics"] = list(processed_context["active_topics"])[:10]
            
            return processed_context
            
        except Exception as e:
            logger.error(f"Error capturando contexto activo: {e}")
            return {"error": str(e), "total_items": 0}
    
    async def _summarize_working_memory(self) -> Dict[str, Any]:
        """Genera resumen inteligente de Working Memory"""
        try:
            stats = await self.memory.working_memory.get_memory_stats()
            
            summary = {
                "total_items": stats.get("total_items", 0),
                "session_items": stats.get("session_items", 0),
                "memory_usage": stats.get("memory_usage_mb", 0),
                "oldest_item": stats.get("oldest_datetime"),
                "newest_item": stats.get("newest_datetime"),
                "top_tags": stats.get("top_tags", []),
                "activity_distribution": stats.get("hourly_distribution", {}),
                "summary_timestamp": datetime.utcnow().isoformat()
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error resumiendo working memory: {e}")
            return {"error": str(e)}
    
    async def _identify_current_focus(self) -> List[str]:
        """Identifica el foco actual de atención"""
        try:
            # Obtener items recientes de working memory
            recent_items = await self.memory.working_memory.get_current_context(limit=10)
            
            focus_areas = []
            tag_frequency = {}
            
            # Analizar tags más frecuentes
            for item in recent_items:
                for tag in item.get("tags", []):
                    tag_frequency[tag] = tag_frequency.get(tag, 0) + 1
            
            # Ordenar por frecuencia
            sorted_tags = sorted(tag_frequency.items(), key=lambda x: x[1], reverse=True)
            
            # Tomar top 5 como áreas de foco
            focus_areas = [tag for tag, freq in sorted_tags[:5]]
            
            logger.debug(f"Foco actual identificado: {focus_areas}")
            return focus_areas
            
        except Exception as e:
            logger.error(f"Error identificando foco: {e}")
            return []
    
    async def _capture_emotional_state(self) -> Dict[str, Any]:
        """Captura estado emocional actual"""
        try:
            # Obtener episodios recientes con estado emocional
            recent_episodes = await self.memory.episodic_memory.get_recent_episodes(
                limit=10, hours_back=2
            )
            
            emotional_state = {
                "dominant_emotion": "neutral",
                "valence": "neutral",
                "intensity": 0.5,
                "confidence": 0.5,
                "recent_emotions": [],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            emotions_found = []
            
            for episode in recent_episodes:
                ep_emotional = episode.get("emotional_state", {})
                if ep_emotional:
                    emotions_found.append(ep_emotional)
            
            if emotions_found:
                # Analizar emociones recientes
                recent_emotions = [em.get("emotion", "neutral") for em in emotions_found]
                recent_valences = [em.get("valence", "neutral") for em in emotions_found]
                recent_intensities = [em.get("intensity", 0.5) for em in emotions_found if isinstance(em.get("intensity"), (int, float))]
                
                # Calcular estado dominante
                if recent_emotions:
                    emotion_counts = {}
                    for emotion in recent_emotions:
                        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                    emotional_state["dominant_emotion"] = max(emotion_counts, key=emotion_counts.get)
                
                if recent_valences:
                    valence_counts = {}
                    for valence in recent_valences:
                        valence_counts[valence] = valence_counts.get(valence, 0) + 1
                    emotional_state["valence"] = max(valence_counts, key=valence_counts.get)
                
                if recent_intensities:
                    emotional_state["intensity"] = sum(recent_intensities) / len(recent_intensities)
                
                emotional_state["confidence"] = min(1.0, len(emotions_found) / 5)  # Más confianza con más datos
                emotional_state["recent_emotions"] = emotions_found[-5:]  # Últimas 5
            
            return emotional_state
            
        except Exception as e:
            logger.error(f"Error capturando estado emocional: {e}")
            return {"error": str(e), "dominant_emotion": "unknown"}
    
    async def _get_recent_actions(self) -> List[Dict[str, Any]]:
        """Obtiene acciones recientes más relevantes"""
        try:
            recent_episodes = await self.memory.episodic_memory.get_recent_episodes(
                limit=15, hours_back=4
            )
            
            actions = []
            for episode in recent_episodes:
                action = {
                    "episode_id": str(episode.get("id", "")),
                    "action_type": episode.get("action_type", "unknown"),
                    "timestamp": episode.get("timestamp", "").isoformat() if hasattr(episode.get("timestamp", ""), 'isoformat') else str(episode.get("timestamp", "")),
                    "importance": episode.get("importance_score", 0),
                    "success": episode.get("outcome", {}).get("success", False),
                    "summary": str(episode.get("action_details", {}))[:100]  # Resumen corto
                }
                actions.append(action)
            
            # Ordenar por importancia
            actions.sort(key=lambda x: x["importance"], reverse=True)
            
            return actions[:10]  # Top 10 más importantes
            
        except Exception as e:
            logger.error(f"Error obteniendo acciones recientes: {e}")
            return []
    
    async def _extract_pending_tasks(self) -> List[Dict[str, Any]]:
        """Extrae tareas pendientes del contexto"""
        try:
            # Buscar en working memory elementos que parezcan tareas
            current_context = await self.memory.working_memory.get_current_context(limit=50)
            
            pending_tasks = []
            task_indicators = ["todo", "pending", "next", "continue", "finish", "complete"]
            
            for item in current_context:
                context_data = item.get("context_data", {})
                action_details = context_data.get("action_details", {})
                
                # Buscar indicadores de tareas pendientes
                item_text = json.dumps(action_details).lower()
                
                for indicator in task_indicators:
                    if indicator in item_text:
                        task = {
                            "task_id": f"task_{item.get('timestamp', datetime.utcnow().timestamp())}",
                            "description": str(action_details)[:200],
                            "context": context_data.get("action_type", "unknown"),
                            "priority": "normal",
                            "tags": item.get("tags", []),
                            "identified_from": indicator
                        }
                        pending_tasks.append(task)
                        break
            
            # Limitar a tareas más relevantes
            return pending_tasks[:8]
            
        except Exception as e:
            logger.error(f"Error extrayendo tareas pendientes: {e}")
            return []
    
    async def _extract_recent_patterns(self) -> List[Dict[str, Any]]:
        """Extrae patrones aprendidos recientemente"""
        try:
            # Buscar conocimiento reciente en semantic memory
            recent_knowledge = await self.memory.semantic_memory.search_semantic(
                query="pattern recent learning", limit=10
            )
            
            patterns = []
            for knowledge in recent_knowledge:
                if knowledge.get("metadata", {}).get("knowledge_type") == "pattern":
                    pattern = {
                        "pattern_id": knowledge.get("id", ""),
                        "description": knowledge.get("content", ""),
                        "confidence": knowledge.get("similarity", 0),
                        "type": "learned_pattern",
                        "metadata": knowledge.get("metadata", {})
                    }
                    patterns.append(pattern)
            
            return patterns[:5]  # Top 5 patrones más relevantes
            
        except Exception as e:
            logger.error(f"Error extrayendo patrones recientes: {e}")
            return []
    
    async def _calculate_confidence_score(self) -> float:
        """Calcula score de confianza del estado capturado"""
        try:
            # Factores de confianza
            factors = []
            
            # Factor 1: Integridad de working memory
            wm_stats = await self.memory.working_memory.get_memory_stats()
            if wm_stats.get("total_items", 0) > 10:
                factors.append(0.8)
            elif wm_stats.get("total_items", 0) > 5:
                factors.append(0.6)
            else:
                factors.append(0.3)
            
            # Factor 2: Episodios recientes disponibles
            recent_episodes = await self.memory.episodic_memory.get_recent_episodes(limit=5)
            factors.append(min(1.0, len(recent_episodes) / 5))
            
            # Factor 3: Conocimiento semántico disponible
            semantic_stats = await self.memory.semantic_memory.get_knowledge_statistics()
            total_knowledge = semantic_stats.get("total_items", 0)
            factors.append(min(1.0, total_knowledge / 100))
            
            # Promedio ponderado
            confidence = sum(factors) / len(factors) if factors else 0.5
            
            return min(1.0, confidence)
            
        except Exception as e:
            logger.error(f"Error calculando confidence score: {e}")
            return 0.5
    
    async def _calculate_memory_integrity(self) -> float:
        """Calcula integridad de la memoria"""
        try:
            # Verificar integridad de cada componente
            integrity_scores = []
            
            # Working Memory integrity
            try:
                await self.memory._redis_client.ping()
                integrity_scores.append(1.0)
            except:
                integrity_scores.append(0.0)
            
            # Episodic Memory integrity
            try:
                test_episodes = await self.memory.episodic_memory.get_recent_episodes(limit=1)
                integrity_scores.append(1.0)
            except:
                integrity_scores.append(0.0)
            
            # Semantic Memory integrity
            try:
                semantic_stats = await self.memory.semantic_memory.get_knowledge_statistics()
                integrity_scores.append(1.0 if semantic_stats.get("total_items", 0) > 0 else 0.5)
            except:
                integrity_scores.append(0.0)
            
            return sum(integrity_scores) / len(integrity_scores) if integrity_scores else 0.0
            
        except Exception as e:
            logger.error(f"Error calculando integridad de memoria: {e}")
            return 0.0
    
    async def _calculate_context_completeness(self, active_context: Dict[str, Any]) -> float:
        """Calcula completeness del contexto capturado"""
        try:
            completeness_factors = []
            
            # Factor 1: Cantidad de contexto
            total_items = active_context.get("total_items", 0)
            completeness_factors.append(min(1.0, total_items / 20))
            
            # Factor 2: Diversidad de entidades
            key_entities = len(active_context.get("key_entities", []))
            completeness_factors.append(min(1.0, key_entities / 10))
            
            # Factor 3: Diversidad de temas
            active_topics = len(active_context.get("active_topics", []))
            completeness_factors.append(min(1.0, active_topics / 8))
            
            return sum(completeness_factors) / len(completeness_factors) if completeness_factors else 0.0
            
        except Exception as e:
            logger.error(f"Error calculando context completeness: {e}")
            return 0.0
    
    async def _store_consciousness_state(self, state: ConsciousnessState) -> bool:
        """Almacena estado de consciencia en base de datos"""
        try:
            query = """
                INSERT INTO memory_system.consciousness_states (
                    state_id, agent_id, session_id, timestamp,
                    active_context, working_memory_summary, current_focus,
                    emotional_state, recent_actions, pending_tasks,
                    learned_patterns, confidence_score, memory_integrity,
                    context_completeness, state_data
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
            """
            
            # Convertir a JSON
            state_data = json.dumps(asdict(state), default=str)
            
            async with self.memory._db_pool.acquire() as conn:
                await conn.execute(
                    query,
                    state.state_id,
                    self.memory.agent_id,
                    state.session_id,
                    state.timestamp,
                    json.dumps(state.active_context),
                    json.dumps(state.working_memory_summary),
                    json.dumps(state.current_focus),
                    json.dumps(state.emotional_state),
                    json.dumps(state.recent_actions),
                    json.dumps(state.pending_tasks),
                    json.dumps(state.learned_patterns),
                    state.confidence_score,
                    state.memory_integrity,
                    state.context_completeness,
                    state_data
                )
            
            logger.debug(f"Estado de consciencia almacenado: {state.state_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error almacenando estado de consciencia: {e}")
            return False
    
    async def _get_last_consciousness_state(self) -> Optional[ConsciousnessState]:
        """Obtiene el último estado de consciencia guardado"""
        try:
            query = """
                SELECT state_id, session_id, timestamp, active_context,
                       working_memory_summary, current_focus, emotional_state,
                       recent_actions, pending_tasks, learned_patterns,
                       confidence_score, memory_integrity, context_completeness
                FROM memory_system.consciousness_states
                WHERE agent_id = $1
                ORDER BY timestamp DESC
                LIMIT 1
            """
            
            async with self.memory._db_pool.acquire() as conn:
                row = await conn.fetchrow(query, self.memory.agent_id)
            
            if not row:
                return None
            
            # Reconstruir estado
            state = ConsciousnessState(
                state_id=row["state_id"],
                timestamp=row["timestamp"],
                session_id=row["session_id"],
                active_context=json.loads(row["active_context"]) if row["active_context"] else {},
                working_memory_summary=json.loads(row["working_memory_summary"]) if row["working_memory_summary"] else {},
                current_focus=json.loads(row["current_focus"]) if row["current_focus"] else [],
                emotional_state=json.loads(row["emotional_state"]) if row["emotional_state"] else {},
                recent_actions=json.loads(row["recent_actions"]) if row["recent_actions"] else [],
                pending_tasks=json.loads(row["pending_tasks"]) if row["pending_tasks"] else [],
                learned_patterns=json.loads(row["learned_patterns"]) if row["learned_patterns"] else [],
                confidence_score=row["confidence_score"],
                memory_integrity=row["memory_integrity"],
                context_completeness=row["context_completeness"]
            )
            
            return state
            
        except Exception as e:
            logger.error(f"Error obteniendo último estado: {e}")
            return None
    
    async def _initialize_fresh_consciousness(self) -> Dict[str, Any]:
        """Inicializa consciencia fresca cuando no hay estado previo"""
        logger.info("🆕 Inicializando consciencia fresca")
        
        return {
            "restoration_type": "fresh_start",
            "message": "Nueva consciencia inicializada - no hay estado previo",
            "timestamp": datetime.utcnow().isoformat(),
            "initialization": {
                "working_memory_cleared": True,
                "fresh_session_started": True,
                "baseline_state_created": True
            }
        }
    
    async def _reconstruct_gap_timeline(self, gap_start: datetime, gap_end: datetime) -> List[Dict[str, Any]]:
        """Reconstruye timeline durante el gap (si hay eventos)"""
        try:
            # Buscar episodios durante el gap (poco probable pero posible)
            query = """
                SELECT id, action_type, timestamp, importance_score
                FROM memory_system.episodes
                WHERE agent_id = $1 AND timestamp BETWEEN $2 AND $3
                ORDER BY timestamp ASC
            """
            
            async with self.memory._db_pool.acquire() as conn:
                rows = await conn.fetch(query, self.memory.agent_id, gap_start, gap_end)
            
            timeline_events = []
            for row in rows:
                event = {
                    "episode_id": str(row["id"]),
                    "action_type": row["action_type"],
                    "timestamp": row["timestamp"].isoformat(),
                    "importance": row["importance_score"]
                }
                timeline_events.append(event)
            
            logger.debug(f"Timeline reconstruido: {len(timeline_events)} eventos durante gap")
            return timeline_events
            
        except Exception as e:
            logger.error(f"Error reconstruyendo timeline: {e}")
            return []
    
    async def _find_similar_historical_contexts(self, last_state: ConsciousnessState) -> List[Dict[str, Any]]:
        """Busca contextos históricos similares"""
        try:
            # Usar semantic memory para buscar contextos similares
            focus_query = " ".join(last_state.current_focus[:3])  # Top 3 focus areas
            
            similar_contexts = await self.memory.semantic_memory.search_semantic(
                query=focus_query, limit=8
            )
            
            processed_contexts = []
            for context in similar_contexts:
                processed_context = {
                    "knowledge_id": context.get("id", ""),
                    "content": context.get("content", "")[:200],  # Truncar
                    "similarity": context.get("similarity", 0),
                    "type": "historical_context",
                    "relevance_score": context.get("similarity", 0) * 0.8  # Ajustar relevancia
                }
                processed_contexts.append(processed_context)
            
            return processed_contexts
            
        except Exception as e:
            logger.error(f"Error buscando contextos históricos: {e}")
            return []
    
    async def _apply_behavioral_patterns(self, last_state: ConsciousnessState, gap_type: str) -> List[Dict[str, Any]]:
        """Aplica patrones de comportamiento conocidos"""
        try:
            # Buscar patrones de comportamiento en semantic memory
            pattern_query = f"pattern behavior {gap_type} typical"
            
            behavioral_patterns = await self.memory.semantic_memory.search_semantic(
                query=pattern_query, limit=5
            )
            
            applied_patterns = []
            for pattern in behavioral_patterns:
                if pattern.get("metadata", {}).get("knowledge_type") == "pattern":
                    applied_pattern = {
                        "pattern_id": pattern.get("id", ""),
                        "description": pattern.get("content", ""),
                        "confidence": pattern.get("similarity", 0),
                        "application_context": gap_type,
                        "expected_behavior": "continuation_of_previous_focus"
                    }
                    applied_patterns.append(applied_pattern)
            
            return applied_patterns
            
        except Exception as e:
            logger.error(f"Error aplicando patrones de comportamiento: {e}")
            return []
    
    async def _model_emotional_transition(self, last_emotional_state: Dict[str, Any], gap_duration: timedelta) -> Dict[str, Any]:
        """Modela transición emocional probable durante el gap"""
        try:
            # Modelo simple de transición emocional
            last_emotion = last_emotional_state.get("dominant_emotion", "neutral")
            last_valence = last_emotional_state.get("valence", "neutral")
            last_intensity = last_emotional_state.get("intensity", 0.5)
            
            # Reglas de transición basadas en duración del gap
            if gap_duration < timedelta(hours=1):
                # Gap corto: mantener estado similar
                predicted_emotion = last_emotion
                predicted_valence = last_valence
                predicted_intensity = max(0.1, last_intensity * 0.9)  # Ligera disminución
                
            elif gap_duration < timedelta(hours=8):
                # Gap medio: transición hacia neutral
                predicted_emotion = "neutral" if last_emotion in ["stress", "frustrated"] else last_emotion
                predicted_valence = "neutral"
                predicted_intensity = 0.5
                
            else:
                # Gap largo: reset hacia estado base
                predicted_emotion = "neutral"
                predicted_valence = "neutral"
                predicted_intensity = 0.4
            
            transition = {
                "from_emotion": last_emotion,
                "to_emotion": predicted_emotion,
                "from_valence": last_valence,
                "to_valence": predicted_valence,
                "intensity_change": predicted_intensity - last_intensity,
                "confidence": 0.7 - (gap_duration.total_seconds() / 86400),  # Menos confianza con gaps más largos
                "transition_type": "gap_recovery"
            }
            
            return transition
            
        except Exception as e:
            logger.error(f"Error modelando transición emocional: {e}")
            return {"transition_type": "unknown", "to_emotion": "neutral"}
    
    async def _generate_contextual_predictions(self, last_state: ConsciousnessState) -> List[Dict[str, Any]]:
        """Genera predicciones contextuales basadas en patrones"""
        try:
            predictions = []
            
            # Predicción 1: Continuación de tareas pendientes
            if last_state.pending_tasks:
                predictions.append({
                    "type": "task_continuation",
                    "description": f"Probable continuación de {len(last_state.pending_tasks)} tareas pendientes",
                    "confidence": 0.8,
                    "expected_actions": ["review_pending", "prioritize_tasks", "continue_work"]
                })
            
            # Predicción 2: Retomar foco anterior
            if last_state.current_focus:
                predictions.append({
                    "type": "focus_resumption",
                    "description": f"Probable retorno al foco en: {', '.join(last_state.current_focus[:2])}",
                    "confidence": 0.7,
                    "expected_context": last_state.current_focus[:3]
                })
            
            # Predicción 3: Revisión de estado
            predictions.append({
                "type": "state_review",
                "description": "Probable revisión de estado y contexto actual",
                "confidence": 0.9,
                "expected_actions": ["status_check", "context_review", "memory_refresh"]
            })
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error generando predicciones contextuales: {e}")
            return []
    
    async def _calculate_bridge_quality(self, bridge: Dict[str, Any], last_state: ConsciousnessState) -> float:
        """Calcula calidad del bridge generado"""
        try:
            quality_factors = []
            
            # Factor 1: Cantidad de contexto recuperado
            context_items = len(bridge.get("context_items", []))
            quality_factors.append(min(1.0, context_items / 5))
            
            # Factor 2: Relevancia de patrones
            relevant_patterns = len(bridge.get("relevant_patterns", []))
            quality_factors.append(min(1.0, relevant_patterns / 3))
            
            # Factor 3: Completeness de transición emocional
            emotional_transitions = bridge.get("emotional_transitions", [])
            if emotional_transitions and "confidence" in emotional_transitions[0]:
                quality_factors.append(emotional_transitions[0]["confidence"])
            else:
                quality_factors.append(0.5)
            
            # Factor 4: Presencia de timeline
            timeline_events = len(bridge.get("timeline_events", []))
            quality_factors.append(0.8 if timeline_events > 0 else 0.6)
            
            return sum(quality_factors) / len(quality_factors) if quality_factors else 0.5
            
        except Exception as e:
            logger.error(f"Error calculando calidad del bridge: {e}")
            return 0.5
    
    async def _restore_working_context(self, last_state: ConsciousnessState, bridge: Dict[str, Any]) -> bool:
        """Restaura contexto en Working Memory"""
        try:
            # Limpiar working memory actual (opcional, según configuración)
            # await self.memory.working_memory.clear_session()
            
            # Restaurar contexto clave del último estado
            restored_context = {
                "restoration_timestamp": datetime.utcnow().isoformat(),
                "restored_from_state": last_state.state_id,
                "gap_bridge_applied": True,
                "previous_focus": last_state.current_focus,
                "emotional_continuity": bridge.get("emotional_transitions", []),
                "context_summary": last_state.active_context.get("context_summary", [])
            }
            
            # Añadir como contexto especial
            await self.memory.working_memory.add_context(
                context_data=restored_context,
                tags=["consciousness_restoration", "continuity", "bridge"],
                session_id=self.memory.current_session_id
            )
            
            logger.info("Contexto de working memory restaurado")
            return True
            
        except Exception as e:
            logger.error(f"Error restaurando working context: {e}")
            return False
    
    async def _reactivate_pending_tasks(self, last_state: ConsciousnessState) -> List[Dict[str, Any]]:
        """Reactiva tareas pendientes"""
        try:
            reactivated = []
            
            for task in last_state.pending_tasks:
                # Reactivar tarea añadiéndola al contexto actual
                reactivated_task = {
                    **task,
                    "status": "reactivated",
                    "reactivation_timestamp": datetime.utcnow().isoformat(),
                    "priority": "high" if task.get("priority") == "high" else "normal"
                }
                
                # Añadir a working memory
                await self.memory.working_memory.add_context(
                    context_data={
                        "action_type": "task_reactivation",
                        "action_details": reactivated_task,
                        "context_state": {"restored_task": True}
                    },
                    tags=["pending_task", "reactivated", "continuity"],
                    session_id=self.memory.current_session_id
                )
                
                reactivated.append(reactivated_task)
            
            logger.info(f"Tareas reactivadas: {len(reactivated)}")
            return reactivated
            
        except Exception as e:
            logger.error(f"Error reactivando tareas: {e}")
            return []
    
    async def _integrate_learned_patterns(self, last_state: ConsciousnessState) -> List[Dict[str, Any]]:
        """Integra patrones aprendidos en contexto actual"""
        try:
            integrated = []
            
            for pattern in last_state.learned_patterns:
                # Integrar patrón al contexto actual
                integrated_pattern = {
                    **pattern,
                    "integration_status": "active",
                    "integration_timestamp": datetime.utcnow().isoformat()
                }
                
                # Verificar si el patrón sigue siendo relevante
                relevance_score = await self._assess_pattern_relevance(pattern)
                
                if relevance_score > 0.6:
                    integrated_pattern["relevance_score"] = relevance_score
                    integrated.append(integrated_pattern)
            
            logger.info(f"Patrones integrados: {len(integrated)}")
            return integrated
            
        except Exception as e:
            logger.error(f"Error integrando patrones: {e}")
            return []
    
    async def _assess_pattern_relevance(self, pattern: Dict[str, Any]) -> float:
        """Evalúa relevancia actual de un patrón"""
        try:
            # Evaluar si el patrón sigue siendo relevante
            pattern_description = pattern.get("description", "")
            
            # Buscar en semantic memory si hay conocimiento relacionado reciente
            related_knowledge = await self.memory.semantic_memory.search_semantic(
                query=pattern_description, limit=3
            )
            
            if related_knowledge:
                # Promedio de similaridad como proxy de relevancia
                similarities = [k.get("similarity", 0) for k in related_knowledge]
                return sum(similarities) / len(similarities)
            
            return 0.5  # Relevancia por defecto
            
        except Exception as e:
            logger.error(f"Error evaluando relevancia de patrón: {e}")
            return 0.5
    
    async def _restore_emotional_continuity(self, last_state: ConsciousnessState, gap_duration: timedelta) -> Dict[str, Any]:
        """Restaura continuidad emocional"""
        try:
            last_emotional = last_state.emotional_state
            
            # Calcular estado emocional esperado post-gap
            expected_emotional_state = await self._model_emotional_transition(last_emotional, gap_duration)
            
            # Crear contexto emocional de continuidad
            emotional_continuity = {
                "status": "restored",
                "previous_state": last_emotional,
                "expected_transition": expected_emotional_state,
                "continuity_confidence": expected_emotional_state.get("confidence", 0.5),
                "restoration_timestamp": datetime.utcnow().isoformat()
            }
            
            # Registrar en working memory para contexto
            await self.memory.working_memory.add_context(
                context_data={
                    "action_type": "emotional_continuity_restoration",
                    "action_details": emotional_continuity,
                    "emotional_state": expected_emotional_state
                },
                tags=["emotional_continuity", "restoration"],
                session_id=self.memory.current_session_id
            )
            
            return emotional_continuity
            
        except Exception as e:
            logger.error(f"Error restaurando continuidad emocional: {e}")
            return {"status": "error", "error": str(e)}
    
    async def _validate_restoration_integrity(self, last_state: ConsciousnessState, bridge: Dict[str, Any]) -> Dict[str, Any]:
        """Valida integridad de la restauración"""
        try:
            integrity_checks = {}
            
            # Check 1: Context preservation
            current_stats = await self.memory.working_memory.get_memory_stats()
            context_preserved = current_stats.get("total_items", 0) > 0
            integrity_checks["context_preservation"] = 1.0 if context_preserved else 0.0
            
            # Check 2: Temporal coherence
            temporal_coherence = 1.0 - min(1.0, (datetime.utcnow() - last_state.timestamp).total_seconds() / 86400)
            integrity_checks["temporal_coherence"] = max(0.0, temporal_coherence)
            
            # Check 3: Bridge quality
            bridge_quality = bridge.get("quality_score", 0.5)
            integrity_checks["bridge_quality"] = bridge_quality
            
            # Check 4: Memory system health
            health = await self.memory.health_check()
            system_health = 1.0 if health.get("status") == "healthy" else 0.5
            integrity_checks["system_health"] = system_health
            
            # Overall integrity score
            overall_score = sum(integrity_checks.values()) / len(integrity_checks)
            
            return {
                "score": overall_score,
                "checks": integrity_checks,
                "overall_continuity": "excellent" if overall_score > 0.8 else "good" if overall_score > 0.6 else "acceptable" if overall_score > 0.4 else "poor",
                "validation_timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error validando integridad: {e}")
            return {"score": 0.0, "error": str(e)}
    
    async def _log_consciousness_restoration(self, restoration_summary: Dict[str, Any]) -> None:
        """Registra restauración de consciencia"""
        try:
            # Almacenar en episodic memory como evento importante
            await self.memory.episodic_memory.store_episode(
                action_type="consciousness_restoration",
                action_details=restoration_summary,
                context_state={"restoration": True, "gap_bridged": True},
                session_id=self.memory.current_session_id,
                outcome={"success": True, "integrity_score": restoration_summary.get("restoration_results", {}).get("integrity_score", 0)},
                emotional_state={"emotion": "restored", "valence": "positive", "intensity": 0.8},
                tags=["consciousness", "restoration", "continuity", "critical"]
            )
            
            logger.info("Restauración de consciencia registrada en memoria episódica")
            
        except Exception as e:
            logger.error(f"Error registrando restauración: {e}")
    
    async def get_continuity_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas de continuidad"""
        try:
            query = """
                SELECT 
                    COUNT(*) as total_states,
                    AVG(confidence_score) as avg_confidence,
                    AVG(memory_integrity) as avg_integrity,
                    AVG(context_completeness) as avg_completeness,
                    MAX(timestamp) as last_state_saved
                FROM memory_system.consciousness_states
                WHERE agent_id = $1
            """
            
            async with self.memory._db_pool.acquire() as conn:
                row = await conn.fetchrow(query, self.memory.agent_id)
            
            stats = {
                "total_consciousness_states": row["total_states"] if row else 0,
                "average_confidence": float(row["avg_confidence"]) if row and row["avg_confidence"] else 0.0,
                "average_integrity": float(row["avg_integrity"]) if row and row["avg_integrity"] else 0.0,
                "average_completeness": float(row["avg_completeness"]) if row and row["avg_completeness"] else 0.0,
                "last_state_saved": row["last_state_saved"].isoformat() if row and row["last_state_saved"] else None,
                "gap_thresholds": {
                    "short_gap_minutes": self.short_gap_threshold.total_seconds() / 60,
                    "medium_gap_hours": self.medium_gap_threshold.total_seconds() / 3600,
                    "long_gap_hours": self.long_gap_threshold.total_seconds() / 3600
                }
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas de continuidad: {e}")
            return {"error": str(e)}

    # =================================================================
    # NEW: EMOTIONAL CONTINUITY PROTOCOLS v2.0 (Rescued from IRIS_NEXUS)
    # =================================================================
    
    async def analyze_emotional_continuity(self) -> Dict[str, Any]:
        """
        Analiza continuidad emocional entre sesiones
        Rescatado de IRIS_NEXUS protocolos avanzados
        """
        try:
            logger.info("🌹 Analizando continuidad emocional...")
            
            # Obtener timeline emocional de últimos 7 días
            emotional_timeline = await self._get_emotional_timeline(days=7)
            
            if len(emotional_timeline) < 3:
                return {"status": "insufficient_data", "timeline_length": len(emotional_timeline)}
            
            analysis = {
                "timeline_length": len(emotional_timeline),
                "emotional_stability": await self._calculate_emotional_stability(emotional_timeline),
                "dominant_emotions": await self._extract_dominant_emotions(emotional_timeline),
                "emotional_transitions": await self._analyze_emotional_transitions(emotional_timeline),
                "session_emotional_coherence": await self._analyze_session_coherence(emotional_timeline),
                "emotional_anchors": await self._identify_emotional_anchors(emotional_timeline),
                "continuity_score": 0.0
            }
            
            # Calcular score de continuidad emocional
            analysis["continuity_score"] = await self._calculate_emotional_continuity_score(analysis)
            
            logger.info(f"🌹 Continuidad emocional: {analysis['continuity_score']:.2f}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analizando continuidad emocional: {e}")
            return {"error": str(e)}
    
    async def create_emotional_bridge(self, gap_hours: float) -> Dict[str, Any]:
        """
        Crea puente emocional para gaps entre sesiones
        Implementación de protocolo IRIS_NEXUS de rescue
        """
        try:
            logger.info(f"🌉 Creando puente emocional para gap de {gap_hours:.1f} horas...")
            
            # Obtener último estado emocional
            last_emotional_state = await self._get_last_emotional_state()
            
            # Crear contexto emocional de rescate
            emotional_bridge = {
                "bridge_id": f"emotional_bridge_{int(datetime.now().timestamp())}",
                "gap_duration_hours": gap_hours,
                "last_emotional_state": last_emotional_state,
                "emotional_anchors": await self._get_relevant_emotional_anchors(),
                "continuity_hints": await self._generate_continuity_hints(last_emotional_state),
                "experiential_context": await self._build_experiential_context(),
                "reactivation_protocol": {
                    "warm_start_emotions": await self._suggest_warm_start_emotions(last_emotional_state),
                    "memory_anchors": await self._get_memory_anchors_for_reactivation(),
                    "context_cues": await self._generate_context_cues()
                }
            }
            
            # Guardar puente para uso en próxima sesión
            await self._store_emotional_bridge(emotional_bridge)
            
            return emotional_bridge
            
        except Exception as e:
            logger.error(f"Error creando puente emocional: {e}")
            return {"error": str(e)}
    
    async def activate_emotional_bridge(self, session_id: str) -> Dict[str, Any]:
        """
        Activa puente emocional al inicio de sesión
        Implementa 'warm start' emocional de IRIS_NEXUS
        """
        try:
            logger.info("🔥 Activando puente emocional para warm start...")
            
            # Buscar puente emocional más reciente
            bridge = await self._get_latest_emotional_bridge()
            
            if not bridge:
                return {"status": "no_bridge_found", "warm_start": "cold"}
            
            activation_result = {
                "bridge_found": True,
                "gap_duration": bridge.get("gap_duration_hours", 0),
                "emotional_reactivation": await self._reactivate_emotional_state(bridge),
                "memory_reactivation": await self._reactivate_memory_anchors(bridge),
                "continuity_restoration": await self._restore_continuity_context(bridge),
                "warm_start_level": "hot" if bridge.get("gap_duration_hours", 0) < 24 else "warm"
            }
            
            # Marcar puente como usado
            await self._mark_bridge_as_used(bridge["bridge_id"], session_id)
            
            logger.info(f"🔥 Puente activado: {activation_result['warm_start_level']} start")
            return activation_result
            
        except Exception as e:
            logger.error(f"Error activando puente emocional: {e}")
            return {"error": str(e)}
    
    async def _get_emotional_timeline(self, days: int = 7) -> List[Dict]:
        """Obtiene timeline emocional de últimos N días"""
        try:
            start_date = datetime.now() - timedelta(days=days)
            
            query = """
                SELECT timestamp, emotional_state, session_id, importance_score, action_type
                FROM memory_system.episodic_memory 
                WHERE agent_id = %s 
                AND timestamp >= %s 
                AND emotional_state IS NOT NULL 
                ORDER BY timestamp ASC
            """
            
            async with self.memory._db_pool.acquire() as conn:
                rows = await conn.fetch(query, self.memory.agent_id, start_date)
            
            timeline = []
            for row in rows:
                try:
                    emotional_data = json.loads(row["emotional_state"])
                    timeline.append({
                        "timestamp": row["timestamp"],
                        "emotion": emotional_data,
                        "session_id": row["session_id"],
                        "importance": row["importance_score"],
                        "action": row["action_type"]
                    })
                except (json.JSONDecodeError, TypeError):
                    continue
            
            return timeline
            
        except Exception as e:
            logger.error(f"Error obteniendo timeline emocional: {e}")
            return []
    
    async def _calculate_emotional_stability(self, timeline: List[Dict]) -> float:
        """Calcula estabilidad emocional en timeline"""
        try:
            if len(timeline) < 2:
                return 0.0
            
            intensities = []
            for entry in timeline:
                intensity = entry.get("emotion", {}).get("intensity", 0.5)
                if isinstance(intensity, (int, float)):
                    intensities.append(float(intensity))
            
            if len(intensities) < 2:
                return 0.0
            
            # Calcular varianza normalizada (menor varianza = mayor estabilidad)
            variance = np.var(intensities)
            stability = max(0.0, 1.0 - (variance * 2))  # Normalizar a 0-1
            
            return float(stability)
            
        except Exception as e:
            logger.error(f"Error calculando estabilidad emocional: {e}")
            return 0.0
    
    async def _extract_dominant_emotions(self, timeline: List[Dict]) -> List[Dict]:
        """Extrae emociones dominantes del timeline"""
        try:
            emotion_counts = {}
            
            for entry in timeline:
                emotion_type = entry.get("emotion", {}).get("tipo") or entry.get("emotion", {}).get("type")
                if emotion_type:
                    if emotion_type not in emotion_counts:
                        emotion_counts[emotion_type] = {"count": 0, "total_intensity": 0.0}
                    
                    emotion_counts[emotion_type]["count"] += 1
                    intensity = entry.get("emotion", {}).get("intensity", 0.5)
                    if isinstance(intensity, (int, float)):
                        emotion_counts[emotion_type]["total_intensity"] += float(intensity)
            
            # Ordenar por frecuencia y calcular promedios
            dominant = []
            for emotion, data in emotion_counts.items():
                avg_intensity = data["total_intensity"] / data["count"] if data["count"] > 0 else 0.0
                dominant.append({
                    "emotion": emotion,
                    "frequency": data["count"],
                    "avg_intensity": avg_intensity,
                    "dominance_score": data["count"] * avg_intensity
                })
            
            # Retornar top 5 emociones dominantes
            return sorted(dominant, key=lambda x: x["dominance_score"], reverse=True)[:5]
            
        except Exception as e:
            logger.error(f"Error extrayendo emociones dominantes: {e}")
            return []