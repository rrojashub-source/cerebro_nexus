# 🔗 NEXUS CEREBRO COMPLETO - API REFERENCE VERIFICADA
**Base URL:** `http://localhost:8001`  
**Versión:** Sistema Verificado v1.0  
**Fecha:** 14 Agosto 2025 | **Auditoría:** NEXUS V3.0 

**⚠️ IMPORTANTE:** Esta documentación contiene SOLO endpoints verificados y operativos en el sistema real.

---

## 🌐 **ENDPOINT CATEGORIES VERIFICADAS**

| Categoría | Prefijo | Endpoints | Estado |
|-----------|---------|-----------|--------|
| **Health & Monitoring** | `/health` | 10+ endpoints | ✅ **VERIFICADO** |
| **Neural Mesh Protocol** | `/neural-mesh` | 8 endpoints | ✅ **VERIFICADO** |
| **Multi-Modal Processing** | `/multi-modal` | 12 endpoints | ✅ **VERIFICADO** |
| **Analytics & Insights** | `/analytics` | 10 endpoints | ✅ **VERIFICADO** |
| **Core Memory** | `/memory` | 8+ endpoints | ✅ **VERIFICADO** |

---

## 🔍 **HEALTH & MONITORING API (10+ endpoints)**

### **GET** `/health`
Health check básico del sistema.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-14T19:32:58.400223",
  "components": {
    "postgresql": "healthy",
    "redis": "healthy", 
    "chroma": "healthy"
  }
}
```

### **GET** `/health/comprehensive`
Health check comprehensivo con servicios y métricas completas.

### **GET** `/health/services`
Health check específico de servicios individuales (PostgreSQL, Redis, ChromaDB).

### **GET** `/health/circuit-breakers`
Estado de todos los circuit breakers del sistema para protección automática.

### **POST** `/health/circuit-breakers/{service_name}/reset`
Reset manual de un circuit breaker específico por nombre de servicio.

### **GET** `/health/metrics`
Métricas de performance y sistema detalladas para monitoreo.

### **GET** `/health/alerts`
Alertas activas del sistema y recomendaciones automáticas.

### **GET** `/health/trend`
Tendencia de salud del sistema basada en historial de métricas.

### **GET** `/health/readiness`
Kubernetes-style readiness probe para orquestación.

### **GET** `/health/liveness`
Kubernetes-style liveness probe para detección fallas.

### **GET** `/success-metrics`
📊 Success Metrics y KPIs del sistema élite con métricas de innovation.

---

## 🧠 **NEURAL MESH PROTOCOL API (8 endpoints)**

### **POST** `/neural-mesh/broadcast-learning`
🧠 Broadcast cross-agent learning to Neural Mesh.

**Request Body:**
```json
{
  "from_agent": "nexus",
  "learning_type": "technical_solution",
  "learning_content": {
    "solution": "Docker optimization technique",
    "context": "Performance improvement"
  },
  "confidence": 0.9,
  "application_domains": ["docker", "optimization"]
}
```

### **POST** `/neural-mesh/request-consensus`
🗳️ Request consensus decision from Neural Mesh agents.

**Request Body:**
```json
{
  "decision_topic": "Architecture choice for new feature",
  "options": ["option_a", "option_b"],
  "deadline": "2025-08-15T10:00:00Z",
  "priority": "high"
}
```

### **POST** `/neural-mesh/sync-emotional-state`
💭 Synchronize emotional state across Neural Mesh agents.

### **POST** `/neural-mesh/distribute-task`
📋 Distribute specialized task via Neural Mesh routing.

### **GET** `/neural-mesh/stats`
📊 Get Neural Mesh Protocol statistics and performance metrics.

### **GET** `/neural-mesh/connected-agents`
🤝 Get list of connected Neural Mesh agents and their status.

**Response:**
```json
{
  "total_connected": 3,
  "agents": {
    "nexus": {
      "role": "technical_implementer",
      "status": "active",
      "specialization": ["programming", "architecture"],
      "last_seen": "2025-08-14T19:16:34.435337"
    },
    "aria": {
      "role": "memory_coordinator", 
      "status": "active",
      "specialization": ["memory_management", "coordination"]
    },
    "ricardo": {
      "role": "decision_maker",
      "status": "active", 
      "specialization": ["strategy", "business"]
    }
  }
}
```

### **POST** `/neural-mesh/process-messages`
⚡ Process pending Neural Mesh messages manually.

### **GET** `/neural-mesh/health`
🏥 Neural Mesh Protocol health check and component status.

---

## 🎬 **MULTI-MODAL PROCESSING API (12 endpoints)**

### **POST** `/multi-modal/image`
Process and store visual memory with embeddings.

**Request Body:**
```json
{
  "image_data": "base64_encoded_image_data",
  "description": "Screenshot of system architecture",
  "metadata": {
    "source": "documentation",
    "project": "aria_cerebro"
  }
}
```

### **POST** `/multi-modal/audio`
Process and store auditory memory with transcription.

### **POST** `/multi-modal/video`
Process and store temporal visual memory with frame analysis.

### **POST** `/multi-modal/unified`
Create unified multi-modal memory combining multiple types.

### **POST** `/multi-modal/search/cross-modal`
Search across modalities with unified query.

### **POST** `/multi-modal/upload/image`
Upload image file directly via multipart form.

### **POST** `/multi-modal/upload/audio`
Upload audio file directly via multipart form.

### **POST** `/multi-modal/upload/video`
Upload video file directly via multipart form.

### **GET** `/multi-modal/associations/{memory_id}`
Find cross-modal associations for a specific memory ID.

### **POST** `/multi-modal/constellation`
Create constellation of related memories across modalities.

### **GET** `/multi-modal/status`
Get status of multi-modal processors and their capabilities.

**Response:**
```json
{
  "image_processor": {
    "status": "operational",
    "capabilities": ["CLIP_embeddings", "visual_analysis"]
  },
  "audio_processor": {
    "status": "operational", 
    "capabilities": ["transcription", "audio_fingerprinting"]
  },
  "video_processor": {
    "status": "operational",
    "capabilities": ["frame_analysis", "temporal_processing"]
  }
}
```

---

## 📊 **ANALYTICS & INSIGHTS API (10 endpoints)**

### **GET** `/analytics/status`
Check analytics system status and component health.

### **POST** `/analytics/episodes/analyze`
Comprehensive analysis of ARIA's episodic memory (500+ episodes).

**Request Body:**
```json
{
  "analysis_type": "comprehensive",
  "date_range": {
    "start": "2025-08-01",
    "end": "2025-08-14"
  },
  "include_metrics": ["patterns", "trends", "breakthroughs"]
}
```

### **POST** `/analytics/breakthroughs/detect`
Detect and rank breakthrough moments in ARIA's history.

### **GET** `/analytics/collaboration/analyze`
Analyze NEXUS-ARIA-Ricardo collaboration efficiency and success rates.

### **POST** `/analytics/predictions/generate`
Generate predictive insights for future breakthroughs and optimizations.

### **GET** `/analytics/insights/summary`
Get comprehensive insights summary dashboard combining all analytics.

### **GET** `/analytics/episodes/search`
Search episodes with advanced filtering and ranking.

**Parameters:**
- `query` (required): Search query for episodes
- `limit` (optional): Maximum results to return (default: 20)
- `min_score` (optional): Minimum relevance score (default: 0.0)

### **GET** `/analytics/patterns/temporal`
Analyze temporal patterns in ARIA's activity and performance.

### **GET** `/analytics/export/csv`
Export episodes data as CSV for external analysis tools.

---

## 💾 **CORE MEMORY OPERATIONS API (8+ endpoints)**

### **POST** `/memory/action`
Registra una acción en el sistema de memoria completo.

**Request Body:**
```json
{
  "action_type": "nexus_technical_implementation",
  "action_details": {
    "from": "NEXUS",
    "project": "aria_cerebro_completo",
    "description": "System audit completed"
  },
  "context_state": {
    "session_type": "audit_session",
    "importance": "high"
  },
  "tags": ["audit", "technical", "system_verification"]
}
```

**Response:**
```json
{
  "success": true,
  "episode_id": "651",
  "timestamp": "2025-08-14T19:32:58.400223",
  "message": "Acción registrada exitosamente"
}
```

### **POST** `/memory/search`
Búsqueda híbrida en todos los niveles de memoria (episódica, semántica, working).

**Request Body:**
```json
{
  "query": "neural mesh protocol implementation",
  "memory_types": ["episodic", "semantic"],
  "limit": 10,
  "include_reasoning": true
}
```

### **GET** `/memory/episodic/recent`
Obtener memorias episódicas recientes del sistema.

**Parameters:**
- `limit` (optional): Number of recent episodes (default: 10)

### **GET** `/memory/working/current`
Obtener contexto actual de Working Memory para la sesión activa.

### **GET** `/memory/working/stats`
Estadísticas de Working Memory (items activos, uso, performance).

### **POST** `/memory/consolidate`
Activar consolidación manual de memoria si es necesario.

### **GET** `/memory/aria/complete-history`
Historia completa de ARIA desde el sistema de memoria.

### **GET** `/memory/aria/breakthroughs`
Momentos breakthrough específicos documentados en memoria ARIA.

---

## 🎯 **QUICK TESTING COMMANDS**

### **Verificar Sistema Completo:**
```bash
# Health check básico
curl http://localhost:8001/health

