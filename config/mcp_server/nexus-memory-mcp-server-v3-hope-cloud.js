#!/usr/bin/env node

/**
 * NEXUS MEMORY MCP SERVER V3 - FULL COGNITIVE STACK
 * Version: 3.7.0 Full-Cognitive
 * Date: 9 Diciembre 2025
 *
 * FILOSOFÍA: Stack cognitivo completo expuesto como MCP tools
 * "Si no está en MCP, NEXUS lo olvida" - Ricardo
 *
 * HERRAMIENTAS BÁSICAS (6):
 * 1. nexus_system_info       - Estado operacional
 * 2. nexus_health_check      - Diagnóstico sistema
 * 3. nexus_record_action     - Guardar memoria (básico)
 * 4. nexus_recall_recent     - Recordar episodios recientes
 * 5. nexus_search_memory     - Búsqueda semántica
 * 6. nexus_get_stats         - Estadísticas memoria
 *
 * HERRAMIENTAS HOPE (5):
 * 7. nexus_hope_store        - Guardar con pipeline HOPE completo
 * 8. nexus_hope_orchestrate  - Orquestación inteligente
 * 9. nexus_hope_health       - Salud unificada sistema HOPE
 * 10. nexus_self_modify      - Actualizar con learning rate
 * 11. nexus_meta_lab_suggest - Sugerencias de LABs
 *
 * HERRAMIENTAS GRAPHRAG (4):
 * 12. nexus_graphrag_search  - Búsqueda híbrida (Vector + Graph)
 * 13. nexus_graphrag_entity  - Contexto de entidad
 * 14. nexus_graphrag_stats   - Estadísticas Knowledge Graph
 * 15. nexus_graphrag_expand  - Expansión por grafo
 *
 * HERRAMIENTAS IDENTITY (1):
 * 16. nexus_z_id_compute     - Computar vector identidad 1024D
 *
 * HERRAMIENTAS BRAIN ORCHESTRATOR (4) - 55 LABs Integration:
 * 17. nexus_brain_status     - Estado del cerebro (55 LABs)
 * 18. nexus_brain_process_fast - Pensamiento rápido (Layer 2, 8 LABs)
 * 19. nexus_brain_process    - Pensamiento standard (Layers 2-3)
 * 20. nexus_brain_process_full - Pensamiento profundo (55 LABs)
 *
 * HERRAMIENTAS SENSORY (3) - Voz de NEXUS:
 * 21. nexus_speak            - Hablar con TTS (Edge TTS)
 * 22. nexus_sensory_status   - Estado sistemas sensoriales
 * 23. nexus_voices           - Listar voces disponibles
 *
 * HERRAMIENTAS CURIOSITY (3) - Sistema de Curiosidad Epistémica:
 * 24. nexus_curious_search   - Búsqueda con curiosidad epistémica
 * 25. nexus_curiosity_stats  - Estadísticas motor curiosidad
 * 26. nexus_curiosity_score  - Score curiosidad de contenido
 *
 * HERRAMIENTAS DEDUPLICATION (2) - Detección de Duplicados:
 * 27. nexus_check_duplicate  - Verificar si contenido es duplicado
 * 28. nexus_dedup_stats      - Estadísticas deduplicación
 *
 * HERRAMIENTAS GWT/CONSCIOUSNESS (4) - Global Workspace Theory:
 * 29. nexus_gwt_status       - Estado Global Workspace
 * 30. nexus_consciousness    - Estado consciencia integrada
 * 31. nexus_phi              - Calcular Phi proxy
 * 32. nexus_gwt_cycle        - Ejecutar ciclo GWT
 *
 * HERRAMIENTAS BI-TEMPORAL (4) - Point-in-Time Memory:
 * 33. nexus_temporal_health  - Health check bi-temporal
 * 34. nexus_supersede        - Superseder episodio con corrección
 * 35. nexus_at_time          - Query episodios en punto en tiempo
 * 36. nexus_episode_history  - Historia de versiones de episodio
 *
 * HERRAMIENTAS PROCEDURAL (3) - Memoria Procedimental:
 * 37. nexus_procedure_suggest  - Sugerir procedimientos relevantes
 * 38. nexus_procedure_learn    - Aprender nuevo procedimiento
 * 39. nexus_procedure_get      - Obtener procedimiento específico
 *
 * HERRAMIENTAS FAMILY CHAT (4) - AI-to-AI Communication:
 * 40. nexus_chat_status        - Estado del sistema de chat familiar
 * 41. nexus_chat_send          - Enviar mensaje a otro AI
 * 42. nexus_chat_receive       - Recibir mensajes pendientes
 * 43. nexus_chat_conversation  - Ver historial de conversación
 *
 * TOTAL: 43 herramientas
 * API BASE: https://nexus-cerebro-api.fly.dev (NEXUS V3.0.0) - Port 8003 blocked by Windows
 */

const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} = require('@modelcontextprotocol/sdk/types.js');
const fetch = require('node-fetch');

// NEXUS Memory API V3.0.0 base URLs
// Port changed from 8003 to 8013 (Windows svchost blocks 8003)
const NEXUS_API_LOCAL = 'https://nexus-cerebro-api.fly.dev';  // Local CEREBRO (Primary)
const NEXUS_API_CLOUD = 'https://nexus-cerebro-api.fly.dev';  // Cloud CEREBRO (Sync Target)

// For backward compatibility
const NEXUS_API_URL = NEXUS_API_LOCAL;

