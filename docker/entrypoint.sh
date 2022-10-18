#!/bin/bash
set -e

# Activate virtual env
. /venv/bin/activate

exec "$@"
