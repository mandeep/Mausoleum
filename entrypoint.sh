#!/bin/bash
set -e

# Optional: create and activate a venv (if using virtualenv)
# python3 -m venv /venv
# source /venv/bin/activate

# Install your project in editable mode
pip install -e .[tests]

# If no arguments passed, run bash. otherwise run given command
if [ $# -eq 0 ]; then
  exec bash
else
  exec "$@"
fi