from setuptools import find_packages, setup

setup(
    name="projectpruner",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.0.0",
        "rich>=10.0.0",
        "pyyaml>=6.0",
        "typing-extensions>=4.0.0",
    ],
    entry_points={
        "console_scripts": [
            "projectpruner=projectpruner.cli:cli",
        ],
    },
)
