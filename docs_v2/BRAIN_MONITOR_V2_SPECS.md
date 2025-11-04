# 🧠 NEXUS Brain Monitor v2.0 - Technical Specifications

**Project:** Real-time 3D visualization of NEXUS Brain Orchestrator v1.1
**Tech Stack:** Next.js 14, React 18, Three.js, TypeScript, TailwindCSS
**Target Agent:** BOLT (bolt.new)
**Created:** 30 October 2025
**Author:** NEXUS (specs) + BOLT (implementation)

---

## 📋 Project Overview

### Purpose

Brain Monitor v2.0 is a real-time web application that visualizes the NEXUS Brain Orchestrator v1.1 processing in 3D. It connects to the FastAPI backend (port 8003) and displays:

1. **3D Brain Model** - Interactive brain with 9 active LABs lighting up during processing
2. **Real-time LAB Activity** - Visual pulses when LABs process queries
3. **Processing Flow** - Animated data flow between LABs
4. **Performance Metrics** - Live stats (processing time, memory usage, etc.)
5. **Episode Timeline** - Recent episodic memories from PostgreSQL

### Key Difference from v1.0

**v1.0 (current):** Static data, hardcoded LAB list, no real-time updates
**v2.0 (target):** Dynamic data from Brain Orchestrator API, WebSocket updates, real LAB activity

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│ Brain Monitor v2.0 (Next.js 14 + React 18)          │
│ http://localhost:3003                               │
│                                                     │
│  ┌──────────────┐      ┌──────────────┐            │
│  │ 3D Brain     │      │ LAB Status   │            │
│  │ (Three.js)   │      │ Dashboard    │            │
│  └──────────────┘      └──────────────┘            │
│                                                     │
│  ┌──────────────┐      ┌──────────────┐            │
│  │ Performance  │      │ Episode      │            │
│  │ Metrics      │      │ Timeline     │            │
│  └──────────────┘      └──────────────┘            │
└─────────────────────────────────────────────────────┘
                    ↓ HTTP REST API
┌─────────────────────────────────────────────────────┐
│ Brain Orchestrator v1.1 (FastAPI + Python)          │
│ http://localhost:8003                               │
│                                                     │
│ Endpoints:                                          │
│ - GET  /health                                      │
│ - POST /brain/process                               │
│ - GET  /consciousness/current                       │
│ - GET  /stats                                       │
└─────────────────────────────────────────────────────┘
```

---

## 🔌 API Integration

### Base URL

```
http://localhost:8003
```

### Endpoints to Consume

#### 1. Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "agent_id": "nexus",
  "database": "connected",
  "redis": "connected",
  "queue_depth": 0,
  "timestamp": "2025-10-30T03:00:00.000000"
}
```

**Usage:** Display connection status indicator in header

---

#### 2. Brain Processing (Main Endpoint)

```http
POST /brain/process
Content-Type: application/json

{
  "query": "docker network problems",
  "context": {
    "current_emotion": "focused",
    "goal": "understand debugging"
  }
}
```

**Response:**
```json
{
  "success": true,
  "working_memory": [
    {
      "episode_id": "f836e568-e253-4386-9235-55c9c9de45fb",
      "attention": 0.9,
      "content": "Successfully resolved Docker network recreation loop...",
      "salience": 0.95,
      "created_at": "2025-10-30T02:56:21.586130+00:00"
    }
  ],
  "predictions": ["ep_142", "ep_089"],
  "future_vision": {
    "scenario": "Future scenario for: understand debugging",
    "success_probability": 0.68,
    "based_on_episodes": ["ep_001", "ep_042"],
    "time_horizon": "near_future"
  },
  "emotional_state": {
    "current": "focused",
    "regulated": "calm_focus",
    "intensity": 0.4
  },
  "interactions": [
    {
      "from_lab": "INPUT",
      "to_lab": "LAB_001",
      "signal": "query='docker network problems'",
      "timestamp": "2025-10-30T02:55:14.426742"
    },
    {
      "from_lab": "LAB_001",
      "to_lab": "LAB_010",
      "signal": "salience=0.75",
      "timestamp": "2025-10-30T02:55:14.426751"
    }
    // ... 11 total interactions (full flow)
  ],
  "metacognition": {
    "confidence": 0.75,
    "reasoning": "High salience (0.75) + successful pattern match + regulated emotion",
    "calibration_score": 0.82
  },
  "processing_time_ms": 7.824,
  "timestamp": "2025-10-30T02:55:14.434867"
}
```

