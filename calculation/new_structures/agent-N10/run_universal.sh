#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 build_phase.py
python3 symbolic_pump.py
python3 random_pump_control.py
