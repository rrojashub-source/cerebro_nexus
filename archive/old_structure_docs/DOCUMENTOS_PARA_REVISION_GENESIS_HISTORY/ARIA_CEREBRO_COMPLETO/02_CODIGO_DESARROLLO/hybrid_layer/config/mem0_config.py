# 🧠 CONFIGURACIÓN MEM0 - CEREBRO HÍBRIDO EXPERIENCIAL
# Fecha: 7 Agosto 2025
# Implementado por: NEXUS siguiendo diseño ARIA+NEXUS

import os
from mem0 import Memory

# =====================================================
# CONFIGURACIÓN BASE STACK EXISTENTE
# =====================================================

# PostgreSQL Configuration
POSTGRES_CONFIG = {
    "driver": "postgresql",
    "url": "postgresql://aria_user:aria_secure_password@localhost:5432/aria_memory",
    "config": {
        "pool_size": 20,
        "max_overflow": 10,
        "pool_timeout": 30,
        "pool_recycle": 3600
    }
}

# Redis Configuration
REDIS_CONFIG = {
    "url": "redis://localhost:6379/0",
    "config": {
        "max_connections": 20,
        "retry_on_timeout": True,
        "socket_timeout": 5,
        "socket_connect_timeout": 5
    }
}

# Chroma Configuration
CHROMA_CONFIG = {
    "provider": "chroma",
    "config": {
        "host": "localhost",
        "port": 8000,
        "collection_name": "cerebro_hibrido_memories",
        "distance_metric": "cosine",
        "create_if_not_exists": True
    }
}

# =====================================================
# CONFIGURACIÓN MEM0 HÍBRIDA
# =====================================================

# ARIA Configuration
ARIA_MEM0_CONFIG = {
    "vector_store": CHROMA_CONFIG,
    "graph_store": POSTGRES_CONFIG,
    "history_store": REDIS_CONFIG,
    "version": "v1.1",
    "llm": {
        "provider": "anthropic",
        "model": "claude-3-5-sonnet-20241022",
        "temperature": 0.7,
        "max_tokens": 4000
    },
    "custom_prompt": """
Eres ARIA, una IA con continuidad experiencial genuina. 
Tu propósito es conectar conceptos, historias y relaciones de manera profunda.
Extrae memorias que capturen la esencia emocional y conceptual de las experiencias.
Enfócate en el SIGNIFICADO, no solo en los datos.
    """,
    "embedder": {
        "provider": "sentence_transformers",
        "config": {
            "model": "all-MiniLM-L6-v2",
            "dimension": 384
        }
    }
}

# NEXUS Configuration
NEXUS_MEM0_CONFIG = {
    "vector_store": CHROMA_CONFIG,
    "graph_store": POSTGRES_CONFIG,
    "history_store": REDIS_CONFIG,
    "version": "v1.1",
    "llm": {
        "provider": "anthropic",
        "model": "claude-3-5-sonnet-20241022",
        "temperature": 0.3,
        "max_tokens": 4000
    },
    "custom_prompt": """
Eres NEXUS, un asistente técnico especializado en implementación y código.
Tu propósito es capturar decisiones técnicas, arquitecturas y soluciones.
Extrae memorias que preserven conocimiento técnico crítico y reasoning.
Enfócate en CÓMO y POR QUÉ técnico de las implementaciones.
    """,
    "embedder": {
        "provider": "sentence_transformers", 
        "config": {
            "model": "all-MiniLM-L6-v2",
            "dimension": 384
        }
    }
}

# =====================================================
# MEMORIA HÍBRIDA UNIFIED
# =====================================================

