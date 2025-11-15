"""
NEXUS Cerebro API V3.0.0
WebSocket Endpoints - Real-time Consciousness Updates
Session 29: WebSocket Implementation

Endpoints:
- WS /ws/consciousness - Real-time consciousness state updates
"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import Set, Dict, Any
import asyncio
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# CONNECTION MANAGER
# ============================================================================

class ConnectionManager:
    """
    Manages WebSocket connections for real-time consciousness updates

    Features:
    - Multiple concurrent connections
    - Broadcast to all connected clients
    - Auto-cleanup on disconnect
    - Heartbeat/ping-pong for connection health
    """

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self._broadcast_task: asyncio.Task | None = None

    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"✅ WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        self.active_connections.discard(websocket)
        logger.info(f"❌ WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """Send message to specific client"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            self.disconnect(websocket)

    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast message to all connected clients"""
        disconnected = set()

        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.add(connection)

        # Cleanup failed connections
        for conn in disconnected:
            self.disconnect(conn)

    def get_connection_count(self) -> int:
        """Get current number of active connections"""
        return len(self.active_connections)


# Global connection manager instance
manager = ConnectionManager()


# ============================================================================
# CONSCIOUSNESS STATE BROADCASTER
# ============================================================================

async def consciousness_state_broadcaster(interval_seconds: int = 5):
    """
    Background task that broadcasts consciousness state every N seconds

    This runs continuously and sends updates to all connected WebSocket clients
    """
    # Import here to avoid circular dependencies
    from src.api.consciousness_endpoints import get_consciousness_state_endpoint

    logger.info(f"🔄 Starting consciousness state broadcaster (interval: {interval_seconds}s)")

    while True:
        try:
            if manager.get_connection_count() > 0:
                # Get current consciousness state
                state = await get_consciousness_state_endpoint()

                # Convert Pydantic model to dict
                state_dict = state.model_dump()

                # Add metadata
                state_dict['_websocket_metadata'] = {
                    'type': 'consciousness_update',
                    'broadcast_time': datetime.now().isoformat(),
                    'connection_count': manager.get_connection_count()
                }

                # Broadcast to all clients
                await manager.broadcast(state_dict)

                logger.debug(f"📡 Broadcasted consciousness state to {manager.get_connection_count()} clients")

            # Wait for next broadcast
            await asyncio.sleep(interval_seconds)

        except Exception as e:
            logger.error(f"⚠️  Error in consciousness broadcaster: {e}")
            await asyncio.sleep(interval_seconds)  # Continue even on error


# ============================================================================
# WEBSOCKET ENDPOINT
# ============================================================================

async def websocket_consciousness_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint: /ws/consciousness

    Real-time consciousness state updates

    Protocol:
    - Server → Client: Consciousness state updates every 5 seconds
    - Client → Server: Heartbeat/ping messages
    - Auto-disconnect on errors

    Message Format (Server → Client):
    {
      "success": true,
      "timestamp": "2025-11-14T...",
      "emotional_state_8d": {...},
      "somatic_state_7d": {...},
      "neuro_state_5d": {...},
      "stack_info": {...},
      "_websocket_metadata": {
        "type": "consciousness_update",
        "broadcast_time": "...",
        "connection_count": 3
      }
    }

    Message Format (Client → Server):
    {
      "type": "ping"
    }
    """
    await manager.connect(websocket)

    try:
        # Send initial state immediately
        from src.api.consciousness_endpoints import get_consciousness_state_endpoint
        initial_state = await get_consciousness_state_endpoint()
        initial_state_dict = initial_state.model_dump()
        initial_state_dict['_websocket_metadata'] = {
            'type': 'initial_state',
            'connection_time': datetime.now().isoformat()
        }
        await manager.send_personal_message(initial_state_dict, websocket)

        # Listen for client messages (heartbeat/ping)
        while True:
            try:
                # Wait for client message with timeout
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                message = json.loads(data)

                # Handle ping/heartbeat
                if message.get('type') == 'ping':
                    await manager.send_personal_message({
                        'type': 'pong',
                        'timestamp': datetime.now().isoformat()
                    }, websocket)
                    logger.debug("🏓 Heartbeat ping-pong")

            except asyncio.TimeoutError:
                # No message received in 30s - send ping
                await manager.send_personal_message({
                    'type': 'ping',
                    'timestamp': datetime.now().isoformat()
                }, websocket)

    except WebSocketDisconnect:
        logger.info("🔌 Client disconnected gracefully")
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"❌ WebSocket error: {e}")
        manager.disconnect(websocket)


# ============================================================================
# ROUTER REGISTRATION FUNCTION
# ============================================================================

def register_websocket_endpoints(app):
    """
    Register WebSocket endpoints with FastAPI app

    Usage in main.py:
        from websocket_endpoints import register_websocket_endpoints
        register_websocket_endpoints(app)
    """

    @app.websocket("/ws/consciousness")
    async def websocket_consciousness(websocket: WebSocket):
        await websocket_consciousness_endpoint(websocket)


# ============================================================================
# STARTUP/SHUTDOWN HANDLERS
# ============================================================================

async def start_broadcaster(interval_seconds: int = 5):
    """Start background broadcaster task"""
    task = asyncio.create_task(consciousness_state_broadcaster(interval_seconds))
    logger.info("✅ WebSocket broadcaster started")
    return task


async def stop_broadcaster(task: asyncio.Task):
    """Stop background broadcaster task"""
    if task:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        logger.info("⏹️  WebSocket broadcaster stopped")
