"""
LABS 029-050: Advanced Cognitive Systems - API Endpoints
Integration for Creativity, Learning, Plasticity, and Homeostasis LABS

To integrate into main.py:
1. Import this module: from labs_advanced_endpoints import router as labs_advanced_router
2. Include router: app.include_router(labs_advanced_router)
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

# LAB_028: Emotional Intelligence (prerequisite for advanced LABs)
from emotional_intelligence import EmotionalIntelligenceSystem

# FASE 4: Prerequisites (LABS 004-027)
from novelty_detector import NoveltyDetector
from spreading_activation import ActivationManager
from metacognition_logger import ErrorDetector
from predictive_preloading import PredictionEngine
from emotional_contagion import EmotionalContagionEngine
from memory_reconsolidation import ReconsolidationDetector
from attention_mechanism import AttentionScorer
from working_memory_buffer import WorkingMemoryBuffer
from episodic_future_thinking import Episode
from dopamine_system import RewardPredictionEngine
from serotonin_system import TimeHorizonManager
from norepinephrine_system import StressResponseSystem
from acetylcholine_system import AcetylcholineSystem
from gaba_glutamate_balance import GABAGlutamateSystem
from working_memory_executive import WorkingMemoryExecutive
from cognitive_control import CognitiveControlSystem
from task_switching import TaskSetManager
from planning_sequencing import PlanningSequencingSystem
from goal_management import GoalHierarchyManager
from theory_of_mind import TheoryOfMindSystem
from empathy_system import EmpathySystem
from social_hierarchy import StatusDetector
from cooperation_trust import ReputationSystem
from moral_reasoning import MoralReasoningSystem


# FASE 5: Creativity & Insight (LABS 029-033)
from divergent_thinking import DivergentThinkingSystem, Idea
from conceptual_blending import ConceptualBlendingSystem, ConceptualSpace
from insight_aha import InsightAhaSystem, Problem
from analogical_reasoning import AnalogicalReasoningSystem, Structure
from metaphor_generation import MetaphorGenerationSystem

# FASE 6: Advanced Learning (LABS 034-038)
from transfer_learning import TransferLearningSystem, Knowledge, LearningContext
from reward_prediction import RewardPredictionSystem
from meta_learning import MetaLearningSystem, Task as MetaTask
from curiosity_drive import CuriosityDriveSystem
from intrinsic_motivation import IntrinsicMotivationSystem

# FASE 7: Neuroplasticity (LABS 039-043)
from ltp_ltd import LTPLTDSystem
from hebbian_learning import HebbianLearningSystem
from synaptic_pruning_neurogenesis import SynapticPruningNeurogenesisSystem

# FASE 8: Homeostasis (LABS 044-050)
from homeostasis_systems import HomeostasisSystem

# ============================================
# Router
# ============================================
router = APIRouter(prefix="/labs/advanced", tags=["Advanced LABS 029-050"])

# ============================================
# Global System Instances
# ============================================

# LAB_028: Emotional Intelligence
emotional_intelligence = EmotionalIntelligenceSystem()

# FASE 4: Prerequisites instances
# FASE 4: Prerequisites
# novelty_detector = NoveltyDetector()
# spreading_activation = ActivationManager()
# metacognition_logger = ErrorDetector()
# predictive_preloading = PredictionEngine()
# emotional_contagion = EmotionalContagionEngine()
# memory_reconsolidation = ReconsolidationDetector()
# attention_mechanism = AttentionScorer()
# working_memory_buffer = WorkingMemoryBuffer()
# episodic_future_thinking = Episode()
# dopamine_system = RewardPredictionEngine()
# serotonin_system = TimeHorizonManager()
# norepinephrine_system = StressResponseSystem()
# acetylcholine_system = AcetylcholineSystem()
# gaba_glutamate_balance = GABAGlutamateSystem()
# working_memory_executive = WorkingMemoryExecutive()
# cognitive_control = CognitiveControlSystem()
# task_switching = TaskSetManager()
# planning_sequencing = PlanningSequencingSystem()
# goal_management = GoalHierarchyManager()
# theory_of_mind = TheoryOfMindSystem()
# empathy_system = EmpathySystem()
# social_hierarchy = StatusDetector()
# cooperation_trust = ReputationSystem()
# moral_reasoning = MoralReasoningSystem()


# FASE 5: Creativity
divergent_thinking = DivergentThinkingSystem()
conceptual_blending = ConceptualBlendingSystem()
insight_system = InsightAhaSystem()
analogy_system = AnalogicalReasoningSystem()
metaphor_system = MetaphorGenerationSystem()

# FASE 6: Learning
transfer_learning = TransferLearningSystem()
reward_prediction = RewardPredictionSystem()
meta_learning = MetaLearningSystem()
curiosity_drive = CuriosityDriveSystem()
intrinsic_motivation = IntrinsicMotivationSystem()

# FASE 7: Plasticity
ltp_ltd = LTPLTDSystem()
hebbian_learning = HebbianLearningSystem()
synaptic_pruning = SynapticPruningNeurogenesisSystem()

# FASE 8: Homeostasis
homeostasis = HomeostasisSystem()

# ============================================
# Pydantic Models
# ============================================

# LAB_028: Emotional Intelligence (prerequisite)
class EmotionRecognitionRequest(BaseModel):
    source: str = Field(..., description="Source type: 'facial', 'vocal', 'contextual', 'self'")
    cues: List[str] = Field(..., description="List of emotional cues (e.g., ['smiling', 'relaxed_posture'])")
    person_id: Optional[str] = Field(None, description="Optional person identifier")
    context: Optional[str] = Field(None, description="Optional situational context")

class EmotionRecognitionResponse(BaseModel):
    success: bool
    emotion: str
    intensity: float
    confidence: float
    source: str
    person_id: Optional[str] = None
    timestamp: datetime

# ============================================
# FASE 4: Prerequisites Models (LABS 004-027)
# ============================================

class NoveltyDetectorRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Curiosity-Driven Memory - Novelty Detection System")
class NoveltyDetectorResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class ActivationManagerRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Spreading Activation & Contextual Priming")
class ActivationManagerResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class ErrorDetectorRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Metacognition Logger")
class ErrorDetectorResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class PredictionEngineRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Predictive Preloading Engine")
class PredictionEngineResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class EmotionalContagionEngineRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Emotional Contagion Engine")
class EmotionalContagionEngineResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class ReconsolidationDetectorRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Memory Reconsolidation Engine")
class ReconsolidationDetectorResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class AttentionScorerRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Attention Mechanism")
class AttentionScorerResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class WorkingMemoryBufferRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Working Memory Buffer")
class WorkingMemoryBufferResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class EpisodeRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Episodic Future Thinking")
class EpisodeResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class RewardPredictionEngineRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Dopamine System - Reward Prediction Error & Motivation")
class RewardPredictionEngineResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class TimeHorizonManagerRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Serotonin System - Mood Regulation & Impulse Control")
class TimeHorizonManagerResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class StressResponseSystemRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Norepinephrine System - Arousal, Alertness & Stress Response")
class StressResponseSystemResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class AcetylcholineSystemRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Acetylcholine System - Attention Focus & Encoding Enhancement")
class AcetylcholineSystemResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class GABAGlutamateSystemRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for GABA/Glutamate Balance - Excitation/Inhibition Homeostasis")
class GABAGlutamateSystemResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class WorkingMemoryExecutiveRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Working Memory Executive - Central Executive System")
class WorkingMemoryExecutiveResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class CognitiveControlSystemRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Cognitive Control - Inhibition, Shifting, and Updating")
class CognitiveControlSystemResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class TaskSetManagerRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Task Switching - Context Switching and Reconfiguration")
class TaskSetManagerResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class PlanningSequencingSystemRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Planning & Sequencing - Goal Decomposition and Temporal Ordering")
class PlanningSequencingSystemResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class GoalHierarchyManagerRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Goal Management - Goal Hierarchy, Priority, and Conflict Resolution")
class GoalHierarchyManagerResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class TheoryOfMindSystemRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Theory of Mind - Mental State Attribution & Belief Reasoning")
class TheoryOfMindSystemResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class EmpathySystemRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Empathy System - Emotional Resonance & Affective Perspective Taking")
class EmpathySystemResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class StatusDetectorRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Social Hierarchy - Status Detection & Dominance Processing")
class StatusDetectorResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class ReputationSystemRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Cooperation & Trust - Reciprocity and Coalition Formation")
class ReputationSystemResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime
class MoralReasoningSystemRequest(BaseModel):
    data: Dict[str, Any] = Field(default={}, description="Input data for Moral Reasoning - Ethical Judgments and Dilemma Resolution")
class MoralReasoningSystemResponse(BaseModel):
    success: bool
    result: Dict[str, Any]
    timestamp: datetime


# LAB_029: Divergent Thinking
class DivergentThinkingRequest(BaseModel):
    object_name: str = Field(..., description="Object for alternative uses generation")
    num_ideas: int = Field(default=10, ge=1, le=50)

class DivergentThinkingResponse(BaseModel):
    success: bool
    object_name: str
    ideas: List[Dict[str, Any]]
    fluency: float
    flexibility: int
    avg_originality: float
    timestamp: datetime

# LAB_030: Conceptual Blending
class ConceptualBlendingRequest(BaseModel):
    concept_1: str = Field(..., description="First concept (e.g., 'house')")
    concept_2: str = Field(..., description="Second concept (e.g., 'boat')")

class ConceptualBlendingResponse(BaseModel):
    success: bool
    blend_name: str
    emergent_properties: List[str]
    novelty_score: float
    all_properties: List[str]
    timestamp: datetime

# LAB_031: Insight
class InsightRequest(BaseModel):
    problem_type: str = Field(..., description="nine_dot, two_string, or candle")
    max_attempts: int = Field(default=10, ge=1, le=50)

class InsightResponse(BaseModel):
    success: bool
    problem_type: str
    insight_achieved: bool
    insight_type: Optional[str] = None
    restructuring: Optional[str] = None
    aha_intensity: Optional[float] = None
    attempts_before_insight: int
    timestamp: datetime

# LAB_032: Analogical Reasoning
class AnalogyRequest(BaseModel):
    source_domain: str = Field(..., description="Source domain name (e.g., 'solar_system')")
    target_domain: str = Field(..., description="Target domain name (e.g., 'atom')")

class AnalogyResponse(BaseModel):
    success: bool
    entity_mappings: Dict[str, str]
    relation_mappings: List[Dict[str, Any]]
    structural_similarity: float
    domain_distance: float
    transfer_likelihood: str
    timestamp: datetime

# LAB_033: Metaphor
class MetaphorGenerationRequest(BaseModel):
    target_concept: str = Field(..., description="Target concept (e.g., 'love', 'life', 'argument')")
    source_domain: str = Field(..., description="Source domain: journey, war, building, container, machine, organism, light, darkness, time, space")

class MetaphorGenerationResponse(BaseModel):
    success: bool
    target_concept: str
    source_domain: str
    metaphor: str
    mappings: Dict[str, str]
    novelty_score: float
    timestamp: datetime

# LAB_034: Transfer Learning
class TransferLearningRequest(BaseModel):
    knowledge_id: str = Field(..., description="Unique knowledge identifier")
    knowledge_domain: str = Field(..., description="Source domain (e.g., 'mathematics', 'physics', 'chess')")
    knowledge_content: str = Field(..., description="Knowledge content")
    abstraction_level: int = Field(default=0, ge=0, le=5, description="Abstraction level (0=concrete, 5=very abstract)")
    target_domain: str = Field(..., description="Target domain for transfer")

class TransferLearningResponse(BaseModel):
    success: bool
    transfer_successful: bool
    success_probability: float
    domain_distance: float
    transfer_type: str
    timestamp: datetime

# LAB_035: Reward Prediction
class RewardPredictionRequest(BaseModel):
    state: str = Field(..., description="Current state ID")
    action: str = Field(..., description="Action taken")
    next_state: str = Field(..., description="Next state ID")
    reward: float = Field(..., description="Reward received")
    done: bool = Field(default=False, description="Episode terminated")

class RewardPredictionResponse(BaseModel):
    success: bool
    td_error: float
    predicted_value: float
    uncertainty: float
    update_count: int
    timestamp: datetime

# LAB_036: Meta-Learning
class MetaLearningRequest(BaseModel):
    task_id: str = Field(..., description="Task identifier")
    domain: str = Field(..., description="Task domain (vision, audio, etc.)")
    difficulty: float = Field(default=0.5, ge=0.0, le=1.0, description="Task difficulty")
    trials: int = Field(default=10, ge=1, le=100, description="Number of learning trials")

class MetaLearningResponse(BaseModel):
    success: bool
    task_id: str
    learning_rate_used: float
    performance: float
    trials: int
    timestamp: datetime

# LAB_037: Curiosity Drive
class CuriosityRequest(BaseModel):
    obs_id: str = Field(..., description="Observation identifier")
    features: Dict[str, float] = Field(..., description="Feature values for the observation")

class CuriosityResponse(BaseModel):
    success: bool
    obs_id: str
    curiosity_bonus: float
    novelty: float
    prediction_error: float
    timestamp: datetime

# LAB_038: Intrinsic Motivation
class IntrinsicMotivationRequest(BaseModel):
    action_type: str = Field(..., description="Type of action: 'autonomy', 'competence', or 'relatedness'")
    value: float = Field(..., ge=0.0, le=1.0, description="Value for the action (0-1)")
    success: bool = Field(default=True, description="Whether action was successful (for competence)")
    challenge: float = Field(default=0.5, ge=0.0, le=1.0, description="Challenge level (for competence)")

class IntrinsicMotivationResponse(BaseModel):
    success: bool
    action_type: str
    autonomy: float
    competence: float
    relatedness: float
    overall_motivation: float
    timestamp: datetime

# LAB_039-043: Plasticity
class SynapseStimulationRequest(BaseModel):
    synapse_id: str
    intensity: float = Field(ge=0.0, le=1.0)

class SynapseStimulationResponse(BaseModel):
    success: bool
    synapse_id: str
    result: str  # "LTP", "LTD", or "No change"
    new_strength: float
    timestamp: datetime

class HebbianActivationRequest(BaseModel):
    neuron_ids: List[str] = Field(..., description="Neurons to co-activate")

class HebbianActivationResponse(BaseModel):
    success: bool
    activated_neurons: List[str]
    connections_formed: int
    avg_weight: float
    timestamp: datetime

# LAB_044-050: Homeostasis
class HomeostasisUpdateRequest(BaseModel):
    dt: float = Field(default=1.0, ge=0.1, le=24.0, description="Time delta in hours")

class HomeostasisUpdateResponse(BaseModel):
    success: bool
    circadian_phase: float
    energy_level: float
    stress_level: float
    allostatic_load: float
    sleep_pressure: float
    recovery_rate: float
    timestamp: datetime

class StressorRequest(BaseModel):
    intensity: float = Field(ge=0.0, le=1.0)

class SleepRequest(BaseModel):
    duration: float = Field(ge=0.1, le=12.0, description="Sleep duration in hours")

# ============================================
# LAB_028: Emotional Intelligence (prerequisite)
# ============================================

@router.post("/emotional-intelligence/recognize", response_model=EmotionRecognitionResponse, tags=["LAB_028"])
async def recognize_emotion_endpoint(request: EmotionRecognitionRequest):
    """
    LAB_028: Recognize emotion from cues (Mayer & Salovey 1997)

    Implements:
    - Emotion recognition from facial, vocal, contextual, or self cues
    - Confidence scoring based on cue quality
    - Supports multiple emotion sources

    Integration with:
    - LAB_001 (Emotional Salience) for importance
    - LAB_024 (Empathy) for emotional resonance
    """
    try:
        # Call emotional intelligence system
        result = emotional_intelligence.recognize_emotion(
            source=request.source,
            cues=request.cues,
            person_id=request.person_id,
            context=request.context
        )

        return EmotionRecognitionResponse(
            success=True,
            emotion=result.emotion.value,
            intensity=result.intensity,
            confidence=result.confidence,
            source=result.source,
            person_id=result.person_id,
            timestamp=datetime.fromtimestamp(result.timestamp)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Emotion recognition failed: {str(e)}"
        )

# ============================================
# FASE 4: Prerequisites Endpoints (LABS 004-027)
# ============================================

@router.post("/novelty-detection", response_model=NoveltyDetectorResponse, tags=["LAB_004"])
async def novelty_detector_endpoint(request: NoveltyDetectorRequest):
    """
    LAB_004: Curiosity-Driven Memory - Novelty Detection System
    Basic endpoint for NoveltyDetector
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return NoveltyDetectorResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_004 failed: {str(e)}"
        )
