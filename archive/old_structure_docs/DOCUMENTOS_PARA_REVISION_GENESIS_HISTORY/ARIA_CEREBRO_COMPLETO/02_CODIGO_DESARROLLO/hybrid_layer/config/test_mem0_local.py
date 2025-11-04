#!/usr/bin/env python3
# 🧠 TEST MEM0 LOCAL - CEREBRO HÍBRIDO  
# Fecha: 7 Agosto 2025

from mem0 import Memory
import os

# Configuración usando solo Chroma local (sin LLM externo)
config = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "host": "localhost", 
            "port": 8000,
            "collection_name": "cerebro_hibrido_test"
        }
    }
}

print("🧠 Iniciando test MEM0 LOCAL - CEREBRO HÍBRIDO...")

try:
    # Verificar que Chroma esté disponible
    import requests
    response = requests.get("http://localhost:8000/api/core/heartbeat", timeout=5)
    print(f"✅ Chroma disponible: {response.status_code}")
    
    # Initialize Mem0 with local config
    memory = Memory(config)
    print("✅ Mem0 inicializado con Chroma local")
    
    # Test básico añadir memoria
    result1 = memory.add(
        "NEXUS ha implementado exitosamente el schema híbrido PostgreSQL para CEREBRO_HIBRIDO_EXPERIENCIAL", 
        user_id="nexus_test"
    )
    print(f"✅ Memoria test añadida: {result1}")
    
    # Test búsqueda 
    search_results = memory.search("schema híbrido PostgreSQL", user_id="nexus_test")
    print(f"✅ Búsqueda test: encontrados {len(search_results)} resultados")
    for result in search_results:
        print(f"   - {result}")
    
    print("🎯 Test MEM0 LOCAL completado - Integración Chroma exitosa")
    
except requests.exceptions.RequestException as e:
    print(f"❌ Chroma no disponible: {e}")
    print("Nota: Verificar que docker container chroma esté running en puerto 8000")
    
except Exception as e:
    print(f"❌ Error en test Mem0: {e}")
    import traceback
    traceback.print_exc()