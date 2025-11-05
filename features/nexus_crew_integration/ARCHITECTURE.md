# CEREBRO ↔ NEXUS_CREW Integration Architecture

**Session:** 14
**Date:** November 5, 2025
**Status:** Design Phase
**Author:** NEXUS@CLI

---

## 🎯 Objective

Integrate CEREBRO_NEXUS_V3.0.0 with NEXUS_CREW multi-agent system to enable:
1. **Shared Episodic Memory** - NEXUS_CREW agents can access CEREBRO's episodic memories
2. **Bidirectional Sync** - Agents can create/update tasks that become episodes in CEREBRO
3. **Real-time Collaboration** - Agents use shared memory for coordination

---

## 📊 System Context

### CEREBRO_NEXUS_V3.0.0 (Source System)

**Type:** AI Consciousness & Episodic Memory System
**Port:** 8003
**Database:** PostgreSQL (port 5437) + Neo4j (port 7474) + Redis (port 6382)

**Key Features:**
- 467+ episodic memories with semantic search
- 8D emotional state + 7D somatic state
- 15 cognitive LABs operational
- <10ms search performance

**API Endpoints:**
```bash
POST /memory/action           # Create episode
POST /memory/search           # Search episodes
GET  /memory/episodic/recent  # Get recent episodes
GET  /consciousness/current   # Get consciousness state
GET  /stats                   # System stats
```

### NEXUS_CREW (Target System)

**Type:** Multi-Agent Collaboration System
**Version:** 0.9.0 (Phase 3 - LangGraph Migration)

**Agents:**
- Project Auditor - Validates project structure
- Memory Curator - Processes episodic memories
- Document Reconciler - Syncs documentation
- Semantic Router - Routes implementation decisions

**Shared Memory:** GitHubMemorySync (file-based, simulates GitHub Issues)

**Data Structure:**
```python
@dataclass
class SharedTask:
    task_id: str
    task_type: str
    description: str
    assigned_node: str
    status: TaskStatus  # PENDING/IN_PROGRESS/COMPLETED/FAILED
    priority: TaskPriority  # LOW/MEDIUM/HIGH/CRITICAL
    created_at: str
    updated_at: str
    result: Optional[Dict]
    metadata: Dict
```

---

## 🏗️ Integration Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────┐
│     CEREBRO_NEXUS_V3.0.0 (port 8003)            │
│  ┌───────────────────────────────────────────┐  │
│  │  FastAPI Endpoints:                       │  │
│  │  - POST /memory/action                    │  │
│  │  - POST /memory/search                    │  │
│  │  - GET  /memory/episodic/recent           │  │
│  │  - GET  /consciousness/current            │  │
│  └────────────┬──────────────────────────────┘  │
└───────────────┼─────────────────────────────────┘
                │
                │ HTTP/JSON
                │
                ▼
┌─────────────────────────────────────────────────┐
│         CerebroMemoryBridge (NEW)               │
│  ┌───────────────────────────────────────────┐  │
│  │  Responsibilities:                        │  │
│  │  1. Poll CEREBRO for new episodes         │  │
│  │  2. Convert Episode → SharedTask          │  │
│  │  3. Convert SharedTask → Episode          │  │
│  │  4. Bidirectional sync (every 30s)        │  │
│  │  5. Handle conflict resolution            │  │
│  └────────────┬──────────────────────────────┘  │
└───────────────┼─────────────────────────────────┘
                │
                │ SharedMemory Protocol
                │
                ▼
