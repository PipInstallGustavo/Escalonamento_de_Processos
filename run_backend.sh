#!/usr/bin/env bash

set -e

SCRIPT_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
cd "$SCRIPT_DIR"

VENV_DIR="$SCRIPT_DIR/.venv"
REQ_FILE="$SCRIPT_DIR/requirements.txt"

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR" > /dev/null 2>&1
fi

source "$VENV_DIR/bin/activate"
pip install -q -r "$REQ_FILE"

exec python3 "$SCRIPT_DIR/api.py"
