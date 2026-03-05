#!/usr/bin/env python3
"""
Test AetherMem imports directly from source files.
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

print("Testing AetherMem direct imports...")
print("=" * 50)

# Test direct imports using module paths
test_cases = [
    ("core.vwl_layer", ["VWLLayer", "VWLManager"]),
    ("core.memory_injector", ["MemoryInjector"]),
    ("core.memory_saver", ["MemorySaver"]),
    ("resonance.temporal_decay", ["TemporalDecay", "AdaptiveDecay"]),
    ("resonance.interaction_metrics", ["InteractionMetrics", "TimeSeriesAnalyzer"]),
    ("integration.config_manager", ["ConfigManager"]),
    ("integration.openclaw.adapter", ["OpenClawAdapter", "create_openclaw_adapter"]),
    ("integration.openclaw.skill_registry", ["register_skill", "install_skill"]),
    ("api", ["ContinuityProtocol", "create_protocol", "get_version"]),
]

all_passed = True

for module_path, expected_classes in test_cases:
    try:
        # Import the module
        module = __import__(module_path, fromlist=expected_classes)

        # Check each expected class
        for class_name in expected_classes:
            if hasattr(module, class_name):
                print(f"✓ {module_path}.{class_name} import successful")
            else:
                print(f"✗ {module_path}.{class_name} not found in module")
                all_passed = False

    except ImportError as e:
        print(f"✗ Failed to import {module_path}: {e}")
        all_passed = False
    except Exception as e:
        print(f"✗ Error importing {module_path}: {e}")
        all_passed = False

print("=" * 50)

# Test API functionality
if all_passed:
    print("Testing API functionality...")
    try:
        from api import create_protocol, get_version

        version = get_version()
        print(f"✓ Version check: {version}")

        protocol = create_protocol()
        print("✓ Protocol creation successful")

        stats = protocol.get_protocol_stats()
        print(f"✓ Protocol stats retrieved: {stats.get('version', 'unknown')}")

        print("=" * 50)
        print("All tests passed! ✅")

    except Exception as e:
        print(f"✗ API functionality test failed: {e}")
        all_passed = False
else:
    print("Some imports failed, skipping API functionality test.")

if not all_passed:
    print("Some tests failed. ❌")
    sys.exit(1)
