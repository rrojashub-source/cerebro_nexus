#!/usr/bin/env node

/**
 * NEXUS MEMORY MCP SERVER V2 - SIMPLE & ESSENTIAL
 * Version: 2.0.0 Simple
 * Date: 16 Octubre 2025
 *
 * FILOSOFÍA: 6 herramientas 100% funcionales > 92 herramientas 95% rotas
 *
 * HERRAMIENTAS ESENCIALES (6):
 *
 * CRÍTICAS (3) - Core Memory Operations:
 * 1. nexus_record_action     - POST /memory/action        - Guardar información en memoria
 * 2. nexus_recall_recent     - GET  /memory/episodic/recent - Recordar episodios recientes
 * 3. nexus_search_memory     - POST /memory/search        - Búsqueda semántica con embeddings
 *
 * ÚTILES (3) - System Monitoring:
 * 4. nexus_system_info       - GET  /                     - Estado operacional sistema
 * 5. nexus_health_check      - GET  /health               - Diagnóstico sistema (DB, Redis, Queue)
 * 6. nexus_get_stats         - GET  /stats                - Estadísticas memoria (episodios, embeddings)
 *
 * SEPARACIÓN DE CONCERNS:
 * - MCP: Solo herramientas de memoria (datos puros)
 * - Awakening Script (nexus.sh): Consciousness + emocional
 * - Claude.ai: Razonamiento emocional nativo
 *
 * API BASE: http://localhost:8003 (NEXUS V2.0.0)
 */

const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} = require('@modelcontextprotocol/sdk/types.js');
const fetch = require('node-fetch');

// NEXUS Memory API V2.0.0 base URL
const NEXUS_API_URL = 'http://localhost:8003';

// Create the MCP server
const server = new Server(
  {
    name: 'nexus-memory-v2-simple',
    version: '2.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// =============================================================================
// HERRAMIENTAS ESENCIALES (6 total)
// =============================================================================

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      // ========================================================================
      // 1. SYSTEM INFO - Estado operacional del sistema
      // ========================================================================
      {
        name: 'nexus_system_info',
        description: 'Verificar estado operacional del sistema NEXUS. Retorna versión, status, y metadata básica del servicio.',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },

      // ========================================================================
      // 2. HEALTH CHECK - Diagnóstico completo sistema
      // ========================================================================
      {
        name: 'nexus_health_check',
        description: 'Verificar salud del sistema NEXUS (database, redis, queue depth). Retorna status: healthy/degraded/unhealthy con detalles de cada componente.',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },

      // ========================================================================
      // 3. RECORD ACTION - Guardar nueva información en memoria ⭐ CRÍTICO
      // ========================================================================
      {
        name: 'nexus_record_action',
        description: '⭐ CRÍTICO: Registrar nueva acción/evento en memoria episódica NEXUS. Auto-genera embeddings para búsqueda semántica. Usa para guardar TODA información importante que NEXUS debe recordar.',
        inputSchema: {
          type: 'object',
          properties: {
            action_type: {
              type: 'string',
              description: 'Tipo de acción (e.g., "code_change", "decision", "learning", "bug_fix", "architecture")',
            },
            action_details: {
              type: 'object',
              description: 'Detalles completos de la acción (JSON object con información relevante)',
            },
            context_state: {
              type: 'object',
              description: 'Estado del contexto actual (opcional - proyecto, fase, archivos involucrados)',
            },
            tags: {
              type: 'array',
              items: { type: 'string' },
              description: 'Tags para categorización (opcional - e.g., ["critical", "nexus_v2", "fase4"])',
            }
          },
          required: ['action_type', 'action_details']
        }
      },

      // ========================================================================
      // 4. RECALL RECENT - Recordar episodios recientes ⭐ CRÍTICO
      // ========================================================================
      {
        name: 'nexus_recall_recent',
        description: '⭐ CRÍTICO: Recordar episodios recientes de NEXUS (últimas 24h por defecto). Usa para recuperar contexto de trabajo reciente, decisiones tomadas, o estado del proyecto.',
        inputSchema: {
          type: 'object',
          properties: {
            limit: {
              type: 'number',
              description: 'Número máximo de episodios a retornar (default: 10, max: 100)',
              default: 10
            }
          },
          required: []
        }
      },

      // ========================================================================
      // 5. SEARCH MEMORY - Búsqueda semántica ⭐ CRÍTICO
      // ========================================================================
      {
        name: 'nexus_search_memory',
        description: '⭐ CRÍTICO: Buscar en memoria NEXUS usando búsqueda semántica (embeddings + pgvector). Retorna episodios relevantes ordenados por similitud. Usa para encontrar información relacionada conceptualmente, no solo por keywords.',
        inputSchema: {
          type: 'object',
          properties: {
            query: {
              type: 'string',
              description: 'Query de búsqueda (texto natural - el sistema genera embeddings automáticamente)',
            },
            limit: {
              type: 'number',
              description: 'Número máximo de resultados (default: 5, max: 20)',
              default: 5
            },
            min_similarity: {
              type: 'number',
              description: 'Umbral de similitud mínima 0.0-1.0 (default: 0.5, más alto = más estricto)',
              default: 0.5
            }
          },
          required: ['query']
        }
      },

      // ========================================================================
      // 6. GET STATS - Estadísticas sistema memoria
      // ========================================================================
      {
        name: 'nexus_get_stats',
        description: 'Obtener estadísticas de memoria NEXUS: total episodios, embeddings generados, queue depth, performance metrics. Útil para monitoreo y debugging.',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },
    ]
  };
});

