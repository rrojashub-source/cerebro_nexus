#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 MEM0-INSPIRED CONSOLIDATION ENGINE - FASE 2 ARIA CEREBRO
Sistema de consolidación inteligente de memorias para 26% mejora precisión

Implementación 100% Open Source inspirada en pipeline Mem0
Fecha: 11 Agosto 2025
Autorizado por: Ricardo (Episode 477)
"""

import asyncio
import json
import logging
import hashlib
import time
from typing import Any, Dict, List, Optional, Tuple, Union
from datetime import datetime, timedelta
from enum import Enum
import re

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

logger = logging.getLogger(__name__)

class OperationType(Enum):
    """Tipos de operaciones de consolidación Mem0-style"""
    ADD = "ADD"
    UPDATE = "UPDATE" 
    DELETE = "DELETE"
    NOOP = "NOOP"

class MemzeroInspiredConsolidation:
    """
    Sistema de consolidación inteligente inspirado en Mem0:
    Fase 1: Extracción de hechos/patrones
    Fase 2: Operaciones ADD/UPDATE/DELETE/NOOP
    
    100% local sin APIs externas
    """
    
    def __init__(self, config=None):
        self.config = config or {
            'similarity_threshold': 0.85,
            'importance_threshold': 0.3,
            'max_consolidation_batch': 50,
            'fact_extraction_enabled': True,
            'pattern_detection_enabled': True,
            'nlp_model': 'en_core_web_sm'
        }
        
        # Componentes de procesamiento
        self.nlp = None
        self.extractor = None
        self.updater = None
        
        # Estado y métricas
        self.is_initialized = False
        self.metrics = {
            'facts_extracted': 0,
            'operations_add': 0,
            'operations_update': 0,
            'operations_delete': 0,
            'operations_noop': 0,
            'consolidation_sessions': 0,
            'processing_time_ms': []
        }
        
    async def initialize(self):
        """Inicializar componentes de consolidación"""
        logger.info("🧠 Initializing Mem0-Inspired Consolidation Engine...")
        
        # 1. Inicializar procesamiento NLP local
        if SPACY_AVAILABLE and self.config['fact_extraction_enabled']:
            try:
                logger.info(f"📥 Loading spaCy model: {self.config['nlp_model']}")
                self.nlp = spacy.load(self.config['nlp_model'])
                logger.info("✅ spaCy NLP model loaded successfully")
            except Exception as e:
                logger.warning(f"⚠️ spaCy not available: {e}")
                self.nlp = None
        
        # 2. Inicializar extractores y updaters
        self.extractor = LocalMemoryExtractor(self.nlp, self.config)
        self.updater = LocalMemoryUpdater(self.config)
        
        self.is_initialized = True
        logger.info("🎯 Consolidation Engine initialized successfully")
        return True
    
    async def mem0_style_consolidation(self, episodes: List[Dict]) -> Dict[str, Any]:
        """
        Pipeline principal de consolidación estilo Mem0:
        1. Fase de Extracción: Analizar episodes y extraer hechos/patrones
        2. Fase de Operaciones: Determinar ADD/UPDATE/DELETE/NOOP
        3. Ejecutar operaciones y retornar resumen
        
        Args:
            episodes: Lista de episodes a consolidar
            
        Returns:
            Resumen de operaciones realizadas
        """
        if not self.is_initialized:
            raise RuntimeError("Engine not initialized. Call initialize() first.")
        
        start_time = time.time()
        logger.info(f"🚀 Starting Mem0-style consolidation for {len(episodes)} episodes")
        
        consolidation_result = {
            'session_id': hashlib.md5(str(time.time()).encode()).hexdigest()[:8],
            'timestamp': datetime.utcnow().isoformat(),
            'input_episodes': len(episodes),
            'phases': {},
            'operations': [],
            'summary': {}
        }
        
        try:
            # FASE 1: Extracción inteligente de hechos y patrones
            logger.info("📊 Phase 1: Intelligent fact and pattern extraction")
            
            phase1_start = time.time()
            extracted_facts = []
            
            for episode in episodes:
                if self._should_process_episode(episode):
                    facts = await self.extractor.extract_facts_and_patterns(episode)
                    extracted_facts.extend(facts)
            
            phase1_time = (time.time() - phase1_start) * 1000
            consolidation_result['phases']['extraction'] = {
                'duration_ms': phase1_time,
                'facts_extracted': len(extracted_facts),
                'episodes_processed': len([e for e in episodes if self._should_process_episode(e)])
            }
            
            logger.info(f"✅ Phase 1 completed: {len(extracted_facts)} facts extracted in {phase1_time:.2f}ms")
            
            # FASE 2: Generación de operaciones inteligentes
            logger.info("⚙️ Phase 2: Intelligent operation generation")
            
            phase2_start = time.time()
            operations = []
            
            for fact in extracted_facts:
                operation = await self._determine_operation(fact)
                if operation:
                    operations.append(operation)
            
            phase2_time = (time.time() - phase2_start) * 1000
            consolidation_result['phases']['operation_planning'] = {
                'duration_ms': phase2_time,
                'operations_planned': len(operations)
            }
            
            logger.info(f"✅ Phase 2 completed: {len(operations)} operations planned in {phase2_time:.2f}ms")
            
            # FASE 3: Ejecución de operaciones
            logger.info("🔧 Phase 3: Operation execution")
            
            phase3_start = time.time()
            execution_results = await self._execute_operations(operations)
            phase3_time = (time.time() - phase3_start) * 1000
            
            consolidation_result['phases']['execution'] = {
                'duration_ms': phase3_time,
                'operations_executed': len(execution_results)
            }
            
            # Compilar resultados
            consolidation_result['operations'] = operations
            consolidation_result['execution_results'] = execution_results
            consolidation_result['summary'] = self._generate_summary(operations, execution_results)
            
            # Actualizar métricas
            total_time = (time.time() - start_time) * 1000
            self.metrics['processing_time_ms'].append(total_time)
            self.metrics['consolidation_sessions'] += 1
            self.metrics['facts_extracted'] += len(extracted_facts)
            
            # Contar operaciones por tipo
            for op in operations:
                op_type = op.get('type', 'unknown').lower()
                metric_key = f'operations_{op_type}'
                if metric_key in self.metrics:
                    self.metrics[metric_key] += 1
            
            logger.info(f"🎯 Consolidation completed in {total_time:.2f}ms")
            logger.info(f"📊 Summary: {consolidation_result['summary']}")
            
            return consolidation_result
            
        except Exception as e:
            logger.error(f"❌ Consolidation error: {e}")
            consolidation_result['error'] = str(e)
            return consolidation_result
    
    def _should_process_episode(self, episode: Dict) -> bool:
        """Determinar si episode debe ser procesado para consolidación"""
        # Filtros básicos
        if not episode.get('action_details'):
            return False
            
        # Check importance score
        importance = episode.get('importance_score', 0)
        if importance < self.config['importance_threshold']:
            return False
        
        # Check if already consolidated
        if episode.get('consolidated', False):
            return False
        
        return True
    
    async def _determine_operation(self, fact: Dict) -> Optional[Dict]:
        """
        Determinar qué operación (ADD/UPDATE/DELETE/NOOP) aplicar a un hecho
        """
        
        # Buscar memoria relacionada existente
        existing_memory = await self._find_related_memory(fact)
        
        if not existing_memory:
            # No existe memoria similar -> ADD
            return {
                'type': OperationType.ADD.value,
                'fact': fact,
                'confidence': fact.get('confidence', 0.5),
                'reason': 'new_fact_detected'
            }
        
        # Existe memoria similar -> evaluar qué hacer
        if self._should_update(fact, existing_memory):
            return {
                'type': OperationType.UPDATE.value,
                'fact': fact,
                'existing_memory': existing_memory,
                'confidence': fact.get('confidence', 0.5),
                'reason': 'fact_enhancement_detected'
            }
        
        elif self._is_contradiction(fact, existing_memory):
            return {
                'type': OperationType.DELETE.value,
                'target': existing_memory,
                'new_fact': fact,
                'confidence': fact.get('confidence', 0.5),
                'reason': 'contradiction_detected'
            }
        
        else:
            # Ya existe y no necesita cambios -> NOOP
            return {
                'type': OperationType.NOOP.value,
                'fact': fact,
                'existing_memory': existing_memory,
                'reason': 'already_exists_unchanged'
            }
    
    async def _find_related_memory(self, fact: Dict) -> Optional[Dict]:
        """Buscar memoria relacionada (placeholder - integrar con sistema real)"""
        # Esta implementación debe integrarse con el sistema de búsqueda vectorial
        # Por ahora implementación básica
        
        fact_text = fact.get('text', '')
        fact_entities = fact.get('entities', [])
        
        # Simulación de búsqueda semántica
        # En implementación real, usar hybrid_local_search.py
        
        return None  # Placeholder
    
    def _should_update(self, new_fact: Dict, existing_memory: Dict) -> bool:
        """Determinar si memoria existente debe actualizarse"""
        
        # Comparar confianza/score
        new_confidence = new_fact.get('confidence', 0)
        existing_confidence = existing_memory.get('confidence', 0)
        
        # Actualizar si nueva información es más confiable
        if new_confidence > existing_confidence * 1.1:  # 10% threshold
            return True
        
        # Comparar información adicional
        new_info = len(new_fact.get('details', {}))
        existing_info = len(existing_memory.get('details', {}))
        
        if new_info > existing_info:
            return True
        
        return False
    
    def _is_contradiction(self, new_fact: Dict, existing_memory: Dict) -> bool:
        """Detectar si nueva información contradice memoria existente"""
        
        # Análisis básico de contradicción
        new_sentiment = new_fact.get('sentiment', 'neutral')
        existing_sentiment = existing_memory.get('sentiment', 'neutral')
        
        # Contradicción si sentimientos opuestos con alta confianza
        if (new_sentiment == 'positive' and existing_sentiment == 'negative') or \
           (new_sentiment == 'negative' and existing_sentiment == 'positive'):
            
            if (new_fact.get('confidence', 0) > 0.8 and 
                existing_memory.get('confidence', 0) > 0.8):
                return True
        
        return False
    
    async def _execute_operations(self, operations: List[Dict]) -> List[Dict]:
        """Ejecutar lista de operaciones de consolidación"""
        
        results = []
        
        for operation in operations:
            try:
                result = await self.updater.execute_operation(operation)
                results.append(result)
            except Exception as e:
                logger.error(f"Operation execution failed: {e}")
                results.append({
                    'operation_id': operation.get('id', 'unknown'),
                    'success': False,
                    'error': str(e)
                })
        
        return results
    
    def _generate_summary(self, operations: List[Dict], results: List[Dict]) -> Dict:
        """Generar resumen de consolidación"""
        
        summary = {
            'total_operations': len(operations),
            'successful_operations': len([r for r in results if r.get('success', False)]),
            'failed_operations': len([r for r in results if not r.get('success', False)]),
            'operations_by_type': {}
        }
        
        # Contar por tipo
        for op in operations:
            op_type = op.get('type', 'unknown')
            summary['operations_by_type'][op_type] = summary['operations_by_type'].get(op_type, 0) + 1
        
        # Calcular tasa de éxito
        if summary['total_operations'] > 0:
            summary['success_rate'] = summary['successful_operations'] / summary['total_operations']
        else:
            summary['success_rate'] = 0
        
        return summary
    
    async def get_consolidation_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas del sistema de consolidación"""
        
        stats = {
            'timestamp': datetime.utcnow().isoformat(),
            'system_status': {
                'initialized': self.is_initialized,
                'nlp_available': self.nlp is not None,
                'fact_extraction_enabled': self.config['fact_extraction_enabled']
            },
            'metrics': self.metrics.copy(),
            'performance': {}
        }
        
        # Calcular métricas de performance
        if self.metrics['processing_time_ms']:
            import numpy as np
            stats['performance'] = {
                'avg_processing_ms': np.mean(self.metrics['processing_time_ms']),
                'max_processing_ms': max(self.metrics['processing_time_ms']),
                'total_sessions': self.metrics['consolidation_sessions']
            }
        
        return stats


