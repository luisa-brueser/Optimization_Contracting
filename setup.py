from setuptools import setup, find_packages

setup(
    name="pv_optimizer_contracting",
    version="0.1.0",
    author="",
    author_email="",
    package_dir={"": "src"},
    setup_requires=["black", "coloredlogs", "sphinx"],
    tests_require=[],
    description="This package provides a solver model for an electricity supply optimization problem",
    install_requires=[],
)