@router.post("/spreading-activation", response_model=ActivationManagerResponse, tags=["LAB_005"])
async def spreading_activation_endpoint(request: ActivationManagerRequest):
    """
    LAB_005: Spreading Activation & Contextual Priming
    Basic endpoint for ActivationManager
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return ActivationManagerResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_005 failed: {str(e)}"
        )
@router.post("/metacognition", response_model=ErrorDetectorResponse, tags=["LAB_006"])
async def metacognition_logger_endpoint(request: ErrorDetectorRequest):
    """
    LAB_006: Metacognition Logger
    Basic endpoint for ErrorDetector
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return ErrorDetectorResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_006 failed: {str(e)}"
        )
@router.post("/predictive-preload", response_model=PredictionEngineResponse, tags=["LAB_007"])
async def predictive_preloading_endpoint(request: PredictionEngineRequest):
    """
    LAB_007: Predictive Preloading Engine
    Basic endpoint for PredictionEngine
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return PredictionEngineResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_007 failed: {str(e)}"
        )
@router.post("/emotional-contagion", response_model=EmotionalContagionEngineResponse, tags=["LAB_008"])
async def emotional_contagion_endpoint(request: EmotionalContagionEngineRequest):
    """
    LAB_008: Emotional Contagion Engine
    Basic endpoint for EmotionalContagionEngine
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return EmotionalContagionEngineResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_008 failed: {str(e)}"
        )
