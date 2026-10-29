#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 -m py_compile pump_window.py test_ports.py
python3 test_ports.py
