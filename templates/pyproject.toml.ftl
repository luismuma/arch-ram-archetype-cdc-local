[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "arch-ram-archetype-cdc"
version = "0.0.0"
description = "CDC configuration project"
requires-python = ">=3.12"
readme = "README.md"

dependencies = [
    "PyYAML>=6.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "requests>=2.31",
    "msal>=1.30"
]

[tool.pytest.ini_options]
testpaths = [
    "tests"
]
python_files = [
    "test_*.py"
]
python_functions = [
    "test_*"
]
addopts = "-v"

[tool.setuptools]
include-package-data = true
