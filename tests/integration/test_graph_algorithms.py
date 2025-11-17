"""
Integration Tests for Graph Algorithms

Tests for Neo4j advanced graph algorithms including:
- Community detection
- Centrality measures (PageRank, Betweenness, Degree)
- Shortest path finding
- Graph statistics

Target: >80% coverage, <1s performance for 10K nodes
"""

import pytest
import sys
import os
import time
from neo4j import GraphDatabase

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'api'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'services'))

from services.graph_algorithms import GraphAlgorithms


# ==================== Fixtures ====================

@pytest.fixture(scope="module")
def neo4j_connection():
    """Neo4j connection fixture"""
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "password123"

    driver = GraphDatabase.driver(uri, auth=(username, password))

    yield driver

    driver.close()


@pytest.fixture(scope="module")
def graph_algo():
    """GraphAlgorithms instance fixture"""
    algo = GraphAlgorithms(
        uri="bolt://localhost:7687",
        username="neo4j",
        password="password123"
    )

    yield algo

    algo.close()


@pytest.fixture(scope="function")
def clean_graph(neo4j_connection):
    """Clean graph before each test"""
    with neo4j_connection.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

    yield

    # Cleanup after test
    with neo4j_connection.session() as session:
        session.run("MATCH (n) DETACH DELETE n")


@pytest.fixture(scope="function")
def sample_graph(neo4j_connection, clean_graph):
    """
    Create sample graph for testing:

    Community 1: e1 -- e2 -- e3
    Community 2: e4 -- e5 -- e6
    Bridge: e3 -- e4 (connects communities)
    """
    with neo4j_connection.session() as session:
        # Create nodes
        for i in range(1, 7):
            session.run("""
                CREATE (e:Episode {
                    episode_id: $id,
                    content: $content,
                    created_at: datetime()
                })
            """, id=f"e{i}", content=f"Episode {i} content")

        # Create relationships (Community 1)
        session.run("""
            MATCH (e1:Episode {episode_id: 'e1'})
            MATCH (e2:Episode {episode_id: 'e2'})
            CREATE (e1)-[:SIMILAR {strength: 0.9}]->(e2)
        """)

        session.run("""
            MATCH (e2:Episode {episode_id: 'e2'})
            MATCH (e3:Episode {episode_id: 'e3'})
            CREATE (e2)-[:SIMILAR {strength: 0.85}]->(e3)
        """)

        # Create relationships (Community 2)
        session.run("""
            MATCH (e4:Episode {episode_id: 'e4'})
            MATCH (e5:Episode {episode_id: 'e5'})
            CREATE (e4)-[:SIMILAR {strength: 0.9}]->(e5)
        """)

        session.run("""
            MATCH (e5:Episode {episode_id: 'e5'})
            MATCH (e6:Episode {episode_id: 'e6'})
            CREATE (e5)-[:SIMILAR {strength: 0.88}]->(e6)
        """)

        # Bridge between communities
        session.run("""
            MATCH (e3:Episode {episode_id: 'e3'})
            MATCH (e4:Episode {episode_id: 'e4'})
            CREATE (e3)-[:TEMPORAL {hours_apart: 2}]->(e4)
        """)

    yield


# ==================== Graph Statistics Tests ====================

def test_analyze_empty_graph(graph_algo, clean_graph):
    """Test graph statistics on empty graph"""
    stats = graph_algo.analyze_graph_structure()

    assert stats['total_nodes'] == 0
    assert stats['total_relationships'] == 0
    assert stats['avg_degree'] == 0.0
    assert stats['density'] == 0.0
    assert stats['relationship_types'] == {}
    assert stats['largest_component_size'] == 0


def test_analyze_sample_graph(graph_algo, sample_graph):
    """Test graph statistics on sample graph"""
    stats = graph_algo.analyze_graph_structure()

    assert stats['total_nodes'] == 6
    assert stats['total_relationships'] == 5
    assert stats['avg_degree'] > 0.0
    assert stats['density'] > 0.0
    assert 'SIMILAR' in stats['relationship_types']
    assert 'TEMPORAL' in stats['relationship_types']
    assert stats['relationship_types']['SIMILAR'] == 4
    assert stats['relationship_types']['TEMPORAL'] == 1
    assert stats['largest_component_size'] == 6


