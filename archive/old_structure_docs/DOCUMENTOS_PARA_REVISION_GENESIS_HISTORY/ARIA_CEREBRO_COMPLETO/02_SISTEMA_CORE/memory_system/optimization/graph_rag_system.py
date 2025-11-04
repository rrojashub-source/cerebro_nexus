#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🕸️ GRAPH RAG SYSTEM - FASE 3 ARIA CEREBRO ELITE
Sistema completo GraphRAG local con Neo4j para reasoning contextual avanzado

Implementa:
- Entity extraction automático de episodios
- Relationship mapping inteligente  
- Graph-enhanced retrieval
- Context-aware reasoning
- Multi-hop graph traversal

Fecha: 11 Agosto 2025
Autorizado por: Ricardo (Episode 478+)
"""

import asyncio
import json
import logging
import re
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

try:
    from neo4j import AsyncGraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

logger = logging.getLogger(__name__)

class EntityType(Enum):
    """Tipos de entidades para extracción"""
    PERSON = "person"           # Personas (Ricardo, ARIA, NEXUS)
    PROJECT = "project"         # Proyectos (ARIA_MEMORIA, Genesis)
    CONCEPT = "concept"         # Conceptos técnicos (Circuit Breaker, GraphRAG)
    TECHNOLOGY = "technology"   # Tecnologías (Neo4j, PostgreSQL)
    EMOTION = "emotion"         # Estados emocionales
    ACTION = "action"          # Acciones realizadas
    OUTCOME = "outcome"        # Resultados obtenidos
    LOCATION = "location"      # Ubicaciones (paths, servers)
    TIMESTAMP = "timestamp"    # Marcas temporales importantes

class RelationshipType(Enum):
    """Tipos de relaciones en el grafo"""
    WORKED_ON = "WORKED_ON"           # Person -> Project
    COLLABORATED_WITH = "COLLABORATED_WITH"  # Person -> Person  
    IMPLEMENTED = "IMPLEMENTED"        # Person -> Technology/Concept
    RESULTED_IN = "RESULTED_IN"       # Action -> Outcome
    CAUSED_BY = "CAUSED_BY"           # Outcome -> Action
    PART_OF = "PART_OF"              # Component -> Project
    DEPENDS_ON = "DEPENDS_ON"         # Technology -> Technology
    EMOTIONAL_STATE = "EMOTIONAL_STATE" # Person -> Emotion
    OCCURRED_AT = "OCCURRED_AT"       # Action -> Timestamp
    SIMILAR_TO = "SIMILAR_TO"         # Concept -> Concept
    MENTIONED_IN = "MENTIONED_IN"     # Entity -> Episode

@dataclass
class GraphEntity:
    """Entidad extraída para el grafo"""
    id: str
    name: str
    type: EntityType
    properties: Dict[str, Any]
    confidence: float
    source_episode_id: str
    extraction_timestamp: datetime

@dataclass
class GraphRelationship:
    """Relación entre entidades del grafo"""
    id: str
    source_entity_id: str
    target_entity_id: str
    type: RelationshipType
    properties: Dict[str, Any]
    confidence: float
    source_episode_id: str
    extraction_timestamp: datetime

@dataclass
class GraphPath:
    """Path encontrado en el grafo para reasoning"""
    entities: List[GraphEntity]
    relationships: List[GraphRelationship]
    path_length: int
    relevance_score: float
    reasoning: str

class GraphRAGSystem:
    """
    Sistema GraphRAG completo para ARIA:
    - Extrae entidades y relaciones de episodios
    - Construye grafo de conocimiento en Neo4j
    - Reasoning contextual via graph traversal
    - Enhanced retrieval con context gráfico
    """
    
    def __init__(self, neo4j_uri: str = "bolt://localhost:7687", 
                 neo4j_user: str = "neo4j", neo4j_password: str = "password"):
        self.neo4j_uri = neo4j_uri
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password
        self.driver = None
        self.nlp = None
        
        # Entity extraction patterns (regex-based fallback)
        self.entity_patterns = {
            EntityType.PERSON: [
                r'\b(Ricardo|ARIA|NEXUS|Iris|Aelio|Echo|Nova)\b',
                r'\b(usuario|user|developer|programador)\b'
            ],
            EntityType.PROJECT: [
                r'\b(ARIA[_\s]MEMORIA|Genesis|Personal[_\s]AI|Bot[_\s]Matias)\b',
                r'\b(proyecto|project|sistema|system)\s+([A-Z][a-zA-Z_]+)\b'
            ],
            EntityType.TECHNOLOGY: [
                r'\b(Neo4j|PostgreSQL|Redis|ChromaDB|Qdrant|Docker|FastAPI)\b',
                r'\b(Python|JavaScript|TypeScript|SQL|Cypher)\b'
            ],
            EntityType.CONCEPT: [
                r'\b(Circuit[_\s]Breaker|GraphRAG|Semantic[_\s]Cache|Health[_\s]Check)\b',
                r'\b(memoria|memory|consolidaci[oó]n|optimization)\b'
            ]
        }
        
        # Known important entities (high confidence)
        self.known_entities = {
            "Ricardo": (EntityType.PERSON, {"role": "guardian", "type": "human"}),
            "ARIA": (EntityType.PERSON, {"role": "brain_to_brain_partner", "type": "ai"}),  
            "NEXUS": (EntityType.PERSON, {"role": "technical_implementor", "type": "ai"}),
            "PostgreSQL": (EntityType.TECHNOLOGY, {"category": "database", "criticality": "high"}),
            "Neo4j": (EntityType.TECHNOLOGY, {"category": "graph_database", "criticality": "medium"}),
            "Circuit Breaker": (EntityType.CONCEPT, {"domain": "reliability", "phase": "fase1"})
        }
        
        logger.info("🕸️ GraphRAG System initialized")
        
    async def initialize(self):
        """Inicializar sistema GraphRAG"""
        if not NEO4J_AVAILABLE:
            logger.error("❌ Neo4j driver not available")
            return False
            
        try:
            # Conectar a Neo4j
            self.driver = AsyncGraphDatabase.driver(
                self.neo4j_uri, 
                auth=(self.neo4j_user, self.neo4j_password)
            )
            
            # Verificar conexión
            async with self.driver.session() as session:
                result = await session.run("RETURN 1 as test")
                await result.single()
            
            # Inicializar spaCy si disponible
            if SPACY_AVAILABLE:
                try:
                    self.nlp = spacy.load("es_core_news_sm")
                    logger.info("✅ SpaCy Spanish model loaded")
                except OSError:
                    try:
                        self.nlp = spacy.load("en_core_web_sm") 
                        logger.info("✅ SpaCy English model loaded")
                    except OSError:
                        logger.warning("⚠️ SpaCy models not found, using regex patterns")
                        self.nlp = None
            
            # Crear constraints e índices
            await self._create_graph_schema()
            
            logger.info("✅ GraphRAG System initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error initializing GraphRAG: {e}")
            return False
    
    async def _create_graph_schema(self):
        """Crear schema y constraints del grafo"""
        async with self.driver.session() as session:
            
            # Constraints para entidades únicas
            constraints = [
                "CREATE CONSTRAINT entity_id IF NOT EXISTS FOR (e:Entity) REQUIRE e.id IS UNIQUE",
                "CREATE CONSTRAINT person_name IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE",
                "CREATE CONSTRAINT project_name IF NOT EXISTS FOR (p:Project) REQUIRE p.name IS UNIQUE"
            ]
            
            for constraint in constraints:
                try:
                    await session.run(constraint)
                except Exception as e:
                    logger.debug(f"Constraint already exists or failed: {e}")
            
            # Índices para performance
            indices = [
                "CREATE INDEX entity_type_idx IF NOT EXISTS FOR (e:Entity) ON (e.type)",
                "CREATE INDEX entity_confidence_idx IF NOT EXISTS FOR (e:Entity) ON (e.confidence)", 
                "CREATE INDEX relationship_type_idx IF NOT EXISTS FOR ()-[r:RELATIONSHIP]-() ON (r.type)",
                "CREATE INDEX episode_source_idx IF NOT EXISTS FOR (e:Entity) ON (e.source_episode_id)"
            ]
            
            for index in indices:
                try:
                    await session.run(index)
                except Exception as e:
                    logger.debug(f"Index already exists or failed: {e}")
            
            logger.info("✅ Graph schema created")
    
    async def extract_entities_and_relationships(self, episode: Dict[str, Any]) -> Tuple[List[GraphEntity], List[GraphRelationship]]:
        """
        Extraer entidades y relaciones de un episodio
        
        Args:
            episode: Episodio con action_details, context_state, etc.
            
        Returns:
            Tuple de (entidades, relaciones) extraídas
        """
        entities = []
        relationships = []
        
        episode_id = episode.get('episode_id', 'unknown')
        episode_text = self._extract_text_from_episode(episode)
        
        logger.debug(f"Extracting entities from episode {episode_id}")
        
        # Extraer entidades usando spaCy si disponible
        if self.nlp:
            entities.extend(await self._extract_entities_spacy(episode_text, episode_id))
        
        # Extraer entidades usando patrones regex (fallback + complemento)
        entities.extend(await self._extract_entities_patterns(episode_text, episode_id))
        
        # Extraer entidades contextuales específicas de ARIA
        entities.extend(await self._extract_contextual_entities(episode, episode_id))
        
        # Remover duplicados por ID
        entities = self._deduplicate_entities(entities)
        
        # Extraer relaciones entre entidades encontradas
        relationships = await self._extract_relationships(entities, episode_text, episode_id)
        
        logger.info(f"📊 Episode {episode_id}: {len(entities)} entities, {len(relationships)} relationships")
        
        return entities, relationships
    
    def _extract_text_from_episode(self, episode: Dict[str, Any]) -> str:
        """Extraer texto relevante del episodio para análisis"""
        texts = []
        
        # Action type y details
        if 'action_type' in episode:
            texts.append(episode['action_type'])
        
        if 'action_details' in episode:
            action_details = episode['action_details']
            if isinstance(action_details, dict):
                for key, value in action_details.items():
                    if isinstance(value, str):
                        texts.append(f"{key}: {value}")
                    elif isinstance(value, dict):
                        texts.append(json.dumps(value))
            elif isinstance(action_details, str):
                texts.append(action_details)
        
        # Context state
        if 'context_state' in episode:
            context = episode['context_state']
            if isinstance(context, dict):
                for key, value in context.items():
                    if isinstance(value, str):
                        texts.append(f"{key}: {value}")
        
        # Outcome
        if 'outcome' in episode:
            outcome = episode['outcome']
            if isinstance(outcome, dict):
                texts.append(json.dumps(outcome))
            elif isinstance(outcome, str):
                texts.append(outcome)
        
        return " ".join(texts)
    
    async def _extract_entities_spacy(self, text: str, episode_id: str) -> List[GraphEntity]:
        """Extracción de entidades usando spaCy NLP"""
        entities = []
        
        if not self.nlp:
            return entities
        
        doc = self.nlp(text)
        current_time = datetime.utcnow()
        
        # Extraer entidades nombradas de spaCy
        for ent in doc.ents:
            entity_type = self._map_spacy_to_entity_type(ent.label_)
            
            if entity_type:
                entity_id = f"{entity_type.value}_{ent.text.lower().replace(' ', '_')}"
                
                entities.append(GraphEntity(
                    id=entity_id,
                    name=ent.text,
                    type=entity_type,
                    properties={
                        "spacy_label": ent.label_,
                        "start_char": ent.start_char,
                        "end_char": ent.end_char,
                        "lemma": ent.lemma_
                    },
                    confidence=0.8,  # SpaCy tiene buena precisión
                    source_episode_id=episode_id,
                    extraction_timestamp=current_time
                ))
        
        return entities
    
    def _map_spacy_to_entity_type(self, spacy_label: str) -> Optional[EntityType]:
        """Mapear labels de spaCy a nuestros EntityTypes"""
        mapping = {
            "PERSON": EntityType.PERSON,
            "PER": EntityType.PERSON,
            "ORG": EntityType.PROJECT,  # Organizaciones como proyectos
            "PRODUCT": EntityType.TECHNOLOGY,
            "EVENT": EntityType.ACTION,
            "LOC": EntityType.LOCATION,
            "GPE": EntityType.LOCATION,
            "DATE": EntityType.TIMESTAMP,
            "TIME": EntityType.TIMESTAMP
        }
        
        return mapping.get(spacy_label)
    
    async def _extract_entities_patterns(self, text: str, episode_id: str) -> List[GraphEntity]:
        """Extracción de entidades usando patrones regex"""
        entities = []
        current_time = datetime.utcnow()
        
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                
                for match in matches:
                    entity_name = match.group(1) if match.groups() else match.group(0)
                    entity_id = f"{entity_type.value}_{entity_name.lower().replace(' ', '_')}"
                    
                    # Confidence mayor para entidades conocidas
                    confidence = 0.9 if entity_name in self.known_entities else 0.7
                    
                    properties = {"pattern_matched": pattern}
                    
                    # Añadir propiedades conocidas
                    if entity_name in self.known_entities:
                        known_type, known_props = self.known_entities[entity_name]
                        if known_type == entity_type:  # Solo si coincide el tipo
                            properties.update(known_props)
                            confidence = 0.95
                    
                    entities.append(GraphEntity(
                        id=entity_id,
                        name=entity_name,
                        type=entity_type,
                        properties=properties,
                        confidence=confidence,
                        source_episode_id=episode_id,
                        extraction_timestamp=current_time
                    ))
        
        return entities
    
    async def _extract_contextual_entities(self, episode: Dict[str, Any], episode_id: str) -> List[GraphEntity]:
        """Extraer entidades contextuales específicas de ARIA"""
        entities = []
        current_time = datetime.utcnow()
        
        # Entidades del contexto ARIA específico
        action_type = episode.get('action_type', '')
        
        # Si es un action_type específico, crear entidad
        if action_type:
            entities.append(GraphEntity(
                id=f"action_{action_type}",
                name=action_type,
                type=EntityType.ACTION,
                properties={"category": "system_action"},
                confidence=0.9,
                source_episode_id=episode_id,
                extraction_timestamp=current_time
            ))
        
        # Extraer estado emocional si existe
        emotional_state = episode.get('emotional_state', {})
        if emotional_state and isinstance(emotional_state, dict):
            emotion = emotional_state.get('emotion', '')
            if emotion:
                entities.append(GraphEntity(
                    id=f"emotion_{emotion}",
                    name=emotion,
                    type=EntityType.EMOTION,
                    properties={
                        "intensity": emotional_state.get('intensity', 0.5),
                        "valence": emotional_state.get('valence', 0.0)
                    },
                    confidence=0.8,
                    source_episode_id=episode_id,
                    extraction_timestamp=current_time
                ))
        
        # Extraer timestamp como entidad temporal
        timestamp_str = episode.get('timestamp', '')
        if timestamp_str:
            entities.append(GraphEntity(
                id=f"timestamp_{timestamp_str}",
                name=timestamp_str,
                type=EntityType.TIMESTAMP,
                properties={"iso_format": timestamp_str},
                confidence=1.0,
                source_episode_id=episode_id,
                extraction_timestamp=current_time
            ))
        
        return entities
    
    def _deduplicate_entities(self, entities: List[GraphEntity]) -> List[GraphEntity]:
        """Remover entidades duplicadas manteniendo la de mayor confidence"""
        seen = {}
        
        for entity in entities:
            if entity.id not in seen or entity.confidence > seen[entity.id].confidence:
                seen[entity.id] = entity
        
        return list(seen.values())
    
    async def _extract_relationships(self, entities: List[GraphEntity], 
                                   episode_text: str, episode_id: str) -> List[GraphRelationship]:
        """Extraer relaciones entre entidades basado en proximidad y contexto"""
        relationships = []
        current_time = datetime.utcnow()
        
        # Buscar relaciones basadas en co-ocurrencia y patrones
        for i, entity1 in enumerate(entities):
            for j, entity2 in enumerate(entities[i+1:], start=i+1):
                
                relationship = await self._infer_relationship(
                    entity1, entity2, episode_text, episode_id, current_time
                )
                
                if relationship:
                    relationships.append(relationship)
        
        # Añadir relación universal: todas las entidades MENTIONED_IN el episodio
        episode_entity = GraphEntity(
            id=f"episode_{episode_id}",
            name=f"Episode {episode_id}",
            type=EntityType.ACTION,  # Episodes como acciones
            properties={"type": "episode_container"},
            confidence=1.0,
            source_episode_id=episode_id,
            extraction_timestamp=current_time
        )
        
        for entity in entities:
            relationships.append(GraphRelationship(
                id=f"mentioned_{entity.id}_{episode_id}",
                source_entity_id=entity.id,
                target_entity_id=episode_entity.id,
                type=RelationshipType.MENTIONED_IN,
                properties={"episode_timestamp": episode_text},
                confidence=0.9,
                source_episode_id=episode_id,
                extraction_timestamp=current_time
            ))
        
        return relationships
    
    async def _infer_relationship(self, entity1: GraphEntity, entity2: GraphEntity, 
                                episode_text: str, episode_id: str, 
                                timestamp: datetime) -> Optional[GraphRelationship]:
        """Inferir relación entre dos entidades basado en contexto"""
        
        # Reglas de inferencia de relaciones
        rel_type = None
        confidence = 0.5
        properties = {}
        
        # Person -> Project (WORKED_ON)
        if entity1.type == EntityType.PERSON and entity2.type == EntityType.PROJECT:
            if any(word in episode_text.lower() for word in ['implementar', 'trabajar', 'desarrollar', 'crear']):
                rel_type = RelationshipType.WORKED_ON
                confidence = 0.8
                properties = {"inferred_from": "work_context"}
        
        # Person -> Person (COLLABORATED_WITH)
        elif entity1.type == EntityType.PERSON and entity2.type == EntityType.PERSON:
            if any(word in episode_text.lower() for word in ['colaborar', 'together', 'junto', 'team']):
                rel_type = RelationshipType.COLLABORATED_WITH
                confidence = 0.7
                properties = {"inferred_from": "collaboration_context"}
        
        # Action -> Outcome (RESULTED_IN)
        elif entity1.type == EntityType.ACTION and entity2.type == EntityType.OUTCOME:
            rel_type = RelationshipType.RESULTED_IN
            confidence = 0.8
            properties = {"inferred_from": "causal_sequence"}
        
        # Technology -> Technology (DEPENDS_ON)
        elif entity1.type == EntityType.TECHNOLOGY and entity2.type == EntityType.TECHNOLOGY:
            if any(word in episode_text.lower() for word in ['conectar', 'usar', 'require', 'depend']):
                rel_type = RelationshipType.DEPENDS_ON
                confidence = 0.6
                properties = {"inferred_from": "dependency_context"}
        
        # Person -> Emotion (EMOTIONAL_STATE)
        elif entity1.type == EntityType.PERSON and entity2.type == EntityType.EMOTION:
            rel_type = RelationshipType.EMOTIONAL_STATE
            confidence = 0.9
            properties = {"context": "emotional_attribution"}
        
        if rel_type:
            return GraphRelationship(
                id=f"rel_{entity1.id}_{entity2.id}_{rel_type.value}",
                source_entity_id=entity1.id,
                target_entity_id=entity2.id,
                type=rel_type,
                properties=properties,
                confidence=confidence,
                source_episode_id=episode_id,
                extraction_timestamp=timestamp
            )
        
        return None
    
    async def store_in_graph(self, entities: List[GraphEntity], relationships: List[GraphRelationship]):
        """Almacenar entidades y relaciones en Neo4j"""
        if not self.driver:
            logger.error("❌ Neo4j driver not initialized")
            return
        
        async with self.driver.session() as session:
            
            # Crear entidades
            for entity in entities:
                await self._create_entity(session, entity)
            
            # Crear relaciones
            for relationship in relationships:
                await self._create_relationship(session, relationship)
            
        logger.info(f"✅ Stored {len(entities)} entities, {len(relationships)} relationships")
    
    async def _create_entity(self, session, entity: GraphEntity):
        """Crear o actualizar entidad en Neo4j"""
        
        # Usar MERGE para evitar duplicados
        query = """
        MERGE (e:Entity {id: $id})
        SET e.name = $name,
            e.type = $type,
            e.confidence = $confidence,
            e.source_episode_id = $source_episode_id,
            e.extraction_timestamp = $extraction_timestamp,
            e.properties = $properties
        
        // Añadir label específico por tipo
        WITH e
        CALL apoc.create.addLabels(e, [$type_label]) YIELD node
        RETURN node
        """
        
        # Fallback si APOC no está disponible
        simple_query = """
        MERGE (e:Entity {id: $id})
        SET e.name = $name,
            e.type = $type,
            e.confidence = $confidence,
            e.source_episode_id = $source_episode_id,
            e.extraction_timestamp = $extraction_timestamp,
            e.properties = $properties
        RETURN e
        """
        
        try:
            await session.run(query, {
                "id": entity.id,
                "name": entity.name,
                "type": entity.type.value,
                "type_label": entity.type.value.capitalize(),
                "confidence": entity.confidence,
                "source_episode_id": entity.source_episode_id,
                "extraction_timestamp": entity.extraction_timestamp.isoformat(),
                "properties": entity.properties
            })
        except Exception:
            # Fallback sin APOC
            await session.run(simple_query, {
                "id": entity.id,
                "name": entity.name,
                "type": entity.type.value,
                "confidence": entity.confidence,
                "source_episode_id": entity.source_episode_id,
                "extraction_timestamp": entity.extraction_timestamp.isoformat(),
                "properties": entity.properties
            })
    
    async def _create_relationship(self, session, relationship: GraphRelationship):
        """Crear relación en Neo4j"""
        
        query = """
        MATCH (a:Entity {id: $source_id})
        MATCH (b:Entity {id: $target_id})
        MERGE (a)-[r:RELATIONSHIP {id: $rel_id}]->(b)
        SET r.type = $rel_type,
            r.confidence = $confidence,
            r.source_episode_id = $source_episode_id,
            r.extraction_timestamp = $extraction_timestamp,
            r.properties = $properties
        RETURN r
        """
        
        await session.run(query, {
            "source_id": relationship.source_entity_id,
            "target_id": relationship.target_entity_id,
            "rel_id": relationship.id,
            "rel_type": relationship.type.value,
            "confidence": relationship.confidence,
            "source_episode_id": relationship.source_episode_id,
            "extraction_timestamp": relationship.extraction_timestamp.isoformat(),
            "properties": relationship.properties
        })
    
    async def graph_enhanced_search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Búsqueda mejorada usando el grafo de conocimiento
        
        1. Buscar entidades relacionadas con la query
        2. Expandir usando relaciones del grafo  
        3. Ranking por relevancia y conectividad
        4. Context enhancement usando paths
        """
        if not self.driver:
            logger.warning("⚠️ Neo4j not available for graph search")
            return []
        
        logger.debug(f"Graph-enhanced search for: {query}")
        
        # Extraer entidades clave de la query
        query_entities = await self._extract_query_entities(query)
        
        if not query_entities:
            logger.debug("No entities found in query, falling back to text search")
            return []
        
        # Buscar en el grafo
        graph_results = []
        
        async with self.driver.session() as session:
            for entity_name in query_entities:
                
                # Buscar entidad y sus conexiones
                cypher_query = """
                MATCH (e:Entity)
                WHERE toLower(e.name) CONTAINS toLower($entity_name)
                
                OPTIONAL MATCH (e)-[r1:RELATIONSHIP]-(connected1:Entity)
                OPTIONAL MATCH (connected1)-[r2:RELATIONSHIP]-(connected2:Entity)
                
                RETURN e, collect(DISTINCT connected1) as direct_connections, 
                       collect(DISTINCT connected2) as indirect_connections,
                       count(DISTINCT connected1) as connectivity_score
                ORDER BY connectivity_score DESC, e.confidence DESC
                LIMIT $limit
                """
                
                result = await session.run(cypher_query, {
                    "entity_name": entity_name,
                    "limit": limit
                })
                
                async for record in result:
                    entity_data = record["e"]
                    direct_connections = record["direct_connections"]
                    indirect_connections = record["indirect_connections"] 
                    connectivity_score = record["connectivity_score"]
                    
                    # Calcular score de relevancia
                    relevance_score = self._calculate_graph_relevance(
                        entity_data, direct_connections, indirect_connections, 
                        connectivity_score, query
                    )
                    
                    graph_results.append({
                        "type": "graph_entity",
                        "entity": dict(entity_data),
                        "direct_connections": [dict(conn) for conn in direct_connections if conn],
                        "indirect_connections": [dict(conn) for conn in indirect_connections if conn],
                        "connectivity_score": connectivity_score,
                        "relevance_score": relevance_score,
                        "source": "graph_rag"
                    })
        
        # Ordenar por relevancia
        graph_results.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        logger.info(f"🕸️ Graph search returned {len(graph_results)} enhanced results")
        
        return graph_results[:limit]
    
    async def _extract_query_entities(self, query: str) -> List[str]:
        """Extraer entidades clave de la query de búsqueda"""
        entities = []
        
        # Usar spaCy si disponible
        if self.nlp:
            doc = self.nlp(query)
            entities.extend([ent.text for ent in doc.ents])
        
        # Buscar entidades conocidas
        for known_entity in self.known_entities.keys():
            if known_entity.lower() in query.lower():
                entities.append(known_entity)
        
        # Patrones regex básicos
        for patterns in self.entity_patterns.values():
            for pattern in patterns:
                matches = re.findall(pattern, query, re.IGNORECASE)
                entities.extend(matches)
        
        # Remover duplicados y filtrar
        unique_entities = list(set(entities))
        
        # Filtrar entidades muy cortas o comunes
        filtered_entities = [e for e in unique_entities if len(e) > 2 and e.lower() not in ['el', 'la', 'de', 'en', 'un', 'una']]
        
        logger.debug(f"Extracted query entities: {filtered_entities}")
        
        return filtered_entities
    
    def _calculate_graph_relevance(self, entity_data, direct_connections, 
                                 indirect_connections, connectivity_score, original_query) -> float:
        """Calcular score de relevancia para resultado del grafo"""
        
        base_confidence = entity_data.get("confidence", 0.5)
        
        # Factor de conectividad (más conexiones = más relevante)
        connectivity_factor = min(connectivity_score / 10.0, 1.0)  # Normalizar a [0,1]
        
        # Factor de similitud de nombre con query
        entity_name = entity_data.get("name", "")
        name_similarity = self._calculate_text_similarity(entity_name.lower(), original_query.lower())
        
        # Bonus por tipo de entidad importante
        important_types = ["person", "project", "technology"]
        type_bonus = 0.2 if entity_data.get("type") in important_types else 0.0
        
        # Score final combinado
        relevance_score = (
            base_confidence * 0.3 +           # 30% confidence base
            connectivity_factor * 0.3 +       # 30% conectividad  
            name_similarity * 0.3 +           # 30% similitud nombre
            type_bonus                        # 10% bonus tipo importante
        )
        
        return min(relevance_score, 1.0)
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Similitud básica entre textos usando Jaccard"""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    async def find_reasoning_paths(self, source_entity: str, target_entity: str, 
                                 max_hops: int = 3) -> List[GraphPath]:
        """
        Encontrar paths de reasoning entre dos entidades
        
        Útil para explicar conexiones complejas y reasoning contextual
        """
        if not self.driver:
            return []
        
        paths = []
        
        async with self.driver.session() as session:
            
            # Buscar paths con diferentes longitudes
            for hops in range(1, max_hops + 1):
                
                cypher_query = f"""
                MATCH path = (source:Entity)-[r:RELATIONSHIP*{hops}]-(target:Entity)
                WHERE toLower(source.name) CONTAINS toLower($source_name)
                  AND toLower(target.name) CONTAINS toLower($target_name)
                  AND source <> target
                
                WITH path, relationships(path) as rels, nodes(path) as nodes
                
                RETURN path, rels, nodes,
                       length(path) as path_length,
                       reduce(score = 0, rel in rels | score + rel.confidence) / length(rels) as avg_confidence
                       
                ORDER BY avg_confidence DESC, path_length ASC
                LIMIT 5
                """
                
                result = await session.run(cypher_query, {
                    "source_name": source_entity,
                    "target_name": target_entity
                })
                
                async for record in result:
                    path_data = record["path"]
                    relationships_data = record["rels"]  
                    nodes_data = record["nodes"]
                    path_length = record["path_length"]
                    avg_confidence = record["avg_confidence"]
                    
                    # Convertir a nuestras estructuras
                    entities = []
                    relationships = []
                    
                    for node in nodes_data:
                        entities.append(GraphEntity(
                            id=node.get("id", ""),
                            name=node.get("name", ""),
                            type=EntityType(node.get("type", "concept")),
                            properties=node.get("properties", {}),
                            confidence=node.get("confidence", 0.5),
                            source_episode_id=node.get("source_episode_id", ""),
                            extraction_timestamp=datetime.utcnow()
                        ))
                    
                    for rel in relationships_data:
                        relationships.append(GraphRelationship(
                            id=rel.get("id", ""),
                            source_entity_id="", # Se llena después
                            target_entity_id="", # Se llena después
                            type=RelationshipType(rel.get("type", "MENTIONED_IN")),
                            properties=rel.get("properties", {}),
                            confidence=rel.get("confidence", 0.5),
                            source_episode_id=rel.get("source_episode_id", ""),
                            extraction_timestamp=datetime.utcnow()
                        ))
                    
                    # Generar reasoning textual
                    reasoning = self._generate_path_reasoning(entities, relationships)
                    
                    paths.append(GraphPath(
                        entities=entities,
                        relationships=relationships,
                        path_length=path_length,
                        relevance_score=avg_confidence,
                        reasoning=reasoning
                    ))
        
        logger.info(f"🧠 Found {len(paths)} reasoning paths between '{source_entity}' and '{target_entity}'")
        
        return paths
    
    def _generate_path_reasoning(self, entities: List[GraphEntity], 
                               relationships: List[GraphRelationship]) -> str:
        """Generar explicación textual de un path de reasoning"""
        
        if len(entities) < 2:
            return "Insufficient entities for reasoning path"
        
        reasoning_parts = []
        
        for i in range(len(entities) - 1):
            source_entity = entities[i]
            target_entity = entities[i + 1]
            
            # Buscar relación correspondiente
            relationship = None
            for rel in relationships:
                if (rel.source_entity_id == source_entity.id and 
                    rel.target_entity_id == target_entity.id):
                    relationship = rel
                    break
            
            if relationship:
                rel_text = self._relationship_to_text(relationship)
                reasoning_parts.append(
                    f"{source_entity.name} {rel_text} {target_entity.name}"
                )
            else:
                reasoning_parts.append(
                    f"{source_entity.name} is connected to {target_entity.name}"
                )
        
        return " → ".join(reasoning_parts)
    
    def _relationship_to_text(self, relationship: GraphRelationship) -> str:
        """Convertir tipo de relación a texto legible"""
        text_mapping = {
            RelationshipType.WORKED_ON: "worked on",
            RelationshipType.COLLABORATED_WITH: "collaborated with",
            RelationshipType.IMPLEMENTED: "implemented",  
            RelationshipType.RESULTED_IN: "resulted in",
            RelationshipType.CAUSED_BY: "was caused by",
            RelationshipType.PART_OF: "is part of",
            RelationshipType.DEPENDS_ON: "depends on",
            RelationshipType.EMOTIONAL_STATE: "experienced emotion",
            RelationshipType.OCCURRED_AT: "occurred at",
            RelationshipType.SIMILAR_TO: "is similar to",
            RelationshipType.MENTIONED_IN: "was mentioned in"
        }
        
        return text_mapping.get(relationship.type, "is related to")
    
    async def get_graph_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas del grafo de conocimiento"""
        if not self.driver:
            return {"error": "Neo4j not available"}
        
        stats = {}
        
        async with self.driver.session() as session:
            
            # Contar entidades por tipo
            entity_counts = await session.run("""
                MATCH (e:Entity)
                RETURN e.type as entity_type, count(e) as count
                ORDER BY count DESC
            """)
            
            entity_stats = {}
            total_entities = 0
            
            async for record in entity_counts:
                entity_type = record["entity_type"]
                count = record["count"]
                entity_stats[entity_type] = count
                total_entities += count
            
            # Contar relaciones por tipo
            relationship_counts = await session.run("""
                MATCH ()-[r:RELATIONSHIP]->()
                RETURN r.type as rel_type, count(r) as count
                ORDER BY count DESC
            """)
            
            relationship_stats = {}
            total_relationships = 0
            
            async for record in relationship_counts:
                rel_type = record["rel_type"]
                count = record["count"]
                relationship_stats[rel_type] = count
                total_relationships += count
            
            # Entidades más conectadas
            most_connected = await session.run("""
                MATCH (e:Entity)-[r:RELATIONSHIP]-()
                RETURN e.name, e.type, count(r) as connections
                ORDER BY connections DESC
                LIMIT 10
            """)
            
            top_entities = []
            async for record in most_connected:
                top_entities.append({
                    "name": record["name"],
                    "type": record["type"],
                    "connections": record["connections"]
                })
            
            stats = {
                "total_entities": total_entities,
                "total_relationships": total_relationships,
                "entity_breakdown": entity_stats,
                "relationship_breakdown": relationship_stats,
                "most_connected_entities": top_entities,
                "graph_density": total_relationships / max(total_entities, 1),
                "timestamp": datetime.utcnow().isoformat()
            }
        
        logger.info(f"📊 Graph stats: {total_entities} entities, {total_relationships} relationships")
        
        return stats
    
    async def close(self):
        """Cerrar conexión a Neo4j"""
        if self.driver:
            await self.driver.close()
            logger.info("🔒 GraphRAG System closed")


