#!/bin/bash

# Multi-Modal Memory Installation Script
# =====================================
# Installs dependencies for ARIA's revolutionary multi-modal capabilities

echo "🎬 Installing ARIA Multi-Modal Memory System..."
echo "=============================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run from project root with 'venv' directory."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

echo "📦 Installing multi-modal dependencies..."

# Core ML libraries
echo "⚙️ Installing PyTorch and Transformers..."
pip install torch>=2.0.0 torchvision>=0.15.0 --index-url https://download.pytorch.org/whl/cpu
pip install transformers>=4.30.0

# Image processing
echo "🖼️ Installing image processing libraries..."
pip install Pillow>=9.5.0 opencv-python>=4.8.0

# Audio processing
echo "🎵 Installing audio processing libraries..."
pip install openai-whisper>=20231117 librosa>=0.10.0 soundfile>=0.12.0

# Text embeddings
echo "📝 Installing text embedding models..."
pip install sentence-transformers>=2.2.0

# Scientific computing
echo "🔬 Installing scientific computing libraries..."
pip install numpy>=1.24.0 scipy>=1.10.0

# FastAPI file uploads
echo "📤 Installing file upload support..."
pip install python-multipart>=0.0.6

# Video processing support
echo "🎥 Installing video processing support..."
pip install ffmpeg-python>=0.2.0

# Optional GPU check
echo "🔍 Checking GPU availability..."
python -c "import torch; print('GPU Available:', torch.cuda.is_available())"

echo ""
echo "✅ Multi-Modal Memory System installation complete!"
echo ""
echo "🎯 ARIA now has revolutionary capabilities:"
echo "   • Visual Memory: CLIP-based image understanding"
echo "   • Auditory Memory: Whisper transcription + audio embeddings"
echo "   • Temporal Memory: Video keyframe extraction"
echo "   • Unified Search: Cross-modal similarity search"
echo "   • Memory Constellations: Multi-modal relationship mapping"
echo ""
echo "📊 Test the installation:"
echo "   curl -X GET http://localhost:8001/multi-modal/status"
echo ""
echo "🚀 Start ARIA API to activate multi-modal endpoints!"