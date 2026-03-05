#!/usr/bin/env python3
"""
Test all AetherMem imports to ensure package structure is correct.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("Testing AetherMem imports...")
print("=" * 50)

# Test core imports
try:
    from aethermem.core.vwl_layer import VWLLayer, VWLManager

    print("✓ Core VWL layer imports successful")
except ImportError as e:
    print(f"✗ Core VWL layer import failed: {e}")

try:
    from aethermem.core.memory_injector import MemoryInjector

    print("✓ Memory injector import successful")
except ImportError as e:
    print(f"✗ Memory injector import failed: {e}")

try:
    from aethermem.core.memory_saver import MemorySaver

    print("✓ Memory saver import successful")
except ImportError as e:
    print(f"✗ Memory saver import failed: {e}")

# Test resonance imports
try:
    from aethermem.resonance.temporal_decay import TemporalDecay, AdaptiveDecay

    print("✓ Temporal decay imports successful")
except ImportError as e:
    print(f"✗ Temporal decay imports failed: {e}")

try:
    from aethermem.resonance.interaction_metrics import InteractionMetrics, TimeSeriesAnalyzer

    print("✓ Interaction metrics imports successful")
except ImportError as e:
    print(f"✗ Interaction metrics imports failed: {e}")

# Test integration imports
try:
    from aethermem.integration.config_manager import ConfigManager

    print("✓ Config manager import successful")
except ImportError as e:
    print(f"✗ Config manager import failed: {e}")

try:
    from aethermem.integration.openclaw import OpenClawAdapter, register_skill

    print("✓ OpenClaw integration imports successful")
except ImportError as e:
    print(f"✗ OpenClaw integration imports failed: {e}")

# Test API imports
try:
    from aethermem.api import ContinuityProtocol, create_protocol, get_version

    print("✓ API imports successful")

    # Test version
    version = get_version()
    print(f"  Version: {version}")

    # Test protocol creation
    protocol = create_protocol()
    print("  Protocol creation successful")

    # Test protocol methods
    stats = protocol.get_protocol_stats()
    print(f"  Protocol stats: {stats.get('version', 'unknown')}")

except ImportError as e:
    print(f"✗ API imports failed: {e}")
except Exception as e:
    print(f"✗ API test failed: {e}")

print("=" * 50)
print("Import test completed.")
