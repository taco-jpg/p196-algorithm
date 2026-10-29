#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
python3 two_track_certificate.py
python3 independent_two_track.py
printf '%s\n' 'AGENT-N07-TWO-TRACK-STRICT-SAFETY ALL CONTROLS PASSED'
