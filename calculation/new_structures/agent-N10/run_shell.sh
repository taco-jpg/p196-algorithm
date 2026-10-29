#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 build_phase.py
python3 shell_soundness.py
python3 shell_bigint_control.py
