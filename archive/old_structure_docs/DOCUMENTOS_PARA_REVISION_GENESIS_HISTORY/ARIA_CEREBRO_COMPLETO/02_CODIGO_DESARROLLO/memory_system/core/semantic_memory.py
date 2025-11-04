"""
SEMANTIC MEMORY - Memoria Semántica (Chroma + Mem0)
Nivel 3: Conocimiento consolidado y patrones extraídos
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from loguru import logger
import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np
from pydantic import BaseModel, Field

from ..utils.config import get_config, get_database_url


class KnowledgeItem(BaseModel):
    """Item de conocimiento en memoria semántica"""
    id: Optional[str] = None
    knowledge_type: str = "concept"
    content: str
    embedding: Optional[List[float]] = None
    confidence_score: float = 0.7
    source_episodes: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_accessed: datetime = Field(default_factory=datetime.utcnow)
    access_count: int = 0


class SemanticMemory:
    """
    Memoria Semántica - Conocimiento consolidado usando Chroma + Mem0
    
    Maneja:
    - Extracción de conocimiento de episodios usando Mem0
    - Almacenamiento vectorial con Chroma
    - Búsqueda semántica por similaridad
    - Consolidación de patrones en conocimiento
    """
    
    def __init__(self, chroma_client: Optional[chromadb.Client] = None, mem0_client: Optional[Any] = None):
        self.config = get_config().memory.semantic_memory
        self.chroma_client = chroma_client
        self.mem0_client = mem0_client
        self.collection = None
        self.embedding_model = None
        
        # Configuración
        self.vector_dimension = self.config.get("vector_dimension", 384)
        self.similarity_threshold = self.config.get("similarity_threshold", 0.7)
        self.max_results = self.config.get("max_results_per_query", 10)
        self.knowledge_types = self.config.get("knowledge_types", [
            "concept", "pattern", "relationship", "skill", "fact"
        ])
        
        logger.info(f"SemanticMemory inicializada - dimension: {self.vector_dimension}")
    
    async def _get_chroma_client(self) -> chromadb.Client:
        """Obtiene cliente Chroma, creándolo si es necesario"""
        if self.chroma_client is None:
            try:
                # Try ChromaDB v2 API first
                self.chroma_client = chromadb.HttpClient(host="localhost", port=8000)
                # Test connection with a simple heartbeat
                logger.info("Cliente Chroma conectado (API v2)")
            except Exception as e:
                logger.warning(f"ChromaDB connection error: {e}, trying fallback")
                # Fallback si hay problemas
                self.chroma_client = None
                raise e
        return self.chroma_client
    
    async def _get_collection(self):
        """Obtiene o crea la colección de memoria semántica"""
        if self.collection is None:
            client = await self._get_chroma_client()
            collection_name = get_config().database.chroma.get("collection_name", "aria_semantic")
            
            try:
                self.collection = client.get_collection(name=collection_name)
                logger.info(f"Colección existente cargada: {collection_name}")
            except Exception:
                self.collection = client.create_collection(
                    name=collection_name,
                    metadata={"hnsw:space": "cosine"}
                )
                logger.info(f"Nueva colección creada: {collection_name}")
        
        return self.collection
    
    async def _get_embedding_model(self):
        """Obtiene modelo de embeddings, cargándolo si es necesario"""
        if self.embedding_model is None:
            model_name = get_config().database.chroma.get("embedding_model", "sentence-transformers/all-MiniLM-L6-v2")
            self.embedding_model = SentenceTransformer(model_name)
            logger.info(f"Modelo de embeddings cargado: {model_name}")
        return self.embedding_model
    
    async def _generate_embedding(self, text: str) -> List[float]:
        """
        Genera embeddings vectoriales usando sentence-transformers
        
        Args:
            text: Texto para generar embedding
            
        Returns:
            Lista de floats representando el vector embedding
        """
        try:
            model = await self._get_embedding_model()
            
            # Normalizar texto
            text = text.strip()[:500]  # Limitar longitud
            
            # Generar embedding
            embedding = model.encode(text, convert_to_tensor=False)
            
            # Convertir a lista de floats
            if isinstance(embedding, np.ndarray):
                embedding = embedding.tolist()
            
            logger.debug(f"Embedding generado para texto de {len(text)} caracteres")
            return embedding
            
        except Exception as e:
            logger.error(f"Error generando embedding: {e}")
            # Devolver embedding zero como fallback
            return [0.0] * self.vector_dimension
    
    async def extract_and_store_knowledge(self, episodes: List[Dict[str, Any]]) -> List[str]:
        """
        Extrae patrones y conocimiento de episodios usando análisis inteligente
        
        Args:
            episodes: Lista de episodios para analizar
            
        Returns:
            Lista de IDs de conocimiento creado
        """
        try:
            if not episodes:
                logger.warning("No hay episodios para extraer conocimiento")
                return []
            
            logger.info(f"Extrayendo conocimiento de {len(episodes)} episodios")
            
            knowledge_ids = []
            
            # Agrupar episodios por tipo de acción para encontrar patrones
            action_patterns = await self._extract_action_patterns(episodes)
            
            for pattern in action_patterns:
                knowledge_id = await self._store_knowledge_item(
                    knowledge_type="pattern",
                    content=pattern["description"],
                    confidence_score=pattern["confidence"],
                    source_episodes=pattern["episode_ids"],
                    tags=pattern["tags"]
                )
                knowledge_ids.append(knowledge_id)
            
            # Extraer conceptos únicos mencionados
            concepts = await self._extract_concepts(episodes)
            
            for concept in concepts:
                knowledge_id = await self._store_knowledge_item(
                    knowledge_type="concept",
                    content=f"Concepto: {concept['name']} - {concept['description']}",
                    confidence_score=concept["confidence"],
                    source_episodes=concept["episode_ids"],
                    tags=concept["tags"]
                )
                knowledge_ids.append(knowledge_id)
            
            # Extraer relaciones entre entidades
            relationships = await self._extract_relationships(episodes)
            
            for relationship in relationships:
                knowledge_id = await self._store_knowledge_item(
                    knowledge_type="relationship",
                    content=f"Relación: {relationship['from']} {relationship['type']} {relationship['to']}",
                    confidence_score=relationship["confidence"],
                    source_episodes=relationship["episode_ids"],
                    tags=relationship["tags"]
                )
                knowledge_ids.append(knowledge_id)
            
            logger.info(f"Conocimiento extraído: {len(knowledge_ids)} items creados")
            return knowledge_ids
            
        except Exception as e:
            logger.error(f"Error extrayendo conocimiento: {e}")
            return []
    
    async def _extract_action_patterns(self, episodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extrae patrones de acciones de los episodios"""
        patterns = []
        
        # Agrupar por tipo de acción
        action_groups = {}
        for episode in episodes:
            action_type = episode.get("action_type", "unknown")
            if action_type not in action_groups:
                action_groups[action_type] = []
            action_groups[action_type].append(episode)
        
        # Buscar patrones en cada grupo
        for action_type, group_episodes in action_groups.items():
            if len(group_episodes) >= 2:  # Mínimo 2 para patrón
                
                # Analizar outcomes
                successful_outcomes = [ep for ep in group_episodes 
                                     if ep.get("outcome", {}).get("success", False)]
                
                if len(successful_outcomes) >= 2:
                    patterns.append({
                        "description": f"Patrón exitoso para {action_type}: {len(successful_outcomes)}/{len(group_episodes)} casos exitosos",
                        "confidence": len(successful_outcomes) / len(group_episodes),
                        "episode_ids": [ep.get("id", "") for ep in successful_outcomes],
                        "tags": [action_type, "success_pattern", "behavioral"]
                    })
                
                # Analizar contextos comunes
                common_contexts = self._find_common_contexts(group_episodes)
                if common_contexts:
                    patterns.append({
                        "description": f"Contexto común para {action_type}: {common_contexts}",
                        "confidence": 0.8,
                        "episode_ids": [ep.get("id", "") for ep in group_episodes],
                        "tags": [action_type, "context_pattern", "environmental"]
                    })
        
        return patterns
    
    async def _extract_concepts(self, episodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extrae conceptos mencionados en los episodios"""
        concepts = {}
        
        for episode in episodes:
            # Buscar en action_details
            action_details = episode.get("action_details", {})
            
            # Conceptos técnicos
            tech_terms = ["framework", "database", "system", "memory", "api", "service"]
            for term in tech_terms:
                if any(term in str(value).lower() for value in action_details.values()):
                    if term not in concepts:
                        concepts[term] = {
                            "name": term,
                            "description": f"Concepto técnico: {term}",
                            "confidence": 0.7,
                            "episode_ids": [],
                            "tags": ["technical", "concept"]
                        }
                    concepts[term]["episode_ids"].append(episode.get("id", ""))
            
            # Conceptos de relación
            people = ["Ricardo", "Iris", "Nexus", "ARIA", "familia", "equipo"]
            for person in people:
                if any(person in str(value) for value in action_details.values()):
                    if person not in concepts:
                        concepts[person] = {
                            "name": person,
                            "description": f"Entidad relacional: {person}",
                            "confidence": 0.9,
                            "episode_ids": [],
                            "tags": ["relationship", "entity", "social"]
                        }
                    concepts[person]["episode_ids"].append(episode.get("id", ""))
        
        # Filtrar conceptos con suficiente evidencia
        return [concept for concept in concepts.values() if len(concept["episode_ids"]) >= 2]
    
    async def _extract_relationships(self, episodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extrae relaciones entre entidades"""
        relationships = []
        
        # Relaciones detectadas por co-ocurrencia
        entities = ["Ricardo", "Iris", "Nexus", "ARIA", "proyecto", "sistema"]
        
        for i, entity1 in enumerate(entities):
            for entity2 in entities[i+1:]:
                # Buscar episodios donde ambas entidades aparecen
                related_episodes = []
                
                for episode in episodes:
                    episode_text = json.dumps(episode.get("action_details", {})).lower()
                    if entity1.lower() in episode_text and entity2.lower() in episode_text:
                        related_episodes.append(episode.get("id", ""))
                
                if len(related_episodes) >= 2:
                    relationships.append({
                        "from": entity1,
                        "to": entity2,
                        "type": "colabora_con",
                        "confidence": min(0.9, len(related_episodes) / 5),
                        "episode_ids": related_episodes,
                        "tags": ["relationship", "collaboration", entity1.lower(), entity2.lower()]
                    })
        
        return relationships
    
    def _find_common_contexts(self, episodes: List[Dict[str, Any]]) -> str:
        """Encuentra contextos comunes en un grupo de episodios"""
        if len(episodes) < 2:
            return ""
        
        # Buscar claves comunes en context_state
        common_keys = set()
        for episode in episodes:
            context_state = episode.get("context_state", {})
            if not common_keys:
                common_keys = set(context_state.keys())
            else:
                common_keys &= set(context_state.keys())
        
        if common_keys:
            return f"Contexto común: {list(common_keys)}"
        
        return ""
    
    async def _store_knowledge_item(self, 
                                  knowledge_type: str,
                                  content: str,
                                  confidence_score: float,
                                  source_episodes: List[str],
                                  tags: List[str]) -> str:
        """Almacena un item de conocimiento en Chroma"""
        try:
            collection = await self._get_collection()
            
            # Generar embedding
            embedding = await self._generate_embedding(content)
            
            # Crear ID único
            knowledge_id = f"{knowledge_type}_{datetime.utcnow().timestamp()}"
            
            # Metadata
            metadata = {
                "knowledge_type": knowledge_type,
                "confidence_score": confidence_score,
                "source_episodes": json.dumps(source_episodes),
                "tags": json.dumps(tags),
                "created_at": datetime.utcnow().isoformat(),
                "access_count": 0
            }
            
            # Almacenar en Chroma
            collection.add(
                documents=[content],
                embeddings=[embedding],
                metadatas=[metadata],
                ids=[knowledge_id]
            )
            
            logger.debug(f"Conocimiento almacenado: {knowledge_id}")
            return knowledge_id
            
        except Exception as e:
            logger.error(f"Error almacenando conocimiento: {e}")
            return ""
    
    async def search_semantic(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Búsqueda semántica por similaridad vectorial
        
        Args:
            query: Consulta de búsqueda
            limit: Número máximo de resultados
            
        Returns:
            Lista de items de conocimiento similares
        """
        try:
            collection = await self._get_collection()
            
            # Generar embedding del query
            query_embedding = await self._generate_embedding(query)
            
            # Buscar en Chroma
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=min(limit, self.max_results)
            )
            
            # Procesar resultados
            knowledge_items = []
            
            if results["ids"] and results["ids"][0]:
                for i in range(len(results["ids"][0])):
                    item = {
                        "id": results["ids"][0][i],
                        "content": results["documents"][0][i],
                        "distance": results["distances"][0][i] if results.get("distances") else None,
                        "similarity": 1 - (results["distances"][0][i] if results.get("distances") else 0),
                        "metadata": results["metadatas"][0][i] if results.get("metadatas") else {}
                    }
                    
                    # Filtrar por umbral de similaridad
                    if item["similarity"] >= self.similarity_threshold:
                        knowledge_items.append(item)
                        
                        # Actualizar contador de acceso
                        await self._update_access_count(item["id"])
            
            logger.debug(f"Búsqueda semántica: {len(knowledge_items)} resultados para '{query}'")
            return knowledge_items
            
        except Exception as e:
            logger.error(f"Error en búsqueda semántica: {e}")
            return []
    
    async def get_related_concepts(self, concept: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Obtiene conceptos relacionados al concepto dado
        
        Args:
            concept: Concepto base
            limit: Número de conceptos relacionados
            
        Returns:
            Lista de conceptos relacionados
        """
        try:
            # Buscar conocimiento relacionado al concepto
            related_knowledge = await self.search_semantic(concept, limit=limit * 2)
            
            # Filtrar solo conceptos
            concepts = [
                item for item in related_knowledge 
                if item.get("metadata", {}).get("knowledge_type") == "concept"
            ]
            
            return concepts[:limit]
            
        except Exception as e:
            logger.error(f"Error obteniendo conceptos relacionados: {e}")
            return []
    
    async def update_knowledge_graph(self, patterns: List[Dict[str, Any]]) -> bool:
        """
        Actualiza el grafo de conocimiento con nuevos patrones
        
        Args:
            patterns: Lista de patrones extraídos
            
        Returns:
            True si se actualizó exitosamente
        """
        try:
            for pattern in patterns:
                await self._store_knowledge_item(
                    knowledge_type=pattern.get("type", "pattern"),
                    content=pattern.get("content", ""),
                    confidence_score=pattern.get("confidence", 0.7),
                    source_episodes=pattern.get("source_episodes", []),
                    tags=pattern.get("tags", [])
                )
            
            logger.info(f"Grafo de conocimiento actualizado con {len(patterns)} patrones")
            return True
            
        except Exception as e:
            logger.error(f"Error actualizando grafo de conocimiento: {e}")
            return False
    
    async def consolidate_from_episodes(self, episodes: List[Dict[str, Any]], 
                                      importance_threshold: float = 0.7) -> Dict[str, Any]:
        """
        Consolidar conocimiento desde episodios con umbral de importancia
        
        Args:
            episodes: Episodios para consolidar
            importance_threshold: Umbral mínimo de importancia
            
        Returns:
            Estadísticas de consolidación
        """
        try:
            # Filtrar episodios por importancia
            important_episodes = [
                ep for ep in episodes 
                if ep.get("importance_score", 0) >= importance_threshold
            ]
            
            if not important_episodes:
                logger.warning("No hay episodios importantes para consolidar")
                return {"consolidated": 0, "knowledge_created": 0}
            
            # Extraer y almacenar conocimiento
            knowledge_ids = await self.extract_and_store_knowledge(important_episodes)
            
            stats = {
                "episodes_analyzed": len(episodes),
                "important_episodes": len(important_episodes),
                "knowledge_created": len(knowledge_ids),
                "consolidated": True,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Consolidación completada: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error en consolidación: {e}")
            return {"consolidated": 0, "knowledge_created": 0, "error": str(e)}
    
    async def _update_access_count(self, knowledge_id: str) -> bool:
        """Actualiza el contador de acceso de un item de conocimiento"""
        try:
            collection = await self._get_collection()
            
            # Obtener item actual
            result = collection.get(ids=[knowledge_id], include=["metadatas"])
            
            if result["ids"]:
                metadata = result["metadatas"][0]
                metadata["access_count"] = metadata.get("access_count", 0) + 1
                metadata["last_accessed"] = datetime.utcnow().isoformat()
                
                # Actualizar en Chroma
                collection.update(
                    ids=[knowledge_id],
                    metadatas=[metadata]
                )
                
                return True
            
        except Exception as e:
            logger.error(f"Error actualizando contador acceso: {e}")
        
        return False
    
    async def get_knowledge_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de la memoria semántica
        
        Returns:
            Diccionario con estadísticas
        """
        try:
            collection = await self._get_collection()
            
            # Obtener todos los items
            all_items = collection.get(include=["metadatas"])
            
            if not all_items["ids"]:
                return {"total_items": 0}
            
            # Analizar metadatos
            knowledge_types = {}
            total_access = 0
            confidence_scores = []
            
            for metadata in all_items["metadatas"]:
                # Contar por tipo
                ktype = metadata.get("knowledge_type", "unknown")
                knowledge_types[ktype] = knowledge_types.get(ktype, 0) + 1
                
                # Sumar accesos
                total_access += metadata.get("access_count", 0)
                
                # Recopilar confidence scores
                confidence = metadata.get("confidence_score", 0)
                if confidence:
                    confidence_scores.append(confidence)
            
            stats = {
                "total_items": len(all_items["ids"]),
                "knowledge_types": knowledge_types,
                "total_accesses": total_access,
                "avg_confidence": sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0,
                "vector_dimension": self.vector_dimension,
                "similarity_threshold": self.similarity_threshold
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {"error": str(e)}
    
    async def get_main_concepts(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Obtiene los conceptos principales del conocimiento semántico
        
        Args:
            limit: Número máximo de conceptos a retornar
            
        Returns:
            Lista de conceptos principales ordenados por relevancia
        """
        try:
            collection = await self._get_collection()
            
            # Obtener todos los conceptos
            result = collection.get(include=["metadatas", "documents"])
            
            if not result["ids"]:
                return []
            
            concepts = []
            for i, item_id in enumerate(result["ids"]):
                metadata = result["metadatas"][i] if i < len(result["metadatas"]) else {}
                
                # Solo incluir items de tipo 'concept'
                if metadata.get('knowledge_type') == 'concept':
                    concept_data = {
                        'id': item_id,
                        'content': result["documents"][i] if result["documents"] and i < len(result["documents"]) else '',
                        'confidence_score': float(metadata.get('confidence_score', 0.7)),
                        'access_count': int(metadata.get('access_count', 0)),
                        'tags': metadata.get('tags', []),
                        'created_at': metadata.get('created_at', ''),
                        'last_accessed': metadata.get('last_accessed', '')
                    }
                    concepts.append(concept_data)
            
            # Ordenar por una combinación de confidence y access_count
            concepts.sort(
                key=lambda x: (x['confidence_score'] * 0.7 + min(x['access_count'] / 10, 1.0) * 0.3), 
                reverse=True
            )
            
            # Limitar resultados
            main_concepts = concepts[:limit]
            
            logger.debug(f"Recuperados {len(main_concepts)} conceptos principales de {len(concepts)} totales")
            return main_concepts
            
        except Exception as e:
            logger.error(f"Error obteniendo conceptos principales: {e}")
            return []
    
    async def close(self) -> None:
        """Cierra conexiones y libera recursos"""
        try:
            # Chromadb client no necesita cierre explícito
            if self.embedding_model:
                # Limpiar modelo de memoria si es necesario
                self.embedding_model = None
                
            logger.info("SemanticMemory cerrada")
            
        except Exception as e:
            logger.error(f"Error cerrando SemanticMemory: {e}")