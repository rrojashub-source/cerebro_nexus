# 🔧 Plan de Reorganización - experiments/

**Fecha:** 4 Noviembre 2025
**Objetivo:** Organizar 50 LABs por Layers de manera clara y lógica

---

## 📊 ESTRUCTURA ACTUAL (Caótica)

```
experiments/
└── NEXUS_LABS/                # 15 carpetas mezcladas
    ├── LAB_001_Emotional_Salience/
    ├── LAB_002_Decay_Modulation/
    ├── LAB_002_Neuroplasticity/      ← DUPLICADO
    ├── LAB_003_Dream_Consolidation/  ← ANTIGUO
    ├── LAB_003_Sleep_Consolidation/
    ├── LAB_004_Curiosity_Driven_Memory/
    ├── LAB_004_Hippocampus_Buffer/   ← ANTIGUO
    ├── LAB_005_MultiModal_Memory/
    ├── LAB_006_Metacognition_Logger/
    ├── LAB_007_Predictive_Preloading/
    ├── LAB_008_Emotional_Contagion/
    ├── LAB_009_Memory_Reconsolidation/
    ├── LAB_010_Attention_Mechanism/
    ├── LAB_011_Working_Memory_Buffer/
    └── LAB_012_Episodic_Future_Thinking/

archive/old_structure_docs/FASE_8_UPGRADE/
└── MASTER_BLUEPRINT_CEREBRO_SINTETICO.md  ← DOCUMENTO CRÍTICO (107KB)
└── INTEGRATION_GUIDE_LABS_029_050.md
└── CHECKPOINT_50_LABS_COMPLETE.md
└── Varios planes de integración
```

**Problemas:**
- ❌ LABs mezclados sin organización por layers
- ❌ Duplicados (LAB_002, LAB_004)
- ❌ Nombres antiguos (Dream_Consolidation, Hippocampus_Buffer)
- ❌ MASTER_BLUEPRINT escondido en archive/
- ❌ No hay README explicando sistema
- ❌ No hay LAB_REGISTRY.json

---

## 🎯 ESTRUCTURA PROPUESTA (Por Layers)

