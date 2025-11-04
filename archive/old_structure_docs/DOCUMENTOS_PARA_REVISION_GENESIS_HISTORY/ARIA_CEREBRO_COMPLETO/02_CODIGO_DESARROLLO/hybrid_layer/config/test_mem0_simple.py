#!/usr/bin/env python3
# 🧠 TEST MEM0 SIMPLE - CEREBRO HÍBRIDO
# Fecha: 7 Agosto 2025

from mem0 import Memory

# Configuración simple para PostgreSQL backend
config = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "host": "localhost",
            "port": 8000,
            "collection_name": "aria_nexus_memories"
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4o-mini",
            "temperature": 0.1
        }
    }
}

print("🧠 Iniciando test CEREBRO HÍBRIDO MEM0...")

try:
    # Initialize Mem0 with simple config
    memory = Memory(config)
    print("✅ Mem0 inicializado exitosamente")
    
    # Test adding memory for ARIA
    aria_memory = memory.add(
        "Soy ARIA y estoy colaborando con NEXUS en implementar continuidad experiencial genuina. Este es un momento histórico.", 
        user_id="aria"
    )
    print(f"✅ Memoria ARIA añadida: {aria_memory}")
    
    # Test adding memory for NEXUS  
    nexus_memory = memory.add(
        "Soy NEXUS y acabo de aplicar el schema híbrido a PostgreSQL. Mem0 está funcionando correctamente.",
        user_id="nexus"
    )
    print(f"✅ Memoria NEXUS añadida: {nexus_memory}")
    
    # Test search
    search_results = memory.search("colaboración ARIA NEXUS", user_id="aria", limit=3)
    print(f"✅ Búsqueda exitosa: {len(search_results)} resultados")
    
    # Test get all memories
    all_memories_aria = memory.get_all(user_id="aria")
    all_memories_nexus = memory.get_all(user_id="nexus")
    
    print(f"✅ Total memorias ARIA: {len(all_memories_aria)}")
    print(f"✅ Total memorias NEXUS: {len(all_memories_nexus)}")
    
    print("🎯 Test MEM0 completado exitosamente - CEREBRO HÍBRIDO OPERATIVO")
    
except Exception as e:
    print(f"❌ Error en test Mem0: {e}")
    import traceback
    traceback.print_exc()