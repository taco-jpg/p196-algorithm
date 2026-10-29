#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
python3 regular_certificate.py
python3 b9_phase_control.py
printf '%s\n' 'AGENT-N07-BASE9-PHASE-DFA POSITIVE CONTROL PASSED'
