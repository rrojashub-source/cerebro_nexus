"""
Smoke Test - CerebroAgentCoordinator with Real CEREBRO API

Session 15 Part 2C: End-to-end validation with production API.

Requirements:
- CEREBRO API running on http://localhost:8003
- PostgreSQL, Redis, Neo4j operational

Tests:
1. Agent creates episode in CEREBRO
2. Agent reads context from CEREBRO
3. Agent syncs results to CEREBRO + SharedMemory
4. Verify coordinator stats
"""

import sys
import tempfile
import shutil
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from features.nexus_crew_integration.cerebro_agent_coordinator import (
    CerebroAgentCoordinator,
    AgentEpisode,
    AgentContext
)


def test_smoke_agent_create_episode():
    """Smoke test: Agent creates episode in real CEREBRO."""
    print("\n🧪 TEST 1: Agent Create Episode")
    print("-" * 60)

    # Create temporary shared memory
    temp_dir = tempfile.mkdtemp()

    try:
        # Initialize coordinator with real CEREBRO
        coordinator = CerebroAgentCoordinator(
            cerebro_base_url="http://localhost:8003",
            shared_memory_path=temp_dir
        )

        # Agent creates episode
        result = coordinator.agent_create_episode(
            agent_name="Smoke_Test_Agent",
            content="Session 15 Part 2C smoke test - CerebroAgentCoordinator operational",
            tags=["smoke_test", "session_15", "nexus_crew_integration"],
            metadata={"test_type": "smoke", "session": 15}
        )

        print(f"✅ Episode created: {result.get('episode_id')}")
        print(f"   Success: {result.get('success')}")
        print(f"   Timestamp: {result.get('timestamp')}")

        assert result["success"] is True, "Failed to create episode"
        assert result["episode_id"] is not None, "No episode_id returned"

        return result["episode_id"]

    finally:
        shutil.rmtree(temp_dir)


def test_smoke_agent_read_context():
    """Smoke test: Agent reads context from CEREBRO."""
    print("\n🧪 TEST 2: Agent Read Context")
    print("-" * 60)

    temp_dir = tempfile.mkdtemp()

    try:
        coordinator = CerebroAgentCoordinator(
            cerebro_base_url="http://localhost:8003",
            shared_memory_path=temp_dir
        )

        # Agent reads recent episodes
        context = coordinator.agent_read_context(
            agent_name="Smoke_Test_Agent",
            limit=5,
            tag_filter="smoke_test"
        )

        print(f"✅ Context retrieved:")
        print(f"   Total episodes: {context['total_episodes']}")
        print(f"   Retrieved at: {context['retrieved_at']}")

        if context['episodes']:
            print(f"   Latest episode: {context['episodes'][0].get('content', '')[:80]}...")

        assert context["total_episodes"] >= 0, "Failed to retrieve context"

    finally:
        shutil.rmtree(temp_dir)


def test_smoke_agent_sync_results():
    """Smoke test: Agent syncs results to CEREBRO + SharedMemory."""
    print("\n🧪 TEST 3: Agent Sync Results")
    print("-" * 60)

    temp_dir = tempfile.mkdtemp()

    try:
        coordinator = CerebroAgentCoordinator(
            cerebro_base_url="http://localhost:8003",
            shared_memory_path=temp_dir
        )

        # Agent syncs task results
        agent_results = {
            "agent_name": "Smoke_Test_Agent",
            "task_type": "smoke_test_validation",
            "status": "completed",
            "result": {
                "tests_passed": 3,
                "integration_validated": True,
                "api_healthy": True
            }
        }

        result = coordinator.agent_sync_results(agent_results)

        print(f"✅ Results synced:")
        print(f"   CEREBRO synced: {result['cerebro_synced']}")
        print(f"   SharedMemory synced: {result['shared_memory_synced']}")
        print(f"   Episode ID: {result.get('episode_id')}")
        print(f"   Task ID: {result.get('task_id')}")

        assert result["cerebro_synced"] is True, "Failed to sync to CEREBRO"
        assert result["shared_memory_synced"] is True, "Failed to sync to SharedMemory"

    finally:
        shutil.rmtree(temp_dir)


def test_smoke_coordinator_stats():
    """Smoke test: Get coordinator statistics."""
    print("\n🧪 TEST 4: Coordinator Stats")
    print("-" * 60)

    temp_dir = tempfile.mkdtemp()

    try:
        coordinator = CerebroAgentCoordinator(
            cerebro_base_url="http://localhost:8003",
            shared_memory_path=temp_dir
        )

        stats = coordinator.get_coordinator_stats()

        print(f"✅ Coordinator stats:")
        print(f"   CEREBRO healthy: {stats['cerebro_healthy']}")
        print(f"   CEREBRO URL: {stats['cerebro_url']}")
        print(f"   Total agent tasks: {stats['total_agent_tasks']}")
        print(f"   Tasks by status: {stats['tasks_by_status']}")

        assert stats["cerebro_healthy"] is True, "CEREBRO not healthy"

    finally:
        shutil.rmtree(temp_dir)


def run_smoke_tests():
    """Run all smoke tests sequentially."""
    print("\n" + "=" * 60)
    print("🔥 SMOKE TEST - CerebroAgentCoordinator + Real CEREBRO API")
    print("=" * 60)

    try:
        # Test 1: Create episode
        episode_id = test_smoke_agent_create_episode()

        # Test 2: Read context
        test_smoke_agent_read_context()

        # Test 3: Sync results
        test_smoke_agent_sync_results()

        # Test 4: Stats
        test_smoke_coordinator_stats()

        print("\n" + "=" * 60)
        print("✅ ALL SMOKE TESTS PASSED")
        print("=" * 60)
        print("\n📊 Summary:")
        print("   - Agent episode creation: ✅")
        print("   - Agent context retrieval: ✅")
        print("   - Bidirectional sync: ✅")
        print("   - Coordinator stats: ✅")
        print("\n🎯 CerebroAgentCoordinator is OPERATIONAL with production CEREBRO API")

        return True

    except Exception as e:
        print(f"\n❌ SMOKE TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_smoke_tests()
    sys.exit(0 if success else 1)