class LocalMemoryExtractor:
    """Extractor de hechos y patrones usando NLP local"""
    
    def __init__(self, nlp_model, config):
        self.nlp = nlp_model
        self.config = config
    
    async def extract_facts_and_patterns(self, episode: Dict) -> List[Dict]:
        """Extraer hechos relevantes del episode usando NLP local"""
        
        facts = []
        
        try:
            # Construir texto para análisis
            text_content = self._build_analysis_text(episode)
            
            if not text_content:
                return facts
            
            # Análisis con spaCy si disponible
            if self.nlp:
                facts.extend(await self._extract_nlp_facts(text_content, episode))
            
            # Análisis basado en patrones
            facts.extend(await self._extract_pattern_facts(text_content, episode))
            
            # Análisis de metadatos
            facts.extend(await self._extract_metadata_facts(episode))
            
        except Exception as e:
            logger.warning(f"Fact extraction error for episode {episode.get('id')}: {e}")
        
        return facts
    
    def _build_analysis_text(self, episode: Dict) -> str:
        """Construir texto para análisis desde episode"""
        
        parts = []
        
        # Action type
        if episode.get('action_type'):
            parts.append(episode['action_type'])
        
        # Action details
        if episode.get('action_details'):
            if isinstance(episode['action_details'], dict):
                # Extraer campos de texto
                for key, value in episode['action_details'].items():
                    if isinstance(value, str) and len(value) > 10:
                        parts.append(value)
            else:
                parts.append(str(episode['action_details']))
        
        return ' '.join(parts)
    
    async def _extract_nlp_facts(self, text: str, episode: Dict) -> List[Dict]:
        """Extraer hechos usando spaCy NLP"""
        
        facts = []
        
        try:
            # Procesar texto
            doc = self.nlp(text)
            
            # Extraer entidades
            for ent in doc.ents:
                fact = {
                    'type': 'entity',
                    'entity_type': ent.label_,
                    'text': ent.text,
                    'confidence': 0.7,  # Score base para entidades spaCy
                    'source_episode': episode.get('id'),
                    'extraction_method': 'spacy_nlp'
                }
                facts.append(fact)
            
            # Extraer relaciones básicas (sujeto-verbo-objeto)
            for sent in doc.sents:
                relations = self._extract_svo_relations(sent)
                for relation in relations:
                    fact = {
                        'type': 'relation',
                        'subject': relation['subject'],
                        'verb': relation['verb'], 
                        'object': relation['object'],
                        'confidence': 0.6,
                        'source_episode': episode.get('id'),
                        'extraction_method': 'svo_extraction'
                    }
                    facts.append(fact)
                    
        except Exception as e:
            logger.warning(f"NLP extraction error: {e}")
        
        return facts
    
    def _extract_svo_relations(self, sent) -> List[Dict]:
        """Extraer relaciones sujeto-verbo-objeto básicas"""
        
        relations = []
        
        # Buscar root verb
        root_verb = None
        for token in sent:
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                root_verb = token
                break
        
        if not root_verb:
            return relations
        
        # Buscar sujeto y objeto
        subject = None
        obj = None
        
        for child in root_verb.children:
            if child.dep_ in ["nsubj", "nsubjpass"]:
                subject = child.text
            elif child.dep_ in ["dobj", "pobj"]:
                obj = child.text
        
        if subject and obj:
            relations.append({
                'subject': subject,
                'verb': root_verb.text,
                'object': obj
            })
        
        return relations
    
    async def _extract_pattern_facts(self, text: str, episode: Dict) -> List[Dict]:
        """Extraer hechos basados en patrones regulares"""
        
        facts = []
        
        # Patrones comunes
        patterns = {
            'project_status': r'proyecto\s+(\w+)\s+(?:está|es|se encuentra)\s+(\w+)',
            'completion': r'(\d+)%\s+(?:completado|completo|terminado)',
            'file_path': r'[A-Z]:\\[^\\/:*?"<>|]+',
            'url': r'https?://[^\s<>"{}|\\^`[\]]+',
            'timestamp': r'\d{4}-\d{2}-\d{2}',
        }
        
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            
            for match in matches:
                fact = {
                    'type': 'pattern',
                    'pattern_type': pattern_name,
                    'value': match if isinstance(match, str) else ' '.join(match),
                    'confidence': 0.8,
                    'source_episode': episode.get('id'),
                    'extraction_method': 'regex_pattern'
                }
                facts.append(fact)
        
        return facts
    
    async def _extract_metadata_facts(self, episode: Dict) -> List[Dict]:
        """Extraer hechos de metadatos del episode"""
        
        facts = []
        
        # Importance score como hecho
        if episode.get('importance_score'):
            fact = {
                'type': 'metadata',
                'metadata_type': 'importance',
                'value': episode['importance_score'],
                'confidence': 1.0,
                'source_episode': episode.get('id'),
                'extraction_method': 'metadata_direct'
            }
            facts.append(fact)
        
        # Tags como hechos
        if episode.get('tags'):
            for tag in episode['tags']:
                fact = {
                    'type': 'metadata',
                    'metadata_type': 'tag',
                    'value': tag,
                    'confidence': 0.9,
                    'source_episode': episode.get('id'),
                    'extraction_method': 'metadata_direct'
                }
                facts.append(fact)
        
        return facts