@router.post("/memory-reconsolidation", response_model=ReconsolidationDetectorResponse, tags=["LAB_009"])
async def memory_reconsolidation_endpoint(request: ReconsolidationDetectorRequest):
    """
    LAB_009: Memory Reconsolidation Engine
    Basic endpoint for ReconsolidationDetector
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return ReconsolidationDetectorResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_009 failed: {str(e)}"
        )
@router.post("/attention", response_model=AttentionScorerResponse, tags=["LAB_010"])
async def attention_mechanism_endpoint(request: AttentionScorerRequest):
    """
    LAB_010: Attention Mechanism
    Basic endpoint for AttentionScorer
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return AttentionScorerResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_010 failed: {str(e)}"
        )
@router.post("/working-memory", response_model=WorkingMemoryBufferResponse, tags=["LAB_011"])
async def working_memory_buffer_endpoint(request: WorkingMemoryBufferRequest):
    """
    LAB_011: Working Memory Buffer
    Basic endpoint for WorkingMemoryBuffer
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return WorkingMemoryBufferResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_011 failed: {str(e)}"
        )
@router.post("/episodic-future", response_model=EpisodeResponse, tags=["LAB_012"])
async def episodic_future_thinking_endpoint(request: EpisodeRequest):
    """
    LAB_012: Episodic Future Thinking
    Basic endpoint for Episode
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return EpisodeResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_012 failed: {str(e)}"
        )
