"""
CONSOLIDATION ENGINE - Motor de Consolidación Nocturna
Extrae patrones de episodios y los convierte en conocimiento semántico
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from loguru import logger
from collections import defaultdict, Counter

from ..utils.config import get_config


class ConsolidationEngine:
    """
    ENHANCED CONSOLIDATION ENGINE v2.0 
    Motor de consolidación que incluye crystallization temporal:
    1. Procesa episodios no consolidados
    2. Extrae patrones usando análisis inteligente
    3. Actualiza memoria semántica
    4. Fortalece memorias importantes
    5. Limpia memorias redundantes
    6. [NEW] Crystallization temporal automática
    7. [NEW] Análisis emocional y continuidad
    8. [NEW] Cross-session threading
    """
    
    def __init__(self, memory_manager):
        self.memory = memory_manager
        self.config = get_config().consolidation
        
        # Configuración de consolidación básica
        self.batch_size = self.config.get("batch_size", 100)
        self.confidence_threshold = self.config.get("confidence_threshold", 0.7)
        self.min_episodes_for_pattern = self.config.get("min_episodes", 2)
        self.similarity_threshold = self.config.get("similarity_threshold", 0.8)
        
        # [NEW] Configuración crystallization temporal
        self.crystallization_config = self.config.get("crystallization", {})
        self.emotional_weight_threshold = self.crystallization_config.get("emotional_threshold", 0.8)
        self.breakthrough_indicators = self.crystallization_config.get("breakthrough_keywords", [
            "breakthrough", "discovery", "revelation", "insight", "epiphany", "realization"
        ])
        self.crystallization_layers = {
            "immediate": 1,      # Dentro de la sesión
            "daily": 24,         # 24 horas  
            "weekly": 168,       # 1 semana
            "monthly": 720,      # 1 mes
            "permanent": -1      # Cristales permanentes
        }
        
        # Configuración de limpieza
        self.cleanup_config = self.config.get("cleanup", {})
        self.low_importance_threshold = self.cleanup_config.get("low_importance_threshold", 0.3)
        self.retention_days = self.cleanup_config.get("retention_days", 90)
        
        logger.info(f"ConsolidationEngine inicializada - batch_size: {self.batch_size}")
    
    async def run_consolidation(self) -> Dict[str, Any]:
        """
        Proceso principal de consolidación
        
        Pasos:
        1. Obtener episodios no consolidados
        2. Extraer patrones con análisis inteligente
        3. Actualizar memoria semántica
        4. Marcar episodios como consolidados
        5. Fortalecer memorias importantes
        6. Limpiar memorias redundantes
        
        Returns:
            Estadísticas de consolidación
        """
        logger.info("🧠 Iniciando consolidación de memoria...")
        
        consolidation_stats = {
            "start_time": datetime.utcnow(),
            "episodes_processed": 0,
            "patterns_extracted": 0,
            "knowledge_created": 0,
            "memories_strengthened": 0,
            "redundant_cleaned": 0,
            "errors": []
        }
        
        try:
            # 1. Obtener episodios no consolidados
            episodes = await self.memory.episodic_memory.get_unconsolidated_episodes(
                limit=self.batch_size
            )
            consolidation_stats["episodes_processed"] = len(episodes)
            
            if not episodes:
                logger.info("No hay episodios para consolidar")
                consolidation_stats["end_time"] = datetime.utcnow()
                return consolidation_stats
            
            logger.info(f"Procesando {len(episodes)} episodios no consolidados")
            
            # 2. Extraer patrones
            patterns = await self._extract_patterns(episodes)
            consolidation_stats["patterns_extracted"] = len(patterns)
            
            # 3. Actualizar memoria semántica
            if patterns:
                knowledge_items = await self._update_semantic_memory(patterns)
                consolidation_stats["knowledge_created"] = len(knowledge_items)
            
            # 4. Marcar como consolidados
            episode_ids = [str(ep["id"]) for ep in episodes]
            marked = await self.memory.episodic_memory.mark_as_consolidated(episode_ids)
            logger.info(f"Marcados {marked} episodios como consolidados")
            
            # 5. Fortalecer memorias importantes
            strengthened = await self._strengthen_important_memories()
            consolidation_stats["memories_strengthened"] = strengthened
            
            # 6. Limpiar redundantes (ejecutar solo ocasionalmente)
            if len(episodes) >= self.batch_size or datetime.utcnow().hour == 2:
                cleaned = await self._prune_redundant_memories()
                consolidation_stats["redundant_cleaned"] = cleaned
            
            # 7. Registrar consolidación
            await self._log_consolidation(consolidation_stats)
            
            consolidation_stats["end_time"] = datetime.utcnow()
            consolidation_stats["duration"] = (
                consolidation_stats["end_time"] - consolidation_stats["start_time"]
            ).total_seconds()
            
            logger.info(f"✅ Consolidación completada: {consolidation_stats}")
            return consolidation_stats
            
        except Exception as e:
            logger.error(f"Error en consolidación: {e}")
            consolidation_stats["errors"].append(str(e))
            consolidation_stats["end_time"] = datetime.utcnow()
            raise
    
    async def _extract_patterns(self, episodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extrae patrones usando análisis inteligente de episodios
        
        Args:
            episodes: Lista de episodios para analizar
            
        Returns:
            Lista de patrones extraídos
        """
        try:
            logger.info("Extrayendo patrones de episodios...")
            patterns = []
            
            # 1. Patrones por tipo de acción
            action_patterns = await self._extract_action_patterns(episodes)
            patterns.extend(action_patterns)
            
            # 2. Patrones de éxito/fallo
            outcome_patterns = await self._extract_outcome_patterns(episodes)
            patterns.extend(outcome_patterns)
            
            # 3. Patrones emocionales
            emotional_patterns = await self._extract_emotional_patterns(episodes)
            patterns.extend(emotional_patterns)
            
            # 4. Patrones de colaboración
            collaboration_patterns = await self._extract_collaboration_patterns(episodes)
            patterns.extend(collaboration_patterns)
            
            # 5. Patrones temporales
            temporal_patterns = await self._extract_temporal_patterns(episodes)
            patterns.extend(temporal_patterns)
            
            # Filtrar patrones por confianza
            filtered_patterns = [
                pattern for pattern in patterns 
                if pattern.get("confidence", 0) >= self.confidence_threshold
            ]
            
            logger.info(f"Patrones extraídos: {len(filtered_patterns)}/{len(patterns)} (filtrados por confianza)")
            return filtered_patterns
            
        except Exception as e:
            logger.error(f"Error extrayendo patrones: {e}")
            return []
    
    async def _extract_action_patterns(self, episodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extrae patrones basados en tipos de acción"""
        patterns = []
        
        # Agrupar por tipo de acción
        action_groups = defaultdict(list)
        for episode in episodes:
            # Validar que episode sea dict y tenga estructura correcta
            if not isinstance(episode, dict):
                logger.warning(f"Episode inválido (no es dict): {type(episode)}")
                continue
            
            # PARSEAR campos JSON que vienen como strings
            try:
                # action_details puede ser string JSON
                if isinstance(episode.get("action_details"), str):
                    episode["action_details"] = json.loads(episode["action_details"])
                
                # context_state puede ser string JSON
                if isinstance(episode.get("context_state"), str):
                    episode["context_state"] = json.loads(episode["context_state"])
                
                # outcome puede ser string JSON
                if isinstance(episode.get("outcome"), str):
                    episode["outcome"] = json.loads(episode["outcome"])
                
                # emotional_state puede ser string JSON
                if isinstance(episode.get("emotional_state"), str):
                    episode["emotional_state"] = json.loads(episode["emotional_state"])
                    
            except json.JSONDecodeError as e:
                logger.warning(f"Error parseando JSON en episode {episode.get('id', 'unknown')}: {e}")
                # Continuar con valores por defecto
                pass
                
            action_type = episode.get("action_type", "unknown")
            action_groups[action_type].append(episode)
        
        # Buscar patrones en cada grupo
        for action_type, group_episodes in action_groups.items():
            # NUEVA LÓGICA: Crear patrón básico para cualquier grupo con 1+ episodios
            if len(group_episodes) >= 1:
                # Patrón básico de actividad
                patterns.append({
                    "type": "activity_pattern",
                    "action_type": action_type,
                    "description": f"Actividad detectada: {action_type} ({len(group_episodes)} ocurrencias)",
                    "confidence": min(0.9, len(group_episodes) / 5),
                    "evidence_count": len(group_episodes),
                    "episode_ids": [str(ep.get("id", "")) for ep in group_episodes],
                    "tags": [action_type, "activity", "frequency"],
                    "metadata": {
                        "total_occurrences": len(group_episodes),
                        "pattern_type": "basic_activity"
                    }
                })
            
            if len(group_episodes) >= self.min_episodes_for_pattern:
                
                # Patrón de éxito para este tipo de acción
                successful = []
                for ep in group_episodes:
                    outcome = ep.get("outcome", {})
                    if isinstance(outcome, dict) and outcome.get("success", False):
                        successful.append(ep)
                    elif isinstance(outcome, str):
                        # Si outcome es string, parsearlo
                        try:
                            outcome_dict = json.loads(outcome)
                            if outcome_dict.get("success", False):
                                successful.append(ep)
                        except:
                            pass
                
                if len(successful) >= 1:
                    success_rate = len(successful) / len(group_episodes)
                    patterns.append({
                        "type": "action_success_pattern",
                        "action_type": action_type,
                        "description": f"Patrón de éxito para {action_type}: {success_rate:.2%} tasa de éxito",
                        "confidence": success_rate,
                        "evidence_count": len(successful),
                        "episode_ids": [str(ep.get("id", "")) for ep in successful],
                        "tags": [action_type, "success_pattern", "behavioral"],
                        "metadata": {
                            "total_attempts": len(group_episodes),
                            "successful_attempts": len(successful),
                            "success_rate": success_rate
                        }
                    })
                
                # Patrón de contexto común
                common_context = self._find_common_context_keys(group_episodes)
                if common_context:
                    patterns.append({
                        "type": "context_pattern",
                        "action_type": action_type,
                        "description": f"Contexto común para {action_type}: {common_context}",
                        "confidence": 0.8,
                        "evidence_count": len(group_episodes),
                        "episode_ids": [str(ep.get("id", "")) for ep in group_episodes],
                        "tags": [action_type, "context_pattern", "environmental"],
                        "metadata": {
                            "common_context_keys": common_context
                        }
                    })
        
        return patterns
    
    async def _extract_outcome_patterns(self, episodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extrae patrones basados en outcomes"""
        patterns = []
        
        # Analizar relación contexto -> outcome
        context_outcome_map = defaultdict(list)
        
        for episode in episodes:
            context_state = episode.get("context_state", {})
            outcome = episode.get("outcome", {})
            
            # Simplificar contexto a claves principales
            context_key = "_".join(sorted(context_state.keys())[:3])  # Top 3 keys
            context_outcome_map[context_key].append(outcome)
        
        # Buscar patrones predecibles
        for context_key, outcomes in context_outcome_map.items():
            if len(outcomes) >= self.min_episodes_for_pattern:
                
                # Analizar consistencia de outcomes
                success_count = sum(1 for outcome in outcomes if outcome.get("success", False))
                consistency = success_count / len(outcomes)
                
                if consistency >= 0.8 or consistency <= 0.2:  # Alta consistencia en cualquier dirección
                    patterns.append({
                        "type": "outcome_prediction_pattern",
                        "description": f"Contexto '{context_key}' predice resultado con {consistency:.2%} consistencia",
                        "confidence": abs(consistency - 0.5) * 2,  # Distancia de random
                        "evidence_count": len(outcomes),
                        "episode_ids": [],  # Se puede mejorar para trackear IDs
                        "tags": ["prediction", "outcome", "contextual"],
                        "metadata": {
                            "context_pattern": context_key,
                            "success_rate": consistency,
                            "sample_size": len(outcomes)
                        }
                    })
        
        return patterns
    
    async def _extract_emotional_patterns(self, episodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extrae patrones emocionales"""
        patterns = []
        
        # Agrupar por estado emocional
        emotional_episodes = []
        for episode in episodes:
            emotional_state = episode.get("emotional_state", {})
            if emotional_state:
                emotional_episodes.append(episode)
        
        if len(emotional_episodes) < self.min_episodes_for_pattern:
            return patterns
        
        # Analizar emociones dominantes
        emotions = []
        valences = []
        intensities = []
        
        for episode in emotional_episodes:
            emotional_state = episode.get("emotional_state", {})
            
            if "emotion" in emotional_state:
                emotions.append(emotional_state["emotion"])
            if "valence" in emotional_state:
                valences.append(emotional_state["valence"])
            if "intensity" in emotional_state:
                intensities.append(emotional_state["intensity"])
        
        # Patrón de emoción dominante
        if emotions:
            emotion_counter = Counter(emotions)
            dominant_emotion = emotion_counter.most_common(1)[0]
            
            if dominant_emotion[1] >= self.min_episodes_for_pattern:
                patterns.append({
                    "type": "emotional_pattern",
                    "description": f"Emoción predominante: {dominant_emotion[0]} ({dominant_emotion[1]} ocurrencias)",
                    "confidence": dominant_emotion[1] / len(emotions),
                    "evidence_count": dominant_emotion[1],
                    "episode_ids": [],
                    "tags": ["emotional", "personality", dominant_emotion[0]],
                    "metadata": {
                        "emotion": dominant_emotion[0],
                        "frequency": dominant_emotion[1],
                        "total_emotional_episodes": len(emotions)
                    }
                })
        
        # Patrón de valencia
        if valences:
            positive_count = valences.count("positive")
            if positive_count > len(valences) * 0.7:
                patterns.append({
                    "type": "emotional_valence_pattern",
                    "description": f"Tendencia emocional positiva: {positive_count}/{len(valences)} episodios",
                    "confidence": positive_count / len(valences),
                    "evidence_count": positive_count,
                    "episode_ids": [],
                    "tags": ["emotional", "positive", "personality"],
                    "metadata": {
                        "positive_ratio": positive_count / len(valences),
                        "total_valence_episodes": len(valences)
                    }
                })
        
        return patterns
    
    async def _extract_collaboration_patterns(self, episodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extrae patrones de colaboración"""
        patterns = []
        
        # Buscar menciones de personas/entidades
        collaborators = ["Ricardo", "Iris", "Nexus", "equipo", "familia"]
        collaboration_episodes = defaultdict(list)
        
        for episode in episodes:
            episode_text = json.dumps(episode.get("action_details", {})).lower()
            
            for collaborator in collaborators:
                if collaborator.lower() in episode_text:
                    collaboration_episodes[collaborator].append(episode)
        
        # Analizar patrones de colaboración
        for collaborator, collab_episodes in collaboration_episodes.items():
            if len(collab_episodes) >= self.min_episodes_for_pattern:
                
                # Analizar éxito en colaboraciones
                successful_collabs = [
                    ep for ep in collab_episodes 
                    if ep.get("outcome", {}).get("success", False)
                ]
                
                if len(successful_collabs) >= 2:
                    success_rate = len(successful_collabs) / len(collab_episodes)
                    
                    patterns.append({
                        "type": "collaboration_pattern",
                        "description": f"Colaboración exitosa con {collaborator}: {success_rate:.2%} tasa de éxito",
                        "confidence": success_rate,
                        "evidence_count": len(successful_collabs),
                        "episode_ids": [str(ep.get("id", "")) for ep in successful_collabs],
                        "tags": ["collaboration", collaborator.lower(), "relationship"],
                        "metadata": {
                            "collaborator": collaborator,
                            "total_collaborations": len(collab_episodes),
                            "successful_collaborations": len(successful_collabs),
                            "success_rate": success_rate
                        }
                    })
        
        return patterns
    
    async def _extract_temporal_patterns(self, episodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extrae patrones temporales"""
        patterns = []
        
        # Agrupar por hora del día
        hourly_activity = defaultdict(list)
        
        for episode in episodes:
            timestamp = episode.get("timestamp")
            if timestamp:
                if isinstance(timestamp, str):
                    try:
                        timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    except:
                        continue
                
                hour = timestamp.hour
                hourly_activity[hour].append(episode)
        
        # Buscar horas de máxima actividad
        if hourly_activity:
            max_activity_hour = max(hourly_activity.keys(), key=lambda h: len(hourly_activity[h]))
            max_episodes = len(hourly_activity[max_activity_hour])
            total_episodes = len(episodes)
            
            if max_episodes >= self.min_episodes_for_pattern and max_episodes / total_episodes > 0.3:
                patterns.append({
                    "type": "temporal_activity_pattern",
                    "description": f"Pico de actividad a las {max_activity_hour}:00 ({max_episodes} episodios)",
                    "confidence": max_episodes / total_episodes,
                    "evidence_count": max_episodes,
                    "episode_ids": [str(ep.get("id", "")) for ep in hourly_activity[max_activity_hour]],
                    "tags": ["temporal", "activity_pattern", f"hour_{max_activity_hour}"],
                    "metadata": {
                        "peak_hour": max_activity_hour,
                        "episodes_at_peak": max_episodes,
                        "total_episodes": total_episodes,
                        "concentration_ratio": max_episodes / total_episodes
                    }
                })
        
        return patterns
    
    def _find_common_context_keys(self, episodes: List[Dict[str, Any]]) -> List[str]:
        """Encuentra claves de contexto comunes en episodios"""
        if not episodes:
            return []
        
        # Intersección de claves de contexto
        common_keys = set()
        for i, episode in enumerate(episodes):
            context_keys = set(episode.get("context_state", {}).keys())
            
            if i == 0:
                common_keys = context_keys
            else:
                common_keys &= context_keys
        
        return list(common_keys)
    
    async def _update_semantic_memory(self, patterns: List[Dict[str, Any]]) -> List[str]:
        """
        Actualiza memoria semántica con patrones extraídos
        
        Args:
            patterns: Lista de patrones extraídos
            
        Returns:
            Lista de IDs de conocimiento creado
        """
        try:
            logger.info(f"Actualizando memoria semántica con {len(patterns)} patrones")
            
            knowledge_ids = []
            
            for pattern in patterns:
                # Usar SemanticMemory para almacenar el patrón como conocimiento
                logger.debug(f"Intentando almacenar patrón: {pattern.get('type', 'pattern')} - {pattern.get('description', '')[:50]}...")
                
                knowledge_id = await self.memory.semantic_memory._store_knowledge_item(
                    knowledge_type=pattern.get("type", "pattern"),
                    content=pattern.get("description", ""),
                    confidence_score=pattern.get("confidence", 0.7),
                    source_episodes=pattern.get("episode_ids", []),
                    tags=pattern.get("tags", [])
                )
                
                if knowledge_id and knowledge_id.strip():
                    knowledge_ids.append(knowledge_id)
                    logger.debug(f"Patrón almacenado exitosamente: {knowledge_id}")
                else:
                    logger.warning(f"Falló almacenamiento de patrón: {pattern.get('type', 'pattern')}")
            
            logger.info(f"Memoria semántica actualizada: {len(knowledge_ids)} items creados")
            return knowledge_ids
            
        except Exception as e:
            logger.error(f"Error actualizando memoria semántica: {e}")
            return []
    
    async def _strengthen_important_memories(self) -> int:
        """
        Fortalece memorias importantes aumentando su accesibilidad
        
        Returns:
            Número de memorias fortalecidas
        """
        try:
            # Obtener episodios de alta importancia recientes
            recent_episodes = await self.memory.episodic_memory.get_recent_episodes(
                limit=50, 
                hours_back=24
            )
            
            important_episodes = [
                ep for ep in recent_episodes 
                if ep.get("importance_score", 0) > 0.8
            ]
            
            strengthened = 0
            
            for episode in important_episodes:
                # Aumentar importance_score ligeramente (máximo 1.0)
                current_score = episode.get("importance_score", 0)
                new_score = min(1.0, current_score + 0.05)
                
                success = await self.memory.episodic_memory.update_episode(
                    episode_id=str(episode["id"]),
                    updates={"importance_score": new_score}
                )
                
                if success:
                    strengthened += 1
            
            logger.info(f"Memorias fortalecidas: {strengthened}")
            return strengthened
            
        except Exception as e:
            logger.error(f"Error fortaleciendo memorias: {e}")
            return 0
    
    async def _prune_redundant_memories(self) -> int:
        """
        Elimina memorias redundantes o de muy baja importancia
        
        Returns:
            Número de memorias eliminadas
        """
        try:
            logger.info("Iniciando limpieza de memorias redundantes...")
            
            # Obtener episodios antiguos de baja importancia
            cutoff_date = datetime.utcnow() - timedelta(days=self.retention_days)
            
            # Query para encontrar episodios candidatos a eliminación
            query = """
                SELECT id, importance_score, timestamp
                FROM memory_system.episodes
                WHERE agent_id = $1 
                  AND importance_score < $2
                  AND timestamp < $3
                  AND consolidated = TRUE
                ORDER BY importance_score ASC, timestamp ASC
                LIMIT 50
            """
            
            async with self.memory._db_pool.acquire() as conn:
                rows = await conn.fetch(
                    query,
                    self.memory.agent_id,
                    self.low_importance_threshold,
                    cutoff_date
                )
            
            if not rows:
                logger.info("No hay memorias para limpiar")
                return 0
            
            # Eliminar episodios de muy baja importancia
            deleted_count = 0
            for row in rows:
                if row["importance_score"] < 0.2:  # Threshold muy bajo
                    delete_query = "DELETE FROM memory_system.episodes WHERE id = $1"
                    
                    async with self.memory._db_pool.acquire() as conn:
                        await conn.execute(delete_query, row["id"])
                    
                    deleted_count += 1
            
            logger.info(f"Memorias redundantes eliminadas: {deleted_count}")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error limpiando memorias: {e}")
            return 0
    
    async def _log_consolidation(self, stats: Dict[str, Any]) -> None:
        """Registra estadísticas de consolidación en la base de datos"""
        try:
            query = """
                INSERT INTO memory_system.consolidation_logs (
                    consolidation_type, episodes_processed, patterns_extracted,
                    knowledge_created, duration_seconds, status
                ) VALUES ($1, $2, $3, $4, $5, $6)
            """
            
            duration = stats.get("duration", 0)
            status = "completed" if not stats.get("errors") else "partial"
            
            async with self.memory._db_pool.acquire() as conn:
                await conn.execute(
                    query,
                    "automatic",
                    stats.get("episodes_processed", 0),
                    stats.get("patterns_extracted", 0),
                    stats.get("knowledge_created", 0),
                    duration,
                    status
                )
                
        except Exception as e:
            logger.warning(f"Error registrando consolidación: {e}")
    
    async def schedule_nightly_consolidation(self) -> None:
        """
        Programa consolidación nocturna automática
        (En implementación real, usaría cron job o scheduler)
        """
        try:
            logger.info("Programando consolidación nocturna...")
            
            # Por ahora, solo registrar la intención
            # En implementación completa, usaría APScheduler o cron
            
            logger.info("Consolidación nocturna programada para 2:00 AM")
            
        except Exception as e:
            logger.error(f"Error programando consolidación nocturna: {e}")
    
    async def get_consolidation_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de consolidaciones pasadas"""
        try:
            query = """
                SELECT 
                    COUNT(*) as total_runs,
                    AVG(episodes_processed) as avg_episodes,
                    AVG(patterns_extracted) as avg_patterns,
                    AVG(knowledge_created) as avg_knowledge,
                    AVG(duration_seconds) as avg_duration,
                    MAX(timestamp) as last_run
                FROM memory_system.consolidation_logs
                WHERE status = 'completed'
            """
            
            async with self.memory._db_pool.acquire() as conn:
                row = await conn.fetchrow(query)
            
            return dict(row) if row else {}
            
        except Exception as e:
            logger.error(f"Error obteniendo stats de consolidación: {e}")
            return {}

    # =====================================================
    # NUEVOS MÉTODOS: CRYSTALLIZATION TEMPORAL v2.0
    # =====================================================
    
    async def run_temporal_crystallization(self) -> Dict[str, Any]:
        """
        Ejecuta crystallization temporal de memorias por capas temporales
        Rescatado de NEXUS_ORGANIZED sistema V2
        """
        try:
            logger.info("🔮 Iniciando Crystallization Temporal v2.0...")
            start_time = datetime.now()
            
            results = {
                "timestamp": start_time.isoformat(),
                "crystals_created": {},
                "emotional_insights": [],
                "breakthrough_moments": [],
                "continuity_threads": []
            }
            
            # 1. Crystallization por capas temporales
            for layer_name, hours_back in self.crystallization_layers.items():
                if hours_back == -1:  # Permanent crystals
                    crystals = await self._create_permanent_crystals()
                else:
                    crystals = await self._create_temporal_crystals(layer_name, hours_back)
                
                results["crystals_created"][layer_name] = len(crystals)
                logger.info(f"✨ {layer_name}: {len(crystals)} cristales creados")
            
            # 2. Análisis emocional avanzado
            emotional_insights = await self._analyze_emotional_continuity()
            results["emotional_insights"] = emotional_insights
            
            # 3. Detección de breakthrough moments
            breakthroughs = await self._detect_breakthrough_moments()
            results["breakthrough_moments"] = breakthroughs
            
            # 4. Cross-session threading
            continuity_threads = await self._extract_continuity_threads()
            results["continuity_threads"] = continuity_threads
            
            # 5. Actualizar metadata de cristalización
            await self._update_crystallization_metadata(results)
            
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"🔮 Crystallization completada en {duration:.2f}s")
            
            return results
            
        except Exception as e:
            logger.error(f"Error en crystallization temporal: {e}")
            return {"error": str(e), "status": "failed"}
    
    async def _create_temporal_crystals(self, layer_name: str, hours_back: int) -> List[Dict]:
        """Crea cristales para una capa temporal específica"""
        try:
            # Obtener episodios del período
            start_time = datetime.now() - timedelta(hours=hours_back)
            
            query = """
                SELECT * FROM memory_system.episodic_memory 
                WHERE timestamp >= %s 
                AND importance_score >= %s
                ORDER BY importance_score DESC, timestamp DESC
            """
            
            async with self.memory._db_pool.acquire() as conn:
                episodes = await conn.fetch(query, start_time, self.emotional_weight_threshold)
            
            crystals = []
            for episode in episodes:
                # Crear cristal temporal
                crystal = await self._create_memory_crystal(episode, layer_name)
                if crystal:
                    crystals.append(crystal)
            
            return crystals
            
        except Exception as e:
            logger.error(f"Error creando cristales temporales {layer_name}: {e}")
            return []
    
    async def _create_memory_crystal(self, episode: Dict, layer: str) -> Optional[Dict]:
        """Convierte un episodio en cristal de memoria con metadata temporal"""
        try:
            crystal = {
                "crystal_id": f"crystal_{layer}_{episode['id']}_{int(datetime.now().timestamp())}",
                "layer": layer,
                "source_episode_id": episode['id'],
                "timestamp": datetime.now().isoformat(),
                "emotional_resonance": await self._calculate_emotional_resonance(episode),
                "breakthrough_level": await self._assess_breakthrough_level(episode),
                "continuity_anchors": await self._extract_continuity_anchors(episode),
                "crystallized_essence": {
                    "core_action": episode.get('action_type'),
                    "emotional_state": json.loads(episode.get('emotional_state', '{}')),
                    "outcome_impact": json.loads(episode.get('outcome', '{}')),
                    "context_keys": await self._extract_context_keys(episode),
                    "learning_extracted": await self._extract_learning(episode)
                }
            }
            
            # Guardar cristal en memoria semántica
            await self._store_crystal_in_semantic_memory(crystal)
            
            return crystal
            
        except Exception as e:
            logger.error(f"Error creando cristal: {e}")
            return None
    
    async def _analyze_emotional_continuity(self) -> List[Dict]:
        """Analiza continuidad emocional entre sesiones - Rescatado de IRIS_NEXUS"""
        try:
            # Obtener últimos 7 días de episodios
            week_ago = datetime.now() - timedelta(days=7)
            
            query = """
                SELECT timestamp, emotional_state, importance_score, action_type, session_id
                FROM memory_system.episodic_memory 
                WHERE timestamp >= %s 
                ORDER BY timestamp ASC
            """
            
            async with self.memory._db_pool.acquire() as conn:
                episodes = await conn.fetch(query, week_ago)
            
            insights = []
            emotional_timeline = []
            
            for episode in episodes:
                try:
                    emotional_data = json.loads(episode.get('emotional_state', '{}'))
                    if emotional_data:
                        emotional_timeline.append({
                            "timestamp": episode['timestamp'],
                            "emotion": emotional_data,
                            "intensity": emotional_data.get('intensity', 0.5),
                            "session": episode['session_id']
                        })
                except json.JSONDecodeError:
                    continue
            
            # Análisis de patrones emocionales
            if len(emotional_timeline) >= 3:
                insights.append({
                    "type": "emotional_continuity_analysis",
                    "timeline_length": len(emotional_timeline),
                    "dominant_emotions": await self._extract_dominant_emotions(emotional_timeline),
                    "emotional_stability": await self._calculate_emotional_stability(emotional_timeline),
                    "session_transitions": await self._analyze_session_transitions(emotional_timeline)
                })
            
            return insights
            
        except Exception as e:
            logger.error(f"Error analizando continuidad emocional: {e}")
            return []
    
    async def _detect_breakthrough_moments(self) -> List[Dict]:
        """Detecta momentos breakthrough basado en keywords y patrones"""
        try:
            breakthroughs = []
            
            # Buscar episodios con indicators de breakthrough
            for keyword in self.breakthrough_indicators:
                query = """
                    SELECT * FROM memory_system.episodes 
                    WHERE (action_details::text ILIKE %s OR action_type ILIKE %s)
                    AND timestamp >= %s
                    AND importance_score >= %s
                    ORDER BY importance_score DESC
                """
                
                week_ago = datetime.now() - timedelta(days=7)
                search_pattern = f"%{keyword}%"
                
                async with self.memory._db_pool.acquire() as conn:
                    episodes = await conn.fetch(
                        query, search_pattern, search_pattern, 
                        week_ago, self.emotional_weight_threshold
                    )
                
                for episode in episodes:
                    breakthrough = {
                        "episode_id": episode['id'],
                        "timestamp": episode['timestamp'],
                        "breakthrough_indicator": keyword,
                        "importance_score": episode['importance_score'],
                        "context": json.loads(episode.get('action_details', '{}')),
                        "emotional_impact": json.loads(episode.get('emotional_state', '{}'))
                    }
                    breakthroughs.append(breakthrough)
            
            # Deduplicar y ordenar por importancia
            unique_breakthroughs = []
            seen_episodes = set()
            
            for bt in sorted(breakthroughs, key=lambda x: x['importance_score'], reverse=True):
                if bt['episode_id'] not in seen_episodes:
                    unique_breakthroughs.append(bt)
                    seen_episodes.add(bt['episode_id'])
            
            return unique_breakthroughs[:10]  # Top 10 breakthroughs
            
        except Exception as e:
            logger.error(f"Error detectando breakthrough moments: {e}")
            return []