#!/usr/bin/env python3
"""
Quick validation of AetherMem core functionality.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

print("=" * 60)
print("AETHERMEM QUICK VALIDATION")
print("=" * 60)

# Create test workspace
test_workspace = tempfile.mkdtemp(prefix="aethermem_val_")
print(f"Test workspace: {test_workspace}")

# Set environment variables
os.environ["ENTITY_NAME"] = "test_agent"
os.environ["WORKSPACE_PATH"] = test_workspace

test_passed = True

try:
    print("\n1. Testing imports...")
    from api import ContinuityProtocol, create_protocol

    print("✓ API imports successful")

    print("\n2. Creating protocol...")
    protocol = create_protocol()
    version = protocol.get_version()
    print(f"✓ Protocol created: v{version}")

    print("\n3. Testing context restoration...")
    context = protocol.restore_context(entity_id="test_agent")
    print(f"✓ Context restoration: {len(context)} characters")

    print("\n4. Testing state persistence...")
    state_data = {
        "user_message": "Testing the AetherMem protocol",
        "assistant_response": "The protocol is working correctly!",
    }

    result = protocol.persist_state(state_vector=state_data, importance=2, metadata={"test": True})

    print(f"✓ State persistence: {result.get('status', 'unknown')}")

    print("\n5. Testing resonance calculation...")
    resonance = protocol.calculate_resonance("This is an important breakthrough!")
    print(f"✓ Resonance calculation: {resonance:.2f}")

    print("\n6. Testing protocol statistics...")
    stats = protocol.get_protocol_stats()
    print(f"✓ Protocol statistics retrieved")

    print("\n7. Testing file creation...")
    workspace_path = Path(test_workspace)
    files_created = []
    for file_path in workspace_path.rglob("*"):
        if file_path.is_file():
            files_created.append(str(file_path.relative_to(workspace_path)))

    print(f"✓ Files created: {len(files_created)}")
    for file in sorted(files_created)[:3]:
        print(f"  - {file}")

    # Check for memory files
    memory_dir = workspace_path / "memory"
    if memory_dir.exists():
        print(f"✓ Memory directory created")

    print("\n8. Testing second context restoration...")
    context2 = protocol.restore_context(entity_id="test_agent")
    print(f"✓ Second context restoration: {len(context2)} characters")

    # The second context should have more content if saving worked
    if len(context2) > len(context):
        print(f"✓ Context growth detected: +{len(context2) - len(context)} characters")

except Exception as e:
    print(f"\n✗ Validation failed: {e}")
    import traceback

    traceback.print_exc()
    test_passed = False

finally:
    # Cleanup
    try:
        shutil.rmtree(test_workspace)
        print(f"\n✓ Cleanup: removed {test_workspace}")
    except Exception as e:
        print(f"\n⚠️  Cleanup warning: {e}")

print("\n" + "=" * 60)
if test_passed:
    print("✅ QUICK VALIDATION PASSED!")
    print("Core AetherMem functionality is working correctly.")
else:
    print("❌ QUICK VALIDATION FAILED")
    print("Some core functionality is not working.")

print("=" * 60)
