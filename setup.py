from setuptools import setup, find_packages

setup(
    name="pybitlaunch",
    version="1.1.1",
    description="BitLaunch API Python SDK (with DNS support)",
    author="BitLaunch",
    packages=find_packages(),
    install_requires=["requests>=2.0"],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
)
