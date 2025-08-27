#!/usr/bin/env python3
"""
Setup script for C Struct YAML Generator
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="c-struct-yaml-generator",
    version="1.0.0",
    author="C Struct YAML Generator",
    author_email="your.email@example.com",
    description="A flexible C struct analysis tool that converts C structures into detailed YAML description files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai_parse_structure",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Documentation",
        "Topic :: System :: Hardware",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pycparser>=2.20",
        "PyYAML>=5.1",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=20.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "c-struct-yaml=pycparser_yaml_generator:main",
            "yaml-struct-viewer=yaml_viewer:main",
        ],
    },
    keywords="c struct yaml parser pycparser memory layout bitfield",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ai_parse_structure/issues",
        "Source": "https://github.com/yourusername/ai_parse_structure",
        "Documentation": "https://github.com/yourusername/ai_parse_structure#readme",
    },
)
