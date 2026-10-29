#!/bin/sh
set -eu
cd "$(dirname "$0")"
g++ -O3 -std=c++17 replay.cpp -o /tmp/agent-x08-replay
/tmp/agent-x08-replay --family
/tmp/agent-x08-replay --survey
/tmp/agent-x08-replay --audit 1497 100000
/tmp/agent-x08-replay --audit 16999 100000
for n in 1497 16999; do
  cpp_hash=$(/tmp/agent-x08-replay --fulltrace "$n" 20000 | sha256sum | cut -d " " -f 1)
  py_output=$(python3 independent.py "$n" 20000)
  printf "%s\n" "$py_output"
  py_hash=$(printf "%s\n" "$py_output" | sed -n 's/^SHA256(whole-orbit-newline)=\([0-9a-f]*\).*/\1/p')
  [ "$cpp_hash" = "$py_hash" ] || { echo "SHA mismatch for $n" >&2; exit 1; }
  echo "PASS whole-orbit independent SHA-256 seed=$n hash=$cpp_hash"
done