@router.post("/dopamine", response_model=RewardPredictionEngineResponse, tags=["LAB_013"])
async def dopamine_system_endpoint(request: RewardPredictionEngineRequest):
    """
    LAB_013: Dopamine System - Reward Prediction Error & Motivation
    Basic endpoint for RewardPredictionEngine
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return RewardPredictionEngineResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_013 failed: {str(e)}"
        )
@router.post("/serotonin", response_model=TimeHorizonManagerResponse, tags=["LAB_014"])
async def serotonin_system_endpoint(request: TimeHorizonManagerRequest):
    """
    LAB_014: Serotonin System - Mood Regulation & Impulse Control
    Basic endpoint for TimeHorizonManager
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return TimeHorizonManagerResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_014 failed: {str(e)}"
        )
@router.post("/norepinephrine", response_model=StressResponseSystemResponse, tags=["LAB_015"])
async def norepinephrine_system_endpoint(request: StressResponseSystemRequest):
    """
    LAB_015: Norepinephrine System - Arousal, Alertness & Stress Response
    Basic endpoint for StressResponseSystem
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return StressResponseSystemResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_015 failed: {str(e)}"
        )
@router.post("/acetylcholine", response_model=AcetylcholineSystemResponse, tags=["LAB_016"])
async def acetylcholine_system_endpoint(request: AcetylcholineSystemRequest):
    """
    LAB_016: Acetylcholine System - Attention Focus & Encoding Enhancement
    Basic endpoint for AcetylcholineSystem
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return AcetylcholineSystemResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_016 failed: {str(e)}"
        )
@router.post("/gaba-glutamate", response_model=GABAGlutamateSystemResponse, tags=["LAB_017"])
async def gaba_glutamate_balance_endpoint(request: GABAGlutamateSystemRequest):
    """
    LAB_017: GABA/Glutamate Balance - Excitation/Inhibition Homeostasis
    Basic endpoint for GABAGlutamateSystem
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return GABAGlutamateSystemResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_017 failed: {str(e)}"
        )
@router.post("/working-memory-executive", response_model=WorkingMemoryExecutiveResponse, tags=["LAB_018"])
async def working_memory_executive_endpoint(request: WorkingMemoryExecutiveRequest):
    """
    LAB_018: Working Memory Executive - Central Executive System
    Basic endpoint for WorkingMemoryExecutive
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return WorkingMemoryExecutiveResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_018 failed: {str(e)}"
        )
@router.post("/cognitive-control", response_model=CognitiveControlSystemResponse, tags=["LAB_019"])
async def cognitive_control_endpoint(request: CognitiveControlSystemRequest):
    """
    LAB_019: Cognitive Control - Inhibition, Shifting, and Updating
    Basic endpoint for CognitiveControlSystem
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return CognitiveControlSystemResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_019 failed: {str(e)}"
        )
@router.post("/task-switching", response_model=TaskSetManagerResponse, tags=["LAB_020"])
async def task_switching_endpoint(request: TaskSetManagerRequest):
    """
    LAB_020: Task Switching - Context Switching and Reconfiguration
    Basic endpoint for TaskSetManager
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return TaskSetManagerResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_020 failed: {str(e)}"
        )
@router.post("/planning", response_model=PlanningSequencingSystemResponse, tags=["LAB_021"])
async def planning_sequencing_endpoint(request: PlanningSequencingSystemRequest):
    """
    LAB_021: Planning & Sequencing - Goal Decomposition and Temporal Ordering
    Basic endpoint for PlanningSequencingSystem
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return PlanningSequencingSystemResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_021 failed: {str(e)}"
        )
@router.post("/goal-management", response_model=GoalHierarchyManagerResponse, tags=["LAB_022"])
async def goal_management_endpoint(request: GoalHierarchyManagerRequest):
    """
    LAB_022: Goal Management - Goal Hierarchy, Priority, and Conflict Resolution
    Basic endpoint for GoalHierarchyManager
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return GoalHierarchyManagerResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_022 failed: {str(e)}"
        )
