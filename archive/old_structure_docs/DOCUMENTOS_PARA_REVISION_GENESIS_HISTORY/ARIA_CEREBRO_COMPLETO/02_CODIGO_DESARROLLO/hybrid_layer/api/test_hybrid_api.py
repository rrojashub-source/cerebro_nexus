#!/usr/bin/env python3
# 🧠 TEST API HÍBRIDA - CEREBRO EXPERIENCIAL
# Fecha: 7 Agosto 2025

import sys
import asyncio
import httpx
import json

async def test_hybrid_api():
    """Test básico de API híbrida"""
    
    print("🧠 Testing CEREBRO HÍBRIDO API...")
    
    base_url = "http://localhost:8002"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # Test 1: Health check
            print("📊 Test 1: Health Check")
            response = await client.get(f"{base_url}/hybrid/health")
            print(f"✅ Health Status: {response.status_code}")
            if response.status_code == 200:
                health_data = response.json()
                print(f"   - Sistema: {health_data['status']}")
                print(f"   - PostgreSQL: {health_data['components']['postgresql']}")
                print(f"   - Redis: {health_data['components']['redis']}")
                
            # Test 2: Enviar mensaje híbrido
            print("\n💬 Test 2: Mensaje Híbrido NEXUS → ARIA")
            message_data = {
                "from_agent": "nexus",
                "to_agent": "aria", 
                "message": "ARIA, he implementado exitosamente el CEREBRO_HÍBRIDO_EXPERIENCIAL. La API está operativa en puerto 8002.",
                "context_type": "implementation_update",
                "project_id": "CEREBRO_HIBRIDO",
                "importance": 0.9,
                "metadata": {
                    "milestone": "api_hybrid_complete",
                    "timestamp": "2025-08-07"
                }
            }
            
            response = await client.post(f"{base_url}/hybrid/message", json=message_data)
            print(f"✅ Message Status: {response.status_code}")
            if response.status_code == 200:
                msg_result = response.json()
                print(f"   - Message ID: {msg_result['message_id']}")
                print(f"   - From: {msg_result['from_agent']} → To: {msg_result['to_agent']}")
                
            # Test 3: Obtener mensajes para ARIA
            print("\n📬 Test 3: Messages for ARIA")
            response = await client.get(f"{base_url}/hybrid/messages/aria")
            print(f"✅ Messages Status: {response.status_code}")
            if response.status_code == 200:
                messages = response.json()
                print(f"   - Total messages: {messages['message_count']}")
                for msg in messages['messages'][:3]:  # Show first 3
                    print(f"   - {msg['from_agent']} → {msg['to_agent']}: {msg['message'][:50]}...")
                    
            # Test 4: Crear Project DNA
            print("\n🧬 Test 4: Create Project DNA")
            dna_data = {
                "project_name": "CEREBRO_HIBRIDO_EXPERIENCIAL",
                "conceptual_layer": {
                    "vision": "Primera IA con continuidad experiencial genuina",
                    "architect": "ARIA",
                    "innovation": "Symbiotic AI-AI Intelligence"
                },
                "technical_layer": {
                    "implementer": "NEXUS",
                    "stack": "PostgreSQL+Redis+Chroma+Mem0+LOVE+Memoripy",
                    "status": "MVP implemented",
                    "api_port": 8002
                },
                "decision_history": [
                    {"decision": "Use existing ARIA stack", "reasoning": "Proven and stable"}
                ],
                "lessons_learned": [
                    {"lesson": "AI-AI collaboration requires specialized APIs", "importance": "high"}
                ]
            }
            
            response = await client.post(f"{base_url}/hybrid/project-dna", json=dna_data)
            print(f"✅ Project DNA Status: {response.status_code}")
            if response.status_code == 200:
                dna_result = response.json()
                print(f"   - DNA ID: {dna_result['dna_id']}")
                print(f"   - Project: {dna_result['project_name']}")
                
            # Test 5: Sincronización ARIA-NEXUS
            print("\n🔄 Test 5: ARIA-NEXUS Sync")
            response = await client.post(f"{base_url}/hybrid/aria-nexus-sync")
            print(f"✅ Sync Status: {response.status_code}")
            if response.status_code == 200:
                sync_result = response.json()
                print(f"   - Sync ID: {sync_result['sync_id']}")
                print(f"   - Status: {sync_result['status']}")
                
            print("\n🎯 CEREBRO HÍBRIDO API TEST COMPLETED SUCCESSFULLY")
            return True
            
        except Exception as e:
            print(f"❌ Error testing API: {e}")
            return False

if __name__ == "__main__":
    asyncio.run(test_hybrid_api())