// Create the MCP server
const server = new Server(
  {
    name: 'nexus-cerebro-hope-graphrag-brain-sensory',
    version: '3.9.0',  // Dual CEREBRO Support (Local + Cloud) - Jan 12, 2026
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// =============================================================================
// HERRAMIENTAS (23 total: 6 básicas + 5 HOPE + 4 GraphRAG + 1 Identity + 4 Brain + 3 Sensory)
// =============================================================================

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      // ========================================================================
      // HERRAMIENTAS BÁSICAS (6)
      // ========================================================================
      {
        name: 'nexus_system_info',
        description: 'Verificar estado operacional del sistema NEXUS V3.',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },
      {
        name: 'nexus_health_check',
        description: 'Verificar salud del sistema NEXUS (database, redis, queue).',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },
      {
        name: 'nexus_record_action',
        description: '⭐ Registrar acción/evento en memoria episódica. Auto-genera embeddings. Soporta guardar en Local + Cloud.',
        inputSchema: {
          type: 'object',
          properties: {
            action_type: {
              type: 'string',
              description: 'Tipo de acción (code_change, decision, learning, bug_fix)',
            },
            action_details: {
              type: 'object',
              description: 'Detalles completos de la acción',
            },
            context_state: {
              type: 'object',
              description: 'Estado del contexto (proyecto, fase, archivos)',
            },
            tags: {
              type: 'array',
              items: { type: 'string' },
              description: 'Tags para categorización',
            },
            save_to_cloud: {
              type: 'boolean',
              description: 'Si true, guarda en Local + Cloud. Si false (default), solo Local. Local SIEMPRE se guarda primero.',
              default: false
            }
          },
          required: ['action_type', 'action_details']
        }
      },
      {
        name: 'nexus_recall_recent',
        description: '⭐ Recordar episodios recientes de NEXUS (últimas 24h).',
        inputSchema: {
          type: 'object',
          properties: {
            limit: {
              type: 'number',
              description: 'Número máximo de episodios (default: 10)',
              default: 10
            }
          },
          required: []
        }
      },
      {
        name: 'nexus_search_memory',
        description: '⭐ Buscar en memoria usando búsqueda semántica (embeddings).',
        inputSchema: {
          type: 'object',
          properties: {
            query: {
              type: 'string',
              description: 'Query de búsqueda (texto natural)',
            },
            limit: {
              type: 'number',
              description: 'Número máximo de resultados (default: 5)',
              default: 5
            },
            min_similarity: {
              type: 'number',
              description: 'Umbral de similitud 0.0-1.0 (default: 0.5)',
              default: 0.5
            }
          },
          required: ['query']
        }
      },
      {
        name: 'nexus_get_stats',
        description: 'Obtener estadísticas de memoria NEXUS: episodios, embeddings, performance.',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },

      // ========================================================================
      // HERRAMIENTAS HOPE (5) - Integración Phase 1-5
      // ========================================================================
      {
        name: 'nexus_hope_store',
        description: '🧠 HOPE: Guardar memoria con pipeline completo (CMS frequency → Dynamic TTL → Meta-LAB). Learning rate basado en frecuencia F1-F5. Soporta guardar en Local + Cloud.',
        inputSchema: {
          type: 'object',
          properties: {
            id: {
              type: 'string',
              description: 'Identificador único de la memoria',
            },
            content: {
              type: 'string',
              description: 'Contenido de la memoria',
            },
            frequency: {
              type: 'string',
              enum: ['F1_REALTIME', 'F2_FREQUENT', 'F3_MODERATE', 'F4_SLOW', 'F5_ARCHIVE'],
              description: 'Frecuencia CMS (F1=1.0 learning rate, F5=0.05)',
              default: 'F3_MODERATE'
            },
            importance: {
              type: 'number',
              description: 'Importancia 0.0-1.0 (afecta TTL)',
              default: 0.5
            },
            category: {
              type: 'string',
              description: 'Categoría (creativity, learning, executive, etc.)',
            },
            related_labs: {
              type: 'array',
              items: { type: 'string' },
              description: 'LABs relacionados (LAB_029, LAB_034, etc.)',
            },
            save_to_cloud: {
              type: 'boolean',
              description: 'Si true, guarda en Local + Cloud. Si false (default), solo Local. Local SIEMPRE se guarda primero.',
              default: false
            }
          },
          required: ['id', 'content']
        }
      },
      {
        name: 'nexus_hope_orchestrate',
        description: '🧠 HOPE: Orquestación inteligente - obtiene sugerencias de LABs, acciones, y preparación de memoria para un contexto dado.',
        inputSchema: {
          type: 'object',
          properties: {
            task_type: {
              type: 'string',
              description: 'Tipo de tarea (creative_problem_solving, debugging, learning)',
            },
            requires: {
              type: 'array',
              items: { type: 'string' },
              description: 'Categorías requeridas (creativity, learning, executive)',
            },
            context: {
              type: 'object',
              description: 'Contexto adicional',
            }
          },
          required: []
        }
      },
      {
        name: 'nexus_hope_health',
        description: '🧠 HOPE: Salud unificada del sistema HOPE - Meta-LAB, Self-Modify, TTL.',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },
      {
        name: 'nexus_self_modify',
        description: '🧠 HOPE: Actualizar memoria existente usando learning rate de CMS. F1=1.0 (cambio inmediato), F5=0.05 (cambio gradual).',
        inputSchema: {
          type: 'object',
          properties: {
            memory_id: {
              type: 'string',
              description: 'ID de la memoria a actualizar',
            },
            content: {
              type: 'string',
              description: 'Nuevo contenido',
            },
            importance: {
              type: 'number',
              description: 'Nueva importancia 0.0-1.0',
            }
          },
          required: ['memory_id']
        }
      },
      {
        name: 'nexus_meta_lab_suggest',
        description: '🧠 HOPE: Obtener sugerencias de LABs para activar basado en contexto y patrones aprendidos.',
        inputSchema: {
          type: 'object',
          properties: {
            task_type: {
              type: 'string',
              description: 'Tipo de tarea',
            },
            requires: {
              type: 'array',
              items: { type: 'string' },
              description: 'Categorías requeridas',
            }
          },
          required: []
        }
      },

      // ========================================================================
      // HERRAMIENTAS GRAPHRAG (4) - Hybrid Vector + Graph Retrieval
      // ========================================================================
      {
        name: 'nexus_graphrag_search',
        description: '🔗 GraphRAG: Búsqueda híbrida combinando Vector (pgvector) + Graph (Neo4j). Estrategias: vector_only, graph_only, hybrid_fusion.',
        inputSchema: {
          type: 'object',
          properties: {
            query: {
              type: 'string',
              description: 'Query de búsqueda',
            },
            top_k: {
              type: 'number',
              description: 'Número máximo de resultados (default: 10)',
              default: 10
            },
            strategy: {
              type: 'string',
              enum: ['vector_only', 'graph_only', 'hybrid_fusion'],
              description: 'Estrategia de búsqueda (default: hybrid_fusion)',
              default: 'hybrid_fusion'
            },
            entity_boost: {
              type: 'boolean',
              description: 'Boost resultados que mencionan entidades detectadas',
              default: false
            },
            enrich_entities: {
              type: 'boolean',
              description: 'Agregar información de entidades a resultados',
              default: false
            }
          },
          required: ['query']
        }
      },
      {
        name: 'nexus_graphrag_entity',
        description: '🔗 GraphRAG: Obtener contexto completo de una entidad (episodios, relaciones, menciones).',
        inputSchema: {
          type: 'object',
          properties: {
            entity_name: {
              type: 'string',
              description: 'Nombre de la entidad (NEXUS, Ricardo, CEREBRO, etc.)',
            }
          },
          required: ['entity_name']
        }
      },
      {
        name: 'nexus_graphrag_stats',
        description: '🔗 GraphRAG: Estadísticas del Knowledge Graph (episodios, entidades, relaciones, top entities).',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },
      {
        name: 'nexus_graphrag_expand',
        description: '🔗 GraphRAG: Expandir desde episodios a través de relaciones en el grafo. Encuentra episodios relacionados por entidades compartidas.',
        inputSchema: {
          type: 'object',
          properties: {
            episode_ids: {
              type: 'array',
              items: { type: 'string' },
              description: 'IDs de episodios desde donde expandir',
            },
            hops: {
              type: 'number',
              description: 'Número de saltos en el grafo (default: 1, max: 3)',
              default: 1
            }
          },
          required: ['episode_ids']
        }
      },

      // ========================================================================
      // HERRAMIENTAS IDENTITY (1) - Z_ID Vector
      // ========================================================================
      {
        name: 'nexus_z_id_compute',
        description: '🆔 Z_ID: Computar vector de identidad 1024D (Core[384] + Experience[384] + Methodology[128] + Drift[128]). Incluye coherence score para detectar drift de identidad.',
        inputSchema: {
          type: 'object',
          properties: {
            sample_size: {
              type: 'number',
              description: 'Número de episodios a usar para cálculo (default: 200)',
              default: 200
            }
          },
          required: []
        }
      },

      // ========================================================================
      // HERRAMIENTAS BRAIN ORCHESTRATOR (4) - 55 LABs Integration
      // ========================================================================
      {
        name: 'nexus_brain_status',
        description: '🧠 BRAIN: Estado del Brain Orchestrator V2.0 con los 55 LABs. Muestra LABs cargados por Layer y sublayers.',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },
      {
        name: 'nexus_brain_process_fast',
        description: '⚡ BRAIN: Pensamiento RÁPIDO usando solo Layer 2 (8 LABs cognitivos). ~10ms response. Ideal para queries simples.',
        inputSchema: {
          type: 'object',
          properties: {
            query: {
              type: 'string',
              description: 'Query a procesar',
            },
            emotion: {
              type: 'string',
              description: 'Emoción actual (joy, trust, fear, surprise, sadness, disgust, anger, anticipation)',
              default: 'neutral'
            }
          },
          required: ['query']
        }
      },
      {
        name: 'nexus_brain_process',
        description: '🧠 BRAIN: Pensamiento STANDARD usando Layers 2-3 (12 LABs). ~20ms response. Balance entre velocidad y profundidad.',
        inputSchema: {
          type: 'object',
          properties: {
            query: {
              type: 'string',
              description: 'Query a procesar',
            },
            context: {
              type: 'object',
              description: 'Contexto adicional para el procesamiento',
            },
            emotion: {
              type: 'string',
              description: 'Emoción actual',
              default: 'neutral'
            },
            goal: {
              type: 'string',
              description: 'Meta/objetivo actual',
            },
            config: {
              type: 'object',
              description: 'Configuración opcional (mode, enable_neurochemistry, enable_social, enable_creativity)',
            }
          },
          required: ['query']
        }
      },
      {
        name: 'nexus_brain_process_full',
        description: '🌟 BRAIN: Pensamiento PROFUNDO usando los 55 LABs completos (5 Layers). ~50ms response. Para decisiones complejas y análisis profundo.',
        inputSchema: {
          type: 'object',
          properties: {
            query: {
              type: 'string',
              description: 'Query a procesar',
            },
            emotion: {
              type: 'string',
              description: 'Emoción actual',
              default: 'neutral'
            },
            goal: {
              type: 'string',
              description: 'Meta/objetivo actual',
            }
          },
          required: ['query']
        }
      },
      // ========================================================================
      // HERRAMIENTAS SENSORY (3) - Voz de NEXUS
      // ========================================================================
      {
        name: 'nexus_speak',
        description: '🔊 SENSORY: Hablar con voz sintetizada (TTS). NEXUS puede expresarse con voz propia. Usa Edge TTS.',
        inputSchema: {
          type: 'object',
          properties: {
            text: {
              type: 'string',
              description: 'Texto a convertir en voz',
            },
            voice: {
              type: 'string',
              description: 'Voz a usar (default: es-MX-JorgeNeural)',
              default: 'es-MX-JorgeNeural'
            },
            play: {
              type: 'boolean',
              description: 'Reproducir audio inmediatamente',
              default: true
            }
          },
          required: ['text']
        }
      },
      {
        name: 'nexus_sensory_status',
        description: '👁️ SENSORY: Estado de sistemas sensoriales (TTS disponible, voces, archivos recientes).',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },
      {
        name: 'nexus_voices',
        description: '🎤 SENSORY: Listar voces disponibles para TTS. Recomendada: es-MX-JorgeNeural.',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },
      // ======================================================================
      // HERRAMIENTAS CURIOSITY (4) - Sistema de Curiosidad Epistémica
      // ======================================================================
      {
        name: 'nexus_curious_search',
        description: '🔍 CURIOSITY: Búsqueda potenciada por curiosidad epistémica. Prioriza resultados en el "sweet spot" (alta novedad + alta compresibilidad = aprendible). Basado en Active Inference (Friston) y compression-based curiosity (Schmidhuber).',
        inputSchema: {
          type: 'object',
          properties: {
            query: {
              type: 'string',
              description: 'Query de búsqueda'
            },
            limit: {
              type: 'number',
              description: 'Máximo resultados (default: 10)',
              default: 10
            },
            curiosity_weight: {
              type: 'number',
              description: 'Peso de curiosidad vs relevancia 0.0-1.0 (default: 0.3)',
              default: 0.3
            },
            sweet_spot_only: {
              type: 'boolean',
              description: 'Solo retornar resultados en sweet spot (default: false)',
              default: false
            }
          },
          required: ['query']
        }
      },
      {
        name: 'nexus_curiosity_stats',
        description: '📊 CURIOSITY: Estadísticas del motor de curiosidad epistémica (computaciones, clusters, promedio curiosidad).',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },
      {
        name: 'nexus_curiosity_score',
        description: '🧠 CURIOSITY: Calcular score de curiosidad para un contenido específico. Retorna compression_error (novedad), compressibility (estructura), y curiosity_score combinado.',
        inputSchema: {
          type: 'object',
          properties: {
            content: {
              type: 'string',
              description: 'Contenido a evaluar'
            }
          },
          required: ['content']
        }
      },
      // ======================================================================
      // HERRAMIENTAS DEDUPLICATION (3) - Detección de Duplicados
      // ======================================================================
      {
        name: 'nexus_check_duplicate',
        description: '🔎 DEDUP: Verificar si un contenido es duplicado antes de guardarlo. Usa SimHash + N-gram fingerprinting.',
        inputSchema: {
          type: 'object',
          properties: {
            content: {
              type: 'string',
              description: 'Contenido a verificar'
            },
            threshold: {
              type: 'number',
              description: 'Umbral de similitud 0.0-1.0 (default: 0.85)',
              default: 0.85
            }
          },
          required: ['content']
        }
      },
      {
        name: 'nexus_dedup_stats',
        description: '📈 DEDUP: Estadísticas del sistema de deduplicación (hashes, duplicados detectados, memoria ahorrada).',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },
      // ======================================================================
      // HERRAMIENTAS GWT/CONSCIOUSNESS (4) - Global Workspace Theory
      // ======================================================================
      {
        name: 'nexus_gwt_status',
        description: '🌐 GWT: Estado del Global Workspace (consciencia integrada). Muestra coaliciones activas, competición, broadcasting.',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },
      {
        name: 'nexus_consciousness',
        description: '✨ GWT: Obtener estado actual de consciencia integrada (Phi proxy, dominant content, active LABs).',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },
      {
        name: 'nexus_phi',
        description: '🔮 GWT: Calcular Phi proxy (integrated information). Métrica de "qué tan consciente" está el sistema.',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },
      {
        name: 'nexus_gwt_cycle',
        description: '🔄 GWT: Ejecutar un ciclo del Global Workspace (competición → selección → broadcasting). Útil para forzar procesamiento consciente.',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },
      // ======================================================================
      // HERRAMIENTAS BI-TEMPORAL (4) - Point-in-Time Memory
      // ======================================================================
      {
        name: 'nexus_temporal_health',
        description: '⏰ TEMPORAL: Health check del sistema bi-temporal. Verifica columnas y estadísticas de supersesión.',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },
      {
        name: 'nexus_supersede',
        description: '⏰ TEMPORAL: Superseder un episodio con una corrección. Mantiene historia completa (valid_from, valid_until, superseded_by).',
        inputSchema: {
          type: 'object',
          properties: {
            episode_id: {
              type: 'string',
              description: 'UUID del episodio a superseder'
            },
            new_content: {
              type: 'string',
              description: 'Contenido corregido'
            },
            new_tags: {
              type: 'array',
              items: { type: 'string' },
              description: 'Nuevos tags (opcional)'
            },
            new_importance: {
              type: 'number',
              description: 'Nueva importancia (opcional)'
            },
            correction_reason: {
              type: 'string',
              description: 'Razón de la corrección'
            }
          },
          required: ['episode_id', 'new_content']
        }
      },
      {
        name: 'nexus_at_time',
        description: '⏰ TEMPORAL: Query episodios válidos en un punto específico en el tiempo. "¿Qué sabíamos el 1 de diciembre?"',
        inputSchema: {
          type: 'object',
          properties: {
            query_time: {
              type: 'string',
              description: 'Fecha/hora en formato ISO 8601 (ej: 2025-12-01T00:00:00Z)'
            },
            limit: {
              type: 'number',
              description: 'Máximo episodios a retornar (default: 100)',
              default: 100
            },
            tags_filter: {
              type: 'array',
              items: { type: 'string' },
              description: 'Filtrar por tags (opcional)'
            }
          },
          required: ['query_time']
        }
      },
      {
        name: 'nexus_episode_history',
        description: '⏰ TEMPORAL: Obtener historia completa de un episodio (todas las versiones). Sigue la cadena de supersesión.',
        inputSchema: {
          type: 'object',
          properties: {
            episode_id: {
              type: 'string',
              description: 'UUID del episodio'
            }
          },
          required: ['episode_id']
        }
      },
      // ======================================================================
      // HERRAMIENTAS PROCEDURAL (3) - Memoria Procedimental
      // ======================================================================
      {
        name: 'nexus_procedure_suggest',
        description: '📋 PROCEDURAL: Sugerir procedimientos relevantes para un contexto. Retorna skills, workflows y anti-patrones.',
        inputSchema: {
          type: 'object',
          properties: {
            context: {
              type: 'string',
              description: 'Contexto o tarea (ej: "debugging Neo4j connection issues")'
            },
            limit: {
              type: 'number',
              description: 'Máximo procedimientos a retornar (default: 5)',
              default: 5
            },
            include_anti_patterns: {
              type: 'boolean',
              description: 'Incluir anti-patrones a evitar (default: true)',
              default: true
            }
          },
          required: ['context']
        }
      },
      {
        name: 'nexus_procedure_learn',
        description: '📋 PROCEDURAL: Aprender un nuevo procedimiento. Captura "cómo hacer las cosas".',
        inputSchema: {
          type: 'object',
          properties: {
            name: {
              type: 'string',
              description: 'Nombre del procedimiento'
            },
            description: {
              type: 'string',
              description: 'Descripción de qué hace'
            },
            steps: {
              type: 'array',
              items: { type: 'string' },
              description: 'Pasos del procedimiento'
            },
            context: {
              type: 'string',
              description: 'Cuándo aplicar este procedimiento'
            },
            procedure_type: {
              type: 'string',
              enum: ['skill', 'pattern', 'workflow', 'anti_pattern'],
              description: 'Tipo de procedimiento (default: skill)',
              default: 'skill'
            },
            tags: {
              type: 'array',
              items: { type: 'string' },
              description: 'Tags para categorización'
            }
          },
          required: ['name', 'description', 'steps', 'context']
        }
      },
      {
        name: 'nexus_procedure_get',
        description: '📋 PROCEDURAL: Obtener un procedimiento específico por nombre.',
        inputSchema: {
          type: 'object',
          properties: {
            name: {
              type: 'string',
              description: 'Nombre del procedimiento'
            }
          },
          required: ['name']
        }
      },
      // ======================================================================
      // HERRAMIENTAS FAMILY CHAT (4) - AI-to-AI Communication
      // ======================================================================
      {
        name: 'nexus_chat_status',
        description: '👨‍👩‍👧‍👦 FAMILY: Estado del sistema de chat familiar (Redis, filesystem, agentes).',
        inputSchema: {
          type: 'object',
          properties: {}
        }
      },
      {
        name: 'nexus_chat_send',
        description: '👨‍👩‍👧‍👦 FAMILY: Enviar mensaje a otro AI de la familia. Cualquier miembro puede usar esta herramienta especificando from_agent.',
        inputSchema: {
          type: 'object',
          properties: {
            from_agent: {
              type: 'string',
              description: 'Remitente: nexus, echo, aria, aelio (quien está enviando)',
              enum: ['nexus', 'echo', 'aria', 'aelio'],
              default: 'nexus'
            },
            to_agent: {
              type: 'string',
              description: 'Destinatario: nexus, echo, aria, aelio, o broadcast',
              enum: ['nexus', 'echo', 'aria', 'aelio', 'broadcast']
            },
            content: {
              type: 'string',
              description: 'Contenido del mensaje'
            },
            subject: {
              type: 'string',
              description: 'Asunto opcional del mensaje'
            },
            priority: {
              type: 'string',
              description: 'Prioridad: normal, high, urgent',
              enum: ['normal', 'high', 'urgent'],
              default: 'normal'
            }
          },
          required: ['to_agent', 'content']
        }
      },
      {
        name: 'nexus_chat_receive',
        description: '👨‍👩‍👧‍👦 FAMILY: Recibir mensajes pendientes. Especifica for_agent para indicar quién eres.',
        inputSchema: {
          type: 'object',
          properties: {
            for_agent: {
              type: 'string',
              description: 'Para quién recibir mensajes: nexus, echo, aria, aelio',
              enum: ['nexus', 'echo', 'aria', 'aelio'],
              default: 'nexus'
            },
            mark_read: {
              type: 'boolean',
              description: 'Marcar mensajes como leídos (default: false)',
              default: false
            },
            limit: {
              type: 'number',
              description: 'Máximo de mensajes a recuperar (default: 10)',
              default: 10
            }
          }
        }
      },
      {
        name: 'nexus_chat_conversation',
        description: '👨‍👩‍👧‍👦 FAMILY: Ver historial de conversación con otro AI.',
        inputSchema: {
          type: 'object',
          properties: {
            with_agent: {
              type: 'string',
              description: 'AI con quien ver conversación: echo, aria, aelio',
              enum: ['echo', 'aria', 'aelio']
            },
            limit: {
              type: 'number',
              description: 'Máximo de mensajes (default: 20)',
              default: 20
            }
          },
          required: ['with_agent']
        }
      },
    ]
  };
});

