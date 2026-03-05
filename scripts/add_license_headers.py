#!/usr/bin/env python3
"""
Add AGPLv3 license headers to Python files.
"""

import os
from pathlib import Path

AGPL_HEADER = '''"""
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
'''


def add_header_to_file(filepath):
    """Add AGPL header to a Python file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if already has a license header
        if "GNU Affero General Public License" in content:
            print(f"✓ {filepath} already has AGPL header")
            return False

        # Check for existing header to replace
        lines = content.split("\n")
        if lines and lines[0].startswith('"""') or lines[0].startswith("'''"):
            # Find end of existing docstring
            end_idx = 0
            for i, line in enumerate(lines[1:], 1):
                if line.strip().endswith('"""') or line.strip().endswith("'''"):
                    end_idx = i
                    break

            if end_idx > 0:
                # Replace existing header
                new_content = AGPL_HEADER + "\n".join(lines[end_idx + 1 :])
            else:
                # Malformed docstring, prepend
                new_content = AGPL_HEADER + content
        else:
            # No existing docstring, prepend
            new_content = AGPL_HEADER + content

        # Write back
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"✓ Added AGPL header to {filepath}")
        return True

    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
        return False


def main():
    """Main function."""
    src_dir = Path("src")

    # Find all Python files
    python_files = list(src_dir.rglob("*.py"))

    print(f"Found {len(python_files)} Python files")
    print("Adding AGPLv3 headers...")

    files_updated = 0
    for py_file in python_files:
        if add_header_to_file(py_file):
            files_updated += 1

    print(f"\nUpdated {files_updated}/{len(python_files)} files")

    # Also update examples
    examples_dir = Path("examples")
    if examples_dir.exists():
        example_files = list(examples_dir.rglob("*.py"))
        for ex_file in example_files:
            add_header_to_file(ex_file)

    print("\n✅ License headers added successfully!")


if __name__ == "__main__":
    main()
