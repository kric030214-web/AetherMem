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

import yaml

logger = logging.getLogger(__name__)


class ConfigManager:
    """Configuration manager with environment variable interpolation."""

    # Default configuration paths (in order of precedence)
    DEFAULT_PATHS = [
        Path(os.getenv("AETHERMEM_CONFIG", "")),
        Path.home() / ".config" / "aethermem" / "config.yaml",
        Path.cwd() / "aethermem-config.yaml",
        Path(__file__).parent.parent.parent / "config" / "config.example.yaml",
    ]

    # Environment variable mappings
    ENV_MAPPINGS = {
        "AETHERMEM_HOME": "entity.workspace_path",
        "AETHERMEM_ENTITY": "entity.name",
        "AETHERMEM_LOG_LEVEL": "system.log_level",
        "AETHERMEM_DEBUG": "system.debug",
    }

    def __init__(self):
        """Initialize configuration manager."""
        self.config: Dict[str, Any] = {}
        self.config_path: Optional[Path] = None

    def load(self, config_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Load configuration from file with environment variable interpolation.

        Args:
            config_path: Optional explicit config path

        Returns:
            Loaded configuration dictionary
        """
        # Find configuration file
        self.config_path = self._find_config_file(config_path)

        if not self.config_path or not self.config_path.exists():
            logger.warning("No configuration file found, using defaults")
            self.config = self._get_default_config()
        else:
            logger.info(f"Loading configuration from {self.config_path}")
            self.config = self._load_from_file(self.config_path)

        # Apply environment variable overrides
        self._apply_env_overrides()

        # Validate configuration
        self._validate_config()

        logger.info(f"Configuration loaded successfully")
        logger.debug(f"Configuration keys: {list(self.config.keys())}")

        return self.config

    def load_default(self) -> Dict[str, Any]:
        """
        Load default configuration.

        Returns:
            Default configuration dictionary
        """
        return self._get_default_config()

    def _find_config_file(self, explicit_path: Optional[Path]) -> Optional[Path]:
        """
        Find configuration file using precedence order.

        Args:
            explicit_path: Optional explicit path

        Returns:
            Path to configuration file or None
        """
        # Check explicit path first
        if explicit_path and explicit_path.exists():
            return explicit_path

        # Check default paths
        for path in self.DEFAULT_PATHS:
            if path and path.exists():
                return path

        return None

    def _load_from_file(self, config_path: Path) -> Dict[str, Any]:
        """
        Load configuration from YAML file.

        Args:
            config_path: Path to configuration file

        Returns:
            Parsed configuration dictionary
        """
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Perform environment variable substitution
            content = self._substitute_env_vars(content)

            # Parse YAML
            config = yaml.safe_load(content)

            if not isinstance(config, dict):
                raise ValueError("Configuration must be a YAML dictionary")

            return config

        except yaml.YAMLError as e:
            logger.error(f"Failed to parse YAML configuration: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise

    def _substitute_env_vars(self, content: str) -> str:
        """
        Substitute environment variables in configuration content.

        Args:
            content: Configuration content as string

        Returns:
            Content with environment variables substituted
        """
        import re

        def replace_env(match):
            env_var = match.group(1)
            default = match.group(2) if match.group(2) else ""

            # Check if it's a path that should be expanded
            value = os.getenv(env_var, default)

            # Expand user home directory if present
            if value.startswith("~"):
                value = os.path.expanduser(value)

            return value

        # Pattern: ${VAR_NAME} or ${VAR_NAME:default}
        pattern = r"\$\{([A-Za-z0-9_]+)(?::([^}]*))?\}"

        return re.sub(pattern, replace_env, content)

    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides to configuration."""
        for env_var, config_path in self.ENV_MAPPINGS.items():
            env_value = os.getenv(env_var)
            if env_value is not None:
                self._set_nested_value(self.config, config_path, env_value)
                logger.debug(f"Set {config_path} = {env_value} from {env_var}")

    def _set_nested_value(self, config: Dict[str, Any], path: str, value: Any) -> None:
        """
        Set a nested value in configuration dictionary.

        Args:
            config: Configuration dictionary
            path: Dot-separated path (e.g., "entity.workspace_path")
            value: Value to set
        """
        parts = path.split(".")
        current = config

        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]

        last_part = parts[-1]

        # Convert string values to appropriate types
        if isinstance(value, str):
            # Boolean conversion
            if value.lower() in ("true", "false"):
                value = value.lower() == "true"
            # Integer conversion
            elif value.isdigit():
                value = int(value)
            # Float conversion
            elif value.replace(".", "", 1).isdigit():
                value = float(value)

        current[last_part] = value

    def _get_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration.

        Returns:
            Default configuration dictionary
        """
        return {
            "system": {
                "name": "AetherMem",
                "version": "1.0.0",
                "environment": "production",
                "debug": False,
                "log_level": "INFO",
            },
            "entity": {
                "name": os.getenv("AETHERMEM_ENTITY", "assistant"),
                "type": "ai_assistant",
                "workspace_path": os.getenv("AETHERMEM_HOME", str(Path.home() / ".aethermem")),
            },
            "memory": {
                "injection": {
                    "enabled": True,
                    "max_context_chars": 20000,
                    "auto_inject": True,
                },
                "vwl": {
                    "enabled": True,
                    "sync_interval": 300,
                    "max_virtual_size": 1048576,
                },
            },
            "emotional_tracking": {
                "enabled": True,
                "resonance_calculation": "weighted_keyword",
            },
        }

    def _validate_config(self) -> None:
        """Validate configuration structure and values."""
        required_sections = ["system", "entity", "memory"]

        for section in required_sections:
            if section not in self.config:
                logger.warning(f"Missing configuration section: {section}")
                self.config[section] = {}

        # Ensure workspace path exists
        workspace_path = self.config.get("entity", {}).get("workspace_path")
        if workspace_path:
            path = Path(workspace_path)
            if not path.exists():
                logger.info(f"Creating workspace directory: {path}")
                path.mkdir(parents=True, exist_ok=True)

    def validate_config(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Validate configuration structure and values.

        Args:
            config: Optional configuration to validate (uses internal config if None)

        Returns:
            True if configuration is valid
        """
        config_to_validate = config if config is not None else self.config

        # Check required sections
        required_sections = ["system", "entity", "memory"]

        for section in required_sections:
            if section not in config_to_validate:
                logger.error(f"Missing required configuration section: {section}")
                return False

        # Check system section
        system_config = config_to_validate.get("system", {})
        if "name" not in system_config:
            logger.warning("System name not specified in configuration")

        # Check entity section
        entity_config = config_to_validate.get("entity", {})
        if "name" not in entity_config:
            logger.warning("Entity name not specified in configuration")

        # Check memory section
        memory_config = config_to_validate.get("memory", {})
        if "injection" not in memory_config:
            logger.warning("Memory injection configuration missing")

        # Check workspace path
        workspace_path = entity_config.get("workspace_path")
        if not workspace_path:
            logger.warning("Workspace path not specified")
        else:
            try:
                path = Path(workspace_path)
                # Don't create it here, just check if it's a valid path
                if not path.parent.exists():
                    logger.warning(f"Parent directory does not exist: {path.parent}")
            except Exception as e:
                logger.warning(f"Invalid workspace path '{workspace_path}': {e}")

        return True

    def save(self, config: Dict[str, Any], config_path: Optional[Path] = None) -> None:
        """
        Save configuration to file.

        Args:
            config: Configuration dictionary
            config_path: Optional path to save to
        """
        save_path = config_path or self.config_path
        if not save_path:
            save_path = Path.home() / ".config" / "aethermem" / "config.yaml"

        # Ensure directory exists
        save_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(save_path, "w", encoding="utf-8") as f:
                yaml.dump(config, f, default_flow_style=False, indent=2)

            logger.info(f"Configuration saved to {save_path}")

        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            raise

    def get_config_path(self) -> Optional[Path]:
        """
        Get the current configuration file path.

        Returns:
            Configuration file path or None
        """
        return self.config_path
