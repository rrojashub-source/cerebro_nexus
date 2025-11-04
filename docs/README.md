# CEREBRO_NEXUS_V3.0.0 - Documentation

**Complete technical documentation for NEXUS Master Brain Orchestrator**

---

## 📚 Documentation Structure

### **Root Files (Start Here)**

- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes
- **[ROADMAP.md](ROADMAP.md)** - Future development plans

---

### **🧪 [../experiments/](../experiments/)**
**Cognitive LABs (50 LABs Architecture) - 16/50 Operational**

- `README.md` - Overview of 50 LABs system (5-layer architecture)
- `LAB_REGISTRY.json` - Complete registry of all 50 LABs
- `MASTER_BLUEPRINT_50_LABS.md` - Complete neuroscience-based design (107KB)
- `INTEGRATION_GUIDE_LABS_029_050.md` - Integration guide for LABs 029-050

**Layer Documentation:**
- `LAYER_1_Memory_Substrate/README.md` - PostgreSQL + pgvector + Redis
- `LAYER_2_Cognitive_Loop/README.md` - 8 operational LABs (141K lines)
- `LAYER_3_Neurochemistry_Base/README.md` - 4 operational LABs (74K lines)
- `LAYER_4_Neurochemistry_Full/README.md` - 5 designed LABs (not implemented)
- `LAYER_5_Higher_Cognition/README.md` - 29 designed LABs (not implemented)

**Status:** 16/50 LABs operational (32%)

---

### **📐 [architecture/](architecture/)**
**System design, architecture diagrams, and technical specifications**

- `ARCHITECTURE_DIAGRAMS.md` - Visual system architecture (Mermaid diagrams)
- `ORCHESTRATION_PROTOCOL.md` - Multi-agent orchestration design
- `CONSCIOUSNESS_IMPLEMENTATION_2025-10-24.md` - Consciousness layer implementation

---

### **📖 [guides/](guides/)**
**How-to guides and best practices**

- `CONTRIBUTING.md` - Contribution guidelines
- `GIT_COMMIT_GUIDE.md` - Git workflow and commit conventions
- `HANDOFF_TO_NEXUS_CLAUDE_CODE.md` - Context handoff between AI assistants

---

### **🔧 [operational/](operational/)**
**Operations, maintenance, backup, and troubleshooting**

- `BACKUP_SYSTEM_GUIDE.md` - Complete backup system documentation
- `BACKUP_QUICK_REFERENCE.md` - Quick backup commands reference
- `TROUBLESHOOTING.md` - Common issues and solutions

---

### **📊 [monitoring/](monitoring/)**
**Monitoring tools documentation**

- `BRAIN_MONITOR_V2_README.md` - Brain Monitor V2 overview
- `BRAIN_MONITOR_V2_SPECS.md` - Complete specifications

See also: `../monitoring/` (actual tools: CLI, Web V1, Web V2)

---

### **🔌 [api/](api/)**
**API reference and endpoint documentation**

*(To be populated with API docs)*

---

### **📜 [history/](history/)**
**Historical documentation from V2.0.0 development**

Includes:
- `PROJECT_DNA.md` - V2.0.0 project history
- `PROCESSING_LOG.md` - Development processing log
- FASE_* folders - Historical phase documentation
- Legacy implementation docs

**Note:** History docs are preserved for reference but not actively maintained.

---

## 🚀 Quick Navigation

**For new developers:**
1. Read [../PROJECT_ID.md](../PROJECT_ID.md) - System overview
2. Read [../README.md](../README.md) - Quick start
3. Read [../experiments/README.md](../experiments/README.md) - 50 LABs architecture
4. Read [architecture/ARCHITECTURE_DIAGRAMS.md](architecture/ARCHITECTURE_DIAGRAMS.md) - System design
5. Read [operational/TROUBLESHOOTING.md](operational/TROUBLESHOOTING.md) - Common issues

**For contributors:**
1. Read [guides/CONTRIBUTING.md](guides/CONTRIBUTING.md)
2. Read [guides/GIT_COMMIT_GUIDE.md](guides/GIT_COMMIT_GUIDE.md)

**For operations:**
1. Read [operational/BACKUP_SYSTEM_GUIDE.md](operational/BACKUP_SYSTEM_GUIDE.md)
2. Read [operational/TROUBLESHOOTING.md](operational/TROUBLESHOOTING.md)

---

## 📝 Documentation Standards

### Markdown Format
- Use GitHub-flavored Markdown
- Include table of contents for long docs (>200 lines)
- Use Mermaid for diagrams

### File Naming
- Use SCREAMING_SNAKE_CASE for general docs (e.g., ARCHITECTURE.md)
- Use lowercase with hyphens for specific guides (e.g., backup-guide.md)

### Updates
- Update CHANGELOG.md for significant changes
- Keep docs synchronized with code
- Archive obsolete docs to history/

---

**Last Updated:** November 4, 2025
**Maintained By:** Ricardo + NEXUS