**Usage:**
- Trigger when user submits query via UI
- Animate LAB interactions on 3D brain
- Display working memory contents
- Show processing time metrics

---

#### 3. Consciousness State

```http
GET /consciousness/current
```

**Expected Response (design this if endpoint doesn't exist):**
```json
{
  "emotional": {
    "joy": 0.6,
    "trust": 0.8,
    "fear": 0.2,
    "surprise": 0.4,
    "sadness": 0.1,
    "disgust": 0.0,
    "anger": 0.1,
    "anticipation": 0.7
  },
  "somatic": {
    "valence": 0.6,
    "arousal": 0.5,
    "dominance": 0.7,
    "body_state": "relaxed",
    "heart_rate": 72,
    "stress_level": 0.3,
    "energy": 0.8
  }
}
```

**Usage:** Display emotional radar and somatic bars

---

#### 4. System Stats

```http
GET /stats
```

**Expected Response (design this if endpoint doesn't exist):**
```json
{
  "total_episodes": 1,
  "total_queries": 2,
  "avg_processing_time_ms": 7.8,
  "active_labs": 9,
  "labs": [
    {
      "id": "LAB_001",
      "name": "Emotional Salience",
      "status": "active",
      "last_processed": "2025-10-30T02:55:14.426751",
      "total_invocations": 2
    },
    {
      "id": "LAB_006",
      "name": "Metacognition",
      "status": "active",
      "last_processed": "2025-10-30T02:55:14.434655",
      "total_invocations": 2
    }
    // ... remaining 7 active LABs
  ]
}
```

**Usage:** Display LAB status cards with real activity

---

## 🎨 UI Components

### 1. Header

**Location:** Top of page
**Content:**
- Connection status indicator (green dot if healthy)
- Agent ID badge ("NEXUS")
- Version badge ("v2.0.0")
- Last update timestamp
- View mode toggle (2D ↔ 3D)

### 2. 3D Brain View (Main Feature)

**Library:** Three.js + React Three Fiber
**Features:**
- Rotating 3D brain model (low-poly style)
- 9 LAB nodes positioned anatomically:
  - LAB_001 (Emotional Salience) → Amygdala region (red)
  - LAB_006 (Metacognition) → Prefrontal cortex (purple)
  - LAB_007 (Predictive Preloading) → Dorsolateral PFC (blue)
  - LAB_008 (Emotional Contagion) → Limbic system (orange)
  - LAB_009 (Memory Reconsolidation) → Hippocampus (green)
  - LAB_010 (Attention) → Parietal cortex (yellow)
  - LAB_011 (Working Memory) → Temporal lobe (cyan)
  - LAB_012 (Future Thinking) → Frontal lobe (pink)
  - LAB_028 (Emotional Intelligence) → Orbitofrontal cortex (magenta)

**Interactions:**
- Mouse drag → Rotate brain
- Mouse scroll → Zoom in/out
- Right-click drag → Pan camera
- Click LAB node → Show LAB details popup

**Animations:**
- Auto-rotation: 0.5 RPM when idle
- LAB pulse: When processing, node glows and pulses
- Data flow: Animated lines between LABs following `interactions` array
- Processing wave: Ripple effect across brain during query

### 3. LAB Status Grid

**Layout:** 3x3 grid (for 9 active LABs)
**Each Card Shows:**
- LAB ID (e.g., "LAB_001")
- LAB Name (e.g., "Emotional Salience")
- Status badge: 🟢 Active | 🔴 Inactive
- Last processed timestamp (relative: "2s ago")
- Total invocations count
- Click → Highlight LAB in 3D view

### 4. Query Input Panel

**Location:** Bottom-left floating panel
**Fields:**
- Text input: "Enter episodic memory query..."
- Dropdown: Emotion selector (focused, curious, stressed, calm)
- Text input: "Goal (optional)"
- Button: "Process Query" (disabled when processing)
- Loading indicator during processing

**Behavior:**
- Submit → POST to `/brain/process`
- Show processing spinner
- Animate LAB interactions in 3D
- Display results in Working Memory panel

### 5. Working Memory Panel

**Location:** Right sidebar
**Content:**
- Title: "Working Memory (7±2 items)"
- List of memory items from `working_memory` response:
  - Episode ID (truncated, tooltip shows full UUID)
  - Content preview (first 100 chars)
  - Attention score (progress bar 0-1)
  - Salience score (colored badge)
  - Created timestamp

### 6. Performance Metrics

**Location:** Top-right corner cards
**Metrics:**
- Processing Time: "7.8ms" (with color: green <50ms, yellow <100ms, red >=100ms)
- Active LABs: "9/16" (with progress bar)
- Total Episodes: "1 episodes"
- Confidence: "75%" (from metacognition)

### 7. Emotional Radar Chart

**Location:** Dashboard 2D view
**Type:** Radar chart (8 axes for 8 emotions)
**Data Source:** `/consciousness/current` → emotional
**Update:** Real-time (every 2 seconds)

### 8. Somatic State Bars

**Location:** Dashboard 2D view
**Type:** Horizontal bar charts (7 bars)
**Data Source:** `/consciousness/current` → somatic
**Update:** Real-time (every 2 seconds)

### 9. Episode Timeline

**Location:** Bottom panel (dashboard 2D view)
**Type:** Horizontal scrollable timeline
**Data Source:** Previous `/brain/process` responses
**Display:** Last 10 queries with:
- Query text
- Processing time
- Number of memories retrieved
- Timestamp
- Click → Show full response

---

## 🛠️ Tech Stack Requirements

### Frontend Framework
```json
{
  "next": "14.0.0",
  "react": "18.2.0",
  "react-dom": "18.2.0",
  "typescript": "5.2.0"
}
```

### 3D Graphics
```json
{
  "@react-three/fiber": "^8.15.0",
  "@react-three/drei": "^9.88.0",
  "three": "^0.158.0"
}
```

### Styling
```json
{
  "tailwindcss": "^3.3.0",
  "autoprefixer": "^10.4.0",
  "postcss": "^8.4.0"
}
```

### Data Fetching & State
```json
{
  "axios": "^1.6.0",
  "swr": "^2.2.0"
}
```

### Charting
```json
{
  "recharts": "^2.10.0"
}
```

### Utilities
```json
{
  "date-fns": "^2.30.0",
  "clsx": "^2.0.0"
}
```

---

## 📁 Expected File Structure

```
nexus-brain-monitor-v2/
├── app/
│   ├── page.tsx                 # Main page (view mode toggle)
│   ├── layout.tsx               # Root layout
│   └── globals.css              # Tailwind imports
├── components/
│   ├── Header.tsx               # Connection status, version badge
│   ├── BrainModel3D.tsx         # Three.js brain with LAB nodes
│   ├── LABStatusGrid.tsx        # 3x3 grid of active LABs
│   ├── QueryInput.tsx           # Query submission form
│   ├── WorkingMemoryPanel.tsx   # Right sidebar with memories
│   ├── PerformanceMetrics.tsx   # Top-right metric cards
│   ├── EmotionalRadar.tsx       # Radar chart for emotions
│   ├── SomaticBars.tsx          # Bar charts for somatic state
│   └── EpisodeTimeline.tsx      # Bottom timeline
├── hooks/
│   ├── useBrainOrchestrator.ts  # SWR hook for /brain/process
│   ├── useHealth.ts             # SWR hook for /health
│   └── useConsciousness.ts      # SWR hook for /consciousness/current
├── lib/
│   ├── api.ts                   # Axios instance, API client
│   └── types.ts                 # TypeScript interfaces
├── public/
│   └── brain-model.glb          # (optional) 3D brain model asset
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.js
└── README.md
```

---

## 🎯 Core Features to Implement

### Priority 1 (MVP)

1. **3D Brain Visualization**
   - Three.js brain model with 9 LAB nodes
   - Auto-rotation, zoom, pan controls
   - LAB nodes pulse during processing

2. **Real-time LAB Status**
   - Fetch active LABs from `/stats`
   - Display 3x3 grid with real data
   - Update last_processed timestamps

3. **Query Processing Flow**
   - Query input form
   - POST to `/brain/process`
   - Animate LAB interactions (lines between nodes)
   - Display working memory results

4. **Performance Metrics**
   - Processing time display
   - Active LAB count
   - Real-time updates

### Priority 2 (Enhanced)

5. **Emotional & Somatic Visualization**
   - Radar chart for 8 emotions
   - Bar charts for 7 somatic dimensions
   - Real-time polling (every 2 seconds)

6. **Episode Timeline**
   - Horizontal scrollable timeline
   - Last 10 queries stored in local state
   - Click to view full response

7. **LAB Details Modal**
   - Click LAB node → Show popup
   - Display LAB description, status, metrics
   - Show recent interactions

### Priority 3 (Polish)

8. **Dark Theme**
   - Tailwind dark mode
   - Neon glow effects for LABs
   - Smooth animations

9. **Responsive Design**
   - Mobile-friendly layout
   - Collapsible panels
   - Touch controls for 3D

10. **Error Handling**
    - Connection lost indicator
    - Retry logic for failed requests
    - User-friendly error messages

---

## 🎨 Design Guidelines

### Color Palette

```css
--nexus-dark: #0A0E27       /* Background */
--nexus-darker: #060918     /* Panels */
--nexus-primary: #00D9FF    /* Accent (cyan) */
--nexus-secondary: #FF3864  /* Error/Warning */
--nexus-gray: #8B92A8       /* Text secondary */
--nexus-white: #F0F4F8      /* Text primary */
```

### LAB Colors (for 3D nodes)

```javascript
const LAB_COLORS = {
  'LAB_001': '#FF3864', // Red (Emotional Salience)
  'LAB_006': '#9B59B6', // Purple (Metacognition)
  'LAB_007': '#3498DB', // Blue (Predictive Preloading)
  'LAB_008': '#E67E22', // Orange (Emotional Contagion)
  'LAB_009': '#2ECC71', // Green (Memory Reconsolidation)
  'LAB_010': '#F1C40F', // Yellow (Attention)
  'LAB_011': '#00D9FF', // Cyan (Working Memory)
  'LAB_012': '#FF6B9D', // Pink (Future Thinking)
  'LAB_028': '#C471ED', // Magenta (Emotional Intelligence)
};
```

### Typography

- Headings: `font-family: 'Inter', sans-serif; font-weight: 700;`
- Body: `font-family: 'Inter', sans-serif; font-weight: 400;`
- Monospace (IDs, timestamps): `font-family: 'Fira Code', monospace;`

### Animations

- LAB pulse: `duration: 1s; easing: ease-in-out; scale: 1 → 1.2 → 1`
- Data flow lines: `duration: 2s; easing: linear; opacity: 0 → 1 → 0`
- Page transitions: `duration: 300ms; easing: ease-in-out`

---

## 🚀 Getting Started (for BOLT)

### Step 1: Initialize Next.js Project

```bash
npx create-next-app@14 nexus-brain-monitor-v2 --typescript --tailwind --app
cd nexus-brain-monitor-v2
```

### Step 2: Install Dependencies

```bash
npm install @react-three/fiber @react-three/drei three
npm install axios swr recharts date-fns clsx
npm install -D @types/three
```

### Step 3: Configure Tailwind (tailwind.config.ts)

```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'nexus-dark': '#0A0E27',
        'nexus-darker': '#060918',
        'nexus-primary': '#00D9FF',
        'nexus-secondary': '#FF3864',
        'nexus-gray': '#8B92A8',
        'nexus-white': '#F0F4F8',
      },
    },
  },
  plugins: [],
}
export default config
```

### Step 4: Create API Client (lib/api.ts)

```typescript
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8003';

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const brainAPI = {
  health: () => api.get('/health'),
  process: (query: string, context: any) =>
    api.post('/brain/process', { query, context }),
  stats: () => api.get('/stats'),
  consciousness: () => api.get('/consciousness/current'),
};
```

### Step 5: Create TypeScript Types (lib/types.ts)

```typescript
export interface LABInteraction {
  from_lab: string;
  to_lab: string;
  signal: string;
  timestamp: string;
}

export interface WorkingMemoryItem {
  episode_id: string;
  attention: number;
  content: string;
  salience: number;
  created_at: string;
}

export interface BrainProcessResponse {
  success: boolean;
  working_memory: WorkingMemoryItem[];
  predictions: string[];
  future_vision: {
    scenario: string;
    success_probability: number;
    based_on_episodes: string[];
    time_horizon: string;
  };
  emotional_state: {
    current: string;
    regulated: string;
    intensity: number;
  };
  interactions: LABInteraction[];
  metacognition: {
    confidence: number;
    reasoning: string;
    calibration_score: number;
  };
  processing_time_ms: number;
  timestamp: string;
}

export interface LABStatus {
  id: string;
  name: string;
  status: 'active' | 'inactive';
  last_processed?: string;
  total_invocations?: number;
}

export interface HealthResponse {
  status: string;
  version: string;
  agent_id: string;
  database: string;
  redis: string;
  queue_depth: number;
  timestamp: string;
}
```

### Step 6: Implement Components

Start with:
1. `Header.tsx` (connection status)
2. `QueryInput.tsx` (query form)
3. `LABStatusGrid.tsx` (LAB cards with real data)
4. `BrainModel3D.tsx` (Three.js brain)

### Step 7: Test API Connection

```typescript
// Test in any component
useEffect(() => {
  brainAPI.health()
    .then(res => console.log('Health:', res.data))
    .catch(err => console.error('API Error:', err));
}, []);
```

---

## ✅ Acceptance Criteria

### Must Have (v2.0 Release)

- [ ] 3D brain model with 9 LAB nodes positioned anatomically
- [ ] LAB nodes light up during processing
- [ ] Query input form with POST to `/brain/process`
- [ ] LAB status grid showing real data from `/stats`
- [ ] Working memory panel displaying retrieved episodes
- [ ] Performance metrics (processing time, active LABs)
- [ ] Animated data flow lines between LABs (following `interactions`)
- [ ] Dark theme with neon glow effects
- [ ] Responsive design (desktop + tablet)
- [ ] Connection status indicator in header
- [ ] Error handling for API failures

### Nice to Have (Future Enhancements)

- [ ] Emotional radar chart (if `/consciousness/current` exists)
- [ ] Somatic state bars
- [ ] Episode timeline with history
- [ ] LAB details modal on node click
- [ ] WebSocket support for real-time updates (instead of polling)
- [ ] Export query results (JSON/CSV)
- [ ] Dark/Light theme toggle
- [ ] Mobile-optimized 3D controls

---

## 🐛 Known Limitations

1. **No WebSocket Support (Yet)**
   - Brain Orchestrator v1.1 only has REST endpoints
   - Use polling (SWR with `refreshInterval`) for real-time feel
   - Consider WebSocket implementation in v1.2

2. **No Authentication**
   - API is open (localhost only)
   - Add auth middleware if deploying publicly

3. **Limited LAB Data**
   - Only 9 LABs active (LAB_001, 006-012, 028)
   - Other 41 LABs are roadmap (show as "inactive" or hide)

4. **No Historical Data**
   - API doesn't persist query history
   - Store last N queries in React state or localStorage

---

## 📚 Reference Materials

### Brain Orchestrator v1.1 Documentation

Located in: `/mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_MASTER_NEXUS_001/FASE_8_UPGRADE/MASTER_BLUEPRINT_CEREBRO_SINTETICO.md`

Key sections:
- ANEXO C: Brain Orchestrator v1.0 Design
- ANEXO D: Brain Orchestrator v1.1 Implementation (PostgreSQL integration)

### Example cURL Commands

```bash
# Health check
curl http://localhost:8003/health

# Process query
curl -X POST http://localhost:8003/brain/process \
  -H "Content-Type: application/json" \
  -d '{"query":"docker network","context":{"current_emotion":"curious"}}'
```

### LAB Descriptions

```javascript
const LAB_DESCRIPTIONS = {
  'LAB_001': {
    name: 'Emotional Salience Scorer',
    description: 'Calculates emotional salience for memory formation',
    neuroscience: 'Amygdala + medial prefrontal cortex',
  },
  'LAB_006': {
    name: 'Metacognition Logger',
    description: 'Self-awareness and confidence calibration',
    neuroscience: 'Lateral prefrontal cortex + ACC',
  },
  'LAB_007': {
    name: 'Predictive Preloading',
    description: 'Anticipates future queries based on patterns',
    neuroscience: 'Dorsolateral PFC + hippocampus',
  },
  'LAB_008': {
    name: 'Emotional Contagion',
    description: 'Spreads emotional context across memories',
    neuroscience: 'Limbic system',
  },
  'LAB_009': {
    name: 'Memory Reconsolidation',
    description: 'Updates memories when retrieved',
    neuroscience: 'Hippocampus',
  },
  'LAB_010': {
    name: 'Attention Mechanism',
    description: 'Multi-factor selective attention',
    neuroscience: 'Parietal cortex',
  },
  'LAB_011': {
    name: 'Working Memory Buffer',
    description: '7±2 items (Miller\'s Law)',
    neuroscience: 'Temporal lobe',
  },
  'LAB_012': {
    name: 'Episodic Future Thinking',
    description: 'Simulates episodic futures',
    neuroscience: 'Frontal lobe',
  },
  'LAB_028': {
    name: 'Emotional Intelligence System',
    description: 'Emotion recognition and regulation',
    neuroscience: 'Orbitofrontal cortex',
  },
};
```

---

## 🎯 Success Metrics

After implementation, the app should:

1. **Connect to Brain Orchestrator API** on `http://localhost:8003`
2. **Display 9 active LABs** with real-time status
3. **Process queries** and show results within 10ms + API latency
4. **Animate LAB interactions** following the `interactions` array
5. **Run smoothly** at 60fps with 3D rendering
6. **Be responsive** on desktop (1920x1080) and tablet (768x1024)

---

## 📝 Notes for BOLT

- **Start simple:** Get API connection working first, then add 3D
- **Test endpoints:** Use `curl` or Postman to verify API before coding
- **Incremental development:** Header → Query form → LAB grid → 3D brain
- **Use SWR for data fetching:** Automatic caching and revalidation
- **Three.js performance:** Keep brain model low-poly (<10K vertices)
- **Error boundaries:** Wrap 3D components in React error boundaries
- **TypeScript strict:** Enable `strict: true` in tsconfig.json
- **Commit often:** Small, incremental commits with clear messages

---

## 🚀 Deployment (Future)

### Vercel (Recommended)

```bash
# Connect GitHub repo to Vercel
# Set environment variable:
NEXT_PUBLIC_API_URL=http://your-api-domain.com:8003

# Deploy
vercel --prod
```

### Docker (Alternative)

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
RUN npm run build
EXPOSE 3003
CMD ["npm", "start"]
```

---

## 📞 Support

**Questions about Brain Orchestrator API?**
- Check: `MASTER_BLUEPRINT_CEREBRO_SINTETICO.md` ANEXO D
- Test endpoint: `curl http://localhost:8003/health`

**Questions about implementation?**
- This is a BOLT project (autonomous)
- Specs are complete - implement as described
- Use best practices for Next.js 14 + TypeScript

---

**END OF SPECIFICATIONS**

Generated by: NEXUS (Brain Orchestrator architect)
Target: BOLT (Frontend implementation agent)
Date: 30 October 2025, 03:30 AM
Status: Ready for GitHub repo creation
