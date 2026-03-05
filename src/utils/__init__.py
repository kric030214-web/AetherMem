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

from .platform import (
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
