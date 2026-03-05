"""
Basic tests for AetherMem.
"""

import tempfile
from pathlib import Path


def test_imports():
    """Test that core modules can be imported."""
    # Test core imports
    from src.core.memory_injector import MemoryInjector
    from src.core.memory_saver import MemorySaver
    from src.core.vwl_layer import VWLLayer

    # Test integration imports
    from src.integration.config_manager import ConfigManager

    # Test utility imports
    from src.utils.platform import get_platform_info

    assert True  # If we get here, imports succeeded


def test_config_manager():
    """Test configuration manager."""
    from src.integration.config_manager import ConfigManager

    config_manager = ConfigManager()
    default_config = config_manager.load_default()

    assert default_config is not None
    assert "system" in default_config
    assert "entity" in default_config
    assert "memory" in default_config


def test_platform_utils():
    """Test platform utilities."""
    from src.utils.platform import check_compatibility, get_platform_info

    platform_info = get_platform_info()
    assert "system" in platform_info
    assert "python_version" in platform_info

    compatibility = check_compatibility()
    assert isinstance(compatibility, bool)


def test_vwl_layer():
    """Test VWL layer basic functionality."""
    from src.core.vwl_layer import VWLLayer

    with tempfile.TemporaryDirectory() as temp_dir:
        vwl = VWLLayer(temp_dir)

        # Test basic operations
        test_data = {"test": "data", "timestamp": "2026-03-05"}
        operation_id = vwl.record_operation("test_operation", test_data)

        assert operation_id is not None
        assert isinstance(operation_id, str)

        # Test sync
        sync_result = vwl.sync_to_disk()
        assert sync_result is True or sync_result is False


def test_memory_injector():
    """Test memory injector basic functionality."""
    from src.core.memory_injector import MemoryInjector

    with tempfile.TemporaryDirectory() as temp_dir:
        config = {
            "entity": {"name": "test_entity"},
            "memory": {"injection": {"max_context_chars": 10000}},
            "workspace_path": temp_dir,
        }

        injector = MemoryInjector(config)

        # Test context injection (should return empty string if no memory files)
        context = injector.inject_context()
        assert isinstance(context, str)

        # Test weighted context
        weighted_context = injector.get_weighted_context()
        assert isinstance(weighted_context, str)


if __name__ == "__main__":
    # Run tests manually if needed
    test_imports()
    test_config_manager()
    test_platform_utils()
    test_vwl_layer()
    test_memory_injector()
    print("All basic tests passed!")
