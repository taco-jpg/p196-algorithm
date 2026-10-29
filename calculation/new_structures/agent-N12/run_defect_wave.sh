#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
"${CXX:-g++}" -O3 -std=c++17 "$HERE/seed_cones.cpp" -o "$TMP/digit"
"${CXX:-g++}" -O3 -std=c++17 "$HERE/chunk_bigint_replay.cpp" -o "$TMP/big"
"${CXX:-g++}" -O3 -std=c++17 "$HERE/defect_tracker.cpp" -o "$TMP/diff"
for case in '31000 6e0a9285178df82218b6529e59bef201fa139e1bfc13640a5ef7579fdbce6854' '31001 2ea97b25748ebacfd9d798b01ab884bb9577060dd925adbd197ff7d31c0b6d8a'; do
 read -r GAP HASH <<< "$case"
 "$TMP/digit" 39 "$GAP" 43 60000 0 "$TMP/digits-$GAP.csv"
 "$TMP/big" 39 "$GAP" 43 60000 0 "$TMP/big-$GAP.csv"
 cmp "$TMP/digits-$GAP.csv" "$TMP/big-$GAP.csv"
 ACTUAL="$(sha256sum "$TMP/digits-$GAP.csv" | cut -d' ' -f1)"
 test "$ACTUAL" = "$HASH"
done
"$TMP/diff" 60000 > "$TMP/defect.csv"
python3 - "$TMP/defect.csv" "$HERE/defect_samples.csv" "$TMP/digits-31000.csv" "$TMP/digits-31001.csv" <<'PY'
import csv,sys
rows={int(r['t']):r for r in csv.DictReader(open(sys.argv[1]))}
samples=list(csv.DictReader(open(sys.argv[2])))
for r in samples:
    actual=rows[int(r['t'])]
    for key,value in r.items():
        assert actual[key]==value,(r['t'],key,value,actual[key])
a=list(csv.DictReader(open(sys.argv[3])))
b=list(csv.DictReader(open(sys.argv[4])))
assert len(a)==len(b)==60001
assert all(x['first16pairs']==y['first16pairs'] for x,y in zip(a,b))
assert all(x['mismatch']==y['mismatch'] for x,y in zip(a,b))
assert rows[51464]['mismatch_count']=='0'
assert rows[51465]['mismatch_count']=='2'
assert rows[60000]['mismatch_count']=='5861'
print('POSTCOLLISION_DEFECT_WAVE_60000_PASS')
PY