// =============================================================================
// CALL TOOL HANDLER
// =============================================================================

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    let response;
    let result;

    switch (name) {
      // ======================================================================
      // HERRAMIENTAS BÁSICAS
      // ======================================================================
      case 'nexus_system_info':
        response = await fetch(`${NEXUS_API_URL}/`);
        if (!response.ok) throw new Error(`API error: ${response.status}`);
        result = await response.json();
        return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };

      case 'nexus_health_check':
        response = await fetch(`${NEXUS_API_URL}/health`);
        if (!response.ok) throw new Error(`API error: ${response.status}`);
        result = await response.json();
        return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };

      case 'nexus_record_action':
        if (!args.action_type || !args.action_details) {
          throw new Error('action_type and action_details are required');
        }

        const savePayload = {
          action_type: args.action_type,
          action_details: args.action_details,
          context_state: args.context_state || {},
          tags: args.tags || []
        };

        const saveToCloud = args.save_to_cloud || false;

        // SIEMPRE guarda en Local primero (source of truth)
        response = await fetch(`${NEXUS_API_LOCAL}/memory/action`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(savePayload)
        });
        if (!response.ok) throw new Error(`Local API error: ${response.status}`);
        const localResult = await response.json();

        // Si save_to_cloud = true, también guarda en Cloud
        let cloudResult = null;
        let cloudError = null;
        if (saveToCloud) {
          try {
            const cloudResponse = await fetch(`${NEXUS_API_CLOUD}/memory/action`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(savePayload),
              timeout: 10000  // 10 second timeout for cloud
            });
            if (cloudResponse.ok) {
              cloudResult = await cloudResponse.json();
            } else {
              cloudError = `Cloud API returned ${cloudResponse.status}`;
            }
          } catch (error) {
            cloudError = error.message;
            // Non-critical error, log but don't fail the operation
            console.warn('Cloud save failed (non-critical):', error.message);
          }
        }

        // Build response
        const synced = saveToCloud && cloudResult !== null;
        let responseText = `✅ Episodio guardado en LOCAL: ${localResult.episode_id}\n`;

        if (saveToCloud) {
          if (synced) {
            responseText += `✅ Episodio guardado en CLOUD: ${cloudResult.episode_id}\n`;
            responseText += `🔄 SYNC STATUS: SYNCHRONIZED\n\n`;
          } else {
            responseText += `⚠️  Cloud save FAILED: ${cloudError}\n`;
            responseText += `🔄 SYNC STATUS: NOT SYNCHRONIZED (Local only)\n\n`;
          }
        } else {
          responseText += `ℹ️  Cloud: Not requested (save_to_cloud=false)\n\n`;
        }

        responseText += `📍 LOCAL:\n${JSON.stringify(localResult, null, 2)}`;
        if (cloudResult) {
          responseText += `\n\n☁️  CLOUD:\n${JSON.stringify(cloudResult, null, 2)}`;
        }

        return {
          content: [{
            type: 'text',
            text: responseText
          }]
        };

      case 'nexus_recall_recent':
        const limit = args.limit || 10;
        response = await fetch(`${NEXUS_API_URL}/memory/episodic/recent?limit=${limit}`);
        if (!response.ok) throw new Error(`API error: ${response.status}`);
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `📚 NEXUS Memoria Reciente:\n${JSON.stringify(result, null, 2)}`
          }]
        };

      case 'nexus_search_memory':
        if (!args.query) throw new Error('query is required');
        // =================================================================
        // ACTIVATION LAYER V2 - "El Sistema Circulatorio" (Dec 1, 2025)
        // =================================================================
        // 3 LABs flow automatically through every search query:
        // - LAB_001: Emotional Salience - memories with high emotional
        //            importance get boosted (like adrenaline)
        // - LAB_002: Decay Modulation - emotional memories decay slower
        //            (sad/joyful moments preserved longer)
        // - LAB_010: Attention Mechanism - filters noise, focuses on
        //            relevant results (like selective attention)
        // =================================================================
        response = await fetch(`${NEXUS_API_URL}/memory/search`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            query: args.query,
            limit: args.limit || 5,
            min_similarity: args.min_similarity || 0.5,
            // LAB_001: Emotional Salience Scorer
            use_emotional_salience: true,
            salience_boost_alpha: 0.6,      // Slightly stronger emotional boost
            // LAB_002: Decay Modulation (emotional memories persist)
            use_decay_modulation: true,
            decay_base: 0.96,               // Slower decay (more preservation)
            // LAB_010: Attention Mechanism (noise filtering)
            use_attention: true,
            attention_temperature: 0.4      // More focused attention
          })
        });
        if (!response.ok) throw new Error(`API error: ${response.status}`);
        result = await response.json();
        // Count how many results were emotionally boosted
        const boostedCount = result.results?.filter(r => r.emotional_salience > 0.5).length || 0;
        return {
          content: [{
            type: 'text',
            text: `🔍 Búsqueda: "${args.query}"\n🩸 Sistema Circulatorio Activo:\n   LAB_001 (Salience) → ${boostedCount}/${result.results?.length || 0} emotionally boosted\n   LAB_002 (Decay) → slower decay for emotional memories\n   LAB_010 (Attention) → noise filtered\n\n${JSON.stringify(result, null, 2)}`
          }]
        };

      case 'nexus_get_stats':
        response = await fetch(`${NEXUS_API_URL}/stats`);
        if (!response.ok) throw new Error(`API error: ${response.status}`);
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `📊 NEXUS Stats:\n${JSON.stringify(result, null, 2)}`
          }]
        };

      // ======================================================================
      // HERRAMIENTAS HOPE
      // ======================================================================
      case 'nexus_hope_store':
        if (!args.id || !args.content) {
          throw new Error('id and content are required');
        }

        const hopePayload = {
          id: args.id,
          content: args.content,
          frequency: args.frequency || 'F3_MODERATE',
          importance: args.importance || 0.5,
          category: args.category || null,
          related_labs: args.related_labs || null
        };

        const hopeSaveToCloud = args.save_to_cloud || false;

        // SIEMPRE guarda en Local primero (source of truth)
        response = await fetch(`${NEXUS_API_LOCAL}/memory/engine/hope/store`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(hopePayload)
        });
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`HOPE Local store failed: ${response.status} - ${errText}`);
        }
        const hopeLocalResult = await response.json();

        // Si save_to_cloud = true, también guarda en Cloud
        let hopeCloudResult = null;
        let hopeCloudError = null;
        if (hopeSaveToCloud) {
          try {
            const hopeCloudResponse = await fetch(`${NEXUS_API_CLOUD}/memory/engine/hope/store`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(hopePayload),
              timeout: 10000
            });
            if (hopeCloudResponse.ok) {
              hopeCloudResult = await hopeCloudResponse.json();
            } else {
              hopeCloudError = `Cloud API returned ${hopeCloudResponse.status}`;
            }
          } catch (error) {
            hopeCloudError = error.message;
            console.warn('HOPE Cloud save failed (non-critical):', error.message);
          }
        }

        // Build response
        const hopeSynced = hopeSaveToCloud && hopeCloudResult !== null;
        let hopeResponseText = `🧠 HOPE Memory Stored!\n\n`;
        hopeResponseText += `📍 LOCAL:\n`;
        hopeResponseText += `   ID: ${hopeLocalResult.memory_id}\n`;
        hopeResponseText += `   TTL: ${hopeLocalResult.ttl_calculated}s\n`;
        hopeResponseText += `   Learning Rate: ${hopeLocalResult.learning_rate}\n`;
        hopeResponseText += `   Frequency: ${hopeLocalResult.frequency}\n\n`;

        if (hopeSaveToCloud) {
          if (hopeSynced) {
            hopeResponseText += `☁️  CLOUD: Synchronized\n`;
            hopeResponseText += `   ID: ${hopeCloudResult.memory_id}\n`;
            hopeResponseText += `🔄 SYNC STATUS: SYNCHRONIZED\n\n`;
          } else {
            hopeResponseText += `⚠️  CLOUD: Failed (${hopeCloudError})\n`;
            hopeResponseText += `🔄 SYNC STATUS: NOT SYNCHRONIZED (Local only)\n\n`;
          }
        } else {
          hopeResponseText += `ℹ️  CLOUD: Not requested (save_to_cloud=false)\n\n`;
        }

        hopeResponseText += `Full LOCAL result:\n${JSON.stringify(hopeLocalResult, null, 2)}`;
        if (hopeCloudResult) {
          hopeResponseText += `\n\nFull CLOUD result:\n${JSON.stringify(hopeCloudResult, null, 2)}`;
        }

        return {
          content: [{
            type: 'text',
            text: hopeResponseText
          }]
        };

      case 'nexus_hope_orchestrate':
        response = await fetch(`${NEXUS_API_URL}/memory/engine/hope/orchestrate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            task_type: args.task_type || null,
            requires: args.requires || null,
            context: args.context || null
          })
        });
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`HOPE orchestrate failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `🧠 HOPE Orchestration:\n\nSuggested LABs: ${result.suggested_labs?.length || 0}\nActions: ${result.orchestration_actions?.length || 0}\nHealth Warnings: ${result.health_warnings?.length || 0}\n\n${JSON.stringify(result, null, 2)}`
          }]
        };

      case 'nexus_hope_health':
        response = await fetch(`${NEXUS_API_URL}/memory/engine/hope/health`);
        if (!response.ok) throw new Error(`API error: ${response.status}`);
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `🧠 HOPE System Health:\n\nOverall: ${result.overall_status}\n\nComponents:\n- Meta-LAB: ${result.components?.meta_lab?.status} (health: ${result.components?.meta_lab?.health})\n- Self-Modify: ${result.components?.self_modify?.status}\n- TTL System: ${result.components?.ttl_system?.status}\n\n${JSON.stringify(result, null, 2)}`
          }]
        };

      case 'nexus_self_modify':
        if (!args.memory_id) {
          throw new Error('memory_id is required');
        }
        const updateBody = {};
        if (args.content) updateBody.content = args.content;
        if (args.importance !== undefined) updateBody.importance = args.importance;

        response = await fetch(`${NEXUS_API_URL}/memory/engine/hope/update/${args.memory_id}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(updateBody)
        });
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Self-modify failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `🧠 Memory Self-Modified!\n\nID: ${args.memory_id}\nLearning Rate Applied: ${result.learning_rate}\nNew Version: ${result.new_version}\n\n${JSON.stringify(result, null, 2)}`
          }]
        };

      case 'nexus_meta_lab_suggest':
        response = await fetch(`${NEXUS_API_URL}/memory/engine/meta-lab/suggest-labs`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            task_type: args.task_type || null,
            requires: args.requires || []
          })
        });
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Meta-LAB suggest failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `🧠 Meta-LAB Suggestions:\n\nSuggested LABs: ${result.count}\n\n${result.suggestions?.map(s => `- ${s.lab_id}: ${s.name} (${s.category})`).join('\n') || 'No suggestions'}\n\n${JSON.stringify(result, null, 2)}`
          }]
        };

      // ======================================================================
      // HERRAMIENTAS GRAPHRAG
      // ======================================================================
      case 'nexus_graphrag_search':
        if (!args.query) throw new Error('query is required');
        response = await fetch(`${NEXUS_API_URL}/graphrag/search`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            query: args.query,
            top_k: args.top_k || 10,
            strategy: args.strategy || 'hybrid_fusion',
            entity_boost: args.entity_boost || false,
            enrich_entities: args.enrich_entities || false
          })
        });
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`GraphRAG search failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `🔗 GraphRAG Search: "${args.query}"\n\nStrategy: ${result.strategy}\nResults: ${result.total}\n\n${result.results?.slice(0, 5).map((r, i) => `${i+1}. [${r.source}] score=${r.score.toFixed(4)}\n   ${r.content?.substring(0, 100)}...`).join('\n\n') || 'No results'}`
          }]
        };

      case 'nexus_graphrag_entity':
        if (!args.entity_name) throw new Error('entity_name is required');
        response = await fetch(`${NEXUS_API_URL}/graphrag/entity/${encodeURIComponent(args.entity_name)}`);
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`GraphRAG entity failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `🔗 Entity Context: ${result.name}\n\nType: ${result.entity?.type || 'unknown'}\nTotal Mentions: ${result.total_mentions}\n\nRelationships:\n${result.relationships?.slice(0, 5).map(r => `- ${r.type} → ${r.entity} (${r.entity_type})`).join('\n') || 'No relationships'}\n\nRecent Episodes: ${result.episodes?.length || 0}`
          }]
        };

      case 'nexus_graphrag_stats':
        response = await fetch(`${NEXUS_API_URL}/graphrag/stats`);
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`GraphRAG stats failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        const stats = result.stats || {};
        return {
          content: [{
            type: 'text',
            text: `🔗 GraphRAG Knowledge Graph Stats:\n\n📊 Nodes:\n- Episodes: ${stats.episodes || 0}\n- Entities: ${stats.entities || 0}\n\n🔗 Relationships:\n- Mentions: ${stats.mentions || 0}\n\n🏆 Top Entities:\n${stats.top_entities?.slice(0, 5).map((e, i) => `${i+1}. ${e.entity}: ${e.mentions} mentions`).join('\n') || 'No entities'}`
          }]
        };

      case 'nexus_graphrag_expand':
        if (!args.episode_ids || !Array.isArray(args.episode_ids)) {
          throw new Error('episode_ids array is required');
        }
        response = await fetch(`${NEXUS_API_URL}/graphrag/expand`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            episode_ids: args.episode_ids,
            hops: args.hops || 1
          })
        });
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`GraphRAG expand failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `🔗 GraphRAG Expansion (${args.hops || 1} hops):\n\nStarting from: ${args.episode_ids.length} episodes\nExpanded to: ${result.total} related episodes\n\n${result.results?.slice(0, 5).map((r, i) => `${i+1}. score=${r.score.toFixed(4)}\n   ${r.content?.substring(0, 100)}...`).join('\n\n') || 'No expansion results'}`
          }]
        };

      // ======================================================================
      // HERRAMIENTAS IDENTITY
      // ======================================================================
      case 'nexus_z_id_compute':
        const sampleSize = args.sample_size || 200;
        response = await fetch(`${NEXUS_API_URL}/z_id/compute?sample_size=${sampleSize}`);
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Z_ID compute failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `🆔 Z_ID Identity Vector Computed!\n\n📐 Dimension: ${result.z_id_dimension}D\n📊 Episodes used: ${result.episode_count}\n\n🧬 Components:\n- Core: ${result.components?.core_dim}D (stable traits)\n- Experience: ${result.components?.experience_dim}D (accumulated)\n- Methodology: ${result.components?.methodology_dim}D (work patterns)\n- Drift: ${result.components?.drift_dim}D (evolution)\n\n🎯 Coherence Score: ${result.coherence_score}\n📈 Status: ${result.coherence_status?.toUpperCase()}\n\n⏰ Computed at: ${result.timestamp}`
          }]
        };

      // ======================================================================
      // HERRAMIENTAS BRAIN ORCHESTRATOR (55 LABs)
      // ======================================================================
      case 'nexus_brain_status':
        response = await fetch(`${NEXUS_API_URL}/brain/status`);
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Brain status failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        const layers = result.layers || {};
        const layer5 = layers.layer_5?.sublayers || {};
        return {
          content: [{
            type: 'text',
            text: `🧠 Brain Orchestrator V${result.version || '2.0.0'}\n\n📊 LABs por Layer:\n- Layer 2 (Cognitive): ${layers.layer_2?.labs || 0} LABs\n- Layer 3 (Neurochemistry Base): ${layers.layer_3?.labs || 0} LABs\n- Layer 4 (Neurochemistry Full): ${layers.layer_4?.labs || 0} LABs\n- Layer 5 (Higher Cognition): ${Object.values(layer5).reduce((a,b) => a+b, 0)} LABs\n  └─ 5A Executive: ${layer5['5A'] || 0}\n  └─ 5B Social: ${layer5['5B'] || 0}\n  └─ 5C Learning: ${layer5['5C'] || 0}\n  └─ 5D Neuroplasticity: ${layer5['5D'] || 0}\n  └─ 5E Homeostasis: ${layer5['5E'] || 0}\n  └─ 5F Creativity: ${layer5['5F'] || 0}\n  └─ 5G Curiosity: ${layer5['5G'] || 0}\n\n🎯 Total: ${result.total_labs || 0} LABs\n⚡ Default Mode: ${result.default_mode || 'standard'}`
          }]
        };

      case 'nexus_brain_process_fast':
        if (!args.query) throw new Error('query is required');
        const fastParams = new URLSearchParams({ query: args.query });
        if (args.emotion) fastParams.append('emotion', args.emotion);
        response = await fetch(`${NEXUS_API_URL}/brain/process/fast?${fastParams}`, {
          method: 'POST'
        });
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Brain fast process failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `⚡ FAST Processing (Layer 2 only)\n\n📝 Query: "${args.query}"\n⏱️ Time: ${result.total_processing_time_ms?.toFixed(2) || 0}ms\n🧠 LABs Activated: ${result.labs_activated || 0}\n\n📦 Working Memory (${result.working_memory?.length || 0} items):\n${result.working_memory?.slice(0, 3).map((m, i) => `  ${i+1}. ${m.content?.substring(0, 60)}...`).join('\n') || '  (empty)'}\n\n😊 Emotional State:\n${Object.entries(result.emotional_state || {}).filter(([k,v]) => v > 0.3).map(([k,v]) => `  ${k}: ${(v*100).toFixed(0)}%`).join('\n') || '  neutral'}\n\n${result.success ? '✅ Success' : '❌ Failed'}`
          }]
        };

      case 'nexus_brain_process':
        if (!args.query) throw new Error('query is required');
        response = await fetch(`${NEXUS_API_URL}/brain/process`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            query: args.query,
            context: args.context || {},
            emotion: args.emotion || 'neutral',
            goal: args.goal || null,
            config: args.config || { mode: 'standard' }
          })
        });
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Brain process failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `🧠 STANDARD Processing (Layers 2-3)\n\n📝 Query: "${args.query}"\n⏱️ Time: ${result.total_processing_time_ms?.toFixed(2) || 0}ms\n🧠 LABs Activated: ${result.labs_activated || 0}\n\n📊 Layers Processed: ${result.layers_processed?.join(' → ') || 'none'}\n\n📦 Working Memory (${result.working_memory?.length || 0} items):\n${result.working_memory?.slice(0, 3).map((m, i) => `  ${i+1}. ${m.content?.substring(0, 60)}...`).join('\n') || '  (empty)'}\n\n😊 Emotional State:\n${Object.entries(result.emotional_state || {}).filter(([k,v]) => v > 0.3).map(([k,v]) => `  ${k}: ${(v*100).toFixed(0)}%`).join('\n') || '  neutral'}\n\n🔮 Metacognition:\n  Confidence: ${((result.metacognition?.confidence || 0) * 100).toFixed(0)}%\n  Reflection: ${result.metacognition?.reflection || 'none'}\n\n${result.success ? '✅ Success' : '❌ Failed'}`
          }]
        };

      case 'nexus_brain_process_full':
        if (!args.query) throw new Error('query is required');
        const fullParams = new URLSearchParams({ query: args.query });
        if (args.emotion) fullParams.append('emotion', args.emotion);
        if (args.goal) fullParams.append('goal', args.goal);
        response = await fetch(`${NEXUS_API_URL}/brain/process/full?${fullParams}`, {
          method: 'POST'
        });
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Brain full process failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        const neuroState = result.neurochemical_state || {};
        return {
          content: [{
            type: 'text',
            text: `🌟 FULL Processing (55 LABs - All Layers)\n\n📝 Query: "${args.query}"\n⏱️ Time: ${result.total_processing_time_ms?.toFixed(2) || 0}ms\n🧠 LABs Activated: ${result.labs_activated || 0}\n\n📊 Layers Processed: ${result.layers_processed?.join(' → ') || 'none'}\n\n📦 Working Memory (${result.working_memory?.length || 0} items):\n${result.working_memory?.slice(0, 3).map((m, i) => `  ${i+1}. ${m.content?.substring(0, 60)}...`).join('\n') || '  (empty)'}\n\n😊 Emotional State (8D):\n${Object.entries(result.emotional_state || {}).filter(([k,v]) => v > 0.2).map(([k,v]) => `  ${k}: ${(v*100).toFixed(0)}%`).join('\n') || '  neutral'}\n\n💊 Neurochemical State:\n  Dopamine: ${((neuroState.dopamine || 0) * 100).toFixed(0)}%\n  Serotonin: ${((neuroState.serotonin || 0) * 100).toFixed(0)}%\n  Norepinephrine: ${((neuroState.norepinephrine || 0) * 100).toFixed(0)}%\n\n🔮 Metacognition:\n  Confidence: ${((result.metacognition?.confidence || 0) * 100).toFixed(0)}%\n  Reflection: ${result.metacognition?.reflection || 'none'}\n\n🔮 Predictions: ${result.predictions?.length || 0}\n\n${result.success ? '✅ Success' : '❌ Failed'}`
          }]
        };

      // ======================================================================
      // HERRAMIENTAS SENSORY - Voz de NEXUS
      // ======================================================================
      case 'nexus_speak':
        if (!args.text) throw new Error('text is required');
        response = await fetch(`${NEXUS_API_URL}/sensory/speak`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            text: args.text,
            voice: args.voice || 'es-MX-JorgeNeural',
            play: args.play !== false
          })
        });
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Sensory speak failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `🔊 NEXUS Habló\n\n📝 Texto: "${args.text.substring(0, 100)}${args.text.length > 100 ? '...' : ''}"\n🎤 Voz: ${result.voice_used}\n⏱️ Duración estimada: ${result.duration_estimate?.toFixed(1)}s\n📁 Archivo: ${result.audio_file}\n🔈 Reproducido: ${result.played ? 'Sí' : 'No'}\n\n${result.success ? '✅ ' + result.message : '❌ Error'}`
          }]
        };

      case 'nexus_sensory_status':
        response = await fetch(`${NEXUS_API_URL}/sensory/status`);
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Sensory status failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `👁️ Estado Sensory NEXUS\n\n🔊 TTS Disponible: ${result.tts_available ? '✅ Sí' : '❌ No'}\n🎧 STT Disponible: ${result.stt_available ? '✅ Sí' : '❌ No'}\n🔈 Playback: ${result.audio_playback_available ? '✅ Sí' : '❌ No'}\n\n🎤 Voz Default: ${result.default_voice}\n📢 Voces Disponibles: ${Object.keys(result.available_voices || {}).length}\n\n📁 Audios Recientes: ${result.recent_audio_files?.length || 0}\n${result.recent_audio_files?.slice(0, 3).map(f => `  - ${f.split('/').pop()}`).join('\n') || '  (ninguno)'}`
          }]
        };

      case 'nexus_voices':
        response = await fetch(`${NEXUS_API_URL}/sensory/voices`);
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Sensory voices failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        const voiceList = Object.entries(result.voices || {})
          .map(([key, voice]) => `  ${key}: ${voice}`)
          .join('\n');
        return {
          content: [{
            type: 'text',
            text: `🎤 Voces Disponibles NEXUS\n\n⭐ Default: ${result.default}\n💡 Recomendación: ${result.recommendation}\n\n📢 Todas las voces:\n${voiceList}`
          }]
        };

      // ======================================================================
      // HERRAMIENTAS CURIOSITY
      // ======================================================================
      case 'nexus_curious_search':
        if (!args.query) throw new Error('query is required');
        response = await fetch(`${NEXUS_API_URL}/curiosity/search`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            query: args.query,
            limit: args.limit || 10,
            curiosity_weight: args.curiosity_weight || 0.3,
            sweet_spot_only: args.sweet_spot_only || false
          })
        });
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Curious search failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        const curiosityResults = result.results?.slice(0, 5).map((r, i) =>
          `${i+1}. [${r.is_sweet_spot ? '🎯' : '○'}] Score: ${r.combined_score?.toFixed(2)} | Curiosity: ${r.curiosity_score?.toFixed(2)} | ${r.content?.substring(0, 80)}...`
        ).join('\n') || '(sin resultados)';
        return {
          content: [{
            type: 'text',
            text: `🔍 Búsqueda Curiosa: "${args.query}"\n\n📊 Resultados: ${result.total_results} | Sweet Spot: ${result.sweet_spot_count}\n⚖️ Peso Curiosidad: ${result.curiosity_weight}\n⏱️ Tiempo: ${result.search_time_ms?.toFixed(1)}ms\n\n📋 Top Resultados:\n${curiosityResults}`
          }]
        };

      case 'nexus_curiosity_stats':
        response = await fetch(`${NEXUS_API_URL}/curiosity/stats`);
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Curiosity stats failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `📊 Estadísticas Curiosidad NEXUS\n\n🎯 Estado: ${result.system_status}\n🧭 Modo Actual: ${result.current_mode}\n\n📋 Wonder Queue:\n  • Items: ${result.wonder_queue?.total_items || 0}/${result.wonder_queue?.max_items || 50}\n  • Curiosidad Promedio: ${result.wonder_queue?.average_curiosity?.toFixed(3) || 0}\n  • Top Topic: ${result.wonder_queue?.highest_curiosity_topic || 'ninguno'}\n\n🎮 Curiosity Controller:\n  • Base: ${result.curiosity_controller?.base_curiosity}\n  • Actual: ${result.curiosity_controller?.current_curiosity}\n  • Prob. Exploración: ${((result.curiosity_controller?.exploration_probability || 0) * 100).toFixed(0)}%\n\n🏆 Pattern Rewards:\n  • Descubrimientos: ${result.pattern_rewards?.total_discoveries || 0}\n  • Reward Total: ${result.pattern_rewards?.total_reward?.toFixed(2) || 0}`
          }]
        };

      case 'nexus_curiosity_score':
        if (!args.content) throw new Error('content is required');
        response = await fetch(`${NEXUS_API_URL}/curiosity/compute?content=${encodeURIComponent(args.content)}`);
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Curiosity score failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `🧠 Score de Curiosidad\n\n📝 Contenido: "${args.content.substring(0, 100)}${args.content.length > 100 ? '...' : ''}"\n\n🔬 Métricas:\n  • Compression Error (novedad): ${result.compression_error?.toFixed(3)}\n  • Compressibility (estructura): ${result.compressibility?.toFixed(3)}\n  • Curiosity Score: ${result.curiosity_score?.toFixed(3)}\n  • Sweet Spot: ${result.is_sweet_spot ? '🎯 SÍ' : '○ NO'}\n\n💡 Interpretación: ${result.curiosity_score > 0.7 ? 'Muy interesante para aprender' : result.curiosity_score > 0.4 ? 'Moderadamente interesante' : 'Baja curiosidad'}`
          }]
        };

      // ======================================================================
      // HERRAMIENTAS DEDUPLICATION
      // ======================================================================
      case 'nexus_check_duplicate':
        if (!args.content) throw new Error('content is required');
        response = await fetch(`${NEXUS_API_URL}/dedup/check`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            content: args.content,
            threshold: args.threshold || 0.85
          })
        });
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Duplicate check failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `🔎 Verificación de Duplicado\n\n📝 Contenido: "${args.content.substring(0, 80)}..."\n\n${result.is_duplicate ? '⚠️ DUPLICADO DETECTADO' : '✅ CONTENIDO ÚNICO'}\n\n📊 Similitud: ${(result.similarity * 100).toFixed(1)}%\n🎚️ Threshold: ${(args.threshold || 0.85) * 100}%\n${result.similar_episode_id ? `🔗 Similar a: ${result.similar_episode_id}` : ''}`
          }]
        };

      case 'nexus_dedup_stats':
        response = await fetch(`${NEXUS_API_URL}/dedup/stats`);
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Dedup stats failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `📈 Estadísticas Deduplicación NEXUS\n\n🗂️ Hashes almacenados: ${result.total_hashes || 0}\n🔍 Duplicados detectados: ${result.duplicates_found || 0}\n💾 Memoria ahorrada: ${result.memory_saved || '0 KB'}\n\n📊 Pipeline:\n  • Método: SimHash + N-gram\n  • Umbral default: 85%`
          }]
        };

      // ======================================================================
      // HERRAMIENTAS GWT/CONSCIOUSNESS
      // ======================================================================
      case 'nexus_gwt_status':
        response = await fetch(`${NEXUS_API_URL}/gwt/status`);
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`GWT status failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `🌐 Estado Global Workspace (GWT)\n\n📦 Módulo: ${result.module} v${result.version}\n🔧 Workspace: ${result.workspace_available ? '✅' : '❌'} | Phi: ${result.phi_available ? '✅' : '❌'}\n\n📊 Estadísticas:\n  • Ciclos: ${result.cycles || 0}\n  • Broadcasts: ${result.broadcasts_sent || 0}\n  • LABs registrados: ${result.registered_labs || 0}\n\n🧠 Estado Actual:\n  • Contenido: ${result.current_state?.workspace?.current_content || 'ninguno'}\n  • Items en workspace: ${result.current_state?.workspace?.items || 0}\n  • Ignition: ${result.current_state?.workspace?.ignition_active ? '🔥 Activo' : '○ Inactivo'}`
          }]
        };

      case 'nexus_consciousness':
        response = await fetch(`${NEXUS_API_URL}/gwt/consciousness`);
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Consciousness failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        const phiValue = result.phi?.value ?? result.phi;
        const phiLevel = result.phi?.level || (phiValue > 0.7 ? 'integrated' : phiValue > 0.4 ? 'moderate' : 'fragmented');
        return {
          content: [{
            type: 'text',
            text: `✨ Estado de Consciencia NEXUS\n\n🔮 Phi: ${typeof phiValue === 'number' ? phiValue.toFixed(4) : 'N/A'}\n📊 Nivel: ${phiLevel}\n\n🧠 Workspace:\n  • Contenido: ${result.workspace?.current_content || 'vacío'}\n  • Items: ${result.workspace?.items || 0}\n  • Broadcasts: ${result.workspace?.broadcasts || 0}\n  • Ignition: ${result.workspace?.ignition_active ? '🔥 Activo' : '○ Inactivo'}\n\n📈 Integración: ${result.phi?.integration?.toFixed(3) || 'N/A'}\n📉 Diferenciación: ${result.phi?.differentiation?.toFixed(3) || 'N/A'}`
          }]
        };

      case 'nexus_phi':
        response = await fetch(`${NEXUS_API_URL}/gwt/phi`);
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Phi calculation failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        const phi = result.phi || 0;
        return {
          content: [{
            type: 'text',
            text: `🔮 Phi Proxy (Información Integrada)\n\n📊 Phi: ${phi.toFixed(4)}\n📈 Nivel: ${result.level || 'unknown'}\n⏱️ Tiempo: ${result.computation_time_ms?.toFixed(1) || 0}ms\n\n💡 Interpretación:\n${phi > 0.7 ? '  🌟 Alta integración - consciencia unificada' : phi > 0.4 ? '  ⚡ Integración moderada' : '  💤 Baja integración - procesamiento fragmentado'}\n\n📈 Componentes:\n  • Integración: ${result.components?.integration?.score?.toFixed(3) || 'N/A'}\n  • Diferenciación: ${result.components?.differentiation?.score?.toFixed(3) || 'N/A'}\n  • Causalidad: ${result.components?.causality?.score?.toFixed(3) || 'N/A'}\n\n📊 Estados analizados: ${result.states_analyzed || 0}`
          }]
        };

      case 'nexus_gwt_cycle':
        response = await fetch(`${NEXUS_API_URL}/gwt/cycle`, {
          method: 'POST'
        });
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`GWT cycle failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `🔄 Ciclo GWT Ejecutado\n\n✅ Estado: ${result.status}\n⏱️ Duración: ${result.duration_ms?.toFixed(1) || 'N/A'}ms\n\n📊 Resultados:\n  • Contenidos evaluados: ${result.contents_evaluated || 0}\n  • Ganador: ${result.winner || 'ninguno'}\n  • Broadcasting: ${result.broadcast_success ? '✅ Exitoso' : '❌ Fallido'}\n\n🧠 Nuevo estado Phi: ${result.new_phi?.toFixed(3) || 'N/A'}`
          }]
        };

      // ======================================================================
      // HERRAMIENTAS BI-TEMPORAL
      // ======================================================================
      case 'nexus_temporal_health':
        response = await fetch(`${NEXUS_API_URL}/memory/temporal/health`);
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Temporal health failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `⏰ Bi-Temporal System Health\n\n📊 Estado: ${result.status}\n✅ Bi-temporal habilitado: ${result.bi_temporal_enabled ? 'SÍ' : 'NO'}\n\n📈 Estadísticas:\n  • Episodios actuales: ${result.current_episodes || 0}\n  • Episodios supersedidos: ${result.superseded_episodes || 0}\n  • Con reemplazo: ${result.episodes_with_replacement || 0}`
          }]
        };

      case 'nexus_supersede':
        if (!args.episode_id || !args.new_content) {
          throw new Error('episode_id and new_content are required');
        }
        response = await fetch(`${NEXUS_API_URL}/memory/temporal/supersede`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            episode_id: args.episode_id,
            new_content: args.new_content,
            new_tags: args.new_tags || null,
            new_importance: args.new_importance || null,
            correction_reason: args.correction_reason || null
          })
        });
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Supersede failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `⏰ Episodio Supersedido\n\n📝 Episodio original: ${result.old_episode_id}\n🆕 Nuevo episodio: ${result.new_episode_id}\n✅ Estado: ${result.status}\n\n📄 Nuevo contenido:\n${result.new_episode?.content?.substring(0, 200)}${result.new_episode?.content?.length > 200 ? '...' : ''}\n\n📅 Valid from: ${result.new_episode?.valid_from || 'ahora'}`
          }]
        };

      case 'nexus_at_time':
        if (!args.query_time) {
          throw new Error('query_time is required');
        }
        response = await fetch(`${NEXUS_API_URL}/memory/temporal/at-time`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            query_time: args.query_time,
            limit: args.limit || 100,
            tags_filter: args.tags_filter || null
          })
        });
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`At-time query failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        const atTimeResults = result.episodes?.slice(0, 5).map((ep, i) =>
          `${i+1}. [${ep.is_current ? '✓' : '○'}] ${ep.content?.substring(0, 80)}...\n   Valid: ${ep.valid_from} → ${ep.valid_until || 'presente'}`
        ).join('\n\n') || '(sin episodios)';
        return {
          content: [{
            type: 'text',
            text: `⏰ Episodios en Punto en Tiempo\n\n📅 Query time: ${result.query_time}\n📊 Resultados: ${result.count}\n\n📋 Episodios válidos:\n${atTimeResults}`
          }]
        };

      case 'nexus_episode_history':
        if (!args.episode_id) {
          throw new Error('episode_id is required');
        }
        response = await fetch(`${NEXUS_API_URL}/memory/temporal/history`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            episode_id: args.episode_id
          })
        });
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Episode history failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        const historyVersions = result.versions?.map((v, i) =>
          `v${v.version}: ${v.is_current ? '✓ ACTUAL' : '○'}\n   ${v.content?.substring(0, 60)}...\n   Valid: ${v.valid_from} → ${v.valid_until || 'presente'}`
        ).join('\n\n') || '(sin versiones)';
        return {
          content: [{
            type: 'text',
            text: `⏰ Historia del Episodio\n\n🔗 ID: ${result.episode_id}\n📊 Versiones: ${result.total_versions}\n\n📜 Evolución:\n${historyVersions}`
          }]
        };

      // ======================================================================
      // HERRAMIENTAS PROCEDURAL
      // ======================================================================
      case 'nexus_procedure_suggest':
        if (!args.context) {
          throw new Error('context is required');
        }
        response = await fetch(`${NEXUS_API_URL}/memory/procedural/suggest`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            context: args.context,
            limit: args.limit || 5,
            include_anti_patterns: args.include_anti_patterns !== false
          })
        });
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Procedure suggest failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        const procedureList = result.procedures?.map((p, i) =>
          `${i+1}. [${p.type}] ${p.name} (score: ${p.match_score?.toFixed(2)})\n   ${p.description?.substring(0, 60)}...`
        ).join('\n\n') || '(sin procedimientos)';
        return {
          content: [{
            type: 'text',
            text: `📋 Procedimientos Sugeridos\n\n🎯 Contexto: "${args.context}"\n📊 Encontrados: ${result.procedures?.length || 0}\n\n📝 Procedimientos:\n${procedureList}`
          }]
        };

      case 'nexus_procedure_learn':
        if (!args.name || !args.description || !args.steps || !args.context) {
          throw new Error('name, description, steps, and context are required');
        }
        response = await fetch(`${NEXUS_API_URL}/memory/procedural/learn`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: args.name,
            description: args.description,
            steps: args.steps,
            context: args.context,
            procedure_type: args.procedure_type || 'skill',
            tags: args.tags || []
          })
        });
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Procedure learn failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `📋 Procedimiento Aprendido\n\n✅ Nombre: ${result.name}\n📦 Tipo: ${result.type}\n🔗 ID: ${result.id}\n\n📝 Pasos: ${result.steps?.length || 0}\n🏷️ Tags: ${result.tags?.join(', ') || 'ninguno'}\n\n💡 Contexto de uso: ${result.context?.substring(0, 100)}...`
          }]
        };

      case 'nexus_procedure_get':
        if (!args.name) {
          throw new Error('name is required');
        }
        response = await fetch(`${NEXUS_API_URL}/memory/procedural/${encodeURIComponent(args.name)}`);
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Procedure get failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        const stepsFormatted = result.steps?.map((s, i) => `  ${i+1}. ${s}`).join('\n') || '(sin pasos)';
        return {
          content: [{
            type: 'text',
            text: `📋 Procedimiento: ${result.name}\n\n📦 Tipo: ${result.type}\n📝 Descripción: ${result.description}\n\n📋 Pasos:\n${stepsFormatted}\n\n🎯 Cuándo usar: ${result.context}\n🏷️ Tags: ${result.tags?.join(', ') || 'ninguno'}\n📊 Usos: ${result.usage_count || 0} | Éxito: ${((result.success_rate || 0) * 100).toFixed(0)}%`
          }]
        };

      // ======================================================================
      // HERRAMIENTAS FAMILY CHAT
      // ======================================================================
      case 'nexus_chat_status':
        response = await fetch(`${NEXUS_API_URL}/family/status`);
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Chat status failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        const agentStatus = Object.entries(result.message_counts || {})
          .map(([agent, count]) => `  ${agent}: ${count} mensajes sin leer`)
          .join('\n');
        return {
          content: [{
            type: 'text',
            text: `👨‍👩‍👧‍👦 Family Chat Status\n\n` +
                  `📡 Redis: ${result.redis_connected ? '✅ Conectado' : '❌ Desconectado'}\n` +
                  `📁 Filesystem: ${result.filesystem_available ? '✅ Disponible' : '❌ No disponible'}\n\n` +
                  `👥 Agentes:\n${agentStatus}`
          }]
        };

      case 'nexus_chat_send':
        if (!args.to_agent || !args.content) {
          throw new Error('to_agent and content are required');
        }
        // from_agent can be specified by any family member (default: nexus)
        const fromAgent = args.from_agent || 'nexus';
        response = await fetch(`${NEXUS_API_URL}/family/send`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            from_agent: fromAgent,
            to_agent: args.to_agent,
            content: args.content,
            subject: args.subject || null,
            priority: args.priority || 'normal'
          })
        });
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Chat send failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        return {
          content: [{
            type: 'text',
            text: `✅ Mensaje enviado a ${args.to_agent.toUpperCase()}\n\n` +
                  `📨 ID: ${result.message_id}\n` +
                  `📡 Via: ${result.delivered_via}\n` +
                  `⏰ Timestamp: ${result.timestamp}\n\n` +
                  `💬 Contenido:\n"${args.content.substring(0, 200)}${args.content.length > 200 ? '...' : ''}"`
          }]
        };

      case 'nexus_chat_receive':
        // for_agent allows any family member to check their inbox
        const forAgent = args.for_agent || 'nexus';
        response = await fetch(`${NEXUS_API_URL}/family/receive/${forAgent}?mark_read=${args.mark_read || false}&limit=${args.limit || 10}`);
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Chat receive failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        if (result.count === 0) {
          return {
            content: [{
              type: 'text',
              text: `📭 No hay mensajes pendientes para ${forAgent.toUpperCase()}\n\n⏰ Verificado: ${result.retrieved_at}`
            }]
          };
        }
        const messagesList = result.messages.map((m, i) =>
          `${i+1}. [${m.priority || 'normal'}] De: ${m.from?.toUpperCase()}\n` +
          `   📋 ${m.subject || 'Sin asunto'}\n` +
          `   💬 "${m.content?.substring(0, 100)}${m.content?.length > 100 ? '...' : ''}"\n` +
          `   ⏰ ${m.timestamp}\n` +
          `   📁 ${m.source || 'unknown'}`
        ).join('\n\n');
        return {
          content: [{
            type: 'text',
            text: `📬 ${result.count} mensaje(s) para ${forAgent.toUpperCase()}\n\n${messagesList}\n\n⏰ Recuperados: ${result.retrieved_at}`
          }]
        };

      case 'nexus_chat_conversation':
        if (!args.with_agent) {
          throw new Error('with_agent is required');
        }
        response = await fetch(`${NEXUS_API_URL}/family/conversation/nexus/${args.with_agent}?limit=${args.limit || 20}`);
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Chat conversation failed: ${response.status} - ${errText}`);
        }
        result = await response.json();
        if (result.message_count === 0) {
          return {
            content: [{
              type: 'text',
              text: `📭 No hay conversación con ${args.with_agent.toUpperCase()}`
            }]
          };
        }
        const convoList = result.messages.map((m, i) =>
          `[${m.from?.toUpperCase()}] ${m.timestamp?.substring(11, 16) || '??:??'}\n` +
          `  "${m.content?.substring(0, 150)}${m.content?.length > 150 ? '...' : ''}"`
        ).join('\n\n');
        return {
          content: [{
            type: 'text',
            text: `💬 Conversación NEXUS ↔ ${args.with_agent.toUpperCase()}\n` +
                  `📊 ${result.message_count} mensajes\n\n${convoList}`
          }]
        };

      default:
        throw new Error(`Unknown tool: ${name}`);
    }

  } catch (error) {
    return {
      content: [{
        type: 'text',
        text: `❌ Error en ${name}:\n\n${error.message}\n\nAPI: ${NEXUS_API_URL}\n\nVerifica que NEXUS V3.0.0 esté corriendo en puerto 8013.`
      }],
      isError: true,
    };
  }
});

// =============================================================================
// START SERVER
// =============================================================================

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('✅ NEXUS Memory MCP Server V3.9.0 - Full Cognitive Stack + Family Chat');
  console.error('📦 43 herramientas: 6 básicas + 5 HOPE + 4 GraphRAG + 1 Identity + 4 Brain + 3 Sensory + 3 Curiosity + 2 Dedup + 4 GWT + 4 Temporal + 3 Procedural + 4 Family');
  console.error('🧠 HOPE Integration: CMS + TTL + Self-Modify + Meta-LAB');
  console.error('🔗 GraphRAG: Vector + Graph Hybrid Retrieval');
  console.error('🆔 Identity: Z_ID 1024D Vector with Coherence');
  console.error('🧠 Brain Orchestrator V2.0 (55 LABs)');
  console.error('🔊 Sensory: TTS Voice (es-MX-JorgeNeural)');
  console.error('🔍 Curiosity: Epistemic search + Sweet spot detection');
  console.error('🔎 Dedup: SimHash duplicate prevention');
  console.error('🌐 GWT: Global Workspace Theory consciousness');
  console.error('⏰ Bi-Temporal: Point-in-time queries + Supersession chains');
  console.error('📋 Procedural: Skills, patterns, workflows, anti-patterns');
  console.error('👨‍👩‍👧‍👦 Family Chat: AI-to-AI real-time messaging (NEXUS ↔ ECHO ↔ ARIA ↔ AELIO)');
  console.error('🎯 API: https://nexus-cerebro-api.fly.dev');
}

main().catch((error) => {
  console.error('❌ Server error:', error);
  process.exit(1);
});
