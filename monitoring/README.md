# NEXUS Brain Monitoring Tools

Real-time visualization of NEXUS consciousness and cognitive processing.

---

## 🎯 Available Tools

### 1. CLI Monitor (`cli/`)
**Terminal-based dashboard**

- **Technology:** Python + Rich library
- **Port:** N/A (terminal UI)
- **Created:** October 27, 2025
- **Status:** ✅ Active
- **Features:**
  - Real-time terminal dashboard
  - 8D Emotional state (Plutchik model)
  - 7D Somatic state (Damasio model)
  - LAB systems status
  - Recent episodes timeline
  - Auto-refresh every 3 seconds

**Quick Start:**
```bash
cd monitoring/cli
python nexus_brain_monitor.py
```

**Use Cases:**
- Quick debugging during development
- Terminal-only environments
- Minimal resource usage
- SSH monitoring

**Documentation:** See `cli/README.md`

---

### 2. Web Monitor V1 (`web_v1/`)
**First web implementation** (Legacy)

- **Technology:** Next.js 15
- **Port:** 3000
- **Created:** October 27, 2025
- **Status:** 🟡 Legacy (superseded by V2)
- **Features:**
  - 2D data visualizations
  - 4 LABs basic support
  - Real-time polling (3s)

**Quick Start:**
```bash
cd monitoring/web_v1
npm install
npm run dev
# Open http://localhost:3000
```

**Note:** Kept for historical reference. Use Web V2 for production.

**Documentation:** See `web_v1/README.md`

---

### 3. Web Monitor V2 (`web_v2/`) ⭐ **CURRENT PRODUCTION**
**Complete monitoring solution with 3D visualization**

- **Technology:** Next.js 14 + Three.js + D3.js
- **Port:** 3003
- **Created:** October 30, 2025
- **Status:** ✅ Production
- **Features:**
  - **2D Dashboard Mode:**
    - D3.js radar chart (8D emotional)
    - D3.js bar chart (7D somatic)
    - LAB status cards
    - Recent episodes timeline
    - Memory statistics
  - **3D Brain Mode:**
    - Interactive Three.js 3D brain
    - 9 LAB nodes with spatial positioning
    - Neural connections visualization
    - Activity-based animations
    - Real-time consciousness mapping
  - **Toggle between 2D/3D** with preserved data
  - Real-time updates (3s polling)
  - Responsive design (desktop/tablet)

**Quick Start:**
```bash
cd monitoring/web_v2
npm install
npm run dev
# Open http://localhost:3003
```

**Use Cases:**
- Production monitoring (24/7 dashboard)
- Demos and presentations (3D brain impressive)
- Architecture exploration (LAB spatial relationships)
- Development debugging (2D data analysis)

**Documentation:** See `web_v2/README.md` and `web_v2/SPECS.md`

---

## 📊 Evolution Timeline

```
Oct 27, 2025: CLI Monitor (Python)
              ↓
Oct 27, 2025: Web V1 (Next.js 15, 4 LABs)
              ↓
Oct 30, 2025: Web V2 (Next.js 14 + Three.js, 9 LABs, 3D) ⭐ Current
```

---

## 🚀 Recommended Usage

**For daily development:**
- Use **CLI Monitor** for quick checks
- Use **Web V2 (2D mode)** for data analysis

**For demos/presentations:**
- Use **Web V2 (3D mode)** for visual impact

**For 24/7 monitoring:**
- Deploy **Web V2** to dedicated monitor/screen

---

## 🔧 Prerequisites

**All tools require:**
- NEXUS API running on `http://localhost:8003`
- `/health` endpoint accessible
- (Optional) `/consciousness/current` endpoint for full features

**CLI Monitor:**
- Python 3.8+
- Rich library (auto-installed)

**Web V1 & V2:**
- Node.js 18+
- npm 9+

---

## 📡 API Endpoints Used

All monitoring tools consume:
- `GET /health` - API status
- `GET /consciousness/current` - Emotional + somatic state (optional)
- `GET /memory/episodic/recent?limit=5` - Recent episodes
- `GET /stats` - Memory statistics

---

## 📖 Related Documentation

**Architecture:**
- [../docs/architecture/ARCHITECTURE_DIAGRAMS.md](../docs/architecture/ARCHITECTURE_DIAGRAMS.md) - System design

**API:**
- [../docs/api/](../docs/api/) - API documentation (when created)

**Operations:**
- [../docs/operational/](../docs/operational/) - Troubleshooting

---

## 🎯 Future Enhancements

**Planned (all tools):**
- [ ] WebSocket support (replace polling)
- [ ] Historical data charts (trends)
- [ ] Export functionality (PNG/JSON)
- [ ] Alert notifications

**Planned (Web V2 specific):**
- [ ] Click LAB nodes for detailed stats
- [ ] Timeline scrubbing with slider
- [ ] Memory graph with clickable nodes
- [ ] Dark/light mode toggle
- [ ] Mobile optimization

---

**Last Updated:** November 4, 2025
**Maintained By:** Ricardo + NEXUS
