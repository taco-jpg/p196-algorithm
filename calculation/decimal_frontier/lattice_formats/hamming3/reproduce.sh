#!/usr/bin/env bash
set -euo pipefail
# From repository root. Sequential low-priority single-process complete runs.
ulimit -v 8388608 2>/dev/null || true
nice -n 10 python3 calculation/decimal_frontier/lattice_formats/hamming3/primary.py
nice -n 10 python3 calculation/decimal_frontier/lattice_formats/hamming3/independent.py
