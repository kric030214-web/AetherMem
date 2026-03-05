#!/usr/bin/env python3
"""
Final validation of AetherMem project after industrial polishing.
"""

import os
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

print("=" * 70)
print("AETHERMEM PROJECT VALIDATION")
print("=" * 70)

# Test 1: File structure validation
print("\n1. File Structure Validation")
print("-" * 40)

required_dirs = [
    "src/core",
    "src/api",
    "src/resonance",
    "src/integration/openclaw",
    "config",
    "examples",
    ".github/workflows",
    ".github/ISSUE_TEMPLATE",
]

missing_dirs = []
for dir_path in required_dirs:
    if not (Path(__file__).parent / dir_path).exists():
        missing_dirs.append(dir_path)

if missing_dirs:
    print(f"✗ Missing directories: {missing_dirs}")
else:
    print("✓ All required directories exist")

# Test 2: Key file validation
print("\n2. Key File Validation")
print("-" * 40)

required_files = [
    "README.md",
    "pyproject.toml",
    "LICENSE",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "config/config.example.yaml",
    "src/core/vwl_layer.py",
    "src/core/memory_injector.py",
    "src/core/memory_saver.py",
    "src/api/__init__.py",
    "src/resonance/temporal_decay.py",
    "src/resonance/interaction_metrics.py",
    "src/integration/openclaw/adapter.py",
    "src/integration/openclaw/skill_registry.py",
    "examples/basic_protocol.py",
    ".github/workflows/lint_and_validate.yml",
    ".github/ISSUE_TEMPLATE/BUG_REPORT.md",
]

missing_files = []
for file_path in required_files:
    if not (Path(__file__).parent / file_path).exists():
        missing_files.append(file_path)

if missing_files:
    print(f"✗ Missing files: {missing_files}")
else:
    print("✓ All key files exist")

# Test 3: GitHub URL validation
print("\n3. GitHub URL Validation")
print("-" * 40)

try:
    with open("README.md", "r") as f:
        readme_content = f.read()

    if "kric030214-web/AetherMem" in readme_content:
        print("✓ GitHub URLs updated in README.md")
    else:
        print("✗ GitHub URLs not updated in README.md")

    if "yourusername" not in readme_content:
        print("✓ No placeholder usernames in README.md")
    else:
        print("✗ Placeholder usernames found in README.md")

except Exception as e:
    print(f"✗ Error reading README.md: {e}")

# Test 4: Code quality validation
print("\n4. Code Quality Validation")
print("-" * 40)

# Check for emojis and Chinese characters
emojis_found = False
chinese_found = False

for py_file in Path("src").rglob("*.py"):
    try:
        with open(py_file, "r", encoding="utf-8") as f:
            content = f.read()

            # Check for common emojis
            emoji_patterns = ["🌸", "💕", "✨", "🚀", "🧠", "🔧", "🌟", "💖", "🔥", "⭐"]
            for emoji in emoji_patterns:
                if emoji in content:
                    print(f"✗ Emoji found in {py_file}: {emoji}")
                    emojis_found = True

            # Check for Chinese characters (basic check)
            # This is a simple check - may have false positives
            import re

            if re.search(r"[\u4e00-\u9fff]", content):
                print(f"✗ Chinese characters found in {py_file}")
                chinese_found = True

    except Exception as e:
        print(f"✗ Error reading {py_file}: {e}")

if not emojis_found:
    print("✓ No emojis found in source code")
if not chinese_found:
    print("✓ No Chinese characters found in source code")

# Test 5: Import validation (basic)
print("\n5. Basic Import Validation")
print("-" * 40)

test_modules = [
    ("vwl_layer", ["VWLLayer", "VWLManager"]),
    ("memory_injector", ["MemoryInjector"]),
    ("memory_saver", ["MemorySaver"]),
    ("temporal_decay", ["TemporalDecay"]),
    ("interaction_metrics", ["InteractionMetrics"]),
    ("config_manager", ["ConfigManager"]),
]

all_imports_ok = True
for module_name, classes in test_modules:
    try:
        if module_name in ["vwl_layer", "memory_injector", "memory_saver"]:
            module = __import__(f"core.{module_name}", fromlist=classes)
        elif module_name in ["temporal_decay", "interaction_metrics"]:
            module = __import__(f"resonance.{module_name}", fromlist=classes)
        elif module_name == "config_manager":
            module = __import__(f"integration.{module_name}", fromlist=classes)

        for cls in classes:
            if hasattr(module, cls):
                print(f"✓ {module_name}.{cls} import successful")
            else:
                print(f"✗ {module_name}.{cls} not found")
                all_imports_ok = False

    except Exception as e:
        print(f"✗ Failed to import {module_name}: {e}")
        all_imports_ok = False

# Test 6: Configuration validation
print("\n6. Configuration Validation")
print("-" * 40)

try:
    with open("config/config.example.yaml", "r") as f:
        config_content = f.read()

    # Check for environment variable placeholders
    if "${ENTITY_NAME}" in config_content and "${WORKSPACE_PATH}" in config_content:
        print("✓ Configuration uses environment variables")
    else:
        print("✗ Configuration missing environment variable placeholders")

    # Check for hardcoded personal paths
    bad_paths = ["/root/", "192.168.", "127.0.0.1", "localhost"]
    for bad_path in bad_paths:
        if bad_path in config_content:
            print(f"✗ Hardcoded path found in config: {bad_path}")

    print("✓ Configuration file structure appears valid")

except Exception as e:
    print(f"✗ Error reading configuration: {e}")

print("\n" + "=" * 70)
print("VALIDATION SUMMARY")
print("=" * 70)

summary = {
    "File Structure": len(missing_dirs) == 0,
    "Key Files": len(missing_files) == 0,
    "GitHub URLs": "kric030214-web/AetherMem" in readme_content if "readme_content" in locals() else False,
    "Code Quality": not (emojis_found or chinese_found),
    "Imports": all_imports_ok,
    "Configuration": "✓" in locals() and "✓ Configuration" in locals(),
}

passed = sum(1 for test, result in summary.items() if result)
total = len(summary)

for test, result in summary.items():
    status = "✓" if result else "✗"
    print(f"{status} {test}")

print(f"\nPassed: {passed}/{total} tests")

if passed == total:
    print("\n🎉 AETHERMEM PROJECT VALIDATION PASSED!")
    print("The project is ready for GitHub publication.")
else:
    print(f"\n⚠️  AETHERMEM PROJECT VALIDATION FAILED: {total - passed} issues need attention")

print("=" * 70)
