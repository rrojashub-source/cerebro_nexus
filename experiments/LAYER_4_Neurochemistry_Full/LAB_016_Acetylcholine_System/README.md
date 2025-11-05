# LAB_016: Acetylcholine System 🎓

**Status:** ✅ Operational (Session 7)
**Code:** ~650 lines (308 main + 324 tests + 12 init)
**Time:** 2 hours (TDD)

## 🧠 Function

**Attention amplification, learning enhancement, encoding strength**

- Novel stimuli → ACh spike
- High ACh → amplified attention
- Encoding/recall mode switching
- Learning readiness gating

## 🎯 Capabilities

1. **ACh Modulation** - Novelty + attention demand spike ACh
2. **Attention Amplification** - High ACh amplifies attention signal
3. **Encoding Modulation** - Strong encoding in encoding mode, weak in recall mode
4. **Learning Readiness** - Plasticity gate controlled by ACh level
5. **Mode Switching** - Encoding vs recall mode

## 📐 Core Algorithm

```python
# ACh update
ach_spike = novelty * novelty_sensitivity + attention_demand * 0.2
ach_level = ach_level + ach_spike + decay_to_baseline

# Attention amplification
amplified_attention = base_attention * (1.0 + ach_level * amplification_gain)

# Encoding modulation
if mode == "encoding":
    encoding_strength = base * (1.0 + ach_level * 0.5)
else:  # recall mode
    encoding_strength = base * 0.3
```

## ✅ Tests

**24/24 PASSED**
- ACh update (3)
- Attention amplification (3)
- Encoding modulation (3)
- Learning readiness (2)
- Mode switching (2)
- ACh stability (2)
- Full processing (3)
- Integration (2)
- Edge cases (2)
- State persistence (2)

## 🔗 API

**POST /acetylcholine/process**
```json
{
  "novelty": 0.8,
  "attention_demand": 0.7,
  "base_attention": 0.5,
  "base_encoding_strength": 0.5
}
```

**GET /acetylcholine/state**

**POST /acetylcholine/mode?mode=encoding** (or recall)

## 🚀 Usage

```python
from LAYER_4_Neurochemistry_Full.LAB_016_Acetylcholine_System import AcetylcholineSystem

ach = AcetylcholineSystem(baseline_ach=0.5, encoding_threshold=0.6)

# Set encoding mode
ach.set_mode("encoding")

# Process novel stimulus
result = ach.process_stimulus(novelty=0.8, attention_demand=0.7)

print(f"ACh: {result['ach_level']}")  # ~0.74
print(f"Amplified Attention: {result['amplified_attention']}")  # ~0.61
print(f"Encoding: {result['encoding']['is_strong_encoding']}")  # True
```

## 📚 Papers

- Hasselmo (2006) - ACh & memory encoding
- Sarter et al. (2009) - Phasic ACh release

---

**Created:** Nov 4, 2025 (Session 7)
**Author:** NEXUS@CLI + Ricardo
**Breakthrough:** 🔥🔥🔥 HIGH (Attention gating & encoding control)
