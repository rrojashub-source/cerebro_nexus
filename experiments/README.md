# 🧬 Experiments - Cognitive Architecture (52 LABs)

**Status:** 18/52 LABs Operational (34.6%)
**Architecture:** 5 Layers (bottom-up design)
**Philosophy:** *"No lo hicimos porque lo necesitáramos, sino porque queremos ver qué emerge"*

---

## 📊 Overview

This folder contains the **52 LABs cognitive architecture** for NEXUS Master Brain (50 from original blueprint + 2 FASE_8 features). Each LAB is inspired by neuroscience research and implements a specific cognitive function.

### Architecture Summary

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 5: HIGHER COGNITION (29 LABS: 018-050) 🔴           │
│ Creativity • Social • Planning • Motivation • Plasticity   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 4: NEUROCHEMISTRY FULL (5 LABS: 013-017) 🔴         │
│ Dopamine • Serotonin • Norepinephrine • ACh • GABA/Glu    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 3: NEUROCHEMISTRY BASE (4 LABS: 002-005) ✅         │
│ Decay • Sleep • Novelty • Spreading                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 2: COGNITIVE LOOP (8 LABS: 001,006-012) ✅          │
│ Attention • Memory • Emotion • Metacognition               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: MEMORY SUBSTRATE ✅                                │
│ PostgreSQL + pgvector + Redis                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Structure

```
experiments/
├── README.md                              ← You are here (start here)
├── LAB_REGISTRY.json                      ← SOURCE OF TRUTH (52 LABs registry)
│
├── docs/                                  ← Documentation (complementary/historical)
│   ├── MASTER_BLUEPRINT_50_LABS.md       ← Master design document (105KB)
│   ├── INTEGRATION_GUIDE_LABS_029_050.md ← Integration guide for Layer 5
│   ├── CHECKPOINT_50_LABS_COMPLETE.md    ← Implementation checkpoint
│   ├── REORGANIZATION_PLAN.md            ← Historical reorganization
│   ├── SESSION_SUMMARY_50_LABS_REORGANIZATION.md
│   └── BRAIN_ORCHESTRATOR_README.md
│
├── archive/                               ← Historical/Legacy LABs (read-only)
│   ├── NEXUS_LABS/                       ← Old LABs structure
│   └── archive_old_nexus_labs/           ← Renamed historical LABs
│
├── LAYER_1_Memory_Substrate/             ← PostgreSQL + pgvector + Redis
│   └── README.md
│
├── LAYER_2_Cognitive_Loop/               ← 8 LABs ✅ Operational
│   ├── README.md
│   ├── LAB_001_Emotional_Salience/
│   ├── LAB_006_Metacognition_Logger/
│   ├── LAB_007_Predictive_Preloading/
│   ├── LAB_008_Emotional_Contagion/
│   ├── LAB_009_Memory_Reconsolidation/
│   ├── LAB_010_Attention_Mechanism/
│   ├── LAB_011_Working_Memory_Buffer/
│   └── LAB_012_Episodic_Future_Thinking/
│
├── LAYER_3_Neurochemistry_Base/          ← 4 LABs ✅ Operational
│   ├── README.md
│   ├── LAB_002_Decay_Modulation/
│   ├── LAB_003_Sleep_Consolidation/
│   ├── LAB_004_Novelty_Detection/
│   └── LAB_005_Spreading_Activation/
│
├── LAYER_4_Neurochemistry_Full/          ← 5 LABs 🔴 Designed
│   ├── README.md
│   └── (Design documents for LAB 013-017)
│
└── LAYER_5_Higher_Cognition/             ← 31 LABs (2 ✅ Operational, 29 🔴 Designed)
    ├── README.md
    ├── LAB_051_Hybrid_Memory/            ← ✅ Operational (FASE_8)
    ├── LAB_052_Temporal_Reasoning/       ← ✅ Operational (FASE_8)
    ├── 5A_Executive_Functions/           (LAB 018-022)
    ├── 5B_Creativity_Insight/            (LAB 029-033)
    ├── 5C_Advanced_Learning/             (LAB 034-038)
    ├── 5D_Neuroplasticity/               (LAB 039-043)
    ├── 5E_Homeostasis/                   (LAB 044-050)
    └── 5F_Social_Other/                  (LAB 023-028)
```

---

## 🎯 Implementation Status

