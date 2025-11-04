#!/usr/bin/env python3
"""Test y fix del embedding model configuration"""

import requests
import json

def test_embedding_configuration():
    """Test directo del embedding model"""
    
    print("🧪 TESTING EMBEDDING MODEL CONFIGURATION")
    
    # Test 1: Verificar que semantic memory tiene embeddings
    print("\n1. Testing semantic memory search (should generate embeddings):")
    
    response = requests.post(
        "http://localhost:8001/memory/search",
        json={
            "query": "test embedding generation",
            "memory_types": ["semantic"],
            "limit": 3
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        semantic_results = data.get('semantic_knowledge', [])
        print(f"   ✅ Semantic search working: {len(semantic_results)} results")
    else:
        print(f"   ❌ Semantic search failed: {response.status_code}")
    
    # Test 2: Forzar queries múltiples para cache warming
    print("\n2. Cache warming with similar queries:")
    
    similar_queries = [
        "ARIA sistema memoria",
        "ARIA memory system", 
        "memoria ARIA sistema",
        "sistema ARIA memoria",
        "ARIA memoria inteligente"
    ]
    
    for i, query in enumerate(similar_queries):
        response = requests.post(
            "http://localhost:8001/memory/search",
            json={
                "query": query,
                "memory_types": ["episodic", "semantic"],
                "limit": 5
            }
        )
        
        if response.status_code == 200:
            print(f"   ✅ Query {i+1}: {query}")
        else:
            print(f"   ❌ Query {i+1} failed: {response.status_code}")
    
    # Test 3: Verificar stats después del warming
    print("\n3. Verificando estadísticas cache post-warming:")
    
    response = requests.get("http://localhost:8001/stats")
    if response.status_code == 200:
        data = response.json()
        cache_stats = data.get('integrated_graph_memory', {}).get('semantic_cache_stats', {})
        
        print(f"   Total queries: {cache_stats.get('total_queries', 0)}")
        print(f"   Cache hits: {cache_stats.get('cache_hits', 0)}")
        print(f"   Hit rate: {cache_stats.get('hit_rate', 0):.1%}")
        print(f"   Embedding index size: {cache_stats.get('distribution', {}).get('embedding_index_size', 0)}")
        print(f"   Embedding cache size: {cache_stats.get('distribution', {}).get('embedding_cache_size', 0)}")
        
        # Test 4: Query repetida para verificar cache hit
        print("\n4. Testing cache hit with repeated query:")
        
        test_query = "ARIA sistema memoria"
        
        # Primera query
        response1 = requests.post(
            "http://localhost:8001/memory/search",
            json={"query": test_query, "memory_types": ["episodic"], "limit": 5}
        )
        
        # Segunda query (debería ser cache hit)
        response2 = requests.post(
            "http://localhost:8001/memory/search", 
            json={"query": test_query, "memory_types": ["episodic"], "limit": 5}
        )
        
        if response1.status_code == 200 and response2.status_code == 200:
            print(f"   ✅ Repeated queries successful")
            
            # Check stats again
            response = requests.get("http://localhost:8001/stats")
            if response.status_code == 200:
                data = response.json()
                cache_stats = data.get('integrated_graph_memory', {}).get('semantic_cache_stats', {})
                final_hit_rate = cache_stats.get('hit_rate', 0)
                print(f"   Final hit rate: {final_hit_rate:.1%}")
                
                if final_hit_rate > 0:
                    print("   🎉 CACHE WORKING!")
                else:
                    print("   ⚠️ Cache still not hitting")
    
    print("\n" + "="*50)
    print("🎯 EMBEDDING TEST COMPLETED")

if __name__ == "__main__":
    test_embedding_configuration()