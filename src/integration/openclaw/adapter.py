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

import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

# Try relative import first, then absolute
try:
    from ...api import ContinuityProtocol
except ImportError:
    # Fall back to absolute import for testing
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from api import ContinuityProtocol

logger = logging.getLogger(__name__)


class OpenClawAdapter:
    """Adapter for integrating AetherMem with OpenClaw runtime."""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize OpenClaw adapter.

        Args:
            config_path: Optional path to configuration file
        """
        self.config_path = config_path
        self.protocol: Optional[ContinuityProtocol] = None
        self.workspace_path: Optional[Path] = None

    def initialize(self) -> bool:
        """
        Initialize adapter with OpenClaw runtime environment.

        Returns:
            True if initialization successful
        """
        try:
            # Detect OpenClaw workspace
            self.workspace_path = self._detect_workspace()
            if not self.workspace_path:
                logger.warning("OpenClaw workspace not detected")
                return False

            # Load configuration
            config = self._load_configuration()

            # Initialize continuity protocol
            self.protocol = ContinuityProtocol(config_path=self.config_path)

            logger.info(f"OpenClaw adapter initialized for workspace: {self.workspace_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize OpenClaw adapter: {e}")
            return False

    def _detect_workspace(self) -> Optional[Path]:
        """
        Detect OpenClaw workspace path.

        Returns:
            Path to workspace or None if not found
        """
        # Check environment variable first
        env_path = os.getenv("OPENCLAW_WORKSPACE")
        if env_path:
            path = Path(env_path)
            if path.exists():
                return path

        # Check common locations
        common_paths = [
            Path.home() / ".openclaw" / "workspace",
            Path("/opt/openclaw/workspace"),
            Path.cwd() / "openclaw-workspace",
        ]

        for path in common_paths:
            if path.exists():
                return path

        return None

    def _load_configuration(self) -> Dict[str, Any]:
        """
        Load configuration for OpenClaw integration.

        Returns:
            Configuration dictionary
        """
        # Default configuration for OpenClaw
        config = {
            "protocol": {
                "version": "1.0",
                "environment": "production",
            },
            "vwl": {
                "enabled": True,
                "sync_interval": 300,
                "max_virtual_size": 1048576,
                "consistency": "eventual",
            },
            "resonance": {
                "decay_rate": 0.1,
                "weight_factors": {
                    "importance": 0.4,
                    "recency": 0.3,
                    "frequency": 0.3,
                },
            },
            "integration": {
                "openclaw": {
                    "runtime_path": str(self.workspace_path),
                    "auto_register": True,
                },
            },
        }

        # Merge with user configuration if provided
        if self.config_path and self.config_path.exists():
            import yaml

            with open(self.config_path, "r") as f:
                user_config = yaml.safe_load(f)
                self._merge_configs(config, user_config)

        return config

    def _merge_configs(self, base: Dict[str, Any], override: Dict[str, Any]) -> None:
        """
        Recursively merge configuration dictionaries.

        Args:
            base: Base configuration dictionary
            override: Override configuration dictionary
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_configs(base[key], value)
            else:
                base[key] = value

    def inject_session_context(self, entity_id: str = "openclaw_agent") -> str:
        """
        Inject context at session start.

        Args:
            entity_id: Entity identifier

        Returns:
            Injected context as string
        """
        if not self.protocol:
            raise RuntimeError("Adapter not initialized")

        context = self.protocol.restore_context(entity_id=entity_id)
        logger.info(f"Injected {len(context)} bytes of context for entity: {entity_id}")
        return context

    def persist_conversation(
        self,
        user_message: str,
        assistant_response: str,
        importance: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Persist conversation with OpenClaw-specific metadata.

        Args:
            user_message: User message
            assistant_response: Assistant response
            importance: Optional importance level
            metadata: Optional conversation metadata

        Returns:
            Persistence result
        """
        if not self.protocol:
            raise RuntimeError("Adapter not initialized")

        # Add OpenClaw-specific metadata
        openclaw_metadata = {
            "runtime": "openclaw",
            "workspace": str(self.workspace_path),
            "timestamp": self._get_timestamp(),
        }

        if metadata:
            openclaw_metadata.update(metadata)

        result = self.protocol.persist_state(
            state_vector={
                "user_message": user_message,
                "assistant_response": assistant_response,
            },
            importance=importance,
            metadata=openclaw_metadata,
        )

        logger.info(f"Persisted conversation with importance: {importance}")
        return result

    def get_weighted_context(self, entity_id: str = "openclaw_agent", max_bytes: int = 20000) -> str:
        """
        Get resonance-weighted context.

        Args:
            entity_id: Entity identifier
            max_bytes: Maximum context size in bytes

        Returns:
            Weighted context
        """
        if not self.protocol:
            raise RuntimeError("Adapter not initialized")

        context = self.protocol.get_weighted_context(entity_id=entity_id, max_bytes=max_bytes)

        logger.info(f"Retrieved {len(context)} bytes of weighted context")
        return context

    def _get_timestamp(self) -> str:
        """
        Get current timestamp in ISO format.

        Returns:
            ISO format timestamp
        """
        from datetime import datetime

        return datetime.now().isoformat()

    def get_stats(self) -> Dict[str, Any]:
        """
        Get adapter statistics.

        Returns:
            Statistics dictionary
        """
        if not self.protocol:
            return {"status": "not_initialized"}

        stats = {
            "status": "initialized",
            "workspace": str(self.workspace_path),
            "protocol_stats": self.protocol.get_stats(),
        }

        return stats


def create_openclaw_adapter(config_path: Optional[Path] = None) -> OpenClawAdapter:
    """
    Create OpenClaw adapter instance.

    Args:
        config_path: Optional configuration path

    Returns:
        OpenClawAdapter instance
    """
    return OpenClawAdapter(config_path)
