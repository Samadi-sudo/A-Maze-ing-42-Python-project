"""Setup script for mazegen package (used by 'python -m build' or pip)."""
from setuptools import setup, find_packages

setup(
    name="mazegen",
    version="1.0.0",
    description="A reusable maze generation module for the A-Maze-ing 42 project",
    long_description=open("README_package.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.10",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)