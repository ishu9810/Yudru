from setuptools import find_packages, setup

setup(
    name="drone-swarm-control",
    version="0.1.0",
    description="Python-based control system for 5-drone Betaflight swarm",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=["PyYAML>=6.0", "mavsdk>=2.8.0"],
)
