#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
D="$(mktemp -d)";trap 'rm -rf "$D"' EXIT
c++ -std=c++17 -O3 -Wall -Wextra pulse_train.cpp -o "$D/pulse_train"
"$D/pulse_train" 4000 > "$D/pulse_train.tsv" 2> "$D/pulse_train.err"
grep -Fqx 'first_overlap=836 first_nonlinear=841 first_unexpected=858' "$D/pulse_train.err"
python3 pulse_train_check.py "$D/pulse_train.tsv" "$D/keyframes.csv"
diff -u pulse_train_keyframes.csv "$D/keyframes.csv"
python3 pulse_train_independent.py "$D/pulse_train.tsv"
echo 'AGENT_N13_PULSE_TRAIN_INTERFERENCE_PASS'
