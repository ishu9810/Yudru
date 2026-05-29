from setuptools import setup, find_packages

setup(
    name="drone_swarm_real",
    version="1.0.0",
    description="Ground control station for 5-drone ArduPilot swarm",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pymavlink>=2.4.41",
        "pyserial>=3.5",
        "PyYAML>=6.0.1",
    ],
    python_requires=">=3.10",
)
