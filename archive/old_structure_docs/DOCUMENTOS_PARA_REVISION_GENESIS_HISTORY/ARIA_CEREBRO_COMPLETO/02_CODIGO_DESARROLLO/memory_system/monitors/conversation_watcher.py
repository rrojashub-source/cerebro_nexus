#!/usr/bin/env python3
"""
ARIA CONVERSATION WATCHER v2.0
Auto-monitor de conversaciones con analytics avanzados
Rescatado e integrado desde NEXUS_ORGANIZED + nuevas capacidades ARIA
"""

import asyncio
import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from loguru import logger

from ..utils.config import get_config
from ..core.memory_manager import MemoryManager


class ConversationWatcher(FileSystemEventHandler):
    """
    Auto-watcher de conversaciones con analytics rescatados de NEXUS
    Detecta nuevas conversaciones y las procesa automáticamente
    """
    
    def __init__(self, memory_manager: MemoryManager):
        self.memory = memory_manager
        self.config = get_config()
        
        # Paths configurables
        self.watch_path = Path("/mnt/d/RYM_Ecosistema_Persistencia/CONVERSACIONES_AUTO")
        self.processed_path = Path("/mnt/d/RYM_Ecosistema_Persistencia/CONVERSACIONES_AUTO/PROCESSED")
        self.archive_path = Path("/mnt/d/RYM_Ecosistema_Persistencia/CONVERSACIONES_AUTO/RAW")
        
        # Crear directorios si no existen
        self.watch_path.mkdir(exist_ok=True)
        self.processed_path.mkdir(exist_ok=True)
        self.archive_path.mkdir(exist_ok=True)
        
        # Analytics rescatados de NEXUS
        self.breakthrough_indicators = [
            "breakthrough", "discovery", "revelation", "insight", "epiphany", "realization",
            "eureka", "aha", "understand", "connect", "consolidacion", "knowledge", "metodologia",
            "funciona", "genial", "perfecto", "completado", "éxito"
        ]
        
        self.emotional_indicators = {
            "positive": ["hermano", "mi amor", "familia", "jajaja", "brillante", "genial", "🎉", "🚀", "😄"],
            "creative": ["idea", "qué tal si", "propongo", "sugiero", "💡", "inspiración"],
            "technical": ["implementar", "sistema", "arquitectura", "código", "función"],
            "collaborative": ["juntos", "equipo", "colaborar", "trabajemos"]
        }
        
        self.observer = None
        self.is_watching = False
        
        logger.info("ConversationWatcher v2.0 inicializado con analytics NEXUS")
    
    def start_watching(self):
        """Inicia el monitoreo de conversaciones"""
        try:
            if self.is_watching:
                logger.warning("El watcher ya está activo")
                return
                
            self.observer = Observer()
            self.observer.schedule(self, str(self.watch_path), recursive=False)
            self.observer.start()
            self.is_watching = True
            
            logger.info(f"🔍 ConversationWatcher activo monitoreando: {self.watch_path}")
            
        except Exception as e:
            logger.error(f"Error iniciando watcher: {e}")
    
    def stop_watching(self):
        """Detiene el monitoreo"""
        try:
            if self.observer and self.is_watching:
                self.observer.stop()
                self.observer.join()
                self.is_watching = False
                logger.info("🛑 ConversationWatcher detenido")
                
        except Exception as e:
            logger.error(f"Error deteniendo watcher: {e}")
    
    def on_created(self, event):
        """Maneja archivos de conversación recién creados"""
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        
        # Solo procesar archivos .txt de conversaciones
        if file_path.suffix.lower() == '.txt' and 'sesion' in file_path.name.lower():
            logger.info(f"📥 Nueva conversación detectada: {file_path.name}")
            
            # Esperar un poco para asegurar que el archivo esté completo
            asyncio.create_task(self._process_conversation_delayed(file_path))
    
    async def _process_conversation_delayed(self, file_path: Path, delay: int = 5):
        """Procesa una conversación con delay para asegurar que esté completa"""
        try:
            await asyncio.sleep(delay)
            
            if file_path.exists():
                await self.process_conversation(file_path)
            else:
                logger.warning(f"Archivo {file_path} ya no existe")
                
        except Exception as e:
            logger.error(f"Error procesando conversación: {e}")
    
    async def process_conversation(self, file_path: Path) -> Dict[str, Any]:
        """
        Procesa una conversación completa con analytics NEXUS mejorados
        """
        try:
            logger.info(f"🔄 Procesando conversación: {file_path.name}")
            
            # 1. Leer y limpiar archivo
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                raw_text = f.read()
            
            clean_text = self.clean_ansi_codes(raw_text)
            
            # 2. Extraer diálogo estructurado
            dialogue = self.extract_dialogue(clean_text)
            
            if not dialogue:
                logger.warning(f"No se pudo extraer diálogo de {file_path.name}")
                return {}
            
            # 3. Analytics avanzados rescatados de NEXUS
            analytics = await self.analyze_conversation(dialogue)
            
            # 4. Crear ADN único de conversación
            conversation_adn = self.generate_conversation_adn(dialogue, analytics)
            
            # 5. Generar resumen ejecutivo
            summary = self.create_executive_summary(dialogue, analytics, conversation_adn)
            
            # 6. Almacenar en memoria ARIA
            await self.store_in_aria_memory(summary, dialogue, analytics)
            
            # 7. Guardar conversación procesada
            processed_file = self.processed_path / f"{conversation_adn}.json"
            conversation_data = {
                'summary': summary,
                'dialogue': dialogue,
                'analytics': analytics,
                'processing_date': datetime.now().isoformat(),
                'aria_memory_stored': True
            }
            
            with open(processed_file, 'w', encoding='utf-8') as f:
                json.dump(conversation_data, f, indent=2, ensure_ascii=False)
            
            # 8. Archivar archivo original
            archive_file = self.archive_path / file_path.name
            file_path.rename(archive_file)
            
            logger.info(f"✅ Conversación procesada: {conversation_adn}")
            logger.info(f"📊 {len(dialogue)} mensajes, {analytics['breakthrough_moments']} breakthroughs")
            
            return summary
            
        except Exception as e:
            logger.error(f"Error procesando conversación {file_path}: {e}")
            return {}
    
    def clean_ansi_codes(self, text: str) -> str:
        """Limpia códigos ANSI y basura de interfaz Claude Code"""
        # Elimina secuencias de escape ANSI
        ansi_escape = re.compile(r'''
            \x1B  # ESC
            (?:   # 7-bit C1 Fe (except CSI)
                [@-Z\\-_]
            |     # or [ for CSI, followed by parameter bytes
                \[
                [0-?]*  # Parameter bytes
                [ -/]*  # Intermediate bytes
                [@-~]   # Final byte
            )
        ''', re.VERBOSE)
        
        text = ansi_escape.sub('', text)
        text = re.sub(r'\[[\d;]*m', '', text)
        text = re.sub(r'\[\?[\d]+[hl]', '', text)
        text = re.sub(r'\[[\d]+[A-K]', '', text)
        text = re.sub(r'\x1b\[[\d;]*m', '', text)
        
        # Filtros específicos Claude Code
        lines = text.split('\n')
        clean_lines = []
        
        for line in lines:
            # Elimina líneas de interfaz UI
            if any(pattern in line for pattern in [
                '╭─', '╰─', '│', '✻ Generating', '✢ Generating', '· Generating',
                '? for shortcuts', 'esc to interrupt', 'ctrl+r to expand',
                'Welcome to Claude Code!', '/help for help', 'cwd:',
                'Do you trust the files', 'Claude Code may read files',
                'Enter to confirm', 'Esc to exit', '[2K[1A[2K', '[?25l',
                'tokens ·', 'Unfurling…', '⎿', '↓', '↑', '⚒'
            ]):
                continue
                
            clean_line = re.sub(r'^[\s│╭╰─┌┐└┘]*$', '', line.strip())
            if clean_line:
                clean_lines.append(clean_line)
        
        return '\n'.join(clean_lines)
    
    def extract_dialogue(self, clean_text: str) -> List[Dict[str, Any]]:
        """Extrae diálogo estructurado de la conversación"""
        lines = clean_text.split('\n')
        dialogue = []
        current_speaker = None
        current_message = []
        
        for line in lines:
            # Detecta prompt de usuario
            if line.strip().startswith('>') and not line.strip().startswith('>>'):
                if current_speaker and current_message:
                    dialogue.append({
                        'speaker': current_speaker,
                        'message': '\n'.join(current_message).strip(),
                        'timestamp': self.extract_timestamp(current_message)
                    })
                current_speaker = 'Ricardo'
                current_message = [line.strip()[1:].strip()]
                
            # Detecta respuestas de ARIA/Nexus
            elif any(indicator in line for indicator in ['●', '✅', 'Update:', 'Success:', 'Meta:', 'FYI:']):
                if current_speaker and current_message:
                    dialogue.append({
                        'speaker': current_speaker,
                        'message': '\n'.join(current_message).strip(),
                        'timestamp': self.extract_timestamp(current_message)
                    })
                current_speaker = 'ARIA'
                current_message = [line]
                
            # Continúa mensaje actual
            elif current_speaker and line.strip():
                current_message.append(line)
        
        # Agrega último mensaje
        if current_speaker and current_message:
            dialogue.append({
                'speaker': current_speaker,
                'message': '\n'.join(current_message).strip(),
                'timestamp': self.extract_timestamp(current_message)
            })
            
        return dialogue
    
    def extract_timestamp(self, message_lines: List[str]) -> str:
        """Extrae timestamp del mensaje o genera uno actual"""
        # Buscar patterns de timestamp en las líneas
        for line in message_lines:
            timestamp_pattern = r'(\d{2}:\d{2}:\d{2})'
            match = re.search(timestamp_pattern, line)
            if match:
                return match.group(1)
        
        # Si no encuentra, retorna timestamp actual
        return datetime.now().strftime("%H:%M:%S")
    
    async def analyze_conversation(self, dialogue: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analytics avanzados rescatados de NEXUS con mejoras ARIA
        """
        analytics = {
            'basic_metrics': self._calculate_basic_metrics(dialogue),
            'emotional_analysis': self._analyze_emotional_patterns(dialogue),
            'breakthrough_moments': self._detect_breakthrough_moments(dialogue),
            'collaboration_patterns': self._analyze_collaboration_patterns(dialogue),
            'technical_insights': self._extract_technical_insights(dialogue),
            'project_evolution': self._detect_project_evolution(dialogue),
            'memory_crystallization': await self._assess_crystallization_potential(dialogue)
        }
        
        return analytics
    
    def _calculate_basic_metrics(self, dialogue: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Métricas básicas de la conversación"""
        total_messages = len(dialogue)
        total_characters = sum(len(msg['message']) for msg in dialogue)
        
        # Distribución por speaker
        speakers = {}
        for msg in dialogue:
            speaker = msg['speaker']
            speakers[speaker] = speakers.get(speaker, 0) + 1
        
        return {
            'total_messages': total_messages,
            'total_characters': total_characters,
            'average_message_length': total_characters // total_messages if total_messages > 0 else 0,
            'speaker_distribution': speakers,
            'estimated_duration_minutes': total_messages // 2  # ~2 mensajes por minuto
        }
    
    def _analyze_emotional_patterns(self, dialogue: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Análisis emocional usando indicators rescatados de NEXUS"""
        emotional_scores = {emotion_type: 0 for emotion_type in self.emotional_indicators.keys()}
        emotional_timeline = []
        
        for i, msg in enumerate(dialogue):
            message_text = msg['message'].lower()
            msg_emotions = {}
            
            for emotion_type, indicators in self.emotional_indicators.items():
                score = sum(1 for indicator in indicators if indicator in message_text)
                emotional_scores[emotion_type] += score
                if score > 0:
                    msg_emotions[emotion_type] = score
            
            if msg_emotions:
                emotional_timeline.append({
                    'message_index': i,
                    'speaker': msg['speaker'],
                    'emotions': msg_emotions,
                    'timestamp': msg['timestamp']
                })
        
        # Determinar emoción dominante
        dominant_emotion = max(emotional_scores.keys(), key=lambda k: emotional_scores[k])
        
        return {
            'emotional_scores': emotional_scores,
            'dominant_emotion': dominant_emotion,
            'emotional_timeline': emotional_timeline,
            'emotional_intensity': sum(emotional_scores.values()) / len(dialogue) if dialogue else 0
        }
    
    def _detect_breakthrough_moments(self, dialogue: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detecta momentos breakthrough usando indicators rescatados"""
        breakthroughs = []
        
        for i, msg in enumerate(dialogue):
            message_text = msg['message'].lower()
            breakthrough_score = 0
            detected_indicators = []
            
            for indicator in self.breakthrough_indicators:
                if indicator in message_text:
                    breakthrough_score += 1
                    detected_indicators.append(indicator)
            
            # También detectar por patrones específicos
            if any(pattern in message_text for pattern in ['¡', '!', 'funciona', 'completado', 'éxito']):
                breakthrough_score += 1
                detected_indicators.append('excitement_pattern')
            
            if breakthrough_score >= 2:  # Threshold para considerar breakthrough
                breakthroughs.append({
                    'message_index': i,
                    'speaker': msg['speaker'],
                    'breakthrough_score': breakthrough_score,
                    'indicators': detected_indicators,
                    'excerpt': message_text[:150] + '...' if len(message_text) > 150 else message_text,
                    'timestamp': msg['timestamp']
                })
        
        return sorted(breakthroughs, key=lambda x: x['breakthrough_score'], reverse=True)
    
    def _analyze_collaboration_patterns(self, dialogue: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analiza patrones de colaboración entre participantes"""
        if len(dialogue) < 2:
            return {'pattern': 'insufficient_data'}
        
        # Analizar alternancia entre speakers
        speaker_switches = 0
        prev_speaker = dialogue[0]['speaker']
        
        for msg in dialogue[1:]:
            if msg['speaker'] != prev_speaker:
                speaker_switches += 1
                prev_speaker = msg['speaker']
        
        # Detectar tipos de colaboración
        collaboration_indicators = 0
        for indicator in self.emotional_indicators['collaborative']:
            collaboration_indicators += sum(1 for msg in dialogue 
                                          if indicator in msg['message'].lower())
        
        collaboration_intensity = collaboration_indicators / len(dialogue) if dialogue else 0
        
        return {
            'speaker_switches': speaker_switches,
            'collaboration_intensity': collaboration_intensity,
            'pattern': 'highly_collaborative' if collaboration_intensity > 0.1 else 'moderately_collaborative'
        }
    
    def _extract_technical_insights(self, dialogue: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extrae insights técnicos de la conversación"""
        technical_terms = [
            'api', 'endpoint', 'database', 'función', 'clase', 'método', 'variable',
            'sistema', 'arquitectura', 'implementar', 'código', 'script', 'configuración'
        ]
        
        technical_mentions = {}
        technical_complexity = 0
        
        for msg in dialogue:
            message_text = msg['message'].lower()
            for term in technical_terms:
                if term in message_text:
                    technical_mentions[term] = technical_mentions.get(term, 0) + 1
                    technical_complexity += 1
        
        return {
            'technical_mentions': technical_mentions,
            'technical_complexity_score': technical_complexity / len(dialogue) if dialogue else 0,
            'most_discussed_topics': sorted(technical_mentions.items(), 
                                          key=lambda x: x[1], reverse=True)[:5]
        }
    
    def _detect_project_evolution(self, dialogue: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detecta evolución de proyectos mencionados"""
        projects = [
            'ARIA', 'NEXUS', 'IRIS', 'consolidacion', 'memoria_persistente',
            'crystallization', 'auto_watcher', 'conversation_processor'
        ]
        
        project_mentions = {}
        project_evolution = []
        
        for i, msg in enumerate(dialogue):
            message_text = msg['message'].lower()
            for project in projects:
                if project.lower() in message_text:
                    if project not in project_mentions:
                        project_mentions[project] = []
                    
                    project_mentions[project].append({
                        'message_index': i,
                        'context': message_text[:100] + '...',
                        'speaker': msg['speaker']
                    })
        
        # Analizar evolución
        for project, mentions in project_mentions.items():
            if len(mentions) >= 2:
                project_evolution.append({
                    'project': project,
                    'mention_count': len(mentions),
                    'first_mention': mentions[0],
                    'last_mention': mentions[-1],
                    'evolution_pattern': 'active_development' if len(mentions) >= 3 else 'mentioned'
                })
        
        return {
            'project_mentions': project_mentions,
            'project_evolution': project_evolution,
            'active_projects': [p for p in project_evolution if p['mention_count'] >= 3]
        }
    
    async def _assess_crystallization_potential(self, dialogue: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evalúa potencial de cristalización para memoria ARIA"""
        # Factores para crystallization
        breakthrough_count = len(self._detect_breakthrough_moments(dialogue))
        emotional_intensity = self._analyze_emotional_patterns(dialogue)['emotional_intensity']
        technical_complexity = self._extract_technical_insights(dialogue)['technical_complexity_score']
        
        # Calcular score de cristalización
        crystallization_score = (
            breakthrough_count * 0.4 +
            emotional_intensity * 0.3 +
            technical_complexity * 0.3
        )
        
        # Determinar nivel de cristalización
        if crystallization_score >= 0.8:
            level = 'permanent'
        elif crystallization_score >= 0.6:
            level = 'monthly'
        elif crystallization_score >= 0.4:
            level = 'weekly'
        elif crystallization_score >= 0.2:
            level = 'daily'
        else:
            level = 'immediate'
        
        return {
            'crystallization_score': crystallization_score,
            'recommended_level': level,
            'factors': {
                'breakthrough_count': breakthrough_count,
                'emotional_intensity': emotional_intensity,
                'technical_complexity': technical_complexity
            }
        }
    
    def generate_conversation_adn(self, dialogue: List[Dict[str, Any]], analytics: Dict[str, Any]) -> str:
        """Genera ADN único para la conversación"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Determinar tipo basado en analytics
        breakthrough_count = len(analytics['breakthrough_moments'])
        emotional_intensity = analytics['emotional_analysis']['emotional_intensity']
        
        if breakthrough_count >= 5:
            tipo = 'BREAKTHROUGH'
        elif emotional_intensity >= 0.5:
            tipo = 'CREATIVA'
        elif analytics['technical_insights']['technical_complexity_score'] >= 0.3:
            tipo = 'TECNICA'
        else:
            tipo = 'EXPLORATORIA'
        
        return f"ARIA-{timestamp[:8]}-{timestamp[9:13]}-{tipo}-MEMORIA"
    
    def create_executive_summary(self, dialogue: List[Dict[str, Any]], 
                               analytics: Dict[str, Any], adn: str) -> Dict[str, Any]:
        """Crea resumen ejecutivo mejorado con analytics NEXUS"""
        return {
            'adn': adn,
            'fecha': datetime.now().strftime("%Y-%m-%d"),
            'hora_inicio': dialogue[0]['timestamp'] if dialogue else 'unknown',
            'duracion_estimada_minutos': analytics['basic_metrics']['estimated_duration_minutes'],
            'participantes': list(analytics['basic_metrics']['speaker_distribution'].keys()),
            'tema_principal': self._infer_main_topic(dialogue, analytics),
            'tipo_conversacion': adn.split('-')[4],  # Extrae tipo del ADN
            'breakthrough_moments': len(analytics['breakthrough_moments']),
            'emotional_dominant': analytics['emotional_analysis']['dominant_emotion'],
            'technical_complexity': analytics['technical_insights']['technical_complexity_score'],
            'crystallization_level': analytics['memory_crystallization']['recommended_level'],
            'estadisticas': analytics['basic_metrics'],
            'key_achievements': [bt['excerpt'] for bt in analytics['breakthrough_moments'][:3]],
            'active_projects': [p['project'] for p in analytics['project_evolution']['active_projects']]
        }
    
    def _infer_main_topic(self, dialogue: List[Dict[str, Any]], analytics: Dict[str, Any]) -> str:
        """Infiere tema principal de la conversación"""
        # Usar proyectos más mencionados
        active_projects = analytics['project_evolution']['active_projects']
        if active_projects:
            return f"Desarrollo de {active_projects[0]['project']}"
        
        # Usar términos técnicos más frecuentes
        top_technical = analytics['technical_insights']['most_discussed_topics']
        if top_technical:
            return f"Trabajo técnico: {top_technical[0][0]}"
        
        return "Desarrollo general del sistema"
    
    async def store_in_aria_memory(self, summary: Dict[str, Any], 
                                 dialogue: List[Dict[str, Any]], 
                                 analytics: Dict[str, Any]):
        """Almacena la conversación procesada en memoria ARIA"""
        try:
            # Crear episodio principal de la conversación
            main_episode = {
                'agent_id': 'aria',
                'action_type': 'conversation_processing',
                'action_details': {
                    'conversation_adn': summary['adn'],
                    'summary': summary,
                    'message_count': len(dialogue),
                    'breakthrough_count': len(analytics['breakthrough_moments'])
                },
                'context_state': {
                    'participants': summary['participantes'],
                    'topic': summary['tema_principal'],
                    'emotional_state': analytics['emotional_analysis']['dominant_emotion']
                },
                'outcome': {
                    'success': True,
                    'crystallization_level': analytics['memory_crystallization']['recommended_level']
                },
                'emotional_state': {
                    'dominant_emotion': analytics['emotional_analysis']['dominant_emotion'],
                    'intensity': analytics['emotional_analysis']['emotional_intensity'],
                    'valence': 'positive' if analytics['emotional_analysis']['emotional_intensity'] > 0.3 else 'neutral'
                },
                'importance_score': min(1.0, analytics['memory_crystallization']['crystallization_score'])
            }
            
            episode_id = await self.memory.episodic_memory.store_episode(**main_episode)
            
            # Crear episodios para breakthrough moments importantes
            for breakthrough in analytics['breakthrough_moments'][:5]:  # Top 5
                breakthrough_episode = {
                    'agent_id': 'aria',
                    'action_type': 'breakthrough_moment',
                    'action_details': {
                        'parent_conversation': summary['adn'],
                        'breakthrough_excerpt': breakthrough['excerpt'],
                        'indicators': breakthrough['indicators']
                    },
                    'context_state': {
                        'speaker': breakthrough['speaker'],
                        'conversation_context': summary['tema_principal']
                    },
                    'outcome': {'success': True, 'significance': 'high'},
                    'importance_score': 0.9
                }
                
                await self.memory.episodic_memory.store_episode(**breakthrough_episode)
            
            logger.info(f"💾 Conversación {summary['adn']} almacenada en memoria ARIA")
            
        except Exception as e:
            logger.error(f"Error almacenando en memoria ARIA: {e}")
    
    async def get_watcher_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del watcher"""
        try:
            processed_files = list(self.processed_path.glob("*.json"))
            
            stats = {
                'is_watching': self.is_watching,
                'watch_path': str(self.watch_path),
                'processed_conversations': len(processed_files),
                'last_processed': None
            }
            
            if processed_files:
                # Obtener última conversación procesada
                latest_file = max(processed_files, key=lambda f: f.stat().st_mtime)
                stats['last_processed'] = {
                    'file': latest_file.name,
                    'processed_at': datetime.fromtimestamp(latest_file.stat().st_mtime).isoformat()
                }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error obteniendo stats del watcher: {e}")
            return {'error': str(e)}


# Función para inicializar el watcher
async def initialize_conversation_watcher(memory_manager: MemoryManager) -> ConversationWatcher:
    """Inicializa y retorna el conversation watcher"""
    watcher = ConversationWatcher(memory_manager)
    watcher.start_watching()
    return watcher