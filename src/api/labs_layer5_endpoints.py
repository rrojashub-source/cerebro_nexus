"""
CEREBRO_NEXUS V3.0.0 - LABs Layer 5 API Endpoints
Session 25+ Integration: LAB_034-050 (17 LABs)

Integration Batches:
- 5C Advanced Learning: LAB_034, 035, 036, 037, 038
- 5D Neuroplasticity: LAB_039, 040, 041, 042, 043
- 5E Homeostasis: LAB_044, 045, 046, 047, 048, 049, 050
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Any
import sys
import os

# Add experiments path for LAB imports
experiments_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "experiments")
sys.path.insert(0, experiments_path)

# ============================================================================
# LAB Imports - Layer 5C: Advanced Learning
# ============================================================================
from LAYER_5_Higher_Cognition.Advanced_Learning.LAB_034_Rest_Recovery.rest_recovery_system import RestRecoverySystem
from LAYER_5_Higher_Cognition.Advanced_Learning.LAB_035_Reward_Prediction_Error.reward_prediction_error_system import RewardPredictionErrorSystem
from LAYER_5_Higher_Cognition.Advanced_Learning.LAB_036_Intrinsic_Motivation.intrinsic_motivation_system import IntrinsicMotivationSystem
from LAYER_5_Higher_Cognition.Advanced_Learning.LAB_037_Curiosity_Drive.curiosity_drive_system import CuriosityDriveSystem
from LAYER_5_Higher_Cognition.Advanced_Learning.LAB_038_Meta_Learning.meta_learning_system import MetaLearningSystem as MetaLearning38

# ============================================================================
# LAB Imports - Layer 5D: Neuroplasticity
# ============================================================================
from LAYER_5_Higher_Cognition.Pattern_Recognition.LAB_039_Habit_Formation.habit_formation_system import HabitFormationSystem
from LAYER_5_Higher_Cognition.Pattern_Recognition.LAB_040_Skill_Acquisition.skill_acquisition_system import SkillAcquisitionSystem
from LAYER_5_Higher_Cognition.Pattern_Recognition.LAB_041_Transfer_Learning.transfer_learning_system import TransferLearningSystem
from LAYER_5_Higher_Cognition.Advanced_Learning.LAB_042_Meta_Learning.meta_learning_system import MetaLearningSystem
from LAYER_5_Higher_Cognition.Advanced_Learning.LAB_043_Flow_State_Detection.flow_state_system import FlowStateSystem

# ============================================================================
# LAB Imports - Layer 5E: Homeostasis
# ============================================================================
from LAYER_5_Higher_Cognition.Advanced_Learning.LAB_044_Meditation_Mindfulness.meditation_system import MeditationSystem
from LAYER_5_Higher_Cognition.Advanced_Learning.LAB_045_Hyperfocus_Mechanism.hyperfocus_system import HyperfocusSystem
from LAYER_5_Higher_Cognition.Advanced_Learning.LAB_046_Default_Mode_Network.dmn_system import DefaultModeNetworkSystem
from LAYER_5_Higher_Cognition.Neuroplasticity.LAB_047_Synaptic_Pruning.synaptic_pruning_system import SynapticPruningSystem
from LAYER_5_Higher_Cognition.Neuroplasticity.LAB_048_Hebbian_Learning.hebbian_learning_system import HebbianLearningSystem
from LAYER_5_Higher_Cognition.Neuroplasticity.LAB_049_Long_Term_Potentiation.ltp_system import LTPSystem
from LAYER_5_Higher_Cognition.Neuroplasticity.LAB_050_Structural_Plasticity.structural_plasticity_system import StructuralPlasticitySystem

# ============================================================================
# LAB System Instances
# ============================================================================
# Layer 5C
rest_recovery = RestRecoverySystem()
rpe_system = RewardPredictionErrorSystem()
intrinsic_motivation = IntrinsicMotivationSystem()
curiosity_drive = CuriosityDriveSystem()
meta_learning_38 = MetaLearning38()

# Layer 5D
habit_formation = HabitFormationSystem()
skill_acquisition = SkillAcquisitionSystem()
transfer_learning = TransferLearningSystem()
meta_learning = MetaLearningSystem()
flow_system = FlowStateSystem()

# Layer 5E
meditation = MeditationSystem()
hyperfocus = HyperfocusSystem()
dmn = DefaultModeNetworkSystem()
synaptic_pruning = SynapticPruningSystem()
hebbian_learning = HebbianLearningSystem()
ltp_system = LTPSystem()
structural_plasticity = StructuralPlasticitySystem()

# ============================================================================
# Pydantic Models - LAB_034: Rest/Recovery
# ============================================================================

class CognitiveWorkRequest(BaseModel):
    intensity: float = Field(..., ge=0.0, le=1.0, description="Work intensity [0-1]")
    duration_minutes: float = Field(..., gt=0, description="Duration in minutes")

class RestRequest(BaseModel):
    duration_minutes: float = Field(..., gt=0, description="Rest duration in minutes")
    quality: float = Field(0.8, ge=0.0, le=1.0, description="Rest quality [0-1]")

class WakefulnessRequest(BaseModel):
    hours: float = Field(..., gt=0, description="Hours of wakefulness to simulate")

# ============================================================================
# Pydantic Models - LAB_035: Reward Prediction Error
# ============================================================================

class RPERequest(BaseModel):
    state: str = Field(..., description="Current state/task identifier")
    actual_reward: float = Field(..., ge=0.0, le=1.0, description="Actual reward received")

class RPEPredictRequest(BaseModel):
    state: str = Field(..., description="State to predict value for")

# ============================================================================
# Pydantic Models - LAB_042: Meta-Learning
# ============================================================================

class MetaLearningRequest(BaseModel):
    domain: str = Field(..., description="Learning domain")
    success: bool = Field(..., description="Was learning successful?")

# ============================================================================
# Pydantic Models - LAB_043: Flow State
# ============================================================================

class FlowDetectionRequest(BaseModel):
    challenge: float = Field(..., ge=0.0, le=1.0, description="Task challenge level")
    skill: float = Field(..., ge=0.0, le=1.0, description="Current skill level")
    attention_absorption: float = Field(..., ge=0.0, le=1.0, description="Attention absorption")
    clear_goals: bool = Field(..., description="Clear goals present?")
    immediate_feedback: bool = Field(..., description="Immediate feedback available?")

class TimeDistortionRequest(BaseModel):
    actual_time_minutes: float = Field(..., gt=0, description="Actual time elapsed")
    perceived_time_minutes: float = Field(..., gt=0, description="Perceived time")

# ============================================================================
# Pydantic Models - LAB_044: Meditation/Mindfulness
# ============================================================================

class MeditationSessionRequest(BaseModel):
    duration_minutes: float = Field(..., gt=0, description="Meditation duration")
    technique: str = Field("mindfulness", description="Meditation technique")
    focus_quality: float = Field(0.7, ge=0.0, le=1.0, description="Focus quality during session")

# ============================================================================
# Pydantic Models - LAB_045: Hyperfocus
# ============================================================================

class HyperfocusDetectionRequest(BaseModel):
    attention_level: float = Field(..., ge=0.0, le=1.0, description="Current attention level")
    task_count: int = Field(..., ge=1, description="Number of tasks being juggled")
    immersion_level: float = Field(..., ge=0.0, le=1.0, description="Immersion in task")
    intrinsic_motivation: bool = Field(..., description="Intrinsically motivated?")

class TimeAwarenessRequest(BaseModel):
    actual_time_minutes: float = Field(..., gt=0, description="Actual time elapsed")
    perceived_time_minutes: float = Field(..., gt=0, description="Perceived time")

# ============================================================================
# Pydantic Models - LAB_046: Default Mode Network
# ============================================================================

class DMNEventRequest(BaseModel):
    event_type: str = Field(..., description="Event type: self_referential, external_task, mind_wandering, etc.")
    task_type: Optional[str] = Field(None, description="Specific task type")
    difficulty: Optional[float] = Field(None, ge=0.0, le=1.0, description="Task difficulty for external tasks")
    external_stimulation: Optional[float] = Field(None, ge=0.0, le=1.0, description="External stimulation level")

# ============================================================================
# Create Router
# ============================================================================

router = APIRouter()

# ============================================================================
# LAB_034: Rest/Recovery Cycles Endpoints
# ============================================================================

@router.post("/lab/034/cognitive_work", tags=["LAB_034"])
async def perform_cognitive_work(request: CognitiveWorkRequest):
    """
    Simulate cognitive work (depletes energy, increases adenosine)

    **Use case**: Track mental energy depletion during work sessions

    **Returns**: Energy depletion, adenosine accumulation, stress increase
    """
    try:
        result = rest_recovery.perform_cognitive_work(
            intensity=request.intensity,
            duration_minutes=request.duration_minutes
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process cognitive work: {str(e)}"
        )

@router.post("/lab/034/simulate_wakefulness", tags=["LAB_034"])
async def simulate_wakefulness(request: WakefulnessRequest):
    """
    Simulate hours of wakefulness (adenosine accumulation)

    **Use case**: Fast-forward sleep pressure for testing/simulation

    **Returns**: Adenosine level, sleep pressure, needs rest flag
    """
    try:
        result = rest_recovery.simulate_wakefulness(hours=request.hours)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to simulate wakefulness: {str(e)}"
        )

@router.get("/lab/034/needs_rest", tags=["LAB_034"])
async def check_needs_rest():
    """
    Check if rest is needed based on current state

    **Use case**: Circuit breaker for burnout prevention

    **Returns**: Boolean flag + reason
    """
    try:
        needs_rest = rest_recovery.needs_rest()
        state = rest_recovery.get_state()
        return {
            "success": True,
            "needs_rest": needs_rest,
            "mental_energy": state["mental_energy"],
            "adenosine_level": state["adenosine_level"],
            "stress_level": state["stress_level"],
            "allostatic_load": state["allostatic_load"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check rest status: {str(e)}"
        )

@router.post("/lab/034/rest", tags=["LAB_034"])
async def take_rest(request: RestRequest):
    """
    Take rest period (restores energy, clears adenosine)

    **Use case**: Execute rest break, sleep simulation

    **Returns**: Energy restored, adenosine cleared, stress reduced
    """
    try:
        result = rest_recovery.rest(
            duration_minutes=request.duration_minutes,
            quality=request.quality
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process rest: {str(e)}"
        )

@router.get("/lab/034/state", tags=["LAB_034"])
async def get_rest_recovery_state():
    """
    Get current rest/recovery system state

    **Returns**: Mental energy, adenosine, stress, allostatic load, sleep pressure
    """
    try:
        state = rest_recovery.get_state()
        return {"success": True, **state}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get state: {str(e)}"
        )

# ============================================================================
# LAB_035: Reward Prediction Error Endpoints
# ============================================================================

@router.post("/lab/035/predict", tags=["LAB_035"])
async def predict_value(request: RPEPredictRequest):
    """
    Predict expected value for a state

    **Use case**: Get expectation before reward delivery

    **Returns**: Predicted value [0-1]
    """
    try:
        result = rpe_system.predict_value(state=request.state)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to predict value: {str(e)}"
        )

@router.post("/lab/035/compute_rpe", tags=["LAB_035"])
async def compute_prediction_error(request: RPERequest):
    """
    Compute Reward Prediction Error (δ = R - V(s))

    **Use case**: Learning signal after reward delivery

    **Biological Inspiration**: VTA dopaminergic neurons (Schultz et al., 1997)

    **Returns**:
    - prediction_error: δ (positive = better than expected)
    - dopamine_signal: burst/dip/none
    - learning_signal: strong/moderate/weak
    """
    try:
        result = rpe_system.compute_prediction_error(
            state=request.state,
            actual_reward=request.actual_reward
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compute RPE: {str(e)}"
        )

@router.get("/lab/035/state", tags=["LAB_035"])
async def get_rpe_state():
    """
    Get current RPE system state

    **Returns**: Value predictions, RPE history, learning signals
    """
    try:
        state = rpe_system.get_state()
        return {"success": True, **state}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get RPE state: {str(e)}"
        )

# ============================================================================
# LAB_042: Meta-Learning Endpoints
# ============================================================================

@router.post("/lab/042/adapt_learning_rate", tags=["LAB_042"])
async def adapt_learning_rate(request: MetaLearningRequest):
    """
    Adapt learning rate based on recent performance

    **Use case**: Learning-to-learn, automatic LR adjustment

    **Returns**: Old LR, new LR, adaptation direction
    """
    try:
        result = meta_learning.adapt_learning_rate(
            domain=request.domain,
            success=request.success
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to adapt learning rate: {str(e)}"
        )

@router.get("/lab/042/state", tags=["LAB_042"])
async def get_meta_learning_state():
    """
    Get current meta-learning system state

    **Returns**: Learning rates per domain, adaptation history
    """
    try:
        state = meta_learning.get_state()
        return {"success": True, **state}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get meta-learning state: {str(e)}"
        )

# ============================================================================
# LAB_043: Flow State Detection Endpoints
# ============================================================================

@router.post("/lab/043/detect_flow", tags=["LAB_043"])
async def detect_flow(request: FlowDetectionRequest):
    """
    Detect if currently in flow state

    **Use case**: Flow detection for optimal performance tracking

    **Biological Inspiration**: Csikszentmihalyi (1990) - Flow Theory

    **Returns**:
    - in_flow: Boolean
    - flow_strength: [0-1]
    - challenge_skill_balance: [0-1]
    """
    try:
        result = flow_system.detect_flow(
            challenge=request.challenge,
            skill=request.skill,
            attention_absorption=request.attention_absorption,
            clear_goals=request.clear_goals,
            immediate_feedback=request.immediate_feedback
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to detect flow: {str(e)}"
        )

@router.post("/lab/043/time_distortion", tags=["LAB_043"])
async def assess_time_distortion(request: TimeDistortionRequest):
    """
    Assess time distortion (flow characteristic)

    **Use case**: Measure temporal perception alteration

    **Returns**: Distortion ratio, significant flag
    """
    try:
        result = flow_system.assess_time_distortion(
            actual_time=request.actual_time_minutes,
            perceived_time=request.perceived_time_minutes
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to assess time distortion: {str(e)}"
        )

@router.get("/lab/043/state", tags=["LAB_043"])
async def get_flow_state():
    """
    Get current flow system state

    **Returns**: Flow active, strength, history, peak performance times
    """
    try:
        state = flow_system.get_state()
        return {"success": True, **state}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get flow state: {str(e)}"
        )

# ============================================================================
# LAB_044: Meditation/Mindfulness Endpoints
# ============================================================================

@router.post("/lab/044/meditation_session", tags=["LAB_044"])
async def meditation_session(request: MeditationSessionRequest):
    """
    Process meditation session

    **Use case**: Track meditation practice, mindfulness cultivation

    **Returns**: Mindfulness increase, body awareness change, stress reduction
    """
    try:
        result = meditation.meditation_session(
            duration_minutes=request.duration_minutes,
            technique=request.technique,
            focus_quality=request.focus_quality
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process meditation session: {str(e)}"
        )

@router.get("/lab/044/state", tags=["LAB_044"])
async def get_meditation_state():
    """
    Get current meditation/mindfulness state

    **Returns**: Mindfulness level, body awareness, practice history
    """
    try:
        state = meditation.get_state()
        return {"success": True, **state}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get meditation state: {str(e)}"
        )

# ============================================================================
# LAB_045: Hyperfocus Mechanism Endpoints
# ============================================================================

@router.post("/lab/045/detect_hyperfocus", tags=["LAB_045"])
async def detect_hyperfocus(request: HyperfocusDetectionRequest):
    """
    Detect if currently in hyperfocus state

    **Use case**: Hyperfocus detection (similar to flow but more intense)

    **Returns**:
    - in_hyperfocus: Boolean
    - hyperfocus_strength: [0-1]
    - task_absorption: [0-1]
    """
    try:
        result = hyperfocus.detect_hyperfocus(
            attention_level=request.attention_level,
            task_count=request.task_count,
            immersion_level=request.immersion_level,
            intrinsic_motivation=request.intrinsic_motivation
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to detect hyperfocus: {str(e)}"
        )

@router.post("/lab/045/time_awareness", tags=["LAB_045"])
async def assess_time_awareness(request: TimeAwarenessRequest):
    """
    Assess time awareness (hyperfocus characteristic)

    **Use case**: Measure time blindness during hyperfocus

    **Returns**: Time blind flag, distortion ratio
    """
    try:
        result = hyperfocus.assess_time_awareness(
            actual_time=request.actual_time_minutes,
            perceived_time=request.perceived_time_minutes
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to assess time awareness: {str(e)}"
        )

@router.get("/lab/045/state", tags=["LAB_045"])
async def get_hyperfocus_state():
    """
    Get current hyperfocus system state

    **Returns**: Hyperfocus active, strength, history, time blindness events
    """
    try:
        state = hyperfocus.get_state()
        return {"success": True, **state}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get hyperfocus state: {str(e)}"
        )

# ============================================================================
# LAB_046: Default Mode Network Endpoints
# ============================================================================

@router.post("/lab/046/process_event", tags=["LAB_046"])
async def process_dmn_event(request: DMNEventRequest):
    """
    Process DMN event (self-referential, external task, mind-wandering, etc.)

    **Use case**: Track DMN activation/suppression during different mental states

    **Biological Inspiration**: Raichle et al. (2001) - Default mode of brain function

    **Returns**: DMN activation level, state change, anticorrelation with task-positive network
    """
    try:
        result = dmn.process_event(
            event_type=request.event_type,
            task_type=request.task_type,
            difficulty=request.difficulty,
            external_stimulation=request.external_stimulation
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process DMN event: {str(e)}"
        )

@router.get("/lab/046/state", tags=["LAB_046"])
async def get_dmn_state():
    """
    Get current Default Mode Network state

    **Returns**: DMN active, activation level, mind-wandering rate, recent events
    """
    try:
        state = dmn.get_state()
        return {"success": True, **state}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get DMN state: {str(e)}"
        )

# ============================================================================
# LAB_036: Intrinsic Motivation Endpoints
# ============================================================================

@router.post("/lab/036/process_event", tags=["LAB_036"])
async def process_intrinsic_motivation_event(request: Dict[str, Any]):
    """Process intrinsic motivation event"""
    try:
        result = intrinsic_motivation.process_event(**request)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

@router.get("/lab/036/state", tags=["LAB_036"])
async def get_intrinsic_motivation_state():
    """Get intrinsic motivation system state"""
    try:
        state = intrinsic_motivation.get_state()
        return {"success": True, **state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

# ============================================================================
# LAB_037: Curiosity Drive Endpoints
# ============================================================================

@router.post("/lab/037/process_event", tags=["LAB_037"])
async def process_curiosity_event(request: Dict[str, Any]):
    """Process curiosity drive event"""
    try:
        result = curiosity_drive.process_event(**request)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

@router.get("/lab/037/state", tags=["LAB_037"])
async def get_curiosity_state():
    """Get curiosity drive system state"""
    try:
        state = curiosity_drive.get_state()
        return {"success": True, **state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

# ============================================================================
# LAB_038: Meta-Learning (Advanced) Endpoints
# ============================================================================

@router.post("/lab/038/process_event", tags=["LAB_038"])
async def process_meta_learning_38_event(request: Dict[str, Any]):
    """Process meta-learning event (LAB_038)"""
    try:
        result = meta_learning_38.process_event(**request)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

@router.get("/lab/038/state", tags=["LAB_038"])
async def get_meta_learning_38_state():
    """Get meta-learning system state (LAB_038)"""
    try:
        state = meta_learning_38.get_state()
        return {"success": True, **state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

# ============================================================================
# LAB_039: Habit Formation Endpoints
# ============================================================================

@router.post("/lab/039/process_event", tags=["LAB_039"])
async def process_habit_event(request: Dict[str, Any]):
    """Process habit formation event"""
    try:
        result = habit_formation.process_event(**request)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

@router.get("/lab/039/state", tags=["LAB_039"])
async def get_habit_state():
    """Get habit formation system state"""
    try:
        state = habit_formation.get_state()
        return {"success": True, **state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

# ============================================================================
# LAB_040: Skill Acquisition Endpoints
# ============================================================================

@router.post("/lab/040/process_event", tags=["LAB_040"])
async def process_skill_event(request: Dict[str, Any]):
    """Process skill acquisition event"""
    try:
        result = skill_acquisition.process_event(**request)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

@router.get("/lab/040/state", tags=["LAB_040"])
async def get_skill_state():
    """Get skill acquisition system state"""
    try:
        state = skill_acquisition.get_state()
        return {"success": True, **state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

# ============================================================================
# LAB_041: Transfer Learning Endpoints
# ============================================================================

@router.post("/lab/041/process_event", tags=["LAB_041"])
async def process_transfer_event(request: Dict[str, Any]):
    """Process transfer learning event"""
    try:
        result = transfer_learning.process_event(**request)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

@router.get("/lab/041/state", tags=["LAB_041"])
async def get_transfer_state():
    """Get transfer learning system state"""
    try:
        state = transfer_learning.get_state()
        return {"success": True, **state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

# ============================================================================
# LAB_047: Synaptic Pruning Endpoints
# ============================================================================

@router.post("/lab/047/process_event", tags=["LAB_047"])
async def process_pruning_event(request: Dict[str, Any]):
    """Process synaptic pruning event"""
    try:
        result = synaptic_pruning.process_event(**request)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

@router.get("/lab/047/state", tags=["LAB_047"])
async def get_pruning_state():
    """Get synaptic pruning system state"""
    try:
        state = synaptic_pruning.get_state()
        return {"success": True, **state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

# ============================================================================
# LAB_048: Hebbian Learning Endpoints
# ============================================================================

@router.post("/lab/048/process_event", tags=["LAB_048"])
async def process_hebbian_event(request: Dict[str, Any]):
    """Process Hebbian learning event"""
    try:
        result = hebbian_learning.process_event(**request)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

@router.get("/lab/048/state", tags=["LAB_048"])
async def get_hebbian_state():
    """Get Hebbian learning system state"""
    try:
        state = hebbian_learning.get_state()
        return {"success": True, **state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

# ============================================================================
# LAB_049: Long-Term Potentiation Endpoints
# ============================================================================

@router.post("/lab/049/process_event", tags=["LAB_049"])
async def process_ltp_event(request: Dict[str, Any]):
    """Process LTP event"""
    try:
        result = ltp_system.process_event(**request)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

@router.get("/lab/049/state", tags=["LAB_049"])
async def get_ltp_state():
    """Get LTP system state"""
    try:
        state = ltp_system.get_state()
        return {"success": True, **state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

# ============================================================================
# LAB_050: Structural Plasticity Endpoints
# ============================================================================

@router.post("/lab/050/process_event", tags=["LAB_050"])
async def process_structural_plasticity_event(request: Dict[str, Any]):
    """Process structural plasticity event"""
    try:
        result = structural_plasticity.process_event(**request)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

@router.get("/lab/050/state", tags=["LAB_050"])
async def get_structural_plasticity_state():
    """Get structural plasticity system state"""
    try:
        state = structural_plasticity.get_state()
        return {"success": True, **state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

# ============================================================================
# Export Router
# ============================================================================

def get_layer5_router():
    """Get FastAPI router with all Layer 5 LAB endpoints"""
    return router
