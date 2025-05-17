#!/bin/bash

# This script executes the complete set of unit tests,
# with code coverage reporting.
# Chris Joakim, 2025

source venv/bin/activate
python --version

rm -rf htmlcov

echo 'executing unit tests with code coverage ...'
pytest -v --cov=src/ --cov-report html tests/
