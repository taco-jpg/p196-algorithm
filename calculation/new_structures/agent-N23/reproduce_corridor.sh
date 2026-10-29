#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 decimal_corridor.py /tmp/n23_corridor174.json 50 174
printf '%s  %s\n' '76e9c877fa07b580e31e167d74ea8641eb0e54e443ebe1721337ecf204ac2882' /tmp/n23_corridor174.json | sha256sum -c -
python3 partial_checker.py /tmp/n23_corridor174.json
python3 independent_corridor.py /tmp/n23_corridor174.json