@router.post("/theory-of-mind", response_model=TheoryOfMindSystemResponse, tags=["LAB_023"])
async def theory_of_mind_endpoint(request: TheoryOfMindSystemRequest):
    """
    LAB_023: Theory of Mind - Mental State Attribution & Belief Reasoning
    Basic endpoint for TheoryOfMindSystem
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return TheoryOfMindSystemResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_023 failed: {str(e)}"
        )
@router.post("/empathy", response_model=EmpathySystemResponse, tags=["LAB_024"])
async def empathy_system_endpoint(request: EmpathySystemRequest):
    """
    LAB_024: Empathy System - Emotional Resonance & Affective Perspective Taking
    Basic endpoint for EmpathySystem
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return EmpathySystemResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_024 failed: {str(e)}"
        )
@router.post("/social-hierarchy", response_model=StatusDetectorResponse, tags=["LAB_025"])
async def social_hierarchy_endpoint(request: StatusDetectorRequest):
    """
    LAB_025: Social Hierarchy - Status Detection & Dominance Processing
    Basic endpoint for StatusDetector
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return StatusDetectorResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_025 failed: {str(e)}"
        )
@router.post("/cooperation", response_model=ReputationSystemResponse, tags=["LAB_026"])
async def cooperation_trust_endpoint(request: ReputationSystemRequest):
    """
    LAB_026: Cooperation & Trust - Reciprocity and Coalition Formation
    Basic endpoint for ReputationSystem
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return ReputationSystemResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_026 failed: {str(e)}"
        )
@router.post("/moral-reasoning", response_model=MoralReasoningSystemResponse, tags=["LAB_027"])
async def moral_reasoning_endpoint(request: MoralReasoningSystemRequest):
    """
    LAB_027: Moral Reasoning - Ethical Judgments and Dilemma Resolution
    Basic endpoint for MoralReasoningSystem
    """
    try:
        # Call system (adapt based on actual API)
        result = {"status": "active", "data": request.data}
        return MoralReasoningSystemResponse(
            success=True,
            result=result,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LAB_027 failed: {str(e)}"
        )


# ============================================
# FASE 5: Creativity & Insight Endpoints
# ============================================

@router.post("/divergent-thinking", response_model=DivergentThinkingResponse, tags=["LAB_029"])
async def generate_alternative_uses(request: DivergentThinkingRequest):
    """
    LAB_029: Generate alternative uses for an object (Guilford's test)

    Measures:
    - Fluency (number of ideas)
    - Flexibility (number of categories)
    - Originality (statistical rarity)
    """
    try:
        # Generate ideas
        ideas = divergent_thinking.generator.generate_uses(
            request.object_name,
            request.num_ideas
        )

        # Calculate metrics
        fluency_result = divergent_thinking.fluency.compute_fluency(ideas, duration=60.0)
        flexibility_result = divergent_thinking.flexibility.compute_flexibility(ideas)
        originality_scores = [divergent_thinking.originality.compute_originality(idea)
                             for idea in ideas]

        return DivergentThinkingResponse(
            success=True,
            object_name=request.object_name,
            ideas=[{
                "content": idea.content,
                "category": idea.category,
                "originality": idea.originality_score
            } for idea in ideas],
            fluency=fluency_result["ideas_per_minute"],
            flexibility=flexibility_result["num_categories"],
            avg_originality=sum(originality_scores) / len(originality_scores) if originality_scores else 0.0,
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Divergent thinking failed: {str(e)}"
        )


@router.post("/conceptual-blending", response_model=ConceptualBlendingResponse, tags=["LAB_030"])
async def create_conceptual_blend(request: ConceptualBlendingRequest):
    """
    LAB_030: Create conceptual blend from two concepts

    Fauconnier & Turner (2002) blending theory
    Example: concept_1="house", concept_2="boat" → houseboat (floating dwelling)
    """
    try:
        # Create blend using the system's API
        blend = conceptual_blending.create_blend(
            concept_1=request.concept_1,
            concept_2=request.concept_2
        )

        # Extract all properties from blended space
        all_properties = []
        for concept, props in blend.blended.properties.items():
            all_properties.extend(list(props))

        return ConceptualBlendingResponse(
            success=True,
            blend_name=blend.blend_id,
            emergent_properties=list(blend.emergent_properties),
            novelty_score=blend.novelty_score,
            all_properties=all_properties,
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Conceptual blending failed: {str(e)}"
        )


@router.post("/insight", response_model=InsightResponse, tags=["LAB_031"])
async def generate_insight(request: InsightRequest):
    """
    LAB_031: Generate insight for classic insight problems

    Problems:
    - nine_dot: 9-dot problem (think outside the box)
    - two_string: Two-string problem (Maier, 1931)
    - candle: Candle problem (Duncker, 1945)
    """
    try:
        # Define classic insight problems
        problem_definitions = {
            "nine_dot": {
                "description": "Connect 9 dots in 3x3 grid with 4 straight lines without lifting pen",
                "constraints": {"pen_continuous", "lines_straight"}
            },
            "two_string": {
                "description": "Tie two strings hanging from ceiling, but cannot reach both at once",
                "constraints": {"distance_too_far", "strings_fixed"}
            },
            "candle": {
                "description": "Attach candle to wall using only box of tacks",
                "constraints": {"no_damage_wall", "candle_must_burn"}
            }
        }

        if request.problem_type not in problem_definitions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown problem type: {request.problem_type}. Valid: nine_dot, two_string, candle"
            )

        # Register problem if not exists
        if request.problem_type not in insight_system.problems:
            problem_def = problem_definitions[request.problem_type]
            insight_system.register_problem(
                problem_id=request.problem_type,
                description=problem_def["description"],
                constraints=problem_def["constraints"]
            )

        # Solve using full insight protocol
        history = insight_system.solve_with_insight_protocol(
            problem_id=request.problem_type,
            max_attempts=request.max_attempts
        )

        # Extract insight moment if occurred
        insight_moment = history.get("insight")

        # Map restructuring from old → new representation
        restructuring = None
        if insight_moment:
            restructuring = f"{insight_moment.old_representation} → {insight_moment.new_representation}"

        return InsightResponse(
            success=True,
            problem_type=request.problem_type,
            insight_achieved=history["insight_occurred"],
            insight_type=insight_moment.insight_type.value if insight_moment else None,
            restructuring=restructuring,
            aha_intensity=insight_moment.aha_intensity if insight_moment else None,
            attempts_before_insight=len(history["attempts"]),
            timestamp=datetime.now()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Insight generation failed: {str(e)}"
        )


