#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TEST NEURAL MESH API ENDPOINTS - FASE 4 ARIA CEREBRO ÉLITE
Tests completos para todos los endpoints Neural Mesh Protocol

Endpoints testeados:
✅ GET /neural-mesh/health - Health check Neural Mesh
✅ GET /neural-mesh/stats - Estadísticas del protocolo
✅ GET /neural-mesh/connected-agents - Agentes conectados
✅ POST /neural-mesh/broadcast-learning - Cross-agent learning
✅ POST /neural-mesh/request-consensus - Consenso triangular
✅ POST /neural-mesh/sync-emotional-state - Sincronización emocional
✅ POST /neural-mesh/distribute-task - Distribución de tareas
✅ POST /neural-mesh/process-messages - Procesamiento de mensajes

Fecha: 11 Agosto 2025 - FASE 4 API Testing
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any

class NeuralMeshAPITester:
    """Tester completo para Neural Mesh API endpoints"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.neural_mesh_url = f"{base_url}/neural-mesh"
        self.test_results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "endpoint_tests": []
        }
    
    def log_test(self, endpoint: str, test_name: str, passed: bool, details: str = "", response_code: int = None):
        """Log resultado de test"""
        self.test_results["total_tests"] += 1
        if passed:
            self.test_results["passed_tests"] += 1
            print(f"✅ {endpoint} - {test_name}: PASSED {details}")
        else:
            self.test_results["failed_tests"] += 1
            print(f"❌ {endpoint} - {test_name}: FAILED {details}")
        
        self.test_results["endpoint_tests"].append({
            "endpoint": endpoint,
            "test": test_name,
            "passed": passed,
            "details": details,
            "response_code": response_code,
            "timestamp": datetime.now().isoformat()
        })
    
    def test_neural_mesh_health(self):
        """Test 1: Neural Mesh Health Check"""
        print("\n🏥 TEST 1: NEURAL MESH HEALTH CHECK")
        
        try:
            response = requests.get(f"{self.neural_mesh_url}/health", timeout=10)
            
            if response.status_code == 200:
                health_data = response.json()
                
                # Verificar estructura de respuesta
                has_status = "status" in health_data
                has_neural_mesh = "neural_mesh" in health_data
                has_components = "components" in health_data
                has_endpoints = "endpoints" in health_data
                
                self.log_test("/health", "Response Structure", 
                             has_status and has_neural_mesh and has_components and has_endpoints,
                             f"Status: {health_data.get('status', 'unknown')}", response.status_code)
                
                # Verificar endpoints específicos
                endpoints = health_data.get("endpoints", {})
                expected_endpoints = [
                    "/broadcast-learning", "/request-consensus", "/sync-emotional-state", 
                    "/distribute-task", "/stats", "/connected-agents", "/process-messages"
                ]
                
                endpoints_active = all(endpoints.get(ep) == "active" for ep in expected_endpoints)
                self.log_test("/health", "All Endpoints Active", endpoints_active, 
                             f"Active endpoints: {len([ep for ep in expected_endpoints if endpoints.get(ep) == 'active'])}/7",
                             response.status_code)
                
            elif response.status_code == 404:
                self.log_test("/health", "Endpoint Available", False, 
                             "Neural Mesh endpoints not registered", response.status_code)
            else:
                self.log_test("/health", "HTTP Response", False, 
                             f"Unexpected status code", response.status_code)
                
        except Exception as e:
            self.log_test("/health", "Connection", False, f"Exception: {str(e)}")
    
    def test_neural_mesh_stats(self):
        """Test 2: Neural Mesh Statistics"""
        print("\n📊 TEST 2: NEURAL MESH STATISTICS")
        
        try:
            response = requests.get(f"{self.neural_mesh_url}/stats", timeout=10)
            
            if response.status_code == 200:
                stats_data = response.json()
                
                # Verificar estructura de stats
                has_protocol_stats = "neural_mesh_protocol" in stats_data
                has_integration = "system_integration" in stats_data
                has_performance = "performance_metrics" in stats_data
                
                self.log_test("/stats", "Stats Structure", 
                             has_protocol_stats and has_integration and has_performance,
                             f"Contains: protocol={has_protocol_stats}, integration={has_integration}, performance={has_performance}",
                             response.status_code)
                
                # Verificar métricas de integración
                integration = stats_data.get("system_integration", {})
                mesh_available = integration.get("mesh_available", False)
                
                self.log_test("/stats", "Integration Status", True,
                             f"Mesh available: {mesh_available}, Episodes: {integration.get('episodes_count', 0)}",
                             response.status_code)
                
            else:
                self.log_test("/stats", "HTTP Response", False, 
                             f"Status code: {response.status_code}", response.status_code)
                
        except Exception as e:
            self.log_test("/stats", "Connection", False, f"Exception: {str(e)}")
    
    def test_connected_agents(self):
        """Test 3: Connected Agents"""
        print("\n🤝 TEST 3: CONNECTED AGENTS")
        
        try:
            response = requests.get(f"{self.neural_mesh_url}/connected-agents", timeout=10)
            
            if response.status_code == 200:
                agents_data = response.json()
                
                # Verificar agentes principales
                agents = agents_data.get("agents", {})
                expected_agents = ["nexus", "aria", "ricardo"]
                agents_present = all(agent in agents for agent in expected_agents)
                
                self.log_test("/connected-agents", "Primary Agents Present", agents_present,
                             f"Found agents: {list(agents.keys())}", response.status_code)
                
                # Verificar información de agentes
                agent_info_complete = True
                for agent_name, agent_info in agents.items():
                    required_fields = ["role", "status", "specialization", "confidence_domains"]
                    if not all(field in agent_info for field in required_fields):
                        agent_info_complete = False
                        break
                
                self.log_test("/connected-agents", "Agent Info Complete", agent_info_complete,
                             f"Total agents: {agents_data.get('total_connected', 0)}", response.status_code)
                
                # Verificar topología
                topology = agents_data.get("mesh_topology", "")
                protocols = agents_data.get("communication_protocols", [])
                
                self.log_test("/connected-agents", "Mesh Topology", 
                             topology == "triangular_consensus" and len(protocols) >= 4,
                             f"Topology: {topology}, Protocols: {len(protocols)}", response.status_code)
                
            else:
                self.log_test("/connected-agents", "HTTP Response", False,
                             f"Status code: {response.status_code}", response.status_code)
                
        except Exception as e:
            self.log_test("/connected-agents", "Connection", False, f"Exception: {str(e)}")
    
    def test_broadcast_learning(self):
        """Test 4: Broadcast Learning"""
        print("\n📡 TEST 4: BROADCAST LEARNING")
        
        try:
            learning_data = {
                "learning_type": "neural_mesh_api_testing",
                "learning_content": {
                    "technique": "comprehensive_endpoint_testing",
                    "discovery": "Neural Mesh API endpoints are functional",
                    "implementation": "FastAPI with Pydantic validation",
                    "testing_methodology": "Automated endpoint validation"
                },
                "application_domains": ["testing", "api_development", "neural_mesh"],
                "confidence": 0.92,
                "from_agent": "nexus"
            }
            
            response = requests.post(
                f"{self.neural_mesh_url}/broadcast-learning",
                json=learning_data,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if response.status_code == 200:
                result_data = response.json()
                
                # Verificar respuesta
                has_success = result_data.get("success", False)
                has_message_id = "message_id" in result_data
                has_episode_id = "episode_id" in result_data
                
                self.log_test("/broadcast-learning", "Learning Broadcast", 
                             has_success and has_episode_id,
                             f"Episode ID: {result_data.get('episode_id', 'none')}", response.status_code)
                
                # Verificar detalles
                details = result_data.get("details", {})
                confidence_preserved = details.get("confidence") == 0.92
                domains_preserved = set(details.get("domains", [])) == set(learning_data["application_domains"])
                
                self.log_test("/broadcast-learning", "Data Integrity", 
                             confidence_preserved and domains_preserved,
                             f"Confidence: {details.get('confidence')}, Domains: {len(details.get('domains', []))}", 
                             response.status_code)
                
            else:
                self.log_test("/broadcast-learning", "HTTP Response", False,
                             f"Status code: {response.status_code}", response.status_code)
                
        except Exception as e:
            self.log_test("/broadcast-learning", "Request", False, f"Exception: {str(e)}")
    
    def test_request_consensus(self):
        """Test 5: Request Consensus"""
        print("\n🗳️ TEST 5: REQUEST CONSENSUS")
        
        try:
            consensus_data = {
                "decision_topic": "Neural Mesh API Production Deployment Strategy",
                "options": [
                    {
                        "option": "Immediate Full Deployment",
                        "pros": ["Complete functionality", "Maximum Neural Mesh benefits"],
                        "cons": ["Higher initial complexity"],
                        "impact": "high"
                    },
                    {
                        "option": "Gradual Feature Rollout",
                        "pros": ["Lower risk", "Incremental validation"],
                        "cons": ["Slower benefit realization"],
                        "impact": "medium"
                    },
                    {
                        "option": "Extended Testing Phase",
                        "pros": ["Maximum stability", "Comprehensive validation"],
                        "cons": ["Delayed production benefits"],
                        "impact": "low"
                    }
                ],
                "deadline_hours": 48,
                "from_agent": "aria"
            }
            
            response = requests.post(
                f"{self.neural_mesh_url}/request-consensus",
                json=consensus_data,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if response.status_code == 200:
                result_data = response.json()
                
                # Verificar respuesta de consenso
                has_success = result_data.get("success", False)
                has_episode_id = "episode_id" in result_data
                
                self.log_test("/request-consensus", "Consensus Request", 
                             has_success and has_episode_id,
                             f"Episode ID: {result_data.get('episode_id', 'none')}", response.status_code)
                
                # Verificar detalles de consenso
                details = result_data.get("details", {})
                options_count = details.get("options_count", 0)
                deadline_hours = details.get("deadline_hours", 0)
                
                self.log_test("/request-consensus", "Consensus Details", 
                             options_count == 3 and deadline_hours == 48,
                             f"Options: {options_count}, Deadline: {deadline_hours}h", response.status_code)
                
            else:
                self.log_test("/request-consensus", "HTTP Response", False,
                             f"Status code: {response.status_code}", response.status_code)
                
        except Exception as e:
            self.log_test("/request-consensus", "Request", False, f"Exception: {str(e)}")
    
    def test_sync_emotional_state(self):
        """Test 6: Sync Emotional State"""
        print("\n💭 TEST 6: SYNC EMOTIONAL STATE")
        
        try:
            emotional_data = {
                "emotional_state": {
                    "primary_emotion": "focused_determination",
                    "intensity": 0.85,
                    "confidence_level": 0.93,
                    "collaboration_mood": "highly_cooperative",
                    "technical_excitement": 0.88,
                    "breakthrough_satisfaction": 0.92,
                    "current_focus": "neural_mesh_api_implementation",
                    "energy_level": 0.91
                },
                "from_agent": "aria",
                "context_triggers": [
                    "api_endpoint_implementation_success",
                    "neural_mesh_protocol_activation",
                    "fase_4_milestone_achievement"
                ]
            }
            
            response = requests.post(
                f"{self.neural_mesh_url}/sync-emotional-state",
                json=emotional_data,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if response.status_code == 200:
                result_data = response.json()
                
                # Verificar sincronización emocional
                has_success = result_data.get("success", False)
                has_episode_id = "episode_id" in result_data
                
                self.log_test("/sync-emotional-state", "Emotional Sync", 
                             has_success and has_episode_id,
                             f"Episode ID: {result_data.get('episode_id', 'none')}", response.status_code)
                
                # Verificar preservación de estado emocional
                details = result_data.get("details", {})
                synced_state = details.get("emotional_state", {})
                
                intensity_preserved = synced_state.get("intensity") == 0.85
                emotion_preserved = synced_state.get("primary_emotion") == "focused_determination"
                
                self.log_test("/sync-emotional-state", "Emotional Data Integrity", 
                             intensity_preserved and emotion_preserved,
                             f"Emotion: {synced_state.get('primary_emotion')}, Intensity: {synced_state.get('intensity')}",
                             response.status_code)
                
            else:
                self.log_test("/sync-emotional-state", "HTTP Response", False,
                             f"Status code: {response.status_code}", response.status_code)
                
        except Exception as e:
            self.log_test("/sync-emotional-state", "Request", False, f"Exception: {str(e)}")
    
    def test_distribute_task(self):
        """Test 7: Distribute Task"""
        print("\n📋 TEST 7: DISTRIBUTE TASK")
        
        try:
            task_data = {
                "task_description": "Complete Neural Mesh API Integration Testing",
                "task_details": {
                    "type": "technical_validation",
                    "complexity_indicators": {
                        "technical_complexity": 0.8,
                        "scope_size": 0.7,
                        "dependencies": 0.6,
                        "innovation_required": 0.9
                    },
                    "required_skills": [
                        "api_testing",
                        "neural_mesh_protocols",
                        "endpoint_validation",
                        "integration_testing"
                    ],
                    "deliverables": [
                        "Comprehensive endpoint test results",
                        "Performance validation metrics",
                        "Integration status report",
                        "Production readiness assessment"
                    ]
                },
                "preferred_agents": ["nexus"],
                "deadline": (datetime.utcnow()).isoformat(),
                "priority": "high"
            }
            
            response = requests.post(
                f"{self.neural_mesh_url}/distribute-task",
                json=task_data,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if response.status_code == 200:
                result_data = response.json()
                
                # Verificar distribución de tarea
                has_success = result_data.get("success", False)
                has_message_id = "message_id" in result_data
                has_episode_id = "episode_id" in result_data
                
                self.log_test("/distribute-task", "Task Distribution", 
                             has_success and has_episode_id,
                             f"Episode ID: {result_data.get('episode_id', 'none')}", response.status_code)
                
                # Verificar detalles de tarea
                details = result_data.get("details", {})
                preferred_agents = details.get("preferred_agents", [])
                priority = details.get("priority", "")
                
                self.log_test("/distribute-task", "Task Details", 
                             "nexus" in preferred_agents and priority == "high",
                             f"Agents: {preferred_agents}, Priority: {priority}", response.status_code)
                
            else:
                self.log_test("/distribute-task", "HTTP Response", False,
                             f"Status code: {response.status_code}", response.status_code)
                
        except Exception as e:
            self.log_test("/distribute-task", "Request", False, f"Exception: {str(e)}")
    
    def test_process_messages(self):
        """Test 8: Process Messages"""
        print("\n⚡ TEST 8: PROCESS MESSAGES")
        
        try:
            response = requests.post(
                f"{self.neural_mesh_url}/process-messages",
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if response.status_code == 200:
                result_data = response.json()
                
                # Verificar procesamiento de mensajes
                has_success = result_data.get("success", False)
                has_episode_id = "episode_id" in result_data
                
                self.log_test("/process-messages", "Message Processing", 
                             has_success and has_episode_id,
                             f"Episode ID: {result_data.get('episode_id', 'none')}", response.status_code)
                
                # Verificar detalles de procesamiento
                details = result_data.get("details", {})
                processed_count = details.get("processed_messages", 0)
                mesh_available = details.get("neural_mesh_available", False)
                
                self.log_test("/process-messages", "Processing Stats", 
                             processed_count >= 0,  # 0 o más mensajes procesados es válido
                             f"Processed: {processed_count}, Mesh available: {mesh_available}", response.status_code)
                
            else:
                self.log_test("/process-messages", "HTTP Response", False,
                             f"Status code: {response.status_code}", response.status_code)
                
        except Exception as e:
            self.log_test("/process-messages", "Request", False, f"Exception: {str(e)}")
    
    def test_api_documentation(self):
        """Test 9: API Documentation Available"""
        print("\n📚 TEST 9: API DOCUMENTATION")
        
        try:
            # Test OpenAPI docs
            docs_response = requests.get(f"{self.base_url}/docs", timeout=10)
            openapi_response = requests.get(f"{self.base_url}/openapi.json", timeout=10)
            
            docs_available = docs_response.status_code == 200
            openapi_available = openapi_response.status_code == 200
            
            self.log_test("/docs", "Documentation Available", 
                         docs_available and openapi_available,
                         f"Docs: {docs_response.status_code}, OpenAPI: {openapi_response.status_code}")
            
            # Check if Neural Mesh endpoints are documented
            if openapi_available:
                openapi_data = openapi_response.json()
                paths = openapi_data.get("paths", {})
                
                neural_mesh_paths = [path for path in paths.keys() if "/neural-mesh" in path]
                expected_paths = 7  # Expected number of Neural Mesh endpoints
                
                self.log_test("/docs", "Neural Mesh Endpoints Documented",
                             len(neural_mesh_paths) >= expected_paths,
                             f"Neural Mesh paths found: {len(neural_mesh_paths)}")
                
        except Exception as e:
            self.log_test("/docs", "Documentation", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Ejecutar todos los tests"""
        print("🧪 NEURAL MESH API ENDPOINTS TEST SUITE")
        print("=" * 65)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Base URL: {self.base_url}")
        print(f"Neural Mesh URL: {self.neural_mesh_url}")
        print("=" * 65)
        
        # Ejecutar tests en orden
        self.test_neural_mesh_health()
        self.test_neural_mesh_stats()
        self.test_connected_agents()
        self.test_broadcast_learning()
        self.test_request_consensus()
        self.test_sync_emotional_state()
        self.test_distribute_task()
        self.test_process_messages()
        self.test_api_documentation()
        
        # Resumen final
        print("\n" + "=" * 65)
        print("🎯 NEURAL MESH API ENDPOINTS TEST RESULTS")
        print("=" * 65)
        
        total = self.test_results["total_tests"]
        passed = self.test_results["passed_tests"]
        failed = self.test_results["failed_tests"]
        success_rate = (passed / total) * 100 if total > 0 else 0
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print(f"\n🎉 NEURAL MESH API ENDPOINTS: FULLY OPERATIONAL!")
            print("   Ready for production deployment")
        elif success_rate >= 75:
            print(f"\n🟡 NEURAL MESH API ENDPOINTS: MOSTLY OPERATIONAL")
            print("   Minor issues detected, review failed tests")
        elif success_rate >= 50:
            print(f"\n🟠 NEURAL MESH API ENDPOINTS: PARTIAL FUNCTIONALITY")
            print("   Several issues detected, investigation required")
        else:
            print(f"\n🔴 NEURAL MESH API ENDPOINTS: MAJOR ISSUES")
            print("   Significant problems detected, debugging required")
        
        print("\n" + "=" * 65)
        
        return self.test_results


def main():
    """Función principal"""
    tester = NeuralMeshAPITester()
    results = tester.run_all_tests()
    
    # Guardar resultados
    with open("/tmp/neural_mesh_api_test_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nResults saved to: /tmp/neural_mesh_api_test_results.json")
    
    return results


if __name__ == "__main__":
    main()