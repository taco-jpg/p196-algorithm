#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
python3 regular_certificate.py
python3 independent_checks.py
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
c++ -std=c++17 -O3 replay196.cpp -o "$TMP/replay196"
"$TMP/replay196" 20000
printf '%s\n' 'AGENT-N07-FOLDED-REGULAR-SAFETY CONTROLS PASSED'
