"""
Setup configuration for quranalyze package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="quranalyze",
    version="0.1.0",
    author="quranalyze contributors",
    description="A research-grade framework for Quranic text analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/quranalyze",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "matplotlib>=3.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "mypy>=0.950",
            "pylint>=2.13",
        ],
    },
    entry_points={
        "console_scripts": [
            "quranalyze-example=quranalyze.examples.basic_usage:main",
        ],
    },
    package_data={
        "quranalyze": ["py.typed"],
    },
    include_package_data=True,
)
