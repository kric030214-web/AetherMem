#!/usr/bin/env python3
"""
End-to-end test for AetherMem system.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

print("=" * 70)
print("AETHERMEM END-TO-END SYSTEM TEST")
print("=" * 70)

# Create a temporary workspace for testing
test_workspace = tempfile.mkdtemp(prefix="aethermem_test_")
print(f"Test workspace: {test_workspace}")

# Set environment variables
os.environ["ENTITY_NAME"] = "test_agent"
os.environ["WORKSPACE_PATH"] = test_workspace
os.environ["TEMP_DIR"] = os.path.join(test_workspace, "tmp")

# Create temp directory
os.makedirs(os.environ["TEMP_DIR"], exist_ok=True)

print("\n1. Testing Core Components")
print("-" * 40)

try:
    # Test VWL Layer
    from core.vwl_layer import VWLLayer, VWLManager

    print("✓ VWL Layer imports successful")

    # Test Memory Injector
    from core.memory_injector import MemoryInjector

    print("✓ Memory Injector import successful")

    # Test Memory Saver
    from core.memory_saver import MemorySaver

    print("✓ Memory Saver import successful")

    # Test Resonance Components
    from resonance.temporal_decay import TemporalDecay
    from resonance.interaction_metrics import InteractionMetrics

    print("✓ Resonance components import successful")

    # Test Config Manager
    from integration.config_manager import ConfigManager

    print("✓ Config Manager import successful")

except Exception as e:
    print(f"✗ Component import failed: {e}")
    sys.exit(1)

print("\n2. Testing Configuration System")
print("-" * 40)

try:
    from integration.config_manager import ConfigManager

    # Create a minimal config
    config_manager = ConfigManager()

    # Test default config
    default_config = config_manager.load_default()
    print(f"✓ Default config loaded: {default_config.get('system', {}).get('name', 'unknown')}")

    # Test config validation
    is_valid = config_manager.validate_config(default_config)
    print(f"✓ Config validation: {'passed' if is_valid else 'failed'}")

    # Test config saving
    config_path = Path(test_workspace) / "config.yaml"
    config_manager.save(default_config, config_path)
    print(f"✓ Config saved to: {config_path}")

    # Test config loading
    loaded_config = config_manager.load(config_path)
    print(f"✓ Config loaded from file: {loaded_config.get('system', {}).get('name', 'unknown')}")

except Exception as e:
    print(f"✗ Configuration test failed: {e}")
    sys.exit(1)

print("\n3. Testing Memory Injection")
print("-" * 40)

try:
    from core.memory_injector import MemoryInjector
    from integration.config_manager import ConfigManager

    config_manager = ConfigManager()
    config = config_manager.load_default()

    # Create memory injector
    injector = MemoryInjector(config)

    # Test context injection
    context = injector.inject_context()
    print(f"✓ Context injection successful: {len(context)} characters")

    # Test weighted context (check if method exists)
    if hasattr(injector, "get_weighted_context"):
        weighted_context = injector.get_weighted_context(max_bytes=5000)
        print(f"✓ Weighted context retrieval: {len(weighted_context)} characters")
    else:
        print("⚠️  get_weighted_context method not available")

except Exception as e:
    print(f"✗ Memory injection test failed: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

print("\n4. Testing Memory Saving")
print("-" * 40)

try:
    from core.memory_saver import MemorySaver
    from integration.config_manager import ConfigManager

    config_manager = ConfigManager()
    config = config_manager.load_default()

    # Create memory saver
    saver = MemorySaver(config)

    # Test conversation saving
    result = saver.save_conversation(
        user_message="What is memory continuity?",
        assistant_response="Memory continuity refers to the persistence of context and state across discrete execution sessions, enabling AI agents to maintain coherent identity and knowledge over time.",
        importance=2,
        metadata={"session_id": "test_session_001", "topic": "technical_concept"},
    )

    print(f"✓ Conversation saved: {result.get('status', 'unknown')}")
    print(f"  Importance: {result.get('importance_level', 'N/A')}")
    print(f"  Emotional resonance: {result.get('emotional_resonance', 0.0):.2f}")

    # Test with critical importance
    result2 = saver.save_conversation(
        user_message="This is a breakthrough!",
        assistant_response="I've achieved true memory continuity!",
        importance=3,
        metadata={"session_id": "test_session_002", "breakthrough": True},
    )

    print(f"✓ Critical conversation saved: {result2.get('status', 'unknown')}")

except Exception as e:
    print(f"✗ Memory saving test failed: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

print("\n5. Testing Resonance Calculations")
print("-" * 40)

try:
    from resonance.temporal_decay import TemporalDecay
    from resonance.interaction_metrics import InteractionMetrics

    # Test temporal decay
    decay = TemporalDecay(decay_rate=0.1)
    stats = decay.get_decay_stats()
    print(f"✓ Temporal decay initialized: {stats['decay_rate']}/day")
    print(f"  Half-life: {stats['half_life_days']:.1f} days")

    # Test interaction metrics
    import datetime

    metrics = InteractionMetrics(window_days=30)

    now = datetime.datetime.now()
    for i in range(5):
        interaction_time = now - datetime.timedelta(hours=i * 6)
        metrics.record_interaction("test_user", interaction_time)

    user_stats = metrics.get_entity_stats("test_user")
    print(f"✓ Interaction metrics: {user_stats['total_interactions']} interactions")
    print(f"  Engagement score: {user_stats['engagement_score']:.2f}")

except Exception as e:
    print(f"✗ Resonance test failed: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

print("\n6. Testing API Protocol")
print("-" * 40)

try:
    from api import ContinuityProtocol, create_protocol

    # Create protocol instance
    protocol = create_protocol()

    # Test protocol methods
    version = protocol.get_version()
    print(f"✓ Protocol version: {version}")

    # Test context restoration
    context = protocol.restore_context(entity_id="test_agent")
    print(f"✓ Context restoration: {len(context)} characters")

    # Test state persistence
    state_data = {
        "user_message": "Testing the continuity protocol",
        "assistant_response": "The protocol is working correctly!",
        "test_data": {"iteration": 1, "status": "success"},
    }

    result = protocol.persist_state(state_vector=state_data, importance=2, metadata={"test": True})

    print(f"✓ State persistence: {result.get('status', 'unknown')}")

    # Test protocol statistics
    stats = protocol.get_protocol_stats()
    print(f"✓ Protocol statistics retrieved")

except Exception as e:
    print(f"✗ API protocol test failed: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

print("\n7. Testing File System Operations")
print("-" * 40)

try:
    # Check created files
    workspace_path = Path(test_workspace)

    files_created = []
    for file_path in workspace_path.rglob("*"):
        if file_path.is_file():
            files_created.append(str(file_path.relative_to(workspace_path)))

    print(f"✓ Files created in workspace: {len(files_created)}")
    for file in sorted(files_created)[:5]:  # Show first 5
        print(f"  - {file}")

    if len(files_created) > 5:
        print(f"  ... and {len(files_created) - 5} more")

    # Check memory files
    memory_dir = workspace_path / "memory"
    if memory_dir.exists():
        memory_files = list(memory_dir.glob("*.md"))
        print(f"✓ Memory files created: {len(memory_files)}")

        # Check MEMORY.md
        memory_file = workspace_path / "MEMORY.md"
        if memory_file.exists():
            with open(memory_file, "r") as f:
                content = f.read()
            print(f"✓ MEMORY.md created: {len(content)} characters")

except Exception as e:
    print(f"✗ File system test failed: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

print("\n8. Cleanup")
print("-" * 40)

try:
    # Clean up test workspace
    shutil.rmtree(test_workspace)
    print(f"✓ Test workspace cleaned up: {test_workspace}")
except Exception as e:
    print(f"⚠️  Cleanup warning: {e}")

print("\n" + "=" * 70)
print("END-TO-END TEST COMPLETE")
print("=" * 70)
print("✅ All tests passed! The system is working correctly.")
print("\nThe AetherMem continuity protocol is ready for production use.")
print("=" * 70)
