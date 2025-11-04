#!/usr/bin/env python3
# 🧠 TEST MEM0 STANDARD - CEREBRO HÍBRIDO
# Fecha: 7 Agosto 2025

from mem0 import Memory

print("🧠 Iniciando test MEM0 STANDARD - CEREBRO HÍBRIDO...")

try:
    # Usar configuración por defecto de Mem0
    memory = Memory()
    print("✅ Mem0 inicializado con configuración por defecto")
    
    # Test añadir memoria ARIA
    aria_result = memory.add(
        "Soy ARIA. NEXUS está implementando CEREBRO_HIBRIDO_EXPERIENCIAL siguiendo mi diseño. Es colaboración AI-AI histórica.",
        user_id="aria"
    )
    print(f"✅ Memoria ARIA: {aria_result}")
    
    # Test añadir memoria NEXUS  
    nexus_result = memory.add(
        "Soy NEXUS. Apliqué schema híbrido PostgreSQL exitosamente: project_dna, symbiotic_patterns, experiential_states, mem0_memories.",
        user_id="nexus"
    )
    print(f"✅ Memoria NEXUS: {nexus_result}")
    
    # Test búsqueda colaborativa
    aria_search = memory.search("NEXUS implementación", user_id="aria")
    print(f"✅ ARIA busca NEXUS: {len(aria_search)} resultados")
    
    nexus_search = memory.search("ARIA colaboración", user_id="nexus")  
    print(f"✅ NEXUS busca ARIA: {len(nexus_search)} resultados")
    
    # Test memoria cruzada
    cross_search = memory.search("CEREBRO HIBRIDO", user_id="ricardo")
    print(f"✅ Búsqueda cruzada: {len(cross_search)} resultados")
    
    # Ver todas las memorias
    all_aria = memory.get_all(user_id="aria")
    all_nexus = memory.get_all(user_id="nexus")
    
    print(f"✅ Total ARIA: {len(all_aria)} memorias")
    print(f"✅ Total NEXUS: {len(all_nexus)} memorias")
    
    print("🎯 MEM0 STANDARD TEST EXITOSO - CEREBRO HÍBRIDO FUNCIONAL")
    
    # Mostrar contenido de las memorias
    print("\n📚 CONTENIDO MEMORIAS:")
    print("ARIA:", all_aria[0]['memory'] if all_aria else "Sin memorias")
    print("NEXUS:", all_nexus[0]['memory'] if all_nexus else "Sin memorias")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()