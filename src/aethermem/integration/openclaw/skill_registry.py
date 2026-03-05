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

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from .adapter import OpenClawAdapter


def register_skill() -> Dict[str, Any]:
    """
    Register AetherMem as an OpenClaw skill.

    Returns:
        Skill registration data
    """
    skill_data = {
        "name": "aethermem",
        "version": "1.0.0",
        "description": "Memory continuity protocol for AI agents",
        "author": "AetherMem Authors",
        "license": "MIT",
        "homepage": "https://github.com/kric030214-web/AetherMem",
        "capabilities": [
            "memory_continuity",
            "context_injection",
            "state_persistence",
            "resonance_weighting",
        ],
        "configuration": {
            "required": [
                "OPENCLAW_WORKSPACE",
            ],
            "optional": [
                "AETHERMEM_CONFIG",
                "AETHERMEM_LOG_LEVEL",
            ],
        },
        "entry_points": {
            "adapter": "aethermem.integration.openclaw.adapter:OpenClawAdapter",
            "create_adapter": "aethermem.integration.openclaw.adapter:create_openclaw_adapter",
        },
        "hooks": {
            "session_start": "inject_session_context",
            "session_end": "persist_conversation",
            "context_request": "get_weighted_context",
        },
    }

    return skill_data


def create_skill_config(workspace_path: Path) -> Dict[str, Any]:
    """
    Create skill configuration for OpenClaw workspace.

    Args:
        workspace_path: Path to OpenClaw workspace

    Returns:
        Skill configuration
    """
    config = {
        "skill": {
            "name": "aethermem",
            "enabled": True,
            "auto_start": True,
            "configuration": {
                "workspace": str(workspace_path),
                "memory_limit": 20000,
                "sync_interval": 300,
            },
        },
        "integration": {
            "memory_injection": {
                "enabled": True,
                "max_chars": 20000,
                "auto_inject": True,
            },
            "state_persistence": {
                "enabled": True,
                "importance_levels": {
                    "critical": {"min_resonance": 0.7},
                    "important": {"min_resonance": 0.4},
                    "routine": {"min_resonance": 0.1},
                },
            },
        },
    }

    return config


def save_skill_config(config: Dict[str, Any], config_path: Path) -> None:
    """
    Save skill configuration to file.

    Args:
        config: Configuration dictionary
        config_path: Path to save configuration
    """
    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Skill configuration saved to: {config_path}")


def install_skill(workspace_path: Optional[Path] = None) -> bool:
    """
    Install AetherMem skill in OpenClaw workspace.

    Args:
        workspace_path: Optional workspace path

    Returns:
        True if installation successful
    """
    try:
        # Detect workspace if not provided
        if not workspace_path:
            workspace_path = _detect_workspace()
            if not workspace_path:
                print("Error: OpenClaw workspace not found")
                return False

        # Create skill directory
        skill_dir = workspace_path / "skills" / "aethermem"
        skill_dir.mkdir(parents=True, exist_ok=True)

        # Create skill configuration
        config = create_skill_config(workspace_path)

        # Save configuration
        config_path = skill_dir / "skill_config.json"
        save_skill_config(config, config_path)

        # Create SKILL.md
        skill_md = skill_dir / "SKILL.md"
        _create_skill_markdown(skill_md)

        print(f"AetherMem skill installed in: {skill_dir}")
        print("Configuration:")
        print(f"  Workspace: {workspace_path}")
        print(f"  Memory Limit: {config['skill']['configuration']['memory_limit']} chars")
        print(f"  Sync Interval: {config['skill']['configuration']['sync_interval']} seconds")

        return True

    except Exception as e:
        print(f"Error installing skill: {e}")
        return False


def _detect_workspace() -> Optional[Path]:
    """
    Detect OpenClaw workspace.

    Returns:
        Workspace path or None
    """
    # Check environment variable
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


def _create_skill_markdown(skill_md_path: Path) -> None:
    """
    Create SKILL.md file for OpenClaw skill.

    Args:
        skill_md_path: Path to SKILL.md file
    """
    content = """# AetherMem Skill

Memory continuity protocol for AI agents.

## Description
AetherMem provides persistent memory continuity across AI agent sessions, eliminating the "fresh start" problem in constrained execution environments.

## Capabilities

### Memory Continuity
- Cross-session context preservation
- Automatic state synchronization
- Configurable memory limits

### Context Injection
- Session-start context restoration
- Resonance-weighted context selection
- Configurable injection thresholds

### State Persistence
- Importance-based archiving
- Temporal decay functions
- Atomic sync operations

## Configuration

### Environment Variables
```bash
export OPENCLAW_WORKSPACE="/path/to/workspace"
export AETHERMEM_CONFIG="/path/to/config.yaml"
export AETHERMEM_LOG_LEVEL="INFO"
```

### Skill Configuration
```json
{
  "skill": {
    "name": "aethermem",
    "enabled": true,
    "auto_start": true,
    "configuration": {
      "workspace": "/path/to/workspace",
      "memory_limit": 20000,
      "sync_interval": 300
    }
  }
}
```

## Usage

### Basic Integration
```python
from aethermem.integration.openclaw import OpenClawAdapter

# Initialize adapter
adapter = OpenClawAdapter()
if adapter.initialize():
    # Inject context at session start
    context = adapter.inject_session_context()
    
    # Persist conversation
    result = adapter.persist_conversation(
        user_message="Hello",
        assistant_response="Hi there!",
        importance=2
    )
    
    # Get weighted context
    weighted_context = adapter.get_weighted_context()
```

### OpenClaw Integration
The skill automatically integrates with OpenClaw runtime:
- Context injection at session start
- Conversation persistence at session end
- Resonance-weighted context retrieval

## Technical Details

### VWL (Virtual Write Layer)
- Filesystem abstraction for constrained environments
- Memory-mapped persistence
- Atomic sync operations

### Resonance Engine
- Temporal decay functions (λ = 0.1/day)
- Weighted indexing based on interaction frequency
- Multi-factor priority scoring

## Support
- Repository: https://github.com/kric030214-web/AetherMem
- Issues: https://github.com/kric030214-web/AetherMem/issues
- Documentation: https://github.com/kric030214-web/AetherMem

## License
MIT License
"""

    with open(skill_md_path, "w") as f:
        f.write(content)

    print(f"SKILL.md created at: {skill_md_path}")