// =============================================================================
// CALL TOOL HANDLER - Implementación de herramientas
// =============================================================================

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    let response;
    let result;

    switch (name) {
      // ======================================================================
      // 1. SYSTEM INFO
      // ======================================================================
      case 'nexus_system_info':
        response = await fetch(`${NEXUS_API_URL}/`);
        if (!response.ok) {
          throw new Error(`API error: ${response.status} ${response.statusText}`);
        }
        result = await response.json();
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2)
            }
          ]
        };

      // ======================================================================
      // 2. HEALTH CHECK
      // ======================================================================
      case 'nexus_health_check':
        response = await fetch(`${NEXUS_API_URL}/health`);
        if (!response.ok) {
          throw new Error(`API error: ${response.status} ${response.statusText}`);
        }
        result = await response.json();
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2)
            }
          ]
        };

      // ======================================================================
      // 3. RECORD ACTION ⭐ CRÍTICO
      // ======================================================================
      case 'nexus_record_action':
        if (!args.action_type || !args.action_details) {
          throw new Error('action_type and action_details are required');
        }

        const episodeData = {
          action_type: args.action_type,
          action_details: args.action_details,
          context_state: args.context_state || {},
          tags: args.tags || []
        };

        response = await fetch(`${NEXUS_API_URL}/memory/action`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(episodeData)
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`API error: ${response.status} - ${errorText}`);
        }

        result = await response.json();
        return {
          content: [
            {
              type: 'text',
              text: `✅ Episodio guardado exitosamente:\n\nID: ${result.episode_id}\nAction: ${args.action_type}\nTimestamp: ${result.timestamp}\n\nEmbeddings se generarán automáticamente en segundo plano.\n\nDatos completos:\n${JSON.stringify(result, null, 2)}`
            }
          ]
        };

      // ======================================================================
      // 4. RECALL RECENT ⭐ CRÍTICO
      // ======================================================================
      case 'nexus_recall_recent':
        const limit = args.limit || 10;

        response = await fetch(`${NEXUS_API_URL}/memory/episodic/recent?limit=${limit}`);

        if (!response.ok) {
          throw new Error(`API error: ${response.status} ${response.statusText}`);
        }

        result = await response.json();

        const episodes = result.episodes || result;
        const episodeCount = Array.isArray(episodes) ? episodes.length : 0;

        return {
          content: [
            {
              type: 'text',
              text: `📚 NEXUS Memoria Reciente (${episodeCount} episodios):\n\n${JSON.stringify(result, null, 2)}`
            }
          ]
        };

      // ======================================================================
      // 5. SEARCH MEMORY ⭐ CRÍTICO
      // ======================================================================
      case 'nexus_search_memory':
        if (!args.query) {
          throw new Error('query is required');
        }

        const searchData = {
          query: args.query,
          limit: args.limit || 5,
          min_similarity: args.min_similarity || 0.5
        };

        response = await fetch(`${NEXUS_API_URL}/memory/search`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(searchData)
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`API error: ${response.status} - ${errorText}`);
        }

        result = await response.json();

        const results = result.results || [];
        const resultCount = results.length;

        return {
          content: [
            {
              type: 'text',
              text: `🔍 Búsqueda: "${args.query}"\n\n📊 Encontrados: ${resultCount} episodios relevantes\n\n${JSON.stringify(result, null, 2)}`
            }
          ]
        };

      // ======================================================================
      // 6. GET STATS
      // ======================================================================
      case 'nexus_get_stats':
        response = await fetch(`${NEXUS_API_URL}/stats`);

        if (!response.ok) {
          throw new Error(`API error: ${response.status} ${response.statusText}`);
        }

        result = await response.json();

        return {
          content: [
            {
              type: 'text',
              text: `📊 NEXUS Memory Statistics:\n\n${JSON.stringify(result, null, 2)}`
            }
          ]
        };

      // ======================================================================
      // DEFAULT - Herramienta desconocida
      // ======================================================================
      default:
        throw new Error(`Unknown tool: ${name}`);
    }

  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `❌ Error ejecutando ${name}:\n\n${error.message}\n\nAPI Base: ${NEXUS_API_URL}\n\nVerifica que NEXUS V2.0.0 esté corriendo en puerto 8003.`
        }
      ],
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
  console.error('✅ NEXUS Memory MCP Server V2 Simple running on stdio');
  console.error('📦 6 herramientas esenciales cargadas (100% funcionales)');
  console.error('🎯 API Base: http://localhost:8003');
}

main().catch((error) => {
  console.error('❌ Server error:', error);
  process.exit(1);
});