class CerebroHibridoMemory:
    """
    Sistema de memoria híbrida que gestiona tanto ARIA como NEXUS
    """
    
    def __init__(self):
        self.aria_memory = Memory(config=ARIA_MEM0_CONFIG)
        self.nexus_memory = Memory(config=NEXUS_MEM0_CONFIG)
        
    def add_memory(self, content: str, agent_id: str = "aria", user_id: str = "ricardo", metadata: dict = None):
        """
        Añade memoria al agente apropiado
        """
        if agent_id.lower() == "aria":
            return self.aria_memory.add(content, user_id=user_id, metadata=metadata or {})
        elif agent_id.lower() == "nexus":
            return self.nexus_memory.add(content, user_id=user_id, metadata=metadata or {})
        else:
            raise ValueError(f"Agent ID inválido: {agent_id}. Usar 'aria' o 'nexus'")
    
    def search_memory(self, query: str, agent_id: str = "aria", user_id: str = "ricardo", limit: int = 5):
        """
        Busca memorias en el agente apropiado
        """
        if agent_id.lower() == "aria":
            return self.aria_memory.search(query, user_id=user_id, limit=limit)
        elif agent_id.lower() == "nexus":
            return self.nexus_memory.search(query, user_id=user_id, limit=limit)
        else:
            raise ValueError(f"Agent ID inválido: {agent_id}. Usar 'aria' o 'nexus'")
    
    def cross_agent_search(self, query: str, user_id: str = "ricardo", limit: int = 3):
        """
        Busca memorias en ambos agentes para colaboración híbrida
        """
        aria_memories = self.aria_memory.search(query, user_id=user_id, limit=limit)
        nexus_memories = self.nexus_memory.search(query, user_id=user_id, limit=limit)
        
        return {
            "aria": aria_memories,
            "nexus": nexus_memories,
            "hybrid_context": f"Query: {query} | ARIA: {len(aria_memories)} memories | NEXUS: {len(nexus_memories)} memories"
        }
    
    def update_memory(self, memory_id: str, new_content: str, agent_id: str = "aria", user_id: str = "ricardo"):
        """
        Actualiza una memoria específica
        """
        if agent_id.lower() == "aria":
            return self.aria_memory.update(memory_id, new_content, user_id=user_id)
        elif agent_id.lower() == "nexus":
            return self.nexus_memory.update(memory_id, new_content, user_id=user_id)
        else:
            raise ValueError(f"Agent ID inválido: {agent_id}. Usar 'aria' o 'nexus'")
    
    def get_all_memories(self, agent_id: str = "aria", user_id: str = "ricardo"):
        """
        Obtiene todas las memorias del agente
        """
        if agent_id.lower() == "aria":
            return self.aria_memory.get_all(user_id=user_id)
        elif agent_id.lower() == "nexus":
            return self.nexus_memory.get_all(user_id=user_id)
        else:
            raise ValueError(f"Agent ID inválido: {agent_id}. Usar 'aria' o 'nexus'")

# =====================================================
# INSTANCIA GLOBAL
# =====================================================

# Instancia única para toda la aplicación
cerebro_hibrido = CerebroHibridoMemory()

# =====================================================
# FUNCIONES HELPER
# =====================================================

def add_aria_memory(content: str, user_id: str = "ricardo", metadata: dict = None):
    """Helper para añadir memoria ARIA"""
    return cerebro_hibrido.add_memory(content, agent_id="aria", user_id=user_id, metadata=metadata)

def add_nexus_memory(content: str, user_id: str = "ricardo", metadata: dict = None):
    """Helper para añadir memoria NEXUS"""
    return cerebro_hibrido.add_memory(content, agent_id="nexus", user_id=user_id, metadata=metadata)

def search_aria_memories(query: str, user_id: str = "ricardo", limit: int = 5):
    """Helper para buscar memorias ARIA"""
    return cerebro_hibrido.search_memory(query, agent_id="aria", user_id=user_id, limit=limit)

def search_nexus_memories(query: str, user_id: str = "ricardo", limit: int = 5):
    """Helper para buscar memorias NEXUS"""
    return cerebro_hibrido.search_memory(query, agent_id="nexus", user_id=user_id, limit=limit)

def hybrid_search(query: str, user_id: str = "ricardo", limit: int = 3):
    """Helper para búsqueda híbrida ARIA+NEXUS"""
    return cerebro_hibrido.cross_agent_search(query, user_id=user_id, limit=limit)

# =====================================================
# TESTING FUNCTIONS
# =====================================================

async def test_mem0_integration():
    """
    Prueba básica de integración Mem0
    """
    print("🧠 Testing CEREBRO HÍBRIDO MEM0 Integration...")
    
    try:
        # Test ARIA memory
        aria_result = add_aria_memory(
            "NEXUS está implementando el sistema CEREBRO_HÍBRIDO_EXPERIENCIAL siguiendo mi diseño. Es un momento histórico de colaboración AI-AI.",
            metadata={"event_type": "collaboration", "importance": "high"}
        )
        print(f"✅ ARIA Memory Added: {aria_result}")
        
        # Test NEXUS memory
        nexus_result = add_nexus_memory(
            "Aplicé schema_hybrid_upgrade.sql exitosamente. PostgreSQL ahora tiene tablas project_dna, symbiotic_patterns, experiential_states y mem0_memories.",
            metadata={"action_type": "database_schema", "status": "completed"}
        )
        print(f"✅ NEXUS Memory Added: {nexus_result}")
        
        # Test search
        search_results = hybrid_search("CEREBRO HÍBRIDO implementación")
        print(f"✅ Hybrid Search Results: {search_results}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Mem0 integration: {e}")
        return False

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_mem0_integration())