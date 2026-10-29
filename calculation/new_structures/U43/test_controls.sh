#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
LATTICE="$ROOT/calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt"
BIN="$(mktemp -t u43-simulator.XXXXXX)"
trap 'rm -f "$BIN"' EXIT
g++ -O3 -std=c++17 -Wall -Wextra -Werror "$HERE/simulator.cpp" -o "$BIN"
run_case() {
  local name="$1" J="$2" U="$3" C="$4" widths="$5" steps="$6"
  local out summary
  out="$(python3 "$HERE/crosscheck.py" --simulator "$BIN" --lattice "$LATTICE" \
      --J "$J" --U "$U" --C "$C" --widths "$widths" --steps "$steps" --epoch 120 --gain 5)"
  summary="$(printf '%s\n' "$out" | tail -n 1)"
  grep -q '"summary":"U43_TRACE_CROSSCHECK_PASS"' <<< "$summary"
  printf 'TRACE_CROSSCHECK_PASS fixture=%s widths=%s steps=%s\n' "$name" "$widths" "$steps"
}
run_case phase0-J5 '5' '9,14,4' '10' '20:20,40:40,80:80,160:160' 240
run_case even-centre '6,4' '9,2,16' '12' '20:20,40:40,80:80,160:160' 240
run_case odd-centre '1,8,2' '9,0,18' '4,8,4' '20:20,40:40,80:80,160:160' 240
run_case rotated-U-empty-JC '' '12,6,9' '' '20:40,40:80,80:160,160:320' 240
python3 "$HERE/crosscheck_r30.py" --simulator "$BIN" --lattice "$LATTICE"
printf 'ALL_U43_CONTROLS_PASS\n'
