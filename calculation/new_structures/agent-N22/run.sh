#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
cxx="${CXX:-g++}"
"$cxx" -O3 -std=c++17 -Wall -Wextra -Werror "$here/replay_digits.cpp" -o "$tmp/array"
"$cxx" -O3 -std=c++17 -Wall -Wextra -Werror "$here/replay_gmp.cpp" -lgmpxx -lgmp -o "$tmp/gmp"
"$tmp/array" "$here/rows.csv" "$here/B.csv" 20000 "$tmp/verified" 100
"$tmp/gmp" "$here/rows.csv" "$here/B.csv" 20000 100 "$tmp/verified_checkpoints.txt" | tail -n 4
python3 "$here/replay_bigint.py" --w "$here/rows.csv" --b "$here/B.csv" --checkpoints "$tmp/verified_checkpoints.txt" --steps 100 | tail -n 1
# The centred defect eventually reaches the rooted exterior. This is NOT an infinite certificate.
"$tmp/array" "$here/rows.csv" "$here/B.csv" 50000 "$tmp/diagnose" 100 --until-break 2> "$tmp/break.txt"
grep -q '^B_BREAK phase=6 t=33062 index=10$' "$tmp/break.txt"
cat "$tmp/break.txt"
python3 - <<'PY'
n=89
for i in range(24):
    assert str(n)!=str(n)[::-1]
    n+=int(str(n)[::-1])
assert str(n)==str(n)[::-1] and n==8813200023188
print('Control: decimal 89 first reaches palindrome after 24 steps')
PY
# A corrupted first lattice coefficient must be rejected, not silently accepted.
cp "$here/rows.csv" "$tmp/bad.csv"
sed -i '1s/^4,/5,/' "$tmp/bad.csv"
if "$tmp/array" "$tmp/bad.csv" "$here/B.csv" 20000 "$tmp/bad" 100 > "$tmp/bad.log" 2>&1; then
  echo 'FAIL: malformed lattice row was accepted' >&2; exit 1
fi
echo 'Control: corrupted lattice row rejected'
echo 'ALL N22 REPLAY CHECKS PASSED'
