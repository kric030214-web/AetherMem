"""
AetherMem - Memory Continuity Protocol for AI Agents
Copyright (C) 2026 kric030214-web

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from pathlib import Path
from typing import Optional

from ..core.memory_injector import MemoryInjector
from ..core.memory_saver import MemorySaver
from ..core.vwl_layer import VWLLayer, VWLManager
from ..resonance.interaction_metrics import InteractionMetrics, TimeSeriesAnalyzer
from ..resonance.temporal_decay import AdaptiveDecay, TemporalDecay
from ..utils.platform import (
    check_compatibility,
    get_default_config_dir,
    get_default_temp_dir,
    get_default_workspace_dir,
    get_platform_info,
    get_platform_name,
    is_linux,
    is_macos,
    is_windows,
    normalize_path,
    platform_info,
    validate_platform_compatibility,
)

__version__ = "1.0.0"
__author__ = "AetherMem Authors"
__license__ = "MIT"


class ContinuityProtocol:
    """Unified continuity protocol interface."""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize the continuity protocol.

        Args:
            config_path: Path to configuration file. If None, uses default configuration.
        """
        self.config_path = config_path
        self._vwl_manager: Optional[VWLManager] = None
        self._injector: Optional[MemoryInjector] = None
        self._saver: Optional[MemorySaver] = None
        self._temporal_decay: Optional[TemporalDecay] = None
        self._interaction_metrics: Optional[InteractionMetrics] = None

    def restore_context(self, entity_id: str = "default") -> str:
        """
        Restore context across session boundary.

        Args:
            entity_id: Identifier of the entity

        Returns:
            Restored context as string
        """
        if self._injector is None:
            self._initialize_components()

        return self._injector.inject_context(entity_id=entity_id)

    def persist_state(
        self, state_vector: dict, importance: Optional[int] = None, metadata: Optional[dict] = None
    ) -> dict:
        """
        Persist state with weighted indexing.

        Args:
            state_vector: State data to persist
            importance: Optional importance level (1-3)
            metadata: Optional state metadata

        Returns:
            Persistence result dictionary
        """
        if self._saver is None:
            self._initialize_components()

        # Convert state_vector to conversation format for compatibility
        user_message = state_vector.get("user_message", "")
        assistant_response = state_vector.get("assistant_response", "")

        return self._saver.save_conversation(user_message, assistant_response, importance, metadata)

    def get_weighted_context(self, entity_id: str = "default", max_bytes: int = 20000) -> str:
        """
        Retrieve resonance-weighted context.

        Args:
            entity_id: Entity identifier
            max_bytes: Maximum context size in bytes

        Returns:
            Weighted context string
        """
        if self._injector is None:
            self._initialize_components()

        # Note: entity_id parameter is currently not used in the implementation
        # but kept for API compatibility
        return self._injector.get_weighted_context(max_bytes)

    def calculate_resonance(self, content: str, entity_id: str = "default") -> float:
        """
        Calculate resonance score for content.

        Args:
            content: Content to analyze
            entity_id: Entity identifier

        Returns:
            Resonance score (0-1)
        """
        if self._saver is None:
            self._initialize_components()

        # Simple resonance calculation based on keyword matching
        # This is a placeholder - in production, this would use the full
        # emotional tracking system from MemorySaver

        # Define emotional keywords and their weights
        emotional_keywords = {
            "love": 0.8,
            "care": 0.7,
            "miss": 0.6,
            "happy": 0.5,
            "sad": 0.6,
            "excited": 0.5,
            "proud": 0.6,
            "grateful": 0.7,
            "appreciate": 0.6,
            "cherish": 0.7,
            "adore": 0.8,
            "breakthrough": 0.9,
            "achievement": 0.8,
            "success": 0.7,
            "milestone": 0.8,
            "historical": 0.9,
            "important": 0.7,
            "critical": 0.9,
            "significant": 0.6,
        }

        # Calculate resonance score
        content_lower = content.lower()
        total_score = 0.0
        keyword_count = 0

        for keyword, weight in emotional_keywords.items():
            if keyword in content_lower:
                total_score += weight
                keyword_count += 1

        # Normalize score
        if keyword_count > 0:
            resonance = total_score / keyword_count
            # Cap at 1.0
            resonance = min(1.0, resonance)
        else:
            resonance = 0.1  # Baseline resonance for neutral content

        return resonance

    def get_protocol_stats(self) -> dict:
        """
        Get protocol statistics.

        Returns:
            Dictionary with protocol statistics
        """
        stats = {
            "version": __version__,
            "components_initialized": {
                "vwl_manager": self._vwl_manager is not None,
                "injector": self._injector is not None,
                "saver": self._saver is not None,
                "temporal_decay": self._temporal_decay is not None,
                "interaction_metrics": self._interaction_metrics is not None,
            },
        }

        if self._vwl_manager:
            stats["vwl_stats"] = self._vwl_manager.get_all_stats()

        if self._interaction_metrics:
            stats["interaction_stats"] = self._interaction_metrics.get_all_stats()

        return stats

    def _initialize_components(self) -> None:
        """Initialize all protocol components."""
        # Try relative import first, then absolute
        try:
            from ..integration.config_manager import ConfigManager
        except ImportError:
            # Fall back to absolute import for testing
            import sys
            from pathlib import Path

            sys.path.insert(0, str(Path(__file__).parent.parent))
            from integration.config_manager import ConfigManager

        config_manager = ConfigManager()
        config = config_manager.load_default()

        self._vwl_manager = VWLManager(config)
        self._injector = MemoryInjector(config)
        self._saver = MemorySaver(config)
        self._temporal_decay = TemporalDecay(decay_rate=0.1)
        self._interaction_metrics = InteractionMetrics(window_days=30)


# Convenience functions
def create_protocol(config_path: Optional[Path] = None) -> ContinuityProtocol:
    """
    Create a new continuity protocol instance.

    Args:
        config_path: Optional path to configuration file

    Returns:
        ContinuityProtocol instance
    """
    return ContinuityProtocol(config_path)


def get_version() -> str:
    """Get the current AetherMem version."""
    return __version__


# Protocol exports
__all__ = [
    # Main protocol
    "ContinuityProtocol",
    "create_protocol",
    "get_version",
    # Core components
    "VWLLayer",
    "VWLManager",
    "MemoryInjector",
    "MemorySaver",
    # Resonance components
    "TemporalDecay",
    "AdaptiveDecay",
    "InteractionMetrics",
    "TimeSeriesAnalyzer",
    # Platform utilities
    "get_platform_info",
    "get_default_temp_dir",
    "get_default_config_dir",
    "get_default_workspace_dir",
    "normalize_path",
    "is_windows",
    "is_macos",
    "is_linux",
    "get_platform_name",
    "validate_platform_compatibility",
    "platform_info",
    "check_compatibility",
    # Integration
    "ConfigManager",
]