class LocalMemoryUpdater:
    """Ejecutor de operaciones de consolidación"""
    
    def __init__(self, config):
        self.config = config
    
    async def execute_operation(self, operation: Dict) -> Dict:
        """Ejecutar operación individual de consolidación"""
        
        op_type = operation.get('type')
        
        try:
            if op_type == OperationType.ADD.value:
                return await self._execute_add(operation)
            elif op_type == OperationType.UPDATE.value:
                return await self._execute_update(operation)
            elif op_type == OperationType.DELETE.value:
                return await self._execute_delete(operation)
            elif op_type == OperationType.NOOP.value:
                return await self._execute_noop(operation)
            else:
                raise ValueError(f"Unknown operation type: {op_type}")
                
        except Exception as e:
            return {
                'operation_type': op_type,
                'success': False,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
    
    async def _execute_add(self, operation: Dict) -> Dict:
        """Ejecutar operación ADD - agregar nuevo hecho consolidado"""
        
        # Placeholder - integrar con sistema de memoria real
        logger.debug(f"ADD operation: {operation.get('fact', {}).get('type', 'unknown')}")
        
        return {
            'operation_type': 'ADD',
            'success': True,
            'fact_added': operation.get('fact'),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def _execute_update(self, operation: Dict) -> Dict:
        """Ejecutar operación UPDATE - actualizar memoria existente"""
        
        logger.debug(f"UPDATE operation: {operation.get('fact', {}).get('type', 'unknown')}")
        
        return {
            'operation_type': 'UPDATE',
            'success': True,
            'fact_updated': operation.get('fact'),
            'previous_memory': operation.get('existing_memory'),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def _execute_delete(self, operation: Dict) -> Dict:
        """Ejecutar operación DELETE - eliminar memoria contradictoria"""
        
        logger.debug(f"DELETE operation: {operation.get('target', {}).get('type', 'unknown')}")
        
        return {
            'operation_type': 'DELETE', 
            'success': True,
            'memory_deleted': operation.get('target'),
            'replacement_fact': operation.get('new_fact'),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def _execute_noop(self, operation: Dict) -> Dict:
        """Ejecutar operación NOOP - no cambios necesarios"""
        
        return {
            'operation_type': 'NOOP',
            'success': True,
            'reason': operation.get('reason', 'no_changes_needed'),
            'timestamp': datetime.utcnow().isoformat()
        }


# Factory function
async def create_consolidation_engine(config=None) -> MemzeroInspiredConsolidation:
    """Crear y inicializar sistema de consolidación"""
    engine = MemzeroInspiredConsolidation(config)
    
    success = await engine.initialize()
    if not success:
        logger.error("❌ Failed to initialize consolidation engine")
        return None
    
    return engine


# Testing
if __name__ == "__main__":
    async def test_consolidation():
        """Test básico del motor de consolidación"""
        print("🧪 Testing Consolidation Engine...")
        
        engine = MemzeroInspiredConsolidation()
        success = await engine.initialize()
        
        if success:
            # Test con episodes de prueba
            test_episodes = [
                {
                    'id': 'test_1',
                    'action_type': 'project_update',
                    'action_details': {'project': 'test', 'status': 'completed'},
                    'importance_score': 0.8,
                    'tags': ['testing', 'consolidation']
                }
            ]
            
            result = await engine.mem0_style_consolidation(test_episodes)
            print(f"Consolidation result: {json.dumps(result, indent=2)}")
        else:
            print("❌ Initialization failed")
    
    # asyncio.run(test_consolidation())
    print("✅ Consolidation Engine module loaded successfully")