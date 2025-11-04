"""
Graph Builder for Memory Curator

Builds and queries Neo4j knowledge graph from episodes and relationships.
"""

from typing import List, Dict, Optional
from datetime import datetime
from neo4j import GraphDatabase


class GraphBuilder:
    """
    Build and query Neo4j knowledge graph

    Creates:
    - Episode nodes with properties (episode_id, content, tags, created_at)
    - Relationship edges (SIMILAR, TEMPORAL, CAUSED_BY)
    - Supports bulk operations and neighbor queries
    """

    def __init__(self, uri: str, username: str, password: str):
        """
        Initialize Neo4j connection

        Args:
            uri: Neo4j bolt URI (e.g. bolt://localhost:7688)
            username: Neo4j username
            password: Neo4j password
        """
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()

    def clear_graph(self):
        """Clear all nodes and relationships (for testing)"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def create_episode_node(self, episode: Dict) -> bool:
        """
        Create episode node in Neo4j

        Args:
            episode: Episode dict with keys:
                - episode_id: str (UUID)
                - content: str
                - tags: List[str]
                - created_at: datetime

        Returns:
            True if created successfully
        """
        query = """
        MERGE (e:Episode {episode_id: $episode_id})
        SET e.content = $content,
            e.tags = $tags,
            e.created_at = datetime($created_at)
        RETURN e
        """

        with self.driver.session() as session:
            result = session.run(
                query,
                episode_id=episode['episode_id'],
                content=episode.get('content', ''),
                tags=episode.get('tags', []),
                created_at=episode['created_at'].isoformat() if isinstance(episode.get('created_at'), datetime) else str(episode.get('created_at'))
            )
            return result.single() is not None

    def create_relationship(self, rel: Dict) -> bool:
        """
        Create relationship edge between two episodes

        Args:
            rel: Relationship dict with keys:
                - from: str (source episode_id)
                - to: str (target episode_id)
                - type: str (SIMILAR, TEMPORAL, CAUSED_BY)
                - strength or hours_apart: float

        Returns:
            True if created successfully
        """
        # Build dynamic relationship type
        rel_type = rel.get('type', 'RELATED')

        # Get relationship properties
        props = {}
        if 'strength' in rel:
            props['strength'] = rel['strength']
        if 'hours_apart' in rel:
            props['hours_apart'] = rel['hours_apart']

        query = f"""
        MATCH (from:Episode {{episode_id: $from_id}})
        MATCH (to:Episode {{episode_id: $to_id}})
        MERGE (from)-[r:{rel_type}]->(to)
        SET r += $props
        RETURN r
        """

        with self.driver.session() as session:
            result = session.run(
                query,
                from_id=rel['from'],
                to_id=rel['to'],
                props=props
            )
            return result.single() is not None

    def bulk_create_episodes(self, episodes: List[Dict]) -> int:
        """
        Bulk create episode nodes

        Args:
            episodes: List of episode dicts

        Returns:
            Number of episodes created
        """
        count = 0
        for episode in episodes:
            if self.create_episode_node(episode):
                count += 1
        return count

    def bulk_create_relationships(self, relationships: List[Dict]) -> int:
        """
        Bulk create relationships

        Args:
            relationships: List of relationship dicts

        Returns:
            Number of relationships created
        """
        count = 0
        for rel in relationships:
            if self.create_relationship(rel):
                count += 1
        return count

    def query_neighbors(self, episode_id: str, max_distance: int = 1) -> List[Dict]:
        """
        Query neighbors of episode within max_distance hops

        Args:
            episode_id: Episode UUID to query from
            max_distance: Maximum hops (1 or 2)

        Returns:
            List of neighbor episode dicts
        """
        query = f"""
        MATCH path = (start:Episode {{episode_id: $episode_id}})-[*1..{max_distance}]-(neighbor:Episode)
        WHERE neighbor.episode_id <> $episode_id
        RETURN DISTINCT neighbor.episode_id as episode_id,
               neighbor.content as content,
               neighbor.tags as tags,
               neighbor.created_at as created_at
        """

        with self.driver.session() as session:
            result = session.run(query, episode_id=episode_id)

            neighbors = []
            for record in result:
                neighbors.append({
                    'episode_id': record['episode_id'],
                    'content': record.get('content', ''),
                    'tags': list(record.get('tags', [])),
                    'created_at': record.get('created_at')
                })

            return neighbors
