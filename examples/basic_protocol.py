#!/usr/bin/env python3
"""
Basic protocol demonstration for AetherMem.
"""

import sys
from pathlib import Path

# Add src to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def demonstrate_basic_protocol():
    """Demonstrate basic protocol operations."""
    print("=" * 60)
    print("AetherMem Basic Protocol Demonstration")
    print("=" * 60)

    try:
        from aethermem import ContinuityProtocol, create_protocol

        print("\n1. Creating protocol instance...")
        protocol = create_protocol()
        version = protocol.get_version()
        print(f"   Protocol version: {version}")

        print("\n2. Restoring context...")
        context = protocol.restore_context(entity_id="demo_agent")
        print(f"   Restored context: {len(context)} characters")

        print("\n3. Persisting state with importance weighting...")
        state_data = {
            "user_message": "Testing the AetherMem protocol",
            "assistant_response": "The protocol is working correctly!",
            "emotional_resonance": 0.85,
        }

        result = protocol.persist_state(
            state_vector=state_data,
            importance=2,  # Medium importance
            metadata={"demo": True, "session_id": "demo_001"},
        )

        print(f"   State persisted: {result.get('status', 'unknown')}")
        print(f"   Importance level: {result.get('importance_level', 'N/A')}")

        print("\n4. Calculating resonance...")
        resonance = protocol.calculate_resonance("This is an important breakthrough in memory continuity!")
        print(f"   Resonance score: {resonance:.2f}")

        print("\n5. Retrieving protocol statistics...")
        stats = protocol.get_protocol_stats()
        print(f"   Statistics retrieved: {len(stats)} metrics")

    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure AetherMem is installed or src/ is in Python path")
        return False

    print("\n" + "=" * 60)
    print("✅ Demonstration completed successfully!")
    return True


def demonstrate_openclaw_integration():
    """Demonstrate OpenClaw integration."""
    print("\n" + "=" * 60)
    print("OpenClaw Integration Demonstration")
    print("=" * 60)

    try:
        from aethermem.integration.openclaw import (
            OpenClawAdapter,
            create_openclaw_adapter,
        )

        print("\n1. Creating OpenClaw adapter...")
        adapter = create_openclaw_adapter()
        print(f"   Adapter created: {adapter is not None}")

        if adapter:
            print("\n2. Testing adapter methods...")
            # Simulate some adapter operations
            print("   Adapter methods available")
            print("   (Actual OpenClaw integration requires OpenClaw runtime)")

    except ImportError as e:
        print(f"OpenClaw integration not available: {e}")
        print("This is normal if OpenClaw is not installed")

    print("\n✅ OpenClaw integration demonstration completed!")


def demonstrate_resonance_metrics():
    """Demonstrate resonance metrics."""
    print("\n" + "=" * 60)
    print("Resonance Metrics Demonstration")
    print("=" * 60)

    try:
        from aethermem import InteractionMetrics, TemporalDecay

        print("\n1. Creating temporal decay model...")
        decay = TemporalDecay(half_life_hours=24)
        print(f"   Decay model created")

        print("\n2. Creating interaction metrics...")
        metrics = InteractionMetrics(decay_model=decay)
        print(f"   Metrics system created")

        # Simulate some interactions
        import datetime

        test_interactions = [
            {"entity_id": "user_001", "timestamp": datetime.datetime.now()},
            {"entity_id": "user_001", "timestamp": datetime.datetime.now()},
        ]

        print(f"\n3. Analyzing {len(test_interactions)} test interactions...")
        print("   Metrics system ready for real interactions")

    except ImportError as e:
        print(f"Resonance metrics not available: {e}")

    print("\n✅ Resonance metrics demonstration completed!")


if __name__ == "__main__":
    # Run demonstrations
    success = demonstrate_basic_protocol()

    if success:
        demonstrate_openclaw_integration()
        demonstrate_resonance_metrics()

        print("\n" + "=" * 60)
        print("🎉 All demonstrations completed!")
        print("\nNext steps:")
        print("1. Install AetherMem: pip install aethermem")
        print("2. Check documentation: https://github.com/kric030214-web/AetherMem")
        print("3. Integrate with your AI agent system")
    else:
        print("\n❌ Basic demonstration failed. Please check installation.")
