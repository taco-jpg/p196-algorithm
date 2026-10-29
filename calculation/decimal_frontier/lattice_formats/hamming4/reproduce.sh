#!/usr/bin/env bash
set -euo pipefail
python3 calculation/decimal_frontier/lattice_formats/hamming4/primary.py
python3 calculation/decimal_frontier/lattice_formats/hamming4/independent.py
