from setuptools import setup, find_packages

setup(
    name="drone-swarm-control",
    version="1.0.0",
    description="Production-ready Python drone swarm control system for ArduPilot",
    author="Drone Swarm Team",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "pymavlink>=2.4.39",
        "pyserial>=3.5",
        "pyyaml>=6.0",
        "numpy>=1.24.3",
        "pytest>=7.4.0",
        "pytest-asyncio>=0.21.1",
    ],
    entry_points={
        "console_scripts": [
            "drone-swarm-gcs=src.main:main",
        ],
    },
)