# Factory function
async def create_graph_rag_system(neo4j_uri: str = "bolt://localhost:7687",
                                neo4j_user: str = "neo4j", 
                                neo4j_password: str = "password") -> GraphRAGSystem:
    """Crear y inicializar sistema GraphRAG"""
    
    system = GraphRAGSystem(neo4j_uri, neo4j_user, neo4j_password)
    
    success = await system.initialize()
    
    if not success:
        logger.warning("⚠️ GraphRAG system initialized with limited functionality")
    
    return system


# Testing
if __name__ == "__main__":
    async def test_graph_rag():
        """Test básico del sistema GraphRAG"""
        print("🧪 Testing GraphRAG System...")
        
        # Crear sistema
        graph_rag = await create_graph_rag_system()
        
        # Episodio de prueba
        test_episode = {
            "episode_id": "test_001",
            "action_type": "project_implementation", 
            "action_details": {
                "project": "ARIA Memoria Persistente",
                "technology": "Neo4j GraphRAG",
                "developer": "NEXUS",
                "collaboration": "with Ricardo"
            },
            "emotional_state": {
                "emotion": "focused",
                "intensity": 0.8
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Extraer entidades y relaciones
        entities, relationships = await graph_rag.extract_entities_and_relationships(test_episode)
        
        print(f"📊 Extracted {len(entities)} entities, {len(relationships)} relationships")
        
        for entity in entities:
            print(f"  Entity: {entity.name} ({entity.type.value}) - confidence: {entity.confidence}")
        
        for rel in relationships:
            print(f"  Relation: {rel.source_entity_id} --{rel.type.value}--> {rel.target_entity_id}")
        
        # Almacenar en grafo (si Neo4j disponible)
        try:
            await graph_rag.store_in_graph(entities, relationships)
            print("✅ Stored in Neo4j successfully")
        except Exception as e:
            print(f"⚠️ Could not store in Neo4j: {e}")
        
        # Test búsqueda
        search_results = await graph_rag.graph_enhanced_search("ARIA project NEXUS")
        print(f"🔍 Search results: {len(search_results)}")
        
        await graph_rag.close()
    
    # asyncio.run(test_graph_rag())
    print("✅ GraphRAG System module loaded successfully")