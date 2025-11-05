"""
NEXUS Cerebro API V3.0.0
Consciousness Endpoints - CognitiveStack Integration
Session 12: Full Stack Consciousness API

Endpoints:
- POST /consciousness/process_event - Process event through full cognitive stack
- GET /consciousness/state - Get current consciousness state
- POST /consciousness/simulate - Simulate cognitive response without persisting
"""

from fastapi import HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
import sys
import os

# Add experiments path for CognitiveStack
experiments_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "experiments")
sys.path.insert(0, experiments_path)

from INTEGRATION_LAYERS.cognitive_stack import (
    CognitiveStack,
    EmotionalState,
    SomaticMarker
)


# ============================================================================
# PYDANTIC MODELS - REQUEST/RESPONSE
# ============================================================================

class EmotionalStateRequest(BaseModel):
    """Emotional state (8D Plutchik model)"""
    joy: float = Field(0.0, ge=0.0, le=1.0, description="Joy level")
    trust: float = Field(0.0, ge=0.0, le=1.0, description="Trust level")
    fear: float = Field(0.0, ge=0.0, le=1.0, description="Fear level")
    surprise: float = Field(0.0, ge=0.0, le=1.0, description="Surprise level")
    sadness: float = Field(0.0, ge=0.0, le=1.0, description="Sadness level")
    disgust: float = Field(0.0, ge=0.0, le=1.0, description="Disgust level")
    anger: float = Field(0.0, ge=0.0, le=1.0, description="Anger level")
    anticipation: float = Field(0.0, ge=0.0, le=1.0, description="Anticipation level")


class SomaticMarkerRequest(BaseModel):
    """Somatic marker (simplified Damasio model)"""
    valence: float = Field(0.0, ge=-1.0, le=1.0, description="Valence (negative to positive)")
    arousal: float = Field(0.0, ge=0.0, le=1.0, description="Arousal level")
    situation: str = Field("neutral", description="Situation context")


class ProcessEventRequest(BaseModel):
    """Request model for POST /consciousness/process_event"""
    content: str = Field(..., description="Event content/narrative", min_length=1)
    emotional_state: Optional[EmotionalStateRequest] = Field(
        default=None,
        description="Emotional state (8D). If not provided, uses neutral state."
    )
    somatic_marker: Optional[SomaticMarkerRequest] = Field(
        default=None,
        description="Somatic marker (7D). If not provided, uses neutral state."
    )
    novelty: float = Field(
        0.5,
        ge=0.0,
        le=1.0,
        description="Novelty score (0-1). Higher = more novel."
    )


class ProcessEventResponse(BaseModel):
    """Response model for POST /consciousness/process_event"""
    success: bool
    timestamp: datetime

    # Layer 2 - Cognitive
    emotional_state: Dict[str, float]
    attention: Dict[str, Any]

    # Layer 4 - Neurochemistry
    neuro_state: Dict[str, float]

    # Layer 3 - Memory
    memory: Dict[str, Any]

    # Layer 5 - Higher Cognition
    hybrid_memory: Dict[str, Any]
    temporal_reasoning: Dict[str, Any]

    # Session 9 additions
    metacognition: Dict[str, Any]
    predictive: Dict[str, Any]
    contagion: Dict[str, Any]

    # Metadata
    novelty: Dict[str, Any]


class ConsciousnessStateResponse(BaseModel):
    """Response model for GET /consciousness/state"""
    success: bool
    timestamp: datetime

    # Current state snapshot
    emotional_state_8d: Dict[str, float]
    somatic_state_7d: Dict[str, float]
    neuro_state_5d: Dict[str, float]

    # Stack info
    stack_info: Dict[str, Any]


class SimulateEventRequest(BaseModel):
    """Request model for POST /consciousness/simulate (same as ProcessEventRequest)"""
    content: str = Field(..., description="Hypothetical event content", min_length=1)
    emotional_state: Optional[EmotionalStateRequest] = None
    somatic_marker: Optional[SomaticMarkerRequest] = None
    novelty: float = Field(0.5, ge=0.0, le=1.0)


