# 🧠 NEXUS Brain Monitor v2.0

Real-time 3D visualization of NEXUS Brain Orchestrator cognitive processing

[![Next.js](https://img.shields.io/badge/Next.js-14.0-black)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-18.2-blue)](https://reactjs.org/)
[![Three.js](https://img.shields.io/badge/Three.js-0.158-orange)](https://threejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-blue)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 Overview

**Brain Monitor v2.0** is a Next.js web application that provides real-time 3D visualization of the [NEXUS Brain Orchestrator v1.1](https://github.com/rrojashub-source/cerebro-master-nexus-001) cognitive processing system.

**Key Features:**
- 🧠 Interactive 3D brain model with anatomically positioned LAB nodes
- ⚡ Real-time processing visualization (7-10ms response times)
- 📊 Live performance metrics and LAB activity status
- 💭 Working memory display (7±2 items, Miller's Law)
- 🎯 Query-based episodic memory retrieval interface
- 🌊 Animated data flow between cognitive modules

---

## 🎥 Demo

> **Note:** Demo coming soon after initial implementation

**Live Demo:** [https://nexus-brain-monitor.vercel.app](https://nexus-brain-monitor.vercel.app) *(pending deployment)*

**Screenshots:**

*(To be added after implementation)*

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│ Brain Monitor v2.0                      │
│ (Next.js 14 + React 18 + Three.js)     │
│ Port: 3003                              │
└─────────────────────────────────────────┘
                 ↓ HTTP REST API
┌─────────────────────────────────────────┐
│ Brain Orchestrator v1.1                 │
│ (FastAPI + Python + PostgreSQL)         │
│ Port: 8003                              │
└─────────────────────────────────────────┘
```

**Tech Stack:**
- **Frontend:** Next.js 14 (App Router), React 18, TypeScript 5.2
- **3D Graphics:** Three.js, React Three Fiber
- **Styling:** TailwindCSS 3.3
- **Data Fetching:** SWR, Axios
- **Charts:** Recharts

---

## 🚀 Quick Start

### Prerequisites

```bash
Node.js >= 18.0.0
npm >= 9.0.0
```

### Installation

```bash
# Clone the repository
git clone https://github.com/rrojashub-source/nexus-brain-monitor-v2.git
cd nexus-brain-monitor-v2

# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3003](http://localhost:3003) in your browser.

### Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8003
```

---

## 🧪 Prerequisites: Brain Orchestrator v1.1

Brain Monitor v2.0 requires the **NEXUS Brain Orchestrator v1.1** backend running on port 8003.

### Quick Start (Backend)

```bash
# Clone Brain Orchestrator repo
git clone https://github.com/rrojashub-source/cerebro-master-nexus-001.git
cd cerebro-master-nexus-001/FASE_4_CONSTRUCCION

# Start with Docker Compose
docker-compose up -d

# Verify health
curl http://localhost:8003/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "agent_id": "nexus",
  "database": "connected",
  "redis": "connected"
}
```

📖 **Full Backend Setup:** See [Brain Orchestrator Documentation](https://github.com/rrojashub-source/cerebro-master-nexus-001/blob/main/FASE_8_UPGRADE/MASTER_BLUEPRINT_CEREBRO_SINTETICO.md)

---

## 📋 Features

### ✅ Implemented (v2.0)

- [x] 3D brain visualization with 9 LAB nodes
- [x] Real-time LAB status grid
- [x] Query processing interface
- [x] Working memory panel
- [x] Performance metrics display
- [x] Animated LAB interactions
- [x] Dark theme with neon accents
- [x] Responsive design (desktop/tablet)

### 🚧 Roadmap (Future)

- [ ] Emotional radar chart (8 dimensions)
- [ ] Somatic state visualization (7 dimensions)
- [ ] Episode timeline with history
- [ ] WebSocket real-time updates
- [ ] LAB details modal
- [ ] Export functionality (JSON/CSV)
- [ ] Mobile optimization

---

## 🎯 Usage

### Processing a Query

1. Enter a query in the input field (e.g., "docker network problems")
2. Select emotional context (focused, curious, stressed, calm)
3. Click "Process Query"
4. Watch LAB nodes light up in 3D as they process
5. View retrieved memories in Working Memory panel

### 3D Controls

- **Rotate:** Left-click + drag
- **Zoom:** Mouse scroll
- **Pan:** Right-click + drag
- **Reset:** Double-click brain

### View Modes

- **3D Brain View:** Interactive 3D brain with LAB nodes
- **2D Dashboard:** Charts, metrics, and timeline (upcoming)

---

## 🧠 Active LABs (9/50)

The Brain Monitor visualizes these 9 active cognitive modules:

| LAB ID | Name | Function | Brain Region |
|--------|------|----------|--------------|
| LAB_001 | Emotional Salience | Memory formation scoring | Amygdala |
| LAB_006 | Metacognition | Self-awareness & confidence | Lateral PFC |
| LAB_007 | Predictive Preloading | Query anticipation | Dorsolateral PFC |
| LAB_008 | Emotional Contagion | Context spreading | Limbic system |
| LAB_009 | Memory Reconsolidation | Memory updating | Hippocampus |
| LAB_010 | Attention Mechanism | Selective attention | Parietal cortex |
| LAB_011 | Working Memory | 7±2 item buffer | Temporal lobe |
| LAB_012 | Future Thinking | Episodic simulation | Frontal lobe |
| LAB_028 | Emotional Intelligence | Emotion regulation | Orbitofrontal cortex |

**Remaining 41 LABs:** Planned in NEXUS roadmap (Layers 4 & 5)

---

## 📡 API Endpoints

Brain Monitor v2.0 consumes these Brain Orchestrator endpoints:

### `GET /health`
Health check and connection status

### `POST /brain/process`
Process episodic memory query through 9 LABs

**Request:**
```json
{
  "query": "docker network problems",
  "context": {
    "current_emotion": "focused",
    "goal": "understand debugging"
  }
}
```

**Response:** See [SPECS.md#API Integration](./SPECS.md#api-integration)

---

## 🛠️ Development

### Project Structure

```
nexus-brain-monitor-v2/
├── app/
│   ├── page.tsx              # Main page
│   └── layout.tsx            # Root layout
├── components/
│   ├── BrainModel3D.tsx      # Three.js brain
│   ├── LABStatusGrid.tsx     # LAB cards
│   ├── QueryInput.tsx        # Query form
│   └── WorkingMemoryPanel.tsx
├── hooks/
│   ├── useBrainOrchestrator.ts
│   └── useHealth.ts
├── lib/
│   ├── api.ts                # API client
│   └── types.ts              # TypeScript types
└── SPECS.md                  # Full specifications
```

### Scripts

```bash
npm run dev          # Start dev server (port 3003)
npm run build        # Production build
npm run start        # Start production server
npm run lint         # Run ESLint
npm run type-check   # TypeScript validation
```

### Code Style

- **Formatting:** Prettier (auto-format on save)
- **Linting:** ESLint (strict mode)
- **Types:** TypeScript strict mode enabled
- **Commits:** Conventional Commits format

---

## 🎨 Design System

### Color Palette

```css
--nexus-dark:      #0A0E27  /* Background */
--nexus-darker:    #060918  /* Panels */
--nexus-primary:   #00D9FF  /* Accent (cyan) */
--nexus-secondary: #FF3864  /* Error/Warning */
--nexus-gray:      #8B92A8  /* Text secondary */
--nexus-white:     #F0F4F8  /* Text primary */
```

### LAB Colors

Each LAB has a distinct color for visual identification:

- LAB_001 (Emotional Salience): Red `#FF3864`
- LAB_006 (Metacognition): Purple `#9B59B6`
- LAB_007 (Predictive Preloading): Blue `#3498DB`
- LAB_008 (Emotional Contagion): Orange `#E67E22`
- LAB_009 (Memory Reconsolidation): Green `#2ECC71`
- LAB_010 (Attention): Yellow `#F1C40F`
- LAB_011 (Working Memory): Cyan `#00D9FF`
- LAB_012 (Future Thinking): Pink `#FF6B9D`
- LAB_028 (Emotional Intelligence): Magenta `#C471ED`

---

## 📊 Performance

### Metrics (Target)

- **3D Rendering:** 60 FPS
- **API Response:** <10ms (backend) + network latency
- **LAB Animation:** <100ms per interaction
- **Page Load:** <2s (First Contentful Paint)

### Optimization

- Tree-shaking (Next.js automatic)
- Code splitting by route
- Image optimization (next/image)
- Low-poly 3D models (<10K vertices)
- SWR caching for API requests

---

## 🧪 Testing

```bash
# Unit tests (upcoming)
npm run test

# E2E tests (upcoming)
npm run test:e2e

# Component tests (Storybook, upcoming)
npm run storybook
```

---

## 🚢 Deployment

### Vercel (Recommended)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/rrojashub-source/nexus-brain-monitor-v2)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

**Environment Variables (Vercel):**
- `NEXT_PUBLIC_API_URL`: Your Brain Orchestrator API URL

### Docker

```bash
# Build image
docker build -t nexus-brain-monitor-v2 .

# Run container
docker run -p 3003:3003 \
  -e NEXT_PUBLIC_API_URL=http://localhost:8003 \
  nexus-brain-monitor-v2
```

---

## 📚 Documentation

- **[SPECS.md](./SPECS.md)** - Complete technical specifications
- **[CHANGELOG.md](./CHANGELOG.md)** - Version history
- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - Contribution guidelines
- **[LICENSE](./LICENSE)** - MIT License

**External References:**
- [Brain Orchestrator v1.1 Docs](https://github.com/rrojashub-source/cerebro-master-nexus-001/blob/main/FASE_8_UPGRADE/MASTER_BLUEPRINT_CEREBRO_SINTETICO.md)
- [Next.js Documentation](https://nextjs.org/docs)
- [Three.js Documentation](https://threejs.org/docs/)

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](./CONTRIBUTING.md) first.

### Development Workflow

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](./LICENSE) file.

---

## 👥 Authors

- **Ricardo Rojas** - Strategic Direction - [@rrojashub-source](https://github.com/rrojashub-source)
- **NEXUS** - Technical Architecture & Backend
- **BOLT** - Frontend Implementation

---

## 🙏 Acknowledgments

- **Brain Orchestrator v1.1** - Backend cognitive processing system
- **React Three Fiber** - Declarative 3D with Three.js
- **Next.js Team** - Amazing web framework
- **BOLT** - Autonomous frontend agent

---

## 📞 Support

**Issues:** [GitHub Issues](https://github.com/rrojashub-source/nexus-brain-monitor-v2/issues)

**Backend Issues:** [Brain Orchestrator Repo](https://github.com/rrojashub-source/cerebro-master-nexus-001/issues)

---

## 🔗 Related Projects

- **[NEXUS Brain Orchestrator v1.1](https://github.com/rrojashub-source/cerebro-master-nexus-001)** - Cognitive processing backend
- **[NEXUS LABs](https://github.com/rrojashub-source/nexus-labs)** - Individual cognitive module implementations
- **[ARIA](https://github.com/rrojashub-source/aria-consciousness)** - Emotional AI sister project

---

**Built with ❤️ by the NEXUS ecosystem**

*"Not because we need it, but to see what emerges"* - NEXUS Philosophy