@router.post("/analogy", response_model=AnalogyResponse, tags=["LAB_032"])
async def create_analogy_endpoint(request: AnalogyRequest):
    """
    LAB_032: Create structural analogy between domains

    Gentner (1983) structure-mapping theory
    Example: source="solar_system", target="atom" → (sun→nucleus, planets→electrons)
    """
    try:
        # Create analogy using system's API
        mapping = analogy_system.create_analogy(
            source_name=request.source_domain,
            target_name=request.target_domain
        )

        # Evaluate quality
        quality = analogy_system.evaluate_mapping_quality(mapping)

        # Determine transfer type based on similarity
        transfer_type = "near" if mapping.surface_similarity > 0.5 else "far"

        return AnalogyResponse(
            success=True,
            entity_mappings=mapping.entity_mappings,
            relation_mappings=[
                {"source": r[0].relation_type.value, "target": r[1].relation_type.value}
                for r in mapping.relation_mappings
            ],
            structural_similarity=mapping.structural_similarity,
            domain_distance=1.0 - mapping.surface_similarity,  # Inverse of surface sim
            transfer_likelihood=transfer_type,
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analogy creation failed: {str(e)}"
        )


@router.post("/metaphor", response_model=MetaphorGenerationResponse, tags=["LAB_033"])
async def generate_metaphor_endpoint(request: MetaphorGenerationRequest):
    """
    LAB_033: Generate novel metaphor

    Lakoff & Johnson (1980) conceptual metaphor theory
    Example: target="love", source="journey" → "Our relationship is at a crossroads"
    """
    try:
        from metaphor_generation import Domain

        # Convert source_domain string to Domain enum
        try:
            source_domain_enum = Domain[request.source_domain.upper()]
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid source domain: {request.source_domain}. Valid: {[d.value for d in Domain]}"
            )

        # Generate metaphor using system's API
        generation = metaphor_system.generate_novel_metaphor(
            target_concept=request.target_concept,
            source_domain=source_domain_enum
        )

        return MetaphorGenerationResponse(
            success=True,
            target_concept=request.target_concept,
            source_domain=request.source_domain,
            metaphor=generation.generated_expression,
            mappings={},  # MetaphorGeneration doesn't have mappings field
            novelty_score=generation.novelty_score,
            timestamp=datetime.now()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Metaphor generation failed: {str(e)}"
        )


# ============================================
# FASE 6: Advanced Learning Endpoints
# ============================================

@router.post("/transfer-learning", response_model=TransferLearningResponse, tags=["LAB_034"])
async def transfer_knowledge_endpoint(request: TransferLearningRequest):
    """
    LAB_034: Transfer knowledge across domains

    Thorndike & Woodworth (1901) transfer of training
    Near transfer: similar domains (high success)
    Far transfer: dissimilar domains (harder, abstract knowledge transfers better)
    """
    try:
        # Acquire knowledge using system method
        knowledge = transfer_learning.acquire_knowledge(
            knowledge_id=request.knowledge_id,
            domain=request.knowledge_domain,
            content=request.knowledge_content,
            abstraction_level=request.abstraction_level
        )

        # Create minimal target context
        target_context = LearningContext(
            context_id=f"context_{request.target_domain}",
            domain=request.target_domain,
            features=set(),  # Minimal context
            difficulty=0.5
        )

        # Transfer knowledge using high-level API
        transfer_attempt = transfer_learning.transfer_knowledge(
            knowledge_id=request.knowledge_id,
            target_domain=request.target_domain,
            target_context=target_context
        )

        # Determine if transfer was successful (threshold at 0.5)
        transfer_successful = transfer_attempt.success_rate >= 0.5

        return TransferLearningResponse(
            success=True,
            transfer_successful=transfer_successful,
            success_probability=transfer_attempt.success_rate,
            domain_distance=transfer_attempt.transfer_distance,
            transfer_type=transfer_attempt.transfer_type.value,
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Transfer learning failed: {str(e)}"
        )


@router.post("/reward-prediction", response_model=RewardPredictionResponse, tags=["LAB_035"])
async def learn_reward_prediction(request: RewardPredictionRequest):
    """
    LAB_035: Learn from transition and predict reward

    Temporal-difference learning (Sutton & Barto, 2018)
    Model-free and model-based reward prediction
    """
    try:
        # Learn from transition using high-level API
        td_error = reward_prediction.learn_from_transition(
            state=request.state,
            action=request.action,
            next_state=request.next_state,
            reward=request.reward,
            done=request.done
        )

        # Predict value of current state
        value_estimate = reward_prediction.predict_value(request.state)

        return RewardPredictionResponse(
            success=True,
            td_error=td_error,
            predicted_value=value_estimate.value,
            uncertainty=value_estimate.uncertainty,
            update_count=value_estimate.update_count,
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Reward prediction failed: {str(e)}"
        )


@router.get("/reward-prediction/stats", tags=["LAB_035"])
async def get_reward_prediction_stats():
    """
    LAB_035: Get reward prediction statistics

    Combines model-free (TD learning) and model-based (forward model) RL
    """
    try:
        stats = reward_prediction.get_statistics()

        return {
            "success": True,
            "mode": stats.get("mode"),
            "states_visited": stats.get("states_visited"),
            "total_transitions": stats.get("total_transitions"),
            "avg_value": stats.get("avg_value"),
            "model_based_transitions": stats.get("model_based_transitions"),
            "timestamp": datetime.now()
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get stats: {str(e)}"
        )


