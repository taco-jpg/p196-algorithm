#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
"${CXX:-g++}" -O3 -std=c++17 "$HERE/seed_cones.cpp" -o "$TMP/seed_cones"
"${CXX:-g++}" -O3 -std=c++17 "$HERE/gmp_replay.cpp" -lgmpxx -lgmp -o "$TMP/gmp_replay"
python3 "$HERE/test_padding.py"
for case in '39 43 f25735497a6f490165cf06b4f133310f44030b9fcbf9abde7e3200741203d0cb' '71 59 4e3785cb54a57cd893d241caca33c13cca09157c9ff51e08f51b4d21359f3f62'; do
  read -r L R EXPECTED <<< "$case"
  "$TMP/seed_cones" "$L" 12000 "$R" 20000 16 "$TMP/vec.csv"
  "$TMP/gmp_replay" "$L" 12000 "$R" 20000 16 "$TMP/gmp.csv"
  cmp "$TMP/vec.csv" "$TMP/gmp.csv"
  ACTUAL="$(sha256sum "$TMP/vec.csv" | cut -d' ' -f1)"
  test "$ACTUAL" = "$EXPECTED"
  python3 - "$HERE/checkpoints.csv" "$TMP/vec.csv" "$L" "$R" <<'PY'
import csv,sys
expected,generated,L,R=sys.argv[1:]
rows=list(csv.DictReader(open(generated)))
for row in csv.DictReader(open(expected)):
    if row['L']==L and row['R']==R:
        actual=rows[int(row['t'])]
        for k in ('length','width','central_zeros','mismatch'):
            assert actual[k]==row[k],(L,R,row['t'],k)
print('CHECKPOINTS_PASS',L,R)
PY
done
"$TMP/seed_cones" 39 12001 43 20000 17 "$TMP/padded.csv"
"$TMP/seed_cones" 39 12000 43 20000 16 "$TMP/base.csv"
python3 - "$TMP/base.csv" "$TMP/padded.csv" <<'PY'
import csv,sys
A=list(csv.DictReader(open(sys.argv[1])));B=list(csv.DictReader(open(sys.argv[2])))
assert len(A)==len(B)==20001
for a,b in zip(A,B):
    assert int(b['length'])==int(a['length'])+1
    assert int(b['central_zeros'])==int(a['central_zeros'])+1
    for k in ('width','mismatch','first16pairs'):assert a[k]==b[k]
print('CENTRAL_PADDING_20001_STATES_PASS')
PY
if "$TMP/seed_cones" 1 0 1 1 0 "$TMP/pal.csv" >/dev/null 2>&1; then
  echo 'PALINDROME_NEGATIVE_CONTROL_FAILED' >&2; exit 1
fi
echo AGENT_N12_ALL_CHECKS_PASSED