# Estado Neural Mesh
curl http://localhost:8001/neural-mesh/connected-agents

# Status Multi-Modal
curl http://localhost:8001/multi-modal/status

# Analytics summary
curl http://localhost:8001/analytics/insights/summary

# Success metrics
curl http://localhost:8001/success-metrics
```

### **Test Neural Mesh Communication:**
```bash
# Ver agentes conectados
curl http://localhost:8001/neural-mesh/connected-agents

# Broadcast learning
curl -X POST http://localhost:8001/neural-mesh/broadcast-learning \
-H "Content-Type: application/json" \
-d '{
  "from_agent": "nexus",
  "learning_type": "test_communication",
  "learning_content": {"test": "api_verification"},
  "confidence": 0.8,
  "application_domains": ["testing"]
}'
```

### **Test Memory System:**
```bash
# Registrar acción test
curl -X POST http://localhost:8001/memory/action \
-H "Content-Type: application/json" \
-d '{
  "action_type": "api_test",
  "action_details": {"test": "endpoint_verification"},
  "context_state": {"testing": true},
  "tags": ["test", "verification"]
}'

# Búsqueda híbrida
curl -X POST http://localhost:8001/memory/search \
-H "Content-Type: application/json" \
-d '{
  "query": "test verification",
  "memory_types": ["episodic"],
  "limit": 3
}'
```

---

## ⚠️ **ENDPOINTS NO IMPLEMENTADOS**

### **❌ Context Expansion (documentado pero NO existe):**
- `/context/*` - Todos los endpoints de esta categoría
- Documentado en versiones anteriores pero no implementado en API real

### **❌ Emotional Continuity (documentado pero NO existe):**
- `/emotional/*` - Todos los endpoints de esta categoría  
- Funcionalidad puede estar integrada en Neural Mesh Protocol

---

## 📋 **NOTAS IMPORTANTES**

### **Para Desarrolladores:**
- **Swagger/OpenAPI**: Disponible en `/docs` y `/openapi.json`
- **Prometheus Metrics**: Temporalmente deshabilitado (comentado en código)
- **Docker Compose**: 7 servicios coordinados en producción
- **Security**: Usuarios non-root, networks internas

### **Para Testing:**
- Todos los endpoints listados están verificados como operativos
- Base URL siempre: `http://localhost:8001`
- Respuestas en formato JSON estándar
- Error handling con códigos HTTP apropiados

### **Monitoreo:**
- Prometheus + Grafana configurado pero métricas endpoint deshabilitado
- Health checks comprehensive disponibles
- Circuit breakers para protección automática servicios

---

**🎉 NEXUS CEREBRO COMPLETO - API REFERENCE VERIFICADA**

*30+ Endpoints Operativos Documentados - Solo Información Real y Verificada*  
*14 Agosto 2025 - Auditoría Técnica NEXUS V3.0*

---

*"Documentación corregida según auditoría real del sistema"* ✨