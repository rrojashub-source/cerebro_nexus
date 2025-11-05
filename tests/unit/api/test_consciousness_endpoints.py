"""
Session 12: Basic tests for consciousness endpoints

Tests:
- Import validation
- Model structure validation
- Endpoint function signatures

Note: Full integration tests (with API server running) will be done via smoke test
"""

import pytest
import sys
import os

# Add src/api to path
api_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "src", "api")
sys.path.insert(0, api_path)


class TestConsciousnessEndpointsImports:
    """Test that consciousness_endpoints module can be imported"""

    def test_import_consciousness_endpoints(self):
        """Should import consciousness_endpoints module"""
        import consciousness_endpoints
        assert consciousness_endpoints is not None

    def test_import_request_models(self):
        """Should import request models"""
        from consciousness_endpoints import (
            ProcessEventRequest,
            SimulateEventRequest,
            EmotionalStateRequest,
            SomaticMarkerRequest
        )
        assert ProcessEventRequest is not None
        assert SimulateEventRequest is not None
        assert EmotionalStateRequest is not None
        assert SomaticMarkerRequest is not None

    def test_import_response_models(self):
        """Should import response models"""
        from consciousness_endpoints import (
            ProcessEventResponse,
            ConsciousnessStateResponse,
            SimulateEventResponse
        )
        assert ProcessEventResponse is not None
        assert ConsciousnessStateResponse is not None
        assert SimulateEventResponse is not None

    def test_import_endpoint_functions(self):
        """Should import endpoint functions"""
        from consciousness_endpoints import (
            process_event_endpoint,
            get_consciousness_state_endpoint,
            simulate_event_endpoint,
            register_consciousness_endpoints
        )
        assert callable(process_event_endpoint)
        assert callable(get_consciousness_state_endpoint)
        assert callable(simulate_event_endpoint)
        assert callable(register_consciousness_endpoints)


class TestRequestModels:
    """Test Pydantic request models structure"""

    def test_emotional_state_request_structure(self):
        """EmotionalStateRequest should have 8D structure"""
        from consciousness_endpoints import EmotionalStateRequest

        # Create instance with all zeros
        emotional_state = EmotionalStateRequest()
        assert emotional_state.joy == 0.0
        assert emotional_state.trust == 0.0
        assert emotional_state.fear == 0.0
        assert emotional_state.surprise == 0.0
        assert emotional_state.sadness == 0.0
        assert emotional_state.disgust == 0.0
        assert emotional_state.anger == 0.0
        assert emotional_state.anticipation == 0.0

    def test_somatic_marker_request_structure(self):
        """SomaticMarkerRequest should have 3D structure (simplified)"""
        from consciousness_endpoints import SomaticMarkerRequest

        # Create instance with defaults
        somatic = SomaticMarkerRequest()
        assert somatic.valence == 0.0
        assert somatic.arousal == 0.0
        assert somatic.situation == "neutral"

    def test_process_event_request_structure(self):
        """ProcessEventRequest should have required fields"""
        from consciousness_endpoints import ProcessEventRequest

        # Create instance with minimal data
        request = ProcessEventRequest(content="Test event")
        assert request.content == "Test event"
        assert request.novelty == 0.5  # default
        assert request.emotional_state is None  # optional
        assert request.somatic_marker is None  # optional

    def test_simulate_event_request_structure(self):
        """SimulateEventRequest should have same structure as ProcessEventRequest"""
        from consciousness_endpoints import SimulateEventRequest

        # Create instance
        request = SimulateEventRequest(content="Hypothetical event")
        assert request.content == "Hypothetical event"
        assert request.novelty == 0.5
        assert request.emotional_state is None
        assert request.somatic_marker is None


class TestResponseModels:
    """Test Pydantic response models structure"""

    def test_process_event_response_structure(self):
        """ProcessEventResponse should have all layer results"""
        from consciousness_endpoints import ProcessEventResponse
        from datetime import datetime

        # Check model fields exist
        fields = ProcessEventResponse.model_fields
        assert 'success' in fields
        assert 'timestamp' in fields
        assert 'emotional_state' in fields
        assert 'attention' in fields
        assert 'neuro_state' in fields
        assert 'memory' in fields
        assert 'hybrid_memory' in fields
        assert 'temporal_reasoning' in fields
        assert 'metacognition' in fields
        assert 'predictive' in fields
        assert 'contagion' in fields
        assert 'novelty' in fields

    def test_consciousness_state_response_structure(self):
        """ConsciousnessStateResponse should have state snapshots"""
        from consciousness_endpoints import ConsciousnessStateResponse

        # Check model fields
        fields = ConsciousnessStateResponse.model_fields
        assert 'success' in fields
        assert 'timestamp' in fields
        assert 'emotional_state_8d' in fields
        assert 'somatic_state_7d' in fields
        assert 'neuro_state_5d' in fields
        assert 'stack_info' in fields

    def test_simulate_event_response_structure(self):
        """SimulateEventResponse should have simulation note"""
        from consciousness_endpoints import SimulateEventResponse

        # Check model fields
        fields = SimulateEventResponse.model_fields
        assert 'success' in fields
        assert 'simulation_note' in fields
        assert 'emotional_state' in fields
        assert 'memory' in fields


class TestHelperFunctions:
    """Test helper conversion functions"""

    def test_convert_emotional_state_none(self):
        """convert_emotional_state should handle None"""
        from consciousness_endpoints import convert_emotional_state

        result = convert_emotional_state(None)
        assert result is not None
        # Should return neutral EmotionalState
        assert result.joy == 0.0

    def test_convert_emotional_state_with_data(self):
        """convert_emotional_state should convert request to dataclass"""
        from consciousness_endpoints import convert_emotional_state, EmotionalStateRequest

        request = EmotionalStateRequest(joy=0.8, trust=0.7)
        result = convert_emotional_state(request)
        assert result.joy == 0.8
        assert result.trust == 0.7

    def test_convert_somatic_marker_none(self):
        """convert_somatic_marker should handle None"""
        from consciousness_endpoints import convert_somatic_marker

        result = convert_somatic_marker(None)
        assert result is not None
        # Should return neutral SomaticMarker
        assert result.valence == 0.0

    def test_convert_somatic_marker_with_data(self):
        """convert_somatic_marker should convert request to dataclass"""
        from consciousness_endpoints import convert_somatic_marker, SomaticMarkerRequest

        request = SomaticMarkerRequest(valence=0.8, arousal=0.9, situation="breakthrough")
        result = convert_somatic_marker(request)
        assert result.valence == 0.8
        assert result.arousal == 0.9
        assert result.situation == "breakthrough"


class TestCognitiveStackIntegration:
    """Test CognitiveStack singleton pattern"""

    def test_get_cognitive_stack_singleton(self):
        """get_cognitive_stack should return singleton"""
        from consciousness_endpoints import get_cognitive_stack

        stack1 = get_cognitive_stack()
        stack2 = get_cognitive_stack()

        assert stack1 is not None
        assert stack1 is stack2  # Same instance


# ============================================================================
# NOTE: Full API integration tests (with server running) are in smoke_test.sh
# These tests validate structure and imports only
# ============================================================================