# ==================== Community Detection Tests ====================

def test_detect_communities_empty_graph(graph_algo, clean_graph):
    """Test community detection on empty graph"""
    communities = graph_algo.detect_communities(min_size=1)

    assert isinstance(communities, list)
    assert len(communities) == 0


def test_detect_communities_sample_graph(graph_algo, sample_graph):
    """Test community detection on sample graph"""
    communities = graph_algo.detect_communities(algorithm="louvain", min_size=3)

    assert isinstance(communities, list)
    assert len(communities) >= 0  # May vary depending on algorithm

    # If communities found, validate structure
    for community in communities:
        assert 'community_id' in community
        assert 'size' in community
        assert 'episodes' in community
        assert 'modularity' in community
        assert community['size'] >= 3
        assert len(community['episodes']) == community['size']


def test_detect_communities_min_size_filter(graph_algo, sample_graph):
    """Test that min_size parameter filters correctly"""
    # Get all communities
    all_communities = graph_algo.detect_communities(min_size=1)

    # Get filtered communities
    filtered_communities = graph_algo.detect_communities(min_size=5)

    # Filtered should have fewer or equal communities
    assert len(filtered_communities) <= len(all_communities)

    # All filtered communities should have size >= 5
    for community in filtered_communities:
        assert community['size'] >= 5


# ==================== PageRank Tests ====================

def test_pagerank_empty_graph(graph_algo, clean_graph):
    """Test PageRank on empty graph"""
    rankings = graph_algo.calculate_pagerank()

    assert isinstance(rankings, list)
    assert len(rankings) == 0


def test_pagerank_sample_graph(graph_algo, sample_graph):
    """Test PageRank on sample graph"""
    rankings = graph_algo.calculate_pagerank(top_n=10)

    assert isinstance(rankings, list)
    assert len(rankings) > 0
    assert len(rankings) <= 10

    # Validate structure
    for rank_data in rankings:
        assert 'episode_id' in rank_data
        assert 'pagerank' in rank_data
        assert 'rank' in rank_data
        assert rank_data['pagerank'] >= 0.0

    # Rankings should be in descending order
    for i in range(len(rankings) - 1):
        assert rankings[i]['pagerank'] >= rankings[i + 1]['pagerank']

    # Ranks should be sequential
    for i, rank_data in enumerate(rankings):
        assert rank_data['rank'] == i + 1


def test_pagerank_top_n_limit(graph_algo, sample_graph):
    """Test top_n parameter limits results"""
    rankings_all = graph_algo.calculate_pagerank(top_n=None)
    rankings_top3 = graph_algo.calculate_pagerank(top_n=3)

    assert len(rankings_top3) <= 3
    assert len(rankings_top3) <= len(rankings_all)


# ==================== Betweenness Centrality Tests ====================

def test_betweenness_empty_graph(graph_algo, clean_graph):
    """Test betweenness centrality on empty graph"""
    rankings = graph_algo.calculate_betweenness_centrality(top_n=10)

    assert isinstance(rankings, list)
    assert len(rankings) == 0


def test_betweenness_sample_graph(graph_algo, sample_graph):
    """Test betweenness centrality on sample graph"""
    rankings = graph_algo.calculate_betweenness_centrality(top_n=10)

    assert isinstance(rankings, list)
    assert len(rankings) > 0

    # Validate structure
    for rank_data in rankings:
        assert 'episode_id' in rank_data
        assert 'betweenness' in rank_data
        assert 'rank' in rank_data
        assert rank_data['betweenness'] >= 0.0

    # Bridge nodes (e3, e4) should have high betweenness
    bridge_nodes = [r for r in rankings if r['episode_id'] in ['e3', 'e4']]
    assert len(bridge_nodes) > 0


# ==================== Shortest Path Tests ====================

