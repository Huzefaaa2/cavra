#!/usr/bin/env python3
"""
CAVRA - Runtime governance for AI coding agents.

Setup script for PyPI distribution.
See README.md and docs/ for more information.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README for long description
repo_root = Path(__file__).parent.resolve()
long_description = (repo_root / "README.md").read_text(encoding="utf-8")

setup(
    name="cavra",
    version="0.1.0",
    author="Huzefa Husain",
    author_email="huzefa@example.com",
    description="Runtime governance platform for AI coding agents in regulated environments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Huzefaaa2/cavra",
    project_urls={
        "Bug Tracker": "https://github.com/Huzefaaa2/cavra/issues",
        "Documentation": "https://github.com/Huzefaaa2/cavra/tree/main/docs",
        "Source Code": "https://github.com/Huzefaaa2/cavra",
    },
    license="BUSL-1.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "cavra": ["py.typed", "schemas/*.json"],
    },
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        "typer[all]>=0.12",
        "rich>=13.7",
        "PyYAML>=6.0",
        "jsonschema>=4.20",
        "python-dateutil>=2.8",
        "fastapi>=0.110",
        "uvicorn>=0.27",
        "cryptography>=42.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0",
            "httpx>=0.27",
            "ruff>=0.1",
            "black>=23.0",
            "mypy>=1.0",
            "build>=1.0",
            "twine>=5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cavra=cavra.cli:main",
            "cavra-mcp-server=cavra.mcp_server:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
    ],
    keywords="ai governance policy agent claude copilot security terraform",
    zip_safe=False,
)
