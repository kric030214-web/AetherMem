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

import os
import platform
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional


def get_platform_info() -> Dict[str, Any]:
    """
    Get detailed platform information.

    Returns:
        Dictionary with platform information
    """
    info = {
        "system": platform.system(),  # Windows, Linux, Darwin
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
    }

    # Add platform-specific details
    if info["system"] == "Windows":
        info["platform"] = "windows"
        info["home_dir"] = os.environ.get("USERPROFILE", "")
        info["temp_dir"] = os.environ.get("TEMP", os.environ.get("TMP", ""))

    elif info["system"] == "Darwin":
        info["platform"] = "macos"
        info["home_dir"] = os.environ.get("HOME", "")
        info["temp_dir"] = "/tmp"

    elif info["system"] == "Linux":
        info["platform"] = "linux"
        info["home_dir"] = os.environ.get("HOME", "")
        info["temp_dir"] = "/tmp"

        # Try to detect distribution
        try:
            import distro

            info["distribution"] = distro.name(pretty=True)
            info["distro_id"] = distro.id()
        except ImportError:
            info["distribution"] = "Unknown Linux"
            info["distro_id"] = "unknown"
    else:
        info["platform"] = "unknown"
        info["home_dir"] = os.environ.get("HOME", "")
        info["temp_dir"] = tempfile.gettempdir()

    return info


def get_default_temp_dir() -> str:
    """
    Get platform-appropriate temporary directory.

    Returns:
        Path to temporary directory
    """
    platform_info = get_platform_info()

    if platform_info["platform"] == "windows":
        # Windows temp directory
        temp_base = platform_info.get("temp_dir", "")
        if not temp_base:
            temp_base = os.environ.get("TEMP", os.environ.get("TMP", ""))
        if not temp_base:
            temp_base = "C:\\Windows\\Temp"
        return temp_base

    else:
        # Unix-like systems (Linux, macOS)
        return "/tmp"


def get_default_config_dir() -> Path:
    """
    Get platform-appropriate configuration directory.

    Returns:
        Path to configuration directory
    """
    platform_info = get_platform_info()

    if platform_info["platform"] == "windows":
        # Windows: %APPDATA%\\aethermem
        appdata = os.environ.get("APPDATA", "")
        if appdata:
            return Path(appdata) / "aethermem"
        else:
            return Path.home() / "AppData" / "Roaming" / "aethermem"

    elif platform_info["platform"] == "macos":
        # macOS: ~/Library/Application Support/aethermem
        return Path.home() / "Library" / "Application Support" / "aethermem"

    else:
        # Linux/Unix: ~/.config/aethermem
        return Path.home() / ".config" / "aethermem"


def get_default_workspace_dir() -> Path:
    """
    Get platform-appropriate workspace directory.

    Returns:
        Path to workspace directory
    """
    platform_info = get_platform_info()

    if platform_info["platform"] == "windows":
        # Windows: %USERPROFILE%\\.aethermem
        return Path.home() / ".aethermem"

    else:
        # Unix-like: ~/.aethermem
        return Path.home() / ".aethermem"


def normalize_path(path_str: str) -> Path:
    """
    Normalize path for current platform.

    Args:
        path_str: Path string (may contain environment variables)

    Returns:
        Normalized Path object
    """
    # Expand environment variables
    expanded = os.path.expandvars(path_str)

    # Expand user home directory
    expanded = os.path.expanduser(expanded)

    # Convert to Path and resolve
    path = Path(expanded)

    # Resolve relative paths
    if not path.is_absolute():
        path = Path.cwd() / path

    return path.resolve()


def is_windows() -> bool:
    """Check if running on Windows."""
    return platform.system() == "Windows"


def is_macos() -> bool:
    """Check if running on macOS."""
    return platform.system() == "Darwin"


def is_linux() -> bool:
    """Check if running on Linux."""
    return platform.system() == "Linux"


def get_platform_name() -> str:
    """Get human-readable platform name."""
    system = platform.system()

    if system == "Windows":
        return "windows"
    elif system == "Darwin":
        return "macos"
    elif system == "Linux":
        return "linux"
    else:
        return system.lower()


def validate_platform_compatibility() -> Dict[str, Any]:
    """
    Validate platform compatibility for AetherMem.

    Returns:
        Dictionary with compatibility status and details
    """
    info = get_platform_info()
    compatibility = {
        "platform": info["platform"],
        "python_version": info["python_version"],
        "compatible": True,
        "issues": [],
        "warnings": [],
    }

    # Check Python version
    python_version = tuple(map(int, info["python_version"].split(".")[:2]))
    if python_version < (3, 8):
        compatibility["compatible"] = False
        compatibility["issues"].append(f"Python {info['python_version']} is below minimum requirement 3.8")

    # Platform-specific checks
    if info["platform"] == "windows":
        # Windows specific checks
        if info.get("release", ""):
            try:
                major_version = int(info["release"].split(".")[0])
                if major_version < 10:
                    compatibility["warnings"].append(f"Windows {info['release']} may have limited support")
            except (ValueError, IndexError):
                pass

    elif info["platform"] == "macos":
        # macOS specific checks
        try:
            major_version = int(info["release"].split(".")[0])
            if major_version < 10:
                compatibility["warnings"].append(f"macOS {info['release']} may have limited support")
        except (ValueError, IndexError):
            pass

    elif info["platform"] == "linux":
        # Linux specific checks - generally well supported
        pass

    else:
        compatibility["warnings"].append(f"Platform {info['system']} is not officially tested")

    return compatibility


# Convenience functions
def platform_info() -> Dict[str, Any]:
    """Get platform information (convenience alias)."""
    return get_platform_info()


def check_compatibility() -> bool:
    """Quick compatibility check."""
    result = validate_platform_compatibility()
    return result["compatible"]


# Export public API
__all__ = [
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
]