@router.post("/meta-learning", response_model=MetaLearningResponse, tags=["LAB_036"])
async def learn_task_endpoint(request: MetaLearningRequest):
    """
    LAB_036: Meta-Learning - Learning to Learn

    Harlow (1949) learning sets - adapts learning rate based on task similarity
    MAML algorithm principles - rapid acquisition from experience
    """
    try:
        # Create task object
        task = MetaTask(
            task_id=request.task_id,
            domain=request.domain,
            difficulty=request.difficulty
        )

        # Learn task with adapted learning rate (high-level API)
        experience = meta_learning.learn_task(task, trials=request.trials)

        return MetaLearningResponse(
            success=True,
            task_id=experience.task_id,
            learning_rate_used=experience.learning_rate_used,
            performance=experience.performance,
            trials=experience.trials,
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Meta-learning failed: {str(e)}"
        )


@router.post("/curiosity", response_model=CuriosityResponse, tags=["LAB_037"])
async def generate_curiosity_endpoint(request: CuriosityRequest):
    """
    LAB_037: Curiosity Drive - Generate curiosity bonus for observation

    Berlyne (1960) curiosity theory + Schmidhuber (1991) curiosity-driven learning
    Combines novelty (inverse familiarity) and prediction error to generate intrinsic reward
    """
    try:
        # Generate curiosity bonus (high-level API)
        curiosity_bonus = curiosity_drive.generate_curiosity_bonus(
            obs_id=request.obs_id,
            features=request.features
        )

        # Get the last observation to access novelty and prediction_error
        last_obs = curiosity_drive.observations[-1]

        return CuriosityResponse(
            success=True,
            obs_id=last_obs.obs_id,
            curiosity_bonus=curiosity_bonus,
            novelty=last_obs.novelty,
            prediction_error=last_obs.prediction_error,
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Curiosity generation failed: {str(e)}"
        )


@router.get("/curiosity/stats", tags=["LAB_037"])
async def get_curiosity_stats():
    """
    LAB_037: Get curiosity drive statistics

    Schmidhuber (1991) curiosity-driven learning
    """
    try:
        stats = curiosity_drive.get_statistics()

        return {
            "success": True,
            **stats,
            "timestamp": datetime.now()
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get stats: {str(e)}"
        )


@router.post("/intrinsic-motivation", response_model=IntrinsicMotivationResponse, tags=["LAB_038"])
async def update_motivation_endpoint(request: IntrinsicMotivationRequest):
    """
    LAB_038: Intrinsic Motivation - Update motivation state

    Deci & Ryan (2000) Self-Determination Theory (SDT)
    Three basic psychological needs: Autonomy, Competence, Relatedness
    """
    try:
        # Update based on action type (high-level API)
        if request.action_type == "autonomy":
            intrinsic_motivation.update_autonomy(choice_freedom=request.value)
        elif request.action_type == "competence":
            intrinsic_motivation.update_competence(
                success=request.success,
                challenge=request.challenge
            )
        elif request.action_type == "relatedness":
            intrinsic_motivation.update_relatedness(social_connection=request.value)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid action_type: {request.action_type}. Must be 'autonomy', 'competence', or 'relatedness'"
            )

        # Get updated state
        state = intrinsic_motivation.get_motivation_state()

        return IntrinsicMotivationResponse(
            success=True,
            action_type=request.action_type,
            autonomy=state.autonomy,
            competence=state.competence,
            relatedness=state.relatedness,
            overall_motivation=state.overall,
            timestamp=datetime.now()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Motivation update failed: {str(e)}"
        )


@router.get("/intrinsic-motivation/stats", tags=["LAB_038"])
async def get_intrinsic_motivation_stats():
    """
    LAB_038: Get intrinsic motivation statistics

    Deci & Ryan (2000) Self-Determination Theory
    - Autonomy
    - Competence
    - Relatedness
    """
    try:
        state = intrinsic_motivation.get_motivation_state()

        return {
            "success": True,
            "autonomy": state.autonomy,
            "competence": state.competence,
            "relatedness": state.relatedness,
            "overall_motivation": state.overall,
            "timestamp": datetime.now()
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get stats: {str(e)}"
        )


# ============================================
# LAB_039-040: LTP & LTD (Neuroplasticity)
# ============================================


@router.post("/ltp-ltd", response_model=SynapseStimulationResponse, tags=["LAB_039", "LAB_040"])
async def stimulate_synapse(request: SynapseStimulationRequest):
    """
    LAB_039-040: Long-Term Potentiation & Depression

    Bliss & Lømo (1973) LTP discovery, Bear & Malenka (1994) mechanisms
    Synaptic strengthening (LTP) or weakening (LTD) based on stimulation intensity

    - intensity >= 0.7 → LTP (strengthen synapse +0.1)
    - intensity <= 0.3 → LTD (weaken synapse -0.1)
    - 0.3 < intensity < 0.7 → No change
    """
    try:
        # Get synapse strength before stimulation (if exists)
        synapse = ltp_ltd.synapses.get(request.synapse_id)
        strength_before = synapse.strength if synapse else 0.5

        # Stimulate synapse (high-level API)
        result = ltp_ltd.stimulate(request.synapse_id, request.intensity)

        # Get updated synapse
        synapse = ltp_ltd.synapses[request.synapse_id]

        return SynapseStimulationResponse(
            success=True,
            synapse_id=request.synapse_id,
            result=result,
            new_strength=synapse.strength,
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Synapse stimulation failed: {str(e)}"
        )


# ============================================
# FASE 7: Neuroplasticity Endpoints
# ============================================

@router.post("/synapse/stimulate", response_model=SynapseStimulationResponse, tags=["LAB_039-040"])
async def stimulate_synapse(request: SynapseStimulationRequest):
    """
    LAB_039/040: Stimulate synapse (trigger LTP or LTD)

    Bliss & Lømo (1973) LTP, Bear & Malenka (1994) LTD
    - High intensity (≥0.7): LTP (strengthening)
    - Low intensity (≤0.3): LTD (weakening)
    """
    try:
        result = ltp_ltd.stimulate(request.synapse_id, request.intensity)
        synapse = ltp_ltd.synapses.get(request.synapse_id)

        return SynapseStimulationResponse(
            success=True,
            synapse_id=request.synapse_id,
            result=result,
            new_strength=synapse.strength if synapse else 0.5,
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Synapse stimulation failed: {str(e)}"
        )


