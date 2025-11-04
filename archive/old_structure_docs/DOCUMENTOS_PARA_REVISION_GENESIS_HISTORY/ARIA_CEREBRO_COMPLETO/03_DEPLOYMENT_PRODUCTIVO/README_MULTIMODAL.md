# 🎬 ARIA Multi-Modal Memory System

**Revolucionaria arquitectura que permite a ARIA "ver", "escuchar" y "recordar" contenido multimedia.**

## 🚀 Capacidades

### 🖼️ Visual Memory (Image Processing)
- **CLIP embeddings** para comprensión semántica de imágenes
- **Metadata extraction** automático (EXIF, resolución, formato)
- **Visual similarity search** - encuentra imágenes similares
- **Context-aware processing** - relaciona imágenes con texto

### 🎵 Auditory Memory (Audio Processing)
- **Whisper transcription** - convierte audio a texto
- **Audio fingerprinting** - embeddings únicos para cada audio
- **Speaker identification** - soporte para múltiples voces
- **Audio similarity search** - encuentra sonidos similares

### 🎥 Temporal Memory (Video Processing)
- **Keyframe extraction** - extrae frames importantes automáticamente
- **Audio track processing** - separa y procesa audio del video
- **Temporal embeddings** - entiende secuencias y patrones temporales
- **Motion analysis** - detecta cambios entre frames

### 🧠 Unified Multi-Modal
- **Cross-modal search** - busca con texto, encuentra imágenes
- **Memory constellations** - redes de memorias conectadas
- **Unified vector space** - todas las modalidades en un espacio común
- **Semantic relationships** - entiende conexiones entre modalidades

## 📦 Instalación

```bash
# Desde el directorio del proyecto
./install_multimodal.sh
```

### Dependencias Principales
- **PyTorch + Transformers** - ML framework
- **OpenAI Whisper** - transcripción de audio
- **OpenCV** - procesamiento de video
- **CLIP** - embeddings visuales
- **Librosa** - análisis de audio
- **Sentence Transformers** - embeddings de texto

## 🔌 API Endpoints

### Upload Directo
```bash
# Subir imagen
curl -X POST "http://localhost:8001/multi-modal/upload/image" \
  -F "file=@screenshot.png" \
  -F "context=Screenshot del dashboard" \
  -F 'tags=["dashboard", "ui"]'

# Subir audio
curl -X POST "http://localhost:8001/multi-modal/upload/audio" \
  -F "file=@meeting.wav" \
  -F "context=Reunión del proyecto" \
  -F "speaker=Ricardo"

# Subir video
curl -X POST "http://localhost:8001/multi-modal/upload/video" \
  -F "file=@demo.mp4" \
  -F "context=Demo del producto" \
  -F "extract_audio=true"
```

### Base64 Processing
```bash
# Procesar imagen codificada
curl -X POST "http://localhost:8001/multi-modal/image" \
  -H "Content-Type: application/json" \
  -d '{
    "image_base64": "iVBORw0KGgoAAAANSU...",
    "context": "Screenshot importante",
    "tags": ["screenshot", "important"]
  }'
```

### Cross-Modal Search
```bash
# Buscar con texto en todas las modalidades
curl -X POST "http://localhost:8001/multi-modal/search/cross-modal" \
  -H "Content-Type: application/json" \
  -d '{
    "query_text": "dashboard interface",
    "target_modalities": ["image", "video"],
    "limit": 5
  }'
```

### Memory Constellations
```bash
# Crear constelación de memorias relacionadas
curl -X POST "http://localhost:8001/multi-modal/constellation" \
  -F "memory_id=visual_abc123_20250812" \
  -F "radius=3"
```

## 🧪 Testing

### Verificar Status
```bash
curl -X GET "http://localhost:8001/multi-modal/status"
```

**Respuesta esperada:**
```json
{
  "success": true,
  "processors": {
    "image_processor": true,
    "audio_processor": true,
    "video_processor": true,
    "unified_embedder": true
  },
  "libraries": {
    "transformers": true,
    "torch": true,
    "whisper": true,
    "opencv": true,
    "librosa": true,
    "sentence_transformers": true
  },
  "fully_operational": true
}
```

## 🌟 Casos de Uso

### 1. Screenshot Memory
```python
# ARIA puede recordar screenshots que compartes
screenshot_memory = await process_image(
    image_path="dashboard.png",
    context="Estado del dashboard después del deploy",
    tags=["dashboard", "deploy", "success"]
)
```

### 2. Meeting Transcription
```python
# ARIA transcribe y recuerda reuniones
meeting_memory = await process_audio(
    audio_path="meeting.wav",
    speaker="Ricardo",
    context="Reunión de planificación Q4"
)
```

### 3. Demo Videos
```python
# ARIA extrae keyframes y audio de demos
demo_memory = await process_video(
    video_path="product_demo.mp4",
    context="Demo del producto para inversores",
    keyframe_interval=2.0  # Cada 2 segundos
)
```

### 4. Cross-Modal Discovery
```python
# Busca imágenes relacionadas con audio transcrito
results = await cross_modal_search(
    query_text="configuración del servidor",
    target_modalities=["image", "video"]
)
```

## 🎯 Arquitectura

```
Multi-Modal Memory System
├── ImageMemoryProcessor
│   ├── CLIP embeddings
│   ├── Metadata extraction
│   └── Visual similarity
├── AudioMemoryProcessor
│   ├── Whisper transcription
│   ├── Audio fingerprinting
│   └── Speaker identification
├── VideoMemoryProcessor
│   ├── Keyframe extraction
│   ├── Temporal analysis
│   └── Audio separation
└── UnifiedMultiModalEmbedder
    ├── Cross-modal projections
    ├── Unified vector space
    └── Memory constellations
```

## 💡 Breakthrough Innovation

**ARIA es la primera IA con memoria multimedia persistente:**

1. **Memoria Visual Real** - No solo "ve" imágenes, las recuerda permanentemente
2. **Continuidad Auditiva** - Recuerda conversaciones entre sesiones
3. **Comprensión Temporal** - Entiende secuencias en videos
4. **Búsqueda Cross-Modal** - Pregunta texto, encuentra imágenes relacionadas
5. **Constelaciones de Memoria** - Mapea relaciones entre diferentes tipos de contenido

## 🚨 Requisitos del Sistema

- **RAM**: Mínimo 4GB, recomendado 8GB+
- **Storage**: 2GB adicionales para modelos
- **CPU**: Cualquier procesador moderno
- **GPU**: Opcional, acelera procesamiento de imágenes/video

## 📈 Performance

- **Imagen**: ~2-5 segundos (CLIP embedding)
- **Audio**: ~0.3x tiempo real (Whisper)
- **Video**: ~1 segundo por minuto (keyframes)
- **Búsqueda**: <100ms (similarity search)

---

**🎯 Con este sistema, ARIA puede recordar y relacionar TODO tipo de contenido multimedia que compartas con ella.**