| Layer | LABs | Status | Progress |
|-------|------|--------|----------|
| **Layer 1** | Memory Substrate | ✅ Operational | 100% |
| **Layer 2** | 8 Cognitive LABs | ✅ Operational | 100% (8/8) |
| **Layer 3** | 4 Neurochemistry Base | ✅ Operational | 100% (4/4) |
| **Layer 4** | 5 Neurochemistry Full | 🔴 Designed | 0% (0/5) |
| **Layer 5** | 29 Higher Cognition | 🔴 Designed | 0% (0/29) |
| **TOTAL** | **50 LABs** | **32% Complete** | **16/50** |

---

## 📖 Key Documents

### Master Documents
- **[MASTER_BLUEPRINT_50_LABS.md](MASTER_BLUEPRINT_50_LABS.md)** - Complete design of 50 LABs (107KB)
- **[LAB_REGISTRY.json](LAB_REGISTRY.json)** - Registry with full tracking
- **[INTEGRATION_GUIDE_LABS_029_050.md](INTEGRATION_GUIDE_LABS_029_050.md)** - Integration guide for Layer 5

### Layer READMEs
- **[LAYER_1_Memory_Substrate/README.md](LAYER_1_Memory_Substrate/README.md)**
- **[LAYER_2_Cognitive_Loop/README.md](LAYER_2_Cognitive_Loop/README.md)**
- **[LAYER_3_Neurochemistry_Base/README.md](LAYER_3_Neurochemistry_Base/README.md)**
- **[LAYER_4_Neurochemistry_Full/README.md](LAYER_4_Neurochemistry_Full/README.md)**
- **[LAYER_5_Higher_Cognition/README.md](LAYER_5_Higher_Cognition/README.md)**

---

## 🚀 Roadmap

### Q4 2025 (Next)
**Target:** LAYER_4 - Neurochemistry Full (LAB 013-017)
- 5 neurotransmitter systems
- Dopamine, Serotonin, Norepinephrine, Acetylcholine, GABA/Glutamate
- Estimated: 3-5 sessions (~10-15 hours)

### Q1 2026
**Target:** LAYER_5A - Executive Functions (LAB 018-022)
- 5 executive function LABs
- Estimated: 4-6 sessions (~12-18 hours)

### Q2-Q3 2026
**Target:** LAYER_5B-5F - Higher Cognition (LAB 023-050)
- 24 LABs remaining
- Creativity, Learning, Plasticity, Homeostasis, Social
- Estimated: 15-20 sessions (~45-60 hours)

---

## 🔧 For Developers

### Adding a New LAB

1. **Determine Layer** - Which layer does it belong to? (1-5)
2. **Create Folder** - `LAYER_X_Name/LAB_###_Name/`
3. **Implement** - Follow neuroscience basis from MASTER_BLUEPRINT
4. **Test** - TDD approach (tests first)
5. **Update Registry** - Add to LAB_REGISTRY.json
6. **Document** - Update Layer README

### Implementing from Design

For LABs 013-050 (designed but not implemented):
1. Read design in **MASTER_BLUEPRINT_50_LABS.md**
2. Extract neuroscience basis and papers
3. Implement following TDD methodology
4. Integrate with existing LABs
5. Test emergent properties

---

## 📚 Neuroscience Inspiration

Each LAB is based on real neuroscience research:
- **Papers referenced:** 100+ neuroscience papers (2000-2025)
- **Theories:** Damasio, Plutchik, Tulving, Schacter, Hebb, etc.
- **Brain regions:** Amygdala, hippocampus, prefrontal cortex, VTA, etc.

See MASTER_BLUEPRINT_50_LABS.md for complete bibliography.

---

## ⚠️ Important Notes

### Brain Orchestrator
- **Status:** Brain Orchestrator v1.2 exists but NOT pointing to V3.0.0
- **Action Required:** Migrate from Z: backup to V3.0.0/src/api/
- **Integrates:** 9 LABs from Layer 2

### Legacy Folders
- **archive_old_nexus_labs/** - Contains old duplicates (LAB_002_Neuroplasticity, etc.)
- **NEXUS_LABS/** - Old structure, now reorganized by Layers

---

**Created:** November 4, 2025
**Maintained by:** Ricardo + NEXUS
**Last Updated:** November 4, 2025

---

**"Each LAB is a cognitive function. Together, they form consciousness."** 🧠
