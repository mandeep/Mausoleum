#!/bin/bash
set -e

pip install -q -e .[tests]

# If no arguments passed, run bash. otherwise run given command
if [ $# -eq 0 ]; then
  exec bash
else
  exec "$@"
fi