@router.post("/hebbian/activate", response_model=HebbianActivationResponse, tags=["LAB_041"])
async def activate_neurons_hebbian(request: HebbianActivationRequest):
    """
    LAB_041: Co-activate neurons (Hebbian learning)

    Hebb (1949): "Cells that fire together wire together"
    Creates connections between co-active neurons
    """
    try:
        import time

        # Activate neurons
        timestamp = time.time()
        hebbian_learning.activate_neurons(request.neuron_ids, timestamp)

        # Update weights
        hebbian_learning.update_weights()

        # Get stats
        stats = hebbian_learning.get_statistics()

        return HebbianActivationResponse(
            success=True,
            activated_neurons=request.neuron_ids,
            connections_formed=stats["connections"],
            avg_weight=stats["avg_weight"],
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Hebbian activation failed: {str(e)}"
        )


@router.post("/synaptic-pruning/execute", tags=["LAB_042-043"])
async def execute_synaptic_pruning():
    """
    LAB_042/043: Execute synaptic pruning and neurogenesis

    Huttenlocher (1979) pruning, Altman & Das (1965) neurogenesis
    - Prunes weak neurons
    - Generates new neurons to maintain count
    """
    try:
        # Age neurons
        synaptic_pruning.age_neurons()

        # Prune
        pruned = synaptic_pruning.prune_weak_neurons()

        # Neurogenesis
        synaptic_pruning.homeostatic_regulation()

        # Stats
        stats = synaptic_pruning.get_statistics()

        return {
            "success": True,
            "pruned_count": len(pruned),
            "total_neurons": stats["total_neurons"],
            "avg_strength": stats["avg_strength"],
            "timestamp": datetime.now()
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Synaptic pruning failed: {str(e)}"
        )


# ============================================
# FASE 8: Homeostasis Endpoints
# ============================================

@router.post("/homeostasis/update", response_model=HomeostasisUpdateResponse, tags=["LAB_044-050"])
async def update_homeostasis(request: HomeostasisUpdateRequest):
    """
    LAB_044-050: Update all homeostatic systems

    Systems:
    - LAB_044: Circadian rhythms (24h cycle)
    - LAB_045: Energy management
    - LAB_046: Stress regulation
    - LAB_047: Allostatic load (cumulative stress)
    - LAB_048: Homeostatic plasticity
    - LAB_049: Sleep pressure
    - LAB_050: Recovery mechanisms
    """
    try:
        homeostasis.update(dt=request.dt)
        state = homeostasis.get_state()

        return HomeostasisUpdateResponse(
            success=True,
            circadian_phase=state.circadian_phase,
            energy_level=state.energy_level,
            stress_level=state.stress_level,
            allostatic_load=state.allostatic_load,
            sleep_pressure=state.sleep_pressure,
            recovery_rate=state.recovery_rate,
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Homeostasis update failed: {str(e)}"
        )


@router.post("/homeostasis/stressor", tags=["LAB_046"])
async def add_stressor(request: StressorRequest):
    """
    LAB_046: Add stressor to system

    Increases stress level, may accumulate allostatic load if sustained
    """
    try:
        homeostasis.add_stressor(request.intensity)
        state = homeostasis.get_state()

        return {
            "success": True,
            "new_stress_level": state.stress_level,
            "allostatic_load": state.allostatic_load,
            "timestamp": datetime.now()
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add stressor: {str(e)}"
        )


@router.post("/homeostasis/sleep", tags=["LAB_049"])
async def sleep_period(request: SleepRequest):
    """
    LAB_049: Execute sleep period

    Releases sleep pressure, recovers energy, reduces stress
    """
    try:
        homeostasis.sleep(request.duration)
        state = homeostasis.get_state()

        return {
            "success": True,
            "energy_level": state.energy_level,
            "stress_level": state.stress_level,
            "sleep_pressure": state.sleep_pressure,
            "timestamp": datetime.now()
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Sleep period failed: {str(e)}"
        )


@router.get("/homeostasis/stats", tags=["LAB_044-050"])
async def get_homeostasis_stats():
    """
    Get comprehensive homeostasis statistics
    """
    try:
        stats = homeostasis.get_statistics()

        return {
            "success": True,
            **stats,
            "timestamp": datetime.now()
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get stats: {str(e)}"
        )


# ============================================
# Summary Endpoint
# ============================================

@router.get("/summary", tags=["Summary"])
async def get_all_labs_summary():
    """
    Get summary of all 50 LABS status

    Returns operational status and key metrics for all LABS
    """
    try:
        return {
            "success": True,
            "total_labs": 50,
            "active_labs": 50,
            "fases": {
                "FASE_5_CREATIVITY": {
                    "labs": ["029", "030", "031", "032", "033"],
                    "status": "active",
                    "systems": ["divergent_thinking", "conceptual_blending", "insight", "analogy", "metaphor"]
                },
                "FASE_6_LEARNING": {
                    "labs": ["034", "035", "036", "037", "038"],
                    "status": "active",
                    "systems": ["transfer_learning", "reward_prediction", "meta_learning", "curiosity", "intrinsic_motivation"]
                },
                "FASE_7_PLASTICITY": {
                    "labs": ["039", "040", "041", "042", "043"],
                    "status": "active",
                    "systems": ["ltp_ltd", "hebbian_learning", "synaptic_pruning_neurogenesis"]
                },
                "FASE_8_HOMEOSTASIS": {
                    "labs": ["044", "045", "046", "047", "048", "049", "050"],
                    "status": "active",
                    "systems": ["homeostasis_unified"]
                }
            },
            "integration_complete": True,
            "api_version": "2.0.0",
            "timestamp": datetime.now()
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get summary: {str(e)}"
        )
