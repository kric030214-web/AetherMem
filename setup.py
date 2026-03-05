#!/usr/bin/env python3
"""
Setup script for AetherMem.
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
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: System :: Filesystems",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=["ai", "memory", "continuity", "vwl", "filesystem", "persistence", "agent"],
    entry_points={
        "console_scripts": [
            "aethermem=aethermem.cli:main",
        ],
        "openclaw.skills": [
            "aethermem=aethermem.integration.openclaw:register_skill",
        ],
    },
)
