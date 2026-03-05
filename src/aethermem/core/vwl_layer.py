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

# Copyright (c) 2026 AetherMem Authors
# Licensed under the MIT License.
# See LICENSE file for full license terms.
"""
VWL (Virtual Write Layer) - Core memory continuity system.

The VWL layer creates a persistent memory bridge between AI agent sessions,
preventing the "fresh out of the box" problem where agents lose all context
between conversations.
"""

import hashlib
import json
import logging
import os
import shutil
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class VWLLayer:
    """Virtual Write Layer for memory continuity."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the VWL layer.

        Args:
            config: Configuration dictionary with:
                - workspace_path: Path to the workspace directory
                - entity_name: Name of the AI entity (e.g., "assistant")
                - sync_interval: Sync interval in seconds (default: 300)
                - max_virtual_size: Maximum size of virtual memory in bytes
        """
        self.config = config
        self.workspace_path = Path(config.get("workspace_path", "."))
        self.entity_name = config.get("entity_name", "assistant")
        self.sync_interval = config.get("sync_interval", 300)  # 5 minutes
        self.max_virtual_size = config.get("max_virtual_size", 1024 * 1024)  # 1MB

        # VWL directory structure
        self.vwl_base = Path(tempfile.gettempdir()) / "vwl"
        self.vwl_base.mkdir(parents=True, exist_ok=True)

        # Entity-specific VWL directory
        entity_hash = hashlib.md5(self.entity_name.encode()).hexdigest()[:8]
        self.vwl_dir = self.vwl_base / entity_hash
        self.vwl_dir.mkdir(exist_ok=True)

        # Virtual memory file
        self.virtual_memory_file = self.vwl_dir / "virtual_memory.json"

        # Sync tracking
        self.last_sync_time = 0
        self.sync_lock_file = self.vwl_dir / ".sync_lock"

        logger.info(f"VWL layer initialized for entity: {self.entity_name}")
        logger.info(f"VWL directory: {self.vwl_dir}")
        logger.info(f"Workspace path: {self.workspace_path}")

    def initialize_from_actual(self, actual_memory_path: Path) -> bool:
        """
        Initialize VWL from an actual memory file.

        Args:
            actual_memory_path: Path to the actual memory file

        Returns:
            True if initialization successful, False otherwise
        """
        try:
            if not actual_memory_path.exists():
                logger.warning(f"Actual memory file not found: {actual_memory_path}")
                # Create empty virtual memory
                self._create_empty_virtual_memory()
                return True

            # Read actual memory
            with open(actual_memory_path, "r", encoding="utf-8") as f:
                actual_content = f.read()

            # Create virtual memory structure
            virtual_memory = {
                "entity": self.entity_name,
                "source_file": str(actual_memory_path),
                "initialized_at": datetime.now().isoformat(),
                "last_sync": datetime.now().isoformat(),
                "content": actual_content,
                "metadata": {
                    "original_size": len(actual_content),
                    "virtual_size": len(actual_content),
                    "character_count": len(actual_content),
                    "line_count": actual_content.count("\n") + 1,
                },
            }

            # Save virtual memory
            with open(self.virtual_memory_file, "w", encoding="utf-8") as f:
                json.dump(virtual_memory, f, ensure_ascii=False, indent=2)

            logger.info(f"VWL initialized from {actual_memory_path}")
            logger.info(f"Virtual memory size: {len(actual_content)} characters")

            return True

        except Exception as e:
            logger.error(f"Failed to initialize VWL from {actual_memory_path}: {e}")
            return False

    def _create_empty_virtual_memory(self) -> None:
        """Create an empty virtual memory structure."""
        virtual_memory = {
            "entity": self.entity_name,
            "source_file": None,
            "initialized_at": datetime.now().isoformat(),
            "last_sync": datetime.now().isoformat(),
            "content": "",
            "metadata": {
                "original_size": 0,
                "virtual_size": 0,
                "character_count": 0,
                "line_count": 0,
            },
        }

        with open(self.virtual_memory_file, "w", encoding="utf-8") as f:
            json.dump(virtual_memory, f, ensure_ascii=False, indent=2)

        logger.info("Created empty virtual memory")

    def read_virtual_memory(self) -> Optional[Dict[str, Any]]:
        """
        Read the current virtual memory.

        Returns:
            Virtual memory dictionary or None if error
        """
        try:
            if not self.virtual_memory_file.exists():
                logger.warning("Virtual memory file does not exist")
                return None

            with open(self.virtual_memory_file, "r", encoding="utf-8") as f:
                virtual_memory = json.load(f)

            return virtual_memory

        except Exception as e:
            logger.error(f"Failed to read virtual memory: {e}")
            return None

    def write_to_virtual_memory(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Write content to virtual memory.

        Args:
            content: Content to write
            metadata: Optional metadata about the content

        Returns:
            True if write successful, False otherwise
        """
        try:
            virtual_memory = self.read_virtual_memory()
            if virtual_memory is None:
                virtual_memory = {
                    "entity": self.entity_name,
                    "source_file": None,
                    "initialized_at": datetime.now().isoformat(),
                    "last_sync": datetime.now().isoformat(),
                    "content": "",
                    "metadata": {
                        "original_size": 0,
                        "virtual_size": 0,
                        "character_count": 0,
                        "line_count": 0,
                    },
                }

            # Append content
            current_content = virtual_memory.get("content", "")
            new_content = current_content + "\n\n" + content if current_content else content

            # Check size limit
            if len(new_content) > self.max_virtual_size:
                logger.warning(f"Virtual memory size ({len(new_content)}) exceeds limit ({self.max_virtual_size})")
                # Truncate old content
                lines = new_content.split("\n")
                # Keep last 50% of lines
                keep_lines = lines[-len(lines) // 2 :]
                new_content = "\n".join(keep_lines)
                logger.info(f"Truncated virtual memory to {len(new_content)} characters")

            # Update virtual memory
            virtual_memory["content"] = new_content
            virtual_memory["last_sync"] = datetime.now().isoformat()
            virtual_memory["metadata"]["virtual_size"] = len(new_content)
            virtual_memory["metadata"]["character_count"] = len(new_content)
            virtual_memory["metadata"]["line_count"] = new_content.count("\n") + 1

            # Add write metadata
            if metadata:
                if "writes" not in virtual_memory:
                    virtual_memory["writes"] = []
                virtual_memory["writes"].append(
                    {"timestamp": datetime.now().isoformat(), "content_length": len(content), "metadata": metadata}
                )

            # Save virtual memory
            with open(self.virtual_memory_file, "w", encoding="utf-8") as f:
                json.dump(virtual_memory, f, ensure_ascii=False, indent=2)

            logger.info(f"Wrote {len(content)} characters to virtual memory")
            logger.debug(f"Total virtual memory size: {len(new_content)} characters")

            return True

        except Exception as e:
            logger.error(f"Failed to write to virtual memory: {e}")
            return False

    def sync_to_actual(self, actual_memory_path: Path, force: bool = False) -> bool:
        """
        Sync virtual memory to actual file.

        Args:
            actual_memory_path: Path to the actual memory file
            force: Force sync even if not needed

        Returns:
            True if sync successful, False otherwise
        """
        # Check if sync is needed
        current_time = time.time()
        if not force and current_time - self.last_sync_time < self.sync_interval:
            logger.debug(f"Sync not needed, last sync was {current_time - self.last_sync_time:.1f}s ago")
            return True

        # Check for sync lock
        if self.sync_lock_file.exists():
            lock_age = current_time - self.sync_lock_file.stat().st_mtime
            if lock_age < 30:  # 30 second lock timeout
                logger.warning(f"Sync locked, lock age: {lock_age:.1f}s")
                return False

        try:
            # Create sync lock
            self.sync_lock_file.touch()

            # Read virtual memory
            virtual_memory = self.read_virtual_memory()
            if virtual_memory is None:
                logger.error("Cannot sync: virtual memory not found")
                self.sync_lock_file.unlink(missing_ok=True)
                return False

            virtual_content = virtual_memory.get("content", "")
            if not virtual_content:
                logger.warning("Virtual memory is empty, nothing to sync")
                self.sync_lock_file.unlink(missing_ok=True)
                return True

            # Ensure actual file directory exists
            actual_memory_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to actual file
            with open(actual_memory_path, "w", encoding="utf-8") as f:
                f.write(virtual_content)

            # Update sync time
            self.last_sync_time = current_time
            virtual_memory["last_sync"] = datetime.now().isoformat()
            virtual_memory["metadata"]["last_actual_sync"] = datetime.now().isoformat()

            # Save updated virtual memory
            with open(self.virtual_memory_file, "w", encoding="utf-8") as f:
                json.dump(virtual_memory, f, ensure_ascii=False, indent=2)

            logger.info(f"Synced virtual memory to {actual_memory_path}")
            logger.info(f"Synced {len(virtual_content)} characters")

            # Remove sync lock
            self.sync_lock_file.unlink(missing_ok=True)

            return True

        except Exception as e:
            logger.error(f"Failed to sync virtual memory: {e}")
            # Remove sync lock on error
            self.sync_lock_file.unlink(missing_ok=True)
            return False

    def get_virtual_content(self) -> str:
        """
        Get the current virtual content.

        Returns:
            Virtual content as string
        """
        virtual_memory = self.read_virtual_memory()
        if virtual_memory is None:
            return ""

        return virtual_memory.get("content", "")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get VWL layer statistics.

        Returns:
            Dictionary with statistics
        """
        virtual_memory = self.read_virtual_memory()
        if virtual_memory is None:
            return {
                "entity": self.entity_name,
                "status": "not_initialized",
                "virtual_size": 0,
                "character_count": 0,
                "line_count": 0,
                "last_sync": None,
                "sync_interval": self.sync_interval,
            }

        return {
            "entity": self.entity_name,
            "status": "active",
            "virtual_size": virtual_memory["metadata"]["virtual_size"],
            "character_count": virtual_memory["metadata"]["character_count"],
            "line_count": virtual_memory["metadata"]["line_count"],
            "last_sync": virtual_memory["last_sync"],
            "sync_interval": self.sync_interval,
            "vwl_directory": str(self.vwl_dir),
            "workspace_path": str(self.workspace_path),
        }

    def cleanup(self, keep_virtual: bool = True) -> bool:
        """
        Clean up VWL resources.

        Args:
            keep_virtual: Whether to keep virtual memory files

        Returns:
            True if cleanup successful, False otherwise
        """
        try:
            # Remove sync lock if exists
            self.sync_lock_file.unlink(missing_ok=True)

            if not keep_virtual:
                # Remove entire VWL directory
                if self.vwl_dir.exists():
                    shutil.rmtree(self.vwl_dir)
                    logger.info(f"Removed VWL directory: {self.vwl_dir}")

            return True

        except Exception as e:
            logger.error(f"Failed to cleanup VWL: {e}")
            return False


class VWLManager:
    """Manager for multiple VWL layers."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize VWL manager.

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.layers: Dict[str, VWLLayer] = {}
        logger.info("VWL manager initialized")

    def get_layer(self, entity_name: str, workspace_path: Optional[Path] = None) -> VWLLayer:
        """
        Get or create a VWL layer for an entity.

        Args:
            entity_name: Name of the entity
            workspace_path: Optional workspace path override

        Returns:
            VWLLayer instance
        """
        if entity_name in self.layers:
            return self.layers[entity_name]

        # Create layer config
        layer_config = self.config.copy()
        layer_config["entity_name"] = entity_name
        if workspace_path:
            layer_config["workspace_path"] = str(workspace_path)

        # Create new layer
        layer = VWLLayer(layer_config)
        self.layers[entity_name] = layer

        logger.info(f"Created VWL layer for entity: {entity_name}")

        return layer

    def sync_all(self) -> Dict[str, bool]:
        """
        Sync all VWL layers to their actual files.

        Returns:
            Dictionary mapping entity names to sync success status
        """
        results = {}

        for entity_name, layer in self.layers.items():
            # Determine actual file path
            workspace_path = Path(layer.config.get("workspace_path", "."))
            actual_file = workspace_path / "MEMORY.md"

            # Sync
            success = layer.sync_to_actual(actual_file)
            results[entity_name] = success

            if success:
                logger.info(f"Synced VWL layer for {entity_name}")
            else:
                logger.warning(f"Failed to sync VWL layer for {entity_name}")

        return results

    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        Get statistics for all VWL layers.

        Returns:
            Dictionary mapping entity names to statistics
        """
        stats = {}

        for entity_name, layer in self.layers.items():
            stats[entity_name] = layer.get_stats()

        return stats

    def cleanup_all(self, keep_virtual: bool = True) -> Dict[str, bool]:
        """
        Clean up all VWL layers.

        Args:
            keep_virtual: Whether to keep virtual memory files

        Returns:
            Dictionary mapping entity names to cleanup success status
        """
        results = {}

        for entity_name, layer in self.layers.items():
            success = layer.cleanup(keep_virtual)
            results[entity_name] = success

            if success:
                logger.info(f"Cleaned up VWL layer for {entity_name}")
            else:
                logger.warning(f"Failed to cleanup VWL layer for {entity_name}")

        # Clear layers dictionary
        self.layers.clear()

        return results