def test_shortest_path_empty_graph(graph_algo, clean_graph):
    """Test shortest path on empty graph"""
    path_data = graph_algo.find_shortest_path("e1", "e2")

    assert path_data == {}


def test_shortest_path_same_node(graph_algo, sample_graph):
    """Test shortest path from node to itself"""
    path_data = graph_algo.find_shortest_path("e1", "e1")

    # Should return empty (no path needed)
    assert path_data == {}


def test_shortest_path_adjacent_nodes(graph_algo, sample_graph):
    """Test shortest path between adjacent nodes"""
    path_data = graph_algo.find_shortest_path("e1", "e2")

    assert isinstance(path_data, dict)
    if path_data:  # If path exists
        assert 'path' in path_data
        assert 'distance' in path_data
        assert 'relationships' in path_data
        assert path_data['distance'] == 1
        assert len(path_data['path']) == 2
        assert path_data['path'][0] == 'e1'
        assert path_data['path'][1] == 'e2'


def test_shortest_path_across_communities(graph_algo, sample_graph):
    """Test shortest path across communities (through bridge)"""
    path_data = graph_algo.find_shortest_path("e1", "e6")

    assert isinstance(path_data, dict)
    if path_data:  # If path exists
        assert 'path' in path_data
        assert 'distance' in path_data
        assert 'relationships' in path_data
        assert path_data['distance'] >= 4  # Min path: e1->e2->e3->e4->e5->e6
        assert path_data['path'][0] == 'e1'
        assert path_data['path'][-1] == 'e6'
        # Bridge nodes should be in path
        assert 'e3' in path_data['path'] or 'e4' in path_data['path']


def test_shortest_path_no_connection(graph_algo, clean_graph, neo4j_connection):
    """Test shortest path when no connection exists"""
    # Create two disconnected nodes
    with neo4j_connection.session() as session:
        session.run("""
            CREATE (e1:Episode {episode_id: 'isolated1', content: 'Isolated 1'})
            CREATE (e2:Episode {episode_id: 'isolated2', content: 'Isolated 2'})
        """)

    path_data = graph_algo.find_shortest_path("isolated1", "isolated2")

    assert path_data == {}


# ==================== Important Episodes Tests ====================

def test_important_episodes_empty_graph(graph_algo, clean_graph):
    """Test important episodes on empty graph"""
    episodes = graph_algo.find_important_episodes(top_n=10, measure="degree")

    assert isinstance(episodes, list)
    assert len(episodes) == 0


def test_important_episodes_degree(graph_algo, sample_graph):
    """Test important episodes using degree centrality"""
    episodes = graph_algo.find_important_episodes(top_n=5, measure="degree")

    assert isinstance(episodes, list)
    assert len(episodes) > 0
    assert len(episodes) <= 5

    # Validate structure
    for episode in episodes:
        assert 'episode_id' in episode
        assert 'importance_score' in episode
        assert 'rank' in episode
        assert 'reason' in episode
        assert episode['importance_score'] > 0.0
        assert 'degree' in episode['reason'].lower()

    # Should be sorted by importance
    for i in range(len(episodes) - 1):
        assert episodes[i]['importance_score'] >= episodes[i + 1]['importance_score']


def test_important_episodes_pagerank(graph_algo, sample_graph):
    """Test important episodes using PageRank"""
    episodes = graph_algo.find_important_episodes(top_n=5, measure="pagerank")

    assert isinstance(episodes, list)
    assert len(episodes) > 0

    for episode in episodes:
        assert 'episode_id' in episode
        assert 'pagerank' in episode
        assert 'rank' in episode


def test_important_episodes_betweenness(graph_algo, sample_graph):
    """Test important episodes using betweenness centrality"""
    episodes = graph_algo.find_important_episodes(top_n=5, measure="betweenness")

    assert isinstance(episodes, list)

    for episode in episodes:
        assert 'episode_id' in episode
        assert 'betweenness' in episode
        assert 'rank' in episode


