#!/usr/bin/env python3
"""
Simple setup script for testing AetherMem installation.
"""

from setuptools import setup, find_packages

setup(
    name="aethermem",
    version="1.0.0",
    description="A high-resilience memory continuity protocol for AI Agents",
    author="AetherMem Authors",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "pydantic>=2.0.0",
        "pyyaml>=6.0",
        "python-dateutil>=2.8.2",
        "filelock>=3.4.0",
    ],
)
