#!/usr/bin/env python3
"""
Find hardcoded paths in configuration files.
"""

import os
import re
from pathlib import Path


def check_file_for_hardcoded_paths(filepath):
    """Check a file for hardcoded paths."""
    hardcoded_patterns = [
        r"127\.0\.0\.1",
        r"localhost",
        r"/root/",
        r"/home/",
        r"/tmp/",
        r"192\.168\.",
        r"10\.",
        r"172\.(1[6-9]|2[0-9]|3[0-1])\.",
    ]

    issues = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.split("\n")

            for i, line in enumerate(lines, 1):
                # Skip comments
                if line.strip().startswith("#"):
                    continue

                for pattern in hardcoded_patterns:
                    if re.search(pattern, line):
                        issues.append({"line": i, "content": line.strip(), "pattern": pattern})

    except Exception as e:
        print(f"Error reading {filepath}: {e}")

    return issues


def main():
    """Main function."""
    print("Checking for hardcoded paths...")
    print("=" * 60)

    config_files = [
        "config/config.example.yaml",
        "pyproject.toml",
        "README.md",
    ]

    # Also check Python files in src/
    python_files = list(Path("src").rglob("*.py"))

    all_issues = {}

    for config_file in config_files:
        if Path(config_file).exists():
            issues = check_file_for_hardcoded_paths(config_file)
            if issues:
                all_issues[config_file] = issues

    for py_file in python_files:
        issues = check_file_for_hardcoded_paths(py_file)
        if issues:
            all_issues[str(py_file)] = issues

    if all_issues:
        print("Found hardcoded paths:")
        print("-" * 60)

        for filepath, issues in all_issues.items():
            print(f"\n{filepath}:")
            for issue in issues:
                print(f"  Line {issue['line']}: {issue['content'][:50]}...")
                print(f"    Pattern: {issue['pattern']}")
    else:
        print("✓ No hardcoded paths found!")

    print("\n" + "=" * 60)

    # Also check for environment variable usage
    print("\nChecking environment variable usage...")
    print("-" * 60)

    env_var_pattern = r"\$\{([A-Z_]+)\}"
    env_vars_found = set()

    for config_file in config_files:
        if Path(config_file).exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    matches = re.findall(env_var_pattern, content)
                    if matches:
                        env_vars_found.update(matches)
            except Exception as e:
                print(f"Error reading {config_file}: {e}")

    if env_vars_found:
        print("✓ Environment variables found:")
        for var in sorted(env_vars_found):
            print(f"  - {var}")
    else:
        print("✗ No environment variables found in config")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