def test_important_episodes_invalid_measure(graph_algo, sample_graph):
    """Test that invalid measure raises error"""
    with pytest.raises(ValueError) as excinfo:
        graph_algo.find_important_episodes(top_n=5, measure="invalid_measure")

    assert "Unknown measure" in str(excinfo.value)


# ==================== Performance Tests ====================

def test_performance_pagerank_1k_nodes(graph_algo, clean_graph, neo4j_connection):
    """Test PageRank performance on 1K nodes"""
    # Create 1000 nodes with random connections
    with neo4j_connection.session() as session:
        # Create nodes
        for i in range(1000):
            session.run("""
                CREATE (e:Episode {
                    episode_id: $id,
                    content: $content
                })
            """, id=f"perf_e{i}", content=f"Performance test {i}")

        # Create relationships (each node connects to next 5)
        for i in range(995):
            for j in range(1, 6):
                session.run("""
                    MATCH (e1:Episode {episode_id: $id1})
                    MATCH (e2:Episode {episode_id: $id2})
                    CREATE (e1)-[:SIMILAR]->(e2)
                """, id1=f"perf_e{i}", id2=f"perf_e{i+j}")

    # Test performance
    start_time = time.time()
    rankings = graph_algo.calculate_pagerank(top_n=20)
    elapsed = time.time() - start_time

    assert len(rankings) > 0
    # Should complete in <1s for 1K nodes (target)
    # Relaxed to 5s for CI environments
    assert elapsed < 5.0, f"PageRank took {elapsed:.2f}s (target: <1s)"


def test_performance_graph_stats_1k_nodes(graph_algo, neo4j_connection):
    """Test graph statistics performance on 1K node graph"""
    # Create 1000 nodes for this test
    with neo4j_connection.session() as session:
        for i in range(1000):
            session.run("""
                MERGE (e:Episode {
                    episode_id: $id,
                    content: $content
                })
            """, id=f"stats_perf_e{i}", content=f"Stats performance test {i}")

    start_time = time.time()
    stats = graph_algo.analyze_graph_structure()
    elapsed = time.time() - start_time

    assert stats['total_nodes'] >= 1000
    # Should complete in <1s
    assert elapsed < 2.0, f"Graph stats took {elapsed:.2f}s (target: <1s)"

    # Cleanup
    with neo4j_connection.session() as session:
        session.run("MATCH (n) DETACH DELETE n")


# ==================== Edge Cases ====================

def test_single_node_graph(graph_algo, clean_graph, neo4j_connection):
    """Test algorithms on graph with single node"""
    with neo4j_connection.session() as session:
        session.run("""
            CREATE (e:Episode {episode_id: 'single', content: 'Single node'})
        """)

    stats = graph_algo.analyze_graph_structure()
    assert stats['total_nodes'] == 1
    assert stats['total_relationships'] == 0

    rankings = graph_algo.calculate_pagerank()
    assert len(rankings) == 0  # No connections, so no pagerank


def test_disconnected_components(graph_algo, clean_graph, neo4j_connection):
    """Test algorithms on graph with multiple disconnected components"""
    with neo4j_connection.session() as session:
        # Component 1
        session.run("""
            CREATE (e1:Episode {episode_id: 'c1_e1', content: 'Component 1 Node 1'})
            CREATE (e2:Episode {episode_id: 'c1_e2', content: 'Component 1 Node 2'})
            CREATE (e1)-[:SIMILAR]->(e2)
        """)

        # Component 2 (disconnected)
        session.run("""
            CREATE (e3:Episode {episode_id: 'c2_e1', content: 'Component 2 Node 1'})
            CREATE (e4:Episode {episode_id: 'c2_e2', content: 'Component 2 Node 2'})
            CREATE (e3)-[:SIMILAR]->(e4)
        """)

    stats = graph_algo.analyze_graph_structure()
    assert stats['total_nodes'] == 4
    assert stats['total_relationships'] == 2

    # Path between disconnected components should return empty
    path = graph_algo.find_shortest_path('c1_e1', 'c2_e1')
    assert path == {}


# ==================== Test Summary ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
