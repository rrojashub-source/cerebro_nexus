"""
LAB_011: Working Memory Buffer - Test Suite

Validate working memory buffer capacity, eviction, rehearsal, and decay.

Author: NEXUS (Autonomous)
Date: October 28, 2025
"""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent.parent / 'implementation'))

from working_memory_buffer import (
    WorkingMemoryBuffer,
    WorkingMemoryItem,
    EvictionStrategy,
    RehearsalManager,
    BufferManager
)


def test_working_memory_system():
    """Test complete working memory system"""

    print("=" * 70)
    print("LAB_011: Working Memory Buffer - Test Suite")
    print("=" * 70)
    print()

    # ========================================================================
    # TEST 1: Capacity Limit
    # ========================================================================

    print("TEST 1: Capacity Limit (Miller's Law: 7 items)")
    print("-" * 70)

    buffer = WorkingMemoryBuffer(capacity=7)

    # Add 10 items (should only keep 7)
    for i in range(10):
        added = buffer.add(f"episode_{i:02d}", attention_weight=0.5 + i*0.05)
        print(f"  Added episode_{i:02d}: {added} (buffer size: {buffer.size()})")

    print()
    print(f"Final buffer size: {buffer.size()} / {buffer.capacity}")
    print(f"Buffer full: {buffer.is_full()}")
    print()

    # ========================================================================
    # TEST 2: Fast Access
    # ========================================================================

    print()
    print("TEST 2: Fast Access (O(1) lookup)")
    print("-" * 70)

    # Measure access time
    start = time.perf_counter()
    item = buffer.get("episode_05")
    end = time.perf_counter()

    access_time_ms = (end - start) * 1000

    print(f"Access time: {access_time_ms:.4f} ms")
    print(f"Item found: {item is not None}")
    if item:
        print(f"  Episode ID: {item.episode_id}")
        print(f"  Attention: {item.attention_weight:.3f}")
        print(f"  Access count: {item.access_count}")
    print()

    # ========================================================================
    # TEST 3: Eviction Policies
    # ========================================================================

    print()
    print("TEST 3: Eviction Policies (LRU, Attention, Hybrid)")
    print("-" * 70)

    # Test LRU eviction
    print("  [A] LRU Eviction")
    lru_buffer = WorkingMemoryBuffer(capacity=3, eviction_strategy=EvictionStrategy.LRU)
    lru_buffer.add("old", attention_weight=0.9)
    time.sleep(0.01)
    lru_buffer.add("middle", attention_weight=0.5)
    time.sleep(0.01)
    lru_buffer.add("new", attention_weight=0.3)

    # Access "old" to make it recent
    lru_buffer.get("old")

    # Add one more (should evict "middle", the LRU)
    lru_buffer.add("newest", attention_weight=0.4)

    in_buffer = lru_buffer.get_episode_ids()
    print(f"    Buffered: {in_buffer}")
    print(f"    'middle' evicted (LRU): {'middle' not in in_buffer}")
    print()

    # Test Attention eviction
    print("  [B] Attention-Based Eviction")
    att_buffer = WorkingMemoryBuffer(capacity=3, eviction_strategy=EvictionStrategy.ATTENTION)
    att_buffer.add("high_att", attention_weight=0.9)
    att_buffer.add("medium_att", attention_weight=0.5)
    att_buffer.add("low_att", attention_weight=0.2)

    # Add one more with medium attention (should evict "low_att")
    att_buffer.add("new_medium", attention_weight=0.6)

    in_buffer = att_buffer.get_episode_ids()
    print(f"    Buffered: {in_buffer}")
    print(f"    'low_att' evicted (lowest attention): {'low_att' not in in_buffer}")
    print()

    # Test Hybrid eviction
    print("  [C] Hybrid Eviction (LRU + Attention)")
    hyb_buffer = WorkingMemoryBuffer(capacity=3, eviction_strategy=EvictionStrategy.HYBRID)
    hyb_buffer.add("old_low", attention_weight=0.3)
    time.sleep(0.01)
    hyb_buffer.add("new_high", attention_weight=0.9)
    time.sleep(0.01)
    hyb_buffer.add("new_medium", attention_weight=0.6)

    # Add one more (should evict "old_low": old + low attention)
    hyb_buffer.add("newest", attention_weight=0.7)

    in_buffer = hyb_buffer.get_episode_ids()
    print(f"    Buffered: {in_buffer}")
    print(f"    'old_low' evicted (old + low attention): {'old_low' not in in_buffer}")
    print()

    # ========================================================================
    # TEST 4: Rehearsal
    # ========================================================================

    print()
    print("TEST 4: Rehearsal (Keep Important Items Alive)")
    print("-" * 70)

    rehearsal_buffer = WorkingMemoryBuffer(capacity=5)
    rehearsal_manager = RehearsalManager(attention_threshold=0.7)

    # Add items with varying attention
    rehearsal_buffer.add("high_att_1", attention_weight=0.9, tags=["important"])
    rehearsal_buffer.add("high_att_2", attention_weight=0.8, tags=["important"])
    rehearsal_buffer.add("low_att_1", attention_weight=0.4, tags=["noise"])
    rehearsal_buffer.add("low_att_2", attention_weight=0.3, tags=["noise"])

    print(f"  Initial buffer: {rehearsal_buffer.get_episode_ids()}")
    print()

    # Rehearse high-attention items
    rehearsed = rehearsal_manager.rehearse_buffer(
        rehearsal_buffer,
        task_tags=["important"]
    )

    print(f"  Rehearsed items: {rehearsed}")
    print()

    # Check rehearsal counts
    for episode_id in rehearsal_buffer.get_episode_ids():
        item = rehearsal_buffer.get(episode_id)
        print(f"    {episode_id}: rehearsal_count={item.rehearsal_count}")

    print()

    # ========================================================================
    # TEST 5: Temporal Decay
    # ========================================================================

    print()
    print("TEST 5: Temporal Decay (Remove Stale Items)")
    print("-" * 70)

    decay_buffer = WorkingMemoryBuffer(capacity=5, decay_threshold_seconds=0.05)  # 50ms

    # Add items
    decay_buffer.add("fresh_1", attention_weight=0.8)
    decay_buffer.add("fresh_2", attention_weight=0.7)
    decay_buffer.add("stale_1", attention_weight=0.6)
    decay_buffer.add("stale_2", attention_weight=0.5)

    print(f"  Initial buffer: {decay_buffer.get_episode_ids()}")
    print()

    # Wait for decay threshold
    time.sleep(0.06)

    # Refresh some items (prevent decay)
    decay_buffer.refresh("fresh_1")
    decay_buffer.refresh("fresh_2")

    # Decay step (should remove stale items)
    evicted = decay_buffer.decay_step()

    print(f"  After decay:")
    print(f"    Evicted: {evicted}")
    print(f"    Remaining: {decay_buffer.get_episode_ids()}")
    print()

    # ========================================================================
    # TEST 6: Buffer Manager Integration
    # ========================================================================

    print()
    print("TEST 6: Buffer Manager (Full System)")
    print("-" * 70)

    manager = BufferManager(capacity=7)

    # Simulate attention mechanism output (LAB_010)
    attended_episodes = [
        ("LAB_010_attention", 0.9),
        ("LAB_011_working_memory", 0.85),
        ("LAB_009_reconsolidation", 0.7),
        ("LAB_005_spreading", 0.6),
        ("current_task", 0.8),
    ]

    # Update buffer from attention
    manager.update_from_attention(attended_episodes)

    print(f"  Active context: {manager.get_active_context()}")
    print()

    # Maintenance step (decay + rehearsal)
    manager.maintenance_step(task_tags=["LAB", "working_memory"])

    # Stats
    stats = manager.get_stats()
    print(f"  Buffer Statistics:")
    print(f"    Size: {stats['buffer']['size']} / {stats['buffer']['capacity']}")
    print(f"    Utilization: {stats['buffer']['utilization']:.1%}")
    print(f"    Avg attention: {stats['buffer']['avg_attention']:.3f}")
    print()

    print(f"  Buffer Contents:")
    for item in stats['contents'][:5]:  # Top 5
        print(f"    {item['episode_id']:<30} att={item['attention']:.2f} age={item['age_seconds']:.2f}s")

    print()

    # ========================================================================
    # Success Criteria
    # ========================================================================

    print("=" * 70)
    print("Success Criteria")
    print("=" * 70)
    print()

    checks = [
        ("Capacity limit respected", buffer.size() <= buffer.capacity, True),
        ("Fast access (<1ms)", access_time_ms < 1.0, True),
        ("LRU eviction works", 'middle' not in lru_buffer.get_episode_ids(), True),
        ("Attention eviction works", 'low_att' not in att_buffer.get_episode_ids(), True),
        ("Hybrid eviction works", 'old_low' not in hyb_buffer.get_episode_ids(), True),
        ("Rehearsal works", len(rehearsed) > 0, True),
        ("Temporal decay works", len(evicted) > 0, True),
        ("Buffer manager integrates", len(manager.get_active_context()) > 0, True),
    ]

    all_pass = True
    for criterion, result, expected in checks:
        passed = result == expected
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}  {criterion:<40} ({result})")
        if not passed:
            all_pass = False

    print()
    if all_pass:
        print("🎉 ALL TESTS PASSED - Working memory buffer operational!")
    else:
        print("⚠️  Some tests failed - Needs debugging")

    print()


if __name__ == "__main__":
    test_working_memory_system()