```
experiments/
├── README.md                              # NEW - Overview sistema 50 LABs
├── MASTER_BLUEPRINT_50_LABS.md           # MOVED from archive/
├── LAB_REGISTRY.json                      # NEW - Tracking 16/50
├── ROADMAP_50_LABS.md                     # NEW - Visual roadmap
│
├── LAYER_1_Memory_Substrate/             # NEW folder
│   └── README.md                          # Explain PostgreSQL + pgvector + Redis
│
├── LAYER_2_Cognitive_Loop/               # RENAMED from NEXUS_LABS/
│   ├── README.md                          # NEW - Explain 12 LABs cognitive
│   ├── LAB_001_Emotional_Salience/       ✅ Keep
│   ├── LAB_006_Metacognition_Logger/     ✅ Keep
│   ├── LAB_007_Predictive_Preloading/    ✅ Keep
│   ├── LAB_008_Emotional_Contagion/      ✅ Keep
│   ├── LAB_009_Memory_Reconsolidation/   ✅ Keep
│   ├── LAB_010_Attention_Mechanism/      ✅ Keep
│   ├── LAB_011_Working_Memory_Buffer/    ✅ Keep
│   └── LAB_012_Episodic_Future_Thinking/ ✅ Keep
│
├── LAYER_3_Neurochemistry_Base/          # NEW folder
│   ├── README.md                          # NEW - Explain 4 LABs neurochemistry
│   ├── LAB_002_Decay_Modulation/         ✅ Move here
│   ├── LAB_003_Sleep_Consolidation/      ✅ Move here
│   ├── LAB_004_Novelty_Detection/        ✅ Move here (rename from Curiosity)
│   └── LAB_005_Spreading_Activation/     ✅ Move here (rename from MultiModal)
│
├── LAYER_4_Neurochemistry_Full/          # NEW folder
│   ├── README.md                          # NEW - Explain 5 neurotransmitters
│   ├── DESIGN_LAB_013_Dopamine.md        # EXTRACT from MASTER_BLUEPRINT
│   ├── DESIGN_LAB_014_Serotonin.md       # EXTRACT from MASTER_BLUEPRINT
│   ├── DESIGN_LAB_015_Norepinephrine.md  # EXTRACT from MASTER_BLUEPRINT
│   ├── DESIGN_LAB_016_Acetylcholine.md   # EXTRACT from MASTER_BLUEPRINT
│   └── DESIGN_LAB_017_GABA_Glutamate.md  # EXTRACT from MASTER_BLUEPRINT
│
├── LAYER_5_Higher_Cognition/             # NEW folder
│   ├── README.md                          # NEW - Explain 29 LABs higher cognition
│   ├── 5A_Executive_Functions/           # LAB 018-022 (5 LABs)
│   │   ├── README.md
│   │   └── DESIGN_LAB_018_022.md         # EXTRACT from MASTER_BLUEPRINT
│   ├── 5B_Creativity_Insight/            # LAB 029-033 (5 LABs)
│   │   ├── README.md
│   │   └── DESIGN_LAB_029_033.md         # EXTRACT + INTEGRATION_GUIDE
│   ├── 5C_Advanced_Learning/             # LAB 034-038 (5 LABs)
│   │   ├── README.md
│   │   └── DESIGN_LAB_034_038.md         # EXTRACT + INTEGRATION_GUIDE
│   ├── 5D_Neuroplasticity/               # LAB 039-043 (5 LABs)
│   │   ├── README.md
│   │   └── DESIGN_LAB_039_043.md         # EXTRACT + INTEGRATION_GUIDE
│   ├── 5E_Homeostasis/                   # LAB 044-050 (7 LABs)
│   │   ├── README.md
│   │   └── DESIGN_LAB_044_050.md         # EXTRACT + INTEGRATION_GUIDE
│   └── 5F_Social_Other/                  # LAB 023-028 (6 LABs)
│       ├── README.md
│       └── DESIGN_LAB_023_028.md         # EXTRACT from MASTER_BLUEPRINT
│
└── archive_old_nexus_labs/               # MOVED - old duplicates
    ├── LAB_002_Neuroplasticity/          # OLD duplicate
    ├── LAB_003_Dream_Consolidation/      # OLD version
    └── LAB_004_Hippocampus_Buffer/       # OLD version
```

---

## ✅ BENEFITS

**Claridad:**
- ✅ Cada Layer tiene su carpeta
- ✅ LABs implementados vs diseñados claramente separados
- ✅ README en cada Layer explica propósito

**Navegabilidad:**
- ✅ Estructura refleja arquitectura real (5 layers)
- ✅ Fácil ver progreso por layer
- ✅ Duplicados movidos a archive_old/

**Documentación:**
- ✅ MASTER_BLUEPRINT visible en experiments/
- ✅ LAB_REGISTRY.json tracking 16/50
- ✅ ROADMAP visual del progreso

**Mantenibilidad:**
- ✅ Agregar nuevo LAB = colocar en layer correspondiente
- ✅ Diseño LABs futuros ya tiene carpeta (LAYER_4, LAYER_5)
- ✅ Zero ambigüedad de ubicaciones

---

## 📋 EXECUTION PLAN

**STEP 1:** Create new Layer folders structure
**STEP 2:** Move MASTER_BLUEPRINT from archive/ to experiments/
**STEP 3:** Move LABs from NEXUS_LABS/ to Layer folders
**STEP 4:** Create LAB_REGISTRY.json
**STEP 5:** Create README.md files (7 total)
**STEP 6:** Move old duplicates to archive_old/
**STEP 7:** Update 5 essential documents
**STEP 8:** Validate structure

---

**Status:** Ready to execute
**Next:** STEP 1 - Create Layer folders
