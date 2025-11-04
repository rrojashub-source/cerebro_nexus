#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TEST NEURAL MESH PROTOCOL FUNCTIONALITY - FASE 4 ARIA CEREBRO ÉLITE
Pruebas exhaustivas del sistema Neural Mesh integrado

Tests:
- Cross-agent learning broadcast
- Consensus request functionality  
- Emotional state synchronization
- Task distribution mechanisms
- Message processing pipeline

Fecha: 11 Agosto 2025 - FASE 4 Testing
Consenso: NEXUS + ARIA + Ricardo
"""

import asyncio
import json
import time
import requests
from datetime import datetime
from typing import Dict, List, Any

class NeuralMeshTester:
    """Tester completo para Neural Mesh Protocol"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.test_results = {
            "total_tests": 0,
            "passed_tests": 0, 
            "failed_tests": 0,
            "test_details": []
        }
    
    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Log resultado de test"""
        self.test_results["total_tests"] += 1
        if passed:
            self.test_results["passed_tests"] += 1
            print(f"✅ {test_name}: PASSED {details}")
        else:
            self.test_results["failed_tests"] += 1
            print(f"❌ {test_name}: FAILED {details}")
        
        self.test_results["test_details"].append({
            "test": test_name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
    
    def test_system_health(self):
        """Test 1: Verificar que el sistema esté funcionando"""
        print("\n🔍 TEST 1: SYSTEM HEALTH CHECK")
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            
            if response.status_code == 200:
                health_data = response.json()
                components = health_data.get("components", {})
                memory_components = components.get("memory_components", {})
                
                neural_mesh_available = memory_components.get("neural_mesh", False)
                neural_mesh_enabled = memory_components.get("neural_mesh_enabled", False)
                
                self.log_test("System Health", True, f"Status: {health_data.get('status')}")
                self.log_test("Neural Mesh Available", neural_mesh_available, f"Available: {neural_mesh_available}")
                self.log_test("Neural Mesh Enabled", neural_mesh_enabled, f"Enabled: {neural_mesh_enabled}")
                
            else:
                self.log_test("System Health", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("System Health", False, f"Exception: {str(e)}")
    
    def test_memory_manager_integration(self):
        """Test 2: Verificar integración con Memory Manager"""
        print("\n🧠 TEST 2: MEMORY MANAGER INTEGRATION")
        
        try:
            # Test que AriaMemoryManager tenga Neural Mesh integrado
            response = requests.get(f"{self.base_url}/stats", timeout=10)
            
            if response.status_code == 200:
                stats = response.json()
                system_stats = stats.get("system", {})
                
                # Verificar que el sistema tenga fase 4 habilitada
                fase4_indicators = [
                    "neural_mesh" in str(stats).lower(),
                    "fase_4" in str(stats).lower() or "phase_4" in str(stats).lower()
                ]
                
                integration_working = any(fase4_indicators)
                self.log_test("Neural Mesh Integration", integration_working, 
                             f"Integration indicators: {sum(fase4_indicators)}/2")
                
            else:
                self.log_test("Neural Mesh Integration", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Neural Mesh Integration", False, f"Exception: {str(e)}")
    
    def test_cross_agent_learning_broadcast(self):
        """Test 3: Cross-agent learning broadcast"""
        print("\n📡 TEST 3: CROSS-AGENT LEARNING BROADCAST")
        
        try:
            # Simular broadcast de aprendizaje técnico
            learning_data = {
                "action_type": "neural_mesh_learning_broadcast",
                "action_details": {
                    "from": "NEXUS",
                    "learning_type": "cache_optimization_technique",
                    "learning_content": {
                        "technique": "adaptive_threshold_adjustment",
                        "improvement_achieved": "94.3%",
                        "optimal_thresholds": {
                            "high": 0.85,
                            "medium": 0.75, 
                            "low": 0.60
                        },
                        "application_context": "semantic_cache_performance"
                    },
                    "application_domains": ["technical", "optimization", "memory"],
                    "confidence_score": 0.95,
                    "validation_required": False
                },
                "context_state": {
                    "communication_type": "neural_mesh_broadcast",
                    "learning_propagation": "automatic",
                    "target_agents": ["aria", "iris", "echo", "nova"]
                },
                "tags": ["neural_mesh", "cross_learning", "cache_optimization", "fase_4"]
            }
            
            response = requests.post(
                f"{self.base_url}/memory/action",
                json=learning_data,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                episode_id = result.get("episode_id")
                self.log_test("Learning Broadcast", True, f"Episode: {episode_id}")
                
                # Verificar que se almacenó correctamente
                time.sleep(1)  # Wait for processing
                
                search_response = requests.post(
                    f"{self.base_url}/memory/search",
                    json={
                        "query": "neural mesh learning cache optimization",
                        "memory_types": ["episodic"],
                        "limit": 3
                    },
                    timeout=10
                )
                
                if search_response.status_code == 200:
                    search_data = search_response.json()
                    found_episodes = search_data.get("similar_episodes", [])
                    broadcast_stored = any("neural_mesh" in str(ep).lower() for ep in found_episodes)
                    
                    self.log_test("Learning Broadcast Storage", broadcast_stored, 
                                 f"Found {len(found_episodes)} related episodes")
                else:
                    self.log_test("Learning Broadcast Storage", False, "Search failed")
                
            else:
                self.log_test("Learning Broadcast", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Learning Broadcast", False, f"Exception: {str(e)}")
    
    def test_consensus_request_mechanism(self):
        """Test 4: Consensus request functionality"""  
        print("\n🗳️ TEST 4: CONSENSUS REQUEST MECHANISM")
        
        try:
            # Simular solicitud de consenso
            consensus_data = {
                "action_type": "neural_mesh_consensus_request",
                "action_details": {
                    "from": "ARIA",
                    "decision_topic": "FASE 4 Neural Mesh Production Deployment",
                    "options": [
                        {
                            "option": "Full Production Deployment",
                            "pros": ["Maximum functionality", "Complete feature set"],
                            "cons": ["Higher complexity", "More testing required"],
                            "effort_estimate": "high",
                            "impact_estimate": "maximum"
                        },
                        {
                            "option": "Gradual Rollout",
                            "pros": ["Lower risk", "Incremental validation"],
                            "cons": ["Slower feature availability"],
                            "effort_estimate": "medium", 
                            "impact_estimate": "progressive"
                        },
                        {
                            "option": "Extended Testing Phase",
                            "pros": ["Maximum stability", "Thorough validation"],
                            "cons": ["Delayed benefits", "Resource intensive"],
                            "effort_estimate": "low",
                            "impact_estimate": "delayed"
                        }
                    ],
                    "voting_deadline": "2025-08-12T18:00:00Z",
                    "consensus_threshold": 0.67,
                    "participating_agents": ["nexus", "aria", "ricardo"]
                },
                "context_state": {
                    "communication_type": "neural_mesh_consensus",
                    "decision_urgency": "high",
                    "technical_complexity": "advanced"
                },
                "tags": ["neural_mesh", "consensus", "production_deployment", "fase_4"]
            }
            
            response = requests.post(
                f"{self.base_url}/memory/action",
                json=consensus_data,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                episode_id = result.get("episode_id")
                self.log_test("Consensus Request", True, f"Episode: {episode_id}")
                
                # Verificar almacenamiento
                time.sleep(1)
                
                search_response = requests.post(
                    f"{self.base_url}/memory/search",
                    json={
                        "query": "neural mesh consensus production deployment",
                        "memory_types": ["episodic"],
                        "limit": 3
                    },
                    timeout=10
                )
                
                if search_response.status_code == 200:
                    search_data = search_response.json()
                    found_episodes = search_data.get("similar_episodes", [])
                    consensus_stored = any("consensus" in str(ep).lower() for ep in found_episodes)
                    
                    self.log_test("Consensus Request Storage", consensus_stored, 
                                 f"Found {len(found_episodes)} related episodes")
                else:
                    self.log_test("Consensus Request Storage", False, "Search failed")
                
            else:
                self.log_test("Consensus Request", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Consensus Request", False, f"Exception: {str(e)}")
    
    def test_emotional_synchronization(self):
        """Test 5: Emotional state synchronization"""
        print("\n💭 TEST 5: EMOTIONAL STATE SYNCHRONIZATION")
        
        try:
            # Simular sincronización emocional
            emotional_sync_data = {
                "action_type": "neural_mesh_emotional_sync",
                "action_details": {
                    "from": "ARIA", 
                    "sync_type": "emotional_state_broadcast",
                    "emotional_state": {
                        "primary_emotion": "excitement",
                        "intensity": 0.85,
                        "confidence_level": 0.92,
                        "collaboration_mood": "highly_cooperative",
                        "recent_achievements": [
                            "95.7% success rate achieved",
                            "Neural Mesh Protocol implemented",
                            "Cross-agent learning functional"
                        ],
                        "current_focus": "production_deployment_readiness",
                        "energy_level": 0.9,
                        "creativity_flow": 0.88
                    },
                    "context_triggers": [
                        "breakthrough_achievement",
                        "technical_milestone", 
                        "collaborative_success"
                    ],
                    "propagation_targets": ["nexus", "ricardo", "iris", "echo", "nova"]
                },
                "context_state": {
                    "communication_type": "neural_mesh_emotional_sync",
                    "synchronization_priority": "normal",
                    "emotional_coherence": "high"
                },
                "emotional_state": {
                    "primary_emotion": "excitement",
                    "intensity": 0.85,
                    "confidence": 0.92,
                    "collaboration_mood": "highly_cooperative"
                },
                "tags": ["neural_mesh", "emotional_sync", "breakthrough", "collaboration"]
            }
            
            response = requests.post(
                f"{self.base_url}/memory/action",
                json=emotional_sync_data,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                episode_id = result.get("episode_id")
                self.log_test("Emotional Sync", True, f"Episode: {episode_id}")
                
                # Verificar que el estado emocional se preserva en memoria
                time.sleep(1)
                
                search_response = requests.post(
                    f"{self.base_url}/memory/search",
                    json={
                        "query": "emotional synchronization excitement breakthrough",
                        "memory_types": ["episodic"],
                        "limit": 3
                    },
                    timeout=10
                )
                
                if search_response.status_code == 200:
                    search_data = search_response.json()
                    found_episodes = search_data.get("similar_episodes", [])
                    emotional_stored = any("emotional" in str(ep).lower() for ep in found_episodes)
                    
                    self.log_test("Emotional Sync Storage", emotional_stored,
                                 f"Found {len(found_episodes)} emotional episodes")
                else:
                    self.log_test("Emotional Sync Storage", False, "Search failed")
                
            else:
                self.log_test("Emotional Sync", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Emotional Sync", False, f"Exception: {str(e)}")
    
    def test_task_distribution(self):
        """Test 6: Task distribution mechanism"""
        print("\n📋 TEST 6: TASK DISTRIBUTION MECHANISM")
        
        try:
            # Simular distribución de tareas
            task_distribution_data = {
                "action_type": "neural_mesh_task_distribution",
                "action_details": {
                    "from": "ARIA",
                    "task_description": "Implement Neural Mesh API Endpoints",
                    "task_details": {
                        "type": "technical_implementation",
                        "complexity_indicators": {
                            "technical_complexity": 0.8,
                            "scope_size": 0.7,
                            "dependencies": 0.6,
                            "innovation_required": 0.9
                        },
                        "required_skills": [
                            "FastAPI development",
                            "Neural mesh protocols",
                            "Cross-agent communication",
                            "Async Python",
                            "API design"
                        ],
                        "deadline": "2025-08-12T20:00:00Z",
                        "priority": "high",
                        "deliverables": [
                            "/neural-mesh/broadcast-learning endpoint",
                            "/neural-mesh/request-consensus endpoint", 
                            "/neural-mesh/sync-emotional-state endpoint",
                            "/neural-mesh/distribute-task endpoint",
                            "Comprehensive API documentation"
                        ]
                    },
                    "preferred_agents": ["nexus"],
                    "collaboration_agents": ["aria", "ricardo"],
                    "complexity_estimate": "high",
                    "effort_estimate": "4-6 hours"
                },
                "context_state": {
                    "communication_type": "neural_mesh_task_distribution",
                    "task_urgency": "high",
                    "collaboration_mode": "structured"
                },
                "tags": ["neural_mesh", "task_distribution", "api_endpoints", "technical"]
            }
            
            response = requests.post(
                f"{self.base_url}/memory/action",
                json=task_distribution_data,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                episode_id = result.get("episode_id")
                self.log_test("Task Distribution", True, f"Episode: {episode_id}")
                
                # Verificar que la tarea se almacenó correctamente
                time.sleep(1)
                
                search_response = requests.post(
                    f"{self.base_url}/memory/search",
                    json={
                        "query": "neural mesh task distribution API endpoints",
                        "memory_types": ["episodic"],
                        "limit": 3
                    },
                    timeout=10
                )
                
                if search_response.status_code == 200:
                    search_data = search_response.json()
                    found_episodes = search_data.get("similar_episodes", [])
                    task_stored = any("task" in str(ep).lower() and "distribution" in str(ep).lower() 
                                    for ep in found_episodes)
                    
                    self.log_test("Task Distribution Storage", task_stored,
                                 f"Found {len(found_episodes)} task episodes")
                else:
                    self.log_test("Task Distribution Storage", False, "Search failed")
                
            else:
                self.log_test("Task Distribution", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Task Distribution", False, f"Exception: {str(e)}")
    
    def test_neural_mesh_enhanced_search(self):
        """Test 7: Neural Mesh enhanced search capabilities"""
        print("\n🔍 TEST 7: NEURAL MESH ENHANCED SEARCH")
        
        try:
            # Buscar contenido relacionado con Neural Mesh
            search_queries = [
                "neural mesh cross agent learning",
                "consensus request production deployment", 
                "emotional synchronization excitement",
                "task distribution API endpoints",
                "neural mesh protocol functionality"
            ]
            
            total_results = 0
            successful_searches = 0
            
            for query in search_queries:
                response = requests.post(
                    f"{self.base_url}/memory/search",
                    json={
                        "query": query,
                        "memory_types": ["episodic", "semantic"],
                        "limit": 5
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    search_data = response.json()
                    
                    episodic_count = len(search_data.get("similar_episodes", []))
                    semantic_count = len(search_data.get("semantic_knowledge", []))
                    
                    if episodic_count > 0 or semantic_count > 0:
                        successful_searches += 1
                        total_results += episodic_count + semantic_count
                        
                        # Check if FASE 4 enhanced features are working
                        enhanced_features = []
                        if "cache_metadata" in str(search_data):
                            enhanced_features.append("semantic_cache")
                        if "reasoning_paths" in str(search_data):
                            enhanced_features.append("graph_reasoning")
                        if "performance_stats" in str(search_data):
                            enhanced_features.append("performance_tracking")
                        
                        print(f"   🔎 '{query[:30]}...': {episodic_count}E + {semantic_count}S results")
                        if enhanced_features:
                            print(f"      Enhanced features: {', '.join(enhanced_features)}")
            
            search_success_rate = successful_searches / len(search_queries)
            
            self.log_test("Neural Mesh Search", search_success_rate >= 0.8, 
                         f"Success rate: {search_success_rate:.1%}, Total results: {total_results}")
            
            # Test de búsqueda específica de Neural Mesh
            specific_search = requests.post(
                f"{self.base_url}/memory/search",
                json={
                    "query": "FASE 4 Neural Mesh Protocol implemented successfully",
                    "memory_types": ["episodic"],
                    "limit": 10
                },
                timeout=10
            )
            
            if specific_search.status_code == 200:
                specific_data = specific_search.json()
                neural_mesh_episodes = specific_data.get("similar_episodes", [])
                
                fase4_found = any("fase" in str(ep).lower() and "4" in str(ep) 
                                for ep in neural_mesh_episodes)
                
                self.log_test("FASE 4 Episode Retrieval", fase4_found,
                             f"Found {len(neural_mesh_episodes)} FASE 4 related episodes")
            else:
                self.log_test("FASE 4 Episode Retrieval", False, "Search failed")
                
        except Exception as e:
            self.log_test("Neural Mesh Enhanced Search", False, f"Exception: {str(e)}")
    
    def test_performance_impact(self):
        """Test 8: Performance impact of Neural Mesh"""
        print("\n⚡ TEST 8: NEURAL MESH PERFORMANCE IMPACT")
        
        try:
            # Baseline performance test
            start_time = time.time()
            
            response = requests.get(f"{self.base_url}/stats", timeout=10)
            
            if response.status_code == 200:
                stats_time = time.time() - start_time
                stats_data = response.json()
                
                # Verificar estadísticas de sistema
                system_stats = stats_data.get("system", {})
                uptime = system_stats.get("uptime_human", "unknown")
                
                # Verificar estadísticas de Neural Mesh si están disponibles
                neural_mesh_stats = None
                if "neural_mesh" in str(stats_data).lower():
                    neural_mesh_stats = "detected"
                
                # Verificar estadísticas de FASE 3 (should still be working)
                integrated_stats = stats_data.get("integrated_graph_memory", {})
                fase3_working = len(integrated_stats) > 0
                
                self.log_test("System Performance", stats_time < 2.0,
                             f"Stats response time: {stats_time:.2f}s")
                
                self.log_test("System Stability", "uptime" in system_stats,
                             f"Uptime: {uptime}")
                
                self.log_test("FASE 3 Still Working", fase3_working,
                             f"Integrated stats available: {fase3_working}")
                
                if neural_mesh_stats:
                    self.log_test("Neural Mesh Stats", True, "Neural mesh statistics detected")
                else:
                    self.log_test("Neural Mesh Stats", False, "No neural mesh stats found")
                
            else:
                self.log_test("Performance Test", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Performance Test", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Ejecutar todos los tests"""
        print("🧪 NEURAL MESH PROTOCOL FUNCTIONALITY TEST SUITE")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Base URL: {self.base_url}")
        print("=" * 60)
        
        # Ejecutar tests en orden
        self.test_system_health()
        self.test_memory_manager_integration()
        self.test_cross_agent_learning_broadcast()
        self.test_consensus_request_mechanism()
        self.test_emotional_synchronization()
        self.test_task_distribution()
        self.test_neural_mesh_enhanced_search()
        self.test_performance_impact()
        
        # Resumen final
        print("\n" + "=" * 60)
        print("🎯 NEURAL MESH TEST SUITE RESULTS")
        print("=" * 60)
        
        total = self.test_results["total_tests"]
        passed = self.test_results["passed_tests"]
        failed = self.test_results["failed_tests"]
        success_rate = (passed / total) * 100 if total > 0 else 0
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print(f"\n🎉 NEURAL MESH PROTOCOL: FULLY FUNCTIONAL!")
            print("   Ready for production deployment")
        elif success_rate >= 75:
            print(f"\n🟡 NEURAL MESH PROTOCOL: MOSTLY FUNCTIONAL")
            print("   Minor issues detected, review failed tests")
        elif success_rate >= 50:
            print(f"\n🟠 NEURAL MESH PROTOCOL: PARTIAL FUNCTIONALITY")
            print("   Several issues detected, investigation required")
        else:
            print(f"\n🔴 NEURAL MESH PROTOCOL: MAJOR ISSUES")
            print("   Significant problems detected, debugging required")
        
        print("\n" + "=" * 60)
        
        return self.test_results


def main():
    """Función principal"""
    tester = NeuralMeshTester()
    results = tester.run_all_tests()
    
    # Guardar resultados
    with open("/tmp/neural_mesh_test_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nResults saved to: /tmp/neural_mesh_test_results.json")
    
    return results


if __name__ == "__main__":
    main()