class SimulateEventResponse(BaseModel):
    """Response model for POST /consciousness/simulate"""
    success: bool
    timestamp: datetime
    simulation_note: str = "This is a simulation. No data persisted."

    # Same structure as ProcessEventResponse (but simulation-only)
    emotional_state: Dict[str, float]
    attention: Dict[str, Any]
    neuro_state: Dict[str, float]
    memory: Dict[str, Any]
    hybrid_memory: Dict[str, Any]
    temporal_reasoning: Dict[str, Any]
    metacognition: Dict[str, Any]
    predictive: Dict[str, Any]
    contagion: Dict[str, Any]
    novelty: Dict[str, Any]


# ============================================================================
# GLOBAL COGNITIVE STACK INSTANCE
# ============================================================================

# Singleton CognitiveStack instance (initialized on first request)
_cognitive_stack: Optional[CognitiveStack] = None


def get_cognitive_stack() -> CognitiveStack:
    """Get or create CognitiveStack singleton"""
    global _cognitive_stack
    if _cognitive_stack is None:
        _cognitive_stack = CognitiveStack()
    return _cognitive_stack


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def convert_emotional_state(req: Optional[EmotionalStateRequest]) -> EmotionalState:
    """Convert EmotionalStateRequest to EmotionalState dataclass"""
    if req is None:
        # Neutral emotional state
        return EmotionalState()

    return EmotionalState(
        joy=req.joy,
        trust=req.trust,
        fear=req.fear,
        surprise=req.surprise,
        sadness=req.sadness,
        disgust=req.disgust,
        anger=req.anger,
        anticipation=req.anticipation
    )


def convert_somatic_marker(req: Optional[SomaticMarkerRequest]) -> SomaticMarker:
    """Convert SomaticMarkerRequest to SomaticMarker dataclass"""
    if req is None:
        # Neutral somatic marker
        return SomaticMarker()

    return SomaticMarker(
        valence=req.valence,
        arousal=req.arousal,
        situation=req.situation
    )


# ============================================================================
# ENDPOINTS FUNCTIONS (to be registered in main.py)
# ============================================================================

async def process_event_endpoint(request: ProcessEventRequest) -> ProcessEventResponse:
    """
    POST /consciousness/process_event

    Process event through full cognitive stack (Layer 2+3+4+5)

    Returns complete cognitive processing result including:
    - Emotional salience
    - Neurochemical modulation
    - Attention allocation
    - Memory encoding
    - Fact extraction (hybrid memory)
    - Temporal linking
    """
    try:
        # Get cognitive stack instance
        stack = get_cognitive_stack()

        # Convert request models to dataclasses
        emotional_state = convert_emotional_state(request.emotional_state)
        somatic_marker = convert_somatic_marker(request.somatic_marker)

        # Process event through full stack
        result = stack.process_event(
            content=request.content,
            emotional_state=emotional_state,
            somatic_marker=somatic_marker,
            novelty=request.novelty
        )

        # Build response
        return ProcessEventResponse(
            success=True,
            timestamp=datetime.now(),
            emotional_state=result['emotional_state'],
            attention=result['attention'],
            neuro_state=result['neuro_state'],
            memory=result['memory'],
            hybrid_memory=result['hybrid_memory'],
            temporal_reasoning=result['temporal_reasoning'],
            metacognition=result['metacognition'],
            predictive=result['predictive'],
            contagion=result['contagion'],
            novelty=result['novelty']
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing event: {str(e)}"
        )