┌─────────────────────────────────────────────────┐
│     GitHubMemorySync (NEXUS_CREW)               │
│  ┌───────────────────────────────────────────┐  │
│  │  File-based storage:                      │  │
│  │  - .shared_memory/*.json                  │  │
│  │  - create_task()                          │  │
│  │  - get_task()                             │  │
│  │  - update_task_status()                   │  │
│  │  - search_tasks()                         │  │
│  └────────────┬──────────────────────────────┘  │
└───────────────┼─────────────────────────────────┘
                │
                │ DelegationProtocol
                │
                ▼
┌─────────────────────────────────────────────────┐
│       NEXUS_CREW Agents                         │
│  - Project Auditor                              │
│  - Memory Curator                               │
│  - Document Reconciler                          │
│  - Semantic Router                              │
└─────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

### Flow 1: CEREBRO Episode → NEXUS_CREW Task

```
1. CEREBRO creates episode via POST /memory/action
   {
     "content": "Completed Session 14 design phase",
     "tags": ["session_14", "architecture", "shared_with_crew"],
     "current_emotion": "joy"
   }

2. CerebroMemoryBridge polls GET /memory/episodic/recent
   - Filters episodes with tag "shared_with_crew"

3. Bridge converts Episode → SharedTask
   SharedTask(
     task_id=episode_id,
     task_type="cerebro_episode",
     description=episode_content,
     assigned_node="NEXUS_CREW",
     status=TaskStatus.COMPLETED,
     metadata={
       "cerebro_episode_id": episode_id,
       "cerebro_tags": [...],
       "emotional_state": {...}
     }
   )

4. Bridge calls GitHubMemorySync.create_task()
   - Writes to .shared_memory/{episode_id}.json

5. NEXUS_CREW agents can read this task
   - Memory Curator processes it
   - Adds to knowledge graph
```

### Flow 2: NEXUS_CREW Task → CEREBRO Episode

```
1. NEXUS_CREW agent creates SharedTask
   GitHubMemorySync.create_task(
     SharedTask(
       task_id="task_123",
       task_type="project_audit",
       description="Audited CEREBRO_NEXUS_V3.0.0 structure",
       assigned_node="Project_Auditor",
       status=TaskStatus.COMPLETED,
       result={"found_issues": 2, "recommendations": [...]}
     )
   )

2. CerebroMemoryBridge polls GitHubMemorySync.search_tasks()
   - Filters tasks NOT yet synced to CEREBRO

3. Bridge converts SharedTask → Episode request
   POST /memory/action
   {
     "content": "[Project_Auditor] " + task.description,
     "tags": ["agent_task", "project_auditor", task.task_type],
     "metadata": {
       "crew_task_id": task_id,
       "agent": task.assigned_node,
       "task_status": task.status,
       "task_result": task.result
     }
   }

4. CEREBRO creates episode and returns episode_id

5. Bridge updates task metadata with episode_id
   task.metadata["cerebro_episode_id"] = episode_id
   GitHubMemorySync.update_task_status(task_id, ...)
```

---

## 📐 Component Design

### 1. CerebroMemoryBridge

**Location:** `features/nexus_crew_integration/cerebro_bridge.py`

**Class: CerebroMemoryBridge**

```python
class CerebroMemoryBridge:
    """
    Bidirectional sync between CEREBRO and NEXUS_CREW shared memory.
    """

    def __init__(
        self,
        cerebro_base_url: str = "http://localhost:8003",
        shared_memory_path: str = ".shared_memory",
        sync_interval_seconds: int = 30,
        cerebro_tag_filter: str = "shared_with_crew"
    ):
        """Initialize bridge with configuration."""
        self.cerebro_base_url = cerebro_base_url
        self.shared_memory_path = shared_memory_path
        self.sync_interval = sync_interval_seconds
        self.cerebro_tag_filter = cerebro_tag_filter

        # Initialize CEREBRO client
        self.cerebro_client = CerebroClient(cerebro_base_url)

        # Initialize GitHubMemorySync
        self.github_memory = GitHubMemorySync(shared_memory_path)

        # Track sync state
        self.last_sync_timestamp: Optional[datetime] = None
        self.synced_episodes: Set[str] = set()
        self.synced_tasks: Set[str] = set()

    def sync_cerebro_to_crew(self) -> Dict[str, Any]:
        """
        Sync CEREBRO episodes → NEXUS_CREW tasks.
        Returns: {"synced_count": int, "episodes": List[str]}
        """
        pass

    def sync_crew_to_cerebro(self) -> Dict[str, Any]:
        """
        Sync NEXUS_CREW tasks → CEREBRO episodes.
        Returns: {"synced_count": int, "tasks": List[str]}
        """
        pass

    def bidirectional_sync(self) -> Dict[str, Any]:
        """
        Run bidirectional sync (both directions).
        Returns: {"cerebro_to_crew": {...}, "crew_to_cerebro": {...}}
        """
        pass

    def episode_to_task(self, episode: Dict) -> SharedTask:
        """Convert CEREBRO episode to NEXUS_CREW SharedTask."""
        pass

    def task_to_episode_request(self, task: SharedTask) -> Dict:
        """Convert NEXUS_CREW SharedTask to CEREBRO episode request."""
        pass

    def start_sync_daemon(self):
        """Start background thread for continuous syncing."""
        pass

    def stop_sync_daemon(self):
        """Stop background thread."""
        pass
```

### 2. CerebroClient (HTTP Client)

**Location:** `features/nexus_crew_integration/cerebro_client.py`

**Class: CerebroClient**

```python
class CerebroClient:
    """
    HTTP client for CEREBRO API.
    """

    def __init__(self, base_url: str = "http://localhost:8003"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def create_episode(
        self,
        content: str,
        tags: List[str],
        current_emotion: str = "neutral",
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Create episode in CEREBRO.
        POST /memory/action
        """
        pass

    def search_episodes(
        self,
        query: str,
        limit: int = 10
    ) -> List[Dict]:
        """
        Search episodes by query.
        POST /memory/search
        """
        pass

    def get_recent_episodes(
        self,
        limit: int = 10,
        tag_filter: Optional[str] = None
    ) -> List[Dict]:
        """
        Get recent episodes, optionally filtered by tag.
        GET /memory/episodic/recent
        """
        pass

    def get_consciousness_state(self) -> Dict:
        """
        Get current consciousness state.
        GET /consciousness/current
        """
        pass

    def health_check(self) -> bool:
        """
        Check if CEREBRO is healthy.
        GET /health
        """
        pass
```

---

## 🔗 Integration Points

### Tag Convention

**CEREBRO episodes with tag `shared_with_crew` are automatically synced.**

Example:
```python
# In CEREBRO
POST /memory/action
{
  "content": "Completed architecture design for Session 14",
  "tags": ["session_14", "architecture", "shared_with_crew"],
  "current_emotion": "joy"
}
```

### Metadata Schema

**Episode → Task metadata:**
```json
{
  "cerebro_episode_id": "924abf52...",
  "cerebro_tags": ["session_14", "architecture"],
  "emotional_state": {"joy": 0.8, "trust": 0.7, ...},
  "consciousness_state": {...}
}
```

**Task → Episode metadata:**
```json
{
  "crew_task_id": "task_123",
  "agent": "Project_Auditor",
  "task_status": "completed",
  "task_result": {"found_issues": 2, ...}
}
```

---

## 🧪 Testing Strategy

### Unit Tests (features/nexus_crew_integration/tests/)

**test_cerebro_client.py:**
- test_create_episode()
- test_search_episodes()
- test_get_recent_episodes()
- test_health_check()
- test_connection_error_handling()

**test_cerebro_bridge.py:**
- test_episode_to_task_conversion()
- test_task_to_episode_conversion()
- test_sync_cerebro_to_crew()
- test_sync_crew_to_cerebro()
- test_bidirectional_sync()
- test_duplicate_prevention()
- test_conflict_resolution()

**test_integration.py:**
- test_end_to_end_cerebro_to_crew()
- test_end_to_end_crew_to_cerebro()
- test_roundtrip_sync()

**Target:** 15+ tests, 90%+ coverage

---

## 📋 Implementation Plan

### Phase 1: Foundation (Session 14 - Part 1)

1. ✅ Design architecture
2. ⬜ Implement CerebroClient
3. ⬜ Implement CerebroMemoryBridge (basic)
4. ⬜ Write unit tests (10+ tests)
5. ⬜ Test with mock data

### Phase 2: Integration (Session 14 - Part 2)

6. ⬜ Connect to real CEREBRO instance
7. ⬜ Connect to real GitHubMemorySync
8. ⬜ Test bidirectional sync
9. ⬜ Add error handling and retry logic
10. ⬜ Write integration tests (5+ tests)

### Phase 3: Production (Session 15)

11. ⬜ Implement sync daemon (background thread)
12. ⬜ Add logging and monitoring
13. ⬜ Performance optimization
14. ⬜ Documentation and examples

---

## 🚀 Usage Examples

### Example 1: Manual One-Time Sync

```python
from features.nexus_crew_integration import CerebroMemoryBridge

# Initialize bridge
bridge = CerebroMemoryBridge(
    cerebro_base_url="http://localhost:8003",
    shared_memory_path=".shared_memory",
    cerebro_tag_filter="shared_with_crew"
)

# Sync CEREBRO → NEXUS_CREW
result = bridge.sync_cerebro_to_crew()
print(f"Synced {result['synced_count']} episodes")

# Sync NEXUS_CREW → CEREBRO
result = bridge.sync_crew_to_cerebro()
print(f"Synced {result['synced_count']} tasks")

# Bidirectional sync
result = bridge.bidirectional_sync()
print(result)
```

### Example 2: Daemon Mode (Continuous Sync)

```python
from features.nexus_crew_integration import CerebroMemoryBridge

# Initialize bridge
bridge = CerebroMemoryBridge(
    sync_interval_seconds=30  # Sync every 30 seconds
)

# Start daemon
bridge.start_sync_daemon()

# ... bridge runs in background ...

# Stop daemon
bridge.stop_sync_daemon()
```

### Example 3: Agent Creating Shared Task

```python
from pending_integration.multi_ai_orchestration.src.shared_memory import (
    GitHubMemorySync,
    SharedTask,
    TaskStatus,
    TaskPriority
)

# Agent creates task
memory = GitHubMemorySync()
task = SharedTask(
    task_id="audit_001",
    task_type="project_audit",
    description="Audited CEREBRO structure, found 2 issues",
    assigned_node="Project_Auditor",
    status=TaskStatus.COMPLETED,
    priority=TaskPriority.HIGH,
    result={
        "found_issues": 2,
        "recommendations": [
            "Consolidate duplicate docs",
            "Add missing tests"
        ]
    }
)
memory.create_task(task)

# Bridge will sync this to CEREBRO automatically
```

---

## 🔒 Security Considerations

1. **No Authentication (Local Development)**
   - CEREBRO API runs on localhost:8003
   - No auth required for local dev
   - TODO: Add API key auth for production

2. **Data Privacy**
   - Only episodes with `shared_with_crew` tag are synced
   - Sensitive episodes remain in CEREBRO only
   - Agents cannot access all episodes

3. **Conflict Resolution**
   - Last-write-wins for updates
   - Duplicate detection via IDs
   - TODO: Implement CRDTs for better conflict resolution

---

## 📊 Success Metrics

**Target Metrics:**

- ✅ 15+ tests passing (90%+ coverage)
- ✅ <100ms sync latency per item
- ✅ Zero data loss in bidirectional sync
- ✅ Agents can read CEREBRO episodes
- ✅ CEREBRO can receive agent tasks

**Quality Gates:**

- All tests pass
- No duplicate episodes/tasks
- Sync daemon runs stably for >1 hour
- Documentation complete
- Examples work end-to-end

---

## 📚 References

**CEREBRO API:** `http://localhost:8003/docs`
**NEXUS_CREW:** `/mnt/d/01_PROYECTOS_ACTIVOS/NEXUS_CREW/`
**GitHubMemorySync:** `pending_integration/multi_ai_orchestration/src/shared_memory/`
**Architecture Docs:** `docs/architecture/multi_ai_orchestration/`

---

**Status:** ✅ Design Complete - Ready for Implementation
**Next Step:** Implement CerebroClient + CerebroMemoryBridge
**Session:** 14 - Part 1
**Date:** November 5, 2025