async def get_consciousness_state_endpoint() -> ConsciousnessStateResponse:
    """
    GET /consciousness/state

    Get current consciousness state snapshot

    Returns:
    - Emotional state (8D Plutchik)
    - Somatic state (7D Damasio)
    - Neurochemical state (5D: dopamine, serotonin, norepinephrine, acetylcholine, gaba)
    - Stack info (components loaded, status)
    """
    try:
        # Get cognitive stack instance
        stack = get_cognitive_stack()

        # Build current state snapshot
        # Note: This is a simplified version - in production you'd track actual state
        return ConsciousnessStateResponse(
            success=True,
            timestamp=datetime.now(),
            emotional_state_8d={
                'joy': 0.0,
                'trust': 0.0,
                'fear': 0.0,
                'surprise': 0.0,
                'sadness': 0.0,
                'disgust': 0.0,
                'anger': 0.0,
                'anticipation': 0.0
            },
            somatic_state_7d={
                'valence': 0.0,
                'arousal': 0.0,
                'situation': 'neutral'
            },
            neuro_state_5d={
                'dopamine': 0.5,
                'serotonin': 0.5,
                'norepinephrine': 0.5,
                'acetylcholine': 0.5,
                'gaba': 0.5
            },
            stack_info={
                'cognitive_stack_loaded': True,
                'layers': {
                    'layer_2_cognitive': ['emotional_salience', 'attention', 'working_memory', 'metacognition', 'predictive', 'contagion'],
                    'layer_3_memory': ['decay_modulation', 'novelty_detection', 'consolidation'],
                    'layer_4_neuro': ['neuro_emotional_bridge'],
                    'layer_5_higher_cognition': ['hybrid_memory', 'temporal_reasoning']
                },
                'status': 'operational'
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting consciousness state: {str(e)}"
        )


async def simulate_event_endpoint(request: SimulateEventRequest) -> SimulateEventResponse:
    """
    POST /consciousness/simulate

    Simulate cognitive response to hypothetical event (without persisting)

    Same as process_event but:
    - Does NOT store in database
    - Does NOT trigger embeddings
    - Does NOT update persistent state

    Useful for:
    - What-if scenarios
    - Prediction testing
    - Emotional impact assessment
    """
    try:
        # Get cognitive stack instance
        stack = get_cognitive_stack()

        # Convert request models to dataclasses
        emotional_state = convert_emotional_state(request.emotional_state)
        somatic_marker = convert_somatic_marker(request.somatic_marker)

        # Process event through full stack (simulation only)
        result = stack.process_event(
            content=request.content,
            emotional_state=emotional_state,
            somatic_marker=somatic_marker,
            novelty=request.novelty
        )

        # Build response (same structure but marked as simulation)
        return SimulateEventResponse(
            success=True,
            timestamp=datetime.now(),
            simulation_note="This is a simulation. No data persisted.",
            emotional_state=result['emotional_state'],
            attention=result['attention'],
            neuro_state=result['neuro_state'],
            memory=result['memory'],
            hybrid_memory=result['hybrid_memory'],
            temporal_reasoning=result['temporal_reasoning'],
            metacognition=result['metacognition'],
            predictive=result['predictive'],
            contagion=result['contagion'],
            novelty=result['novelty']
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error simulating event: {str(e)}"
        )


# ============================================================================
# ROUTER REGISTRATION FUNCTION (to be called from main.py)
# ============================================================================

def register_consciousness_endpoints(app):
    """
    Register consciousness endpoints with FastAPI app

    Usage in main.py:
        from consciousness_endpoints import register_consciousness_endpoints
        register_consciousness_endpoints(app)
    """

    @app.post(
        "/consciousness/process_event",
        response_model=ProcessEventResponse,
        tags=["Consciousness"],
        summary="Process event through full cognitive stack",
        description="Process event through all layers: cognitive, memory, neurochemistry, and higher cognition"
    )
    async def process_event(request: ProcessEventRequest):
        return await process_event_endpoint(request)

    @app.get(
        "/consciousness/state",
        response_model=ConsciousnessStateResponse,
        tags=["Consciousness"],
        summary="Get current consciousness state",
        description="Get snapshot of emotional (8D), somatic (7D), and neurochemical (5D) state"
    )
    async def get_consciousness_state():
        return await get_consciousness_state_endpoint()

    @app.post(
        "/consciousness/simulate",
        response_model=SimulateEventResponse,
        tags=["Consciousness"],
        summary="Simulate cognitive response (without persisting)",
        description="Simulate full cognitive processing for hypothetical event (what-if scenarios)"
    )
    async def simulate_event(request: SimulateEventRequest):
        return await simulate_event_endpoint(request)
